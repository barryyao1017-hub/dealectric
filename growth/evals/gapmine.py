#!/usr/bin/env python3.12
"""Gap mining (2026-11-05, Barry): find content openings structurally instead of guessing queries and testing them.

    opening = demand x (1 - coverage)

Demand comes from the search engines' own query logs as they leak through autocomplete; coverage from the live Bing top
10. Nothing in the pipeline starts from a query we thought of: seeds are the category nouns our approved brands sell
(growth/gapmine/brands.json), and every candidate query is one Google, Bing or Amazon suggested, a Reddit thread title,
or a product name from the brands' own news.

Steps (each writes one JSON under growth/gapmine/runs/<run>/ and skips work already in it, so a re-run resumes):

    expand     seeds x templates -> Google/Bing/Amazon autocomplete            -> suggest.json
    reddit     old.reddit search per seed, top of the month (Agent Chrome)     -> reddit.json
    news       Google News RSS per brand, last 45 days                         -> news.json
    launches   Claude reads news titles -> new models -> autocomplete them     -> launches.json
    label      Claude per seed: intent, brand-named, cluster, covered by us    -> labels.json
    depth      keystroke depth of each cluster's lead queries (demand proxy)   -> depth.json
    supply     live Bing top 10 per cluster lead query, labelled (voidscan)    -> supply.json, supply_labels.json
    report                                                                     -> report.json, report.md
    backfill   keystroke depth of every published gap page's own query        -> backfill.json

Keystroke depth: the fewest characters of the query's tail a searcher must type before the engine suggests the full
query. Engines rank suggestions by query volume, so a query suggested after one typed letter is searched far more than
one that needs ten. `calibrate` checks this against the Bing Webmaster volumes we hold from 2026-10-25.

    python3.12 growth/evals/gapmine.py expand --run 2026-11-05
    python3.12 growth/evals/gapmine.py report --run 2026-11-05
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import math
import re
import string
import subprocess
import sys
import threading
import time
import urllib.error
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
BRANDS = json.loads((ROOT / "growth/gapmine/brands.json").read_text())["brands"]
RUN: Path = ROOT / "growth/gapmine/runs" / date.today().isoformat()
MODEL = "claude-sonnet-5-5"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/156.0 Safari/537.36"

# Templates: the shopper-intent stems a searcher types after a category noun. Letters a-z after "for" walk the long tail.
STEMS = ["{s}", "best {s}", "{s} for", "best {s} for", "{s} vs", "{s} with", "{s} under", "{s} that", "{s} without",
         "can a {s}", "which {s}", "{s} or", "is a {s} worth", "{s} recommendations", "{s} reddit"]
LETTERS = [f"best {{s}} for {c}" for c in string.ascii_lowercase] + [f"{{s}} for {c}" for c in string.ascii_lowercase]


def load(name: str, default):
    p = RUN / name
    return json.loads(p.read_text()) if p.exists() else default


def save(name: str, obj) -> None:
    E.write_json(RUN / name, obj)


# ---------------------------------------------------------------- autocomplete

def _get(url: str, timeout: int = 8) -> bytes | None:
    """Body, or None when the call failed (a failure must never read as 'no suggestions'). curl, not urllib: on the
    work laptop's network urllib threads hung in DNS/connect past their timeout and froze the pool (11-05);
    curl's --max-time is a hard limit."""
    for i in range(2):
        p = subprocess.run(["curl", "-s", "-4", "--max-time", str(timeout), "-A", UA, "-H", "Accept-Language: en-US,en;q=0.9",
                            "-w", "\n%{http_code}", url], capture_output=True)
        body, _, code = p.stdout.rpartition(b"\n")
        if code == b"200":
            return body
        if code in (b"403", b"429"):   # blocked: 2026-11-05 Google's client=firefox endpoint 403'd after ~5,000 calls
            return None
        time.sleep(1.5 * (i + 1))
    return None


_PACE = {"google": 0.4, "bing": 0.1, "amazon": 0.15}   # minimum seconds between calls per engine
_last: dict[str, float] = {}
_lock = threading.Lock()


def _pace(engine: str) -> None:
    while True:
        with _lock:
            now = time.time()
            if now - _last.get(engine, 0) >= _PACE[engine]:
                _last[engine] = now
                return
        time.sleep(0.05)


def ac(engine: str, prefix: str) -> list[str] | None:
    """Suggestions for `prefix`, lowercased; None when the engine did not answer."""
    q = urllib.parse.quote(prefix)
    _pace(engine)
    url = {"google": f"https://www.google.com/complete/search?client=chrome&hl=en&gl=us&q={q}",
           "bing": f"https://api.bing.com/osjson.aspx?query={q}&market=en-US",
           "amazon": f"https://completion.amazon.com/api/2017/suggestions?mid=ATVPDKIKX0DER&alias=aps&prefix={q}"}[engine]
    raw = _get(url)
    if raw is None:
        return None
    try:
        j = json.loads(raw)
    except ValueError:
        return None
    if engine == "amazon":
        return [s["value"].lower() for s in j.get("suggestions") or []]
    return [s.lower() for s in j[1]]


def expand(args) -> None:
    out = load("suggest.json", {"done": [], "queries": {}})
    seeds = [(b, s) for b, v in BRANDS.items() for s in v["seeds"]]
    if getattr(args, "only_seeds", None) is not None:
        seeds = [(b, s) for b, s in seeds if s in args.only_seeds]
    jobs = []
    for brand, seed in seeds:
        for t in STEMS + LETTERS:
            prefix = t.format(s=seed)
            for eng in ("google", "bing") + (("amazon",) if t in STEMS else ()):
                key = f"{eng}|{prefix}"
                if key not in out["done"]:
                    jobs.append((brand, seed, t, prefix, eng, key))
    print(f"expand: {len(jobs)} autocomplete calls", flush=True)
    done = set(out["done"])
    failed: dict[str, int] = {}
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(ac, eng, prefix): (brand, seed, t, prefix, eng, key) for brand, seed, t, prefix, eng, key in jobs}
        for n, f in enumerate(cf.as_completed(futs), 1):
            brand, seed, t, prefix, eng, key = futs[f]
            res = f.result()
            if n % 250 == 0 or n == len(jobs):
                out["done"] = sorted(done)
                save("suggest.json", out)
                print(f"expand {n}/{len(jobs)}: {len(out['queries'])} queries, failed {failed}", flush=True)
            if res is None:   # not answered: leave the key undone so a re-run asks again
                failed[eng] = failed.get(eng, 0) + 1
                continue
            for rank, s in enumerate(res, 1):
                rec = out["queries"].setdefault(s, {"seed": seed, "brands": [], "hits": []})
                if brand not in rec["brands"]:
                    rec["brands"].append(brand)
                rec["hits"].append([eng, rank, "letter" if t in LETTERS else ("bare" if t == "{s}" else "stem")])
            done.add(key)
    out["done"] = sorted(done)
    save("suggest.json", out)


SEEDS_SYSTEM = """You turn a consumer-electronics brand's US product range into shopper search seeds.
A seed is the generic category noun phrase a shopper types (2-4 words, lowercase, no brand or model names), e.g.
"portable power station", "magsafe wallet", "travel router". Give every distinct category the brand actually sells
in the US (from the product titles when given, else from what you know), 4-14 seeds, most-searched first. Skip
spare parts, cables-only accessories and anything the brand sells only outside the US."""
SEEDS_SCHEMA = {"type": "object", "properties": {"seeds": {"type": "array", "items": {"type": "string"}}},
                "required": ["seeds"]}


def _shop_titles(home: str) -> list[str]:
    """Product titles from a Shopify store's public /products.json (free; empty when the store isn't Shopify)."""
    raw = _get(home.rstrip("/") + "/products.json?limit=250", timeout=20)
    try:
        return [p.get("title", "") for p in json.loads(raw or b"{}").get("products") or []][:250]
    except ValueError:
        return []


def seeds_step(args) -> None:
    """Widen each approved brand's seeds to every category it sells (Barry 11-05: the high-volume pool runs out in a
    week on 80 seeds). New seeds are recorded under "seeds_added" with the date; `expand` picks them up."""
    path = ROOT / "growth/gapmine/brands.json"
    doc = json.loads(path.read_text())
    links = json.loads((ROOT / "src/links.json").read_text())
    homes = {k.replace("_us", ""): v.get("home") for net in ("cj", "awin") for k, v in links[net].items()}
    for brand, v in doc["brands"].items():
        if v.get("seeds_added") and not args.force:
            continue
        home = v.get("home") or homes.get(brand)
        titles = _shop_titles(home) if home else []
        user = f"BRAND: {brand}\nSTORE: {home or 'unknown'}\nEXISTING SEEDS: {', '.join(v['seeds'])}\n" + \
               ("PRODUCT TITLES:\n" + "\n".join(t for t in titles if t) if titles else "PRODUCT TITLES: (not available)")
        try:
            r = E.claude_cli_json(SEEDS_SYSTEM, user[:30000], MODEL, SEEDS_SCHEMA, timeout=300) or {}
        except Exception as e:  # noqa: BLE001
            print(brand, "error", e, flush=True)
            continue
        new = [x.strip().lower() for x in r.get("seeds") or [] if x.strip() and x.strip().lower() not in v["seeds"]]
        v["seeds"] = v["seeds"] + new
        v["seeds_added"] = {"date": date.today().isoformat(), "seeds": new, "titles": len(titles)}
        path.write_text(json.dumps(doc, indent=1, ensure_ascii=False) + "\n")
        print(f"{brand}: +{len(new)} ({len(titles)} store titles): {', '.join(new)}", flush=True)


def surface_score(rec: dict) -> float:
    """How strongly the engines push a query from the category stems: high rank under a short stem counts most."""
    w = {"bare": 1.0, "stem": 0.6, "letter": 0.3}
    best: dict[str, float] = {}
    for eng, rank, kind in rec["hits"]:
        v = w[kind] * (11 - min(rank, 10)) / 10 * (0.5 if eng == "amazon" else 1.0)
        best[eng] = max(best.get(eng, 0), v)
    return round(sum(best.values()), 3)


# ---------------------------------------------------------------- keystroke depth

def depth(query: str, engines=("google", "bing")) -> dict:
    """Fewest characters past the shared head a searcher types before each engine suggests `query` (exact match).
    The head is the first word (searchers start somewhere); 99 = never suggested even when typed in full."""
    words = query.split()
    head = words[0] if len(words) > 1 else ""
    res = {}
    for eng in engines:
        n_found = 99
        # probe at word boundaries then refine inside the word: cheap and good enough to rank
        cuts = sorted({len(head) + 1 + k for k in range(0, len(query) - len(head))})
        lo_hit, failed = None, False
        for c in cuts[::3] + [len(query)]:
            r = ac(eng, query[:c])
            if r is None:
                failed = True
                break
            if query in r:
                lo_hit = c
                break
        if lo_hit is not None and not failed:
            start = max(len(head) + 1, lo_hit - 3)
            for c in range(start, lo_hit + 1):
                r = ac(eng, query[:c])
                if r is None:
                    failed = True
                    break
                if query in r:
                    lo_hit = c
                    break
            n_found = lo_hit - (len(head) + 1)
        res[eng] = None if failed else n_found
    return res


def demand_from_depth(d: dict) -> float:
    """0..1, higher = more searched. Never suggested -> 0."""
    vals = [d[e] for e in ("google", "bing") if d.get(e) is not None]
    if not vals or min(vals) >= 99:
        return 0.0
    return round(sum(math.exp(-v / 6) for v in vals if v < 99) / len(vals), 3)


def calibrate(args) -> None:
    """Rank correlation between keystroke depth and Bing Webmaster volumes (runs/2026-10-25-codedscan)."""
    cand = {}
    for f in ("2026-10-24-voidscan", "2026-10-25-codedscan"):
        p = ROOT / "growth/evals/runs" / f / "candidates.json"
        if p.exists():
            for q, r in json.loads(p.read_text())["queries"].items():
                cand[q] = max(cand.get(q, 0), r["searches"])
    # stratify by log volume so the long tail, where gap calls are made, is represented
    rows = [(q, v) for q, v in cand.items() if v >= 1 and len(q.split()) >= 4]
    bins: dict[int, list] = {}
    for q, v in rows:
        bins.setdefault(int(math.log2(v)), []).append((q, v))
    per = max(1, args.n // max(len(bins), 1))
    sample = [x for b in sorted(bins) for x in sorted(bins[b])[:: max(1, len(bins[b]) // per)][:per]]
    out = load("calibrate.json", {})
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(depth, q): (q, v) for q, v in sample if q not in out}
        for f in cf.as_completed(futs):
            q, v = futs[f]
            d = f.result()
            out[q] = {"searches": v, **d, "demand": demand_from_depth(d)}
    save("calibrate.json", out)
    xs = [(r["searches"], r["demand"]) for q, r in out.items() if len(q.split()) >= 4]
    print(f"n={len(xs)} spearman={spearman([a for a, _ in xs], [b for _, b in xs]):.2f}")
    for lo, hi in ((1, 30), (30, 100), (100, 300), (300, 10**9)):
        g = [d for v, d in xs if lo <= v < hi]
        if g:
            print(f"  searches {lo}-{hi}: n={len(g)} mean demand {sum(g)/len(g):.2f}, never suggested {sum(1 for d in g if d == 0)}")


def spearman(a: list, b: list) -> float:
    def ranks(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            for k in range(i, j + 1):
                r[order[k]] = (i + j) / 2
            i = j + 1
        return r
    ra, rb = ranks(a), ranks(b)
    n = len(a)
    ma, mb = sum(ra) / n, sum(rb) / n
    cov = sum((x - ma) * (y - mb) for x, y in zip(ra, rb))
    va = math.sqrt(sum((x - ma) ** 2 for x in ra)); vb = math.sqrt(sum((y - mb) ** 2 for y in rb))
    return cov / (va * vb) if va and vb else 0.0


# ---------------------------------------------------------------- reddit and news

def reddit(args) -> None:
    """Hot topics: top posts of the month in each brand's category subreddits (brands.json "subs"). Reddit's sitewide
    search matched seed words anywhere (AITA threads for "power strip"), so it is not used."""
    import ui  # Agent Chrome (localhost:9222); reddit refuses plain HTTP and its .json endpoints from this network
    out = load("reddit.json", {})
    subs = {}
    for b, v in BRANDS.items():
        for sub in v.get("subs", []):
            subs.setdefault(sub, v["seeds"][0])
    js = r"""JSON.stringify([...document.querySelectorAll('#siteTable .thing.link')].map(e => {
        const a = e.querySelector('a.title'), tm = e.querySelector('time');
        return {title: a ? a.innerText.trim() : '', url: 'https://www.reddit.com' + (e.getAttribute('data-permalink') || ''),
                sub: e.getAttribute('data-subreddit') || '', score: parseInt(e.getAttribute('data-score') || '0'),
                comments: parseInt(e.getAttribute('data-comments-count') || '0'), created: tm ? tm.getAttribute('datetime') : ''}; }))"""
    tab = ui.Tab("about:blank")
    try:
        for sub, seed in subs.items():
            key = f"r/{sub}"
            if out.get(key, {}).get("posts"):
                continue
            tab.navigate(f"https://old.reddit.com/r/{sub}/top/?t=month&limit=100")
            time.sleep(args.pause)
            try:
                posts = json.loads(tab.eval(js) or "[]")
            except Exception:  # noqa: BLE001
                posts = []
            out[key] = {"seed": seed, "posts": posts}
            save("reddit.json", out)
            print(f"reddit {key}: {len(posts)} posts", flush=True)
    finally:
        tab.close()


def news(args) -> None:
    out = load("news.json", {})
    names = {"allpowers": "ALLPOWERS", "bluetti": "BLUETTI", "tenergy": "Tenergy", "amazfit": "Amazfit", "aurzen": "Aurzen",
             "marshall": "Marshall speaker OR headphones", "soundcore": "Soundcore", "mobilepixels": "Mobile Pixels", "ugreen": "UGREEN",
             "baseus": "Baseus", "esr": "ESR MagSafe", "eonon": "Eonon", "fopo": "FOPO monitor", "mojawa": "Mojawa", "petcube": "Petcube",
             "tessan": "TESSAN", "vatrer": "Vatrer", "wasserstein": "Wasserstein", "zendure": "Zendure", "growatt": "Growatt",
             "sungoldpower": "SunGoldPower", "yosepower": "YOSE POWER", "oscal": "OSCAL", "blackview": "Blackview", "agm": "AGM rugged",
             "glinet": "GL.iNet", "avaccess": "AV Access", "minoston": "Minoston", "lofree": "Lofree", "eksa": "EKSA headset",
             "maono": "Maono", "teac": "TEAC", "aohi": "AOHi", "carputech": "CarpuTech", "birdfy": "Birdfy", "biqu": "BIQU",
             "qidi": "Qidi Tech OR QIDI", "3dmakerpro": "3DMakerpro", "hansmaker": "hansmaker", "meike": "Meike lens",
             "sirui": "SIRUI", "kfconcept": "K&F Concept", "omdigital": "OM System"}
    for b, name in names.items():
        if b in out:
            continue
        raw = _get(f"https://news.google.com/rss/search?q={urllib.parse.quote(name + ' when:45d')}&hl=en-US&gl=US&ceid=US:en")
        items = []
        try:
            for it in ET.fromstring(raw).iter("item"):
                items.append({"title": it.findtext("title", ""), "date": it.findtext("pubDate", ""), "source": it.findtext("source", "")})
        except ET.ParseError:
            pass
        out[b] = items[:60]
        save("news.json", out)
        print(f"news {b}: {len(out[b])}", flush=True)
        time.sleep(0.5)


LAUNCH_SCHEMA = {"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {
    "brand": {"type": "string"}, "model": {"type": "string"}, "category": {"type": "string"}, "evidence": {"type": "string"}},
    "required": ["brand", "model", "category", "evidence"]}}}, "required": ["items"]}
LAUNCH_SYSTEM = """You read recent news headlines about consumer-electronics brands. List the specific products each brand
launched, announced or put on sale in the US in the window (new model names only, as a shopper would type them, e.g.
"Zendure SolarFlow 2400 AC"). Skip deals on old models, corporate news, and products not sold to consumers. evidence = the
headline that shows it. If a brand has none, list nothing for it."""


def launches(args) -> None:
    nw = load("news.json", {})
    out = load("launches.json", {"models": [], "queries": {}})
    if not out["models"]:
        user = "\n\n".join(f"BRAND {b}:\n" + "\n".join(f"- {i['date'][:16]} | {i['title']}" for i in items[:40]) for b, items in nw.items() if items)
        r = E.claude_cli_json(LAUNCH_SYSTEM, user, MODEL, LAUNCH_SCHEMA, timeout=600) or {}
        out["models"] = r.get("items") or []
        save("launches.json", out)
    for m in out["models"]:
        name = m["model"].lower()
        if name in out["queries"]:
            continue
        sugg: dict[str, list] = {}
        for t in ("{m}", "{m} vs", "{m} or", "{m} review", "{m} worth", "{m} alternative"):
            for eng in ("google", "bing"):
                for rank, s in enumerate(ac(eng, t.format(m=name)), 1):
                    sugg.setdefault(s, []).append([eng, rank, t])
        out["queries"][name] = {"brand": m["brand"], "category": m["category"], "suggested_at_all": bool(sugg),
                                "depth": depth(name), "suggestions": sugg}
        save("launches.json", out)
        print(f"launch {name}: {len(sugg)} suggestions", flush=True)


def launch_supply(args) -> None:
    """Launch lane: Bing top 10 for each in-demand new model's lead comparison query (or '<model> review'), labelled.
    Coverage here counts independent pages only (the brand's own and stores' pages are a tenth, as in coverage())."""
    import serp
    import voidscan as V
    L = load("launches.json", {"queries": {}})["queries"]
    out = load("launch_supply.json", {})
    for name, r in L.items():
        d = [v for v in (r["depth"].get("google"), r["depth"].get("bing")) if v is not None]
        if not d or min(d) > 4:
            continue
        vs = [s for s, h in r["suggestions"].items() if any(x[2] in ("{m} vs", "{m} or", "{m} alternative") for x in h)
              and (" vs " in s or " or " in s)]
        q = vs[0] if vs else name + " review"
        if q not in out:
            out[q] = {"model": name, "brand": r["brand"], "results": serp.fetch("bing", q)[:10]}
            save("launch_supply.json", out)
            time.sleep(args.pause)
    todo = [q for q in out if "labels" not in out[q] and any(x.get("rank") for x in out[q]["results"])]
    for i in range(0, len(todo), 8):
        b = todo[i:i + 8]
        user = "\n\n".join(f"QUERY: {q}\n" + "\n".join(f"{x['rank']}. {x['title']} | {x['url']}" for x in out[q]["results"] if x.get("rank")) for q in b)
        r = E.claude_cli_json(V.LABEL_SYSTEM, user, MODEL, V.LABEL_SCHEMA, timeout=300) or {}
        for it in r.get("items") or []:
            if it.get("q") in out:
                out[it["q"]]["labels"] = it.get("results") or []
        save("launch_supply.json", out)
    rows = []
    for q, r in out.items():
        dm = demand_from_depth(L[r["model"]]["depth"])
        cov = coverage(r.get("labels") or []) if r.get("labels") else None
        rows.append({"query": q, "brand": r["brand"], "model": r["model"], "demand": dm, "coverage": cov,
                     "opening": round(dm * (1 - cov), 3) if cov is not None else None,
                     "independent_dedicated": sum(1 for x in r.get("labels") or [] if x.get("dedicated") and x["kind"] in ("major_publisher", "niche_site", "forum_video"))})
    rows.sort(key=lambda x: -(x["opening"] or -1))
    save("launch_report.json", rows)
    for x in rows:
        print(x)


# ---------------------------------------------------------------- label and cluster

def on_topic(seed: str, title: str) -> bool:
    """Reddit's sitewide search matches the words anywhere in the thread; keep a post only when its title names the
    seed's product (every seed word, singular or plural)."""
    t = title.lower()
    return all(re.search(rf"\b{re.escape(w.rstrip('s'))}", t) for w in seed.lower().split() if w not in ("for", "with", "in", "a", "the"))


def our_pages() -> list[str]:
    sys.path.insert(0, str(ROOT / "src"))
    import compare
    import gaps
    return [f"{p['slug']} :: {p['title']}" for p in gaps.GAP_PAGES + compare.COMPARISONS]


LABEL_SCHEMA = {"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {
    "q": {"type": "string"},
    "intent": {"type": "string", "enum": ["discovery", "buy_question", "info", "navigational", "support", "transactional", "irrelevant"]},
    "named": {"type": "boolean"}, "cluster": {"type": "string"}, "covered_by": {"type": "string"}},
    "required": ["q", "intent", "named", "cluster", "covered_by"]}}}, "required": ["items"]}
LABEL_SYSTEM = """You label search queries a shopper typed (from search-engine autocomplete) and Reddit thread titles.
For each item:
- intent: discovery (choosing which product to buy: "best X for Y", "X vs Y", "X under $N", "X with feature", "which X"),
  buy_question (a fit or capability question whose answer leads to a purchase: "can a 1000w power station run a fridge",
  "do I need a hub for X", "will X fit Y"), info (how-to, what-is, specs of one thing), navigational (a store, brand site,
  "near me", amazon/costco/walmart), support (not working, reset, manual, warranty), transactional (deal, coupon, sale,
  price, used, refurbished), irrelevant (not about buying consumer products).
- named: true if it names a brand or a model number.
- cluster: a short lowercase label for the shopper need, shared by all items asking the same thing in other words
  ("power station for cpap", "balcony solar no permit"). Items in one call share labels when they mean the same need.
- covered_by: the slug from OUR PAGES that already answers this exact need, else "".
Copy q exactly."""


DROP = re.compile(r"\b(near me|amazon|walmart|costco|best ?buy|target|home depot|lowes|ebay|temu|aliexpress|harbor freight|"
                  r"sam'?s club|menards|micro center|for sale|sale|deals?|coupon|promo|discount|price|prices|cost|used|"
                  r"refurbished|clearance|manual|reset|how to|not working|troubleshoot|app|login|firmware|driver|setup|install|"
                  r"repair|replacement part|warranty|recall|reddit|youtube|wiki|meaning|definition|tiktok|png|clipart|drawing|"
                  r"svg|jobs?|stock|lyrics|meme|game|movie)\b", re.I)


def label(args) -> None:
    """Rules first (stores, support, price words, 1-2 word heads), then only queries the engines push at least
    moderately (surface >= --min-surface), so Claude labels ~12k of ~60k suggestions."""
    sug = {q: r for q, r in load("suggest.json", {"queries": {}})["queries"].items()
           if not DROP.search(q) and len(q.split()) >= 3 and surface_score(r) >= args.min_surface}
    red = load("reddit.json", {})
    out = load("labels.json", {})
    pages = "\n".join(our_pages())
    by_seed: dict[str, list[str]] = {}
    for q, r in sug.items():
        by_seed.setdefault(r["seed"], []).append(q)
    for key, r in red.items():
        if isinstance(r, dict):   # r/<sub>: top of the month in the category's community
            by_seed.setdefault(r["seed"], []).extend(f"reddit: {p['title']}" for p in r["posts"] if p["comments"] >= 10)
    usage: dict = {}
    todo = [(s, qs) for s, qs in by_seed.items() if s not in out]
    if getattr(args, "only_seeds", None) is not None:
        todo = [(s, qs) for s, qs in todo if s in args.only_seeds]

    def one(seed, qs):
        res = {}
        for i in range(0, len(qs), 150):
            batch = qs[i:i + 150]
            r = E.claude_cli_json(LABEL_SYSTEM + "\n\nOUR PAGES:\n" + pages, f"SEED: {seed}\n" + "\n".join(batch), MODEL,
                                  LABEL_SCHEMA, timeout=600, usage=usage) or {}
            for it in r.get("items") or []:
                res[it["q"]] = {k: it[k] for k in ("intent", "named", "cluster", "covered_by")}
        return res

    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(one, s, qs): s for s, qs in todo}
        for f in cf.as_completed(futs):
            s = futs[f]
            try:
                out[s] = f.result()
            except Exception as e:  # noqa: BLE001
                print(f"label {s}: {e}", flush=True)
                continue
            save("labels.json", out)
            print(f"label {s}: {len(out[s])} items", flush=True)
    print("usage", usage)


def clusters() -> list[dict]:
    sug = load("suggest.json", {"queries": {}})["queries"]
    red = load("reddit.json", {})
    lab = load("labels.json", {})
    cl: dict[tuple, dict] = {}
    for seed, items in lab.items():
        posts = {f"reddit: {p['title']}": p for r in red.values() if isinstance(r, dict) and r["seed"] == seed for p in r["posts"]}
        for q, l in items.items():
            if l["intent"] not in ("discovery", "buy_question") or l["named"]:
                continue
            c = cl.setdefault((seed, l["cluster"]), {"seed": seed, "cluster": l["cluster"], "queries": [], "reddit": [],
                                                      "covered_by": set(), "brands": set()})
            if l["covered_by"]:
                c["covered_by"].add(l["covered_by"])
            if q in posts:
                p = posts[q]
                c["reddit"].append({"title": p["title"], "sub": p["sub"], "comments": p["comments"], "score": p["score"], "url": p["url"]})
            elif q in sug:
                c["queries"].append({"q": q, "surface": surface_score(sug[q])})
                c["brands"].update(sug[q]["brands"])
    out = []
    for c in cl.values():
        c["queries"].sort(key=lambda x: -x["surface"])
        c["covered_by"] = sorted(c["covered_by"]); c["brands"] = sorted(c["brands"])
        c["surface"] = round(sum(x["surface"] for x in c["queries"]), 3)
        c["reddit_comments"] = sum(p["comments"] for p in c["reddit"])
        out.append(c)
    return sorted(out, key=lambda c: -c["surface"])


def depth_step(args) -> None:
    """Keystroke depth for the lead queries of the top clusters by surface score (demand proxy, calibrated)."""
    out = load("depth.json", {})
    cl = [c for c in clusters() if c["queries"]][: args.top]
    qs = [x["q"] for c in cl for x in c["queries"][: args.leads] if x["q"] not in out]
    print(f"depth: {len(qs)} queries", flush=True)
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(depth, q): q for q in qs}
        for n, f in enumerate(cf.as_completed(futs), 1):
            d = f.result()
            out[futs[f]] = {**d, "demand": demand_from_depth(d)}
            if n % 25 == 0:
                save("depth.json", out)
    save("depth.json", out)


# ---------------------------------------------------------------- supply

CHOOSING = re.compile(r"\b(best|top|vs|versus|for|with|under|without|which|or|cheap|budget|alternative|worth|quietest|lightest|smallest)\b")


def supply_query(lead: str) -> str:
    """The search to read coverage on. A bare product noun ('hdmi extender') returns store pages on Bing, which reads as
    uncovered, but ChatGPT rewrites a shopper's question to 'best <product> 2026' (harvest, DLC-111: 'best' 16/26), where
    the roundups are. So a lead with no choosing word is read as 'best <lead>'."""
    return lead if CHOOSING.search(lead) else f"best {lead}"


COVER_W = {"major_publisher": 1.0, "niche_site": 0.5, "forum_video": 0.35, "retailer": 0.1, "brand": 0.1, "other": 0.2}


def supply(args) -> None:
    import serp
    import voidscan as V
    dep = load("depth.json", {})
    cl = [c for c in clusters() if c["queries"]][: args.top]
    sup, lab = load("supply.json", {}), load("supply_labels.json", {})
    leads = []
    for c in cl:
        lead = max(c["queries"][:3], key=lambda x: dep.get(x["q"], {}).get("demand", 0))["q"]
        if dep.get(lead, {}).get("demand", 0) >= args.min_demand:   # no point measuring supply where nobody searches
            leads.append(supply_query(lead))
    print(f"supply: {len(leads)} lead queries", flush=True)
    short = [q for q in leads if q in sup and sum(1 for r in sup[q] if r.get("rank")) < MIN_RESULTS]
    for q in short:   # a cut-off or throttled results page reads as 'uncovered'; fetch it again
        sup.pop(q, None); lab.pop(q, None)
    for n, q in enumerate([q for q in leads if q not in sup], 1):
        sup[q] = serp.fetch("bing", q)[:10]
        save("supply.json", sup)
        print(f"supply {n}: {q!r} {sum(1 for r in sup[q] if r.get('rank'))} results", flush=True)
        time.sleep(args.pause)
    todo = [q for q in leads if q not in lab and any(r.get("rank") for r in sup.get(q, []))]
    usage: dict = {}
    for i in range(0, len(todo), 8):
        batch = todo[i:i + 8]
        user = "\n\n".join(f"QUERY: {q}\n" + "\n".join(f"{r['rank']}. {r['title']} | {r['url']}" for r in sup[q] if r.get("rank")) for q in batch)
        try:
            r = E.claude_cli_json(V.LABEL_SYSTEM, user, MODEL, V.LABEL_SCHEMA, timeout=300, usage=usage) or {}
        except Exception as e:  # noqa: BLE001
            print("label error", e, flush=True)
            continue
        for it in r.get("items") or []:
            if it.get("q") in batch:
                lab[it["q"]] = it.get("results") or []
        save("supply_labels.json", lab)
    print("usage", usage)


def label_results(sup: dict, lab: dict, todo: list[str], save_as: str | None = None) -> dict:
    """Label each query's top 10 (kind + written-for-the-query) with voidscan's labeller, 8 queries per claude -p call."""
    import voidscan as V
    usage: dict = {}
    for i in range(0, len(todo), 8):
        batch = todo[i:i + 8]
        user = "\n\n".join(f"QUERY: {q}\n" + "\n".join(f"{r['rank']}. {r['title']} | {r['url']}" for r in sup[q] if r.get("rank")) for q in batch)
        try:
            r = E.claude_cli_json(V.LABEL_SYSTEM, user, MODEL, V.LABEL_SCHEMA, timeout=300, usage=usage) or {}
        except Exception as e:  # noqa: BLE001
            print("label error", e, flush=True)
            continue
        for it in r.get("items") or []:
            if it.get("q") in batch:
                lab[it["q"]] = it.get("results") or []
        if save_as:
            save(save_as, lab)
    return usage


def _src_readings(src: str, qs: list[str]) -> tuple[dict, dict]:
    """Top-10 readings and labels of `src` for the queries, fetched (capped, ledgered) and labelled where missing.
    `bing` is the Agent Chrome reading already in supply.json; every other source is cached in srccal_<src>.json."""
    import serpsources as S
    if src == "bing":
        return load("supply.json", {}), load("supply_labels.json", {})
    ssup, slab = load(f"srccal_{src}.json", {}), load(f"srccal_{src}_labels.json", {})
    todo = [q for q in qs if q not in ssup]
    if todo and src == "dataforseo":   # one Standard-queue batch instead of one wait per query
        got = S.dataforseo_many(todo)
        for q, res in got.items():
            if res is not None:
                ssup[q] = res
        save(f"srccal_{src}.json", ssup)
        print(f"{src}: {sum(1 for r in got.values() if r is not None)}/{len(todo)} readings", flush=True)
    else:
        misses = 0
        for q in todo:
            res = S.fetch(src, q)
            if res is None:   # one network blip (DNS failure seen 11-06) skips the query; three in a row, or a cap, stop
                misses += 1
                if misses >= 3 or S.room(src) <= 0 or S.key(src) is None:
                    print(f"{src}: no reading for {q!r} (cap, key or 3 errors in a row); stopping", flush=True)
                    break
                print(f"{src}: no reading for {q!r} (error); skipping", flush=True)
                continue
            misses = 0
            ssup[q] = res
            save(f"srccal_{src}.json", ssup)
            print(f"{src}: {q!r} {len(res)} results", flush=True)
    label_results(ssup, slab, [q for q in qs if q in ssup and q not in slab and ssup[q]], f"srccal_{src}_labels.json")
    return ssup, slab


def srccal(args) -> None:
    """Does one source's coverage track another's? Default reference: the Agent Chrome Bing readings. Reads the
    Bing-scored lead queries (>= MIN_RESULTS results) on `--source` (and on `--ref` when it isn't bing), labels each
    top 10 the same way, and reports Spearman and gate agreement (coverage < 0.4 on both).
    2026-11-06 (Barry): is a gap on Bing also a gap in OpenAI's index? `--source openai`, `--source dataforseo`,
    `--source openai --ref dataforseo`."""
    sup, lab = load("supply.json", {}), load("supply_labels.json", {})
    qs = [q for q in lab if sum(1 for r in sup.get(q, []) if r.get("rank")) >= MIN_RESULTS and lab[q]]
    if getattr(args, "n", None):   # a fixed sample: the first n in label order, the same set for every source pair
        qs = qs[:args.n]
    pool = getattr(args, "pool", "bing") or "bing"
    if pool in ("backlog", "both"):   # 2026-11-06: widen past the Bing-scored set with the biggest unscored clusters
        vol, dep = vols(), load("depth.json", {})
        rows = []
        for c in clusters():
            if not c["queries"] or c["covered_by"]:
                continue
            n = sum(vol.get(x["q"], 0) for x in c["queries"])
            sq = supply_query(lead_of(c, dep, vol))
            if n >= MIN_SEARCHES and sq not in qs and not (sq in lab and sum(1 for r in sup.get(sq, []) if r.get("rank")) >= MIN_RESULTS):
                rows.append((n, sq))
        rows.sort(reverse=True)
        back = list(dict.fromkeys(sq for _, sq in rows))[:getattr(args, "n_backlog", 110)]
        qs = back if pool == "backlog" else qs + back
        print(f"srccal sample: {len(qs)} queries ({len(back)} from the unscored backlog)", flush=True)
    src, ref = args.source, (getattr(args, "ref", None) or "bing")
    rsup, rlab = _src_readings(ref, qs)
    ssup, slab = _src_readings(src, qs)
    both = [q for q in qs if rlab.get(q) and slab.get(q)]
    pairs = [(coverage(rlab[q]), coverage(slab[q])) for q in both]
    if len(pairs) < 5:
        print(f"{src} vs {ref}: only {len(pairs)} paired readings"); return
    rho = spearman([a for a, _ in pairs], [b for _, b in pairs])
    agree = sum(1 for a, b in pairs if (a < GATE) == (b < GATE))
    ru = {q: [r["url"].split("#")[0].rstrip("/") for r in rsup.get(q, []) if r.get("rank") and r.get("url")][:10] for q in both}
    su = {q: [r["url"].split("#")[0].rstrip("/") for r in ssup.get(q, []) if r.get("rank") and r.get("url")][:10] for q in both}
    overlap = [len(set(ru[q]) & set(su[q])) / max(len(ru[q]), 1) for q in both]
    out = {"source": src, "ref": ref, "n": len(pairs), "spearman": round(rho, 3), "gate_agree": agree,
           "ref_open": sum(1 for a, _ in pairs if a < GATE), "src_open": sum(1 for _, b in pairs if b < GATE),
           "url_overlap_mean": round(sum(overlap) / len(overlap), 3),
           "pairs": {q: [coverage(rlab[q]), coverage(slab[q])] for q in both}}
    import random as _r
    rng, boots = _r.Random(7), []
    for _ in range(1000):   # bootstrap 95% interval for the Spearman, resampling clusters
        smp = [pairs[rng.randrange(len(pairs))] for _ in pairs]
        try:
            boots.append(spearman([a for a, _ in smp], [b for _, b in smp]))
        except Exception:  # noqa: BLE001  (a degenerate resample)
            pass
    boots.sort()
    out["spearman_ci95"] = [round(boots[int(0.025 * len(boots))], 3), round(boots[int(0.975 * len(boots)) - 1], 3)] if boots else None
    out["pool"] = pool
    name = f"srccal_{src}_result.json" if ref == "bing" else f"srccal_{src}_vs_{ref}_result.json"
    if pool != "bing":
        name = name.replace("_result.json", f"_{pool}_result.json")
    save(name, out)
    print(f"{src} vs {ref}: n={len(pairs)} Spearman {rho:.2f}; gate (<{GATE}) agrees on {agree}/{len(pairs)}; "
          f"open on {ref} {out['ref_open']}, on {src} {out['src_open']}; top-10 URL overlap {out['url_overlap_mean']:.0%}; "
          f"Spearman 95% CI {out['spearman_ci95']}")


MIN_RESULTS = 6   # fewer organic results than this = the page did not load fully; no coverage reading


def coverage(results: list[dict]) -> float:
    """Share of the query's demand the current top 10 already serves, 0..1: dedicated pages count by source kind and
    rank (position-weighted like click share), non-dedicated pages a quarter of that."""
    pos = [0.28, 0.16, 0.11, 0.08, 0.07, 0.06, 0.05, 0.04, 0.04, 0.03]
    tot = 0.0
    for r in results:
        k = r.get("rank", 0)
        if not 1 <= k <= 10:
            continue
        w = COVER_W.get(r.get("kind", "other"), 0.2) * (1.0 if r.get("dedicated") else 0.25)
        tot += pos[k - 1] * w
    return round(min(tot / sum(pos) * 1.6, 1.0), 3)   # 1.6: a top 10 of dedicated niche pages (0.5) reads as ~80% served


# ---------------------------------------------------------------- report

BWT = "https://ssl.bing.com/webmaster/api.svc/json/"


def bwt(method: str, **params) -> list | None:
    """Bing Webmaster Tools API (key in the keychain as bing-webmaster-api-key, created 2026-11-05). Free; no published
    rate limit, but measured 2026-11-05: one caller at ~1.6 calls/s ran 200 calls clean, while 4 parallel callers got
    {"ErrorCode":4,"Message":"ERROR!!! ThrottleUser"} after ~150 calls, cleared within a minute. So: --workers 1."""
    if not hasattr(bwt, "key"):
        bwt.key = subprocess.run(["security", "find-generic-password", "-s", "bing-webmaster-api-key", "-w"],
                                 capture_output=True, text=True).stdout.strip()
    q = urllib.parse.urlencode({**params, "apikey": bwt.key})
    for wait in (60, 60, 120, None):
        raw = _get(f"{BWT}{method}?{q}", timeout=30)
        if raw:
            try:
                return json.loads(raw).get("d")
            except ValueError:
                pass
        if wait is None:
            return None
        time.sleep(wait)


def _ms(d: str) -> int:
    return int(re.search(r"-?\d+", d).group())


def volume(args) -> None:
    """Real Bing US search counts (Bing Webmaster Tools API). Per seed: GetRelatedKeywords for the seed and 'best <seed>'
    (3-month window). Then GetKeywordStats (weekly series) for every variant of the top clusters, summed over the
    latest 13 weeks. A query with no rows is below Bing's reporting threshold, itself a low-volume signal."""
    import datetime as dt
    end = date.today() - dt.timedelta(days=14)
    start = end - dt.timedelta(days=89)
    out = load("volume.json", {"volumes": {}})
    out.setdefault("api_done", [])
    out["window"] = [start.isoformat(), end.isoformat()]
    done = set(out["api_done"])
    seeds = sorted({s for v in BRANDS.values() for s in v["seeds"]})
    jobs = [("rel", kw) for s in seeds for kw in (s, f"best {s}")]
    for c in [c for c in clusters() if c["queries"]][: args.top]:
        jobs += [("stats", x["q"]) for x in c["queries"]]
    jobs = [j for j in dict.fromkeys(jobs) if f"{j[0]}|{j[1]}" not in done]
    print(f"volume (API): {len(jobs)} calls", flush=True)

    def one(job):
        kind, kw = job
        if kind == "rel":
            return job, bwt("GetRelatedKeywords", q=kw, country="us", language="en-US", startDate=start.isoformat(), endDate=end.isoformat())
        return job, bwt("GetKeywordStats", q=kw, country="us", language="en-US")

    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for n, f in enumerate(cf.as_completed([ex.submit(one, j) for j in jobs]), 1):
            (kind, kw), d = f.result()
            if d is not None:
                if kind == "rel":
                    for r in d:
                        q = (r.get("Query") or "").strip().lower()
                        if q:
                            out["volumes"][q] = max(out["volumes"].get(q, 0), int(r.get("Impressions") or 0))
                elif d:
                    last = max(_ms(r["Date"]) for r in d)
                    out["volumes"][kw] = max(out["volumes"].get(kw, 0),
                                             sum(int(r.get("Impressions") or 0) for r in d if _ms(r["Date"]) > last - 91 * 86400 * 1000))
                out["api_done"].append(f"{kind}|{kw}")
            if n % 100 == 0 or n == len(jobs):
                save("volume.json", out)
                print(f"volume {n}/{len(jobs)}: {len(out['api_done'])} done, {len(out['volumes'])} queries with counts", flush=True)
    save("volume.json", out)


def msvolume(args) -> None:
    """Bing US search counts from Microsoft Advertising Ad Insight (tools/msads.py): last 3 complete months, all
    devices, 1,000 keywords per call, for every variant of every cluster. Added 2026-11-05 when the Webmaster API hit
    an undocumented daily cap after ~700 calls. Stored as volume.json["ms"]; calibrate() compares it with the
    Webmaster counts."""
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "tools"))
    import msads
    out = load("volume.json", {"volumes": {}})
    ms = out.setdefault("ms", {})
    qs = [q for q in dict.fromkeys(x["q"] for c in clusters() for x in c["queries"]) if q not in ms and len(q) <= 100]
    qs += [q for q in out.get("volumes", {}) if q not in ms and q not in qs and len(q) <= 100][: args.calib]
    print(f"msvolume: {len(qs)} queries, {-(-len(qs) // 1000)} calls", flush=True)
    for i in range(0, len(qs), 1000):
        ms.update(msads.search_counts(qs[i:i + 1000]))
        save("volume.json", out)
        print(f"msvolume {min(i + 1000, len(qs))}/{len(qs)}: {sum(v is not None for v in ms.values())} with counts", flush=True)


def volcal(args) -> None:
    """Webmaster (impressions, ~3 months) vs Ad Insight (searches, 3 complete months) on queries both report."""
    import statistics as st
    out = load("volume.json", {})
    wm, ms = out.get("volumes", {}), out.get("ms", {})
    both = [(wm[q], ms[q]) for q in wm if ms.get(q) and wm[q]]
    if len(both) < 20:
        print(f"calibrate: only {len(both)} shared queries"); return
    lw, lm = [math.log(a) for a, _ in both], [math.log(b) for _, b in both]
    mw, mm = st.mean(lw), st.mean(lm)
    r = sum((a - mw) * (b - mm) for a, b in zip(lw, lm)) / math.sqrt(sum((a - mw) ** 2 for a in lw) * sum((b - mm) ** 2 for b in lm))
    rw, rm = (sorted(range(len(lw)), key=lambda i: v[i]) for v in (lw, lm))
    rank = [0] * len(lw); rank2 = [0] * len(lw)
    for k, i in enumerate(rw): rank[i] = k
    for k, i in enumerate(rm): rank2[i] = k
    rho = 1 - 6 * sum((a - b) ** 2 for a, b in zip(rank, rank2)) / (len(lw) * (len(lw) ** 2 - 1))
    ratio = st.median(a / b for a, b in both)
    out["calibration"] = {"shared": len(both), "pearson_log": round(r, 3), "spearman": round(rho, 3),
                          "median_wm_over_ms": round(ratio, 3)}
    save("volume.json", out)
    print(json.dumps(out["calibration"]))


def report(args) -> None:
    dep, sup, lab = load("depth.json", {}), load("supply.json", {}), load("supply_labels.json", {})
    _v = load("volume.json", {})
    # One source per ranking: Ad Insight when present (complete coverage), else the Webmaster counts.
    vol = {q: v for q, v in _v.get("ms", {}).items() if v} or _v.get("volumes", {})
    rows = []
    for c in clusters():
        if not c["queries"]:
            continue
        leads = c["queries"][:3]
        d = max((dep.get(x["q"], {}).get("demand", -1) for x in leads), default=-1)
        lead = max(leads, key=lambda x: dep.get(x["q"], {}).get("demand", 0))["q"]
        sq = supply_query(lead)
        n_res = sum(1 for x in sup.get(sq, []) if x.get("rank"))
        cov = coverage(lab[sq]) if sq in lab and n_res >= MIN_RESULTS else None
        searches = sum(vol.get(x["q"], 0) for x in c["queries"])   # Bing US, 3 months, summed over the cluster's variants
        rows.append({**c, "lead": lead, "demand": d if d >= 0 else None, "coverage": cov,
                     "searches": searches, "lead_searches": vol.get(lead, 0),
                     "open_searches": round(searches * (1 - cov)) if cov is not None and searches else None,
                     "opening": round(d * (1 - cov), 3) if d >= 0 and cov is not None else None,
                     "supply_query": sq,
                     "top10": [{"rank": r["rank"], "title": next((x["title"] for x in sup.get(sq, []) if x["rank"] == r["rank"]), ""),
                                "kind": r["kind"], "dedicated": r["dedicated"]} for r in lab.get(sq, [])]})
    # Real counts first (uncovered searches), then the autocomplete proxy for clusters below Bing's threshold.
    rows.sort(key=lambda r: (-(r["open_searches"] or 0), -(r["opening"] or -1), -r["surface"]))
    save("report.json", rows)
    brand_link = {b: v["linked"] for b, v in BRANDS.items()}
    L = [f"# Gap mining report ({RUN.name})", "",
         "opening = demand x (1 - coverage). demand: keystroke depth on Google + Bing autocomplete, 0..1 (1 = suggested "
         "after the first letter). coverage: position-weighted share of the live Bing top 10 that is a page written for "
         "the query, weighted by source kind. Brand-named queries and non-buying intents are excluded.", "",
         "Ranked by **uncovered searches** = Bing US searches (3 months, Bing Webmaster Keyword Research, summed over the "
         "cluster's variants) x (1 - coverage); clusters below Bing's reporting threshold follow, ranked by the proxy.", "",
         "| # | cluster | lead query (coverage read on) | Bing searches 3 mo | demand proxy | coverage | uncovered searches | opening (proxy) | variants | brands | we cover |",
         "|---:|---|---|---:|---:|---:|---:|---:|---:|---|---|"]
    for i, r in enumerate([r for r in rows if r["opening"] is not None][: args.show], 1):
        brands = ", ".join(b + ("" if brand_link.get(b) else "*") for b in r["brands"])
        L.append(f"| {i} | {r['cluster']} | {r['lead']}" + (f" ({r['supply_query']})" if r['supply_query'] != r['lead'] else "") + f" | {r['searches'] or '<threshold'} | {r['demand']} | {r['coverage']} | **{r['open_searches'] or '–'}** | {r['opening']} | "
                 f"{len(r['queries'])} | {brands} | {', '.join(r['covered_by']) or '–'} |")
    L += ["", "\\* brand approved but not linked yet.", ""]
    # Reddit lane: buying questions asked this month in the category's own subreddits, grouped by need
    red = [c for c in clusters() if c["reddit"]]
    red.sort(key=lambda c: (-len(c["reddit"]), -c["reddit_comments"]))
    L += ["## Reddit hot topics (top posts of the month in category subreddits, buying questions only)", "",
          "| need | threads | comments | example | also in autocomplete |", "|---|---:|---:|---|---|"]
    for c in red[:25]:
        ex = max(c["reddit"], key=lambda p: p["comments"])
        L.append(f"| {c['cluster']} | {len(c['reddit'])} | {c['reddit_comments']} | [{ex['title'][:70]}]({ex['url']}) | "
                 f"{c['queries'][0]['q'] if c['queries'] else '–'} |")
    # Launch lane
    lr = load("launch_report.json", [])
    if lr:
        L += ["", "## Launch lane (new models in the brands' news, last 45 days)", "",
              "| lead query | brand | demand | coverage | opening | independent pages written for it |", "|---|---|---:|---:|---:|---:|"]
        for x in lr:
            L.append(f"| {x['query']} | {x['brand']} | {x['demand']} | {x['coverage']} | **{x['opening']}** | {x['independent_dedicated']} |")
    (RUN / "report.md").write_text("\n".join(L) + "\n")
    print("\n".join(L[:40]))


def backfill(args) -> None:
    """Keystroke depth of each published gap/compare page's own title query: did we build where people search?"""
    sys.path.insert(0, str(ROOT / "src"))
    import compare
    import gaps
    out = load("backfill.json", {})
    todo = []
    for p in gaps.GAP_PAGES + compare.COMPARISONS:
        q = re.sub(r"\s*[\(:].*$", "", p["title"]).strip().lower()
        q = re.sub(r"[^a-z0-9 $.\-]", "", q)
        if p["slug"] not in out:
            todo.append((p["slug"], p["question"], q))
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(depth, q): (slug, qid, q) for slug, qid, q in todo}
        for f in cf.as_completed(futs):
            slug, qid, q = futs[f]
            d = f.result()
            out[slug] = {"question": qid, "query": q, **d, "demand": demand_from_depth(d)}
            save("backfill.json", out)
    print(f"backfill: {len(out)} pages")


HEAD_SCHEMA = {"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {
    "slug": {"type": "string"}, "head": {"type": "string"}}, "required": ["slug", "head"]}}}, "required": ["items"]}
HEAD_SYSTEM = """For each page (slug and title) write the shortest search a shopper with this page's need would most
likely type into Google, 2 to 6 words, lowercase, no year, no brand names unless the need is about one product
(e.g. "Best power banks for flying (2026): airline rules and picks under 100 Wh" -> "power bank for flying").
Copy slug exactly."""


def backfill_head(args) -> None:
    """Fairer backfill: the page's need in a shopper's shortest words (Claude), keystroke depth on Bing only. An upper
    bound on the page's demand: a page whose short form is never suggested serves a need almost nobody searches."""
    bf = load("backfill.json", {})
    out = load("backfill_head.json", {})
    sys.path.insert(0, str(ROOT / "src"))
    import compare
    import gaps
    pages = {p["slug"]: p["title"] for p in gaps.GAP_PAGES + compare.COMPARISONS}
    if not all(s in out for s in pages):
        r = E.claude_cli_json(HEAD_SYSTEM, "\n".join(f"{s} :: {t}" for s, t in pages.items() if s not in out), MODEL,
                              HEAD_SCHEMA, timeout=600) or {}
        for it in r.get("items") or []:
            if it["slug"] in pages:
                out[it["slug"]] = {"head": it["head"].lower().strip()}
        save("backfill_head.json", out)
    todo = [s for s, r in out.items() if "bing" not in r]
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        futs = {ex.submit(depth, out[s]["head"], ("bing",)): s for s in todo}
        for f in cf.as_completed(futs):
            d = f.result()
            out[futs[f]].update(d)
            out[futs[f]]["demand"] = demand_from_depth(d)
            save("backfill_head.json", out)
    rep = {r["slug"]: r for r in load("backfill_report.json", [])}
    rows = sorted(((s, r["head"], r.get("demand", 0), rep.get(s, {}).get("age"), rep.get(s, {}).get("land", 0)) for s, r in out.items()),
                  key=lambda x: -x[2])
    for lo, hi in ((0, 0.001), (0.001, 0.3), (0.3, 0.6), (0.6, 1.01)):
        g = [x for x in rows if lo <= x[2] < hi]
        print(f"head demand {lo}-{hi}: {len(g)} pages, landings {sum(x[4] for x in g)}")
    (RUN / "backfill_head.md").write_text("| page | shopper's short form | Bing depth demand | age (d) | landings |\n|---|---|---:|---:|---:|\n" +
                                         "\n".join(f"| /{a} | {b} | {c} | {d} | {e} |" for a, b, c, d, e in rows) + "\n")


def backfill_report(args) -> None:
    """Join backfill demand with the latest page scoreboard (outside fetches + landings) and page age."""
    bf = load("backfill.json", {})
    sb = sorted((ROOT / "growth/scoreboard").glob("*.md"))[-1].read_text()
    sig = {}
    for line in sb.splitlines():
        m = re.match(r"\| /([a-z0-9-]+) \| (?:gap|compare) [^|]*\|[^|]*\| (\d+) \| (\d+) \| (\d+) \| (\d+) \|", line)
        if m and m.group(1) not in sig:   # first table only ("Pages with outside signal"); later tables differ
            sig[m.group(1)] = {"fetch": int(m.group(3)), "land": int(m.group(4)), "go": int(m.group(5))}
    sys.path.insert(0, str(ROOT / "src"))
    import compare
    import gaps
    pub = {p["slug"]: p.get("published", "") for p in gaps.GAP_PAGES + compare.COMPARISONS}
    rows = []
    for slug, r in bf.items():
        s_ = sig.get(slug, {"fetch": 0, "land": 0, "go": 0})
        age = (date.today() - date.fromisoformat(pub[slug])).days if pub.get(slug) else None
        rows.append({"slug": slug, "query": r["query"], "demand": r["demand"], "age": age, **s_})
    rows.sort(key=lambda r: -r["demand"])
    save("backfill_report.json", rows)
    L = ["| page | title query | demand | age (d) | outside fetches | landings |", "|---|---|---:|---:|---:|---:|"]
    for r in rows:
        L.append(f"| /{r['slug']} | {r['query']} | {r['demand']} | {r['age']} | {r['fetch']} | {r['land']} |")
    (RUN / "backfill.md").write_text("\n".join(L) + "\n")
    for lo, hi in ((0, 0.001), (0.001, 0.3), (0.3, 0.6), (0.6, 1.01)):
        g = [r for r in rows if lo <= r["demand"] < hi]
        old = [r for r in g if (r["age"] or 0) >= 6]
        print(f"demand {lo}-{hi}: {len(g)} pages ({len(old)} aged 6d+), landings {sum(r['land'] for r in g)}, "
              f"outside fetches {sum(r['fetch'] for r in g)}; aged 6d+: landings {sum(r['land'] for r in old)}")


# ---------------------------------------------------------------- daily $0 run (growth/gapmine/daily-plan.md)

POOL = "pool"          # one accumulating run folder for the daily job
SEEDS_PER_DAY = 8      # ~100 autocomplete calls per seed (Google, Bing, Amazon), paced
MIN_SEARCHES = 500     # Ad Insight Bing US searches over 3 months, summed over the cluster's variants
GATE = 0.4             # coverage below this goes to the page queue (vote and coverage agreed on 11-05)
# Barry 2026-11-06: gate on Claude's search alone ($0) until the business breaks even (DLC-190/191). Against OpenAI's
# index on 142 clusters, Claude coverage < 0.3 picks with precision 0.70 / recall 0.80 (< 0.4: 0.58 / 0.82).
GATE_BY_SOURCE = {"claude": 0.3}


def gate_for(source: str) -> float:
    return GATE_BY_SOURCE.get(source, GATE)
EXPAND_KEYS = None


def _seed_done(seed: str, done: set) -> bool:
    keys = [f"{eng}|{t.format(s=seed)}" for t in STEMS + LETTERS for eng in ("google", "bing") + (("amazon",) if t in STEMS else ())]
    return all(k in done for k in keys)


def lead_of(c: dict, dep: dict, vol: dict) -> str:
    """The cluster's lead query: by keystroke depth where it was measured, else by Ad Insight searches."""
    if any(x["q"] in dep for x in c["queries"][:3]):
        return max(c["queries"][:3], key=lambda x: dep.get(x["q"], {}).get("demand", 0))["q"]
    return max(c["queries"], key=lambda x: (vol.get(x["q"]) or 0, x["surface"]))["q"]


MS_BLOCK = ROOT / "growth/gapmine/msads_blocked.json"
WM_TO_MS = 5.0          # volcal 11-05: Webmaster ~= 0.20 x Ad Insight on 3,175 queries both report
WM_DAILY = 300          # Webmaster GetKeywordStats calls per day (an undocumented cap stopped it after ~700 on 11-05)


def vols() -> dict:
    """Search counts on the Ad Insight scale: Ad Insight where it has them, else Webmaster x WM_TO_MS (estimated)."""
    v = load("volume.json", {})
    ms = {q: n for q, n in v.get("ms", {}).items() if n}
    wm = {q: round(n * WM_TO_MS) for q, n in v.get("volumes", {}).items() if n and q not in ms}
    return {**wm, **ms}


def wm_fill(args) -> dict:
    """Webmaster counts for cluster variants Ad Insight hasn't counted, at most WM_DAILY calls per calendar day across
    every pass (fallback while Microsoft Ads is blocked). The day's calls are kept in volume.json "wm_calls" (11-11: the
    cap used to reset with each `daily` run, so three passes made ~900 calls)."""
    out = load("volume.json", {"volumes": {}})
    out.setdefault("api_done", [])
    calls = out.setdefault("wm_calls", {})
    day = date.today().isoformat()
    room = max(0, WM_DAILY - calls.get(day, 0))
    done, ms = set(out["api_done"]), out.get("ms", {})
    qs = [x["q"] for c in clusters() if c["queries"] and not c["covered_by"] for x in c["queries"][:6]]
    qs = [q for q in dict.fromkeys(qs) if q not in ms and f"stats|{q}" not in done][:room]
    got = 0
    for q in qs:
        d = bwt("GetKeywordStats", q=q, country="us", language="en-US")
        calls[day] = calls.get(day, 0) + 1   # a failed call still counts against the day
        if d is None:   # throttled or failed: stop for today, never retry in a loop
            break
        if d:
            last = max(_ms(r["Date"]) for r in d)
            out["volumes"][q] = sum(int(r.get("Impressions") or 0) for r in d if _ms(r["Date"]) > last - 91 * 86400 * 1000)
            got += 1
        out["api_done"].append(f"stats|{q}")
    save("volume.json", out)
    return {"asked": len(qs), "with_counts": got, "calls_today": calls.get(day, 0), "cap": WM_DAILY}


def supply_daily(args) -> dict:
    """Coverage for the biggest unscored clusters, through the capped free sources (serpsources.py), largest first."""
    import serpsources as S
    vol = vols()
    dep, sup, lab = load("depth.json", {}), load("supply.json", {}), load("supply_labels.json", {})
    src_of = load("supply_source.json", {})
    rows = []
    for c in clusters():
        if not c["queries"] or c["covered_by"]:
            continue
        n = sum(vol.get(x["q"], 0) for x in c["queries"])
        sq = supply_query(lead_of(c, dep, vol))
        if n >= MIN_SEARCHES and not (sq in lab and sum(1 for r in sup.get(sq, []) if r.get("rank")) >= MIN_RESULTS):
            rows.append((n, sq))
    rows.sort(reverse=True)
    read = {}
    for n, sq in rows:
        srcs = [x for x in S.available() if x in args.sources.split(",")]
        if not srcs:
            break
        res = S.fetch(srcs[0], sq)
        if res is None:
            continue
        sup[sq], src_of[sq] = res, srcs[0]
        read[srcs[0]] = read.get(srcs[0], 0) + 1
        save("supply.json", sup); save("supply_source.json", src_of)
    label_results(sup, lab, [q for q in src_of if q not in lab and len(sup.get(q) or []) >= MIN_RESULTS], "supply_labels.json")
    return {"unscored_over_min": len(rows), "read": read}


def queue_step(args) -> list[dict]:
    """Clusters that pass the gate (searches >= MIN_SEARCHES, coverage < GATE, no page of ours) join the page queue."""
    qpath = ROOT / "growth/gapmine/queue.json"
    queue = json.loads(qpath.read_text()) if qpath.exists() else []
    have = {(x["seed"], x["cluster"]) for x in queue}
    vol = vols()
    dep, sup, lab = load("depth.json", {}), load("supply.json", {}), load("supply_labels.json", {})
    src_of = load("supply_source.json", {})
    added = []
    for c in clusters():
        if not c["queries"] or c["covered_by"] or (c["seed"], c["cluster"]) in have:
            continue
        lead = lead_of(c, dep, vol); sq = supply_query(lead)
        if not (sq in lab and len(sup.get(sq) or []) >= MIN_RESULTS):
            continue
        n, cov = sum(vol.get(x["q"], 0) for x in c["queries"]), coverage(lab[sq])
        import serpsources as S
        if n >= MIN_SEARCHES and cov < gate_for(src_of.get(sq, "bing")) and src_of.get(sq, "bing") in S.GATING:
            added.append({"seed": c["seed"], "cluster": c["cluster"], "lead": lead, "supply_query": sq, "searches": n,
                          "coverage": cov, "uncovered": round(n * (1 - cov)), "source": src_of.get(sq, "bing"),
                          "brands": c["brands"], "variants": [x["q"] for x in c["queries"][:10]],
                          "queued": date.today().isoformat(), "status": "new"})
    queue += sorted(added, key=lambda x: -x["uncovered"])
    qpath.write_text(json.dumps(queue, indent=1) + "\n")
    return added


def prune_pool() -> None:
    """Keep the pool's suggest.json small enough to commit (the daily job runs in another clone): once a seed is
    labelled, only its labelled queries matter; the 'done' keys stay so nothing is fetched twice."""
    sug, lab = load("suggest.json", {"done": [], "queries": {}}), load("labels.json", {})
    keep = {}
    for q, r in sug["queries"].items():
        if r["seed"] not in lab or q in lab[r["seed"]]:
            keep[q] = r
    sug["queries"] = keep
    (RUN / "suggest.json").write_text(json.dumps(sug, separators=(",", ":")))


def daily(args) -> None:
    """One unattended $0 pass: widen seeds -> expand a few new seeds -> label -> Ad Insight volume -> capped coverage
    -> gate -> queue. Writes growth/gapmine/daily/<date>.md with readings per source against each cap."""
    import serpsources as S
    global BRANDS
    log = {"date": date.today().isoformat()}
    pool = ROOT / "growth/gapmine/runs" / POOL
    if not (pool / "labels.json").exists():   # start the pool from the first full run
        import shutil
        for f in ("suggest.json", "labels.json", "volume.json", "supply.json", "supply_labels.json", "depth.json", "reddit.json"):
            if (ROOT / "growth/gapmine/runs/2026-11-05" / f).exists():
                shutil.copy(ROOT / "growth/gapmine/runs/2026-11-05" / f, pool / f)
    seeds_step(args)
    BRANDS = json.loads((ROOT / "growth/gapmine/brands.json").read_text())["brands"]
    done = set(load("suggest.json", {"done": []})["done"])
    pending = [s for v in BRANDS.values() for s in v["seeds"] if not _seed_done(s, done)]
    args.only_seeds = set(pending[:SEEDS_PER_DAY])
    log["seeds"] = {"pending": len(pending), "today": sorted(args.only_seeds)}
    if args.only_seeds:
        expand(args)
    done = set(load("suggest.json", {"done": []})["done"])
    labelled = set(load("labels.json", {}))
    args.only_seeds = {s for v in BRANDS.values() for s in v["seeds"] if _seed_done(s, done) and s not in labelled}
    if args.only_seeds:
        label(args)
    if MS_BLOCK.exists():   # Microsoft suspended the account on 11-05 (reinstatement is Barry's, DLC-178): don't retry
        b = json.loads(MS_BLOCK.read_text())
        log["msvolume"] = f"BLOCKED since {b['date']} (DLC-178: {b['reason'][:120]}); Webmaster fallback"
    else:
        try:
            msvolume(args)
            log["msvolume"] = "ok"
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            if "InvalidCredentials" in msg or '"Code":105' in msg:
                MS_BLOCK.write_text(json.dumps({"date": date.today().isoformat(), "reason": msg[:300]}, indent=1) + "\n")
                log["msvolume"] = "BLOCKED today (HTTP 401 code 105: Microsoft Ads account suspended, DLC-178); Webmaster fallback"
            else:   # e.g. refresh token expired (tools/msads_auth.py, DLC-174)
                log["msvolume"] = f"FAILED: {msg}"[:300]
    if not log["msvolume"].startswith("ok"):
        log["webmaster"] = wm_fill(args)
        log["msvolume"] += f"; Webmaster counted {log['webmaster']['with_counts']} of {log['webmaster']['asked']} new variants (x{WM_TO_MS:g} to Ad Insight scale)"
    prune_pool()
    log["supply"] = supply_daily(args)
    log["queued"] = [f"{x['cluster']} ({x['uncovered']} uncovered, cov {x['coverage']}, {x['source']})" for x in queue_step(args)]
    log["sources"] = S.status()
    d = ROOT / "growth/gapmine/daily"
    d.mkdir(parents=True, exist_ok=True)
    md = [f"# Gap mining daily run {log['date']}", "",
          f"- Seeds: {len(log['seeds']['today'])} expanded today, {log['seeds']['pending']} pending: {', '.join(log['seeds']['today']) or '-'}",
          f"- Ad Insight volume: {log['msvolume']}",
          f"- Coverage: {log['supply']['unscored_over_min']} clusters >= {MIN_SEARCHES} searches unscored before today; read today: {log['supply']['read'] or 'none'}",
          f"- Queued for pages (coverage < {GATE_BY_SOURCE.get('claude', GATE)} on Claude): {len(log['queued'])}", *[f"  - {x}" for x in log["queued"]], "",
          "## Free sources, used / cap", "", "```", log["sources"], "```"]
    (d / f"{log['date']}.md").write_text("\n".join(md) + "\n")
    print("\n".join(md))


def main() -> None:
    global RUN
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=["expand", "reddit", "news", "launches", "label", "depth", "supply", "report", "backfill", "backfillreport", "calibrate", "launchsupply", "backfillhead", "volume", "msvolume", "volcal", "srccal", "seeds", "daily", "queue"])
    ap.add_argument("--run", default=date.today().isoformat())
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--pause", type=float, default=4.0)
    ap.add_argument("--top", type=int, default=120, help="depth/supply: clusters to measure, by surface score")
    ap.add_argument("--calib", type=int, default=3000, help="msvolume: extra Webmaster-counted queries fetched for calibration")
    ap.add_argument("--show", type=int, default=60)
    ap.add_argument("--force", action="store_true", help="seeds: redo brands already widened")
    ap.add_argument("--sources", default="claude", help="daily: coverage sources allowed, by priority (Claude only since 11-06, DLC-190)")
    ap.add_argument("--source", default="claude", help="srccal/supply: free SERP source (growth/evals/serpsources.py)")
    ap.add_argument("--ref", default="bing", help="srccal: reference source (default: the Agent Chrome Bing readings)")
    ap.add_argument("--pool", default="bing", choices=["bing", "backlog", "both"], help="srccal: Bing-scored set, unscored backlog, or both")
    ap.add_argument("--n-backlog", type=int, default=110, help="srccal: queries taken from the unscored backlog, biggest first")
    ap.add_argument("--n", type=int, default=60, help="calibrate: sample size")
    ap.add_argument("--leads", type=int, default=1, help="depth: lead queries measured per cluster")
    ap.add_argument("--min-demand", type=float, default=0.3, help="supply: skip clusters whose lead query scores below this")
    ap.add_argument("--min-surface", type=float, default=0.3, help="label: skip suggestions the engines barely push")
    args = ap.parse_args()
    if args.step in ("daily", "queue"):
        args.run = POOL
    RUN = ROOT / "growth/gapmine/runs" / args.run
    RUN.mkdir(parents=True, exist_ok=True)
    {"expand": expand, "reddit": reddit, "news": news, "launches": launches, "label": label, "depth": depth_step,
     "supply": supply, "report": report, "backfill": backfill, "backfillreport": backfill_report, "calibrate": calibrate, "launchsupply": launch_supply, "backfillhead": backfill_head, "volume": volume, "msvolume": msvolume, "volcal": volcal, "srccal": srccal, "seeds": seeds_step, "daily": daily, "queue": queue_step}[args.step](args)


if __name__ == "__main__":
    main()
