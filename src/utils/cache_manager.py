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

    async def clear_cache(self):
        try:
            await self.redis.flushdb()  # Очищаем базу данных Redis
            print("Cache cleared")  # Можно использовать логирование
        except Exception as e:
            print(f"Error clearing cache: {e}")

    async def close(self):
        if self.redis:
            await self.redis.close()