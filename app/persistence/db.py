from sqlmodel import SQLModel, create_engine, Session
from typing import Generator
from contextlib import contextmanager

DATABASE_URL = "sqlite:///./ecommerce.db"
engine = create_engine("sqlite:///ecommerce.db", echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

