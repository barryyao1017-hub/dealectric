"""Length gate (fastloop check --research, ranks 1/3/6, each page's must phrases) on the 65 treated pages, from the repo
root after a build: python3.12 growth/focus/ab/push4/gate.py"""
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
import abpage
S = [l.strip() for l in open(Path(__file__).parent / 'slugs.txt') if l.strip()]
fails = []
for s in S:
    d = json.loads((ROOT / 'growth/focus/ab' / s / 'draft.json').read_text())
    cmd = ["python3.12", "growth/evals/fastloop.py", "check", f"docs/{s}.html", "--packs", abpage.pack_from_harvest(s), "--ranks", "1,3,6", "--research"]
    for m in d["must"]:
        cmd += ["--must", m]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if "PASS" not in r.stdout:
        fails.append((s, (r.stdout[r.stdout.find("FAIL"):] or r.stdout[-300:] or r.stderr[-300:])[:400]))
print(len(S), "pages,", len(fails), "fail")
for f in fails:
    print(f)
