from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean,
    LargeBinary,
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):

    __tablename__ = "Users"
    __table_args__ = {"schema": "dbo"}

    UserID = Column("UserID", Integer, primary_key=True)

    UserName = Column("UserName", String(50))

    Mobile = Column("Mobile", String(50))

    EMail = Column("EMail", String(50))

    LoginID = Column("LoginID", String(50))

    Password = Column("Password", LargeBinary)

    UserRole = Column("UserRole", String(50))

    UserLocation = Column("UserLocation", Boolean)

    ClientID = Column("ClientID", Integer)