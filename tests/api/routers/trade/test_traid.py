import pytest
from httpx import AsyncClient


class TestTrade:
    async def test_get_all_trades(self, async_client: AsyncClient, add_in_db):

        response = await async_client.get("/api/trades/all_trades", params={"limit": 10})
        assert response.status_code == 200, f"Unexpected status code: {response.status_code}"

        json_response = response.json()
        assert "payload" in json_response, "Payload not found in response"
        assert isinstance(json_response["payload"], list), "Payload should be a list"
        assert len(json_response["payload"]) <= 10, "Payload limit should be 10 or less"

    async def test_get_last_trading_dates(self, async_client: AsyncClient, add_in_db):

        response = await async_client.get("/api/trades/last_trading_dates", params={"limit": 10})
        assert response.status_code == 200

        json_response = response.json()
        assert "payload" in response.json()
        assert len(json_response["payload"]) == 2
        assert len(json_response["payload"]) <= 10

        for trading_date in json_response["payload"]:
            assert isinstance(trading_date, dict), "Each trading date should be a dictionary"
            assert "date" in trading_date, "Trading date should have a 'date' key"
            assert isinstance(trading_date["date"], str), "Trading date should be a string"

    async def test_get_trading_result(self, async_client: AsyncClient, add_in_db):
        params = {
            "oil_id": "A592",
            "delivery_type_id": "W",
            "delivery_basis_id": "NYC",
        }

        response = await async_client.get("/api/trades/trading_results", params=params)
        assert response.status_code == 200

        json_response = response.json()
        error = json_response.get("error", False)  # Предполагаем, что ошибка находится в этом поле
        assert not error, "Error should be False"

        assert "payload" in json_response, "Payload not found in response"
        for item in json_response["payload"]:
            assert isinstance(item, dict), "Each item in payload should be a dictionary"

    @pytest.mark.parametrize(
        "oil_id, delivery_type_id, delivery_basis_id, start_date, end_date, expected_status_code",
        [
            (1, "W", "NYC", '2023-01-01', '2024-01-01', 404),
            (None, None, None, '2023-01-01', '2024-01-01', 404),
            (None, "W", None, '2023-01-01', '2024-01-01', 404),
            (None, None, "NYC", '2023-01-01', '2024-01-01', 404),
            ("A592", "W", "NYC", None, '2024-01-01', 422),
            ("A592", "W", "NYC", '2023-01-01', None, 422),
            ("A592", "W", "NYC", None, None, 422),
            ("A592", "W", "NYC", '2023-01-01', '2024-01-01', 200),
            ("A10K", "W", "ZLY", '2023-01-01', '2025-01-01', 200),
        ]
    )
    async def test_get_dynamics(
            self,
            async_client: AsyncClient,
            add_in_db, oil_id,
            delivery_type_id,
            delivery_basis_id,
            start_date,
            end_date,
            expected_status_code
    ):
        params = {
            "oil_id": oil_id,
            "delivery_type_id": delivery_type_id,
            "delivery_basis_id": delivery_basis_id,
            "start_date": start_date,
            "end_date": end_date,
        }

        response = await async_client.get("/api/trades/dynamics", params=params)
        assert response.status_code == expected_status_code
        if expected_status_code != 200:
            data = response.json()
            assert isinstance(data, dict)
            assert 'detail' in data  # Проверяем наличие ключа 'detail' для ошибок
        else:

            data = response.json()
            error = data.get("error", True)
            assert not error, "Error should be True"
            assert isinstance(data, dict)
            assert "payload" in data
            assert isinstance(data["payload"], list)
