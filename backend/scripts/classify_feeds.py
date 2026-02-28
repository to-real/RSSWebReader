#!/usr/bin/env python
"""
Classify feeds using AI (handles all feeds in batches)
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.db import SessionLocal
from app.models import Feed
from app.services.claude import ClaudeService
import json
import asyncio


VALID_CATEGORIES = [
    "AI/ML", "Engineering", "Business", "Security",
    "Web", "Systems", "Culture", "Science",
    "Design", "Productivity"
]


async def classify_batch(feeds, claude):
    """Classify a batch of feeds"""
    feed_list = []
    for f in feeds:
        feed_list.append(f"- {f.title}")

    prompt = f"""请给以下 RSS feeds 分类。每个 feed 分配一个最合适的类别。

可用类别: {', '.join(VALID_CATEGORIES)}

返回 JSON 格式，不要包含其他内容:
{{"{feeds[0].title}": "AI/ML", "{feeds[1].title}": "Engineering", ...}}

Feeds:
{chr(10).join(feed_list)}"""

    response = await claude.client.messages.create(
        model=claude.model,
        max_tokens=4000,
        messages=[{"role": "user", "content": prompt}]
    )

    # Parse response
    text = response.content[0].text.strip()
    if text.startswith("```"):
        text = text.split("\n", 1)[1].rsplit("```", 1)[0]

    return json.loads(text)


def classify_feeds():
    """Classify all feeds using AI"""
    db = SessionLocal()
    feeds = db.query(Feed).filter(Feed.category == None).all()
    db.close()

    if not feeds:
        print("✅ All feeds already classified!")
        return

    print(f"📊 Classifying {len(feeds)} unclassified feeds...")

    claude = ClaudeService()
    updated = 0

    # Process in batches of 20
    batch_size = 20
    for i in range(0, len(feeds), batch_size):
        batch = feeds[i:i+batch_size]
        print(f"\n📦 Batch {i//batch_size + 1}: {len(batch)} feeds")

        db = SessionLocal()
        try:
            classification = asyncio.run(classify_batch(batch, claude))

            # Update database
            for f in batch:
                if f.title in classification:
                    new_category = classification[f.title]
                    if new_category in VALID_CATEGORIES:
                        feed_obj = db.query(Feed).filter(Feed.id == f.id).first()
                        feed_obj.category = new_category
                        updated += 1
                        print(f"  ✅ {f.title[:40]}... → {new_category}")

            db.commit()

        except Exception as e:
            print(f"  ❌ Batch failed: {e}")
            db.rollback()
        finally:
            db.close()

    # Final stats
    db = SessionLocal()
    print(f"\n✅ Updated {updated} feeds")

    print("\n📈 Category breakdown:")
    for cat in VALID_CATEGORIES:
        count = db.query(Feed).filter(Feed.category == cat).count()
        if count > 0:
            print(f"   {cat}: {count}")

    still_unclassified = db.query(Feed).filter(Feed.category == None).count()
    if still_unclassified > 0:
        print(f"   Uncategorized: {still_unclassified}")

    db.close()


if __name__ == "__main__":
    classify_feeds()
