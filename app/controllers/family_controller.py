from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.family_model import Family
from app.schemas.pagination import PaginatedResponse
from app.schemas.family_schema import FamilyCreate, FamilyModel
from app.services import family_service

router = APIRouter(prefix="/family", tags=["family"])

@router.post("/", response_model=FamilyModel, status_code=status.HTTP_201_CREATED)
async def create_family(family: FamilyCreate, db: AsyncSession = Depends(get_db)):
  return await family_service.create(db, family.model_dump())

@router.get("/", response_model=PaginatedResponse[FamilyModel])
async def list_family(
  page: int = Query(1, gt=0),
  limit: int = Query(10, gt=0),
  nome: str | None = None,
  descricao: str | None = None,
  publicidade: str | None = None,
  db: AsyncSession = Depends(get_db),
) -> Dict[str, Any]:
  filters: Dict[str, Any] = {}
  if nome: filters["nome"] = nome
  if descricao: filters["descricao"] = descricao
  if publicidade: filters["publicidade"] = publicidade
  return await family_service.list(db, page, limit, filters)

@router.get("/quantidade")
async def get_family_quantity(db: AsyncSession = Depends(get_db)):
  return {"quantidade": await family_service.count(db)}

@router.get("/search", response_model=PaginatedResponse[FamilyModel])
async def search_family(
  field: str = Query(...),
  value: str = Query(...),
  page: int = Query(1, ge=1),
  limit: int = Query(10, ge=1, le=100),
  db: AsyncSession = Depends(get_db),
):
  if not hasattr(Family, field):
    raise HTTPException(status_code=400, detail=f"Campo inválido: {field}")

  filters = {field: int(value) if value.isdigit() else value}
  return await family_service.list(db, page, limit, filters)

@router.get("/{family_id}", response_model=FamilyModel)
async def get_family(family_id: int, db: AsyncSession = Depends(get_db)):
  return await family_service.get(db, family_id)

@router.put("/{family_id}", response_model=FamilyModel)
async def update_family(family_id: int, family: FamilyCreate, db: AsyncSession = Depends(get_db)):
  return await family_service.update(db, family_id, family.model_dump())

@router.delete("/{family_id}")
async def delete_family(family_id: int, db: AsyncSession = Depends(get_db)):
  return await family_service.delete(db, family_id)