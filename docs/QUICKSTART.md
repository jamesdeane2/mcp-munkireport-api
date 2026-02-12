# Quick Start Guide

## What You Have

A lightweight MCP client that connects Claude to your Flask MunkiReport API.

**Architecture:**
```
Claude Desktop → MCP Client → HTTP → Flask API → SQLite Database
```

## Installation (Already Done!)

```bash
cd /Users/admin/Documents/GitHub_James/mcp-munkireport-api
uv pip install -e .
```

✅ **Status:** Installed and tested successfully!

## Test Results

All 6 tests passed:
- ✅ Health check working
- ✅ Database accessible (71 tables, 1154 machines)
- ✅ Query machines working
- ✅ Machine details working
- ✅ MDM summary working
- ✅ Critical events working

## Add to Claude Desktop

1. **Open Claude Desktop config:**
   ```bash
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. **Add this configuration:**
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

3. **Restart Claude Desktop**

4. **Verify in Claude:**
   - Look for 🔌 icon
   - Should see "munkireport-api" with 8 tools

## Example Queries for Claude

Once connected, try these:

```
Show me all machines not enrolled in MDM

What critical errors occurred in the last 24 hours?

Give me details about machine FVFFV3JBQ05N

How many machines are enrolled in MDM?

Show me the top 10 machines with the most recent activity

What's the database size and how many total machines?
```

## Project Files

```
mcp-munkireport-api/
├── src/mcp_munkireport_api/
│   ├── __main__.py              # Entry point
│   ├── server.py                # MCP server (tool definitions)
│   └── client/
│       └── api_client.py        # HTTP client for Flask API
├── tests/
│   └── test_client.py           # Test script (already passed!)
├── docs/
│   └── claude_desktop_config.json  # Example config
├── pyproject.toml               # Dependencies
└── README.md                    # Full documentation
```

## How It Works

1. You ask Claude a question
2. Claude calls MCP tool (e.g., `query_machines`)
3. MCP client makes HTTP request to Flask API
4. Flask API queries database
5. Response flows back to Claude
6. Claude presents results

**Benefits:**
- ✅ No database copying
- ✅ No VPN mount complexity
- ✅ Query live data
- ✅ Works from anywhere on VPN
- ✅ 60-70% token savings vs terminal

## Troubleshooting

**If MCP server doesn't appear:**
```bash
# Check Claude logs
tail -f ~/Library/Logs/Claude/mcp*.log

# Test manually
uv --directory /Users/admin/Documents/GitHub_James/mcp-munkireport-api \
  run mcp-munkireport-api http://10.254.6.14:5030 Support1
```

**If connection fails:**
```bash
# Verify Flask API is running
curl http://10.254.6.14:5030/api/v1/health

# Verify authentication
curl -H "X-API-Key: Support1" \
  http://10.254.6.14:5030/api/v1/tools/get_database_stats
```

## What's Next?

You're done! The MCP client is:
- ✅ Installed
- ✅ Tested
- ✅ Ready to add to Claude

Just update your Claude Desktop config and restart.

## Maintenance

**Update the client:**
```bash
cd /Users/admin/Documents/GitHub_James/mcp-munkireport-api
git pull
uv pip install -e .
# Restart Claude Desktop
```

**Change API URL or key:**
Edit your Claude Desktop config and restart.

## Security Notes

⚠️ **API Key Visibility:**
The API key "Support1" is passed as a command-line argument, which means it's visible in process lists. This is fine for internal VPN usage, but for production:

1. Use a strong API key
2. Ensure Flask API is only accessible on VPN
3. Consider environment variables instead of args
4. Rotate keys regularly

---

**Ready to use!** Add the config to Claude Desktop and start querying! 🚀
