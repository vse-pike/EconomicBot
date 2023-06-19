from sqlalchemy import Integer, String, Column, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Income(Base):
    __tablename__ = 'income'
    id = Column(Integer, primary_key=True)
    value = Column(Integer, nullable=False)
    currency = Column(String(100), nullable=False)
    created_date = Column(DateTime())
    modified_date = Column(DateTime())


class Investment(Base):
    __tablename__ = 'investment'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    value = Column(Integer, nullable=False)
    currency = Column(String(100), nullable=False)
    created_date = Column(DateTime())
    modified_date = Column(DateTime())
