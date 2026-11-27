#!/usr/bin/env python3.12
"""Proposals and gates (page flow, DLC-369): the lines of a cluster's map become queue items only when they pass every
gate, so the flow never builds a page for the sake of a page. A run in which nothing passes queues nothing.

    python3.12 tools/pageflow/propose.py gate <cluster> [--no-demand]   # gate the map's lines -> growth/pageflow/queue.json
    python3.12 tools/pageflow/propose.py queue                          # what is queued, best first
    python3.12 tools/pageflow/propose.py pick <n> [--cluster <id>]      # the next n by the 70/20/10 split

The gates, in order (the first that fails is recorded with its reason, on the line and in the queue):
  1. real       the line's breakpoint or feature is sourced (a `why` and a source URL), and shoppers ask it (`asked`),
                unless it is marked a hunch;
  2. ours       a product we link is honestly in the line's top three (the map's ours_rank), and it exists: a record that
                can be bought, or a product on an approved program's store;
  3. uncovered  no page of ours answers the line already (the map's covered_by, and a title match against the ledger);
  4. demand     search suggestions complete the question (growth/evals/gapmine.py keystroke depth); a hunch needs
                demand, a sourced line may pass without it at a lower score. Openness, the other half of Barry's
                "opening = demand x (1 - coverage)", is read from ChatGPT's own results in the build's harvest step
                (driver.py keep), before any research is paid for;
  5. value      never fails a line: it orders the queue (brand ticket, cart-tested code, own program against Amazon;
                growth/evals/brandvalue.py).
Score = prior x demand x value x rank, where prior is the ledger's shopper visits a page for this cluster and page type
(shrunk toward the site-wide rate): what worked gets more, what did not gets less.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlparse

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import ledger as L  # noqa: E402

TIER_SHARE = {"proven": 0.7, "adjacent": 0.2, "new": 0.1}
RANK = {1: 1.0, 2: 0.8, 3: 0.6}
STOP = set("the a an for with and or of to in on best top which what is are that can under over my your i buy should 2026 2027".split())


def _tokens(s: str) -> set:
    return {t for t in re.findall(r"[a-z0-9.]+", s.lower().replace("-", " ")) if t not in STOP}


def similar(a: str, b: str) -> float:
    x, y = _tokens(a), _tokens(b)
    return len(x & y) / len(x | y) if x and y else 0.0


def _host(u: str) -> str:
    return re.sub(r"^www\.", "", urlparse(u).netloc.lower())


def ours_exist(line: dict, cid: str) -> tuple[bool, str]:
    import gappage
    recs = {p["slug"]: p for p in C.records()}
    stores = {_host(v.split("store ")[-1]) for v in gappage.programs().values() if "store " in v}   # any approved program's store
    good = []
    for o in line.get("ours") or []:
        if o in recs:
            if recs[o].get("in_stock") is not False:
                good.append(o)
        elif o.startswith("http") and (_host(o) in stores or "amazon.com" in o):
            good.append(o)
    if not good:
        return False, "the products named as ours are sold out, unknown, or not on an approved program's store"
    return True, ", ".join(good)[:200]


def demand(question: str) -> tuple[float, dict]:
    import gapmine
    q0 = re.sub(r"\s+", " ", question.lower().replace("-", " ").replace("?", "")).strip()   # suggestions write "usb c", not "usb-c"
    variants = [q0] + ([question.lower()] if question.lower() != q0 else [])
    if not q0.startswith("best "):
        variants.append("best " + q0)
    best, seen = 0.0, {}
    for q in variants:
        d = gapmine.depth(q)
        v = gapmine.demand_from_depth(d)
        seen[q] = d
        best = max(best, v)
    return best, seen


def value(line: dict, cid: str) -> float:
    import brandvalue as V
    recs = {p["slug"]: p for p in C.records()}
    names = [recs[o]["brand"] for o in line.get("ours") or [] if o in recs] or [(line.get("product") or {}).get("brand") or ""]
    f = max((V.factor(V.brand(n)) for n in names if n), default=V.factor(None))
    return round(min(max(f / 300.0, 0.3), 3.0), 2)   # 1.0 = a $300 ticket with no code; clipped so value orders, never decides alone


def gate_line(line: dict, cid: str, led: dict, with_demand: bool = True) -> dict:
    g = {"date": C.today()}
    srcs = [s for s in line.get("sources") or [] if str(s).startswith("http")]
    if not line.get("why") or not srcs:
        return dict(g, passed=False, failed="real", reason="no sourced breakpoint or feature")
    if not line.get("hunch") and not line.get("asked"):
        return dict(g, passed=False, failed="real", reason="no evidence shoppers ask it, and not marked a hunch")
    if line["ptype"] not in C.PTYPES:
        return dict(g, passed=False, failed="real", reason=f"page type {line['ptype']!r} is not one the flow builds")
    if not 1 <= int(line.get("ours_rank") or 0) <= 3:
        return dict(g, passed=False, failed="ours", reason="none of the products we link is in the top three")
    ok, what = ours_exist(line, cid)
    if not ok:
        return dict(g, passed=False, failed="ours", reason=what)
    if line.get("covered_by"):
        return dict(g, passed=False, failed="uncovered", reason="covered by /" + line["covered_by"])
    if line["ptype"] != "product":
        for slug, p in led["pages"].items():
            if p["cluster"] == cid and p["kind"] != "product" and max(similar(line["question"], p["title"]), similar(line["question"], slug)) >= 0.85:   # a backstop for exact repeats only: one more word ("wireless") is another line
                return dict(g, passed=False, failed="uncovered", reason="covered by /" + slug + " (title match)")
    dem, seen = (demand(line["question"]) if with_demand and line["ptype"] != "product" else (None, {}))
    if line.get("hunch") and dem is not None and dem <= 0:
        return dict(g, passed=False, failed="demand", reason="a hunch, and no search suggestion completes the question", depth=seen)
    val = value(line, cid)
    pri = L.prior(led, cid, line["ptype"])
    dfac = 1.0 if dem is None else 0.5 + dem      # 0.5 (never suggested) to 1.5
    score = round(max(pri, 0.1) * dfac * val * RANK[int(line["ours_rank"])] * (0.7 if line.get("hunch") else 1.0), 3)
    return dict(g, passed=True, ours=what, demand=dem, depth=seen, value=val, prior=pri, score=score)


def gate(cid: str, with_demand: bool = True) -> list[dict]:
    m = C.jload(C.MAPS / f"{cid}.json")
    if not m:
        raise SystemExit(f"no map for {cid}: run maps.py build {cid}")
    led = C.jload(C.LEDGER) or L.build()
    q = C.jload(C.QUEUE) or {"items": []}
    items = {i["id"]: i for i in q["items"]}
    out = []
    for line in m["lines"]:
        iid = f"{cid}:{line['id']}"
        if line.get("status") in ("built", "retired") or items.get(iid, {}).get("status") in ("building", "built"):
            continue
        g = gate_line(line, cid, led, with_demand)
        line["gate"] = {k: v for k, v in g.items() if k != "depth"}
        item = {"id": iid, "cluster": cid, "line": line["id"], "ptype": line["ptype"], "question": line["question"], "hunch": bool(line.get("hunch")),
                "status": "queued" if g["passed"] else "failed:" + g["failed"], "reason": g.get("reason", ""), "score": g.get("score", 0),
                "gate": g, "map_built": m["built"], "added": items.get(iid, {}).get("added", C.today())}
        if items.get(iid, {}).get("status", "").startswith("skipped"):   # the harvest or the research said no: keep that verdict until the map changes the line
            item["status"], item["reason"] = items[iid]["status"], items[iid].get("reason", "")
        items[iid] = item
        out.append(item)
    C.jsave(C.MAPS / f"{cid}.json", m)
    q["items"] = sorted(items.values(), key=lambda i: -i.get("score", 0))
    q["updated"] = C.today()
    C.jsave(C.QUEUE, q)
    return out


def pick(n: int, cluster: str | None = None) -> list[dict]:
    """The next n queued lines. Across clusters the build budget is split 70/20/10 between proven, adjacent and new
    clusters (best score first inside each); whatever a tier leaves unused goes to the best of the rest."""
    q = (C.jload(C.QUEUE) or {"items": []})["items"]
    queued = [i for i in q if i["status"] == "queued" and (cluster is None or i["cluster"] == cluster)]
    if cluster:
        return queued[:n]
    tiers = {cid: c.get("tier", "new") for cid, c in C.clusters().items()}
    out = []
    for tier, share in TIER_SHARE.items():
        out += [i for i in queued if tiers.get(i["cluster"]) == tier][:max(1, round(n * share)) if n >= 3 else n]
    out = sorted(out, key=lambda i: -i["score"])[:n]
    for i in queued:
        if len(out) >= n:
            break
        if i not in out:
            out.append(i)
    return out


def set_status(iid: str, status: str, **extra) -> None:
    q = C.jload(C.QUEUE) or {"items": []}
    for i in q["items"]:
        if i["id"] == iid:
            i.update(status=status, **extra)
    C.jsave(C.QUEUE, q)
    cid, _, lid = iid.partition(":")
    m = C.jload(C.MAPS / f"{cid}.json")
    if m:
        for l in m["lines"]:
            if l["id"] == lid:
                l["status"] = status
                l.update({k: v for k, v in extra.items() if k in ("page", "run", "reason")})
        C.jsave(C.MAPS / f"{cid}.json", m)


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "queue"
    if cmd == "gate":
        items = gate(sys.argv[2], "--no-demand" not in sys.argv)
        for i in sorted(items, key=lambda i: -i["score"]):
            print(f"{i['status']:18s} {i['score']:6.2f} | {i['ptype']:8s} | {i['question']}" + (f"  [{i['reason']}]" if i["reason"] else ""))
        print(f"{sum(1 for i in items if i['status'] == 'queued')} of {len(items)} lines queued")
    elif cmd == "queue":
        for i in (C.jload(C.QUEUE) or {"items": []})["items"]:
            print(f"{i['status']:18s} {i['score']:6.2f} | {i['cluster']:16s} | {i['ptype']:8s} | {i['question']}")
    elif cmd == "pick":
        cl = sys.argv[sys.argv.index("--cluster") + 1] if "--cluster" in sys.argv else None
        for i in pick(int(sys.argv[2]), cl):
            print(f"{i['score']:6.2f} | {i['id']} | {i['question']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
