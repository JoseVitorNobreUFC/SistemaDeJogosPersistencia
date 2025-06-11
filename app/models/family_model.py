from datetime import datetime, timezone
from sqlalchemy import DateTime, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import List, TYPE_CHECKING

if TYPE_CHECKING: ## Para evitar importações circulares
    from app.models.user_model import User
    from app.models.user_family_model import UserFamily

class Family(Base):
    __tablename__ = "families"

    id: Mapped[int] = mapped_column(primary_key=True)
    nome: Mapped[str] = mapped_column(String(100))
    data_criacao: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
    descricao: Mapped[str | None] = mapped_column(Text)
    criador_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    publicidade: Mapped[str] = mapped_column(String(100))

    members: Mapped[List["User"]] = relationship(
        secondary="user_families",
        back_populates="families"
    )

    user_associations: Mapped[List["UserFamily"]] = relationship(
        back_populates="family"
    )
