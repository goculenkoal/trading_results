from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime
from pyexpat import model
from typing import Any, Never

from sqlalchemy import select, Result
from sqlalchemy.ext.asyncio import AsyncSession

from database import async_session_maker
from src.schemas.schemas import TradingResultDateSchema


class AbstractRepository(ABC):

    # @abstractmethod
    # async def add_one(self):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # async def find_all(self):
    #     raise NotImplementedError

    @abstractmethod
    async def get_by_query_all_limit(self, *args: Any, **kwargs: Any) -> Never:
        raise NotImplementedError


class SqlAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession) -> None:
        self.session = session
    # @abstractmethod
    # async def add_one(self):
    #     raise NotImplementedError
    #
    # @abstractmethod
    # async def find_all(self):
    #     raise NotImplementedError

    async def get_by_query_all_limit(self, limit: int) -> Sequence[type(model)]:
            query = select(self.model).distinct().limit(limit=limit)
            result = await self.session.execute(query)
            res = result.scalars().all()
            return res

    async def get_by_query_last_trades(self,
                                       oil_id: str,
                                       #delivery_type_id: str,
                                       #delivery_basis_id: str
                                       ) -> Sequence[type(model)]:
        async with async_session_maker() as session:
            query = (select(self.model)
                     .filter(self.model.oil_id == oil_id)
                     # .filter(SpimexTradingResults.delivery_type_id == delivery_type_id)
                     # .filter(SpimexTradingResults.delivery_basis_id == delivery_basis_id)
                     )
            result = await session.execute(query)
            return result.scalars().all()

    async def get_by_query_dates(self, limit: int) -> Sequence[type(model)]:
        async with async_session_maker() as session:
            query = select(self.model.date).distinct().order_by(self.model.date.desc()).limit(limit=limit)
            # print(query)
            result = await session.execute(query)
            trades = result.scalars().all()
            # print(f'TRADES: {trades}')

            return [TradingResultDateSchema(date=data) for data in trades]

    async def get_by_query_dynamics(self,
                                    oil_id: str,
                                    #delivery_type_id: str,
                                    #delivery_basis_id: str,
                                    #start_date: datetime,
                                    #end_date: datetime
                                    ) -> Sequence[type(model)]:
        async with async_session_maker() as session:
            query = (select(self.model)
                     .filter(self.model.oil_id == oil_id)
                     #.filter(SpimexTradingResults.delivery_type_id == delivery_type_id)
                     #.filter(SpimexTradingResults.delivery_basis_id == delivery_basis_id)
                     #.filter(SpimexTradingResults.date >= start_date)
                     #.filter(SpimexTradingResults.date <= end_date)
                     ).limit(30)
            result = await session.execute(query)
            trades = result.scalars().all()
            return trades
