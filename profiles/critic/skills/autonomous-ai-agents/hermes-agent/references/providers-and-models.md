# Providers & Model Aliases

Set via `hermes model` (picker) or `hermes setup`. 35+ provider profiles ship as
plugins under `plugins/model-providers/`; user plugins of the same name override.
Full docs: https://hermes-agent.nousresearch.com/docs/integrations/providers

### Providers

| Provider | Auth | Key env var(s) |
|----------|------|----------------|
| openrouter | API key | `OPENROUTER_API_KEY` |
| anthropic | API key | `ANTHROPIC_API_KEY` (also `CLAUDE_CODE_OAUTH_TOKEN`) |
| nous | OAuth device code | `hermes auth add nous` (or `NOUS_API_KEY`) |
| openai-codex | OAuth | `hermes auth add openai-codex` |
| qwen-oauth | OAuth | `hermes auth add qwen-oauth` |
| minimax-oauth | OAuth | `hermes auth add minimax-oauth` |
| copilot | Token | `COPILOT_GITHUB_TOKEN` / `GH_TOKEN` (Copilot device flow — `gh auth login` tokens do NOT work) |
| copilot-acp | External CLI | Copilot CLI on PATH or `COPILOT_CLI_PATH` |
| gemini | API key | `GOOGLE_API_KEY` or `GEMINI_API_KEY` |
| xai | API key | `XAI_API_KEY` (SuperGrok OAuth also supported) |
| deepseek | API key | `DEEPSEEK_API_KEY` |
| zai (GLM) | API key | `GLM_API_KEY` / `ZAI_API_KEY` |
| minimax / minimax-cn | API key | `MINIMAX_API_KEY` / `MINIMAX_CN_API_KEY` |
| kimi-coding / -cn | API key | `KIMI_API_KEY` / `KIMI_CN_API_KEY` |
| alibaba (+coding-plan) | API key | `DASHSCOPE_API_KEY` / `ALIBABA_CODING_PLAN_API_KEY` |
| xiaomi | API key | `XIAOMI_API_KEY` |
| huggingface | Token | `HF_TOKEN` |
| fireworks / novita / nvidia / deepinfra / gmi / arcee / stepfun / upstage / kilocode / ai-gateway / opencode-zen / opencode-go / ollama-cloud | API key | `<NAME>_API_KEY` |
| bedrock / vertex / azure-foundry | Cloud SDK / key | AWS SDK creds / Vertex ADC / `AZURE_FOUNDRY_API_KEY` |
| custom | Config | `model.base_url` + `model.api_key` in config.yaml |

Multiple credentials per provider pool and rotate automatically (`hermes auth`).

### Fallback providers

`hermes fallback add` opens the SAME interactive picker as `hermes model` and takes NO
flags — it needs a TTY, so a non-interactive agent cannot use it. Configure the chain by
writing `fallback_providers` directly into `config.yaml` (a list; `fallback_model` is the
legacy key — never set both, the chain merges them and can double a slot):

```yaml
fallback_providers:
  - provider: groq
    model: openai/gpt-oss-120b
  - provider: nous
    model: reflection/beam-1.0-501b-a23b:free
```

Each entry needs `provider` and `model` (an entry missing either is silently dropped);
optional `base_url`, and `api_key` / `key_env` when the endpoint carries its own credential.
Entries are tried in order on rate-limit / overload / 5xx / connection errors. Verify with
`hermes fallback list` (renders the effective chain, primary first). Delegated children and
cron jobs inherit the chain only when unpinned — a pinned owner (explicit provider/model)
borrows nothing unless it declares its own.

Pitfalls:
- **A listed entry is not a working entry.** `hermes fallback list` proves only that the
  config parsed. Prove each entry with a LIVE request before calling it configured — a valid
  key still 403s when the account is not entitled to that model, so fetch the provider's
  real list (`GET /v1/models`) and pick a model that is actually present.
- **Groq's API 403s clients with no `User-Agent` header** (urllib's default is refused;
  curl and the SDKs set one). Send `User-Agent: curl/8.0` on raw probes, or you will
  misread a header problem as a dead key.
- An expired OAuth provider (e.g. `nous` with a past `expires_at`) cannot serve as an
  fallback — re-auth it, or leave it out of the chain.
- **Nous without credits serves only `:free` models.** A linked account with an empty
  balance 404s EVERY paid model with "requires available credits" — the message names the
  model, which reads like a typo'd id but is a billing gate. Free variants carry a `:free`
  suffix in `GET /v1/models`; pick one of those. Free models can 429 ("at capacity
  upstream") intermittently, so keep a second entry rather than a single `:free` route.
- **Gemini model ids drift by account.** `gemini-2.5-flash` 404s for new keys (the error
  points at `gemini-3.8-flash`, which is a live/audio model and does NOT answer
  `generateContent` — RemoteDisconnected). Prove the id with a live `GET /v1/models` and
  one chat call before adding it; `gemini-3-flash-preview` (or `gemini-flash-latest`) is
  the safe text default. The OpenAI-compatible endpoint authenticates with
  `Authorization: Bearer <key>`; the native endpoint uses `?key=<key>`.
- **Re-auth Nous with the device flow:** `hermes auth upgrade --no-browser` prints a
  `https://portal.nousresearch.com/claim?code=...` URL and code — run it in a BACKGROUND
  PTY, hand the user the URL/code (never speak the code aloud), and poll the process until
  it prints `Signed in as <email>`. `hermes auth status nous` then reads `logged in`.

### Free-provider landscape (as of late 2026 — re-verify before relying)

A long free fallback chain is built from no-card providers first. Checked 2026-10:

- **Dead / gone free tiers:** Cerebras (no-card tier ended, card now required), GitHub Models (retired), Together AI (free tier closed), Kluster (shut down), GLHF (rebranded).
- **Best no-card, instant key:** Google AI Studio `gemini` (most generous; `gemini-3-flash-preview` — `gemini-2.5-flash` is gone for new keys), Groq `groq`, Z.ai `zai` (`glm-4.x-flash`), Cloudflare Workers AI, Cohere, SambaNova `sambanova`, DeepInfra `deepinfra`, Novita `novita`, Chutes `chutes`, Vercel AI Gateway `ai-gateway`, Ollama Cloud `ollama-cloud`.
- **Need a phone number:** NVIDIA NIM `nvidia`, Mistral `mistral`; SiliconFlow also needs real-name ID. **Need a card:** Together, xAI, Moonshot/Kimi, Hyperbolic.
- **Hugging Face** gives free accounts no inference credits (needs PRO) — deprioritize.
- Hermes knows most ids natively (`get_provider(id)` returns its base_url/env vars); a few (Cloudflare, Hyperbolic, Kluster, Together) have NO plugin id and need a `custom` entry with explicit `base_url`.
- **Always prove an entry live** (`GET /v1/models` + one chat call) before adding it to the chain — an id in `hermes fallback list` proves only that the config parsed. Send `User-Agent: curl/8.0` on raw urllib probes (Groq and others 403 a UA-less client).

### User-defined model aliases

Work with `/model <name>` in CLI and every gateway platform. Resolved by
`hermes_cli/model_switch.py::resolve_alias()`; user aliases are checked BEFORE
the built-in table, so a user `sonnet`/`grok` shadows the built-in.

```yaml
# Full form
model_aliases:
  fav:
    model: claude-sonnet-4.6
    provider: anthropic
  local-qwen:
    model: qwen3.5:397b
    provider: custom
    base_url: "https://ollama.com/v1"
  theta:
    model: theta-1
    provider: custom
    base_url: "https://theta.example.com/v1"
    key_env: THETA_API_KEY        # or: api_key: "${THETA_API_KEY}"

# Short form ("provider/model"), also via CLI:
#   hermes config set model.aliases.fav openrouter/anthropic/claude-sonnet-4.6
model:
  aliases:
    fav: openrouter/anthropic/claude-sonnet-4.6
```

`/model fav` — session-scoped; add `--global` to persist as default.

An alias with its own `base_url` authenticates with its own credential
(`api_key`, which also accepts a `"${VAR}"` reference, or `key_env`). With
neither set the key is resolved from the alias HOST, never carried over from
the provider that was active before the switch.

Built-in aliases (catalog-resolved against the active provider): `sonnet`,
`opus`, `haiku`, `claude`, `gpt5`, `gpt`, `codex`, `o3`, `o4`, `gemini`,
`deepseek`, `grok`, `llama`, `qwen`, `minimax`, `nemotron`, `kimi`, `glm`,
`step`, `mimo`, `trinity`.
