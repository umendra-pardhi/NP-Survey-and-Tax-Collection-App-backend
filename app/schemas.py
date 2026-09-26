from pydantic import BaseModel, EmailStr
from typing import Optional

class DBCredentials(BaseModel):
    server: str
    database: str
    db_username: str
    db_password: str


# Register API Schema

class UserRegister(DBCredentials):

    UserName: str

    Mobile: Optional[str] = None

    EMail: EmailStr

    LoginID: str

    Password: str

    UserRole: Optional[str] = "user"

    UserLocation: Optional[bool] = False

    ClientID: Optional[int] = None


# Login API Schema

class UserLogin(DBCredentials):

    LoginID: str

    Password: str

class InitialDBConnectRequest(BaseModel):
    server: str
    database: str = "GramDB"
    db_username: str
    db_password: str