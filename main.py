from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException as StarletteHTTPException

from app.persistence.db import create_db_and_tables
from app.routes import (
    detalle_pedido_routes,
    pedido_routes,
    producto_routes,
    usuario_routes,
)
from app.utils.ProblemDetailsException import problem_detail_response

app = FastAPI(
    title="E-commerce API",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()


app.include_router(producto_routes.router)
app.include_router(usuario_routes.router)
app.include_router(pedido_routes.router)
app.include_router(detalle_pedido_routes.router)

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    return problem_detail_response(
        status_code=exc.status_code,
        title="HTTP Exception",
        detail=exc.detail,
        instance=str(request.url)
    )

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return problem_detail_response(
        status_code=422,
        title="Validation Error",
        detail=str(exc),
        instance=str(request.url)
    )

@app.get("/health", tags=["Sistema"])
def health_check():
    return {"status": "ok"}

@app.get("/version", tags=["Sistema"])
def get_version():
    return {"version": "1.0.0"}
