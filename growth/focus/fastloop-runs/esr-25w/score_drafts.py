#!/usr/bin/env python3.12
"""ESR run, step 6: score drafts A, B, C on the open-page replay, gpt-6 only, 1 answer per result set over the 18 sets
of TARGETS["esr-25w"] at rank 5 (iterate.py's engine and cache, so a quota stop resumes where it left off). Exit 75 on
a stall. Writes scores.json next to this file."""
import importlib.util, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[3]
sys.path[:0] = [str(REPO / "growth" / "evals"), str(REPO / "src")]
import iterate as I  # noqa: E402

spec = importlib.util.spec_from_file_location("drafts", HERE / "drafts.py")
D = importlib.util.module_from_spec(spec); spec.loader.exec_module(D)

tgt = I.TARGETS["esr-25w"]
out = HERE / "scoring"
out.mkdir(exist_ok=True)
eng = I.Engine("open", "gpt-6.1-sol", "c1", "v1", models=["gpt-6"], max_wait_min=60, heartbeat=out / "heartbeat.json")
KEYS = sys.argv[1] if len(sys.argv) > 1 else "ABC"   # D, E come from draft2 (the single-pad pick)
drafts = {k: (I.render(D.draft(k) if k in "ABC" else D.draft2(k)), out / f"{k}.jsonl") for k in KEYS}
try:
    sc = I.score_round(drafts, tgt, eng, 1)
except I.Stall as e:
    print(f"stall: {e}", flush=True)
    sys.exit(75)
I.E.write_json(HERE / f"scores-{KEYS}.json", sc)
for k, s in sc.items():
    print(f"{k}: answers {s['answers']}, linked {s['linked']}, M1 {s['m1']:.0%} ({s['m1_hits']}/{s['linked']}), "
          f"M2 {s['m2']:.0%}, M3 {s['m3']:.0%}")
