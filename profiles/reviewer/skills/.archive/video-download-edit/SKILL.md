---
name: video-download-edit
description: "Download reels/shorts and edit video with yt-dlp + ffmpeg."
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [video, yt-dlp, ffmpeg, instagram, reels, editing, frames, drawtext]
    related_skills: [youtube-content, jarvis-hud]
---

# Download and edit social video

Fetch video from a link (Instagram reels, YouTube, TikTok, X) and edit it — cut,
overlay text, add music, or extract frames so the agent can "watch" it.

## When to Use

A link to a reel/short/video, or a request to edit or annotate an existing video
file ("наложи текст", "обрежь", "сделай такой же", "посмотри это видео").

## Tools (resolve by glob — version dirs are partly masked in output)

```bash
PY=$(ls -d "$LOCALAPPDATA"/hermes/tools/python-*/python.exe 2>/dev/null | head -1)
FF=$(ls -d "$LOCALAPPDATA"/hermes/tools/ffmpeg-*/bin/ffmpeg.exe 2>/dev/null | head -1)
FP=$(ls -d "$LOCALAPPDATA"/hermes/tools/ffmpeg-*/bin/ffprobe.exe 2>/dev/null | head -1)
```

- **yt-dlp** installs into Hermes's managed Python; its `Scripts` dir is NOT on
  PATH, so invoke it as a module: `"$PY" -m yt_dlp ...`.
- Install it if missing: `"$PY" -m pip install --upgrade yt-dlp`.

## Download

```bash
"$PY" -m yt_dlp --no-warnings -f "mp4/best" -o "рилс_%(id)s.%(ext)s" "<URL>"
```

Public Instagram reels download without cookies. Private/age-gated posts will ask
for cookies — export them from the browser and pass `--cookies`.

## Extract frames so the agent can see the video

An agent cannot watch a video directly; convert it to stills and read them with
`vision_analyze`.

```bash
"$FP" -v error -show_entries format=duration -show_entries stream=width,height -of default=noprint_wrappers=1 "$VID"
"$FF" -hide_banner -loglevel error -i "$VID" -vf "fps=1,scale=960:-1" "$OUT/к_%03d.png"
```

`fps=1` = one frame per second; use `fps=2` for a short clip. Probe duration first
so you know how many frames to expect.

## Overlay text (Cyrillic-safe)

```bash
"$FF" -hide_banner -loglevel error -y -i in.mp4 \
  -vf "scale=720:-2,drawtext=fontfile='C\:/Windows/Fonts/arialbd.ttf':text='ТЕКСТ':fontcolor=white:fontsize=48:x=(w-text_w)/2:y=h-th-40:box=1:boxcolor=black@0.6:boxborderw=12" \
  -c:a copy out.mp4
```

Note the escaped drive colon in `fontfile` (`C\:`) — ffmpeg's filter parser
requires it.

## Pitfalls

- **Pass native `C:/...` paths to ffmpeg/ffprobe, not `/c/...`.** They are native
  Windows binaries and MSYS path translation is off here; a `/c/...` input fails
  with `No such file or directory`.
- **Verify an edit landed by extracting a frame and looking at it** — do not
  report success from ffmpeg's exit code alone.
- **Check the download actually produced a file** (`ls -la`) before analysing;
  a failed yt-dlp run prints errors but exits without a video.
