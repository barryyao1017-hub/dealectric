#!/usr/bin/env python3.12
"""Write src/buycompare.json (DLC-240 pilot) from a tools/buycheck.py report: for each named product, the other sellers'
prices a page shows beside the price through our link. Keeps the lowest price per trusted US retailer, Amazon included
(Barry 11-12: written permission to show Amazon prices; src/amazon_prices.json's read wins when the product has an ASIN),
at most four retailers, plus the brand store's own price without our link. build.py shows them as
"Lowest of N sellers checked <date>: ..." (Barry 11-13). Products whose verdict is not "cheapest" are refused unless --force.

    python3.12 tools/buycompare.py growth/buylink/<date>-cheapest.json slug [slug ...] [--force]
"""
from __future__ import annotations

import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import build as B  # noqa: E402

NAMES = [("amazon", "Amazon"), ("walmart", "Walmart"), ("best buy", "Best Buy"), ("bestbuy", "Best Buy"), ("newegg", "Newegg"),
         ("home depot", "Home Depot"), ("lowe", "Lowe's"), ("target", "Target"), ("b&h", "B&H"), ("costco", "Costco"),
         ("micro center", "Micro Center"), ("adorama", "Adorama"), ("rei", "REI"), ("sam's club", "Sam's Club")]


def retailer(merchant: str):
    m = merchant.lower()
    return next((n for k, n in NAMES if k in m), None)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("report"); ap.add_argument("slugs", nargs="+"); ap.add_argument("--force", action="store_true")
    ap.add_argument("--file", default="src/buycompare.json", help="src/buycompare_ab.json for the A/B-treated gap pages")
    a = ap.parse_args()
    rep = {r["slug"]: r for r in json.load(open(a.report))}
    date = re.search(r"(\d{4}-\d{2}-\d{2})", Path(a.report).name).group(1)
    path = ROOT / a.file
    out = json.loads(path.read_text()) if path.exists() else {"products": {}}
    for s in a.slugs:
        r, p = rep[s], B.BY_SLUG[s]
        if r.get("verdict") != "cheapest" and not a.force:
            print(f"refused {s}: verdict {r.get('verdict')}"); continue
        best = {}
        for c in r["cards"]:
            n = retailer(c["merchant"])
            if n and c["kind"] in ("retailer", "brand") and c["price"] < best.get(n, 1e9):
                best[n] = c["price"]
        amz = B.amz_price(p["asin"]) if p.get("asin") else None
        if amz and amz[2]:
            best["Amazon"] = amz[0]
        sellers = sorted(best.items(), key=lambda x: x[1])[:4]
        shown = r.get("brand_shown")   # the brand store's price as Google Shopping shows it today, else our record's
        sellers.append((f"{B.store_host(p)} without the link", float(shown) if shown not in (None, "", "None") else float(p["price"])))
        out["products"][s] = {"date": date, "sellers": [[n, x] for n, x in sellers]}
        print(s, out["products"][s])
    path.write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
