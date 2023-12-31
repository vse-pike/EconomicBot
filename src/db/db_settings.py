import os
import time

from dotenv import load_dotenv
from psycopg2 import OperationalError
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.db.db_tables import mapper_registry as m


def db_create_engine():
    load_dotenv()

    # Получить значения переменных среды
    db_user = os.getenv("POSTGRES_USER")
    db_password = os.getenv("POSTGRES_PASSWORD")
    db_name = os.getenv("POSTGRES_DB")
    db_host = os.getenv("POSTGRES_HOST")

    # Создать строку подключения
    db_url = f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:5432/{db_name}"
    print(db_url)

    time.sleep(15)

    engine = create_engine(db_url, echo=True)
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
