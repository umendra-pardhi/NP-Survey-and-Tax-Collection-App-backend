import os

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
    if server.strip().lower() == "postgres":
        server = os.getenv("POSTGRES_HOST", server)

    database_url = URL.create(
        "postgresql+psycopg",
        username=username,
        password=password,
        host=server,
        port=5432,
        database=database,
    )

    engine = create_engine(
        database_url,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )

    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

    return SessionLocal, engine