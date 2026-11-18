#!/usr/bin/env python3.12
"""Best-offer inputs for the BLUETTI items of bluetti_1118.py (DLC-321 phase 3, rule of DLC-320).

BLUETTI's own store offers a first-time buyer the same 5% our code gives ("Sign up now for 5% off your first order!" on
every product page, read 2026-11-18), so every entry is a tie: the page opens with our code price and makes no lowest
claim. A seller we cannot link that is cheaper is recorded as "beaten" by tools/bestoffer.py as usual.

    python3.12 growth/focus/offers/bluetti_bestoffer.py hand [--group 1,2] [--keep slug,...]       # writes the hand file for tools/bestoffer.py decide
    python3.12 growth/focus/offers/bluetti_bestoffer.py fallback [--group 1,2] [--keep slug,...]   # after decide: entries for slugs with no Google Shopping read

`fallback` exists because Google stopped the Shopping reads with a CAPTCHA part-way (never solved by tools): a slug
without a read gets the same tie entry from its cart test alone, marked with a note, so it still claims nothing.
"""
import json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path[:0] = [str(HERE), str(ROOT / "src")]
import bluetti_1118 as G  # noqa: E402
import build as B  # noqa: E402

DAY = G.DAY
HAND = ROOT / "growth" / "buylink" / f"{DAY}-bestoffer-hand-bluetti.json"
OWN = "bluettipower.com with BLUETTI's own 5% first-order sign-up offer and no link"
NOTE = ("BLUETTI's store offers 5% off a first order to anyone who signs up (banner on every product page, read 2026-11-18), "
        "the same 5% as code DEALECTRIC: a tie, no lowest line.")

if __name__ == "__main__":
    groups = {int(x) for x in sys.argv[sys.argv.index("--group") + 1].split(",")} if "--group" in sys.argv else None
    keep = set(sys.argv[sys.argv.index("--keep") + 1].split(",")) if "--keep" in sys.argv else None
    recs = G.records(groups, keep)[0]
    if sys.argv[1] == "hand":
        h = json.load(open(HAND)) if HAND.exists() else {}
        for d in recs:
            h[d["slug"]] = {"add": [[OWN, B.link_price(B.BY_SLUG[d["slug"]])]], "note": NOTE}
        HAND.write_text(json.dumps(dict(sorted(h.items())), indent=1, ensure_ascii=False) + "\n")
        print("hand entries:", len(h))
    elif sys.argv[1] == "fallback":
        path = ROOT / "src" / "bestoffer.json"
        out = json.loads(path.read_text())
        n = 0
        for d in recs:
            if d["slug"] in out["products"]:
                continue
            p = B.BY_SLUG[d["slug"]]
            ours, store = B.link_price(p), d["_runs"][0]["total"]
            out["products"][d["slug"]] = {"date": d["_test"]["date"], "sellers": [[OWN, ours], [f"{B.store_host(p)} without the link", store]],
                                          "tie": [OWN, ours], "note": "no Google Shopping read (Google asked for a CAPTCHA on 2026-11-18); entry from the cart test and the store's own offer"}
            n += 1
        path.write_text(json.dumps({"products": dict(sorted(out["products"].items()))}, indent=1) + "\n")
        print("fallback entries written:", n)
