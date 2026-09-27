import os
import sqlite3
import threading
import uuid
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel, Field


router = APIRouter(prefix="/api/v1/photos", tags=["photos"])

UPLOAD_ROOT = Path(
    os.getenv("PHOTO_UPLOAD_ROOT", "uploads/properties-photos")
).resolve()
MAX_BATCH_FILES = 5000
MAX_FILE_SIZE = 25 * 1024 * 1024
CHUNK_SIZE = 1024 * 1024
ALLOWED_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}
_SCHEMA_LOCK = threading.Lock()
_INITIALIZED_ROOTS = set()


class CreatePhotoBatchRequest(BaseModel):
    expected_files: int | None = Field(default=None, ge=1, le=MAX_BATCH_FILES)


def _database_path() -> Path:
    UPLOAD_ROOT.mkdir(parents=True, exist_ok=True)
    return UPLOAD_ROOT / ".photo_uploads.sqlite3"


def _connect() -> sqlite3.Connection:
    database_path = _database_path()
    root_key = str(database_path)

    with _SCHEMA_LOCK:
        if root_key not in _INITIALIZED_ROOTS:
            connection = sqlite3.connect(database_path, timeout=30)
            try:
                connection.executescript(
                    """
                    CREATE TABLE IF NOT EXISTS photo_batches (
                        batch_id TEXT PRIMARY KEY,
                        status TEXT NOT NULL CHECK (status IN ('open', 'completed')),
                        expected_files INTEGER,
                        created_at TEXT NOT NULL,
                        completed_at TEXT
                    );
                    CREATE TABLE IF NOT EXISTS photo_files (
                        file_id TEXT PRIMARY KEY,
                        batch_id TEXT NOT NULL REFERENCES photo_batches(batch_id),
                        filename TEXT NOT NULL,
                        mime_type TEXT NOT NULL,
                        relative_path TEXT NOT NULL,
                        size_bytes INTEGER NOT NULL DEFAULT 0,
                        status TEXT NOT NULL CHECK (status IN ('uploading', 'uploaded')),
                        created_at TEXT NOT NULL
                    );
                    CREATE INDEX IF NOT EXISTS ix_photo_files_batch_status
                        ON photo_files(batch_id, status);
                    """
                )
            finally:
                connection.close()
            _INITIALIZED_ROOTS.add(root_key)

    connection = sqlite3.connect(database_path, timeout=30)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


@contextmanager
def _database_connection():
    connection = _connect()
    try:
        yield connection
        connection.commit()
    except Exception:
        connection.rollback()
        raise
    finally:
        connection.close()


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _get_batch(connection: sqlite3.Connection, batch_id: str):
    batch = connection.execute(
        "SELECT * FROM photo_batches WHERE batch_id = ?", (batch_id,)
    ).fetchone()
    if batch is None:
        raise HTTPException(status_code=404, detail="Photo batch not found")
    return batch


@router.post("/batches", status_code=201)
def create_photo_batch(payload: CreatePhotoBatchRequest | None = None):
    batch_id = str(uuid.uuid4())
    created_at = _now()
    with _database_connection() as connection:
        connection.execute(
            """INSERT INTO photo_batches
               (batch_id, status, expected_files, created_at)
               VALUES (?, 'open', ?, ?)""",
            (batch_id, payload.expected_files if payload else None, created_at),
        )
    return {
        "batch_id": batch_id,
        "status": "open",
        "expected_files": payload.expected_files if payload else None,
        "created_at": created_at,
    }


@router.post("/batches/{batch_id}/files", status_code=201)
def upload_photo(batch_id: str, file: UploadFile = File(...)):
    filename = Path((file.filename or "").replace("\\", "/")).name
    extension = Path(filename).suffix.lower()
    mime_type = file.content_type or "application/octet-stream"
    if extension not in ALLOWED_EXTENSIONS or not (
        mime_type.startswith("image/") or mime_type == "application/octet-stream"
    ):
        raise HTTPException(status_code=415, detail="Unsupported photo type")

    file_id = str(uuid.uuid4())
    relative_path = f"{file_id}{extension}"
    target_directory = UPLOAD_ROOT
    target_path = target_directory / f"{file_id}{extension}"
    temporary_path = target_directory / f".{file_id}.part"
    created_at = _now()

    with _database_connection() as connection:
        connection.execute("BEGIN IMMEDIATE")
        batch = _get_batch(connection, batch_id)
        if batch["status"] != "open":
            raise HTTPException(status_code=409, detail="Photo batch is complete")

        count = connection.execute(
            "SELECT COUNT(*) FROM photo_files WHERE batch_id = ?", (batch_id,)
        ).fetchone()[0]
        if count >= MAX_BATCH_FILES:
            raise HTTPException(status_code=409, detail="Photo batch limit reached")
        if batch["expected_files"] is not None and count >= batch["expected_files"]:
            raise HTTPException(status_code=409, detail="Expected photo count reached")

        connection.execute(
            """INSERT INTO photo_files
               (file_id, batch_id, filename, mime_type, relative_path,
                size_bytes, status, created_at)
               VALUES (?, ?, ?, ?, ?, 0, 'uploading', ?)""",
            (file_id, batch_id, filename, mime_type, relative_path, created_at),
        )

    size_bytes = 0
    try:
        target_directory.mkdir(parents=True, exist_ok=True)
        with temporary_path.open("xb") as destination:
            while chunk := file.file.read(CHUNK_SIZE):
                size_bytes += len(chunk)
                if size_bytes > MAX_FILE_SIZE:
                    raise HTTPException(
                        status_code=413,
                        detail="Photo exceeds the 25 MB file size limit",
                    )
                destination.write(chunk)

        if size_bytes == 0:
            raise HTTPException(status_code=400, detail="Photo file is empty")

        os.replace(temporary_path, target_path)
        with _database_connection() as connection:
            connection.execute(
                """UPDATE photo_files SET size_bytes = ?, status = 'uploaded'
                   WHERE file_id = ? AND batch_id = ?""",
                (size_bytes, file_id, batch_id),
            )
    except Exception:
        temporary_path.unlink(missing_ok=True)
        target_path.unlink(missing_ok=True)
        with _database_connection() as connection:
            connection.execute(
                "DELETE FROM photo_files WHERE file_id = ? AND batch_id = ?",
                (file_id, batch_id),
            )
        raise

    return {
        "file_id": file_id,
        "batch_id": batch_id,
        "filename": filename,
        "mime_type": mime_type,
        "size_bytes": size_bytes,
        "path": f"uploads/properties-photos/{relative_path}",
    }


@router.get("/batches/{batch_id}")
def get_photo_batch(batch_id: str):
    with _database_connection() as connection:
        batch = _get_batch(connection, batch_id)
        counts = connection.execute(
            """SELECT COUNT(*) AS total_files,
                      SUM(CASE WHEN status = 'uploaded' THEN 1 ELSE 0 END) AS uploaded_files,
                      SUM(CASE WHEN status = 'uploading' THEN 1 ELSE 0 END) AS uploading_files
               FROM photo_files WHERE batch_id = ?""",
            (batch_id,),
        ).fetchone()

    total_files = counts["total_files"]
    uploaded_files = counts["uploaded_files"] or 0
    uploading_files = counts["uploading_files"] or 0
    expected_files = batch["expected_files"]
    progress_percent = (
        round(uploaded_files * 100 / expected_files, 2)
        if expected_files is not None
        else None
    )

    return {
        "batch_id": batch_id,
        "status": batch["status"],
        "expected_files": batch["expected_files"],
        "total_files": total_files,
        "uploaded_files": uploaded_files,
        "uploading_files": uploading_files,
        "progress_percent": progress_percent,
        "created_at": batch["created_at"],
        "completed_at": batch["completed_at"],
    }


@router.post("/batches/{batch_id}/complete")
def complete_photo_batch(batch_id: str):
    completed_at = _now()
    with _database_connection() as connection:
        connection.execute("BEGIN IMMEDIATE")
        batch = _get_batch(connection, batch_id)
        if batch["status"] == "completed":
            return {"batch_id": batch_id, "status": "completed", "completed_at": batch["completed_at"]}

        counts = connection.execute(
            """SELECT COUNT(*) AS total_files,
                      SUM(CASE WHEN status = 'uploading' THEN 1 ELSE 0 END) AS uploading_files
               FROM photo_files WHERE batch_id = ?""",
            (batch_id,),
        ).fetchone()
        if counts["uploading_files"]:
            raise HTTPException(status_code=409, detail="Photo uploads are still in progress")
        if counts["total_files"] == 0:
            raise HTTPException(status_code=409, detail="Cannot complete an empty photo batch")
        if (
            batch["expected_files"] is not None
            and counts["total_files"] != batch["expected_files"]
        ):
            raise HTTPException(status_code=409, detail="Expected photo count is incomplete")

        connection.execute(
            "UPDATE photo_batches SET status = 'completed', completed_at = ? WHERE batch_id = ?",
            (completed_at, batch_id),
        )

    return {"batch_id": batch_id, "status": "completed", "completed_at": completed_at}