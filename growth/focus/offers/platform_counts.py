#!/usr/bin/env python3.12
"""Platform counts for buying phrases (2026-11-17): exact Bing US searches over the latest 13 weeks (Bing Webmaster
GetKeywordStats, one keyword per call, single caller) for the phrases behind offers rather than long questions:
<brand> discount / coupon / promo code, category deal phrases, kit phrases, <model> price. Resumes from
data/keywords.json. A keyword with no rows is below Bing's reporting threshold (stored as 0); a failed call is null.\n"broad" is Bing's broad-match count for the same weeks (searches that contain the phrase's words), "weeks" the rows returned.

    python3.12 growth/focus/offers/platform_counts.py
"""
import json, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "growth/evals")); sys.path.insert(0, str(ROOT / "src"))
import gapmine as G  # noqa: E402
import products as P  # noqa: E402
OUT = ROOT / "growth/focus/offers/data/keywords.json"

brands = sorted({p["brand"] for p in P.PRODUCTS if not p["program"].startswith("amazon")})
kw = {}
for b in brands:
    for form in ("discount code", "coupon code", "promo code"):
        kw[f"{b.lower()} {form}"] = ("code", b)
for b in ["BLUETTI", "ALLPOWERS", "Anker SOLIX", "OSCAL", "Growatt", "Nature's Generator", "Mango Power", "Jackery", "EcoFlow"]:
    kw[f"{b.lower()} black friday"] = ("brand-deal", b)
    kw[f"{b.lower()} solar generator"] = ("brand-kit", b)
    kw[f"{b.lower()} sale"] = ("brand-deal", b)
DEALS = ["power station black friday", "solar generator black friday", "solar generator black friday deals",
         "portable power station black friday deals", "solar generator deals", "power station deals",
         "portable power station deals", "solar generator sale", "best solar generator deals", "nas black friday deals",
         "3d printer black friday deals", "3d printer deals", "projector black friday deals", "headphones black friday deals",
         "power bank deals", "robot mower deals", "robot lawn mower black friday", "security camera deals",
         "lifepo4 battery black friday", "lifepo4 battery deals", "3d scanner deals", "kvm switch deals",
         "smartwatch black friday deals", "dehumidifier deals", "solar panel deals", "home battery backup deals"]
KITS = ["solar generator kit", "solar generator with solar panels", "power station and solar panel",
        "portable power station with solar panel included", "solar generator bundle", "power station bundle",
        "solar generator kit for home", "solar generator kit for rv", "solar generator kit for camping",
        "best solar generator kit", "home battery backup with solar panels", "off grid solar kit with battery",
        "solar kit with battery", "complete solar kit", "rv solar kit with battery", "shed solar kit", "cabin solar kit",
        "solar generator for camping with panels", "solar generator with panels for home", "solar generator with panels for rv",
        "1000w solar generator with panels", "2000w solar generator with panels", "3000w solar generator with panels",
        "bluetti ac180 solar panel", "bluetti ac200l solar panel", "bluetti elite 200 v2 solar panel", "allpowers r2500",
        "allpowers p1800", "allpowers solar generator kit", "bluetti solar generator kit", "anker solix c1000 solar panel",
        "anker solix f3800 solar panels", "anker solix solar generator kit", "oscal powermax", "mango power e",
        "nature's generator powerhouse",
        "nas with hard drives included", "3d printer starter kit", "3d printer bundle", "projector and screen bundle",
        "security camera kit", "security camera system with monitor", "robot mower with garage", "trolling motor battery kit",
        "lifepo4 battery with charger", "golf cart lithium battery conversion kit", "rv lithium battery kit",
        "dash cam front and rear with hardwire kit", "3d scanner bundle", "portable monitor bundle", "kvm switch with cables"]
PRICE = ["bluetti ac180 price", "bluetti elite 200 v2 price", "bluetti ac200l price", "allpowers r2500 price",
         "anker solix f3800 price", "anker solix c1000 price", "ecoflow delta pro 3 price", "jackery 2000 plus price",
         "bluetti apex 300 price", "solar generator price", "power station price", "bluetti price history",
         "is bluetti black friday sale worth it", "best time to buy solar generator", "when do solar generators go on sale"]
for k in DEALS: kw[k] = ("deal", "")
for k in KITS: kw[k] = ("kit", "")
for k in PRICE: kw[k] = ("price", "")

done = json.load(open(OUT)) if OUT.exists() else {}
ORDER = {"kit": 0, "deal": 1, "brand-kit": 2, "brand-deal": 3, "price": 4, "code": 5}
FIRST = ["BLUETTI", "ALLPOWERS", "Anker SOLIX", "OSCAL", "Mango Power", "Nature's Generator", "Growatt", "Sun Gold Power", "Mobile Pixels", "Anker", "UGREEN", "soundcore"]
todo = sorted((k for k in kw if done.get(k, {}).get("n") is None or "broad" not in done[k]),
              key=lambda k: (ORDER[kw[k][0]], FIRST.index(kw[k][1]) if kw[k][1] in FIRST else 99, not k.endswith("discount code")))
print(len(kw), "keywords,", len(todo), "to ask", flush=True)
for i, k in enumerate(todo):
    d = G.bwt("GetKeywordStats", q=k, country="us", language="en-US")
    time.sleep(0.3)
    wk = [] if d is None else sorted(d, key=lambda x: G._ms(x["Date"]))[-13:]
    n = None if d is None else sum(x.get("Impressions") or 0 for x in wk)
    done[k] = {"kind": kw[k][0], "brand": kw[k][1], "n": n, "broad": sum(x.get("BroadImpressions") or 0 for x in wk), "weeks": len(wk)}
    if i % 20 == 0 or n:
        print(i, k, n, done[k]["broad"], flush=True)
    if i % 10 == 0:
        json.dump(done, open(OUT, "w"), indent=0)
json.dump(done, open(OUT, "w"), indent=0)
print("DONE", sum(1 for v in done.values() if v["n"]), "with volume;", sum(1 for v in done.values() if v["n"] is None), "failed")
