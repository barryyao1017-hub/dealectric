"""Research today's new clusters as their harvest chats land (DLC-208): two pages at a time, until all are done."""
import json, subprocess, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "tools"))
import abpage as A
Q = json.loads((ROOT / "growth/focus/ab-harvest-new-2026-11-08.json").read_text())["questions"]
RUN = "2026-11-08-ab-harvest-new"
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
