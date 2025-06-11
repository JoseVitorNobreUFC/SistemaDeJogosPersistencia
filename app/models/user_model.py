from datetime import datetime, timezone
from sqlalchemy import String, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING: ## Para evitar importações circulares
    from app.models.user_family_model import UserFamily
    from app.models.family_model import Family

class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    nome: Mapped[str] = mapped_column(String(100), index=True)
    email: Mapped[str] = mapped_column(String(120), unique=True, index=True)
    senha_hash: Mapped[str] = mapped_column(String(255))
    data_cadastro: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    pais: Mapped[str] = mapped_column(String(60))

    families: Mapped[List["Family"]] = relationship(
        secondary="user_families",
        back_populates="members"
    )

    family_associations: Mapped[List["UserFamily"]] = relationship(
        back_populates="user"
    )
