---
name: windows-cleanup
description: "Clean up a Windows PC: disk, autostart, adware."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [windows, cleanup, disk-space, autostart, adware, persistence, powershell]
    related_skills: [computer-use]
---

# Windows cleanup & startup-persistence audit

Covers "почисти компьютер", "ускорь систему", freeing disk space, trimming
autostart, and hunting adware that re-creates itself. The machine is Windows;
the `terminal` tool runs through git-bash/MSYS (POSIX syntax), but native
registry/task work must go through PowerShell — see Pitfalls.

## When to Use

Trigger on any request to clean, debloat, or speed up a Windows machine: free
disk space, clear temp/cache, trim autostart, or investigate something that
launches at logon. Also use it when a Run/autostart entry keeps coming back —
the re-creation check is the whole point of step 4.

## Procedure

### 1. Recon first — never delete before surveying

Report the state before touching anything:

```bash
df -h / | tail -1                     # free space on C: (MSYS root == C:)
du -sh "$LOCALAPPDATA/Temp" "$WINDIR/Temp" "$LOCALAPPDATA/CrashDumps" 2>/dev/null
```

Do NOT run a blanket `du -sh` over the whole user profile — it times out on
large profiles. Measure the specific targets you intend to clean.

### 2. Safe-to-delete targets

`%LOCALAPPDATA%\Temp`, `%WINDIR%\Temp`, `%LOCALAPPDATA%\CrashDumps`,
`%WINDIR%\SoftwareDistribution\Download`, the Recycle Bin, and the
thumbnail/icon cache (`%LOCALAPPDATA%\Microsoft\Windows\Explorer\thumbcache_*.db`,
`iconcache_*.db`). Emptying `INetCache` is also fine.

**Do NOT bulk-delete `%LOCALAPPDATA%\Packages`** — it holds real per-app data
and deleting it breaks Store apps. Report its size, leave it alone.

Expect Temp not to empty fully: files held open by running processes survive.
Re-measure and report the remainder instead of claiming a full wipe.

### 3. Autostart inventory

Enumerate every startup surface (the full list is in
`references/persistence-locations.md`). Minimum set:

```powershell
foreach ($k in @('HKCU:\Software\Microsoft\Windows\CurrentVersion\Run',
                 'HKLM:\Software\Microsoft\Windows\CurrentVersion\Run',
                 'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run')) {
  $p = Get-ItemProperty -Path $k -ErrorAction SilentlyContinue
  if ($p) { "[$k]"; $p.PSObject.Properties | ? { $_.Name -notlike 'PS*' } | % { "  $($_.Name) = $($_.Value)" } }
}
```

Also list both Startup folders (`%APPDATA%` and `%ProgramData%`
`\Microsoft\Windows\Start Menu\Programs\Startup`) and resolve each `.lnk` with
`(New-Object -ComObject WScript.Shell).CreateShortcut($f)` to see its target.

`scripts/audit-autostart.ps1` runs the whole read-only sweep in one shot.

### 4. Check for re-creation (the step that matters)

A Run entry can be re-created at every logon by a scheduled task. **Deleting the
Run value without removing the task is a no-op** — it returns after reboot.
Always scan task actions for the tell-tale patterns:

```powershell
Get-ScheduledTask | ? { $_.Actions.Execute -match 'cmd|mshta|wscript|powershell' } |
  % { "$($_.TaskName) -> $($_.Actions.Execute) $($_.Actions.Arguments)" }
```

Look for `reg add ...\Run`, `start www.<site>`, `mshta ... .hta`. A task whose
only job is to write a Run value is persistence — remove the task AND the value.

### 5. Back up before deleting

```bash
reg export "HKCU\Software\Microsoft\Windows\CurrentVersion\Run" "$USERPROFILE/Desktop/autostart_backup.reg" /y
```

Tell the user where the backup landed.

### 6. Classify each item before removing it

For any unfamiliar executable or startup entry, check its signature and metadata
before deciding:

```powershell
$i = Get-Item $path
$i.VersionInfo | Format-List FileDescription,CompanyName,ProductName
Get-AuthenticodeSignature $path | Format-List Status,SignerCertificate
```

- **Validly signed + real vendor** (e.g. a printer/KKT driver under `C:\<Vendor>`) → legitimate, leave it. A `C:\`-root folder is not by itself evidence of malware.
- **Unsigned `cmd.exe`/`mshta.exe` launcher, or a root-folder HTA search bar** → adware, remove it.
- **Windows components** — leave alone: `SecurityHealth`, Windows Defender tasks, `hpatchmonTask.cmd` (hotpatch/VBS), `dsregcmd` tasks, and the user's own startup scripts.
- **Hermes' own persistence is legitimate — never remove it.** A scheduled task
  running `wscript.exe ...\hermes\gateway-service\Hermes_Gateway.vbs`, or a
  restart helper `C:\Users\Public\hermes_gw_restart.vbs` (kills `python.exe`
  with `gateway run`, then `schtasks /Run /TN Hermes_Gateway`), is Hermes
  infrastructure, not malware. A file living in `C:\Users\Public\` is not by
  itself suspicious; read it before judging. Removing these breaks the agent.
- **A scheduled task whose target script no longer exists** (e.g. a
  `nodeupdate.vbs` under a uTorrent profile folder) is a harmless orphan left
  behind after its payload was cleaned — note it, do not chase it.

### 7. Remove, then verify by reading back

After deletion, re-query the same key/task and print the result. Never report
success from the delete command's exit code alone — a permission-denied delete
returns non-zero but so can a no-op.

### 8. Browser adware / popups (when the symptom is in-browser)

If the user reports popups/ads that reappear after closing, investigate the
browser layer separately from OS autostart:

1. **Identify the browser** (Edge/Chrome/Yandex/Firefox) and whether the popup
   is an in-page ad, a push notification, or a new tab/window.
2. **Extensions:** list installed extensions by ID under
   `%LOCALAPPDATA%\<Browser>\User Data\Default\Extensions`. Cross-check IDs
   against known adware. Remove suspicious ones via the browser's extension
   management page (not by deleting folders while the browser runs).
3. **Scheduled tasks:** scan task actions for `mshta`, `wscript`, `powershell`
   launching browser URLs or `.hta`/`.vbs` files (step 4). A task that opens a
   browser URL at logon is persistence.
4. **Hosts file:** `%WINDIR%\System32\drivers\etc\hosts` — check for
   redirects to ad/malware domains. Legitimate blocks (e.g. fake FitGirl sites)
   are fine; unexpected redirects are not.
5. **Push notifications:** browser site notifications can masquerade as system
   popups. Reset site permissions in browser settings.
6. **Startup entries:** browsers re-adding their own Run key at launch is
   app behavior, not malware — fix in browser settings.

Do NOT delete the browser's entire profile or user data folder — that destroys
bookmarks/passwords. Target the specific extension or permission instead.

## Pitfalls

- **MSYS bash mangles non-ASCII registry data.** `reg query` and `reg delete`
  corrupt or mis-handle Cyrillic value names (you get `???`/mojibake), and
  `grep -P` fails outright under a non-UTF8 locale. Do ALL registry enumeration
  and deletion through PowerShell (`Get-ItemProperty` / `Remove-ItemProperty`),
  which round-trips Unicode names correctly. `reg delete /v <name>` also fails
  when the name is Cyrillic — delete by matching on the *value* instead.
- **`HKLM` and scheduled tasks need administrator rights.** An elevated-only
  delete fails with `Access Denied` / `HRESULT 0x80070005`, and the agent cannot
  self-elevate. Don't retry in a loop. Best path: write the elevated work as a
  self-elevating launcher the user runs with the mouse — `templates/elevated-launcher.bat`
  re-launches itself via `Start-Process -Verb RunAs` and calls a companion
  `.ps1` (start from `templates/elevated-work.ps1`) that does the work and writes
  a log. Put both on the Desktop, tell the
  user to right-click the `.bat` → "Запуск от имени администратора", then read
  the log back to verify. This keeps the session alive (no app restart) and
  needs no shell typing from the user. Fallbacks: the GUI path (`Win` →
  "Планировщик заданий" → Task Scheduler Library → find the task → right-click →
  Delete), or restarting the app as administrator.
- **A single Run value may exist under more than one name.** When hunting a
  specific payload (a URL, a path), scan by *value* across all Run/RunOnce keys,
  not by guessing the value name — duplicates under different names are common.
- **Don't equate "in autostart" with "malware".** Verify signature first; a
  signed vendor driver that happens to auto-start is not a threat, and removing
  it breaks hardware (printers, cash registers).
- **A PowerShell log written with `Out-File -Encoding UTF8` on PS 5.1 is UTF-16,
  so reading it with bash `cat` shows `\u0000`-riddled mojibake.** Read the log
  back through PowerShell (`Get-Content`) or match on its ASCII markers — do not
  conclude the script failed just because the bytes look garbled in the shell.
- **Re-check autostart after a reboot.** A self-resetting app (e.g. a browser
  re-adding its own Run key at each launch) can reappear even after a clean
  removal; that is the app's behavior, not persistence — fix it in the app's
  settings, don't keep deleting the key.

## Reporting to this user

Rustam works by voice dictation and is not comfortable in a shell. Deliver
results as a short status table (what was cleaned, how much freed, what remains),
name anything you deliberately left untouched and why, and give any
admin-required step as a mouse-only GUI path. Verify each step by reading state
back — do not take "готово" at face value.
