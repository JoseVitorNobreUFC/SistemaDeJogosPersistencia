import logging
from typing import Any, Dict
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import purchase_repository
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("purchase")

async def create(db: AsyncSession, data: Dict[str, Any]):
  try:
    obj = await purchase_repository.create(db, data)
    logger.info("Compra criada")
    return obj
  except IntegrityError as e:
    if "duplicated purchase" in str(e.orig).lower():
      logger.error(f"Tentativa de comprar o mesmo jogo: {data.get('jogo_id'), data.get('usuario_id')}")
      raise HTTPException(
          status_code=status.HTTP_409_CONFLICT,
          detail="Este jogo ja foi comprado por esse usuario"
      )
    elif "jogo_id" in str(e.orig) and "not present in table" in str(e.orig):
      logger.error(f"Tentativa de criar review para jogo inexistente: {data.get('jogo_id')}")
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST, 
          detail="Não existe um jogo com este id"
      )
    elif "usuario_id" in str(e.orig) and "not present in table" in str(e.orig):
        logger.error(f"Tentativa de criar review para usuário inexistente: {data.get('usuario_id')}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Não existe um usuário com este id"
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Erro de integridade nos dados"
    )

async def get(db: AsyncSession, purchase_id: int):
  obj = await purchase_repository.get(db, purchase_id)
  if not obj:
    logger.error("Compra nao encontrada")
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Compra nao encontrada")
  return obj

async def list_(
    db: AsyncSession,
    page: int,
    limit: int,
    filters: Dict[str, Any],
):
  skip = (page - 1) * limit
  return await purchase_repository.list_(db, skip, limit, filters)

async def update(db: AsyncSession, purchase_id: int, data: Dict[str, Any]):
  await get(db, purchase_id)
  
  try:
    await purchase_repository.update_(db, purchase_id, data)
    logger.info("Compra atualizada")
    return {"message": "Compra atualizada com sucesso"}
  except IntegrityError as e:
    await db.rollback()
    if "duplicated purchase" in str(e.orig).lower():
      logger.error(f"Tentativa de comprar o mesmo jogo: {data.get('jogo_id'), data.get('usuario_id')}")
      raise HTTPException(
          status_code=status.HTTP_409_CONFLICT,
          detail="Tentando atualizar para um jogo ja comprado por esse usuario"
      )
    elif "jogo_id" in str(e.orig) and "not present in table" in str(e.orig):
      logger.error(f"Tentativa de criar review para jogo inexistente: {data.get('jogo_id')}")
      raise HTTPException(
          status_code=status.HTTP_400_BAD_REQUEST, 
          detail="Não existe um jogo com este id"
      )
    elif "usuario_id" in str(e.orig) and "not present in table" in str(e.orig):
        logger.error(f"Tentativa de criar review para usuário inexistente: {data.get('usuario_id')}")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Não existe um usuário com este id"
        )
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="Erro de integridade nos dados"
    )

async def delete(db: AsyncSession, purchase_id: int):
  await get(db, purchase_id)
  await purchase_repository.delete_(db, purchase_id)
  logger.info("Compra excluida")
  return {"message": "Compra excluida com sucesso"}

async def count(db: AsyncSession):
  return await purchase_repository.count(db)