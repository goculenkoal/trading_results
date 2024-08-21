from datetime import datetime
import pytest

from src.models.trade import SpimexTradingResults


@pytest.fixture(scope="session")
@pytest.mark.asyncio
async def add_in_db(async_session_maker):
    """В рамках сессии добавляем данные в БД"""
    async with async_session_maker() as session:
        data = [
            SpimexTradingResults(
                exchange_product_id="test1",
                exchange_product_name="test1",
                oil_id="A592",
                delivery_basis_id="NYC",
                delivery_basis_name="in",
                delivery_type_id="W",
                volume=1,
                total=2,
                count=3,
                date=datetime(2024, 1, 1)
            ),
            SpimexTradingResults(
                exchange_product_id="test2",
                exchange_product_name="test2",
                oil_id="A10K",
                delivery_basis_id="ZLY",
                delivery_basis_name="in",
                delivery_type_id="W",
                volume=1,
                total=2,
                count=3,
                date=datetime(2024, 2, 15)
            ),
        ]
        session.add_all(data)
        await session.commit()
