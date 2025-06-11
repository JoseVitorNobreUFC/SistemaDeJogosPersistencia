from datetime import date
from decimal import Decimal
import logging
from typing import Any, Dict
from fastapi import HTTPException, status
from sqlalchemy import Date, Integer, Numeric, String, Text, select
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.dlc_model import DLCModel
from app.repositories import dlc_repository
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("dlcs")

async def create(db: AsyncSession, data: Dict[str, Any]):
  try:
    obj = await dlc_repository.create(db, data)
    logger.info("DLC criado")
    return obj
  except IntegrityError as e:
    if "titulo" in str(e.orig):
      logger.error(f"Tentativa de criar DLC com título duplicado: {data.get('titulo')}")
      raise HTTPException(
          status_code=status.HTTP_409_CONFLICT, 
          detail="Já existe um DLC com este título"
      )
    if "jogo_id" in str(e.orig) and "not present in table" in str(e.orig):
      logger.error(f"Tentativa de criar DLC para jogo inexistente: {data.get('jogo_id')}")
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST, 
          detail="Não existe um jogo com este id"
      )
    if "jogo_id" in str(e.orig) and "unique constraint" in str(e.orig).lower():
      logger.error(f"Tentativa de criar DLC para jogo inexistente: {data.get('jogo_id')}")
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST, 
          detail="Já existe um DLC para este jogo"
      )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Erro de integridade nos dados"
    )
    
async def get(db: AsyncSession, dlc_id: int):
  obj = await dlc_repository.get(db, dlc_id)
  if not obj:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="DLC nao encontrado"
    )
  return obj

async def list_(db: AsyncSession, page: int, limit: int, filters: dict = {}):
  query = select(DLCModel)

  for field, value in filters.items():
        column_attr = getattr(DLCModel, field, None)
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
  items = await dlc_repository.list_(db, skip, limit, filters)
  total = await dlc_repository.count_filtered(db, filters)

  return {
      "items":     items,
      "page":      page,
      "per_page":  limit,
      "total":     total,
  }
  
async def update(db: AsyncSession, dlc_id: int, data: Dict[str, Any]):
  await get(db, dlc_id)
  
  try:
    await dlc_repository.update_(db, dlc_id, data)
    logger.info("DLC atualizado")
    return {"message": "DLC atualizado com sucesso"}
  except IntegrityError as e:
    await db.rollback()
    if "titulo" in str(e.orig) or "unique constraint" in str(e.orig).lower():
      logger.error(f"Tentativa de criar DLC com título duplicado: {data.get('titulo')}")
      raise HTTPException(
          status_code=status.HTTP_409_CONFLICT, 
          detail="Já existe um DLC com este título"
      )
    if "jogo_id" in str(e.orig) and "not present in table" in str(e.orig):
      logger.error(f"Tentativa de criar DLC para jogo inexistente: {data.get('jogo_id')}")
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST, 
          detail="Não existe um jogo com este id"
      )
    if "jogo_id" in str(e.orig) and "unique constraint" in str(e.orig).lower():
      logger.error(f"Tentativa de criar DLC para jogo inexistente: {data.get('jogo_id')}")
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST, 
          detail="Já existe um DLC para este jogo"
      )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Erro de integridade nos dados"
    )
    
async def delete(db: AsyncSession, dlc_id: int):
  await get(db, dlc_id)
  await dlc_repository.delete_(db, dlc_id)
  logger.info("DLC deletado")
  return {"message": "DLC deletado com sucesso"}

async def count(db: AsyncSession):
  return await dlc_repository.count_(db)