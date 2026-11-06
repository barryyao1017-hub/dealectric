#!/usr/bin/env python3.12
"""Render a Dealectric YouTube video and its Short from a script file (DLC-187).

    python3.12 growth/video/render.py <id> [--only long|short] [--slides]

Reads growth/video/scripts/<id>.json and writes growth/video/out/<id>/ (gitignored):
  long.mp4  (1920x1080)   short.mp4 (1080x1920, under 60 s)
  long.srt  short.srt     captions, one cue per sentence (upload them: the transcript is what AI search reads)
  long.txt  short.txt     title, description and tags, with today's price and tested code read from src/
  slides/                 the PNG of every scene (--slides renders only these, no audio, for a quick look)

Each scene is a slide we draw ourselves (HTML, screenshotted by headless Chrome as tools/images.py does) plus a
narration line voiced by OpenAI text-to-speech (key: keychain openai-api-key; audio cached by text in out/cache/).
No prices are spoken or drawn: a video can't be edited after upload, its description can. Prices, codes and the
last-pass date go in the description, which is rewritten from src/ each render.
"""
import hashlib, html, json, os, re, subprocess, sys, tempfile, urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, os.path.join(REPO, "src"))
import build  # noqa: E402  (price, code and last-pass helpers the site uses)

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
VOICE, TTS_MODEL = "ash", "gpt-4o-mini-tts"
TTS_STYLE = ("A calm, clear, friendly product reviewer explaining specs to a shopper. Natural American English, "
             "moderate pace, no hype. Read numbers and units naturally (Wh as watt-hours, W as watts).")
PAD = 0.45  # seconds of silence after each scene
FPS = 30
SIZES = {"long": (1920, 1080), "short": (1080, 1920)}
GO = "https://dealectric.com/go/{slug}?utm_source=youtube&utm_campaign={vid}"
PAGE = "https://dealectric.com/{page}?utm_source=youtube&utm_campaign={vid}"
DISCLOSURE = ("Links above are affiliate links: they open each brand's official US store at no cost to you, and "
              "Dealectric earns a commission on a purchase, which pays for the testing. Amazon links: as an Amazon "
              "Associate Dealectric earns from qualifying purchases.")
AI_NOTE = ("How this video is made: the script is written from Dealectric's published spec tables (makers' US pages) "
           "and the narration is an AI voice. No product was filmed; the slides are our own.")

CSS = """
*{box-sizing:border-box;margin:0}html,body{width:%(w)dpx;height:%(h)dpx;overflow:hidden}
body{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;background:#fbfbf9;color:#1a1a1a;
 display:flex;flex-direction:column;padding:%(pad)dpx;border-top:18px solid #0b6b4f}
.kicker{font-size:%(k)dpx;font-weight:700;letter-spacing:.12em;text-transform:uppercase;color:#0b6b4f}
h1{font-size:%(h1)dpx;line-height:1.08;font-weight:780;letter-spacing:-.02em;margin-top:%(g)dpx}
h2{font-size:%(h2)dpx;line-height:1.12;font-weight:750;letter-spacing:-.015em;margin-top:%(g2)dpx}
.sub{font-size:%(b)dpx;line-height:1.35;color:#3d3d3a;margin-top:%(g)dpx;max-width:30em}
.body{flex:1;display:flex;flex-direction:column;justify-content:center}
.pts{display:grid;gap:%(gap)dpx;margin-top:%(g)dpx}
.pt{display:flex;gap:%(gap)dpx;align-items:flex-start;background:#fff;border:2px solid #e4e2dc;border-radius:18px;padding:%(pp)dpx}
.pt .n{flex:none;width:%(nn)dpx;height:%(nn)dpx;border-radius:50%%;background:#0b6b4f;color:#fff;font-weight:800;
 font-size:%(nf)dpx;display:flex;align-items:center;justify-content:center}
.pt b{display:block;font-size:%(b)dpx;font-weight:720}.pt span{display:block;font-size:%(s)dpx;color:#4a4a46;margin-top:4px;line-height:1.3}
table{border-collapse:collapse;margin-top:%(g)dpx;width:100%%;font-size:%(t)dpx;background:#fff}
th{background:#0b6b4f;color:#fff;text-align:left;padding:%(tp)dpx;font-weight:650}
td{padding:%(tp)dpx;border-bottom:2px solid #e4e2dc;vertical-align:top}td:first-child{font-weight:680}
tr.hi td{background:#e3f1ea}
.big{font-size:%(big)dpx;font-weight:820;color:#0b6b4f;letter-spacing:-.03em;line-height:1}
.cap{font-size:%(h2)dpx;font-weight:700;line-height:1.15;margin-top:%(g)dpx;max-width:20em}
.note{font-size:%(s)dpx;color:#5c5c58;margin-top:%(g)dpx;line-height:1.35}
.foot{display:flex;justify-content:space-between;align-items:flex-end;gap:24px;font-size:%(f)dpx;color:#5c5c58;padding-top:16px}
.logo{font-size:%(lg)dpx;font-weight:800;color:#1a1a1a;white-space:nowrap}.logo i{font-style:normal;color:#0b6b4f}
.bolt{display:inline-block;width:%(lg)dpx;height:%(lg)dpx;vertical-align:-.15em;margin-right:.25em}
"""

BOLT = '<svg class="bolt" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#0b6b4f"/><path d="M18 5 9 18h7l-2 9 9-13h-7z" fill="#fff"/></svg>'


def css_for(fmt):
    w, h = SIZES[fmt]
    if fmt == "long":
        v = dict(pad=90, k=34, h1=96, h2=64, b=40, s=32, g=34, g2=18, gap=24, pp=24, nn=58, nf=30, t=34, tp=16, big=260, f=26, lg=44)
    else:
        v = dict(pad=80, k=40, h1=104, h2=74, b=46, s=38, g=44, g2=22, gap=26, pp=30, nn=66, nf=34, t=34, tp=14, big=260, f=30, lg=52)
    return CSS % dict(v, w=w, h=h)


def esc(s):
    return html.escape(str(s))


def slide_html(sl, fmt):
    k = sl.get("kind")
    head = f'<div class="kicker">{esc(sl["kicker"])}</div>' if sl.get("kicker") else ""
    if k == "title":
        body = f'{head}<h1>{esc(sl["h"])}</h1>' + (f'<div class="sub">{esc(sl["sub"])}</div>' if sl.get("sub") else "")
    elif k == "points":
        items = "".join(f'<div class="pt"><div class="n">{i + 1}</div><div><b>{esc(a)}</b>' + (f"<span>{esc(b)}</span>" if b else "") + "</div></div>"
                        for i, (a, b) in enumerate(sl["items"]))
        body = f'{head}<h2>{esc(sl["h"])}</h2><div class="pts">{items}</div>'
    elif k == "table":
        cols = sl["cols"]
        rows = sl["rows"]
        hi = set(sl.get("hi", []))
        th = "".join(f"<th>{esc(c)}</th>" for c in cols)
        trs = "".join(f'<tr class="{"hi" if i in hi else ""}">' + "".join(f"<td>{esc(c)}</td>" for c in r) + "</tr>" for i, r in enumerate(rows))
        body = f'{head}<h2>{esc(sl["h"])}</h2><table><tr>{th}</tr>{trs}</table>'
    elif k == "stat":
        n = len(sl["big"])
        size = (260 if n <= 4 else 220 if n <= 6 else 170) if fmt == "long" else (240 if n <= 4 else 170 if n <= 6 else 130)
        body = (f'{head}<div class="big" style="margin-top:20px;font-size:{size}px;white-space:nowrap">{esc(sl["big"])}</div>'
                f'<div class="cap">{esc(sl["cap"])}</div>')
    elif k == "end":
        lines = "".join(f'<div class="pt"><div class="n">{i + 1}</div><div><b>{esc(a)}</b></div></div>' for i, a in enumerate(sl["items"]))
        body = f'{head}<h2>{esc(sl["h"])}</h2><div class="pts">{lines}</div>'
    else:
        raise ValueError(f"unknown slide kind {k!r}")
    if sl.get("note"):
        body += f'<div class="note">{esc(sl["note"])}</div>'
    foot_l = esc(sl.get("foot", "Specs from each maker's official US page"))
    return (f'<!doctype html><meta charset="utf-8"><style>{css_for(fmt)}</style><div class="body">{body}</div>'
            f'<div class="foot"><div>{foot_l}</div><div class="logo">{BOLT}Deal<i>ectric</i></div></div>')


def shoot(doc, path, fmt, tmp):
    w, h = SIZES[fmt]
    src = os.path.join(tmp, "slide.html")
    open(src, "w").write(doc)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--user-data-dir={os.path.join(tmp, 'profile')}", f"--window-size={w},{h}", f"--screenshot={path}",
                    "file://" + src], check=True, capture_output=True, timeout=90)


# Spoken forms the voice gets wrong when it reads the written ones (checked by transcribing a render with whisper-1:
# "Dealectric" came back as "Dielectric", "LiFePO4" as "LEAF P04"). Of "Deal-ectric", "Deal-lectric", "Deel-ektrik" and
# "Deal Electric", only the last transcribed back as "Deal ..." (2026-11-06). Captions keep the written form.
SPEAK = [(r"\bDealectric\b", "Deal Electric"), (r"\bdealectric dot com\b", "deal electric dot com"),
         (r"\bLiFePO4\b", "lithium iron phosphate")]


def tts(text, cache):
    for pat, rep in SPEAK:
        text = re.sub(pat, rep, text)
    key = hashlib.sha1(f"{TTS_MODEL}|{VOICE}|{TTS_STYLE}|{text}".encode()).hexdigest()[:16]
    path = os.path.join(cache, f"{key}.mp3")
    if os.path.exists(path):
        return path
    api_key = subprocess.run(["security", "find-generic-password", "-a", "dealectric", "-s", "openai-api-key", "-w"],
                             capture_output=True, text=True, check=True).stdout.strip()
    req = urllib.request.Request("https://api.openai.com/v1/audio/speech", method="POST",
                                 data=json.dumps({"model": TTS_MODEL, "voice": VOICE, "input": text, "instructions": TTS_STYLE,
                                                  "response_format": "mp3"}).encode(),
                                 headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
    open(path, "wb").write(data)
    return path


def duration(path):
    return float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", path],
                                capture_output=True, text=True, check=True).stdout)


def clip(png, mp3, dur, out, fmt):
    w, h = SIZES[fmt]
    frames = int(round(dur * FPS))
    # A slow push-in (1.00 -> ~1.03) so a still slide doesn't read as a frozen frame.
    vf = (f"scale={w * 2}:{h * 2},zoompan=z='1+0.03*on/{frames}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)'"
          f":d={frames}:s={w}x{h}:fps={FPS},format=yuv420p")
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", png, "-i", mp3, "-filter_complex",
                    f"[0:v]{vf}[v];[1:a]aresample=48000,apad=pad_dur={PAD}[a]", "-map", "[v]", "-map", "[a]",
                    "-t", f"{dur:.3f}", "-c:v", "libx264", "-preset", "medium", "-crf", "19", "-r", str(FPS),
                    "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-ac", "2", out], check=True)


def ts(t):
    ms = int(round(t * 1000))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def srt_cues(scenes_timed):
    """One cue per sentence, timed in proportion to its length inside the scene's spoken part."""
    out, n = [], 1
    for start, spoken, text in scenes_timed:
        parts = [p for p in re.split(r"(?<=[.!?])\s+", text.strip()) if p]
        total = sum(len(p) for p in parts) or 1
        t = start
        for p in parts:
            d = spoken * len(p) / total
            out.append(f"{n}\n{ts(t)} --> {ts(t + d)}\n{p}\n")
            n += 1
            t += d
    return "\n".join(out)


def offer_lines(slugs, vid):
    lines = []
    for slug in slugs:
        p = build.BY_SLUG[slug]
        name = build.short_name(p) if hasattr(build, "short_name") else p["name"]
        if p.get("program", "").startswith("amazon:"):
            lines.append(f"• {p['name']}: {p['url']}")   # Amazon: direct tagged link, no price (DLC-159)
            continue
        c, s, after, date = build.best_offer(p)
        state = (f" (pre-order, ships {p['preorder']})" if p.get("preorder") else " (sold out when checked)" if p.get("in_stock") is False else "")
        price = f"{build.money(p['price'])} on {p['brand']}'s US store, checked {p.get('verified') or build.VERIFIED}{state}"
        code = (f" Code {c['code']} saves {build.money(s)}, {build.pass_clause(p, c, date)}." if c else "")
        lines.append(f"• {p['name']}: {GO.format(slug=slug, vid=vid)}\n  {price}.{code}")
    return "\n".join(lines)


def describe(s, fmt, chapters):
    vid = s["id"]
    title = s["title"] if fmt == "long" else s["short_title"]
    parts = [s["summary"] if fmt == "long" else s.get("short_summary", s["summary"])]
    parts.append(f"Full comparison, prices checked on the makers' US stores and codes tested in their carts:\n{PAGE.format(page=s['page'], vid=vid)}")
    if s.get("products"):
        parts.append("Products in this video. Dealectric earns a commission when you buy through these links, at no cost to you:\n"
                     + offer_lines(s["products"], vid))
    if fmt == "long" and chapters:
        parts.append("Chapters:\n" + "\n".join(f"{int(t // 60)}:{int(t % 60):02d} {c}" for t, c in chapters))
    parts.append("Prices and codes change; the page above is updated daily and is the current word.")
    parts.append(DISCLOSURE)
    parts.append(AI_NOTE)
    if fmt == "short":
        parts.append("#Shorts")
    tags = ", ".join(s.get("tags", []))
    return f"TITLE: {title}\n\nDESCRIPTION:\n" + "\n\n".join(parts) + f"\n\nTAGS: {tags}\n"


def render(s, fmt, slides_only):
    out = os.path.join(HERE, "out", s["id"])
    os.makedirs(os.path.join(out, "slides"), exist_ok=True)
    cache = os.path.join(HERE, "out", "cache")
    os.makedirs(cache, exist_ok=True)
    scenes = s[fmt]
    with tempfile.TemporaryDirectory() as tmp:
        clips, timed, chapters, t = [], [], [], 0.0
        for i, sc in enumerate(scenes):
            png = os.path.join(out, "slides", f"{fmt}-{i:02d}.png")
            shoot(slide_html(sc["slide"], fmt), png, fmt, tmp)
            if slides_only:
                continue
            mp3 = tts(sc["say"], cache)
            spoken = duration(mp3)
            dur = spoken + PAD
            c = os.path.join(tmp, f"c{i:02d}.mp4")
            clip(png, mp3, dur, c, fmt)
            clips.append(c)
            timed.append((t, spoken, sc["say"]))
            if sc.get("chapter"):
                chapters.append((t, sc["chapter"]))
            t += duration(c)
        if slides_only:
            print(f"{s['id']} {fmt}: {len(scenes)} slides in {out}/slides")
            return
        lst = os.path.join(tmp, "list.txt")
        open(lst, "w").write("".join(f"file '{c}'\n" for c in clips))
        mp4 = os.path.join(out, f"{fmt}.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy",
                        "-movflags", "+faststart", mp4], check=True)
    open(os.path.join(out, f"{fmt}.srt"), "w").write(srt_cues(timed))
    if chapters and chapters[0][0] > 0:
        chapters.insert(0, (0.0, "Intro"))
    open(os.path.join(out, f"{fmt}.txt"), "w").write(describe(s, fmt, chapters))
    total = duration(mp4)
    print(f"{s['id']} {fmt}: {total:.1f} s, {len(scenes)} scenes -> {mp4}")
    if fmt == "short" and total > 60:
        print(f"  WARNING: short is {total:.1f} s, over 60 s")


def main(argv):
    if not argv:
        sys.exit(__doc__)
    vid = argv[0]
    only = argv[argv.index("--only") + 1] if "--only" in argv else None
    s = json.load(open(os.path.join(HERE, "scripts", f"{vid}.json")))
    for fmt in ("long", "short"):
        if only and fmt != only:
            continue
        render(s, fmt, "--slides" in argv)


if __name__ == "__main__":
    main(sys.argv[1:])
