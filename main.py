from fastapi import FastAPI

app = FastAPI(
    title="E-commerce API",
    version="1.0.0"
)

# Endpoint de prueba
@app.get("/health", tags=["Sistema"])
def health_check():
    return {"status": "ok"}

@app.get("/version", tags=["Sistema"])
def get_version():
    return {"version": "1.0.0"}
