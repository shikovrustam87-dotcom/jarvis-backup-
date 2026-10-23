"""
Dashboard API для плагина jarvis-switch.
Эндпоинт: POST /api/plugins/jarvis-switch/switch
Реальное переключение окон Визуал/Чат через PowerShell + user32.dll.
"""
import os
import subprocess
import tempfile

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


class SwitchRequest(BaseModel):
    target: str


HUD_DIR = r"C:\Users\Пользователь\Desktop\Для Джарвиса"
HUD_APP = r"C:\Users\Пользователь\Desktop\Для Джарвиса\jarvis_app.py"
PYTHON_EXE = r"C:\Users\Пользователь\AppData\Local\Programs\Python\Python311\python.exe"

PS_HEADER = r'''
Add-Type -AssemblyName System.Windows.Forms
$sig = @'
[DllImport("user32.dll")] public static extern bool SetWindowPos(IntPtr h, IntPtr a, int x, int y, int cx, int cy, uint f);
[DllImport("user32.dll")] public static extern bool ShowWindow(IntPtr h, int n);
[DllImport("user32.dll")] public static extern bool SetForegroundWindow(IntPtr h);
'@
$t = Add-Type -MemberDefinition $sig -Name SW -Namespace NS -PassThru
$SWP = 0x40
$b = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
'''

PS_VISUAL = PS_HEADER + r'''
$jar = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 -and $_.MainWindowTitle.Trim() -eq 'Джарвис' } | Select-Object -First 1
if (-not $jar) {
    Start-Process -FilePath "''' + PYTHON_EXE + r'''" -ArgumentList "''' + HUD_APP + r'''" -WorkingDirectory "''' + HUD_DIR + r'''"
    Start-Sleep -Seconds 9
    $jar = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 -and $_.MainWindowTitle.Trim() -eq 'Джарвис' } | Select-Object -First 1
}
if ($jar) {
    $t::ShowWindow($jar.MainWindowHandle, 1) | Out-Null
    $t::SetWindowPos($jar.MainWindowHandle, [IntPtr]::Zero, 0, 0, $b.Width, $b.Height, $SWP) | Out-Null
    $t::SetForegroundWindow($jar.MainWindowHandle) | Out-Null
}
$her = Get-Process hermes -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
if ($her) { $t::ShowWindow($her.MainWindowHandle, 6) | Out-Null }
if ($jar) { Write-Output "OK: visual"; exit 0 } else { Write-Output "ERR: hud not found"; exit 1 }
'''

PS_CHAT = PS_HEADER + r'''
$her = Get-Process hermes -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 } | Select-Object -First 1
if ($her) {
    $t::ShowWindow($her.MainWindowHandle, 1) | Out-Null
    $t::SetWindowPos($her.MainWindowHandle, [IntPtr]::Zero, 0, 0, $b.Width, $b.Height, $SWP) | Out-Null
    $t::SetForegroundWindow($her.MainWindowHandle) | Out-Null
}
$jar = Get-Process python -ErrorAction SilentlyContinue | Where-Object { $_.MainWindowHandle -ne 0 -and $_.MainWindowTitle.Trim() -eq 'Джарвис' } | Select-Object -First 1
if ($jar) { $t::ShowWindow($jar.MainWindowHandle, 6) | Out-Null }
if ($her) { Write-Output "OK: chat"; exit 0 } else { Write-Output "ERR: hermes not found"; exit 1 }
'''


def _run_ps(script: str):
    fd, path = tempfile.mkstemp(suffix=".ps1", prefix="jarvis_switch_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8-sig") as f:
            f.write(script)
        proc = subprocess.run(
            ["powershell", "-NoProfile", "-ExecutionPolicy", "Bypass", "-File", path],
            capture_output=True,
            text=True,
            timeout=30,
        )
        return proc.returncode, (proc.stdout or "").strip(), (proc.stderr or "").strip()
    finally:
        try:
            os.remove(path)
        except OSError:
            pass


@router.post("/switch")
async def switch(req: SwitchRequest):
    target = req.target
    if target not in ("visual", "chat"):
        raise HTTPException(status_code=400, detail="target must be 'visual' or 'chat'")
    if target == "visual":
        rc, out, err = _run_ps(PS_VISUAL)
    else:
        rc, out, err = _run_ps(PS_CHAT)
    ok = rc == 0 and out.startswith("OK:")
    message = out if out else (err if err else "done")
    return {"ok": ok, "message": message}
