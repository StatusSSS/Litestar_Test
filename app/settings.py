from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import os
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env", override=True)


@dataclass(slots=True, frozen=True)
class Settings:
    debug: bool = os.getenv("DEBUG", "0").lower() in {"1", "true", "yes", "on"}
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+asyncpg://postgres:postgres@db:5432/postgres",
    )



settings = Settings()