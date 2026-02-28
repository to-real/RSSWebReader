from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class RecommendationCreate(BaseModel):
    """Schema for creating a new recommendation"""
    feed_url: str
    feed_name: Optional[str] = None
    reason: Optional[str] = None
    contact: Optional[str] = None


class RecommendationResponse(BaseModel):
    """Schema for recommendation response"""
    id: int
    feed_url: str
    feed_name: Optional[str] = None
    reason: Optional[str] = None
    is_reviewed: bool = False
    is_approved: bool = False
    created_at: datetime

    class Config:
        from_attributes = True
