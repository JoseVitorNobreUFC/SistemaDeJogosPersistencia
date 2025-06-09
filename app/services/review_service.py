import logging
from typing import Any, Dict
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import review_repository
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("reviews")

async def create(db: AsyncSession, payload: Dict[str, Any]):
    try:
        obj = await review_repository.create(db, payload)
        logger.info("Review criada")
        return obj
    except IntegrityError as e:
        if "jogo_id" in str(e.orig) and "not present in table" in str(e.orig):
            logger.error(f"Tentativa de criar review para jogo inexistente: {payload.get('jogo_id')}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Não existe um jogo com este id"
            )
        elif "usuario_id" in str(e.orig) and "not present in table" in str(e.orig):
            logger.error(f"Tentativa de criar review para usuário inexistente: {payload.get('usuario_id')}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Não existe um usuário com este id"
            )
        logger.error(f"Erro de integridade ao criar review: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade nos dados"
        )

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
    try:
        await review_repository.update_(db, review_id, payload)
        logger.info("Review atualizada")
        return {"message": "Review atualizada com sucesso"}
    except IntegrityError as e:
        await db.rollback()
        if "jogo_id" in str(e.orig) and "not present in table" in str(e.orig):
            logger.error(f"Tentativa de atualizar review para jogo inexistente: {payload.get('jogo_id')}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Não existe um jogo com este id"
            )
        elif "usuario_id" in str(e.orig) and "not present in table" in str(e.orig):
            logger.error(f"Tentativa de atualizar review para usuário inexistente: {payload.get('usuario_id')}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="Não existe um usuário com este id"
            )
        logger.error(f"Erro de integridade ao atualizar review: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade nos dados"
        )

async def delete(db: AsyncSession, review_id: int):
    await get(db, review_id)
    await review_repository.delete_(db, review_id)
    logger.info("Review excluída")
    return {"message": "Review excluída com sucesso"}

async def count(db: AsyncSession):
    return await review_repository.count(db)
