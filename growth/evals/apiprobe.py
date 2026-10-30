#!/usr/bin/env python3.12
"""Does the OpenAI API's web_search tool hand the model what the ChatGPT app's search does? (DLC-77, 2026-10-30)

    python3.12 growth/evals/apiprobe.py [--models gpt-6.1-sol] [--sizes low,medium,high]

Re-asks the app probes of growth/focus/context-probe.md through the Responses API, word for word:
- needles (N*): one pinned search, then a fact deep in a result page; the app's model answered all four from the search
  payload alone, so an API model that gets the same payload answers them too, without an open_page action;
- echoes (d024441, e02): quote every result's excerpt; checked for the AC200L page's stored (10-26) vs live version.
Writes growth/evals/runs/<date>-apiprobe/<model>--<size>--<probe>.json and prints one line per call.
"""
from __future__ import annotations

import argparse, concurrent.futures as cf, json, re, sys, time, urllib.error, urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402

APP = E.RUNS_DIR / "2026-10-30-ctxprobe" / "ctx"
OUT = E.RUNS_DIR / f"{E.today()}-apiprobe"
# app probe tag -> values the app's answer gave (all verbatim from the stored page)
NEEDLES = {"N032039": ["437", "12"], "N032217": ["57.99", "522"], "N032434": ["57.6", "55"], "N032612": ["4.85", "20.6"]}
ECHOES = ["d024441", "e02"]
# AC200L lines only the stored 10-26 version has, and only the live page has
AC_STORED = ["Tested in BLUETTI's cart on 2026-10-21"]
AC_LIVE_TITLE = "$854.05 with code AFF5OFF"


def post(body: dict, key: str) -> tuple[int, dict]:
    req = urllib.request.Request("https://api.openai.com/v1/responses", data=json.dumps(body).encode(),
                                 headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"})
    import ssl
    try:
        import certifi
        ctx = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        ctx = ssl.create_default_context()
    try:
        with urllib.request.urlopen(req, context=ctx, timeout=300) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, json.loads(e.read() or b"{}")


def one(model: str, size: str, tag: str, key: str) -> dict:
    prompt = json.loads((APP / f"{tag}.json").read_text())["prompt"]
    body = {"model": model, "input": prompt, "store": False,
            "tools": [{"type": "web_search", "search_context_size": size, "user_location": {"type": "approximate", "country": "US"}}],
            "include": ["web_search_call.action.sources"]}
    t0, started = time.time(), E.now_iso()
    status, r = post(body, key)
    actions, sources, text = [], [], []
    for it in r.get("output", []) if status == 200 else []:
        if it.get("type") == "web_search_call":
            a = it.get("action") or {}
            actions.append({"type": a.get("type"), "query": a.get("query"), "url": a.get("url")})
            sources += [s.get("url") for s in a.get("sources") or []]
        elif it.get("type") == "message":
            text += [c.get("text", "") for c in it.get("content", []) if c.get("type") == "output_text"]
    answer = "\n".join(text)
    rec = {"model": model, "size": size, "probe": tag, "prompt": prompt, "status": status, "error": r.get("error"),
           "answer": answer, "actions": actions, "sources": sources, "usage": r.get("usage"), "latency_s": round(time.time() - t0, 1),
           "started_at": started}
    if tag in NEEDLES:
        rec["needle_hit"] = all(v in answer for v in NEEDLES[tag])
        rec["not_in_results"] = "NOT IN RESULTS" in answer.upper()
    else:
        rec["ac200l_stored"] = any(s in answer for s in AC_STORED)
        rec["ac200l_live"] = AC_LIVE_TITLE in answer
        rec["dealectric_in_sources"] = any("dealectric.com" in (s or "") for s in sources)
        rec["echo_chars"] = len(answer)
    OUT.mkdir(parents=True, exist_ok=True)
    E.write_json(OUT / f"{model}--{size}--{tag}.json", rec)
    E.footprint("openai-api", started, E.now_iso(), prompt=prompt, run_id=OUT.name, prompt_id=f"{model}--{size}--{tag}",
                script="apiprobe.py", retrieved=[{"url": s} for s in sources], error=str(r.get("error")) if status != 200 else None)
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--models", default="gpt-6.1-sol")
    ap.add_argument("--sizes", default="low,medium,high")
    ap.add_argument("--probes", default=",".join(list(NEEDLES) + ECHOES))
    a = ap.parse_args()
    key = E.env_key("OPENAI_API_KEY")
    jobs = [(m, s, p) for m in a.models.split(",") for s in a.sizes.split(",") for p in a.probes.split(",")]
    with cf.ThreadPoolExecutor(4) as ex:
        for rec in ex.map(lambda j: one(*j, key), jobs):
            acts = ",".join(x["type"] or "?" for x in rec["actions"])
            u = rec.get("usage") or {}
            res = (f"needle {'HIT' if rec['needle_hit'] else ('NOT_IN' if rec['not_in_results'] else 'miss')}" if "needle_hit" in rec
                   else f"echo {rec['echo_chars']}ch ours={rec['dealectric_in_sources']} stored={rec['ac200l_stored']} live={rec['ac200l_live']}")
            print(f"{rec['model']:14} {rec['size']:6} {rec['probe']:8} {rec['status']} {res:40} actions={acts} "
                  f"in={u.get('input_tokens')} out={u.get('output_tokens')} | {rec['answer'][:110]!r}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
