"""After a day's new pages are applied: mark each status-new queue cluster published (with its slug) or skip."""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
day = sys.argv[1]
Q = json.loads((ROOT / f"growth/focus/ab-harvest-new-{day}.json").read_text())["questions"]
queue = json.loads((ROOT / "growth/gapmine/queue.json").read_text())
res = {}
for q in Q:
    p = ROOT / "growth/focus/ab" / q["slug"] / "draft.json"
    d = json.loads(p.read_text()) if p.exists() else {}
    g = d.get("gate") or {}
    res[q["cluster"]] = ("published", d.get("slug")) if g.get("pass") else ("skip", d.get("reason") or "; ".join(g.get("errors") or [])[:200] or "no draft")
n = 0
for x in queue:
    if x.get("status") == "new" and x.get("cluster") in res:
        st, v = res[x["cluster"]]
        x["status"], x["tried"] = st, day
        if st == "published":
            x["slug"], x["result"] = v, "research method ab-2026-11 (tools/abpage.py)"
        else:
            x["result"] = v
        n += 1
(ROOT / "growth/gapmine/queue.json").write_text(json.dumps(queue, indent=1) + "\n")
print(n, "rows marked:", {k: v[0] for k, v in res.items()})
