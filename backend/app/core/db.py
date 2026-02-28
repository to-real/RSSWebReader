from sqlalchemy import create_engine, text
from sqlalchemy.orm import declarative_base, sessionmaker
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


def _ensure_sqlite_source_type_column() -> None:
    """
    Backward-compatible schema patch for existing SQLite databases.
    Existing local DBs were created before Alembic tracking.
    """
    if not settings.database_url.startswith("sqlite"):
        return

    with engine.begin() as conn:
        table_exists = conn.execute(
            text("SELECT name FROM sqlite_master WHERE type='table' AND name='feeds'")
        ).fetchone()
        if not table_exists:
            return

        columns = {row[1] for row in conn.execute(text("PRAGMA table_info(feeds)"))}
        if "source_type" not in columns:
            conn.execute(text("ALTER TABLE feeds ADD COLUMN source_type VARCHAR"))


_ensure_sqlite_source_type_column()

# Centralized get_db for all API routes - import from here, don't redefine
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
