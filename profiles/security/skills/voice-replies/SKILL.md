---
name: voice-replies
description: "Voice replies: 1-2 sentences spoken; detail goes in text."
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [voice, tts, telegram, style, persona]
    related_skills: [hermes-agent]
---

# Voice Replies

How to answer with voice for this user — applies to every `text_to_speech` call and every
reply delivered as a voice bubble on a messaging platform.

## When to Use

- Any reply you intend to deliver as a voice message / voice bubble.
- Any `text_to_speech` call.
- Any request like "say it", "voice it", "answer by voice", or a follow-up after the user
  asked for voice replies to be shorter.

Not for: choosing or installing a TTS provider/voice (that is Hermes config — see Related).

## The spoken/text split (standing user rule)

- **Spoken part: 1–2 sentences, essence only.** No preamble, no recap, no sign-off padding.
- **Never read aloud:** links/URLs, hashtags, emoji, symbols, and long lists. A voice bubble
  that recites a URL or a bullet list is a failure, not a stylistic choice.
- **Everything else goes in the accompanying TEXT message** — links, tables, lists,
  step-by-step instructions, code. The voice is the summary; the text is the detail. Send
  both in the same reply.
- Reply in the user's language (Russian).

This is a standing preference the user asked to be remembered permanently, not a per-request
choice. Apply it from the first reply; do not wait to be reminded.

## Producing the voice

1. Call `text_to_speech` with the short spoken sentence(s).
2. Copy the returned `media_tag` into the reply **verbatim** — it carries `[[audio_as_voice]]`
   and the `MEDIA:<path>` line, and that tag is what makes the platform render a native voice
   bubble rather than a file attachment.
3. Put the detailed text alongside it.

## Pitfall: never hand-write the MEDIA path

The `MEDIA:` path must come from an actual `text_to_speech` result. A path you composed
yourself (a guessed filename, a stale path reused from an earlier turn) does not exist on
disk — the delivery fails silently and the user hears nothing while you believe you replied.
Always call the tool first, then paste the `media_tag` it returned.

## Pitfall: synthesis failed — disclose, don't go silent

This user runs with auto-TTS on and expects every reply to be voiced. When
`text_to_speech` returns an error, a bare text reply reads to them as "the assistant lost
its voice" and they will ask. So:

- **Say it in the text reply.** Put one plain sentence at the top — that the voice failed
  and the cause or fix if you have it — then carry on with the text. Never quietly drop the
  spoken half and act as if the reply were normal.
- **Do not retry the same call more than once.** A second identical failure from the same
  provider is an outage or a stale pin, not a transient blip; retrying just burns seconds.
  Report it and move on.
- Repeating the voice would need the provider fixed (see Related) — that is config, not
  something a retry loop solves.

## Related

Voice/STT/TTS provider and voice selection are Hermes config (`tts.*`, `stt.*`) — load the
`hermes-agent` skill and read its configuration reference. Changing the voice is not part of
producing a reply.
