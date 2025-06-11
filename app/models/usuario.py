from typing import Optional

from sqlmodel import Field, SQLModel


class Usuario(SQLModel, table=True):  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    email: str = Field(index=True, unique=True)
    password: str
