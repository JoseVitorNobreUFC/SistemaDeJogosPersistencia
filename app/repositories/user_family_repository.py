from decimal import Decimal
from typing import Any, Dict, List
from sqlalchemy import func, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_family_model import UserFamily

async def create(db: AsyncSession, data: Dict[str, Any]) -> UserFamily:
  res = await db.execute(select(UserFamily).where(UserFamily.user_id == data["usuario_id"]), UserFamily.family_id == data["familia_id"])
  if res.scalar_one_or_none():
    raise IntegrityError("Esse usuario já pertence a familia", params=None, orig="duplicated")
  
  obj = UserFamily(**data)
  db.add(obj)
  await db.commit()
  await db.refresh(obj)
  return obj

async def get(db: AsyncSession, user_id: int, family_id: int) -> UserFamily | None:
  res = await db.execute(select(UserFamily).where(UserFamily.user_id == user_id, UserFamily.family_id == family_id))
  return res.scalar_one_or_none()

async def list_(
    db: AsyncSession,
    skip: int,
    limit: int,
    filters: Dict[str, Any],
) -> List[UserFamily]:
  query = select(UserFamily)
  if id_ := filters.get("id"):
    query = query.where(UserFamily.id == id_)
  if user_id := filters.get("user_id"):
    query = query.where(UserFamily.user_id == user_id)
  if family_id := filters.get("family_id"):
    query = query.where(UserFamily.family_id == family_id)
  res = await db.execute(query.offset(skip).limit(limit))
  return res.scalars().all()

async def update_(db: AsyncSession, user_family_id: int, data: Dict[str, Any]) -> None:
  await db.execute(update(UserFamily).where(UserFamily.id == user_family_id).values(**data))
  await db.commit()

async def delete_(db: AsyncSession, user_family_id: int) -> None:
  await db.execute(delete(UserFamily).where(UserFamily.id == user_family_id))
  await db.commit()
  
async def count(db: AsyncSession) -> int:
  res = await db.execute(select(func.count()).select_from(UserFamily))
  return res.scalar_one()