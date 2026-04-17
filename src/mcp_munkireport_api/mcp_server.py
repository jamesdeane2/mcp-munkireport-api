"""FastMCP server that exposes MunkiReport API as MCP tools."""

from typing import Any, Optional

from fastmcp import FastMCP

from .client import MunkiReportAPIClient
from .config import settings

# Create the MCP server
mcp = FastMCP(
    name="munkireport-api",
    instructions=(
        "MunkiReport API tools for querying Mac fleet management data. "
        "Use these tools to query machines, events, MDM status, and database statistics."
    ),
)

# Global client instance
_client: MunkiReportAPIClient | None = None


def get_client() -> MunkiReportAPIClient:
    """Get or create the API client."""
    global _client
    if _client is None:
        _client = MunkiReportAPIClient(settings.api_url, settings.api_key)
    return _client


@mcp.tool()
async def query_machines(
    filters: Optional[dict[str, Any]] = None,
    include: Optional[list[str]] = None,
    order_by: Optional[str] = None,
    limit: Optional[int] = None,
) -> list[dict[str, Any]]:
    """Query machines with flexible filters and optional related data.

    Args:
        filters: Filters to apply. Examples: {'mdm_enrolled': 'No', 'serial_number': 'ABC123'}.
                 Special keys: 'last_seen_before', 'last_seen_after' (Unix timestamps).
        include: Related tables to include: 'reportdata', 'mdm_status'
        order_by: Order specification (e.g., 'hostname', 'last_seen DESC')
        limit: Maximum number of results

    Returns:
        List of machine dictionaries
    """
    client = get_client()
    return await client.query_machines(
        filters=filters,
        include=include,
        order_by=order_by,
        limit=limit,
    )


@mcp.tool()
async def get_machine_details(serial_number: str) -> dict[str, Any] | None:
    """Get complete details about a specific machine by serial number.

    Args:
        serial_number: Machine serial number

    Returns:
        Machine details dictionary or None if not found
    """
    client = get_client()
    return await client.get_machine_details(serial_number)


@mcp.tool()
async def get_mdm_enrollment_summary() -> dict[str, Any]:
    """Get summary statistics of MDM enrollment status across all machines.

    Returns:
        Summary dictionary with enrollment statistics
    """
    client = get_client()
    return await client.get_mdm_enrollment_summary()


@mcp.tool()
async def get_events(
    filters: Optional[dict[str, Any]] = None,
    include_machine: bool = False,
    order_by: Optional[str] = None,
    limit: Optional[int] = None,
) -> list[dict[str, Any]]:
    """Query events with optional machine information.

    Args:
        filters: Filters to apply. Examples: {'type': ['error', 'warning'], 'serial_number': 'ABC123'}.
                 Special keys: 'timestamp_before', 'timestamp_after'
        include_machine: Whether to include machine details
        order_by: Order specification (e.g., 'timestamp DESC')
        limit: Maximum number of results

    Returns:
        List of event dictionaries
    """
    client = get_client()
    return await client.get_events(
        filters=filters,
        include_machine=include_machine,
        order_by=order_by,
        limit=limit,
    )


@mcp.tool()
async def get_error_summary() -> dict[str, Any]:
    """Get summary of errors and warnings by machine.

    Returns:
        Summary dictionary with error statistics
    """
    client = get_client()
    return await client.get_error_summary()


@mcp.tool()
async def get_recent_critical_events(
    hours: int = 24,
    limit: int = 50,
) -> list[dict[str, Any]]:
    """Get recent critical events (danger/error) from the last N hours.

    Args:
        hours: Number of hours to look back (default: 24)
        limit: Maximum number of results (default: 50)

    Returns:
        List of critical event dictionaries
    """
    client = get_client()
    return await client.get_recent_critical_events(hours=hours, limit=limit)


@mcp.tool()
async def get_database_stats() -> dict[str, Any]:
    """Get overall database statistics including table counts and size.

    Returns:
        Database statistics dictionary
    """
    client = get_client()
    return await client.get_database_stats()


@mcp.tool()
async def get_table_summary(
    table_name: str,
    group_by: Optional[str] = None,
    filters: Optional[dict[str, Any]] = None,
) -> dict[str, Any]:
    """Get aggregated statistics for any table in the database.

    Args:
        table_name: Name of the table to summarize
        group_by: Optional field to group by
        filters: Optional filters to apply

    Returns:
        Summary dictionary
    """
    client = get_client()
    return await client.get_table_summary(
        table_name=table_name,
        group_by=group_by,
        filters=filters,
    )


@mcp.tool()
async def get_machine_profiles(serial_number: str) -> list[dict[str, Any]]:
    """Get all configuration profiles installed on a specific machine.

    Returns profile details including profile name, UUID, organization,
    verification state, payloads, and installation information.

    Args:
        serial_number: Machine serial number to look up profiles for

    Returns:
        List of profile dictionaries with fields:
        - profile_uuid: Unique identifier for the profile
        - profile_name: Display name of the profile
        - profile_organization: Organization that created the profile
        - profile_verification_state: Verification status (e.g., 'verified')
        - profile_method: Installation method (e.g., 'Native')
        - profile_install_date: Unix timestamp of installation
        - profile_removal_allowed: Whether profile can be removed
        - profile_description: Description of the profile
        - payload_name: Name of the payload
        - payload_display: Display name of the payload
        - user: User scope ('System Level' or username)
    """
    client = get_client()
    return await client.get_machine_profiles(serial_number)


@mcp.tool()
async def get_filevault_status(serial_number: str) -> dict[str, Any] | None:
    """Get FileVault encryption status for a specific machine.

    Returns encryption state, recovery key status, and conversion progress.

    Args:
        serial_number: Machine serial number to look up FileVault status for

    Returns:
        FileVault status dictionary with fields:
        - filevault_status: Current status (e.g., 'On', 'Off')
        - has_personal_recovery_key: Whether a personal recovery key exists
        - has_institutional_recovery_key: Whether an institutional key exists
        - conversion_state: Encryption conversion state
        - conversion_percent: Percentage of encryption complete
        - filevault_users: Users enabled for FileVault
        - bootstraptoken_escrowed: Whether bootstrap token is escrowed
        Returns None if not found.
    """
    client = get_client()
    return await client.get_filevault_status(serial_number)


@mcp.tool()
async def get_firewall_status(serial_number: str) -> dict[str, Any] | None:
    """Get firewall status for a specific machine.

    Returns firewall state, stealth mode, and application rules.

    Args:
        serial_number: Machine serial number to look up firewall status for

    Returns:
        Firewall status dictionary with fields:
        - globalstate: Firewall state (0=off, 1=on, 2=essential)
        - stealthenabled: Whether stealth mode is enabled
        - loggingenabled: Whether logging is enabled
        - allowsignedenabled: Allow signed apps automatically
        - firewallunload: Whether firewall is unloaded
        - applications: List of application-specific rules
        - services: List of service rules
        Returns None if not found.
    """
    client = get_client()
    return await client.get_firewall_status(serial_number)


@mcp.tool()
async def get_icloud_status(serial_number: str) -> dict[str, Any] | None:
    """Get iCloud account and services status for a specific machine.

    Returns iCloud login state and enabled services.

    Args:
        serial_number: Machine serial number to look up iCloud status for

    Returns:
        iCloud status dictionary with fields:
        - logged_in: Whether an iCloud account is logged in
        - display_name: iCloud account display name
        - account_id: iCloud account ID
        - find_my_mac_enabled: Whether Find My Mac is enabled
        - clouddesktop_desktop_enabled: Desktop sync enabled
        - clouddesktop_documents_enabled: Documents sync enabled
        - keychain_sync_enabled: Keychain sync enabled
        - photo_stream_enabled: Photo stream enabled
        - is_managed_apple_id: Whether using managed Apple ID
        Returns None if not found.
    """
    client = get_client()
    return await client.get_icloud_status(serial_number)


@mcp.tool()
async def get_local_admins(serial_number: str) -> dict[str, Any] | None:
    """Get local administrator users for a specific machine.

    Returns list of users with admin privileges.

    Args:
        serial_number: Machine serial number to look up local admins for

    Returns:
        Local admins dictionary with fields:
        - users: Comma-separated list of admin usernames
        - user_count: Number of local admin users
        Returns None if not found.
    """
    client = get_client()
    return await client.get_local_admins(serial_number)


@mcp.tool()
async def get_defender_status(serial_number: str) -> dict[str, Any] | None:
    """Get Microsoft Defender antivirus status for a specific machine.

    Returns Defender health, protection state, and definitions info.

    Args:
        serial_number: Machine serial number to look up Defender status for

    Returns:
        Defender status dictionary with fields:
        - healthy: Overall health status
        - licensed: Whether properly licensed
        - real_time_protection_enabled: Real-time protection state
        - real_time_protection_available: Whether RTP is available
        - cloud_enabled: Cloud protection enabled
        - definitions_version: Virus definitions version
        - definitions_updated: Last definitions update timestamp
        - app_version: Defender app version
        - engine_version: Scan engine version
        - org_id: Organization ID
        Returns None if not found.
    """
    client = get_client()
    return await client.get_defender_status(serial_number)


@mcp.tool()
async def get_storage_report(serial_number: str) -> list[dict[str, Any]]:
    """Get storage/disk report for a specific machine.

    Returns information about all disks including capacity, usage, and health.

    Args:
        serial_number: Machine serial number to look up storage for

    Returns:
        List of disk dictionaries with fields:
        - volumename: Name of the volume
        - mountpoint: Mount point path
        - totalsize: Total size in bytes
        - freespace: Free space in bytes
        - percentage: Percentage used
        - volumetype: Type of volume (e.g., 'APFS')
        - media_type: Media type (e.g., 'SSD')
        - encrypted: Whether volume is encrypted
        - smartstatus: SMART health status
        - internal: Whether disk is internal
        - busprotocol: Bus protocol (e.g., 'PCI-Express')
    """
    client = get_client()
    return await client.get_storage_report(serial_number)


@mcp.tool()
async def get_ce_plus_compliance(
    manifest: str,
    include_passing: bool = False,
) -> dict[str, Any]:
    """Get Cyber Essentials Plus compliance report for a fleet scoped by manifest name.

    Runs 8 compliance checks against all machines matching the manifest:
    FileVault encryption, firewall, OS supported, OS patched, gatekeeper,
    SIP, auto-update, and admin account hygiene (including stale detection).

    Args:
        manifest: MunkiReport manifest name to scope the report (e.g. "Pablo").
                  Filters machines by manifest, not hostname prefix.
        include_passing: If True, include machines that pass all checks.
                        Defaults to False (only show failures).

    Returns:
        Dictionary with:
        - success: bool
        - manifest: manifest name used
        - summary: {total_machines, compliant, non_compliant, compliance_rate,
                    checks (per-check pass/fail counts), stale_machines}
        - machines: list of per-machine results with check details
    """
    client = get_client()
    return await client.get_ce_plus_compliance(manifest, include_passing)
