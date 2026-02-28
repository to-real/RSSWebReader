#!/usr/bin/env python
"""
Import manual source taxonomy CSV and update feeds.
"""
import csv
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.db import SessionLocal
from app.models import Feed
from app.core.taxonomy import DOMAIN_CATEGORY_SET, SOURCE_TYPE_SET


def normalize_domain(url: str) -> str:
    host = urlparse(url).netloc.lower().strip()
    if host.startswith("www."):
        host = host[4:]
    return host


def load_rows(csv_path: Path) -> list[dict]:
    if not csv_path.exists():
        raise FileNotFoundError(f"CSV not found: {csv_path}")

    with csv_path.open("r", encoding="utf-8-sig", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader)


def import_taxonomy(csv_path: Path) -> None:
    rows = load_rows(csv_path)
    db = SessionLocal()
    try:
        feeds = db.query(Feed).all()
        by_url = {feed.url: feed for feed in feeds}

        by_domain = {}
        for feed in feeds:
            domain = normalize_domain(feed.url)
            by_domain.setdefault(domain, []).append(feed)

        updated = 0
        skipped = 0

        for idx, row in enumerate(rows, start=2):
            feed_url = (row.get("feed_url") or "").strip()
            domain = (row.get("domain") or "").strip().lower()
            category = (row.get("category") or "").strip()
            source_type = (row.get("source_type") or "").strip()

            if not category and not source_type:
                skipped += 1
                continue

            if category and category not in DOMAIN_CATEGORY_SET:
                print(f"[row {idx}] invalid category: {category}")
                skipped += 1
                continue

            if source_type and source_type not in SOURCE_TYPE_SET:
                print(f"[row {idx}] invalid source_type: {source_type}")
                skipped += 1
                continue

            target = None
            if feed_url:
                target = by_url.get(feed_url)
                if not target:
                    print(f"[row {idx}] feed_url not found: {feed_url}")
                    skipped += 1
                    continue
            else:
                if not domain:
                    print(f"[row {idx}] missing feed_url and domain")
                    skipped += 1
                    continue
                candidates = by_domain.get(domain, [])
                if len(candidates) == 1:
                    target = candidates[0]
                elif len(candidates) == 0:
                    print(f"[row {idx}] domain not found: {domain}")
                    skipped += 1
                    continue
                else:
                    print(f"[row {idx}] domain ambiguous ({domain}), use feed_url")
                    skipped += 1
                    continue

            target.category = category or None
            target.source_type = source_type or None
            updated += 1

        db.commit()
    finally:
        db.close()

    print(f"Imported taxonomy from {csv_path}")
    print(f"Updated rows: {updated}")
    print(f"Skipped rows: {skipped}")


if __name__ == "__main__":
    default_path = Path(__file__).parent.parent / "data" / "feed_taxonomy.csv"
    source = Path(sys.argv[1]) if len(sys.argv) > 1 else default_path
    import_taxonomy(source)
