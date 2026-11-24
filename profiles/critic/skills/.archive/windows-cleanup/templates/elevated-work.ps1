# Elevated work template. Launched by templates/elevated-launcher.bat, which
# re-runs itself via `Start-Process -Verb RunAs`, so this script already has
# administrator rights when it starts.
#
# Two rules that keep this reliable:
#   1. Keep every string literal in this file ASCII. PowerShell 5.1 can read a
#      UTF-8 no-BOM file with the wrong codepage and mangle Cyrillic literals.
#   2. Write findings to a log, then read the log back from the main session to
#      verify. Do not trust the launcher's exit code alone.

$ErrorActionPreference = 'Continue'
$log = Join-Path ([Environment]::GetFolderPath('Desktop')) 'elevated_log.txt'
"=== ELEVATED RUN $(Get-Date) ===" | Out-File -FilePath $log -Encoding UTF8
function Log($m) { $m | Tee-Object -FilePath $log -Append | Out-Null }

Log "--- BEFORE ---"

# --- the admin-only work goes here, e.g. ---
# $t = Get-ScheduledTask | Where-Object { $_.Actions.Arguments -like '*<payload>*' }
# foreach ($task in $t) {
#     Log ("Removing task: [" + $task.TaskName + "] at " + $task.TaskPath)
#     Unregister-ScheduledTask -TaskName $task.TaskName -TaskPath $task.TaskPath -Confirm:$false
# }
# Remove-ItemProperty -Path 'HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Run' -Name '<value>' -Force

Log ""
Log "--- AFTER (read back to verify) ---"

Log "=== DONE ==="
