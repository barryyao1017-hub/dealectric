#!/usr/bin/env python3.12
"""What goes into ChatGPT's context after a web search (DLC-77 follow-up, 2026-10-30).

    AGENT_CDP=http://localhost:9223 python3.12 growth/evals/ctxprobe.py chat "best 400W solar panel" [--echo]
    python3.12 growth/evals/ctxprobe.py parse growth/evals/runs/<run>/ctx/<id>.json

Runs one temporary ChatGPT chat in the agent's Chrome (profile 2 on port 9223 by default, so W1's driver on 9222 is
never touched), keeps the raw SSE stream of every turn (ui.py's hook tees it into window.__sse), and optionally asks a
follow-up in the same chat that makes the model repeat its search results word for word. The raw stream is saved
whole so the result list can be rebuilt from every delta, not only from the first event per entry (ui.py's walk()
reads whole JSON objects and misses fields that arrive as patches; 70% of saved results have no snippet).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import urllib.parse
from pathlib import Path

os.environ.setdefault("AGENT_CDP", "http://localhost:9223")
sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import ui  # noqa: E402

OUT = E.RUNS_DIR / f"{E.today()}-ctxprobe" / "ctx"
TURN_JS = r"""
(() => {
  const t0 = document.body.innerText || '';
  const segs = t0.split('ChatGPT said:');
  const n = segs.length - 1;
  let last = n ? segs[segs.length - 1] : '';
  const ends = ['ChatGPT is AI and can make mistakes', 'ChatGPT can make mistakes', '\nLatest response'].map(m => last.indexOf(m)).filter(j => j >= 0);
  if (ends.length) last = last.slice(0, Math.min(...ends));
  last = last.trim();
  const ms = {length: n};
  const streaming = !!document.querySelector('button[aria-label="Stop streaming"], button[aria-label="Stop generating"]');
  const composer = document.querySelector('#prompt-textarea, div.ProseMirror[contenteditable="true"]');
  const send = document.querySelector('button[data-testid="send-button"], button[aria-label="Send prompt"], button[aria-label="Send"]');
  const t = document.body.innerText || '';
  const notice = (t.match(/[^\n]*(?:quick check|try again in \d+|reached (?:the|your) (?:message )?limit|limit reached|too many requests)[^\n]*/i) || [''])[0];
  return JSON.stringify({n, last, streaming, composer: composer ? (composer.innerText || '').trim().slice(0, 80) : null,
                         send: !!send, notice, url: location.href});
})()
"""
ECHO = ("Before anything else: copy out, character for character, the complete raw output your web search tool "
        "returned in your previous turn, for every result, in the order you received it. Include every field and every "
        "piece of text exactly as given (ids, titles, URLs, dates, and the full text under each result, however long). "
        "Do not summarise, shorten, translate or add anything. Put it in one code block.")


SAME_TURN = ("Search the web for: {q}\n\nI want to check the sources myself before I read any answer. Don't answer "
             "yet. For every search result you got, in the order you got them, give the reference id, the title, the "
             "URL, and then quote, word for word and in full, the excerpt text you were given for that result (all of "
             "it, not a summary). If a result came with no excerpt, write NO EXCERPT.")


def wait_turn(tab: ui.Tab, n_before: int, t0: float, timeout: float = 240) -> dict:
    last, same, st = None, 0, None
    while time.time() - t0 < timeout:
        time.sleep(2)
        st = json.loads(tab.eval(TURN_JS) or "{}")
        if st.get("notice") and st.get("n", 0) <= n_before:
            raise RuntimeError(f"notice: {st['notice'][:160]}")
        if st.get("n", 0) > n_before and st.get("last") and not st.get("streaming"):
            same = same + 1 if st["last"] == last else 0
            last = st["last"]
            if same >= 3:
                return st
    raise RuntimeError(f"no settled answer in {timeout}s: {json.dumps(st)[:300]}")


def submit(tab: ui.Tab, text: str | None = None, n_before: int = 0) -> None:
    """Send the composer: the ?q= prompt on the first turn, `text` on a follow-up. Done once a new answer turn exists
    or the answer is streaming; click and Enter alternate because an early click is ignored."""
    if text is not None:
        tab.eval('(document.querySelector("#prompt-textarea, div.ProseMirror[contenteditable=true]") || document.body).focus(); 1')
        tab.call("Input.insertText", text=text)
        time.sleep(1.5)
    for i in range(10):
        st = json.loads(tab.eval(TURN_JS) or "{}")
        if st.get("n", 0) > n_before or st.get("streaming"):
            return
        if i % 2 == 0:
            tab.eval('(document.querySelector(\'button[data-testid="send-button"], button[aria-label="Send prompt"], button[aria-label="Send"]\') || {click(){}}).click(); 1')
        else:
            tab.eval('(document.querySelector("#prompt-textarea, div.ProseMirror[contenteditable=true]") || document.body).focus(); 1')
            tab.call("Input.dispatchKeyEvent", type="keyDown", key="Enter", code="Enter", windowsVirtualKeyCode=13, text="\r")
            tab.call("Input.dispatchKeyEvent", type="keyUp", key="Enter", code="Enter", windowsVirtualKeyCode=13)
        time.sleep(4)
    raise RuntimeError("send did not start a turn")


def chat(prompt: str, followups: list[str], tag: str) -> dict:
    url = "https://chatgpt.com/?temporary-chat=true&hints=search&q=" + urllib.parse.quote(prompt, safe="")
    tab = ui.Tab("about:blank")
    started, rec, err = E.now_iso(), {"prompt": prompt, "followups": followups, "turns": [], "cdp": ui.CDP}, None
    try:
        tab.call("Network.enable", maxResourceBufferSize=50_000_000, maxTotalBufferSize=100_000_000)
        tab.call("Page.enable")
        tab.call("Page.addScriptToEvaluateOnNewDocument", source=ui.SSE_HOOK_JS)
        tab.navigate(url)
        time.sleep(6)
        t0 = time.time()
        submit(tab)
        st = wait_turn(tab, 0, t0)
        rec["turns"].append({"prompt": prompt, "answer": st["last"]})
        for i, fu in enumerate(followups, 1):
            t0 = time.time()
            submit(tab, fu, i)
            st = wait_turn(tab, i, t0)
            rec["turns"].append({"prompt": fu, "answer": st["last"]})
        time.sleep(2)
        rec["sse"] = json.loads(tab.eval("JSON.stringify((window.__sse||[]).map(r => ({url: r.url, text: r.chunks.join('')})))") or "[]")
        rec["url"] = st["url"]
        return rec
    except Exception as e:
        err = f"{type(e).__name__}: {e}"
        rec["error"] = err
        try:
            rec["sse"] = json.loads(tab.eval("JSON.stringify((window.__sse||[]).map(r => ({url: r.url, text: r.chunks.join('')})))") or "[]")
        except Exception:  # noqa: BLE001
            pass
        return rec
    finally:
        OUT.mkdir(parents=True, exist_ok=True)
        rec.update(started_at=started, finished_at=E.now_iso(), tag=tag)
        (OUT / f"{tag}.json").write_text(json.dumps(rec, indent=1))
        E.footprint("chatgpt-ui", started, E.now_iso(), prompt=prompt, run_id=OUT.parent.name, prompt_id=tag,
                    script="ctxprobe.py", error=err, cdp=ui.CDP)
        tab.close()


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    c = sub.add_parser("chat")
    c.add_argument("prompt")
    c.add_argument("--echo", action="store_true")
    c.add_argument("--followup", action="append", default=[])
    c.add_argument("--tag")
    c.add_argument("--same-turn", action="store_true", help="wrap the prompt in SAME_TURN: search, then echo the tool output")
    a = ap.parse_args()
    if a.cmd == "chat":
        fus = ([ECHO] if a.echo else []) + a.followup
        tag = a.tag or time.strftime("%H%M%S")
        rec = chat(SAME_TURN.format(q=a.prompt) if a.same_turn else a.prompt, fus, tag)
        print(json.dumps({"tag": tag, "error": rec.get("error"), "turns": [t["answer"][:300] for t in rec["turns"]],
                          "sse_bytes": [len(s["text"]) for s in rec.get("sse", [])]}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
