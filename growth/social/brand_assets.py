#!/usr/bin/env python3.12
"""Profile image and banners for Dealectric's official accounts (DLC-186). Writes growth/social/assets/:
  avatar.png           800x800    YouTube, X, Pinterest profile picture (shown in a circle)
  youtube-banner.png   2560x1440  text kept inside YouTube's 1546x423 safe area
  x-header.png         1500x500
Drawn as HTML and screenshotted by headless Chrome, as tools/images.py does.   python3.12 growth/social/brand_assets.py"""
import os, subprocess, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "assets")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
GREEN = "#0b6b4f"
BOLT = '<path d="M18 5 9 18h7l-2 9 9-13h-7z" fill="#fff"/>'
BASE = ("*{box-sizing:border-box;margin:0}html,body{width:%dpx;height:%dpx;overflow:hidden}"
        "body{font-family:-apple-system,BlinkMacSystemFont,'Helvetica Neue',Arial,sans-serif}")

AVATAR = (f'<style>{BASE % (800, 800)}body{{background:{GREEN};display:flex;align-items:center;justify-content:center}}</style>'
          f'<svg viewBox="0 0 32 32" width="520" height="520">{BOLT}</svg>')


def banner(w, h, safe_w, title_px, sub_px):
    return (f'<style>{BASE % (w, h)}body{{background:#fbfbf9;display:flex;align-items:center;justify-content:center;'
            f'border-top:{h // 40}px solid {GREEN};border-bottom:{h // 40}px solid {GREEN}}}'
            f'.box{{width:{safe_w}px;display:flex;align-items:center;gap:{title_px // 2}px}}'
            f'.t{{font-size:{title_px}px;font-weight:800;color:#1a1a1a;letter-spacing:-.02em}}.t i{{font-style:normal;color:{GREEN}}}'
            f'.s{{font-size:{sub_px}px;color:#3d3d3a;margin-top:{sub_px // 3}px}}</style>'
            f'<div class="box"><svg viewBox="0 0 32 32" width="{int(title_px * 1.6)}" height="{int(title_px * 1.6)}">'
            f'<rect width="32" height="32" rx="7" fill="{GREEN}"/>{BOLT}</svg>'
            f'<div><div class="t">Deal<i>ectric</i></div>'
            f'<div class="s">Power stations and solar kits, compared on the numbers · codes tested daily</div></div></div>')


def shoot(doc, name, w, h, tmp):
    src = os.path.join(tmp, "a.html")
    open(src, "w").write('<!doctype html><meta charset="utf-8">' + doc)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--user-data-dir={os.path.join(tmp, 'p')}", f"--window-size={w},{h}",
                    f"--screenshot={os.path.join(OUT, name)}", "file://" + src], check=True, capture_output=True, timeout=90)


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        shoot(AVATAR, "avatar.png", 800, 800, tmp)
        shoot(banner(2560, 1440, 1500, 120, 36), "youtube-banner.png", 2560, 1440, tmp)
        shoot(banner(1500, 500, 1300, 110, 34), "x-header.png", 1500, 500, tmp)
    print("wrote", OUT)
