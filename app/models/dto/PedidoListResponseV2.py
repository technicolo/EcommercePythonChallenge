from typing import List

from pydantic import BaseModel

from app.domain.entities.pedido_entity import PedidoEntity


class PedidoListResponseV2(BaseModel):
    version: str
    cantidad: int
    pedidos: List[PedidoEntity]
