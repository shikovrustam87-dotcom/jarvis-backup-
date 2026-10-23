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

## Hotkey switcher (jarvis_switch.py)

Companion script for toggling between visual (HUD) and chat (Hermes) windows via F9/F10.
Lives in `C:\Users\Пользователь\Desktop\Для Джарвиса\` alongside `1_ВИЗУАЛ.bat` and `2_ЧАТ.bat`.

### Key technique: window switching from a background process

`SetForegroundWindow` does NOT work from a background Python process (Windows restricts foreground to the active process). Two approaches:

1. **WinAPI with AttachThreadInput** — attach to the foreground thread, call AllowSetForegroundWindow(ASFW_ANY), then SetForegroundWindow. May still fail on some window types.
2. **Delegate to .bat files via CREATE_NEW_CONSOLE** (recommended) — launch `cmd.exe /c <bat>` with `creationflags=CREATE_NEW_CONSOLE`. The new console process gets foreground rights and runs PowerShell with user32.dll P/Invoke. This is the reliable method.

### .bat file pattern

Each .bat runs PowerShell with a here-string defining user32.dll imports (SetWindowPos, ShowWindow, SetForegroundWindow), then:
- Find target window by process name + MainWindowTitle
- ShowWindow(handle, SW_SHOWNORMAL=1) → SetWindowPos to screen bounds → SetForegroundWindow
- Minimize the other window (ShowWindow, 6)

### Gotchas
- .bat files must look for the correct process: jarvis_app.py runs as `python` with MainWindowTitle `Джарвис` (not `browser`).
- When filtering windows in PowerShell, always combine process name AND MainWindowTitle (e.g., `Get-Process python | Where-Object { $_.MainWindowHandle -ne 0 -and $_.MainWindowTitle -eq 'Джарвис' }`), not just MainWindowTitle. Multiple processes (Hermes, jarvis_app.py, browser) can share similar or identical titles, and a bare title match picks the wrong window or none at all.
- The Hermes desktop app process is named `Hermes` (not `python`); its window title is also `Hermes`. Look it up by process name `hermes`, not by title substring.
- PowerShell here-strings break when run via `subprocess.run(shell=True)` with CRLF; use `cmd.exe /c` with CREATE_NEW_CONSOLE instead.
- Add `time.sleep()` after launching .bat to let PowerShell complete before next key press.
- Poll keys with `GetAsyncKeyState` + 50ms debounce (time.sleep(0.05)).