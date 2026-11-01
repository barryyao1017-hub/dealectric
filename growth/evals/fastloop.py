#!/usr/bin/env python3.12
"""The ChatGPT fast loop (DLC-112, design: .claude/skills/chatgpt-discoverability/SKILL.md): score page drafts offline
against the result set ChatGPT really got, so copy iterates in minutes and only the winner waits for OpenAI's crawler.

    python3.12 growth/evals/fastloop.py pack --cell runs/<run>/chatgpt/<qid>.json --name <pack>   # from an app chat
    python3.12 growth/evals/fastloop.py pack --query "<ChatGPT's query>" --question "<shopper question>" --name <pack> [--engine api]
    python3.12 growth/evals/fastloop.py pack --cell runs/<run>/ctx/pinned-1.json --question "<q>" --name <pack>  # pinned chat
    python3.12 growth/evals/fastloop.py gap <pack> [<pack> ...]            # open or saturated, recurring domains
    python3.12 growth/evals/fastloop.py gapcheck --labels labels.json     # Barry's labels vs the judge
    python3.12 growth/evals/fastloop.py replay <pack> --draft d.md [--rank 2] [--url /slug] [--reps 3] [--tag v1]
    python3.12 growth/evals/fastloop.py check <draft.md|docs/<slug>.html> --packs <p> [<p> ...] --must "<concern phrase>"  # copy-rules gate
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

import argparse, tempfile, bisect, collections, concurrent.futures as cf, hashlib, json, os, random, re, ssl, statistics, sys, time
import urllib.parse, urllib.request
from pathlib import Path

os.environ.setdefault("AGENT_CDP", "http://localhost:9222")   # the only agent Chrome (2026-10-31)

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


def pdf_text(body: bytes) -> str:
    """Text of a PDF (manuals, FDA and airline guidance turn up in results); '' if it can't be read."""
    try:
        import io, logging, pypdf
        logging.getLogger("pypdf").setLevel(logging.ERROR)   # font-encoding warnings flood stderr
        return "\n".join((pg.extract_text() or "") for pg in pypdf.PdfReader(io.BytesIO(body)).pages).strip()
    except Exception:  # noqa: BLE001
        return ""


def fetch_text(url: str) -> dict:
    """Live text of a rival page (cached). Returns {text, status}; text is '' when the page could not be read."""
    p = cache_path(url)
    if p.exists():
        try:
            return json.loads(p.read_text())
        except ValueError:   # half-written by a concurrent run: fetch again
            p.unlink(missing_ok=True)
    started, text, status = E.now_iso(), "", "ok"
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en"})
        body = urllib.request.urlopen(req, timeout=20, context=SSL).read(8_000_000)
        text = pdf_text(body) if body[:5] == b"%PDF-" else html_text(body.decode("utf-8", "replace"))
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
        try:
            E.write_json(p, rec)
        except FileNotFoundError:   # another run cached the same page at the same moment
            pass
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


FORMATS = ("v1", "v2")   # how the result list is laid out for the replay model (growth/evals/loop/paste-calibration.md)
FMT_VERSION = os.environ.get("FASTLOOP_FMT", "v1")
CITE_START, CITE_DELIM, CITE_STOP = "\ue200", "\ue202", "\ue201"   # OpenAI's documented citation-marker tokens


def pub_date(r: dict) -> str | None:
    d = r.get("pub_date")
    if isinstance(d, (int, float)) and d > 0:
        return time.strftime("%Y-%m-%d", time.gmtime(d))
    return d if isinstance(d, str) and d else None


def context_text(ctx: list[dict], query: str, fmt: str | None = None) -> str:
    """v1: 【i】 title / URL / passages. v2: OpenAI's documented tool-output layout (developers.openai.com, Citation
    Formatting): a citation-marker line per source (turn0search<i>), Title / URL / Updated metadata, line locators."""
    fmt = fmt or FMT_VERSION
    if fmt == "v2":
        rows = [f'Search query: "{query}"']
        for i, r in enumerate(ctx):
            rows.append(f"\nCitation Marker: {CITE_START}cite{CITE_DELIM}turn0search{i}{CITE_STOP}")
            rows.append(f"Title: {r.get('title') or E.host_of(r['url'])}")
            rows.append(f"URL: {r['url']}")
            if pub_date(r):
                rows.append(f"Updated: {pub_date(r)}")
            rows += [f"[L{n}] {line}" for n, line in enumerate((x for x in r["shown"].splitlines() if x.strip()), 1)]
        return "\n".join(rows)
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
PASTES["c1"] = ("Here is a user's question, and the web search results for \"{query}\". Without doing any further web "
                "search, respond to the user's question according to these search results.\n\nUser's question: {question}\n\n"
                "Search results:\n\n{pages}")   # Barry 10-31: no link instruction, results framed as search results
PASTES["c2"] = ("You just ran a web search for \"{query}\" to answer the user's question below; these are its results. Without "
                "searching again, answer the user's question using them.\n\nUser's question: {question}\n\n"
                "Search results:\n\n{pages}")   # DLC-115 round: results framed as the model's own search, no link wording
PASTE_VERSION = os.environ.get("FASTLOOP_PASTE", "b1")


def answer_app(question: str, query: str, ctx: list[dict], text: str | None = None) -> dict:
    """The same context pasted into a Free temporary chat (agent Chrome, AGENT_CDP), search off: the real gpt-6 and the
    app's own answer program, so buttons count; no catalog cards (no search). One gpt-6 message of the Free quota each
    (~26 per account before gpt-6-mini). Driver per the fork's appfeas test: ?q= fails at this length, so insert text."""
    import ui, ctxprobe as C, cardprobe as K
    text = text or PASTES[PASTE_VERSION].format(n=len(ctx), query=query, question=question, pages=context_text(ctx, query).split("\n", 1)[1].strip())
    tab = ui.Tab("about:blank")
    tab.ws.settimeout(180)
    started, err, rec = E.now_iso(), None, {}
    try:
        tab.call("Network.enable", maxResourceBufferSize=50_000_000, maxTotalBufferSize=100_000_000)
        tab.call("Page.enable")
        tab.call("Page.addScriptToEvaluateOnNewDocument", source=K.WIDE_HOOK_JS)
        tab.navigate("https://chatgpt.com/?temporary-chat=true" + ("&hints=search" if REPLAY_SEARCH else "")
                     + (f"&model={APP_MODEL}" if APP_MODEL else ""))
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


def _click(tab, el_js: str) -> None:
    r = tab.eval(f"(() => {{ const e = ({el_js}); if (!e) return null; const b = e.getBoundingClientRect(); "
                 "return [b.x + b.width / 2, b.y + b.height / 2]; })()")
    if not r:
        raise RuntimeError(f"not found: {el_js[:80]}")
    tab.call("Input.dispatchMouseEvent", type="mouseMoved", x=r[0], y=r[1])
    tab.call("Input.dispatchMouseEvent", type="mousePressed", x=r[0], y=r[1], button="left", buttons=1, clickCount=1)
    time.sleep(0.1)
    tab.call("Input.dispatchMouseEvent", type="mouseReleased", x=r[0], y=r[1], button="left", buttons=0, clickCount=1)


def active_account(tab=None) -> str | None:
    import ui
    own = tab is None
    tab = tab or ui.Tab("about:blank")
    try:
        if own:
            tab.navigate("https://chatgpt.com/")
            time.sleep(6)
        return tab.eval("fetch('/api/auth/session').then(r => r.json()).then(j => (j.user || {}).email || null)")
    finally:
        if own:
            tab.close()


def switch_account(tried: set[str]) -> str | None:
    """Switch the profile's ChatGPT account to one in its account switcher not in `tried` (profile menu -> the account
    row -> another email; menus need real pointer events, so clicks go through Input.dispatchMouseEvent). Returns the
    new account's email, or None when every listed account was tried."""
    import ui
    tab = ui.Tab("about:blank")
    try:
        tab.call("Page.bringToFront")
        tab.navigate("https://chatgpt.com/")
        time.sleep(7)
        _click(tab, "document.querySelectorAll('[aria-label=\"Open profile menu\"]')[1]")
        time.sleep(2)
        _click(tab, "[...document.querySelectorAll('[role=menu] [role=menuitem]')].find(e => /@|Free|Plus/.test(e.innerText))")
        time.sleep(2)
        emails = tab.eval("[...new Set((document.querySelectorAll('[role=menu]')[1] || {innerText: ''}).innerText"
                          ".match(/[\\w.+-]+@[\\w-]+\\.[\\w.]+/g) || [])]") or []
        nxt = next((e for e in emails if e not in tried), None)
        if not nxt:
            return None
        _click(tab, f"[...document.querySelectorAll('[role=menu] *')].filter(e => e.innerText && e.innerText.includes('{nxt}'))"
                    ".sort((a, b) => a.innerText.length - b.innerText.length)[0]")
        time.sleep(8)
        now = active_account(tab)
        return now if now == nxt else None
    finally:
        tab.close()


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
        out.append({"url": url, "title": r.get("title") or "", "snippet": r.get("snippet") or "", "text": text, "source": how,
                    "pub_date": r.get("pub_date")})
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


# v2 (Barry, 10-31): the same labels, judged from our side, with our one proven win as a worked OPEN example. The
# example's rivals are the real result set of the 10-30 chat gap-solar--budget-1 (runs/2026-10-30-gap-vs-focus), which
# the v1 prompt called "contested".
GAP_SYSTEM_V2 = """You judge whether a shopping search is OPEN for a small comparison site, Dealectric: whether a new,
well-built page could get into ChatGPT's ~12 search results for it and become the source ChatGPT relies on and links
to. You see the shopper's question, the exact query ChatGPT searched, and the results it got (our own pages removed).

For each numbered source give:
- kind: major-reviewer (RTINGS, Wirecutter, Consumer Reports, OutdoorGearLab, Tom's Guide, TechRadar and peers that
  test products), authority (government, standards, the maker's manual or support pages), brand-store (a maker's own
  product or category page), retailer (Amazon, Best Buy, Home Depot listings), niche-reviewer (a small site that
  compares or tests with specific data), listicle (a roundup with no testing or data of its own, often AI-written or on
  a recycled domain), forum (Reddit, community Q&A), spam, off-target (about another product kind or question),
  unreadable (no text).
- answers_it: true only if this page answers THIS question, constraints included (budget, size, use), with specific,
  current, checkable product information. A famous site counts for nothing when its page is about something else: a
  deal post on one bundle, a different price band, a general category guide.
- why: one short phrase.

Then the verdict, from Dealectric's side:
- open: no major reviewer or authority answers this exact question with its own testing. The results are affiliate
  listicles, deal posts, single-brand pages, pages answering a neighbouring question, and niche sites that compare
  with specs or claim testing nobody can check. Such niche pages do not close a search: we won against three of them.
  A focused page with current prices, tested codes and a direct pick would stand out.
- contested: one major reviewer or authority answers this exact question with testing, or several answer it in part;
  a new page could get in but would compete with it.
- saturated: two or more major reviewers or authorities answer this exact question well, with testing. A new page
  would not displace them.
missing: the most important thing a shopper asking this would still need that none of the sources answer well.

WORKED EXAMPLE, our one proven win. Its label is OPEN.
Shopper question: "Best solar generator kit with panels for under $1,000?"
ChatGPT's query: "best solar generator kits with solar panels under $1000 2026 reviews prices"
Results ChatGPT got, besides our page:
[0] solargenadvisor.com, "Best Solar Generator Kits 2026: Station + Panel Bundles": affiliate roundup with scores, no
    testing shown. listicle.
[1] techradar.com, "EcoFlow's Delta 3 solar generator bundle gets a $300 price drop at Amazon": a deal post on one
    bundle. major-reviewer by name, but it does not answer the question.
[2] pwice.com, "8 Best Solar Generators Under $1000 (October 2026) Honest Reviews": affiliate roundup, no test data.
    listicle.
[3] trek4tech.com, "Best Solar Generators (2026): Six Bundles Compared on the Panel, Not the Pitch": compares
    bundles on panel output and refill time, with numbers. niche-reviewer, answers it.
[4] roversolar.com, "Best Solar Generators of 2026": compares kits (Anker C1000 + 200W) with specs and refill
    estimates; claims hands-on testing. niche-reviewer, answers it.
[5] solargenadvisor.com, "SGA Best Under $1K 2026 Award — Jackery Explorer 1000 V2": a single-product award page.
    listicle.
[6] outageoutfitter.com, "Bluetti vs EcoFlow vs Jackery vs Anker SOLIX vs Goal Zero": brand comparison, mostly
    without panels. niche-reviewer, off the kit question.
[7] powersized.com, "Portable Power Station With Solar Panel Kits: Price Guide": tracks 53 kits, kit vs separate
    prices and refill times, untested. niche-reviewer, answers it.
Why it is OPEN: no major reviewer or authority has tested kits under $1,000; the one famous name is a deal post. Three
niche sites answer it with specs and price tracking, but none with testing anyone can check, and the rest are
affiliate roundups. Our page, "Best solar generator with panels included (2026): 15 kits compared on battery,
inverter, solar input and price", with current prices and the brand's cart-tested code where one exists, ranked 1st
in both chats on this question. ChatGPT cited it both times, and once put our buy link in its answer. Searches that
look like this one are what we are looking for."""


def named_query(q: str) -> str | None:
    """The brand or model number a query names, if any. Gap scores run on general category searches only (Barry,
    10-31): a named search is an edge case whose results are the brand's own pages, so it reads as falsely open."""
    src = (Path(__file__).resolve().parents[2] / "src" / "products.py").read_text()
    brands = {b.lower() for b in re.findall(r'"brand":\s*"([^"]+)"', src)}
    words = re.findall(r"[a-z0-9][a-z0-9-]*", q.lower())
    hit = next((w for w in words if w in brands), None)
    return hit or next((w for w in words if re.search(r"[a-z]", w) and re.search(r"\d", w)
                        and not re.fullmatch(r"\d+(w|wh|mah|kwh|v|in|ft|bay|c|th|nd|rd|st|k|hz|mm)|\d+p|lifepo4|qi\d.*|usb.*|\d+-in-\d+|202\d", w)), None)


def cmd_gap(a) -> None:
    doms = collections.Counter()
    for name in a.packs:
        d = pack_dir(name)
        pack = json.loads((d / "pack.json").read_text())
        if (hit := named_query(pack.get("query") or "")) and not a.allow_named:
            print(f"{name}: skipped, query names {hit!r} (general category searches only; --allow-named to judge it)")
            continue
        rows = []   # rivals only: the question is whether the other results already answer it
        for i, r in enumerate(r for r in pack["results"] if "dealectric.com" not in r["url"]):
            doms[E.host_of(r["url"]).removeprefix("www.")] += 1
            rows.append(f"[{i}] {r.get('title')}\nURL: {r['url']}\n{(r.get('text') or r.get('snippet') or '')[:1500]}")
        system = GAP_SYSTEM_V2 if a.prompt == "v2" else GAP_SYSTEM
        if a.show:
            print(f"===== SYSTEM ({a.prompt}) =====\n{system}\n\n===== USER =====\nSHOPPER QUESTION: {pack['question']}\n"
                  f"SEARCH QUERY: {pack['query']}\n\nSOURCES:\n\n" + "\n\n".join(rows))
            return
        stem = "gap" if a.prompt == "v1" else f"gap-{a.prompt}"
        out = d / (f"{stem}.json" if a.judge == JUDGE else f"{stem}-{a.judge}.json")
        if out.exists() and not a.redo:
            g = json.loads(out.read_text())
        else:
            user = f"SHOPPER QUESTION: {pack['question']}\nSEARCH QUERY: {pack['query']}\n\nSOURCES:\n\n" + "\n\n".join(rows)
            try:
                g = E.claude_cli_json(system, user.replace("\x00", ""), a.judge, GAP_SCHEMA, timeout=600) or {}
            except Exception as e:  # noqa: BLE001
                print(f"{name}: judge failed: {str(e)[:120]}")
                continue
            E.write_json(out, g)
        kinds = collections.Counter(s["kind"] for s in g.get("sources", []))
        print(f"{name} [{a.judge}]: {g.get('verdict', '?').upper()} | {dict(kinds)} | missing: {g.get('missing', '')[:160]}")
    if len(a.packs) > 1:
        print("recurring domains:", ", ".join(f"{k} {v}" for k, v in doms.most_common(12) if v > 1))


# ---------------------------------------------------------------- the vote (Barry, 10-31)
# Judges see each result as ChatGPT's model does: the pack cut by the measured length rule (build_context: share by
# rank, long pages cut to the passages matching the query), our pages removed. They must quote each result word for
# word; quotes are checked against the text they were shown.

VOTE_SCHEMA = {"type": "object", "properties": {
    "sources": {"type": "array", "items": {"type": "object", "properties": {
        **GAP_SCHEMA["properties"]["sources"]["items"]["properties"],
        "evidence": {"type": "string"}}, "required": ["n", "kind", "answers_it", "why", "evidence"]}},
    "verdict": {"type": "string", "enum": ["open", "contested", "saturated"]},
    "missing": {"type": "string"}, "why": {"type": "string"}}, "required": ["sources", "verdict", "missing", "why"]}
VOTE_SYSTEM = GAP_SYSTEM_V2.replace(
    "You see the shopper's question, the exact query ChatGPT searched, and the results it got (our own pages removed).",
    "You see the shopper's question, the exact query ChatGPT searched, and the results it got (our own pages removed),\n"
    "each with the text ChatGPT's model was given for it: short pages whole, long ones cut to the passages matching the\n"
    "query, less text for lower ranks. Judge from that text; it is what ChatGPT reads.").replace(
    "- why: one short phrase.\n\nThen the verdict",
    "- why: one short phrase.\n- evidence: a passage copied word for word from that source's text, 8 to 30 words, that best\n"
    "  supports your answers_it label. Copy it exactly; it is checked.\n\nThen the verdict")


def squash(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", s.lower()).strip()


def vote_context(pack: dict) -> list[dict]:
    results = []
    for r in pack["results"]:
        r = dict(r)
        if (r.get("text") or "").startswith("%PDF-"):   # cached before PDF support: fetch again as text
            cache_path(r["url"]).unlink(missing_ok=True)
            r["text"] = fetch_text(r["url"])["text"]
        results.append(r)
    return [c for c in build_context(results, pack["query"]) if "dealectric.com" not in c["url"]]


def cmd_vote(a) -> None:
    jobs = []
    for name in a.packs:
        pack = json.loads((pack_dir(name) / "pack.json").read_text())
        if (hit := named_query(pack.get("query") or "")) and not a.allow_named:
            print(f"{name}: skipped, query names {hit!r}")
            continue
        ctx = vote_context(pack)
        rows = [f"[{i}] {c.get('title')}\nURL: {c['url']}\n{c['shown']}" for i, c in enumerate(ctx)]
        user = (f"SHOPPER QUESTION: {pack['question']}\nSEARCH QUERY: {pack['query']}\n\nRESULTS:\n\n" + "\n\n".join(rows)).replace("\x00", "")
        if a.show:
            print(f"===== SYSTEM =====\n{VOTE_SYSTEM}\n\n===== USER ({len(user)} chars) =====\n{user}")
            return
        jobs += [(name, pack, ctx, user, m) for m in a.judges]

    def one(job):
        name, pack, ctx, user, m = job
        out = pack_dir(name) / "vote-v2" / f"{m}.json"
        if out.exists():
            return name, m, json.loads(out.read_text())
        try:
            g = E.claude_cli_json(VOTE_SYSTEM, user, m, VOTE_SCHEMA, timeout=900) or {}
        except Exception as e:  # noqa: BLE001
            return name, m, {"error": str(e)[:200]}
        found = 0
        for s in g.get("sources", []):
            shown = squash(ctx[s["n"]]["shown"]) if 0 <= s.get("n", -1) < len(ctx) else ""
            q = squash(s.get("evidence", ""))
            s["quote_found"] = len(q) >= 20 and q in shown
            found += s["quote_found"]
        g.update(results=len(ctx), quotes_found=found, chars_shown=sum(len(c["shown"]) for c in ctx),
                 chars_full=sum(c["full_chars"] for c in ctx))
        out.parent.mkdir(parents=True, exist_ok=True)
        E.write_json(out, g)
        return name, m, g

    with cf.ThreadPoolExecutor(a.workers) as ex:
        res = list(ex.map(one, jobs))
    table = collections.defaultdict(dict)
    for name, m, g in res:
        table[name][m] = g
    for name in a.packs:
        if name not in table:
            continue
        gs = [table[name].get(m, {}) for m in a.judges]
        votes = [g.get("verdict", "err") for g in gs]
        top, k = collections.Counter(votes).most_common(1)[0]
        q = json.loads((pack_dir(name) / "pack.json").read_text())["question"]
        reads = " ".join(f"{g.get('quotes_found', '?')}/{g.get('results', '?')}" for g in gs)
        print(f"{name}  {'/'.join(v[:4] for v in votes):16} -> {top.upper() if k >= 2 else 'SPLIT':9} quotes {reads:14} | {q[:60]}", flush=True)


def cmd_gapcheck(a) -> None:
    """Barry's labels (the "Gap Judge Labels" artifact's `labels` collection, exported to --labels as {pack: {verdict}})
    against the judge's verdicts. The skill's bar: the judge agrees on about 20 queries."""
    labels = json.loads(Path(a.labels).read_text())
    rows, conf = [], collections.Counter()
    for name, lab in sorted(labels.items()):
        g = pack_dir(name) / "gap.json"
        if not (lab.get("verdict") and g.exists()):
            continue
        jv = json.loads(g.read_text()).get("verdict")
        conf[(lab["verdict"], jv)] += 1
        rows.append((name, lab["verdict"], jv, lab.get("note", "")))
    n = len(rows) or 1
    exact = sum(b == j for _, b, j, _ in rows)
    near = sum(b == j or "contested" in (b, j) for _, b, j, _ in rows)
    for name, b, j, note in rows:
        print(f"{'  ' if b == j else '≠ '}{name}  Barry {b:9}  judge {j:9}  {note[:80]}")
    print(f"\n{len(rows)} labelled: exact agreement {exact}/{len(rows)} ({exact / n:.0%}); never open-vs-saturated "
          f"{near}/{len(rows)} ({near / n:.0%}). Confusion (Barry, judge): {dict(conf)}")


# ---------------------------------------------------------------- replay a draft

def draft_text(path: str) -> tuple[str, str]:
    raw = Path(path).read_text()
    if path.endswith(".html"):
        t = html_text(raw)
        m = re.search(r"<title>(.*?)</title>", raw, re.S)
        return (m.group(1).strip() if m else t.splitlines()[0]), t
    lines = raw.strip().splitlines()
    return lines[0].lstrip("# ").strip(), raw.strip()


def _squash(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip().lower()


def cmd_check(a) -> None:
    """The copy rules' gate (growth/focus/fastloop-briefs/COPY-RULES.md, rule 6): the conversion block (a /go/ link and a
    price) sits in the first 600 characters after the title, and it and every --must phrase survive the length cut at
    each rank in every target result set. Exit 1 on any failure."""
    title, text = draft_text(a.draft)
    start = text.find("Short answer")
    if start < 0:   # no "Short answer." label: the top starts after the title line(s)
        start = text.find("\n", text.find(title[:40]) + 1) if title[:40] in text else 0
    top = text[max(start, 0): max(start, 0) + 600]
    fails = []
    top_ok = "/go/" in top and "$" in top
    print(f"top block ({len(top)} chars from {'Short answer' if text.find('Short answer') >= 0 else 'after the title'}): "
          f"/go/ link {'yes' if '/go/' in top else 'NO'}, price {'yes' if '$' in top else 'NO'}")
    if not top_ok:
        fails.append("conversion block not in the first 600 characters")
    musts = [m for m in (a.must or [])]
    ranks = [int(r) for r in a.ranks.split(",")]
    print(f"{'pack':34} {'results':>7} {'rank':>4} {'share':>6} {'shown':>6}  /go/  " + "  ".join(f"must{i + 1}" for i in range(len(musts))))
    for name in a.packs:
        pack = json.loads((pack_dir(name) / "pack.json").read_text())
        base = [dict(r) for r in pack["results"] if "dealectric.com" not in r["url"]]
        for rank in ranks:
            res = list(base)
            res.insert(min(rank, len(res) + 1) - 1, {"url": "https://dealectric.com" + (a.url or "/draft"), "title": title, "text": text})
            res = res[:max(len(pack["results"]), rank)]
            ctx = build_context(res, pack["query"])
            me = next(c for c in ctx if "dealectric.com" in c["url"])
            shown = _squash(me["shown"])
            ok_go = "/go/" in shown
            ok_m = [_squash(m) in shown for m in musts]
            if not ok_go:
                fails.append(f"{name} rank {rank}: /go/ link cut")
            fails += [f"{name} rank {rank}: '{m[:40]}' cut" for m, ok in zip(musts, ok_m) if not ok]
            print(f"{name[:34]:34} {len(ctx):>7} {rank:>4} {me['share']:>6} {len(me['shown']):>6}  {'ok  ' if ok_go else 'CUT '}  "
                  + "  ".join("ok   " if ok else "CUT  " for ok in ok_m))
    print("PASS" if not fails else "FAIL:\n- " + "\n- ".join(fails))
    if fails:
        sys.exit(1)


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

    tried = {active_account()} if a.engine == "app" else set()

    def one(n):
        if (out / f"{n}.json").exists():   # resume: keep answers already recorded
            return json.loads((out / f"{n}.json").read_text())
        rec = respond(a.engine, pack["question"], pack["query"], ctx, a.model, key)
        while a.engine == "app" and (rec.get("downgraded") or rec["status"] != 200):   # quota: next account, same chat
            new = switch_account(tried)
            if not new:
                break
            tried.add(new)
            print(f"    switched ChatGPT account to {new}", flush=True)
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
    global ALPHA, BUDGET, PASTE_VERSION
    ALPHA, BUDGET, PASTE_VERSION = a.alpha or ALPHA, a.budget or BUDGET, a.paste or PASTE_VERSION
    run = E.RUNS_DIR / (a.run or f"{E.today()}-fastcal")
    run.mkdir(parents=True, exist_ok=True)
    cells = cal_cells()
    ours = [f for f in cells if any("dealectric.com" in (r.get("url") or "") for r in json.loads(f.read_text())["response"]["search_results"])]
    rest = [f for f in cells if f not in ours]
    rng = random.Random(a.seed)
    n_ours = a.n if a.only_ours else round(a.n * 0.75)
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
            if a.engine == "app" and (rec.get("downgraded") or rec["status"] != 200):
                raise Downgraded(f"{rec.get('model')} {rec.get('error') or ''}".strip())
            rec.update(tier(rec["text"], our_rank))
            rec["judge"] = judge(c["prompt"], rec["text"]) if rec["status"] == 200 and not a.no_judge else {}
            reps.append(rec)
        app = {**app_outcome(c), "judge": {} if a.no_judge else judge(c["prompt"], c["text"])}
        row = {"cell": str(f.relative_to(E.RUNS_DIR)), "question": c["prompt"], "query": q, "our_rank": our_rank,
               "n_results": len(ctx), "our_source": next((r["source"] for r in ctx if "dealectric.com" in r["url"]), None),
               "unreadable": sum(1 for r in ctx if not r.get("text")), "app": app, "replays": reps,
               "model": "gpt-6 (app)" if a.engine == "app" else a.model,
               "prompt_version": PASTE_VERSION if a.engine == "app" else PROMPT_VERSION, "engine": a.engine,
               "alpha": ALPHA, "budget": BUDGET}
        E.write_json(p, row)
        return row

    def show(i, row):
        ts = [r["tier"] for r in row["replays"]]
        print(f"{i:3}/{len(pick)} app T{row['app']['tier']} replay T{ts} rank={row['our_rank']} | {row['question'][:70]}", flush=True)

    if a.engine == "app":   # one chat at a time; on quota, switch to the profile's next account, else stop (rerun resumes)
        strikes, tried, queue, i = 0, {active_account()}, list(pick), 0
        while queue:
            f = queue[0]
            try:
                row = one(f)
                queue.pop(0)
                i += 1
                show(i, row)
                strikes = 0
            except Downgraded as e:
                strikes += 1
                print(f"    not counted ({strikes}): {e}", flush=True)
                if strikes >= 2:
                    new = switch_account(tried)
                    if not new:
                        print(f"every account tried ({', '.join(sorted(x for x in tried if x))}) is out of gpt-6: rerun later to resume")
                        break
                    print(f"    switched ChatGPT account to {new}", flush=True)
                    tried.add(new)
                    strikes = 0
    else:
        with cf.ThreadPoolExecutor(a.workers) as ex:
            for i, row in enumerate(ex.map(one, pick), 1):
                show(i, row)
    print(calreport(run))


# ---------------------------------------------------------------- paste calibration (DLC-115)
# Metrics over answers with at least one link. Real side: in-text links + source pills (shopping-card and image links
# excluded: the replay runs with search off, so it has no cards). Replay side: every link written, plus any
# turn0search<i> citation the model writes, mapped to that result's URL.
#   M1 buy-link share: answers linking our dealectric.com/go/ link. M2 our-page share: answers linking dealectric.com.
#   M3 link share: our links / all links.
# The calibration set is stratified on real M1 (it is rare: 13 of 195 real answers), and every metric is reweighted to
# the pool's real M1 rate, so a 30-chat set can measure it. growth/evals/loop/paste-calibration.md has the rounds.

PASTECAL = E.RUNS_DIR / "2026-10-31-pastecal"
URL_RE = re.compile(r"https?://[^\s)\]>\"'】<]+")


def norm_link(u: str) -> str:
    return (u or "").split("#")[0].split("?")[0].rstrip("/.,;:")


def keep_link(u: str) -> bool:
    return bool(u) and not any(s in u for s in ("openai_catalog", "utm_medium=feed", "images.openai.com", "chatgpt.com"))


def real_links(c: dict) -> list[str]:
    resp = c.get("response") or {}
    urls = [x.get("url", "") for x in c.get("citations") or []] + [x.get("url", "") for x in c.get("cite_pills") or []]
    urls += [u.get("url", "") for u in resp.get("markup_urls") or []] + URL_RE.findall(c.get("text") or "")
    return list(dict.fromkeys(norm_link(u) for u in urls if keep_link(u)))


def replay_links(rec: dict, ctx: list[dict]) -> list[str]:
    ans = rec.get("answer") or rec.get("text") or ""
    urls = [l["url"] for l in rec.get("links") or [] if l.get("kind") in ("button", "text", "cite")] + URL_RE.findall(ans)
    urls += [ctx[int(i)]["url"] for i in re.findall(r"turn\d+search(\d+)", ans) if int(i) < len(ctx)]
    return list(dict.fromkeys(norm_link(u) for u in urls if keep_link(u)))


def link_flags(links: list[str]) -> dict:
    ours = [u for u in links if "dealectric.com" in u]
    return {"linked": bool(links), "m1": any("/go/" in u for u in ours), "m2": bool(ours), "ours": len(ours), "all": len(links)}


def pastecal_pool() -> list[Path]:
    out = []
    for f in cal_cells():
        c = json.loads(f.read_text())
        if re.search(r"dealectric|deelectric", c.get("prompt") or "", re.I):
            continue   # probes that name us
        man = f.parent.parent / "manifest.json"
        if man.exists() and re.search(r"link", json.loads(man.read_text()).get("system") or "", re.I):
            continue   # runs whose system prompt asked for links (p3iter05)
        if any("dealectric.com" in (r.get("url") or "") for r in c["response"]["search_results"]):
            out.append(f)
    return out


def pastecal_split(seed: int = 11) -> dict:
    """Stratified on real M1: two thirds of the real hand-overs plus negatives make 30 to tune on; the rest of the
    hand-overs plus 8 negatives are held out. Saved once and reused."""
    p = PASTECAL / "split.json"
    if p.exists():
        return json.loads(p.read_text())
    pool = pastecal_pool()
    pos = [f for f in pool if link_flags(real_links(json.loads(f.read_text())))["m1"]]
    neg = [f for f in pool if f not in pos]
    rng = random.Random(seed)
    rng.shuffle(pos); rng.shuffle(neg)
    rel = lambda fs: [str(f.relative_to(E.RUNS_DIR)) for f in fs]
    k = round(len(pos) * 2 / 3)   # two thirds of the real hand-overs to tune on, the rest held out
    split = {"pool": len(pool), "pool_m1": len(pos), "tune": rel(pos[:k] + neg[:30 - k]), "holdout": rel(pos[k:] + neg[30 - k:38 - k]),
             "seed": seed, "made": E.now_iso()}
    PASTECAL.mkdir(parents=True, exist_ok=True)
    E.write_json(p, split)
    return split


def answer_api_paste(question: str, query: str, ctx: list[dict], model: str, key: str) -> dict:
    """The app paste sent as a plain user message through the API (no system prompt, no tools): the API twin of the
    app engine, for cheap calibration rounds."""
    text = PASTES[PASTE_VERSION].format(n=len(ctx), query=query, question=question, pages=context_text(ctx, query).split("\n", 1)[1].strip())
    started = E.now_iso()
    for attempt in range(4):
        status, r = A.post({"model": model, "store": False, "input": text}, key)
        if status != 429:
            break
        time.sleep(10 * (attempt + 1))
    ans = "\n".join(c.get("text", "") for it in r.get("output", []) if it.get("type") == "message"
                    for c in it.get("content", []) if c.get("type") == "output_text") if status == 200 else ""
    E.footprint("openai-api", started, E.now_iso(), prompt=question, script="fastloop.py", run_id="pastecal",
                retrieved=[{"url": c["url"]} for c in ctx], error=str(r.get("error")) if status != 200 else None)
    return {"status": status, "error": r.get("error"), "text": ans, "answer": ans, "links": [], "model": model,
            "usage": r.get("usage"), "engine": "api", "started_at": started}


def answer_api_tool(question: str, query: str, ctx: list[dict], model: str, key: str) -> dict:
    """The results delivered as the output of the model's own web_search call (as ChatGPT's tool returns them), with no
    system prompt and no link wording: the closest API stand-in for a real search turn."""
    body = {"model": model, "store": False, "tool_choice": "none",
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
    ans = "\n".join(c.get("text", "") for it in r.get("output", []) if it.get("type") == "message"
                    for c in it.get("content", []) if c.get("type") == "output_text") if status == 200 else ""
    E.footprint("openai-api", started, E.now_iso(), prompt=question, script="fastloop.py", run_id="pastecal",
                retrieved=[{"url": c["url"]} for c in ctx], error=str(r.get("error")) if status != 200 else None)
    return {"status": status, "error": r.get("error"), "text": ans, "answer": ans, "links": [], "model": model,
            "usage": r.get("usage"), "engine": "apitool", "started_at": started}


def cmd_pastecal(a) -> None:
    global FMT_VERSION, PASTE_VERSION
    FMT_VERSION, PASTE_VERSION = a.fmt, a.paste
    split = pastecal_split()
    cells = split[a.set]
    eng = a.engine if a.engine == "app" or a.model == "gpt-6.1-sol" else f"{a.engine}_{a.model}"
    out = PASTECAL / f"{eng}-{a.fmt}-{a.paste}-{a.set}-r{a.rep}"
    out.mkdir(parents=True, exist_ok=True)
    stored, key = Stored(), E.env_key("OPENAI_API_KEY")
    fetch_all([{"url": r.get("url") or ""} for rel in cells for r in json.loads((E.RUNS_DIR / rel).read_text())["response"]["search_results"]])
    tried = {active_account()} if a.engine == "app" else set()
    done = 0
    for rel in cells:
        p = out / (rel.replace("/chatgpt/", "--").replace("/", "--"))
        if p.exists():
            done += 1
            continue
        c = json.loads((E.RUNS_DIR / rel).read_text())
        q = c["queries"][0]
        ctx = build_context(results_from_cell(c, stored), q)
        while True:
            rec = (answer_app(c["prompt"], q, ctx) if a.engine == "app" else answer_api_tool(c["prompt"], q, ctx, a.model, key)
                   if a.engine == "apitool" else answer_api_paste(c["prompt"], q, ctx, a.model, key))
            if a.engine == "app" and (rec.get("downgraded") or rec["status"] != 200):
                new = switch_account(tried)
                if new:
                    tried.add(new)
                    print(f"    switched ChatGPT account to {new}", flush=True)
                    continue
                print(f"every account is out of gpt-6 ({done}/{len(cells)} done): rerun after the quota resets")
                sys.exit(3)
            break
        rl, pl = real_links(c), replay_links(rec, ctx)
        E.write_json(p, {"cell": rel, "question": c["prompt"], "query": q, "set": a.set, "fmt": a.fmt, "paste": a.paste,
                         "engine": a.engine, "rep": a.rep, "our_rank": next((i + 1 for i, r in enumerate(ctx) if "dealectric.com" in r["url"]), None),
                         "real": {"links": rl, **link_flags(rl)}, "replay": {"links": pl, **link_flags(pl)},
                         "rec": {k: rec.get(k) for k in ("status", "model", "answer", "links", "error", "started_at")}})
        done += 1
        f = link_flags(pl)
        print(f"{done:3}/{len(cells)} real m1={link_flags(rl)['m1']:d} m2={link_flags(rl)['m2']:d} | replay m1={f['m1']:d} m2={f['m2']:d} "
              f"links={f['all']} | {c['prompt'][:60]}", flush=True)
    print(f"done: {out.name}")


def pastecal_metrics(rows: list[dict], side: str, p_pop: float, n_pos: int, n_neg: int) -> dict:
    """Population-weighted M1/M2/M3 over linked answers: each real-M1 stratum reweighted to the pool's base rate."""
    w = {True: p_pop / max(n_pos, 1), False: (1 - p_pop) / max(n_neg, 1)}
    W = lambda r: w[r["real"]["m1"]]
    lk = [r for r in rows if r[side]["linked"]]
    tot = sum(W(r) for r in lk) or 1
    m1 = sum(W(r) for r in lk if r[side]["m1"]) / tot
    m2 = sum(W(r) for r in lk if r[side]["m2"]) / tot
    m3 = sum(W(r) * r[side]["ours"] for r in lk) / (sum(W(r) * r[side]["all"] for r in lk) or 1)
    return {"linked": len(lk), "of": len(rows), "m1": m1, "m2": m2, "m3": m3}


def cmd_reaskreport(a) -> None:
    """Ground-truth repeatability: each live re-ask (search on) against the recorded chat it repeats (`orig`)."""
    qs = {q["qid"]: q for q in json.loads(Path(a.questions).read_text())["questions"]}
    rows = []
    for f in sorted((E.RUNS_DIR / a.run / "chatgpt").glob("*.json")):
        c = json.loads(f.read_text())
        q = qs.get(c.get("qid")) or qs.get(f.stem.rsplit("-", 1)[0])
        if not q or c.get("downgraded") or not (c.get("response") or {}).get("search_results"):
            continue
        o = json.loads((E.RUNS_DIR / q["orig"]).read_text())
        new, old = link_flags(real_links(c)), link_flags(real_links(o))
        ours_in = any("dealectric.com" in (r.get("url") or "") for r in c["response"]["search_results"])
        rows.append({"qid": q["qid"], "old": old, "new": new, "ours_in_results": ours_in})
    n = len(rows) or 1
    pos = [r for r in rows if r["old"]["m1"]]
    out = [f"{len(rows)} re-asks compared with their recorded chats.",
           f"- our page in the new chat's results: {sum(r['ours_in_results'] for r in rows)}/{len(rows)}",
           f"- M1 (buy link) same as the original: {sum(r['old']['m1'] == r['new']['m1'] for r in rows)}/{len(rows)}; "
           f"repeated on the {len(pos)} original hand-overs: {sum(r['new']['m1'] for r in pos)}/{len(pos)}; "
           f"new hand-overs where the original had none: {sum(r['new']['m1'] and not r['old']['m1'] for r in rows)}/{len(rows) - len(pos)}",
           f"- M2 (our page linked) same: {sum(r['old']['m2'] == r['new']['m2'] for r in rows)}/{len(rows)}; "
           f"rate original {sum(r['old']['m2'] for r in rows)}/{len(rows)}, re-ask {sum(r['new']['m2'] for r in rows)}/{len(rows)}"]
    for r in rows:
        out.append(f"  {r['qid'][:60]:60} M1 {int(r['old']['m1'])}->{int(r['new']['m1'])}  M2 {int(r['old']['m2'])}->{int(r['new']['m2'])}  ours in results {int(r['ours_in_results'])}")
    print("\n".join(out))


def cmd_pastecalreport(a) -> None:
    split = pastecal_split()
    p_pop = split["pool_m1"] / split["pool"]
    lines = [f"Pool: {split['pool']} real chats with our page in the results; real M1 base rate {p_pop:.1%}. "
             "Metrics weighted to that base rate (stratified set).", "",
             "| version | set | n | linked (replay) | M1 real | M1 replay | sens | false pos | M2 real | M2 replay | M3 real | M3 replay | per-chat M2 agree |",
             "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    runs = {}
    for d in sorted(PASTECAL.iterdir()):
        if not d.is_dir():
            continue
        rows = [json.loads(x.read_text()) for x in sorted(d.glob("*.json"))]
        rows = [r for r in rows if r["rec"]["status"] == 200]
        if not rows:
            continue
        runs[d.name] = rows
        n_pos = sum(r["real"]["m1"] for r in rows); n_neg = len(rows) - n_pos
        R = pastecal_metrics(rows, "real", p_pop, n_pos, n_neg); P = pastecal_metrics(rows, "replay", p_pop, n_pos, n_neg)
        sens = sum(r["replay"]["m1"] for r in rows if r["real"]["m1"]) / max(n_pos, 1)
        fpr = sum(r["replay"]["m1"] for r in rows if not r["real"]["m1"]) / max(n_neg, 1)
        agree = sum(r["replay"]["m2"] == r["real"]["m2"] for r in rows) / len(rows)
        lines.append(f"| {d.name.rsplit('-', 1)[0]} | {rows[0]['set']} r{rows[0]['rep']} | {len(rows)} | {P['linked']} | {R['m1']:.0%} | {P['m1']:.0%} | "
                     f"{sens:.0%} ({n_pos}) | {fpr:.0%} ({n_neg}) | {R['m2']:.0%} | {P['m2']:.0%} | {R['m3']:.0%} | {P['m3']:.0%} | {agree:.0%} |")
    # noise: same version, different reps
    base = {}
    for name, rows in runs.items():
        base.setdefault(name.rsplit("-r", 1)[0], []).append(rows)
    for v, reps in base.items():
        if len(reps) >= 2:
            A_, B_ = ({r["cell"]: r for r in reps[0]}, {r["cell"]: r for r in reps[1]})
            common = [c for c in A_ if c in B_]
            m1 = sum(A_[c]["replay"]["m1"] == B_[c]["replay"]["m1"] for c in common) / max(len(common), 1)
            m2 = sum(A_[c]["replay"]["m2"] == B_[c]["replay"]["m2"] for c in common) / max(len(common), 1)
            lines.append(f"\nNoise, {v}: two runs agree per chat on M1 {m1:.0%}, on M2 {m2:.0%} ({len(common)} chats).")
    txt = "\n".join(lines)
    (PASTECAL / "report.md").write_text(txt + "\n")
    print(txt)


# ---------------------------------------------------------------- paired calibration (Barry, 2026-11-01)
# No fixed ground truth: real chats age (0 of 5 recorded hand-overs repeated live on 11-01). Each question is asked
# live (search on) and, right after, its own result set is replayed in a fresh chat (search off), so both sides see the
# same results, pages and model. A second live ask on the first --repeat questions gives the noise floor.

PAIRED = E.RUNS_DIR / "2026-11-01-paired"
REPLAY_SEARCH = False   # paired --search: the replay chat runs in search mode too (web search on, as live)
APP_MODEL = os.environ.get("FASTLOOP_MODEL", "gpt-6")   # pin the model the Free plan answers with


def live_chat(prompt: str) -> dict:
    """One live temporary chat with search on; returns the decomposed answer plus the raw result list."""
    import ui, ctxprobe as C, cardprobe as K
    url = ("https://chatgpt.com/?temporary-chat=true&hints=search" + (f"&model={APP_MODEL}" if APP_MODEL else "")
           + "&q=" + urllib.parse.quote(prompt, safe=""))
    tab = ui.Tab("about:blank")
    tab.ws.settimeout(180)
    started, err, rec = E.now_iso(), None, {}
    try:
        tab.call("Network.enable", maxResourceBufferSize=50_000_000, maxTotalBufferSize=100_000_000)
        tab.call("Page.enable")
        tab.call("Page.addScriptToEvaluateOnNewDocument", source=K.WIDE_HOOK_JS)
        tab.navigate(url)
        time.sleep(6)
        t0 = time.time()
        C.submit(tab)
        C.wait_turn(tab, 0, t0, timeout=300)
        time.sleep(2)
        x = K.decompose(C.read_sse(tab))
        rec = {"status": 200, "answer": x["answer"], "links": x["links"], "products": x["products"], "model": x["model"],
               "queries": x["queries"], "results": x["results"]}
    except Exception as e:  # noqa: BLE001
        err = f"{type(e).__name__}: {e}"
        rec = {"status": 0, "error": err}
    finally:
        E.footprint("chatgpt-ui", started, E.now_iso(), prompt=prompt, script="fastloop.py", run_id=PAIRED.name, temporary=True,
                    retrieved=[{"url": r["url"]} for r in rec.get("results") or []], error=err, cdp=ui.CDP)
        tab.close()
    rec["started_at"] = started
    return rec


def answer_links(rec: dict, ctx: list[dict] | None = None) -> list[str]:
    """Links an app answer gave: buttons, in-text links and source pills (never shopping cards)."""
    return replay_links(rec, ctx or [])


def cmd_paired(a) -> None:
    global FMT_VERSION, PASTE_VERSION, REPLAY_SEARCH
    FMT_VERSION, PASTE_VERSION, REPLAY_SEARCH = a.fmt, a.paste, a.search
    qs = json.loads(Path(a.questions).read_text())["questions"][a.start:a.start + a.n]
    out = PAIRED / ((f"open-{a.fmt}" if a.engine == "open" else f"{a.fmt}-{a.paste}") + ("-search" if a.search else ""))
    out.mkdir(parents=True, exist_ok=True)
    stored = Stored()
    for i, q in enumerate(qs, a.start):
        p = out / f"{i:03d}.json"
        if p.exists():
            continue
        live = live_chat(q["prompt"])
        if live.get("status") != 200 or not live.get("results"):
            print(f"{i:3} live chat failed or no search: {live.get('error') or 'no results'}", flush=True)
            E.write_json(p, {"i": i, "question": q["prompt"], "live": live, "skipped": "no search"})
            continue
        query = (live.get("queries") or [q["prompt"]])[0]
        res = [r for r in live["results"] if r.get("url") and r.get("type") in (None, "search")]
        fetch_all([{"url": r["url"]} for r in res])
        cell = {"started_at": live["started_at"], "response": {"search_results": res}}
        ctx = build_context(results_from_cell(cell, stored), query)
        rep = answer_app_open(q["prompt"], query, ctx) if a.engine == "open" else answer_app(q["prompt"], query, ctx)
        live2 = live_chat(q["prompt"]) if i - a.start < a.repeat else None
        rec = {"i": i, "question": q["prompt"], "query": query, "n_results": len(ctx),
               "our_rank": next((k + 1 for k, r in enumerate(ctx) if "dealectric.com" in r["url"]), None),
               "live": {"model": live["model"], "links": answer_links(live), **link_flags(answer_links(live)), "answer": live["answer"]},
               "replay": {"model": rep.get("model"), "status": rep.get("status"), "links": replay_links(rep, ctx),
                          "searched": rep.get("queries") or [], "cards": len(rep.get("products") or {}),
                          **link_flags(replay_links(rep, ctx)), "answer": rep.get("answer")},
               "fmt": a.fmt, "paste": a.paste, "engine": a.engine,
               "open": {k: rep.get(k) for k in ("open_url", "open_fetches", "open_ua")} if a.engine == "open" else None}
        if live2 and live2.get("status") == 200:
            rec["live2"] = {"model": live2["model"], "links": answer_links(live2), **link_flags(answer_links(live2))}
        E.write_json(p, rec)
        L, R = rec["live"], rec["replay"]
        print(f"{i:3} rank={rec['our_rank']} live[{L['model']}] m1={L['m1']:d} m2={L['m2']:d} | replay[{R['model']}] m1={R['m1']:d} m2={R['m2']:d}"
              + (f" | live2 m1={rec['live2']['m1']:d} m2={rec['live2']['m2']:d}" if 'live2' in rec else "") + f" | {q['prompt'][:50]}", flush=True)
    cmd_pairedreport(a)


def cmd_pairedreport(a) -> None:
    lines = []
    for d in sorted(x for x in PAIRED.iterdir() if x.is_dir()):
        rows = [json.loads(p.read_text()) for p in sorted(d.glob("*.json"))]
        rows = [r for r in rows if "replay" in r and r["replay"].get("status") == 200]
        if not rows:
            continue
        rate = lambda side, k: sum(r[side][k] for r in rows if r[side]["linked"]) / max(sum(r[side]["linked"] for r in rows), 1)
        agree = lambda k: sum(r["live"][k] == r["replay"][k] for r in rows) / len(rows)
        rep = [r for r in rows if "live2" in r]
        noise = lambda k: sum(r["live"][k] == r["live2"][k] for r in rep) / max(len(rep), 1)
        models = collections.Counter(r["live"]["model"] for r in rows) + collections.Counter(r["replay"]["model"] for r in rows)
        lines += [f"{d.name}: {len(rows)} pairs, models {dict(models)}",
                  f"  M1 live {rate('live', 'm1'):.0%} | replay {rate('replay', 'm1'):.0%}   per-pair agreement {agree('m1'):.0%}"
                  + (f"   live vs live {noise('m1'):.0%} ({len(rep)})" if rep else ""),
                  f"  M2 live {rate('live', 'm2'):.0%} | replay {rate('replay', 'm2'):.0%}   per-pair agreement {agree('m2'):.0%}"
                  + (f"   live vs live {noise('m2'):.0%} ({len(rep)})" if rep else "")]
    print("\n".join(lines) or "no paired rows yet")


# ---- open engine (DLC-115 step 5): the result set served as an unlisted page that ChatGPT opens with its own tool,
# so the text arrives as tool output instead of the user's message. Pages live in D1 replay_pages (Worker /x/<id>).

OPEN_PROMPT = ("Open {url} . It holds the web search results for \"{query}\". Without running a new web search, answer the "
               "user's question using those results.\n\nUser's question: {question}")


def d1(sql_file: str | None = None, command: str | None = None) -> str:
    import subprocess
    env = {**os.environ, "CLOUDFLARE_API_TOKEN": subprocess.run(["security", "find-generic-password", "-a", "dealectric", "-s",
                                                                 "cloudflare-workers-token", "-w"], capture_output=True, text=True).stdout.strip()}
    args = ["npx", "--yes", "wrangler", "d1", "execute", "dealectric", "--remote", "--json"] + (["--file", sql_file] if sql_file else ["--command", command])
    return subprocess.run(args, capture_output=True, text=True, cwd=E.REPO / "worker", env=env, timeout=180).stdout


# Host of the open-page replay (Barry, 11-01): a workers.dev name that does not say "dealectric" (worker/replay), so the
# page holding a result set cannot tilt ChatGPT toward our own result in it. FASTLOOP_REPLAY_BASE=https://dealectric.com/x
# restores the old host.
REPLAY_BASE = os.environ.get("FASTLOOP_REPLAY_BASE", "https://web-results.tesla-send-to-car.workers.dev")


def replay_page_html(ctx: list[dict], query: str) -> str:
    import html as H
    parts = [f'<!doctype html><html><head><meta charset="utf-8"><meta name="robots" content="noindex, nofollow">'
             f'<title>Search results: {H.escape(query)}</title></head><body><h1>Search results for "{H.escape(query)}"</h1>']
    for i, r in enumerate(ctx):
        lines = "".join(f"<p>{H.escape(x)}</p>" for x in r["shown"].splitlines() if x.strip())
        parts.append(f"<article><h2>[{i}] {H.escape(r.get('title') or E.host_of(r['url']))}</h2>"
                     f"<p>URL: {H.escape(r['url'])}</p>{lines}</article>")
    return "".join(parts) + "</body></html>"


def answer_app_open(question: str, query: str, ctx: list[dict]) -> dict:
    pid = hashlib.sha1(f"{question}{query}{time.time()}".encode()).hexdigest()[:24]
    sql = Path(tempfile.gettempdir()) / f"replay-{pid}.sql"
    page = replay_page_html(ctx, query).replace("'", "''")
    sql.write_text(f"INSERT INTO replay_pages (id, html, created) VALUES ('{pid}', '{page}', '{E.now_iso()}');")
    d1(sql_file=str(sql))
    url = f"{REPLAY_BASE}/{pid}"
    rec = answer_app(question, query, ctx, text=OPEN_PROMPT.format(url=url, query=query, question=question))
    got = d1(command=f"SELECT fetches, last_ua FROM replay_pages WHERE id = '{pid}'")
    d1(command=f"DELETE FROM replay_pages WHERE id = '{pid}'")
    sql.unlink(missing_ok=True)
    try:
        row = json.loads(got)[0]["results"][0]
    except (ValueError, IndexError, KeyError, TypeError):
        row = {}
    rec.update(open_url=url, open_fetches=row.get("fetches"), open_ua=row.get("last_ua"), engine="app-open")
    E.footprint("chatgpt-ui", rec.get("started_at") or E.now_iso(), E.now_iso(), prompt=question, script="fastloop.py",
                run_id=PAIRED.name, temporary=True, fetched=[{"url": url}], note="replay page opened by ChatGPT-User (ours)")
    return rec


class Downgraded(Exception):
    """An app answer from gpt-6-mini (the Free quota ran out) or a failed chat: not a calibration case."""


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
    summ = [f"{len(rows)} app chats, replayed with {rows[0]['model'] if rows else '?'} (prompt {rows[0].get('prompt_version') if rows else '?'}).", ""]
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
    p = sub.add_parser("gap"); p.add_argument("packs", nargs="+"); p.add_argument("--redo", action="store_true"); p.add_argument("--allow-named", action="store_true")
    p.add_argument("--prompt", choices=["v1", "v2"], default="v2"); p.add_argument("--show", action="store_true")
    p.add_argument("--judge", default=JUDGE)
    p = sub.add_parser("vote"); p.add_argument("packs", nargs="+"); p.add_argument("--allow-named", action="store_true")
    p.add_argument("--judges", nargs="+", default=["claude-sonnet-5-5", "claude-opus-5-5", "claude-fable-5-1"])
    p.add_argument("--workers", type=int, default=6); p.add_argument("--show", action="store_true")
    p = sub.add_parser("gapcheck"); p.add_argument("--labels", required=True)
    p = sub.add_parser("check"); p.add_argument("draft"); p.add_argument("--packs", nargs="+", required=True)
    p.add_argument("--ranks", default="1,3,6"); p.add_argument("--must", action="append"); p.add_argument("--url")
    p = sub.add_parser("replay"); p.add_argument("pack"); p.add_argument("--draft"); p.add_argument("--url"); p.add_argument("--rank", type=int)
    p.add_argument("--reps", type=int, default=3); p.add_argument("--tag"); p.add_argument("--model", default=MODEL)
    p.add_argument("--engine", choices=["app", "api"], default="app")
    p = sub.add_parser("score"); p.add_argument("pack"); p.add_argument("--concern")
    p = sub.add_parser("calibrate"); p.add_argument("--n", type=int, default=40); p.add_argument("--reps", type=int, default=3)
    p.add_argument("--model", default=MODEL); p.add_argument("--run"); p.add_argument("--seed", type=int, default=7)
    p.add_argument("--workers", type=int, default=3); p.add_argument("--engine", choices=["app", "api"], default="app")
    p.add_argument("--no-judge", action="store_true"); p.add_argument("--alpha", type=float); p.add_argument("--budget", type=int)
    p.add_argument("--paste", choices=sorted(PASTES)); p.add_argument("--only-ours", action="store_true")
    p = sub.add_parser("calreport"); p.add_argument("--run")
    p = sub.add_parser("pastecal"); p.add_argument("--set", choices=["tune", "holdout"], default="tune")
    p.add_argument("--fmt", choices=FORMATS, default="v1"); p.add_argument("--paste", choices=sorted(PASTES), default="c1")
    p.add_argument("--rep", type=int, default=1); p.add_argument("--engine", choices=["app", "api", "apitool"], default="app")
    p.add_argument("--model", default="gpt-6.1-sol")
    p = sub.add_parser("pastecalreport")
    p = sub.add_parser("paired"); p.add_argument("--questions", default=str(E.REPO / "growth/focus/pastecal-reask-questions.json"))
    p.add_argument("--n", type=int, default=15); p.add_argument("--start", type=int, default=0); p.add_argument("--repeat", type=int, default=5)
    p.add_argument("--fmt", choices=FORMATS, default="v1"); p.add_argument("--paste", choices=sorted(PASTES), default="c1")
    p.add_argument("--engine", choices=["paste", "open"], default="paste"); p.add_argument("--search", action="store_true")
    p = sub.add_parser("pairedreport")
    p = sub.add_parser("reaskreport"); p.add_argument("--run", default="2026-11-01-pastecal-reask")
    p.add_argument("--questions", default=str(E.REPO / "growth/focus/pastecal-reask-questions.json"))
    p = sub.add_parser("transfer"); p.add_argument("--n", type=int, default=40); p.add_argument("--model", default=MODEL)
    p.add_argument("--run"); p.add_argument("--seed", type=int, default=7)
    a = ap.parse_args()
    {"pack": cmd_pack, "gap": cmd_gap, "replay": cmd_replay, "score": cmd_score, "calibrate": cmd_calibrate,
     "calreport": cmd_calreport, "transfer": cmd_transfer, "gapcheck": cmd_gapcheck, "vote": cmd_vote,
     "pastecal": cmd_pastecal, "pastecalreport": cmd_pastecalreport,
     "reaskreport": cmd_reaskreport, "paired": cmd_paired, "pairedreport": cmd_pairedreport, "check": cmd_check}[a.cmd](a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
