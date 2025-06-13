# app/services/detalle_pedido_service.py

from typing import List, Optional

from fastapi import HTTPException
from sqlmodel import Session, select

from app.domain.entities.detalle_pedido_entity import DetallePedidoEntity
from app.mappers.detalle_pedido_mapper import to_entity, to_model
from app.models.detalle_pedido import DetallePedido
from app.models.pedido import Pedido
from app.services.pedido_service import PedidoService


class DetallePedidoService:
    def __init__(self, session: Session):
        self.session = session
        self.pedido_service = PedidoService(session)

    def crear_detalle(self, detalle: DetallePedidoEntity) -> DetallePedidoEntity:
        pedido = self.session.get(Pedido, detalle.pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado para este detalle")

        model = to_model(detalle)
        self.session.add(model)
        self.session.commit()
        self.session.refresh(model)

        self.pedido_service.actualizar_total_pedido(detalle.pedido_id)

        return to_entity(model)

    def obtener_detalles(self) -> List[DetallePedidoEntity]:
        resultados = self.session.exec(select(DetallePedido)).all()
        return [to_entity(det) for det in resultados]

    def obtener_detalle_por_id(self, detalle_id: int) -> Optional[DetallePedidoEntity]:
        detalle = self.session.get(DetallePedido, detalle_id)
        return to_entity(detalle) if detalle else None

    def actualizar_detalle(self, detalle_id: int, datos: DetallePedidoEntity) -> Optional[DetallePedidoEntity]:
        detalle = self.session.get(DetallePedido, detalle_id)
        if not detalle:
            return None
    
        # 1. Calcular valor anterior
        valor_anterior = detalle.cantidad * detalle.precio_unitario
    
        # 2. Actualizar campos
        detalle.pedido_id = datos.pedido_id
        detalle.producto_id = datos.producto_id
        detalle.cantidad = datos.cantidad
        detalle.precio_unitario = datos.precio_unitario
    
        # 3. Calcular nuevo valor
        valor_nuevo = detalle.cantidad * detalle.precio_unitario
    
        # 4. Ajustar total del pedido
        pedido = self.session.get(Pedido, detalle.pedido_id)
        if not pedido:
            raise HTTPException(status_code=404, detail="Pedido no encontrado")
    
        pedido.total = pedido.total - valor_anterior + valor_nuevo
    
        # 5. Guardar cambios
        self.session.commit()
        self.session.refresh(detalle)
    
        return to_entity(detalle)


    def eliminar_detalle(self, detalle_id: int) -> bool:
        detalle = self.session.get(DetallePedido, detalle_id)
        if not detalle:
            return False
        self.session.delete(detalle)
        self.session.commit()
        return True
