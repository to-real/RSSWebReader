from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import Recommendation
from app.schemas.recommendation import RecommendationCreate, RecommendationResponse
from typing import List

router = APIRouter()


@router.post("/", response_model=dict)
async def create_recommendation(
    recommendation: RecommendationCreate,
    db: Session = Depends(get_db)
):
    """Submit a new RSS feed recommendation"""
    # Check if URL already recommended
    existing = db.query(Recommendation).filter(
        Recommendation.feed_url == recommendation.feed_url
    ).first()

    if existing:
        return {
            "success": True,
            "message": "这个 RSS 源已经被推荐过了，我们会尽快处理！"
        }

    # Create new recommendation
    db_rec = Recommendation(
        feed_url=recommendation.feed_url,
        feed_name=recommendation.feed_name,
        reason=recommendation.reason,
        contact=recommendation.contact,
    )
    db.add(db_rec)
    db.commit()

    return {
        "success": True,
        "message": "感谢推荐！我们会尽快审核这个 RSS 源。"
    }


@router.get("/", response_model=List[RecommendationResponse])
async def list_recommendations(
    skip: int = 0,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """List all recommendations (for admin use)"""
    recommendations = db.query(Recommendation).order_by(
        Recommendation.created_at.desc()
    ).offset(skip).limit(limit).all()
    return recommendations
