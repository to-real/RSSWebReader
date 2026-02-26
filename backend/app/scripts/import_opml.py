import asyncio
import sys
from pathlib import Path

# Add backend directory to Python path
backend_dir = Path(__file__).parent.parent.parent
sys.path.insert(0, str(backend_dir))

from sqlalchemy.orm import Session
from app.core.db import SessionLocal, engine
from app.models import Feed
from app.scripts.opml_parser import parse_opml
from app.core import logger

async def import_feeds(opml_path: str = "feeds.opml"):
    """Import feeds from OPML file"""
    # Resolve path relative to project root (go up from backend/app/scripts to RSSWebReader)
    project_root = Path(__file__).parent.parent.parent.parent
    full_path = project_root / opml_path

    feeds_data = parse_opml(str(full_path))

    db: Session = SessionLocal()
    try:
        imported = 0
        for feed_data in feeds_data:
            existing = db.query(Feed).filter(Feed.url == feed_data.url).first()
            if not existing:
                feed = Feed(
                    url=feed_data.url,
                    title=feed_data.title,
                    description=feed_data.description,
                    is_active=True,
                    fetch_interval_minutes=30
                )
                db.add(feed)
                imported += 1
        db.commit()
        logger.info("opml_import_completed", total=len(feeds_data), imported=imported)
        print(f"Imported {imported}/{len(feeds_data)} feeds")
    finally:
        db.close()

if __name__ == "__main__":
    asyncio.run(import_feeds())
