#!/usr/bin/env python3.12
"""Comparison pages for the BLUETTI products whose ChatGPT product panel shows no seller (Barry 2026-11-15, via the fork
session): ChatGPT types these rows without a catalog card, so the page it cites is the only way to buy. Each page targets
a search with demand, features the product honestly, and puts our /go/ link beside the product's name with the saving as
checkable text (record flag "buy_by_name", src/build.py checkable_offer; DLC-281 test).

Runs on growth/focus/open-pages/openpage.py (harvest from saved chats only, retarget mode, abpage research and gates):

    python3.12 growth/focus/bluetti-four/pages.py harvest|prep|research|links|apply [folder...]
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "growth/focus/open-pages"))
import openpage as O  # noqa: E402

RUNS = "/Users/j0y0825/code/dealectric/growth/evals/runs/"
RUN = "bluetti-1115"


def brief(*keys):
    out = []
    for k in keys:
        d = json.loads((HERE / f"{k}.json").read_text())
        out.append({"product": d.get("product"), "price_today": d.get("price_today"), "wins": d.get("wins"), "weak": d.get("weak"),
                    "wins_for": d.get("wins_for"), "not_for": d.get("not_for"), "rivals": d.get("rivals")})
    return json.dumps(out, ensure_ascii=False)[:30000]


def rules(target, demand, featured, extra):
    return f"""## Rules for this page (BLUETTI pages, Barry 2026-11-15)
- Target search: "{target}" (demand: {demand}). Title and H1 in plain shopper words built on that search, no model numbers;
  the answer's first sentence keeps the search's words.
- Featured product: {featured}. Its row must be in the table with its measured strengths and its weak points stated
  plainly. The pick is whatever wins the page's question on the evidence; if the featured product does not win the
  headline need, show the shopper need it does win and say which product wins the headline. Never bend a finding toward
  a product we earn on.
- The table's figures each carry their source (named reviewer or lab, the maker's page or manual) and the date read, in
  the cell; derived figures are labelled arithmetic with the one-line sum in the after-section.
- Dealectric does not test units. Say so once in the after-section; never imply a test.
- Rows for products we list use their slug (the renderer prints the store price, the price through our link, the code
  and the cart-test date beside the product name). Don't restate our prices in cells.
- {extra}
## Product research done for this run (verify any figure you use at its source)
""" + "{brief}"


PAGES = {
    "best-bluetti-power-station": {
        "retarget": True, "run": RUN, "flags": {"buy_by_name": True},
        "query": "which bluetti power station should i buy",
        "files": [RUNS + "2026-11-07-liveplain-rest/chatgpt/pl-122-best-bluetti-power-station--plain-1.json"],
        "rules": rules("bluetti power station", "5,404 Bing searches in 13 weeks; 'bluetti solar generator' 449; 'bluetti portable "
                       "power station' 227", "BLUETTI's current US lineup, above all the Elite 30 V2 (and its 100 W panel kit), "
                       "the Elite 100 V2 and the Elite 200 V2 (and its panel kits)",
                       "This page answers which BLUETTI to buy for which need: one row per current model on BLUETTI's US store "
                       "(each with the need it fits), kits with panels where BLUETTI sells them as one item. The AC70 is listed "
                       "on BLUETTI's US store at $359 but every variant was unavailable and its cart refused it on 2026-11-15: "
                       "mention it only as unavailable. Include where a rival brand beats BLUETTI for a need, briefly.")
                 .format(brief=brief("elite-30-v2", "elite-100-v2", "elite-200-v2")),
    },
    "best-2000wh-power-station": {
        "retarget": True, "run": RUN, "flags": {"buy_by_name": True},
        "query": "best 2000 watt portable power station",
        "files": [RUNS + "2026-11-14-openq/chatgpt/pm029-which-2000-watt-hour-power-station-is-the-chea.json"],
        "rules": rules("portable power station 2000w", "247 Bing searches in 13 weeks; shortlist cluster 1,217", "BLUETTI Elite 200 V2 "
                       "(2,073.6 Wh, 2,600 W)", "Shoppers say '2000 watt' for either output watts or watt-hours; answer both "
                       "readings in one short line and compare the stations that are about 2,000 Wh and 2,000 W or more.")
                 .format(brief=brief("elite-200-v2")),
    },
    "bl-portable-power-station-1000w": {
        "run": RUN, "flags": {"buy_by_name": True},
        "query": "best 1000 watt portable power station",
        "files": [RUNS + "2026-11-14-openq/chatgpt/pm005-which-1000-watt-hour-power-station-is-the-smal.json",
                  RUNS + "2026-11-15-openq-confirm/chatgpt/pm005-which-1000-watt-hour-power-station-is-the-smal.json",
                  RUNS + "2026-11-15-openq-third/chatgpt/pm005-which-1000-watt-hour-power-station-is-the-smal.json",
                  RUNS + "2026-11-14-openq/chatgpt/pm021-which-power-station-under-500-dollars-runs-the.json"],
        "rules": rules("portable power station 1000w", "301 Bing searches in 13 weeks; shortlist cluster 1,483", "BLUETTI Elite 100 V2 "
                       "(1,024 Wh, 1,800 W)", "Shoppers say '1000 watt' for either output watts or watt-hours; answer both "
                       "readings in one short line and compare the 1 kWh-class stations. Slug: portable-power-station-1000w.")
                 .format(brief=brief("elite-100-v2")),
    },
}
O.PAGES.update(PAGES)
O.IN_SCOPE |= set(PAGES)

if __name__ == "__main__":
    sys.argv = [sys.argv[0], *sys.argv[1:]] if len(sys.argv) > 2 else [sys.argv[0], sys.argv[1], *PAGES]
    sys.exit(O.main())
