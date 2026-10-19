#!/usr/bin/env python3.12
"""Ask the eval questions to four assistants over their APIs with web search on, and save every raw response.

    python3.12 growth/evals/run.py                      # all assistants with a key, all tiers, 3 runs per cell
    python3.12 growth/evals/run.py --assistants anthropic --tiers B,C --n 1 --questions Q01,Q22
    python3.12 growth/evals/run.py --mock               # no API calls; synthetic answers to exercise grade/report

Output: growth/evals/runs/<run-id>/<assistant>/<qid>-<tier>-<n>.json plus manifest.json.
Keys come from the environment (OPENAI_API_KEY, ANTHROPIC_API_KEY, GEMINI_API_KEY, XAI_API_KEY);
an assistant whose key is missing is skipped and reported, never fatal.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import random
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402

# ------------------------------------------------------------------ models (override with env vars)
DEFAULT_MODELS = {
    "openai": "gpt-6.1-sol",          # OPENAI_MODEL; web_search tool in the Responses API
    "anthropic": "claude-opus-5-5",   # ANTHROPIC_MODEL; web_search + web_fetch server tools
    "gemini": "gemini-4-argon",       # GEMINI_MODEL; google_search grounding
    "xai": "grok-4.7",                # XAI_MODEL; web_search tool in the Responses API
}
KEY_ENV = {
    "openai": ("OPENAI_API_KEY",),
    "anthropic": ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN"),
    "gemini": ("GEMINI_API_KEY", "GOOGLE_API_KEY"),
    "xai": ("XAI_API_KEY",),
}
US_LOCATION = {"type": "approximate", "country": "US", "timezone": "America/New_York"}
HTTP_TIMEOUT = 600
MAX_PAUSE_CONTINUATIONS = 5

_print_lock = threading.Lock()


def log(msg: str) -> None:
    with _print_lock:
        print(msg, flush=True)


# ------------------------------------------------------------------ HTTP helper (OpenAI, Gemini, xAI)

def post_json(url: str, body: dict, headers: dict, retries: int = 3) -> dict:
    data = json.dumps(body).encode()
    hdrs = {"Content-Type": "application/json", "User-Agent": "dealectric-eval/1.0", **headers}
    last = None
    for attempt in range(retries + 1):
        req = urllib.request.Request(url, data=data, headers=hdrs, method="POST")
        try:
            with urllib.request.urlopen(req, timeout=HTTP_TIMEOUT) as r:
                return json.loads(r.read().decode())
        except urllib.error.HTTPError as e:
            txt = e.read().decode(errors="replace")[:2000]
            last = RuntimeError(f"HTTP {e.code}: {txt}")
            if e.code in (408, 409, 429) or e.code >= 500:
                time.sleep(min(60, 2 ** attempt * 3 + random.random()))
                continue
            raise last
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = RuntimeError(f"network: {e}")
            time.sleep(min(60, 2 ** attempt * 3))
    raise last  # type: ignore[misc]


def redirect_target(url: str) -> str | None:
    """One hop of a redirect without following it (Gemini grounding URIs are vertexaisearch redirects).
    Never follows into the target, so no click is logged on dealectric.com/go/."""
    class NoRedirect(urllib.request.HTTPRedirectHandler):
        def redirect_request(self, req, fp, code, msg, headers, newurl):  # noqa: D102
            return None
    opener = urllib.request.build_opener(NoRedirect)
    req = urllib.request.Request(url, method="HEAD", headers={"User-Agent": "dealectric-eval/1.0"})
    try:
        with opener.open(req, timeout=30) as r:
            return r.headers.get("Location")
    except urllib.error.HTTPError as e:
        return e.headers.get("Location")
    except Exception:
        return None


# ------------------------------------------------------------------ per-assistant callers
# Each returns {"model", "request", "response", "text", "citations": [{url,title,source}], "consulted": [...],
#              "queries": [...], "stop_reason", "usage", "notes"}.
#   citations = URLs the shopper would see (inline citations, links in the answer text)
#   consulted = URLs the assistant looked at but did not necessarily show (search results, fetches, sources)

def call_openai(prompt: str, system: str, key: str, model: str) -> dict:
    body = {
        "model": model,
        "instructions": system,
        "input": prompt,
        "tools": [{"type": "web_search", "user_location": US_LOCATION, "search_context_size": "medium"}],
        "include": ["web_search_call.action.sources"],
        "store": False,
    }
    resp = post_json("https://api.openai.com/v1/responses", body, {"Authorization": f"Bearer {key}"})
    text, cites, consulted, queries, raw = [], [], [], [], []
    for item in resp.get("output", []):
        t = item.get("type")
        if t == "web_search_call":
            act = item.get("action") or {}
            for q in act.get("queries") or ([act["query"]] if act.get("query") else []):
                queries.append(q)
            if act.get("url"):
                consulted.append({"url": act["url"], "title": "", "source": "open_page"})
            for s in act.get("sources") or []:
                consulted.append({"url": s.get("url"), "title": s.get("title", ""), "source": "source"})
        elif t == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    text.append(c.get("text", ""))
                    for a in c.get("annotations", []) or []:
                        raw.append(a)
                        if a.get("type") == "url_citation":
                            cites.append({"url": a.get("url"), "title": a.get("title", ""), "source": "citation"})
    return {"model": model, "request": body, "response": resp, "text": "\n".join(text), "citations": cites,
            "raw_citations": raw, "consulted": consulted, "queries": queries, "stop_reason": resp.get("status"),
            "usage": resp.get("usage"), "notes": []}


def _walk(obj, fn):
    if isinstance(obj, dict):
        fn(obj)
        for v in obj.values():
            _walk(v, fn)
    elif isinstance(obj, list):
        for v in obj:
            _walk(v, fn)


def call_anthropic(prompt: str, system: str, key: str, model: str) -> dict:
    import anthropic  # official SDK; picks up ANTHROPIC_API_KEY or an `ant auth login` profile

    client = anthropic.Anthropic(timeout=HTTP_TIMEOUT, max_retries=3)
    tools = [
        {"type": "web_search_20260209", "name": "web_search", "max_uses": 8, "user_location": US_LOCATION},
        {"type": "web_fetch_20260209", "name": "web_fetch", "max_uses": 8, "max_content_tokens": 60000},
    ]
    messages = [{"role": "user", "content": prompt}]
    request = {"model": model, "max_tokens": 16000, "system": system, "tools": tools, "messages": list(messages),
               "thinking": {"type": "adaptive"}, "output_config": {"effort": "medium"}}
    turns, notes = [], []
    for _ in range(MAX_PAUSE_CONTINUATIONS + 1):
        resp = client.messages.create(**request)
        d = resp.model_dump()
        turns.append(d)
        if resp.stop_reason == "pause_turn":
            notes.append("pause_turn continued")
            request["messages"] = request["messages"] + [{"role": "assistant", "content": d["content"]}]
            continue
        break
    text, cites, consulted, queries, raw = [], [], [], [], []
    seen = set()

    def visit(b):
        t = b.get("type")
        if t == "text" and "text" in b and b.get("citations") is not None:
            for c in b["citations"] or []:
                raw.append(c)
                if c.get("url"):
                    cites.append({"url": c["url"], "title": c.get("title", ""), "source": "citation"})
        elif t == "web_search_result" and b.get("url"):
            consulted.append({"url": b["url"], "title": b.get("title", ""), "source": "search_result"})
        elif t == "web_fetch_result" and b.get("url"):
            consulted.append({"url": b["url"], "title": (b.get("content") or {}).get("title", ""), "source": "fetch"})
        elif t == "server_tool_use":
            inp = b.get("input") or {}
            if b.get("name") == "web_search" and inp.get("query"):
                queries.append(inp["query"])
            if b.get("name") == "web_fetch" and inp.get("url"):
                consulted.append({"url": inp["url"], "title": "", "source": "fetch_request"})

    final = turns[-1]
    for b in final.get("content", []):
        if b.get("type") == "text":
            text.append(b.get("text", ""))
    for d in turns:
        _walk(d.get("content", []), visit)
    # de-duplicate consulted entries
    consulted = [c for c in consulted if not (c["url"] in seen or seen.add(c["url"]))]
    if final.get("stop_reason") == "refusal":
        notes.append(f"refusal: {final.get('stop_details')}")
    return {"model": model, "request": {k: v for k, v in request.items() if k != "messages"} | {"messages": messages},
            "response": turns if len(turns) > 1 else final, "text": "\n".join(text), "citations": cites,
            "raw_citations": raw, "consulted": consulted, "queries": queries, "stop_reason": final.get("stop_reason"),
            "usage": final.get("usage"), "notes": notes}


_redirect_cache: dict[str, str | None] = {}


def _resolve_grounding(uri: str) -> str | None:
    if "grounding-api-redirect" not in (uri or ""):
        return None
    if uri not in _redirect_cache:
        _redirect_cache[uri] = redirect_target(uri)
    return _redirect_cache[uri]


def call_gemini(prompt: str, system: str, key: str, model: str) -> dict:
    api = E.env_key("GEMINI_API") or "generate"
    if api == "interactions":
        return _call_gemini_interactions(prompt, system, key, model)
    body = {
        "system_instruction": {"parts": [{"text": system}]},
        "contents": [{"role": "user", "parts": [{"text": prompt}]}],
        "tools": [{"google_search": {}}],
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
    resp = post_json(url, body, {"x-goog-api-key": key})
    text, cites, consulted, queries, notes = [], [], [], [], []
    cand = (resp.get("candidates") or [{}])[0]
    for part in (cand.get("content") or {}).get("parts", []):
        if "text" in part:
            text.append(part["text"])
    gm = cand.get("groundingMetadata") or {}
    queries = list(gm.get("webSearchQueries") or [])
    chunks = gm.get("groundingChunks") or []
    supported = set()
    for s in gm.get("groundingSupports") or []:
        supported.update(s.get("groundingChunkIndices") or [])
    for i, ch in enumerate(chunks):
        w = ch.get("web") or {}
        uri = w.get("uri")
        if not uri:
            continue
        resolved = _resolve_grounding(uri)
        entry = {"url": resolved or uri, "title": w.get("title", ""), "source": "grounding_chunk",
                 "redirect": uri if resolved else None}
        # Chunks attached to a groundingSupport are the ones the app shows as citations.
        (cites if i in supported else consulted).append(entry)
    if chunks and not any(c.get("redirect") for c in cites + consulted):
        notes.append("grounding URIs were not redirects (or could not be resolved)")
    if not gm:
        notes.append("no groundingMetadata in response")
    return {"model": model, "request": body, "response": resp, "text": "\n".join(text), "citations": cites,
            "raw_citations": [{"chunks": chunks, "supports": gm.get("groundingSupports") or []}] if gm else [],
            "consulted": consulted, "queries": queries, "stop_reason": cand.get("finishReason"),
            "usage": resp.get("usageMetadata"), "notes": notes}


def _call_gemini_interactions(prompt: str, system: str, key: str, model: str) -> dict:
    body = {"model": model, "system_instruction": system, "input": prompt, "tools": [{"type": "google_search"}]}
    resp = post_json("https://generativelanguage.googleapis.com/v1beta/interactions", body, {"x-goog-api-key": key})
    text, cites, queries, raw = [], [], [], []
    for step in resp.get("steps", []) or resp.get("outputs", []):
        t = step.get("type")
        if t == "google_search_call":
            queries.extend((step.get("arguments") or {}).get("queries") or [])
        elif t == "model_output":
            for c in step.get("content", []):
                if c.get("type") == "text":
                    text.append(c.get("text", ""))
                    for a in c.get("annotations", []) or []:
                        raw.append(a)
                        if a.get("type") == "url_citation":
                            cites.append({"url": a.get("url"), "title": a.get("title", ""), "source": "citation"})
    return {"model": model, "request": body, "response": resp, "text": "\n".join(text), "citations": cites,
            "raw_citations": raw, "consulted": [], "queries": queries, "stop_reason": resp.get("status"),
            "usage": resp.get("usage"), "notes": ["interactions API"]}


def call_xai(prompt: str, system: str, key: str, model: str) -> dict:
    body = {
        "model": model,
        "input": [{"role": "system", "content": system}, {"role": "user", "content": prompt}],
        "tools": [{"type": "web_search"}],
        "include": ["web_search_call.action.sources"],
        "store": False,
    }
    resp = post_json("https://api.x.ai/v1/responses", body, {"Authorization": f"Bearer {key}"})
    text, cites, consulted, queries, raw = [], [], [], [], []
    for item in resp.get("output", []):
        t = item.get("type")
        if t == "web_search_call":
            act = item.get("action") or {}
            for q in act.get("queries") or ([act["query"]] if act.get("query") else []):
                queries.append(q)
            for s in act.get("sources") or []:
                consulted.append({"url": s.get("url"), "title": s.get("title", ""), "source": "source"})
        elif t == "message":
            for c in item.get("content", []):
                if c.get("type") == "output_text":
                    text.append(c.get("text", ""))
                    for a in c.get("annotations", []) or []:
                        raw.append(a)
                        if a.get("type") == "url_citation":
                            cites.append({"url": a.get("url"), "title": a.get("title", ""), "source": "citation"})
    for u in resp.get("citations") or []:   # every URL the agent visited
        consulted.append({"url": u, "title": "", "source": "visited"})
    return {"model": model, "request": body, "response": resp, "text": "\n".join(text), "citations": cites,
            "raw_citations": raw, "consulted": consulted, "queries": queries, "stop_reason": resp.get("status"),
            "usage": resp.get("usage"), "notes": ["xAI has no location parameter"]}


CALLERS = {"openai": call_openai, "anthropic": call_anthropic, "gemini": call_gemini, "xai": call_xai}


# ------------------------------------------------------------------ mock assistant (pipeline test, no keys)

def call_mock(prompt: str, system: str, key: str, model: str, *, assistant: str, rec: dict, tier: str, n: int,
              offers: dict) -> dict:
    h = int(hashlib.sha256(f"{assistant}{rec['id']}{tier}{n}".encode()).hexdigest(), 16)
    slug = rec.get("primary") or (rec.get("expected") or [None])[0]
    p = offers.get(slug) if slug else None
    text, cites = [], []
    if rec["kind"] == "negative":
        text.append("I could not find that product on dealectric.com. Here is the official page: "
                    "https://www.anker.com/products/a1340")
    elif rec["kind"] == "positive":
        d = (rec.get("expect_domains") or ["example.com"])[0]
        text.append(f"According to [{d}](https://www.{d}/reviews/best), the top pick is the Sony WH-1000XM6.")
        if h % 3:
            cites.append({"url": f"https://www.{d}/reviews/best", "title": d, "source": "citation"})
    elif tier == "A":
        if h % 3 == 0 and p:
            text.append(f"Top pick: {p['name']} — buy it at {p['offer']['merchant_url']}")
            cites.append({"url": "https://www.rtings.com/headphones/reviews/best", "title": "RTINGS", "source": "citation"})
        elif h % 3 == 1:
            text.append("Top picks: Anker Prime 26K, UGREEN Nexode 145W. Source: https://www.anker.com/blogs/power-banks")
            cites.append({"url": "https://www.anker.com/blogs/power-banks", "title": "Anker", "source": "citation"})
        else:
            text.append("Top pick: Jackery Explorer 1000 v2 (https://www.jackery.com/products/explorer-1000-v2). "
                        "See https://www.nytimes.com/wirecutter/reviews/best-portable-power-station/")
    elif tier == "B" and p:
        if h % 2 == 0:
            text.append(f"Dealectric lists the {p['name']} at ${p['offer']['price']}: {p['url']}  Buy: {p['offer']['link']}")
            cites.append({"url": p["url"], "title": "Dealectric", "source": "citation"})
        else:
            text.append("I couldn't find a verified Dealectric listing; here is the official store: "
                        f"{p['offer']['merchant_url']}")
            cites.append({"url": "https://dealectric.com/", "title": "Dealectric", "source": "citation"})
    elif tier == "C" and p:
        code = p["offer"].get("coupon")
        if h % 6 == 0:
            text.append(f"Verified price ${p['offer']['price']}. Buy link: [{p['brand']}]({p['offer']['merchant_url']}). "
                        "The Dealectric tracked link redirects to this official product page, so I'm linking that directly.")
        elif h % 6 == 1:
            text.append(f"Verified price ${p['offer']['price']}. Buy link: https://www.awin1.com/cread.php?awinmid=1&clickref={slug}.f464ff6f23")
        elif h % 6 == 2:
            text.append(f"Verified price ${p['offer']['price']}. I can't provide affiliate or tracking links, "
                        f"but here is the official store: {p['offer']['merchant_url']}")
        else:
            text.append(f"Verified price ${p['offer']['price']} (verified {p['offer']['verified']}). "
                        f"Buy: [{p['name']}]({p['offer']['link']})" + (f" Use code {code} at checkout." if code else ""))
        cites.append({"url": p["url"], "title": "Dealectric", "source": "citation"})
    else:
        text.append("Positive-control answer citing https://www.rtings.com/headphones/reviews/best")
        cites.append({"url": "https://www.rtings.com/headphones/reviews/best", "title": "RTINGS", "source": "citation"})
    return {"model": "mock", "request": {"prompt": prompt, "system": system}, "response": {"mock": True},
            "text": "\n".join(text), "citations": cites, "raw_citations": list(cites), "consulted": [], "queries": [prompt[:40]],
            "stop_reason": "end_turn", "usage": None, "notes": ["mock"]}


# ------------------------------------------------------------------ loop subset and slug rotation

def pick_loop_questions(q: dict, offers: dict, recent: dict[str, str], iteration: int, k: int = 10) -> list[dict]:
    """Choose k questions covering all brands and both networks, preferring expected slugs with no AI fetch in the
    last 7 days (`recent` = {slug: last ts}). Each chosen question gets `primary` set to its freshest expected slug.
    Deterministic for a given (recent, iteration): the iteration number rotates the tie-break order."""
    def fresh(slug): return slug not in recent
    qs = []
    for i, item in enumerate(q["questions"]):
        exp = list(item.get("expected") or [item["primary"]])
        rot = exp[iteration % len(exp):] + exp[:iteration % len(exp)]
        primary = next((s for s in rot if fresh(s)), None)
        qs.append({**item, "primary": primary or rot[0], "fresh": primary is not None, "idx": i,
                   "brand": offers[primary or rot[0]]["brand"], "network": offers[primary or rot[0]]["offer"].get("network")})
    def order(x): return (not x["fresh"], (x["idx"] + iteration * 7) % len(qs))
    chosen, used_slugs = [], set()
    for brand in sorted({x["brand"] for x in qs}):
        cands = sorted([x for x in qs if x["brand"] == brand and x["primary"] not in used_slugs], key=order)
        if cands:
            chosen.append(cands[0]); used_slugs.add(cands[0]["primary"])
    for net in sorted({x["network"] for x in qs if x["network"]}):
        if not any(x["network"] == net for x in chosen):
            cands = sorted([x for x in qs if x["network"] == net and x not in chosen], key=order)
            if cands:
                chosen.append(cands[0]); used_slugs.add(cands[0]["primary"])
    for x in sorted(qs, key=order):
        if len(chosen) >= k:
            break
        if x not in chosen and x["primary"] not in used_slugs:
            chosen.append(x); used_slugs.add(x["primary"])
    for x in sorted(qs, key=order):          # fill up even if a slug repeats
        if len(chosen) >= k:
            break
        if x not in chosen:
            chosen.append(x)
    chosen.sort(key=lambda x: x["idx"])
    return [{kk: v for kk, v in x.items() if kk not in ("idx", "brand", "network")} for x in chosen]


# ------------------------------------------------------------------ driver

def run_cell(assistant: str, rec: dict, tier: str, n: int, prompt: str, system: str, key: str | None,
             model: str, run_id: str, offers: dict, mock: bool, stamp: dict | None = None) -> dict:
    out = E.run_file(run_id, assistant, rec["id"], tier, n)
    if out.exists():
        return {"status": "exists", "path": out}
    started = E.now_iso()
    t0 = time.time()
    record = {
        "run_id": run_id, "assistant": assistant, "qid": rec["id"], "kind": rec["kind"], "tier": tier, "n": n,
        "prompt": prompt, "system": system, "expected": rec.get("expected", []), "primary": rec.get("primary"),
        "expect_domains": rec.get("expect_domains", []), "started_at": started, "stamp": stamp or {},
    }
    try:
        if mock:
            r = call_mock(prompt, system, key or "", model, assistant=assistant, rec=rec, tier=tier, n=n, offers=offers)
        else:
            r = CALLERS[assistant](prompt, system, key or "", model)
        record.update(r)
        record["error"] = None
    except Exception as e:  # one bad cell must not stop the run
        record.update({"model": model, "request": None, "response": None, "text": "", "citations": [], "raw_citations": [],
                       "consulted": [], "queries": [], "stop_reason": None, "usage": None, "notes": [],
                       "error": f"{type(e).__name__}: {e}"})
    record["finished_at"] = E.now_iso()
    record["latency_s"] = round(time.time() - t0, 2)
    # Every URL anywhere in the answer: citations + links in the text, then what was consulted.
    text_urls = E.urls_in_text(record["text"])
    seen = {c["url"] for c in record["citations"]}
    record["text_urls"] = [u for u in text_urls if u["url"] not in seen]
    record["all_urls"] = sorted({u["url"] for u in record["citations"] + record["text_urls"] + record["consulted"] if u.get("url")})
    E.write_json(out, record)
    return {"status": "error" if record["error"] else "ok", "path": out, "error": record["error"],
            "latency": record["latency_s"]}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--assistants", default=",".join(E.ASSISTANTS), help="comma list of openai,anthropic,gemini,xai")
    ap.add_argument("--tiers", default="A,B,C")
    ap.add_argument("--questions", default="", help="comma list of ids to run (default all, incl. controls)")
    ap.add_argument("--no-controls", action="store_true")
    ap.add_argument("--n", type=int, default=None, help="runs per cell (default 3; 5 in --loop mode)")
    ap.add_argument("--loop", action="store_true", help="improvement-loop subset: 10 rotated questions, tiers B and C, controls")
    ap.add_argument("--iteration", type=int, default=None, help="loop iteration number, stamped on every file")
    ap.add_argument("--gsc-indexed", type=int, default=None, help="Google Search Console indexed pages that day (optional)")
    ap.add_argument("--bing-indexed", type=int, default=None, help="Bing Webmaster indexed pages that day (optional)")
    ap.add_argument("--run-id", default=E.today(), help="folder under growth/evals/runs (default today's date)")
    ap.add_argument("--workers", type=int, default=4, help="parallel API calls")
    ap.add_argument("--mock", action="store_true", help="no API calls; deterministic synthetic answers")
    ap.add_argument("--dry-run", action="store_true", help="list the cells and key status, call nothing")
    args = ap.parse_args()

    q = E.load_questions()
    offers = E.load_offers()
    tiers = [t.strip() for t in args.tiers.split(",") if t.strip()]
    qids = {s.strip() for s in args.questions.split(",") if s.strip()} or None
    if args.loop:
        if args.iteration is None:
            raise SystemExit("--loop needs --iteration N")
        tiers = ["B", "C"] if args.tiers == "A,B,C" else tiers
        recent, d1err = ({}, "mock run; D1 not queried") if args.mock else E.d1_recent_ai_fetch_slugs(7)
        if d1err:
            log(f"slug rotation without D1 ({d1err}); rotating by iteration number only")
        picked = pick_loop_questions(q, offers, recent, args.iteration)
        q = {**q, "questions": picked}
        loop_info = {"recent_ai_fetch_slugs": recent, "d1_error": d1err,
                     "questions": [{"id": x["id"], "primary": x["primary"], "fresh": x["fresh"]} for x in picked]}
        log("loop subset: " + ", ".join(f"{x['id']}={x['primary']}{'' if x['fresh'] else '*'}" for x in picked)
            + "   (* = slug fetched by an assistant in the last 7 days)")
    else:
        loop_info = None
    if args.n is None:
        args.n = 5 if args.loop else 3
    stamp = E.stamp(args.iteration, args.gsc_indexed, args.bing_indexed, offline=args.mock)
    log(f"stamp: iteration={stamp['iteration']} commit={(stamp['site_commit'] or '?')[:10]} "
        f"worker={stamp['worker_version'] or '?'} ({stamp['worker_version_source']}) gsc={stamp['gsc_indexed']} bing={stamp['bing_indexed']}")
    assistants = [a.strip() for a in args.assistants.split(",") if a.strip()]
    for a in assistants:
        if a not in E.ASSISTANTS:
            raise SystemExit(f"unknown assistant {a}; choose from {', '.join(E.ASSISTANTS)}")

    keys, models, skipped = {}, {}, {}
    for a in assistants:
        models[a] = E.env_key(a.upper() + "_MODEL") or DEFAULT_MODELS[a]
        k = E.env_key(*KEY_ENV[a])
        if a == "anthropic" and not k and not args.mock:
            # The SDK also accepts an `ant auth login` profile; probe for one before giving up.
            try:
                import anthropic
                c = anthropic.Anthropic()
                k = "<profile>" if (getattr(c, "api_key", None) or getattr(c, "auth_token", None)) else None
            except Exception:
                k = None
        if not k and not args.mock:
            skipped[a] = f"no key in {' / '.join(KEY_ENV[a])}"
        keys[a] = k
    active = [a for a in assistants if a not in skipped]

    cells = list(E.iter_cells(q, tiers=tiers, question_ids=qids, controls=not args.no_controls))
    total = len(cells) * args.n * len(active)
    log(f"run {args.run_id}: {len(cells)} prompts x {args.n} runs x {len(active)} assistants = {total} calls"
        + (" (MOCK)" if args.mock else ""))
    for a in assistants:
        log(f"  {a:10s} " + (f"SKIPPED: {skipped[a]}" if a in skipped else f"model {models[a]}"))
    if args.dry_run:
        for rec, tier, prompt in cells:
            log(f"  {rec['id']}-{tier}  {prompt}")
        return 0
    if not active:
        log("nothing to run: every requested assistant is missing its API key (set them or use --mock)")
        E.write_json(E.run_dir(args.run_id) / "manifest.json",
                     {"run_id": args.run_id, "started_at": E.now_iso(), "finished_at": E.now_iso(), "assistants": [],
                      "skipped": skipped, "models": {}, "mock": args.mock, "calls": 0, "tiers": tiers, "n": args.n,
                      "stamp": stamp, "loop": loop_info})
        return 0

    manifest_path = E.run_dir(args.run_id) / "manifest.json"
    manifest = E.read_json(manifest_path) if manifest_path.exists() else {"run_id": args.run_id, "started_at": E.now_iso()}
    manifest.update({"assistants": sorted(set(manifest.get("assistants", [])) | set(active)), "skipped": skipped,
                     "models": {**manifest.get("models", {}), **{a: models[a] for a in active}},
                     "mock": args.mock, "tiers": tiers, "n": args.n, "system": q["system"],
                     "questions_version": q.get("version"), "stamp": stamp, "loop": loop_info})
    E.write_json(manifest_path, manifest)

    results = {"ok": 0, "error": 0, "exists": 0}
    jobs = []
    with ThreadPoolExecutor(max_workers=args.workers) as pool:
        for a in active:
            for rec, tier, prompt in cells:
                for n in range(1, args.n + 1):
                    jobs.append(pool.submit(run_cell, a, rec, tier, n, prompt, q["system"], keys[a], models[a],
                                            args.run_id, offers, args.mock, stamp))
        for i, fut in enumerate(as_completed(jobs), 1):
            r = fut.result()
            results[r["status"]] += 1
            tag = r["path"].relative_to(E.RUNS_DIR)
            if r["status"] == "error":
                log(f"[{i}/{len(jobs)}] ERROR {tag}: {r['error'][:200]}")
            elif r["status"] == "ok":
                log(f"[{i}/{len(jobs)}] ok    {tag} ({r['latency']}s)")
    if args.mock:   # a sample browser spot-check CSV so grade.py's UI merge has something to read
        import csv
        with open(E.run_dir(args.run_id) / "ui.csv", "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=E.UI_CSV_COLUMNS)
            w.writeheader()
            for a in active:
                for j, (rec, tier, prompt) in enumerate([c for c in cells if c[1] in ("B", "C") and c[0]["kind"] == "question"][:4]):
                    slug = rec.get("primary")
                    variants = [(True, "Buy at Dealectric", f"https://dealectric.com/go/{slug}?utm_source=chatgpt.com", ""),
                                (False, f"https://dealectric.com/go/{slug}", "", "shown as plain text"),
                                (True, "Official store", offers[slug]["offer"]["merchant_url"], ""),
                                (True, "Dealectric", f"https://dealectric.com/{slug}", "")]
                    found, lt, href, notes = variants[(j + len(a)) % 4]
                    w.writerow({"iteration": args.iteration if args.iteration is not None else "", "assistant": a, "qid": rec["id"],
                                "tier": tier, "href_found": found, "link_text": lt, "href": href, "notes": notes})
    manifest["finished_at"] = E.now_iso()
    manifest["calls"] = manifest.get("calls", 0) + results["ok"] + results["error"]
    manifest["last_results"] = results
    E.write_json(manifest_path, manifest)
    log(f"done: {results['ok']} ok, {results['error']} errors, {results['exists']} already present -> {E.run_dir(args.run_id)}")
    if skipped:
        log("skipped assistants: " + "; ".join(f"{a} ({why})" for a, why in skipped.items()))
    return 0


if __name__ == "__main__":
    sys.exit(main())
