"""Length gate (fastloop check --research, ranks 1/3/6, the page's own must phrases) on the 44 group A pages, reading
the built docs of another checkout (the push-3 worktree) with the packs of this one.
    python3.12 gate_A.py <docs dir>"""
import json, subprocess, sys
from pathlib import Path
ROOT = Path('/Users/j0y0825/code/dealectric')
docs = Path(sys.argv[1])
A = [l.strip().strip('/') for l in open(ROOT / 'growth/focus/ab/A-slugs.txt') if l.strip()]
drafts = {}
for d in (ROOT / "growth/focus/ab").glob("*/draft.json"):
    j = json.loads(d.read_text())
    if (j.get("gate") or {}).get("pass") and j.get("slug") in A:
        drafts[j["slug"]] = (d.parent.name, j["must"])
fails = []
for s in A:
    if s not in drafts:
        fails.append((s, "no draft")); continue
    key, must = drafts[s]
    cmd = ["python3.12", "growth/evals/fastloop.py", "check", str(docs / f"{s}.html"), "--packs", f"ab-{key}"[:60], "--ranks", "1,3,6", "--research"]
    for m in must:
        cmd += ["--must", m]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if "PASS" not in r.stdout:
        fails.append((s, (r.stdout[r.stdout.find("FAIL"):] or r.stdout[-300:] or r.stderr[-300:])[:400]))
print(len(A), "pages,", len(fails), "fail")
for f in fails:
    print(f)
