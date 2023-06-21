from sqlalchemy.orm import registry
from sqlalchemy import Integer, String, Column, DateTime, Table, UUID, ForeignKey

from src.models.income import Income
from src.models.investment import Investment
from src.models.user import User

mapper_registry = registry()

user = Table(
    'users', mapper_registry.metadata,
    Column('id_user', Integer, primary_key=True)
)

income = Table(
    'incomes', mapper_registry.metadata,
    Column('id_income', UUID(as_uuid=True), primary_key=True),
    Column('id_user', Integer, ForeignKey('users.id_user')),
    Column('name', String(100), nullable=False),
    Column('value', Integer, nullable=False),
    Column('currency', String(100), nullable=False),
    Column('created_date', DateTime()),
    Column('modified_date', DateTime()),

)

investment = Table(
    'investments', mapper_registry.metadata,
    Column('id_investment', UUID(as_uuid=True), primary_key=True),
    Column('id_user', Integer, ForeignKey('users.id_user')),
    Column('name', String(100), nullable=False),
    Column('value', Integer, nullable=False),
    Column('currency', String(100), nullable=False),
    Column('created_date', DateTime()),
    Column('modified_date', DateTime()),
)

mapper_registry.map_imperatively(User, user)
mapper_registry.map_imperatively(Income, income)
mapper_registry.map_imperatively(Investment, investment)
