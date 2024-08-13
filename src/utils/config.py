from typing import Optional

from dotenv import find_dotenv, load_dotenv

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    MODE: str

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_USER: Optional[str] = None
    REDIS_PASSWORD: Optional[str] = None

    @property
    def DB_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    @property
    def REDIS_URL(self):
        # Если используется пользователь, добавляем его к URL
        if self.REDIS_USER and self.REDIS_PASSWORD:
            return f'redis://{self.REDIS_USER}:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}'
        elif self.REDIS_PASSWORD:
            return f'redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}'
        return f'redis://{self.REDIS_HOST}:{self.REDIS_PORT}'

    model_config = SettingsConfigDict(env_file='.env')


load_dotenv(find_dotenv('.env'))
settings = Settings()
