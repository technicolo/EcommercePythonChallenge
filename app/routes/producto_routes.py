# app/routes/producto_routes.py

from typing import List

from fastapi import APIRouter, Body, Depends, File, HTTPException, Path, UploadFile
from sqlmodel import Session

from app.domain.entities.producto_entity import ProductoEntity
from app.mappers.producto_mapper import to_entity, to_model
from app.models.producto import Producto
from app.persistence.db import get_session
from app.services.dependencies import get_producto_service
from app.services.producto_service import ProductoService
from app.utils.csv_parser import parse_csv_to_productos

router = APIRouter(prefix="/productos", tags=["Productos"])

@router.post("/importar-csv")
def importar_productos_csv(file: UploadFile = File(...), db: Session = Depends(get_session)):
    contents = file.file.read().decode("utf-8")
    productos = parse_csv_to_productos(contents)
    
    db.add_all([to_model(p) for p in productos])
    db.commit()
    
    return {"mensaje": f"{len(productos)} productos importados correctamente"}

@router.post("/lote", response_model=List[ProductoEntity])
def crear_productos_lote(
    productos: List[ProductoEntity], db: Session = Depends(get_session)
):
    modelos = [to_model(p) for p in productos]
    db.add_all(modelos)
    db.commit()
    return [to_entity(m) for m in modelos]


@router.put("/actualizar-lote", response_model=List[ProductoEntity])
def actualizar_productos_lote(
    productos: List[ProductoEntity] = Body(...),  # 👈 esto es clave
    db: Session = Depends(get_session)
):
    actualizados = []
    for prod in productos:
        existente = db.get(Producto, prod.id)
        if existente:
            existente.nombre = prod.nombre
            existente.precio = prod.precio
            existente.stock = prod.stock
            actualizados.append(existente)
    db.commit()
    return [to_entity(p) for p in actualizados]


@router.delete("/lote")
def eliminar_productos_lote(
    ids: List[int] = Body(...),  # 👈 también va en el body
    db: Session = Depends(get_session)
):
    for producto_id in ids:
        producto = db.get(Producto, producto_id)
        if producto:
            db.delete(producto)
    db.commit()
    return {"mensaje": f"Se intentó eliminar {len(ids)} productos"}

@router.get("/", response_model=List[ProductoEntity])
def listar_productos(offset: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    return ProductoService(db).obtener_productos(offset=offset, limit=limit)


@router.get("/{producto_id}", response_model=ProductoEntity)
def obtener(producto_id: int = Path(..., title="ID del producto"),service: ProductoService = Depends(get_producto_service)):
    producto = service.obtener_producto_por_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.put("/{producto_id}", response_model=ProductoEntity)
def actualizar(producto_id: int = Path(..., title="ID del producto"),datos: ProductoEntity = Body(...),service: ProductoService = Depends(get_producto_service)):
    producto = service.actualizar_producto(producto_id, datos)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.delete("/{producto_id}")
def eliminar(producto_id: int = Path(..., title="ID del producto"),service: ProductoService = Depends(get_producto_service)):
    if not service.eliminar_producto(producto_id):
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return {"mensaje": "Producto eliminado"}
