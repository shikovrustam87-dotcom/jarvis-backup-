# Real system stats for the HUD

## Live machine metrics (PowerShell)

Collect CPU / RAM / disk / uptime / Hermes process footprint. Either write compact
JSON, or regex-replace the `var STATUS = {...}` numbers inside the HUD itself
(the reliable path — the browser cannot fetch local JSON).

```powershell
$os=Get-CimInstance Win32_OperatingSystem
$cpu=[int](Get-CimInstance Win32_Processor | Measure-Object -Property LoadPercentage -Average).Average
$ram=[math]::Round((($os.TotalVisibleMemorySize-$os.FreePhysicalMemory)/$os.TotalVisibleMemorySize)*100,0)
$ramFree=[math]::Round($os.FreePhysicalMemory/1MB,1)
$d=Get-CimInstance Win32_LogicalDisk -Filter "DeviceID='C:'"
$disk=[math]::Round((($d.Size-$d.FreeSpace)/$d.Size)*100,0)
$up=[math]::Round(((Get-Date)-$os.LastBootUpTime).TotalHours,1)
$hb=Get-Process Hermes,python -ErrorAction SilentlyContinue | Measure-Object -Property WorkingSet64 -Sum
$hbMB=[math]::Round($hb.Sum/1MB,0); $hbN=(Get-Process Hermes,python).Count
```

Colour the bar by severity: under 65% blue, 65-85% amber, over 85% red.

## Wallet / tokens

`hermes usage` prints the configured provider's account limits — for OpenRouter
it is the credits balance and spend:

```
Credits balance: $8.95
API key usage: $1.05 total - $0.34 today - ...
```

Parse those into the wallet card (provider name, balance, spend). Do not invent a
crypto wallet balance — if the user means a crypto wallet, ask for the address and
pull a real rate.

## Connected programs

- Desktop + gateway: the `hermes`/`python` processes (`Get-Process Hermes,python`).
- Messaging channels: `$HERMES_HOME/sessions/sessions.json` maps
  `agent:main:<platform>:...` keys to active sessions — use it to list which
  messengers are wired in.

## Refresher

A background `.bat` loop re-runs the block every few seconds and regex-replaces
the `STATUS` numbers inside the HTML. Because the browser cannot fetch local
JSON, writing into the page itself is the reliable path.
