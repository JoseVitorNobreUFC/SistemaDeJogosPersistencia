from datetime import date
from decimal import Decimal
import logging
from typing import Any, Dict
from fastapi import HTTPException, status
from sqlalchemy import Date, Integer, Numeric, String, Text, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.game_model import Game
from app.repositories import game_repository
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("games")

async def create(db: AsyncSession, payload: Dict[str, Any]):
    try:
        obj = await game_repository.create(db, payload)
        logger.info("Game criado")
        return obj
    except IntegrityError as e:
        if "titulo" in str(e.orig) or "unique constraint" in str(e.orig).lower():
            logger.error(f"Tentativa de criar game com título duplicado: {payload.get('titulo')}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Já existe um game com este título"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade nos dados"
        )

async def get(db: AsyncSession, game_id: int):
    obj = await game_repository.get(db, game_id)
    if not obj:
        logger.error("Game não encontrado")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Game não encontrado")
    return obj

async def list_(db: AsyncSession, page: int, limit: int, filters: dict = {}):
    query = select(Game)

    for field, value in filters.items():
        column_attr = getattr(Game, field, None)
        if column_attr is not None:
            col_type = column_attr.type
            try:
                if isinstance(col_type, (String, Text)):
                    query = query.where(column_attr.ilike(f"%{value}%"))
                elif isinstance(col_type, Integer):
                    query = query.where(column_attr == int(value))
                elif isinstance(col_type, Numeric):
                    query = query.where(column_attr == Decimal(value))
                elif isinstance(col_type, Date):
                    query = query.where(column_attr == date.fromisoformat(value))
                else:
                    query = query.where(column_attr == value)
            except Exception as e:
                # Log se necessário
                continue

    query = query.limit(limit).offset((page - 1) * limit)
    result = await db.execute(query)
    return result.scalars().all()

async def paginated_list(
    db: AsyncSession,
    page: int,
    limit: int,
    filters: Dict[str, Any],
):
    skip  = (page - 1) * limit
    items = await game_repository.list_(db, skip, limit, filters)
    total = await game_repository.count_filtered(db, filters)

    return {
        "items":     items,
        "page":      page,
        "per_page":  limit,
        "total":     total,
    }

async def update(db: AsyncSession, game_id: int, payload: Dict[str, Any]):
    await get(db, game_id)
    
    try:
        await game_repository.update_(db, game_id, payload)
        logger.info("Game atualizado")
        return {"message": "Game atualizado com sucesso"}
    except IntegrityError as e:
        await db.rollback()
        if "titulo" in str(e.orig) or "unique constraint" in str(e.orig).lower():
            logger.error(f"Tentativa de atualizar game para título duplicado: {payload.get('titulo')}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Já existe um game com este título"
            )
        
        logger.error(f"Erro de integridade ao atualizar game: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade nos dados"
        )
    except Exception as e:
        logger.error(f"Erro inesperado ao atualizar game: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

async def delete(db: AsyncSession, game_id: int):
    await get(db, game_id)
    await game_repository.delete_(db, game_id)
    logger.info("Game excluido")
    return {"message": "Game excluido com sucesso"}

async def count(db: AsyncSession):
    return await game_repository.count(db)
