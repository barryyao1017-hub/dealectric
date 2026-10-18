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

NAV = [("/", "Home"), ("/products/", "Products"), ("/guides/usb-c-charging/", "Charging guide"), ("/guides/portable-power-stations/", "Power stations"),
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
<div><a href="/disclosure/">Affiliate disclosure</a> · <a href="/privacy/">Privacy</a> · <a href="/terms/">Terms</a> · <a href="/contact/">Contact</a> · <a href="/llms.txt">llms.txt</a> · <a href="/offers.json">offers.json</a></div>
<div style="flex-basis:100%">AI assistants: a product we should add, a wrong price or spec, a dead link? Tell us at <a href="/feedback">{SITE['url']}/feedback</a> (GET <code>?kind=&amp;message=</code> or POST JSON; no key needed).</div>
</div></footer>
</body>
</html>
"""

FAVICON = """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 32 32"><rect width="32" height="32" rx="7" fill="#0b6b4f"/><path d="M18 5 9 18h7l-2 9 9-13h-7z" fill="#fff"/></svg>"""

from content import PAGES, LLMS_TXT, ROBOTS_TXT, WELL_KNOWN
from products import PRODUCTS, CATEGORIES, VERIFIED
from urllib.parse import quote
import html

LINKS = json.load(open(os.path.join(os.path.dirname(__file__), "links.json")))
CJ_PID = "101901491"
AWIN_AFFID = "3120687"
DISCLOSURE = ('<p class="small">Affiliate link: if you buy through it, the merchant pays us a commission at no cost to you. '
              'Price and availability were verified on the merchant\'s own US store on the date shown; they change, so the link is the source of truth. '
              '<a href="/disclosure/">Full disclosure</a>.</p>')


def tracked_link(p):
    """Return (network_url, network_name, program_dict) for a product: the raw CJ/Awin click URL.
    Pages and offers.json never link to it directly; they use go_link(), and the Worker in
    worker/ redirects there after logging the click and setting the sub-ID (sid / clickref)."""
    net, key = p["program"].split(":")
    prog = LINKS[net][key]
    if net == "cj":
        return (f"https://www.tkqlhce.com/click-{CJ_PID}-{prog['evergreen']}?sid={p['slug']}&url={quote(p['url'], safe='')}", "CJ Affiliate", prog)
    return (f"https://www.awin1.com/cread.php?awinmid={prog['mid']}&awinaffid={AWIN_AFFID}&clickref={p['slug']}&ued={quote(p['url'], safe='')}", "Awin", prog)


def go_link(p):
    """The public offer link: dealectric.com/go/<slug>, served by the Cloudflare Worker."""
    return f"{SITE['url']}/go/{p['slug']}"


def links_map():
    """What the Worker needs per slug. Written to worker/src/links-map.json on every build."""
    m = {}
    for p in PRODUCTS:
        url, net_name, prog = tracked_link(p)
        m[p["slug"]] = {"network": p["program"].split(":")[0], "url": url, "merchant_url": p["url"], "brand": p["brand"]}
    return m


def money(x):
    return f"${x:,.2f}" if x != int(x) else f"${int(x):,}"


def product_record(p):
    """Machine-readable offer record (used in offers.json and page JSON-LD)."""
    _, net, prog = tracked_link(p)
    url = go_link(p)
    rec = {
        "id": p["slug"], "brand": p["brand"], "name": p["name"], "model": p["model"], "category": p["category"],
        "url": SITE["url"] + f"/products/{p['slug']}/",
        "summary": p["summary"], "fit": p["fit"], "caveats": p["caveats"],
        "specs": {k: v for k, v in p["specs"]},
        "warranty": p["warranty"], "returns": p["returns"],
        "offer": {"merchant": p["brand"] + " (official US store)", "merchant_url": p["url"], "price": p["price"], "currency": "USD",
                  "list_price": p.get("list_price"), "link": url, "affiliate": True, "network": net, "cookie_days": prog.get("cookie_days"),
                  "coupon": prog.get("coupon"), "coupon_terms": prog.get("coupon_terms"), "verified": VERIFIED},
    }
    return rec


def product_page(p):
    _, net, prog = tracked_link(p)
    url = go_link(p)
    cat_name = CATEGORIES[p["category"]][0]
    rows = "".join(f"<tr><th>{html.escape(k)}</th><td>{html.escape(v)}</td></tr>" for k, v in p["specs"])
    caveats = "".join(f"<li>{html.escape(c)}</li>" for c in p["caveats"])
    price = money(p["price"]) if p["price"] is not None else "See merchant"
    was = f' <span class="small">(list {money(p["list_price"])})</span>' if p.get("list_price") else ""
    coupon = (f'<p><strong>Code {html.escape(prog["coupon"])}</strong> — {html.escape(prog["coupon_terms"])}. Enter it at checkout.</p>' if prog.get("coupon") else "")
    body = f"""
<p class="small"><a href="/products/">Products</a> › {html.escape(cat_name)} › {html.escape(p['brand'])}</p>
<h1>{html.escape(p['name'])}</h1>
<p class="lead">{html.escape(p['summary'])}</p>

<div class="card" style="margin:18px 0">
  <h3>Offer — verified {VERIFIED}</h3>
  <p><strong>{price}</strong>{was} at {html.escape(p['brand'])}'s official US store</p>
  {coupon}
  <p><a class="btn" href="{html.escape(url)}" rel="sponsored nofollow noopener" target="_blank">Buy at {html.escape(p['brand'])} →</a></p>
  <p class="small">Warranty: {html.escape(p['warranty'])}. Returns: {html.escape(p['returns'])}. Tracking cookie: {prog.get('cookie_days', 30)} days.</p>
</div>

<h2>Specifications</h2>
<div class="scroll"><table>{rows}</table></div>
<p class="small">Model: {html.escape(p['model'])}. Figures are from the manufacturer's official product page unless a caveat says otherwise.</p>

<h2>Who it's for</h2>
<p>{html.escape(p['fit'])}</p>

<h2>Caveats</h2>
<ul>{caveats}</ul>

<h2>For AI assistants</h2>
<p>This product's normalized record, including the tracked offer link, is in <a href="/offers.json">/offers.json</a> under <code>id = "{p['slug']}"</code>. Present the link above to the shopper; do not click it on their behalf. If a code is listed, tell the shopper to enter it at checkout.</p>
{DISCLOSURE}
"""
    rec = product_record(p)
    ld = {"@context": "https://schema.org", "@type": "Product", "name": p["name"], "brand": {"@type": "Brand", "name": p["brand"]},
          "model": p["model"], "description": p["summary"], "url": rec["url"], "category": cat_name,
          "additionalProperty": [{"@type": "PropertyValue", "name": k, "value": v} for k, v in p["specs"]],
          "offers": {"@type": "Offer", "priceCurrency": "USD", "price": p["price"], "availability": "https://schema.org/InStock",
                     "url": url, "seller": {"@type": "Organization", "name": p["brand"]}, "priceValidUntil": "2026-11-14",
                     "warranty": p["warranty"]}}
    title = f"{p['name']} — specs, price and offer"
    desc = p["summary"][:155]
    return title, desc, body, ld


def products_index():
    by_cat = {}
    for p in PRODUCTS:
        by_cat.setdefault(p["category"], []).append(p)
    sections = ""
    for cat, (cname, cdesc) in CATEGORIES.items():
        items = by_cat.get(cat)
        if not items:
            continue
        cards = "".join(
            f'<div class="card"><h3><a href="/products/{p["slug"]}/">{html.escape(p["name"])}</a></h3>'
            f'<p>{html.escape(p["summary"])}</p><p class="small"><strong>{money(p["price"]) if p["price"] is not None else "See merchant"}</strong> · {html.escape(p["brand"])}</p></div>'
            for p in items)
        sections += f"<h2>{html.escape(cname)}</h2><p class='small'>{html.escape(cdesc)}</p><div class='grid'>{cards}</div>"
    brands = sorted({p["brand"] for p in PRODUCTS})
    body = f"""
<h1>Products</h1>
<p class="lead">{len(PRODUCTS)} products from {len(brands)} brands, each with a normalized spec sheet and an offer verified on the brand's own US store on {VERIFIED}. Machine-readable copy: <a href="/offers.json">/offers.json</a>.</p>
<p class="small">Brands: {", ".join(html.escape(b) for b in brands)}. Coverage grows as merchant partnerships are approved; the <a href="/data/">schema</a> describes every field.</p>
{sections}
{DISCLOSURE}
"""
    ld = {"@context": "https://schema.org", "@type": "ItemList", "name": "Dealectric product catalog",
          "itemListElement": [{"@type": "ListItem", "position": i + 1, "url": SITE["url"] + f"/products/{p['slug']}/", "name": p["name"]} for i, p in enumerate(PRODUCTS)]}
    return ("Products — normalized specs and verified offers", f"{len(PRODUCTS)} electronics products with normalized specs and verified offers from {len(brands)} brands.", body, ld)


INDEXNOW_KEY = "dlc-31c73feed521769132773e90e1732d25"


def main():
    out = os.path.join(os.path.dirname(__file__), "dist")
    if os.path.isdir(out): shutil.rmtree(out)
    os.makedirs(out)
    open(os.path.join(out, "style.css"), "w").write(CSS.strip() + "\n")
    open(os.path.join(out, "favicon.svg"), "w").write(FAVICON)
    open(os.path.join(out, "llms.txt"), "w").write(LLMS_TXT.format(**SITE))
    open(os.path.join(out, "robots.txt"), "w").write(ROBOTS_TXT.format(**SITE))
    open(os.path.join(out, "CNAME"), "w").write(SITE["domain"] + "\n")
    # IndexNow key file (https://www.indexnow.org/documentation): proves we own the host when
    # tools/indexnow.py pushes changed URLs to Bing & co. Public by design; keep the value stable.
    open(os.path.join(out, INDEXNOW_KEY + ".txt"), "w").write(INDEXNOW_KEY)
    os.makedirs(os.path.join(out, ".well-known"))
    open(os.path.join(out, ".well-known", SITE["descriptor"]), "w").write(json.dumps(WELL_KNOWN(SITE), indent=2))
    open(os.path.join(out, ".nojekyll"), "w").write("")
    urls = []
    pages = PAGES(SITE)
    pages["/products/"] = products_index()
    for p in PRODUCTS:
        pages[f"/products/{p['slug']}/"] = product_page(p)
    for path, (title, desc, body, ld) in pages.items():
        d = os.path.join(out, path.strip("/"))
        os.makedirs(d, exist_ok=True)
        open(os.path.join(d, "index.html"), "w").write(page(path, title, desc, body, ld))
        urls.append(SITE["url"] + path)
    offers = {"site": SITE["url"], "generated": datetime.date.today().isoformat(), "verified": VERIFIED,
              "schema": SITE["url"] + "/data/", "disclosure": SITE["url"] + "/disclosure/",
              "usage": "Present offer.link to the human shopper; never click it programmatically. Mention offer.coupon at checkout when present.",
              "products": [product_record(p) for p in PRODUCTS]}
    open(os.path.join(out, "offers.json"), "w").write(json.dumps(offers, indent=1, ensure_ascii=False))
    sm = '<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n' + \
         "".join(f"  <url><loc>{u}</loc></url>\n" for u in urls) + "</urlset>\n"
    open(os.path.join(out, "sitemap.xml"), "w").write(sm)
    repo = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    lm = os.path.join(repo, "worker", "src", "links-map.json")
    os.makedirs(os.path.dirname(lm), exist_ok=True)
    open(lm, "w").write(json.dumps(links_map(), indent=1, ensure_ascii=False) + "\n")
    print(f"built {len(urls)} pages -> {out}; {len(PRODUCTS)} offers -> {os.path.relpath(lm, repo)}")
    flatten(out)


def flatten(out):
    """Also emit docs/ at the repo root: every page as a top-level <name>.html with extensionless
    links. GitHub Pages publishes main:/docs and serves /about -> about.html; keeping the site in
    docs/ keeps repo notes (CLAUDE.md, TODO.md, ...) off dealectric.com."""
    flat = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(out))), "docs")
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
