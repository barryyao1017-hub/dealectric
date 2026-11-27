#!/usr/bin/env python3.12
"""Weekly price and stock check (DLC-9): read every Shopify product record's live price and availability from the
store's /products/<handle>.js and list what differs from src/products.py. Read-only; it never edits the records.

    python3.12 tools/pricecheck.py [--out growth/codes/<date>-prices.json] [--stock-out src/stock.json] [slug ...]

--stock-out (DLC-201; the daily cart sweep runs it) writes {"date", "in_stock": {slug: bool}} for every record it could
read. build.py lets that read override a record's in_stock, so a sold-out product's /go/ link opens its sold_out_alt
and switches back by itself the day the store has it again. A record it could not read keeps its products.py value.

The variant is the one the record names (?variant= in its URL, else cart_variant). A record that names none is matched
to the listing by its name and price (pick_variant, shared with tools/freshapply.py), so a record whose own variant is
sold out reads sold out even while a sibling variant is in stock (DLC-306). Only when that match fails (titles and
price single out no variant, or the title match is priced too far from the record to be it) does the read fall back to
the first available variant, the rule the cart sweep uses; the row's `variant_how` says which rule chose. A store that answers 429 to this network (iallpowers.com and esrtech.com do to the work
laptop) is read through r.jina.ai instead. Non-Shopify stores (Tenergy, Amazon records) are listed as skipped.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
import subprocess
import sys
import threading
import time
from concurrent.futures import ThreadPoolExecutor
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
from products import PRODUCTS  # noqa: E402

JSON_HOST = {"www.soundcore.com": "us.soundcore.com"}
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"
JINA = "https://r.jina.ai/"
DEADLINE = 1200   # seconds; the sweep kills the read at 1500
MAX_MOVE = 0.25   # a title-only match priced further than this from the record is not taken as the record's variant


def _curl(url: str, extra: list[str] | None = None) -> tuple[int, str]:
    p = subprocess.run(["curl", "-s", "-4", "-L", "--max-time", "40", "-A", UA, *(extra or []), "-w", "\n%{http_code}", url],
                       capture_output=True, text=True, errors="replace")
    body, _, code = p.stdout.rpartition("\n")
    return (int(code) if code.isdigit() else 0), body


def jina(url: str, fmt: str = "text", meta: bool = False) -> tuple[int, str]:
    """One read of `url` through r.jina.ai, the outside reader the tools here fall back to when a store answers this
    network with a 429 (also tools/linkcheck.py). `fmt` is its X-Return-Format (text, html). With `meta` the answer is
    its JSON envelope: data.httpStatus (the store's own status), data.finalUrl, and data.text or data.html. Without a
    key r.jina.ai answers 20 requests a minute; the caller paces."""
    return _curl(JINA + url, ["-H", f"X-Return-Format: {fmt}"] + (["-H", "Accept: application/json"] if meta else []))


_JSON_CACHE: dict[str, tuple[dict | None, str]] = {}
_JSON_LOCK = threading.Lock()


def product_json(js_url: str) -> tuple[dict | None, str]:
    """One read per listing per run: records that are variants of one listing (BLUETTI's bundles) share it."""
    with _JSON_LOCK:
        if js_url in _JSON_CACHE:
            return _JSON_CACHE[js_url]
    r = _product_json(js_url)
    with _JSON_LOCK:
        _JSON_CACHE[js_url] = r
    return r


_LOCK = threading.Lock()
_HOST_NEXT: dict[str, float] = {}   # per store: when the next direct read may go
_BLOCKED: set[str] = set()           # stores that answered 429 this run: read through r.jina.ai from then on
_JINA_NEXT = [0.0]                   # r.jina.ai without a key takes 20 requests a minute in all
HOST_GAP, JINA_GAP = 1.5, 3.2


def _wait_slot(key, gap):
    with _LOCK:
        nxt = _HOST_NEXT.get(key, 0.0) if key != "jina" else _JINA_NEXT[0]
        now = time.monotonic()
        slot = max(nxt, now)
        if key == "jina":
            _JINA_NEXT[0] = slot + gap
        else:
            _HOST_NEXT[key] = slot + gap
    if slot > now:
        time.sleep(slot - now)


def _product_json(js_url: str) -> tuple[dict | None, str]:
    """DLC-358 (11-26): some stores answer every direct read from this machine with a 429 (iallpowers.com, us.ugreen.com,
    sungoldpower.com that day). A store that does is marked and read through r.jina.ai for the rest of the run, without
    retries that would hold up the other stores; each store is paced on its own, r.jina.ai on one shared pace."""
    host = urllib.parse.urlsplit(js_url).netloc
    via = "direct blocked earlier this run"
    if host not in _BLOCKED:
        _wait_slot(host, HOST_GAP)
        code, body = _curl(js_url)
        if code == 200 and body.lstrip().startswith("{"):
            return json.loads(body), "direct"
        if code == 429:
            _BLOCKED.add(host)
        via = f"direct {code}"
    for _ in range(2):
        _wait_slot("jina", JINA_GAP)
        code, body = jina(js_url)
        i = body.find("{")
        if code == 200 and i >= 0:
            try:
                return json.loads(body[i:]), via + ", read via r.jina.ai"
            except json.JSONDecodeError:
                pass
    return None, f"{via}; r.jina.ai {code}"


def _toks(t: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", str(t).lower()))


def pick_variant(model: str, variants: list[dict], shown: float | None):
    """The listing variant that is this model, as (variant, how) or (None, why). One variant: that one. Several: the
    variants whose titles fit the model best (model words present, extra words such as "Plus" or a bundle's panel count
    against); the one at the shown price among them if any (the price still holds), else the single best, else None."""
    if not variants:
        return None, "no variants read"
    if len(variants) == 1:
        return variants[0], "single variant"
    mt = _toks(model)
    def score(v):
        vt = _toks(v.get("title"))
        return len(mt & vt) - 0.5 * len(vt - mt)
    best = max(score(v) for v in variants)
    cands = [v for v in variants if score(v) == best]
    if shown is not None:
        same = [v for v in cands if abs(v["price"] - shown) < 0.01]
        if same:   # several equal fits at that price (colours): the record names none of them, the page opens on an available one
            return next((v for v in same if v.get("available")), same[0]), "variant at the shown price"
    if len(cands) == 1 and len(mt & _toks(cands[0].get("title"))) > 0:
        return cands[0], "variant title matches the model"
    return None, f"ambiguous variant ({len(variants)} on the listing, titles don't single out the model)"


def record_variant(p: dict, vs: list[dict]) -> tuple[dict | None, str]:
    """(variant, how) for a record that names no variant id, from the store's product JSON variants (prices in cents).

    The record's own variant is the one pick_variant() matches to its name and price. Two cases fall back to the first
    available variant, the old rule and what the product page opens on: no variant can be singled out, and a match by
    title alone whose price is more than MAX_MOVE from the record's (GardePro Link 1.0, 2026-11-17: the titles pointed
    at a $162.99 add-on camera for a $229.68 hub kit, which would have read an in-stock kit as sold out)."""
    if not vs:
        return None, "no variants"
    if len(vs) == 1:
        return vs[0], "single variant"
    price = float(p["price"]) if p.get("price") is not None else None
    pick, how = pick_variant(p.get("name") or "", [{"id": x["id"], "title": x.get("title"), "price": x["price"] / 100,
                                                    "available": bool(x.get("available"))} for x in vs], price)
    if pick is not None and price and how == "variant title matches the model" and abs(pick["price"] - price) / price > MAX_MOVE:
        pick, how = None, f"the title match {pick['title']!r} costs {pick['price']:g}, the record says {price:g}"
    if pick is None:
        return next((x for x in vs if x.get("available")), vs[0]), f"first available variant ({how})"
    return next(x for x in vs if x["id"] == pick["id"]), how


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
    if want:
        v, how = next((x for x in vs if str(x["id"]) == str(want)), None), "named in the record"
        if not v:
            return {**out, "error": f"variant {want} not on the listing", "via": via}
    else:
        v, how = record_variant(p, vs)
    if not v:
        return {**out, "error": "no variants", "via": via}
    live = v["price"] / 100
    out.update(live_price=live, live_compare=(v.get("compare_at_price") or 0) / 100 or None, live_available=bool(v.get("available")),
               variant=v["id"], variant_how=how, via=via)
    out["price_diff"] = p.get("price") is not None and abs(live - float(p["price"])) >= 0.01
    out["stock_diff"] = bool(v.get("available")) != bool(p.get("in_stock", True))
    return out


def main(argv: list[str]) -> int:
    args = [a for a in argv if not a.startswith("--")]
    outp = argv[argv.index("--out") + 1] if "--out" in argv else None
    stockp = argv[argv.index("--stock-out") + 1] if "--stock-out" in argv else None
    args = [a for a in args if a not in (outp, stockp)]
    # DLC-358 (11-26): read one store per thread, each store paced on its own and a store that answers 429 read through r.jina.ai (_product_json), so ~580 records
    # across ~100 stores finish well inside the sweep's 1500 s; past DEADLINE the rows read so far are written anyway
    # (the 11-18 to 11-26 runs read one record at a time, timed out every day and left stock.json at 11-18).
    todo = [p for p in PRODUCTS if not args or p["slug"] in args]
    by_host: dict[str, list[dict]] = {}
    for p in todo:
        by_host.setdefault(urllib.parse.urlsplit(p.get("url") or "").netloc, []).append(p)
    start, done = time.monotonic(), {}

    def run_host(ps):
        for p in ps:
            if time.monotonic() - start > DEADLINE:
                return
            r = check(p)
            done[p["slug"]] = r
            flag = ("SKIP " + r["skip"]) if "skip" in r else ("ERROR " + r["error"]) if "error" in r else (
                ("PRICE " if r["price_diff"] else "") + ("STOCK " if r["stock_diff"] else "") or "ok")
            live = f"{r['price']} -> {r['live_price']} avail={r['live_available']}" if "live_price" in r else ""
            print(f"{p['slug'][:60]:60} {flag} {live}", flush=True)

    with ThreadPoolExecutor(max_workers=8) as ex:
        list(ex.map(run_host, sorted(by_host.values(), key=len, reverse=True)))
    rows = [done[p["slug"]] for p in todo if p["slug"] in done]
    if len(rows) < len(todo):
        print(f"deadline: {len(todo) - len(rows)} records not read in {DEADLINE} s", flush=True)
    if outp:
        Path(outp).write_text(json.dumps({"date": _dt.date.today().isoformat(), "rows": rows}, indent=1))
    if stockp:
        read = {r["slug"]: r["live_available"] for r in rows if "live_available" in r}
        # UTC date, like the sweep's own date and VERIFIED comparisons in build.py
        Path(stockp).write_text(json.dumps({"date": _dt.datetime.now(_dt.timezone.utc).date().isoformat(),
                                            "in_stock": dict(sorted(read.items()))}, indent=1) + "\n")
        flips = [f"{r['slug']} {'back in stock' if r['live_available'] else 'sold out'}" for r in rows if r.get("stock_diff")]
        print(f"stock: {len(read)} read, {len(rows) - len(read)} unread; differs from products.py: {', '.join(flips) or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
