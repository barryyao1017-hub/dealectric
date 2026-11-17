#!/usr/bin/env python3.12
"""Turn a refresh pass's research files (growth/bfcm/research-<MMDD>-*.json, brief research-brief-1117.md) into
growth/bfcm/curated-refresh-<date>.json, which growth/bfcm/curated.py layers over its hand-curated entries (DLC-221).

    python3.12 growth/bfcm/refresh.py 2026-11-17     # then python3.12 growth/bfcm/curated.py

Per brand: the pass's phases replace the old ones (undated phases get "seen" = the pass date, "announced" when the
brand only announced them); last_year, store, sells, new and network_codes carry over from the current entry unless
the pass found a last_year; a brand the pass could not read keeps its old entry and date. HEADLINE / NAME / DROP below
are the hand edits: the brand's own words, shortened.
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DATE = sys.argv[1] if len(sys.argv) > 1 else "2026-11-17"
MMDD = DATE[5:7] + DATE[8:10]
ALIAS = {"Nitecore": "NITECORE Store", "Autel Robotics": "Autelpilot", "NUU": "NUU Mobile"}

HEADLINE = {}     # (brand, phase name) -> shortened headline
NAME = {}         # (brand, phase name) -> phase name to show
DROP = set()      # (brand, phase name) -> leave out (not a Black Friday sale, or not checkable)
UNREAD = set()    # brands the pass couldn't read and that have no earlier entry
EXTRA = {}        # brand -> phases to add (e.g. a Cyber Monday phase the research gave under cyber_monday)
EDITS = ROOT / f"growth/bfcm/refresh-edits-{MMDD}.py"
if EDITS.exists():
    exec(EDITS.read_text())


def main():
    cur = json.loads((ROOT / "src/bfcm.json").read_text())["brands"]
    out = {}
    for f in sorted((ROOT / "growth/bfcm").glob(f"research-{MMDD}-*.json")):
        for r in json.loads(f.read_text()):
            b = r["brand"]
            old = dict(cur.get(b) or cur.get(ALIAS.get(b, "")) or {})
            if r.get("status") not in ("live", "announced", "none_found"):
                if old:
                    out[b] = old            # unread: keep the earlier entry with its own date
                elif b in UNREAD:
                    out[b] = {"checked": DATE, "unread": True}
                continue
            phases = []
            for p in r.get("phases") or []:
                key = (b, p.get("name"))
                if key in DROP:
                    continue
                ph = {"name": NAME.get(key, p.get("name")), "start": p.get("start"), "end": p.get("end"),
                      "headline": HEADLINE.get(key, p.get("headline")), "url": p.get("url")}
                if not (ph["start"] or ph["end"]):
                    ph["seen"] = DATE
                    if r.get("status") == "announced":
                        ph["announced"] = True
                phases.append({k: v for k, v in ph.items() if v})
            phases += EXTRA.get(b, [])
            e = {k: old[k] for k in ("store", "sells", "new", "network_codes", "last_year") if old.get(k)}
            ly = r.get("last_year") or {}
            if ly.get("start") and not e.get("last_year"):
                e["last_year"] = {k: v for k, v in ly.items() if v and k in ("name", "start", "end", "headline", "url")}
            e.update({"checked": DATE, "phases": phases})
            out[b] = e
    p = ROOT / f"growth/bfcm/curated-refresh-{DATE}.json"
    p.write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(out)} brands -> {p.relative_to(ROOT)}; {sum(1 for e in out.values() if e.get('phases'))} with a sale")


if __name__ == "__main__":
    main()
