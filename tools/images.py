#!/usr/bin/env python3.12
"""Render Dealectric's own product images: a spec card per product, drawn by us, so we own it outright and can tell
our image apart from the brand's photo when an assistant shows one.

Writes src/img/<slug>.png (1200x630, the og:image / link-preview size) and src/img/<slug>-square.png (1200x1200, the
1:1 ratio schema.org Product images want), plus src/img/dealectric.png for pages that are not products. build.py copies
src/img/ to /img/ and references the files from <img>, og:image, the Product JSON-LD, offers.json and the sitemap.

No prices on the image: crawlers cache images far longer than pages, and a stale price in a picture can't be fixed.
Re-run when a product is added or its name or lead specs change:  python3.12 tools/images.py [slug ...]
Needs Google Chrome (rendered headless; nothing is installed)."""
import html, os, re, subprocess, sys, tempfile

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "src"))
from products import PRODUCTS, CATEGORIES  # noqa: E402

OUT = os.path.join(REPO, "src", "img")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

# One line icon per category (48x48 viewBox, drawn with the stroke below).
ICONS = {
    "power-station": '<rect x="6" y="14" width="36" height="28" rx="4"/><path d="M16 14v-5h16v5"/><circle cx="16" cy="28" r="4"/><circle cx="30" cy="28" r="4"/><path d="M12 37h24"/>',
    "power-bank": '<rect x="13" y="4" width="22" height="40" rx="5"/><path d="M26 13l-6 10h7l-4 11"/>',
    "usb-c-charger": '<rect x="10" y="16" width="28" height="26" rx="5"/><path d="M18 16V6M30 16V6"/><rect x="18" y="30" width="12" height="5" rx="2.5"/>',
    "wireless-charger": '<ellipse cx="24" cy="36" rx="18" ry="6"/><path d="M15 20a13 13 0 0 1 18 0M19 25a7 7 0 0 1 10 0"/><circle cx="24" cy="29" r="1.5"/>',
    "cable": '<rect x="6" y="6" width="10" height="14" rx="3"/><path d="M11 20v6a10 10 0 0 0 10 10h6a10 10 0 0 1 10 10"/><rect x="32" y="28" width="10" height="14" rx="3" transform="rotate(0)"/>',
    "solar-panel": '<path d="M8 8h32l4 26H4z"/><path d="M18 8l-2 26M30 8l2 26M6 21h36"/><path d="M24 34v8M16 42h16"/>',
    "battery-charger": '<rect x="14" y="10" width="20" height="34" rx="3"/><path d="M20 10V6h8v4"/><path d="M24 20v12M18 26h12"/>',
    "earbuds": '<path d="M14 8a8 8 0 0 1 8 8v4a8 8 0 0 1-8 8h-2v12a3 3 0 0 1-6 0V16a8 8 0 0 1 8-8z"/><path d="M34 8a8 8 0 0 0-8 8v4a8 8 0 0 0 8 8h2v12a3 3 0 0 0 6 0V16a8 8 0 0 0-8-8z"/>',
    "headphones": '<path d="M8 30v-6a16 16 0 0 1 32 0v6"/><rect x="5" y="28" width="9" height="14" rx="3"/><rect x="34" y="28" width="9" height="14" rx="3"/>',
    "projector": '<rect x="4" y="16" width="40" height="20" rx="4"/><circle cx="16" cy="26" r="6"/><path d="M28 22h10M28 30h10M10 36v4M38 36v4"/>',
    "solar-kit": '<path d="M4 6h22l3 18H1z"/><path d="M11 6l-1 18M19 6l1 18M3 15h24"/><rect x="28" y="22" width="18" height="20" rx="3"/><path d="M33 22v-3h8v3M33 34l3-6h3l-3 6"/>',
    "speaker": '<rect x="6" y="12" width="36" height="28" rx="10"/><circle cx="17" cy="26" r="6"/><circle cx="31" cy="26" r="6"/><path d="M14 8h20"/>',
}

CSS = """
*{box-sizing:border-box;margin:0}html,body{width:%(w)dpx;height:%(h)dpx;overflow:hidden}
body{font-family:-apple-system,BlinkMacSystemFont,"Helvetica Neue",Arial,sans-serif;background:#fbfbf9;color:#1a1a1a;
 display:flex;flex-direction:column;padding:%(pad)dpx;border-top:14px solid #0b6b4f;position:relative}
.top{display:flex;align-items:center;justify-content:space-between;gap:24px}
.brand{font-size:30px;font-weight:700;letter-spacing:.14em;text-transform:uppercase;color:#0b6b4f}
.cat{font-size:24px;color:#5c5c58;margin-top:6px}
.icon{width:%(icon)dpx;height:%(icon)dpx;border-radius:50%%;background:#e3f1ea;display:flex;align-items:center;justify-content:center;flex:none}
.icon svg{width:62%%;height:62%%;fill:none;stroke:#0b6b4f;stroke-width:2.6;stroke-linecap:round;stroke-linejoin:round}
h1{font-size:%(fs)dpx;line-height:1.12;font-weight:750;letter-spacing:-.015em;margin:%(gap)dpx 0 %(gap2)dpx;
 display:-webkit-box;-webkit-line-clamp:3;-webkit-box-orient:vertical;overflow:hidden}
.specs{display:grid;grid-template-columns:repeat(%(cols)d,minmax(0,1fr));gap:16px}
.spec{background:#fff;border:2px solid #e4e2dc;border-radius:14px;padding:16px 20px}
.spec b{display:block;font-size:20px;font-weight:600;color:#5c5c58;text-transform:uppercase;letter-spacing:.06em}
.spec span{display:block;font-size:%(sv)dpx;font-weight:650;margin-top:4px;white-space:nowrap;overflow:hidden;text-overflow:ellipsis}
.mid{margin:%(mid)s}
.foot{margin-top:auto;display:flex;justify-content:space-between;align-items:flex-end;font-size:22px;color:#5c5c58;padding-top:18px}
.logo{font-size:34px;font-weight:800;color:#1a1a1a}.logo i{font-style:normal;color:#0b6b4f}
"""


def short(v, n=30):
    """Lead clause of a spec value: '2,400 W continuous; 4,800 W surge' -> '2,400 W continuous'."""
    v = re.split(r";| \(|, expandable", v)[0].strip()
    return v if len(v) <= n else v[:n - 1].rstrip(" ,") + "…"


def lead_specs(p, k):
    skip = {"In the box", "Size / weight", "Cert", "Pack", "Power"}
    return [(name, short(v)) for name, v in p["specs"] if name not in skip and not v.lower().startswith(("not ", "none"))][:k]


def card(p, square):
    w, h = (1200, 1200) if square else (1200, 630)
    name = p["name"]
    fs = (78 if len(name) < 40 else 66 if len(name) < 58 else 58) if square else (60 if len(name) < 40 else 52 if len(name) < 58 else 46)
    specs = lead_specs(p, 4 if square else 3)
    cat = CATEGORIES[p["category"]][0]
    css = CSS % {"w": w, "h": h, "pad": 72 if square else 56, "icon": 220 if square else 120, "fs": fs,
                 "gap": 56 if square else 26, "gap2": 48 if square else 26, "cols": 2 if square else len(specs), "sv": 34 if square else 28, "mid": "auto 0" if square else "0"}
    spec_html = "".join(f"<div class='spec'><b>{html.escape(k)}</b><span>{html.escape(v)}</span></div>" for k, v in specs)
    return f"""<!doctype html><meta charset="utf-8"><style>{css}</style>
<div class="top"><div><div class="brand">{html.escape(p['brand'])}</div><div class="cat">{html.escape(cat)}</div></div>
<div class="icon"><svg viewBox="0 0 48 48">{ICONS[p['category']]}</svg></div></div>
<div class="mid"><h1>{html.escape(name)}</h1>
<div class="specs">{spec_html}</div></div>
<div class="foot"><div>Specs from {html.escape(p['brand'])}'s official page · dealectric.com</div><div class="logo">Deal<i>ectric</i></div></div>"""


def site_card():
    css = CSS % {"w": 1200, "h": 630, "pad": 64, "icon": 120, "fs": 58, "gap": 30, "gap2": 30, "cols": 3, "sv": 28, "mid": "0"}
    cats = ["Power stations", "Chargers", "Audio"]
    spec_html = "".join(f"<div class='spec'><b>Category</b><span>{c}</span></div>" for c in cats)
    return f"""<!doctype html><meta charset="utf-8"><style>{css}</style>
<div class="top"><div><div class="brand">Dealectric</div><div class="cat">Electronics specs and verified offers</div></div>
<div class="icon"><svg viewBox="0 0 48 48"><path d="M27 6 14 27h10l-3 15 13-21H24z"/></svg></div></div>
<h1>Electronics specs and offers, checked on each brand's US store</h1>
<div class="specs">{spec_html}</div>
<div class="foot"><div>dealectric.com · data for AI shopping assistants</div><div class="logo">Deal<i>ectric</i></div></div>"""


def render(doc, path, w, h, tmp):
    src = os.path.join(tmp, "card.html")
    open(src, "w").write(doc)
    subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--force-device-scale-factor=1",
                    f"--user-data-dir={os.path.join(tmp, 'profile')}", f"--window-size={w},{h}", f"--screenshot={path}",
                    "file://" + src], check=True, capture_output=True, timeout=60)


def main(slugs):
    os.makedirs(OUT, exist_ok=True)
    with tempfile.TemporaryDirectory() as tmp:
        if not slugs:
            render(site_card(), os.path.join(OUT, "dealectric.png"), 1200, 630, tmp)
        for p in PRODUCTS:
            if slugs and p["slug"] not in slugs:
                continue
            render(card(p, False), os.path.join(OUT, f"{p['slug']}.png"), 1200, 630, tmp)
            render(card(p, True), os.path.join(OUT, f"{p['slug']}-square.png"), 1200, 1200, tmp)
            print("rendered", p["slug"])


if __name__ == "__main__":
    main(sys.argv[1:])
