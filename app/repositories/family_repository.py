from decimal import Decimal
from typing import Any, Dict, List
from sqlalchemy import func, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.family_model import Family

async def create(db: AsyncSession, data: Dict[str, Any]) -> Family:
  res = await db.execute(select(Family).where(Family.name == data["criador_id"]))
  if res.scalar_one_or_none():
    raise IntegrityError("Um usuario não pode ser o dono de mais de uma familia", params=None, orig="criador_id")
  
  if data.get("publicidade") not in {"public", "private"}:
    raise IntegrityError("Familia deve ter uma publicidade valida", params=None, orig="publicity error")
  
  obj = Family(**data)
  db.add(obj)
  await db.commit()
  await db.refresh(obj)
  return obj

async def get(db: AsyncSession, family_id: int) -> Family | None:
  res = await db.execute(select(Family).where(Family.id == family_id))
  return res.scalar_one_or_none()

async def list_(
    db: AsyncSession,
    skip: int,
    limit: int,
    filters: Dict[str, Any],
) -> List[Family]:
  query = select(Family)
  if id_ := filters.get("id"):
    query = query.where(Family.id == id_)
  if name := filters.get("name"):
    query = query.where(Family.name.ilike(f"%{name}%"))
  if descricao := filters.get("descricao"):
    query = query.where(Family.descricao.ilike(f"%{descricao}%"))
  if publicidade := filters.get("publicidade"):
    query = query.where(Family.publicity == publicidade)
  if criador_id := filters.get("criador_id"):
    query = query.where(Family.criador_id == criador_id)
  if data_criacao := filters.get("data_criacao"):
    query = query.where(Family.data_criacao == data_criacao)
  res = await db.execute(query.offset(skip).limit(limit))
  return res.scalars().all()

async def update_(db: AsyncSession, family_id: int, data: Dict[str, Any]) -> None:
  await db.execute(update(Family).where(Family.id == family_id).values(**data))
  await db.commit()

async def delete_(db: AsyncSession, family_id: int) -> None:
  await db.execute(delete(Family).where(Family.id == family_id))
  await db.commit()
  
async def count(db: AsyncSession) -> int:
  res = await db.execute(select(func.count()).select_from(Family))
  return res.scalar_one()