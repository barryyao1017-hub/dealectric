#!/usr/bin/env python3.12
"""Follow-up probe (DLC-217): does ChatGPT search again when a shopper asks a follow-up, and with what words?

One temporary chat per gap page in the agent's Chrome (localhost:9222, background tab, via ui.py's Tab). Turn 1 is
the page's own typed query; the follow-ups are the questions the unpicked research angles answer, plus one
conversational control ("which would you pick?"). Nothing forces search (no hints=search): ChatGPT decides per turn,
as for a shopper who just types. Per turn we record ChatGPT's search queries, the results it was shown, the cite
pills and whether dealectric.com was among them (SSE stream, see ui.SSE_HOOK_JS), and every turn is logged to the
footprint log.

    python3.12 growth/evals/followup_probe.py [--only <slug>,...] [--out runs/<id>]
"""
from __future__ import annotations

import argparse
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import ui  # noqa: E402

CONTROL = "Which one would you pick if you were me?"
CHATS = [
    ("1000wh-power-station-with-400w-solar-panel-bundle", "1000 wh power station bundled with a 400 w solar panel", [
        ("A/C", "Will the Bluetti AC180 actually take the full 400W from two 200W panels? Do I wire them in series or parallel?"),
        ("B", "Is it cheaper to buy the AC180 and a second panel separately instead of the 2x200W bundle?"),
    ]),
    ("power-station-to-run-a-gas-furnace-in-an-outage", "can a portable power station run a gas furnace during a power outage and how do you connect it", [
        ("A", "Does the Bluetti power lifting or EcoFlow X-Boost mode help start the furnace blower?"),
        ("D", "I read that some furnaces run fine on a power station in pass-through mode but won't light once it switches to battery. Why does that happen?"),
        ("C", "Can I connect an Anker F3800 Plus to Anker's home backup transfer switch kit?"),
    ]),
    ("best-nas-under-500-for-plex-4k-transcoding", "best nas under $500 for plex 4k hardware transcoding", [
        ("C/D", "Can the Synology DS225+ do hardware transcoding in Plex?"),
        ("B", "Is the N150 in the TerraMaster F2-425 Plus noticeably better for transcoding than the N100 in the UGREEN DXP2800?"),
        ("E", "How much power does the UGREEN DXP2800 use at idle?"),
    ]),
    ("kvm-switch-for-a-mac-and-pc-4k-144hz", "which kvm switch holds 4k 144 hz between a macbook pro and a gaming pc on one monitor", [
        ("C", "I have a 2021 M1 Pro MacBook Pro. Can it send 4K 144Hz through one of these KVMs?"),
        ("A/B", "Do DisplayPort 1.4 KVM switches really do 4K 144Hz, or is that only with compression?"),
    ]),
    ("best-iphone-case-with-wallet", "iphone case with wallet", [
        ("A", "Which of these has the strongest magnet so the wallet doesn't slide off in my pocket?"),
        ("E", "How much weight does a wallet case add to the phone?"),
        ("C", "Do any of them come in iPhone 18 Pro size yet?"),
    ]),
    ("new-over-ear-headphones-with-mic", "over ear headphones with mic", [
        ("A/B", "How many hours of calls do I get per charge on the Jabra Evolve3 85 versus the Sony WH-1000XM6?"),
        ("C", "Does the Sony WH-1000XM6 mic work when it's plugged into my PC with the cable?"),
    ]),
    ("best-cassette-deck", "best cassette deck", [
        ("C", "Can the TEAC W-1200 record on metal tapes with Dolby noise reduction?"),
        ("A/E", "How does the TEAC W-1200's wow and flutter compare with a vintage Nakamichi deck?"),
    ]),
    ("new-electric-cooler-for-camping", "electric coolers for camping", [
        ("B", "How many days would a Dometic CFX5 45 run on a 1000Wh power station in summer heat?"),
        ("E", "Is Anker's battery life claim for the EverFrost 2 realistic?"),
    ]),
]

TURN_JS = r"""
(() => {
  // 11-09: the DOM no longer carries data-message-author-role; count the "ChatGPT said:" markers (as ui.READ_JS does)
  const t = document.body.innerText || '';
  const parts = t.split('ChatGPT said:');
  const n = parts.length - 1;
  let last = n ? parts[parts.length - 1] : '';
  const ends = ['ChatGPT is AI and can make mistakes', 'ChatGPT can make mistakes', 'For safety, we may keep a copy'].map(m => last.indexOf(m)).filter(j => j >= 0);
  if (ends.length) last = last.slice(0, Math.min(...ends));
  last = last.trim();
  const msgs = {length: n};
  const streaming = !!document.querySelector('button[aria-label="Stop streaming"], button[aria-label="Stop generating"], button[data-testid="stop-button"]');
  const composer = document.querySelector('#prompt-textarea, div.ProseMirror[contenteditable="true"]');
  const send = document.querySelector('button[data-testid="send-button"], button[aria-label="Send prompt"], button[aria-label="Send"]');
  const notice = (t.match(/[^\n]*(?:quick check|try again in \d+|reached (?:the|your) (?:message )?limit|limit reached|too many requests)[^\n]*/i) || [''])[0];
  return JSON.stringify({n: msgs.length, last, streaming, composer: composer ? (composer.innerText || '').trim().slice(0, 80) : null,
                         send: !!send, notice, logged_in: !!document.querySelector('button[aria-label="Open profile menu"]'),
                         temporary: t.includes('Temporary chat')});
})()
"""


class _Slice:
    """Feeds ui.search_trace only the SSE streams of one turn."""
    def __init__(self, streams):
        self.streams = streams

    def eval(self, js):
        return json.dumps(self.streams)


def state(tab):
    raw = tab.eval(TURN_JS)
    return json.loads(raw) if raw else {}


def send_turn(tab, text: str, n_before: int, timeout: int = 240) -> dict:
    tab.eval('(document.querySelector("#prompt-textarea, div.ProseMirror[contenteditable=true]") || document.body).focus(); "f"')
    tab.call("Input.insertText", text=text)
    t0, sent, last, same, s = time.time(), 0, None, 0, {}
    while time.time() - t0 < timeout:
        time.sleep(2)
        s = state(tab)
        if s.get("notice"):
            raise RuntimeError(f"notice: {s['notice'][:140]}")
        if s.get("n", 0) <= n_before:
            if s.get("composer") and s.get("send") and sent < 6 and (time.time() - t0) > 2 * (sent + 1):
                if sent % 2 == 0:
                    tab.eval('document.querySelector(\'button[data-testid="send-button"], button[aria-label="Send prompt"], button[aria-label="Send"]\').click(); "s"')
                else:
                    tab.call("Input.dispatchKeyEvent", type="keyDown", key="Enter", code="Enter", windowsVirtualKeyCode=13, text="\r")
                    tab.call("Input.dispatchKeyEvent", type="keyUp", key="Enter", code="Enter", windowsVirtualKeyCode=13)
                sent += 1
            continue
        if s["last"] and not s["streaming"]:
            same = same + 1 if s["last"] == last else 0
            last = s["last"]
            if same >= ui.SETTLE_POLLS:
                return s
    raise RuntimeError(f"no settled answer in {timeout}s (n={s.get('n')}, streaming={s.get('streaming')})")


def run_chat(slug: str, first: str, followups: list, out: Path) -> dict:
    turns = [("Q", first)] + followups + [("control", CONTROL)]
    tab = ui.Tab("about:blank")
    rec = {"slug": slug, "started_at": E.now_iso(), "turns": []}
    try:
        tab.call("Network.enable", maxResourceBufferSize=50_000_000, maxTotalBufferSize=100_000_000)
        tab.call("Page.enable")
        tab.call("Page.addScriptToEvaluateOnNewDocument", source=ui.SSE_HOOK_JS)
        tab.navigate("https://chatgpt.com/?temporary-chat=true")
        for _ in range(30):
            time.sleep(1)
            s = state(tab)
            if s.get("composer") is not None:
                break
        rec["account"] = "signed in" if s.get("logged_in") else "logged out"
        rec["temporary"] = bool(s.get("temporary"))
        n = 0
        for angle, text in turns:
            started = E.now_iso()
            k = json.loads(tab.eval("String((window.__sse||[]).length)") or "0")
            err, st, tr = None, {}, {}
            try:
                st = send_turn(tab, text, n)
                n = st["n"]
                time.sleep(1)
                streams = json.loads(tab.eval("JSON.stringify((window.__sse||[]).map(r => r.chunks.join('')))") or "[]")
                tr = ui.search_trace(_Slice(streams[k:]))
            except Exception as e:  # noqa: BLE001
                err = f"{type(e).__name__}: {e}"
            res = tr.get("results") or []
            t = {"angle": angle, "prompt": text, "searched": bool(tr.get("queries")), "queries": tr.get("queries") or [],
                 "n_results": len(res), "results": res,
                 "ours_retrieved": [r["url"] for r in res if "dealectric.com" in r["url"]],
                 "ours_cited": [c["url"] for c in (tr.get("cite_pills") or []) if "dealectric.com" in c["url"]],
                 "cite_pills": tr.get("cite_pills") or [], "model": tr.get("model"), "answer": (st.get("last") or "")[:4000],
                 "error": err}
            rec["turns"].append(t)
            E.footprint("chatgpt-ui", started, E.now_iso(), run_id=out.name, prompt_id=f"{slug}:{angle}", prompt=text,
                        account=rec["account"], temporary=rec["temporary"], cited=t["ours_cited"], retrieved=res, error=err,
                        model=t["model"])
            print(f"  [{angle}] searched={t['searched']} q={t['queries'][:3]} ours_ret={len(t['ours_retrieved'])} "
                  f"ours_cited={len(t['ours_cited'])} {err or ''}", flush=True)
            if err:
                break
            time.sleep(4)
        try:
            ui.screenshot(tab, out / f"{slug}.jpg")
        except Exception:  # noqa: BLE001
            pass
    finally:
        tab.close()
    rec["finished_at"] = E.now_iso()
    (out / f"{slug}.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False))
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--only", default="")
    ap.add_argument("--out", default=str(E.RUNS_DIR / f"{E.today()}-followups"))
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    only = set(filter(None, a.only.split(",")))
    for slug, first, fus in CHATS:
        if only and slug not in only:
            continue
        if (out / f"{slug}.json").exists():
            print(f"skip {slug} (done)"); continue
        print(slug, flush=True)
        try:
            run_chat(slug, first, fus, out)
        except Exception as e:  # noqa: BLE001
            print(f"  FAILED {e}", flush=True)
        time.sleep(8)
    return 0


if __name__ == "__main__":
    sys.exit(main())
