import asyncio
import feedparser
import requests  # requests works better on Windows SSL than httpx
from datetime import datetime
from typing import Optional
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models import Feed, Article, Summary
from app.core.logging import logger
from app.utils.url import content_hash
from app.utils.html import clean_html

class RSSFetcher:
    def __init__(self, max_concurrent: int = 10):
        self.semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_all(self) -> None:
        """Fetch all active feeds"""
        db: Session = SessionLocal()
        try:
            active_feeds = db.query(Feed).filter(Feed.is_active == True).all()
            logger.info("fetch_started", feed_count=len(active_feeds))

            tasks = [self._fetch_one(feed) for feed in active_feeds]
            results = await asyncio.gather(*tasks, return_exceptions=True)

            success_count = sum(1 for r in results if r is not None and not isinstance(r, Exception))
            logger.info("fetch_completed", success=success_count, total=len(active_feeds))
        finally:
            db.close()

    async def _fetch_one(self, feed: Feed) -> Optional[int]:
        """Fetch single feed using requests (sync) in thread pool"""
        async with self.semaphore:
            try:
                # Use requests in thread pool (better SSL on Windows)
                # Per-feed SSL verification setting
                verify_ssl = not getattr(feed, 'skip_ssl_verification', False)
                if not verify_ssl:
                    logger.warning("ssl_verification_skipped", feed_url=feed.url)

                response = await asyncio.to_thread(
                    requests.get,
                    feed.url,
                    timeout=30,
                    headers={'User-Agent': 'RSS-Web-Reader/1.0'},
                    verify=verify_ssl
                )
                response.raise_for_status()

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
        cleaned_content = clean_html(content) if content else ''

        article = Article(
            content_hash=hash_key,
            url=url,
            title=title,
            content=cleaned_content[:10000],  # Limit size
            author=entry.get('author'),
            published_at=self._parse_date(entry.get('published')),
            feed_id=feed_id,
        )
        db.add(article)
        db.flush()

        # Check if summary already exists (handle duplicate creation)
        existing_summary = db.query(Summary).filter(Summary.article_id == article.id).first()
        if not existing_summary:
            summary = Summary(article_id=article.id, status="pending")
            db.add(summary)

        return True

    def _parse_date(self, date_str: Optional[str]) -> Optional[datetime]:
        """Parse various date formats"""
        if not date_str:
            return None
        try:
            from email.utils import parsedate_to_datetime
            return parsedate_to_datetime(date_str)
        except:
            return None
