from sqlmodel import Session, select
from app.domain.producto import Producto
from app.persistence.db import get_session
from typing import List, Optional


def crear_producto(producto: Producto) -> Producto:
    with get_session() as session:
        session.add(producto)
        session.commit()
        session.refresh(producto)
        return producto


def obtener_productos() -> List[Producto]:
    with get_session() as session:
        productos = session.exec(select(Producto)).all()
        return productos


def obtener_producto_por_id(producto_id: int) -> Optional[Producto]:
    with get_session() as session:
        return session.get(Producto, producto_id)


def actualizar_producto(producto_id: int, datos_actualizados: Producto) -> Optional[Producto]:
    with get_session() as session:
        producto = session.get(Producto, producto_id)
        if not producto:
            return None
        producto.nombre = datos_actualizados.nombre
        producto.precio = datos_actualizados.precio
        producto.stock = datos_actualizados.stock
        session.commit()
        session.refresh(producto)
        return producto


def eliminar_producto(producto_id: int) -> bool:
    with get_session() as session:
        producto = session.get(Producto, producto_id)
        if not producto:
            return False
        session.delete(producto)
        session.commit()
        return True
