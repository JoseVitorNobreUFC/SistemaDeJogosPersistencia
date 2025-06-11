from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import inspect
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.review_model import Review
from app.schemas.review_schema import ReviewCreate, ReviewModel
from app.services import review_service

router = APIRouter(prefix="/reviews", tags=["reviews"])

@router.post("/", response_model=ReviewModel, status_code=status.HTTP_201_CREATED)
async def create_review(review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    return await review_service.create(db, review.model_dump())

@router.get("/", response_model=list[ReviewModel])
async def list_reviews(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    usuario_id: int | None = None,
    jogo_id: int | None = None,
    nota_min: int | None = Query(None, ge=1, le=10),
    nota_max: int | None = Query(None, ge=1, le=10),
    db: AsyncSession = Depends(get_db),
):
    filters: Dict[str, Any] = {}
    if usuario_id is not None:
        filters["usuario_id"] = usuario_id
    if jogo_id is not None:
        filters["jogo_id"] = jogo_id
    if nota_min is not None:
        filters["nota_min"] = nota_min
    if nota_max is not None:
        filters["nota_max"] = nota_max
    return await review_service.list_(db, page, limit, filters)

@router.get("/quantidade")
async def quantidade_reviews(db: AsyncSession = Depends(get_db)):
    return {"quantidade": await review_service.count(db)}

@router.get("/search")
async def search_review(
    field: str = Query(...),
    value: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    mapper = inspect(Review)
    if field not in mapper.columns:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Campo inválido: {field}"
        )

    column = mapper.columns[field]

    python_type = column.type.python_type
    try:
        typed_value = python_type(value)
    except (ValueError, TypeError):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Valor inválido para o tipo do campo {field}"
        )

    filters = {field: typed_value}
    return await review_service.list_(db, page=1, limit=1000, filters=filters)

@router.get("/{review_id}", response_model=ReviewModel)
async def get_review(review_id: int, db: AsyncSession = Depends(get_db)):
    return await review_service.get(db, review_id)

@router.put("/{review_id}")
async def update_review(review_id: int, review: ReviewCreate, db: AsyncSession = Depends(get_db)):
    return await review_service.update(db, review_id, review.model_dump())

@router.delete("/{review_id}")
async def delete_review(review_id: int, db: AsyncSession = Depends(get_db)):
    return await review_service.delete(db, review_id)
