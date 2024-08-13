from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any, Never

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.schemas.schemas import TradingResultDateSchema


class AbstractRepository(ABC):

    @abstractmethod
    async def find_all(self):
        raise NotImplementedError

    @abstractmethod
    async def get_by_query_all_limit(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_by_query_all_limit(self, limit: int) -> Sequence[type(model)]:
        query = select(self.model).distinct().limit(limit=limit)
        result = await self.session.execute(query)
        res = result.scalars().all()

        return res

    async def get_by_query_dates(self, limit: int) -> Sequence[type(model)]:
        query = select(self.model.date).distinct().order_by(self.model.date.desc()).limit(limit=limit)
        result = await self.session.execute(query)
        trades = result.scalars().all()

        return [TradingResultDateSchema(date=data) for data in trades]

    async def get_by_query_all(self,
                               oil_id: str,
                               #delivery_type_id: str,
                               #delivery_basis_id: str
                               ) -> Sequence[type(model)]:
        query = (select(self.model)
                 .filter(self.model.oil_id == oil_id)
                 # .filter(SpimexTradingResults.delivery_type_id == delivery_type_id)
                 # .filter(SpimexTradingResults.delivery_basis_id == delivery_basis_id)
                 )
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_by_query_all_dynamics(self,
                                        oil_id: str,
                                        #delivery_type_id: str,
                                        #delivery_basis_id: str,
                                        #start_date: datetime,
                                        #end_date: datetime
                                        ) -> Sequence[type(model)]:
            query = (select(self.model)
                     .filter(self.model.oil_id == oil_id)
                     #.filter(SpimexTradingResults.delivery_type_id == delivery_type_id)
                     #.filter(SpimexTradingResults.delivery_basis_id == delivery_basis_id)
                     #.filter(SpimexTradingResults.date >= start_date)
                     #.filter(SpimexTradingResults.date <= end_date)
                     ).limit(30)
            result = await self.session.execute(query)
            trades = result.scalars().all()
            return trades

    async def find_all(self):
        pass
