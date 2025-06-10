from typing import Optional

from pydantic import BaseModel


class UsuarioEntity(BaseModel):
    id: Optional[int] = None
    nombre: str
    email: str
