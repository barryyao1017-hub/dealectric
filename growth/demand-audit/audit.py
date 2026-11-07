"""Demand audit (2026-11-07): Bing volume of each query group x where we sit in OpenAI's own index for the
ChatGPT-style rewrite. Usage: python3.12 growth/demand-audit/audit.py <run-dir>"""
import json, sys, pathlib
sys.path.insert(0, "growth/evals")
import serpsources as S

run = pathlib.Path(sys.argv[1])
vol = json.load(open("growth/gapmine/runs/2026-11-05/volume.json"))
V = {k: c for k, c in vol["volumes"].items() if c}
for k, c in vol["ms"].items():
    if c:
        V.setdefault(k, c)
out_f = run / "readings.json"
out = json.load(open(out_f)) if out_f.exists() else {}
for cluster, q, group in json.load(open(run / "queries.json")):
    if q not in out:
        res = S.fetch("openai", q)
        if res is None:
            print("no reading", q); continue
        out[q] = {"cluster": cluster, "results": res}
    out[q]["volume"] = sum(V.get(g, 0) for g in group)
    out[q]["group"] = group
    ours = [r for r in out[q]["results"] if "dealectric.com" in r["url"]]
    out[q]["ours"] = [(r["rank"], r["url"].split("dealectric.com")[-1]) for r in ours]
    json.dump(out, open(out_f, "w"), indent=1)
    print(f'{out[q]["volume"]:6} {str(out[q]["ours"]):60} {q}')
