from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

class GameCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    data_lancamento: date
    preco: Decimal
    desenvolvedora: str

class GameModel(GameCreate):
    id: int
    class Config:
        orm_mode = True