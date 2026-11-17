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


SPEC = re.compile(r"(\d+(?:\.\d+)?)\s*(mah|wh|kwh|ah|w|v|k)\b", re.I)


def specs(t: str) -> dict:
    out = {}
    for n, u in SPEC.findall(re.sub(r"(?<=\d),(?=\d{3})", "", t or "")):   # "1,024 Wh"
        out.setdefault(u.lower(), set()).add(float(n))
    return out


def same_item(card_title: str, product_name: str) -> bool:
    """A card for a sibling model (10000 mAh vs our 25000 mAh, 2K vs 4K) shares the name but not the spec: reject a card
    that states a capacity, wattage or resolution the product's own name contradicts (11-17, Baseus FC41)."""
    ps, cs = specs(product_name), specs(card_title)
    near = lambda x, vs: any(abs(x - v) <= 0.02 * v for v in vs)   # "1451.6 Wh" is the 1,451 Wh unit
    return all(any(near(x, ps[u]) for x in cs[u]) for u in cs if u in ps)   # "25W wireless, 45W cable" names ours too


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
        name = f"{p.get('brand', '')} {p.get('name', '')} {s.replace('-', ' ')}"
        cards = [c for c in r["cards"] if same_item(c["title"], name)]
        for c in r["cards"]:
            if c not in cards:
                print(f"  {s}: dropped other-item card {c['merchant']} ${c['price']} {c['title'][:80]}")
        if not a.force and any(c["price"] < float(r["after"]) for c in cards if c["kind"] in ("retailer", "brand")):
            print(f"refused {s}: a same-item card is below our price"); continue
        brand_cards = [c["price"] for c in cards if c["kind"] == "brand"]
        if r.get("brand_shown") not in (None, "", "None") and float(r["brand_shown"]) not in brand_cards:
            r["brand_shown"] = min(brand_cards) if brand_cards else None   # the brand price was read off another item's card
        best = {}
        for c in cards:
            n = retailer(c["merchant"])
            if n and c["kind"] in ("retailer", "brand") and c["price"] < best.get(n, 1e9):
                best[n] = c["price"]
        amz = B.amz_price(p["asin"]) if p.get("asin") else None
        if amz and amz[2]:
            best["Amazon"] = amz[0]
        sellers = sorted(best.items(), key=lambda x: x[1])[:4]
        shown = r.get("brand_shown")   # the brand store's price as Google Shopping shows it today, else our record's
        if shown not in (None, "", "None") and r.get("list") and float(shown) > 1.10 * float(r["list"]):
            print(f"  {s}: brand card ${shown} is over 10% above the store price we read (${r['list']}): a bundle or another item, using ours")
            shown = None
        sellers.append((f"{B.store_host(p)} without the link", float(shown) if shown not in (None, "", "None") else float(p["price"])))
        out["products"][s] = {"date": date, "sellers": [[n, x] for n, x in sellers]}
        print(s, out["products"][s])
    path.write_text(json.dumps(out, indent=1) + "\n")


if __name__ == "__main__":
    main()
