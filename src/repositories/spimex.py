from src.models.models import SpimexTradingResults
from src.utils.repository import SqlAlchemyRepository


class SpimexRepository(SqlAlchemyRepository):
    """класс для работы репозитория чз модель"""
    model = SpimexTradingResults
