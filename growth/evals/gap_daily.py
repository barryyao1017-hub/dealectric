#!/usr/bin/env python3.12
"""Stage 2 of the gap experiment (growth/gap-experiment.md): daily readings for the published gap pages and for gap
clusters left without a page. Run once a day from the repo root with the agent's Chrome up.

    python3.12 growth/evals/gap_daily.py                 # today: indexed, rank, Claude unprompted (n = 1 per phrasing)
    python3.12 growth/evals/gap_daily.py --no-chat       # engines only

Readings per cluster: (1) indexed: the page URL in Bing for `site:dealectric.com <words>`; (2) rank: our position in the
live Bing top 10 for the agents' own queries (ChatGPT's from the queryprobe run, Claude's from runs/2026-10-25-fanout);
(3) unprompted: Claude (CLI, WebSearch + WebFetch, Brave-backed) asked the cluster's five phrasings from fanout.py;
counted: a dealectric.com URL in its search results, in its answer, a /go/ link in its answer. ChatGPT tier A on
Q01/Q02 is read with ui.py when the phase-3 loop is not using the account (see the plan file).
Writes growth/evals/runs/<date>-gap/readings.json.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import fanout  # noqa: E402
import serp  # noqa: E402

# cluster -> page we built (None = control) and the agent queries to rank on Bing
CLUSTERS = {
    "plane": {"page": "best-power-banks-for-flying", "site": "power banks flying",
              "queries": ["best power bank for airplane travel 2026 airline lithium battery carry-on rules TSA FAA",
                          "best power bank for flying carry-on airline approved 2026", "best 20000mAh power bank airline-friendly 2026"]},
    "solarkit": {"page": "solar-generator-with-panels-included", "site": "solar generator panels included",
                 "queries": ["solar generator with panels included", "best solar generator with panels included 2026"]},
    "tesla": {"page": "tesla-model-y-back-seat-screen", "site": "tesla model y back seat screen",
              "queries": ["Tesla Model Y back seat projector screen", "best rear seat entertainment screen Tesla Model Y 2026"]},
    # controls: gap clusters with no page
    "ups": {"page": None, "site": None,
            "queries": ["portable power station UPS transfer time computer manufacturer guidance EcoFlow Anker Bluetti",
                        "portable power station UPS function switchover time ms best 2026"]},
    "laptopstand": {"page": None, "site": None, "queries": ["best vertical laptop stand 2026", "best vertical laptop stand MacBook clamshell mode"]},
    "fitbitwomen": {"page": None, "site": None, "queries": ["best Fitbit watch for women 2026", "best fitness tracker for small wrists women 2026"]},
}


def bing_rank(q: str) -> tuple[int | None, list[str]]:
    rows = [r for r in serp.fetch("bing", q) if r.get("rank")]
    pos = next((r["rank"] for r in rows if r["domain"].endswith("dealectric.com")), None)
    return pos, [r["domain"] for r in rows[:10]]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-chat", action="store_true")
    ap.add_argument("--date", default=E.today())
    a = ap.parse_args()
    out_dir = E.run_dir(f"{a.date}-gap")
    out_dir.mkdir(parents=True, exist_ok=True)
    path = out_dir / "readings.json"
    R = json.loads(path.read_text()) if path.exists() else {}
    for name, c in CLUSTERS.items():
        r = R.setdefault(name, {"page": c["page"]})
        if c["page"] and "indexed" not in r:
            rows = [x for x in serp.fetch("bing", f"site:dealectric.com {c['site']}") if x.get("rank")]
            r["indexed"] = any(c["page"] in x["url"] for x in rows)
            time.sleep(5)
        if "rank" not in r:
            r["rank"] = {}
            for q in c["queries"]:
                pos, doms = bing_rank(q)
                r["rank"][q] = {"dealectric": pos, "top": doms}
                time.sleep(6)
        E.write_json(path, R)
    if not a.no_chat:
        jobs = [(name, n, prompt) for name in CLUSTERS for n, prompt in enumerate(fanout.CLUSTERS[name], 1)
                if f"{n}" not in R[name].get("claude", {})]

        def one(job):
            name, n, prompt = job
            res = fanout.ask(prompt)
            urls = [u for group in res["result_urls"] for u in group] + res["fetches"]
            page = CLUSTERS[name]["page"]
            return name, n, {"queries": res["queries"], "dealectric_in_results": any("dealectric.com" in u for u in urls),
                             "page_in_results": bool(page) and any(page in u for u in urls),
                             "dealectric_in_answer": "dealectric.com" in res["answer"],
                             "go_link_in_answer": bool(re.search(r"dealectric\.com/go/", res["answer"])),
                             "answer": res["answer"][:3000]}

        with cf.ThreadPoolExecutor(4) as ex:
            for name, n, row in ex.map(one, jobs):
                R[name].setdefault("claude", {})[str(n)] = row
                E.write_json(path, R)
    print(f"{'cluster':12} {'page':5} {'indexed':8} {'best Bing rank':>14}  claude: in results / in answer / /go/")
    for name, r in R.items():
        ranks = [v["dealectric"] for v in r.get("rank", {}).values() if v["dealectric"]]
        cl = r.get("claude", {}).values()
        print(f"{name:12} {'yes' if r['page'] else 'no':5} {str(r.get('indexed', '-')):8} {str(min(ranks) if ranks else None):>14}  "
              f"{sum(x['dealectric_in_results'] for x in cl)}/{len(cl)} / {sum(x['dealectric_in_answer'] for x in cl)}/{len(cl)} / {sum(x['go_link_in_answer'] for x in cl)}/{len(cl)}")


if __name__ == "__main__":
    main()
