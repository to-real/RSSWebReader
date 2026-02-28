"""
Test to verify summary display issue
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

import pytest
from sqlalchemy.orm import Session
from app.core.db import SessionLocal
from app.models import Article, Summary


def test_first_page_has_summaries(db: Session):
    """Verify that first page of articles shows summaries if available"""
    # Get first page from API
    from fastapi import Query
    from typing import Optional

    # Simulate API call
    db = SessionLocal()
    query = db.query(
        Article,
        Summary.one_liner,
        Summary.status
    ).outerjoin(Summary)

    articles = query.limit(20).all()

    print(f"\n=== First 20 articles ===")
    has_summary_count = 0
    for a in articles:
        has_one_liner = a.one_liner is not None
        if has_one_liner:
            has_summary_count += 1
        print(f"ID={a.Article.id}, has_one_liner={has_one_liner}, status={a.status}")

    print(f"\nArticles with one_liner on first page: {has_summary_count}/20")

    # Check total completed summaries in DB
    total_completed = db.query(Summary).filter(Summary.status == 'completed').count()
    print(f"Total completed summaries in DB: {total_completed}")

    db.close()

    # This should fail if we have summaries but they're not on first page
    if total_completed > 0:
        assert has_summary_count > 0, "Has summaries in DB but none on first page!"


if __name__ == "__main__":
    import sys
    sys.path.insert(0, '.')
    test_first_page_has_summaries(None)
