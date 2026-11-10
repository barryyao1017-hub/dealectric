"""Brand onboarding with the research method (Barry 11-10): commit each brand draft's products only (gappage gate),
take the Claude coverage reading for the brand's chosen query, and list the open ones (< gate) for a research-method
page (abpage harvest -> research -> apply). Usage: python3.12 growth/focus/ab/brand_apply.py <queued-date>"""
import copy, json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools")); sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "growth/evals"))
import gappage as G
day = sys.argv[1]
out = []
for item in [x for x in G.load_queue() if x.get("kind") == "brand" and x.get("queued") == day and x["status"] == "drafted"]:
    d = json.loads((G.DRAFTS / f"{item['draft']}.json").read_text()); d.pop("item", None)
    q, cov = d.get("query"), None
    if d.get("status") == "ok" and q:
        probe, it = copy.deepcopy(d), copy.deepcopy(item)
        G.prepare_brand(probe, it)            # coverage reading; probe flips to products_only when the query isn't open
        cov = it.get("coverage")
        item.update({k: it[k] for k in ("lead", "supply_query", "variants", "source", "coverage") if k in it})
    open_q = bool(q) and cov is not None and cov < __import__("gapmine").gate_for("claude")
    d["status"] = "products_only"
    for k in ("slug", "must", "page"):
        d.pop(k, None)
    r = G.run_one(item, "local", d)
    g = r.get("gate") or {}
    item["status"] = "committed" if r.get("published") == "committed" else ("failed" if not g.get("pass") else "ready")
    item["result"] = r.get("published") or g.get("errors") or r.get("reason")
    q2 = G.load_queue()
    for i, y in enumerate(q2):
        if y.get("kind") == "brand" and y.get("cluster") == item["cluster"]:
            q2[i] = item
    G.save_queue(q2)
    if item["status"] == "committed":
        G.sh("git", "add", str(G.QUEUE)); G.sh("git", "commit", "-q", "-m", f"queue: {item['brand']} products committed\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
    row = {"brand": item["brand"], "program": item["program"], "status": item["status"], "query": q, "coverage": cov,
           "page": open_q, "products": [p["slug"] for p in d.get("products") or []], "codes": [c.get("code") for c in d.get("codes") or []],
           "result": str(item["result"])[:300]}
    out.append(row); print(json.dumps(row, ensure_ascii=False), flush=True)
(ROOT / f"growth/focus/ab/brands-{day}.json").write_text(json.dumps(out, indent=1, ensure_ascii=False))
print("BRAND APPLY DONE", flush=True)
