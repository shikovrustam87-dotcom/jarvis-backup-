# Window switching: hotkeys, standalone app, autostart

The visual and the chat are two separate windows on one monitor, and Rustam
toggles between them. He rejected, in order: two tiled windows, desktop
shortcuts, and an in-app sidebar plugin. What he accepted is a **background
hotkey listener** — he presses a key, one window fills the screen and the other
minimises. F9 = visual, F10 = chat.

## Interpreter rule

Run every standalone script here with the **system** Python:

```
%LOCALAPPDATA%\Programs\Python\Python311\python.exe
```

The Hermes tools interpreter is the wrong choice: its directory name comes back
from tool output partially masked (`python-3.14.7+202****0901-win32-x64`), so a
literal path copied from a listing fails with `No such file or directory` even
though the folder exists. Glob `%LOCALAPPDATA%\hermes\tools\python-*` only as a
fallback. The launcher `.bat` should prefer the system path and fall back to
the glob.

## The hotkey listener

`jarvis_switch.py` — an edge-detected poll loop (act on key-down, not while
held), ~40 ms tick, `END` to quit:

```python
import ctypes, ctypes.wintypes as wt, time
user32 = ctypes.windll.user32
VK_F9, VK_F10, VK_END = 0x78, 0x79, 0x23
SW_RESTORE, SW_MAXIMIZE, SW_MINIMIZE = 9, 3, 6

f9 = f10 = False
while True:
    if user32.GetAsyncKeyState(VK_F9) & 0x8000:
        if not f9:
            f9 = True
            show_visual()
    else:
        f9 = False
    # ... same shape for F10 -> show_chat(), and VK_END to break
    time.sleep(0.04)
```

Window lookup: enumerate top-level windows, skip invisible ones and empty
titles, and classify by title — **exactly** `Джарвис` (the pywebview app) vs.
exactly `Hermes`. Do NOT match `Джарвис` as a substring or match `Ядро`: an old
browser tab titled `Джарвис — Ядро v2` then wins the lookup and the hotkey
keeps raising the browser instead of the app.

```python
EnumProc = ctypes.WINFUNCTYPE(wt.BOOL, wt.HWND, wt.LPARAM)
user32.EnumWindows(EnumProc(cb), 0)   # cb collects handles into lists
```

Activate the wanted window and hide the other:

```python
if user32.IsIconic(win):
    user32.ShowWindow(win, SW_RESTORE)
    time.sleep(0.3)
user32.ShowWindow(win, SW_SHOWNORMAL)
time.sleep(0.1)
user32.ShowWindow(win, SW_MAXIMIZE)
time.sleep(0.1)
user32.SetForegroundWindow(win)
user32.BringWindowToTop(win)
time.sleep(0.2)
if other:
    user32.ShowWindow(other, SW_MINIMIZE)
```

**Pitfall — `ShowWindow(SW_MAXIMIZE)` alone is unreliable for minimised windows.** A window that was minimised to the taskbar often ignores a bare `ShowWindow(SW_MAXIMIZE)`: the call returns success but nothing visibly changes (the user reports \"F10 ничего не делает на чистом экране\"). The robust sequence is restore → normal → maximise → foreground, with a short `time.sleep` between each step (0.1–0.3 s). `SetForegroundWindow` also silently fails when the calling process is not the foreground process — the sleep + `BringWindowToTop` combination helps, but do not promise instant focus.

**Pitfall — the `.bat` files (PowerShell here-strings) break when invoked programmatically.** Running `2_ЧАТ.bat` via `subprocess.run([bat], shell=True)` or `cmd /c` produces `UnexpectedCharactersAfterHereStringHeader` — the here-string header `@'` is mis-parsed. Prefer **direct WinAPI** (`ctypes` + `user32`) in the listener; the `.bat` files are for double-click use by the user, not for the listener to call.

**Toggle behaviour.** Both keys flip between the two modes, not \"show X\". Track a `visual_on` boolean (initialised by checking whether the Jarvis window is currently maximised). On F9 or F10 press: if `visual_on` → `show_chat()`, `visual_on = False`; else → `show_visual()`, `visual_on = True`. This makes each key work on a clean screen (nothing maximised): the first press shows the corresponding mode instead of being a no-op.

## Launching the app from the hotkey

F9 must bring up the visual even when it is not running. Launch the app, not
the HTML — opening the `.html` hands the job to the browser, which he rejected
("у нас визуал открывается в браузере почему-то"). Give the app time to
appear (a 7–9 s sleep) before re-scanning for its window.

```python
flags = subprocess.CREATE_NO_WINDOW | subprocess.DETACHED_PROCESS
subprocess.Popen([PYTHON, JARVIS_APP], cwd=JARVIS_DIR,
                 creationflags=flags, close_fds=True)
time.sleep(9)
```

## The standalone app (no browser chrome)

`pip install pywebview`, then a window whose only content is the HUD:

```python
import webview
webview.create_window(title="Джарвис", url=HTML, fullscreen=True,
                      background_color="#01030a",   # no white flash on open
                      text_select=False)
webview.start(debug=False, private_mode=False)
```

`background_color` matching the HUD's `#01030a` matters — the default flashes
white before the page paints. Close with Esc or Alt+F4. Verify it opened by
checking for a process whose `MainWindowTitle` is exactly `Джарвис`.

## Autostart

The listener must survive a reboot. Drop a shortcut to the launcher `.bat` in
the user's Startup folder:

```powershell
$sh = New-Object -ComObject WScript.Shell
$startup = [Environment]::GetFolderPath('Startup')
$lnk = $sh.CreateShortcut((Join-Path $startup 'Джарвис — переключатель.lnk'))
$lnk.TargetPath = '<...>\ЗАПУСК_ПЕРЕКЛЮЧАТЕЛЯ.bat'
$lnk.WorkingDirectory = '<...>\Для Джарвиса'
$lnk.WindowStyle = 7      # minimised, no console flash
$lnk.Save()
```

## Verifying it is actually running

A launch that failed leaves no process but may leave a stale PID you misread.
Confirm by matching the command line, not by process count:

```powershell
Get-CimInstance Win32_Process -Filter "Name='python.exe'" |
  Where-Object { $_.CommandLine -like '*jarvis_switch*' } |
  Select-Object ProcessId
```

Start it with `terminal(..., background=true)`; a foreground `&`/`nohup` is
refused by the tool, and `Start-Process` inside a one-liner repeatedly failed to
leave the process alive.

## What did NOT work

Do not re-try these — they were tried and rejected or never activated:

- **Desktop shortcuts** to the `.bat` files: he asked for the toggle to live in
  the app, not on the Desktop.
- **In-app sidebar plugin** (rows «Визуал»/«Чат»): built, enabled in
  `config.yaml`, files placed correctly, and still never rendered. Do not
  present it to him as a working path.
