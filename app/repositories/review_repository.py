from decimal import Decimal
from typing import Any, Dict, List
from sqlalchemy import func, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.review_model import Review

async def create(db: AsyncSession, data: Dict[str, Any]) -> Review:
    obj = Review(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get(db: AsyncSession, review_id: int) -> Review | None:
    res = await db.execute(select(Review).where(Review.id == review_id))
    return res.scalar_one_or_none()

async def list_(
    db: AsyncSession,
    skip: int,
    limit: int,
    filters: Dict[str, Any],
) -> List[Review]:
    query = select(Review)
    if usuario_id := filters.get("usuario_id"):
        query = query.where(Review.usuario_id == usuario_id)
    if jogo_id := filters.get("jogo_id"):
        query = query.where(Review.jogo_id == jogo_id)
    if nota_min := filters.get("nota_min"):
        query = query.where(Review.nota >= nota_min)
    if nota_max := filters.get("nota_max"):
        query = query.where(Review.nota <= nota_max)
    res = await db.execute(query.offset(skip).limit(limit))
    return res.scalars().all()

async def update_(db: AsyncSession, review_id: int, data: Dict[str, Any]) -> None:
    await db.execute(update(Review).where(Review.id == review_id).values(**data))
    await db.commit()

async def delete_(db: AsyncSession, review_id: int) -> None:
    await db.execute(delete(Review).where(Review.id == review_id))
    await db.commit()

async def count(db: AsyncSession) -> int:
    res = await db.execute(select(func.count()).select_from(Review))
    return res.scalar_one()
