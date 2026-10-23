# Portable Agent Plugins (Agent Plugins v1)

Create, install, and enable portable agent plugin packages — directory-based bundles that ship MCP servers and skills together, installable via `hermes plugins install`.

## When to Use

- The user wants to package an MCP server + skills into a reusable, shareable plugin.
- You need to create a portable plugin for a specific integration (e.g., Obsidian, a custom API).
- The user asks about the Agent Plugins v1 format or portable plugin structure.

## Plugin Structure

A portable plugin is a directory with this layout:

```
my-plugin/
├── plugin.json          # manifest (Agent Plugins v1 schema)
├── mcp.json             # MCP server configuration
├── skills/
│   └── my-skill/
│       └── SKILL.md     # skill files
└── README.md            # documentation (optional)
```

## plugin.json Format

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "my-plugin",
  "version": "1.0.0",
  "description": "What this plugin does",
  "author": { "name": "Author Name" },
  "license": "MIT",
  "keywords": ["relevant", "tags"]
}
```

**Critical:** The `$schema` field is REQUIRED. Without it, Hermes reports "plugin.json declares an unsupported or missing Agent Plugins schema" and refuses to load the plugin.

**Do NOT include** `capabilities`, `mcp`, or `skills` fields in plugin.json — those are defined in separate files (mcp.json and skills/ directory).

## mcp.json Format

```json
{
  "mcpServers": {
    "server-name": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-filesystem", "/path/to/dir"],
      "env": {}
    }
  }
}
```

Supports stdio (command + args) and Streamable HTTP (url + headers) transports. Legacy `sse` entries are reported and skipped.

## Skills Directory

Skills go in `skills/<skill-name>/SKILL.md` with standard SKILL.md frontmatter. They are read-only, namespaced, and loaded through `skills_list` + `skill_view`. Namespaces have the form `agent-plugin-<slug>-<hash>`.

## Installation Workflow

### Create locally

1. Create the plugin directory under `~/.hermes/plugins/<name>/`
2. Write plugin.json, mcp.json, skills/, README.md
3. Initialize a git repo in the plugin directory (required for install)
4. Install: `hermes plugins install /path/to/plugin --enable`
   - Note: local path install may not work; alternative is to place the directory manually and enable via config

### Enable manually

If install from local path fails:
1. Place the plugin directory in `~/.hermes/plugins/<name>/`
2. Enable via: `hermes config set plugins.enabled '["existing", "new-plugin", ...]'`
   - Include ALL existing plugins in the list (the command replaces the entire list)
3. Verify: `hermes plugins list | grep <name>`

### From a Git repository

```bash
hermes plugins install owner/repo --enable
```

## MCP Server Configuration

The MCP server in mcp.json uses the same format as `mcp_servers` in config.yaml. Environment variables for the MCP subprocess go in the `env` object. Do not store secrets in mcp.json — use environment variables or the secrets system.

## Security Notes

- Portable plugins run with full trust (same as native plugins)
- `PLUGIN_ROOT` points to the resolved package root
- `PLUGIN_DATA` points to a profile-scoped writable directory
- Values in `mcp.json` `env` are visible package data, not a secret storage mechanism
- Do not place credentials in mcp.json

## Troubleshooting

### "plugin.json declares an unsupported or missing Agent Plugins schema"

The `$schema` field is missing from plugin.json. Add:
```json
"$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json"
```

### Plugin not appearing in `hermes plugins list`

- Ensure plugin.json has the correct `$schema`
- Ensure the directory is under `~/.hermes/plugins/`
- Try `hermes plugins install` from the local git repo
- Enable via `hermes config set plugins.enabled '[...]'`

### MCP server not connecting

- Verify the MCP server command works independently (e.g., `npx -y @modelcontextprotocol/server-filesystem /path`)
- Check that Node.js is installed for npx-based servers
- Increase `connect_timeout` in mcp.json if the server is slow to start

## Verification

- `hermes plugins list` shows the plugin with status `enabled`
- `hermes plugins list` shows no schema errors
- MCP tools from the plugin appear in the tool list after restart
- Skills from the plugin are discoverable via `skills_list`
