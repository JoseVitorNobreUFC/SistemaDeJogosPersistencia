from pydantic import BaseModel, conint

class UserFamilyCreate(BaseModel):
    usuario_id: int
    familia_id: int

class UserFamilyModel(UserFamilyCreate):
    id: int
    class Config:
        orm_mode = True
