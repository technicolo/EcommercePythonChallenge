from sqlmodel import Session, select
from app.domain.usuario import Usuario
from app.persistence.db import get_session
from typing import List, Optional


def crear_usuario(usuario: Usuario) -> Usuario:
    with get_session() as session:
        session.add(usuario)
        session.commit()
        session.refresh(usuario)
        return usuario


def obtener_usuarios() -> List[Usuario]:
    with get_session() as session:
        return session.exec(select(Usuario)).all()


def obtener_usuario_por_id(usuario_id: int) -> Optional[Usuario]:
    with get_session() as session:
        return session.get(Usuario, usuario_id)


def actualizar_usuario(usuario_id: int, datos_actualizados: Usuario) -> Optional[Usuario]:
    with get_session() as session:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            return None
        usuario.nombre = datos_actualizados.nombre
        usuario.email = datos_actualizados.email
        session.commit()
        session.refresh(usuario)
        return usuario


def eliminar_usuario(usuario_id: int) -> bool:
    with get_session() as session:
        usuario = session.get(Usuario, usuario_id)
        if not usuario:
            return False
        session.delete(usuario)
        session.commit()
        return True
