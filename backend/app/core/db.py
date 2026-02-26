from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import get_settings

settings = get_settings()
# NOTE: MVP uses sync SQLAlchemy for simplicity. Future migration to async:
# - Replace create_engine with create_async_engine
# - Replace SessionLocal with AsyncSession (async_sessionmaker)
# - Replace aiosqlite driver for SQLite: sqlite+aiosqlite:///
engine = create_engine(
    settings.database_url,
    connect_args={"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
)
SessionLocal = sessionmaker(bind=engine)
Base = declarative_base()

# Centralized get_db for all API routes - import from here, don't redefine
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
