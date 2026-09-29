import os
from pathlib import Path
from typing import Optional

from pydantic_settings import BaseSettings, SettingsConfigDict

_PROJECT_ROOT = Path(__file__).resolve().parent.parent


def _pick_env_file() -> str:
    """
    Какой файл настроек читать.

    Порядок: явный ENV_FILE → .env.local, если он есть → .env.

    .env.local лежит только на машине разработчика (он в gitignore и не
    попадает ни в образ, ни на сервер), поэтому автоподхват безопасен:
    в проде файла нет и читается обычный .env. Зато локальный запуск
    больше не требует настраивать переменные окружения в PyCharm —
    иначе берётся .env с хостом `postgres` из docker-сети, который
    с ноутбука не резолвится.
    """
    explicit = os.environ.get("ENV_FILE")
    if explicit:
        return explicit
    if (_PROJECT_ROOT / ".env.local").exists():
        return ".env.local"
    return ".env"


ENV_FILE = _pick_env_file()


class Settings(BaseSettings):
    # Bot
    BOT_TOKEN: str
    ADMIN_USER: int

    # Database
    DATABASE_URL: str
    DATABASE_URL_SYNC: str

    # Optional / infra (можно хранить в .env, но боту не обязательно)
    ENV: Optional[str] = None
    LOG_LEVEL: Optional[str] = None
    LOG_DIR: Optional[str] = None
    SENTRY_DSN: Optional[str] = None

    # Docker / Postgres service vars (если лежат в .env — не должны ломать Settings)
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=ENV_FILE,
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore",  # <-- ключевое: игнорим лишние переменные в .env
    )


settings = Settings()
