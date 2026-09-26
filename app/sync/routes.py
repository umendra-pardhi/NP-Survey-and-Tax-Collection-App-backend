# app/sync_routes.py

from fastapi import APIRouter, Header, Request
from app.sync.schemas import (
    LocalToRemoteRequest,
    RemoteToLocalRequest, RemoteSyncRequest
)

from app.sync.services import SyncService
from app.database import create_dynamic_session

router = APIRouter()


@router.post("/sync/local-to-remote")
async def sync_local_to_remote(
    payload: LocalToRemoteRequest
):

    SessionLocal, engine = create_dynamic_session(
            payload.server,
            payload.database,
            payload.db_username,
            payload.db_password
        )

    db = SessionLocal()

    return SyncService.process_local_to_remote(
        db,
        payload
    )


@router.post("/sync/local-to-remote/stream")
async def sync_local_to_remote_stream(
    server: str,
    database: str,
    table_name: str,
    request: Request,
    db_username: str = Header(..., alias="X-DB-Username"),
    db_password: str = Header(..., alias="X-DB-Password"),
):

    SessionLocal, engine = create_dynamic_session(
            server,
            database,
            db_username,
            db_password
        )

    db = None
    try:
        db = SessionLocal()
        return await SyncService.process_local_to_remote_stream(
            db,
            request,
            table_name
        )
    finally:
        try:
            if db is not None:
                db.close()
        finally:
            engine.dispose()



@router.post("/sync/remote-to-local")
async def remote_to_local(
    payload: RemoteSyncRequest
):


    SessionLocal, engine = create_dynamic_session(
            payload.server,
            payload.database,
            payload.db_username,
            payload.db_password
        )

    db = SessionLocal()

    return await SyncService.stream_remote_to_local(
        db,
        payload
    )