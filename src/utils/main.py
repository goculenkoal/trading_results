import os
from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger

from src.utils.cache_manager import CacheManager
from src.api.routers.trade.trade import router
from src.utils.metadata import TITLE, DESCRIPTION, VERSION, TAG_METADATA
from src.utils.config import settings

scheduler = AsyncIOScheduler()


@asynccontextmanager
async def lifespan(_app: FastAPI) -> AsyncIterator[None]:
    cache_manager = CacheManager(settings.REDIS_URL)
    await cache_manager.initialize()  # Инициализация кэширования

    # Настройка задачи для очистки кэша
    async def clean_cache() -> None:
        await cache_manager.clear_cache()  # Вызываем метод очистки кэша

    # Настройка триггера Cron для выполнения задачи в 14:11 каждый день
    scheduler.add_job(
        func=clean_cache,  # Указываем асинхронную функцию для очистки кэша
        trigger=CronTrigger(hour=10, minute=51),  # Время для очистки кэша
        id="cache_cleanup_job",
        replace_existing=True,
    )

    scheduler.start()

    yield
    await cache_manager.close()  # Закрытие соединения при завершении
    scheduler.shutdown()


def create_fast_api_app() -> FastAPI:
    load_dotenv(find_dotenv(".env"))
    env_name = os.getenv("MODE", "DEV")

    if env_name != "PROD":
        _app = FastAPI(
            default_response_class=ORJSONResponse,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
            lifespan=lifespan,
        )
    else:
        _app = FastAPI(
            default_response_class=ORJSONResponse,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
            docs_url=None,
            redoc_url=None,
        )

    @_app.get("/")
    def hello() -> str:
        return "Welcome"

    _app.include_router(router, prefix="/api")
    return _app


app = create_fast_api_app()
