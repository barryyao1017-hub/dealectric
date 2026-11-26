#!/usr/bin/env python3.12
"""Open-query discovery (Barry, 2026-11-14): ask candidate shopper questions in the ChatGPT app before any page
exists, and read from the answer whether the query is open to us.

    python3.12 growth/evals/openscan.py run   [--run-id 2026-11-14-openq] [--pace 10]
    python3.12 growth/evals/openscan.py score [--run-id ...]      # re-read saved answers -> readings.json

Queue: growth/focus/open-queries/queue.jsonl, one JSON object per line {qid, prompt, group, shape, source, ...}. The
runner re-reads it before every chat, so candidates can be appended while it runs; when the queue is empty it waits
up to --idle seconds for more and then exits.

Each question is asked once, plain, in a temporary chat (Agent Chrome on 9222, ui.ask_chatgpt). Search is NOT forced
(no hints=search): whether ChatGPT searches at all is part of the reading, since a question it answers from memory
cannot be won by a page. Every chat keeps its full-length screenshot and is logged to the footprint log.

Readings per answer (the gate from the 11-14 top/bottom analysis, growth/focus/top-bottom/):
  searched      ChatGPT ran a web search
  rows          product rows in the answer; `carded` = rows bound to an OpenAI catalog record (Entity ref=turnNproductK),
                `typed` = rows ChatGPT wrote itself (Entity value="...", no ref)
  cited         domains of the web results the answer cites (Cite refs -> response.search_results)
  results       the first 12 result domains
  ours          our rank in the results and whether the answer cites or links us (visibility_scan.score)

It stops when the account is throttled twice or an answer comes from a model other than --model (the plan's quota).
"""
from __future__ import annotations

import argparse, json, re, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ui  # noqa: E402
import evallib as E  # noqa: E402
import visibility_scan as VS  # noqa: E402

ROOT = E.EVALS_DIR.parent.parent
QUEUE = ROOT / "growth" / "focus" / "open-queries" / "queue.jsonl"


def markup_of(rec: dict) -> str:
    m = (rec.get("response") or {}).get("markup") or [""]
    return max(m, key=len) if isinstance(m, list) else (m or "")


def reading(rec: dict) -> dict:
    m = markup_of(rec)
    carded, typed = set(), []
    for e in re.findall(r"<Entity\b([^>]*)/?>", m):
        if 'category="product"' not in e:
            continue
        r = re.search(r'ref="(\w+)"', e)
        if r:
            carded.add(r.group(1))
        else:
            v = re.search(r'value="([^"]+)"', e)
            if v and v.group(1) not in typed:
                typed.append(v.group(1))
    res = (rec.get("response") or {}).get("search_results") or []
    idx = sorted({int(i) for i in re.findall(r"turn\d+search(\d+)", m)})
    cited = [res[i]["domain"].removeprefix("www.") for i in idx if i < len(res)]
    links = [{"title": c.get("title"), "url": (c.get("url") or "").split("?")[0]} for c in rec.get("citations") or []]
    return {"searched": bool(rec.get("queries")), "queries": rec.get("queries") or [], "n_results": len(res),
            "carded": len(carded), "typed": len(typed), "typed_names": typed, "cited": cited,
            "results": [r["domain"].removeprefix("www.") for r in res[:12]],
            "result_titles": [(r.get("title") or "")[:110] for r in res[:12]],
            "links": links[:12], "answer_chars": len(rec.get("text") or "")}


def queue() -> list[dict]:
    global QUEUE
    if not QUEUE.exists():
        return []
    out, seen = [], set()
    for l in QUEUE.read_text().splitlines():
        if l.strip():
            q = json.loads(l)
            if q["qid"] not in seen:
                seen.add(q["qid"])
                out.append(q)
    return out


def log(path: Path, row: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False, default=str) + "\n")


def run(args) -> int:
    out = E.RUNS_DIR / args.run_id
    (out / "chatgpt").mkdir(parents=True, exist_ok=True)
    scan, events = out / "scan.jsonl", out / "events.jsonl"
    done = {json.loads(l)["qid"] for l in scan.read_text().splitlines()} if scan.exists() else set()
    log(events, {"at": E.now_iso(), "event": "start", "done": len(done), "pace_s": args.pace, "model": args.model})
    throttles, idle_since, n_ok = 0, None, 0
    while True:
        todo = [q for q in queue() if q["qid"] not in done]
        if not todo:
            idle_since = idle_since or time.time()
            if time.time() - idle_since > args.idle:
                log(events, {"at": E.now_iso(), "event": "queue_empty", "ok": n_ok})
                return 0
            time.sleep(20)
            continue
        idle_since = None
        q = todo[0]
        shot = out / "chatgpt" / f"{q['qid']}.jpg"
        started = E.now_iso()
        try:
            rec = ui.ask_chatgpt(q["prompt"], shot, fp={"run_id": args.run_id, "prompt_id": q["qid"], "script": "openscan.py"},
                                 search=False)
        except ui.Throttled as t:
            throttles += 1
            log(events, {"at": E.now_iso(), "event": "throttled", "after_ok": n_ok, "qid": q["qid"], "wait_s": t.wait_s, "notice": str(t)[:200]})
            if throttles >= 2:
                log(events, {"at": E.now_iso(), "event": "stop", "why": "throttled twice", "ok": n_ok})
                return 3
            time.sleep(min(t.wait_s, 1800) + 30)
            continue
        except Exception as e:  # noqa: BLE001
            q["_errors"] = q.get("_errors", 0)
            log(events, {"at": E.now_iso(), "event": "error", "qid": q["qid"], "error": f"{type(e).__name__}: {e}"[:300]})
            errs = sum(1 for l in events.read_text().splitlines() if f'"qid": "{q["qid"]}"' in l and '"event": "error"' in l)
            if errs >= 2:      # skip a question that fails twice
                done.add(q["qid"])
                log(scan, {"qid": q["qid"], "prompt": q["prompt"], "failed": True})
            time.sleep(45)
            continue
        if not (rec.get("account") or "").startswith("signed in"):
            log(events, {"at": E.now_iso(), "event": "not_signed_in", "account": rec.get("account")})
            return 2
        model = rec.get("answer_model") or ((rec.get("models") or [None])[-1])
        rec.update(qid=q["qid"], slug=q.get("slug", ""), prompt=q["prompt"], started_at=started, finished_at=E.now_iso(),
                   run_id=args.run_id, downgraded=model != args.model, queue=q)
        (out / "chatgpt" / f"{q['qid']}.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False, default=str))
        if model != args.model:
            log(events, {"at": E.now_iso(), "event": "downgraded", "after_ok": n_ok, "qid": q["qid"], "models": rec.get("models")})
            log(events, {"at": E.now_iso(), "event": "stop", "why": f"answer from {model}", "ok": n_ok})
            return 3
        s = VS.score(rec, {"code": None})
        row = {"qid": q["qid"], "prompt": q["prompt"], "group": q.get("group"), "shape": q.get("shape"), "source": q.get("source"),
               "started_at": started, "latency_s": rec.get("latency_s"), "answer_model": model,
               "tier": s["tier"], "our_rank": s["our_rank"], "our_pages": s["pages"], "go": s["go"], **reading(rec)}
        log(scan, row)
        done.add(q["qid"])
        n_ok += 1
        print(f"{n_ok} {q['qid']} searched={row['searched']} rows carded={row['carded']} typed={row['typed']} "
              f"cited={row['cited'][:4]} ours=T{s['tier']}", flush=True)
        time.sleep(args.pace)


def score(args) -> int:
    out = E.RUNS_DIR / args.run_id
    rows = []
    for f in sorted((out / "chatgpt").glob("*.json")):
        rec = json.loads(f.read_text())
        s = VS.score(rec, {"code": None})
        q = rec.get("queue") or {}
        rows.append({"qid": rec["qid"], "prompt": rec["prompt"], "group": q.get("group"), "shape": q.get("shape"),
                     "source": q.get("source"), "answer_model": rec.get("answer_model"), "tier": s["tier"],
                     "our_rank": s["our_rank"], "our_pages": s["pages"], "go": s["go"], **reading(rec)})
    (out / "readings.json").write_text(json.dumps(rows, indent=1, ensure_ascii=False))
    print(len(rows), "answers ->", out / "readings.json")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["run", "score"])
    ap.add_argument("--run-id", default="2026-11-14-openq")
    ap.add_argument("--pace", type=float, default=10)
    ap.add_argument("--idle", type=float, default=1800, help="seconds to wait for new queue lines before exiting")
    ap.add_argument("--model", default="gpt-6")
    ap.add_argument("--queue", help="queue file (default growth/focus/open-queries/queue.jsonl)")
    args = ap.parse_args()
    if args.queue:
        global QUEUE
        QUEUE = Path(args.queue)
    return run(args) if args.cmd == "run" else score(args)


if __name__ == "__main__":
    sys.exit(main())
