"""One-off Webmaster count for a day's newly labelled seeds (2026-11-18): pass 1 spent the day's 300 calls on stale
variants because Bing autocomplete was failing (gapmine UA), so the new clusters had no count. Asks the top variants of
the new seeds' clusters, biggest suggestion surface first, and records the calls in volume.json "wm_calls" like wm_fill.
Hard stop at TOTAL calls for the day (kept under the ~700 where Microsoft's cap stopped us on 11-05).

    python3.12 growth/gapmine/wm_targeted.py <seed>,<seed>... [--total 600] [--per-cluster 3]
"""
import sys, argparse
from datetime import date
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
for p in ("growth/evals", "src", "tools"):
    sys.path.insert(0, str(ROOT / p))
import gapmine as GM
GM.RUN = ROOT / "growth/gapmine/runs/pool"
ap = argparse.ArgumentParser()
ap.add_argument("seeds"); ap.add_argument("--total", type=int, default=600); ap.add_argument("--per-cluster", type=int, default=3)
a = ap.parse_args()
seeds = set(a.seeds.split(","))
out = GM.load("volume.json", {"volumes": {}})
out.setdefault("api_done", []); calls = out.setdefault("wm_calls", {})
day = date.today().isoformat()
done, ms = set(out["api_done"]), out.get("ms", {})
cl = sorted([c for c in GM.clusters() if c.get("seed") in seeds and c["queries"] and not c["covered_by"]], key=lambda c: -c["surface"])
qs = [x["q"] for c in cl for x in c["queries"][: a.per_cluster]]
qs = [q for q in dict.fromkeys(qs) if q not in ms and f"stats|{q}" not in done]
room = max(0, a.total - calls.get(day, 0))
print(f"{len(qs)} variants waiting, room {room}", flush=True)
got = 0
for n, q in enumerate(qs[:room], 1):
    d = GM.bwt("GetKeywordStats", q=q, country="us", language="en-US")
    calls[day] = calls.get(day, 0) + 1
    if d is None:
        print("throttled or failed: stopping", flush=True); break
    if d:
        last = max(GM._ms(r["Date"]) for r in d)
        out["volumes"][q] = sum(int(r.get("Impressions") or 0) for r in d if GM._ms(r["Date"]) > last - 91 * 86400 * 1000)
        got += 1
    out["api_done"].append(f"stats|{q}")
    if n % 50 == 0:
        GM.save("volume.json", out); print(f"{n} asked, {got} with counts", flush=True)
GM.save("volume.json", out)
print(f"DONE asked {min(len(qs), room)}, with counts {got}, calls today {calls.get(day)}", flush=True)
