from collections.abc import Callable, Sequence
from typing import TypeVar, Any

from fastapi import HTTPException

from src.models.trade import SpimexTradingResults
from src.utils.unit_of_work import UnitOfWork

ReturnType = TypeVar("ReturnType")


class Handle:

    @staticmethod
    async def handle_query(
            method: Callable[..., ReturnType],
            uow: UnitOfWork, *args: Any,
            **kwargs: Any,
    ) -> Sequence[SpimexTradingResults]:
        result = await method(*args, uow=uow, **kwargs)
        if not result:
            raise HTTPException(status_code=404, detail="No results found")
        return result
