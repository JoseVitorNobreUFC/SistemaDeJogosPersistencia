import logging
from typing import Any, Dict
from fastapi import HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.repositories import user_family_repository
from sqlalchemy.exc import IntegrityError

logger = logging.getLogger("user_family")

async def create(db: AsyncSession, data: Dict[str, Any]) -> Any:
  try:
    obj = await user_family_repository.create(db, data)
    logger.info("Familia criada")
    return obj
  except IntegrityError as e:
    if "duplicated" in str(e.orig).lower():
      logger.error(f"Tentativa de atribuir membro a uma mesma familia: {data.get('familia_id')}")
      raise HTTPException(
        status_code=status.HTTP_409_CONFLICT, 
        detail="Esse membro já está na familia"
      )
    