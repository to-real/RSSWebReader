from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from app.core.db import get_db
from app.models import Article, Feed, Summary
from app.schemas.article import ArticleListItem, ArticleDetail, PaginatedArticlesResponse
from typing import Optional
from datetime import datetime, timedelta

router = APIRouter()

@router.get("/", response_model=PaginatedArticlesResponse)
async def list_articles(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    feed_id: Optional[int] = None,
    keyword: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Get paginated article list

    NOTE: keyword search only searches titles for MVP.
    Full-text search including keywords requires PostgreSQL.
    """
    query = db.query(
        Article,
        Feed.title.label("feed_title"),
        Feed.category.label("feed_category"),
        Summary.status.label("summary_status"),
        Summary.one_liner,
        Summary.keywords
    ).join(Feed).outerjoin(Summary)

    if feed_id:
        query = query.filter(Article.feed_id == feed_id)

    if keyword:
        # MVP: title-only search (SQLite compatible)
        query = query.filter(Article.title.ilike(f"%{keyword}%"))

    total = query.count()
    articles = query.order_by(Article.published_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

    items = [
        ArticleListItem(
            id=a.Article.id,
            title=a.Article.title,
            url=a.Article.url,
            one_liner=a.one_liner,
            keywords=a.keywords or [],
            published_at=a.Article.published_at,
            feed_title=a.feed_title,
            feed_category=a.feed_category,
        )
        for a in articles
    ]

    return PaginatedArticlesResponse(
        items=items,
        total=total,
        page=page,
        page_size=page_size,
        has_next=page * page_size < total,
    )

@router.get("/latest", response_model=list[ArticleListItem])
async def get_latest_articles(
    limit: int = Query(20, ge=1, le=50),
    db: Session = Depends(get_db)
):
    """Get articles from last 24 hours"""
    yesterday = datetime.utcnow() - timedelta(hours=24)

    articles = db.query(
        Article,
        Feed.title.label("feed_title"),
        Feed.category.label("feed_category"),
        Summary.one_liner,
        Summary.keywords
    ).join(Feed).outerjoin(Summary).filter(
        Article.published_at >= yesterday
    ).order_by(Article.published_at.desc()).limit(limit).all()

    return [
        ArticleListItem(
            id=a.Article.id,
            title=a.Article.title,
            url=a.Article.url,
            one_liner=a.one_liner,
            keywords=a.keywords or [],
            published_at=a.Article.published_at,
            feed_title=a.feed_title,
            feed_category=a.feed_category,
        )
        for a in articles
    ]

@router.get("/{id}", response_model=ArticleDetail)
async def get_article(id: int, db: Session = Depends(get_db)):
    """Get article detail with summary"""
    article = db.query(Article, Feed.title.label("feed_title"), Summary).join(
        Feed).outerjoin(
        Summary, Summary.article_id == Article.id
    ).filter(Article.id == id).first()

    if not article:
        from fastapi import HTTPException
        raise HTTPException(status_code=404, detail="Article not found")

    a, feed_title, summary = article

    return ArticleDetail(
        id=a.id,
        title=a.title,
        url=a.url,
        content=a.content or "",
        content_hash=a.content_hash,
        author=a.author,
        language=a.language,
        published_at=a.published_at,
        feed_title=feed_title,
        summary_cn=summary.summary_cn if summary else None,
        one_liner=summary.one_liner if summary else None,
        keywords=summary.keywords if summary else [],
        summary_status=summary.status if summary else "pending",
    )
