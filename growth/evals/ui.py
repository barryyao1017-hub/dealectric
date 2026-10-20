#!/usr/bin/env python3.12
"""Ask the eval questions in the consumer apps through the agent's Chrome (DevTools protocol on localhost:9222) and
save run files in the same shape as run.py's, so grade.py and report.py treat an app like any other assistant.
This is the loop's primary reading since 2026-10-20 (Barry: shoppers use the apps, not the APIs).

    python3.12 growth/evals/ui.py --app chatgpt --loop --iteration 1 --n 2
    python3.12 growth/evals/ui.py --app chatgpt --questions Q04,Q25 --tiers B,C --n 1 --run-id 2026-10-20-iter01

Apps: chatgpt = chatgpt.com logged out with web search on (?hints=search&q=...; no account needed; a lighter model
than paying users get, so a floor). claude-ai, gemini, grok: once their logins exist in agent-vault (DLC-40).

Each prompt gets a fresh tab (fresh chat, no memory), the answer is read from the DOM when it stops changing, and
every <a href> in the answer is recorded as a citation; ad links (oppref/olref/utm_source=oa) are dropped. Records
carry ui: true and no text_urls, so grade.py scores only real hyperlinks (a /go/ URL shown as plain text is
PLAIN_TEXT, not L4). Start the browser first: uv --directory ~/Desktop/agent-vault run agent-vault browser
"""
from __future__ import annotations

import argparse
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

CDP = "http://localhost:9222"
APPS = {
    "chatgpt": {"model": "chatgpt.com logged-out, web search on", "ua_bucket": "openai"},
}
ANSWER_TIMEOUT = 180
SHOT_MAX_H = 4000         # px; full-page screenshot of the finished chat, saved as <qid>-<tier>-<n>.jpg next to the run file
SHOT_QUALITY = 70
SETTLE_POLLS = 3          # consecutive 2 s polls with identical text before the answer counts as finished
AD_RE = re.compile(r"[?&](oppref|olref)=|utm_source=oa\b", re.I)
APP_HOST_RE = re.compile(r"^https?://([a-z0-9-]+\.)*(chatgpt\.com|openai\.com|oaiusercontent\.com)(/|$)", re.I)
BLOCK_RE = re.compile(r"verify you are human|too many requests|unusual activity|please log in to continue|sign up or log in to continue", re.I)

READ_JS = r"""
(() => {
  const t = document.body.innerText || '';
  const i = t.indexOf('ChatGPT said:');
  const j = t.indexOf('ChatGPT is AI and can make mistakes');
  const answer = i >= 0 ? t.slice(i + 'ChatGPT said:'.length, j > i ? j : undefined).trim() : '';
  const streaming = !!document.querySelector('button[aria-label="Stop streaming"], button[aria-label="Stop generating"]');
  const links = [...document.querySelectorAll('a[href]')].map(a => ({text: (a.textContent || '').trim().slice(0, 120), href: a.href, rel: a.rel || ''}));
  return JSON.stringify({streaming, answer, links, url: location.href, title: document.title, body_len: t.length,
                         login_wall: !!document.querySelector('[data-testid="login-button"]') && answer === ''});
})()
"""


# ---------------------------------------------------------------- minimal CDP client

class Tab:
    def __init__(self, url: str = "about:blank"):
        req = urllib.request.Request(f"{CDP}/json/new?{urllib.parse.quote(url, safe=':/?&=')}", method="PUT")
        self.info = json.loads(urllib.request.urlopen(req, timeout=10).read())
        self.ws = websocket.create_connection(self.info["webSocketDebuggerUrl"], timeout=30, suppress_origin=True)
        self._id = 0

    def call(self, method: str, **params):
        self._id += 1
        self.ws.send(json.dumps({"id": self._id, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self._id:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

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
                urllib.request.urlopen(f"{CDP}/json/close/{self.info['id']}", timeout=10).read()
            except Exception:
                pass


def browser_ok() -> str | None:
    try:
        v = json.loads(urllib.request.urlopen(f"{CDP}/json/version", timeout=5).read())
        return v.get("Browser")
    except Exception:
        return None


# ---------------------------------------------------------------- one prompt

def ask_chatgpt(prompt: str, shot_path: Path | None = None) -> dict:
    url = "https://chatgpt.com/?hints=search&q=" + urllib.parse.quote(prompt, safe="")
    tab = Tab("about:blank")
    try:
        tab.navigate(url)
        t0 = time.time()
        last, same, state = None, 0, None
        while time.time() - t0 < ANSWER_TIMEOUT:
            time.sleep(2)
            try:
                raw = tab.eval(READ_JS)
            except RuntimeError:
                continue
            state = json.loads(raw) if raw else None
            if not state:
                continue
            if state["answer"] and BLOCK_RE.search(state["answer"][:400]):
                raise RuntimeError(f"blocked: {state['answer'][:120]}")
            if state["answer"] and not state["streaming"]:
                same = same + 1 if state["answer"] == last else 0
                last = state["answer"]
                if same >= SETTLE_POLLS:
                    break
            elif not state["answer"] and time.time() - t0 > 60 and BLOCK_RE.search(state.get("title", "") + " " + (state.get("body_len") and "" or "")):
                raise RuntimeError("blocked before answering")
        if not state or not state["answer"]:
            raise RuntimeError(f"no answer within {ANSWER_TIMEOUT}s (url {state['url'] if state else url})")
        finished = same >= SETTLE_POLLS
        shot = screenshot(tab, shot_path) if shot_path else None
        links = [l for l in state["links"] if not APP_HOST_RE.match(l["href"]) and not AD_RE.search(l["href"])]
        cites = [{"url": l["href"], "title": l["text"], "source": "ui_href"} for l in links]
        return {"model": APPS["chatgpt"]["model"], "request": {"url": url, "method": "fresh tab, auto-submitted via ?q="},
                "response": {"final_url": state["url"], "title": state["title"], "links_all": state["links"], "answer": state["answer"]},
                "text": state["answer"], "citations": cites, "raw_citations": links, "consulted": [], "queries": [],
                "stop_reason": "settled" if finished else "timeout", "usage": None, "ui": True, "screenshot": shot,
                "notes": ["chatgpt.com logged out, agent Chrome via CDP, hrefs from the DOM"] + ([] if finished else ["answer still changing at timeout"]),
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
        record.update(ASKERS[app](prompt, out.with_suffix(".jpg")))
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
    ap.add_argument("--loop", action="store_true", help="the loop subset (10 rotated questions) like run.py --loop")
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
    loop_info = None
    if args.loop:
        if args.iteration is None:
            raise SystemExit("--loop needs --iteration N")
        recent, d1err = E.d1_recent_ai_fetch_slugs(7)
        if d1err:
            R.log(f"slug rotation without D1 ({d1err}); rotating by iteration number only")
        picked = R.pick_loop_questions(q, offers, recent, args.iteration)
        q = {**q, "questions": picked}
        loop_info = {"recent_ai_fetch_slugs": recent, "d1_error": d1err,
                     "questions": [{"id": x["id"], "primary": x["primary"], "fresh": x["fresh"]} for x in picked]}
        R.log("loop subset: " + ", ".join(f"{x['id']}={x['primary']}{'' if x['fresh'] else '*'}" for x in picked))
    cells = list(E.iter_cells(q, tiers=tiers, question_ids=qids, controls=not args.no_controls, controls_all_tiers=args.loop))
    R.log(f"ui run {args.run_id}: app {args.app}, {len(cells)} prompts x {args.n} = {len(cells) * args.n} chats")
    if args.dry_run:
        for rec, tier, prompt in cells:
            R.log(f"  {rec['id']}-{tier}  {prompt}")
        return 0
    b = browser_ok()
    if not b:
        raise SystemExit("no browser on localhost:9222; start it: uv --directory ~/Desktop/agent-vault run agent-vault browser")
    stamp = E.stamp(args.iteration, args.gsc_indexed, args.bing_indexed)
    R.log(f"browser {b}; stamp: iteration={stamp['iteration']} commit={(stamp['site_commit'] or '?')[:10]} worker={stamp['worker_version'] or '?'}")

    manifest_path = E.run_dir(args.run_id) / "manifest.json"
    manifest = E.read_json(manifest_path) if manifest_path.exists() else {"run_id": args.run_id, "started_at": E.now_iso()}
    manifest.update({"assistants": sorted(set(manifest.get("assistants", [])) | {args.app}),
                     "models": {**manifest.get("models", {}), args.app: APPS[args.app]["model"]},
                     "mock": False, "tiers": sorted(set(manifest.get("tiers", [])) | set(tiers)), "n": max(manifest.get("n", 0), args.n),
                     "system": q["system"], "questions_version": q.get("version"), "stamp": stamp, "loop": loop_info or manifest.get("loop"),
                     "ui_apps": {**manifest.get("ui_apps", {}), args.app: {"browser": b, "n": args.n, "tiers": tiers}}})
    E.write_json(manifest_path, manifest)

    results = {"ok": 0, "error": 0, "exists": 0}
    jobs = [(rec, tier, prompt, n) for rec, tier, prompt in cells for n in range(1, args.n + 1)]
    for i, (rec, tier, prompt, n) in enumerate(jobs, 1):
        r = run_cell(args.app, rec, tier, n, prompt, args.run_id, stamp, args.pause)
        results[r["status"]] += 1
        tag = r["path"].relative_to(E.RUNS_DIR)
        if r["status"] == "error":
            R.log(f"[{i}/{len(jobs)}] ERROR {tag}: {str(r['error'])[:160]}")
        elif r["status"] == "ok":
            R.log(f"[{i}/{len(jobs)}] ok    {tag} ({r['latency']}s)")
    manifest["finished_at"] = E.now_iso()
    manifest["calls"] = manifest.get("calls", 0) + results["ok"] + results["error"]
    manifest["last_results"] = results
    E.write_json(manifest_path, manifest)
    R.log(f"done: {results['ok']} ok, {results['error']} errors, {results['exists']} already present -> {E.run_dir(args.run_id)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
