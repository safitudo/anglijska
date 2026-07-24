# Lyric-video pipeline (TikTok 1080×1920)

Makes HQ vertical lyric videos from a Suno MP3: EN line + UA translation cards,
animated gradient background, waveform, title.

Pipeline per new song:
1. Transcribe the MP3 with Deepgram (`nova-3`, key in vault `.secrets/api-keys.txt`)
   to get word timestamps of the sung vocals.
2. Build the line-timing table (EN, UA, start, end) — anchor lines on transcribed
   words, interpolate lines the model missed (see `line_timings.py` for the
   steps/tomahawk tables built 2026-07-24).
3. `render_lyric_video.py` renders line cards with Pillow (Arial Bold EN 62px,
   Arial UA 44px, italic ADLIB style for spoken lines) and composites with ffmpeg:
   gradients background + showwaves + timed overlays with alpha fades,
   libx264 crf 17, AAC 320k.

NOTE: homebrew ffmpeg on this Mac has NO libass/freetype (no `subtitles`/`drawtext`
filters) — that's why text is pre-rendered to PNGs with Pillow.
Scripts still reference the session scratchpad dir — adjust paths when reusing.
