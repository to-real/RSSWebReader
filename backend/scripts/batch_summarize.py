#!/usr/bin/env python
"""
Batch process summaries with concurrent execution and progress tracking
"""
import sys
import time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import asyncio
from app.tasks.processor import AIProcessor
from app.core.db import SessionLocal
from app.models import Summary
from datetime import datetime


async def batch_process(concurrency: int = 2, max_articles: int = None):
    """Process all pending summaries with progress tracking"""

    processor = AIProcessor(max_concurrent=concurrency)
    start_time = time.time()

    while True:
        db = SessionLocal()
        pending_count = db.query(Summary).filter(Summary.status == "pending").count()

        # Track progress
        completed_before = db.query(Summary).filter(Summary.status == "completed").count()
        failed_before = db.query(Summary).filter(Summary.status == "failed").count()
        db.close()

        if pending_count == 0:
            print(f"\n✅ No more pending summaries!")
            break

        if max_articles and (completed_before + failed_before) >= max_articles:
            print(f"\n✅ Reached max_articles limit: {max_articles}")
            break

        print(f"\n{'='*60}")
        print(f"📊 {datetime.now().strftime('%H:%M:%S')} | Pending: {pending_count} | Completed: {completed_before} | Failed: {failed_before}")
        print(f"⏱️  Elapsed: {int((time.time() - start_time)/60)} min")

        # Process one batch (max 50 at a time)
        await processor.process_pending()

        # Small delay to let API breathe
        await asyncio.sleep(1)

    # Final stats
    db = SessionLocal()
    stats = {}
    for status in ["pending", "completed", "failed"]:
        stats[status] = db.query(Summary).filter(Summary.status == status).count()
    db.close()

    elapsed = int((time.time() - start_time)/60)
    print(f"\n{'='*60}")
    print(f"✅ All done! Elapsed: {elapsed} min")
    print(f"📈 Final stats: {stats}")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--concurrency", type=int, default=2, help="Concurrent API calls")
    parser.add_argument("--max", type=int, help="Max articles to process (default: all)")
    args = parser.parse_args()

    print(f"🚀 Starting batch processing")
    print(f"   Concurrency: {args.concurrency}")
    print(f"   Max articles: {args.max or 'all pending'}")

    asyncio.run(batch_process(args.concurrency, args.max))
