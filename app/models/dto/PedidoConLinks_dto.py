from typing import Dict, Optional

from app.domain.entities.pedido_entity import PedidoEntity


class PedidoConLinksDTO(PedidoEntity):
    links: Optional[Dict[str, Dict[str, str]]]
