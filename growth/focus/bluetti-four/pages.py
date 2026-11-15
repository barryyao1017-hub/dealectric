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
    "best-home-battery-backup-system": {
        "retarget": True, "run": RUN, "flags": {"buy_by_name": True},
        "query": "best home battery backup system",
        "files": [RUNS + "2026-11-07-liveplain-rest/chatgpt/pl-131-best-home-battery-backup-system--plain-1.json",
                  RUNS + "2026-11-14-openq/chatgpt/ac019-what-is-the-best-home-battery-backup-system.json",
                  RUNS + "2026-11-14-openq/chatgpt/vq000-home-battery-backup-system.json",
                  RUNS + "2026-11-14-openq/chatgpt/vq007-best-battery-backup-for-home.json",
                  RUNS + "2026-11-14-openq/chatgpt/vq013-best-home-battery-backup.json"],
        "rules": rules("home battery backup system", "'home backup battery systems' 2,214 Bing searches in 13 weeks; 'battery backup "
                       "for home' 2,053; 'home battery backup for power outages' 392; 'whole house battery backup' 437",
                       "the Jackery Explorer 5000 Plus (Amazon B0DFGLG35L), the EcoFlow DELTA 3 Ultra (Amazon B0FQVBFLHL) and the "
                       "OUPES Mega 1 (Amazon B0DG8JQNS4), which ChatGPT names for home backup",
                       "Compare plug-in home backup batteries (portable power stations sized for a home) by a measured result that "
                       "decides home backup: usable energy delivered, idle draw with the inverter on, and 240 V capability. Rows for "
                       "products we list on Amazon use their slugs: jackery-explorer-5000-plus, ecoflow-delta-3-ultra, oupes-mega-1; "
                       "BLUETTI and Anker rows use our program slugs where we list them (bluetti-apex-300, bluetti-apex-300-b300k, "
                       "anker-solix-s5000, anker-solix-f3800-plus). Installed systems (Tesla Powerwall, Enphase) may appear as "
                       "context rows without links. No $ figure in the text for an Amazon product.")
                 .format(brief=brief("explorer-5000-plus", "delta-3-ultra", "oupes-mega-1")),
    },
    "bl-jackery-power-station": {
        "run": RUN, "flags": {"buy_by_name": True}, "query": "which jackery power station should i buy",
        "web": [("Just don't immerse it: Jackery reveals world's lightest kWh-capacity IP65 power station", "https://www.techradar.com/pro/just-dont-immerse-it-jackery-reveals-worlds-lightest-kwh-capacity-ip65-rated-portable-power-station-and-it-can-even-withstand-a-1m-fall"),
                ("Jackery HomePower 1000 Plus V2 review", "https://www.gearbrain.com/amp/jackery-homepower-1000-plus-v2-2677792853"),
                ("Jackery launches rugged Explorer 1500 Ultra", "https://www.notebookcheck.net/Jackery-launches-rugged-Explorer-1500-Ultra-power-station-with-3-600W-peak-output.1191310.0.html"),
                ("Jackery Explorer 1500 Ultra", "https://www.protoolreviews.com/jackery-explorer-1500-ultra/"),
                ("Jackery unveils Explorer 1000 v2", "https://www.notebookcheck.net/Jackery-unveils-Explorer-1000-v2-power-station-utilizing-LFP-batteries-and-AI-controlled-charging.879414.0.html"),
                ("Jackery portable power station gear review", "https://www.10adventures.com/jackery-portable-power-station-gear-review/"),
                ("Jackery Explorer 300 Plus", "https://www.rei.com/product/238341"),
                ("Introducing Jackery Portable Power Stations: What, Why and How Much", "https://www.jackery.com/blogs/news/introducing-jackery-portable-power-stations-what-why-and-how-much"),
                ("Jackery's No. 1 bestselling power station", "https://tech.yahoo.com/general/articles/jackerys-no-1-bestselling-power-233000620.html")],
        "rules": rules("jackery power station", "'jackery power station' 4,146, 'jackery solar generator' 3,108, 'jackery portable power "
                       "station' 2,039, 'jackery solar generator 5000 plus' 146 Bing searches in 13 weeks", "Jackery's current US lineup, "
                       "above all the Explorer 5000 Plus (our record jackery-explorer-5000-plus, Amazon)",
                       "This page answers which Jackery to buy for which need: one row per current Jackery model, each with the "
                       "need it fits and a measured figure. Jackery is not a program we have: rows link our Amazon records "
                       "(jackery-explorer-5000-plus, jackery-explorer-1000-v2) or, for other models, plain rows with the maker url "
                       "(the run adds a confirmed Amazon listing where one exists). If another brand clearly beats Jackery for a "
                       "need, say so in one line. No $ figure in the text for an Amazon product. The Explorer 300D: Jackery's store "
                       "sells it for less than Amazon; don't feature an Amazon link for it. Slug: which-jackery-power-station-to-buy.")
                 .format(brief=brief("explorer-5000-plus")),
    },
    "bl-ecoflow-power-station": {
        "run": RUN, "flags": {"buy_by_name": True}, "query": "which ecoflow power station should i buy",
        "web": [("EcoFlow power stations at a glance", "https://solarkontor.de/en/pages/ratgeber-ecoflow-powerstations"),
                ("EcoFlow Delta Pro, RIVER Pro & WAVE AC review", "https://www.trailandkale.com/gear/ecoflow-review-portable-power-stations/"),
                ("EcoFlow collection", "https://www.shopsolarkits.com/collections/ecoflow"),
                ("EcoFlow DELTA Max review", "https://explorersweb.com/ecoflow-delta-max/"),
                ("EcoFlow DELTA 3 Plus review", "https://tech.yahoo.com/home/articles/ecoflow-delta-3-plus-review-110015757.html"),
                ("EcoFlow Trail 300 DC now available", "https://www.notebookcheck.net/EcoFlow-Trail-300-DC-compact-power-station-now-available.1078339.0.html"),
                ("EcoFlow RIVER 2 Pro", "https://www.rei.com/product/226839"),
                ("EcoFlow reviews", "https://www.techradar.com/tag/ecoflow"),
                ("EcoFlow RIVER 3 Plus launches", "https://www.notebookcheck.net/EcoFlow-River-3-Plus-EcoFlow-s-new-portable-power-station-launches-with-286-Wh-capacity.986745.0.html")],
        "rules": rules("ecoflow power station", "'ecoflow power station' 2,504, 'ecoflow solar generator' 171, 'ecoflow portable power "
                       "station' 139 Bing searches in 13 weeks", "EcoFlow's current US lineup, above all the DELTA 3 Ultra (our record "
                       "ecoflow-delta-3-ultra, Amazon)",
                       "This page answers which EcoFlow to buy for which need: one row per current EcoFlow model (RIVER 3, RIVER 3 "
                       "Plus, DELTA 3, DELTA 3 Plus, DELTA 3 Max, DELTA 3 Ultra, DELTA Pro 3, DELTA Pro Ultra), each with the need it "
                       "fits and a measured figure. EcoFlow is not a program we have: rows link our Amazon records (ecoflow-river-3-245wh, "
                       "ecoflow-delta-3-1024wh, ecoflow-delta-3-plus-1024wh, ecoflow-delta-2-max, ecoflow-delta-3-ultra) or plain rows "
                       "with the maker url. If another brand clearly beats EcoFlow for a need, say so in one line. No $ figure in the "
                       "text for an Amazon product. Slug: which-ecoflow-power-station-to-buy.")
                 .format(brief=brief("delta-3-ultra")),
    },
    "bl-oupes-power-station": {
        "run": RUN, "flags": {"buy_by_name": True}, "query": "oupes portable power station",
        "web": [("TLDR Review: OUPES Exodus 1200 Power Station", "https://shopsavvy.com/reviews-tldr/oupes-exodus-1200-power-station.md"),
                ("Portable Power Stations For Off-Grid Living - OUPES", "https://oupes.com/pages/off-grid-power-station"),
                ("Portable Power Station - OUPES", "https://oupes.com/collections/portable-power-station?page=2"),
                ("OUPES power station review", "https://nerdtechy.com/oupes-power-station-review"),
                ("OUPES Portable Power Station 1100W Review", "https://maketecheasier.com/review/oupes-portable-power-station/"),
                ("OUPES Mega Series Portable Power Stations", "https://oupes.com/products/oupes-2400w-portable-power-station"),
                ("Portable Solar Company Touts New Power Station", "https://rv-pro.com/news/portable-solar-company-touts-new-power-station/"),
                ("Review of the OUPES Exodus 1200", "https://www.activegearreview.com/electronics/oupes-exodus-1200-review/"),
                ("Exodus 1200", "https://ca.oupes.com/products/exodus-1200")],
        "rules": rules("oupes portable power station", "'oupes portable power station' 457, 'oupes' 887, 'oupes power station' 30 Bing "
                       "searches in 13 weeks", "the OUPES Mega 1 (our record oupes-mega-1, Amazon)",
                       "This page answers which OUPES power station to buy for which need: the current Mega and Exodus models, each "
                       "with the need it fits and a measured figure, plus the closest rival from another brand where it beats OUPES. "
                       "OUPES is not a program we have: rows link our Amazon record oupes-mega-1 or plain rows with the maker url. "
                       "Note where OUPES's own store and Amazon differ in price only from pages you read today, and no $ figure in "
                       "the text for an Amazon product. Slug: oupes-portable-power-station.")
                 .format(brief=brief("oupes-mega-1")),
    },
}
O.PAGES.update(PAGES)
O.IN_SCOPE |= set(PAGES)

if __name__ == "__main__":
    sys.argv = [sys.argv[0], *sys.argv[1:]] if len(sys.argv) > 2 else [sys.argv[0], sys.argv[1], *PAGES]
    sys.exit(O.main())
