import asyncio
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from app.tasks.fetcher import RSSFetcher
from app.tasks.processor import AIProcessor
from app.core.logging import logger
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
