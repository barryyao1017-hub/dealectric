#!/usr/bin/env python3.12
"""Kit mining (DLC-223, Barry 2026-11-10): find "what do I need for X" queries where one researched bundle of products,
behind one buy link that opens a filled cart, is the answer.

Same rule as gapmine: opening = demand x (1 - coverage), and nothing starts from a query we made up. Candidates are what
Google and Bing autocomplete for kit-shaped stems ("<category> setup", "what do i need for <category>", "<situation>
essentials") over the category nouns our approved brands sell (growth/gapmine/brands.json) and the situations that
already appear in real suggestions in the gap pool. On top of gapmine's score a kit query must also need knowledge to
assemble (Barry: the bundle is worth handing over only when picking the set takes real compatibility or sizing
depth), and our catalog must be able to fill at least two of its items from one cart (one Shopify store, or Amazon).

Steps (each writes one JSON under growth/kits/runs/<run>/ and resumes):
    situations  Claude reads the gap pool's cluster names -> situations/projects shoppers name -> situations.json
    expand      (brand seeds + situations) x KIT stems -> Google/Bing autocomplete            -> suggest.json
    label       Claude: kit or not, brand-named, cluster, items needed, knowledge depth 0-3     -> labels.json
    volume      Bing Webmaster weekly counts for each cluster's variants (13 weeks)            -> volume.json
    depth       keystroke depth of the lead query (demand fallback where Webmaster has no row)  -> depth.json
    supply      capped free SERP reading of the lead query (serpsources gating source), labelled -> supply.json
    fit         Claude: which of our products fill which items, grouped by cart                  -> fit.json
    report      score and queue                                                                 -> report.md, queue.json
    python3.12 growth/evals/kitmine.py <step> --run 2026-11-10
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import math
import re
import sys
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import gapmine as G  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RUN: Path = ROOT / "growth/kits/runs" / date.today().isoformat()
MODEL = "claude-sonnet-5-5"

# Kit-shaped stems: what a shopper types when the answer is a set of things, not one product.
SEED_STEMS = ["{s} setup", "{s} kit", "{s} starter kit", "{s} accessories", "{s} essentials", "what do i need for {s}",
              "what do i need with a {s}", "what else do i need for {s}", "{s} setup for"]
SITU_STEMS = ["what do i need for {s}", "{s} setup", "{s} essentials", "{s} kit", "{s} gear list", "{s} must haves",
              "{s} power setup"]


def load(name, default):
    p = RUN / name
    return json.loads(p.read_text()) if p.exists() else default


def save(name, obj):
    RUN.mkdir(parents=True, exist_ok=True)
    E.write_json(RUN / name, obj)


def seeds() -> list[str]:
    b = json.loads((ROOT / "growth/gapmine/brands.json").read_text())["brands"]
    return list(dict.fromkeys(s for v in b.values() for s in v["seeds"]))


# ---------------------------------------------------------------- situations

SITU_SYSTEM = """You read cluster names from real search-engine autocomplete suggestions around consumer electronics
(power stations, solar, NAS, cameras, 3D printers, phones, chargers, smart home, outdoor gear...). List the SITUATIONS or
PROJECTS shoppers name in them: the activity, place or job the products are for, where a shopper would plausibly need
SEVERAL products that must work together (e.g. "van life", "cpap camping", "home lab", "starlink off grid",
"plex server", "ice fishing", "hurricane prep", "rv boondocking", "home security system", "dash cam install").
Rules: only situations that occur in the cluster names given (no inventions); 1-4 words, lowercase, no brand names, no
product nouns alone; merge near-duplicates; skip situations served by one product. Up to 120."""
SITU_SCHEMA = {"type": "object", "properties": {"situations": {"type": "array", "items": {"type": "object", "properties": {
    "s": {"type": "string"}, "evidence": {"type": "string"}}, "required": ["s", "evidence"]}}}, "required": ["situations"]}


def situations(args):
    if load("situations.json", None):
        print("situations: done"); return
    lab = json.loads((ROOT / "growth/gapmine/runs/pool/labels.json").read_text())
    names = sorted({l["cluster"] for items in lab.values() for l in items.values() if l.get("cluster")})
    print(f"situations: {len(names)} pool clusters", flush=True)
    out, usage = {}, {}
    for i in range(0, len(names), 1500):
        r = E.claude_cli_json(SITU_SYSTEM, "\n".join(names[i:i + 1500]), MODEL, SITU_SCHEMA, timeout=900, usage=usage) or {}
        for it in r.get("situations") or []:
            out.setdefault(it["s"].strip().lower(), it["evidence"])
    save("situations.json", out)
    print(f"situations: {len(out)}", usage)


# ---------------------------------------------------------------- expand

def expand(args):
    out = load("suggest.json", {"queries": {}, "done": []})
    done = set(out["done"])
    jobs = [(s, t, "seed") for s in seeds() for t in SEED_STEMS]
    jobs += [(s, t, "situation") for s in load("situations.json", {}) for t in SITU_STEMS]
    todo = [(s, t, k, eng) for s, t, k in jobs for eng in ("google", "bing") if f"{eng}|{t.format(s=s)}" not in done]
    print(f"expand: {len(todo)} calls", flush=True)

    def one(j):
        s, t, k, eng = j
        return j, G.ac(eng, t.format(s=s))

    n = 0
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for (s, t, k, eng), res in ex.map(one, todo):
            if res is None:
                continue   # failed: retried on the next run, never recorded as "no suggestions"
            prefix = t.format(s=s)
            for rank, q in enumerate(res, 1):
                r = out["queries"].setdefault(q, {"seed": s, "kind": k, "hits": []})
                r["hits"].append([eng, rank, prefix])
            out["done"].append(f"{eng}|{prefix}")
            n += 1
            if n % 500 == 0:
                save("suggest.json", out); print(f"expand {n}/{len(todo)}: {len(out['queries'])} queries", flush=True)
    save("suggest.json", out)
    print(f"expand: {len(out['queries'])} queries")


def surface(r) -> float:
    best = {}
    for eng, rank, _ in r["hits"]:
        best[eng] = max(best.get(eng, 0), (11 - min(rank, 10)) / 10)
    return round(sum(best.values()), 3)


# ---------------------------------------------------------------- label

LABEL_SYSTEM = """You label search queries for Dealectric, a US shopping-guide site for consumer electronics with
affiliate links. We are looking for queries whose best answer is a BUNDLE: a set of 2+ different products bought
together that must work together (e.g. a power station + the right solar panel + the right cable for a CPAP; a NAS +
CMR drives + a UPS whose USB shutdown the NAS supports; a 3D printer + filament dryer + the right build plate; a dash cam
+ hardwire kit + high-endurance card).

For each query return:
- kit: true if a good answer is a set of 2+ distinct products the shopper buys now (accessories for a product they
  already own count when there are 2+ of them). False for single-product questions, how-tos, troubleshooting, prices,
  jobs, services, software only, food, clothing, vehicles, furniture.
- named: true if it names a brand, store or model number.
- cluster: a short normalized label for the need (same need, different wording = same label), e.g. "cpap camping power
  setup", "plex nas starter kit".
- items: the product types the set needs (2-6, generic nouns).
- depth: how much knowledge it takes to pick a set that WORKS (0 = any items do; 1 = some sizing; 2 = real
  compatibility or sizing traps a shopper usually gets wrong; 3 = several interacting constraints (voltages, connectors,
  protocols, firmware, wattage vs runtime, standards) where a wrong pick fails or is unsafe).
Return every query given."""
LABEL_SCHEMA = {"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {
    "q": {"type": "string"}, "kit": {"type": "boolean"}, "named": {"type": "boolean"}, "cluster": {"type": "string"},
    "items": {"type": "array", "items": {"type": "string"}}, "depth": {"type": "integer"}},
    "required": ["q", "kit", "named", "cluster", "items", "depth"]}}}, "required": ["items"]}


def label(args):
    sug = load("suggest.json", {"queries": {}})["queries"]
    out = load("labels.json", {})
    qs = [q for q, r in sug.items() if q not in out and len(q.split()) >= 3 and not G.DROP.search(q)
          and surface(r) >= args.min_surface]
    print(f"label: {len(qs)} queries", flush=True)
    usage = {}

    def one(batch):
        r = E.claude_cli_json(LABEL_SYSTEM, "\n".join(batch), MODEL, LABEL_SCHEMA, timeout=600, usage=usage) or {}
        return {it["q"]: {k: it[k] for k in ("kit", "named", "cluster", "items", "depth")}
                for it in r.get("items") or [] if it.get("q") in batch}

    batches = [qs[i:i + 120] for i in range(0, len(qs), 120)]
    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for i, res in enumerate(ex.map(lambda b: _safe(one, b), batches), 1):
            out.update(res)
            save("labels.json", out)
            print(f"label batch {i}/{len(batches)}: {len(res)}", flush=True)
    print("usage", usage)


def _safe(fn, *a):
    try:
        return fn(*a)
    except Exception as e:  # noqa: BLE001
        print("error", e, flush=True)
        return {}


def clusters() -> list[dict]:
    sug, lab = load("suggest.json", {"queries": {}})["queries"], load("labels.json", {})
    cl = {}
    for q, l in lab.items():
        if not l["kit"] or l["named"] or q not in sug:
            continue
        c = cl.setdefault(l["cluster"], {"cluster": l["cluster"], "queries": [], "items": {}, "depths": []})
        c["queries"].append({"q": q, "surface": surface(sug[q])})
        c["depths"].append(l["depth"])
        for it in l["items"]:
            c["items"][it] = c["items"].get(it, 0) + 1
    out = []
    for c in cl.values():
        c["queries"].sort(key=lambda x: -x["surface"])
        c["depth"] = round(sum(c["depths"]) / len(c["depths"]), 2)
        c["items"] = [k for k, _ in sorted(c["items"].items(), key=lambda kv: -kv[1])][:6]
        c["surface"] = round(sum(x["surface"] for x in c["queries"]), 3)
        del c["depths"]
        out.append(c)
    return sorted(out, key=lambda c: -c["surface"])


def shortlist(args) -> list[dict]:
    return [c for c in clusters() if c["depth"] >= args.min_depth][: args.top]


def fitted(args) -> list[dict]:
    """Shortlisted clusters our catalog can fill with 2+ items in one cart (fit step)."""
    ft = load("fit.json", {})
    return [c for c in shortlist(args) if any(len(x["slugs"]) >= 2 for x in ft.get(c["cluster"], []))]


# ---------------------------------------------------------------- demand

def volume(args):
    import datetime as dt  # noqa: F401
    out = load("volume.json", {})
    qs = [x["q"] for c in shortlist(args) for x in c["queries"][:5]]
    qs = [q for q in dict.fromkeys(qs) if q not in out][: args.wm_cap]
    print(f"volume: {len(qs)} Webmaster calls", flush=True)
    for i, q in enumerate(qs, 1):
        d = G.bwt("GetKeywordStats", q=q, country="us", language="en-US")
        if d is None:
            print("volume: Webmaster stopped answering; resume later", flush=True); break
        if d:
            last = max(G._ms(r["Date"]) for r in d)
            out[q] = sum(int(r.get("Impressions") or 0) for r in d if G._ms(r["Date"]) > last - 91 * 86400 * 1000)
        else:
            out[q] = 0
        if i % 25 == 0:
            save("volume.json", out); print(f"volume {i}/{len(qs)}", flush=True)
    save("volume.json", out)


def depth_step(args):
    out = load("depth.json", {})
    vol = load("volume.json", {})
    leads = [lead(c, vol) for c in fitted(args)]
    todo = [q for q in leads if q not in out]
    print(f"depth: {len(todo)}", flush=True)
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        for q, d in zip(todo, ex.map(G.depth, todo)):
            out[q] = {**d, "demand": G.demand_from_depth(d)}
            save("depth.json", out)


def lead(c, vol) -> str:
    return max(c["queries"][:6], key=lambda x: (vol.get(x["q"]) or 0, x["surface"]))["q"]


def searches(c, vol) -> int:
    """Bing US searches over 13 weeks, summed over the cluster's counted variants."""
    return sum(vol.get(x["q"]) or 0 for x in c["queries"])


# ---------------------------------------------------------------- supply

def supply(args):
    import serpsources as S
    vol, dep = load("volume.json", {}), load("depth.json", {})
    sup, lab = load("supply.json", {}), load("supply_labels.json", {})
    cl = [c for c in fitted(args) if searches(c, vol) >= args.min_searches or dep.get(lead(c, vol), {}).get("demand", 0) >= 0.3]
    src = sorted(S.gating())[0] if S.gating() else "claude"
    todo = [lead(c, vol) for c in cl if lead(c, vol) not in sup]
    print(f"supply: {len(todo)} readings on {src}", flush=True)

    def one(q):
        return q, S.fetch(src, q)

    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        for q, res in ex.map(one, todo):
            if res and len(res) >= G.MIN_RESULTS:
                sup[q] = {"source": src, "results": [{**r, "rank": i} for i, r in enumerate(res[:10], 1)]}
                save("supply.json", sup)
    G.RUN = RUN
    need = [q for q in sup if q not in lab]
    G.label_results({q: v["results"] for q, v in sup.items()}, lab, need, save_as="supply_labels.json")
    save("supply_labels.json", lab)


# ---------------------------------------------------------------- fit

FIT_SYSTEM = """You match a shopper's kit need to Dealectric's catalog. A bundle link opens ONE store's cart with every
item in it, so items only bundle together when they are sold through the same cart: the same brand's own store
(network cj/awin/rakuten), or Amazon (program amazon:us, any brand). For the need, list the carts that could hold at
least 2 of the kit's items from our catalog, the product slugs for each item, and what the kit would still lack.
Be strict: a product fills an item only if it is genuinely that item and suits the need. Return carts best first."""
FIT_SCHEMA = {"type": "object", "properties": {"carts": {"type": "array", "items": {"type": "object", "properties": {
    "cart": {"type": "string"}, "slugs": {"type": "array", "items": {"type": "string"}},
    "covers": {"type": "array", "items": {"type": "string"}}, "lacks": {"type": "array", "items": {"type": "string"}}},
    "required": ["cart", "slugs", "covers", "lacks"]}}}, "required": ["carts"]}


def catalog() -> str:
    sys.path.insert(0, str(ROOT / "src"))
    import products as P
    return "\n".join(f"{p['slug']} | {p['brand']} | {p['program']} | {p['category']} | {p['name']}"
                     for p in P.PRODUCTS if p["slug"] not in P.RETIRED)


def fit(args):
    out = load("fit.json", {})
    vol = load("volume.json", {})
    cl = [c for c in shortlist(args) if c["cluster"] not in out]
    cat, usage = catalog(), {}
    print(f"fit: {len(cl)} clusters", flush=True)

    def one(c):
        u = f"NEED: {c['cluster']}\nQUERIES: {'; '.join(x['q'] for x in c['queries'][:6])}\nKIT ITEMS: {', '.join(c['items'])}"
        return c["cluster"], E.claude_cli_json(FIT_SYSTEM + "\n\nCATALOG (slug | brand | program | category | name):\n" + cat,
                                               u, MODEL, FIT_SCHEMA, timeout=600, usage=usage) or {}

    with cf.ThreadPoolExecutor(max_workers=args.workers) as ex:
        for k, r in ex.map(lambda c: _safe(one, c) or (c["cluster"], {}), cl):
            out[k] = r.get("carts") or []
            save("fit.json", out)
    print("usage", usage)


# ---------------------------------------------------------------- report

def ours_match(q: str) -> str:
    """The title of an existing page of ours that shares most of the query's words (>= 70%), else ''."""
    words = set(re.findall(r"[a-z0-9]+", q.lower())) - {"best", "for", "a", "the", "with", "and", "what", "do", "i", "need", "to", "of"}
    best = ("", 0.0)
    for t in G.our_pages():
        tw = set(re.findall(r"[a-z0-9]+", t.lower()))
        s = len(words & tw) / max(len(words), 1)
        if s > best[1]:
            best = (t, s)
    return best[0] if best[1] >= 0.7 else ""


def report(args):
    vol, dep, sup, lab, ft = (load(n, {}) for n in ("volume.json", "depth.json", "supply.json", "supply_labels.json", "fit.json"))
    rows = []
    for c in shortlist(args):
        q = lead(c, vol)
        if q not in lab:
            continue
        res = {r["rank"]: r for r in sup[q]["results"]}
        labelled = [{**res.get(x.get("rank"), {}), **x} for x in lab[q]]
        cov = G.coverage(labelled)
        n = searches(c, vol)
        dem = dep.get(q, {}).get("demand", 0)
        carts = [x for x in ft.get(c["cluster"], []) if len(x["slugs"]) >= 2]
        demand = n if n else round(dem * 300)   # depth 0.6 ~ 100+ searches per 3 months (gapmine calibrate)
        score = round(demand * (1 - cov) * (0.5 + c["depth"] / 3), 1)
        rows.append({"ours": ours_match(q), "cluster": c["cluster"], "lead": q, "searches": n, "depth_demand": dem, "coverage": cov,
                     "knowledge": c["depth"], "items": c["items"], "carts": carts, "score": score,
                     "variants": [x["q"] for x in c["queries"][:8]]})
    rows.sort(key=lambda r: -r["score"])
    gate = [r for r in rows if r["carts"] and r["coverage"] < args.max_cov]
    save("report.json", rows)
    save("queue.json", gate[: args.queue])
    md = [f"# Kit mining {RUN.name}", "", f"{len(rows)} clusters scored; {len(gate)} pass (a 2+ item cart from our catalog, "
          f"coverage < {args.max_cov}); queue = top {args.queue}.", "",
          "| # | cluster | lead query | searches (13 wk) | coverage | knowledge | best cart | score |", "|---|---|---|---|---|---|---|---|"]
    for i, r in enumerate(gate[: args.show], 1):
        cart = r["carts"][0]
        md.append(f"| {i} | {r['cluster']}{' (ours: ' + r['ours'][:50] + ')' if r['ours'] else ''} | {r['lead']} | {r['searches'] or '~' + str(round(r['depth_demand'] * 300))} | "
                  f"{r['coverage']} | {r['knowledge']} | {cart['cart']}: {', '.join(cart['slugs'])} | {r['score']} |")
    (RUN / "report.md").write_text("\n".join(md) + "\n")
    print("\n".join(md[:args.show + 6]))


def harvest_file(args):
    """growth/focus/kit-harvest-<run>.json: each queued cluster's lead query typed as is, plain prompt, two chats
    (the DLC-208 harvest, run with visibility_scan.py --n 2)."""
    q = load("queue.json", [])
    tag = "k" + RUN.name[5:7] + RUN.name[8:10]
    qs = []
    for i, r in enumerate(q):
        s = re.sub(r"[^a-z0-9]+", "-", r["cluster"].lower()).strip("-")[:50]
        qs.append({"qid": f"{tag}-{i:02d}-{s[:30]}--plain", "slug": f"{tag}-{s}", "cluster": r["cluster"], "level": "G2",
                   "type": "kit", "mode": "natural", "search": False, "prompt": r["lead"]})
    out = ROOT / f"growth/focus/kit-harvest-{RUN.name}.json"
    out.write_text(json.dumps({"version": RUN.name, "note": "Kit clusters (DLC-223): lead query typed as is, plain prompt, two chats, before research.",
                               "questions": qs}, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(qs)} questions -> {out.relative_to(ROOT)}")


def main():
    global RUN
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=["situations", "expand", "label", "volume", "depth", "supply", "fit", "report", "clusters", "harvestfile"])
    ap.add_argument("--run", default=date.today().isoformat())
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--min-surface", type=float, default=0.3)
    ap.add_argument("--min-depth", type=float, default=1.5, help="mean knowledge depth (0-3) a cluster needs")
    ap.add_argument("--top", type=int, default=150, help="clusters carried past label, by surface")
    ap.add_argument("--wm-cap", type=int, default=300)
    ap.add_argument("--min-searches", type=int, default=100)
    ap.add_argument("--max-cov", type=float, default=0.4)
    ap.add_argument("--queue", type=int, default=20)
    ap.add_argument("--show", type=int, default=40)
    args = ap.parse_args()
    RUN = ROOT / "growth/kits/runs" / args.run
    if args.step == "clusters":
        for c in shortlist(args)[: args.show]:
            print(f"{c['surface']:6} d{c['depth']} {c['cluster']}: {c['queries'][0]['q']} | {', '.join(c['items'])}")
        return
    {"situations": situations, "expand": expand, "label": label, "volume": volume, "depth": depth_step, "supply": supply,
     "fit": fit, "report": report, "harvestfile": harvest_file}[args.step](args)


if __name__ == "__main__":
    main()
