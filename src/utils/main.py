import os
from contextlib import asynccontextmanager

from dotenv import load_dotenv, find_dotenv
from fastapi import FastAPI
from fastapi.responses import ORJSONResponse

from src.api.routers.trade.trade import router
from src.utils.metadata import TITLE, DESCRIPTION, VERSION, TAG_METADATA
from src.utils.config import settings
from src.utils.cache_manager import CacheManager


@asynccontextmanager
async def lifespan(_app: FastAPI):
    cache_manager = CacheManager(settings.REDIS_URL)
    await cache_manager.initialize()  # Инициализация кэширования
    yield
    await cache_manager.close()  # Закрытие соединения при завершении


def create_fast_api_app():
    load_dotenv(find_dotenv(".env"))
    env_name = os.getenv('MODE', 'DEV')

    if env_name != 'PROD':
        _app = FastAPI(
            default_response_class=ORJSONResponse,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
            lifespan=lifespan
        )
    else:
        _app = FastAPI(
            default_response_class=ORJSONResponse,
            title=TITLE,
            description=DESCRIPTION,
            version=VERSION,
            openapi_tags=TAG_METADATA,
            docs_url=None,
            redoc_url=None
        )

    @_app.get('/')
    def hello():
        return "Welcome"

    _app.include_router(router, prefix='/api')
    return _app


app = create_fast_api_app()
