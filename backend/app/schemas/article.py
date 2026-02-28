from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class ArticleListItem(BaseModel):
    id: int
    title: str
    url: str
    one_liner: Optional[str] = None
    keywords: List[str] = []
    published_at: Optional[datetime] = None
    feed_title: str
    feed_category: Optional[str] = None

class ArticleDetail(BaseModel):
    id: int
    title: str
    url: str
    content: str
    content_hash: str
    summary_cn: Optional[str] = None
    one_liner: Optional[str] = None
    keywords: List[str] = []
    summary_status: str = "pending"
    published_at: Optional[datetime] = None
    feed_title: str
    source_type: Optional[str] = None
    author: Optional[str] = None

class PaginatedArticlesResponse(BaseModel):
    items: List[ArticleListItem]
    total: int
    page: int
    page_size: int
    has_next: bool
