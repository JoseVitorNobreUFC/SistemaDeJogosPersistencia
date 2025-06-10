from pydantic import BaseModel
from typing import Optional
from datetime import date
from decimal import Decimal

class PurchaseCreate(BaseModel):
  jogo_id: int
  usuario_id: int
  preco_pago: Decimal
  forma_pagamento: str
  data_compra: date

class PurchaseModel(PurchaseCreate):
  id: int
  class Config:
    orm_mode = True