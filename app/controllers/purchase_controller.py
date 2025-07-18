from decimal import Decimal
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.purchase_model import Purchase
from app.schemas.pagination import PaginatedResponse
from app.schemas.purchase_schema import PurchaseCreate, PurchaseModel
from app.services import purchase_service

router = APIRouter(prefix="/purchase", tags=["purchase"])

@router.post("/", response_model=PurchaseModel, status_code=status.HTTP_201_CREATED)
async def create_purchase(purchase: PurchaseCreate, db: AsyncSession = Depends(get_db)):
  return await purchase_service.create(db, purchase.model_dump())

@router.get("/", response_model=PaginatedResponse[PurchaseModel])
async def list_purchases(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    usuario_id: int | None = None,
    jogo_id: int | None = None,
    preco_min: Decimal | None = Query(None, alias="precoMin"),
    preco_max: Decimal | None = Query(None, alias="precoMax"),
    forma_pagamento: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    filters: Dict[str, Any] = {}
    if usuario_id is not None:
        filters["usuario_id"] = usuario_id
    if jogo_id is not None:
        filters["jogo_id"] = jogo_id
    if preco_min is not None:
        filters["preco_min"] = preco_min
    if preco_max is not None:
        filters["preco_max"] = preco_max
    if forma_pagamento is not None:
        filters["forma_pagamento"] = forma_pagamento

    items  = await purchase_service.list_(db, page, limit, filters)
    total  = await purchase_service.count_filtered(db, filters)

    return {
        "page":     page,
        "per_page": limit,
        "total":    total,
        "items":    items,
    }
  
@router.get("/quantidade")
async def quantidade(db: AsyncSession = Depends(get_db)):
    return {"quantidade": await purchase_service.count(db)}
  
@router.get("/search", response_model=PaginatedResponse[PurchaseModel])
async def search_purchase(
    field: str = Query(...),
    value: str = Query(...),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    if not hasattr(Purchase, field):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Campo inválido: {field}",
        )

    filters = {field: int(value) if value.isdigit() else value}
    return await purchase_service.paginated_list(db, page, limit, filters)

  
@router.get("/{purchase_id}", response_model=PurchaseModel)
async def get_purchase(purchase_id: int, db: AsyncSession = Depends(get_db)):
    return await purchase_service.get(db, purchase_id)
  
@router.put("/{purchase_id}")
async def update_purchase(purchase_id: int, purchase: PurchaseCreate, db: AsyncSession = Depends(get_db)):
    return await purchase_service.update(db, purchase_id, purchase.model_dump())
  
@router.delete("/{purchase_id}")
async def delete_purchase(purchase_id: int, db: AsyncSession = Depends(get_db)):
    return await purchase_service.delete(db, purchase_id)