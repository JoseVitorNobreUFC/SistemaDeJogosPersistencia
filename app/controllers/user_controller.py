from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.schemas.user_schema import UserCreate, UserModel
from app.services import user_service

router = APIRouter(prefix="/users", tags=["users"])

@router.post("/", response_model=UserModel, status_code=status.HTTP_201_CREATED)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.create(db, user.model_dump())

@router.get("/", response_model=list[UserModel])
async def list_users(
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    nome: str | None = None,
    email: str | None = None,
    pais: str | None = None,
    db: AsyncSession = Depends(get_db),
):
    filters: Dict[str, Any] = {}
    if nome:
        filters["nome"] = nome
    if email:
        filters["email"] = email
    if pais:
        filters["pais"] = pais
    return await user_service.list_(db, page, limit, filters)

@router.get("/quantidade")
async def quantidade_users(db: AsyncSession = Depends(get_db)):
    return {"quantidade": await user_service.count(db)}

@router.get("/search")
async def search_user(
    field: str = Query(...),
    value: str = Query(...),
    db: AsyncSession = Depends(get_db),
):
    if field not in {"nome", "email", "pais"}:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campo inválido")
    filters = {field: value}
    return await user_service.list_(db, 1, 1000, filters)

@router.get("/{user_id}", response_model=UserModel)
async def get_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await user_service.get(db, user_id)

@router.put("/{user_id}")
async def update_user(user_id: int, user: UserCreate, db: AsyncSession = Depends(get_db)):
    return await user_service.update(db, user_id, user.model_dump())

@router.delete("/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db)):
    return await user_service.delete(db, user_id)
