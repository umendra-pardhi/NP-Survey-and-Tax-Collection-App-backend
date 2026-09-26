from sqlalchemy import text

from .database import create_dynamic_session


def connect_to_gramdb(
    server,
    database,
    username,
    password
):


    try:
        SessionLocal, engine = create_dynamic_session(
            server,
            database,
            username,
            password,
        )

        try:
            with SessionLocal() as db:
                result = db.execute(text('''
                    SELECT loginid AS "LoginID", username AS "Username"
                    FROM users
                '''))
                clients = [dict(row) for row in result.mappings()]
        finally:
            engine.dispose()

        return {
            "success": True,
            "message": "Database connected successfully",
            "client_count": len(clients),
            "clients": clients
        }

    except Exception as error:
        original_error = getattr(error, "orig", None)
        sqlstate = getattr(original_error, "sqlstate", None)
        error_message = str(error).lower()

        if sqlstate == "3D000":
            return {
                "success": False,
                "error_code": "DATABASE_NOT_FOUND",
                "message": "Database does not exist"
            }

        if sqlstate in {"28P01", "28000"}:
            return {
                "success": False,
                "error_code": "INVALID_DB_CREDENTIALS",
                "message": "Invalid database username or password"
            }

        if (
            "could not translate host name" in error_message
            or "connection refused" in error_message
            or "could not connect" in error_message
            or "timeout" in error_message
        ):
            return {
                "success": False,
                "error_code": "SERVER_UNREACHABLE",
                "message": "Unable to connect to PostgreSQL server"
            }

        return {
            "success": False,
            "error_code": "CONNECTION_FAILED",
            "message": "Database connection failed"
        }