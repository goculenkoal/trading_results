from typing import Any, Sequence, Optional
from src.utils.unit_of_work import UnitOfWork


class TradingResultsService:
    async def get_by_query_all_limit(self, uow: UnitOfWork, limit: int) -> Optional[any]:
        async with uow:
            result = await uow.trading_results.get_by_query_all_limit(limit=limit)

            return result

    async def get_by_query_dates(self, uow: UnitOfWork, limit: int) -> Optional[Any]:
        async with uow:
            result = await uow.trading_results.get_by_query_dates(limit=limit)

            return result

    async def get_by_query_all(self, uow: UnitOfWork, oil_id: str) -> Optional[Any]:
        async with uow:
            result = await uow.trading_results.get_by_query_all(oil_id=oil_id)

            return result

    async def get_by_query_all_dynamics(self, uow: UnitOfWork, oil_id: str) -> Optional[Any]:
        async with uow:
            result = await uow.trading_results.get_by_query_all_dynamics(oil_id=oil_id)

            return result
