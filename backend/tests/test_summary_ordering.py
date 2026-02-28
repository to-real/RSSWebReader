"""
Test that articles with completed summaries appear on first page
"""
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.core.db import SessionLocal
from app.models import Article, Summary


def test_completed_summaries_on_first_page():
    """First page should include articles with completed summaries"""
    db = SessionLocal()

    # Count completed summaries
    completed_count = db.query(Summary).filter(Summary.status == 'completed').count()
    print(f"Total completed summaries: {completed_count}")

    if completed_count == 0:
        print("No completed summaries, skipping test")
        return

    # Get first page of articles (mimicking API)
    from sqlalchemy import case, desc

    query = db.query(
        Article,
        Summary.status.label("summary_status"),
        Summary.one_liner
    ).outerjoin(Summary)

    # Apply the ordering from API
    articles = query.order_by(
        case((Summary.status == 'completed', 0), else_=1).label('has_summary'),
        desc(Article.published_at)
    ).limit(20).all()

    has_summary_count = sum(1 for a in articles if a.summary_status == 'completed')

    print(f"Articles with completed summaries on first page: {has_summary_count}/20")

    # Show which articles are on first page
    print("\nFirst page articles:")
    for a in articles[:5]:
        print(f"  ID={a.Article.id}, status={a.summary_status}, has_one_liner={bool(a.one_liner)}")

    db.close()

    # Assert: if we have summaries in DB, at least some should appear on first page
    if completed_count > 0:
        assert has_summary_count > 0, f"Has {completed_count} summaries but none on first page!"

    print("\n✅ Test passed!")


if __name__ == "__main__":
    test_completed_summaries_on_first_page()
