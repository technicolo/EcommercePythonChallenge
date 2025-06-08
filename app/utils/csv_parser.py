import csv
from io import StringIO
from typing import List
from fastapi import HTTPException
from app.domain.producto import Producto

def parse_csv_to_productos(file_content: str) -> List[Producto]:
    productos = []
    csv_reader = csv.DictReader(StringIO(file_content))

    if not csv_reader.fieldnames:
        raise HTTPException(status_code=400, detail="El archivo CSV está vacío o mal formado")

    # Normalizamos los encabezados
    field_map = {col.lower().strip(): col for col in csv_reader.fieldnames}
    expected_fields = {"nombre", "precio", "stock"}

    if not expected_fields.issubset(field_map.keys()):
        raise HTTPException(
            status_code=400,
            detail=f"El CSV debe tener las columnas: {expected_fields}. Columnas encontradas: {field_map.keys()}"
        )

    for i, row in enumerate(csv_reader, start=2):
        try:
            nombre = row[field_map["nombre"]].strip()
            precio = float(row[field_map["precio"]].strip())
            stock = int(row[field_map["stock"]].strip())

            productos.append(Producto(nombre=nombre, precio=precio, stock=stock))
        except Exception as e:
            raise HTTPException(
                status_code=400,
                detail=f"Error en fila {i}: {row} -> {str(e)}"
            )

    return productos
