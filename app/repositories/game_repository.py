from decimal import Decimal
from typing import Any, Dict, List
from sqlalchemy import func, select, update, delete
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from app.models.game_model import Game

async def create(db: AsyncSession, data: Dict[str, Any]) -> Game:
    res = await db.execute(select(Game).where(Game.titulo == data["titulo"]))
    if res.scalar_one_or_none():
        raise IntegrityError("Título duplicado", params=None, orig="titulo")

    obj = Game(**data)
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

async def get(db: AsyncSession, game_id: int) -> Game | None:
    res = await db.execute(select(Game).where(Game.id == game_id))
    return res.scalar_one_or_none()

async def list_(
    db: AsyncSession,
    skip: int,
    limit: int,
    filters: Dict[str, Any],
) -> List[Game]:
    query = select(Game)
    if titulo := filters.get("titulo"):
        query = query.where(Game.titulo.ilike(f"%{titulo}%"))
    if dev := filters.get("desenvolvedora"):
        query = query.where(Game.desenvolvedora.ilike(f"%{dev}%"))
    preco_min: Decimal | None = filters.get("preco_min")
    preco_max: Decimal | None = filters.get("preco_max")
    if preco_min is not None:
        query = query.where(Game.preco >= preco_min)
    if preco_max is not None:
        query = query.where(Game.preco <= preco_max)
    res = await db.execute(query.offset(skip).limit(limit))
    return res.scalars().all()

async def update_(db: AsyncSession, game_id: int, data: Dict[str, Any]) -> None:
    await db.execute(update(Game).where(Game.id == game_id).values(**data))
    await db.commit()

async def delete_(db: AsyncSession, game_id: int) -> None:
    await db.execute(delete(Game).where(Game.id == game_id))
    await db.commit()

async def count(db: AsyncSession) -> int:
    res = await db.execute(select(func.count()).select_from(Game))
    return res.scalar_one()
