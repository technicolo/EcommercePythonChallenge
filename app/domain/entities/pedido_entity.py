from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class PedidoEntity(BaseModel):
    id: Optional[int] = None
    usuario_id: int
    estado: str
    fecha: datetime
    total: float
