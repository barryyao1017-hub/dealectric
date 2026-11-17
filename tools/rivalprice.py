#!/usr/bin/env python3.12
"""Read today's price and stock for the rival rows of comparison (gap) pages: rows in src/gaps.py that name a maker URL
but are neither one of our product records (`slug`, priced by tokens) nor an Amazon row (`asin`, tools/amzprice.py).

For a Shopify product URL it reads the store's /products/<handle>.js (the URL's ?variant=, else the first available
variant, as tools/pricecheck.py); for any other page it reads the schema.org Offer in the page's JSON-LD. Read-only: it
writes a report and never edits src/. The row's current price is the first $ figure of its `price` cell.

    python3.12 tools/rivalprice.py --out growth/codes/<date>-rivals.json [--skip-pages file.json] [page-slug ...]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from gaps import GAP_PAGES  # noqa: E402

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
MONEY = re.compile(r"\$\s?([\d,]+(?:\.\d\d)?)")
JSON_HOST = {"www.soundcore.com": "us.soundcore.com"}


def curl(url: str) -> tuple[int, str]:
    p = subprocess.run(["curl", "-s", "-L", "--max-time", "30", "-A", UA, "-H", "Accept-Language: en-US,en;q=0.9",
                        "-w", "\n%{http_code}", url], capture_output=True, text=True, errors="replace")
    body, _, code = p.stdout.rpartition("\n")
    return (int(code) if code.isdigit() else 0), body


def shopify(url: str) -> dict:
    u = urllib.parse.urlsplit(url)
    want = urllib.parse.parse_qs(u.query).get("variant", [""])[0]
    host = JSON_HOST.get(u.netloc, u.netloc)
    js = f"{u.scheme}://{host}{u.path.rstrip('/')}.js"
    code, body = curl(js)
    if code != 200 or not body.lstrip().startswith("{"):
        first = code   # a 429 or a block: read the same JSON through r.jina.ai, as tools/pricecheck.py does
        for _ in range(2):
            time.sleep(4)
            code, body = curl("https://r.jina.ai/" + js)
            i = body.find("{")
            if code == 200 and i >= 0:
                body = body[i:]
                break
        else:
            return {"error": f"product JSON {first}; r.jina.ai {code}"}
    try:
        d = json.loads(body)
    except json.JSONDecodeError:
        return {"error": "product JSON did not parse"}
    vs = d.get("variants") or []
    v = next((x for x in vs if str(x["id"]) == want), None) if want else None
    if want and not v:
        return {"error": f"variant {want} not on the listing"}
    v = v or next((x for x in vs if x.get("available")), vs[0] if vs else None)
    if not v:
        return {"error": "no variants"}
    return {"live_price": v["price"] / 100, "live_compare": (v.get("compare_at_price") or 0) / 100 or None,
            "live_available": bool(v.get("available")), "variant": v["id"], "variant_title": v.get("title"),
            "variant_named": bool(want), "listing_title": d.get("title"), "source": "shopify",
            "variants": [{"id": x["id"], "title": x.get("title"), "price": x["price"] / 100, "available": bool(x.get("available"))}
                         for x in vs]}


def _offers(node, out):
    if isinstance(node, list):
        for x in node:
            _offers(x, out)
    elif isinstance(node, dict):
        if node.get("@type") in ("Offer", "AggregateOffer") or "price" in node or "lowPrice" in node:
            p = node.get("price", node.get("lowPrice"))
            if p not in (None, ""):
                try:
                    out.append((float(str(p).replace(",", "")), str(node.get("availability", ""))))
                except ValueError:
                    pass
        for k in ("offers", "@graph", "hasVariant", "mainEntity"):
            if k in node:
                _offers(node[k], out)


def jsonld(url: str) -> dict:
    code, body = curl(url)
    if code != 200:
        return {"error": f"page {code}"}
    found = []
    for m in re.finditer(r'<script[^>]+application/ld\+json[^>]*>(.*?)</script>', body, re.S | re.I):
        try:
            _offers(json.loads(m.group(1).strip()), found)
        except json.JSONDecodeError:
            continue
    found = [f for f in found if f[0] > 0]
    if not found:
        return {"error": "no schema.org Offer price on the page"}
    prices = sorted({f[0] for f in found})
    if len(prices) > 1:
        return {"error": f"several Offer prices on the page: {prices[:6]}"}
    avail = found[0][1]
    return {"live_price": prices[0], "live_available": (None if not avail else "InStock" in avail or "PreOrder" in avail),
            "source": "json-ld"}


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--skip-pages", default=None, help="JSON list of page slugs to leave out")
    ap.add_argument("--records", nargs="+", default=None, help="read these product records (src/products.py slugs) instead")
    ap.add_argument("pages", nargs="*")
    a = ap.parse_args()
    if a.records:
        from products import PRODUCTS
        by = {p["slug"]: p for p in PRODUCTS}
        rows = []
        for slug in a.records:
            p = by[slug]
            res = shopify(p["url"]) if "/products/" in p["url"] else jsonld(p["url"])
            rows.append({"slug": slug, "name": p["name"], "model": p.get("model"), "url": p["url"], "record_price": p.get("price"),
                         "cart_variant": p.get("cart_variant"), "read_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), **res})
            print(slug, res.get("live_price", res.get("error")), len(res.get("variants", [])), flush=True)
            time.sleep(2.5)
        Path(a.out).write_text(json.dumps({"date": dt.date.today().isoformat(), "rows": rows}, indent=1))
        return 0
    skip = set(json.load(open(a.skip_pages))) if a.skip_pages else set()
    rows, last = [], {}
    for g in GAP_PAGES:
        if g["slug"] in skip or (a.pages and g["slug"] not in a.pages):
            continue
        for i, r in enumerate(g.get("rows", [])):
            if r.get("slug") or r.get("asin") or not r.get("url"):
                continue
            cell = str(r.get("cells", {}).get("price", ""))
            m = MONEY.search(cell)
            host = urllib.parse.urlsplit(r["url"]).netloc
            wait = 2.5 - (time.time() - last.get(host, 0))
            if wait > 0:
                time.sleep(wait)
            res = shopify(r["url"]) if "/products/" in r["url"] else jsonld(r["url"])
            last[host] = time.time()
            row = {"page": g["slug"], "row": i, "brand": r.get("brand"), "model": r.get("model"), "url": r["url"],
                   "price_cell": cell or None, "shown_price": float(m.group(1).replace(",", "")) if m else None,
                   "read_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), **res}
            rows.append(row)
            print(f"{g['slug'][:40]:40} {str(r.get('model'))[:40]:40} {row.get('shown_price')} -> "
                  f"{row.get('live_price', row.get('error'))} avail={row.get('live_available')}", flush=True)
    Path(a.out).write_text(json.dumps({"date": dt.date.today().isoformat(), "rows": rows}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
