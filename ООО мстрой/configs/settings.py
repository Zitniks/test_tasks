"""Настройки приложения (хост, порт, путь к данным)."""

from pathlib import Path

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфигурация сервера и путей к данным."""

    host: str = '127.0.0.1'
    port: int = 8000
    data_file: Path = Path(__file__).resolve().parent.parent / 'data' / 'items.json'

    model_config = {
        'env_file': '.env',
        'case_sensitive': False,
    }


settings = Settings()
