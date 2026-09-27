import os
import sys
from getpass import getpass

try:
    import pyodbc
except ImportError:
    print("pyodbc is not installed. Install the project requirements first.")
    raise SystemExit(1)

from sqlalchemy import URL, create_engine, text
from sqlalchemy.exc import SQLAlchemyError


SERVER = os.getenv("SQLSERVER_SERVER", r"localhost\SQLEXPRESS01")
DATABASE = os.getenv("SQLSERVER_DATABASE", "NagarPanchayat")
USERNAME = os.getenv("SQLSERVER_USERNAME", "umendra")
DRIVER = os.getenv("SQLSERVER_ODBC_DRIVER", "ODBC Driver 18 for SQL Server")


def main() -> int:
    available_drivers = pyodbc.drivers()
    print(f"ODBC drivers available: {', '.join(available_drivers) or '(none)'}")
    if DRIVER not in available_drivers:
        print(f"Required driver is not installed: {DRIVER}")
        return 1

    password = os.getenv("SQLSERVER_PASSWORD")
    if password is None:
        password = getpass(f"Password for {USERNAME}@{SERVER}: ")

    database_url = URL.create(
        "mssql+pyodbc",
        username=USERNAME,
        password=password,
        host=SERVER,
        database=DATABASE,
        query={
            "driver": DRIVER,
            "Encrypt": "yes",
            "TrustServerCertificate": "yes",
        },
    )

    engine = create_engine(database_url, pool_pre_ping=True)
    try:
        with engine.connect() as connection:
            result = connection.execute(
                text(
                    "SELECT DB_NAME() AS database_name, "
                    "@@SERVERNAME AS server_name"
                )
            ).mappings().one()
            print(
                f"Connected to database {result['database_name']} "
                f"on SQL Server {result['server_name']}"
            )

            tables = connection.execute(
                text(
                    "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES "
                    "WHERE TABLE_SCHEMA = 'dbo' "
                    "AND TABLE_NAME IN ('Accounts', 'Users') "
                    "ORDER BY TABLE_NAME"
                )
            ).scalars().all()
            print(f"Expected dbo tables found: {', '.join(tables) or '(none)'}")
            missing_tables = {"Accounts", "Users"} - set(tables)
            if missing_tables:
                print(f"Missing expected tables: {', '.join(sorted(missing_tables))}")
                return 2

        print("Database connection and schema check passed.")
        return 0
    except SQLAlchemyError as error:
        print(f"Database connection failed: {error}", file=sys.stderr)
        return 1
    finally:
        engine.dispose()


if __name__ == "__main__":
    raise SystemExit(main())