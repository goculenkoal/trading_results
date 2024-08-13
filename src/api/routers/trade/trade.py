from typing import Sequence

from fastapi import APIRouter, Depends, HTTPException
from fastapi_cache.decorator import cache

from src.api.routers.trade.handle import Handle
from src.models.trade import SpimexTradingResults
from src.schemas.wrapper import TradingResultWrapper, TradingResultDateWrapper
from src.services.trading_results_service import TradingResultsService
from src.utils.unit_of_work import UnitOfWork

router = APIRouter(
    prefix='/trades',
    tags=['Trade']
)

trading_results = TradingResultsService()
handle = Handle()


@router.get("/all_trades")
@cache()
async def get_all_trades(limit: int,
                         uow: UnitOfWork = Depends(UnitOfWork)
                         ) -> TradingResultWrapper:
    trades: Sequence[SpimexTradingResults] | None = await handle.handle_query(trading_results.get_by_query_all_limit,
                                                                              uow=uow,
                                                                              limit=limit)

    return TradingResultWrapper(payload=trades)


@router.get("/last_trading_dates")
@cache()
async def get_last_trading_dates(limit: int,
                                 uow: UnitOfWork = Depends(UnitOfWork)
                                 ) -> TradingResultDateWrapper:
    dates: Sequence[SpimexTradingResults] | None = await handle.handle_query(trading_results.get_by_query_dates,
                                                                             uow=uow,
                                                                             limit=limit)

    return TradingResultDateWrapper(payload=dates)


@router.get('/trading_results')
@cache()
async def get_trading_results(oil_id: str,
                              # delivery_type_id: str,
                              # delivery_basis_id: str,
                              uow: UnitOfWork = Depends(UnitOfWork)
                              ) -> TradingResultWrapper:
    trades: Sequence[SpimexTradingResults] | None = await handle.handle_query(trading_results.get_by_query_all,
                                                                              uow=uow,
                                                                              oil_id=oil_id)

    return TradingResultWrapper(status=200, payload=trades)


@router.get('/dynamics')
@cache()
async def get_dynamics(oil_id: str,
                       #delivery_type_id: str,
                       #delivery_basis_id:
                       #str, start_date: datetime,
                       #end_date: datetime,
                       uow: UnitOfWork = Depends(UnitOfWork)
                       ) -> TradingResultWrapper:
    trades: Sequence[SpimexTradingResults] | None = await handle.handle_query(trading_results.get_by_query_all_dynamics,
                                                                              uow=uow,
                                                                              oil_id=oil_id)

    return TradingResultWrapper(status=200, payload=trades)
