from sqlalchemy import (
    Column,
    Integer,
    String,
    Boolean
)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):

    __tablename__ = "users"

    UserID = Column("userid", Integer, primary_key=True, index=True)

    UserName = Column("username", String(50))

    Mobile = Column("mobile", String(50))

    EMail = Column("email", String(50), index=True)

    LoginID = Column("loginid", String(50), unique=True, index=True)

    Password = Column("Password", String(255))

    UserRole = Column("userrole", String(50))

    UserLocation = Column("userlocation", Boolean)

    ClientID = Column("clientid", Integer)