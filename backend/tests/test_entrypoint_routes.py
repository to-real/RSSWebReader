import pytest
from httpx import ASGITransport, AsyncClient

from app.core.db import get_db
from main import app as entrypoint_app


@pytest.mark.asyncio
async def test_main_entrypoint_exposes_stats_under_api_stats(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    entrypoint_app.dependency_overrides[get_db] = override_get_db
    try:
        transport = ASGITransport(app=entrypoint_app)
        async with AsyncClient(transport=transport, base_url="http://testserver") as client:
            stats_response = await client.get("/api/stats/")
            assert stats_response.status_code == 200

            legacy_response = await client.get("/api/")
            assert legacy_response.status_code == 404
    finally:
        entrypoint_app.dependency_overrides.clear()
