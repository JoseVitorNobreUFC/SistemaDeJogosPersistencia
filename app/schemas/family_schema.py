from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

class FamilyCreate(BaseModel): # Atualizar o esquema para ficar congruente com o model
    titulo: str
    descricao: Optional[str] = None
    data_lancamento: date
    preco: Decimal
    desenvolvedora: str

class FamilyModel(FamilyCreate):
    id: int
    class Config:
        orm_mode = True