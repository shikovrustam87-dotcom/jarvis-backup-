---
name: windows-defender
description: "Windows Defender: scan, threats, exclusions, quarantine."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [windows, defender, antivirus, scan, threats, exclusions, quarantine, security, powershell]
    related_skills: [windows-cleanup, computer-use]
---

# Windows Defender — antivirus operations

Covers "проверь на вирусы", running Defender scans, reading threat detections,
and removing suspicious exclusions. The `terminal` tool runs through git-bash/MSYS
(POSIX syntax), but registry/Defender work must go through PowerShell — see
Pitfalls.

## When to Use

Trigger on any request to check a Windows PC for viruses, run an antivirus scan,
review threat detections, or remove Defender exclusions. Also use when the user
reports that Defender "doesn't see" a suspicious folder — it may be excluded.

## Procedure

### 1. Recon first — check Defender status

```powershell
Get-MpComputerStatus | Select-Object AntivirusEnabled, RealTimeProtectionEnabled,
  AntispywareEnabled, NISEnabled, AMServiceEnabled, QuickScanAge, FullScanAge
```

Report whether real-time protection is on and when the last scan ran. Do not
assume the last scan was recent — `QuickScanAge`/`FullScanAge` are in days.

### 2. Run a scan

- **Quick scan** (2–10 min): `Start-MpScan -ScanType QuickScan`
- **Full scan** (30 min–2 h+): `Start-MpScan -ScanType FullScan`

Full scans on machines with large game libraries can take 1–2 hours. Run in the
background and poll `FullScanAge` (becomes 0 when complete) rather than
blocking. Do not re-launch if a scan is already running — check `MsMpEng`
process or `FullScanAge` first.

### 3. Read threats

```powershell
# Active threats currently on the system
Get-MpThreat | Select-Object ThreatName, ThreatID, SeverityID, CategoryID, Resources

# Historical detections (what Defender found and acted on)
Get-MpThreatDetection | Select-Object ThreatName, DetectionID, Status,
  ActionSuccess, InitialDetectionTime, Resources
```

`Get-MpThreat` returns threats still present (including in quarantine). `Status`
empty with `ActionSuccess = True` means Defender already acted (cleaned/quarantined).
SeverityID 5 = severe (trojan), 4 = high, 1 = low (PUA).

### 4. Inspect exclusions (critical step)

Malware often adds itself to Defender exclusions to hide. Always check:

```powershell
$pref = Get-MpPreference
$pref.ExclusionPath
$pref.ExclusionProcess
$pref.ExclusionExtension
```

Suspicious patterns: folders with random-looking names under `%ProgramData%`
(e.g. `BackupCitadel-<guid>`, `CloudProtector-<guid>`, `DataBridgeElite-<guid>`),
`NEXTRP Launcher`, `ivanovsasha224`, or `C:\Windows\SysWOW64` excluded entirely.
These are NOT legitimate exclusions — remove them.

### 5. Remove exclusions — registry, not MpPreference

**Pitfall:** exclusions added via Group Policy live in the registry and
`Remove-MpPreference` reports success but does NOT remove them. They persist.

Check and remove from the policy key:

```powershell
$regPath = 'HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender\Exclusions\Paths'
if (Test-Path $regPath) {
    Get-ItemProperty $regPath | Select-Object -ExcludeProperty PS*
    Remove-Item -Path $regPath -Recurse -Force
}
```

Verify by re-reading `Get-MpPreference | Select ExclusionPath` — count must drop.
Also remove `ExclusionProcess` and `ExclusionExtension` subkeys if present.

After removal, the running full scan may still skip already-scanned excluded
folders; future scans will check them.

### 6. Check for active suspicious processes

```powershell
Get-Process | Where-Object { $_.Path -like '*DataBridgeElite*' -or
  $_.Path -like '*BackupCitadel*' -or $_.Path -like '*CloudProtector*' -or
  $_.Path -like '*NetworkSentinel*' } | Select-Object Name, Id, Path
```

Stop with `Stop-Process -Id <id> -Force`.

### 7. Report

Deliver a short table: what was found (threat count by severity), what was
removed (exclusions, processes), what scan is running, and what remains. Name
anything deliberately left untouched and why.

## Pitfalls

- **MSYS bash mangles non-ASCII registry data.** `reg query`/`reg delete`
  corrupt Cyrillic value names. Do ALL registry/Defender work through PowerShell
  (`Get-ItemProperty` / `Remove-Item` / `Remove-MpPreference`).
- **Exclusions set via Group Policy (registry) cannot be removed with
  `Remove-MpPreference`.** It reports success but the key persists. Remove the
  registry key directly under `HKLM:\SOFTWARE\Policies\Microsoft\Windows Defender\Exclusions\`.
- **`HKLM` changes need admin rights.** If access is denied, write a
  self-elevating launcher (see `windows-cleanup` pitfall) rather than retrying.
- **Do not delete system folders that happen to be excluded.** `SysWOW64` is a
  legitimate Windows directory — only remove the *exclusion*, not the folder.
- **Do not delete user data folders** (Downloads, Desktop) even if threats were
  found there — quarantine via Defender instead.
- **Verify by reading back.** Never report success from a delete command's exit
code alone.
- **A full scan running in the background:** poll `FullScanAge` rather than
  blocking the session. Do not launch a second scan concurrently.
