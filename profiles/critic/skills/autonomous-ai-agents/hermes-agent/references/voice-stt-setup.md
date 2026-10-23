# Voice: STT / TTS Setup, Verification, and Diagnosis

Setting up speech in either direction touches a venv, a config key, a model download,
and the audio path. "I installed it" and "it works" are different claims — the
procedures below end in a probe that decides the question.

Applies to voice messages auto-transcribed by the gateway, to a local STT request,
and to "the user says they cannot hear me" reports on any surface.

## 1. Install the local extra (free, offline, no API key)

faster-whisper is a *venv extra*, not a pip install into whatever python is on PATH.
Install it into Hermes' own tools interpreter, from the Hermes source directory:

```bash
cd "$HERMES_HOME/hermes-agent"                    # or the git-install dir
PY=$(ls -d "$HERMES_HOME/tools/python-"*/ | head -1)   # resolve, never hardcode
"$PY/python.exe" -c "import pm; pm.sync_venv(['stt-whisper'], explicit=True)"
```

- **Never hardcode the tools-interpreter version string.** Destinations look like
  `tools/python-<version>+<build>-win32-x64/python.exe`, and the build suffix can come
  back from tool output masked or normalised (`202****0901`). A copied literal then fails
  with `No such file or directory` while the directory plainly exists. Glob `python-*`,
  or list `$HERMES_HOME/tools/`, and build the path from the result.
- The extra name is `stt-whisper` (aliases: `voice`). Hook key `faster_whisper`;
  `hermes tools post-setup` only accepts the narrower fixed key list and does not
  cover every python extra, so drive `pm.sync_venv` directly.
- Confirm the *installed* interpreter can import it — the parent process's PATH proves nothing:

```bash
"$PY/python.exe" -c "import faster_whisper; print(faster_whisper.__version__)"
```

## 2. Point the config at it

```bash
hermes config set stt.enabled true
hermes config set stt.local.model small     # see model note below
hermes config set stt.language ru           # "" = auto-detect
```

- Setting `stt.provider local` prints
  `'stt.provider' is not a recognized config key — it was saved anyway`. **That warning is
  benign here**: `local` is the first entry in auto-detect priority, so local is selected
  whenever faster-whisper is importable. Do not chase the warning or pick a cloud provider
  to silence it. The value is still written and is honoured if present.
- Prefer leaving `provider` unset outright unless the user wants a *specific* provider:
  an explicit provider suppresses the silent cloud fallback, so a typo turns transcription
  off instead of degrading to Groq.

## 3. Model choice — this is where quality is won or lost

| Model | Verdict |
|---|---|
| `tiny`, `base` | **Unusable for real speech** — return confident, fluent-looking nonsense. `base` is Hermes' config default; do not leave it on a machine the user will actually dictate to. |
| `small` | Practical floor. Correct output on ordinary speech at CPU int8 speeds. |
| `medium`, `large-v3` | Better quality, but after the CPU measurements below treat every large model as a latency risk until you benchmark it on the actual host. |
| `turbo` | Highest accuracy of the family, **slowest on CPU** — 3-6x `small` on a 16-thread box. A quality upgrade only when the host is fast enough; never the default choice for interactive dictation. |

**Measured on CPU int8, Russian, two synthetic phrases:** `base` garbled real-voice-style audio
(`Hilo, Tissuesa and Tests of Lockers Peach...`); `small`, `medium` and `turbo` were all
accurate. When reporting recall, normalise `ё`→`е` first — `отчёт` vs `отчет` is a scorer
artifact, not a transcription error, and it silently costs a point.

**Pin the device in config, or pay for a failed CUDA attempt on every cold load.**
`device="auto"` picks CUDA whenever the ctranslate2 wheel ships CUDA libs, even on a host with
no NVIDIA runtime. The load then fails (`Library cublas64_12.dll is not found`), the cached
model is evicted, and it reloads on CPU — pure added latency, repeated each time the model is
unloaded and reloaded:

```bash
hermes config set stt.local.device cpu
hermes config set stt.local.compute_type int8
```

`hermes config set` prints "not a recognized config key" for both — benign here, the loader
reads them (`transcription_tools.py`: `local_cfg.get("device", "auto")`). Confirm the fix by
re-running the probe: the CUDA-fallback warning line must be gone.
faster-whisper downloads the model on first use — give the first transcription a long
(several-minute) timeout and expect it to be slow, then fast.

**On CPU, `turbo` is a LATENCY trap — benchmark before recommending it.** Hermes hardcodes
`beam_size: 5` in `build_local_transcribe_kwargs`, and this machine (16 logical cores,
Windows, int8) measured per 8 s utterance: `small` 3.1 s, `small` beam=5 3.8 s, `turbo`
12-20 s, `base` 1.6 s — precisely why dictation felt like half a minute. Two thread traps:
- 0 unused threads (measured 4) is fastest: `cpu_threads=8` or `16` was 2-6x SLOWER than 4.
- `cpu_threads=16` (or any value near core count) can produce a pathological stall.
Do not pass `cpu_threads` from config (it is not read) — leave the library default and
lower `stt.local.model` instead. Run `scripts/bench_stt_models.py <sample.wav> small turbo --lang <code>`
to measure it on the current host instead of reasoning about it; on a synthetic clip, also
confirm the winner on real dictation. Diagnose latency from `agent.log`'s legacy phrase
`Transcribed <file> via local whisper (<model>, lang=.., N s audio)` — its timestamp minus
the preceding `faster_whisper: Processing audio` line is the real transcribe cost per turn.
Model choice is per-machine: rerun the benchmark after any CPU/host change.

## 4. Prove it: round-trip probe

Installing the extra says nothing about whether transcription is correct. Synthesize a
known phrase, transcribe it, and score word recall — run `scripts/verify_local_stt.py`
(see that file's docstring for usage), or inline the same shape:

1. Synthesize ground truth (Windows: PowerShell `System.Speech.Synthesis.SpeechSynthesizer`;
   macOS `say`; Linux `espeak-ng`).
2. `WhisperModel(model, device="cpu", compute_type="int8").transcribe(wav, language=..., beam_size=5, temperature=0.0)`.
3. Normalise both strings to lowercase word lists and compute recall of the expected words.
   **PASS at ≥80% recall.**

Synthesized speech is a smoke test, not a fidelity claim: it proves the chain is wired and
that the model size is adequate, not that the user's own voice will score the same. Say so
when reporting, and offer `medium` or a free Groq key as the upgrade path.

**Run the probe in both the user's language and English.** A model that reads a language it
was trained on heavily can still mangle the user's own — the language the user will actually
speak is the one that must pass. Note also that if the probe passes but live dictation fails,
suspect the synthesized voice's language, not the models.

## 5. Confirm Hermes itself resolves the provider

Read the config through Hermes' own loader and ask its resolver — do not eyeball the YAML:

```python
from tools.transcription_tools import _get_provider, _detect_local_backend, _HAS_FASTER_WHISPER
from tools.transcription_local import build_local_transcribe_kwargs
from hermes_cli.config import load_config      # NOT `config` — the module is hermes_cli.config

print(_HAS_FASTER_WHISPER, _detect_local_backend())
stt = load_config().get("stt", {})
print(_get_provider(stt), build_local_transcribe_kwargs(stt))
```

Expected: `True local` / `local` / a kwargs dict carrying `language` and `vad_filter`.

**Restart Hermes (gateway / desktop) after installing the extra.** Provider availability is
resolved from a flag computed at import time, so a long-running process may not see the new
dependency.

## 6. Switching to a cloud STT provider (Groq et al.)

**Add the key BEFORE switching the provider.** Set `stt.provider` to a cloud provider
with no usable key and `_get_provider` resolves to `none` — an explicit provider
suppresses the silent fallback, so transcription stops working *entirely* rather than
degrading to local or the next provider in line. Sequence it: key → verify → then flip
`stt.provider`, and re-run the round-trip probe (§4) afterwards.

**Never accept a provider secret in chat — not even after the user offers it twice and picks
"paste it here" in a confirmation prompt.** It persists in session history and logs forever;
decline, explain in one sentence, and give a route that never touches the chat.

**Stage the file yourself so the user's only action is paste + save.** Handing over a shell
command to run is the failing step: a command read aloud, retyped, or voice-dictated loses its
quotes, silently writes nothing, and the user still reports success ("готово"). Do this instead:

1. Back up the file first — you are editing the user's only copy of every other secret:
   `cp .env ".env.backup-$(date +%Y%m%d-%H%M%S)"`.
2. Append the key line yourself, empty, under a marker comment:
   `printf '\n# --- GROQ STT ---\n# Paste the key right after "=" and save:\nGROQ_API_KEY=\n' >> .env`.
   Also set the non-secret half up front (`hermes config set stt.groq.model whisper-large-v3-turbo`).
3. Open that exact path in the user's editor for them and leave it there:
   `notepad.exe "C:\Users\<user>\AppData\Local\hermes\.env"` — terminal needs
   `background=true` (a foreground `&` is refused), and the window may open behind the app, so
   tell them to look in the taskbar. Instructions become three keystrokes: Ctrl+End (or "cursor is
   already at the end"), Ctrl+V, Ctrl+S.
4. Only then offer the alternative one-liner (below) as a fallback — never as the first route.

A user's "готово" after this is still not evidence; re-read the file before flipping the provider.

**Append BEFORE opening the editor, never after — and re-verify after every save.** A GUI
editor holds the snapshot it loaded and rewrites the whole file on save, silently discarding
anything appended since it opened. Order: append → verify → open the editor at the last line →
wait for their save → re-read. A write you make while their window is open is lost at their
next Ctrl+S, and the file then looks as if the user "saved nothing" — which is exactly the
wrong thing to tell them.

**Verify the VALUE, not the line.** A placeholder `GROQ_API_KEY=` that you appended yourself
makes a `^GROQ_API_KEY=` grep pass while the secret is still absent. Require
`^GROQ_API_KEY=\s*\S` and sanity-check shape (Groq keys are long and start `gsk_`). Report
masked: length + first four characters + a boolean, never the value.

**Windows `.env` is CRLF.** Append `\r\n`, not `\n` (`printf '\r\nGROQ_API_KEY=\r\n'`), or the
new line merges into the previous one and mixed endings accumulate. Confirm with
`tail -3 .env | cat -A` — every line must end `^M$`.

**Do not launch a second editor blindly.** `notepad.exe <path>` started from the terminal opens
*behind* the desktop app, and a repeat call just stacks another invisible window while the user
reports "you didn't open it". Before launching, count the windows and find the real one:

```bash
tasklist /FI "IMAGENAME eq notepad.exe"                       # single-slash flags
powershell -NoProfile -Command "Get-Process notepad | Select-Object Id,MainWindowTitle"
```

- **Single-slash flags.** Under MSYS bash `tasklist //FI` and `taskkill //F` fail with
  `неверный параметр '//F'` — the double slash is not a translation escape here; use
  `taskkill /F /IM notepad.exe` and `tasklist /FI "..."` verbatim.
- **An empty `MainWindowTitle` means the window is not visible** (hidden/session-attached child).
  The process with `*.env - Блокнот` in that column is the one the user can actually see. Kill
  the strays with `taskkill /F /IM notepad.exe` before opening a clean single instance.

**After ANY user-side attempt, diff against the backup — a failed edit can corrupt, not just
omit.** Check `diff .env.backup-* .env`: a botched paste/`Add-Content` can land stray text
mid-file (a bare filename path in place of a line) while the tail looks untouched, so a
looks-empty last line is not the whole story. Restore from the backup you took, then re-stage
the line. Never report "the file is fine" from a tail-only read.

**Give the non-technical / voice-dictating user a mouse-only route.** Hotkeys are the failing
step for someone reading instructions aloud: "Ctrl+V" gets heard and typed as "Ctrl plus N",
which in Notepad means **New file** (it does not delete anything — say so at once, or a
frightened user stops touching the file). Ship both routes every time:
1. Keyboard: `Ctrl+End`, then `End`, then `Ctrl+V`, then `Ctrl+S`.
2. Mouse: scroll the bar to the bottom → click right after `=` → right-click → «Вставить» →
   menu «Файл» → «Сохранить».
Never phrase a key as "Ctrl plus N", and never ask them to retype a shell command.

**`hermes auth add groq` is rejected — groq is not a model provider in Hermes.**
`PROVIDER_REGISTRY` (`hermes_cli/auth.py`, `_REGISTRY_ROWS`) lists OpenAI/xAI/Gemini/DeepSeek
and friends; Groq appears only as an *STT* provider, so `_is_known_provider` fails with
`Unknown provider 'groq' … Run hermes auth to see the provider list`. Do not send the user to
`hermes auth`, `hermes auth status groq`, or `hermes model` for STT — they all answer "not a
provider" and read as the same failure repeating. The key belongs in the environment instead:

```powershell
# LAST resort, only if the user insists on running it themselves. Never the first route.
Add-Content -Path "$env:LOCALAPPDATA\hermes\.env" -Value "GROQ_API_KEY=<key>"
hermes config set stt.groq.model whisper-large-v3-turbo
```

The compact `"`nGROQ_API_KEY=<key>"` form is the one that arrives mangled: it needs a leading
escape *inside* a quoted value that is itself inside a quoted command, so a copy from chat, a
retype, or a voice-dictated command loses a quote (or the whole newline escape) and the write
silently becomes empty. Use `-Path`/`-Value` named parameters and no escape sequences, and
re-read the file afterwards either way.

`_has_groq_key` resolves `GROQ_API_KEY` (`.env` → env scope → pool), and `_HAS_OPENAI` must
be true — the Groq path rides the OpenAI SDK, so confirm `import openai` in the tools
interpreter before promising it works. `hermes auth status groq` printing `logged out` is
correct and permanent for groq; it is not evidence of a broken setup.

**Empty verdict on "did the key land":** check the resolver, not the file —
`from tools.transcription_tools import _get_provider, _load_stt_config;
print(_get_provider(_load_stt_config()))` must return `groq`, not `none`/`local`.

**A Groq reachability probe must send a `User-Agent`, or it gets a false 403.**
`urllib.request.urlopen` with only an `Authorization` header returns
`HTTPError: HTTP Error 403: Forbidden` from `https://api.groq.com/openai/v1/models` while
`curl` on the same key returns 200 — Groq rejects the bare stdlib request. Add
`"User-Agent": "Mozilla/5.0 ..."` to the request headers and the probe returns 200. Do not
conclude from a 403 that the key is bad; curl the endpoint first to separate a key problem
from a header problem.

When reading `.env` directly, count *uncommented* `^GROQ_API_KEY=` lines rather than
searching for the substring: the shipped template already carries a commented
`# GROQ_API_KEY=***` sample, so a substring hit reports success while nothing was added —
and a user typing a long quoted `Add-Content` command by ear routinely writes nothing at all.
Do not believe "готово" without that check.

When `hermes` is not on PATH, drive the same CLI through the managed interpreter from the
`hermes-agent` directory:
`"$PY/python.exe" -c "import sys; sys.argv=['hermes','config','set','stt.local.model','small']; from hermes_cli.main import main; main()"`.
`hermes config set` writes the value even for keys it labels "not a recognized config key" —
confirm with a `grep` of the written YAML rather than trusting the message.

**Confirm the key landed INSIDE its section, not just that it is present.** For a nested
key that does not already exist in the file, `hermes config set stt.provider groq` appends
the line at the wrong indent — it lands *between* top-level sections (e.g. after the
`stt:` block's comments, just above the next `code_execution:` heading) instead of inside
`stt:`. The key then exists, `hermes config get` echoes it back, and it does nothing — the
provider never changes. The same misplacement happened with `plugins.enabled`. So after any
nested `config set`, read the surrounding lines and verify the indentation places the key in
its parent block; if it is adrift, fix it with a line-aware rewrite (read `config.yaml` as a
list of lines, drop the stray lines, re-insert them right after the `stt:` line, write back
with `newline=""`) rather than a regex over the whole text — the file is CRLF and a naive
multi-line pattern silently fails to match. Confirm afterwards that the unrelated key you
did not mean to touch (e.g. `model.default`) is still intact.

The built-in free-tier choice is Groq with `whisper-large-v3-turbo` (`stt.groq.model`).
Cloud providers also gain client-side silence trimming (`stt.cloud_trim_silence`), which
matters for per-minute billing.

### Cloud-with-local-fallback: an external guard, not a config option

Hermes has no automatic provider fallback — an explicit `stt.provider` is honoured with no
silent degradation, so a cloud provider that goes unreachable takes transcription down
completely instead of dropping to local whisper. When the user wants "Groq, but keep working
when the network drops", the working shape is a small external watcher that flips
`stt.provider` based on connectivity:

1. Every ~30 s, probe the cloud endpoint (remember the `User-Agent` above).
2. Reachable → `hermes config set stt.provider groq`; unreachable → `... stt.provider local`.
3. Only write when the desired value differs from the current one, so you are not rewriting
   `config.yaml` every tick.

Read the current value by scanning `config.yaml` for the `provider:` line inside the `stt:`
block (stop at the first non-indented line), and drive the switch through the `hermes` CLI
(`hermes.exe` under `hermes-agent/.hermes/bin/`) so the write goes through Hermes' own
writer. Ship it as a `.bat` launcher plus a Startup-folder shortcut, like the other
background helpers.

Honest status note: the probe and the provider-write were each verified by direct call
(probe returns 200 with the header; the CLI write moves `stt.provider`), but the *automatic*
switch was never exercised against a real outage — say so when reporting, and do not claim
seamless failover you have not watched happen.

## 7. TTS: separate synthesis from playback

"I cannot hear you" is an *audio-path* report, not automatically an engine fault. Split the
layers before changing anything.

- **`voice.auto_tts` is a gateway/messaging-platform setting** (`gateway/platforms/base.py`),
  and it fires on *voice input*. It is **not** the desktop app's auto-speak toggle — toggling
  it will not fix a desktop playback problem. Do not confuse the two.
- **Prove synthesis independently, then let the user play the artifact.** Generate a known
  phrase and deliver it as a real audio file (`MEDIA:`) so the user plays it with their own
  player. Audible → synthesis is fine and the fault is in the app's player, its volume, or
  the output device. Silent → the problem is system output. This one step halves the search
  space and gives the user something concrete to react to.
- **edge-tts (the default provider, no API key) can fail transiently** with
  `NoAudioReceived` from `Communicate.save()`. That is a Microsoft-side token/cold-start
  hiccup, not a broken install — **retry once before declaring it broken**, and check
  `await edge_tts.list_voices()` returns a populated list to separate "voice id wrong"
  from "synthesis failing".
- **Validate the artifact before blaming playback**: a multi-KB file with a valid MP3/ID3
  header was synthesized correctly. Size of zero or a missing header points back at the engine.
- The configured voice id must exist for the locale. `hermes config set tts.edge.voice ...`
  with a hallucinated name is a silent-looking failure; list voices to confirm the id first.

## Pitfalls

- **`audioop` is gone (Python 3.13+).** Reading WAV sample levels to check an audio file is
  not silent must use `array` + `wave`, not `audioop.rms` / `audioop.max`.
- **Do not diagnose from the transcript alone.** Garbled output has two candidate causes —
  too-weak model, or bad input audio. Check the file first (channels, sample width, rate,
  peak/RMS) before spending minutes on a larger model; studio-quality audio with a bad
  transcript means model size, and near-zero peak means the audio.
- **`hermes doctor` may print nothing about voice even when STT is healthy.** Absence of an
  STT line is not evidence of misconfiguration; use the resolver check in step 5.
- **Long-running verification belongs in a tracked background process.** Model-sync and
  first-model-download runs exceed a normal foreground timeout; start them backgrounded and
  poll rather than re-issuing the command after an interrupt.
