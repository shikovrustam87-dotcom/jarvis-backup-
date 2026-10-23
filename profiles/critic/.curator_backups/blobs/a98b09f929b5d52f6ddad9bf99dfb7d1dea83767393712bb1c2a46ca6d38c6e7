# Troubleshooting

### Voice not working
1. Check `stt.enabled: true` in config.yaml
2. Verify provider: `python -c "import pm; pm.sync_venv(['stt-whisper'], explicit=True)"` or set API key
3. In gateway: `/restart`. In CLI: exit and relaunch.

### STT / faster-whisper import errors (av version conflict)
`faster-whisper==1.2.1` pulls `av>=19` which is incompatible — `Transcribe()` raises
`TypeError: open() got an unexpected keyword argument 'metadata_errors'`. Fix: pin `av`
to a compatible version. On Windows without C++ build tools, `av` can only be installed
from a pre-built wheel — prefer `av==16.0.1` (wheel available; `14.x` requires C++ build
tools and fails). Install via uv into the active venv:
```bash
cd tools && UV=$(ls -d uv-*/uv.exe | head -1)
$UV pip install --python <venv>/Scripts/python.exe "av==16.0.1"
```
After the fix, restart the gateway so the new module loads.

### Edge TTS returns 403 "Invalid response status"
The bundled pin is stale: `pyproject.toml` pins `edge-tts = ["edge-tts==X.Y.Z"]`, and old versions get 403 from Microsoft's `speech.platform.bing.com` endpoint. Fix:
1. Find the ACTIVE environment venv: read `installs/<hash>/facts.json` → `packages.venv.environment` (other `environments/<hash>/venv` dirs are stale).
2. Upgrade inside it: `tools/uv-*/uv.exe pip install --python <venv>/Scripts/python.exe "edge-tts==<latest>"` (native Windows path).
3. Bump the same pin in `hermes-agent/pyproject.toml` so a re-sync doesn't revert it.
4. Restart the gateway (below) — the module is cached in the running gateway's `sys.modules`, so it never reimports without a restart. Tell-tale: the tool still 403s while a direct `edge_tts.Communicate(...).save()` from the venv python succeeds. After the bump a transient "No audio was received" can appear once — retrying succeeds.

### Restarting the gateway from inside the gateway (Windows)
`hermes gateway restart` is blocked from a gateway-run agent (SIGTERM would kill the command's own parent). Plain detached children (`Start-Process wscript`, `cmd /c start`) are ALSO killed when the terminal call returns — the tool tears down the process tree. The one path that survives is Windows Task Scheduler:
1. Write a pure-ASCII `.vbs` under an ASCII path (e.g. `C:\Users\Public\` — Cyrillic path/content breaks `wscript`'s ANSI read). Declare EVERY variable under `Option Explicit`, or it dies silently before writing a log.
2. `schtasks /Create /F /TN "HermesGWRestart" /SC ONCE /ST <HH:MM> /TR "wscript.exe //B //Nologo C:\path\script.vbs"` then `schtasks /Run /TN "HermesGWRestart"` (prefix `export MSYS2_ARG_CONV_EXCL="*"` in git-bash).
3. The task runs under the scheduler service, outside the agent's tree. Have the script `WScript.Sleep` ~15s first so the agent's reply is delivered, then terminate the gateway python (WMI `Win32_Process WHERE Name='python.exe'` + CommandLine contains `gateway run` → `.Terminate()`), then `schtasks /Run /TN "Hermes_Gateway"`.
4. Verify the PID changed (`hermes gateway status`). `schtasks /End` alone does NOT kill the detached python — only `.Terminate()`/taskkill does. Clean up the task and scripts afterwards.

### Tool not available
1. `hermes tools` — check if toolset is enabled for your platform
2. Some tools need env vars (check `.env`)
3. `/reset` after enabling tools

### Model/provider issues
1. `hermes doctor` — check config and dependencies
2. `hermes auth` — re-authenticate OAuth providers (or `hermes auth add <provider>`)
3. Check `.env` has the right API key
4. **Copilot 403**: `gh auth login` tokens do NOT work for Copilot API. You must use the Copilot-specific OAuth device code flow via `hermes model` → GitHub Copilot.

### Agent became slow, or "dumb"/ineffective
Quantify before theorizing — read the turn durations and the error signature; do not
guess at cause:
```bash
cd "${HERMES_HOME:-$HOME/.hermes}/logs"
grep -aE "tui turn finished.*duration=" agent.log | tail -30   # per-turn wall time
grep -aiE "402|429|APIConnectionError|Retrying API call" errors.log | tail -30
```
A normal turn is ~2-5 s. Durations of 100-700 s mean requests are being rejected and
retried, not that the model is thinking hard. Ranked causes, most common first:

1. **Provider credits exhausted (HTTP 402).** OpenRouter answers
   `402 ... "This request requires more credits, or fewer max_tokens ... can only afford N"`
   and `reason: in_flight_budget_exhausted`. Each rejected call is retried ~3x and the
   agent then **falls back to the weaker free models in `fallback_providers`** — so the
   symptom is not only slowness but a visible drop in capability. Fix the quota (top up,
   or point the main model at a provider whose key has headroom). Do NOT treat
   "the agent got dumber" as a prompt/config problem while 402s are in the log.
2. **Context bloat.** The 402 body carries the prompt size (e.g.
   `Prompt tokens limit exceeded: 105201 > 25800`). With a thin balance a large prompt is
   unaffordable forever. Lower `compression.threshold` and/or start a fresh session.
3. **`fallback_providers` silently active** — check which model actually served the turn;
   every turn may be running on Groq/Nous free models without any error reaching the user.
4. **Network** — `APIConnectionError`, `ConnectTimeout`: transient, not fixable in config.

An exhausted main provider also breaks `auxiliary.*` tasks pinned to it (vision,
compression, title_generation) — they need their own quota, not just the main key.

### Evaluating a provider switch before recommending it
Probe reachability AND the per-minute limits from the response headers — a provider can be
perfectly reachable and still unusable for a large context. Run
`scripts/probe_provider_limits.sh <BASE_URL> <MODEL> <ENV_KEY_NAME>` (reads the key from
`.env`, prints the `x-ratelimit-*` headers). Key facts to read:
- `x-ratelimit-limit-tokens` is **tokens per minute (TPM)**. Groq's free tier reports
  **8000 TPM**: a single turn carrying tens of thousands of tokens of context cannot fit,
  so the agent stalls between turns waiting for the bucket to refill.
- Report the MEASURED number, never a remembered one, and compare it against the current
  prompt size before recommending the switch — a "free and fast" provider with a low TPM
  cap is a worse experience than a paid one for a long-lived session.
- **Confirm the model is actually servable on the target key before recommending it.**
  Probing `GET /v1/models` is part of the switch check, not optional — catalogs change and a
  familiar model name is not a plan. Groq's free catalog lists no chat Llama at all (only
  `llama-prompt-guard` classifiers, which are not chat models), and OpenRouter rejects a
  `:free` Llama slug with `404 ... This model is unavailable for free`. Quote the exact model
  slug the target key actually lists, and say plainly when the requested model is not offered
  rather than substituting a guess.

### Changes not taking effect
- **Tools/skills:** `/reset` starts a new session with updated toolset
- **Config changes:** In gateway: `/restart`. In CLI: exit and relaunch.
- **Code changes:** Restart the CLI or gateway process

### web_extract shows a stale page (result caching)
`web_search`/`web_extract` cache results for 20 minutes (PR #94618) — a
repeat fetch of the same URL within the TTL is served from cache, which
can look like "my website changes aren't showing up."

Automatic carveouts (always fetched live, never cached):
- localhost / 127.0.0.1 / `*.local` / `*.localhost` / single-label LAN
  hostnames / private + link-local IP ranges (dev servers, hot-reload
  builds, chat-GUI artifact previews)
- URLs matched by `security.website_blocklist`
- failed responses and keyless-rescue-served responses

Developing a site tested over the PUBLIC internet (Vercel/Netlify
preview, ngrok/cloudflared tunnel, staging domain)? Public DNS isn't
auto-carved-out — list the host in config.yaml:

```yaml
web:
  cache_exempt_hosts:      # always fetched live; effective immediately
    - mysite.vercel.app
    - "*.ngrok-free.app"
    - mysite.dev           # suffix match: also covers preview.mysite.dev
```

Blunt instruments: `web.cache_ttl_minutes: 1` (min) or
`web.cache_enabled: false` disables both caches entirely.

### Skills not showing
1. `hermes skills list` — verify installed
2. `hermes skills config` — check platform enablement
3. Load explicitly: `hermes -s name` (or the skill's own `/<name>` slash command)

### Gateway issues
Check logs first:
```bash
grep -i "failed to send\|error" ~/.hermes/logs/gateway.log | tail -20
```

Common gateway problems:
- **Gateway dies on SSH logout**: Enable linger: `sudo loginctl enable-linger $USER`
- **Gateway dies on WSL2 close**: WSL2 requires `systemd=true` in `/etc/wsl.conf` for systemd services to work. Without it, gateway falls back to `nohup` (dies when session closes).
- **Gateway crash loop**: Reset the failed state: `systemctl --user reset-failed hermes-gateway`

### Platform-specific issues
- **Discord bot silent**: Must enable **Message Content Intent** in Bot → Privileged Gateway Intents.
- **Slack bot only works in DMs**: Must subscribe to `message.channels` event. Without it, the bot ignores public channels.
- **Windows-specific issues** (`Alt+Enter` newline, WinError 10106, UTF-8 BOM config, line endings): see `references/windows-quirks.md`.

### Auxiliary models not working
If `auxiliary` tasks fail or the log floods with `Auxiliary Nous client unavailable` /
`resolve_provider_client: nous requested but Nous Portal not configured`, the `auto` provider
chain fell through to Nous Portal without an auth. Set `OPENROUTER_API_KEY`/`GOOGLE_API_KEY`, or
pin each task's provider explicitly (a working key already configured for the main model means
`openrouter` is the safe pin):
```bash
hermes config set auxiliary.vision.provider openrouter
hermes config set auxiliary.compression.provider openrouter
hermes config set auxiliary.title_generation.provider openrouter
```
- **Only some `auxiliary.*` keys are actually read.** `web_extract` and `session_search` no
  longer use an aux LLM — their config blocks are leftovers and are IGNORED; setting them logs
  a "not a recognized config key" notice and changes nothing. Live task keys include `vision`,
  `compression`, `title_generation`, `tts_audio_tags`, `background_review`, `review`, `mcp`,
  `curator`, `monitor`, `goal_judge`, `triage_specifier`, `kanban_decomposer` (see
  `config_defaults.py` `DEFAULT_CONFIG["auxiliary"]` for the current list).
- `hermes config set auxiliary.<task>.provider` writes a NEW `auxiliary:` block at the END of
  `config.yaml` (not into an existing commented one) — verify it landed as a real top-level
  block with correct indentation, and confirm `hermes config get auxiliary.<task>.provider`
  echoes the value.

### "Reset permissions" / auto-approving everything
See `references/security-privacy.md` — wipe the "Always allow" stores, don't touch yolo mode.

