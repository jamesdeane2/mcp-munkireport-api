"""Pydantic models for request/response schemas."""

from typing import Any, Optional
from pydantic import BaseModel, Field


# Request Models

class QueryMachinesRequest(BaseModel):
    """Request model for querying machines."""
    filters: Optional[dict[str, Any]] = Field(
        default=None,
        description=(
            "Filters to apply. Examples: {'mdm_enrolled': 'No', "
            "'serial_number': 'ABC123', 'manifest': 'Pablo'}. "
            "Special keys: 'last_seen_before', 'last_seen_after' (Unix timestamps)."
        ),
    )
    include: Optional[list[str]] = Field(
        default=None,
        description="Related tables to include: 'reportdata', 'mdm_status'",
    )
    order_by: Optional[str] = Field(
        default=None,
        description="Order specification (e.g., 'hostname', 'last_seen DESC')",
    )
    limit: Optional[int] = Field(
        default=None,
        description="Maximum number of results",
    )


class GetEventsRequest(BaseModel):
    """Request model for querying events."""
    filters: Optional[dict[str, Any]] = Field(
        default=None,
        description=(
            "Filters to apply. Examples: "
            "{'type': ['error', 'warning'], 'serial_number': 'ABC123'}. "
            "Special keys: 'timestamp_before', 'timestamp_after'"
        ),
    )
    include_machine: bool = Field(
        default=False,
        description="Whether to include machine details",
    )
    order_by: Optional[str] = Field(
        default=None,
        description="Order specification (e.g., 'timestamp DESC')",
    )
    limit: Optional[int] = Field(
        default=None,
        description="Maximum number of results",
    )


class TableSummaryRequest(BaseModel):
    """Request model for table summary."""
    table_name: str = Field(
        ...,
        description="Name of the table to summarize",
    )
    group_by: Optional[str] = Field(
        default=None,
        description="Optional field to group by",
    )
    filters: Optional[dict[str, Any]] = Field(
        default=None,
        description="Optional filters to apply",
    )


# Response Models

class HealthResponse(BaseModel):
    """Response model for health check."""
    status: str


class StatusResponse(BaseModel):
    """Response model for API status."""
    status: str
    database_connected: bool
    version: Optional[str] = None


class MachineResponse(BaseModel):
    """Response model for a single machine."""
    serial_number: str
    hostname: Optional[str] = None
    computer_name: Optional[str] = None
    machine_model: Optional[str] = None
    os_version: Optional[str] = None

    class Config:
        extra = "allow"


class MachineListResponse(BaseModel):
    """Response model for list of machines."""
    data: list[dict[str, Any]]
    count: int


class MachineDetailsResponse(BaseModel):
    """Response model for machine details."""
    data: Optional[dict[str, Any]] = None
    found: bool = True
    message: Optional[str] = None


class MDMEnrollmentSummaryResponse(BaseModel):
    """Response model for MDM enrollment summary."""
    data: dict[str, Any]


class EventListResponse(BaseModel):
    """Response model for list of events."""
    data: list[dict[str, Any]]
    count: int


class ErrorSummaryResponse(BaseModel):
    """Response model for error summary."""
    data: dict[str, Any]


class DatabaseStatsResponse(BaseModel):
    """Response model for database statistics."""
    data: dict[str, Any]


class TableSummaryResponse(BaseModel):
    """Response model for table summary."""
    data: dict[str, Any]


class ErrorResponse(BaseModel):
    """Response model for errors."""
    detail: str
