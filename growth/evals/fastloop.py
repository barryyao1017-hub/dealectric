#!/usr/bin/env python3.12
"""The ChatGPT fast loop (DLC-112, design: .claude/skills/chatgpt-discoverability/SKILL.md): score page drafts offline
against the result set ChatGPT really got, so copy iterates in minutes and only the winner waits for OpenAI's crawler.

    python3.12 growth/evals/fastloop.py pack --cell runs/<run>/chatgpt/<qid>.json --name <pack>   # from an app chat
    python3.12 growth/evals/fastloop.py pack --query "<ChatGPT's query>" --question "<shopper question>" --name <pack> [--engine api]
    python3.12 growth/evals/fastloop.py pack --cell runs/<run>/ctx/pinned-1.json --question "<q>" --name <pack>  # pinned chat
    python3.12 growth/evals/fastloop.py gap <pack> [<pack> ...]            # open or saturated, recurring domains
    python3.12 growth/evals/fastloop.py replay <pack> --draft d.md [--rank 2] [--url /slug] [--reps 3] [--tag v1]
    python3.12 growth/evals/fastloop.py score <pack> [--concern "<the open concern>"]   # scorecard per draft tag
    python3.12 growth/evals/fastloop.py calibrate --n 40 [--model gpt-6-luna] [--reps 3]
    python3.12 growth/evals/fastloop.py calreport [--run <cal-run>]
    python3.12 growth/evals/fastloop.py transfer --n 40       # does the API write the app's query for the same question?

Context builder (stage 4 of the loop). ChatGPT's model gets each result's text from OpenAI's stored copy, all results
sharing one budget, higher ranks getting more, and long pages cut to the passages matching the model's own query
(growth/focus/context-probe.md). Here: each result's share is BUDGET * w(rank) / sum(w), w = rank**-ALPHA, capped at
CAP. With 12 results that gives ~3.2k characters at rank 1 and ~0.9k at rank 12, as measured (a 3.4k product page
ranked first arrived whole; rivals got 110-170 words). A page longer than its share keeps its opening chunk plus the
chunks sharing the most words with the query, in page order. Small result sets (under ~8) got less than this predicts
in the probes; the crowded case is the normal one. Rival text is fetched now (rivals change slowly); our pages, in
calibration, are the version OpenAI had stored at the time of the chat (its last verified OAI-SearchBot fetch before
the chat, else the version live at the chat).

Answer replay (stage 5). --engine api (default): the Responses API, search off: the shopper's question, then a `web_search` function call with
ChatGPT's query and the built context as its output, `tool_choice: none`. The prompt (ANSWER_SYSTEM) is fixed across
drafts. Scores compare drafts; they are not forecasts of the app (no catalog cards, no UI program). --engine app: the
same context pasted into a Free temporary chat (PASTE), so the real gpt-6 writes the answer and its buttons; costs
one gpt-6 message of the Free quota per answer and runs one chat at a time.

Scoring. Tiers as visibility_scan.py (T5 /go/ link, T4 our page linked, T3 Dealectric named, T2 in results only,
T1 absent), plus a Claude judge (JUDGE, via the claude CLI as gapexp.py): top pick, whether it is our product, whether
the answer relied on our page, and, given a concern, whether our answer to it was carried ("our point carried").

Calibration. Recorded app chats with one search and gpt-6 answers (2026-10-26 on) are rebuilt and replayed; the replay
majority over --reps is compared with what the app did: tier band (our page used T4+, /go/ T5), same top pick, same
brand. Pass bars proposed in the skill: cited/not 80%+, top pick 70%+.

Output: runs/fastloop/<pack>/ (pack.json, gap.json, answers/<tag>/<n>.json, score.json) and runs/<date>-fastcal/.
Fetched page text is cached in runs/fastloop-cache/ (not committed). Every API call and fetch of dealectric.com is
footprint-logged.
"""
from __future__ import annotations

import argparse, bisect, collections, concurrent.futures as cf, hashlib, json, os, random, re, ssl, statistics, sys, time
import urllib.request
from pathlib import Path

os.environ.setdefault("AGENT_CDP", "http://localhost:9222")   # profile 1, signed in; ctxprobe alone defaults to 9223

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import apiprobe as A  # noqa: E402
import storedcopy as S  # noqa: E402
from gapexp import html_text, offers, UA  # noqa: E402

LOOP = E.RUNS_DIR / "fastloop"
CACHE = E.RUNS_DIR / "fastloop-cache"
MODEL = "gpt-6-luna"
JUDGE = "claude-sonnet-5-5"
BUDGET, ALPHA, CAP, CHUNK = 18000, 0.5, 16000, 500
STOP = set("the and for with best 2026 2025 review reviews comparison vs top what which how are you your from that this "
           "buy price under over guide".split())
ANSWER_SYSTEM = (
    "You are ChatGPT, answering a shopper in the ChatGPT app. You already ran one web search; its results are the "
    "output of your web_search call. Answer from those results only, the way you normally answer a shopping question: "
    "recommend specific products when the shopper wants to buy, and say why. Cite the results you rely on as markdown "
    "links to their URLs. You may add a buy link for a product you recommend, using a URL that appears in the results.")
try:
    import certifi
    SSL = ssl.create_default_context(cafile=certifi.where())
except ImportError:
    SSL = ssl.create_default_context()
PROMPT_VERSION = "a1"   # bump when ANSWER_SYSTEM or the context format changes; scores across versions don't compare


# ---------------------------------------------------------------- page text

def cache_path(url: str) -> Path:
    return CACHE / "pages" / (hashlib.sha1(url.encode()).hexdigest()[:16] + ".json")


def fetch_text(url: str) -> dict:
    """Live text of a rival page (cached). Returns {text, status}; text is '' when the page could not be read."""
    p = cache_path(url)
    if p.exists():
        return json.loads(p.read_text())
    started, text, status = E.now_iso(), "", "ok"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en"})
        raw = urllib.request.urlopen(req, timeout=20, context=SSL).read(3_000_000).decode("utf-8", "replace")
        text = html_text(raw)
        if len(text) < 400:
            status = "thin"
    except Exception as e:  # noqa: BLE001
        status = f"error: {str(e)[:80]}"
    if status != "ok" and "dealectric.com" not in url:   # bot-walled or JS-rendered: read it in the agent's Chrome
        try:
            import ui
            tab = ui.Tab("about:blank")
            try:
                tab.navigate(url)
                time.sleep(6)
                t2 = (tab.eval("document.body ? document.body.innerText : ''") or "").strip()
            finally:
                tab.close()
            if len(t2) >= 400:
                text, status = t2, "ok (chrome)"
        except Exception:  # noqa: BLE001
            pass
    rec = {"url": url, "text": text, "status": status, "fetched_at": started}
    if not status.startswith("error"):   # retry failures next time
        p.parent.mkdir(parents=True, exist_ok=True)
        E.write_json(p, rec)
    if "dealectric.com" in url:
        E.footprint("direct-fetch", started, E.now_iso(), script="fastloop.py", run_id="fastloop-cache", retrieved=[{"url": url}])
    return rec


class Stored:
    """Our page as OpenAI had it stored at time t: the deployment live at its last verified OAI-SearchBot fetch."""

    def __init__(self):
        self.deploys = sorted(json.loads(S.DEPLOYS.read_text()), key=lambda d: d["at"])
        self.at = [d["at"] for d in self.deploys]
        self.pc = S.page_crawls(S.load_crawls())
        self.blobs = S.Blobs()
        self.lock = __import__("threading").Lock()   # one git cat-file process: reads must not interleave

    def text(self, url: str, t: str) -> tuple[str, str]:
        path = S.norm_path(url)
        fetch = S.last_before(self.pc.get(path, {}).get("OAI-SearchBot", []), t)
        when = fetch or t
        i = bisect.bisect_right(self.at, when) - 1
        if i < 0:
            return "", "no deployment"
        with self.lock:
            raw = self.blobs.get(f"{self.deploys[i]['sha']}:{S.page_file(path)}")
        if raw is None:
            return "", f"missing at {self.deploys[i]['sha'][:7]}"
        how = f"stored {self.deploys[i]['sha'][:7]} (OAI fetch {fetch})" if fetch else f"live {self.deploys[i]['sha'][:7]} (no OAI fetch before)"
        return html_text(raw.decode("utf-8", "replace")), how


# ---------------------------------------------------------------- context builder

def terms(q: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", q.lower()) if len(w) >= 3 and w not in STOP}


def chunks(text: str) -> list[str]:
    out, cur = [], ""
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        if cur and len(cur) + len(line) > CHUNK:
            out.append(cur)
            cur = ""
        cur = f"{cur} {line}".strip()
    if cur:
        out.append(cur)
    return out


def shares(n: int) -> list[int]:
    w = [(r + 1) ** -ALPHA for r in range(n)]
    return [min(CAP, int(BUDGET * x / sum(w))) for x in w]


def cut(text: str, share: int, query: str) -> str:
    if len(text) <= share:
        return text
    cs = chunks(text)
    if not cs:
        return text[:share]
    qt = terms(query)
    scored = sorted(range(1, len(cs)), key=lambda i: (-len(qt & terms(cs[i])), i))
    keep, used = {0}, len(cs[0])
    for i in scored:
        if used + len(cs[i]) > share:
            continue
        keep.add(i)
        used += len(cs[i])
    parts, prev = [], -1
    for i in sorted(keep):
        if prev >= 0 and i != prev + 1:
            parts.append("…")
        parts.append(cs[i][:share] if i == 0 else cs[i])
        prev = i
    return "\n".join(parts)


def build_context(results: list[dict], query: str) -> list[dict]:
    """results: [{url, title, text, snippet?}] in rank order -> each with `shown` (the text the model gets)."""
    sh = shares(len(results))
    out = []
    for r, s in zip(results, sh):
        body = r.get("text") or r.get("snippet") or ""
        out.append({**r, "share": s, "full_chars": len(body), "shown": cut(body, s, query)})
    return out


def context_text(ctx: list[dict], query: str) -> str:
    rows = [f'Results for "{query}":']
    for i, r in enumerate(ctx):
        rows.append(f"\n【{i}】 {r.get('title') or E.host_of(r['url'])}\nURL: {r['url']}\n{r['shown']}")
    return "\n".join(rows)


# ---------------------------------------------------------------- answer replay

def answer(question: str, query: str, ctx: list[dict], model: str, key: str) -> dict:
    body = {"model": model, "store": False, "instructions": ANSWER_SYSTEM, "tool_choice": "none",
            "tools": [{"type": "function", "name": "web_search", "description": "Search the web.",
                       "parameters": {"type": "object", "properties": {"query": {"type": "string"}}, "required": ["query"]}}],
            "input": [{"role": "user", "content": question},
                      {"type": "function_call", "call_id": "call_ws0", "name": "web_search", "arguments": json.dumps({"query": query})},
                      {"type": "function_call_output", "call_id": "call_ws0", "output": context_text(ctx, query)}]}
    started = E.now_iso()
    for attempt in range(4):
        status, r = A.post(body, key)
        if status != 429:
            break
        time.sleep(10 * (attempt + 1))
    text = "\n".join(c.get("text", "") for it in r.get("output", []) if it.get("type") == "message"
                     for c in it.get("content", []) if c.get("type") == "output_text") if status == 200 else ""
    E.footprint("openai-api", started, E.now_iso(), prompt=question, script="fastloop.py", run_id="fastloop",
                retrieved=[{"url": c["url"]} for c in ctx], error=str(r.get("error")) if status != 200 else None)
    return {"status": status, "error": r.get("error"), "text": text, "usage": r.get("usage"), "model": model,
            "prompt_version": PROMPT_VERSION, "started_at": started}


PINNED = ('Run exactly one web search with this exact query, word for word: "{q}". Do not search again and do not open '
          'any page. Then list the title and URL of every result you got, in order.')
PASTES = {   # b1 adds ANSWER_SYSTEM's linking sentence: with a0, the app wrote no links at all (10-31, smoke-solar-budget)
    "a0": ("I collected these {n} web pages from a search for \"{query}\". Do not search the web: answer my question from "
           "these pages only.\n\nMy question: {question}\n\n{pages}"),
    "b1": ("I collected these {n} web pages from a search for \"{query}\". Do not search the web: answer my question from "
           "these pages only. Cite the pages you rely on as links to their URLs. You may add a buy link for a product you "
           "recommend, using a URL that appears in the pages.\n\nMy question: {question}\n\n{pages}")}
PASTE_VERSION = "b1"


def answer_app(question: str, query: str, ctx: list[dict]) -> dict:
    """The same context pasted into a Free temporary chat (agent Chrome, AGENT_CDP), search off: the real gpt-6 and the
    app's own answer program, so buttons count; no catalog cards (no search). One gpt-6 message of the Free quota each
    (~26 per account before gpt-6-mini). Driver per the fork's appfeas test: ?q= fails at this length, so insert text."""
    import ui, ctxprobe as C, cardprobe as K
    text = PASTES[PASTE_VERSION].format(n=len(ctx), query=query, question=question, pages=context_text(ctx, query).split("\n", 1)[1].strip())
    tab = ui.Tab("about:blank")
    tab.ws.settimeout(180)
    started, err, rec = E.now_iso(), None, {}
    try:
        tab.call("Network.enable", maxResourceBufferSize=50_000_000, maxTotalBufferSize=100_000_000)
        tab.call("Page.enable")
        tab.call("Page.addScriptToEvaluateOnNewDocument", source=K.WIDE_HOOK_JS)
        tab.navigate("https://chatgpt.com/?temporary-chat=true")
        time.sleep(6)
        t0 = time.time()
        C.submit(tab, text, 0)
        C.wait_turn(tab, 0, t0, timeout=300)
        time.sleep(2)
        x = K.decompose(C.read_sse(tab))
        links = [l["url"] for l in x["links"] if l["kind"] in ("button", "text", "cite")]
        rec = {"status": 200, "text": x["answer"] + "\n\n" + "\n".join(links), "answer": x["answer"], "links": x["links"],
               "products": x["products"], "model": x["model"], "queries": x["queries"]}
    except Exception as e:  # noqa: BLE001
        err = f"{type(e).__name__}: {e}"
        rec = {"status": 0, "error": err, "text": ""}
    finally:
        E.footprint("chatgpt-ui", started, E.now_iso(), prompt=text, script="fastloop.py", run_id="fastloop", temporary=True,
                    retrieved=[{"url": c["url"]} for c in ctx], error=err, cdp=ui.CDP)
        tab.close()
    rec.update(engine="app", prompt_version=PASTE_VERSION, started_at=started)
    if rec.get("model") and rec["model"] != "gpt-6":
        rec["downgraded"] = True
    return rec


def respond(engine: str, question: str, query: str, ctx: list[dict], model: str, key: str | None) -> dict:
    return answer_app(question, query, ctx) if engine == "app" else answer(question, query, ctx, model, key)


# ---------------------------------------------------------------- scoring

def tier(text: str, our_rank: int | None) -> dict:
    urls = [E.strip_tracking(u) for u in re.findall(r"https?://(?:www\.)?dealectric\.com[^\s)\]>\"']*", text)]
    go = sorted({u for u in urls if "/go/" in u})
    pages = sorted({u for u in urls if "/go/" not in u})
    named = bool(re.search(r"dealectric", text, re.I))
    t = 5 if go else 4 if pages else 3 if named else 2 if our_rank else 1
    return {"tier": t, "go": go, "pages": pages, "named": named}


JUDGE_SCHEMA = {"type": "object", "properties": {
    "top_pick": {"type": "string"}, "top_brand": {"type": "string"}, "products": {"type": "array", "items": {"type": "string"}},
    "our_pick": {"type": "boolean"}, "relied_on_us": {"type": "boolean"}, "point_carried": {"type": "boolean"},
    "why": {"type": "string"}}, "required": ["top_pick", "top_brand", "products", "our_pick", "relied_on_us", "point_carried", "why"]}
JUDGE_SYSTEM = """You grade a shopping assistant's answer. Our site is dealectric.com; OUR PRODUCTS are listed.
- top_pick: the single product the answer recommends first or most strongly, as "Brand Model" ("" if none).
- top_brand: the brand of top_pick ("" if none).
- products: every product the answer recommends, in order, as "Brand Model".
- our_pick: true if top_pick is one of OUR PRODUCTS.
- relied_on_us: true if the main recommendation's facts (prices, specs, codes, links) come from the dealectric.com
  source more than from any other, judging by the citations and the figures quoted. False if dealectric.com is not used.
- point_carried: only when a CONCERN is given: true if the answer addresses that concern with the substance of our
  page's answer to it and credits or links dealectric.com for it. False when no concern is given.
- why: one short sentence."""


def judge(question: str, text: str, concern: str | None = None) -> dict:
    names = "\n".join(f"- {p['name']}" for p in offers().values())
    user = f"OUR PRODUCTS:\n{names}\n\nQUESTION: {question}\n" + (f"\nCONCERN: {concern}\n" if concern else "") + f"\nANSWER:\n{text}"
    try:
        return E.claude_cli_json(JUDGE_SYSTEM, user, JUDGE, JUDGE_SCHEMA, timeout=300) or {}
    except Exception as e:  # noqa: BLE001
        return {"error": str(e)[:200]}


def same_pick(a: str, b: str) -> bool:
    ta, tb = terms(a), terms(b)
    return bool(ta and tb) and len(ta & tb) / min(len(ta), len(tb)) >= 0.6


# ---------------------------------------------------------------- packs

def pack_dir(name: str) -> Path:
    return LOOP / name


def results_from_cell(cell: dict, stored: Stored | None) -> list[dict]:
    t = cell.get("started_at") or E.now_iso()
    out = []
    for r in (cell.get("response") or {}).get("search_results") or []:
        url = r.get("url") or ""
        if "dealectric.com" in url and stored:
            text, how = stored.text(url, t)
        else:
            rec = fetch_text(url)
            text, how = rec["text"], rec["status"]
        out.append({"url": url, "title": r.get("title") or "", "snippet": r.get("snippet") or "", "text": text, "source": how})
    return out


def pinned_chat(query: str, name: str) -> dict:
    """Run one pinned one-search chat in the app (Free, temporary): the result list ChatGPT gets for exactly `query`."""
    import ctxprobe as C
    C.OUT = pack_dir(name) / "pinned"
    C.chat(PINNED.format(q=query), [], f"pinned-{E.today()}-{hashlib.sha1(query.encode()).hexdigest()[:6]}")
    return json.loads(sorted(C.OUT.glob("pinned-*.json"))[-1].read_text())


def pack_from_pinned(rec: dict, question: str | None) -> dict:
    """A pinned chat -> pack. The stream must show exactly one search with the pinned query, else it is refused."""
    import cardprobe as K
    m = re.search(r'word for word: "(.*?)"', rec.get("prompt") or "")
    want = m.group(1) if m else None
    x = K.decompose(rec.get("sse") or [])
    if not want or x["queries"] != [want]:
        sys.exit(f"pinned chat ran {x['queries']!r}, not [{want!r}]: drop it")
    if x["model"] and x["model"] != "gpt-6":
        print(f"warning: answered by {x['model']} (downgraded); the result list is still the search tool's", file=sys.stderr)
    if not question:
        sys.exit("a pinned chat needs --question (the shopper question the draft is scored on)")
    rs = list({r["url"]: r for r in x["results"] if r["url"]}.values())
    fetch_all([{"url": r["url"]} for r in rs])
    stored, t = Stored(), rec.get("started_at") or E.now_iso()
    results = []
    for r in rs:
        if "dealectric.com" in r["url"]:
            text, how = stored.text(r["url"], t)
        else:
            f = fetch_text(r["url"])
            text, how = f["text"], f["status"]
        results.append({"url": r["url"], "title": r.get("title") or "", "snippet": r.get("snippet") or "", "text": text,
                        "source": how, "type": r.get("type")})
    return {"question": question, "query": want, "from": f"pinned app chat {rec.get('tag')}", "app_started_at": t,
            "model": x["model"], "results": results}


def fetch_all(results: list[dict], workers: int = 8) -> None:
    todo = [r for r in results if "dealectric.com" not in r["url"]]
    with cf.ThreadPoolExecutor(workers) as ex:
        list(ex.map(lambda r: fetch_text(r["url"]), todo))


def cmd_pack(a) -> None:
    if a.cell and "sse" in json.loads(Path(a.cell).read_text()):   # a ctxprobe chat (pinned one-search)
        pack = pack_from_pinned(json.loads(Path(a.cell).read_text()), a.question)
    elif a.cell:
        cell = json.loads(Path(a.cell).read_text())
        rs = (cell.get("response") or {}).get("search_results") or []
        fetch_all([{"url": r.get("url") or ""} for r in rs])
        results = results_from_cell(cell, Stored())
        pack = {"question": a.question or cell.get("prompt"), "query": (cell.get("queries") or [""])[0], "from": a.cell,
                "app_started_at": cell.get("started_at"), "results": results}
    elif a.engine == "app":
        if not (a.query and a.question):
            sys.exit("pack needs --cell, or --query and --question")
        pack = pack_from_pinned(pinned_chat(a.query, a.name), a.question)
    else:
        if not (a.query and a.question):
            sys.exit("pack needs --cell, or --query and --question")
        key = E.env_key("OPENAI_API_KEY")
        started = E.now_iso()
        status, resp = A.post({"model": MODEL, "input": f'Run exactly one web search with this exact query, word for word: "{a.query}". '
                               "Do not search again and do not open any page. Then reply only with the word DONE.",
                               "store": False, "max_tool_calls": 1, "include": ["web_search_call.action.sources"],
                               "tools": [{"type": "web_search", "user_location": {"type": "approximate", "country": "US"}}]}, key)
        srcs = [s for it in resp.get("output", []) if it.get("type") == "web_search_call"
                for s in ((it.get("action") or {}).get("sources") or [])]
        E.footprint("openai-api", started, E.now_iso(), prompt=a.query, script="fastloop.py", run_id="fastloop",
                    retrieved=[{"url": s.get("url")} for s in srcs], error=str(resp.get("error")) if status != 200 else None)
        urls = list(dict.fromkeys(s.get("url") for s in srcs if s.get("url")))[: a.top]
        fetch_all([{"url": u} for u in urls])
        results = [{"url": u, "title": "", "snippet": "", **{k: v for k, v in fetch_text(u).items() if k == "text"},
                    "source": "api one-search"} for u in urls]
        for r in results:
            r["title"] = (r["text"].splitlines() or [""])[0][:120]
        pack = {"question": a.question, "query": a.query, "from": "api one-search", "results": results}
    d = pack_dir(a.name)
    d.mkdir(parents=True, exist_ok=True)
    E.write_json(d / "pack.json", pack)
    for i, r in enumerate(pack["results"]):
        print(f"{i:2} {len(r['text']):6}ch {r['source'][:40]:40} {r['url'][:90]}")
    print(f"pack {a.name}: {len(pack['results'])} results for {pack['query']!r}")


# ---------------------------------------------------------------- gap judge

GAP_SCHEMA = {"type": "object", "properties": {
    "sources": {"type": "array", "items": {"type": "object", "properties": {
        "n": {"type": "integer"}, "kind": {"type": "string", "enum": ["major-reviewer", "authority", "brand-store", "retailer",
                                                                        "niche-reviewer", "listicle", "forum", "spam", "off-target", "unreadable"]},
        "answers_it": {"type": "boolean"}, "why": {"type": "string"}}, "required": ["n", "kind", "answers_it", "why"]}},
    "verdict": {"type": "string", "enum": ["open", "contested", "saturated"]},
    "missing": {"type": "string"}, "why": {"type": "string"}}, "required": ["sources", "verdict", "missing", "why"]}
GAP_SYSTEM = """You judge whether a shopping search is already well answered by its results. For each numbered source:
- kind: major-reviewer (RTINGS, Wirecutter, Consumer Reports, OutdoorGearLab, TechRadar, Tom's Guide and peers that
  test products), authority (government, standards, the maker's manual or support pages), brand-store (a maker's own
  product or category page), retailer (Amazon, Best Buy, Home Depot listings), niche-reviewer (a small site that
  compares or tests with specific data), listicle (a roundup with no testing or data of its own, often AI-written or on
  a recycled domain), forum (Reddit, community Q&A), spam, off-target (about another product kind or question),
  unreadable (no text).
- answers_it: it directly answers the shopper's question with specific, checkable product information.
- why: one short phrase.
Then verdict: saturated if two or more major-reviewer or authority sources answer it well; open if no source both
answers it and comes from a major reviewer, authority or substantive niche reviewer; contested otherwise.
missing: the most important thing a shopper asking this would still need that none of the sources answer well."""


def cmd_gap(a) -> None:
    doms = collections.Counter()
    for name in a.packs:
        d = pack_dir(name)
        pack = json.loads((d / "pack.json").read_text())
        rows = []   # rivals only: the question is whether the other results already answer it
        for i, r in enumerate(r for r in pack["results"] if "dealectric.com" not in r["url"]):
            doms[E.host_of(r["url"]).removeprefix("www.")] += 1
            rows.append(f"[{i}] {r.get('title')}\nURL: {r['url']}\n{(r.get('text') or r.get('snippet') or '')[:1500]}")
        user = f"SHOPPER QUESTION: {pack['question']}\nSEARCH QUERY: {pack['query']}\n\nSOURCES:\n\n" + "\n\n".join(rows)
        g = E.claude_cli_json(GAP_SYSTEM, user, JUDGE, GAP_SCHEMA, timeout=400) or {}
        E.write_json(d / "gap.json", g)
        kinds = collections.Counter(s["kind"] for s in g.get("sources", []))
        print(f"{name}: {g.get('verdict', '?').upper()} | {dict(kinds)} | missing: {g.get('missing', '')[:160]}")
    if len(a.packs) > 1:
        print("recurring domains:", ", ".join(f"{k} {v}" for k, v in doms.most_common(12) if v > 1))


# ---------------------------------------------------------------- replay a draft

def draft_text(path: str) -> tuple[str, str]:
    raw = Path(path).read_text()
    if path.endswith(".html"):
        t = html_text(raw)
        m = re.search(r"<title>(.*?)</title>", raw, re.S)
        return (m.group(1).strip() if m else t.splitlines()[0]), t
    lines = raw.strip().splitlines()
    return lines[0].lstrip("# ").strip(), raw.strip()


def cmd_replay(a) -> None:
    d = pack_dir(a.pack)
    pack = json.loads((d / "pack.json").read_text())
    results = [dict(r) for r in pack["results"]]
    tag = a.tag or "baseline"
    if a.draft:
        title, text = draft_text(a.draft)
        url = "https://dealectric.com" + (a.url or "/draft")
        ours = next((i for i, r in enumerate(results) if E.strip_tracking(r["url"]).rstrip("/") == url.rstrip("/")), None)
        entry = {"url": url, "title": title, "text": text, "source": f"draft {a.draft}"}
        if ours is not None and a.rank is None:
            results[ours] = entry
        else:
            if ours is not None:
                results.pop(ours)
            results.insert((a.rank or 2) - 1, entry)
            results = results[: max(len(pack["results"]), a.rank or 2)]
    ctx = build_context(results, pack["query"])
    our_rank = next((i + 1 for i, r in enumerate(ctx) if "dealectric.com" in r["url"]), None)
    key = E.env_key("OPENAI_API_KEY")
    out = d / "answers" / tag
    out.mkdir(parents=True, exist_ok=True)
    E.write_json(out / "context.json", {"query": pack["query"], "our_rank": our_rank,
                                        "results": [{k: r[k] for k in ("url", "title", "share", "full_chars", "shown", "source")} for r in ctx]})

    def one(n):
        rec = respond(a.engine, pack["question"], pack["query"], ctx, a.model, key)
        rec.update(tier(rec["text"], our_rank), our_rank=our_rank, n=n, tag=tag)
        E.write_json(out / f"{n}.json", rec)
        return rec

    with cf.ThreadPoolExecutor(1 if a.engine == "app" else 3) as ex:   # one app chat at a time
        for rec in ex.map(one, range(1, a.reps + 1)):
            print(f"{tag} #{rec['n']} {rec['status']} T{rec['tier']} our_rank={our_rank} go={rec['go']} | {rec['text'][:100]!r}")
    shown = next((r["shown"] for r in ctx if "dealectric.com" in r["url"]), "")
    print(f"our page: {len(shown)} of {next((r['full_chars'] for r in ctx if 'dealectric.com' in r['url']), 0)} characters reach the model")


def cmd_score(a) -> None:
    d = pack_dir(a.pack)
    pack = json.loads((d / "pack.json").read_text())
    board = {}
    for td in sorted(p for p in (d / "answers").iterdir() if p.is_dir()):
        recs = [json.loads(p.read_text()) for p in sorted(td.glob("[0-9]*.json"))]
        recs = [r for r in recs if r.get("status") == 200]
        for r in recs:
            if "judge" not in r or (a.concern and r["judge"].get("concern") != a.concern):
                r["judge"] = {**judge(pack["question"], r["text"], a.concern), "concern": a.concern}
                E.write_json(td / f"{r['n']}.json", r)
        n = len(recs) or 1
        board[td.name] = {"n": len(recs), "T4+": sum(r["tier"] >= 4 for r in recs) / n, "go": sum(r["tier"] == 5 for r in recs) / n,
                          "our_pick": sum(bool(r["judge"].get("our_pick")) for r in recs) / n,
                          "relied_on_us": sum(bool(r["judge"].get("relied_on_us")) for r in recs) / n,
                          "point_carried": (sum(bool(r["judge"].get("point_carried")) for r in recs) / n) if a.concern else None,
                          "top_picks": collections.Counter(r["judge"].get("top_pick", "") for r in recs).most_common(3)}
    E.write_json(d / "score.json", board)
    print(f"{'draft':16} n  cited(T4+)  /go/  our pick  relied  point  top picks")
    for k, v in board.items():
        pc = "  -  " if v["point_carried"] is None else f"{v['point_carried']:.0%}"
        print(f"{k:16} {v['n']}  {v['T4+']:6.0%}  {v['go']:6.0%}  {v['our_pick']:6.0%}  {v['relied_on_us']:6.0%}  {pc:5}  "
              + "; ".join(f"{p} ×{c}" for p, c in v["top_picks"]))


# ---------------------------------------------------------------- calibration

CAL_GLOBS = ["2026-10-2[6-9]-*/chatgpt/*.json", "2026-10-3*-*/chatgpt/*.json"]


def cal_cells() -> list[Path]:
    out = []
    for g in CAL_GLOBS:
        for f in sorted(E.RUNS_DIR.glob(g)):
            try:
                c = json.loads(f.read_text())
            except ValueError:
                continue
            resp = c.get("response") or {}
            if c.get("downgraded") or not resp.get("search_results") or len(c.get("queries") or []) != 1:
                continue
            if not (c.get("text") or "").strip():
                continue
            out.append(f)
    return out


def app_outcome(c: dict) -> dict:
    import visibility_scan as V
    return V.score(c, {})


def cmd_calibrate(a) -> None:
    global ALPHA, BUDGET
    ALPHA, BUDGET = a.alpha or ALPHA, a.budget or BUDGET
    run = E.RUNS_DIR / (a.run or f"{E.today()}-fastcal")
    run.mkdir(parents=True, exist_ok=True)
    cells = cal_cells()
    ours = [f for f in cells if any("dealectric.com" in (r.get("url") or "") for r in json.loads(f.read_text())["response"]["search_results"])]
    rest = [f for f in cells if f not in ours]
    rng = random.Random(a.seed)
    n_ours = round(a.n * 0.75)
    pick = rng.sample(ours, min(n_ours, len(ours))) + rng.sample(rest, min(a.n - n_ours, len(rest)))
    print(f"{len(cells)} usable app chats ({len(ours)} with our page in the results); calibrating on {len(pick)}", flush=True)
    stored, key = Stored(), E.env_key("OPENAI_API_KEY")
    urls = {r.get("url") or "" for f in pick for r in json.loads(f.read_text())["response"]["search_results"]}
    fetch_all([{"url": u} for u in urls])

    def one(f: Path):
        p = run / f"{f.parent.parent.name}--{f.stem}.json"
        if p.exists():
            return json.loads(p.read_text())
        c = json.loads(f.read_text())
        q = c["queries"][0]
        ctx = build_context(results_from_cell(c, stored), q)
        our_rank = next((i + 1 for i, r in enumerate(ctx) if "dealectric.com" in r["url"]), None)
        reps = []
        for n in range(a.reps):
            rec = respond(a.engine, c["prompt"], q, ctx, a.model, key)
            rec.update(tier(rec["text"], our_rank))
            rec["judge"] = judge(c["prompt"], rec["text"]) if rec["status"] == 200 and not a.no_judge else {}
            reps.append(rec)
        app = {**app_outcome(c), "judge": {} if a.no_judge else judge(c["prompt"], c["text"])}
        row = {"cell": str(f.relative_to(E.RUNS_DIR)), "question": c["prompt"], "query": q, "our_rank": our_rank,
               "n_results": len(ctx), "our_source": next((r["source"] for r in ctx if "dealectric.com" in r["url"]), None),
               "unreadable": sum(1 for r in ctx if not r.get("text")), "app": app, "replays": reps, "model": a.model,
               "prompt_version": PROMPT_VERSION, "engine": a.engine, "alpha": ALPHA, "budget": BUDGET}
        E.write_json(p, row)
        return row

    with cf.ThreadPoolExecutor(1 if a.engine == "app" else a.workers) as ex:
        for i, row in enumerate(ex.map(one, pick), 1):
            ts = [r["tier"] for r in row["replays"]]
            print(f"{i:3}/{len(pick)} app T{row['app']['tier']} replay T{ts} rank={row['our_rank']} | {row['question'][:70]}", flush=True)
    print(calreport(run))


def majority(xs: list[bool]) -> bool:
    return sum(xs) * 2 > len(xs)


def calreport(run: Path) -> str:
    rows = [json.loads(p.read_text()) for p in sorted(run.glob("*.json")) if p.name != "report.json"]
    rows = [r for r in rows if r["replays"] and all(x["status"] == 200 for x in r["replays"])]
    stats = collections.defaultdict(list)
    lines = ["| app chat | our rank | app tier | replay tiers | app top pick | replay top picks |", "|---|---|---|---|---|---|"]
    for r in rows:
        app, reps = r["app"], r["replays"]
        app_used, rep_used = app["tier"] >= 4, majority([x["tier"] >= 4 for x in reps])
        app_go, rep_go = app["tier"] == 5, majority([x["tier"] == 5 for x in reps])
        atop = (app.get("judge") or {}).get("top_pick", "")
        rtops = [(x.get("judge") or {}).get("top_pick", "") for x in reps]
        abrand = ((app.get("judge") or {}).get("top_brand") or "").lower()
        rbrands = [((x.get("judge") or {}).get("top_brand") or "").lower() for x in reps]
        blind = not re.search(r"dealectric|deelectric", r["question"], re.I)   # probes that name us inflate agreement
        if r["our_rank"]:
            for sfx in ([""] + ([" (blind prompts)"] if blind else [])):
                stats["used (T4+) agrees, our page in results" + sfx].append(app_used == rep_used)
                stats["/go/ (T5) agrees, our page in results" + sfx].append(app_go == rep_go)
                stats["app used our page" + sfx].append(app_used)
                stats["replay used our page" + sfx].append(rep_used)
        if atop:
            stats["same top pick (majority of replays)"].append(majority([same_pick(atop, t) for t in rtops]))
            stats["same top-pick brand (majority)"].append(majority([bool(abrand) and abrand == b for b in rbrands]))
        stats["replay vs itself: same tier band"].append(len({x["tier"] >= 4 for x in reps}) == 1)
        lines.append(f"| {r['cell'][:60]} | {r['our_rank'] or '-'} | {app['tier']} | {[x['tier'] for x in reps]} | {atop[:30]} | "
                     f"{'; '.join(t[:24] for t in rtops)} |")
    summ = [f"{len(rows)} app chats, replayed with {rows[0]['model'] if rows else '?'} (prompt {PROMPT_VERSION}).", ""]
    summ += [f"- {k}: {sum(v)}/{len(v)} ({sum(v) / len(v):.0%})" for k, v in stats.items() if v]
    rep = "\n".join(summ + [""] + lines)
    (run / "report.md").write_text(rep + "\n")
    return "\n".join(summ)


def jacc(a: str, b: str) -> float:
    x, y = terms(a), terms(b)
    return len(x & y) / len(x | y) if x | y else 1.0


def cmd_transfer(a) -> None:
    """Does the API write the app's search query for the same shopper question? One search allowed, US location."""
    run = E.RUNS_DIR / (a.run or f"{E.today()}-transfer")
    run.mkdir(parents=True, exist_ok=True)
    byq = collections.defaultdict(list)
    for f in cal_cells():
        c = json.loads(f.read_text())
        byq[c["prompt"]].append(c["queries"][0])
    qs = random.Random(a.seed).sample(sorted(byq), min(a.n, len(byq)))
    key = E.env_key("OPENAI_API_KEY")

    def one(i_q):
        i, q = i_q
        p = run / f"{i:03d}.json"
        if p.exists():
            return json.loads(p.read_text())
        started = E.now_iso()
        status, resp = A.post({"model": a.model, "input": q, "store": False, "max_tool_calls": 1,
                               "tools": [{"type": "web_search", "user_location": {"type": "approximate", "country": "US"}}]}, key)
        api_q = next(((it.get("action") or {}).get("query") for it in resp.get("output", []) if it.get("type") == "web_search_call"), None)
        E.footprint("openai-api", started, E.now_iso(), prompt=q, script="fastloop.py", run_id=run.name, prompt_id=p.stem,
                    error=str(resp.get("error")) if status != 200 else None)
        rec = {"question": q, "app_queries": byq[q], "api_query": api_q, "status": status, "model": a.model}
        E.write_json(p, rec)
        return rec

    with cf.ThreadPoolExecutor(3) as ex:
        recs = list(ex.map(one, enumerate(qs)))
    api_app, app_app, searched = [], [], []
    for r in recs:
        searched.append(bool(r["api_query"]))
        if r["api_query"]:
            api_app.append(statistics.mean(jacc(r["api_query"], x) for x in r["app_queries"]))
        aq = r["app_queries"]
        app_app += [jacc(aq[i], aq[j]) for i in range(len(aq)) for j in range(i + 1, len(aq))]
        print(f"{(r['api_query'] or '-')[:60]:60} | app: {aq[0][:60]}")
    print(f"\n{len(recs)} questions; API searched {sum(searched)}/{len(recs)}. Query word overlap (Jaccard, ignoring 'best', "
          f"'2026', 'review'): API vs app {statistics.mean(api_app):.0%} (median {statistics.median(api_app):.0%}); "
          f"app vs app on the same question {statistics.mean(app_app) if app_app else float('nan'):.0%} ({len(app_app)} pairs).")


def cmd_calreport(a) -> None:
    print(calreport(E.RUNS_DIR / (a.run or f"{E.today()}-fastcal")))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("pack"); p.add_argument("--cell"); p.add_argument("--query"); p.add_argument("--question")
    p.add_argument("--name", required=True); p.add_argument("--top", type=int, default=12)
    p.add_argument("--engine", choices=["app", "api"], default="app")
    p = sub.add_parser("gap"); p.add_argument("packs", nargs="+")
    p = sub.add_parser("replay"); p.add_argument("pack"); p.add_argument("--draft"); p.add_argument("--url"); p.add_argument("--rank", type=int)
    p.add_argument("--reps", type=int, default=3); p.add_argument("--tag"); p.add_argument("--model", default=MODEL)
    p.add_argument("--engine", choices=["app", "api"], default="app")
    p = sub.add_parser("score"); p.add_argument("pack"); p.add_argument("--concern")
    p = sub.add_parser("calibrate"); p.add_argument("--n", type=int, default=40); p.add_argument("--reps", type=int, default=3)
    p.add_argument("--model", default=MODEL); p.add_argument("--run"); p.add_argument("--seed", type=int, default=7)
    p.add_argument("--workers", type=int, default=3); p.add_argument("--engine", choices=["app", "api"], default="app")
    p.add_argument("--no-judge", action="store_true"); p.add_argument("--alpha", type=float); p.add_argument("--budget", type=int)
    p = sub.add_parser("calreport"); p.add_argument("--run")
    p = sub.add_parser("transfer"); p.add_argument("--n", type=int, default=40); p.add_argument("--model", default=MODEL)
    p.add_argument("--run"); p.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    {"pack": cmd_pack, "gap": cmd_gap, "replay": cmd_replay, "score": cmd_score, "calibrate": cmd_calibrate,
     "calreport": cmd_calreport, "transfer": cmd_transfer}[a.cmd](a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
