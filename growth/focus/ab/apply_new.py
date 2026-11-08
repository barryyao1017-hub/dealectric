"""Apply today's new-page drafts one at a time as they land (DLC-208); commits locally, no push."""
import json, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import abpage as A
Q = [q["slug"] for q in json.loads((ROOT / "growth/focus/ab-harvest-new-2026-11-08.json").read_text())["questions"]]
tried = {}
while True:
    pending = 0
    skip = set((ROOT / "growth/focus/ab/skip.txt").read_text().split()) if (ROOT / "growth/focus/ab/skip.txt").exists() else set()
    for s in Q:
        if s in skip:
            continue
        d = A.jload(A.AB / s / "draft.json")
        if not d:
            pending += 1
            continue
        g = d.get("gate") or {}
        if g.get("pass") or g.get("skipped"):
            continue
        mt = (A.AB / s / "draft.json").stat().st_mtime
        if tried.get(s) == mt:
            continue
        r = A.apply(s, local=True)
        tried[s] = (A.AB / s / "draft.json").stat().st_mtime
        print("APPLY " + json.dumps(r, ensure_ascii=False)[:600], flush=True)
    feed = (ROOT / "growth/focus/ab/feed-new.log").read_text() if (ROOT / "growth/focus/ab/feed-new.log").exists() else ""
    if pending == 0 and "FEED DONE" in feed:
        break
    time.sleep(90)
print("APPLY DONE", flush=True)
