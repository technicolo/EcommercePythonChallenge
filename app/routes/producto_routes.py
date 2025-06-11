# app/routes/producto_routes.py

import csv
from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from sqlmodel import Session

from app.domain.entities.producto_entity import ProductoEntity
from app.models.producto import Producto
from app.persistence.db import get_session
from app.services.dependencies import get_producto_service
from app.services.producto_service import ProductoService

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.get("/", response_model=List[ProductoEntity])
def listar_productos(offset: int = 0, limit: int = 10, db: Session = Depends(get_session)):
    return ProductoService(db).obtener_productos(offset=offset, limit=limit)


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

@router.post("/importar-csv")
def importar_productos_csv(file: UploadFile = File(...), db: Session = Depends(get_session)):
    contents = file.file.read().decode("utf-8").splitlines()
    reader = csv.DictReader(contents)
    productos = [
        Producto(nombre=row["nombre"], precio=float(row["precio"]), stock=int(row["stock"]))
        for row in reader
    ]
    db.add_all(productos)
    db.commit()
    return {"mensaje": f"{len(productos)} productos importados correctamente"}
