---
name: windows-window-switching
description: 'Switch Windows windows by hotkey. Use for desktop toggles.'
version: 1.0.0
author: hermes
license: MIT
metadata:
  hermes:
    tags: [windows, hotkey, window-switching, desktop, powershell]
    related_skills: []
---

# Windows Window Switching via PowerShell .ps1

## When to use

- Building a hotkey-driven window switcher on Windows 11 (F9/F10/etc.).
- Managing windows from a background Python process that lacks foreground rights.
- Need to maximize one window and minimize another reliably.

## Core approach

1. **Use `.ps1` files, not `.bat` files.** PowerShell here-strings (`@'...'@`) break when wrapped in `.bat` with `^` line continuations. A `.ps1` file keeps the here-string intact.

2. **Launch via `subprocess.Popen` with `CREATE_NEW_CONSOLE`** (flag `0x00000010`). This gives the PowerShell process its own console, bypassing the `SetForegroundWindow` restriction.

3. **PowerShell script pattern** (Add-Type with user32.dll):
   ```powershell
   Add-Type @"
   using System; using System.Runtime.InteropServices;
   public class Win {
       [DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr a, int x, int y, int cx, int cy, uint f);
       [DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);
       [DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
   }
   "@
   $SWP = 0x40
   Add-Type -AssemblyName System.Windows.Forms
   $b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
   $proc = Get-Process <name> | Where-Object { $_.MainWindowTitle -eq '<title>' } | Select-Object -First 1
   if ($proc) {
       [Win]::ShowWindow($proc.MainWindowHandle, 1) | Out-Null
       [Win]::SetWindowPos($proc.MainWindowHandle, [IntPtr]::Zero, 0, 0, $b.Width, $b.Height, $SWP) | Out-Null
       [Win]::SetForegroundWindow($proc.MainWindowHandle) | Out-Null
   }
   $other = Get-Process <other> | Where-Object { $_.MainWindowTitle -eq '<title>' } | Select-Object -First 1
   if ($other) { [Win]::ShowWindow($other.MainWindowHandle, 6) | Out-Null }
   Start-Sleep -Seconds 2
   ```

4. **Python listener pattern** (polling with 50 ms debounce):
   ```python
   import ctypes, subprocess, time, os
   VK_F9 = 0x78
   CREATE_NEW_CONSOLE = 0x00000010
   DIR = r"C:\path\to\scripts"
   PS_VISUAL = os.path.join(DIR, "visual.ps1")
   PS_CHAT = os.path.join(DIR, "chat.ps1")

   def run_ps(path):
       subprocess.Popen(
           ["powershell.exe", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", path],
           cwd=DIR, creationflags=CREATE_NEW_CONSOLE, close_fds=True,
       )

   f9 = f10 = False
   while True:
       if ctypes.windll.user32.GetAsyncKeyState(VK_F9) & 0x8000:
           if not f9:
               f9 = True
               run_ps(PS_VISUAL)
       else:
           f9 = False
       time.sleep(0.05)
   ```

## Pitfalls

- **`.bat` + here-strings = broken.** PowerShell here-strings collapse onto one line when joined by `^` in a `.bat`. Always use a `.ps1` file with `-File`.
- **`.ps1` files with Cyrillic must have UTF-8 BOM.** Without BOM, PowerShell reads the file as ANSI (Windows-1251) and mangles Cyrillic characters in `Where-Object` filters (e.g., `$_ .MainWindowTitle -eq 'Джарвис'` fails silently). Add BOM: `open(path, 'wb').write(b'\xef\xbb\xbf' + content.encode('utf-8'))` or save with UTF-8 BOM in editor.
- **`Start-Process` with Cyrillic paths: use `-FilePath` explicitly.** When the path contains non-ASCII characters, the positional `Start-Process "path"` binding can fail with `PositionalParameterNotFound`. Always use `Start-Process -FilePath "path" -ArgumentList ...` to avoid encoding-related parameter binding errors.
- **Background Python can't call `SetForegroundWindow` directly.** Even with `AllowSetForegroundWindow` and `AttachThreadInput`, it's unreliable. Delegating to a separate PowerShell process (CREATE_NEW_CONSOLE) works.
- **`Get-Process` by name may return multiple processes.** Filter by `MainWindowTitle`. Use `Select-Object -First 1`.
- **Filter by process name AND title, not title alone.** Multiple apps can share a title (e.g., Hermes window is titled `Hermes`, jarvis_app.py is titled `Джарвис` but runs as `python`). Always combine: `Get-Process <name> | Where-Object { $_.MainWindowHandle -ne 0 -and $_.MainWindowTitle -eq '<title>' }`.
- **The Hermes desktop app process is named `Hermes`** (window title also `Hermes`), not `python`. jarvis_app.py runs as `python` (title `Джарвис`). Use the correct process name for each target.
- **Minimizing a pywebview/Electron window:** `ShowWindow(hwnd, 6)` (SW_MINIMIZE) works for most. If not, try `ShowWindow(hwnd, 0)` (SW_HIDE).
- **The `Start-Sleep` at the end** of the .ps1 keeps the window open long enough for `SetForegroundWindow` to take effect.

## User preferences

- Hotkeys: F9 = visual (HUD), F10 = chat (Hermes). Both switch windows; they are NOT toggles.
- The listener runs as a background process.
- No lags: debounce 50 ms is sufficient.

## Related files

- `C:/Users/Пользователь/Desktop/Для Джарвиса/jarvis_switch.py` — the listener.
- `C:/Users/Пользователь/Desktop/Для Джарвиса/1_ВИЗУАЛ.ps1` — show visual.
- `C:/Users/Пользователь/Desktop/Для Джарвиса/2_ЧАТ.ps1` — show chat.
