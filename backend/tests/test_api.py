from app.core.config import settings

def test_health_check(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

def test_list_feeds_empty(client):
    response = client.get("/api/feeds/")
    assert response.status_code == 200
    assert response.json() == []

def test_list_articles_empty(client):
    response = client.get("/api/articles/")
    assert response.status_code == 200
    assert response.json()["total"] == 0
