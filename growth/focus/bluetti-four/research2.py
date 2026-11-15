"""Product research, second batch (Barry 11-15 via the fork session): the products ChatGPT names whose catalog record it
probably lacks (never seen with a card or a panel seller in ~400 saved chats) and that we can link. One Opus 5.5 high
agent per product, same rules as the angle agents. Besides where the product wins and which searches to target, each
agent returns a product record for src/products.py: BLUETTI ones on our Awin program, the others as Amazon Associates
records on the brand's own Amazon listing (confirmed later with combopage.amazon_verify). Output: <key>.json here."""
import json, subprocess, sys, concurrent.futures as cf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import abpage as A
OUT = Path(__file__).resolve().parent

PRODUCTS = {
    "pioneer-na": ("BLUETTI Pioneer Na", "Pioneer Na", "bluetti",
                   "BLUETTI US store: https://www.bluettipower.com/products/sodium-ion-battery-pioneer-na ($700.00 on 2026-11-15, variant "
                   "47699009143003, in stock); a +200 W panel bundle at https://www.bluettipower.com/products/pioneer-na-200w ($999). "
                   "Program awin:bluetti_us, code DEALECTRIC (5%). ChatGPT typed it 9 times, mostly for charging in freezing weather."),
    "elite-100-mini": ("BLUETTI Elite 100 mini", "Elite 100 mini", "bluetti",
                       "BLUETTI US store: https://www.bluettipower.com/products/elite-100-mini-portable-power-station ($429.00 on "
                       "2026-11-15, variant 49212162277595, in stock; 1,004 Wh, 700 W). Program awin:bluetti_us, code DEALECTRIC (5%)."),
    "explorer-5000-plus": ("Jackery Explorer 5000 Plus", "5000 Plus", "amazon",
                           "Amazon listing B0DFGLG35L ('Jackery Explorer 5000 Plus Power Station, 5040Wh, 7200W AC Output'), "
                           "already confirmed as the same item; Amazon price $3,499 on 2026-11-15. ChatGPT typed it 28 times."),
    "explorer-300d": ("Jackery Explorer 300D", "300D", "amazon", "Find Jackery's own Amazon listing (sold by Jackery or Amazon)."),
    "delta-3-ultra": ("EcoFlow DELTA 3 Ultra", "DELTA 3 Ultra", "amazon", "Find EcoFlow's own Amazon listing (sold by EcoFlow or Amazon)."),
    "delta-3-plus-220w": ("EcoFlow DELTA 3 Plus + 220 W solar panel bundle", "DELTA 3 Plus", "amazon",
                          "We already list the DELTA 3 Plus alone on Amazon (B0DCC2BVFW). Find EcoFlow's own Amazon listing for the "
                          "DELTA 3 Plus + 220 W bifacial panel bundle; if Amazon has no such bundle from EcoFlow, say so."),
    "oupes-mega-1": ("OUPES Mega 1", "Mega 1", "amazon", "Find OUPES's own Amazon listing (sold by OUPES or Amazon)."),
}
DEMAND = """Bing search counts (13 weeks; growth/gapmine/runs/pool/volume.json, the main session's shortlist):
jackery power station 4,146; jackery solar generator 3,108; jackery portable power station 2,039; jackery solar generator 5000 plus 146; jackery explorer 300d 14;
ecoflow power station 2,504; ecoflow solar generator 171; ecoflow portable power station 139; ecoflow delta 3 plus portable power station 39;
oupes 887; oupes portable power station 457; oupes power station 30;
bluetti power station 5,404; bluetti solar generator 449; bluetti portable power station 227;
solar generators for home use 2,796 (cluster 20,539); home backup battery systems 2,214; best portable power station for home backup 400; whole house battery backup 437; whole house battery backup without solar 317; solar generator for whole house 221;
solar generator with panels 3,192; portable power station 1000w 301; portable power station 2000w 247; solar generator for camping 700;
portable power station with ac outlet 1,049; solar generator for rv 260; solar generator for refrigerator 218; home battery backup for power outages 392.
No search with volume found for: sodium-ion, cold-weather or winter power stations, Pioneer Na, Elite 100 mini, DELTA 3 Ultra, Mega 1."""


def library(word):
    r = subprocess.run(["python3.12", "tools/research_library.py", "find", word], cwd=ROOT, capture_output=True, text=True)
    return r.stdout[:30000]


RECORD_BLUETTI = """{"slug": "<bluetti-...>", "brand": "BLUETTI", "program": "awin:bluetti_us", "category": "power-station", "name": "<full name with Wh and W>",
 "model": "<model>", "url": "<bluettipower.com product url>", "official_page": "<same>", "price": <number, today's store price>, "verified": "YYYY-MM-DD",
 "specs": [["<label>", "<value>"], ...6-10 rows from BLUETTI's page or manual], "warranty": "<from BLUETTI's warranty page, with the page>",
 "returns": "<from BLUETTI's returns policy>", "summary": "<one or two sentences: what it is and the measured fact that matters>",
 "fit": "<who it suits>", "caveats": ["<sourced weakness>", ...]}"""
RECORD_AMAZON = """{"slug": "<brand-model>", "brand": "<Brand>", "program": "amazon:us", "asin": "<ASIN of the brand's own listing>",
 "asin_title": "<the listing title as Amazon shows it>", "asin_seller": "<who sells and ships it, as Amazon shows it>",
 "category": "power-station", "name": "<full name with Wh and W>", "model": "<model>", "url": "https://www.amazon.com/dp/<ASIN>",
 "official_page": "<maker's US product page>", "price": null, "specs": [["<label>", "<value>"], ...6-10 rows from the maker's page or manual],
 "warranty": "<maker's warranty with the page>", "returns": "<Amazon / maker returns>", "summary": "<one or two sentences>",
 "fit": "<who it suits>", "caveats": ["<sourced weakness>", ...]}  (no $ figure anywhere in an Amazon record)"""


def prompt(key):
    name, word, route, note = PRODUCTS[key]
    return "\n\n".join([
        A.COMMON_RULES.replace("TOOLS", str(ROOT / "tools")).replace("Spend about 25 tool calls at most", "Spend about 40 tool calls at most"),
        f"## Your job: product research on the {name}",
        f"Where we can sell it: {note}",
        "When ChatGPT recommends this product it usually types the row itself; in the checks so far its product panel showed no "
        "seller, so the pages it cites may be the only way to buy from that answer (a lead, not a fact: never write it on a page). "
        "We need to know, honestly: (1) where it MEASURABLY beats its rivals (named reviewer or lab measurements, maker manuals, "
        "or arithmetic labelled as arithmetic), each claim with its source URL and the date read; (2) where it is weak or loses; "
        "(3) which shopper needs it honestly wins and which it should not be recommended for; (4) which searches with real demand "
        "(list below) we should target with a comparison page featuring it, and a plain-shopper headline for each (no model "
        "numbers in the headline); a brand search ('<brand> power station') counts when the product is that brand's best answer "
        "for some need. Prefer searches with volume; say plainly when no search with volume fits. (5) A product record for our "
        "site in the shape below." + (" For Amazon: find the brand's own listing with `python3.12 TOOLS/amzcheck.py` (search, "
        "then the product page), confirm the title is exactly this product alone (not a bundle, not another capacity, not "
        "renewed), and record who sells it. If Amazon has no listing from the brand or Amazon itself, return asin null and say so."
        .replace("TOOLS", str(ROOT / "tools")) if route == "amazon" else ""),
        f"## Today\n{A.today()}",
        "## Demand evidence\n" + DEMAND,
        f"## Research library findings mentioning '{word}' (earlier agents; re-check before relying on them)\n" + library(word),
        "## Output JSON\n" + """{"product": "<name>",
 "price_today": {"value": "<$ at the seller we link, or 'Amazon price not read'>", "source": "<url>", "read": "YYYY-MM-DD"},
 "wins": [{"need": "...", "claim": "<what it beats, against which rivals>", "figure": "...", "source": "<url>", "who": "...", "read": "YYYY-MM-DD"}],
 "weak": [{"claim": "...", "figure": "...", "source": "...", "read": "..."}],
 "wins_for": ["..."], "not_for": ["<need, and what wins instead>"],
 "rivals": [{"model": "...", "price": "<$ with source and date>", "where_it_beats_ours": "..."}],
 "targets": [{"search": "<search with demand from the list>", "demand": "<count and source>", "headline": "...", "why_it_wins_there": "<measured reason with source>"}],
 "record": """ + (RECORD_AMAZON if route == "amazon" else RECORD_BLUETTI) + """,
 "unsourced": ["..."]}""",
    ])


def run(key):
    out = A.claude(prompt(key), timeout=5400)
    A.jsave(OUT / f"{key}.json", out)
    return key, out.get("status", "ok"), len(out.get("wins") or []), (out.get("record") or {}).get("asin")


if __name__ == "__main__":
    keys = sys.argv[1:] or list(PRODUCTS)
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for r in ex.map(run, keys):
            print(json.dumps(r), flush=True)
    print("PRODUCT RESEARCH 2 DONE", flush=True)
