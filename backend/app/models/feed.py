from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime
from app.core.db import Base

class Feed(Base):
    __tablename__ = "feeds"

    id = Column(Integer, primary_key=True)
    url = Column(String, unique=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=True)
    category = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    fetch_interval_minutes = Column(Integer, default=30)
    last_fetched_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
