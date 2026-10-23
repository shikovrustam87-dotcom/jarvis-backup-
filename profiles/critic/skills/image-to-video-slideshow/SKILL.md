---
name: image-to-video-slideshow
description: "Create video slideshow from images via ffmpeg with effects."
version: 0.1.0
author: Jarvis
category: media
license: MIT
metadata:
  hermes:
    tags: [video, slideshow, ffmpeg, ken-burns, crossfade, image-to-video]
    related_skills: [video-download-edit]
---

# Image-to-Video Slideshow with Effects

Create a polished video slideshow from static images using ffmpeg. Adds Ken Burns (slow zoom/pan) and crossfade transitions between slides. Reliable fallback when real AI video generation is unavailable.

## When to Use

- User wants a video but real AI video generation (Raphael AI, Google Flow, etc.) is unavailable, unreliable, or too slow.
- User has images (from Canva, generated, or provided) and wants them turned into a video.
- User accepts a slideshow-style video with effects as a compromise.

## Procedure

### 1. Prepare images

Ensure all slide images are downloaded to a working directory. Use consistent naming (e.g., `slide1.png`, `slide2.png`, ...). PNG format preferred for quality.

### 2. Create individual slide videos with Ken Burns effect

For each image, create a short video clip with slow zoom:

```bash
ffmpeg -loop 1 -i slideN.png \
  -vf "zoompan=z='min(zoom+0.002,1.3)':d=90:x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s=1280x720" \
  -t 3 -pix_fmt yuv420p -r 30 slideN_kb.mp4 -y
```

Parameters:
- `zoom+0.002` — zoom speed (increase for faster zoom)
- `1.3` — max zoom factor (1.3 = 30% zoom)
- `d=90` — duration in frames (90 frames at 30fps = 3 seconds)
- `s=1280x720` — output resolution
- `-t 3` — clip duration in seconds

### 3. Concatenate with crossfade transitions

Use ffmpeg's `xfade` filter to blend slides:

```bash
ffmpeg -i slide1_kb.mp4 -i slide2_kb.mp4 -i slide3_kb.mp4 -i slide4_kb.mp4 -i slide5_kb.mp4 \
  -filter_complex "
  [0][1]xfade=transition=fade:duration=0.5:offset=2.5[v01];
  [v01][2]xfade=transition=fade:duration=0.5:offset=5.0[v012];
  [v012][3]xfade=transition=fade:duration=0.5:offset=7.5[v0123];
  [v0123][4]xfade=transition=fade:duration=0.5:offset=10.0[vfinal]
  " \
  -map "[vfinal]" -pix_fmt yuv420p -r 30 output.mp4 -y
```

Offset calculation: for N slides of D seconds each with T-second transitions:
- Transition k offset: k×D - k×T
- Total duration: N×D - (N-1)×T

### 4. Verify output

```bash
ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 output.mp4
```

## Pitfalls

- **Browser session unreliability for long tasks**: When using browser-based image generation (Canva, etc.), sessions can drop during long waits. Download images immediately after generation; do not leave them in the browser.
- **URL expiration**: Canva export URLs expire quickly (minutes). Download all images in a single batch immediately after export.
- **Resolution consistency**: All input images should have the same aspect ratio. Canva presentations default to 16:9; adjust `s=` in zoompan to match.
- **User preference**: The user prefers real AI video over slideshows. Always attempt real video generation first if the user requests it, but offer this slideshow approach as a reliable fallback when real generation fails or is too slow.

## References

- ffmpeg zoompan filter: `z` = zoom expression, `d` = duration in frames, `x`/`y` = pan position, `s` = output size.
- ffmpeg xfade filter: `transition` = fade/wipeleft/wiperight/etc., `duration` = transition length, `offset` = when transition starts.
