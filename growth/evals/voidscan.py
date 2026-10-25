#!/usr/bin/env python3.12
"""Void scan (growth/void-scan.md): are there product-discovery queries with real search demand whose Bing top 10 holds
few pages written to answer them? Uses Bing Webmaster Tools → Keyword Research in the agent's Chrome (signed in as
barrryyao) for demand (the related and question keyword lists per category seed, with US search counts), and the live
Bing results page per query for supply (serp.py's fetcher). An LLM (Claude CLI) labels query intent and each result.

    python3.12 growth/evals/voidscan.py harvest      # seeds → candidates.json (query → US searches, 3 months)
    python3.12 growth/evals/voidscan.py intent       # candidates → intent.json (discovery or not)
    python3.12 growth/evals/voidscan.py supply       # discovery queries → supply.json (live Bing top 10)
    python3.12 growth/evals/voidscan.py label        # supply → labels.json (dedicated? source kind)
    python3.12 growth/evals/voidscan.py report       # → report.json + report.md

Each step skips what its output file already holds, so a re-run fills the gaps.
Start the browser first: uv --directory ~/Desktop/agent-vault run agent-vault browser
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import serp  # noqa: E402
import ui  # noqa: E402

RUN = E.run_dir("2026-10-24-voidscan")
WINDOW = ("2026-07-24T00:00:00.000Z", "2026-10-21T00:00:00.000Z")
SITE = "https://dealectric.com/"
MODEL = "claude-sonnet-5-5"
PAUSE_S = 3.0
BACKOFF_S = (60, 120, 300, 600)   # Bing answers 429 TooManyRequests after a burst (seen at ~7 calls 0.5 s apart)

SEEDS = """wireless earbuds; noise cancelling headphones; bluetooth speaker; soundbar; portable monitor; mechanical keyboard;
gaming mouse; webcam; mesh wifi router; power bank; wireless charger; usb c hub; smartwatch; fitness tracker; e-reader;
tablet; laptop stand; dash cam; security camera; video doorbell; smart lock; smart thermostat; robot vacuum;
cordless vacuum; air purifier; dehumidifier; humidifier; space heater; portable air conditioner; tower fan;
water filter pitcher; espresso machine; coffee grinder; air fryer; blender; stand mixer; rice cooker; electric kettle;
chef knife; cast iron skillet; mattress; pillow; weighted blanket; office chair; standing desk; desk lamp;
electric toothbrush; water flosser; hair dryer; electric shaver; massage gun; treadmill; exercise bike;
adjustable dumbbells; yoga mat; running shoes; hiking boots; backpack; carry on luggage; camping tent; sleeping bag;
camping stove; cooler; kayak; electric bike; electric scooter; bike helmet; baby monitor; stroller; car seat;
dog food; cat litter; dog bed; pressure washer; cordless drill; lawn mower; leaf blower; generator; solar panel;
ev charger; car vacuum; tire inflator; jump starter; 3d printer; label maker; sewing machine; portable power station;
battery charger; cpap battery""".replace("\n", " ")
SEEDS = [s.strip() for s in SEEDS.split(";") if s.strip()]

HOOK = r"""(() => { const of = window.fetch; window.fetch = function(u, o) {
  try { const h = o && o.headers; if (h) { const hh = h instanceof Headers ? h : new Headers(h); if (hh.has('X-CSRF-Token')) window.__hdr = hh; } } catch (e) {}
  return of.apply(this, arguments); }; })();"""


class KR:
    """Keyword Research API from inside a background tab on the tool's own page. The POST endpoints want the page's
    X-CSRF-Token header, which the page sets on its own fetch calls; a script injected before load keeps a copy."""

    def __init__(self):
        self.tab = ui.Tab("about:blank")
        self.tab.call("Page.enable")
        self.tab.call("Page.addScriptToEvaluateOnNewDocument", source=HOOK)
        self.tab.navigate(f"https://www.bing.com/webmasters/keywordresearch?siteUrl={urllib.parse.quote(SITE)}&keyword=air%20fryer")
        for _ in range(30):
            time.sleep(1)
            if self.tab.eval("!!window.__hdr"):
                return
        raise RuntimeError("no X-CSRF-Token seen; is the agent's Chrome signed in to Bing Webmaster Tools?")

    def post(self, endpoint: str, keyword: str, page_size: int | None = None):
        body = {"keyword": keyword, "siteUrl": SITE, "StartDate": WINDOW[0], "EndDate": WINDOW[1],
                "Country": "us", "Language": "", "Vertical": ""}
        if page_size:
            body["Pagination"] = {"pageSize": page_size, "pageNum": 1}
        js = f"""(async () => {{ const r = await fetch('/webmasters/api/keywordresearch/{endpoint}', {{method: 'POST',
            headers: window.__hdr, body: {json.dumps(json.dumps(body))}, credentials: 'include'}});
            return JSON.stringify({{status: r.status, text: await r.text()}}); }})()"""
        r = self._fetch(js)
        if r["status"] == 404:   # the tool answers 404 when it has no list for the keyword
            return None
        if r["status"] != 200:
            raise RuntimeError(f"{endpoint} {keyword!r}: HTTP {r['status']} {r['text'][:200]}")
        return json.loads(r["text"])

    def _fetch(self, js: str) -> dict:
        for wait in (*BACKOFF_S, None):
            r = json.loads(self.tab.eval(js))
            time.sleep(PAUSE_S)
            if r["status"] != 429 or wait is None:
                return r
            print(f"429, waiting {wait} s", flush=True)
            time.sleep(wait)
        return r

    def close(self):
        self.tab.close()


def load(name: str, default):
    p = RUN / name
    return json.loads(p.read_text()) if p.exists() else default


def save(name: str, obj) -> None:
    RUN.mkdir(parents=True, exist_ok=True)
    E.write_json(RUN / name, obj)


def harvest(args) -> None:
    cand = load("candidates.json", {"seeds_done": [], "queries": {}})
    kr = KR()
    try:
        for seed in SEEDS:
            if seed in cand["seeds_done"]:
                continue
            for kw, ep in ((seed, "relatedkeywords"), (seed, "questionkeywords"), (f"best {seed}", "relatedkeywords")):
                j = kr.post(ep, kw, page_size=50) or {}
                for s in j.get("KeywordStats") or []:
                    q = (s.get("Query") or "").strip().lower()
                    if not q:
                        continue
                    rec = cand["queries"].setdefault(q, {"searches": 0, "seeds": [], "lists": []})
                    rec["searches"] = max(rec["searches"], int(s.get("ImpressionCount") or 0))
                    if seed not in rec["seeds"]:
                        rec["seeds"].append(seed)
                    if ep not in rec["lists"]:
                        rec["lists"].append(ep)
            cand["seeds_done"].append(seed)
            save("candidates.json", cand)
            print(f"{seed}: {len(cand['queries'])} queries so far", flush=True)
    finally:
        kr.close()


INTENT_SCHEMA = {"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {
    "q": {"type": "string"}, "discovery": {"type": "boolean"}}, "required": ["q", "discovery"]}}}, "required": ["items"]}
INTENT_SYSTEM = """You label search queries. A query is "discovery" when the searcher is choosing which product to buy and
a page that compares or recommends products would answer it: "best X", "best X for Y", "X vs Y", "X under $200",
"alternatives to X", "which X should I buy", "top rated X", "quietest X", "X for small apartment". It is NOT discovery
when it is navigational (a brand, store or model name alone, "X near me", "X amazon", "X costco", a model number),
informational or support ("how to clean X", "what is X", "X not working", "X manual", "X recall"), or a bare category
noun with no choosing signal ("air fryer", "air fryers"). Answer for every query given, copying q exactly."""


def intent(args) -> None:
    cand = load("candidates.json", {"queries": {}})["queries"]
    out = load("intent.json", {})
    todo = [q for q in cand if q not in out and cand[q]["searches"] >= args.min_searches]
    usage: dict = {}
    for i in range(0, len(todo), 60):
        batch = todo[i:i + 60]
        r = E.claude_cli_json(INTENT_SYSTEM, "\n".join(batch), MODEL, INTENT_SCHEMA, usage=usage) or {}
        for it in r.get("items") or []:
            if it.get("q") in batch:
                out[it["q"]] = bool(it.get("discovery"))
        save("intent.json", out)
        print(f"intent {min(i + 60, len(todo))}/{len(todo)}: {sum(out.values())} discovery", flush=True)
    print("usage", usage)


def supply(args) -> None:
    """Live Bing results page per query, read with serp.py's fetcher. Keyword Research's own top-URL list would do,
    but the tool's quota (429 after about 120 calls on 2026-10-24, still blocked 20 minutes later) cannot carry it."""
    disc = [q for q, d in load("intent.json", {}).items() if d]
    out = load("supply.json", {})
    todo = [q for q in disc if not any(r.get("rank") for r in out.get(q) or [])]
    for n, q in enumerate(todo, 1):
        out[q] = serp.fetch("bing", q)[:10]
        time.sleep(args.pause)
        if n % 10 == 0 or n == len(todo):
            save("supply.json", out)
            print(f"supply {n}/{len(todo)}: {q!r} {sum(1 for r in out[q] if r.get('rank'))} results", flush=True)
    save("supply.json", out)


KINDS = ["major_publisher", "niche_site", "retailer", "brand", "forum_video", "other"]
LABEL_SCHEMA = {"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {
    "q": {"type": "string"},
    "results": {"type": "array", "items": {"type": "object", "properties": {
        "rank": {"type": "integer"}, "dedicated": {"type": "boolean"}, "kind": {"type": "string", "enum": KINDS}},
        "required": ["rank", "dedicated", "kind"]}}}, "required": ["q", "results"]}}}, "required": ["items"]}
LABEL_SYSTEM = """For each search query you get the top results (rank, title, URL). Label every result:
- dedicated: true only if the page was written to answer THIS query, matching its qualifiers. For "best air purifier for
  smoke" a "Best Air Purifiers for Smoke (2026)" page is dedicated; a general "Best Air Purifiers" list, a product page,
  a store category page or a forum thread is not. For "dyson vs shark" a page comparing those two brands is dedicated.
  For a plain "best X" query a "Best X" list is dedicated.
- kind: major_publisher (large editorial or testing outlets: NYT Wirecutter, RTINGS, Consumer Reports, CNET, Tom's Guide,
  PCMag, The Verge, Wired, TechRadar, Good Housekeeping, Popular Mechanics, Forbes Vetted, Bob Vila, OutdoorGearLab,
  Serious Eats, Engadget, ZDNET, Business Insider, People, Healthline, US News and the like), niche_site (smaller review
  or blog sites), retailer (Amazon, Walmart, Best Buy, Home Depot, Target, Costco, REI and other stores), brand
  (the maker's own site), forum_video (Reddit, Quora, YouTube, forums), other.
Copy q exactly and return one entry per result rank given."""


def label(args) -> None:
    sup = load("supply.json", {})
    out = load("labels.json", {})
    todo = [q for q, rows in sup.items() if any(r.get("rank") for r in rows) and q not in out]
    usage: dict = {}
    step = 8
    for i in range(0, len(todo), step):
        batch = todo[i:i + step]
        user = "\n\n".join(f"QUERY: {q}\n" + "\n".join(f"{r['rank']}. {r['title']} | {r['url']}" for r in sup[q] if r.get("rank")) for q in batch)
        try:
            r = E.claude_cli_json(LABEL_SYSTEM, user, MODEL, LABEL_SCHEMA, timeout=300, usage=usage) or {}
        except Exception as e:  # noqa: BLE001
            print("label error", e, flush=True)
            continue
        for it in r.get("items") or []:
            if it.get("q") in batch:
                out[it["q"]] = it.get("results") or []
        save("labels.json", out)
        print(f"label {min(i + step, len(todo))}/{len(todo)}", flush=True)
    print("usage", usage)


def report(args) -> None:
    cand = load("candidates.json", {"queries": {}})["queries"]
    sup, lab = load("supply.json", {}), load("labels.json", {})
    rows = []
    for q, res in lab.items():
        top = {r["rank"]: r for r in sup.get(q, [])}
        ded = [r for r in res if r.get("dedicated")]
        rows.append({
            "q": q, "searches": cand.get(q, {}).get("searches", 0), "seed": (cand.get(q, {}).get("seeds") or [""])[0],
            "n_results": len(res), "dedicated": len(ded),
            "dedicated_major": sum(1 for r in ded if r["kind"] == "major_publisher"),
            "major_any": sum(1 for r in res if r["kind"] == "major_publisher"),
            "kinds": {k: sum(1 for r in res if r["kind"] == k) for k in KINDS},
            "dedicated_titles": [top.get(r["rank"], {}).get("title", "") for r in ded][:4],
        })
    rows = [r for r in rows if r["n_results"] >= 5]   # too few results to judge supply
    med = statistics.median(r["searches"] for r in rows)
    mean_ded = statistics.mean(r["dedicated"] for r in rows)
    for r in rows:
        r["opening"] = r["searches"] >= med and r["dedicated"] < mean_ded and r["dedicated_major"] == 0
    openings = sorted((r for r in rows if r["opening"]), key=lambda r: -r["searches"])
    summary = {"discovery_queries_scored": len(rows), "median_searches": med, "mean_dedicated": round(mean_ded, 2),
               "openings": len(openings), "openings_share": round(len(openings) / len(rows), 3) if rows else 0,
               "thesis_threshold_met": len(openings) >= 10 and len(openings) / max(len(rows), 1) >= 0.05}
    save("report.json", {"summary": summary, "rows": sorted(rows, key=lambda r: -r["searches"])})
    lines = [f"# Void scan report ({E.today()})", "", "```", json.dumps(summary, indent=1), "```", "",
             "| query | Bing US searches, 3 mo | dedicated in top 10 | major publishers (any) | kinds | dedicated titles |",
             "|---|---|---|---|---|---|"]
    for r in openings:
        kinds = ", ".join(f"{k} {v}" for k, v in r["kinds"].items() if v)
        lines.append(f"| {r['q']} | {r['searches']} | {r['dedicated']} | {r['major_any']} | {kinds} | {'; '.join(r['dedicated_titles'])} |")
    (RUN / "report.md").write_text("\n".join(lines) + "\n")
    print(json.dumps(summary, indent=1))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=["harvest", "intent", "supply", "label", "report"])
    ap.add_argument("--min-searches", type=int, default=10, help="intent: skip queries below this many searches")
    ap.add_argument("--pause", type=float, default=3.0, help="supply: seconds between Bing queries")
    args = ap.parse_args()
    {"harvest": harvest, "intent": intent, "supply": supply, "label": label, "report": report}[args.step](args)


if __name__ == "__main__":
    main()
