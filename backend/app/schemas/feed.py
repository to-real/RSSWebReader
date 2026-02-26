from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class FeedBase(BaseModel):
    url: str
    title: str
    description: Optional[str] = None
    category: Optional[str] = None
    fetch_interval_minutes: int = 30


class FeedCreate(FeedBase):
    pass


class FeedResponse(FeedBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_active: bool
    last_fetched_at: Optional[datetime] = None
    created_at: datetime
