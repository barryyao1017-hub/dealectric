"""Claude-coverage gate (gapmine's rule: open when coverage < 0.3) for candidate new pilot pages (DLC-237 new-page arm)."""
import json, sys, time
sys.path.insert(0, "growth/evals")
import serpsources as S, gapmine as G
QS = json.load(open(sys.argv[1]))
out_p = sys.argv[2]
try:
    out = json.load(open(out_p))
except FileNotFoundError:
    out = {}
sup = {}
for q in QS:
    if q in out:
        continue
    res = S.fetch("claude", q)
    if not res:
        print("no results", q); continue
    sup[q] = res[:10]
    time.sleep(3)
lab = {}
G.label_results(sup, lab, list(sup))
for q in sup:
    rs = lab.get(q) or []
    out[q] = {"coverage": G.coverage(rs), "results": [dict(r, **{k: v for k, v in (x or {}).items()}) for r, x in zip(sup[q], rs + [None] * 10)]}
    print(f"{out[q]['coverage']:.3f}  {q}")
json.dump(out, open(out_p, "w"), indent=1)
