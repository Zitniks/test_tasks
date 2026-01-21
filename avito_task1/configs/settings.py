from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url: str = 'postgresql://urlshortener:urlshortener@localhost:5432/urlshortener'
    base_url: str = 'http://localhost:8000'
    short_code_length: int = 6

    class Config:
        env_file = '.env'
        case_sensitive = False


settings = Settings()
