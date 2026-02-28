import pytest

from app.models import Article, Feed, Summary


@pytest.mark.asyncio
async def test_article_detail_includes_source_type(client, db):
    feed = Feed(
        url="https://source-type.example/feed.xml",
        title="Source Type Feed",
        category="安全",
        source_type="个人博客",
        is_active=True,
        fetch_interval_minutes=30,
    )
    db.add(feed)
    db.flush()

    article = Article(
        content_hash="source-type-hash-1",
        url="https://source-type.example/post-1",
        title="Post 1",
        content="hello",
        feed_id=feed.id,
    )
    db.add(article)
    db.flush()

    db.add(
        Summary(
            article_id=article.id,
            status="completed",
            one_liner="line",
            summary_cn="summary",
            keywords=["k1"],
        )
    )
    db.commit()

    response = await client.get(f"/api/articles/{article.id}")
    assert response.status_code == 200

    payload = response.json()
    assert payload["source_type"] == "个人博客"


@pytest.mark.asyncio
async def test_list_feeds_includes_source_type(client, db):
    db.add(
        Feed(
            url="https://feed-source.example/rss.xml",
            title="Feed Source",
            category="AI",
            source_type="研究机构",
            is_active=True,
            fetch_interval_minutes=30,
        )
    )
    db.commit()

    response = await client.get("/api/feeds/")
    assert response.status_code == 200

    payload = response.json()
    assert payload[0]["source_type"] == "研究机构"


@pytest.mark.asyncio
async def test_articles_filter_by_source_domain_category(client, db):
    security_feed = Feed(
        url="https://security-source.example/rss.xml",
        title="Security Source",
        category="安全",
        source_type="个人博客",
        is_active=True,
        fetch_interval_minutes=30,
    )
    ai_feed = Feed(
        url="https://ai-source.example/rss.xml",
        title="AI Source",
        category="AI",
        source_type="研究机构",
        is_active=True,
        fetch_interval_minutes=30,
    )
    db.add_all([security_feed, ai_feed])
    db.flush()

    db.add_all(
        [
            Article(
                content_hash="security-hash-1",
                url="https://security-source.example/post-1",
                title="Security Post",
                content="security content",
                feed_id=security_feed.id,
            ),
            Article(
                content_hash="ai-hash-1",
                url="https://ai-source.example/post-1",
                title="AI Post",
                content="ai content",
                feed_id=ai_feed.id,
            ),
        ]
    )
    db.commit()

    response = await client.get("/api/articles/?category=安全&page_size=20")
    assert response.status_code == 200

    payload = response.json()
    assert payload["total"] == 1
    assert payload["items"][0]["feed_category"] == "安全"
