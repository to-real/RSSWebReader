from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import Feed
from app.schemas.feed import FeedResponse
from typing import List

router = APIRouter()

@router.get("/", response_model=List[FeedResponse])
async def list_feeds(db: Session = Depends(get_db)):
    """Get all feeds"""
    feeds = db.query(Feed).order_by(Feed.title).all()
    return [
        FeedResponse(
            id=f.id,
            url=f.url,
            title=f.title,
            description=f.description,
            category=f.category,
            source_type=f.source_type,
            is_active=f.is_active,
            fetch_interval_minutes=f.fetch_interval_minutes,
            last_fetched_at=f.last_fetched_at,
            created_at=f.created_at,
        )
        for f in feeds
    ]

@router.get("/categories", response_model=List[str])
async def list_categories(db: Session = Depends(get_db)):
    """Get all unique categories"""
    categories = db.query(Feed.category).filter(
        Feed.category.isnot(None)
    ).distinct().all()
    return [c[0] for c in categories if c[0]]
