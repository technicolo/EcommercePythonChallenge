# app/services/usuario_service.py
from sqlmodel import Session, select
from typing import List, Optional
from app.domain.usuario import Usuario

class UsuarioService:
    def __init__(self, session: Session):
        self.session = session

    def crear_usuario(self, usuario: Usuario) -> Usuario:
        self.session.add(usuario)
        self.session.commit()
        self.session.refresh(usuario)
        return usuario

    def obtener_usuarios(self) -> List[Usuario]:
        return self.session.exec(select(Usuario)).all()

    def obtener_usuario_por_id(self, usuario_id: int) -> Optional[Usuario]:
        return self.session.get(Usuario, usuario_id)

    def actualizar_usuario(self, usuario_id: int, datos_actualizados: Usuario) -> Optional[Usuario]:
        usuario = self.session.get(Usuario, usuario_id)
        if not usuario:
            return None
        usuario.nombre = datos_actualizados.nombre
        usuario.email = datos_actualizados.email
        self.session.commit()
        self.session.refresh(usuario)
        return usuario

    def eliminar_usuario(self, usuario_id: int) -> bool:
        usuario = self.session.get(Usuario, usuario_id)
        if not usuario:
            return False
        self.session.delete(usuario)
        self.session.commit()
        return True
