from unittest.mock import MagicMock, patch

import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from src.repositories.spimex import SpimexRepository
from src.utils.unit_of_work import UnitOfWork


class TestUnitOfWork:
    @pytest.mark.asyncio
    async def test_unit_of_work_initialization(self, mock_async_session):
        uow = UnitOfWork()

        async with uow:
            assert uow.session is mock_async_session
            assert isinstance(uow.trading_results, SpimexRepository)

    @patch('src.utils.unit_of_work.async_session_maker')
    async def test_unit_of_work_unique_sessions(self, mock_async_session_maker):
        # Создаем уникальные экземпляры для каждой сессии
        mock_async_session_1 = MagicMock(spec=AsyncSession)
        mock_async_session_2 = MagicMock(spec=AsyncSession)

        mock_async_session_maker.side_effect = [mock_async_session_1, mock_async_session_2]

        uow1 = UnitOfWork()
        uow2 = UnitOfWork()

        async with uow1:
            session1 = uow1.session
            assert session1 is mock_async_session_1

        async with uow2:
            session2 = uow2.session
            assert session2 is mock_async_session_2

        # Проверяем, что сессии уникальны
        assert session1 is not session2

        # Проверка, что метод close был вызван для каждой сессии
        mock_async_session_1.close.assert_awaited()
        mock_async_session_2.close.assert_awaited()

        # # Проверка, что close был вызван дважды
        assert mock_async_session_maker.call_count == 2

    async def test_unit_of_work_commit(self, mock_async_session):
        uow = UnitOfWork()

        async with uow:
            pass

        # Проверка, что метод commit был вызван
        mock_async_session.commit.assert_awaited_once()

    async def test_unit_of_work_session_close(self, mock_async_session):
        uow = UnitOfWork()

        async with uow:
            assert uow.session is not None  # Сессия должна быть инициализирована
            assert uow.session is mock_async_session  # Проверка на соответствие мок-сессии

        # Проверка, что сессия была закрыта после использования
        mock_async_session.close.assert_awaited_once()

    async def test_unit_of_work_rollback_on_exception(self, mock_async_session):
        uow = UnitOfWork()

        with pytest.raises(ValueError):
            async with uow:
                raise ValueError("Something went wrong!")  # Исключение должно вызвать rollback

        # Проверка, что метод rollback был вызван/ метод commit не вызван
        mock_async_session.rollback.assert_awaited()
        mock_async_session.commit.assert_not_awaited()

    async def test_unit_of_work_rollback_on_different_exception(self, mock_async_session):
        uow = UnitOfWork()

        with pytest.raises(KeyError):
            async with uow:
                raise KeyError("This is a KeyError!")

        # Проверка, что метод rollback был вызван
        mock_async_session.rollback.assert_called_once()

    async def test_unit_of_work_commit_called(self, mock_async_session):
        uow = UnitOfWork()

        async with uow:
            await uow.trading_results.add_one()  # Пример добавления сущности
        # Проверка, что метод commit был вызван / метод rollback не был вызван
        mock_async_session.commit.assert_awaited()
        mock_async_session.rollback.assert_not_awaited()
