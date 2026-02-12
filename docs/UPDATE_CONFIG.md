# Update Claude Desktop Config

## What I Did

✅ Backed up your existing config to:
`~/Library/Application Support/Claude/claude_desktop_config.json.backup-YYYYMMDD-HHMMSS`

✅ Added the new `munkireport-api` server to your config

## What You Need to Do

**Edit the config file and replace the placeholders:**

```bash
nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
```

**Find this section:**
```json
"munkireport-api": {
  "command": "uv",
  "args": [
    "--directory",
    "/Users/admin/Documents/GitHub_James/mcp-munkireport-api",
    "run",
    "mcp-munkireport-api",
    "https://YOUR-DOMAIN-HERE.com",
    "YOUR-API-KEY-HERE"
  ]
}
```

**Replace with your actual values:**
```json
"munkireport-api": {
  "command": "uv",
  "args": [
    "--directory",
    "/Users/admin/Documents/GitHub_James/mcp-munkireport-api",
    "run",
    "mcp-munkireport-api",
    "https://your-actual-domain.com",
    "your-actual-api-key"
  ]
}
```

## Example with Real Values

If your reverse proxy setup is:
- URL: `https://munkireport-api.supportplan.com`
- API Key: `sk_live_abc123xyz789...`

Then it would look like:
```json
"munkireport-api": {
  "command": "uv",
  "args": [
    "--directory",
    "/Users/admin/Documents/GitHub_James/mcp-munkireport-api",
    "run",
    "mcp-munkireport-api",
    "https://munkireport-api.supportplan.com",
    "sk_live_abc123xyz789..."
  ]
}
```

## After Updating

1. **Save the file** (Ctrl+X, then Y, then Enter in nano)

2. **Restart Claude Desktop:**
   - Cmd+Q to quit
   - Reopen from Applications

3. **Verify it's working:**
   - Look for the 🔌 icon in Claude
   - Should see "munkireport-api" listed
   - Should show 8 available tools

4. **Test with a query:**
   ```
   How many machines are in the MunkiReport database?
   ```

## If It Doesn't Work

**Check the logs:**
```bash
tail -f ~/Library/Logs/Claude/mcp-*.log
```

**Test manually:**
```bash
# Test the API directly
curl https://your-domain.com/api/v1/health

# Test with authentication
curl -H "X-API-Key: your-key" \
  https://your-domain.com/api/v1/tools/get_database_stats

# Test the MCP client
uv --directory /Users/admin/Documents/GitHub_James/mcp-munkireport-api \
  run mcp-munkireport-api https://your-domain.com your-key
```

## Current Config Status

- ✅ Config file updated with placeholder values
- ⏳ Waiting for you to add real URL and API key
- ⏳ Waiting for restart of Claude Desktop
- ⏳ Ready to test

## Notes

- The placeholder values `YOUR-DOMAIN-HERE.com` and `YOUR-API-KEY-HERE` won't work
- Make sure your Flask API is accessible at the URL you provide
- Make sure the API key matches what's in the Flask server's `.env` file
- The URL should include `https://` (not `http://` for production)
