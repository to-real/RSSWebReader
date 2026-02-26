import pytest
from app.schemas import FeedCreate, FeedResponse

def test_feed_create_schema():
    feed = FeedCreate(url="https://example.com/feed", title="Test Feed")
    assert feed.url == "https://example.com/feed"
    assert feed.fetch_interval_minutes == 30  # default value
