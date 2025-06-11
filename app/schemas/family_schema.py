from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal
from datetime import datetime

class FamilyCreate(BaseModel): 
    nome: str
    descricao: Optional[str] = None
    publicidade: str
    criador_id: int
    data_criacao: datetime
    

class FamilyModel(FamilyCreate):
    id: int
    class Config:
        orm_mode = True