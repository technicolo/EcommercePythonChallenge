from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class DetallePedido(SQLModel, table=True):  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    pedido_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float

class DetallePedidoDTO(BaseModel):
    producto_id: int
    cantidad: int
    precio_unitario: float

class PedidoConDetallesDTO(BaseModel):
    id: int
    usuario_id: int
    total: float
    fecha: datetime
    detalles: List[DetallePedidoDTO]