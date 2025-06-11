from datetime import datetime
import logging
from typing import Any, Dict
from fastapi import HTTPException, status
from sqlalchemy import DateTime, Integer, String, Text, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.user_model import User
from app.repositories import user_repository
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("users.service")

async def create(db: AsyncSession, payload: Dict[str, Any]):
    try:
        obj = await user_repository.create(db, payload)
        logger.info("User criado")
        return obj
    except IntegrityError as e:
        await db.rollback()
        error_msg = str(e.orig).lower()
        if "email" in error_msg or "unique constraint" in error_msg:
            logger.error(f"Tentativa de criar usuário com email duplicado: {payload.get('email')}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Já existe um usuário com este email"
            )
        logger.error(f"Erro de integridade ao criar usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade nos dados fornecidos"
        )
    except ValueError as e:
        logger.error(f"Erro de validação: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )
    except Exception as e:
        logger.error(f"Erro inesperado ao criar usuário: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Erro interno do servidor"
        )

async def get(db: AsyncSession, user_id: int):
    obj = await user_repository.get(db, user_id)
    if not obj:
        logger.error("User não encontrado")
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User não encontrado")
    return obj

async def list_(db: AsyncSession, page: int, limit: int, filters: dict = {}):
    query = select(User)

    for field, value in filters.items():
        column_attr = getattr(User, field, None)
        if column_attr is not None:
            col_type = column_attr.type
            try:
                if isinstance(col_type, (String, Text)):
                    query = query.where(column_attr.ilike(f"%{value}%"))
                elif isinstance(col_type, Integer):
                    query = query.where(column_attr == int(value))
                elif isinstance(col_type, DateTime):
                    query = query.where(column_attr == datetime.fromisoformat(value))
                else:
                    query = query.where(column_attr == value)
            except Exception:
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
    skip   = (page - 1) * limit
    items  = await user_repository.list_(db, skip, limit, filters)
    total  = await user_repository.count_filtered(db, filters)

    return {
        "items":     items,
        "page":      page,
        "per_page":  limit,
        "total":     total,
    }


async def update(db: AsyncSession, user_id: int, payload: Dict[str, Any]):
    await get(db, user_id)
    try:
        await user_repository.update_(db, user_id, payload)
        logger.info("User atualizado")
        return {"message": "User atualizado com sucesso"}
    except IntegrityError as e:
        await db.rollback()
        error_msg = str(e.orig).lower()
        if "email" in error_msg or "unique constraint" in error_msg:
            logger.error(f"Tentativa de atualizar usuário para email duplicado: {payload.get('email')}")
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, 
                detail="Já existe um usuário com este email"
            )
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Erro de integridade nos dados fornecidos"
        )

async def delete(db: AsyncSession, user_id: int):
    await get(db, user_id)
    await user_repository.delete_(db, user_id)
    logger.info("User excluido")
    return {"message": "User excluido com sucesso"}

async def count(db: AsyncSession):
    return await user_repository.count(db)
