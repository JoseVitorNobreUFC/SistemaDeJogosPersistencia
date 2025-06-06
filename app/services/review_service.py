import logging
from typing import Any, Dict
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import review_repository

logger = logging.getLogger("reviews")

async def create(db: AsyncSession, payload: Dict[str, Any]):
    obj = await review_repository.create(db, payload)
    logger.info("Review criada")
    return obj

async def get(db: AsyncSession, review_id: int):
    obj = await review_repository.get(db, review_id)
    if not obj:
        logger.error("Review não encontrada")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Review não encontrada")
    return obj

async def list_(
    db: AsyncSession,
    page: int,
    limit: int,
    filters: Dict[str, Any],
):
    skip = (page - 1) * limit
    return await review_repository.list_(db, skip, limit, filters)

async def update(db: AsyncSession, review_id: int, payload: Dict[str, Any]):
    await get(db, review_id)
    await review_repository.update_(db, review_id, payload)
    logger.info("Review atualizada")
    return {"message": "Review atualizada com sucesso"}

async def delete(db: AsyncSession, review_id: int):
    await get(db, review_id)
    await review_repository.delete_(db, review_id)
    logger.info("Review excluída")
    return {"message": "Review excluída com sucesso"}

async def count(db: AsyncSession):
    return await review_repository.count(db)
