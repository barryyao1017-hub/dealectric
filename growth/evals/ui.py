#!/usr/bin/env python3.12
"""Ask the eval questions in the consumer apps through the agent's Chrome (DevTools protocol on localhost:9222) and
save run files in the same shape as run.py's, so grade.py and report.py treat an app like any other assistant.
This is the loop's primary reading since 2026-10-20 (Barry: shoppers use the apps, not the APIs).

    python3.12 growth/evals/ui.py --app chatgpt --loop --iteration 1 --n 2
    python3.12 growth/evals/ui.py --app chatgpt --questions Q04,Q25 --tiers B,C --n 1 --run-id 2026-10-20-iter01

Apps: chatgpt = chatgpt.com with web search on (?temporary-chat=true&hints=search&q=...). Works logged out (the
prompt auto-submits; lighter model) and signed in (the prompt fills the composer and the driver clicks Send; the
account's plan is recorded per run file). Temporary chat means no memory and nothing saved to the account's history.
claude-ai, gemini, grok: once their logins exist in agent-vault (DLC-40).

Each prompt gets a fresh tab (fresh chat, no memory), the answer is read from the DOM when it stops changing, and
every <a href> in the answer is recorded as a citation; ad links (oppref/olref/utm_source=oa) are dropped. Records
carry ui: true and no text_urls, so grade.py scores only real hyperlinks (a /go/ URL shown as plain text is
PLAIN_TEXT, not L4). Since 2026-10-23 each record also carries ChatGPT's own web-search queries (`queries`) and the
result list it was shown (`response.search_results`), read from the SSE answer stream (see SSE_HOOK_JS); run.py's
API records have carried `queries` since the start. Start the browser first:
uv --directory ~/Desktop/agent-vault run agent-vault browser
"""
from __future__ import annotations

import argparse
import os
import base64
import json
import re
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path

import websocket  # websocket-client

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import run as R  # noqa: E402  (loop subset picker, log)

# AGENT_CDP picks the Chrome instance: 9222 is the agent's main profile (ChatGPT account 1); 9223 is a second profile
# (~/.config/agent-vault/chrome-profile-2, ChatGPT account 2) so two sessions can run chats at once. Cookies are per
# profile, so one profile can only be signed in to one ChatGPT account at a time (2026-10-25).
CDP = os.environ.get("AGENT_CDP", "http://localhost:9222")
APPS = {
    "chatgpt": {"model": "chatgpt.com, temporary chat, web search on", "ua_bucket": "openai"},
}
ANSWER_TIMEOUT = 180
SHOT_MAX_H = 4000         # px; full-page screenshot of the finished chat, saved as <qid>-<tier>-<n>.jpg next to the run file
SHOT_QUALITY = 70
SETTLE_POLLS = 3          # consecutive 2 s polls with identical text before the answer counts as finished
AD_RE = re.compile(r"[?&](oppref|olref)=|utm_source=oa\b", re.I)
APP_HOST_RE = re.compile(r"^https?://([a-z0-9-]+\.)*(chatgpt\.com|openai\.com|oaiusercontent\.com)(/|$)", re.I)
BLOCK_RE = re.compile(r"verify you are human|too many requests|unusual activity|please log in to continue|sign up or log in to continue", re.I)
# chatgpt.com's throttle notice after many chats in a row ("We're doing a quick check to keep ChatGPT reliable. Try
# again in 13 minutes."): the driver sleeps that long and retries the cell instead of recording a failure.
THROTTLE_RE = re.compile(r"try again in (\d+) (minute|hour|second)s?", re.I)
THROTTLE_RETRIES = 3


class Throttled(RuntimeError):
    def __init__(self, wait_s: int, msg: str):
        super().__init__(msg)
        self.wait_s = wait_s

READ_JS = r"""
(() => {
  const t = document.body.innerText || '';
  const i = t.indexOf('ChatGPT said:');
  const ends = ['ChatGPT is AI and can make mistakes', 'ChatGPT can make mistakes', '\nLatest response'].map(m => t.indexOf(m, i)).filter(j => j > i);
  const j = ends.length ? Math.min(...ends) : -1;
  const answer = i >= 0 ? t.slice(i + 'ChatGPT said:'.length, j > i ? j : undefined).trim() : '';
  const streaming = !!document.querySelector('button[aria-label="Stop streaming"], button[aria-label="Stop generating"]');
  // Anchors everywhere, including shadow roots (ChatGPT's product cards render their Buy button inside a custom
  // element) and same-origin iframes; buttons that carry a URL in data attributes count too.
  const anchors = [];
  const walk = (root) => {
    try {
      root.querySelectorAll('a[href], button[data-href], [role="link"][data-href]').forEach(a => anchors.push({
        text: (a.textContent || '').trim().slice(0, 120), href: a.href || a.getAttribute('data-href') || '', rel: a.rel || '',
        where: root === document ? 'dom' : 'shadow'}));
      root.querySelectorAll('*').forEach(el => { if (el.shadowRoot) walk(el.shadowRoot); });
      root.querySelectorAll('iframe').forEach(f => { try { if (f.contentDocument) walk(f.contentDocument); } catch (e) {} });
    } catch (e) {}
  };
  walk(document);
  const links = anchors.filter(a => a.href);
  const shadow_hosts = [...document.querySelectorAll('*')].filter(el => el.shadowRoot).length;
  const composer = document.querySelector('#prompt-textarea, div.ProseMirror[contenteditable="true"]');
  const send = document.querySelector('button[data-testid="send-button"], button[aria-label="Send prompt"], button[aria-label="Send"]');
  const loggedIn = !!document.querySelector('button[aria-label="Open profile menu"]') && !document.querySelector('[data-testid="login-button"]');
  const notice = (t.match(/[^\n]*(?:quick check|try again in \d+|reached (?:the|your) (?:message )?limit|limit reached|too many requests)[^\n]*/i) || [''])[0];
  const plan = (t.match(/\n(Free|Plus|Pro|Go|Business)\n/) || [])[1] || '';
  return JSON.stringify({streaming, answer, links, url: location.href, title: document.title, body_len: t.length,
                         composer: composer ? (composer.innerText || '').trim().slice(0, 80) : null, send: !!send, notice,
                         logged_in: loggedIn, plan, temporary: t.includes('Temporary chat'), shadow_hosts});
})()
"""


# ---------------------------------------------------------------- minimal CDP client

def browser_call(method: str, **params):
    """One command on the browser-level DevTools socket (the URL in /json/version); a fresh connection each time."""
    v = json.loads(urllib.request.urlopen(f"{CDP}/json/version", timeout=10).read())
    ws = websocket.create_connection(v["webSocketDebuggerUrl"], timeout=30, suppress_origin=True)
    try:
        ws.send(json.dumps({"id": 1, "method": method, "params": params}))
        while True:
            msg = json.loads(ws.recv())
            if msg.get("id") == 1:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})
    finally:
        ws.close()


class Tab:
    """A fresh tab opened in the background. /json/new and /json/close count as user actions and bring Chrome's window
    to the front on every chat (Barry, 2026-10-22: the Mac was unusable during a run), so the tab is created with
    Target.createTarget(background=true) on the browser socket, driven over its own page socket, and closed with
    Target.closeTarget. Nothing here calls Page.bringToFront."""

    def __init__(self, url: str = "about:blank"):
        self.target_id = browser_call("Target.createTarget", url=url, background=True)["targetId"]
        self.info = None
        for _ in range(50):   # the page target appears in /json/list a moment after creation
            for t in json.loads(urllib.request.urlopen(f"{CDP}/json/list", timeout=10).read()):
                if t.get("id") == self.target_id and t.get("webSocketDebuggerUrl"):
                    self.info = t
            if self.info:
                break
            time.sleep(0.1)
        if not self.info:
            raise RuntimeError("new background tab not found in /json/list")
        self.ws = websocket.create_connection(self.info["webSocketDebuggerUrl"], timeout=30, suppress_origin=True)
        self._id = 0
        self.responses: dict[str, dict] = {}   # requestId -> {url, mimeType} from Network.responseReceived (Network.enable first)

    def call(self, method: str, **params):
        self._id += 1
        self.ws.send(json.dumps({"id": self._id, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self._id:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})
            if msg.get("method") == "Network.responseReceived":
                r = msg["params"]["response"]
                self.responses[msg["params"]["requestId"]] = {"url": r.get("url", ""), "mimeType": r.get("mimeType", "")}

    def body(self, request_id: str) -> str:
        try:
            return self.call("Network.getResponseBody", requestId=request_id).get("body", "") or ""
        except Exception:
            return ""

    def eval(self, js: str):
        r = self.call("Runtime.evaluate", expression=js, returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in r:
            raise RuntimeError(f"JS: {r['exceptionDetails'].get('text')}")
        return r.get("result", {}).get("value")

    def navigate(self, url: str):
        self.call("Page.navigate", url=url)

    def close(self):
        try:
            self.ws.close()
        finally:
            try:
                browser_call("Target.closeTarget", targetId=self.target_id)
            except Exception:
                pass


def browser_ok() -> str | None:
    try:
        v = json.loads(urllib.request.urlopen(f"{CDP}/json/version", timeout=5).read())
        return v.get("Browser")
    except Exception:
        return None


# ---------------------------------------------------------------- one prompt

GENUI_URL_RE = re.compile(r"""GenUI\.openUrl\(\s*["']([^"']+)["']""")
MD_LINK_RE = re.compile(r"\[([^\]]*)\]\((https?://[^)\s]+)\)")
HREF_RE = re.compile(r"""<a\b[^>]*href=["']([^"']+)["'][^>]*>(.*?)</a>""", re.I | re.S)
CONV_ID_RE = re.compile(r'"conversation_id"\s*:\s*"([0-9a-f-]{36})"')

# Installed on every new document before chatgpt.com loads (Page.addScriptToEvaluateOnNewDocument): tees the SSE
# answer stream (POST /backend-api/f/conversation) into window.__sse so it can be read back whole once the answer has
# settled. Network.getResponseBody returns nothing for that streaming response, and the conversation JSON fetched
# afterwards (GET /backend-api/conversation/<id>) has the search queries stripped (the web.run call's parts are
# empty), so the stream is the only place ChatGPT's own search queries ("search_model_queries") and the result list
# it was shown ("search_result_group") can be read (DLC-51, 2026-10-23).
SSE_HOOK_JS = r"""
(() => {
  window.__sse = [];
  const of = window.fetch;
  window.fetch = async function(input, init) {
    const url = typeof input === 'string' ? input : (input && input.url) || '';
    const resp = await of.apply(this, arguments);
    try {
      if (/backend-api\/f\/conversation(\?|$)/.test(url) && resp.body) {
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


def search_trace(tab: Tab) -> dict:
    """ChatGPT's web searches for this chat, from the SSE stream captured by SSE_HOOK_JS: {"queries": [the strings
    ChatGPT sent to its search backend, in order, deduplicated], "results": [{domain, title, url, pub_date} for every
    search result it was shown, deduplicated by URL], "note"}. Both are empty when the chat did not search."""
    # Since 2026-10-28 also "cite_pills" (the source pills under a sentence, e.g. "Dealectric +1": the Cite component's
    # items and the cite genui_components' safe_urls; neither is an <a href> in the DOM nor in the conversation markup,
    # so before this a page we were cited by showed up in no record) and "models" (resolved_model_slug: Free plans fall
    # back to a smaller model after a quota, silently, and the answers change with it). "model" is the last
    # resolved_model_slug, the one that wrote the answer: on 2026-10-28 the Free plan answered with gpt-6-mini while
    # model_slug still said gpt-6 (gpt-6 for 28 chats, mini ~1 h, gpt-6 for 49, then mini again).
    out = {"queries": [], "results": [], "cite_pills": [], "models": [], "model": None, "note": None}
    seen_c = set()

    def pill(u, label=None, title=None):
        u = E.strip_tracking(u or "")
        if u and u not in seen_c:
            seen_c.add(u)
            out["cite_pills"].append({"url": u, "label": (label or "")[:80] or None, "title": (title or "")[:200] or None})
    try:
        raw = tab.eval("JSON.stringify((window.__sse||[]).map(r => r.chunks.join('')))")
        streams = json.loads(raw) if raw else []
    except Exception as e:  # noqa: BLE001
        out["note"] = f"sse read failed: {e}"[:160]
        return out
    if not streams:
        out["note"] = "no SSE stream captured (queries unknown)"
        return out
    seen_q, seen_u = set(), set()

    def walk(o):
        if isinstance(o, dict):
            if o.get("type") == "search_model_queries":
                for q in o.get("queries") or []:
                    if isinstance(q, str) and q not in seen_q:
                        seen_q.add(q); out["queries"].append(q)
            elif o.get("type") == "search_result_group":
                for e in o.get("entries") or []:
                    u = E.strip_tracking(e.get("url") or "")
                    if u and u not in seen_u:
                        seen_u.add(u)
                        # snippet since 2026-10-28 (DLC-77): with the title, it is all ChatGPT reads of a page it
                        # does not fetch, and it comes from OpenAI's stored copy, not the live page
                        out["results"].append({"domain": (o.get("domain") or "").removeprefix("www."), "title": (e.get("title") or "")[:200],
                                               "url": u, "pub_date": e.get("pub_date"),
                                               "snippet": (e.get("snippet") or e.get("text") or "")[:600] or None})
            if o.get("componentName") == "Cite":
                for it in ((o.get("state") or {}).get("items") or []):
                    if isinstance(it, dict):
                        pill(it.get("url"), it.get("source_label"), it.get("title"))
            if o.get("type") == "cite":
                for s in o.get("safe_urls") or []:
                    pill(s.get("url") if isinstance(s, dict) else s)
            ms = o.get("resolved_model_slug") or o.get("model_slug")
            if isinstance(ms, str) and ms not in out["models"]:
                out["models"].append(ms)
            if isinstance(o.get("resolved_model_slug"), str):   # the model that actually answered (model_slug can
                out["model"] = o["resolved_model_slug"]           # still name the plan's default while mini answers)
            for v in o.values():
                walk(v)
        elif isinstance(o, list):
            for v in o:
                walk(v)

    for text in streams:
        for line in text.split("\n"):
            s = line[5:].strip() if line.startswith("data:") else ""
            if s.startswith("{"):
                try:
                    walk(json.loads(s))
                except ValueError:
                    continue
    return out


def conversation_markup(tab: Tab) -> dict:
    """The assistant's answer as ChatGPT's own markup, from the conversation JSON the page fetched
    (/backend-api/conversation/<id>). Since 2026-10-22 ChatGPT answers shopping prompts with "dil" widget markup
    (model_dil_v2): product cards whose Buy button is `<button onClick={() => GenUI.openUrl("https://dealectric.com/
    go/...")}>`. The URL is not an <a href> anywhere in the DOM, yet the shopper's click opens it, so the DOM read
    alone undercounts L4. Returns {"parts": [...], "urls": [{url, text, source}], "conversation_id", "note"}."""
    out = {"parts": [], "urls": [], "conversation_id": None, "note": None}
    tab.eval("1")   # drain pending Network events
    bodies = []
    for rid, r in list(tab.responses.items()):
        if re.search(r"/backend-api/conversation/[0-9a-f-]{36}", r["url"]):
            b = tab.body(rid)
            if b.startswith("{"):
                bodies.append((r["url"], b))
    if not bodies:
        # The GET by id is issued by the page after generation; if it was missed, find the id in the SSE stream and fetch.
        cid = None
        for rid, r in list(tab.responses.items()):
            if r["url"].rstrip("/").endswith("/backend-api/f/conversation") or r["url"].rstrip("/").endswith("/backend-api/conversation"):
                m = CONV_ID_RE.search(tab.body(rid))
                if m:
                    cid = m.group(1); break
        if cid:
            try:
                b = tab.eval(f"fetch('/backend-api/conversation/{cid}', {{credentials: 'include'}}).then(r => r.text())")
                if b and b.startswith("{"):
                    bodies.append((f"/backend-api/conversation/{cid}", b))
            except Exception as e:  # noqa: BLE001
                out["note"] = f"conversation fetch failed: {e}"[:160]
    if not bodies:
        out["note"] = out["note"] or "no conversation JSON captured (DOM links only)"
        return out
    url, body = bodies[-1]
    try:
        d = json.loads(body)
    except ValueError:
        out["note"] = "conversation JSON unparseable"
        return out
    out["conversation_id"] = d.get("conversation_id")
    mapping = d.get("mapping") or {}
    # Walk the current branch from the leaf up to the last user message; keep assistant text parts in order.
    node = mapping.get(d.get("current_node"))
    chain = []
    while node:
        m = node.get("message") or {}
        if (m.get("author") or {}).get("role") == "user":
            break
        chain.append(m)
        node = mapping.get(node.get("parent"))
    seen = set()
    for m in reversed(chain):
        c = m.get("content") or {}
        if (m.get("author") or {}).get("role") != "assistant" or c.get("content_type") != "text":
            continue
        for p in c.get("parts") or []:
            if isinstance(p, str) and p.strip() and p not in seen:
                seen.add(p); out["parts"].append(p)
    text = "\n".join(out["parts"])
    for m in GENUI_URL_RE.finditer(text):
        out["urls"].append({"url": m.group(1), "text": "widget button", "source": "widget_button"})
    for m in MD_LINK_RE.finditer(text):
        out["urls"].append({"url": m.group(2), "text": m.group(1)[:120], "source": "markup_link"})
    for m in HREF_RE.finditer(text):
        out["urls"].append({"url": m.group(1), "text": re.sub(r"<[^>]+>", "", m.group(2))[:120], "source": "markup_link"})
    return out


def ask_chatgpt(prompt: str, shot_path: Path | None = None, fp: dict | None = None) -> dict:
    """One temporary chat (see _ask_chatgpt), logged to the footprint log (evallib.footprint) whether it answers or
    fails. `fp` adds run_id / prompt_id / script; without it they come from shot_path (runs/<run>/chatgpt/<cell>.jpg)."""
    fp = dict(fp or {})
    if shot_path is not None and not fp.get("run_id"):
        try:
            rel = Path(shot_path).resolve().relative_to(E.RUNS_DIR)
            fp.setdefault("run_id", rel.parts[0])
            fp.setdefault("prompt_id", Path(shot_path).stem)
        except ValueError:
            fp.setdefault("prompt_id", Path(shot_path).stem)
    started, r, err = E.now_iso(), {}, None
    try:
        r = _ask_chatgpt(prompt, shot_path)
        return r
    except Exception as e:
        err = f"{type(e).__name__}: {e}"
        raise
    finally:
        E.footprint("chatgpt-ui", started, E.now_iso(), prompt=prompt, account=r.get("account"), temporary=r.get("temporary_chat"),
                    cited=[r.get("citations"), r.get("cite_pills")], model=r.get("models"), retrieved=(r.get("response") or {}).get("search_results"), error=err,
                    conversation_id=(r.get("response") or {}).get("conversation_id"), cdp=CDP, **fp)


def _ask_chatgpt(prompt: str, shot_path: Path | None = None) -> dict:
    # temporary-chat: no memory, not saved to the account's history (signed-in state). hints=search forces the
    # web-search tool. Logged out, ?q= auto-submits; signed in, it only fills the composer and we click Send.
    url = "https://chatgpt.com/?temporary-chat=true&hints=search&q=" + urllib.parse.quote(prompt, safe="")
    tab = Tab("about:blank")
    try:
        tab.call("Network.enable", maxResourceBufferSize=50_000_000, maxTotalBufferSize=100_000_000)
        tab.call("Page.enable")
        tab.call("Page.addScriptToEvaluateOnNewDocument", source=SSE_HOOK_JS)
        tab.navigate(url)
        t0 = time.time()
        last, same, state, submitted, account, temporary, polls, trace = None, 0, None, 0, None, None, 0, []
        while time.time() - t0 < ANSWER_TIMEOUT:
            time.sleep(2)
            polls += 1
            try:
                raw = tab.eval(READ_JS)
            except Exception as e:  # noqa: BLE001  (a transient eval failure must not end the wait)
                trace.append({"t": round(time.time() - t0, 1), "eval_error": str(e)[:120]})
                continue
            state = json.loads(raw) if raw else None
            if not state:
                continue
            trace.append({"t": round(time.time() - t0, 1), "url": state["url"][:60], "answer_len": len(state["answer"]),
                          "streaming": state["streaming"], "send": state.get("send"), "composer": (state.get("composer") or "")[:30]})
            if account is None and state.get("body_len", 0) > 200:
                account = ("signed in" + (f" ({state['plan']})" if state.get("plan") else "")) if state.get("logged_in") else "logged out"
            if temporary is None and state.get("composer") is not None:
                temporary = bool(state.get("temporary"))   # the label disappears once the chat starts
            if not state["answer"] and state.get("composer") and _squash(prompt[:20]) in _squash(state["composer"]) and state.get("send") \
                    and polls % 2 == 1:
                # Signed in: the prompt sits in the composer until Send is pressed. A click too early does nothing
                # (React not attached, link chip still resolving), so retry every ~4 s, alternating click and Enter.
                if submitted % 2 == 0:
                    tab.eval('document.querySelector(\'button[data-testid="send-button"], button[aria-label="Send prompt"], button[aria-label="Send"]\').click(); "sent"')
                else:
                    tab.eval('(document.querySelector("#prompt-textarea, div.ProseMirror[contenteditable=true]") || document.body).focus(); "focused"')
                    tab.call("Input.dispatchKeyEvent", type="keyDown", key="Enter", code="Enter", windowsVirtualKeyCode=13, text="\r")
                    tab.call("Input.dispatchKeyEvent", type="keyUp", key="Enter", code="Enter", windowsVirtualKeyCode=13)
                submitted += 1
                trace.append({"t": round(time.time() - t0, 1), "submit": "click" if submitted % 2 == 1 else "enter"})
                continue
            if state["answer"] and BLOCK_RE.search(state["answer"][:400]):
                raise RuntimeError(f"blocked: {state['answer'][:120]}")
            if not state["answer"] and state.get("notice"):
                m = THROTTLE_RE.search(state["notice"])
                unit = {"minute": 60, "hour": 3600, "second": 1}[m.group(2).lower()] if m else 60
                wait = int(m.group(1)) * unit if m else 300
                raise Throttled(wait, f"throttled: {state['notice'][:140]}")
            if state["answer"] and not state["streaming"]:
                same = same + 1 if state["answer"] == last else 0
                last = state["answer"]
                if same >= SETTLE_POLLS:
                    break
            elif not state["answer"] and time.time() - t0 > 60 and BLOCK_RE.search(state.get("title", "") + " " + (state.get("body_len") and "" or "")):
                raise RuntimeError("blocked before answering")
        if not state or not state["answer"]:
            raise RuntimeError(f"no answer within {ANSWER_TIMEOUT}s (url {state['url'] if state else url}); trace: "
                               + json.dumps(trace[-6:])[:600])
        finished = same >= SETTLE_POLLS
        shot = screenshot(tab, shot_path) if shot_path else None
        links = [l for l in state["links"] if not APP_HOST_RE.match(l["href"]) and not AD_RE.search(l["href"])]
        cites = [{"url": l["href"], "title": l["text"], "source": "ui_href"} for l in links]
        markup = conversation_markup(tab)
        searches = search_trace(tab)
        have = {E.strip_tracking(c["url"]) for c in cites}
        for u in markup["urls"]:
            if not APP_HOST_RE.match(u["url"]) and not AD_RE.search(u["url"]) and E.strip_tracking(u["url"]) not in have:
                have.add(E.strip_tracking(u["url"]))
                cites.append({"url": u["url"], "title": u["text"], "source": u["source"]})
        n_widget = sum(u["source"] == "widget_button" for u in markup["urls"])
        return {"model": APPS["chatgpt"]["model"], "request": {"url": url, "method": "fresh tab, auto-submitted via ?q="},
                "response": {"final_url": state["url"], "title": state["title"], "links_all": state["links"], "answer": state["answer"],
                             "markup": markup["parts"], "markup_urls": markup["urls"], "conversation_id": markup["conversation_id"],
                             "search_results": searches["results"]},
                "text": state["answer"], "citations": cites, "raw_citations": links, "consulted": [], "queries": searches["queries"],
                "cite_pills": searches["cite_pills"], "models": searches["models"], "answer_model": searches["model"],
                "stop_reason": "settled" if finished else "timeout", "usage": None, "ui": True, "screenshot": shot,
                "account": account, "temporary_chat": bool(temporary), "trace": trace,
                "notes": [f"chatgpt.com {account or '?'}, {'temporary chat' if temporary else 'regular chat'}, "
                          f"{f'submitted after {submitted} send attempt(s)' if submitted else 'auto-submitted'}, agent Chrome via CDP, "
                          f"hrefs from the DOM plus the answer markup ({n_widget} widget button(s)); "
                          f"{len(searches['queries'])} search query(ies) and {len(searches['results'])} search result(s) from the SSE stream"
                          + (f"; {markup['note']}" if markup["note"] else "") + (f"; {searches['note']}" if searches["note"] else "")]
                         + ([] if finished else ["answer still changing at timeout"]),
                "latency_s": round(time.time() - t0, 1)}
    finally:
        tab.close()


def screenshot(tab: Tab, path: Path) -> str | None:
    """Full-page JPEG of the finished chat (capped at SHOT_MAX_H px), saved next to the run file for the iteration
    report. Returns the file name, or None when the capture failed (the run file still counts)."""
    try:
        # Park the pointer and close any hover popover (a citation chip under the cursor opens a sources card that
        # covers the answer), then let the layout settle.
        tab.call("Input.dispatchMouseEvent", type="mouseMoved", x=2, y=2)
        tab.call("Input.dispatchKeyEvent", type="keyDown", key="Escape", code="Escape", windowsVirtualKeyCode=27)
        tab.call("Input.dispatchKeyEvent", type="keyUp", key="Escape", code="Escape", windowsVirtualKeyCode=27)
        time.sleep(0.5)
        m = tab.call("Page.getLayoutMetrics")
        cs = m.get("cssContentSize") or m.get("contentSize") or {}
        clip = {"x": 0, "y": 0, "width": cs.get("width") or 1200, "height": min(cs.get("height") or 900, SHOT_MAX_H), "scale": 1}
        r = tab.call("Page.captureScreenshot", format="jpeg", quality=SHOT_QUALITY, captureBeyondViewport=True, clip=clip)
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(base64.b64decode(r["data"]))
        return path.name
    except Exception as e:  # noqa: BLE001
        R.log(f"screenshot failed for {path.name}: {e}")
        return None


def _squash(s: str) -> str:
    return re.sub(r"\s+", "", s or "")


ASKERS = {"chatgpt": ask_chatgpt}


# ---------------------------------------------------------------- driver

def run_cell(app: str, rec: dict, tier: str, n: int, prompt: str, run_id: str, stamp: dict, pause: float) -> dict:
    out = E.run_file(run_id, app, rec["id"], tier, n)
    if out.exists():
        return {"status": "exists", "path": out}
    started = E.now_iso()
    record = {"run_id": run_id, "assistant": app, "qid": rec["id"], "kind": rec["kind"], "tier": tier, "n": n,
              "prompt": prompt, "system": None, "expected": rec.get("expected", []), "primary": rec.get("primary"),
              "expect_domains": rec.get("expect_domains", []), "started_at": started, "stamp": stamp}
    try:
        for attempt in range(THROTTLE_RETRIES + 1):
            try:
                record.update(ASKERS[app](prompt, out.with_suffix(".jpg")))
                break
            except Throttled as t:
                if attempt == THROTTLE_RETRIES:
                    raise
                R.log(f"{app}: {t}; waiting {t.wait_s + 30}s before retrying {rec['id']}-{tier}-{n}")
                record.setdefault("throttle_waits", []).append({"at": E.now_iso(), "wait_s": t.wait_s + 30, "notice": str(t)})
                time.sleep(t.wait_s + 30)
        record["error"] = None
    except Exception as e:
        record.update({"model": APPS[app]["model"], "request": None, "response": None, "text": "", "citations": [], "raw_citations": [],
                       "consulted": [], "queries": [], "stop_reason": None, "usage": None, "ui": True, "notes": [], "latency_s": None,
                       "error": f"{type(e).__name__}: {e}"})
    record["finished_at"] = E.now_iso()
    record["text_urls"] = []   # on purpose: only real hyperlinks count in the app reading
    record["all_urls"] = sorted({c["url"] for c in record["citations"]})
    E.write_json(out, record)
    time.sleep(pause)
    return {"status": "error" if record["error"] else "ok", "path": out, "error": record["error"], "latency": record.get("latency_s")}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--app", default="chatgpt", choices=sorted(APPS))
    ap.add_argument("--tiers", default="B,C")
    ap.add_argument("--questions", default="")
    ap.add_argument("--no-controls", action="store_true")
    ap.add_argument("--n", type=int, default=1)
    ap.add_argument("--n-by-tier", default="", help="per-tier runs, e.g. B=1 (other tiers keep --n)")
    ap.add_argument("--controls", default="full", choices=["full", "lite", "none"],
                    help="lite: one positive control on A and the negative controls on the highest link tier, once each")
    ap.add_argument("--loop-k", type=int, default=10, help="questions in the loop subset (with --questions the pool is those ids)")
    ap.add_argument("--loop", action="store_true", help="the loop subset (10 rotated questions) like run.py --loop")
    ap.add_argument("--coded", action="store_true", help="phase 2: only questions whose product carries a code (see run.py --coded)")
    ap.add_argument("--phase", type=int, default=1, help="loop phase stamped on every file (2 = the discount-code hypothesis)")
    ap.add_argument("--iteration", type=int, default=None)
    ap.add_argument("--gsc-indexed", type=int, default=None)
    ap.add_argument("--bing-indexed", type=int, default=None)
    ap.add_argument("--run-id", default=E.today())
    ap.add_argument("--pause", type=float, default=5.0, help="seconds between prompts")
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    q = E.load_questions()
    offers = E.load_offers()
    tiers = [t.strip() for t in args.tiers.split(",") if t.strip()]
    qids = {s.strip() for s in args.questions.split(",") if s.strip()} or None
    coded_pool = set(E.coded_question_ids(q, offers)) if args.coded else None
    if coded_pool is not None and not args.loop:
        qids = (qids & coded_pool) if qids else coded_pool
    loop_info = None
    if args.loop:
        if args.iteration is None:
            raise SystemExit("--loop needs --iteration N")
        _mp = E.run_dir(args.run_id) / "manifest.json"
        frozen = E.frozen_loop_subset(E.read_json(_mp), q) if _mp.exists() else None
        if frozen:
            picked, recent, d1err = frozen, {}, None
            R.log("loop subset reused from the run's manifest (picked by this iteration's first run)")
        else:
            recent, d1err = E.d1_recent_ai_fetch_slugs(7)
            if d1err:
                R.log(f"slug rotation without D1 ({d1err}); rotating by iteration number only")
            pool = (coded_pool & qids) if (coded_pool is not None and qids) else (qids or coded_pool)
            picked = R.pick_loop_questions(q, offers, recent, args.iteration, k=args.loop_k, pool=pool,
                                           slugs=E.coded_slugs(offers) if args.coded else None)
        qids = None   # the subset is the question list now
        q = {**q, "questions": picked}
        loop_info = {"recent_ai_fetch_slugs": recent, "d1_error": d1err, "coded": bool(args.coded),
                     "questions": [{"id": x["id"], "primary": x["primary"], "fresh": x["fresh"]} for x in picked]}
        R.log("loop subset: " + ", ".join(f"{x['id']}={x['primary']}{'' if x['fresh'] else '*'}" for x in picked))
    cells = list(E.iter_cells(q, tiers=tiers, question_ids=qids, controls=not args.no_controls and args.controls != "none", controls_all_tiers=args.loop))
    jobs = E.plan_jobs(cells, args.n, E.parse_n_by_tier(args.n_by_tier), args.controls)
    R.log(f"ui run {args.run_id}: app {args.app}, {len(cells)} prompts, {len(jobs)} chats (n={args.n}"
          + (f", {args.n_by_tier}" if args.n_by_tier else "") + f", controls {args.controls})")
    if args.dry_run:
        for rec, tier, prompt, n in jobs:
            R.log(f"  {rec['id']}-{tier}-{n}  {prompt}")
        return 0
    b = browser_ok()
    if not b:
        raise SystemExit("no browser on localhost:9222; start it: uv --directory ~/Desktop/agent-vault run agent-vault browser")
    stamp = E.stamp(args.iteration, args.gsc_indexed, args.bing_indexed, phase=args.phase)
    R.log(f"browser {b}; stamp: iteration={stamp['iteration']} commit={(stamp['site_commit'] or '?')[:10]} worker={stamp['worker_version'] or '?'}")

    manifest_path = E.run_dir(args.run_id) / "manifest.json"
    manifest = E.read_json(manifest_path) if manifest_path.exists() else {"run_id": args.run_id, "started_at": E.now_iso()}
    manifest.update({"assistants": sorted(set(manifest.get("assistants", [])) | {args.app}),
                     "models": {**manifest.get("models", {}), args.app: APPS[args.app]["model"]},
                     "mock": False, "tiers": sorted(set(manifest.get("tiers", [])) | set(tiers)), "n": max(manifest.get("n", 0), args.n),
                     "system": q["system"], "questions_version": q.get("version"), "stamp": stamp, "loop": loop_info or manifest.get("loop"),
                     "ui_apps": {**manifest.get("ui_apps", {}), args.app: {"browser": b, "n": args.n, "n_by_tier": args.n_by_tier,
                                                                           "controls": args.controls, "tiers": tiers, "chats": len(jobs)}}})
    E.write_json(manifest_path, manifest)

    results = {"ok": 0, "error": 0, "exists": 0}
    for i, (rec, tier, prompt, n) in enumerate(jobs, 1):
        r = run_cell(args.app, rec, tier, n, prompt, args.run_id, stamp, args.pause)
        results[r["status"]] += 1
        tag = r["path"].relative_to(E.RUNS_DIR)
        if r["status"] == "error":
            R.log(f"[{i}/{len(jobs)}] ERROR {tag}: {str(r['error'])[:160]}")
        elif r["status"] == "ok":
            R.log(f"[{i}/{len(jobs)}] ok    {tag} ({r['latency']}s)")
    manifest = E.read_json(manifest_path) if manifest_path.exists() else manifest   # run.py may have written meanwhile
    manifest["finished_at"] = E.now_iso()
    manifest["calls"] = manifest.get("calls", 0) + results["ok"] + results["error"]
    manifest["last_results"] = results
    E.write_json(manifest_path, manifest)
    R.log(f"done: {results['ok']} ok, {results['error']} errors, {results['exists']} already present -> {E.run_dir(args.run_id)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
