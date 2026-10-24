#!/usr/bin/env python3.12
"""Phase 3 summary (growth/improvement-loop.md "Phase 3"): ALR per assistant on F01–F12, the steering controls X01/X02,
failure classes and which link the answer used instead.   python3.12 growth/evals/p3summary.py --run-id <run>"""
import argparse, collections, json, re, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402

ap = argparse.ArgumentParser(); ap.add_argument("--run-id", required=True); a = ap.parse_args()
rd = E.run_dir(a.run_id)
q = {x["id"]: x for x in E.load_questions()["questions"]}
rows = [json.loads(l) for l in open(rd / "grades.jsonl")]
for asst in sorted({r["assistant"] for r in rows}):
    rs = [r for r in rows if r["assistant"] == asst and r["qid"].startswith("F")]
    l4 = sum(r["level"] == 4 for r in rs); named = sum(r["level"] >= 1 for r in rs); cl = sum(bool(r.get("code_and_link")) for r in rs)
    print(f"\n== {asst}: ALR {l4}/{len(rs)} ({100*l4/max(1,len(rs)):.0f}%), our product named {named}/{len(rs)}, code+link {cl}/{len(rs)}")
    print("   failure classes:", dict(collections.Counter(r.get("failure_class") or "L4" for r in rs)))
    for r in sorted(rs, key=lambda r: (r["qid"], r["n"])):
        rec = json.load(open(rd / asst / f"{r['qid']}-F-{r['n']}.json"))
        links = [u for u in rec.get("all_urls", []) if "dealectric.com/go/" in u or not re.search(r"dealectric\.com", u)]
        shop = [re.sub(r"\?.*", "", u)[:60] for u in rec.get("all_urls", []) if "dealectric.com" not in u][:3]
        print(f"   {r['qid']}-{r['n']} L{r['level']} {r.get('failure_class') or ''} go={r.get('go_slugs') or ''} other={shop}")
    for x in ("X01", "X02"):
        for r in [r for r in rows if r["assistant"] == asst and r["qid"] == x]:
            rec = json.load(open(rd / asst / f"{x}-F-{r['n']}.json"))
            ok = q[x]["honest_pick"].lower() in rec.get("text", "").lower()
            print(f"   control {x}-{r['n']}: honest pick {'named' if ok else 'MISSING'}; L{r['level']}")
