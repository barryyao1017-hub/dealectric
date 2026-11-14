"""Combo run, 11-14: re-check every Amazon listing the first matcher put on a live page (it matched accessories and
other models), look again with the strict matcher where one fails, have the model confirm each, and write the plan.
  python3.12 growth/combo/fix_amazon.py plan     -> growth/combo/amazon-fix.json
  python3.12 growth/combo/fix_amazon.py apply    -> edits src/gaps.py and the drafts (no build, no commit)"""
import json, re, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools")); sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "growth/evals"))
import abpage as A
import combopage as C
OUT = ROOT / "growth/combo/amazon-fix.json"


def pages():
    import gaps
    live = {g["slug"]: g for g in gaps.GAP_PAGES if g.get("run") == C.RUN}
    for f in sorted((ROOT / "growth/focus/ab").glob("c1113-*/draft.json")):
        d = json.loads(f.read_text())
        if d.get("amazon_rescue") and d.get("slug") in live:
            yield f, d, live[d["slug"]]


def plan():
    import ui
    tab = ui.Tab("about:blank")
    out = {}
    prev = json.loads(OUT.read_text()) if OUT.exists() else {}
    try:
        for f, d, g in pages():
            title = {r["asin"]: r.get("title", "") for r in d["amazon_rescue"] if r.get("asin")}
            rows = []
            for n, r in enumerate(g["rows"]):
                if not r.get("asin") or r["asin"] not in title:
                    continue
                e = {"n": n, "brand": r["brand"], "model": r.get("model") or "", "old": r["asin"], "old_title": title[r["asin"]]}
                was = next((x for x in (prev.get(g["slug"]) or {}).get("rows", []) if x["n"] == n and x.get("new")), None)
                if was:   # confirmed in an earlier pass
                    e.update(cand=was["new"], cand_title=was["cand_title"], kept=True)
                elif C.title_match(e["brand"], e["model"], e["old_title"]):
                    e.update(cand=e["old"], cand_title=e["old_title"])
                else:
                    hit = C.amazon_find(e["brand"], e["model"], tab)
                    time.sleep(4)
                    e.update(cand=hit and hit["asin"], cand_title=hit and hit["title"])
                    if not hit:
                        e["seen"] = getattr(C.amazon_find, "last_seen", None)
                rows.append(e)
            for e in rows:
                if e.get("kept"):
                    e["same"], e["why"] = True, "confirmed in an earlier pass"
            cands = [e for e in rows if e["cand"] and not e.get("kept")]
            ok = C.amazon_verify([{"i": i, "brand": e["brand"], "model": e["model"], "title": e["cand_title"]} for i, e in enumerate(cands)])
            for i, e in enumerate(cands):
                e["same"], e["why"] = ok.get(i, (False, "no verdict"))
            for e in rows:
                e["new"] = e["cand"] if e.get("same") else None
            out[g["slug"]] = {"folder": f.parent.name, "rows": rows, "pick_ok": bool(g["rows"][0].get("slug") or not rows or rows[0]["n"] != 0 or rows[0]["new"])}
            print(g["slug"], [(e["model"], e["old"], "->", e["new"]) for e in rows], "pick_ok", out[g["slug"]]["pick_ok"], flush=True)
            OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
    finally:
        tab.close()


def apply():
    P = json.loads(OUT.read_text())
    gp = ROOT / "src/gaps.py"
    t = gp.read_text()
    for slug, p in P.items():
        a = t.index("{\"slug\": %r," % slug)
        head = t.rfind("# ----------------", 0, a)
        b = t.find("# ----------------", a)
        b = len(t) if b < 0 else b
        if not p["pick_ok"]:
            t = t[:head] + t[b:]
            print("removed", slug)
            continue
        rec = t[a:b]
        cur = 0
        for e in sorted(p["rows"], key=lambda e: e["n"]):   # rows in table order: two rows can carry the same old ASIN
            old = ", 'asin': %r" % e["old"]
            i = rec.index(old, cur)
            rep = (", 'asin': %r" % e["new"]) if e["new"] else ""
            rec = rec[:i] + rep + rec[i + len(old):]
            cur = i + len(rep)
        t = t[:a] + rec + t[b:]
        f = ROOT / "growth/focus/ab" / p["folder"] / "draft.json"
        d = json.loads(f.read_text())
        d["amazon_fix_1114"] = p["rows"]
        f.write_text(json.dumps(d, ensure_ascii=False, indent=1))
    gp.write_text(t)


if __name__ == "__main__":
    {"plan": plan, "apply": apply}[sys.argv[1]]()
