from pydantic import BaseModel
from typing import Optional
from datetime import date, datetime
from decimal import Decimal

class PurchaseCreate(BaseModel):
  jogo_id: int
  usuario_id: int
  preco_pago: Decimal
  forma_pagamento: str
  data_compra: datetime

class PurchaseModel(PurchaseCreate):
  id: int
  class Config:
    orm_mode = True