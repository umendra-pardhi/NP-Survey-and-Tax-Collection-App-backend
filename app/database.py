# from sqlalchemy import URL, create_engine
# from sqlalchemy.orm import sessionmaker
# from dotenv import load_dotenv


# load_dotenv()


# def create_dynamic_session(
#     server: str,
#     database: str,
#     username: str,
#     password: str
# ):
#     database_url = URL.create(
#         "mssql+pyodbc",
#         username=username,
#         password=password,
#         host=server,
#         database=database,
#         query={
#             "driver": "ODBC Driver 18 for SQL Server",
#             "Encrypt": "yes",
#             "TrustServerCertificate": "yes",
#         },
#     )

#     engine = create_engine(
#         database_url,
#         pool_pre_ping=True,
#         pool_size=5,
#         max_overflow=10,
#         fast_executemany=True,
#         connect_args={"timeout": 5}
#     )

#     SessionLocal = sessionmaker(
#         autocommit=False,
#         autoflush=False,
#         bind=engine,
#     )

#     return SessionLocal, engine

from sqlalchemy import URL, create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from dotenv import load_dotenv

load_dotenv()


def create_dynamic_session(
    server: str,
    database: str,
    username: str,
    password: str,
    port: int = 1433,
):
    database_url = URL.create(
        "mssql+pyodbc",
        username=username,
        password=password,
        host=server,
        port=port,
        database=database,
        query={
            "driver": "ODBC Driver 18 for SQL Server",
            "Encrypt": "yes",
            "TrustServerCertificate": "yes",
        },
    )

    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        fast_executemany=True,
        # connect_args={"timeout": 5},
    )

    try:
        # Test the actual database connection
        with engine.connect() as connection:
            result = connection.execute(
                text("SELECT @@SERVERNAME, DB_NAME()")
            )
            server_name, database_name = result.fetchone()

            print("Connection successful!")
            print("Server:", server_name)
            print("Database:", database_name)

    except SQLAlchemyError as exc:
        engine.dispose()
        print("Database connection failed:", str(exc))
        raise

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    return SessionLocal, engine