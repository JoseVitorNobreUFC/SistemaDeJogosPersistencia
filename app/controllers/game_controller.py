from decimal import Decimal
from typing import Any, Dict
from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.database import get_db
from app.models.game_model import Game
from app.schemas.game_schema import GameCreate, GameModel
from app.schemas.pagination import PaginatedResponse
from app.services import game_service

router = APIRouter(prefix="/games", tags=["games"])

@router.post("/", response_model=GameModel, status_code=status.HTTP_201_CREATED)
async def create_game(game: GameCreate, db: AsyncSession = Depends(get_db)):
    return await game_service.create(db, game.model_dump())

@router.get("/", response_model=PaginatedResponse[GameModel])
async def list_games(
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

    return await game_service.paginated_list(db, page, limit, filters)

@router.get("/quantidade")
async def quantidade(db: AsyncSession = Depends(get_db)):
    return {"quantidade": await game_service.count(db)}

@router.get("/search", response_model=PaginatedResponse[GameModel])
async def search_game(
    field: str = Query(...),
    value: str = Query(...),
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    if not hasattr(Game, field):
        raise HTTPException(status_code=400, detail=f"Campo inválido: {field}")

    filters = {field: int(value) if value.isdigit() else value}
    return await game_service.paginated_list(db, page, limit, filters)


@router.get("/{game_id}", response_model=GameModel)
async def get_game(game_id: int, db: AsyncSession = Depends(get_db)):
    return await game_service.get(db, game_id)

@router.put("/{game_id}")
async def update_game(game_id: int, game: GameCreate, db: AsyncSession = Depends(get_db)):
    return await game_service.update(db, game_id, game.model_dump())

@router.delete("/{game_id}")
async def delete_game(game_id: int, db: AsyncSession = Depends(get_db)):
    return await game_service.delete(db, game_id)
