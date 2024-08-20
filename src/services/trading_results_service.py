# ruff: noqa: PLR0917,PLR0913
from datetime import datetime
from typing import Any

from src.utils.unit_of_work import UnitOfWork


class TradingResultsService:
    @staticmethod
    async def get_by_query_all_limit(uow: UnitOfWork, limit: int) -> Any | None:
        async with uow:
            return await uow.trading_results.get_by_query_all_limit(limit=limit)

    @staticmethod
    async def get_by_query_dates(uow: UnitOfWork, limit: int) -> Any | None:
        async with uow:
            return await uow.trading_results.get_by_query_dates(limit=limit)

    @staticmethod
    async def get_by_query_all(
            uow: UnitOfWork,
            oil_id: str,
            delivery_type_id: str,
            delivery_basis_id: str,
    ) -> Any | None:
        async with uow:
            return await uow.trading_results.get_by_query_all(
                oil_id=oil_id,
                delivery_type_id=delivery_type_id,
                delivery_basis_id=delivery_basis_id,
            )

    @staticmethod
    async def get_by_query_all_dynamics(
            uow: UnitOfWork,
            oil_id: str,
            delivery_type_id: str,
            delivery_basis_id: str,
            start_date: datetime,
            end_date: datetime,

    ) -> Any | None:

        async with uow:
            return await uow.trading_results.get_by_query_all_dynamics(
                oil_id=oil_id,
                delivery_type_id=delivery_type_id,
                delivery_basis_id=delivery_basis_id,
                start_date=start_date,
                end_date=end_date,
            )
