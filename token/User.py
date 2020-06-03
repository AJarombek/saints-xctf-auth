"""
Model object for the 'user' table found in RDS/MySQL.
Author: Andrew Jarombek
Date: 5/31/2020
"""

from sqlalchemy import Column, VARCHAR
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    username = Column(VARCHAR(20), primary_key=True)
    first = Column(VARCHAR(30), nullable=False, index=True)
    last = Column(VARCHAR(30), nullable=False, index=True)
    password = Column(VARCHAR(255), nullable=False)
    email = Column(VARCHAR(50), index=True)
