import json
import unittest
from unittest.mock import patch

from fastapi import HTTPException

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
                patch.object(
                    SyncService,
                    "upsert_row",
                    side_effect=lambda _db, _table, row: rows.append(row),
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
                patch.object(SyncService, "upsert_row"):
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
                patch.object(SyncService, "upsert_row"):
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
                patch.object(SyncService, "upsert_row"):
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


if __name__ == "__main__":
    unittest.main()