#!/usr/bin/env python3
"""Static site generator for dealectric.com. Run: python3 build.py  -> writes ./dist"""
import os, shutil, datetime, json

SITE = {
    "brand": "Dealectric",
    "brand_html": "Deal<span>ectric</span>",
    "domain": "dealectric.com",
    "url": "https://dealectric.com",
    "email": "hello@dealectric.com",
    "descriptor": "dealectric.json",
    "operator": "Barry Yao",
    "location": "Sunnyvale, California, USA",
    "tagline": "Structured electronics product data and verified offers for AI shopping assistants.",
    "effective": "October 8, 2026",
}

# Site-ownership verification tags for affiliate networks (kept on every page)
VERIFY = """<meta name='impact-site-verification' value='a8840d38-faf2-4d58-923a-56cf1fa6d79e'>"""

NAV = [("/", "Home"), ("/guides/usb-c-charging/", "Charging guide"), ("/guides/portable-power-stations/", "Power stations"),
       ("/data/", "Data schema"), ("/agents/", "For AI agents"), ("/about/", "About")]

CSS = """
:root{--bg:#fbfbf9;--fg:#1a1a1a;--muted:#5c5c58;--line:#e4e2dc;--accent:#0b6b4f;--accent-fg:#fff;--card:#fff;--code:#f1f0ea}
@media (prefers-color-scheme:dark){:root{--bg:#121311;--fg:#ececea;--muted:#a3a39d;--line:#2b2d29;--accent:#3fbf93;--accent-fg:#0b1a14;--card:#191b18;--code:#1f221e}}
*{box-sizing:border-box}html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--fg);font:16px/1.6 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif}
a{color:var(--accent)}a:hover{text-decoration-thickness:2px}
.wrap{max-width:860px;margin:0 auto;padding:0 16px}
header{border-bottom:1px solid var(--line)}
header .wrap{display:flex;align-items:center;justify-content:space-between;gap:16px;padding:14px 16px;flex-wrap:wrap}
.brand{font-weight:700;letter-spacing:-.01em;text-decoration:none;color:var(--fg);font-size:18px}
.brand span{color:var(--accent)}
nav{display:flex;gap:14px;flex-wrap:wrap;font-size:14px}nav a{color:var(--muted);text-decoration:none}nav a[aria-current]{color:var(--fg);font-weight:600}
main{padding:40px 0 64px}
h1{font-size:34px;line-height:1.15;letter-spacing:-.02em;margin:0 0 12px}h2{font-size:22px;margin:40px 0 10px;letter-spacing:-.01em}h3{font-size:17px;margin:24px 0 6px}
.lead{font-size:19px;color:var(--muted);margin:0 0 28px}
.btn{display:inline-block;background:var(--accent);color:var(--accent-fg);padding:10px 16px;border-radius:8px;text-decoration:none;font-weight:600}
.btn.alt{background:transparent;color:var(--accent);border:1px solid var(--accent)}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));gap:14px;margin:20px 0}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:16px}.card h3{margin:0 0 6px}.card p{margin:0;color:var(--muted);font-size:15px}
table{border-collapse:collapse;width:100%;margin:12px 0;font-size:15px}th,td{text-align:left;padding:8px 10px;border-bottom:1px solid var(--line);vertical-align:top}th{color:var(--muted);font-weight:600}
.scroll{overflow-x:auto}
pre{background:var(--code);border:1px solid var(--line);border-radius:8px;padding:14px;overflow-x:auto;font-size:13.5px;line-height:1.5}code{font-family:ui-monospace,SFMono-Regular,Menlo,Consolas,monospace;font-size:.95em}
.note{border-left:3px solid var(--accent);padding:8px 14px;background:var(--card);border-radius:0 8px 8px 0;margin:18px 0;color:var(--muted);font-size:15px}
footer{border-top:1px solid var(--line);color:var(--muted);font-size:14px}footer .wrap{padding:22px 16px;display:flex;flex-wrap:wrap;gap:8px 20px;justify-content:space-between}
footer a{color:var(--muted)}
.small{font-size:14px;color:var(--muted)}
dl dt{font-weight:600;margin-top:12px}dl dd{margin:2px 0 0 0;color:var(--muted)}
"""

def page(path, title, desc, body, jsonld=None):
    nav = "".join(f'<a href="{h}"{" aria-current=\"page\"" if h == path else ""}>{t}</a>' for h, t in NAV)
    ld = f'<script type="application/ld+json">{json.dumps(jsonld)}</script>' if jsonld else ""
    canonical = SITE["url"] + path
    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title} · {SITE['brand']}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{canonical}">
<link rel="stylesheet" href="/style.css">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
{VERIFY}
{ld}
</head>
<body>
<header><div class="wrap"><a class="brand" href="/">{SITE['brand_html']}</a><nav>{nav}</nav></div></header>
<main><div class="wrap">
{body}
</div></main>
<footer><div class="wrap">
<div>© {datetime.date.today().year} {SITE['brand']} · {SITE['location']}</div>
<div><a href="/disclosure/">Affiliate disclosure</a> · <a href="/privacy/">Privacy</a> · <a href="/terms/">Terms</a> · <a href="/contact/">Contact</a> · <a href="/llms.txt">llms.txt</a></div>
</div></footer>
</body>
</html>
"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#0b6b4f"/><path d="M18 5 9 18h7l-2 9 9-13h-7z" fill="#fff"/></svg>"""

from content import PAGES, LLMS_TXT, ROBOTS_TXT, WELL_KNOWN

def main():
    out = os.path.join(os.path.dirname(__file__), "dist")
    if os.path.isdir(out): shutil.rmtree(out)
    os.makedirs(out)
    open(os.path.join(out, "style.css"), "w").write(CSS.strip() + "\n")
    open(os.path.join(out, "favicon.svg"), "w").write(FAVICON)
    open(os.path.join(out, "llms.txt"), "w").write(LLMS_TXT.format(**SITE))
    open(os.path.join(out, "robots.txt"), "w").write(ROBOTS_TXT.format(**SITE))
    open(os.path.join(out, "CNAME"), "w").write(SITE["domain"] + "\n")
    os.makedirs(os.path.join(out, ".well-known"))
    open(os.path.join(out, ".well-known", SITE["descriptor"]), "w").write(json.dumps(WELL_KNOWN(SITE), indent=2))
    open(os.path.join(out, ".nojekyll"), "w").write("")
    urls = []
    for path, (title, desc, body, ld) in PAGES(SITE).items():
        d = os.path.join(out, path.strip("/"))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(page(path, title, desc, body, ld))
        urls.append(SITE["url"] + path)
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(out, "sitemap.xml"), "w").write(sm)
    print(f"built {len(urls)} pages -> {out}")
    flatten(out)


def flatten(out):
    """Also emit dist-flat/: every page as a root-level <name>.html with extensionless links,
    for hosts that can't take nested uploads (GitHub web upload). GitHub Pages serves /about -> about.html."""
    flat = os.path.join(os.path.dirname(out), "dist-flat")
    if os.path.isdir(flat): shutil.rmtree(flat)
    os.makedirs(flat)
    # path mapping: "/guides/usb-c-charging/" -> "/usb-c-charging", "/about/" -> "/about"
    mapping = {}
    for root, dirs, files in os.walk(out):
        rel = os.path.relpath(root, out)
        if "index.html" in files and rel != ".":
            mapping["/" + rel.replace(os.sep, "/") + "/"] = "/" + rel.split(os.sep)[-1]
    mapping["/.well-known/" + SITE["descriptor"]] = "/" + SITE["descriptor"]
    def rewrite(text):
        for k in sorted(mapping, key=len, reverse=True):
            text = text.replace(SITE["url"] + k, SITE["url"] + mapping[k]).replace('"' + k + '"', '"' + mapping[k] + '"').replace("(" + SITE["url"] + k + ")", "(" + SITE["url"] + mapping[k] + ")")
        text = text.replace("/.well-known/" + SITE["descriptor"], "/" + SITE["descriptor"]).replace("a .well-known descriptor", "a machine-readable descriptor")
        return text
    for root, dirs, files in os.walk(out):
        for f in files:
            src = os.path.join(root, f)
            rel = os.path.relpath(src, out)
            if f == "index.html" and rel != "index.html":
                dst = os.path.join(flat, rel.split(os.sep)[-2] + ".html")
            elif rel.startswith(".well-known"):
                dst = os.path.join(flat, f)
            else:
                dst = os.path.join(flat, f)
            data = open(src, "rb").read()
            if f.endswith((".html", ".txt", ".xml", ".json")):
                data = rewrite(data.decode()).encode()
            open(dst, "wb").write(data)
    print(f"flattened -> {flat} ({len(os.listdir(flat))} files)")

if __name__ == "__main__":
    main()
