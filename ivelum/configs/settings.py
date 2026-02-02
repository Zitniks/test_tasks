"""Настройки приложения (хост, порт, URL Hacker News)."""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Конфигурация прокси-сервера и upstream URL."""

    host: str = "127.0.0.1"
    port: int = 8232
    hn_base_url: str = "https://news.ycombinator.com"
    request_timeout: float = Field(default=30.0, gt=0, description="Таймаут запроса к upstream (сек).")

    model_config = {
        "env_file": ".env",
        "case_sensitive": False,
    }


settings = Settings()
