from sqlmodel import SQLModel, Field
from typing import Optional


class Producto(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    nombre: str
    precio: float
    stock: int
