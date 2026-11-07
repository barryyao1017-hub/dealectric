#!/usr/bin/env python3.12
"""Weekly price and stock check (DLC-9): read every Shopify product record's live price and availability from the
store's /products/<handle>.js and list what differs from src/products.py. Read-only; it never edits the records.

    python3.12 tools/pricecheck.py [--out growth/codes/<date>-prices.json] [slug ...]

The variant is the one the record names (?variant= in its URL, else cart_variant), else the first available one, the
same rule the cart sweep uses. A store that answers 429 to this network (iallpowers.com and esrtech.com do to the work
laptop) is read through r.jina.ai instead. Non-Shopify stores (Tenergy, Amazon records) are listed as skipped.
"""
from __future__ import annotations

import datetime as _dt
import json
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from products import PRODUCTS  # noqa: E402

JSON_HOST = {"www.soundcore.com": "us.soundcore.com"}
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"


def _curl(url: str, extra: list[str] | None = None) -> tuple[int, str]:
    p = subprocess.run(["curl", "-s", "-4", "-L", "--max-time", "40", "-A", UA, *(extra or []), "-w", "\n%{http_code}", url],
                       capture_output=True, text=True, errors="replace")
    body, _, code = p.stdout.rpartition("\n")
    return (int(code) if code.isdigit() else 0), body


def product_json(js_url: str) -> tuple[dict | None, str]:
    code, body = _curl(js_url)
    if code == 200 and body.lstrip().startswith("{"):
        return json.loads(body), "direct"
    via = f"direct {code}"
    for _ in range(2):
        code, body = _curl("https://r.jina.ai/" + js_url, ["-H", "X-Return-Format: text"])
        i = body.find("{")
        if code == 200 and i >= 0:
            try:
                return json.loads(body[i:]), via + ", read via r.jina.ai"
            except json.JSONDecodeError:
                pass
        time.sleep(4)
    return None, f"{via}; r.jina.ai {code}"


def check(p: dict) -> dict:
    out = {"slug": p["slug"], "brand": p["brand"], "price": p.get("price"), "in_stock": p.get("in_stock", True)}
    if str(p.get("program", "")).startswith("amazon") or not p.get("url"):
        return {**out, "skip": "Amazon record or no URL"}
    u = urllib.parse.urlsplit(p["url"])
    if "/products/" not in u.path:
        return {**out, "skip": "not a Shopify product URL"}
    want = urllib.parse.parse_qs(u.query).get("variant", [""])[0] or p.get("cart_variant")
    host = JSON_HOST.get(u.netloc, u.netloc)   # as tools/linkcheck.py: www.soundcore.com's .js is its 404 page
    js = f"{u.scheme}://{host}{u.path.rstrip('/')}.js"
    d, via = product_json(js)
    if not d:
        return {**out, "error": via}
    vs = d.get("variants") or []
    v = next((x for x in vs if str(x["id"]) == str(want)), None) if want else None
    if want and not v:
        return {**out, "error": f"variant {want} not on the listing", "via": via}
    v = v or next((x for x in vs if x.get("available")), vs[0] if vs else None)
    if not v:
        return {**out, "error": "no variants", "via": via}
    live = v["price"] / 100
    out.update(live_price=live, live_compare=(v.get("compare_at_price") or 0) / 100 or None, live_available=bool(v.get("available")),
               variant=v["id"], via=via)
    out["price_diff"] = p.get("price") is not None and abs(live - float(p["price"])) >= 0.01
    out["stock_diff"] = bool(v.get("available")) != bool(p.get("in_stock", True))
    return out


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    outp = argv[argv.index("--out") + 1] if "--out" in argv else None
    if outp:
        args = [a for a in args if a != outp]
    rows = []
    for p in PRODUCTS:
        if args and p["slug"] not in args:
            continue
        r = check(p)
        rows.append(r)
        flag = ("SKIP " + r["skip"]) if "skip" in r else ("ERROR " + r["error"]) if "error" in r else (
            ("PRICE " if r["price_diff"] else "") + ("STOCK " if r["stock_diff"] else "") or "ok")
        live = f"{r['price']} -> {r['live_price']} avail={r['live_available']}" if "live_price" in r else ""
        print(f"{p['slug'][:60]:60} {flag} {live}", flush=True)
        time.sleep(1.5)
    if outp:
        Path(outp).write_text(json.dumps({"date": _dt.date.today().isoformat(), "rows": rows}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
