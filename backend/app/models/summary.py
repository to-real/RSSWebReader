from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Text, JSON
from datetime import datetime
from app.core.db import Base

class Summary(Base):
    __tablename__ = "summaries"

    id = Column(Integer, primary_key=True)
    article_id = Column(Integer, ForeignKey("articles.id"), unique=True, nullable=False)
    status = Column(String, default="pending")  # pending/completed/failed
    summary_cn = Column(Text, nullable=True)
    one_liner = Column(String, nullable=True)
    # JSON type works with both SQLite and PostgreSQL (no migration needed)
    keywords = Column(JSON, nullable=True)  # Stores ["kw1", "kw2", ...]
    model_version = Column(String, nullable=True)
    error = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
