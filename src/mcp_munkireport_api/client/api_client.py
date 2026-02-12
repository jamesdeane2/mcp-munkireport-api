"""Async HTTP client for Flask MunkiReport API."""

import httpx
from typing import Any, Optional
from urllib.parse import urljoin


class MunkiReportAPIClient:
    """Async client for making requests to Flask MunkiReport API."""

    def __init__(self, base_url: str, api_key: str, timeout: float = 30.0):
        """Initialize API client.

        Args:
            base_url: Base URL of the API (e.g., http://10.254.6.14:5030)
            api_key: API key for authentication
            timeout: Request timeout in seconds
        """
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.timeout = timeout
        self._client: Optional[httpx.AsyncClient] = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Get or create the async HTTP client."""
        if self._client is None or self._client.is_closed:
            self._client = httpx.AsyncClient(
                headers={"X-API-Key": self.api_key},
                timeout=self.timeout,
                follow_redirects=True,
            )
        return self._client

    async def _make_request(
        self,
        method: str,
        endpoint: str,
        json: Optional[dict[str, Any]] = None,
        params: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Make HTTP request to API.

        Args:
            method: HTTP method (GET, POST)
            endpoint: API endpoint (e.g., /api/v1/tools/query_machines)
            json: JSON body for POST requests
            params: Query parameters for GET requests

        Returns:
            Response JSON data

        Raises:
            httpx.HTTPError: On request failure
        """
        client = await self._get_client()
        url = urljoin(self.base_url, endpoint)

        response = await client.request(
            method=method,
            url=url,
            json=json,
            params=params,
        )

        response.raise_for_status()
        return response.json()

    async def health_check(self) -> dict[str, Any]:
        """Check API health status."""
        return await self._make_request("GET", "/api/v1/health")

    async def get_status(self) -> dict[str, Any]:
        """Get API status including database connectivity."""
        return await self._make_request("GET", "/api/v1/status")

    # Machine endpoints

    async def query_machines(
        self,
        filters: Optional[dict[str, Any]] = None,
        include: Optional[list[str]] = None,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[dict[str, Any]]:
        """Query machines with filters.

        Args:
            filters: Dictionary of filters to apply
            include: List of related tables to include
            order_by: Order specification
            limit: Maximum number of results

        Returns:
            List of machine dictionaries
        """
        result = await self._make_request(
            "POST",
            "/api/v1/tools/query_machines",
            json={
                "filters": filters,
                "include": include,
                "order_by": order_by,
                "limit": limit,
            },
        )
        return result.get("data", [])

    async def get_machine_details(self, serial_number: str) -> Optional[dict[str, Any]]:
        """Get complete details for a specific machine.

        Args:
            serial_number: Machine serial number

        Returns:
            Machine details dictionary or None if not found
        """
        try:
            result = await self._make_request(
                "GET",
                f"/api/v1/tools/get_machine_details/{serial_number}",
            )
            return result.get("data")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    async def get_mdm_enrollment_summary(self) -> dict[str, Any]:
        """Get MDM enrollment summary statistics.

        Returns:
            Summary dictionary with enrollment statistics
        """
        result = await self._make_request(
            "GET", "/api/v1/tools/get_mdm_enrollment_summary"
        )
        return result.get("data", {})

    # Event endpoints

    async def get_events(
        self,
        filters: Optional[dict[str, Any]] = None,
        include_machine: bool = False,
        order_by: Optional[str] = None,
        limit: Optional[int] = None,
    ) -> list[dict[str, Any]]:
        """Query events with optional machine information.

        Args:
            filters: Dictionary of filters to apply
            include_machine: Whether to include machine details
            order_by: Order specification
            limit: Maximum number of results

        Returns:
            List of event dictionaries
        """
        result = await self._make_request(
            "POST",
            "/api/v1/tools/get_events",
            json={
                "filters": filters,
                "include_machine": include_machine,
                "order_by": order_by,
                "limit": limit,
            },
        )
        return result.get("data", [])

    async def get_error_summary(self) -> dict[str, Any]:
        """Get summary of errors and warnings by machine.

        Returns:
            Summary dictionary with error statistics
        """
        result = await self._make_request("GET", "/api/v1/tools/get_error_summary")
        return result.get("data", {})

    async def get_recent_critical_events(
        self, hours: int = 24, limit: int = 50
    ) -> list[dict[str, Any]]:
        """Get recent critical events (danger/error).

        Args:
            hours: Number of hours to look back
            limit: Maximum number of results

        Returns:
            List of critical event dictionaries
        """
        result = await self._make_request(
            "GET",
            "/api/v1/tools/get_recent_critical_events",
            params={"hours": hours, "limit": limit},
        )
        return result.get("data", [])

    # Database endpoints

    async def get_database_stats(self) -> dict[str, Any]:
        """Get overall database statistics.

        Returns:
            Database statistics dictionary
        """
        result = await self._make_request("GET", "/api/v1/tools/get_database_stats")
        return result.get("data", {})

    async def get_table_summary(
        self,
        table_name: str,
        group_by: Optional[str] = None,
        filters: Optional[dict[str, Any]] = None,
    ) -> dict[str, Any]:
        """Get aggregated statistics for a table.

        Args:
            table_name: Name of the table to summarize
            group_by: Optional field to group by
            filters: Optional filters to apply

        Returns:
            Summary dictionary
        """
        result = await self._make_request(
            "POST",
            "/api/v1/tools/get_table_summary",
            json={
                "table_name": table_name,
                "group_by": group_by,
                "filters": filters,
            },
        )
        return result.get("data", {})

    # Profile endpoints

    async def get_machine_profiles(self, serial_number: str) -> list[dict[str, Any]]:
        """Get all configuration profiles installed on a machine.

        Args:
            serial_number: Machine serial number

        Returns:
            List of profile dictionaries or empty list if none found
        """
        try:
            result = await self._make_request(
                "GET",
                f"/api/v1/tools/get_machine_profiles/{serial_number}",
            )
            return result.get("data", [])
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return []
            raise

    # FileVault endpoints

    async def get_filevault_status(self, serial_number: str) -> Optional[dict[str, Any]]:
        """Get FileVault encryption status for a machine.

        Args:
            serial_number: Machine serial number

        Returns:
            FileVault status dictionary or None if not found
        """
        try:
            result = await self._make_request(
                "GET",
                f"/api/v1/tools/get_filevault_status/{serial_number}",
            )
            return result.get("data")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    # Firewall endpoints

    async def get_firewall_status(self, serial_number: str) -> Optional[dict[str, Any]]:
        """Get firewall status for a machine.

        Args:
            serial_number: Machine serial number

        Returns:
            Firewall status dictionary or None if not found
        """
        try:
            result = await self._make_request(
                "GET",
                f"/api/v1/tools/get_firewall_status/{serial_number}",
            )
            return result.get("data")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    # iCloud endpoints

    async def get_icloud_status(self, serial_number: str) -> Optional[dict[str, Any]]:
        """Get iCloud account status for a machine.

        Args:
            serial_number: Machine serial number

        Returns:
            iCloud status dictionary or None if not found
        """
        try:
            result = await self._make_request(
                "GET",
                f"/api/v1/tools/get_icloud_status/{serial_number}",
            )
            return result.get("data")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    # Local admin endpoints

    async def get_local_admins(self, serial_number: str) -> Optional[dict[str, Any]]:
        """Get local admin users for a machine.

        Args:
            serial_number: Machine serial number

        Returns:
            Local admins dictionary or None if not found
        """
        try:
            result = await self._make_request(
                "GET",
                f"/api/v1/tools/get_local_admins/{serial_number}",
            )
            return result.get("data")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    # Microsoft Defender endpoints

    async def get_defender_status(self, serial_number: str) -> Optional[dict[str, Any]]:
        """Get Microsoft Defender status for a machine.

        Args:
            serial_number: Machine serial number

        Returns:
            Defender status dictionary or None if not found
        """
        try:
            result = await self._make_request(
                "GET",
                f"/api/v1/tools/get_defender_status/{serial_number}",
            )
            return result.get("data")
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return None
            raise

    # Storage endpoints

    async def get_storage_report(self, serial_number: str) -> list[dict[str, Any]]:
        """Get storage/disk report for a machine.

        Args:
            serial_number: Machine serial number

        Returns:
            List of disk dictionaries or empty list if none found
        """
        try:
            result = await self._make_request(
                "GET",
                f"/api/v1/tools/get_storage_report/{serial_number}",
            )
            return result.get("data", [])
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                return []
            raise

    async def close(self):
        """Close the HTTP client."""
        if self._client is not None and not self._client.is_closed:
            await self._client.aclose()
            self._client = None

    async def __aenter__(self):
        """Async context manager entry."""
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        """Async context manager exit."""
        await self.close()
