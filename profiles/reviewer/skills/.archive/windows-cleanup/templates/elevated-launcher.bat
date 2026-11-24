@echo off
REM Self-elevating launcher for admin-only Windows cleanup work.
REM
REM Use when a delete needs administrator rights (HKLM Run keys, scheduled tasks)
REM and the agent cannot self-elevate. Copy this .bat and its companion
REM elevated-work.ps1 to the Desktop (keep the same folder), then tell the user to
REM right-click the .bat -> "Run as administrator". It re-launches itself elevated
REM and runs the companion script, which does the work and writes a log the agent
REM reads back.
REM
REM Keep the user's only action a mouse click: never hand them a command to retype.

chcp 65001 >nul

net session >nul 2>&1
if %errorlevel% neq 0 (
    echo Requesting administrator rights...
    powershell -NoProfile -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
    exit /b
)

echo Running elevated work...
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0elevated-work.ps1"
echo.
echo Finished. The script wrote a log beside itself.
pause
