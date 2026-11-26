"""Score the demand-shortlist run (2026-11-15-shortlist, panelprobe.py): per question, what ChatGPT's answer gives the
catalog and what it leaves to web pages.
  catalog reach = product rows with an inline card + typed product names whose panel offers a seller ("Visit"),
                  out of rows with a card plus typed names that were clicked.
  strict open   = searched, named products, catalog reach <= half, primary sources <= a third of citations.
"""
import json, sys, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
sys.path.insert(0, str(HERE)); sys.path.insert(0, str(ROOT / "growth" / "evals"))
from domains import classify
import openscan as O, visibility_scan as VS
# usage: shortlist_score.py [run id] [queue file] [output name] [--quiet]
ARGS = [a for a in sys.argv[1:] if not a.startswith("--")]
RUN = ROOT / "growth/evals/runs" / (ARGS[0] if ARGS else "2026-11-15-shortlist")
QF = Path(ARGS[1]) if len(ARGS) > 1 else HERE / "shortlist-queue.jsonl"
OUTN = ARGS[2] if len(ARGS) > 2 else "shortlist-results.json"
q = {json.loads(l)["qid"]: json.loads(l) for l in QF.read_text().splitlines() if l.strip()}
out = []
for l in (RUN / "panels.jsonl").read_text().splitlines():
    p = json.loads(l)
    if not (RUN / f"{p['qid']}.json").exists():
        continue
    rec = json.loads((RUN / f"{p['qid']}.json").read_text())
    rd = O.reading(rec); s = VS.score(rec, {"code": None})
    clicked = [x for x in p["panels"] if x.get("found")]
    offers = [x for x in clicked if x.get("visit")]
    free = [x["name"] for x in clicked if not x.get("visit")]
    denom = rd["carded"] + len(clicked)
    reach = (rd["carded"] + len(offers)) / denom if denom else None
    cited = [d for d in rd["cited"] if classify(d) != "ours"]
    prim = sum(classify(d) in ("maker", "official", "publisher") for d in cited) / len(cited) if cited else 0.0
    rows = rd["carded"] + rd["typed"]
    if not rd["searched"]: v = "no search"
    elif rows == 0: v = "no products named"
    elif reach is not None and reach <= 0.5 and prim <= 1 / 3: v = "open"
    elif (reach is None or reach <= 0.5) or prim <= 1 / 3: v = "partly"
    else: v = "closed"
    qq = q.get(p["qid"], {})
    out.append({"qid": p["qid"], "prompt": p["prompt"], "cluster": qq.get("demand_cluster"), "demand": qq.get("demand"), "source": qq.get("source"),
                "searched": rd["searched"], "carded": rd["carded"], "typed": rd["typed"], "clicked": len(clicked), "offers": len(offers),
                "sellers": sorted({s2 for x in offers for s2 in x.get("sellers") or []}), "free": free, "offer_names": [x["name"] for x in offers],
                "reach": reach, "prim": prim, "cited": cited, "cited_cls": [classify(d) for d in cited], "verdict": v, "our_rank": s["our_rank"], "tier": s["tier"],
                "queries": rd["queries"]})
(HERE / "report" / OUTN).write_text(json.dumps(out, indent=1))
c = collections.Counter(x["verdict"] for x in out)
print(len(out), dict(c))
tot_typed = sum(x["clicked"] for x in out); tot_off = sum(x["offers"] for x in out); tot_card = sum(x["carded"] for x in out)
print("rows with inline card", tot_card, "| typed names clicked", tot_typed, "| of those with a seller in the panel", tot_off)
for x in [] if "--quiet" in sys.argv else sorted(out, key=lambda x: ({"open": 0, "partly": 1, "closed": 2, "no products named": 3, "no search": 4}[x["verdict"]], -(x["demand"] or 0))):
    print(f"{x['verdict'][:8]:8} d={x['demand'] or 0:6} card={x['carded']} typed={x['typed']} offer={x['offers']}/{x['clicked']} prim={x['prim']:.2f} rank={x['our_rank']} T{x['tier']} | {x['prompt'][:60]:60} | free={x['free'][:3]} | {','.join(f'{d}:{k[:3]}' for d,k in zip(x['cited'],x['cited_cls']))[:70]}")
free = collections.Counter(n for x in out for n in x["free"]); off = collections.Counter(n for x in out for n in x["offer_names"])
print("FREE (no seller in panel):", free.most_common(40))
print("WITH SELLER:", off.most_common(25))
