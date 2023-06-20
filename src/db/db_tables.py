from sqlalchemy.orm import registry
from sqlalchemy import Integer, String, Column, DateTime, Table, UUID

from src.models.income import Income
from src.models.investment import Investment

mapper_registry = registry()

income = Table(
    'income', mapper_registry.metadata,
    Column('id_income', UUID(as_uuid=True), primary_key=True),
    Column('value', Integer, nullable=False),
    Column('currency', String(100), nullable=False),
    Column('created_date', DateTime()),
    Column('modified_date', DateTime())
)

investment = Table(
    'investment', mapper_registry.metadata,
    Column('id_investment', UUID(as_uuid=True), primary_key=True),
    Column('name', String(100), nullable=False),
    Column('value', Integer, nullable=False),
    Column('currency', String(100), nullable=False),
    Column('created_date', DateTime()),
    Column('modified_date', DateTime())
)

mapper_registry.map_imperatively(Income, income)
mapper_registry.map_imperatively(Investment, investment)
