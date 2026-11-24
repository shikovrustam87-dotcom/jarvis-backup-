---
name: jarvis-hud
description: "Build/extend the Jarvis-style fullscreen HUD page."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [jarvis, hud, html, ui, orb, dashboard, fullscreen, system-stats]
    related_skills: [claude-design, video-download-edit]
---

# Jarvis-style HUD interface

Rustam's ongoing project: a fullscreen Iron-Man/Jarvis interface — a glowing
orb that reacts to voice, flanked by corner panels (prayer times, system stats,
wallet). Built as a local HTML file opened in a browser. He iterates on it by
voice across many sessions, so treat it as a living artifact, not a one-off.

## When to Use

Any request to build, extend, or restyle the Jarvis HUD: "сделай шар больше",
"поменяй цвет", "добавь панель", "как в видео", fullscreen scaling, prayer
times, a system-monitor panel, a wallet/token panel.

## Project layout

All under `C:\Users\Пользователь\Desktop\Для Джарвиса\`:

- `jarvis_core_v2.html` — the main HUD. Iterate by writing a NEW versioned
  filename (`_v2`, `_v3`) rather than fighting the overwrite guard (see
  Pitfalls); it doubles as an A/B compare.
- `logo_mif.png` — the cropped «М&Ф» monogram the orb displays (see
  `references/logo-from-photo.md`).
- `mif_boot.html` — boot splash (galaxy + planets, "МиФ").
- `jarvis_app.py` — the HUD as a STANDALONE APP window (pywebview), no browser
  chrome. This is what he wants to see, not a browser tab.
- `jarvis_switch.py` — background hotkey listener: F9 = visual, F10 = chat,
  END = quit. The primary mode toggle.
- `ЗАПУСК_ПЕРЕКЛЮЧАТЕЛЯ.bat` — double-click launcher for `jarvis_switch.py`;
  a shortcut to it sits in the Startup folder so the keys work after reboot.
- `обновлять_в_файле.bat` — background refresher that writes real stats INTO
  the HTML (see `references/system-stats-source.md`).
- `1_ВИЗУАЛ.bat` / `2_ЧАТ.bat` — the underlying maximise-one / minimise-other
  actions the hotkeys invoke (see "Launching & window layout").
- `снимок_экрана.bat`, `разобрать_видео.bat` — helpers; the video one is
  covered by the `video-download-edit` skill.
- `stt_guard.py` + `ЗАПУСК_СТОРОЖА.bat` — unrelated to the HUD itself but living in
  this folder: the speech-recognition watchdog that flips `stt.provider` between
  Groq and local whisper on connectivity. Covered by the `hermes-agent` skill's
  voice/STT reference.

## Design conventions (this user's taste)

- **Palette**: near-black navy background `#01030a`, deep-navy orb core
  (`#3d7fe0` → `#1e4fa8` → `#010812`), cyan accents `#4fd8ff`, gold `#e8c85a`
  reserved for the single "current" highlight. Dark, deep, low-glow. He asked
  for "более тёмные тона, выраженные тёмно-синие", then later to brighten the
  orb while keeping it navy — so: a **rich navy gradient, brighter centre but
  never a white or pale-blue hotspot**. The one hard rule is no white core.
- **The orb must be BIG** — nearly filling its ring, not a small ball with air
  around it. When in doubt, scale up.
- **Corner panels use `position: fixed`** (anchored to the viewport), NOT
  `position: absolute` inside the centred `.stage` — otherwise they drift
  toward centre and touch the orb. He wanted them "в самом углу, чтобы не
  касался шара".
- **The orb is VOICE-DRIVEN, not timer-driven.** Its size comes straight from
  live mic loudness in JS (`getUserMedia` + `AnalyserNode` →
  `core.style.transform = scale(...)`), with fast-attack / slow-release
  smoothing so it breathes in the rhythm of speech. **Delete every CSS
  `animation` on `.core` first** — a keyframe animation overwrites the inline
  transform each frame, so the orb ignores the voice and just emits a fixed
  pulse (he reported exactly this: "просто волны пускает", not reacting to
  speech). Full recipe: `references/voice-reactive-orb.md`.
- **Direction encodes who is talking**: Rustam's voice → orb expands OUTWARD;
  Jarvis's voice → contracts INWARD. He asked for this distinction explicitly —
  keep both.
- **Surface an on-screen state badge for any invisible input.** A mic/audio
  effect can look like it works while silently failing. Render a small
  corner badge that shows the real state (`МИК ЕСТЬ` / `ОТКАЗ: <name>` / `НЕТ
  API`); it converts "доверься мне" into something he can see, and it is how
  you tell a dead `getUserMedia` from a quiet one.
- **Fullscreen scales the scene**: `:fullscreen .stage { width:min(150vmin,1600px) }`
  so the orb grows to fill the monitor instead of looking small. Keep a
  fullscreen toggle button (bottom-centre, fades to near-invisible when active).
- **The right panel is a stack of bordered cards** (label + value + bar fill),
  mirroring the reference reel — not a bare equalizer of columns.
- **Background: starfield, not flat.** Two layered `.stars` divs of tiny
  `radial-gradient` dots with offset `twinkle` animation. He wanted the stars
  clearly visible — sizes around 5–7px, not the near-invisible 1px default.
- **Cyrillic-safe "medieval" font**: `OLDENGL.TTF` (Old English Text MT) has NO
  Cyrillic — it draws Russian letters as dotted garbage. On this machine
  `Palatino Linotype` is the most period-looking serif that DOES support
  Russian (also fine: Bookman Old Style, Constantia). Always probe a font
  renders Cyrillic (`PrivateFontCollection` + `DrawString`) before promising it.
- **Central label — it is now a cropped LOGO, not typed text.** The orb carries
  the «М&Ф» monogram with a crown above it, lifted from his product label
  photo. Recipe: crop the logo region, knock the light/parchment background out
  to transparent with PIL, then place it in the SVG as an `<image href>` — do
  not retype it in a font. Full recipe: `references/logo-from-photo.md`.
  (Earlier the orb carried typed «МиФ» — capital «М»/«Ф», small «и» — in the
  serif font above; he later replaced it with the real logo.)
- **Waves are small jagged pulse-lines, never a big expanding ring.** He
  rejected both the plain expanding circles and a large white ring as "белый
  круг" — the wanted effect is a small, dark, cardiogram-like zigzag hugging the
  orb, plus short spikes around it. Keep amplitude low (a few px) and colour it
  in the orb's own dark navy; a bright/white wave reads as wrong.

## Launching & window layout

He wants the two modes **SWITCHED, not tiled**. First he asked for two windows
side by side, then rejected that outright: *"мне так не нужно. Мне нужно именно
с переключением"* — when he wants the visual, the screen shows ONLY the visual;
when he wants chat, ONLY the chat.

**Current shape: a background hotkey listener drives it.** He asked for this
after rejecting both desktop shortcuts and an in-app plugin ("нажимаю f9 f10
ничего не меня"). `jarvis_switch.py` polls `GetAsyncKeyState` for F9/F10 and
runs the maximise-one / minimise-other action; F9 also *launches* the visual if
it is not running. He confirmed it working: "работает, все хорошо, четко".
Full recipe (listener loop, window find/activate, pywebview app, autostart):
`references/window-switching.md`.

- `1_ВИЗУАЛ.bat` — maximise the HUD window to the full screen, minimise Hermes.
- `2_ЧАТ.bat` — maximise Hermes, minimise the HUD.

Each launches the HUD if it is not running, then:

```powershell
$sig=@'
[DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr after, int X, int Y, int cx, int cy, uint f);
[DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);
[DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
'@
$t=Add-Type -MemberDefinition $sig -Name WS -Namespace NS -PassThru
Add-Type -AssemblyName System.Windows.Forms
$b=[System.Windows.Forms.Screen]::PrimaryScreen.Bounds
# maximise the wanted window to the WHOLE screen
$t::ShowWindow($wanted.MainWindowHandle,1)|Out-Null
$t::SetWindowPos($wanted.MainWindowHandle,[IntPtr]::Zero,0,0,$b.Width,$b.Height,0x40)|Out-Null
$t::SetForegroundWindow($wanted.MainWindowHandle)|Out-Null
# hide the other: ShowWindow(handle, 6) = minimise
$t::ShowWindow($other.MainWindowHandle,6)|Out-Null
```

The HUD window is the process whose `MainWindowTitle` is **exactly** `Джарвис`
(the pywebview app); the chat is the `Hermes` process with a non-empty title.
Match the title EXACTLY — never by substring. A leftover browser tab titled
`Джарвис — Ядро v2` (the old browser form of the HUD) is matched by `Джарвис`
in title or `Ядро` in title and silently wins the lookup, so F9 maximises that
stale tab and the real app never appears. Minimising (not closing) the HUD
keeps its mic loop alive in the background.

To *preview* a variant in-app instead, use `desktop_preview` (action=open with
the HTML path, action=close to dismiss) — fine for showing him an option, but
it is not his steady-state layout.

## Build & verify loop

1. Edit the HTML (patch for a small change; a new versioned file for a rewrite).
2. Open it: `powershell -NoProfile -Command "Start-Process '<path>'"`.
3. Screenshot and LOOK at it before claiming the change landed.
4. To capture a specific window, bring it forward first.

## Jarvis desktop plugin (sidebar buttons Визуал/Чат)

For the full breakdown see the skill `jarvis-plugin` (created this session): one folder
`plugins/jarvis-switch/` with `dashboard/manifest.json` + `dashboard/plugin_api.py` +
`desktop/plugin.js`. No `plugin.yaml` — it breaks the Python loader (`No __init__.py`).

Before shipping: check `state.db` for a stale `jarvis-switch` record (search
`messages_fts_trigram` table) and reset via `state.db` delete + restart if found.


1. Edit the HTML (patch for a small change; a new versioned file for a rewrite).
2. Open it: `powershell -NoProfile -Command "Start-Process '<path>'"`.
3. Screenshot and LOOK at it before claiming the change landed:
   PowerShell `[System.Windows.Forms.SystemInformation]::VirtualScreen` +
   `Graphics.CopyFromScreen` → save PNG → inspect with `vision_analyze`.
   Never report a visual change you have not seen.
4. To capture a specific window, bring it forward first —
   `ShowWindow(handle, 3)` then `SetForegroundWindow(handle)` — otherwise the
   Hermes window sits on top and you photograph the wrong thing.

## Pitfalls

- **`ShowWindow(SW_MAXIMIZE)` alone is unreliable for minimised windows.** A
  minimised window often ignores a bare `ShowWindow(SW_MAXIMIZE)` — the call
  returns success but nothing visibly changes. Use the full sequence:
  `SW_RESTORE` → `SW_SHOWNORMAL` → `SW_MAXIMIZE` → `SetForegroundWindow` →
  `BringWindowToTop`, with a short `time.sleep` (0.1–0.3 s) between each step.
  Full recipe: `references/window-switching.md`.

- **A browser blocks `fetch()` of local files under `file://`.** A HUD that
  reads `jarvis_status.json` via fetch shows `—` for every value. Inline the
  data into the HTML instead (a `var STATUS = {...}` block) and have the
  refresher script rewrite those numbers in place.
- **A browser caches `file://` pages.** After editing, the open window keeps
  the old render — close it (`CloseMainWindow()`) and re-`Start-Process` before
  judging. Otherwise the user reports "ничего не изменилось" and you chase a
  phantom bug.
- **`write_file` refuses to overwrite a file it has not read in the current
  task** (`stale_write_blocked`). Read it first, or save a new versioned
  filename. Versioned filenames are the cheaper habit here.
- **Cyrillic in `.bat` paths and console output mangles.** Do Unicode work
  (registry, Cyrillic paths) through PowerShell, and write files with
  `[System.IO.File]::WriteAllText($f,$t,[Text.Encoding]::UTF8)` rather than
  `Set-Content`.
- **Launching a `.bat` from this shell — two traps, one working form.**
  `cmd //c file.bat` fails under MSYS, and `powershell -File file.bat` also
  fails ("файл сценария не является PS1" — `-File` accepts only `.ps1`). The
  form that works is `powershell -NoProfile -Command "Start-Process -FilePath
  '<path>.bat'"` (add `-WindowStyle Hidden` for a background refresher). When
  you only need the PowerShell body, run it inline instead of via the `.bat`.
- **The two `.bat` switchers are the WORKING mode-toggle; the in-app plugin
  route is unfinished — do not promise it as working.** Launching
  `1_ВИЗУАЛ.bat` / `2_ЧАТ.bat` with `Start-Process -FilePath` was verified to
  maximise one window and minimise the other. The alternative — a desktop
  plugin adding «Визуал»/«Чат» rows to the sidebar — was NOT completed. Facts
  found by reading the Hermes source (so a future attempt does not re-grep for
  them): the sidebar nav area constant is `SIDEBAR_NAV_AREA = 'sidebar.nav'`
  (NOT `'sidebarNav'` — the wrong string silently contributes nothing); a
  plugin that must run a command needs a Python backend — `plugins/<id>/`
  holding `plugin.yaml` with an `api: dashboard/plugin_api.py` key, a
  `dashboard/plugin_api.py` (FastAPI `APIRouter`, reached from JS via
  `ctx.rest`/`fetch('/api/plugins/<id>/…')`), and the UI half copied to
  `desktop/plugin.js` — enabled via `plugins.enabled` in config.yaml.
  `host.request` exposes no command-execution method, so the JS half cannot
  launch a script by itself. **Activation has two separate gates**: the
  Python half is gated by `plugins.enabled` in config.yaml (set it with
  `hermes plugins enable "<Display Name>"` — the DISPLAY NAME, not the folder
  id; the id form errors), while the desktop half ships `defaultEnabled:
  false` and stays off until the user flips it in **Capabilities → Plugins**.
  Only then does **Reload desktop plugins** (⌘K) matter. Load the `hermes-agent`
  skill and read its desktop-plugins reference for the SDK.
- **Run standalone scripts with the SYSTEM Python, not the Hermes tools one.**
  The Hermes tools interpreter path contains characters that come back masked
  from tool output (`python-3.14.7+202****0901-win32-x64`), so a copied literal
  path fails with `No such file or directory` while the directory plainly
  exists. `%LOCALAPPDATA%\Programs\Python\Python311\python.exe` is a plain
  path, has `pip`, and is what the launcher `.bat` and all verification probes
  should use; glob `tools/python-*` only as a fallback.
- **bash eats `$var` and `$env:` in an inline PowerShell command.**
  `terminal("powershell.exe -NoProfile -Command \"$py = Get-ChildItem $env:LOCALAPPDATA...\"")`
  arrives at PowerShell with the variables already expanded away (`= : ...
  CommandNotFoundException`). Put the PowerShell body in a `.ps1` or a `.bat`
  and invoke that file, or avoid `$` names entirely — do not try to escape it.
- **Start the hotkey listener as a tracked background process.**
  `terminal(..., background=true)` — a foreground `&` / `nohup` is refused, and
  `Start-Process` from inside a one-liner repeatedly failed to leave the
  process alive. Poll for the process by command-line match
  (`Win32_Process ... CommandLine -like '*jarvis_switch*'`) to confirm it is up;
  the earlier launch attempts exited immediately and looked "running" only
  because a stale PID was present.
- **Match the HUD window by EXACT title, or a stale browser tab steals the
  hotkey.** With a substring match, an old browser window titled `Джарвис —
  Ядро v2` satisfies the test and is returned first, so F9 keeps raising the
  browser (he reported "F9 запускает папку/браузер", the app never opening).
  Compare `title.strip() == "Джарвис"` only. When switching the steady-state
  to the pywebview app, close the old browser tab first, and re-test the
  lookup after the change rather than trusting the edit.
- **Verify any UI claim with a screenshot you inspected.** This user cannot
  read the raw HTML; the screenshot is the shared ground truth.
- **When he says "я перекинул фото, посмотри" — find the file, don't ask.**
  He drops a reference image on the Desktop and expects you to locate it.
  Search by mtime over `Desktop`/`Downloads`/`Pictures`, and EXCLUDE your own
  screenshot debris (`_check*`, `_dark*`, `_voice*`, `_wave*`, `_mif*`, `_ft_*`)
  or you will "find" your last screenshot and analyse the wrong image. Then
  inspect it with `vision_analyze` and match the reference (spikes, ripples,
  colour). Clean up the debris at the end — it piles up in his folder.

## Reporting to this user

Rustam works by voice dictation (Russian) and cannot comfortably use a shell.
After every change: show the artifact (`::preview{file="..."}` for the HTML)
AND state what changed as a short before/after table. Give him mouse-only steps
for anything he must trigger (double-click a `.bat`, press Esc to leave
fullscreen). Verify by reading state back — a screenshot you inspected — never
by trusting "готово".

- **Act on the obvious reading and SHOW a result; do not open with a
  multi-question `clarify` form.** He cancelled several of these mid-flow —
  while iterating he wants to see the next variant, not answer a
  questionnaire. When his dictation breaks off mid-sentence ("сделай пожалуйста
  галактику…"), ask ONE short question, or build the most likely variant and
  show it.
- **"Покажи оба варианта" means build and display both, not describe them.**
  When he is unsure which he wants, produce the versions and let him react to
  pixels rather than asking him to choose in the abstract.
- **Some transcript lines are not for you.** He dictates in a room with
  family present; fragments arrive that are his son talking or a remark to
  someone else ("Это я не тебе", "ориентируйся на мой голос только"). Do not
  act on or answer those — hold the task thread and wait for the next real
  instruction rather than treating every garbled line as a request.
- **He will catch a false "done".** He flagged a claimed voice-reaction that
  was only a CSS animation ("Это ты просто картинку сделал, да?"). Never
  report a behavioural change you have not observed working; if you cannot
  verify it, say what you did and what remains unverified.
