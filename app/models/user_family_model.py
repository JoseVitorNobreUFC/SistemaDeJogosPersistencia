from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING: ## Para evitar importações circulares
    from app.models.user_model import User
    from app.models.family_model import Family

class UserFamily(Base):
    __tablename__ = "user_families"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    family_id: Mapped[int] = mapped_column(ForeignKey("families.id"), primary_key=True)

    user: Mapped["User"] = relationship(back_populates="family_associations")
    family: Mapped["Family"] = relationship(back_populates="user_associations")
