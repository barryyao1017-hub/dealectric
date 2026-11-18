#!/usr/bin/env python3.12
"""Feed and apply loop for the j1118 kit set: as each question's two plain chats land, harvest and research it (three
pages at a time, six angle agents each), then add Amazon links and apply it (one page at a time, local commit).
Ends when the harvest log shows the scan has exited and every harvested folder is researched and applied."""
import json, sys, time, traceback
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "growth/focus/offers"))
import kitpages_j1118  # noqa: F401,E402  (points kitpages at this set)
import kitpages as K  # noqa: E402
O, A = K.O, K.A
HLOG = ROOT / "growth/focus/ab/harvest-jkits.log"
Q = list(K._questions())
started, applied, futs = set(), set(), {}
ex = ThreadPoolExecutor(max_workers=3)


def research(slug):
    try:
        r = O.research(slug, False)
    except Exception as e:  # noqa: BLE001
        r = {"slug": slug, "status": "error", "reason": f"{type(e).__name__}: {e}"}
    print("RESEARCH " + json.dumps(r, ensure_ascii=False)[:700], flush=True)
    return r


while True:
    hdone = HLOG.exists() and "HARVEST EXIT" in HLOG.read_text()
    for slug in Q:
        if slug in started:
            continue
        files = K._chat_files(slug)
        if len(files) >= 2 or (hdone and files):
            K.register()
            h = O.harvest(slug)
            print(f"HARVEST {slug}: {len(h['chats'])} chats, searched {h['searched_as'][:2]}", flush=True)
            started.add(slug)
            futs[slug] = ex.submit(research, slug)
    for slug, f in list(futs.items()):
        if f.done() and slug not in applied:
            applied.add(slug)
            try:
                r = O.apply(slug)
            except Exception as e:  # noqa: BLE001
                r = {"folder": slug, "status": "error", "reason": f"{type(e).__name__}: {e}", "trace": traceback.format_exc()[-400:]}
            print("APPLY " + json.dumps(r, ensure_ascii=False)[:900], flush=True)
    if hdone and all(s in started or not K._chat_files(s) for s in Q) and all(f.done() for f in futs.values()) and applied >= started:
        break
    time.sleep(60)
try:
    import research_library
    research_library.build()
except Exception as e:  # noqa: BLE001
    print("library:", e, flush=True)
print("RUN DONE", flush=True)
