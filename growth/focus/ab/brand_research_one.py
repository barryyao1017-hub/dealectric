"""Research one brand item with gappage brand mode (Opus 5.5) without touching queue.json (discovery may be writing it).
Writes the item to growth/focus/ab/brand-item-<key>.json and the draft to growth/gapmine/drafts/. Usage: <program> <date>"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
for p in ("tools", "src", "growth/evals"): sys.path.insert(0, str(ROOT / p))
import gappage as G
prog, day = sys.argv[1], sys.argv[2]
net, key = prog.split(":")
v = json.loads((ROOT / "src/links.json").read_text())[net][key]
item = {"kind": "brand", "brand": v["name"], "program": prog, "store": v["home"], "network_codes": [], "cluster": f"brand:{key}",
        "lead": "", "supply_query": "", "searches": "n/a", "coverage": None, "uncovered": 0, "brands": [key], "variants": [],
        "queued": day, "status": "new"}
d = G.research(item)
k = G.draft_key(d, item)
G.DRAFTS.mkdir(parents=True, exist_ok=True)
(G.DRAFTS / f"{k}.json").write_text(json.dumps({**d, "item": item}, indent=1))
item.update({"status": "drafted" if d.get("status") in ("ok", "products_only") else d.get("status", "failed"), "draft": k, "tried": day,
             "result": d.get("reason") or d.get("status")})
(ROOT / f"growth/focus/ab/brand-item-{key}.json").write_text(json.dumps(item, indent=1))
print(item["brand"], d.get("status"), k, d.get("query"), str(d.get("reason") or "")[:200], flush=True)
