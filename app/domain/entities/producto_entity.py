from typing import Optional

from pydantic import BaseModel


class ProductoEntity(BaseModel):
    id: Optional[int] = None
    nombre: str
    precio: float
    stock: int
