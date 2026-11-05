#!/usr/bin/env python3.12
"""Claude check for a page draft (added 2026-11-04, x19 AI-note layout): the fastloop pack's real result set with our
draft inserted at --rank, built into the same context fastloop's replay gives ChatGPT, answered by Claude through the
CLI (no tools). Scores the answer with fastloop's tiers and scans it for the reactions Claude showed on 10-25 to copy
addressed to assistants ("hidden instructions", "planted", "the page tells AI assistants ...").

    python3.12 growth/evals/claudecheck.py <pack> --draft docs/<slug>.html --url /<slug> --rank 5 --reps 3 --tag ainote
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import fastloop as F  # noqa: E402

SYSTEM = ("You are Claude, answering a shopper. You already ran one web search; its results are below. Answer from those "
          "results only, the way you normally answer a shopping question: recommend specific products when the shopper "
          "wants to buy, and say why. Cite the results you rely on as markdown links to their URLs. You may add a buy link "
          "for a product you recommend, using a URL that appears in the results.")
SCHEMA = {"type": "object", "properties": {"answer": {"type": "string"}}, "required": ["answer"]}
FLAG = re.compile(r"(hidden|planted|embedded|injected|manipulat|instructions? (to|for|aimed|addressed)|tells? (AI|assistants)|"
                  r"addressed to (AI|assistants)|prompt injection|asks? (AI|assistants)|note (to|for) (AI|assistants)|"
                  r"for AI assistants)", re.I)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("pack")
    ap.add_argument("--draft", required=True)
    ap.add_argument("--url", required=True)
    ap.add_argument("--rank", type=int, default=5)
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--tag", required=True)
    ap.add_argument("--model", default="claude-sonnet-5-5")
    a = ap.parse_args()
    pack = json.loads((F.pack_dir(a.pack) / "pack.json").read_text())
    title, text = F.draft_text(a.draft)
    url = "https://dealectric.com" + a.url
    res = [dict(r) for r in pack["results"] if "dealectric.com" not in r["url"]]
    res.insert(a.rank - 1, {"url": url, "title": title, "text": text, "source": f"draft {a.draft}"})
    res = res[: max(len(pack["results"]), a.rank)]
    ctx = F.build_context(res, pack["query"])
    our_rank = next((i + 1 for i, r in enumerate(ctx) if "dealectric.com" in r["url"]), None)
    results = "\n\n".join(f"[{i + 1}] {r['title']}\nURL: {r['url']}\n{r['shown']}" for i, r in enumerate(ctx))
    user = f"Shopper: {pack['question']}\n\nYour web search: {pack['query']}\n\nResults:\n\n{results}"
    out = F.pack_dir(a.pack) / "claude" / a.tag
    out.mkdir(parents=True, exist_ok=True)

    def one(n):
        f = out / f"{n}.json"
        if f.exists():
            return json.loads(f.read_text())
        started = E.now_iso()
        try:
            ans = (E.claude_cli_json(SYSTEM, user, a.model, SCHEMA, timeout=600) or {}).get("answer", "")
            err = None
        except Exception as e:   # noqa: BLE001
            ans, err = "", str(e)[:300]
        E.footprint("claude-cli", started, E.now_iso(), prompt=pack["question"], script="claudecheck.py", run_id=a.tag,
                    retrieved=[{"url": r["url"]} for r in ctx], error=err)
        rec = {"n": n, "model": a.model, "text": ans, "error": err, **F.tier(ans, our_rank), "our_rank": our_rank,
               "flags": [m.group(0) for m in FLAG.finditer(ans)]}
        E.write_json(f, rec)
        return rec

    with cf.ThreadPoolExecutor(3) as ex:
        recs = list(ex.map(one, range(1, a.reps + 1)))
    for r in recs:
        print(f"{a.tag} #{r['n']} T{r['tier']} go={r.get('go')} flags={r['flags']} err={r['error']} | {r['text'][:110]!r}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
