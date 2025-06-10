from datetime import datetime
from typing import Optional

from sqlmodel import Field, SQLModel


class Pedido(SQLModel, table=True):  # type: ignore
    id: Optional[int] = Field(default=None, primary_key=True)
    fecha: datetime = Field(default_factory=datetime.utcnow)
    total: float
    usuario_id: int


class PedidoCreate(SQLModel):
    usuario_id: int
