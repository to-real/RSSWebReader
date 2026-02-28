from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class Settings(BaseSettings):
    database_url: str
    claude_api_key: str = ""
    zhipu_api_key: str = ""
    anthropic_api_key: str = ""
    newapi_api_key: str = ""
    anthropic_base_url: str = ""
    ai_provider: str = "claude"  # "claude" or "zhipu"
    fetch_interval_minutes: int = 30
    claude_max_concurrency: int = 3
    claude_max_content_length: int = 3000
    log_level: str = "INFO"
    sentry_dsn: str = ""
    frontend_url: str = "http://localhost:3000"  # Frontend URL for CORS

    model_config = SettingsConfigDict(env_file=".env")

@lru_cache()
def get_settings() -> Settings:
    return Settings()
