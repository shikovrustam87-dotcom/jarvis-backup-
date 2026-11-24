# Unicode-safe autostart + persistence audit for Windows.
# Run: powershell -NoProfile -ExecutionPolicy Bypass -File audit-autostart.ps1
# Read-only: enumerates and prints, deletes nothing.

$ErrorActionPreference = 'SilentlyContinue'

function Show-Key($path) {
  $p = Get-ItemProperty -Path $path
  if ($p) {
    Write-Output "[$path]"
    $p.PSObject.Properties | Where-Object { $_.Name -notlike 'PS*' } |
      ForEach-Object { Write-Output "  $($_.Name) = $($_.Value)" }
    Write-Output ''
  }
}

Write-Output '=== REGISTRY RUN KEYS ==='
foreach ($k in @(
  'HKCU:\Software\Microsoft\Windows\CurrentVersion\Run',
  'HKCU:\Software\Microsoft\Windows\CurrentVersion\RunOnce',
  'HKLM:\Software\Microsoft\Windows\CurrentVersion\Run',
  'HKLM:\Software\Microsoft\Windows\CurrentVersion\RunOnce',
  'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run',
  'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\RunOnce'
)) { Show-Key $k }

Write-Output '=== STARTUP FOLDERS ==='
$sh = New-Object -ComObject WScript.Shell
foreach ($d in @(
  "$env:APPDATA\Microsoft\Windows\Start Menu\Programs\Startup",
  "$env:ProgramData\Microsoft\Windows\Start Menu\Programs\Startup"
)) {
  Write-Output "[$d]"
  Get-ChildItem -Path $d -ErrorAction SilentlyContinue | ForEach-Object {
    if ($_.Extension -eq '.lnk') {
      $l = $sh.CreateShortcut($_.FullName)
      Write-Output "  $($_.Name) -> $($l.TargetPath) $($l.Arguments)"
    } else {
      Write-Output "  $($_.Name) (not a shortcut — inspect contents)"
    }
  }
  Write-Output ''
}

Write-Output '=== SCHEDULED TASKS LAUNCHING A SCRIPT HOST ==='
Get-ScheduledTask | Where-Object { $_.Actions.Execute -match 'cmd|mshta|wscript|cscript|powershell' } |
  ForEach-Object {
    Write-Output "$($_.TaskName) [$($_.TaskPath)] -> $($_.Actions.Execute) $($_.Actions.Arguments)"
  }
Write-Output ''

Write-Output '=== TASKS REFERENCING A URL OR reg add ==='
Get-ScheduledTask | Where-Object { $_.Actions.Arguments -match 'http|reg add' } |
  ForEach-Object { Write-Output "$($_.TaskName) [$($_.TaskPath)] -> $($_.Actions.Arguments)" }
Write-Output '(done)'
