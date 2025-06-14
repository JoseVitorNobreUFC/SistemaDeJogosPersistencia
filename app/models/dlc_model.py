from datetime import date
from decimal import Decimal
from sqlalchemy import Date, Numeric, String, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from app.database import Base

class DLCModel(Base):
    __tablename__ = "dlc"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    titulo: Mapped[str] = mapped_column(String(100), unique=True, index=True)
    descricao: Mapped[str | None] = mapped_column(Text)
    data_lancamento: Mapped[date] = mapped_column(Date)
    preco: Mapped[Decimal] = mapped_column(Numeric(10, 2))
    desenvolvedora: Mapped[str] = mapped_column(String(100))    
    jogo_id: Mapped[int] = mapped_column(ForeignKey("games.id"), nullable=False, unique=True)
