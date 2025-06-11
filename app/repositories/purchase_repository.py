from datetime import datetime
from decimal import Decimal
from typing import Any, Dict, List
from sqlalchemy import DateTime, Numeric, String, Text, func, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.purchase_model import Purchase
from app.models.game_model import Game

async def create(db: AsyncSession, data: Dict[str, Any]) -> Purchase:
  res = await db.execute(select(Purchase).where(Purchase.jogo_id == data["jogo_id"], Purchase.usuario_id == data["usuario_id"])) 
  if res.first() is not None:
    raise IntegrityError("Compra duplicada", params=None, orig="duplicated purchase")

  jogo_res = await db.execute(select(Game).where(Game.id == data["jogo_id"]))
  jogo = jogo_res.scalar_one_or_none()

  if not jogo:
    raise IntegrityError("Jogo inexistente", params=None, orig="jogo_id not present")

  if data["preco_pago"] > jogo.preco:
    raise IntegrityError("Preco pago maior que o preco do jogo", params=None, orig="price too high")
  obj = Purchase(**data)
  db.add(obj)
  await db.commit()
  await db.refresh(obj)
  return obj

async def get(db: AsyncSession, purchase_id: int) -> Purchase | None:
  res = await db.execute(select(Purchase).where(Purchase.id == purchase_id))
  return res.scalar_one_or_none()

async def list_(
    db: AsyncSession,
    skip: int,
    limit: int,
    filters: Dict[str, Any],
) -> List[Purchase]:
  query = select(Purchase)
  if id_ := filters.get("id"):
    query = query.where(Purchase.id == id_)
  if jogo_id := filters.get("jogo_id"):
    query = query.where(Purchase.jogo_id == jogo_id)
  if usuario_id := filters.get("usuario_id"):
    query = query.where(Purchase.usuario_id == usuario_id)
  if preco_min := filters.get("preco_min"):
    query = query.where(Purchase.preco >= preco_min)
  if preco_max := filters.get("preco_max"):
    query = query.where(Purchase.preco <= preco_max)
  if preco := filters.get("preco"):
    query = query.where(Purchase.preco.like(f"%{preco}%"))
  if forma_pagamento := filters.get("forma_pagamento"):
    query = query.where(Purchase.forma_pagamento.like(f"%{forma_pagamento}%"))
  if data_compra := filters.get("data_compra"):
    query = query.where(Purchase.data_compra.like(f"%{data_compra}%"))
  res = await db.execute(query.offset(skip).limit(limit))
  return res.scalars().all()

async def count_filtered(
    db: AsyncSession,
    filters: Dict[str, Any],
) -> int:
    query = select(func.count(Purchase.id))

    if (preco_min := filters.get("preco_min")) is not None:
        query = query.where(Purchase.preco_pago >= Decimal(preco_min))
    if (preco_max := filters.get("preco_max")) is not None:
        query = query.where(Purchase.preco_pago <= Decimal(preco_max))

    for field, value in filters.items():
        if field in {"preco_min", "preco_max"}:
            continue
        column_attr = getattr(Purchase, field, None)
        if column_attr is None:
            continue
        col_type = column_attr.type
        try:
            if isinstance(col_type, (String, Text)):
                query = query.where(column_attr.ilike(f"%{value}%"))
            elif col_type.python_type is int:
                query = query.where(column_attr == int(value))
            elif isinstance(col_type, Numeric):
                query = query.where(column_attr == Decimal(value))
            elif isinstance(col_type, DateTime):
                query = query.where(
                    column_attr == datetime.fromisoformat(str(value))
                )
            else:
                query = query.where(column_attr == value)
        except Exception:
            continue

    result = await db.execute(query)
    return result.scalar_one()

async def update_(db: AsyncSession, purchase_id: int, data: Dict[str, Any]) -> None:
  await db.execute(update(Purchase).where(Purchase.id == purchase_id).values(**data))
  await db.commit()

async def delete_(db: AsyncSession, purchase_id: int) -> None:
  await db.execute(delete(Purchase).where(Purchase.id == purchase_id))
  await db.commit()

async def count(db: AsyncSession) -> int:
  res = await db.execute(select(func.count(Purchase.id)))
  return res.scalar()