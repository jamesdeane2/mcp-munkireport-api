# MCP MunkiReport API Client

MCP server that wraps the Flask MunkiReport API for use with Claude Desktop.

## Overview

This is a lightweight MCP client that forwards requests to your Flask MunkiReport API. It provides the same functionality as the direct database MCP server, but works over HTTP instead of direct SQLite access.

## Architecture

```
Claude Desktop
    ↓
MCP Client (this project)
    ↓ HTTP
Flask API (flask-munkireport)
    ↓ SQLite
MunkiReport Database
```

## Installation

```bash
cd /Users/admin/Documents/GitHub_James/mcp-munkireport-api
uv pip install -e .
```

## Usage

### Claude Desktop Configuration

Add to `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "munkireport-api": {
      "command": "uv",
      "args": [
        "--directory",
        "/Users/admin/Documents/GitHub_James/mcp-munkireport-api",
        "run",
        "mcp-munkireport-api",
        "http://10.254.6.14:5030",
        "Support1"
      ]
    }
  }
}
```

**Arguments:**
1. API URL (your Flask server)
2. API key (from Flask server's `.env`)

### Testing

Test the client without Claude:

```bash
# Install dependencies first
uv pip install -e .

# Run test script
python tests/test_client.py http://10.254.6.14:5030 Support1
```

## Available Tools

The MCP server exposes 8 tools that map directly to Flask API endpoints:

1. **query_machines** - Query machines with filters
2. **get_machine_details** - Get complete machine information
3. **get_mdm_enrollment_summary** - MDM enrollment statistics
4. **get_events** - Query events with filters
5. **get_error_summary** - Error/warning summary by machine
6. **get_recent_critical_events** - Recent critical events
7. **get_database_stats** - Database statistics
8. **get_table_summary** - Table aggregations

## Example Queries

Once connected in Claude:

- "Show me all machines not enrolled in MDM"
- "What critical errors occurred in the last 24 hours?"
- "Give me details about machine serial number FVFFV3JBQ05N"
- "How many machines are enrolled in MDM?"

## Advantages Over Direct Database Access

**Over VPN/Mount/Copy:**
- ✅ No need to copy database
- ✅ Query live data
- ✅ Works from anywhere
- ✅ No server downtime

**Over SSH Tunnel MCP:**
- ✅ More stable connection
- ✅ Can use from multiple clients
- ✅ Better error handling
- ✅ Request/response logging

## Project Structure

```
mcp-munkireport-api/
├── src/
│   └── mcp_munkireport_api/
│       ├── __init__.py
│       ├── __main__.py          # Entry point
│       ├── server.py            # MCP server implementation
│       └── client/
│           ├── __init__.py
│           └── api_client.py    # HTTP client for Flask API
├── tests/
│   └── test_client.py           # Test script
├── pyproject.toml               # UV/pip configuration
└── README.md
```

## Dependencies

- `mcp>=1.0.0` - Model Context Protocol
- `httpx>=0.27.0` - Modern HTTP client

## How It Works

1. Claude sends MCP tool call
2. MCP server receives request
3. HTTP client makes request to Flask API
4. Flask API queries SQLite database
5. Response flows back to Claude

**Token efficiency:** Same as Flask API (60-70% savings vs terminal)

## Development

```bash
# Install in development mode
uv pip install -e .

# Test the client
python tests/test_client.py http://10.254.6.14:5030 your-api-key

# Check Claude Desktop logs if issues
tail -f ~/Library/Logs/Claude/mcp*.log
```

## Troubleshooting

**MCP server not appearing in Claude:**
- Check Claude Desktop config JSON is valid
- Verify API URL is correct
- Ensure Flask API is running
- Check logs: `~/Library/Logs/Claude/`

**Connection errors:**
- Verify Flask API is accessible: `curl http://10.254.6.14:5030/api/v1/health`
- Check API key is correct
- Ensure you're on VPN if required

**Timeout errors:**
- Increase timeout in Claude Desktop config
- Check Flask API logs for slow queries
- Consider adding pagination

## Security Notes

- API key is passed as command-line argument (visible in process list)
- For production, consider using environment variables
- Flask API should be behind HTTPS in production
- Restrict Flask API access to known IPs

## Comparison with Direct Database MCP

| Feature | This (API Client) | Direct Database |
|---------|------------------|-----------------|
| Connection | HTTP | Direct SQLite |
| Setup | Requires Flask API | Direct to DB |
| Remote access | ✅ Easy | ❌ Complex |
| Multiple clients | ✅ Yes | ⚠️ Careful |
| Token efficiency | 60-70% | 60-70% |
| Latency | ~50-200ms | ~10-50ms |

**When to use this:** Remote access, multiple users, production stability

**When to use direct DB:** Local development, single user, lowest latency

---

**Ready to use!** Restart Claude Desktop after updating config.
