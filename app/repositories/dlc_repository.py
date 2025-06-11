from decimal import Decimal
from typing import Any, Dict, List
from sqlalchemy import Integer, Numeric, String, Text, func, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.dlc_model import DLCModel

async def create(db: AsyncSession, data: Dict[str, Any]) -> DLCModel:
  res = await db.execute(select(DLCModel).where(DLCModel.titulo == data["titulo"]))
  if res.scalar_one_or_none():
    raise IntegrityError("Título duplicado", params=None, orig="titulo")

  obj = DLCModel(**data)
  db.add(obj)
  await db.commit()
  await db.refresh(obj)
  return obj

async def get(db: AsyncSession, dlc_id: int) -> DLCModel | None:
    res = await db.execute(select(DLCModel).where(DLCModel.id == dlc_id))
    return res.scalar_one_or_none()
  
async def list_(
    db: AsyncSession,
    skip: int,
    limit: int,
    filters: Dict[str, Any],
) -> List[DLCModel]:
  query = select(DLCModel)
  if titulo := filters.get("titulo"):
    query = query.where(DLCModel.titulo.ilike(f"%{titulo}%"))
  if desenvolvedora := filters.get("desenvolvedora"):
    query = query.where(DLCModel.desenvolvedora.ilike(f"%{desenvolvedora}%"))
  preco_min: Decimal | None = filters.get("preco_min")
  preco_max: Decimal | None = filters.get("preco_max")
  if preco_min is not None:
    query = query.where(DLCModel.preco >= preco_min)
  if preco_max is not None:
    query = query.where(DLCModel.preco <= preco_max)
    
  for field, value in filters.items():
    if field in {"titulo", "desenvolvedora", "preco_min", "preco_max"}:
      continue

    column_attr = getattr(DLCModel, field, None)
    if column_attr is None:
      continue

    if isinstance(column_attr.type, (String, Text)):
      query = query.where(column_attr.ilike(f"%{value}%"))
    else:
      query = query.where(column_attr == value)
  res = await db.execute(query.offset(skip).limit(limit))
  return res.scalars().all()

async def count_filtered(db: AsyncSession, filters: Dict[str, Any]) -> int:
  query = select(func.count(DLCModel.id))

  if (preco_min := filters.get("preco_min")) is not None:
    query = query.where(DLCModel.preco >= Decimal(preco_min))
  if (preco_max := filters.get("preco_max")) is not None:
    query = query.where(DLCModel.preco <= Decimal(preco_max))

  for field, value in filters.items():
    if field in {"preco_min", "preco_max"}:
      continue
    column_attr = getattr(DLCModel, field, None)
    if column_attr is None:
      continue
    col_type = column_attr.type
    try:
      if isinstance(col_type, (String, Text)):
        query = query.where(column_attr.ilike(f"%{value}%"))
      elif isinstance(col_type, Integer):
        query = query.where(column_attr == int(value))
      elif isinstance(col_type, Numeric):
        query = query.where(column_attr == Decimal(value))
      else:
        query = query.where(column_attr == value)
    except Exception:
      continue

  result = await db.execute(query)
  return result.scalar_one()

async def update_(db: AsyncSession, dlc_id: int, data: Dict[str, Any]):
    await db.execute(update(DLCModel).where(DLCModel.id == dlc_id).values(**data))
    await db.commit()
    
async def delete_(db: AsyncSession, dlc_id: int) -> None:
    await db.execute(delete(DLCModel).where(DLCModel.id == dlc_id))
    await db.commit()
    
async def count_(db: AsyncSession) -> int:
    res = await db.execute(select(func.count()).select_from(DLCModel))
    return res.scalar_one()