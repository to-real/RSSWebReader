from pydantic import BaseModel, ConfigDict
from typing import List, Optional

class SummaryResponse(BaseModel):
    model_config = ConfigDict(protected_namespaces=())

    id: int
    article_id: int
    status: str
    summary_cn: Optional[str] = None
    one_liner: Optional[str] = None
    keywords: List[str] = []
    model_version: Optional[str] = None

class StatsResponse(BaseModel):
    total_feeds: int
    active_feeds: int
    total_articles: int
    articles_today: int
    summaries_pending: int
    summaries_failed: int
    summaries_completed: int
    last_fetch_at: Optional[str] = None
    completion_rate: float
