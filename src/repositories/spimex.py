from datetime import datetime
from typing import Sequence

from sqlalchemy import select

from src.schemas.schemas import TradingResultDateSchema
from src.models.trade import SpimexTradingResults
from src.utils.repository import SqlAlchemyRepository


class SpimexRepository(SqlAlchemyRepository):
    """класс для работы репозитория чз модель."""

    model = SpimexTradingResults

    async def get_by_query_all_limit(self, limit: int) -> Sequence[type(model)]:
        query = select(self.model).distinct().limit(limit=limit)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_query_dates(self, limit: int) -> Sequence[type(model)]:
        query = (select(self.model.date)
                 .distinct().order_by(self.model.date.desc())
                 .limit(limit=limit))
        result = await self.session.execute(query)
        trades = result.scalars().all()

        return [TradingResultDateSchema(date=data) for data in trades]

    async def get_by_query_all(
            self,
            oil_id: str,
            delivery_type_id: str,
            delivery_basis_id: str,
    ) -> Sequence[type(model)]:
        query = (select(self.model)
                 .filter(self.model.oil_id == oil_id)
                 .filter(self.model.delivery_type_id == delivery_type_id)
                 .filter(self.model.delivery_basis_id == delivery_basis_id)
                 )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_query_all_dynamics(
            self,
            oil_id: str,
            delivery_type_id: str,
            delivery_basis_id: str,
            start_date: datetime,
            end_date: datetime,
    ) -> Sequence[type(model)]:
        query = (select(self.model)
                 .filter(self.model.oil_id == oil_id)
                 .filter(self.model.delivery_type_id == delivery_type_id)
                 .filter(self.model.delivery_basis_id == delivery_basis_id)
                 .filter(self.model.date >= start_date)
                 .filter(self.model.date <= end_date)
                 ).limit(30)
        result = await self.session.execute(query)
        return result.scalars().all()
