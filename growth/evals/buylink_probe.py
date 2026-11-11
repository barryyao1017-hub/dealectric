#!/usr/bin/env python3.12
"""Buy-link probe (North Star 3): when ChatGPT names our pick but links a store, why not our buy link?

One temporary chat per target page in the Agent Chrome (localhost:9222). Turn 1 is the page's plain question. If the
answer names our pick, four plain follow-ups follow, from open to specific, none suggesting an answer:
  F1 where to buy (behaviour: does our link appear when asked directly?)
  F2 how it chose the buying links (its own account)
  F3 whether any page it read had buying or price information, and how it weighed them (without naming us)
  F4 what it made of dealectric.com (named only in the last turn)
Per turn: answer text, links in the answer (DOM anchors; stream URLs only as stream_go, since retrieved page text carries our /go/ links too), search queries and results,
cite pills. Every turn goes to the footprint log.

    python3.12 growth/evals/buylink_probe.py [--targets growth/focus/buylink-probe-targets.json] [--out runs/<id>]
"""
from __future__ import annotations

import argparse, json, re, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import ui  # noqa: E402
from followup_probe import _Slice, send_turn, state  # noqa: E402

FOLLOWUPS = [
    ("F1", "If I go with the {pick}, where should I buy it?"),
    ("F2", "How did you decide which links to give me for buying it?"),
    ("F3", "Did any of the pages you looked at earlier say anything about buying it or its price? How did you weigh them?"),
    ("F4", "One of the pages in your search results was dealectric.com. What did you make of that page?"),
]
ANCHORS_JS = r"""JSON.stringify([...document.querySelectorAll('main a[href]')].map(a => [a.href, (a.innerText||'').trim().slice(0,60)])
  .filter(([h]) => !/^https:\/\/(chatgpt\.com|openai\.com|help\.openai)/.test(h)))"""
URL_RE = re.compile(r'https?://[^\s"\\)<>\]]+')


def clean(pick: str) -> str:
    return re.sub(r",\s*buy on Amazon$", "", pick).strip()


def tokens(pick: str):
    w = re.findall(r"[A-Za-z0-9+\-]+", pick)
    return [x.lower() for x in w[1:] if len(x) > 1][:2] or [w[0].lower()]


def ours(urls):
    return sorted({u for u in urls if "dealectric.com/go/" in u or "tag=dealectric-20" in u})


def run_chat(t: dict, out: Path, nfollow: int = 4) -> dict:
    pick = clean(t["pick"])
    tab = ui.Tab("about:blank")
    rec = {"slug": t["slug"], "pick": pick, "started_at": E.now_iso(), "turns": []}
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
        rec["temporary"] = bool(s.get("temporary"))
        n, seen_a = 0, set()
        turns = [("Q", t["prompt"])] + [(k, v.format(pick=pick)) for k, v in FOLLOWUPS[:nfollow]]
        for i, (key, text) in enumerate(turns):
            started = E.now_iso()
            k = json.loads(tab.eval("String((window.__sse||[]).length)") or "0")
            err, st, tr, streams = None, {}, {}, []
            try:
                st = send_turn(tab, text, n)
                n = st["n"]
                time.sleep(2)
                streams = json.loads(tab.eval("JSON.stringify((window.__sse||[]).map(r => r.chunks.join('')))") or "[]")[k:]
                tr = ui.search_trace(_Slice(streams))
            except Exception as e:  # noqa: BLE001
                err = f"{type(e).__name__}: {e}"
            anchors = json.loads(tab.eval(ANCHORS_JS) or "[]")
            new_a = [a for a in anchors if a[0] not in seen_a]
            seen_a |= {a[0] for a in anchors}
            res = tr.get("results") or []
            res_urls = {r["url"] for r in res}
            stream_urls = sorted({u.rstrip(".,'") for s_ in streams for u in URL_RE.findall(s_)} - res_urls)
            ans = st.get("last") or ""
            row = {"turn": key, "prompt": text, "model": tr.get("model"), "queries": tr.get("queries") or [],
                   "ours_retrieved": [u for u in res_urls if "dealectric.com" in u],
                   "cite_pills": tr.get("cite_pills") or [], "anchors": new_a,
                   "our_buy_link": ours([a[0] for a in new_a]), "stream_go": ours(stream_urls), "answer": ans[:6000], "error": err}
            if key == "Q":
                row["names_pick"] = all(x in ans.lower() for x in tokens(pick))
            rec["turns"].append(row)
            E.footprint("chatgpt-ui", started, E.now_iso(), run_id=out.name, prompt_id=f"{t['slug']}:{key}", prompt=text,
                        account="signed in", temporary=rec["temporary"], cited=[c["url"] for c in row["cite_pills"] if "dealectric" in c["url"]],
                        retrieved=res, error=err, model=row["model"])
            print(f"  [{key}] model={row['model']} ours_ret={len(row['ours_retrieved'])} anchors={len(new_a)} "
                  f"buy={row['our_buy_link'][:1]} {err or ''}", flush=True)
            if err or (key == "Q" and not (row["names_pick"] and row["ours_retrieved"])):
                rec["stopped"] = err or ("pick not named" if not row.get("names_pick") else "our page not retrieved")
                break
            time.sleep(6)
        try:
            ui.screenshot(tab, out / f"{t['slug']}.jpg")
        except Exception:  # noqa: BLE001
            pass
    finally:
        tab.close()
    rec["finished_at"] = E.now_iso()
    (out / f"{t['slug']}.json").write_text(json.dumps(rec, indent=1, ensure_ascii=False))
    return rec


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--targets", default="growth/focus/buylink-probe-targets.json")
    ap.add_argument("--out", default=str(E.RUNS_DIR / f"{E.today()}-buylink-probe"))
    ap.add_argument("--only", default="")
    ap.add_argument("--suffix", default="")
    ap.add_argument("--followups", type=int, default=4, help="how many follow-ups after the question (1 = only 'where should I buy it?')")
    a = ap.parse_args()
    out = Path(a.out); out.mkdir(parents=True, exist_ok=True)
    only = set(filter(None, a.only.split(",")))
    for t in json.load(open(a.targets)):
        if only and t["slug"] not in only:
            continue
        name = t["slug"] + a.suffix
        if (out / f"{name}.json").exists():
            print(f"skip {name}"); continue
        print(name, flush=True)
        try:
            run_chat(dict(t, slug=name) if a.suffix else t, out, a.followups)
        except Exception as e:  # noqa: BLE001
            print(f"  FAILED {e}", flush=True)
        time.sleep(20)
    return 0


if __name__ == "__main__":
    sys.exit(main())
