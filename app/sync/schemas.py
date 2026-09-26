# app/sync_schemas.py

from pydantic import BaseModel
from typing import Dict, List, Any
from datetime import datetime


class SyncBase(BaseModel):

    server: str
    database: str
    db_username: str
    db_password: str

    device_id: str
    last_sync_time: datetime


class LocalToRemoteRequest(SyncBase):

    tables: Dict[str, List[dict]]


class RemoteToLocalRequest(SyncBase):
    pass

class RemoteSyncRequest(BaseModel):

    server: str
    database: str
    db_username: str
    db_password: str

    table_name: str

    last_sync_time: datetime

    last_id: int = 0

    limit: int = 100