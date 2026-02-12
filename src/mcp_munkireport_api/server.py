"""FastAPI server implementation that wraps the Flask API."""

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, HTTPException, Query

from .client import MunkiReportAPIClient
from .config import settings
from .schemas import (
    DatabaseStatsResponse,
    ErrorSummaryResponse,
    EventListResponse,
    GetEventsRequest,
    HealthResponse,
    MachineDetailsResponse,
    MachineListResponse,
    MDMEnrollmentSummaryResponse,
    QueryMachinesRequest,
    StatusResponse,
    TableSummaryRequest,
    TableSummaryResponse,
)


# Global client instance
_client: MunkiReportAPIClient | None = None


def get_client() -> MunkiReportAPIClient:
    """Get the API client instance."""
    if _client is None:
        raise RuntimeError("API client not initialized")
    return _client


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan - startup and shutdown."""
    global _client
    _client = MunkiReportAPIClient(settings.api_url, settings.api_key)
    yield
    await _client.close()
    _client = None


def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="MunkiReport API",
        description="FastAPI wrapper for MunkiReport Flask API",
        version="0.1.0",
        lifespan=lifespan,
    )

    # Health and status endpoints

    @app.get("/api/v1/health", response_model=HealthResponse, tags=["status"])
    async def health_check() -> dict[str, Any]:
        """Check API health status."""
        client = get_client()
        return await client.health_check()

    @app.get("/api/v1/status", response_model=StatusResponse, tags=["status"])
    async def get_status() -> dict[str, Any]:
        """Get API status including database connectivity."""
        client = get_client()
        return await client.get_status()

    # Machine endpoints

    @app.post(
        "/api/v1/machines/query",
        response_model=MachineListResponse,
        tags=["machines"],
    )
    async def query_machines(request: QueryMachinesRequest) -> dict[str, Any]:
        """Query machines with flexible filters and optional related data.

        Supports filtering by MDM status, manifest/business_unit, last seen date, and more.
        Can include reportdata and mdm_status tables.
        """
        client = get_client()
        data = await client.query_machines(
            filters=request.filters,
            include=request.include,
            order_by=request.order_by,
            limit=request.limit,
        )
        return {"data": data, "count": len(data)}

    @app.get(
        "/api/v1/machines/{serial_number}",
        response_model=MachineDetailsResponse,
        tags=["machines"],
    )
    async def get_machine_details(serial_number: str) -> dict[str, Any]:
        """Get complete details about a specific machine by serial number."""
        client = get_client()
        data = await client.get_machine_details(serial_number)
        if data is None:
            raise HTTPException(status_code=404, detail=f"Machine not found: {serial_number}")
        return {"data": data, "found": True}

    @app.get(
        "/api/v1/machines/mdm/summary",
        response_model=MDMEnrollmentSummaryResponse,
        tags=["machines"],
    )
    async def get_mdm_enrollment_summary() -> dict[str, Any]:
        """Get summary statistics of MDM enrollment status across all machines."""
        client = get_client()
        data = await client.get_mdm_enrollment_summary()
        return {"data": data}

    # Event endpoints

    @app.post(
        "/api/v1/events/query",
        response_model=EventListResponse,
        tags=["events"],
    )
    async def get_events(request: GetEventsRequest) -> dict[str, Any]:
        """Query events with optional machine information.

        Supports filtering by type (danger, error, warning), timestamp, etc.
        """
        client = get_client()
        data = await client.get_events(
            filters=request.filters,
            include_machine=request.include_machine,
            order_by=request.order_by,
            limit=request.limit,
        )
        return {"data": data, "count": len(data)}

    @app.get(
        "/api/v1/events/errors/summary",
        response_model=ErrorSummaryResponse,
        tags=["events"],
    )
    async def get_error_summary() -> dict[str, Any]:
        """Get summary of errors and warnings by machine."""
        client = get_client()
        data = await client.get_error_summary()
        return {"data": data}

    @app.get(
        "/api/v1/events/critical",
        response_model=EventListResponse,
        tags=["events"],
    )
    async def get_recent_critical_events(
        hours: int = Query(default=24, description="Number of hours to look back"),
        limit: int = Query(default=50, description="Maximum number of results"),
    ) -> dict[str, Any]:
        """Get recent critical events (danger/error) from the last N hours."""
        client = get_client()
        data = await client.get_recent_critical_events(hours=hours, limit=limit)
        return {"data": data, "count": len(data)}

    # Database endpoints

    @app.get(
        "/api/v1/database/stats",
        response_model=DatabaseStatsResponse,
        tags=["database"],
    )
    async def get_database_stats() -> dict[str, Any]:
        """Get overall database statistics including table counts and size."""
        client = get_client()
        data = await client.get_database_stats()
        return {"data": data}

    @app.post(
        "/api/v1/database/table/summary",
        response_model=TableSummaryResponse,
        tags=["database"],
    )
    async def get_table_summary(request: TableSummaryRequest) -> dict[str, Any]:
        """Get aggregated statistics for any table in the database."""
        client = get_client()
        data = await client.get_table_summary(
            table_name=request.table_name,
            group_by=request.group_by,
            filters=request.filters,
        )
        return {"data": data}

    return app


# Create the default app instance
app = create_app()
