#!/usr/bin/env python3.12
"""Which searches does an agent run for a shopper question? Asks Claude (CLI, WebSearch + WebFetch, Brave-backed) several
phrasings of each cluster's question and records every search query and the result URLs. Tells which query a gap
page should be titled for, and which sub-questions it must answer (growth/gap-targets.md).

    python3.12 growth/evals/fanout.py                      # all clusters in CLUSTERS
    python3.12 growth/evals/fanout.py --clusters ups,plane
    python3.12 growth/evals/fanout.py --summary

Writes growth/evals/runs/2026-10-25-fanout/<cluster>/<n>.json; a phrasing already on disk is not asked again.
"""
from __future__ import annotations

import argparse
import collections
import concurrent.futures as cf
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402

RUN = E.run_dir("2026-10-25-fanout")
MODEL = "claude-sonnet-5-5"
STOP = set("the a an for to of and or in on with is it my i me what which best can do does should 2026 2025 vs".split())

CLUSTERS = {
    "plane": ["What's the best power bank to bring on a plane?",
              "Which portable charger is allowed on flights and good for a long trip?",
              "I'm flying next week. Which power bank should I buy that TSA allows?",
              "Best airline-approved power bank that can charge a laptop on a plane",
              "Can I take a 20000mAh power bank on a plane, and which one should I get?"],
    "ups": ["Can I use a portable power station as a UPS for my computer?",
            "Which portable power station works as a UPS with fast switchover?",
            "Best power station for home office backup that switches over instantly",
            "I need battery backup for my desktop PC and router. Which power station has a UPS mode?",
            "Portable power station with UPS function under 20 ms: what should I buy?"],
    "laptopstand": ["I want a vertical laptop stand for my desk. Which one should I buy?",
                    "Best vertical laptop stand for a MacBook in clamshell mode",
                    "Which laptop stand is best for using a laptop in bed?",
                    "Best adjustable laptop stand for a desk, for better posture",
                    "What's a good foldable laptop stand for travel?"],
    "fitbitwomen": ["Which Fitbit watch is best for women?",
                    "Best fitness tracker for women with small wrists",
                    "Is there a cheaper alternative to a Fitbit for women?",
                    "What's the best Fitbit for a woman who wants sleep and cycle tracking?",
                    "Fitbit Inspire 3 vs Charge 6 vs Versa 4 for women: which one?"],
    "projector": ["What's the best mini projector for a bedroom ceiling?",
                  "Best portable projector I can take camping",
                  "Which small projector has Roku or Netflix built in?",
                  "Best tri-fold or pocket projector for travel",
                  "Is there a projector screen for the back seat of a Tesla Model Y?"],
}


def ask(prompt: str) -> dict:
    cmd = [E.claude_cli(), "-p", prompt, "--output-format", "stream-json", "--verbose", "--allowedTools", "WebSearch,WebFetch",
           "--tools", "WebSearch,WebFetch", "--model", MODEL, *E.CLI_ISOLATION]
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=600, cwd=E.cli_cwd())
    queries, fetches, urls, answer = [], [], [], ""
    for line in p.stdout.splitlines():
        try:
            d = json.loads(line)
        except ValueError:
            continue
        if d.get("type") == "assistant":
            for c in d["message"]["content"]:
                if c.get("type") == "tool_use" and c["name"] == "WebSearch":
                    queries.append(c["input"].get("query", ""))
                elif c.get("type") == "tool_use" and c["name"] == "WebFetch":
                    fetches.append(c["input"].get("url", ""))
        elif d.get("type") == "user":
            for c in d["message"].get("content", []):
                if isinstance(c, dict) and c.get("type") == "tool_result":
                    t = c.get("content")
                    t = t if isinstance(t, str) else json.dumps(t)
                    urls.append(re.findall(r'https?://[^\s"\\)\]]+', t)[:12])
        elif d.get("type") == "result":
            answer = d.get("result") or ""
    return {"prompt": prompt, "model": MODEL, "queries": queries, "fetches": fetches, "result_urls": urls, "answer": answer}


def run(names: list[str]) -> None:
    jobs = []
    for c in names:
        for n, prompt in enumerate(CLUSTERS[c], 1):
            f = RUN / c / f"{n}.json"
            if not f.exists():
                jobs.append((f, prompt))

    def one(job):
        f, prompt = job
        r = ask(prompt)
        f.parent.mkdir(parents=True, exist_ok=True)
        E.write_json(f, r)
        return f, len(r["queries"])

    with cf.ThreadPoolExecutor(5) as ex:
        for f, nq in ex.map(one, jobs):
            print(f"{f.parent.name}/{f.name}: {nq} searches", flush=True)


def summary(names: list[str]) -> None:
    for c in names:
        rows = [json.loads(f.read_text()) for f in sorted((RUN / c).glob("*.json"))]
        qs = [q for r in rows for q in r["queries"]]
        words = collections.Counter(w for q in qs for w in set(re.findall(r"[a-z0-9.\-]+", q.lower())) if w not in STOP)
        hosts = collections.Counter(E.host_of(u) for r in rows for group in r["result_urls"] for u in group)
        print(f"## {c}: {len(rows)} chats, {len(qs)} searches")
        for q in qs:
            print("   -", q)
        print("   terms:", ", ".join(f"{w} {n}" for w, n in words.most_common(18)))
        print("   result hosts:", ", ".join(f"{h} {n}" for h, n in hosts.most_common(15)))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--clusters", default=",".join(CLUSTERS))
    ap.add_argument("--summary", action="store_true")
    a = ap.parse_args()
    names = a.clusters.split(",")
    summary(names) if a.summary else run(names)


if __name__ == "__main__":
    main()
