from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    host: str = '127.0.0.1'
    port: int = 8232
    hn_base_url: str = 'https://news.ycombinator.com'

    class Config:
        env_file = '.env'
        case_sensitive = False


settings = Settings()
