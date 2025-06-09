import csv
from io import StringIO
from typing import List
from fastapi import HTTPException
from app.domain.producto import Producto

def parse_csv_to_productos(file_content: str) -> List[Producto]:
    from io import StringIO
    import csv

    def try_parse(separator: str):
        reader = csv.DictReader(StringIO(file_content), delimiter=separator)
        if not reader.fieldnames:
            return None, None
        clean_fields = [col.strip().replace("\ufeff", "") for col in reader.fieldnames]
        field_map = {col.lower(): orig for col, orig in zip(clean_fields, reader.fieldnames)}
        return reader, field_map

    expected_fields = {"nombre", "precio", "stock"}
    for sep in [",", ";"]:
        csv_reader, field_map = try_parse(sep)
        if csv_reader and expected_fields.issubset(field_map.keys()):
            break
    else:
        raise HTTPException(
            status_code=400,
            detail=f"El CSV debe tener las columnas: {expected_fields}. Columnas encontradas: {field_map.keys() if field_map else 'desconocidas'}"
        )

    productos = []
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
