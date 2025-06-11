from pydantic import BaseModel, EmailStr


class RegisterDTO(BaseModel):
    email: EmailStr
    password: str
