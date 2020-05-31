from sqlalchemy import Column, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    username = Column(VARCHAR(20), primary_key=True)
    first = Column(VARCHAR(30), nullable=False, index=True)
    last = Column(VARCHAR(30), nullable=False, index=True)
