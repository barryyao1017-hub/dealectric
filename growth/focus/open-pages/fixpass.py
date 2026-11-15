"""One sourced fix pass on a verified draft, with errors written by hand (open-query run). Usage: fixpass.py <folder> <errors.json>"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "growth/focus/open-pages")); sys.path.insert(0, str(ROOT / "tools"))
import openpage  # noqa: F401  (this run's patches)
import abpage as A
folder, errs = sys.argv[1], json.loads(Path(sys.argv[2]).read_text())
d = A.pdir(folder)
draft = A.jload(d / "draft.json")
fx = A.claude(A.fix_prompt(draft, errs))
A.jsave(d / "fixpass.json", fx)
if fx.get("draft"):
    keep = {k: draft[k] for k in ("new_page", "searched_as", "angle", "why_angle", "query", "slug", "verified_changes", "verified_removed") if k in draft}
    A.jsave(d / "draft.pre-fixpass.json", draft)
    A.jsave(d / "draft.json", {**fx["draft"], **keep, "status": "ok", "hand_fix": {"errors": errs, "log": fx.get("log")}})
    print("fixed:", json.dumps(fx.get("log"), ensure_ascii=False)[:1500])
else:
    print("no draft back:", str(fx)[:500])
