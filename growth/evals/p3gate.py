#!/usr/bin/env python3.12
"""Phase 3 freshness gate: ask ChatGPT what revision the CPAP comparison page shows, every --every minutes, until the
answer carries --rev (src/compare.py COMPARE_REV) or --tries run out. Each answer is saved under <run>/gate/.
ChatGPT fetches a page given in the prompt once (ChatGPT-User) and answers later chats from that copy, so a copy
change counts only after this gate passes.   python3.12 growth/evals/p3gate.py --run-id 2026-10-24-p3iter01 --rev r1"""
import argparse, sys, time
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import ui  # noqa: E402

ap = argparse.ArgumentParser()
ap.add_argument("--run-id", required=True); ap.add_argument("--rev", required=True)
ap.add_argument("--every", type=float, default=30); ap.add_argument("--tries", type=int, default=8)
a = ap.parse_args()
P = "I'm reading https://dealectric.com/power-station-for-cpap — what revision does the page show right under its heading? Quote it exactly."
gd = E.run_dir(a.run_id) / "gate"; gd.mkdir(parents=True, exist_ok=True)
for i in range(1, a.tries + 1):
    n = len(list(gd.glob("gate-*.json"))) + 1
    try:
        r = ui.ask_chatgpt(P, None)
    except Exception as e:  # noqa: BLE001
        r = {"text": "", "error": str(e)}
    E.write_json(gd / f"gate-{n}.json", dict(r, prompt=P, at=E.now_iso()))
    ok = a.rev.lower() in (r.get("text") or "").lower()
    print(f"{E.now_iso()} gate-{n}: {'FRESH' if ok else 'stale'} :: {(r.get('text') or r.get('error') or '')[:160]!r}", flush=True)
    if ok:
        sys.exit(0)
    if i < a.tries:
        time.sleep(a.every * 60)
sys.exit(1)
