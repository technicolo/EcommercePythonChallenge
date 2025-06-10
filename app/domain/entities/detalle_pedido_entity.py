from typing import Optional

from pydantic import BaseModel


class DetallePedidoEntity(BaseModel):
    id: Optional[int] = None
    pedido_id: int
    producto_id: int
    cantidad: int
    precio_unitario: float
