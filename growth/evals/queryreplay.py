#!/usr/bin/env python3.12
"""Replay the ChatGPT app's own search query through the API and compare result lists (DLC-77, 2026-10-30).

    python3.12 growth/evals/queryreplay.py api [--reps 3] [--model gpt-6-luna]   # replay every captured app query
    python3.12 growth/evals/queryreplay.py report                                # overlap tables

App chats: every saved raw-stream chat (runs/2026-10-30-cardprobe/app, runs/2026-10-30-ctxprobe/ctx) whose answer ran
exactly one search. For each, the API gets the same query verbatim in a prompt that allows one search and nothing
else (`max_tool_calls: 1`), and its `web_search_call.action.sources` are compared with the app's search results
(`search_result_groups`, all ref types). URLs are compared without tracking parameters, scheme, `www.` and trailing
slash. Output: runs/2026-10-30-queryreplay/<app-tag>--<rep>.json.
"""
from __future__ import annotations

import argparse, concurrent.futures as cf, json, re, statistics, sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import apiprobe as A  # noqa: E402
import cardprobe as K  # noqa: E402

APP_DIRS = [E.RUNS_DIR / "2026-10-30-cardprobe" / "app", E.RUNS_DIR / "2026-10-30-ctxprobe" / "ctx",
            E.RUNS_DIR / "2026-10-30-cardprobe" / "details"]
OUT = E.RUNS_DIR / "2026-10-30-queryreplay"
PROMPT = ('Run exactly one web search with this exact query, word for word: "{q}". Do not search again and do not '
          'open any page. Then reply only with the word DONE.')


def norm(u: str) -> str:
    u = E.strip_tracking(u or "").lower()
    u = re.sub(r"^https?://(www\.)?", "", u)
    return u.split("#")[0].rstrip("/")


def app_chats() -> list[dict]:
    out = []
    for d in APP_DIRS:
        for f in sorted(d.glob("*.json")):
            r = json.loads(f.read_text())
            if not r.get("sse"):
                continue
            x = K.decompose(r["sse"])
            # first turn only (echo follow-ups run their own searches)
            if len(x["queries"]) != 1 or not x["results"]:
                continue
            out.append({"tag": f"{d.name}-{f.stem}", "query": x["queries"][0], "results": [norm(e["url"]) for e in x["results"]],
                        "types": [e["type"] for e in x["results"]], "started_at": r.get("started_at")})
    return out


def run_api(reps: int, model: str) -> None:
    key = E.env_key("OPENAI_API_KEY")
    OUT.mkdir(parents=True, exist_ok=True)

    def one(job):
        c, rep = job
        p = OUT / f"{c['tag']}--{rep}.json"
        if p.exists():
            return None
        prompt = PROMPT.format(q=c["query"])
        started = E.now_iso()
        status, resp = A.post({"model": model, "input": prompt, "store": False, "max_tool_calls": 1,
                               "tools": [{"type": "web_search", "user_location": {"type": "approximate", "country": "US"}}],
                               "include": ["web_search_call.action.sources"]}, key)
        calls = [it for it in resp.get("output", []) if it.get("type") == "web_search_call"] if status == 200 else []
        acts = [(it.get("action") or {}) for it in calls]
        rec = {"app_tag": c["tag"], "rep": rep, "model": model, "status": status, "error": resp.get("error"),
               "app_query": c["query"], "api_queries": [a.get("query") for a in acts], "n_calls": len(calls),
               "sources": [norm(s.get("url")) for a in acts for s in a.get("sources") or []], "usage": resp.get("usage"),
               "started_at": started}
        E.write_json(p, rec)
        E.footprint("openai-api", started, E.now_iso(), prompt=prompt, run_id=OUT.name, prompt_id=p.stem, script="queryreplay.py",
                    retrieved=[{"url": s} for s in rec["sources"]], error=str(resp.get("error")) if status != 200 else None)
        return rec

    jobs = [(c, r) for c in app_chats() for r in range(1, reps + 1)]
    with cf.ThreadPoolExecutor(3) as ex:
        for rec in ex.map(one, jobs):
            if rec:
                print(f"{rec['app_tag'][:60]:60} {rec['rep']} {rec['status']} calls={rec['n_calls']} same_q={rec['api_queries'] == [rec['app_query']]} "
                      f"src={len(rec['sources'])}", flush=True)


def report() -> str:
    chats = {c["tag"]: c for c in app_chats()}
    rows, stats = [], {"recall": [], "jacc": [], "api_self": [], "top5": []}
    for tag, c in chats.items():
        reps = [json.loads(p.read_text()) for p in sorted(OUT.glob(f"{tag}--*.json"))]
        reps = [r for r in reps if r["status"] == 200 and r["n_calls"] == 1]
        if not reps:
            continue
        app = list(dict.fromkeys(c["results"]))
        A_ = set(app)
        rec_, jac = [], []
        for r in reps:
            S = set(r["sources"])
            rec_.append(len(A_ & S) / len(A_))
            jac.append(len(A_ & S) / len(A_ | S) if A_ | S else 0)
        top5 = sum(u in set().union(*[set(r["sources"]) for r in reps]) for u in app[:5]) / min(5, len(app))
        selfs = []
        for i in range(len(reps)):
            for j in range(i + 1, len(reps)):
                X, Y = set(reps[i]["sources"]), set(reps[j]["sources"])
                selfs.append(len(X & Y) / len(X | Y) if X | Y else 1)
        ours_app = sorted({u.split("dealectric.com")[1] or "/" for u in app if "dealectric.com" in u})
        ours_api = sorted({u.split("dealectric.com")[1] or "/" for r in reps for u in r["sources"] if "dealectric.com" in u})
        stats["recall"] += rec_; stats["jacc"] += jac; stats["top5"].append(top5); stats["api_self"] += selfs
        rows.append(f"| {tag[:58]} | {c['query'][:60]} | {len(app)} | {statistics.mean(len(r['sources']) for r in reps):.0f} | "
                    f"{statistics.mean(rec_):.0%} | {top5:.0%} | {statistics.mean(jac):.0%} | {statistics.mean(selfs):.0%} | "
                    f"{', '.join(ours_app) or '-'} | {', '.join(ours_api) or '-'} |" if selfs else "")
    head = ["| app chat | app query | app results | API sources (mean) | app results the API also got | app top 5 in any API rep | overlap (Jaccard) | API vs itself (Jaccard) | our pages, app | our pages, API (any rep) |",
            "|---|---|---|---|---|---|---|---|---|---|"]
    summ = (f"\n{len(rows)} queries. Mean share of the app's results the API also returned: {statistics.mean(stats['recall']):.0%}; "
            f"app top-5 found in any API rep: {statistics.mean(stats['top5']):.0%}; Jaccard app vs API {statistics.mean(stats['jacc']):.0%}; "
            f"API vs itself {statistics.mean(stats['api_self']):.0%}.")
    # app vs app: chats that ran the identical query
    byq = {}
    for c in chats.values():
        byq.setdefault(c["query"], []).append(c)
    aa = []
    for q, cs in byq.items():
        for i in range(len(cs)):
            for j in range(i + 1, len(cs)):
                X, Y = set(cs[i]["results"]), set(cs[j]["results"])
                rec = len(X & Y) / len(X)
                aa.append((q, cs[i]["tag"], cs[j]["tag"], len(X & Y) / len(X | Y), rec))
    if aa:
        summ += (f"\nApp vs app on the identical query ({len(aa)} pairs): Jaccard {statistics.mean(x[3] for x in aa):.0%}, "
                 f"share of one chat's results in the other {statistics.mean(x[4] for x in aa):.0%}.\n"
                 + "\n".join(f"- {q[:70]} | {a} vs {b}: Jaccard {j:.0%}" for q, a, b, j, _ in aa))
    return "\n".join(head + [r for r in rows if r]) + summ


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["api", "report", "list"])
    ap.add_argument("--reps", type=int, default=3)
    ap.add_argument("--model", default="gpt-6-luna")
    a = ap.parse_args()
    if a.cmd == "list":
        for c in app_chats():
            print(c["tag"], "|", c["query"], "|", len(c["results"]))
    elif a.cmd == "api":
        run_api(a.reps, a.model)
    else:
        print(report())
    return 0


if __name__ == "__main__":
    sys.exit(main())
