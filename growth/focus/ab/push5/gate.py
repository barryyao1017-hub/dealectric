"""Length gate (fastloop check --research, ranks 1/3/6, each page's must phrases) on the 207 adopted pages (DLC-291), from the
repo root after a build: python3.12 growth/focus/ab/push5/gate.py. A page researched in a batch keeps its draft in the batch
folder (growth/focus/ab/library.json maps folder -> slug)."""
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / 'tools'))
import abpage
S = [l.strip() for l in open(Path(__file__).parent / 'slugs.txt') if l.strip()]
AB = ROOT / 'growth/focus/ab'
F = {}
for p in json.loads((AB / 'library.json').read_text())['pages']:
    F.setdefault(p['slug'], p['folder'])
F.update({s: s for s in S if (AB / s / 'draft.json').exists()})
fails = []
for s in S:
    f = F.get(s)
    if not f or not (AB / f / 'draft.json').exists() or not (AB / f / 'harvest.json').exists():
        fails.append((s, 'no draft or harvest folder'))
        continue
    d = json.loads((AB / f / 'draft.json').read_text())
    cmd = ["python3.12", "growth/evals/fastloop.py", "check", f"docs/{s}.html", "--packs", abpage.pack_from_harvest(f), "--ranks", "1,3,6", "--research"]
    for m in d["must"]:
        cmd += ["--must", m]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if "PASS" not in r.stdout:
        fails.append((s, (r.stdout[r.stdout.find("FAIL"):] or r.stdout[-300:] or r.stderr[-300:])[:400]))
print(len(S), "pages,", len(fails), "fail")
for f in fails:
    print(f)
