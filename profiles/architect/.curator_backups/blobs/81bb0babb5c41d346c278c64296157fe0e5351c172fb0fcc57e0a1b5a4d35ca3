# Windows autostart & persistence locations

Check every one of these when auditing what launches on a machine. A payload
that is gone from one location routinely survives in another.

## Registry Run keys

| Key | Scope |
|---|---|
| `HKCU\Software\Microsoft\Windows\CurrentVersion\Run` | current user, logon |
| `HKCU\...\RunOnce` | current user, once then self-deletes |
| `HKLM\Software\Microsoft\Windows\CurrentVersion\Run` | all users, logon |
| `HKLM\Software\Microsoft\Windows\CurrentVersion\RunOnce` | all users, once |
| `HKLM\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run` | 32-bit apps on 64-bit Windows |
| `HKLM\...\WOW6432Node\...\RunOnce` | 32-bit, once |

HKCU is user-writable and the agent can edit it; HKLM and WOW6432Node need admin.

## Startup folders

- `%APPDATA%\Microsoft\Windows\Start Menu\Programs\Startup` (per-user)
- `%ProgramData%\Microsoft\Windows\Start Menu\Programs\Startup` (all users)

Resolve every `.lnk` to its target — the filename tells you nothing:

```powershell
$sh = New-Object -ComObject WScript.Shell
Get-ChildItem "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\Startup" |
  ? Extension -eq '.lnk' | % { $l = $sh.CreateShortcut($_.FullName); "$($_.Name) -> $($l.TargetPath) $($l.Arguments)" }
```

(`.bat`/`.cmd` in a startup folder are run directly — read their contents.)

## Scheduled tasks

The re-creation vector. A task can write a Run value on every logon, so the Run
entry comes back no matter how many times you delete it.

```powershell
# tasks that launch a script host at all
Get-ScheduledTask | ? { $_.Actions.Execute -match 'cmd|mshta|wscript|cscript|powershell' } |
  % { "$($_.TaskName) [$($_.TaskPath)] -> $($_.Actions.Execute) $($_.Actions.Arguments)" }

# full detail on one task
Get-ScheduledTask -TaskName '<name>' | % { $_.Actions | Format-List *; $_.Triggers | Format-List * }
```

Red flags: `Execute` is a script host AND `Arguments` contain `reg add`, `start
www.<something>`, a path under a root folder, or a bare URL. Also watch for
tasks masquerading as updaters (`EdgeUpdate` running `auditpol`, etc.).

Remove with `Unregister-ScheduledTask -TaskName X -TaskPath Y -Confirm:$false`
(requires admin). TaskPath matters — tasks can live in subfolders, not just `\`.

## Legitimate things that look suspicious

Verify before removing anything from this list:

- `hpatchmonTask.cmd` and similar hotpatch/VBS scripts in `System32` — a Windows component.
- `SecurityHealth` (`SecurityHealthSystray.exe`) — Windows Security.
- Windows Defender scheduled tasks (`MpCmdRun.exe` with `-IdleTask`).
- `dsregcmd.exe` tasks (`Automatic-Device-Join`, `Recovery-Check`) — Entra/Azure AD join.
- Signed vendor software that auto-starts: printer/KKT drivers, VPN clients, `OneDrive`.
- The user's own startup scripts (a personal `*.bat` they wrote).
