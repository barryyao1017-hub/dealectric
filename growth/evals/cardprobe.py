#!/usr/bin/env python3.12
"""Where the ChatGPT app's answer parts come from, and how the API differs (DLC-77, 2026-10-30).

    python3.12 growth/evals/cardprobe.py app  --run <run-id> [--qids a,b] [--reps 1]   # app chats, raw stream kept
    python3.12 growth/evals/cardprobe.py api  --run <run-id> [--qids a,b] [--reps 3] [--models gpt-6.1-sol,gpt-6-luna]
    python3.12 growth/evals/cardprobe.py parse <ctx-or-run-file.json>                  # one app chat, decomposed
    python3.12 growth/evals/cardprobe.py report --run <run-id>                          # app vs API tables

The app's SSE stream is delta-encoded (v1: add / append / replace / patch on JSON paths), so the final state of each
message is rebuilt from every op (`rebuild`). From the rebuilt messages a chat decomposes into:
- queries: the web.run search queries; results: every search_result_group entry with its ref (turn<id>search<n>);
- products: catalog records the answer binds (`model_dil_v2.appData.opGenui.modelDataBindings`, refs
  turn<id>product<n>): title, price, merchant, product_page URL (utm_campaign=openai_catalog / utm_medium=feed);
- links in the answer, by kind: `card` (a catalog record's product_page, rendered by ChatGPT's product card), `button`
  (GenUI.openUrl / Link with a literal URL the model wrote), `cite` (source pills), `text` (markdown links).
API runs (Responses API, web_search) keep queries, sources and answer links for the same prompts.
"""
from __future__ import annotations

import argparse, json, re, sys, time
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402

QFILES = [E.REPO / "growth" / "focus" / "loop-questions.json", E.REPO / "growth" / "focus" / "loop-questions-allpowers.json"]
URL_RE = re.compile(r"https?://[^\s\"'<>)\]}]+")


# ------------------------------------------------------------------ stream rebuild
def _set(obj, path, op, val):
    keys = [k for k in path.split("/") if k != ""]
    if not keys:
        return
    cur = obj
    for k in keys[:-1]:
        cur = cur[int(k)] if isinstance(cur, list) else cur.setdefault(k, {})
    last = int(keys[-1]) if isinstance(cur, list) else keys[-1]
    if op in ("replace", "add"):
        if isinstance(cur, list) and last == len(cur):
            cur.append(val)
        else:
            cur[last] = val
    elif op == "append":
        if isinstance(cur, dict) and last not in cur:
            cur[last] = val
        elif isinstance(cur[last], str):
            cur[last] += val
        elif isinstance(cur[last], list):
            cur[last] += val if isinstance(val, list) else [val]
        elif isinstance(cur[last], dict) and isinstance(val, dict):
            cur[last].update(val)
        else:
            cur[last] = val
    elif op == "remove":
        if isinstance(cur, list):
            cur.pop(last)
        else:
            cur.pop(last, None)


def rebuild(text: str) -> list[dict]:
    msgs, cur = [], None
    for line in text.split("\n"):
        if not line.startswith("data:"):
            continue
        s = line[5:].strip()
        if not s.startswith("{"):
            continue
        try:
            d = json.loads(s)
        except ValueError:
            continue
        v = d.get("v")
        if isinstance(v, dict) and "message" in v and d.get("o") in (None, "add") and not d.get("p"):
            cur = {"message": v["message"]}
            msgs.append(cur)
            continue
        if d.get("o") == "patch":
            ops = v
        elif "p" in d and "o" in d:
            ops = [d]
        elif isinstance(v, str) and "p" not in d:
            ops = [{"p": "/message/content/parts/0", "o": "append", "v": v}]
        elif isinstance(v, list) and "o" not in d:
            ops = v
        else:
            ops = []
        for op in ops or []:
            if cur is not None and isinstance(op, dict) and "p" in op:
                try:
                    _set(cur, op["p"], op.get("o", "replace"), op.get("v"))
                except (KeyError, IndexError, TypeError, ValueError):
                    pass
    return [m["message"] for m in msgs]


def host(u: str) -> str:
    return E.host_of(u or "")


def decompose(sse: list[dict]) -> dict:
    """One app chat -> queries, results, products, links by kind, model."""
    msgs = [m for st in sse for m in rebuild(st.get("text", ""))]
    out = {"queries": [], "results": [], "products": {}, "links": [], "model": None, "answer": ""}
    seen_r = set()
    for m in msgs:
        md = m.get("metadata") or {}
        if md.get("resolved_model_slug") or md.get("model_slug"):
            out["model"] = md.get("resolved_model_slug") or md["model_slug"]
        q = md.get("search_model_queries")
        if isinstance(q, dict):
            out["queries"] += [x for x in q.get("queries") or [] if x not in out["queries"]]
        for g in md.get("search_result_groups") or []:
            for e in g.get("entries") or []:
                ref = e.get("ref_id") or {}
                key = (ref.get("turn_index"), ref.get("ref_type"), ref.get("ref_index"), e.get("url"))
                if key in seen_r:
                    continue
                seen_r.add(key)
                out["results"].append({"ref": f"turn{ref.get('turn_index')}{ref.get('ref_type')}{ref.get('ref_index')}",
                                       "type": ref.get("ref_type"), "url": E.strip_tracking(e.get("url") or ""), "title": e.get("title"),
                                       "snippet": e.get("snippet") or ""})
        if (m.get("author") or {}).get("role") != "assistant" or (m.get("content") or {}).get("content_type") != "text":
            continue
        parts = [p for p in (m["content"].get("parts") or []) if isinstance(p, str)]
        if parts and len(parts[0]) > len(out["answer"]):
            out["answer"] = parts[0]
        dil = md.get("model_dil_v2") or {}
        og = (dil.get("appData") or {}).get("opGenui") or {}
        for ref, rec in (og.get("modelDataBindings") or {}).items():
            if isinstance(rec, dict):
                url = ((rec.get("product_page") or {}).get("uri")) or ""
                out["products"][ref] = {"title": rec.get("title"), "merchant": rec.get("merchant"), "price": rec.get("displayed_price"),
                                        "url": E.strip_tracking(url), "host": host(url),
                                        "feed": "openai_catalog" in url or "utm_medium=feed" in url}
        code = dil.get("code") or ""
        consts = json.dumps(dil.get("constants") or {})
        for u in re.findall(r"GenUI\.openUrl\(\s*[\"']([^\"']+)", code + consts + parts[0] if parts else code):
            out["links"].append({"kind": "button", "url": E.strip_tracking(u)})
        for u in re.findall(r'Link,\{"url":"([^"]+)"', code):
            out["links"].append({"kind": "button", "url": E.strip_tracking(u)})
        for ref in re.findall(r'product_page\?\.uri', code) and og.get("modelDataBindings") or {}:
            pass
        for ref, p in out["products"].items():
            if ref in code and p["url"]:
                out["links"].append({"kind": "card", "url": p["url"], "merchant": p["merchant"]})
        for c in md.get("genui_components") or []:
            if c.get("type") == "cite":
                for s in c.get("safe_urls") or []:
                    u = s.get("url") if isinstance(s, dict) else s
                    if u and "images.openai.com" not in u:
                        out["links"].append({"kind": "cite", "url": E.strip_tracking(u)})
        text = (dil.get("fallbackMarkdown") or "") + (parts[0] if parts else "")
        for _, u in re.findall(r"\[([^\]]*)\]\((https?://[^)\s]+)\)", text):
            out["links"].append({"kind": "text", "url": E.strip_tracking(u)})
    dedup, seen = [], set()
    for l in out["links"]:
        k = (l["kind"], l["url"])
        if k not in seen:
            seen.add(k)
            dedup.append(l)
    out["links"] = dedup
    return out


# ------------------------------------------------------------------ runs
def questions(qids: list[str] | None) -> list[tuple[str, str]]:
    out = []
    for f in QFILES:
        d = json.loads(f.read_text())
        qs = d if isinstance(d, list) else d.get("questions", [])
        for q in qs:
            if isinstance(q, dict) and (not qids or q.get("qid") in qids):
                if q["qid"] not in [x for x, _ in out]:
                    out.append((q["qid"], q["prompt"]))
    return out


# ui.SSE_HOOK_JS tees only POST /backend-api/f/conversation; on 2026-10-30 one chat's answer continued in another
# streaming response and the capture stopped at the search. This hook (set for this process only, W1's driver keeps
# ui.py's) tees every backend response served as text/event-stream.
WIDE_HOOK_JS = r"""
(() => {
  window.__sse = [];
  const of = window.fetch;
  window.fetch = async function(input, init) {
    const url = typeof input === 'string' ? input : (input && input.url) || '';
    const resp = await of.apply(this, arguments);
    try {
      const ct = (resp.headers && resp.headers.get('content-type')) || '';
      if (/backend-(api|anon)\//.test(url) && /event-stream/.test(ct) && resp.body) {
        const [a, b] = resp.body.tee();
        const rec = {url, chunks: []}; window.__sse.push(rec);
        (async () => { const rd = b.getReader(); const dec = new TextDecoder();
          while (true) { const {done, value} = await rd.read(); if (done) break; rec.chunks.push(dec.decode(value, {stream: true})); } })();
        return new Response(a, {status: resp.status, statusText: resp.statusText, headers: resp.headers});
      }
    } catch (e) {}
    return resp;
  };
})();
"""


def run_app(run: str, qs, reps: int, gap: float) -> None:
    import ctxprobe as C
    import ui
    ui.SSE_HOOK_JS = WIDE_HOOK_JS
    C.OUT = E.RUNS_DIR / run / "app"
    for r in range(1, reps + 1):
        for qid, prompt in qs:
            tag = f"{qid}--{r}"
            if (C.OUT / f"{tag}.json").exists():
                continue
            rec = C.chat(prompt, [], tag)
            d = decompose(rec.get("sse") or [])
            print(f"app {tag:55} {d['model']} err={rec.get('error')} q={len(d['queries'])} res={len(d['results'])} "
                  f"prod={len(d['products'])} links={Counter(l['kind'] for l in d['links'])}", flush=True)
            time.sleep(gap)


def run_api(run: str, qs, reps: int, models: list[str]) -> None:
    import concurrent.futures as cf
    import apiprobe as A
    key = E.env_key("OPENAI_API_KEY")
    out = E.RUNS_DIR / run / "api"
    out.mkdir(parents=True, exist_ok=True)

    def one(job):
        model, (qid, prompt), r = job
        p = out / f"{model}--{qid}--{r}.json"
        if p.exists():
            return None
        started = E.now_iso()
        status, resp = A.post({"model": model, "input": prompt, "store": False,
                               "tools": [{"type": "web_search", "user_location": {"type": "approximate", "country": "US"}}],
                               "include": ["web_search_call.action.sources"]}, key)
        queries, sources, links, answer = [], [], [], []
        for it in resp.get("output", []) if status == 200 else []:
            if it.get("type") == "web_search_call":
                a = it.get("action") or {}
                queries += [q for q in (a.get("queries") or ([a["query"]] if a.get("query") else []))]
                sources += [E.strip_tracking(s.get("url") or "") for s in a.get("sources") or []]
            elif it.get("type") == "message":
                for c in it.get("content", []):
                    if c.get("type") == "output_text":
                        answer.append(c.get("text", ""))
                        for an in c.get("annotations") or []:
                            if an.get("type") == "url_citation":
                                links.append({"kind": "cite", "url": E.strip_tracking(an.get("url") or "")})
        text = "\n".join(answer)
        for _, u in re.findall(r"\[([^\]]*)\]\((https?://[^)\s]+)\)", text):
            links.append({"kind": "text", "url": E.strip_tracking(u)})
        rec = {"model": model, "qid": qid, "rep": r, "prompt": prompt, "status": status, "error": resp.get("error"),
               "queries": queries, "sources": sources, "links": links, "answer": text, "usage": resp.get("usage"), "started_at": started}
        E.write_json(p, rec)
        E.footprint("openai-api", started, E.now_iso(), prompt=prompt, run_id=run, prompt_id=p.stem, script="cardprobe.py",
                    retrieved=[{"url": s} for s in sources], cited=[links], error=str(resp.get("error")) if status != 200 else None)
        return rec

    jobs = [(m, q, r) for m in models for q in qs for r in range(1, reps + 1)]
    with cf.ThreadPoolExecutor(6) as ex:
        for rec in ex.map(one, jobs):
            if rec:
                print(f"api {rec['model']:12} {rec['qid']:50} {rec['rep']} {rec['status']} q={len(rec['queries'])} src={len(rec['sources'])} "
                      f"links={Counter(l['kind'] for l in rec['links'])}", flush=True)


def is_ours(u: str) -> bool:
    return "dealectric.com" in (u or "")


def is_go(u: str) -> bool:
    return "dealectric.com/go/" in (u or "")


def report(run: str) -> str:
    """Per question: app (one chat each) vs API (reps per model): queries, our pages in results, links by kind."""
    base = E.RUNS_DIR / run
    app = {}
    for f in sorted((base / "app").glob("*.json")):
        r = json.loads(f.read_text())
        qid = f.stem.rsplit("--", 1)[0]
        d = decompose(r.get("sse") or [])
        d["complete"] = bool(d["answer"]) or bool(d["links"])
        app.setdefault(qid, []).append(d)
    api = defaultdict(lambda: defaultdict(list))
    for f in sorted((base / "api").glob("*.json")):
        r = json.loads(f.read_text())
        if r.get("status") == 200:
            api[r["qid"]][r["model"]].append(r)
    L = ["| question | channel | queries | our page in results | our page cited | /go/ link given | catalog card (merchant) | other buy links |",
         "|---|---|---|---|---|---|---|---|"]
    for qid in sorted(set(app) | set(api)):
        for d in app.get(qid, []):
            res_ours = sorted({x["url"].split("dealectric.com")[1] or "/" for x in d["results"] if is_ours(x["url"])})
            cited = sorted({l["url"].split("dealectric.com")[1] or "/" for l in d["links"] if is_ours(l["url"]) and not is_go(l["url"])})
            go = sorted({l["kind"] + ":" + l["url"].split("/go/")[1] for l in d["links"] if is_go(l["url"])})
            cards = sorted({f"{p['merchant']} ({p['host']})" for p in d["products"].values() if any(l['kind'] == 'card' and l['url'] == p['url'] for l in d['links'])})
            other = sorted({l["kind"] + ":" + host(l["url"]) for l in d["links"] if l["kind"] in ("button", "text") and not is_ours(l["url"])})
            L.append(f"| {qid} | app {d['model'] or '?'}{'' if d['complete'] else ' (stream cut)'} | {len(d['queries'])} | {', '.join(res_ours) or '-'} | "
                     f"{', '.join(cited) or '-'} | {', '.join(go) or '-'} | {'; '.join(cards) or '-'} | {', '.join(other) or '-'} |")
        for model, rs in sorted(api.get(qid, {}).items()):
            n = len(rs)
            inres = sum(any(is_ours(s) for s in r["sources"]) for r in rs)
            cit = sum(any(is_ours(l["url"]) and not is_go(l["url"]) for l in r["links"]) or ("dealectric.com" in r["answer"] and "/go/" not in r["answer"]) for r in rs)
            go = sum(any(is_go(l["url"]) for l in r["links"]) or "dealectric.com/go/" in r["answer"] for r in rs)
            other = Counter(host(l["url"]) for r in rs for l in r["links"] if l["kind"] == "text" and not is_ours(l["url"]))
            q = sum(len(r["queries"]) for r in rs) / n
            L.append(f"| {qid} | API {model} ×{n} | {q:.1f} avg | {inres}/{n} | {cit}/{n} | {go}/{n} | n/a | {', '.join(f'{h} {c}' for h, c in other.most_common(3))} |")
    return "\n".join(L)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["app", "api", "parse", "report"])
    ap.add_argument("file", nargs="?")
    ap.add_argument("--run")
    ap.add_argument("--qids")
    ap.add_argument("--reps", type=int, default=1)
    ap.add_argument("--gap", type=float, default=20)
    ap.add_argument("--models", default="gpt-6.1-sol,gpt-6-luna")
    a = ap.parse_args()
    qs = questions(a.qids.split(",") if a.qids else None)
    if a.cmd == "parse":
        print(json.dumps(decompose(json.loads(Path(a.file).read_text())["sse"]), indent=1)[:20000])
    elif a.cmd == "report":
        print(report(a.run))
    elif a.cmd == "app":
        run_app(a.run, qs, a.reps, a.gap)
    else:
        run_api(a.run, qs, a.reps, a.models.split(","))
    return 0


if __name__ == "__main__":
    sys.exit(main())
