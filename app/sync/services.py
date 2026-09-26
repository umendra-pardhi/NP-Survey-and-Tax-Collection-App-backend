import json

from sqlalchemy import text
from fastapi.responses import StreamingResponse
from typing import Dict, Any
import re


SAFE_COLUMNS = {
    "Accounts": [
        "ACID",
        "Owner_Name",
        "MobileNo",
        "Address",
        "updated_at",
        "deleted_at",
        "sync_version"
    ],
    "Users": [
        "userid",
        "username",
        "email",
        "updated_at",
        "deleted_at",
        "sync_version"
    ]
}


class SyncService:

    @staticmethod
    async def stream_remote_to_local(
        db,
        payload
    ):

        table = payload.table_name

        columns = SAFE_COLUMNS[table]

        column_string = ", ".join(columns)

        async def generate():

            query = text(f"""
                SELECT {column_string}
                FROM {table}
                WHERE (
                updated_at IS NULL OR
                        updated_at > :last_sync
                     OR deleted_at IS NOT NULL
                )
                AND {SyncService.get_primary_key(table)} > :last_id
                ORDER BY {SyncService.get_primary_key(table)} ASC
            """)

            result = db.execute(query, {
               
                "last_sync": payload.last_sync_time,
                "last_id": payload.last_id
            })

            for row in result.mappings():

                yield (
                    json.dumps(
                        dict(row),
                        default=str
                    ) + "\n"
                )

        return StreamingResponse(
            generate(),
            media_type="application/x-ndjson"
        )

    @staticmethod
    def _sanitize_column(name: str) -> str:
        # allow only letters, numbers and underscore in column names
        if re.match(r"^[A-Za-z0-9_]+$", name):
            return name
        raise ValueError("Invalid column name")

    @staticmethod
    def _get_columns_and_params(row: Dict[str, Any]):
        cols = []
        params = {}
        for k, v in row.items():
            col = SyncService._sanitize_column(k)
            cols.append(col)
            params[col] = v
        return cols, params

    @staticmethod
    def upsert_row(db, table: str, row: Dict[str, Any]):
        pk = SyncService.get_primary_key(table)

        cols, params = SyncService._get_columns_and_params(row)

        if pk in params and params.get(pk) is not None:
            # check existence
            exists_q = text(f"SELECT 1 FROM {table} WHERE {pk} = :pk")
            res = db.execute(exists_q, {"pk": params[pk]}).fetchone()

            if res:
                # perform update
                set_parts = []
                upd_params = {"pk": params[pk]}
                for c in cols:
                    if c == pk:
                        continue
                    set_parts.append(f"{c} = :{c}")
                    upd_params[c] = params[c]

                if set_parts:
                    upd_q = text(f"UPDATE {table} SET {', '.join(set_parts)} WHERE {pk} = :pk")
                    db.execute(upd_q, upd_params)
                return

        # insert
        insert_cols = ", ".join(cols)
        insert_vals = ", ".join([f":{c}" for c in cols])
        ins_q = text(f"INSERT INTO {table} ({insert_cols}) VALUES ({insert_vals})")
        db.execute(ins_q, params)

    @staticmethod
    def process_local_to_remote(db, payload):
        # payload.tables is a dict: {table_name: [rows]}
        total = 0
        for table, rows in payload.tables.items():
            for row in rows:
                SyncService.upsert_row(db, table, row)
                total += 1
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        return {"status": "ok", "rows": total}

    @staticmethod
    async def process_local_to_remote_stream(db, request, table_name: str):
        # Expect NDJSON: one JSON object per line
        buffer = ""
        count = 0

        async for chunk in request.stream():
            text_chunk = chunk.decode("utf-8")
            buffer += text_chunk

            while "\n" in buffer:
                line, buffer = buffer.split("\n", 1)
                line = line.strip()
                if not line:
                    continue
                obj = json.loads(line)
                SyncService.upsert_row(db, table_name, obj)
                count += 1

                # commit in batches
                if count % 500 == 0:
                    try:
                        db.commit()
                    except Exception:
                        db.rollback()
                        raise

        # leftover
        if buffer.strip():
            obj = json.loads(buffer.strip())
            SyncService.upsert_row(db, table_name, obj)
            count += 1

        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        return {"status": "ok", "rows": count}

    @staticmethod
    def get_primary_key(table):

        mapping = {
            "Accounts": "ACID",
            "Users": "UserID"
        }

        return mapping[table]