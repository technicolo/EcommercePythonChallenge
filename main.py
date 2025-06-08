from fastapi import FastAPI
from app.persistence.db import create_db_and_tables
from app.routes import detalle_pedido_routes, pedido_routes, producto_routes, usuario_routes

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

@app.get("/health", tags=["Sistema"])
def health_check():
    return {"status": "ok"}

@app.get("/version", tags=["Sistema"])
def get_version():
    return {"version": "1.0.0"}
