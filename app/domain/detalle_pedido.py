from sqlmodel import SQLModel, Field
from typing import Optional


class DetallePedido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
