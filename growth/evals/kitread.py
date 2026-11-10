#!/usr/bin/env python3.12
"""Buy-link hand-over reading for the kit pilot (DLC-223, North Star 3).

Reads saved app chats (growth/evals/runs/<run>/chatgpt/*.json, written by visibility_scan.py) and, per chat answered by
plain gpt-6, records: was a dealectric.com page in the search results, was it cited, and did the answer hand over our buy
link: a dealectric.com/go/ link (a kit's /go/kit-... counted separately) or an amazon.com link carrying our tag
(tag=dealectric-20, or AssociateTag=dealectric-20 on the Add-to-Cart form an Amazon kit uses).

Groups come from the question file's "group" field ("kit" or "control"). North Star 3's rate is hand-overs over chats
with our page in the results.

    python3.12 growth/evals/kitread.py --runs 2026-11-1x-kit-read --questions growth/focus/kit-read-<date>.json
"""
import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TAG = "dealectric-20"


def urls_of(c: dict) -> list[str]:
    r = c.get("response") or {}
    us = [x.get("url", "") for x in (c.get("citations") or []) + (c.get("cite_pills") or [])]
    us += [u.get("url", "") for u in r.get("markup_urls") or []]
    blob = (c.get("text") or "") + "\n".join(r.get("markup") or [])
    us += re.findall(r"https?://[^\s\"'<>)\]]+", blob)
    return [u for u in us if u]


def read(c: dict) -> dict:
    us = urls_of(c)
    go = sorted({u.split("?")[0] for u in us if re.match(r"https?://(www\.)?dealectric\.com/go/", u)})
    amz = sorted({u for u in us if "amazon.com" in u and TAG in u})
    results = (c.get("response") or {}).get("search_results") or []
    rank = next((i for i, x in enumerate(results, 1) if "dealectric.com" in (x.get("url") or "")), None)
    cited = any(re.match(r"https?://(www\.)?dealectric\.com/(?!go/)", u) for u in us)
    return {"rank": rank, "cited": cited, "go": go, "amazon": amz, "kit_link": any("/go/kit-" in u for u in go) or any("cart/add" in u for u in amz),
            "handover": bool(go or amz)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--runs", nargs="+", required=True)
    ap.add_argument("--questions", required=True)
    a = ap.parse_args()
    qs = {q["qid"]: q for q in json.loads(Path(a.questions).read_text())["questions"]}
    rows = []
    for run in a.runs:
        for f in sorted((ROOT / "growth/evals/runs" / run / "chatgpt").glob("*.json")):
            c = json.loads(f.read_text())
            m = c.get("answer_model") or ""
            q = qs.get(c.get("qid"))
            if not q or not m.startswith("gpt-6") or m.endswith("mini"):
                continue
            rows.append({"qid": q["qid"], "group": q.get("group", "?"), "page": q.get("page"), **read(c)})
    by = defaultdict(list)
    for r in rows:
        by[r["group"]].append(r)
    print("| group | chats | our page in results | cited | hand-over (any) | hand-over / in results | kit link |")
    print("|---|---|---|---|---|---|---|")
    for g, rs in sorted(by.items()):
        inr = [r for r in rs if r["rank"]]
        ho = [r for r in inr if r["handover"]]
        print(f"| {g} | {len(rs)} | {len(inr)} | {sum(r['cited'] for r in inr)} | {sum(r['handover'] for r in rs)} | "
              f"{len(ho)}/{len(inr)} ({100 * len(ho) / len(inr):.0f}%) | {sum(r['kit_link'] for r in rs)} |" if inr else
              f"| {g} | {len(rs)} | 0 | 0 | {sum(r['handover'] for r in rs)} | - | {sum(r['kit_link'] for r in rs)} |")
    out = ROOT / "growth/evals/runs" / a.runs[-1] / "kitread.json"
    out.write_text(json.dumps(rows, indent=1))
    print(f"\n{len(rows)} chats; rows in {out.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
