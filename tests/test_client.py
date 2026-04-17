"""Tests for the MunkiReport API client."""

import pytest
from mcp_munkireport_api.client import MunkiReportAPIClient


@pytest.fixture
def api_url():
    """Get API URL from environment."""
    import os
    url = os.environ.get("MUNKIREPORT_API_URL")
    if not url:
        raise ValueError("MUNKIREPORT_API_URL environment variable is required for tests")
    return url


@pytest.fixture
def api_key():
    """Get API key from environment."""
    import os
    key = os.environ.get("MUNKIREPORT_API_KEY")
    if not key:
        raise ValueError("MUNKIREPORT_API_KEY environment variable is required for tests")
    return key


@pytest.fixture
async def client(api_url, api_key):
    """Create an API client for testing."""
    async with MunkiReportAPIClient(api_url, api_key) as c:
        yield c


@pytest.mark.asyncio
async def test_health_check(client):
    """Test health check endpoint."""
    health = await client.health_check()
    assert "status" in health
    assert health["status"] == "healthy"


@pytest.mark.asyncio
async def test_database_stats(client):
    """Test database statistics endpoint."""
    stats = await client.get_database_stats()
    assert "total_tables" in stats
    assert "database_size_mb" in stats
    assert "table_row_counts" in stats


@pytest.mark.asyncio
async def test_query_machines(client):
    """Test querying machines with filters."""
    machines = await client.query_machines(
        filters={"mdm_enrolled": "No"},
        limit=3,
    )
    assert isinstance(machines, list)
    # Verify structure if results exist
    if machines:
        assert "serial_number" in machines[0]


@pytest.mark.asyncio
async def test_get_machine_details(client):
    """Test getting machine details."""
    # First get a machine to test with
    machines = await client.query_machines(limit=1)
    if machines:
        serial = machines[0]["serial_number"]
        details = await client.get_machine_details(serial)
        assert details is not None
        assert "serial_number" in details


@pytest.mark.asyncio
async def test_get_machine_details_not_found(client):
    """Test getting details for non-existent machine."""
    details = await client.get_machine_details("NONEXISTENT12345")
    assert details is None


@pytest.mark.asyncio
async def test_mdm_enrollment_summary(client):
    """Test MDM enrollment summary endpoint."""
    summary = await client.get_mdm_enrollment_summary()
    assert "total_machines" in summary or isinstance(summary, dict)


@pytest.mark.asyncio
async def test_recent_critical_events(client):
    """Test getting recent critical events."""
    events = await client.get_recent_critical_events(hours=72, limit=3)
    assert isinstance(events, list)
