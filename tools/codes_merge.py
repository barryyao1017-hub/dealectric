#!/usr/bin/env python3
"""Fold cart-check logs (growth/codes/*.jsonl, written by tools/codecheck.py runs) into src/coupons.json.

Each code's `tests` list is rebuilt from the logs: one entry per (product, qty), keeping the latest check.
Codes in the log that coupons.json doesn't know yet are added from META below (or skipped with a warning).
Hand-entered tests (e.g. Tenergy, checked in the browser) are kept. Run after a sweep, then rebuild.

  python3 tools/codes_merge.py growth/codes/2026-10-21-checks.jsonl
"""
import json, os, sys
from urllib.parse import urlsplit

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(REPO, "src"))
from products import PRODUCTS  # noqa: E402

# Store handle -> our slug, where the store's handle differs from our product URL.
HANDLES = {"ac180": "bluetti-ac180", "15w-mini-wireless-charger": "esr-qi2-mini-wireless-charger-15w"}
for p in PRODUCTS:
    if "/products/" in p["url"]:
        HANDLES[urlsplit(p["url"]).path.rstrip("/").split("/products/")[1]] = p["slug"]

CJ, AWIN, SITES = "{}'s affiliate code (CJ Affiliate)", "{}'s affiliate code (Awin)", "coupon sites"
# Metadata for codes first seen in a log. result is set from the tests unless given ("inconclusive": the test product was
# outside the code's advertised scope, so a rejection proves nothing).
META = {
    ("ALLPOWERS", "EXTRA10"): dict(type="percent", value=10, terms="10% off power stations", categories=["power-station"], expires="2026-11-15", source=CJ.format("ALLPOWERS"), publish=True),
    ("ALLPOWERS", "BULKRATE"): dict(type="percent", value=11, terms="11% off when you buy 2 or more", min_qty=2, expires="2026-11-15", source=CJ.format("ALLPOWERS"), publish=True),
    ("ALLPOWERS", "EXTRA12"): dict(type="percent", value=12, terms="12% off orders over $1,200", min_order=1200, expires="2026-11-15", source=CJ.format("ALLPOWERS"), publish=True),
    ("ALLPOWERS", "AFFAP"): dict(type="percent", value=10, terms="10% off sitewide", source=SITES, publish=False),
    ("ALLPOWERS", "ALLPOWERSAF"): dict(type="percent", value=10, terms="10% off sitewide", source=SITES, publish=False),
    ("ALLPOWERS", "AFALLPOWERS"): dict(type="percent", value=10, terms="10% off sitewide", source=SITES, publish=False),
    ("ALLPOWERS", "10SAVEAF"): dict(type="percent", value=10, terms="10% off sitewide", source=SITES, publish=False),
    ("ALLPOWERS", "AFHZ8"): dict(type="percent", value=8, terms="8% off sitewide", source=SITES, publish=False),
    ("ALLPOWERS", "AFAK8"): dict(type="percent", value=8, terms="8% off sitewide", source=SITES, publish=False),
    ("ALLPOWERS", "BFEXTRA"): dict(type="percent", value=10, terms="10% off (as advertised)", source=SITES),
    ("ALLPOWERS", "AFAPSAS"): dict(type="percent", value=10, terms="10% off (as advertised)", source=SITES),
    ("BLUETTI", "NEW5"): dict(type="percent", value=5, terms="5% off sitewide", source=SITES, publish=False),
    ("BLUETTI", "SOUTH5"): dict(type="percent", value=5, terms="5% off sitewide", source=SITES, publish=False),
    ("BLUETTI", "HOMEBACKUP5"): dict(type="percent", value=5, terms="5% off sitewide", source=SITES, publish=False),
    ("BLUETTI", "PD5OFFEDM"): dict(type="percent", value=5, terms="5% off sitewide", source=SITES, publish=False),
    ("BLUETTI", "BACKUPSNS5"): dict(type="percent", value=5, terms="5% off sitewide", source=SITES, publish=False),
    ("BLUETTI", "exclusive5"): dict(type="percent", value=5, terms="5% off sitewide", source=SITES, publish=False),
    ("BLUETTI", "POWER6"): dict(type="percent", value=5, terms="5% off (advertised as 6%)", source=SITES, publish=False),
    ("BLUETTI", "power5"): dict(type="percent", value=5, terms="5% off", source=SITES, publish=False),
    ("BLUETTI", "power3"): dict(type="percent", value=3, terms="3% off", source=SITES, publish=False),
    ("BLUETTI", "EDME6"): dict(type="percent", value=6, terms="6% off Elite 400, B500K and RV5 (as advertised)", source=SITES, result="inconclusive"),
    ("Baseus", "NEW10OFF"): dict(type="percent", value=10, terms="10% off (advertised as a first-order code for email subscribers)", source=SITES, publish=False),
    ("Baseus", "NEXT15"): dict(type="percent", value=15, terms="15% off (advertised as a next-order code)", source=SITES, publish=False),
    ("Baseus", "NEW5OFF"): dict(type="percent", value=5, terms="5% off orders of $30 or more", source=SITES, publish=False),
    ("Baseus", "Thankyou15"): dict(type="percent", value=15, terms="15% off", source=SITES, publish=False),
    ("Baseus", "THANKYOU13"): dict(type="percent", value=13, terms="13% off", source=SITES, publish=False),
    ("Baseus", "CART12"): dict(type="percent", value=12, terms="12% off", source=SITES, publish=False),
    ("Baseus", "Baseus10"): dict(type="percent", value=10, terms="10% off", source=SITES, publish=False),
    ("Baseus", "HONEY10"): dict(type="percent", value=10, terms="10% off", source=SITES, publish=False),
    ("Baseus", "BEST15"): dict(type="percent", value=15, terms="15% off (as advertised)", source=SITES),
    ("Baseus", "BEST12"): dict(type="percent", value=12, terms="12% off (as advertised)", source=SITES),
    ("Baseus", "NEW12"): dict(type="percent", value=12, terms="12% off (as advertised)", source=SITES),
    ("Baseus", "BASEUS8"): dict(type="percent", value=8, terms="8% off (as advertised)", source=SITES),
    ("Baseus", "SAVE100"): dict(type="fixed", value=100, terms="$100 off orders over $500 (as advertised)", source=SITES),
    ("ESR", "xtendcar20ANI"): dict(type="percent", value=20, terms="20% off Xtend car chargers (as advertised)", source=SITES, result="inconclusive"),
    ("ESR", "SFS20"): dict(type="percent", value=20, terms="20% off 3+ final-sale items (as advertised)", source=SITES, result="inconclusive"),
    ("ESR", "FINAL20"): dict(type="percent", value=20, terms="20% off (as advertised)", source=SITES),
    ("ESR", "FINAL25"): dict(type="percent", value=25, terms="25% off (as advertised)", source=SITES),
    ("ESR", "CYBER25"): dict(type="percent", value=25, terms="25% off (as advertised)", source=SITES),
    ("ESR", "MBR15"): dict(type="percent", value=15, terms="15% off (as advertised)", source=SITES),
    ("ESR", "ESRS25"): dict(type="percent", value=25, terms="25% off (as advertised)", source=SITES),
    ("ESR", "CYHKD30"): dict(type="percent", value=30, terms="30% off (as advertised)", source=SITES),
    ("ESR", "AWIN20"): dict(type="percent", value=20, terms="20% off (as advertised)", source=SITES),
    ("Soundcore", "WSTD3035US"): dict(type="percent", value=10, terms="10% off eligible orders (as advertised)", source=SITES),
    ("Soundcore", "SOUNDCORE10"): dict(type="percent", value=10, terms="10% off the Liberty 4 NC (as advertised)", source=SITES, result="inconclusive"),
}
INCONCLUSIVE = {("ESR", "cyclone20ANI"), ("ESR", "xtend20ANI")}  # product-scoped codes tested on another product


def main(logs):
    path = os.path.join(REPO, "src", "coupons.json")
    data = json.load(open(path))
    by_key = {(c["brand"], c["code"]): c for c in data["codes"]}
    latest = {}
    for log in logs:
        for line in open(log):
            r = json.loads(line)
            if r.get("error") or r["code"] == "ZZNOTACODE7Q":
                continue
            slug = HANDLES.get(urlsplit(r["url"]).path.rstrip("/").split("/products/")[1])
            if not slug:
                print("unknown product", r["url"]); continue
            k = (r["brand"], r["code"], slug, r["qty"])
            if k not in latest or r["checked_at"] > latest[k]["checked_at"]:
                latest[k] = r
    logged = {}
    for (brand, code, slug, qty), r in latest.items():
        logged.setdefault((brand, code), []).append(
            {"date": r["checked_at"][:10], "product": slug, "qty": qty, "subtotal": r["subtotal"], "discount": r["code_amount"] if r["applicable"] else 0})
    for key, tests in logged.items():
        c = by_key.get(key)
        if not c:
            if key not in META:
                print("no metadata, skipped:", key); continue
            c = {"brand": key[0], "code": key[1], **META[key], "tests": []}
            data["codes"].append(c); by_key[key] = c
        hand = [t for t in c["tests"] if (t["product"], t["qty"]) not in {(x["product"], x["qty"]) for x in tests}]
        c["tests"] = sorted(hand + tests, key=lambda t: (t["product"], t["qty"]))
        if key in INCONCLUSIVE or META.get(key, {}).get("result") == "inconclusive":
            c["result"] = "inconclusive"
        else:
            c["result"] = "works" if any(t["discount"] > 0 for t in c["tests"]) else "rejected"
    order = {"works": 0, "rejected": 1, "inconclusive": 2}
    data["codes"].sort(key=lambda c: (order[c["result"]], not c.get("publish"), c["brand"], c["code"].upper()))
    with open(path, "w") as f:
        f.write('{\n "_notes": ' + json.dumps(data["_notes"], ensure_ascii=False) + ',\n "checked": ' + json.dumps(data["checked"]) + ',\n "codes": [\n')
        f.write(",\n".join("  " + json.dumps(c, ensure_ascii=False) for c in data["codes"]) + "\n ]\n}\n")
    n = {k: sum(c["result"] == k for c in data["codes"]) for k in order}
    print(f"{len(data['codes'])} codes: {n}; published: {[c['code'] for c in data['codes'] if c.get('publish') and c['result'] == 'works']}")


if __name__ == "__main__":
    main(sys.argv[1:])
