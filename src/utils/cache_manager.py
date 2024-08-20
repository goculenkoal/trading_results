from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CacheManager:
    def __init__(self, redis_url: str) -> None:
        self.redis_url = redis_url
        self.redis = None

    async def initialize(self) -> None:
        self.redis = await aioredis.from_url(self.redis_url)
        logger.info("Подключился к редис")
        FastAPICache.init(RedisBackend(self.redis), prefix="fastapi-cache")

    async def clear_cache(self) -> None:
        try:
            await self.redis.flushdb()
            logger.info("Cache cleared")
        except Exception:
            logger.exception("Error clearing cache: %s")

    async def close(self) -> None:
        if self.redis:
            await self.redis.close()
