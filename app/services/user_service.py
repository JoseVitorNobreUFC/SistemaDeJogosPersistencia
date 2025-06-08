import logging
from typing import Any, Dict
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import user_repository

logger = logging.getLogger("users.service")

async def create(db: AsyncSession, payload: Dict[str, Any]):
    obj = await user_repository.create(db, payload)
    logger.info("User criado")
    return obj

async def get(db: AsyncSession, user_id: int):
    obj = await user_repository.get(db, user_id)
    if not obj:
        logger.error("User não encontrado")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User não encontrado")
    return obj

async def list_(
    db: AsyncSession,
    page: int,
    limit: int,
    filters: Dict[str, Any],
):
    skip = (page - 1) * limit
    return await user_repository.list_(db, skip, limit, filters)

async def update(db: AsyncSession, user_id: int, payload: Dict[str, Any]):
    await get(db, user_id)
    await user_repository.update_(db, user_id, payload)
    logger.info("User atualizado")
    return {"message": "User atualizado com sucesso"}

async def delete(db: AsyncSession, user_id: int):
    await get(db, user_id)
    await user_repository.delete_(db, user_id)
    logger.info("User excluido")
    return {"message": "User excluido com sucesso"}

async def count(db: AsyncSession):
    return await user_repository.count(db)
