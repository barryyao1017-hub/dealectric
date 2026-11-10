"""Research today's new clusters as their harvest chats land (DLC-208): two pages at a time, until all are done."""
import json, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import abpage as A
import os
DAY = os.environ.get("DAY", "2026-11-08")
Q = json.loads((ROOT / f"growth/focus/ab-harvest-new-{DAY}.json").read_text())["questions"]
RUN = f"{DAY}-ab-harvest-new"
SKIP = set((ROOT / "growth/focus/ab/skip.txt").read_text().split()) if (ROOT / "growth/focus/ab/skip.txt").exists() else set()
Q = [q for q in Q if q["slug"] not in SKIP]
started = set()
ex = ThreadPoolExecutor(max_workers=2)
futs = {}
def run(slug):
    r = A.research(slug, new_page=True)
    print(json.dumps(r, ensure_ascii=False), flush=True)
    return r
while True:
    for q in Q:
        s = q["slug"]
        if s in started:
            continue
        if any((ROOT / "growth/evals/runs" / RUN / "chatgpt").glob(f"{q['qid']}-*.json")):
            A.harvest(s, [RUN])
            started.add(s)
            futs[s] = ex.submit(run, s)
            print(f"queued research {s}", flush=True)
    if len(started) == len(Q) and all(f.done() for f in futs.values()):
        break
    time.sleep(120)
print("FEED DONE", flush=True)
