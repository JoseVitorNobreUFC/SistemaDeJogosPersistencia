from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

class DLCCreate(BaseModel):
    titulo: str
    descricao: Optional[str] = None
    data_lancamento: date
    preco: Decimal
    desenvolvedora: str
    jogo_id: int
class DLCModelId(DLCCreate):
    id: int
    class Config:
        orm_mode = True