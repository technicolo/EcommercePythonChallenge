from typing import Generator

from sqlmodel import Session, SQLModel, create_engine

DATABASE_URL = "sqlite:///./ecommerce.db"
engine = create_engine("sqlite:///ecommerce.db", echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session

