from datetime import datetime
from typing import Sequence

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_async_session
from src.repositories.spimex import SpimexRepository
from src.schemas.schemas import TradingResultSchema, TradingResultDateSchema
from src.models.models import SpimexTradingResults

router = APIRouter(
    prefix='/operations',
    tags=['Operation']
)


#Работает на все записи
@router.get("/")
async def get_operations(limit: int) -> Sequence[TradingResultSchema]:
    traids = await SpimexRepository().get_by_query_all_limit(limit)
    # query = select(SpimexTradingResults).distinct().limit(10)
    # result = await session.execute(query)
    # traids = result.scalars().all()
    # print(traids)
    return traids


#get_trading_results – список последних торгов (фильтрация по oil_id, delivery_type_id, delivery_basis_id)
@router.get('/results')
async def get_trading_results(oil_id: str,
                              #delivery_type_id: str,
                              #delivery_basis_id: str,
                              session: AsyncSession = Depends(get_async_session)):
    trades = await SpimexRepository().get_by_query_last_trades(oil_id)
    # query = (select(SpimexTradingResults)
    #          .filter(SpimexTradingResults.oil_id == oil_id)
    #          #.filter(SpimexTradingResults.delivery_type_id == delivery_type_id)
    #          #.filter(SpimexTradingResults.delivery_basis_id == delivery_basis_id)
    #          )
    # result = await session.execute(query)
    # trades = result.scalars().all()
    return trades


#Список дат последних торговых дней
@router.get("/last_dates")
async def get_last_trading_dates(limit: int) -> Sequence[TradingResultDateSchema]:
    # query = select(SpimexTradingResults.date).distinct().order_by(SpimexTradingResults.date.desc()).limit(limit)
    # print(query)
    # result = await session.execute(query)
    # trades = result.scalars().all()
    # # print(f'TRADES: {trades}')
    #
    # return [TradingResultDateSchema(date=data) for data in trades]
    dates = await SpimexRepository().get_by_query_dates(limit)
    return dates


@router.get('/dynamics', response_model=list[TradingResultSchema])
async def get_dynamics(oil_id: str,
                       #delivery_type_id: str,
                       #delivery_basis_id:
                       #str, start_date: datetime,
                       #end_date: datetime,
                       session: AsyncSession = Depends(get_async_session)):
    # query = (select(SpimexTradingResults)
    #          .filter(SpimexTradingResults.oil_id == oil_id)
    #          #.filter(SpimexTradingResults.delivery_type_id == delivery_type_id)
    #          #.filter(SpimexTradingResults.delivery_basis_id == delivery_basis_id)
    #          #.filter(SpimexTradingResults.date >= start_date)
    #          #.filter(SpimexTradingResults.date <= end_date)
    #          ).limit(30)
    # print(query)
    # result = await session.execute(query)
    # trades = result.scalars().all()
    trades = await SpimexRepository().get_by_query_dynamics(oil_id)
    return trades
