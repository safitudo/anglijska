# -*- coding: utf-8 -*-
import subprocess, os, sys
from PIL import Image, ImageDraw, ImageFont

SCRATCH = "/private/tmp/claude-501/-Users-stanislav-code-stanislav-v1/9d0230e4-280e-4706-96ef-b855e34827e5/scratchpad"
sys.path.insert(0, SCRATCH)
import importlib.util
spec = importlib.util.spec_from_file_location("gv", os.path.join(SCRATCH, "gen_videos.py"))
# reuse STEPS/TOMA tables by parsing the file namespace without running renders
src = open(os.path.join(SCRATCH, "gen_videos.py")).read()
ns = {}
exec(src.split("\nbuild_ass(")[0], ns)   # everything up to first build_ass call (defs + tables)
STEPS, TOMA = ns["STEPS"], ns["TOMA"]

F_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
F_REG  = "/System/Library/Fonts/Supplemental/Arial.ttf"
F_ITAL = "/System/Library/Fonts/Supplemental/Arial Italic.ttf"

def wrap(draw, text, font, maxw):
    words, lines, cur = text.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if draw.textlength(t, font=font) <= maxw or not cur:
            cur = t
        else:
            lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def line_png(path, en, ua):
    W, H = 1080, 640
    img = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(img)
    blocks = []
    if en is None:
        f = ImageFont.truetype(F_ITAL, 52)
        for l in wrap(d, ua, f, 960): blocks.append((l, f, (200,207,232,255), 3))
    else:
        fe = ImageFont.truetype(F_BOLD, 62)
        for l in wrap(d, en, fe, 960): blocks.append((l, fe, (255,255,255,255), 4))
        blocks.append((None, None, None, 22))  # gap
        fu = ImageFont.truetype(F_REG, 44)
        for l in wrap(d, ua, fu, 980): blocks.append((l, fu, (232,214,200,255), 3))
    heights = []
    for t, f, c, s in blocks:
        if t is None: heights.append(s); continue
        bb = d.textbbox((0,0), t, font=f, stroke_width=s)
        heights.append(bb[3]-bb[1]+14)
    y = (H - sum(heights)) // 2
    for (t, f, c, s), h in zip(blocks, heights):
        if t is None: y += h; continue
        w = d.textlength(t, font=f)
        d.text(((W-w)//2, y), t, font=f, fill=c, stroke_width=s, stroke_fill=(12,12,18,230))
        y += h
    img.save(path)

def title_png(path, ua, en):
    W, H = 1080, 280
    img = Image.new("RGBA", (W, H), (0,0,0,0))
    d = ImageDraw.Draw(img)
    ft = ImageFont.truetype(F_BOLD, 56)
    fs = ImageFont.truetype(F_REG, 27)
    w = d.textlength(ua, font=ft)
    d.text(((W-w)//2, 60), ua, font=ft, fill=(255,255,255,255), stroke_width=3, stroke_fill=(12,12,18,230))
    w = d.textlength(en, font=fs)
    d.text(((W-w)//2, 150), en, font=fs, fill=(184,191,212,255), stroke_width=2, stroke_fill=(12,12,18,200))
    img.save(path)

def render(tag, lines, title_ua, title_en, mp3, grad, out, dur):
    ldir = os.path.join(SCRATCH, f"lines_{tag}")
    os.makedirs(ldir, exist_ok=True)
    title_png(os.path.join(ldir, "title.png"), title_ua, title_en)
    for i, (en, ua, a, b) in enumerate(lines):
        line_png(os.path.join(ldir, f"l{i:02d}.png"), en, ua)
    cmd = ["ffmpeg", "-y", "-f", "lavfi", "-i", grad + f":d={dur+0.5}", "-i", mp3,
           "-loop", "1", "-i", os.path.join(ldir, "title.png")]
    for i in range(len(lines)):
        cmd += ["-loop", "1", "-i", os.path.join(ldir, f"l{i:02d}.png")]
    fc = ["[1:a]showwaves=s=1080x220:mode=cline:colors=0xFFFFFF@0.25:rate=30[wv]",
          "[0:v][wv]overlay=0:1580[bg0]",
          "[bg0][2:v]overlay=0:70[c0]"]
    prev = "c0"
    for i, (en, ua, a, b) in enumerate(lines):
        idx = 3 + i
        fc.append(f"[{idx}:v]format=rgba,fade=in:st={a:.2f}:d=0.25:alpha=1,fade=out:st={b-0.25:.2f}:d=0.25:alpha=1[f{i}]")
        nxt = f"c{i+1}"
        fc.append(f"[{prev}][f{i}]overlay=0:800:enable='between(t,{a-0.05:.2f},{b+0.05:.2f})'[{nxt}]")
        prev = nxt
    graph = ";".join(fc)
    cmd += ["-filter_complex", graph, "-map", f"[{prev}]", "-map", "1:a",
            "-c:v", "libx264", "-crf", "17", "-preset", "medium", "-pix_fmt", "yuv420p",
            "-r", "30", "-c:a", "aac", "-b:a", "320k", "-t", str(dur), out]
    print("rendering", out, "…")
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        print("FFMPEG ERROR:\n", r.stderr[-2500:]); raise SystemExit(1)
    print("ok:", out)

render("steps", STEPS, "17 000 КРОКІВ", "SEVENTEEN THOUSAND STEPS · Warsaw 2026",
       "/Users/stanislav/Downloads/Seventeen Thousand Steps.mp3",
       "gradients=s=1080x1920:speed=0.012:nb_colors=3:c0=0x141a3d:c1=0x2a1548:c2=0x54123a:x0=200:y0=200:x1=900:y1=1750",
       "/Users/stanislav/Downloads/17000-krokiv-tiktok.mp4", 167.92)

render("toma", TOMA, "ТОМАГАВК", "THE TOMAHAWK WOMEN · Nafplio 2026",
       "/Users/stanislav/Downloads/How Could They Eat It.mp3",
       "gradients=s=1080x1920:speed=0.012:nb_colors=3:c0=0x2b0a12:c1=0x4a1020:c2=0x1a0a2e:x0=200:y0=200:x1=900:y1=1750",
       "/Users/stanislav/Downloads/tomahawk-tiktok.mp4", 231.52)
