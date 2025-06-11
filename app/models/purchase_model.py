from datetime import datetime, timezone
from sqlalchemy import Text, ForeignKey, DateTime, Float, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class Purchase(Base):
    __tablename__ = "purchase"
    __table_args__ = (
        UniqueConstraint("usuario_id", "jogo_id", name="purchase_usuario_jogo"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    usuario_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    jogo_id: Mapped[int] = mapped_column(ForeignKey("games.id"), nullable=False)
    preco_pago: Mapped[float] = mapped_column(Float, nullable=False)
    forma_pagamento: Mapped[str] = mapped_column(Text, nullable=False)
    data_compra: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
    )
