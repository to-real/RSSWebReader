from sqlalchemy import Column, Integer, String, DateTime, Boolean
from datetime import datetime
from app.core.db import Base


class Recommendation(Base):
    """User-submitted RSS feed recommendations"""
    __tablename__ = "recommendations"

    id = Column(Integer, primary_key=True)
    feed_url = Column(String, nullable=False)
    feed_name = Column(String, nullable=True)
    reason = Column(String, nullable=True)
    contact = Column(String, nullable=True)  # Optional email for follow-up
    is_reviewed = Column(Boolean, default=False)
    is_approved = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    reviewed_at = Column(DateTime, nullable=True)
