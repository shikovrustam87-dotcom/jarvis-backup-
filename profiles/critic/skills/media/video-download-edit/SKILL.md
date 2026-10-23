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

A link to a reel/short/video, a request to edit or annotate an existing video
file ("наложи текст", "обрежь", "сделай такой же", "посмотри это видео"),
or a request to generate a new video from a text description or script.

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

## Create slideshow from image sequence (Canva → video)

When the source is a set of still images (e.g. exported Canva slides), build a
video with the ffmpeg concat demuxer.

```bash
# 1. Build a list file (each image shown N seconds)
printf "file 'slide_1.png'\nduration 3\nfile 'slide_2.png'\nduration 3\n...\nfile 'slide_N.png'\n" > list.txt
# 2. Render
ffmpeg -f concat -safe 0 -i list.txt -pix_fmt yuv420p -r 30 output.mp4 -y
```

### Canva → video workflow

1. Generate a presentation design (5 slides max for speed).
2. `CREATE_DESIGN_FROM_CANDIDATE` to make it editable.
3. `GET_EXPORT_FORMATS` to confirm PNG/MP4 are supported.
4. `EXPORT_DESIGN` as PNG — download URLs expire within ~1 hour, so download
   immediately.
5. Build the concat list file and render with ffmpeg.

### User preferences for generated video

- **Faces must be blurred or hidden** in every generated scene. Never show
  identifiable human faces.
- **Narrative arc**: poor/desperate → gradual improvement → prosperity → final
  message/quote. Each scene 3 seconds.
- **Final slide**: dark background with golden text, no people.

## AI video generation (Raphael AI — free, no sign-up)

When the user wants a *real* AI-generated video (not a slideshow), use Raphael AI.
Other free options: Google Flow (50 credits/day, Veo 3.1, needs Google account),
ZSky AI (unlimited, 5s clips, small watermark), Free.ai (30k tokens/day).

### Workflow

1. Navigate to `https://raphael.app/ai-video-generator`.
2. Click the **Video** tab (button text contains "Video" and "Free").
3. Fill the textarea with placeholder `Describe the video you want to generate...`.
4. Click the **Generate** button (text contains "Generate").
5. Wait 2–3 minutes. Poll every 30–60 s; status text cycles through
   "Generating…" → "In queue…" → "Almost done…" → result ready.
6. Extract the download URL: look for `<video>` elements whose `src` contains
   `cdn.raphael.app`.
7. Download with **curl** (urllib gets 403 from the CDN):
   ```bash
   curl -L -o scene.mp4 "<URL>" -H "User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
   ```
8. Repeat for each scene, then concatenate with ffmpeg.

### Constraints

- Free tier: 480P, 4 seconds per clip (MiniMax H3 Turbo).
- Browser session may disconnect during the 2–3 min wait — if it does, navigate
  back and check if the video is ready; the result URL persists on the page.
- Each clip is independent; there is no character/style consistency across clips.
- Download URLs are temporary — fetch immediately after generation completes.

### User preferences for AI-generated video

- Same as slideshow: faces blurred or hidden, narrative arc poor→prosperity→message,
  final scene is text on dark background.
- Keep prompts descriptive but concise (model has limited token budget).

## Pitfalls

- **Pass native `C:/...` paths to ffmpeg/ffprobe, not `/c/...`.** They are native
  Windows binaries and MSYS path translation is off here; a `/c/...` input fails
  with `No such file or directory`.
- **Verify an edit landed by extracting a frame and looking at it** — do not
  report success from ffmpeg's exit code alone.
- **Check the download actually produced a file** (`ls -la`) before analysing;
  a failed yt-dlp run prints errors but exits without a video.
- **Canva export URLs expire fast** (~1 hour). Download immediately after export;
  if a URL returns 403, re-export the design to get fresh URLs.
- **Python paths on Windows**: use `C:\\Users\\...` (native), not `/c/Users/...`
  (MSYS) — the latter creates a wrong relative directory silently.
- **Repeat the last image in the concat list** so the final frame holds for the
  full duration (concat demuxer drops the last entry's duration otherwise).
- **Raphael AI CDN blocks urllib** — always use curl with a User-Agent header;
  Python's urllib.request gets HTTP 403.
- **Browser sessions disconnect during long AI generation waits** (2–3 min).
  After reconnecting, navigate back to the page and check for the result URL;
  the generated video URL persists on the page.
- **Raphael AI free tier is 480P / 4s per clip** — set expectations accordingly;
  for higher quality or longer clips, the user must sign in or upgrade.
