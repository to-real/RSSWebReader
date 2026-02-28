#!/usr/bin/env python
"""
Export current feeds into a manual taxonomy CSV template.
"""
import csv
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.db import SessionLocal
from app.models import Feed
from app.core.taxonomy import DOMAIN_CATEGORIES, DOMAIN_CATEGORY_SET, SOURCE_TYPES


def normalize_domain(url: str) -> str:
    host = urlparse(url).netloc.lower().strip()
    if host.startswith("www."):
        host = host[4:]
    return host


def export_template(output_path: Path) -> None:
    db = SessionLocal()
    try:
        feeds = db.query(Feed).order_by(Feed.title.asc()).all()
    finally:
        db.close()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "feed_url",
                "domain",
                "feed_title",
                "current_category",
                "category",
                "source_type",
            ],
        )
        writer.writeheader()
        for feed in feeds:
            suggested_category = feed.category if (feed.category in DOMAIN_CATEGORY_SET) else ""
            writer.writerow(
                {
                    "feed_url": feed.url,
                    "domain": normalize_domain(feed.url),
                    "feed_title": feed.title,
                    "current_category": feed.category or "",
                    "category": suggested_category,
                    "source_type": feed.source_type or "",
                }
            )

    print(f"Exported {len(feeds)} feeds -> {output_path}")
    print("Allowed category values:", ", ".join(DOMAIN_CATEGORIES))
    print("Allowed source_type values:", ", ".join(SOURCE_TYPES))


if __name__ == "__main__":
    default_path = Path(__file__).parent.parent / "data" / "feed_taxonomy.csv"
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else default_path
    export_template(target)
