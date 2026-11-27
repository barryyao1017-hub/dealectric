#!/usr/bin/env python3.12
"""Retire rule (page flow, DLC-369): pages that never drew a shopper are reworked once, then retired, slowly enough
that the site keeps growing.

    python3.12 tools/pageflow/retire.py report     # who is a candidate, who is due, what the guard allows
    python3.12 tools/pageflow/retire.py step       # advance the states in growth/pageflow/retire.json (no page is touched)

The rule (Barry 2026-11-27, with the plan's safeguards):
  candidate   a comparison page (gap, comparison or kit page; never a product, codes, seasonal or site page), live
              MIN_AGE days or more, with no shopper visit, no buy-link click and no sale;
  seen        and OpenAI's crawler fetched it at least once since it was published. A page OAI-SearchBot never fetched
              has an indexing problem, not a content problem: it is listed apart and not counted against the page;
  rework      a candidate first gets one rework: its cluster's map names the line it should answer (pages_to_fix), and
              the driver rebuilds it on that line with a new title, keeping the URL;
  retire      still at zero REWORK_WAIT days after the rework, it is due: the page becomes a short "no longer kept up"
              page that links to the nearest live page of its cluster, noindex and out of the sitemap, as retired
              product pages already are;
  guard       at most one page is retired for every two added in the trailing 30 days, the least-visited clusters
              first, so the site expands while it prunes.
Retiring itself is off until growth/pageflow/RETIRE_ON exists (switched on after the first 28-day readings of the pages
the flow built). Until then `step` only records candidates and the dates they were first seen.
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import propose as P  # noqa: E402

MIN_AGE = 45
REWORK_WAIT = 30
KINDS = ("gap", "comparison", "kit")
STATE = C.DATA / "retire.json"
SWITCH = C.DATA / "RETIRE_ON"


def fetched_pages() -> set | None:
    """Pages OAI-SearchBot fetched (200) at least once, from the crawl log storedcopy.py keeps; None when there is no log."""
    try:
        import storedcopy as S
        crawls = S.load_crawls()
        if not crawls:
            return None
        pc = S.page_crawls(crawls)
        return {p.strip("/") for p, bots in pc.items() if any("OAI-SearchBot" in b or "ChatGPT" in b for b in bots)}
    except Exception:   # noqa: BLE001  (the log is a convenience: without it nothing is retired)
        return None


def successor(slug: str, led: dict) -> str:
    """The nearest live page: same cluster, visited, most alike by title; else the cluster's most visited page."""
    p = led["pages"][slug]
    peers = [(s, q) for s, q in led["pages"].items() if s != slug and q["cluster"] == p["cluster"] and q["kind"] in KINDS and q["visits"] > 0]
    if not peers:
        return ""
    best = max(peers, key=lambda x: (round(P.similar(p["title"], x[1]["title"]), 2), x[1]["visits"]))
    return best[0]


def candidates(led: dict) -> dict:
    seen = fetched_pages()
    out = {"candidates": [], "unseen": [], "crawl_log": seen is not None}
    for slug, p in led["pages"].items():
        if p["kind"] not in KINDS or p["age"] is None or p["age"] < MIN_AGE:
            continue
        if p["visits"] or p["clicks"] or p["sales"]:
            continue
        if seen is not None and slug not in seen:
            out["unseen"].append(slug)
            continue
        out["candidates"].append(slug)
    return out


def allowance(led: dict, st: dict) -> int:
    added = sum(1 for p in led["pages"].values() if p["kind"] in KINDS and p["age"] is not None and p["age"] < 30)
    retired = sum(1 for v in st["pages"].values() if v.get("retired") and C.days_between(v["retired"], C.today()) < 30)
    return max(0, added // 2 - retired)


def step() -> dict:
    led = C.jload(C.LEDGER)
    st = C.jload(STATE) or {"pages": {}}
    c = candidates(led)
    today = C.today()
    for slug in list(st["pages"]):   # a page that drew a shopper since is no longer a candidate
        if slug in led["pages"] and (led["pages"][slug]["visits"] or led["pages"][slug]["clicks"]) and not st["pages"][slug].get("retired"):
            st["pages"].pop(slug)
    for slug in c["candidates"]:
        v = st["pages"].setdefault(slug, {"first_flagged": today, "state": "rework", "cluster": led["pages"][slug]["cluster"]})
        if v["state"] == "reworked" and C.days_between(v["reworked"], today) >= REWORK_WAIT:
            v["state"], v["to"] = "due", successor(slug, led)
    st.update(updated=today, switch=SWITCH.exists(), allowance=allowance(led, st), unseen=len(c["unseen"]), crawl_log=c["crawl_log"])
    C.jsave(STATE, st)
    return st


def report() -> str:
    led = C.jload(C.LEDGER)
    st = step()
    by = {}
    for slug, v in st["pages"].items():
        by.setdefault(v["state"], []).append(slug)
    lines = [f"Retire rule ({'ON' if st['switch'] else 'off: no page is retired yet'}), ledger of {led['built']}:",
             f"- {len(by.get('rework', []))} pages are {MIN_AGE}+ days old with no shopper visit, click or sale (first step for each: one rework)",
             f"- {len(by.get('reworked', []))} reworked and waiting {REWORK_WAIT} days; {len(by.get('due', []))} due to retire; "
             f"{sum(1 for v in st['pages'].values() if v.get('retired'))} retired",
             f"- {st['unseen']} more are at zero but OpenAI's crawler never fetched them (an indexing problem, not counted against the page)"
             if st["crawl_log"] else "- no crawl log here, so 'never fetched' pages cannot be told apart yet (nothing is retired without it)",
             f"- the growth guard allows {st['allowance']} retirements now (one for every two pages added in the last 30 days)"]
    cl = {}
    for slug in by.get("rework", []):
        cl[st["pages"][slug].get("cluster") or "-"] = cl.get(st["pages"][slug].get("cluster") or "-", 0) + 1
    if cl:
        lines.append("- candidates by cluster: " + ", ".join(f"{k} {n}" for k, n in sorted(cl.items(), key=lambda x: -x[1])))
    return "\n".join(lines)


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "report"
    if cmd == "step":
        st = step()
        print(f"retire states: {len(st['pages'])} pages tracked, allowance {st['allowance']}, switch {'on' if st['switch'] else 'off'}")
    else:
        print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
