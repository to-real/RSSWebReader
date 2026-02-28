from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.core.db import get_db
from app.models import Feed, Article, Summary
from app.schemas.summary import StatsResponse
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/", response_model=StatsResponse)
async def get_stats(db: Session = Depends(get_db)):
    """Get site statistics"""
    total_feeds = db.query(Feed).count()
    active_feeds = db.query(Feed).filter(Feed.is_active == True).count()
    total_articles = db.query(Article).count()

    yesterday = datetime.utcnow() - timedelta(hours=24)
    articles_today = db.query(Article).filter(Article.created_at >= yesterday).count()

    summaries_pending = db.query(Summary).filter(Summary.status == "pending").count()
    summaries_failed = db.query(Summary).filter(Summary.status == "failed").count()
    summaries_completed = db.query(Summary).filter(Summary.status == "completed").count()

    total_summaries = summaries_pending + summaries_failed + summaries_completed
    completion_rate = summaries_completed / total_summaries if total_summaries > 0 else 0

    last_fetch = db.query(Feed).filter(
        Feed.last_fetched_at.isnot(None)
    ).order_by(Feed.last_fetched_at.desc()).first()

    return StatsResponse(
        total_feeds=total_feeds,
        active_feeds=active_feeds,
        total_articles=total_articles,
        articles_today=articles_today,
        summaries_pending=summaries_pending,
        summaries_failed=summaries_failed,
        summaries_completed=summaries_completed,
        last_fetch_at=last_fetch.last_fetched_at.isoformat() if last_fetch else None,
        completion_rate=completion_rate,
    )
