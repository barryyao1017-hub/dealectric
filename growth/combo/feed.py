"""Combo run: research each harvested question (shape -> single / kit / bundle research), N pages at a time.
BATCH env names growth/combo/batch-<BATCH>.json ({"questions": [{qid, slug, prompt}]}); harvest run id 2026-11-13-combo-<BATCH>."""
import json, os, sys, time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
import abpage as A
import combopage as C
BATCH = os.environ["BATCH"]
Q = json.loads((ROOT / f"growth/combo/batch-{BATCH}.json").read_text())["questions"]
RUN = f"2026-11-13-combo-{BATCH}"
SKIP = set((ROOT / "growth/combo/skip.txt").read_text().split()) if (ROOT / "growth/combo/skip.txt").exists() else set()
Q = [q for q in Q if q["slug"] not in SKIP]
ex = ThreadPoolExecutor(max_workers=int(os.environ.get("PAGES", "3")))
started, futs = set(), {}
def run(slug):
    try:
        r = C.research(slug)
    except Exception as e:  # noqa: BLE001
        r = {"slug": slug, "status": "error", "reason": repr(e)[:300]}
    print(json.dumps({k: v for k, v in r.items() if k != "_meta"}, ensure_ascii=False)[:500], flush=True)
    return r
while True:
    for q in Q:
        s = q["slug"]
        if s in started:
            continue
        if q.get("reused_harvest"):   # a retried cluster: its harvest.json was copied from the earlier folder
            started.add(s)
            futs[s] = ex.submit(run, s)
            continue
        n = len(list((ROOT / "growth/evals/runs" / RUN / "chatgpt").glob(f"{q['qid']}-*.json")))
        if n >= int(os.environ.get("MINCHATS", "2")) or (n >= 1 and (ROOT / f"growth/combo/harvest-{BATCH}.done").exists()):
            A.harvest(s, [RUN])
            started.add(s)
            futs[s] = ex.submit(run, s)
    if len(started) == len(Q) and all(f.done() for f in futs.values()):
        break
    if (ROOT / f"growth/combo/harvest-{BATCH}.done").exists() and all(f.done() for f in futs.values()) and \
            all(s["slug"] in started or not list((ROOT / "growth/evals/runs" / RUN / "chatgpt").glob(f"{s['qid']}-*.json")) for s in Q):
        break   # harvest over; the questions with no chat stay unbuilt
    time.sleep(60)
print("FEED DONE", flush=True)
