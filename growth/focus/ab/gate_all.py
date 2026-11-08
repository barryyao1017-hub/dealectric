"""Re-run the length gate (fastloop check --research, ranks 1/3/6) on every research-method page in docs/."""
import json, subprocess, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
import gaps
v2 = {g["slug"] for g in gaps.GAP_PAGES if g.get("method") == "ab-2026-11"}
drafts = {}
for d in (ROOT / "growth/focus/ab").glob("*/draft.json"):
    j = json.loads(d.read_text())
    if (j.get("gate") or {}).get("pass") and j.get("slug") in v2:
        drafts[j["slug"]] = (d.parent.name, j["must"])
fails = []
for s in sorted(v2):
    if s not in drafts:
        fails.append((s, "no draft")); continue
    key, must = drafts[s]
    cmd = ["python3.12", "growth/evals/fastloop.py", "check", f"docs/{s}.html", "--packs", f"ab-{key}"[:60], "--ranks", "1,3,6", "--research"]
    for m in must:
        cmd += ["--must", m]
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=ROOT)
    if "PASS" not in r.stdout:
        fails.append((s, r.stdout[r.stdout.find("FAIL"):][:300]))
print(len(v2), "pages,", len(fails), "fail")
for f in fails:
    print(f)
sys.exit(1 if fails else 0)
