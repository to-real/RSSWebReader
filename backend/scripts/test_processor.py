import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from app.tasks.processor import AIProcessor

async def main():
    processor = AIProcessor()
    await processor.process_pending()

if __name__ == "__main__":
    asyncio.run(main())
