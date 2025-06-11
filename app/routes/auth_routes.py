from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from app.models.dto.register_dto import RegisterDTO
from app.models.dto.usuarioDTO import LoginDTO
from app.models.usuario import Usuario
from app.persistence.db import get_session
from app.utils.security import create_access_token, hash_password, verify_password

router = APIRouter()

@router.post("/register", response_model=Usuario)
def register(datos: RegisterDTO, session: Session = Depends(get_session)):
    existente = session.exec(select(Usuario).where(Usuario.email == datos.email)).first()
    if existente:
        raise HTTPException(status_code=400, detail="El email ya está registrado")

    nuevo_usuario = Usuario(
        email=datos.email,
        password=hash_password(datos.password),
        nombre="Usuario"  # si es obligatorio en tu modelo, podés usar uno genérico o generarlo luego
    )

    session.add(nuevo_usuario)
    session.commit()
    session.refresh(nuevo_usuario)
    return nuevo_usuario

# 🔐 Endpoint de login
@router.post("/login")
def login(datos: LoginDTO, session: Session = Depends(get_session)):
    user = session.exec(select(Usuario).where(Usuario.email == datos.email)).first()
    if not user or not verify_password(datos.password, user.password):
        raise HTTPException(status_code=400, detail="Credenciales inválidas")

    token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": token, "token_type": "bearer"}
