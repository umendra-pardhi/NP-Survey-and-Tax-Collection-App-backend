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
                    SELECT [LoginID], [UserName]
                    FROM [dbo].[Users]
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
        error_message = str(error).lower()
        error_text = str(original_error or error)

        if "cannot open database" in error_message or "4060" in error_text:
            return {
                "success": False,
                "error_code": "DATABASE_NOT_FOUND",
                "message": "Database does not exist"
            }

        if "login failed" in error_message or "18456" in error_text:
            return {
                "success": False,
                "error_code": "INVALID_DB_CREDENTIALS",
                "message": "Invalid database username or password"
            }

        if (
            "could not translate host name" in error_message
            or "connection refused" in error_message
            or "could not connect" in error_message
            or "08001" in error_text
            or "timeout" in error_message
        ):
            return {
                "success": False,
                "error_code": "SERVER_UNREACHABLE",
                "message": "Unable to connect to SQL Server"
            }

        return {
            "success": False,
            "error_code": "CONNECTION_FAILED",
            "message": "Database connection failed"
        }