from decimal import Decimal
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.dlc_model import DLCModel
from app.schemas.dlc_schema import DLCCreate, DLCModelId
from app.schemas.pagination import PaginatedResponse
from app.services import dlc_service

router = APIRouter(prefix="/dlcs", tags=["dlcs"])

@router.post("/", response_model=DLCModelId, status_code=status.HTTP_201_CREATED)
async def create_dlc(dlc: DLCCreate, db: AsyncSession = Depends(get_db)):
  return await dlc_service.create(db, dlc.model_dump())

@router.get("/", response_model=PaginatedResponse[DLCModelId])
async def list_dlcs(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    titulo: str | None = None,
    desenvolvedora: str | None = None,
    preco_min: Decimal | None = Query(None, alias="precoMin"),
    preco_max: Decimal | None = Query(None, alias="precoMax"),
    db:   AsyncSession = Depends(get_db),
):
    filters: Dict[str, Any] = {}
    if titulo:          filters["titulo"]         = titulo
    if desenvolvedora:  filters["desenvolvedora"] = desenvolvedora
    if preco_min is not None: filters["preco_min"] = preco_min
    if preco_max is not None: filters["preco_max"] = preco_max

    return await dlc_service.paginated_list(db, page, limit, filters)
  
@router.get("/quantidade")
async def quantidade(db: AsyncSession = Depends(get_db)):
    return {"quantidade": await dlc_service.count(db)}
  
@router.get("/search", response_model=PaginatedResponse[DLCModelId])
async def search_dlc(
    field: str = Query(...),
    value: str = Query(...),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    if not hasattr(DLC, field):
        raise HTTPException(status_code=400, detail=f"Campo inválido: {field}")

    filters = {field: int(value) if value.isdigit() else value}
    return await dlc_service.paginated_list(db, page, limit, filters)

@router.get("/{dlc_id}", response_model=DLCModelId)
async def get_dlc(dlc_id: int, db: AsyncSession = Depends(get_db)):
    return await dlc_service.get(db, dlc_id)

@router.put("/{dlc_id}")
async def update_dlc(dlc_id: int, dlc: DLCCreate, db: AsyncSession = Depends(get_db)):
    return await dlc_service.update(db, dlc_id, dlc.model_dump())

@router.delete("/{dlc_id}")
async def delete_dlc(dlc_id: int, db: AsyncSession = Depends(get_db)):
    return await dlc_service.delete(db, dlc_id)