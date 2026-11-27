#!/usr/bin/env python3.12
"""The choices ChatGPT offers shoppers in a cluster (page flow, DLC-369; Barry 2026-11-27: "ChatGPT's multiple choice
questions show you the specs to target").

    python3.12 tools/pageflow/ask.py run <cluster> [--n 2]    # plain chats on the cluster's broad prompts, then extract
    python3.12 tools/pageflow/ask.py extract <cluster>        # re-read the saved chats only
    python3.12 tools/pageflow/ask.py show <cluster>

A broad question ("which <product> should I buy") makes ChatGPT split the category the way it thinks shoppers differ:
it asks back ("phone only, or a laptop too?") and it sorts its picks by a few figures ("30 W for a phone, 65 W with PPS
for a light laptop"). Those questions, their options and those figures are read from the saved chats by a model with
no tools and written to growth/pageflow/options/<cluster>.json, which the map builder gets as an input.

The chats go through growth/evals/visibility_scan.py (Agent Chrome, plain temporary chats, one at a time, logged in the
footprint log by that script). Three prompts x n chats per cluster and refresh: a few minutes and 6 chats of the quota.
"""
from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

EVAL_RUNS = C.ROOT / "growth/evals/runs"


def run_id(cid: str, day: str | None = None) -> str:
    return f"{day or C.today()}-pageflow-ask-{cid}"


def questions(cid: str) -> Path:
    c = C.clusters()[cid]
    qs = [{"qid": f"ask-{cid}-{i}--plain", "slug": f"ask-{cid}-{i}", "cluster": c["name"], "ptype": "ask", "level": "G0", "type": "ask",
           "mode": "natural", "search": "False", "prompt": p} for i, p in enumerate(c["seeds"], 1)]
    path = C.OPTIONS / f"{cid}-questions.json"
    C.jsave(path, {"version": 1, "note": f"page flow: broad {c['name']} prompts, to read the choices ChatGPT offers back", "questions": qs})
    return path


def chats(cid: str) -> tuple[str, list[dict]]:
    """The newest ask run for the cluster that has chats, and its chats."""
    for d in sorted(EVAL_RUNS.glob(f"*-pageflow-ask-{cid}"), reverse=True):
        out = []
        for f in sorted((d / "chatgpt").glob("*.json")):
            c = C.jload(f)
            if c and c.get("text") and (c.get("answer_model") or "").startswith("gpt-") and not (c.get("answer_model") or "").endswith("mini"):
                out.append(c)
        if out:
            return d.name, out
    return "", []


def extract(cid: str) -> dict:
    import abpage as A
    rid, cs = chats(cid)
    if not cs:
        return {"status": "error", "reason": "no saved chats for this cluster"}
    c = C.clusters()[cid]
    body = "\n\n".join(f"### Chat {i} | shopper typed: {ch['prompt']} | ChatGPT searched: {' | '.join(ch.get('queries') or [])}\n{ch['text'][:7000]}"
                       for i, ch in enumerate(cs, 1))
    prompt = f"""Below are {len(cs)} answers ChatGPT gave to broad shopper questions about {c['name']}. Read how it divides the category.
Report only what the answers themselves say; do not add your own knowledge.

1. choices: every question it asked the shopper back, or decision it told the shopper to make first, with the options it
   offered or implied, in its words ("phone only" / "phone and a light laptop" / "a laptop that needs 100 W"). Merge the
   same question across chats and count the chats it appeared in.
2. split_by: the figures or features by which it sorted its picks, each with the values it used and what each value was
   for ("output watts: 30 W phone, 65 W light laptop, 100 W+ larger laptop").
3. picks: the products it recommended, each with the split it was the pick for.
4. searched: the words it searched with, as given.

{body}

Your whole reply is ONE JSON object:
{{"choices": [{{"question": "", "options": ["", ""], "chats": 0}}],
 "split_by": ["<figure: value (what for), value (what for)>"],
 "picks": [{{"product": "", "for": ""}}],
 "searched": [""]}}"""
    out = A.claude(prompt, tools=False, timeout=900)
    if out.get("status") == "error" or "choices" not in out:
        return {"status": "error", "reason": out.get("reason") or "no choices in the reply"}
    out.pop("_meta", None)
    out.update(cluster=cid, read=C.today(), run=rid, chats=len(cs), prompts=sorted({ch["prompt"] for ch in cs}))
    C.jsave(C.OPTIONS / f"{cid}.json", out)
    return out


def run(cid: str, n: int = 2) -> dict:
    q = questions(cid)
    r = subprocess.run(["python3.12", str(C.ROOT / "growth/evals/visibility_scan.py"), "--questions", str(q), "--run-id", run_id(cid), "--n", str(n)],
                       cwd=C.ROOT, capture_output=True, text=True)
    if r.returncode:
        print("scan exit", r.returncode, (r.stdout or r.stderr)[-400:])
    return extract(cid)


def main() -> int:
    cmd, cid = (sys.argv + ["", ""])[1:3]
    if cid not in C.clusters():
        print("clusters:", ", ".join(C.clusters()))
        return 1
    if cmd == "run":
        n = int(sys.argv[sys.argv.index("--n") + 1]) if "--n" in sys.argv else 2
        out = run(cid, n)
    elif cmd == "extract":
        out = extract(cid)
    else:
        out = C.jload(C.OPTIONS / f"{cid}.json") or {"status": "error", "reason": "not read yet"}
    if out.get("status") == "error":
        print("ask failed:", out["reason"])
        return 2
    print(f"{cid}: {out['chats']} chats ({out['run']})")
    for ch in out["choices"]:
        print(f"- {ch['question']} -> {' | '.join(ch['options'])}  ({ch['chats']} chats)")
    for s in out.get("split_by", []):
        print("  split:", s)
    return 0


if __name__ == "__main__":
    sys.exit(main())
