from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Pedido(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: datetime = Field(default_factory=datetime.utcnow)
    total: float
    usuario_id: int


class PedidoCreate(SQLModel):
    usuario_id: int
