#!/usr/bin/env python3.12
"""Open-query pages, 2026-11-15 (Barry): one page per open query from the 11-14/15 discovery run (22 queries that stayed
open in most plain ChatGPT chats; list in /Users/j0y0825/code/dealectric/growth/focus/open-queries/targets-22.json,
report https://claude.ai/artifact/1mBS24PWyoaPZNJET1kQBk). The research method is tools/abpage.py, unchanged; this file
only feeds it and adds this run's rules:

  * harvest from the saved discovery chats (no new ChatGPT chat: the account is busy with discovery);
  * "retarget": an existing page that already serves the query's need keeps its URL, and its title and H1 are rewritten
    in the query's plain words (abpage's own rebuild mode keeps them fixed for the A/B test);
  * the page's core is a cross-brand table of the measured result the question asks for, every figure with its source
    and the date read, or labelled arithmetic; Dealectric does not test units;
  * every row links (all_links): our program, else our tagged Amazon listing confirmed by combopage.amazon_verify, else
    the maker's page; the pick is the product that wins on the measured result (keep_pick when it has no link).

    python3.12 growth/focus/open-pages/openpage.py harvest [folder...]
    python3.12 growth/focus/open-pages/openpage.py research <folder>... [--workers 3] [--force]
    python3.12 growth/focus/open-pages/openpage.py links <folder>...      # Amazon listings for rows with no link
    python3.12 growth/focus/open-pages/openpage.py apply <folder>...      # abpage.apply (gates, build, commit locally)
    python3.12 growth/focus/open-pages/openpage.py status
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import datetime as dt
import json
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
for _p in ("tools", "src", "growth/evals"):
    sys.path.insert(0, str(ROOT / _p))
import abpage as A  # noqa: E402

RUN = "open-1115"
# Barry 2026-11-15 ("Cut to demand"): build only the two queries with search demand; the other folders keep their
# research (angle reports in the research library) and are not composed or published.
IN_SCOPE = {"best-solar-generator-for-power-outages", "power-station-for-cpap"}
TARGETS = Path("/Users/j0y0825/code/dealectric/growth/focus/open-queries/targets-22.json")   # main checkout, read only

# folder -> the queries it answers. "retarget": an existing page (folder = its slug) rebuilt for the query.
PAGES = {
    # rebuilt / retargeted existing pages
    # ac030: this page's H1 already read "Best solar generator for home use and backup" (G04): one page per search
    "best-solar-generator-for-power-outages": {"qids": ["ac030"], "retarget": True},
    "small-power-station-to-keep-wifi-router-and-modem-on-in-an-outage": {"qids": ["pm014", "pm015"], "retarget": True},
    "1kwh-power-station-with-1000w-solar-input-two-ports": {"qids": ["pm022"], "retarget": True},
    "power-station-to-run-a-pellet-stove-in-an-outage": {"qids": ["pm026"], "retarget": True},
    # pq025: /power-station-for-cpap already ranks "nights per charge" (moved from compare.py to gaps.py for this); the
    # week-of-camping page names one CPAP model and stays as it is
    "power-station-for-cpap": {"qids": ["pq025"], "retarget": True},
    "solar-generator-that-can-run-a-well-pump": {"qids": ["fk010"], "retarget": True},
    "best-240v-portable-power-station": {"qids": ["pq021"], "retarget": True},
    "quietest-1000wh-power-station-while-charging": {"qids": ["pq023"], "retarget": True, "hold": "former B page in DLC-272 reading 3"},
    "1000wh-power-station-that-can-run-a-microwave": {"qids": ["pr008"], "retarget": True, "hold": "former B page in DLC-272 reading 3"},
    "lightest-1000wh-lifepo4-power-station-for-car-camping": {"qids": ["pm005"], "retarget": True, "hold": "former B page in DLC-272 reading 3"},
    # new pages
    "oq-pm004-starts-biggest-appliances-for-size": {"qids": ["pm004"]},
    "oq-pq016-power-stations-linked-together": {"qids": ["pq016"]},
    "oq-pr006-fan-all-night-most-nights": {"qids": ["pr006"]},
    "oq-pp006-charge-in-freezing-weather": {"qids": ["pp006", "fm035"]},
    "oq-pp002-most-of-advertised-capacity": {"qids": ["pp002"]},
    "oq-pp004-recharges-fastest-from-solar": {"qids": ["pp004"]},
    "oq-pq006-charges-fastest-from-a-car": {"qids": ["pq006"]},
    "oq-pn010-enclosed-3d-printer-fastest-abs": {"qids": ["pn010"], "other": True},
    "oq-pn005-3d-scanner-big-car-part": {"qids": ["pn005"], "other": True},
    "oq-ps003-robot-mower-wet-grass": {"qids": ["ps003"], "other": True},
}


def targets() -> dict:
    return {t["qid"]: t for t in json.loads(TARGETS.read_text())}


def queries(folder: str) -> list[str]:
    if PAGES[folder].get("query"):   # a page fed from chat files with its own target search (bluetti-four run)
        return [PAGES[folder]["query"]]
    T = targets()
    return [T[q]["query"] for q in PAGES[folder]["qids"]]


def run_of(folder: str) -> str:
    return PAGES.get(folder, {}).get("run", RUN)


# ---------------------------------------------------------------- harvest (saved chats only)

def harvest(folder: str) -> dict:
    T = targets()
    d = A.pdir(folder)
    if (d / "harvest.json").exists():
        old = A.jload(d / "harvest.json")
        if old.get("run") != run_of(folder):   # the page's earlier harvest (another query): keep it with the page's history
            keep = d / "history" / dt.datetime.now().strftime("%Y-%m-%dT%H%M")
            keep.mkdir(parents=True, exist_ok=True)
            shutil.copy(d / "harvest.json", keep / "harvest.json")
    chats = []
    if PAGES[folder].get("web"):   # no saved ChatGPT chat for this search: a web search's top results stand in, labelled as such
        q = PAGES[folder]["query"]
        res = [{"rank": i, "domain": re.sub(r"^www\.", "", re.sub(r"^https?://", "", u).split("/")[0]), "title": t, "url": u,
                "dated": None, "cited": False, "ours": "dealectric.com" in u} for i, (t, u) in enumerate(PAGES[folder]["web"], 1)]
        chats.append({"chat": "web-stand-in", "at": A.today(), "model": "none (web search stand-in)", "typed": q, "queries": [q],
                      "results": res, "carousel": [], "cited_elsewhere": [], "verdict": None,
                      "answer": "No saved ChatGPT chat exists for this search. The results above are a web search's top results for "
                                "the same words, read " + A.today() + ", standing in for the pages a shopper's assistant would see."})
    srcs = [] if chats else [(f, None) for f in PAGES[folder].get("files", [])] or [(c["file"], c.get("verdict")) for q in PAGES[folder]["qids"] for c in T[q]["chats"]]
    for file, verdict in srcs:
        raw = json.loads(Path(file).read_text())
        f = A._chat_facts(raw)
        f["verdict"] = verdict
        chats.append(f)
    tags = []
    for ch in sorted(chats, key=lambda x: x.get("at") or "", reverse=True):
        for q in ch["queries"]:
            q = re.sub(r"\s{2,}", " ", q).strip()
            if q and q.lower() not in {t.lower() for t in tags}:
                tags.append(q)
    h = {"slug": folder, "run": run_of(folder), "updated": A.today(), "qids": PAGES[folder].get("qids", []), "chats": chats,
         "searched_as": tags[:6],
         "carousel": list(dict.fromkeys(p for ch in chats for p in ch["carousel"])),
         "cited_rivals": list(dict.fromkeys(x["url"] for ch in chats for x in ch["results"] if x["cited"] and not x["ours"]))}
    A.jsave(d / "harvest.json", h)
    return h


# ---------------------------------------------------------------- this run's prompt rules

RUN_RULES = """## Rules for this page (open-query run, Barry 2026-11-15)
- This question asks for a RESULT someone has to measure or work out across brands. The page's core is one table of that
  result for every candidate: each figure carries who measured it (named reviewer or lab) or which maker document states
  it, and the date read, in the cell's note or the cell itself ("RTINGS, read 2026-11-15"). A derived figure is labelled
  as arithmetic and shows its one-line sum in the after-section. Where nobody has measured it for a product, say so in
  the after-section and show the best derivable figure, labelled.
- Dealectric does not test units. Say so once, plainly, in the after-section (for example "Dealectric does not test
  units; the figures come from the named reviewers, the makers' manuals, or the arithmetic shown"). Never imply a test.
- Title and H1: the shopper's question in its own plain words (light trimming allowed), no model numbers, no jargon, no
  brand names unless the question has one. The answer's first sentence keeps the question's words.
- The pick is the product that wins on the measured result. Among near-ties prefer what can be bought through a link we
  have: an approved program (list below), then a product sold on amazon.com (the page links Amazon for rows with no
  program), then the maker's own page. If the clear winner is a product we don't list, it is still the pick and row 1;
  never bend the result toward a product we earn on. Our product then wins the segment it honestly wins (say which).
- A page needs at least one row we can link (a product we list, or one sold on amazon.com). If the honest answer has no
  such product at all, return status "skip" with the reason."""


def _compose_patch():
    orig = A.compose_prompt

    def compose_prompt(slug, h, query, angles, new_page):
        p = PAGES.get(slug, {})
        if p.get("retarget"):
            text = orig(slug, h, query, angles, False)
            text = re.sub(r"\n## Fixed for this page \(A/B test: retrieval must not move\)\n.*?own words\.",
                          f"\n## This page is retargeted\nKeep slug {slug} (the URL stays). Write a NEW title and h1 in the shopper "
                          "question's own plain words (the current page's title and h1 are not kept); desc rewritten too.",
                          text, flags=re.S)
        else:
            text = orig(slug, h, query, angles, new_page)
        if len(PAGES.get(slug, {}).get("qids", [])) > 1 and not p.get("query"):
            qs = queries(slug)
            text += ("\n\n## One page for two shopper questions\nThe chats above come from two questions that need the same page: "
                     + " | ".join(qs) + ". Title and h1 use the first; the answer paragraph must also answer the second in its "
                     "own words, and one after-section h2 uses the second question's words.")
        return text + "\n\n" + p.get("rules", RUN_RULES)
    A.compose_prompt = compose_prompt

    orig_q = A.query_for

    def query_for(slug, h):
        if slug in PAGES:
            return " / ".join(queries(slug))
        return orig_q(slug, h)
    A.query_for = query_for

    orig_v = A.validate

    def validate(draft, new_page):
        errs = orig_v(draft, new_page)
        if PAGES.get(draft.get("slug"), {}).get("retarget"):
            errs = [e for e in errs if not e.startswith("title or h1 changed")]
        if any(r.get("asin") for r in (draft.get("page") or {}).get("rows") or []):
            errs = [e for e in errs if not e.startswith("NO_LISTED_PRODUCT")]
        return errs
    A.validate = validate

    orig_rt = A.record_text

    def record_text(draft, old, gnum):
        t = orig_rt(draft, old, gnum)
        p = PAGES.get(draft.get("slug"), {})
        extra = "".join(f'"{k}": {v!r},\n ' for k, v in (p.get("flags") or {}).items())
        return t.replace('"method": ', f'"run": {run_of(draft.get("slug"))!r},\n {extra}"method": ', 1)
    A.record_text = record_text


_compose_patch()


def prep(folder: str) -> list[str]:
    """A retargeted page's earlier research (committed, for its old query) moves to history/ so the new query is
    researched from scratch without --force (a --force re-run would also redo angle reports this run already paid for)."""
    import subprocess
    d = A.pdir(folder)
    if not PAGES[folder].get("retarget") or PAGES[folder].get("hold"):
        return []
    old = []
    for f in sorted(d.glob("angle-*.json")) + [d / n for n in ("compose.json", "verify.json", "draft.json")]:
        if not f.exists():
            continue
        rel = str(f.relative_to(ROOT))
        tracked = subprocess.run(["git", "ls-files", "--error-unmatch", rel], cwd=ROOT, capture_output=True).returncode == 0
        clean = subprocess.run(["git", "diff", "--quiet", "--", rel], cwd=ROOT).returncode == 0
        if tracked and clean:
            old.append(f)
    if old:
        keep = d / "history" / ("before-" + RUN)
        keep.mkdir(parents=True, exist_ok=True)
        for f in old:
            shutil.copy(f, keep / f.name)
            f.unlink()
    (d / ".lock").unlink(missing_ok=True)
    return [f.name for f in old]


def research(folder: str, force: bool) -> dict:
    if PAGES[folder].get("hold") and not PAGES[folder].get("release"):
        return {"slug": folder, "status": "held: " + PAGES[folder]["hold"]}
    new = not PAGES[folder].get("retarget")
    return A.research(folder, new_page=new, force=force)


# ---------------------------------------------------------------- links (every row links)

def links(folder: str) -> dict:
    """Rows with no product record get our tagged Amazon listing where one exists and the same-item check confirms it."""
    import combopage as C
    import products as P
    sys.path.insert(0, str(ROOT / "growth/evals"))
    import ui
    import time
    d = A.pdir(folder)
    draft = A.jload(d / "draft.json")
    if not draft or draft.get("status") != "ok":
        return {"folder": folder, "status": "no draft"}
    C.sanitize(draft)
    C.fill_policy(draft)
    known = {p["slug"] for p in P.PRODUCTS} | {p["slug"] for p in draft.get("products") or []}
    rows = draft["page"]["rows"]
    todo = [r for r in rows if not r.get("slug") and not r.get("asin") and r.get("brand") and not re.search(r"used|refurb", str(r.get("model")), re.I)]
    found = []
    if todo:
        tab = ui.Tab("about:blank")
        try:
            for r in todo:
                hit = C.amazon_find(r["brand"], r.get("model") or "", tab)
                found.append({"row": f"{r['brand']} {r.get('model')}", "brand": r["brand"], "model": r.get("model"), **(hit or {"asin": None})})
                if hit:
                    r["asin"] = hit["asin"]
                time.sleep(4)
        finally:
            tab.close()
        hits = [f for f in found if f.get("asin")]
        ok = C.amazon_verify([{"i": i, "brand": f["brand"], "model": f"{f['brand']} {f['model']}", "title": f["title"]} for i, f in enumerate(hits)])
        for i, f in enumerate(hits):
            same, why = ok.get(i, (False, "no verdict"))
            f["verified"], f["why"] = same, why
            if not same:
                for r in rows:
                    if r.get("asin") == f["asin"] and not r.get("slug"):
                        r.pop("asin")
                f["rejected"], f["asin"] = f["asin"], None
    draft["amazon_links"] = found
    draft["all_links"] = True
    first = rows[0] if rows else {}
    draft["keep_pick"] = bool(first and not first.get("slug") and not first.get("asin"))
    if draft["keep_pick"] and not first.get("url"):
        draft["links_note"] = "pick has no link and no maker url"
    linked = [r for r in rows if r.get("slug") in known or r.get("asin")]
    draft["linkable_rows"] = len(linked)
    A.jsave(d / "draft.json", draft)
    return {"folder": folder, "rows": len(rows), "linked": len(linked), "keep_pick": draft["keep_pick"],
            "amazon": [(f["row"], f.get("asin"), f.get("verified")) for f in found]}


def apply(folder: str) -> dict:
    if PAGES[folder].get("hold") and not PAGES[folder].get("release"):
        return {"folder": folder, "status": "held: " + PAGES[folder]["hold"]}
    dr = A.jload(A.pdir(folder) / "draft.json") or {}
    if "amazon_links" not in dr:
        links(folder)
    return A.apply(folder, local=True)


def status() -> None:
    for f in PAGES:
        d = A.AB / f
        dr = A.jload(d / "draft.json", {}) or {}
        n = len(list(d.glob("angle-*.json"))) if d.exists() else 0
        g = dr.get("gate") or {}
        print(f"{f:68} h {'y' if (d / 'harvest.json').exists() else '-'} angles {n} draft {dr.get('slug', '-') if dr else '-':55.55} "
              f"gate {g.get('pass', '-')}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["harvest", "prep", "research", "links", "apply", "status"])
    ap.add_argument("folders", nargs="*")
    ap.add_argument("--workers", type=int, default=3)
    ap.add_argument("--force", action="store_true")
    a = ap.parse_args()
    fs = a.folders or list(PAGES)
    if a.cmd == "status":
        status()
    elif a.cmd == "harvest":
        for f in fs:
            h = harvest(f)
            print(f"{f}: {len(h['chats'])} chats, searched {h['searched_as'][:2]}", flush=True)
    elif a.cmd == "prep":
        for f in fs:
            print(f, prep(f), flush=True)
    elif a.cmd == "research":
        with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
            for r in ex.map(lambda f: research(f, a.force), fs):
                print(json.dumps(r, ensure_ascii=False), flush=True)
        import research_library
        research_library.build()
    elif a.cmd == "links":
        for f in fs:
            print(json.dumps(links(f), ensure_ascii=False), flush=True)
    elif a.cmd == "apply":
        for f in fs:
            print(json.dumps(apply(f), ensure_ascii=False)[:900], flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
