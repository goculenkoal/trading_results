from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession


@pytest.fixture()
def mock_async_session(scope="function"):
    """Фикстура для мок-сессии, которая будет использоваться в тестах."""
    mock_session = MagicMock(spec=AsyncSession)
    with patch('src.utils.unit_of_work.async_session_maker', return_value=mock_session):
        yield mock_session
