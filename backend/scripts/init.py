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
from app.core import logger

async def init():
    """Initialize database and import feeds"""
    print("🚀 Initializing RSS Web Reader...")

    # Import OPML
    print("📡 Importing feeds from OPML...")
    from app.scripts.import_opml import import_feeds

    # Resolve path to feeds.opml at project root
    project_root = Path(__file__).parent.parent.parent
    feeds_opml = project_root / "feeds.opml"

    await import_feeds(str(feeds_opml))

    # Trigger initial fetch
    print("🔍 Fetching initial articles...")
    fetcher = RSSFetcher(max_concurrent=10)
    await fetcher.fetch_all()

    print("✅ Initialization complete!")

    # Show stats
    db: Session = SessionLocal()
    try:
        from app.models import Article
        feed_count = db.query(Feed).count()
        article_count = db.query(Article).count()
        print(f"   - Feeds imported: {feed_count}")
        print(f"   - Articles fetched: {article_count}")
        print(f"   - Run 'python -m app.tasks.scheduler' to start background tasks")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(init())
