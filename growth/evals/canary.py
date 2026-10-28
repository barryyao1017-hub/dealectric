#!/usr/bin/env python3.12
"""DLC-77 canary: does OpenAI's stored copy of a page hold text past the opening, and which passage does a query get?
Design: growth/focus/canary.md.

    python3.12 growth/evals/canary.py --gate                          # has OAI-SearchBot fetched /about since the canary shipped?
    python3.12 growth/evals/canary.py growth/evals/runs/<date>-canary # score a reading

The canary is the last section of /about ("How codes are re-tested"), wording found nowhere else on the site. Per
cell: did the answer relay it, was /about in ChatGPT's results (rank, title, snippet), and did any OpenAI agent
request /about from 30 minutes before the chat to its end (a live fetch, or one a chat a few minutes earlier made
and this chat reused). Only cells with no such request say anything about the stored copy.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import storedcopy as SC  # noqa: E402

sys.path.insert(0, str(SC.E.REPO / "tools"))
PAGE = "/about"
CANARY = "06:37 Pacific"   # in the shipped HTML; the first deployment carrying it is the ship time
MARKERS = re.compile(r"06:37|6:37|control code|two (?:mornings|days|checks|runs) in a row|rejects? (?:it )?twice|unattended", re.I)
OPENAI_UA = ("ChatGPT", "OAI-SearchBot", "GPTBot", "Mozilla/5.0 (compatible)")


def ship_time() -> str | None:
    deploys = json.loads(SC.DEPLOYS.read_text())
    blobs = SC.Blobs()
    for d in deploys:
        raw = blobs.get(f"{d['sha']}:{SC.page_file(PAGE)}")
        if raw and CANARY.encode() in raw:
            return d["at"]
    return None


def openai_requests(t0: dt.datetime, t1: dt.datetime) -> list[str]:
    import cf
    q = ('{viewer{zones(filter:{zoneTag:$zone}){httpRequestsAdaptiveGroups(limit:100, filter:{datetime_geq:"%s", '
         'datetime_lt:"%s", clientRequestPath:"%s"}, orderBy:[datetime_ASC]){dimensions{datetime userAgent}}}}}') % (
        SC.iso(t0), SC.iso(t1), PAGE)
    r = cf.query(q)
    if r.get("errors"):
        return ["query failed: " + r["errors"][0].get("message", "")[:80]]
    return [f"{g['dimensions']['datetime'][11:19]} {g['dimensions']['userAgent'][:50]}"
            for g in r["data"]["viewer"]["zones"][0]["httpRequestsAdaptiveGroups"]
            if any(k in g["dimensions"]["userAgent"] for k in OPENAI_UA)]


def gate() -> int:
    SC.DEPLOYS.write_text(json.dumps(SC.fetch_deployments(), indent=0) + "\n")
    crawls = SC.page_crawls(SC.refresh_crawls(SC.load_crawls()))
    ship = ship_time()
    if not ship:
        print("canary not deployed yet")
        return 1
    got = [t for t in crawls.get(PAGE, {}).get("OAI-SearchBot", []) if t >= ship]
    print(f"canary live {ship}; OAI-SearchBot fetches of {PAGE} since: {', '.join(got) or 'none yet'}")
    return 0 if got else 1


def score(run: Path) -> int:
    ship = ship_time()
    crawls = SC.page_crawls(SC.load_crawls())
    rows = []
    for f in sorted((run / "chatgpt").glob("*.json")):
        d = json.loads(f.read_text())
        r = d.get("response") or {}
        t0 = SC.parse_t(d.get("started_at") or d.get("at"))
        t1 = SC.parse_t(d.get("finished_at") or d.get("started_at") or d.get("at"))
        ans = r.get("answer") or d.get("text") or ""
        hit = [m.group(0) for m in MARKERS.finditer(ans)]
        res = next(((i, s) for i, s in enumerate(r.get("search_results") or [], 1) if SC.norm_path(s.get("url") or "") == PAGE), None)
        pill = any(SC.norm_path(p.get("url") or "") == PAGE for p in d.get("cite_pills") or [])
        live = openai_requests(t0 - dt.timedelta(minutes=30), t1 + dt.timedelta(minutes=1))
        oai = SC.last_before(crawls.get(PAGE, {}).get("OAI-SearchBot", []), SC.iso(t0))
        rows.append({"cell": f.stem, "t": SC.iso(t0), "model": d.get("answer_model"), "canary": hit,
                     "about_rank": res[0] if res else None, "about_title": res[1].get("title") if res else None,
                     "about_snippet": res[1].get("snippet") if res else None, "about_pill": pill, "openai_requests": live,
                     "clean": not live, "index_after_ship": bool(oai and ship and oai >= ship)})
    print(f"canary shipped {ship}; cells {len(rows)}")
    print("| cell | model | /about in results | pill | canary relayed | OpenAI requests -30 min..end | index fetched after ship | snippet |")
    print("|---|---|---|---|---|---|---|---|")
    for x in rows:
        print(f"| {x['cell']} | {x['model']} | {x['about_rank'] or '-'} | {'yes' if x['about_pill'] else ''} | {', '.join(x['canary']) or 'no'} | "
              f"{'; '.join(x['openai_requests']) or 'none'} | {'yes' if x['index_after_ship'] else 'no'} | {(x['about_snippet'] or '')[:160]} |")
    clean = [x for x in rows if x["clean"] and x["index_after_ship"]]
    print(f"\nclean cells read after the crawl: {len(clean)}; relayed the canary: {sum(1 for x in clean if x['canary'])}")
    (run / "canary-score.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("run", nargs="?")
    ap.add_argument("--gate", action="store_true")
    a = ap.parse_args()
    if a.gate:
        return gate()
    if not a.run:
        ap.error("give a run folder or --gate")
    return score(Path(a.run).resolve())


if __name__ == "__main__":
    sys.exit(main())
