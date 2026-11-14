"""Combo run: apply each drafted page as it lands, one at a time, committing locally (no push)."""
import json, os, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import abpage as A
import combopage as C
BATCHES = os.environ["BATCH"].split(",")
Q = [q["slug"] for b in BATCHES for q in json.loads((ROOT / f"growth/combo/batch-{b}.json").read_text())["questions"]]
tried = {}
while True:
    pending = 0
    skip = set((ROOT / "growth/combo/skip.txt").read_text().split()) if (ROOT / "growth/combo/skip.txt").exists() else set()
    for s in Q:
        if s in skip:
            continue
        p = A.AB / s / "draft.json"
        d = A.jload(p)
        if not d:
            pending += 1
            continue
        g = d.get("gate") or {}
        if g.get("pass") or g.get("skipped"):
            continue
        if tried.get(s) == p.stat().st_mtime:
            continue
        try:
            r = C.apply(s)
        except Exception as e:  # noqa: BLE001
            r = {"slug": s, "status": "error", "reason": repr(e)[:300]}
        if "uncommitted" in str(r.get("reason", "")):
            continue
        tried[s] = p.stat().st_mtime if p.exists() else 0
        print("APPLY " + json.dumps(r, ensure_ascii=False)[:600], flush=True)
    logs = [ROOT / f"growth/combo/feed-{b}.log" for b in BATCHES]
    if pending == 0 and all(l.exists() and "FEED DONE" in l.read_text() for l in logs):
        break
    if all(l.exists() and "FEED DONE" in l.read_text() for l in logs):
        break   # research over; folders with no draft were skipped or failed in research
    time.sleep(90)
print("APPLY DONE", flush=True)
