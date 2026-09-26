from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from fastapi.responses import JSONResponse

from .schemas import UserRegister, UserLogin, InitialDBConnectRequest
from .database import create_dynamic_session
from .services import connect_to_gramdb
from .models import User
from .auth import (
    hash_password,
    verify_password,
    create_access_token
)

router = APIRouter()


@router.post("/register")
def register(request: UserRegister):

    try:

        SessionLocal, engine = create_dynamic_session(
            request.server,
            request.database,
            request.db_username,
            request.db_password
        )

        db = SessionLocal()

        existing_user = (
            db.query(User)
            .filter(User.LoginID == request.LoginID)
            .first()
        )

        if existing_user:

            return {
                "success": False,
                "message": "Login ID already exists"
            }

        new_user = User(

            UserName=request.UserName,

            Mobile=request.Mobile,

            EMail=request.EMail,

            LoginID=request.LoginID,

            Password=hash_password(request.Password),

            UserRole=request.UserRole,

            UserLocation=request.UserLocation,

            ClientID=request.ClientID
        )

        db.add(new_user)

        db.commit()

        db.refresh(new_user)

        db.close()

        engine.dispose()

        return {
            "success": True,
            "message": "User registered successfully",
            "user_id": new_user.UserID
        }

    except SQLAlchemyError:

        return {
            "success": False,
            "message": "Database operation failed"
        }

    except Exception as e:

        print("REGISTER ERROR:", str(e))

        return {
            "success": False,
            "message": str(e)
        }

@router.post("/login")
def login(request: UserLogin):

    try:

        SessionLocal, engine = create_dynamic_session(
            request.server,
            request.database,
            request.db_username,
            request.db_password
        )

        db = SessionLocal()

        user = (
            db.query(User)
            .filter(User.LoginID == request.LoginID)
            .first()
        )

        if not user:

            return {
                "success": False,
                "message": "Invalid Login ID or Password"
            }

        if not verify_password(
            request.Password,
            user.Password
        ):

            return {
                "success": False,
                "message": "Invalid Login ID or Password"
            }

        token = create_access_token({
            "sub": str(user.UserID),
            "login_id": user.LoginID
        })

        db.close()

        engine.dispose()

        return {
            "success": True,
            "message": "Login successful",
            "access_token": token,
            "token_type": "bearer",
            "user": {
                "UserID": user.UserID,
                "UserName": user.UserName,
                "UserRole": user.UserRole,
                "ClientID": user.ClientID,
                "EMail": user.EMail,
                "Mobile": user.Mobile,
                "LoginID": user.LoginID
            }
        }

    except Exception as e:

        print("LOGIN ERROR:", str(e))

        return {
            "success": False,
            "message": "Login failed: "+str(e)
        }

@router.post("/initial-connect")
def initial_connect(
    request: InitialDBConnectRequest
):

    result = connect_to_gramdb(
        server=request.server,
        database=request.database,
        username=request.db_username,
        password=request.db_password
    )

    if not result["success"]:

        return JSONResponse(
            status_code=400,
            content=result
        )

    return JSONResponse(
        status_code=200,
        content=result
    )