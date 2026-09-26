import json

from fastapi import HTTPException
from sqlalchemy import MetaData, Table, insert, select, update
from fastapi.responses import StreamingResponse
from typing import Dict, Any


SAFE_COLUMNS = {
    "accounts": [
        "acid",
        "clientid",
        "ledgerid",
        "zid",
        "wardno",
        "propertyno",
        "partno",
        "citysurveyno",
        "plotno",
        "o_onlineno",
        "o_zid",
        "o_wardno",
        "o_propertyno",
        "o_partno",
        "o_citysurveyno",
        "o_plotno",
        "o_usage",
        "o_taxablevalue",
        "o_anualrentalvalue",
        "aadhar_no",
        "CTID",
        "puid",
        "o_totaltax",
        "owner_name",
        "holder_name",
        "wife_name",
        "buildingname",
        "buildingno",
        "address",
        "mobileno",
        "exchange",
        "hastoilet",
        "toiletseats1",
        "toiletseats2",
        "haswaterconnection",
        "totalwaterconnections",
        "hassolarelectricity",
        "hasrainwaterharvesting",
        "hastree",
        "boundry_east",
        "boundry_west",
        "boundry_north",
        "boundry_south",
        "lengthoneast",
        "lengthonwest",
        "lengthonnorth",
        "lengthonsouth",
        "avg_length",
        "avg_breadth",
        "area",
        "opa",
        "gharkul",
        "hasgharkul",
        "treenos",
        "hastenant",
        "hasbore",
        "haswell",
        "tenantname",
        "photopath",
        "mappath",
        "Length",
        "breadth",
        "asmcomplete",
        "oldbuiltuparea",
        "remark1",
        "remark2",
        "hastower",
        "manualratablevalue",
        "manualtax",
        "remarks3",
        "numberingremarks",
        "numberingdone",
        "surveydone",
        "created_at",
        "updated_at",
        "deleted_at",
        "sync_version"
    ],
    "users": [
        "userid",
        "username",
        "mobile",
        "dob",
        "email",
        "loginid",
        "Password",
        "userrole",
        "userlocation",
        "clientid",
        "created_at",
        "updated_at",
        "deleted_at",
        "sync_version"
    ]
}

PRIMARY_KEYS = {
    "accounts": "acid",
    "users": "userid"
}

MAX_SYNC_LINE_BYTES = 1024 * 1024
SYNC_BATCH_SIZE = 500


class SyncService:

    @staticmethod
    def _reflect_table(db, requested_name: str):
        table_name = requested_name.casefold()
        if table_name not in PRIMARY_KEYS:
            raise ValueError(f"Unsupported sync table: {requested_name}")

        return Table(
            table_name,
            MetaData(),
            autoload_with=db.get_bind()
        )

    @staticmethod
    def _normalize_row(table, row: Dict[str, Any]):
        actual_columns = {column.name.casefold(): column.name for column in table.columns}
        normalized = {}
        for name, value in row.items():
            actual_name = actual_columns.get(name.casefold())
            if actual_name is None:
                raise ValueError(f"Unknown column '{name}' for table '{table.name}'")
            if actual_name in normalized:
                raise ValueError(f"Duplicate column name: {name}")
            normalized[actual_name] = value
        return normalized

    @staticmethod
    async def stream_remote_to_local(
        db,
        payload
    ):

        table = SyncService._reflect_table(db, payload.table_name)
        key = table.name
        columns = [table.c[name] for name in SAFE_COLUMNS[key]]
        primary_key = table.c[PRIMARY_KEYS[key]]

        async def generate():
            query = (
                select(*columns)
                .where(
                    ((table.c.updated_at.is_(None)) |
                     (table.c.updated_at > payload.last_sync_time) |
                     (table.c.deleted_at.is_not(None))) &
                    (primary_key > payload.last_id)
                )
                .order_by(primary_key.asc())
            )
            result = db.execute(query)

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
    def upsert_row(db, table, row: Dict[str, Any]):
        table = table if isinstance(table, Table) else SyncService._reflect_table(db, table)
        values = SyncService._normalize_row(table, row)
        primary_key = PRIMARY_KEYS[table.name]
        key_value = values.get(primary_key)

        if key_value is not None:
            key_column = table.c[primary_key]
            exists = db.execute(
                select(key_column).where(key_column == key_value)
            ).first()
            if exists:
                updates = {name: value for name, value in values.items() if name != primary_key}
                if updates:
                    db.execute(
                        update(table)
                        .where(key_column == key_value)
                        .values(updates)
                    )
                return

        db.execute(insert(table).values(values))

    @staticmethod
    def process_local_to_remote(db, payload):
        # payload.tables is a dict: {table_name: [rows]}
        total = 0
        for table, rows in payload.tables.items():
            reflected_table = SyncService._reflect_table(db, table)
            for row in rows:
                SyncService.upsert_row(db, reflected_table, row)
                total += 1
        try:
            db.commit()
        except Exception:
            db.rollback()
            raise

        return {"status": "ok", "rows": total}

    @staticmethod
    async def process_local_to_remote_stream(db, request, table_name: str):
        try:
            table = SyncService._reflect_table(db, table_name)
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc

        buffer = bytearray()
        line_number = 0
        pending_rows = 0
        committed_rows = 0

        def process_line(line: bytes):
            nonlocal line_number, pending_rows
            line_number += 1
            if len(line) > MAX_SYNC_LINE_BYTES:
                raise HTTPException(
                    status_code=413,
                    detail=f"NDJSON line {line_number} exceeds the 1 MiB limit",
                )

            if not line.strip():
                return

            try:
                row = json.loads(line.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as exc:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid NDJSON on line {line_number}",
                ) from exc

            if not isinstance(row, dict):
                raise HTTPException(
                    status_code=400,
                    detail=f"NDJSON line {line_number} must contain a JSON object",
                )

            try:
                SyncService.upsert_row(db, table, row)
            except ValueError as exc:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid row on line {line_number}: {exc}",
                ) from exc
            pending_rows += 1

        try:
            async for chunk in request.stream():
                buffer.extend(chunk)
                print(f"Received chunk: {chunk}")

                while True:
                    newline = buffer.find(b"\n")
                    if newline < 0:
                        if len(buffer) > MAX_SYNC_LINE_BYTES:
                            raise HTTPException(
                                status_code=413,
                                detail="NDJSON line exceeds the 1 MiB limit",
                            )
                        break

                    line = bytes(buffer[:newline]).rstrip(b"\r")
                    del buffer[:newline + 1]
                    process_line(line)

                    if pending_rows >= SYNC_BATCH_SIZE:
                        try:
                            db.commit()
                        except Exception as exc:
                            db.rollback()
                            raise HTTPException(
                                status_code=500,
                                detail={
                                    "message": "Database write failed",
                                    "committed_rows": committed_rows,
                                },
                            ) from exc
                        committed_rows += pending_rows
                        pending_rows = 0

            if buffer:
                process_line(bytes(buffer).rstrip(b"\r"))

            if pending_rows:
                try:
                    db.commit()
                except Exception as exc:
                    db.rollback()
                    raise HTTPException(
                        status_code=500,
                        detail={
                            "message": "Database write failed",
                            "committed_rows": committed_rows,
                        },
                    ) from exc
                committed_rows += pending_rows

            return {"status": "ok", "rows": committed_rows}
        except HTTPException as exc:
            db.rollback()
            detail = exc.detail
            if committed_rows:
                if not isinstance(detail, dict):
                    detail = {"message": detail}
                detail["committed_rows"] = committed_rows
                raise HTTPException(
                    status_code=exc.status_code,
                    detail=detail,
                ) from exc
            raise
        except BaseException:
            db.rollback()
            raise

    @staticmethod
    def get_primary_key(table):
        table_name = table.name if isinstance(table, Table) else table.casefold()
        try:
            return PRIMARY_KEYS[table_name]
        except KeyError as exc:
            raise ValueError(f"Unsupported sync table: {table_name}") from exc