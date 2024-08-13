import asyncio
from datetime import datetime

from fastapi_cache.backends.redis import RedisBackend
from redis import asyncio as aioredis
from fastapi_cache import FastAPICache


class CacheManager:
    def __init__(self, redis_url: str):
        self.redis_url = redis_url
        self.redis = None

    async def initialize(self):
        self.redis = await aioredis.from_url(self.redis_url)
        print("Подключился к редис")
        FastAPICache.init(RedisBackend(self.redis), prefix="fastapi-cache")

        asyncio.create_task(self.reset_cache())

    async def close(self):
        if self.redis:
            await self.redis.close()

    async def reset_cache(self):
        while True:
            now = datetime.now()
            # Сбрасываем кэш в 14:11
            if now.hour == 14 and now.minute == 11:
                print("Drop Cache")
                await FastAPICache.clear()
                await asyncio.sleep(60)
            else:
                await asyncio.sleep(60)  # Ожидание 1 минуты перед следующей проверкой
