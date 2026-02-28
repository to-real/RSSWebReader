"""
Test that exactly matches the API query
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.db import SessionLocal
from app.models import Article, Feed, Summary
from sqlalchemy import case, desc


def test_api_query_exact():
    """Exact replica of API query"""
    db = SessionLocal()

    # Exact API query
    query = db.query(
        Article,
        Feed.title.label("feed_title"),
        Feed.category.label("feed_category"),
        Summary.status.label("summary_status"),
        Summary.one_liner,
        Summary.keywords
    ).join(Feed).outerjoin(Summary)

    total = query.count()
    print(f"Total articles: {total}")

    # Apply ordering from API
    articles = query.order_by(
        case((Summary.status == 'completed', 0), else_=1).label('has_summary'),
        desc(Article.published_at)
    ).limit(20).all()

    print(f"\nFirst 20 articles (exact API query):")
    has_summary = 0
    for a in articles[:10]:
        has = bool(a.one_liner)
        if has:
            has_summary += 1
        print(f"  ID={a.Article.id}, has_one_liner={has}, title={a.Article.title[:40]}...")

    print(f"\nWith summaries: {has_summary}/20")

    # Check what Summary.status actually is
    print("\nChecking Summary.status values:")
    for a in articles[:5]:
        print(f"  ID={a.Article.id}, Summary.status={a.summary_status}")

    db.close()


if __name__ == "__main__":
    test_api_query_exact()
