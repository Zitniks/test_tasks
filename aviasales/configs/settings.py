"""Application settings (env and defaults)."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings loaded from environment and .env."""

    host: str = '127.0.0.1'
    port: int = 8000
    xml_file_1: str = 'RS_Via-3.xml'
    xml_file_2: str = 'RS_ViaOW.xml'

    model_config = {
        'env_file': '.env',
        'case_sensitive': False,
    }


settings = Settings()
