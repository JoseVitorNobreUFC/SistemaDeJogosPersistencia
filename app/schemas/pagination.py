from typing import Generic, TypeVar, List
from pydantic import BaseModel
from pydantic.generics import GenericModel

T = TypeVar("T")

class PaginatedResponse(GenericModel, Generic[T]):
    page: int
    per_page: int
    total: int
    items: List[T]

    class Config:
        orm_mode = True