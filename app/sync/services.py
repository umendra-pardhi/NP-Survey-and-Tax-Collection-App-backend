import json
from datetime import date, datetime
from typing import Any, Dict

from fastapi import HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy import Date, DateTime, MetaData, Table, bindparam, insert, select, update


SAFE_COLUMNS = {
    "accounts": [
        "ACID",
        "ClientID",
        "LedgerID",
        "ZID",
        "WardNo",
        "PropertyNo",
        "PartNo",
        "CitySurveyNo",
        "PlotNo",
        "O_OnlineNo",
        "O_ZID",
        "O_WardNo",
        "O_PropertyNo",
        "O_PartNo",
        "O_CitySurveyNo",
        "O_PlotNo",
        "Aadhar_No",
        "CTID",
        "PUID",
        "O_TotalTax",
        "Owner_Name",
        "Holder_Name",
        "Wife_Name",
        "BuildingName",
        "BuildingNo",
        "Address",
        "MobileNo",
        "Exchange",
        "HasToilet",
        "ToiletSeats1",
        "ToiletSeats2",
        "HasWaterConnection",
        "TotalWaterConnections",
        "HasSolarElectricity",
        "HasRainWaterHarvesting",
        "HasTree",
        "Boundry_East",
        "Boundry_West",
        "Boundry_North",
        "Boundry_South",
        "LengthOnEast",
        "LengthOnWest",
        "LengthOnNorth",
        "LengthOnSouth",
        "Avg_Length",
        "Avg_Breadth",
        "Area",
        "OPA",
        "Gharkul",
        "HasGharkul",
        "TreeNos",
        "HasTenant",
        "HasBore",
        "HasWell",
        "TenantName",
        "PhotoPath",
        "MapPath",
        "Length",
        "Breadth",
        "AsmComplete",
        "oldbuiltuparea",
        "Remark1",
        "Remark2",
        "HasTower",
        "ManualRatableValue",
        "ManualTax",
        "Remarks3",
        "PropertyKNRNo",
        "WaterKNRNo",
        "numberingremarks",
        "numberingdone",
        "surveydone",
        "created_at",
        "updated_at",
        "deleted_at",
        "sync_version"
    ],
    "accountsphotos": [
        "ImageId",
        "ACID",
        "FileName",
        "MimeType",
        "ImagePath",
        "created_at",
        "updated_at",
        "deleted_at",
        "sync_version"
    ],
    "users": [
        "UserID",
        "UserName",
        "Mobile",
        "DOB",
        "EMail",
        "LoginID",
        "Password",
        "UserRole",
        "UserLocation",
        "ClientID",
        "created_at",
        "updated_at",
        "deleted_at",
        "sync_version"
    ]
}

PRIMARY_KEYS = {
    "accounts": "ACID",
    "accountsphotos": "ImageId",
    "users": "UserID"
}

TABLE_NAMES = {
    "accounts": "Accounts",
    "accountsphotos": "AccountsPhotos",
    "users": "Users",
}

MAX_SYNC_LINE_BYTES = 1024 * 1024
SYNC_BATCH_SIZE = 500


class SyncService:

    @staticmethod
    def _reflect_table(db, requested_name: str):
        table_name = requested_name.casefold()
        if table_name.startswith("dbo."):
            table_name = table_name[4:]
        if table_name not in PRIMARY_KEYS:
            raise ValueError(f"Unsupported sync table: {requested_name}")

        return Table(
            TABLE_NAMES[table_name],
            MetaData(),
            schema="dbo",
            autoload_with=db.get_bind()
        )

    @staticmethod
    def _coerce_value_for_column(column, value):
        if value is None:
            return None

        if isinstance(value, (datetime, date)):
            return value

        if not isinstance(value, str):
            return value

        if isinstance(column.type, DateTime):
            text = value.strip()
            if text.endswith("Z"):
                text = text[:-1] + "+00:00"
            return datetime.fromisoformat(text)

        if isinstance(column.type, Date):
            return date.fromisoformat(value.strip())

        if column.name == "Password":
            return value.encode("utf-8")

        return value

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
            column = table.columns[actual_name]
            value = SyncService._coerce_value_for_column(column, value)
            normalized[actual_name] = value
        return normalized

    @staticmethod
    async def stream_remote_to_local(
        db,
        payload
    ):

        table = SyncService._reflect_table(db, payload.table_name)
        key = table.name.casefold()
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
                        default=lambda value: (
                            value.decode("utf-8")
                            if isinstance(value, bytes)
                            else str(value)
                        )
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
        primary_key = PRIMARY_KEYS[table.name.casefold()]
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
    def upsert_rows(db, table, rows):
        if not rows:
            return

        primary_key = PRIMARY_KEYS[table.name.casefold()]
        key_column = table.c[primary_key]
        keyed_rows = {}
        keyless_rows = []

        for row in rows:
            key_value = row.get(primary_key)
            if key_value is None:
                keyless_rows.append(row)
            else:
                keyed_rows.setdefault(key_value, {}).update(row)

        keys = list(keyed_rows)
        existing_keys = set()
        for offset in range(0, len(keys), SYNC_BATCH_SIZE):
            existing_keys.update(
                db.execute(
                    select(key_column).where(
                        key_column.in_(keys[offset:offset + SYNC_BATCH_SIZE])
                    )
                ).scalars()
            )

        insert_groups = {}
        for row in keyless_rows:
            insert_groups.setdefault(tuple(sorted(row)), []).append(row)
        update_groups = {}

        for key_value, row in keyed_rows.items():
            if key_value not in existing_keys:
                insert_groups.setdefault(tuple(sorted(row)), []).append(row)
                continue

            values = {name: value for name, value in row.items() if name != primary_key}
            if values:
                update_groups.setdefault(tuple(sorted(values)), []).append(
                    (key_value, values)
                )

        for column_names, grouped_rows in insert_groups.items():
            db.execute(insert(table), grouped_rows)

        for column_names, grouped_rows in update_groups.items():
            parameters = {
                name: f"_sync_value_{index}"
                for index, name in enumerate(column_names)
            }
            statement = (
                update(table)
                .where(key_column == bindparam("_sync_key"))
                .values({name: bindparam(parameter) for name, parameter in parameters.items()})
            )
            mappings = [
                {
                    "_sync_key": key_value,
                    **{parameters[name]: value for name, value in values.items()},
                }
                for key_value, values in grouped_rows
            ]
            db.execute(statement, mappings)

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
        pending_rows = []
        committed_rows = 0

        def commit_pending_rows():
            nonlocal committed_rows
            if not pending_rows:
                return

            row_count = len(pending_rows)
            try:
                SyncService.upsert_rows(db, table, pending_rows)
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
            committed_rows += row_count
            pending_rows.clear()

        def process_line(line: bytes):
            nonlocal line_number
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
                normalized_row = SyncService._normalize_row(table, row)
            except ValueError as exc:
                raise HTTPException(
                    status_code=400,
                    detail=f"Invalid row on line {line_number}: {exc}",
                ) from exc
            pending_rows.append(normalized_row)

        try:
            async for chunk in request.stream():
                buffer.extend(chunk)
                # print(f"Received chunk: {chunk}")

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

                    if len(pending_rows) >= SYNC_BATCH_SIZE:
                        commit_pending_rows()

            if buffer:
                process_line(bytes(buffer).rstrip(b"\r"))

            commit_pending_rows()

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