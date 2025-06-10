from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile
from sqlmodel import Session, select

from app.domain.producto import Producto
from app.persistence.db import get_session
from app.services.dependencies import get_producto_service
from app.services.producto_service import ProductoService
from app.utils.csv_parser import parse_csv_to_productos

router = APIRouter(prefix="/productos", tags=["Productos"])


@router.post("/", response_model=Producto)
def crear(producto: Producto, service: ProductoService = Depends(get_producto_service)):
    return service.crear_producto(producto)


@router.get("/", response_model=List[Producto])
def listar_productos(
    offset: int = Query(0, ge=0),
    limit: int = Query(10, ge=1),
    session: Session = Depends(get_session)  # Caso especial: paginación directa
):
    query = select(Producto).offset(offset).limit(limit)
    return session.exec(query).all()


@router.get("/{producto_id}", response_model=Producto)
def obtener(producto_id: int, service: ProductoService = Depends(get_producto_service)):
    producto = service.obtener_producto_por_id(producto_id)
    if not producto:
        raise HTTPException(status_code=404, detail="Producto no encontrado")
    return producto


@router.put("/{producto_id}", response_model=Producto)
def actualizar(producto_id: int, datos: Producto, service: ProductoService = Depends(get_producto_service)):
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
async def importar_productos_csv(file: UploadFile = File(...), session: Session = Depends(get_session)):
    if not file.filename.endswith(".csv"):
        raise HTTPException(status_code=400, detail="El archivo debe ser un CSV")

    content = (await file.read()).decode("utf-8")
    productos = parse_csv_to_productos(content)

    session.add_all(productos)
    session.commit()

    return {"mensaje": f"Se importaron {len(productos)} productos correctamente"}
