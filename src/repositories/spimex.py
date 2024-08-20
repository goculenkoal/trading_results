from src.models.trade import SpimexTradingResults
from src.utils.repository import SqlAlchemyRepository


class SpimexRepository(SqlAlchemyRepository):
    """класс для работы репозитория чз модель."""

    model = SpimexTradingResults
