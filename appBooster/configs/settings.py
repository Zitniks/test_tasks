"""Application settings (env and defaults)."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Settings loaded from environment and .env."""

    base_url: str = 'http://localhost:8000'
    database_url: str = 'sqlite:///./abtesting.db'
    # Used by data migration (env BUTTON_COLOR_OPTIONS / PRICE_OPTIONS). Format: "value1:weight1,value2:weight2,..."
    button_color_options: str = '#FF0000:33,#00FF00:33,#0000FF:34'
    price_options: str = '10:75,20:10,50:5,5:10'

    model_config = {
        'env_file': '.env',
        'case_sensitive': False,
    }


settings = Settings()
