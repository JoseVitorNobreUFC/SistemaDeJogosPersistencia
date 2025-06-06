from datetime import datetime
from typing import Optional, Annotated
from pydantic import BaseModel, conint

class ReviewCreate(BaseModel):
    usuario_id: int
    jogo_id: int
    nota: Annotated[int, conint(ge=1, le=10)]
    comentario: Optional[str] = None

class ReviewModel(ReviewCreate):
    id: int
    data_avaliacao: datetime

    class Config:
        orm_mode = True
