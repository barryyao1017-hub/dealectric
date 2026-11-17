#!/usr/bin/env python3.12
"""Brand Black Friday deal pages (Barry, 2026-11-17): cart-test every way to pay for each product and keep the cheapest.

    python3.12 growth/bfcm/brandpages.py test [--only allpowers-black-friday-deals] [--slug <product slug>]
    python3.12 growth/bfcm/brandpages.py rows        # -> src/bfcm_brandpages.json (then python3.12 src/build.py)

`test` puts one unit of each product (the record's own cart variant) in the brand's US cart from a background tab of
the Agent Chrome (tools/codecheck_browser.py), first with a made-up control code, which shows what the store charges
with its automatic discounts alone, then with each candidate code. Results append to
growth/bfcm/brandpages/tests-<date>.jsonl. `rows` takes each product's latest test and picks the lowest cart total:
the store's own discount with no code, or a code (on these stores a code replaces the automatic discount instead of
adding to it, so the two are compared, never summed). A code whose total is no lower than the store's own discount is
listed as tested, not recommended, even when it is ours.

Page texts live in growth/bfcm/brandpages/spec.json; this script copies them into src/bfcm_brandpages.json with the rows.
"""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))
DIR = ROOT / "growth/bfcm/brandpages"
SPEC = DIR / "spec.json"
OUT = ROOT / "src/bfcm_brandpages.json"
CONTROL = "ZZNOTACODE7Q"

# Candidate codes per brand: ours first, then the network's own Black Friday codes that can beat it on some carts.
CODES = {
    "ALLPOWERS": ["DEALECTRIC10", "APBF12"],
    "BLUETTI": ["DEALECTRIC"],
    "Sun Gold Power": [],
}
EXTRA = {"bluetti-elite-300": ["EDME8"], "bluetti-ac180": ["AC180"]}   # product-only codes


def products_for(spec):
    import products as P
    out = []
    for p in P.PRODUCTS:
        if p["slug"] in P.RETIRED or str(p.get("program", "")).startswith("amazon") or p.get("price") is None:
            continue
        if p["brand"] in spec.get("brands", [p["brand"]]) and (not spec.get("categories") or p["category"] in spec["categories"]):
            out.append(p)
    return out


def cmd_test(args):
    import codecheck_browser as B
    spec = json.loads(SPEC.read_text())
    only = args[args.index("--only") + 1] if "--only" in args else None
    slug = args[args.index("--slug") + 1] if "--slug" in args else None
    today = dt.date.today().isoformat()
    DIR.mkdir(parents=True, exist_ok=True)
    seen = set() if "--force" in args else {s for s, rows in latest_tests().items() if rows and rows[0]["date"] == today
                                            and any(r.get("code") == CONTROL and r.get("subtotal") is not None for r in rows)}
    with open(DIR / f"tests-{today}.jsonl", "a") as f:
        for page in spec["pages"]:
            if only and page["slug"] != only:
                continue
            for p in products_for(page):
                if p["slug"] in seen or (slug and p["slug"] != slug) or "/products/" not in (p.get("url") or ""):
                    continue
                seen.add(p["slug"])
                codes = CODES.get(p["brand"], []) + EXTRA.get(p["slug"], [])
                for r in B.check_many(p["url"], codes, pause=4.0, variant=p.get("cart_variant") or p.get("variant")):
                    r.update({"slug": p["slug"], "date": today})
                    f.write(json.dumps(r) + "\n")
                    f.flush()
                    print(p["slug"], r.get("code"), r.get("applicable"), r.get("subtotal"), r.get("total"), str(r.get("error", ""))[:80], flush=True)


def latest_tests():
    """{slug: [rows of that product's most recent test date]}"""
    by = {}
    for f in sorted(DIR.glob("tests-*.jsonl")):
        for line in f.open():
            r = json.loads(line)
            if r.get("slug"):
                by.setdefault(r["slug"], {}).setdefault(r["date"], []).append(r)
    return {s: d[max(d)] for s, d in by.items()}


def best_row(slug, rows):
    ctrl = next((r for r in reversed(rows) if r.get("code") == CONTROL and r.get("subtotal") is not None and not r.get("applicable")), None)
    if not ctrl or any(r.get("void") for r in rows):
        return None
    store, auto = ctrl["subtotal"], ctrl["total"]
    codes = {}
    for r in rows:
        if r.get("code") not in (None, CONTROL) and r.get("applicable") and abs(r["subtotal"] - store) < 0.01:
            codes[r["code"]] = min(codes.get(r["code"], 1e12), r["total"])
    ranked = sorted(codes.items(), key=lambda kv: kv[1])
    if ranked and ranked[0][1] < auto - 0.004:
        best = {"how": "code", "code": ranked[0][0], "pay": ranked[0][1]}
        others = [{"code": c, "pay": t} for c, t in ranked[1:]]
    else:
        best = {"how": "auto" if auto < store - 0.004 else "none", "pay": auto}
        others = [{"code": c, "pay": t, "note": "no lower than the store's own price"} for c, t in ranked]
    tried = [r["code"] for r in rows if r.get("code") not in (None, CONTROL) and r.get("subtotal") is not None and not r.get("applicable")]
    others += [{"code": c, "pay": auto, "note": "not accepted"} for c in dict.fromkeys(tried) if c not in codes]
    return {"slug": slug, "store": store, "auto": auto, "best": best, "others": others, "tested": rows[0]["date"]}


def cmd_rows():
    spec = json.loads(SPEC.read_text())
    tests = latest_tests()
    pages = []
    for page in spec["pages"]:
        rows = []
        for p in products_for(page):
            r = best_row(p["slug"], tests.get(p["slug"], []))
            if r:
                rows.append(r)
        pages.append({**page, "rows": rows})
        print(f"{page['slug']}: {len(rows)} rows ({sum(1 for r in rows if r['best']['how'] == 'code')} by code)")
    OUT.write_text(json.dumps({"checked": max((r["tested"] for pg in pages for r in pg["rows"]), default=""), "pages": pages},
                              indent=1, ensure_ascii=False) + "\n")


if __name__ == "__main__":
    {"test": lambda: cmd_test(sys.argv[2:]), "rows": cmd_rows}[sys.argv[1]]()
