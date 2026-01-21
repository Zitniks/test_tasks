import os
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    base_url: str = 'http://localhost:8000'
    _database_url: str | None = None

    class Config:
        env_file = '.env'
        case_sensitive = False
        env_prefix = ''

    @property
    def database_url(self) -> str:
        if self._database_url:
            return self._database_url
        
        db_url = os.getenv('DATABASE_URL', '')
        if db_url and db_url.startswith('sqlite'):
            self._database_url = db_url
            return db_url
        
        self._database_url = 'sqlite:///./abtesting.db'
        return self._database_url


settings = Settings()
