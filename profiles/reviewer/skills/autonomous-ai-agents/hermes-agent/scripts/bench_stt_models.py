"""Benchmark faster-whisper models on THIS machine, so local STT model choice is measured,
not assumed.

Why: latency complaints on voice input are almost always local decode cost, not the LLM.
Hermes hardcodes beam_size=5 in build_local_transcribe_kwargs, so benchmark with that value
and with the same audio the user actually dictates in (their language).

Usage (from the hermes-agent dir, using the managed interpreter):

    PY=$(ls -d "$HERMES_HOME/tools/python-"*/ | head -1)
    "$PY/python.exe" scripts/bench_stt_models.py stt_sample.wav small turbo base
    "$PY/python.exe" scripts/bench_stt_models.py stt_sample.wav --lang ru --beam 5

Read the output as cost per utterance:
  * load  = paid once per process (and again after an idle unload)
  * tr    = the per-turn delay the user feels, on top of mic capture and the LLM call
Pick the smallest model still accurate in the user's language; report both numbers.

Threads: cpu_threads is NOT read from config and is deliberately left at the library
default. Measured on a 16-thread Windows box, cpu_threads=4 beat 8 and 16 by 2-6x, and a
value near the core count produced pathological stalls. Only pass --threads to confirm that.
"""

import argparse
import sys
import time


def pick_sample(path: str) -> str:
    return path


def bench(models, audio, lang, beam, threads):
    from faster_whisper import WhisperModel  # imported late so --help works without it

    rows = []
    for name in models:
        t0 = time.time()
        kwargs = {"device": "cpu", "compute_type": "int8"}
        if threads:
            kwargs["cpu_threads"] = threads
        model = WhisperModel(name, **kwargs)
        load = time.time() - t0

        t1 = time.time()
        segs = list(model.transcribe(
            audio, language=lang or None, vad_filter=True,
            beam_size=beam, condition_on_previous_text=False)[0])
        tr = time.time() - t1
        text = " ".join(s.text.strip() for s in segs).strip()
        rows.append((name, load, tr, text))
        print(f"{name:8} load={load:5.1f}s  transcribe={tr:6.2f}s  | {text[:70]}")
        del model

    if rows:
        best = min(rows, key=lambda r: r[2])
        print(f"\nfastest: {best[0]} at {best[2]:.2f}s/utterance")
        print("confirm the winner on real dictation before making it default — "
              "speed on a synthetic clip is not accuracy on the user's voice.")
    return 0


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("audio", help="wav/webm of real speech in the user's language")
    ap.add_argument("models", nargs="*", default=["small", "turbo"],
                    help="model names to compare (default: small turbo)")
    ap.add_argument("--lang", default="", help="language code, e.g. ru")
    ap.add_argument("--beam", type=int, default=5, help="beam size (Hermes uses 5)")
    ap.add_argument("--threads", type=int, default=0, help="cpu_threads override (0 = library default)")
    args = ap.parse_args(argv)
    return bench(args.models, pick_sample(args.audio), args.lang, args.beam, args.threads)


if __name__ == "__main__":
    sys.exit(main())
