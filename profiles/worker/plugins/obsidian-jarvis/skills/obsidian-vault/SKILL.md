---
name: obsidian-vault
description: "Work with the JarvisVault Obsidian knowledge base: read, search, create and edit notes. Use when the user asks about their notes, knowledge base, or wants to save information to Obsidian."
---

# Obsidian Vault — JarvisVault

## Vault Location
`C:\Users\Пользователь\Documents\JarvisVault`

## Structure
- `raw/` — source documents (append-only, never edit)
- `wiki/` — knowledge pages (short, Russian, with [[links]])
- `daily/` — daily notes (YYYY-MM-DD.md)
- `inbox/` — user's thoughts and ideas
- `index.md` — table of contents
- `log.md` — journal of changes
- `ПРАВИЛА.md` — full rules for vault maintenance

## Rules
1. Before any work with the vault, read `ПРАВИЛА.md` first
2. `raw/` is append-only — never modify or delete
3. `wiki/` pages should be concise, in Russian, with [[backlinks]]
4. Always update `index.md` when adding new wiki pages
5. Log all changes in `log.md`
6. Daily notes go in `daily/YYYY-MM-DD.md`

## Common Operations
- **Search notes**: use search_files on the vault directory
- **Read note**: use read_file with the note path
- **Create note**: use write_file to create new notes in appropriate folders
- **Edit note**: use patch to make targeted edits
- **List notes**: use search_files with target="files" and glob pattern "*.md"

## Naming Conventions
- Wiki pages: descriptive Russian names, e.g., "Родословная Шиковых.md"
- Daily notes: "YYYY-MM-DD.md" format
- Inbox notes: short descriptive names
