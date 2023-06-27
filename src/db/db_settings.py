from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.db_tables import mapper_registry as m


def db_create_engine():
    path = "postgresql+psycopg2://user:123@postgres:5432/economic-bot"
    engine = create_engine(path, echo=True)
    m.metadata.create_all(engine)

    return engine


def db_create_session(engine):
    Session = sessionmaker(bind=engine)
    session = Session()

    return session


class Db:
    def __init__(self):
        self.engine = db_create_engine()
        self.session = db_create_session(self.engine)
