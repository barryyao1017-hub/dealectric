#!/usr/bin/env python3.12
"""Kits each partner store sells that we have no product record for (2026-11-17). Reads the store lists saved under
data/stores/ (Shopify /products.json for ALLPOWERS, OSCAL, Mango Power, Nature's Generator, Sun Gold Power; product
sitemaps for BLUETTI and Anker SOLIX, which give a URL but no price or stock). Writes data/uncovered-kits.json.

    python3.12 growth/focus/offers/store_kits.py
"""
import collections, json, re, sys, urllib.parse
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
S = ROOT / "growth/focus/offers/data/stores"
sys.path.insert(0, str(ROOT / "src"))
import products as P  # noqa: E402

ours = collections.defaultdict(set)
for p in P.PRODUCTS:
    u = urllib.parse.urlparse(p["url"])
    ours[u.netloc.replace("www.", "").replace("us.", "")].add(u.path.rstrip("/").split("/")[-1])

SHOPIFY = {"ALLPOWERS": ("iallpowers.com", r"solar generator.*(kit|\+|with .*panel)|\+ .*solar panel"),
           "OSCAL": ("store.oscal.hk", r"solar generator kit"),
           "Mango Power": ("mangopower.com", r"\bkit\b"),
           "Nature's Generator": ("www.naturesgenerator.com", r"system|\bkit\b|\+|bundle|with .*(panel|wind)"),
           "Sun Gold Power": ("sungoldpower.com", r"solar kit|bundle")}
out = []
for brand, (host, pat) in SHOPIFY.items():
    ps = json.load(open(S / f"{host}.p1.json"))["products"]
    have = ours[host.replace("www.", "")]
    for p in ps:
        if not re.search(pat, p["title"], re.I): continue
        price = min(float(v["price"]) for v in p["variants"])
        if price < 150: continue
        out.append(dict(brand=brand, title=p["title"].strip(), price=price, stock=any(v.get("available") for v in p["variants"]),
                        url=f"https://{host}/products/{p['handle']}", ours=p["handle"] in have))

def sitemap(brand, f, host, station, panel, drop):
    locs = sorted(set(re.findall(r"<loc>([^<]+)</loc>", open(S / f).read())))
    have = ours[host.replace("www.", "")]
    for l in locs:
        h = l.rstrip("/").split("/")[-1]
        if "/products/" not in l or re.search(drop, h) or not (re.search(station, h) and re.search(panel, h)): continue
        out.append(dict(brand=brand, title=h, price=None, stock=None, url=l, ours=h in have))

sitemap("BLUETTI", "bluetti-products.xml", "www.bluettipower.com",
        r"(^|-)(ac\d+[a-z]*|elite|apex|ep\d+|eb\d+[a-z]*|pioneer|premium|rv5|fridgepower)", r"pv\d+|sp\d+l?|\d{2,3}w(-|$)|solar", r"bulk-sale|cable|cms|copy|refurb|trade-in|power-station|charger|blush|glacier|sand-grey|meadow|twilight|green$")
sitemap("Anker SOLIX", "anker-products.xml", "www.ankersolix.com",
        r"(^|-)(c\d+|f\d+|e10)", r"solar-panel", r"refurb|cable|installation")
json.dump(out, open(ROOT / "growth/focus/offers/data/uncovered-kits.json", "w"), indent=0)
print(f"{'brand':20} kits  ours  missing  missing in stock  price range of missing")
for b in dict.fromkeys(o["brand"] for o in out):
    v = [o for o in out if o["brand"] == b]; m = [o for o in v if not o["ours"]]
    pr = [o["price"] for o in m if o["price"]]
    print(f"{b:20} {len(v):4} {sum(o['ours'] for o in v):5} {len(m):8} {sum(1 for o in m if o['stock']) if pr else '   ?':>17}  "
          + (f"${min(pr):,.0f} to ${max(pr):,.0f}" if pr else "not in the sitemap"))
if "-v" in sys.argv:
    for o in out:
        if not o["ours"] and o["stock"] is not False: print(f"  {o['brand'][:12]:12} {('$%.0f' % o['price']) if o['price'] else '':>7} {o['title'][:100]}")
