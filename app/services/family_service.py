import logging
from typing import Any, Dict
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import family_repository
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("family")

async def create(db: AsyncSession, data: Dict[str, Any]) -> Any:
  try:
    obj = await family_repository.create(db, data)
    logger.info("Familia criada")
    return obj
  except IntegrityError as e:
    if "criador_id" in str(e.orig).lower():
      logger.error(f"Não é possivel ser o criador de mais de uma familia")
      raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail="Não é possivel ser o criador de mais de uma familia"
      )
    elif "publicity error" in str(e.orig).lower():
      logger.error(f"Familia deve ter uma publicidade valida")
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Publicidade deve ser public ou private"
      )
    else:
      logger.error(f"Erro de integridade ao criar familia: {str(e)}")
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=e.orig
      )

async def get(db: AsyncSession, family_id: int) -> Any:
  obj = await family_repository.get(db, family_id)
  if not obj:
    logger.error("Familia não encontrada")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Familia não encontrada")
  return obj

async def list_(db: AsyncSession, page: int, limit: int, filters: dict = {}):
  query = select(Family)
  count_query = select(func.count()).select_from(Family)

  for field, value in filters.items():
    column_attr = getattr(Family, field, None)
    if column_attr is not None:
      condition = column_attr.ilike(f"%{value}%") if field == "name" else column_attr == value
      query = query.where(condition)
      count_query = count_query.where(condition)

  total = (await db.execute(count_query)).scalar_one()
  query = query.limit(limit).offset((page - 1) * limit)
  result = await db.execute(query)
  items = result.scalars().all()

  return {
    "page": page,
    "per_page": limit,
    "total": total,
    "items": items,
  }
  
async def update(db: AsyncSession, family_id: int, data: Dict[str, Any]):
  await get(db, family_id)
  try:
    await family_repository.update(db, family_id, data)
    logger.info("Familia atualizada")
    return {"message": "Familia atualizada com sucesso"}
  except IntegrityError as e:
    await db.rollback()
    if "criador_id" in str(e.orig).lower():
      logger.error(f"Não é possivel ser o criador de mais de uma familia")
      raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail="Não é possivel ser o criador de mais de uma familia"
      )
    elif "publicity error" in str(e.orig).lower():
      logger.error(f"Familia deve ter uma publicidade valida")
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Publicidade deve ser public ou private"
      )
    else:
      logger.error(f"Erro de integridade ao criar familia: {str(e)}")
      raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=e.orig
      )
      
async def delete(db: AsyncSession, family_id: int):
  await get(db, family_id)
  await family_repository.delete(db, family_id)
  logger.info("Familia excluída")
  return {"message": "Familia excluída com sucesso"}

async def count(db: AsyncSession):
  return await family_repository.count(db)