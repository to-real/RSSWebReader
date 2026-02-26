from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text
from datetime import datetime
from app.core.db import Base

class Article(Base):
    __tablename__ = "articles"

    id = Column(Integer, primary_key=True)
    content_hash = Column(String, unique=True, nullable=False, index=True)
    url = Column(String, nullable=False)
    title = Column(String, nullable=False)
    content = Column(Text, nullable=True)
    author = Column(String, nullable=True)
    language = Column(String, default="en")
    published_at = Column(DateTime, nullable=True)
    feed_id = Column(Integer, ForeignKey("feeds.id"), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
