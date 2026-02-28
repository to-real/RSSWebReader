import pytest


@pytest.mark.asyncio
async def test_health_check(client):
    response = await client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_api_health_check(client):
    response = await client.get("/api/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@pytest.mark.asyncio
async def test_list_feeds_empty(client):
    response = await client.get("/api/feeds/")
    assert response.status_code == 200
    assert response.json() == []

@pytest.mark.asyncio
async def test_list_articles_empty(client):
    response = await client.get("/api/articles/")
    assert response.status_code == 200
    assert response.json()["total"] == 0
