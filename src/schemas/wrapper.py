from pydantic import BaseModel
from collections.abc import Sequence

from src.schemas.schemas import TradingResultSchema, TradingResultDateSchema


class BaseWrapper(BaseModel):
    status: int = 200
    error: bool = False


class TradingResultWrapper(BaseWrapper):
    payload: Sequence[TradingResultSchema]


class TradingResultDateWrapper(BaseWrapper):
    payload: Sequence[TradingResultDateSchema]
