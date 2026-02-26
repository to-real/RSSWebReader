import asyncio
from app.tasks.fetcher import RSSFetcher

async def main():
    fetcher = RSSFetcher(max_concurrent=3)  # Test with lower concurrency
    await fetcher.fetch_all()

if __name__ == "__main__":
    asyncio.run(main())
