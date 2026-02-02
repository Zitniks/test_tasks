"""Application settings (env and defaults)."""

from pydantic import field_validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings loaded from environment and .env."""

    database_url: str = 'postgresql://urlshortener:urlshortener@localhost:5432/urlshortener'
    base_url: str = 'http://localhost:8000'
    short_code_length: int = 6

    model_config = {
        'env_file': '.env',
        'case_sensitive': False,
    }

    @field_validator('short_code_length')
    @classmethod
    def short_code_length_range(cls, v: int) -> int:
        if not 4 <= v <= 20:
            raise ValueError('short_code_length must be between 4 and 20')
        return v


settings = Settings()
