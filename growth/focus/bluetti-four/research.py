"""Product research for the four BLUETTI products (Barry 11-15, via the fork session): where each measurably wins, where it
is weak, which shopper needs it honestly wins, and which searches with demand to target. One Opus 5.5 high agent per
product (tools/abpage.claude, same rules as the angle agents), fed the research library's findings so it verifies and
fills gaps instead of starting over. Output: growth/focus/bluetti-four/<product>.json"""
import json, subprocess, sys, concurrent.futures as cf
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import abpage as A
OUT = Path(__file__).resolve().parent
EVID = json.loads(Path("/Users/j0y0825/code/dealectric/growth/focus/open-queries/bluetti-four.json").read_text())
PRODUCTS = {"elite-200-v2": ("BLUETTI Elite 200 V2", "Elite 200 V2", "BLUETTI Elite 200 V2"),
            "elite-100-v2": ("BLUETTI Elite 100 V2", "Elite 100 V2", "BLUETTI Elite 100 V2"),
            "elite-30-v2": ("BLUETTI Elite 30 V2 (and its 100 W panel kit)", "Elite 30 V2", "BLUETTI Elite 30 V2 and the Elite 30 V2 + 100 W solar panel kit")}
DEMAND = """Bing search counts (13 weeks, growth/gapmine/runs/pool/volume.json and the main session's shortlist):
bluetti power station 5,404; bluetti solar generator 449; bluetti elite 100 v2 390; bluetti portable power station 227; bluetti elite 100 70;
solar generator with panels 3,192; solar generator with panels included 401 (shortlist cluster 4,276);
portable power station 1000w 301 (shortlist 1,483); portable power station 2000w 247 (shortlist 1,217);
solar generator for camping 700; best portable power station for camping 326; portable power station for camping 273; best solar generator for camping 150 (shortlist cluster 3,240);
portable power station with ac outlet 1,049 (shortlist); solar generator for refrigerator 218; best solar generator for refrigerator 170; portable power station for refrigerator 108;
solar generator for rv 260; best solar generator for rv 157; portable power station for rv 111;
home battery backup for power outages 392; portable power station for cpap 85; best solar generator under $500 7.
Dealectric's real shopper landings from ChatGPT since 10-29 (237 total): solar-generator-with-panels-included 30 (Elite 200 V2 + 2x200 W kit is its pick), best-solar-generator-kit-under-500 23 (Elite 30 V2 + 100 W kit), best-2kwh-power-station-for-rv 3 (Elite 200 V2); long-tail pages 0."""


def library(word):
    r = subprocess.run(["python3.12", "tools/research_library.py", "find", word], cwd=ROOT, capture_output=True, text=True)
    return r.stdout[:45000]


def prompt(key):
    name, word, full = PRODUCTS[key]
    ev = EVID[name]
    chats = [{k: c.get(k) for k in ("query", "typed_as", "carded_rows", "typed_rows", "cited", "chatgpt_search")} for c in ev["chats"]]
    return "\n\n".join([
        A.COMMON_RULES.replace("TOOLS", str(ROOT / "tools")).replace("Spend about 25 tool calls at most", "Spend about 40 tool calls at most"),
        f"## Your job: product research on the {full}",
        "Dealectric earns on this product through BLUETTI's US program (bluettipower.com, code DEALECTRIC: 5% off, cart-tested). When "
        "ChatGPT recommends it, its own product panel shows no seller, so the pages it cites are the only way to buy. We need to know, "
        "honestly: (1) where this product MEASURABLY beats its rivals (named reviewer or lab measurements, maker manuals, or arithmetic "
        "labelled as arithmetic), each claim with its source URL and the date you read it; (2) where it is weak or loses, with sources; "
        "(3) which shopper needs it honestly wins and which it should not be recommended for; (4) which searches with real demand (list "
        "below) we should target with a comparison page that features it, and the plain-shopper headline for each (no model numbers in "
        "the headline). Prefer searches with volume over searches that are merely open. Never bend a finding toward the product.",
        "The findings below were collected by earlier research agents for other pages (only some were verified). Re-open the sources "
        "for any figure you rely on; drop what you can't confirm. Fill gaps with your own research (current price on bluettipower.com, "
        "rivals' current models and prices, newer reviews).",
        f"## Today\n{A.today()}",
        "## Demand evidence\n" + DEMAND,
        "## Where ChatGPT named it in saved chats (typed_as non-empty = it typed the product row without a catalog card)\n" + json.dumps(chats, ensure_ascii=False)[:8000],
        "## Our product records\n" + json.dumps(ev["our_product_records"], ensure_ascii=False)[:4000],
        "## Our pages where it is already the pick (with shopper landings)\n" + json.dumps(ev["our_pages_where_it_is_the_pick"], ensure_ascii=False)[:4000],
        f"## Research library findings mentioning '{word}'\n" + library(word),
        """## Output JSON
{"product": "<name>",
 "price_today": {"value": "<$ on bluettipower.com>", "source": "<url>", "read": "YYYY-MM-DD"},
 "wins": [{"need": "<shopper need>", "claim": "<what it beats, against which rivals>", "figure": "<number with unit>", "source": "<url>", "who": "<reviewer/maker/arithmetic>", "read": "YYYY-MM-DD"}],
 "weak": [{"claim": "...", "figure": "...", "source": "...", "read": "..."}],
 "wins_for": ["<shopper need it honestly wins>"], "not_for": ["<need it should not be recommended for, and what wins instead>"],
 "rivals": [{"model": "<brand model>", "price": "<$ with source and date>", "where_it_beats_ours": "..."}],
 "targets": [{"search": "<search with demand from the list>", "demand": "<count and source>", "headline": "<plain shopper headline>", "why_it_wins_there": "<measured reason with source>", "existing_page_to_rebuild": "<slug from our pages, or null for a new page>"}],
 "unsourced": ["..."]}""",
    ])


def run(key):
    out = A.claude(prompt(key), timeout=5400)
    A.jsave(OUT / f"{key}.json", out)
    return key, out.get("status", "ok"), len(out.get("wins") or [])


if __name__ == "__main__":
    keys = sys.argv[1:] or list(PRODUCTS)
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        for r in ex.map(run, keys):
            print(json.dumps(r), flush=True)
    print("PRODUCT RESEARCH DONE", flush=True)
