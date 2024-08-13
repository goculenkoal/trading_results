from typing import Sequence

from fastapi import APIRouter, Depends

from src.services.trading_results_service import TradingResults
from src.schemas.schemas import TradingResultSchema, TradingResultDateSchema
from src.utils.unit_of_work import UnitOfWork

router = APIRouter(
    prefix='/trades',
    tags=['Trade']
)


@router.get("/all_trades")
async def get_all_trades(limit: int,
                         uow: UnitOfWork = Depends(UnitOfWork)
                         ) -> Sequence[TradingResultSchema]:
    traids = await TradingResults().get_by_query_all_limit(uow=uow, limit=limit)

    return traids


@router.get("/last_trading_dates")
async def get_last_trading_dates(limit: int,
                                 uow: UnitOfWork = Depends(UnitOfWork)
                                 ) -> Sequence[TradingResultDateSchema]:
    dates = await TradingResults().get_by_query_dates(uow=uow, limit=limit)



    return dates


@router.get('/trading_results')
async def get_trading_results(oil_id: str,
                              # delivery_type_id: str,
                              # delivery_basis_id: str,
                              uow: UnitOfWork = Depends(UnitOfWork)
                              ) -> Sequence[TradingResultSchema]:
    trades = await TradingResults().get_by_query_all(uow=uow, oil_id=oil_id)

    return trades


@router.get('/dynamics')
async def get_dynamics(oil_id: str,
                       #delivery_type_id: str,
                       #delivery_basis_id:
                       #str, start_date: datetime,
                       #end_date: datetime,
                       uow: UnitOfWork = Depends(UnitOfWork)
                       ) -> Sequence[TradingResultSchema]:
    trades = await TradingResults().get_all_dunamics(uow=uow, oil_id=oil_id)

    return trades
