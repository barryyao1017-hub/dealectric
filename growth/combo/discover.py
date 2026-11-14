"""Combo run 2026-11-13 (Barry): broader discovery for an ad hoc batch of 50+ pages, apart from the daily flow.

Candidates are real autocomplete clusters already in the gap pool (growth/gapmine/runs/pool) that never got a coverage
reading because Bing Webmaster has no count for them (Ad Insight blocked, DLC-178). Here demand is the cluster's
suggestion surface instead of a search count, weighted by the brand value factor (brandvalue.py); clusters whose best
brand sells under $150 are left out. Nothing here edits the daily queue or the pool's volume rules.

    python3.12 growth/combo/discover.py rank [--top 150]     -> growth/combo/candidates.json (solar first)
    python3.12 growth/combo/discover.py cover [--max 150]    Claude coverage reading per candidate (one-off cap override)
    python3.12 growth/combo/discover.py pick                 -> growth/combo/picked.json (coverage < 0.3), value order
"""
import json, os, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
for p in ("growth/evals", "src", "tools"):
    sys.path.insert(0, str(ROOT / p))
import gapmine as GM
import brandvalue as BV
GM.RUN = ROOT / "growth/gapmine/runs/pool"
OUT = ROOT / "growth/combo"
SOLAR = {"allpowers", "bluetti", "ankersolix", "naturesgenerator", "growatt", "sungoldpower", "vatrer", "redodo", "zendure",
         "ecoflow", "jackery", "goalzero", "anker"}
SOLAR_WORDS = re.compile(r"solar|power station|generator|lifepo4|lithium batter|battery backup|inverter|off.?grid|kwh|outage|"
                         r"home backup|rv batter|golf cart batter|trolling|sump pump|cpap", re.I)
NAMED = re.compile(r"\b(vs|versus|review|reviews|manual|app|login|warranty|coupon|discount code|promo|uk|philippines|pakistan|india|"
                   r"australia|canada|nz|ireland|south africa|nigeria|kenya|caravan|near me|hat|reddit|amazon|walmart|costco|"
                   r"harbor freight|home depot|lowes|ebay|diy|how to|what is|meaning|worth it|brands)\b", re.I)


def rank(top: int) -> list[dict]:
    vol, dep = GM.vols(), GM.load("depth.json", {})
    lab = GM.load("supply_labels.json", {})
    queue = json.loads((ROOT / "growth/gapmine/queue.json").read_text())
    queued = {x.get("cluster") for x in queue}
    labels = GM.load("labels.json", {})
    named = {q for seed in labels.values() for q, v in seed.items() if isinstance(v, dict) and v.get("named")}
    rows = []
    for c in GM.clusters():
        if not c["queries"] or c["covered_by"] or c["cluster"] in queued:
            continue
        lead = GM.lead_of(c, dep, vol)
        sq = GM.supply_query(lead)
        if sq in lab or lead in named or NAMED.search(lead) or len(lead.split()) < 2:
            continue
        s = BV.score({"brands": c.get("brands") or [], "uncovered": 1})
        if s["park"]:
            continue
        f = s["value"]   # uncovered=1 -> the brand factor itself
        solar = bool(SOLAR_WORDS.search(c["cluster"]) or SOLAR_WORDS.search(lead)) and bool(set(c.get("brands") or []) & SOLAR or SOLAR_WORDS.search(lead))
        rows.append({"cluster": c["cluster"], "seed": c["seed"], "lead": lead, "supply_query": sq, "brands": c.get("brands") or [],
                     "surface": round(c.get("surface") or 0, 2), "searches": sum(vol.get(x["q"], 0) for x in c["queries"]),
                     "factor": f, "ticket": s["ticket"], "code": s["code"], "solar": solar,
                     "score": round((c.get("surface") or 0) * f), "variants": [x["q"] for x in c["queries"][:6]]})
    rows.sort(key=lambda r: -r["score"])
    LOW = re.compile(r"earbud|headphone|earphone|cable|cord|charger|phone case|keycap|mouse|power bank|adapter|flashlight|headlamp|"
                     r"smart plug|power strip|speaker|keyboard|webcam|hub|dongle|screen protector|battery box", re.I)   # sub-$150 products
    per_seed, keep = {}, []
    for r in rows:   # diversity: near-duplicate clusters of one seed would become near-duplicate pages
        cap = 5 if r["solar"] else 3
        if (not r["solar"] and LOW.search(r["lead"])) or per_seed.get(r["seed"], 0) >= cap:
            continue
        per_seed[r["seed"]] = per_seed.get(r["seed"], 0) + 1
        keep.append(r)
    rows = keep
    sol = [r for r in rows if r["solar"]][: top // 2]
    oth = [r for r in rows if not r["solar"]][: top - len(sol)]
    out = sol + oth
    (OUT / "candidates.json").write_text(json.dumps(out, indent=1))
    return out


def cover(mx: int) -> None:
    import threading
    import concurrent.futures as cf
    import serpsources as S
    S.SOURCES["claude"]["daily"] = int(os.environ.get("COMBO_CLAUDE_CAP", "220"))   # one-off for this run; the daily cap is untouched
    cands = json.loads((OUT / "candidates.json").read_text())
    sup, lab, src = GM.load("supply.json", {}), GM.load("supply_labels.json", {}), GM.load("supply_source.json", {})
    todo = [r["supply_query"] for r in cands if not lab.get(r["supply_query"]) and len(sup.get(r["supply_query"]) or []) < GM.MIN_RESULTS][:mx]
    lock, n = threading.Lock(), [0]
    def one(sq):
        res = S.fetch("claude", sq)
        with lock:
            n[0] += 1
            if res:
                sup[sq], src[sq] = res, "claude"
                GM.save("supply.json", sup); GM.save("supply_source.json", src)
            if n[0] % 10 == 0:
                print(f"read {n[0]}/{len(todo)}", flush=True)
    with cf.ThreadPoolExecutor(max_workers=4) as ex:
        list(ex.map(one, todo))
    GM.label_results(sup, lab, [q for q in src if q not in lab and len(sup.get(q) or []) >= GM.MIN_RESULTS], "supply_labels.json")
    print("COVER DONE", n[0], flush=True)


def pick() -> list[dict]:
    lab = GM.load("supply_labels.json", {})
    out = []
    for r in json.loads((OUT / "candidates.json").read_text()):
        l = lab.get(r["supply_query"])
        if not l:
            continue
        cov = GM.coverage(l)
        r["coverage"] = cov
        if cov is not None and cov < GM.gate_for("claude"):
            out.append(r)
    out.sort(key=lambda r: (-r["solar"], -r["score"] * (1 - r["coverage"])))
    (OUT / "picked.json").write_text(json.dumps(out, indent=1))
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    n = int(sys.argv[sys.argv.index("--top") + 1]) if "--top" in sys.argv else int(sys.argv[sys.argv.index("--max") + 1]) if "--max" in sys.argv else 150
    if cmd == "rank":
        rows = rank(n)
        for r in rows:
            print(f"{'S' if r['solar'] else ' '} {r['score']:>7} surf {r['surface']:>6} x{r['factor']:>6.0f} | {r['lead'][:52]:52} | {','.join(r['brands'])[:30]}")
    elif cmd == "cover":
        cover(n)
    elif cmd == "pick":
        for r in pick():
            print(f"{'S' if r['solar'] else ' '} cov {r['coverage']:<5} {r['score']:>7} | {r['lead'][:55]:55} | {','.join(r['brands'])[:28]}")
