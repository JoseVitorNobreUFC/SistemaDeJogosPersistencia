from datetime import date
from decimal import Decimal
from sqlalchemy import Date, Numeric, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base
from typing import List
from app.models.user_model import User
from app.models.family_model import Family

class UserFamily(Base):
    __tablename__ = "user_families"

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), primary_key=True)
    family_id: Mapped[int] = mapped_column(ForeignKey("family.id"), primary_key=True)

    # Relacionamentos (opcional, se quiser acessar diretamente)
    user: Mapped["User"] = relationship(back_populates="family_associations")
    family: Mapped["Family"] = relationship(back_populates="user_associations")