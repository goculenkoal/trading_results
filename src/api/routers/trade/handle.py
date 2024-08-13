from fastapi import HTTPException

from src.utils.unit_of_work import UnitOfWork


class Handle:
    async def handle_query(self, method, uow: UnitOfWork, *args, **kwargs):
        result = await method(uow=uow, *args, **kwargs)
        if not result:
            raise HTTPException(status_code=404, detail='No results found')
        return result
