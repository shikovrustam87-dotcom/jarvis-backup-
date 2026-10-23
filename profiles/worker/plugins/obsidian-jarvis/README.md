# Obsidian Jarvis Plugin

Portable plugin for integrating Obsidian (JarvisVault) with Hermes Agent.

## Features
- Filesystem MCP server for reading/writing notes in JarvisVault
- Skill for knowledge base management rules

## Vault Structure
- `raw/` — source documents (append-only)
- `wiki/` — knowledge pages
- `daily/` — daily notes
- `inbox/` — user's thoughts
- `index.md` — table of contents
- `log.md` — journal of changes
- `ПРАВИЛА.md` — maintenance rules

## Installation
```bash
hermes plugins install obsidian-jarvis --enable
```

## Requirements
- Node.js (for npx)
- Obsidian vault at `C:/Users/Пользователь/Documents/JarvisVault`
