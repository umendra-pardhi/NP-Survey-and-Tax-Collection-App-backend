import json
import unittest
from datetime import datetime
from unittest.mock import patch

from fastapi import HTTPException
from sqlalchemy import Column, DateTime, Integer, MetaData, String, Table, create_engine, event
from sqlalchemy.orm import Session

from app.sync.services import MAX_SYNC_LINE_BYTES, SyncService


class FakeDatabase:
    def __init__(self):
        self.commits = 0
        self.rollbacks = 0

    def commit(self):
        self.commits += 1

    def rollback(self):
        self.rollbacks += 1


class FakeRequest:
    def __init__(self, chunks):
        self.chunks = chunks

    async def stream(self):
        for chunk in self.chunks:
            yield chunk


class LocalToRemoteStreamTests(unittest.IsolatedAsyncioTestCase):
    async def test_handles_utf8_and_json_split_across_chunks(self):
        rows = []
        db = FakeDatabase()
        chunks = [b'{"name":"Jos\xc3', b'\xa9"}\n{"name":"Ana"}']

        with patch.object(SyncService, "_reflect_table", return_value=object()), \
                patch.object(SyncService, "_normalize_row", side_effect=lambda _table, row: row), \
                patch.object(
                    SyncService,
                    "upsert_rows",
                    side_effect=lambda _db, _table, batch: rows.extend(batch),
                ):
            result = await SyncService.process_local_to_remote_stream(
                db,
                FakeRequest(chunks),
                "accounts",
            )

        self.assertEqual(result, {"status": "ok", "rows": 2})
        self.assertEqual(rows, [{"name": "Jos\u00e9"}, {"name": "Ana"}])
        self.assertEqual(db.commits, 1)

    async def test_malformed_line_rolls_back_pending_rows(self):
        db = FakeDatabase()

        with patch.object(SyncService, "_reflect_table", return_value=object()), \
            patch.object(SyncService, "_normalize_row", side_effect=lambda _table, row: row), \
            patch.object(SyncService, "upsert_rows"):
            with self.assertRaises(HTTPException) as raised:
                await SyncService.process_local_to_remote_stream(
                    db,
                    FakeRequest([b'{"id":1}\nnot-json\n']),
                    "accounts",
                )

        self.assertEqual(raised.exception.status_code, 400)
        self.assertEqual(db.commits, 0)
        self.assertEqual(db.rollbacks, 1)

    async def test_commits_rows_in_bounded_batches(self):
        db = FakeDatabase()
        payload = b"".join(
            (json.dumps({"id": row_id}) + "\n").encode("utf-8")
            for row_id in range(501)
        )

        with patch.object(SyncService, "_reflect_table", return_value=object()), \
            patch.object(SyncService, "_normalize_row", side_effect=lambda _table, row: row), \
            patch.object(SyncService, "upsert_rows"):
            result = await SyncService.process_local_to_remote_stream(
                db,
                FakeRequest([payload]),
                "accounts",
            )

        self.assertEqual(result, {"status": "ok", "rows": 501})
        self.assertEqual(db.commits, 2)

    async def test_reports_rows_committed_before_later_input_error(self):
        db = FakeDatabase()
        payload = b"".join(
            (json.dumps({"id": row_id}) + "\n").encode("utf-8")
            for row_id in range(500)
        ) + b"not-json\n"

        with patch.object(SyncService, "_reflect_table", return_value=object()), \
            patch.object(SyncService, "_normalize_row", side_effect=lambda _table, row: row), \
            patch.object(SyncService, "upsert_rows"):
            with self.assertRaises(HTTPException) as raised:
                await SyncService.process_local_to_remote_stream(
                    db,
                    FakeRequest([payload]),
                    "accounts",
                )

        self.assertEqual(raised.exception.status_code, 400)
        self.assertEqual(raised.exception.detail["committed_rows"], 500)
        self.assertEqual(db.commits, 1)

    async def test_rejects_oversized_line(self):
        db = FakeDatabase()

        with patch.object(SyncService, "_reflect_table", return_value=object()):
            with self.assertRaises(HTTPException) as raised:
                await SyncService.process_local_to_remote_stream(
                    db,
                    FakeRequest([b"x" * (MAX_SYNC_LINE_BYTES + 1)]),
                    "accounts",
                )

        self.assertEqual(raised.exception.status_code, 413)
        self.assertEqual(db.rollbacks, 1)

    def test_normalizes_iso_datetime_strings_for_sql_server_columns(self):
        metadata = MetaData()
        table = Table(
            "Accounts",
            metadata,
            Column("ACID", Integer, primary_key=True),
            Column("created_at", DateTime),
            Column("updated_at", DateTime),
            Column("deleted_at", DateTime),
        )

        normalized = SyncService._normalize_row(
            table,
            {
                "ACID": 2,
                "created_at": "2026-09-28 00:23:18.343000",
                "updated_at": "2026-09-27T20:42:57.201Z",
                "deleted_at": None,
            },
        )

        self.assertIsInstance(normalized["created_at"], datetime)
        self.assertIsInstance(normalized["updated_at"], datetime)
        self.assertIsNone(normalized["deleted_at"])
        self.assertEqual(normalized["created_at"].microsecond, 343000)
        self.assertEqual(normalized["updated_at"].tzinfo.utcoffset(normalized["updated_at"]).total_seconds(), 0)

    def test_batch_upserts_group_inserts_and_updates(self):
        engine = create_engine("sqlite:///:memory:")
        metadata = MetaData()
        table = Table(
            "Accounts",
            metadata,
            Column("ACID", Integer, primary_key=True),
            Column("Owner_Name", String),
            Column("Address", String),
        )
        metadata.create_all(engine)
        executions = []

        def record_execution(_connection, _cursor, statement, _parameters, _context, executemany):
            executions.append((statement.lstrip().split(None, 1)[0].upper(), executemany))

        with Session(engine) as db:
            db.execute(
                table.insert(),
                [
                    {"ACID": 1, "Owner_Name": "Old", "Address": "Keep"},
                    {"ACID": 4, "Owner_Name": "Also old", "Address": "Keep"},
                    {"ACID": 5, "Owner_Name": "Yet another old", "Address": "Keep"},
                ],
            )
            db.commit()

            event.listen(engine, "before_cursor_execute", record_execution)
            try:
                SyncService.upsert_rows(
                    db,
                    table,
                    [
                        {"ACID": 1, "Owner_Name": "First"},
                        {"ACID": 1, "Address": "Updated"},
                        {"ACID": 4, "Owner_Name": "Four"},
                        {"ACID": 5, "Owner_Name": "Five"},
                        {"ACID": 2, "Owner_Name": "New"},
                        {"ACID": 3, "Owner_Name": "Also new"},
                    ],
                )
                db.commit()
            finally:
                event.remove(engine, "before_cursor_execute", record_execution)

            results = db.execute(table.select().order_by(table.c.ACID)).mappings().all()

        self.assertEqual(
            [dict(row) for row in results],
            [
                {"ACID": 1, "Owner_Name": "First", "Address": "Updated"},
                {"ACID": 2, "Owner_Name": "New", "Address": None},
                {"ACID": 3, "Owner_Name": "Also new", "Address": None},
                {"ACID": 4, "Owner_Name": "Four", "Address": "Keep"},
                {"ACID": 5, "Owner_Name": "Five", "Address": "Keep"},
            ],
        )
        self.assertEqual(
            [operation for operation, executemany in executions if operation in {"INSERT", "UPDATE"} and executemany],
            ["INSERT", "UPDATE"],
        )


if __name__ == "__main__":
    unittest.main()