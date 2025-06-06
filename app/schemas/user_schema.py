from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserCreate(BaseModel):
    nome: str
    email: EmailStr
    senha_hash: str
    pais: str


class UserModel(UserCreate):
    id: int
    data_cadastro: datetime

    class Config:
        orm_mode = True
