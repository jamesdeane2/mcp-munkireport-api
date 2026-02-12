"""Tests for the FastAPI endpoints."""

import pytest
from httpx import AsyncClient, ASGITransport

from mcp_munkireport_api.server import create_app


@pytest.fixture
def app():
    """Create a test app instance."""
    return create_app()


@pytest.fixture
async def client(app):
    """Create an async test client."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest.mark.asyncio
async def test_health_endpoint(client):
    """Test the health check endpoint."""
    response = await client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert "status" in data


@pytest.mark.asyncio
async def test_status_endpoint(client):
    """Test the status endpoint."""
    response = await client.get("/api/v1/status")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_query_machines_endpoint(client):
    """Test the query machines endpoint."""
    response = await client.post(
        "/api/v1/machines/query",
        json={"filters": {"mdm_enrolled": "No"}, "limit": 3},
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "count" in data


@pytest.mark.asyncio
async def test_get_machine_details_not_found(client):
    """Test getting details for non-existent machine."""
    response = await client.get("/api/v1/machines/NONEXISTENT12345")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_mdm_summary_endpoint(client):
    """Test the MDM enrollment summary endpoint."""
    response = await client.get("/api/v1/machines/mdm/summary")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


@pytest.mark.asyncio
async def test_query_events_endpoint(client):
    """Test the query events endpoint."""
    response = await client.post(
        "/api/v1/events/query",
        json={"filters": None, "limit": 5},
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "count" in data


@pytest.mark.asyncio
async def test_error_summary_endpoint(client):
    """Test the error summary endpoint."""
    response = await client.get("/api/v1/events/errors/summary")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_critical_events_endpoint(client):
    """Test the critical events endpoint."""
    response = await client.get("/api/v1/events/critical?hours=24&limit=10")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data
    assert "count" in data


@pytest.mark.asyncio
async def test_database_stats_endpoint(client):
    """Test the database stats endpoint."""
    response = await client.get("/api/v1/database/stats")
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


@pytest.mark.asyncio
async def test_table_summary_endpoint(client):
    """Test the table summary endpoint."""
    response = await client.post(
        "/api/v1/database/table/summary",
        json={"table_name": "machine"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "data" in data


@pytest.mark.asyncio
async def test_openapi_docs(client):
    """Test that OpenAPI docs are available."""
    response = await client.get("/docs")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_openapi_json(client):
    """Test that OpenAPI JSON schema is available."""
    response = await client.get("/openapi.json")
    assert response.status_code == 200
    data = response.json()
    assert "openapi" in data
    assert "paths" in data
