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
        # Using ClaudeService which supports NewAPI/Zhipu compatibility
        self.ai_service = ClaudeService()
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

            result = await self.ai_service.summarize(article.title, article.content or "")

            summary.status = "completed"
            summary.summary_cn = result["summary"]
            summary.one_liner = result["one_liner"]
            summary.keywords = result["keywords"]
            summary.model_version = "claude-3-5-sonnet"  # Uses NewAPI endpoint
            db.commit()

            logger.info("summary_completed", article_id=article.id)
            return True

        except Exception as e:
            logger.error("summary_failed", summary_id=summary_id, error=str(e))
            # Rollback the failed transaction first
            db.rollback()
            # Now update the status in a fresh transaction
            try:
                summary = db.query(Summary).filter(Summary.id == summary_id).first()
                if summary:
                    summary.status = "failed"
                    summary.error = str(e)
                    db.commit()
            except Exception as inner_e:
                logger.error("summary_status_update_failed", summary_id=summary_id, error=str(inner_e))
                db.rollback()
            return False
        finally:
            db.close()
