from datetime import datetime

from sqlalchemy import DateTime, TIMESTAMP, func
from sqlalchemy.orm import Mapped, mapped_column

from src.models.base import BaseModel


class SpimexTradingResults(BaseModel):
    __tablename__ = "spimex_trading_results"

    exchange_product_id: Mapped[str]
    exchange_product_name: Mapped[str]
    oil_id: Mapped[str]
    delivery_basis_id: Mapped[str]
    delivery_basis_name: Mapped[str]
    delivery_type_id: Mapped[str]
    volume: Mapped[int]
    total: Mapped[int]
    count: Mapped[int]
    date: Mapped[datetime] = mapped_column(DateTime())
    created_on: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP,
        default=func.now(timezone=True),
    )
    updated_on: Mapped[TIMESTAMP] = mapped_column(
        TIMESTAMP,
        default=func.now(timezone=True),
        onupdate=func.now(timezone=True),
    )
