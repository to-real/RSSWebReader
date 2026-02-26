from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    claude_api_key: str
    fetch_interval_minutes: int = 30
    claude_max_concurrency: int = 3
    claude_max_content_length: int = 3000
    log_level: str = "INFO"
    sentry_dsn: str = ""

    class Config:
        env_file = ".env"

@lru_cache()
def get_settings() -> Settings:
    return Settings()
