from sqlalchemy import create_engine
from src.models.db_models import Base


def db_connect():
    path = "postgresql+psycopg2://user:123@localhost:5432/economic-bot"
    engine = create_engine(path, echo=True)
    Base.metadata.create_all(engine)
