#!/usr/bin/env python3
"""Round-trip local-STT probe: synthesize a known phrase, transcribe it, score word recall.

Run with Hermes' tools interpreter (the one that has faster-whisper installed), from the
Hermes source directory so `faster_whisper` resolves:

    PY=$(ls -d "$HERMES_HOME/tools/python-"*/ | head -1)
    cd "$HERMES_HOME/hermes-agent"
    "$PY/python.exe" path/to/scripts/verify_local_stt.py --lang ru

Exit code 0 = PASS (>=80% word recall), 1 = FAIL, 2 = could not synthesize reference audio.

Why a round trip: a successful `import faster_whisper` only proves the package is present.
Synthesized ground truth is the cheapest way to tell "model too weak" apart from "audio bad"
and to confirm the configured model size is adequate before blaming the user's microphone.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
import time

PHRASES = {
    "en": "Hello, this is a test of local speech recognition.",
    "ru": "Привет, это проверка распознавания русской речи.",
}

# Windows SAPI voice per language. A missing voice falls back to the system default, which
# may be the wrong language and makes the probe fail for uninteresting reasons.
SAPI_VOICES = {"ru": "Microsoft Irina Desktop", "en": "Microsoft Zira Desktop"}


def synthesize(text: str, lang: str, out: str) -> bool:
    """Write `text` spoken aloud to `out` (wav). Returns False if no TTS backend found."""
    if sys.platform == "win32":
        voice = SAPI_VOICES.get(lang, "")
        select = 'try { $s.SelectVoice("%s") } catch { }' % voice if voice else ""
        ps = f'''
Add-Type -AssemblyName System.Speech
$s = New-Object System.Speech.Synthesis.SpeechSynthesizer
{select}
$s.SetOutputToWaveFile("{out}")
$s.Speak("{text}")
$s.Dispose()
'''
        r = subprocess.run(["powershell", "-NoProfile", "-Command", ps],
                           capture_output=True, text=True, timeout=180)
        return r.returncode == 0 and os.path.exists(out)

    if sys.platform == "darwin" and shutil.which("say"):
        r = subprocess.run(["say", "-o", out, "--data-format=LEI16@16000", text],
                           capture_output=True, timeout=180)
        return r.returncode == 0 and os.path.exists(out)

    for cmd in ("espeak-ng", "espeak"):
        if shutil.which(cmd):
            r = subprocess.run([cmd, "-v", lang, "-w", out, text],
                               capture_output=True, timeout=180)
            return r.returncode == 0 and os.path.exists(out)

    print("No TTS backend available (need PowerShell, say, or espeak-ng).", file=sys.stderr)
    return False


def describe_audio(path: str) -> None:
    """Print channels/rate/duration and peak/RMS so bad audio is ruled in or out early.

    Uses `wave` + `array`: `audioop` was removed in Python 3.13.
    """
    import array
    import wave

    with wave.open(path, "rb") as w:
        ch, sw, rate, nf = w.getnchannels(), w.getsampwidth(), w.getframerate(), w.getnframes()
        data = w.readframes(nf)
    print(f"audio: {ch}ch {sw*8}bit {rate}Hz {nf/rate:.2f}s")
    if sw == 2 and data:
        a = array.array("h")
        a.frombytes(data)
        if ch == 2:
            a = a[::2]
        peak = max(abs(x) for x in a)
        rms = (sum(x * x for x in a) / len(a)) ** 0.5
        flag = "  <-- near silence!" if peak < 500 else ""
        print(f"audio level: peak={peak} rms={rms:.1f}{flag}")


def words(s: str) -> list:
    return re.sub(r"[^\w\s]", "", s.lower(), flags=re.UNICODE).split()


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--lang", default="ru", help="language code; picks the default phrase")
    ap.add_argument("--text", help="override the ground-truth phrase")
    ap.add_argument("--model", default="small", help="faster-whisper size (small is the floor)")
    ap.add_argument("--min-recall", type=float, default=0.8)
    args = ap.parse_args()

    text = args.text or PHRASES.get(args.lang, PHRASES["en"])
    wav = os.path.join(tempfile.gettempdir(), f"stt_probe_{args.lang}.wav")

    print(f"phrase : {text}")
    if not synthesize(text, args.lang, wav):
        return 2
    describe_audio(wav)

    from faster_whisper import WhisperModel

    t0 = time.time()
    model = WhisperModel(args.model, device="cpu", compute_type="int8")
    print(f"model  : {args.model} loaded in {time.time()-t0:.1f}s (downloads on first use)")

    t0 = time.time()
    segments, _info = model.transcribe(wav, language=args.lang, beam_size=5, temperature=0.0)
    got = " ".join(s.text.strip() for s in segments).strip()
    print(f"elapsed: {time.time()-t0:.1f}s")
    print(f"result : {got}")

    exp, act = words(text), words(got)
    recall = sum(1 for w in exp if w in act)
    ratio = recall / len(exp) if exp else 0.0
    print(f"recall : {recall}/{len(exp)} = {ratio:.0%}  (threshold {args.min_recall:.0%})")
    ok = ratio >= args.min_recall
    print("VERDICT:", "PASS" if ok else "FAIL")
    if not ok:
        print("  -> try --model medium; if the audio level above is near zero, the input is the problem")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
