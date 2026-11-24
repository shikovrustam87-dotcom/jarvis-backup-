---
name: jarvis-plugin
description: Визуал Чат плагин Джарвиса
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [jarvis, desktop-plugin]
---

# Jarvis desktop UI plugin

The Jarvis HUD needs a sidebar toggle in Hermes: two rows Визуал and Чат.
Implemented as a desktop UI plugin (JS half) + dashboard API (Python half).

## Required structure

plugins/jarvis-switch/
├── dashboard/
│   ├── manifest.json
│   └── plugin_api.py
└── desktop/
    └── plugin.js

NEVER include plugin.yaml — it breaks the Python loader.