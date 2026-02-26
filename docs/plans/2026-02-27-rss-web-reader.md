# RSS Web Reader Implementation Plan

> **For Claude:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Build an RSS aggregator website that fetches 92 tech blogs, generates AI summaries in Chinese, and presents them in a clean web interface.

**Architecture:**
- Backend: FastAPI + SQLAlchemy, async RSS fetching with httpx, AI processing with Claude API
- Frontend: React + Vite + TailwindCSS + shadcn/ui, data fetching with React Query
- Storage: SQLite (MVP) → PostgreSQL (production)
- Deployment: Railway monorepo (separate API + worker services)

**Tech Stack:**
- Backend: Python 3.11+, FastAPI, SQLAlchemy, httpx, feedparser, Anthropic SDK
- Frontend: React 18, Vite, TypeScript, TailwindCSS, shadcn/ui, React Query
- Dev: Alembic (migrations), pytest (tests)

---

## Task 1: Project Skeleton & Monorepo Setup

**Files:**
- Create: `backend/pyproject.toml`
- Create: `backend/requirements.txt`
- Create: `backend/main.py`
- Create: `frontend/package.json`
- Create: `frontend/vite.config.ts`
- Create: `docker-compose.yml`
- Create: `.env.example`
- Create: `README.md`
- Create: `railway.toml`

**Step 1: Create backend pyproject.toml**

```toml
[project]
name = "rss-web-reader-backend"
version = "0.1.0"
requires-python = ">=3.11"
dependencies = [
    "fastapi>=0.109.0",
    "uvicorn[standard]>=0.27.0",
    "sqlalchemy>=2.0.25",
    "alembic>=1.13.1",
    "httpx>=0.26.0",
    "feedparser>=6.0.10",
    "anthropic>=0.18.0",
    "tenacity>=8.2.3",
    "structlog>=24.1.0",
    "pydantic>=2.5.3",
    "pydantic-settings>=2.1.0",
    "python-dotenv>=1.0.0",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4.4",
    "pytest-asyncio>=0.23.3",
    "httpx>=0.26.0",
]
```

**Step 2: Create backend requirements.txt** (for Railway deployment)

```txt
fastapi>=0.109.0
uvicorn[standard]>=0.27.0
sqlalchemy>=2.0.25
alembic>=1.13.1
httpx>=0.26.0
feedparser>=6.0.10
anthropic>=0.18.0
tenacity>=8.2.3
structlog>=24.1.0
pydantic>=2.5.3
pydantic-settings>=2.1.0
python-dotenv>=1.0.0
```

**Step 3: Create frontend package.json**

```json
{
  "name": "rss-web-reader-frontend",
  "version": "0.1.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "preview": "vite preview"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "@tanstack/react-query": "^5.17.0",
    "zustand": "^4.5.0",
    "axios": "^1.6.5",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",
    "date-fns": "^3.0.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "autoprefixer": "^10.4.0",
    "postcss": "^8.4.0",
    "tailwindcss": "^3.4.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0"
  }
}
```

**Step 4: Create backend/main.py (minimal FastAPI app)**

```python
from fastapi import FastAPI
from app.core.config import settings

app = FastAPI(title="RSS Web Reader API")

@app.get("/health")
async def health():
    return {"status": "ok", "db": "connected", "last_fetch": None}

@app.get("/")
async def root():
    return {"message": "RSS Web Reader API"}
```

**Step 5: Create frontend/vite.config.ts**

```ts
import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      }
    }
  }
})
```

**Step 6: Create docker-compose.yml for local development**

```yaml
version: '3.8'
services:
  api:
    build: ./backend
    ports: ["8000:8000"]
    environment:
      - DATABASE_URL=sqlite:///./rss.db
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports: ["3000:3000"]
    volumes:
      - ./frontend:/app
```

**Step 7: Create .env.example**

```env
# Database
DATABASE_URL=sqlite:///./rss.db

# Claude API
CLAUDE_API_KEY=your-api-key-here

# Fetcher Settings
FETCH_INTERVAL_MINUTES=30
CLAUDE_MAX_CONCURRENCY=3
CLAUDE_MAX_CONTENT_LENGTH=3000

# Logging
LOG_LEVEL=INFO

# Optional
SENTRY_DSN=
```

**Step 8: Create railway.toml**

```toml
[build]
builder = "NIXPACKS"

# API Service
[services.api]
command = "uvicorn main:app --host 0.0.0.0 --port $PORT"
env = ["PORT=$PORT"]

# Worker Service
[services.worker]
command = "python -m app.tasks.scheduler"
```

**Step 9: Create README.md**

```markdown
# RSS Web Reader

RSS 聚合 + AI 摘要 + 中文解读

## 开发

```bash
# Backend
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Frontend
cd frontend
npm install
npm run dev
```

## 部署

Railway 自动部署，推送即可。
```

**Step 10: Verify skeleton structure**

Run: `ls -la e:/RSSWebReader/`
Expected:
```
backend/
frontend/
feeds.opml
docker-compose.yml
.env.example
README.md
railway.toml
docs/
```

**Step 11: Commit**

```bash
cd e:/RSSWebReader
git init
git add .
git commit -m "feat: initialize monorepo structure with backend and frontend"
```

---

## Task 2: Backend Core Configuration & Database Setup

**Files:**
- Create: `backend/app/__init__.py`
- Create: `backend/app/core/__init__.py`
- Create: `backend/app/core/config.py`
- Create: `backend/app/core/db.py`
- Create: `backend/app/core/logging.py`
- Create: `backend/alembic.ini`

**Step 1: Create backend/app/core/config.py**

```python
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
```

**Step 2: Create backend/app/core/db.py**

```python
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
```

**Step 3: Create backend/app/core/logging.py**

```python
import structlog
import logging
from app.core.config import get_settings

def configure_logging():
    settings = get_settings()
    logging.basicConfig(
        format="%(message)s",
        level=getattr(logging, settings.log_level.upper()),
    )
    structlog.configure(
        processors=[
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
    )

configure_logging()
logger = structlog.get_logger()
```

**Step 4: Create backend/app/core/__init__.py**

```python
from app.core.config import get_settings
from app.core.db import Base, engine, get_db
from app.core.logging import logger

__all__ = ["get_settings", "Base", "engine", "get_db", "logger"]
```

**Step 5: Create backend/app/__init__.py**

```python
# Backend package
```

**Step 6: Initialize Alembic**

Run: `cd backend && alembic init alembic`

Expected: Creates `backend/alembic/` directory and `backend/alembic.ini`

**Step 7: Configure alembic/env.py**

Edit `backend/alembic/env.py`, add at top:

```python
from app.core.db import Base
target_metadata = Base.metadata
```

**Step 8: Update main.py to use core modules**

```python
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core import logger
from app.api import health, articles, feeds, stats

app = FastAPI(title="RSS Web Reader API")

# CORS middleware - needed for production when frontend/backend are on different domains
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # TODO: Restrict to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(health.router, tags=["health"])
app.include_router(stats.router, prefix="/api", tags=["stats"])
app.include_router(articles.router, prefix="/api/articles", tags=["articles"])
app.include_router(feeds.router, prefix="/api/feeds", tags=["feeds"])

@app.on_event("startup")
async def startup():
    logger.info("api_started")

@app.on_event("shutdown")
async def shutdown():
    logger.info("api_stopped")
```

**Step 9: Create placeholder API modules**

```python
# backend/app/api/__init__.py
# backend/app/api/health.py
# backend/app/api/articles.py
# backend/app/api/feeds.py
```

Each with a basic router:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def root():
    return {"status": "ok"}
```

**Step 10: Commit**

```bash
git add backend/
git commit -m "feat: backend core config, database, and logging setup"
```

---

## Task 3: Database Models

**Files:**
- Create: `backend/app/models/__init__.py`
- Create: `backend/app/models/feed.py`
- Create: `backend/app/models/article.py`
- Create: `backend/app/models/summary.py`

**Step 1: Create backend/app/models/feed.py**

```python
from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.core.db import Base

class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    fetch_interval_minutes = Column(Integer, default=30)
    last_fetched_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

**Step 2: Create backend/app/models/article.py**

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from app.core.db import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    content_hash = Column(String, unique=True, nullable=False, index=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    author = Column(String, nullable=True)
    language = Column(String, default="en")
    published_at = Column(DateTime, nullable=True)
    feed_id = Column(Integer, ForeignKey("feeds.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
```

**Step 3: Create backend/app/models/summary.py**

```python
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from datetime import datetime
from app.core.db import Base

class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("articles.id"), unique=True, nullable=False)
    status = Column(String, default="pending")  # pending/completed/failed
    summary_cn = Column(Text, nullable=True)
    one_liner = Column(String, nullable=True)
    # JSON type works with both SQLite and PostgreSQL (no migration needed)
    keywords = Column(JSON, nullable=True)  # Stores ["kw1", "kw2", ...]
    model_version = Column(String, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
```

**Step 4: Create backend/app/models/__init__.py**

```python
from app.models.feed import Feed
from app.models.article import Article
from app.models.summary import Summary

__all__ = ["Feed", "Article", "Summary"]
```

**Step 5: Import models in core/db.py**

```python
# Add after Base declaration:
from app.models import Feed, Article, Summary  # noqa: E402 (must be after Base)
```

**Step 6: Create first Alembic migration**

Run: `cd backend && alembic revision --autogenerate -m "initial models"`

Expected: Creates new migration file in `alembic/versions/`

**Step 7: Run migration**

Run: `cd backend && alembic upgrade head`

Expected: Creates database tables

**Step 8: Verify tables created**

Run (SQLite): `sqlite3 backend/rss.db ".tables"`

Expected: `alembic_version articles feeds summaries`

**Step 9: Write model tests**

Create `backend/tests/test_models.py`:

```python
import pytest
from app.models import Feed, Article, Summary
from app.core.db import SessionLocal

def test_create_feed(db):
    feed = Feed(url="https://example.com/feed.xml", title="Test Feed")
    db.add(feed)
    db.commit()
    assert feed.id is not None
    assert feed.title == "Test Feed"
```

**Step 10: Commit**

```bash
git add backend/
git commit -m "feat: database models for Feed, Article, Summary"
```

---

## Task 4: Pydantic Schemas

**Files:**
- Create: `backend/app/schemas/__init__.py`
- Create: `backend/app/schemas/feed.py`
- Create: `backend/app/schemas/article.py`
- Create: `backend/app/schemas/summary.py`

**Step 1: Create backend/app/schemas/feed.py**

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class FeedBase(BaseModel):
    url: str
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    fetch_interval_minutes: int = 30

class FeedCreate(FeedBase):
    pass

class FeedResponse(FeedBase):
    id: int
    is_active: bool
    last_fetched_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True
```

**Step 2: Create backend/app/schemas/article.py**

```python
from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ArticleBase(BaseModel):
    url: str
    title: str
    content: Optional[str] = None
    author: Optional[str] = None
    language: str = "en"

class ArticleListItem(BaseModel):
    id: int
    title: str
    url: str
    one_liner: Optional[str] = None
    keywords: List[str] = []
    published_at: Optional[datetime] = None
    feed_title: str
    feed_category: Optional[str] = None

class ArticleDetail(ArticleBase):
    id: int
    content_hash: str
    summary_cn: Optional[str] = None
    one_liner: Optional[str] = None
    keywords: List[str] = []
    summary_status: str = "pending"
    published_at: Optional[datetime] = None
    feed_title: str
    author: Optional[str] = None

class PaginatedArticlesResponse(BaseModel):
    items: List[ArticleListItem]
    total: int
    page: int
    page_size: int
    has_next: bool
```

**Step 3: Create backend/app/schemas/summary.py**

```python
from pydantic import BaseModel
from typing import List, Optional

class SummaryCreate(BaseModel):
    article_id: int

class SummaryResponse(BaseModel):
    id: int
    article_id: int
    status: str
    summary_cn: Optional[str] = None
    one_liner: Optional[str] = None
    keywords: List[str] = []
    model_version: Optional[str] = None

class StatsResponse(BaseModel):
    total_feeds: int
    active_feeds: int
    total_articles: int
    articles_today: int
    summaries_pending: int
    summaries_failed: int
    summaries_completed: int
    last_fetch_at: Optional[str] = None
    completion_rate: float
```

**Step 4: Create backend/app/schemas/__init__.py**

```python
from app.schemas.feed import FeedCreate, FeedResponse
from app.schemas.article import ArticleListItem, ArticleDetail, PaginatedArticlesResponse
from app.schemas.summary import SummaryResponse, StatsResponse

__all__ = [
    "FeedCreate", "FeedResponse",
    "ArticleListItem", "ArticleDetail", "PaginatedArticlesResponse",
    "SummaryResponse", "StatsResponse",
]
```

**Step 5: Write schema validation tests**

Create `backend/tests/test_schemas.py`:

```python
from app.schemas import FeedCreate, FeedResponse

def test_feed_create_schema():
    feed = FeedCreate(url="https://example.com/feed", title="Test")
    assert feed.url == "https://example.com/feed"
    assert feed.fetch_interval_minutes == 30  # default value
```

**Step 6: Commit**

```bash
git add backend/
git commit -m "feat: Pydantic schemas for request/response validation"
```

---

## Task 5: OPML Import Script

**Files:**
- Create: `backend/scripts/__init__.py`
- Create: `backend/scripts/import_opml.py`

**Step 1: Write OPML parser**

```python
import xml.etree.ElementTree as ET
from typing import List
from app.schemas import FeedCreate

def parse_opml(file_path: str) -> List[FeedCreate]:
    """Parse OPML file and return list of FeedCreate objects"""
    tree = ET.parse(file_path)
    root = tree.getroot()

    feeds = []
    # OPML uses namespaces, find outline elements
    for outline in root.iter():
        if outline.tag.endswith('outline'):
            xml_url = outline.get('xmlUrl')
            if xml_url:
                feeds.append(FeedCreate(
                    url=xml_url,
                    title=outline.get('title', outline.get('text', '')),
                    html_url=outline.get('htmlUrl'),
                ))
    return feeds
```

**Step 2: Create import script**

Create `backend/scripts/import_opml.py`:

```python
import asyncio
from pathlib import Path
from sqlalchemy.orm import Session
from app.core.db import SessionLocal, engine
from app.models import Feed
from app.scripts.opml_parser import parse_opml

async def import_feeds(opml_path: str = "feeds.opml"):
    """Import feeds from OPML file"""
    feeds_data = parse_opml(opml_path)

    db: Session = SessionLocal()
    try:
        for feed_data in feeds_data:
            existing = db.query(Feed).filter(Feed.url == feed_data.url).first()
            if not existing:
                feed = Feed(
                    url=feed_data.url,
                    title=feed_data.title,
                    is_active=True,
                    fetch_interval_minutes=30
                )
                db.add(feed)
        db.commit()
        print(f"Imported {len(feeds_data)} feeds")
    finally:
        db.close()

if __name__ == "__main__":
    import asyncio
    asyncio.run(import_feeds())
```

**Step 3: Test OPML import**

Run: `cd backend && python scripts/import_opml.py`

Expected: `Imported 92 feeds`

**Step 4: Verify in database**

Run: `sqlite3 backend/rss.db "SELECT COUNT(*) FROM feeds;"`

Expected: `92`

**Step 5: Commit**

```bash
git add backend/
git commit -m "feat: OPML import script for 92 feeds"
```

---

## Task 6: RSS Fetcher Service

**Files:**
- Create: `backend/app/tasks/__init__.py`
- Create: `backend/app/tasks/fetcher.py`

**Step 1: Create URL normalization utility**

Create `backend/app/utils/url.py`:

```python
from urllib.parse import urlparse, urlunparse, parse_qs, urlencode
import hashlib

def normalize_url(url: str) -> str:
    """Remove tracking parameters and normalize URL"""
    parsed = urlparse(url)
    # Remove utm_* parameters
    params = parse_qs(parsed.query)
    clean_params = {k: v for k, v in params.items() if not k.startswith('utm_')}
    query = urlencode(clean_params, doseq=True)
    return urlunparse(parsed._replace(query=query))

def content_hash(url: str, title: str) -> str:
    """Generate hash for deduplication"""
    combined = normalize_url(url) + title
    return hashlib.sha256(combined.encode()).hexdigest()
```

**Step 2: Create HTML content cleaner**

Create `backend/app/utils/html.py`:

```python
import re
from bs4 import BeautifulSoup

def clean_html(html: str) -> str:
    """Extract clean text content from HTML"""
    soup = BeautifulSoup(html, 'html.parser')
    # Remove script and style elements
    for script in soup(['script', 'style']):
        script.decompose()
    text = soup.get_text()
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text
```

**Step 3: Create RSS fetcher with async and semaphore**

Create `backend/app/tasks/fetcher.py`:

```python
import asyncio
import httpx
import feedparser
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models import Feed, Article, Summary
from app.core import logger
from app.utils.url import content_hash

class RSSFetcher:
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_all(self) -> None:
        """Fetch all active feeds"""
        db: Session = SessionLocal()
        try:
            active_feeds = db.query(Feed).filter(Feed.is_active == True).all()
            logger.info("fetch_started", feed_count=len(active_feeds))

            async with httpx.AsyncClient(timeout=30) as client:
                tasks = [self._fetch_one(feed, client) for feed in active_feeds]
                results = await asyncio.gather(*tasks, return_exceptions=True)

            success_count = sum(1 for r in results if r is not None and not isinstance(r, Exception))
            logger.info("fetch_completed", success=success_count, total=len(active_feeds))
        finally:
            db.close()

    async def _fetch_one(self, feed: Feed, client: httpx.Client) -> int | None:
        """Fetch single feed"""
        async with self.semaphore:
            try:
                response = await client.get(feed.url)
                # feedparser is sync, run in thread
                parsed = await asyncio.to_thread(feedparser.parse, response.content)

                db: Session = SessionLocal()
                try:
                    new_count = 0
                    for entry in parsed.entries[:50]:  # Limit per fetch
                        if await self._process_entry(entry, feed.id, db):
                            new_count += 1

                    feed.last_fetched_at = datetime.utcnow()
                    db.commit()
                    logger.info("feed_fetched", feed=feed.title, new_articles=new_count)
                    return new_count
                finally:
                    db.close()
            except Exception as e:
                logger.error("fetch_failed", feed_url=feed.url, error=str(e))
                return None

    async def _process_entry(self, entry, feed_id: int, db: Session) -> bool:
        """Process single feed entry, return True if new"""
        url = entry.get('link', '')
        title = entry.get('title', '')

        if not url or not title:
            return False

        hash_key = content_hash(url, title)
        existing = db.query(Article).filter(Article.content_hash == hash_key).first()
        if existing:
            return False

        # Extract content
        content = entry.get('content', [{}])[0].get('value', '') if entry.get('content') else entry.get('description', '')

        article = Article(
            content_hash=hash_key,
            url=url,
            title=title,
            content=content[:10000],  # Limit size
            author=entry.get('author'),
            published_at=self._parse_date(entry.get('published')),
            feed_id=feed_id,
        )
        db.add(article)
        db.flush()

        # Create pending summary
        summary = Summary(article_id=article.id, status="pending")
        db.add(summary)

        return True

    def _parse_date(self, date_str: str | None) -> datetime | None:
        """Parse various date formats"""
        if not date_str:
            return None
        try:
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(date_str)
        except:
            return None
```

**Step 4: Create scheduler entry point**

Create `backend/app/tasks/scheduler.py`:

```python
import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.tasks.fetcher import RSSFetcher
from app.tasks.processor import AIProcessor
from app.core import logger
from app.core.config import get_settings

settings = get_settings()

scheduler = AsyncIOScheduler()

@scheduler.scheduled_job('interval', minutes=settings.fetch_interval_minutes)
async def scheduled_fetch():
    logger.info("scheduled_fetch_started")
    fetcher = RSSFetcher()
    await fetcher.fetch_all()
    logger.info("scheduled_fetch_completed")

@scheduler.scheduled_job('interval', minutes=5)
async def scheduled_process():
    logger.info("scheduled_process_started")
    processor = AIProcessor()
    await processor.process_pending()
    logger.info("scheduled_process_completed")

def start_scheduler():
    logger.info("scheduler_starting")
    scheduler.start()
    try:
        asyncio.get_event_loop().run_forever()
    except KeyboardInterrupt:
        scheduler.shutdown()

if __name__ == "__main__":
    start_scheduler()
```

**Step 5: Add APScheduler to requirements**

```txt
apscheduler>=3.0.0
beautifulsoup4>=4.12.0
```

**Step 6: Test fetcher manually**

Create `backend/scripts/test_fetcher.py`:

```python
import asyncio
from app.tasks.fetcher import RSSFetcher

async def main():
    fetcher = RSSFetcher(max_concurrent=3)
    await fetcher.fetch_all()

asyncio.run(main())
```

Run: `cd backend && python scripts/test_fetcher.py`

Expected: Logs showing feed fetch progress

**Step 7: Commit**

```bash
git add backend/
git commit -m "feat: RSS fetcher with concurrent fetching and deduplication"
```

---

## Task 7: AI Processor Service

**Files:**
- Create: `backend/app/tasks/processor.py`
- Create: `backend/app/services/__init__.py`
- Create: `backend/app/services/claude.py`

**Step 1: Create Claude service**

Create `backend/app/services/claude.py`:

```python
import json
from anthropic import AsyncAnthropic
from tenacity import retry, stop_after_attempt, wait_exponential
from app.core.config import get_settings
from app.core import logger

settings = get_settings()

class ClaudeService:
    def __init__(self):
        self.client = AsyncAnthropic(api_key=settings.claude_api_key)
        self.model = "claude-3-5-sonnet-20241022"

    def _build_prompt(self, article_title: str, article_content: str) -> str:
        """Build prompt for article summarization"""
        truncated = article_content[:settings.claude_max_content_length]
        return f"""请阅读以下英文技术文章，生成中文摘要。

标题：{article_title}
正文：{truncated}

请严格按以下 JSON 格式返回，不要包含其他内容：
{{
  "summary": "200字以内的中文摘要",
  "one_liner": "一句话推荐理由，不超过30字",
  "keywords": ["关键词1", "关键词2", "关键词3"]
}}"""

    def _parse_response(self, response_text: str) -> dict:
        """Parse Claude response with defensive handling"""
        text = response_text.strip()
        # Remove markdown code blocks
        if text.startswith("```"):
            text = text.split("\n", 1)[1].rsplit("```", 1)[0]
        return json.loads(text)

    @retry(wait=wait_exponential(min=1, max=60), stop=stop_after_attempt(5))
    async def summarize(self, title: str, content: str) -> dict:
        """Generate summary for article"""
        prompt = self._build_prompt(title, content)

        response = await self.client.messages.create(
            model=self.model,
            max_tokens=1000,
            messages=[{"role": "user", "content": prompt}]
        )

        result = self._parse_response(response.content[0].text)
        logger.info("claude_summary_generated", title=title)
        return result
```

**Step 2: Create AI processor**

Create `backend/app/tasks/processor.py`:

```python
import asyncio
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models import Article, Summary
from app.services.claude import ClaudeService
from app.core import logger
from app.core.config import get_settings

settings = get_settings()

class AIProcessor:
    def __init__(self, max_concurrent: int = None):
        self.claude = ClaudeService()
        self.semaphore = asyncio.Semaphore(max_concurrent or settings.claude_max_concurrency)

    async def process_pending(self) -> None:
        """Process all pending summaries"""
        db: Session = SessionLocal()
        try:
            pending = db.query(Summary).filter(
                Summary.status == "pending"
            ).join(Article).limit(50).all()

            if not pending:
                return

            logger.info("ai_processing_started", count=len(pending))

            async def _process(summary_id: int):
                async with self.semaphore:
                    return await self._generate_summary(summary_id)

            tasks = [_process(s.id) for s in pending]
            await asyncio.gather(*tasks, return_exceptions=True)

            logger.info("ai_processing_completed", total=len(pending))
        finally:
            db.close()

    async def _generate_summary(self, summary_id: int) -> bool:
        """Generate summary for single article

        CRITICAL: Each coroutine gets its own Session to avoid threading issues.
        SQLAlchemy Session is NOT thread/coroutine-safe.
        """
        db: Session = SessionLocal()
        try:
            summary = db.query(Summary).filter(Summary.id == summary_id).first()
            if not summary:
                return False

            article = db.query(Article).filter(Article.id == summary.article_id).first()
            if not article:
                summary.status = "failed"
                summary.error = "Article not found"
                db.commit()
                return False

            result = await self.claude.summarize(article.title, article.content or "")

            summary.status = "completed"
            summary.summary_cn = result["summary"]
            summary.one_liner = result["one_liner"]
            summary.keywords = result["keywords"]
            summary.model_version = "claude-3-5-sonnet"
            db.commit()

            logger.info("summary_completed", article_id=article.id)
            return True

        except Exception as e:
            logger.error("summary_failed", summary_id=summary_id, error=str(e))
            db: Session = SessionLocal()
            try:
                summary = db.query(Summary).filter(Summary.id == summary_id).first()
                if summary:
                    summary.status = "failed"
                    summary.error = str(e)
                    db.commit()
            finally:
                db.close()
            return False
        finally:
            db.close()
```

**Step 3: Test processor manually**

Create `backend/scripts/test_processor.py`:

```python
import asyncio
from app.tasks.processor import AIProcessor

async def main():
    processor = AIProcessor()
    await processor.process_pending()

asyncio.run(main())
```

**Step 4: Commit**

```bash
git add backend/
git commit -m "feat: AI processor with Claude API integration and retry logic"
```

---

## Task 8: API Endpoints - Health & Stats

**Files:**
- Modify: `backend/app/api/health.py`
- Create: `backend/app/api/stats.py`

**Step 1: Implement health endpoint**

Create `backend/app/api/health.py`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models import Feed
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/health")
async def health():
    """Health check endpoint"""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
    }
```

**Step 2: Create stats endpoint**

Create `backend/app/api/stats.py`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.db import get_db
from app.models import Feed, Article, Summary
from app.schemas.summary import StatsResponse
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/stats", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    """Get site statistics"""
    total_feeds = db.query(Feed).count()
    active_feeds = db.query(Feed).filter(Feed.is_active == True).count()
    total_articles = db.query(Article).count()

    yesterday = datetime.utcnow() - timedelta(hours=24)
    articles_today = db.query(Article).filter(Article.created_at >= yesterday).count()

    summaries_pending = db.query(Summary).filter(Summary.status == "pending").count()
    summaries_failed = db.query(Summary).filter(Summary.status == "failed").count()
    summaries_completed = db.query(Summary).filter(Summary.status == "completed").count()

    total_summaries = summaries_pending + summaries_failed + summaries_completed
    completion_rate = summaries_completed / total_summaries if total_summaries > 0 else 0

    last_fetch = db.query(Feed).filter(
        Feed.last_fetched_at.isnot(None)
    ).order_by(Feed.last_fetched_at.desc()).first()

    return StatsResponse(
        total_feeds=total_feeds,
        active_feeds=active_feeds,
        total_articles=total_articles,
        articles_today=articles_today,
        summaries_pending=summaries_pending,
        summaries_failed=summaries_failed,
        summaries_completed=summaries_completed,
        last_fetch_at=last_fetch.last_fetched_at.isoformat() if last_fetch else None,
        completion_rate=completion_rate,
    )
```

**Step 3: Update main.py to include stats router**

```python
from app.api import stats

app.include_router(stats.router, prefix="/api", tags=["stats"])
```

**Step 4: Test endpoints**

Run: `curl http://localhost:8000/api/health`

Run: `curl http://localhost:8000/api/stats`

**Step 5: Commit**

```bash
git add backend/
git commit -m "feat: health and stats API endpoints"
```

---

## Task 9: API Endpoints - Articles & Feeds

**Files:**
- Modify: `backend/app/api/articles.py`
- Modify: `backend/app/api/feeds.py`

**Step 1: Implement articles list endpoint**

Create `backend/app/api/articles.py`:

```python
from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.db import SessionLocal, get_db
from app.models import Article, Feed, Summary
from app.schemas.article import ArticleListItem, ArticleDetail, PaginatedArticlesResponse
from typing import Optional

router = APIRouter()

@router.get("/", response_model=PaginatedArticlesResponse)
async def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    feed_id: Optional[int] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get paginated article list

    NOTE: keyword search only searches titles for MVP.
    Full-text search including keywords requires PostgreSQL.
    """
    query = db.query(
        Article,
        Feed.title.label("feed_title"),
        Feed.category.label("feed_category"),
        Summary.status.label("summary_status"),
        Summary.one_liner,
        Summary.keywords
    ).join(Feed).outerjoin(Summary)

    if feed_id:
        query = query.filter(Article.feed_id == feed_id)

    if keyword:
        # MVP: title-only search (SQLite compatible)
        # TODO: Add full-text search with PostgreSQL + GIN index
        query = query.filter(Article.title.ilike(f"%{keyword}%"))

    total = query.count()
    articles = query.order_by(Article.published_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    items = [
        ArticleListItem(
            id=a.Article.id,
            title=a.Article.title,
            url=a.Article.url,
            one_liner=a.one_liner,
            keywords=a.keywords or [],
            published_at=a.Article.published_at,
            feed_title=a.feed_title,
            feed_category=a.feed_category,
        )
        for a in articles
    ]

    return PaginatedArticlesResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        has_next=page * page_size < total,
    )

@router.get("/latest", response_model=list[ArticleListItem])
async def get_latest_articles(
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get articles from last 24 hours"""
    from datetime import datetime, timedelta
    yesterday = datetime.utcnow() - timedelta(hours=24)

    articles = db.query(
        Article,
        Feed.title.label("feed_title"),
        Feed.category.label("feed_category"),
        Summary.one_liner,
        Summary.keywords
    ).join(Feed).outerjoin(Summary).filter(
        Article.published_at >= yesterday
    ).order_by(Article.published_at.desc()).limit(limit).all()

    return [
        ArticleListItem(
            id=a.Article.id,
            title=a.Article.title,
            url=a.Article.url,
            one_liner=a.one_liner,
            keywords=a.keywords or [],
            published_at=a.Article.published_at,
            feed_title=a.feed_title,
            feed_category=a.feed_category,
        )
        for a in articles
    ]

@router.get("/{id}", response_model=ArticleDetail)
async def get_article(id: int, db: Session = Depends(get_db)):
    """Get article detail with summary"""
    article = db.query(Article, Feed.title.label("feed_title"), Summary).join(
        Feed).outerjoin(Summary, Summary.article_id == Article.id).filter(
        Article.id == id).first()

    if not article:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Article not found")

    a, feed_title, summary = article

    return ArticleDetail(
        id=a.id,
        title=a.title,
        url=a.url,
        content=a.content or "",
        content_hash=a.content_hash,
        author=a.author,
        language=a.language,
        published_at=a.published_at,
        feed_title=feed_title,
        summary_cn=summary.summary_cn if summary else None,
        one_liner=summary.one_liner if summary else None,
        keywords=summary.keywords if summary else [],
        summary_status=summary.status if summary else "pending",
    )
```

**Step 2: Implement feeds endpoint**

Create `backend/app/api/feeds.py`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import Feed
from app.schemas.feed import FeedResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[FeedResponse])
async def list_feeds(db: Session = Depends(get_db)):
    """Get all feeds"""
    feeds = db.query(Feed).order_by(Feed.title).all()
    return [
        FeedResponse(
            id=f.id,
            url=f.url,
            title=f.title,
            description=f.description,
            category=f.category,
            is_active=f.is_active,
            fetch_interval_minutes=f.fetch_interval_minutes,
            last_fetched_at=f.last_fetched_at,
            created_at=f.created_at,
        )
        for f in feeds
    ]

@router.get("/categories", response_model=List[str])
async def list_categories(db: Session = Depends(get_db)):
    """Get all unique categories"""
    categories = db.query(Feed.category).filter(
        Feed.category.isnot(None)
    ).distinct().all()
    return [c[0] for c in categories if c[0]]
```

**Step 3: Test endpoints**

```bash
curl http://localhost:8000/api/articles/
curl http://localhost:8000/api/articles/latest
curl http://localhost:8000/api/feeds/
curl http://localhost:8000/api/feeds/categories
```

**Step 4: Commit**

```bash
git add backend/
git commit -m "feat: articles and feeds API endpoints"
```

---

## Task 10: Frontend Setup - Tailwind & Shadcn

**Files:**
- Create: `frontend/index.html`
- Create: `frontend/src/main.tsx`
- Create: `frontend/src/App.tsx`
- Create: `frontend/tailwind.config.js`
- Create: `frontend/postcss.config.js`
- Create: `frontend/src/lib/utils.ts`

**Step 1: Create frontend/index.html**

```html
<!DOCTYPE html>
<html lang="zh-CN">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>RSS Web Reader</title>
  </head>
  <body>
    <div id="root"></div>
    <script type="module" src="/src/main.tsx"></script>
  </body>
</html>
```

**Step 2: Create frontend/tailwind.config.js**

```js
/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}
```

**Step 3: Create frontend/postcss.config.js**

```js
export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}
```

**Step 4: Create frontend/src/index.css**

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
}
```

**Step 5: Create frontend/src/lib/utils.ts**

```ts
import { clsx, type ClassValue } from 'clsx'
import { twMerge } from 'tailwind-merge'

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}
```

**Step 6: Create frontend/src/main.tsx**

```tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import App from './App'
import './index.css'

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <App />
  </React.StrictMode>,
)
```

**Step 7: Create frontend/src/App.tsx (placeholder)**

```tsx
function App() {
  return <div className="p-8">RSS Web Reader</div>
}

export default App
```

**Step 8: Install dependencies**

Run: `cd frontend && npm install`

**Step 9: Verify dev server runs**

Run: `cd frontend && npm run dev`

Expected: Server at http://localhost:3000

**Step 10: Commit**

```bash
git add frontend/
git commit -m "feat: frontend base setup with Vite, React, Tailwind"
```

---

## Task 11: Frontend - API Client & React Query Setup

**Files:**
- Create: `frontend/src/lib/api.ts`
- Create: `frontend/src/main.tsx` (update)
- Create: `frontend/src/types/index.ts`

**Step 1: Create TypeScript types**

Create `frontend/src/types/index.ts`:

```ts
export interface Article {
  id: number
  title: string
  url: string
  one_liner: string | null
  keywords: string[]
  published_at: string | null
  feed_title: string
  feed_category: string | null
}

export interface ArticleDetail extends Article {
  content: string
  content_hash: string
  author: string | null
  language: string
  summary_cn: string | null
  summary_status: 'pending' | 'completed' | 'failed'
}

export interface PaginatedResponse<T> {
  items: T[]
  total: number
  page: number
  page_size: number
  has_next: boolean
}

export interface Feed {
  id: number
  url: string
  title: string
  description: string | null
  category: string | null
  is_active: boolean
  fetch_interval_minutes: number
  last_fetched_at: string | null
}

export interface Stats {
  total_feeds: number
  active_feeds: number
  total_articles: number
  articles_today: number
  summaries_pending: number
  summaries_failed: number
  summaries_completed: number
  last_fetch_at: string | null
  completion_rate: number
}
```

**Step 2: Create API client**

Create `frontend/src/lib/api.ts`:

```ts
import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
})

export const articlesApi = {
  list: (params: { page?: number; page_size?: number; feed_id?: number; keyword?: string }) =>
    api.get<PaginatedResponse<Article>>('/articles/', { params }),

  getLatest: (limit = 20) =>
    api.get<Article[]>('/articles/latest', { params: { limit } }),

  get: (id: number) =>
    api.get<ArticleDetail>(`/articles/${id}`),
}

export const feedsApi = {
  list: () => api.get<Feed[]>('/feeds/'),

  getCategories: () => api.get<string[]>('/feeds/categories'),
}

export const statsApi = {
  get: () => api.get<Stats>('/stats'),
}

export const healthApi = {
  check: () => api.get<{ status: string }>('/health'),
}
```

**Step 3: Set up React Query**

Update `frontend/src/main.tsx`:

```tsx
import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import App from './App'
import './index.css'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 5 * 60 * 1000, // 5 minutes
      retry: 1,
    },
  },
})

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <App />
    </QueryClientProvider>
  </React.StrictMode>,
)
```

**Step 4: Commit**

```bash
git add frontend/
git commit -m "feat: API client and React Query setup"
```

---

## Task 12: Frontend - ArticleCard Component

**Files:**
- Create: `frontend/src/components/ArticleCard.tsx`
- Create: `frontend/src/hooks/useDebounce.ts`

**Step 1: Create useDebounce hook**

Create `frontend/src/hooks/useDebounce.ts`:

```ts
import { useEffect, useState } from 'react'

export function useDebounce<T>(value: T, delay = 300): T {
  const [debounced, setDebounced] = useState(value)

  useEffect(() => {
    const handler = setTimeout(() => setDebounced(value), delay)
    return () => clearTimeout(handler)
  }, [value, delay])

  return debounced
}
```

**Step 2: Create ArticleCard component**

Create `frontend/src/components/ArticleCard.tsx`:

```tsx
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { articlesApi } from '../lib/api'
import { Article } from '../types'
import { formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'

interface ArticleCardProps {
  article: Article
}

export function ArticleCard({ article }: ArticleCardProps) {
  const [expanded, setExpanded] = useState(false)

  const { data: detail, isLoading } = useQuery({
    queryKey: ['article', article.id],
    queryFn: () => articlesApi.get(article.id).then(res => res.data),
    enabled: expanded,
  })

  const formatDate = (dateStr: string | null) => {
    if (!dateStr) return ''
    return formatDistanceToNow(new Date(dateStr), { addSuffix: true, locale: zhCN })
  }

  return (
    <article className="border-b border-gray-200 py-4">
      {/* Title */}
      <a
        href={article.url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-lg font-semibold text-gray-900 hover:text-blue-600"
      >
        {article.title}
      </a>

      {/* One-liner */}
      {article.one_liner && (
        <p className="text-sm text-gray-600 mt-1">{article.one_liner}</p>
      )}

      {/* Keywords */}
      {article.keywords.length > 0 && (
        <div className="flex flex-wrap gap-2 mt-2">
          {article.keywords.map(kw => (
            <span key={kw} className="px-2 py-0.5 bg-gray-100 text-gray-600 text-xs rounded">
              {kw}
            </span>
          ))}
        </div>
      )}

      {/* Expand button */}
      <button
        onClick={() => setExpanded(!expanded)}
        className="text-sm text-blue-500 mt-2 hover:underline"
      >
        {expanded ? '收起' : '展开摘要'}
      </button>

      {/* Expanded summary */}
      {expanded && (
        <div className="mt-2">
          {isLoading && (
            <div className="bg-yellow-50 p-3 rounded text-sm text-yellow-700">
              ⏳ AI 正在生成摘要...
            </div>
          )}
          {detail && detail.summary_status === 'pending' && (
            <div className="bg-yellow-50 p-3 rounded text-sm text-yellow-700">
              ⏳ AI 摘要生成中，通常需要几分钟
            </div>
          )}
          {detail && detail.summary_status === 'failed' && (
            <div className="bg-red-50 p-3 rounded text-sm text-red-700">
              ⚠️ 摘要生成失败，稍后会自动重试
            </div>
          )}
          {detail && detail.summary_status === 'completed' && detail.summary_cn && (
            <div className="bg-gray-50 p-3 rounded text-sm">
              <p className="font-semibold mb-1">💡 一句话推荐</p>
              <p className="text-gray-600 mb-2">{detail.one_liner}</p>
              <p className="text-gray-700">{detail.summary_cn}</p>
            </div>
          )}
        </div>
      )}

      {/* Meta */}
      <div className="text-xs text-gray-400 mt-2">
        {article.feed_title} · {formatDate(article.published_at)}
      </div>
    </article>
  )
}
```

**Step 3: Add date-fns Chinese locale**

Add to `frontend/package.json` dependencies:
```json
"date-fns": "^3.0.0"
```

**Step 4: Commit**

```bash
git add frontend/
git commit -m "feat: ArticleCard component with expandable summary"
```

---

## Task 13: Frontend - Main Layout & Article List

**Files:**
- Create: `frontend/src/components/Layout.tsx`
- Create: `frontend/src/components/ArticleList.tsx`
- Create: `frontend/src/components/Sidebar.tsx`
- Update: `frontend/src/App.tsx`

**Step 1: Create Sidebar component**

Create `frontend/src/components/Sidebar.tsx`:

```tsx
import { useQuery } from '@tanstack/react-query'
import { feedsApi } from '../lib/api'
import { cn } from '../lib/utils'

interface SidebarProps {
  selectedCategory: string | null
  onSelectCategory: (category: string | null) => void
}

export function Sidebar({ selectedCategory, onSelectCategory }: SidebarProps) {
  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: () => feedsApi.getCategories().then(res => res.data),
  })

  return (
    <aside className="w-full md:w-64 bg-gray-50 md:min-h-screen p-4">
      <h2 className="font-bold text-lg mb-4">分类</h2>

      <button
        onClick={() => onSelectCategory(null)}
        className={cn(
          "w-full text-left px-3 py-2 rounded mb-1",
          !selectedCategory ? "bg-blue-100 text-blue-700" : "hover:bg-gray-100"
        )}
      >
        全部 Feeds
      </button>

      {categories?.map(cat => (
        <button
          key={cat}
          onClick={() => onSelectCategory(cat)}
          className={cn(
            "w-full text-left px-3 py-2 rounded mb-1",
            selectedCategory === cat ? "bg-blue-100 text-blue-700" : "hover:bg-gray-100"
          )}
        >
          {cat}
        </button>
      ))}
    </aside>
  )
}
```

**Step 2: Create ArticleList component**

Create `frontend/src/components/ArticleList.tsx`:

```tsx
import { useQuery } from '@tanstack/react-query'
import { articlesApi } from '../lib/api'
import { ArticleCard } from './ArticleCard'
import { useState } from 'react'

interface ArticleListProps {
  category?: string | null
  keyword?: string
}

export function ArticleList({ category, keyword }: ArticleListProps) {
  const [page, setPage] = useState(1)

  const { data, isLoading, error } = useQuery({
    queryKey: ['articles', page, category, keyword],
    queryFn: () => articlesApi.list({
      page,
      page_size: 20,
      keyword: keyword || undefined,
    }).then(res => res.data),
  })

  if (isLoading) {
    return <div className="p-8 text-center text-gray-500">加载中...</div>
  }

  if (error) {
    return <div className="p-8 text-center text-red-500">加载失败，请稍后重试</div>
  }

  if (!data || data.items.length === 0) {
    return (
      <div className="p-8 text-center text-gray-500">
        {keyword ? '没有找到匹配的文章' : '文章正在采集中，预计几分钟后刷新即可看到内容'}
      </div>
    )
  }

  return (
    <div>
      <div className="px-4 py-2 text-sm text-gray-500">
        共 {data.total} 篇文章
      </div>

      {data.items.map(article => (
        <ArticleCard key={article.id} article={article} />
      ))}

      {/* Pagination */}
      <div className="flex justify-center gap-2 py-4">
        <button
          onClick={() => setPage(p => Math.max(1, p - 1))}
          disabled={page === 1}
          className="px-4 py-2 border rounded disabled:opacity-50"
        >
          上一页
        </button>
        <span className="px-4 py-2">第 {page} 页</span>
        <button
          onClick={() => setPage(p => (data.has_next ? p + 1 : p))}
          disabled={!data.has_next}
          className="px-4 py-2 border rounded disabled:opacity-50"
        >
          下一页
        </button>
      </div>
    </div>
  )
}
```

**Step 3: Create Layout component**

Create `frontend/src/components/Layout.tsx`:

```tsx
import { ReactNode } from 'react'

interface LayoutProps {
  children: ReactNode
}

export function Layout({ children }: LayoutProps) {
  return (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold">RSS Web Reader</h1>
          <SearchBar />
        </div>
      </header>

      {/* Main */}
      <main className="max-w-6xl mx-auto">
        {children}
      </main>
    </div>
  )
}

function SearchBar() {
  // Search implementation in next task
  return null
}
```

**Step 4: Update App.tsx**

```tsx
import { useState } from 'react'
import { Layout } from './components/Layout'
import { Sidebar } from './components/Sidebar'
import { ArticleList } from './components/ArticleList'

function App() {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)

  return (
    <Layout>
      <div className="flex flex-col md:flex-row">
        <Sidebar
          selectedCategory={selectedCategory}
          onSelectCategory={setSelectedCategory}
        />
        <div className="flex-1">
          <ArticleList category={selectedCategory} />
        </div>
      </div>
    </Layout>
  )
}

export default App
```

**Step 5: Commit**

```bash
git add frontend/
git commit -m "feat: main layout with Sidebar and ArticleList"
```

---

## Task 14: Frontend - Search & Empty States

**Files:**
- Update: `frontend/src/components/Layout.tsx`
- Create: `frontend/src/components/EmptyState.tsx`
- Update: `frontend/src/App.tsx`

**Step 1: Create EmptyState component**

Create `frontend/src/components/EmptyState.tsx`:

```tsx
interface EmptyStateProps {
  type: 'loading' | 'no-results' | 'initial'
}

export function EmptyState({ type }: EmptyStateProps) {
  const states = {
    loading: {
      emoji: '⏳',
      title: '加载中...',
      message: '正在获取文章列表',
    },
    'no-results': {
      emoji: '🔍',
      title: '没有找到匹配的文章',
      message: '试试其他关键词',
    },
    initial: {
      emoji: '📡',
      title: '文章正在采集中',
      message: '预计几分钟后刷新即可看到内容',
    },
  }

  const { emoji, title, message } = states[type]

  return (
    <div className="flex flex-col items-center justify-center py-20 text-center">
      <div className="text-6xl mb-4">{emoji}</div>
      <h3 className="text-xl font-semibold text-gray-700 mb-2">{title}</h3>
      <p className="text-gray-500">{message}</p>
    </div>
  )
}
```

**Step 2: Implement SearchBar**

Update `frontend/src/components/Layout.tsx`:

```tsx
import { ReactNode, useState, useEffect } from 'react'
import { useDebounce } from '../hooks/useDebounce'

interface LayoutProps {
  children: ReactNode
  onSearch: (keyword: string) => void
}

export function Layout({ children, onSearch }: LayoutProps) {
  const [searchInput, setSearchInput] = useState('')
  const debouncedSearch = useDebounce(searchInput, 300)

  // Trigger search when debounced value changes
  useEffect(() => {
    onSearch(debouncedSearch)
  }, [debouncedSearch, onSearch])

  return (
    <div className="min-h-screen bg-white">
      <header className="bg-white border-b sticky top-0 z-10">
        <div className="max-w-6xl mx-auto px-4 py-4 flex items-center justify-between">
          <h1 className="text-xl font-bold">RSS Web Reader</h1>
          <input
            type="text"
            placeholder="搜索文章标题..."
            value={searchInput}
            onChange={e => setSearchInput(e.target.value)}
            className="px-4 py-2 border rounded-lg w-64 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
        </div>
      </header>

      <main className="max-w-6xl mx-auto">
        {children}
      </main>
    </div>
  )
}
```

**Step 3: Update App.tsx to handle search**

```tsx
import { useState } from 'react'
import { Layout } from './components/Layout'
import { Sidebar } from './components/Sidebar'
import { ArticleList } from './components/ArticleList'

function App() {
  const [selectedCategory, setSelectedCategory] = useState<string | null>(null)
  const [searchKeyword, setSearchKeyword] = useState('')

  return (
    <Layout onSearch={setSearchKeyword}>
      <div className="flex flex-col md:flex-row">
        <Sidebar
          selectedCategory={selectedCategory}
          onSelectCategory={setSelectedCategory}
        />
        <div className="flex-1">
          <ArticleList
            category={selectedCategory}
            keyword={searchKeyword || undefined}
          />
        </div>
      </div>
    </Layout>
  )
}

export default App
```

**Step 4: Commit**

```bash
git add frontend/
git commit -m "feat: search functionality and empty states"
```

---

## Task 15: Frontend - Responsive Design Refinement

**Files:**
- Update: `frontend/src/components/Sidebar.tsx`
- Update: `frontend/src/components/ArticleCard.tsx`
- Update: `frontend/src/index.css`

**Step 1: Make Sidebar mobile-friendly**

Update `frontend/src/components/Sidebar.tsx`:

```tsx
import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { feedsApi } from '../lib/api'
import { cn } from '../lib/utils'

interface SidebarProps {
  selectedCategory: string | null
  onSelectCategory: (category: string | null) => void
}

export function Sidebar({ selectedCategory, onSelectCategory }: SidebarProps) {
  const [isOpen, setIsOpen] = useState(false)
  const { data: categories } = useQuery({
    queryKey: ['categories'],
    queryFn: () => feedsApi.getCategories().then(res => res.data),
  })

  return (
    <>
      {/* Mobile toggle button */}
      <button
        className="md:hidden fixed bottom-4 right-4 z-50 bg-blue-500 text-white p-3 rounded-full shadow-lg"
        onClick={() => setIsOpen(!isOpen)}
      >
        {isOpen ? '×' : '☰'}
      </button>

      {/* Sidebar - desktop: always visible, mobile: drawer */}
      <aside className={cn(
        "fixed md:static inset-y-0 left-0 z-40 w-64 bg-gray-50 transform transition-transform duration-300",
        "md:min-h-screen md:transform-none md:transition-none",
        isOpen ? "translate-x-0" : "-translate-x-full md:translate-x-0"
      )}>
        <div className="p-4">
          <h2 className="font-bold text-lg mb-4">分类</h2>

          <button
            onClick={() => { onSelectCategory(null); setIsOpen(false) }}
            className={cn(
              "w-full text-left px-3 py-2 rounded mb-1",
              !selectedCategory ? "bg-blue-100 text-blue-700" : "hover:bg-gray-100"
            )}
          >
            全部 Feeds
          </button>

          {categories?.map(cat => (
            <button
              key={cat}
              onClick={() => { onSelectCategory(cat); setIsOpen(false) }}
              className={cn(
                "w-full text-left px-3 py-2 rounded mb-1",
                selectedCategory === cat ? "bg-blue-100 text-blue-700" : "hover:bg-gray-100"
              )}
            >
              {cat}
            </button>
          ))}
        </div>
      </aside>

      {/* Overlay for mobile */}
      {isOpen && (
        <div
          className="md:hidden fixed inset-0 bg-black bg-opacity-50 z-30"
          onClick={() => setIsOpen(false)}
        />
      )}
    </>
  )
}
```

**Step 2: Refine ArticleCard for mobile**

Update `frontend/src/components/ArticleCard.tsx` - adjust padding and font sizes:

```tsx
// Update the article className for better mobile spacing:
<article className="border-b border-gray-200 py-3 px-2 md:px-4">
```

**Step 3: Add responsive utilities**

Update `frontend/src/index.css`:

```css
@tailwind base;
@tailwind components;
@tailwind utilities;

body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', 'Roboto', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* Custom scrollbar for webkit */
::-webkit-scrollbar {
  width: 8px;
}

::-webkit-scrollbar-track {
  background: #f1f1f1;
}

::-webkit-scrollbar-thumb {
  background: #888;
  border-radius: 4px;
}

::-webkit-scrollbar-thumb:hover {
  background: #555;
}
```

**Step 4: Commit**

```bash
git add frontend/
git commit -m "feat: responsive design with mobile sidebar and refinements"
```

---

## Task 16: Deployment Configuration

**Files:**
- Update: `railway.toml`
- Create: `backend/Dockerfile`
- Create: `frontend/Dockerfile`
- Create: `.github/workflows/deploy.yml` (optional)

**Step 1: Update railway.toml for production**

```toml
[build]
builder = "NIXPACKS"

# API Service
[services.api]
command = "uvicorn main:app --host 0.0.0.0 --port $PORT"
env = ["PORT=$PORT"]

# Worker Service
[services.worker]
command = "python -m app.tasks.scheduler"

[deploy]
startCommand = "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT"
healthcheckPath = "/health"
healthcheckTimeout = 300
restartPolicyType = "ON_FAILURE"
```

**Step 2: Create backend Dockerfile**

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Run migrations on start
CMD ["sh", "-c", "alembic upgrade head && uvicorn main:app --host 0.0.0.0 --port $PORT"]
```

**Step 3: Create frontend Dockerfile**

```dockerfile
FROM node:20-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

**Step 4: Create nginx.conf for frontend**

```nginx
server {
    listen 80;
    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass $API_URL;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

**Step 5: Create deployment guide**

Create `docs/DEPLOYMENT.md`:

```markdown
# Deployment Guide

## Railway Deployment

1. Create new project on Railway
2. Add PostgreSQL database
3. Set environment variables:
   - `DATABASE_URL`
   - `CLAUDE_API_KEY`
   - `FETCH_INTERVAL_MINUTES=30`
4. Push to GitHub
5. Connect GitHub repo to Railway
6. Deploy!

## Environment Variables

See `.env.example` for full list.
```

**Step 6: Commit**

```bash
git add .
git commit -m "feat: deployment configuration for Railway"
```

---

## Task 17: Initialization Script & Final Polish

**Files:**
- Create: `backend/scripts/init.py`
- Update: `README.md`

**Step 1: Create initialization script**

Create `backend/scripts/init.py`:

```python
#!/usr/bin/env python
"""
Initialize the RSS Web Reader database and data.
"""
import asyncio
from pathlib import Path
from sqlalchemy.orm import Session
from app.core.db import SessionLocal, engine
from app.models import Feed
from app.tasks.fetcher import RSSFetcher

async def init():
    """Initialize database and import feeds"""
    print("🚀 Initializing RSS Web Reader...")

    # Run migrations
    print("📦 Running database migrations...")
    import subprocess
    subprocess.run(["alembic", "upgrade", "head"], check=True)

    # Import OPML
    print("📡 Importing feeds from OPML...")
    from app.scripts.import_opml import import_feeds
    await import_feeds("../../feeds.opml")

    # Trigger initial fetch
    print("🔍 Fetching initial articles...")
    fetcher = RSSFetcher(max_concurrent=10)
    await fetcher.fetch_all()

    print("✅ Initialization complete!")
    print(f"   - Feeds imported: {SessionLocal().query(Feed).count()}")
    print(f"   - Run 'python -m app.tasks.scheduler' to start background tasks")

if __name__ == "__main__":
    asyncio.run(init())
```

**Step 2: Update README.md with complete instructions**

```markdown
# RSS Web Reader

RSS 聚合 + AI 摘要 + 中文解读

## Features

- 📡 聚合 92 个顶级技术博客
- 🤖 Claude AI 生成中文摘要
- 📱 响应式设计，支持移动端
- 🔍 实时搜索文章
- 🏷️ 智能关键词标签

## Quick Start

### Backend

\`\`\`bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
cp .env.example .env  # Edit .env with your Claude API key
python scripts/init.py  # Initialize database and fetch articles
\`\`\`

### Frontend

\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

Visit http://localhost:3000

## Development

### Start API server

\`\`\`bash
cd backend
uvicorn main:app --reload
\`\`\`

### Start worker (RSS fetcher + AI processor)

\`\`\`bash
cd backend
python -m app.tasks.scheduler
\`\`\`

## Deployment

See [docs/DEPLOYMENT.md](docs/DEPLOYMENT.md)

## License

MIT
```

**Step 3: Add missing Chinese locale import for date-fns**

Make sure `frontend/src/components/ArticleCard.tsx` imports:

```ts
import { formatDistanceToNow } from 'date-fns'
import { zhCN } from 'date-fns/locale'

// Use in function:
formatDistanceToNow(new Date(dateStr), { addSuffix: true, locale: zhCN })
```

**Step 4: Final commit**

```bash
git add .
git commit -m "feat: complete MVP with initialization script and docs"
```

---

## Task 18: Testing & Validation

**Files:**
- Create: `backend/tests/conftest.py`
- Create: `backend/tests/test_api.py`
- Create: `backend/tests/test_fetcher.py`

**Step 1: Create test fixtures**

Create `backend/tests/conftest.py`:

```python
import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.db import Base, get_db

# Test database
TEST_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(bind=engine)

@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()
```

**Step 2: Create API tests**

Create `backend/tests/test_api.py`:

```python
def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_list_feeds_empty(client):
    response = client.get("/api/feeds/")
    assert response.status_code == 200
    assert response.json() == []

def test_list_articles_empty(client):
    response = client.get("/api/articles/")
    assert response.status_code == 200
    assert response.json()["total"] == 0
```

**Step 3: Create fetcher tests**

Create `backend/tests/test_fetcher.py`:

```python
from app.utils.url import normalize_url, content_hash

def test_normalize_url_removes_utm():
    url = "https://example.com?utm_source=google&foo=bar"
    result = normalize_url(url)
    assert "utm_source" not in result
    assert "foo=bar" in result

def test_content_hash_consistent():
    h1 = content_hash("https://example.com", "Title")
    h2 = content_hash("https://example.com", "Title")
    assert h1 == h2

def test_content_hash_different():
    h1 = content_hash("https://example.com", "Title1")
    h2 = content_hash("https://example.com", "Title2")
    assert h1 != h2
```

**Step 4: Run tests**

Run: `cd backend && pytest tests/ -v`

**Step 5: Commit**

```bash
git add backend/tests/
git commit -m "test: add API and utility tests"
```

---

## Completion Checklist

- [ ] Project skeleton created
- [ ] Database models defined
- [ ] Pydantic schemas created
- [ ] OPML import script working
- [ ] RSS fetcher fetching articles
- [ ] AI processor generating summaries
- [ ] API endpoints tested
- [ ] Frontend displaying articles
- [ ] Search functionality working
- [ ] Mobile responsive design
- [ ] Deployment configured
- [ ] Tests passing
- [ ] Documentation complete

---

## Summary

This plan builds the complete RSS Web Reader MVP in 18 tasks:

1. **Project skeleton** - Monorepo setup
2. **Core configuration** - Database, logging, settings
3. **Database models** - Feed, Article, Summary
4. **Pydantic schemas** - Request/response validation
5. **OPML import** - Load 92 feeds
6. **RSS fetcher** - Async fetching with concurrency control
7. **AI processor** - Claude integration with retry logic
8. **Health & stats API** - Monitoring endpoints
9. **Articles & feeds API** - Main data endpoints
10. **Frontend setup** - Vite, React, Tailwind
11. **API client** - Axios + React Query
12. **ArticleCard** - Expandable summaries
13. **Main layout** - Sidebar + article list
14. **Search** - Debounced search with empty states
15. **Responsive design** - Mobile-friendly UI
16. **Deployment** - Railway configuration
17. **Init script** - One-command setup
18. **Testing** - API and utility tests

**Estimated time**: 3-4 days for a focused developer
**Tech risk**: Low - all technologies are mature
**Cost**: ~$5-10/month for Railway + Claude API usage
