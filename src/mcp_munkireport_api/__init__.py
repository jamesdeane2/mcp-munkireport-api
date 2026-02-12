"""MunkiReport API - FastAPI + MCP wrapper for MunkiReport API."""

__version__ = "0.1.0"

from .server import app, create_app
from .client import MunkiReportAPIClient
from .mcp_server import mcp

__all__ = ["app", "create_app", "MunkiReportAPIClient", "mcp"]
