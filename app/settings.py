from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent  # /app/..

class Settings(BaseSettings):
    debug: bool = Field(False, env="DEBUG")

    database_url: str = Field(
        "postgresql+asyncpg://postgres:postgres@db:5432/postgres",
        env="DATABASE_URL",
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

@lru_cache
def get_settings() -> Settings:
    return Settings()