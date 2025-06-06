import logging
from typing import Any, Dict, List
from sqlalchemy import func, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import User

logger = logging.getLogger("users.repo")

async def create(db: AsyncSession, data: Dict[str, Any]) -> User:
    obj = User(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get(db: AsyncSession, user_id: int) -> User | None:
    res = await db.execute(select(User).where(User.id == user_id))
    return res.scalar_one_or_none()

async def list_(
    db: AsyncSession,
    skip: int,
    limit: int,
    filters: Dict[str, Any],
) -> List[User]:
    query = select(User)
    if nome := filters.get("nome"):
        query = query.where(User.nome.ilike(f"%{nome}%"))
    if email := filters.get("email"):
        query = query.where(User.email.ilike(f"%{email}%"))
    if pais := filters.get("pais"):
        query = query.where(User.pais.ilike(f"%{pais}%"))
    res = await db.execute(query.offset(skip).limit(limit))
    return res.scalars().all()

async def update_(db: AsyncSession, user_id: int, data: Dict[str, Any]) -> None:
    await db.execute(update(User).where(User.id == user_id).values(**data))
    await db.commit()

async def delete_(db: AsyncSession, user_id: int) -> None:
    await db.execute(delete(User).where(User.id == user_id))
    await db.commit()

async def count(db: AsyncSession) -> int:
    res = await db.execute(select(func.count()).select_from(User))
    return res.scalar_one()
