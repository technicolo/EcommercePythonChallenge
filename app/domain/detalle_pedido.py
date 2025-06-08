from sqlmodel import SQLModel, Field
from typing import Optional
from typing import List
from datetime import datetime
from pydantic import BaseModel

class DetallePedido(SQLModel, table=True):
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