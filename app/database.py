from sqlalchemy import URL, create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


load_dotenv()


def create_dynamic_session(
    server: str,
    database: str,
    username: str,
    password: str
):
    database_url = URL.create(
        "mssql+pyodbc",
        username=username,
        password=password,
        host=server,
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
        connect_args={"timeout": 5}
    )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    return SessionLocal, engine

# from sqlalchemy import URL, create_engine, text
# from sqlalchemy.orm import sessionmaker
# from sqlalchemy.exc import SQLAlchemyError
# from dotenv import load_dotenv

# load_dotenv()


# def parse_sql_server(server: str) -> tuple[str, int | None]:
#     """
#     Accept host, host,port, or host\\instance (see project Readme).
#     Named instances omit an explicit port so ODBC can resolve the instance.
#     """
#     server = server.strip()
#     if not server:
#         raise ValueError("SQL Server host is required")

#     if "," in server:
#         host, port_str = server.rsplit(",", 1)
#         return host.strip(), int(port_str.strip())

#     if "\\" in server:
#         return server, None

#     return server, 1433


# def create_dynamic_session(
#     server: str,
#     database: str,
#     username: str,
#     password: str,
#     port: int | None = None,
# ):
#     host, parsed_port = parse_sql_server(server)
#     if port is not None:
#         parsed_port = port

#     url_kwargs: dict = {
#         "drivername": "mssql+pyodbc",
#         "username": username,
#         "password": password,
#         "host": host,
#         "database": database,
#         "query": {
#             "driver": "ODBC Driver 18 for SQL Server",
#             "Encrypt": "yes",
#             "TrustServerCertificate": "yes",
#         },
#     }
#     if parsed_port is not None:
#         url_kwargs["port"] = parsed_port

#     database_url = URL.create(**url_kwargs)

#     engine = create_engine(
#         database_url,
#         pool_pre_ping=True,
#         pool_size=5,
#         max_overflow=10,
#         fast_executemany=True,
#         connect_args={"timeout": 5},
#     )

#     try:
#         # Test the actual database connection
#         with engine.connect() as connection:
#             result = connection.execute(
#                 text("SELECT @@SERVERNAME, DB_NAME()")
#             )
#             server_name, database_name = result.fetchone()

#             print("Connection successful!")
#             print("Server:", server_name)
#             print("Database:", database_name)

#     except SQLAlchemyError as exc:
#         engine.dispose()
#         print("Database connection failed:", str(exc))
#         raise

#     SessionLocal = sessionmaker(
#         autocommit=False,
#         autoflush=False,
#         bind=engine,
#     )

#     return SessionLocal, engine