from app.utils.url import normalize_url, content_hash

def test_normalize_url_removes_utm():
    url = "https://example.com?utm_source=google&foo=bar"
    result = normalize_url(url)
    assert "utm_source" not in result
    assert "foo=bar" in result

def test_content_hash_consistent():
    h1 = content_hash("https://example.com", "Title1")
    h2 = content_hash("https://example.com", "Title1")
    assert h1 == h2

def test_content_hash_different_titles():
    h1 = content_hash("https://example.com", "Title1")
    h2 = content_hash("https://example.com", "title2")
    assert h1 != h2
