---
name: windows-software-installation
description: "Install Windows apps when package managers unavailable."
version: 1.0.0
author: Hermes
license: MIT
metadata:
  hermes:
    tags: [windows, installation, installer]
    related_skills: [windows-cleanup]
---

# Windows Software Installation

## When to Use

Use when the user asks to install a Windows desktop application and `winget`/`choco` are unavailable or unsuitable.

## Procedure

1. Check for package managers first:
   - `winget --version`
   - `choco --version`
   If one is available, prefer it.

2. Otherwise find the official download URL and download the installer into the user's Downloads folder with `curl -L`.

2a. For portable apps distributed as a zip, extract to a short ASCII path such as `C:\AppName` (not under the user profile) to avoid non-ASCII path failures, then launch the main executable from there.

3. Try a silent install using the installer's known flags:
   - Inno Setup: `/VERYSILENT /SUPPRESSMSGBOXES /NORESTART /SP-`
   - NSIS: `/S`
   Run it through `cmd //c "..."`, not by executing the `.exe` directly from MSYS bash — direct execution can fail with `Permission denied`.

4. If silent installation fails or the installer requires interaction, launch it with `cmd //c "start \"\" \"installer.exe\""` and guide the user through the GUI steps.

5. Verify installation by searching Program Files and AppData for the application executable before reporting success.

6. Report the installed location and how to launch it.

## Pitfalls

- MSYS bash may refuse to run a Windows `.exe` directly with `Permission denied`; use `cmd //c`.
- Silent flags are installer-specific; if unknown, use the interactive fallback instead of guessing.
- UAC prompts or installer GUI steps may require the user; do not assume an unattended install succeeded without verifying the executable exists.
- Leave the installer in Downloads unless the user asks to remove it.
- Installers that require UAC elevation cannot be started reliably from MSYS bash or from Python's subprocess.Popen (WinError 740); launch them via Explorer or PowerShell `Start-Process ... -Verb RunAs`, and only report success after verifying the executable exists.
- Cyrillic paths in the user profile can break `cd`/relative commands in cmd launched from MSYS; prefer absolute paths or launch from Explorer.
- Some portable apps distributed as zip fail to start when located under a profile path containing non-ASCII characters; extract or move them to a simple ASCII path such as `C:\AppName` and launch from there.
