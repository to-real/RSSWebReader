from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./rss.db"
    CLAUDE_API_KEY: str = ""
    FETCH_INTERVAL_MINUTES: int = 30
    CLAUDE_MAX_CONCURRENCY: int = 3
    CLAUDE_MAX_CONTENT_LENGTH: int = 3000
    LOG_LEVEL: str = "INFO"

    class Config:
        env_file = ".env"


settings = Settings()
