import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_endpoint(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["service"] == "The Lenny Growth Assistant API"
    assert "database" in data
    assert "llm_provider" in data


@pytest.mark.asyncio
async def test_providers_status_endpoint(client: AsyncClient):
    response = await client.get("/api/v1/providers/status")
    assert response.status_code == 200
    data = response.json()
    assert "provider" in data
    assert "available_providers" in data
    assert "ollama" in data["available_providers"]
