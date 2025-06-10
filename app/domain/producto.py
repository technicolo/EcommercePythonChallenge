from typing import Optional

from sqlmodel import Field, SQLModel


class Producto(SQLModel, table=True):  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    precio: float
    stock: int
