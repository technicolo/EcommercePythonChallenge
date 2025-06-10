# app/routes/producto_routes.py

from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from app.domain.entities.producto_entity import ProductoEntity
from app.models.producto import Producto
from app.persistence.db import get_session
from app.services.dependencies import get_producto_service
from app.services.producto_service import ProductoService

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/", response_model=ProductoEntity)
def crear(producto: ProductoEntity, service: ProductoService = Depends(get_producto_service)):
    return service.crear_producto(producto)


@router.get("/", response_model=List[ProductoEntity])
def listar_productos(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session)
):
    query = select(Producto).offset(offset).limit(limit)
    results = session.exec(query).all()
    # Convertir los modelos a entidades de dominio
    from app.mappers.producto_mapper import to_entity
    return [to_entity(p) for p in results]


@router.get("/{producto_id}", response_model=ProductoEntity)
def obtener(producto_id: int, service: ProductoService = Depends(get_producto_service)):
    producto = service.obtener_producto_por_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.put("/{producto_id}", response_model=ProductoEntity)
def actualizar(producto_id: int, datos: ProductoEntity, service: ProductoService = Depends(get_producto_service)):
    producto = service.actualizar_producto(producto_id, datos)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.delete("/{producto_id}")
def eliminar(producto_id: int, service: ProductoService = Depends(get_producto_service)):
    if not service.eliminar_producto(producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado"}
