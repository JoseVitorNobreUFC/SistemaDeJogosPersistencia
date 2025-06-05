import logging
from typing import Any, Dict

from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import game_repository

logger = logging.getLogger("games")

async def create(db: AsyncSession, payload: Dict[str, Any]):
    obj = await game_repository.create(db, payload)
    logger.info("Game criado")
    return obj

async def get(db: AsyncSession, game_id: int):
    obj = await game_repository.get(db, game_id)
    if not obj:
        logger.error("Game não encontrado")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game não encontrado")
    return obj

async def list_(
    db: AsyncSession,
    page: int,
    limit: int,
    filters: Dict[str, Any],
):
    skip = (page - 1) * limit
    return await game_repository.list_(db, skip, limit, filters)

async def update(db: AsyncSession, game_id: int, payload: Dict[str, Any]):
    await get(db, game_id)
    await game_repository.update_(db, game_id, payload)
    logger.info("Game atualizado")
    return {"message": "Game atualizado com sucesso"}

async def delete(db: AsyncSession, game_id: int):
    await get(db, game_id)
    await game_repository.delete_(db, game_id)
    logger.info("Game excluido")
    return {"message": "Game excluido com sucesso"}

async def count(db: AsyncSession):
    return await game_repository.count(db)
