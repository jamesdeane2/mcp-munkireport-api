"""Main entry point - supports both MCP (stdio) and HTTP (FastAPI) modes."""

import sys


def main():
    """Run the server in MCP mode (default) or HTTP mode with --http flag."""
    # Check for --http flag
    if "--http" in sys.argv:
        sys.argv.remove("--http")
        run_http()
    else:
        run_mcp()


def run_mcp():
    """Run as MCP server over stdio for Claude Desktop."""
    from .config import settings
    from .mcp_server import mcp

    # Allow overriding settings via CLI args for convenience
    if len(sys.argv) >= 3:
        settings.api_url = sys.argv[1]
        settings.api_key = sys.argv[2]

    if not settings.api_key:
        print(
            "Usage: mcp-munkireport-api <api_url> <api_key>",
            file=sys.stderr,
        )
        print(
            "   Or: Set MUNKIREPORT_API_URL and MUNKIREPORT_API_KEY environment variables",
            file=sys.stderr,
        )
        print(
            "Example: mcp-munkireport-api https://mra.example.com API_KEY",
            file=sys.stderr,
        )
        print(
            "\nFor HTTP mode: mcp-munkireport-api --http <api_url> <api_key>",
            file=sys.stderr,
        )
        sys.exit(1)

    # Run MCP server over stdio
    mcp.run()


def run_http():
    """Run as HTTP server using FastAPI/uvicorn."""
    import uvicorn
    from .config import settings

    # Allow overriding settings via CLI args for convenience
    if len(sys.argv) >= 3:
        settings.api_url = sys.argv[1]
        settings.api_key = sys.argv[2]

    if not settings.api_key:
        print(
            "Usage: mcp-munkireport-api --http <api_url> <api_key>",
            file=sys.stderr,
        )
        print(
            "   Or: Set MUNKIREPORT_API_URL and MUNKIREPORT_API_KEY environment variables",
            file=sys.stderr,
        )
        print(
            "Example: mcp-munkireport-api --http https://mra.example.com API_KEY",
            file=sys.stderr,
        )
        sys.exit(1)

    uvicorn.run(
        "mcp_munkireport_api.server:app",
        host=settings.host,
        port=settings.port,
        reload=settings.reload,
    )


if __name__ == "__main__":
    main()
