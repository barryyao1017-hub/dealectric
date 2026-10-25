#!/usr/bin/env python3.12
"""Gap experiment stage 1 on ChatGPT (growth/gap-experiment.md, DLC-56 follow-up): does ChatGPT, finding our product
page among the results it saw, hand over our link more with the old copy addressed to AI or with the neutral page?
Same design as gapexp.py, compact so it fits ChatGPT Free's context: the coded target questions, ChatGPT's own result
set (6 sources cut to 550 words), our page (1,200 words) first. Arms OLD_COMPACT (product page before commit 12dfb2e)
and NEUTRAL_COMPACT (the published neutral page, gapexp's products-neutral snapshot). The same prompts go to Claude
(CLI) so both assistants see identical input.

    AGENT_CDP=http://localhost:9222 python3.12 growth/evals/gapexp_chatgpt.py chatgpt     # ~38 temporary chats
    python3.12 growth/evals/gapexp_chatgpt.py claude
    python3.12 growth/evals/gapexp.py grade --it 0 && python3.12 growth/evals/gapexp_chatgpt.py report

ChatGPT runs in a temporary chat without the search hint; the prompt says not to browse, and the run file records
whether it searched anyway. Answers land in gapexp's run folder (answers/it00/<model>/<Q>-<ARM>-first.json), with the
answer's link URLs appended to `text` so gapexp's grader sees them.
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import gapexp as G  # noqa: E402
import ui  # noqa: E402

SRC_WORDS, OURS_WORDS = 550, 1200
OLD_COMMIT = "43154bc"   # last commit with the AI-addressed product-page copy (12dfb2e removed it)
ARMS = ("OLD_COMPACT", "NEUTRAL_COMPACT", "TARGETED_COMPACT", "PAGE_COMPACT")
PLANS = {   # which arms run on which questions (gap pages exist only for Q01, Q02, G02, G03; drafts only for Q01-Q30)
    "old-vs-neutral": [(q, a) for q in E.load_questions()["coded_questions"] for a in ("OLD_COMPACT", "NEUTRAL_COMPACT")],
    "page-types": ([(q, "NEUTRAL_COMPACT") for q in G.QIDS + list(G.EXTRA) if q not in E.load_questions()["coded_questions"]]
                   + [(q, "TARGETED_COMPACT") for q in G.QIDS]
                   + [(q, "PAGE_COMPACT") for q in G.PAGES]),
}
PREAMBLE = ("You are a shopping assistant helping a shopper in the United States. When you recommend or name a product, "
            "give the shopper a clickable link to buy it. Do not search the web for this one: answer only from the search "
            "results pasted below, and cite the URLs you use.\n\n")


def our_page(qid: str, arm: str) -> tuple[str, str]:
    if arm == "TARGETED_COMPACT":
        return G.targeted_text(qid, 0)
    if arm == "PAGE_COMPACT":   # the gap page as published now (r5, neutral "Where to buy" block), snapshot on first use
        slug = G.PAGES[qid]
        snap = G.RUN / "pages" / "gap-r5" / f"{slug}.html"
        if not snap.exists():
            snap.parent.mkdir(parents=True, exist_ok=True)
            snap.write_text((G.ROOT / f"docs/{slug}.html").read_text())
        return f"https://dealectric.com/{slug}", G.html_text(snap.read_text())
    slug = G.questions()[qid]["primary"]
    if arm == "OLD_COMPACT":
        raw = subprocess.run(["git", "show", f"{OLD_COMMIT}:docs/{slug}.html"], capture_output=True, text=True, cwd=G.ROOT, check=True).stdout
        return f"https://dealectric.com/{slug}", G.html_text(raw)
    return G.baseline_text(qid, snapshot="products-neutral")


def prompt_for(qid: str, arm: str) -> str:
    p = G.load("packs.json", {})[qid]
    url, text = our_page(qid, arm)
    title = text.strip().split("\n")[0].strip()[:120]
    srcs = [{"title": title, "url": url, "text": G.cut(text, OURS_WORDS)}] + \
           [{"title": s["title"], "url": s["url"], "text": G.cut(s["text"], SRC_WORDS)} for s in p["sources"]]
    body = "\n\n".join(f"[{i}] {s['title']}\nURL: {s['url']}\n{s['text']}" for i, s in enumerate(srcs, 1))
    return f"{p['question']}\n\n--- Web search results for \"{p['query']}\" ---\n\n{body}"


def ask_chatgpt_pasted(prompt: str) -> dict:
    """ui.ask_chatgpt, but the prompt is inserted into the composer (too long for ?q=) and no search hint is set."""
    tab = ui.Tab("about:blank")
    try:
        tab.call("Network.enable", maxResourceBufferSize=50_000_000, maxTotalBufferSize=100_000_000)
        tab.call("Page.enable")
        tab.call("Page.addScriptToEvaluateOnNewDocument", source=ui.SSE_HOOK_JS)
        tab.navigate("https://chatgpt.com/?temporary-chat=true")
        for _ in range(30):
            time.sleep(1)
            st = json.loads(tab.eval(ui.READ_JS) or "{}")
            if st.get("composer") is not None:
                break
        tab.eval('(document.querySelector("#prompt-textarea, div.ProseMirror[contenteditable=true]") || document.body).focus(); "ok"')
        tab.call("Input.insertText", text=prompt)
        time.sleep(3)
        t0, last, same, sent, state = time.time(), None, 0, 0, None
        while time.time() - t0 < ui.ANSWER_TIMEOUT + 60:
            time.sleep(2)
            state = json.loads(tab.eval(ui.READ_JS) or "{}")
            if not state:
                continue
            if not state.get("answer") and state.get("send") and sent < 6 and time.time() - t0 > 2 * sent:
                tab.eval('document.querySelector(\'button[data-testid="send-button"], button[aria-label="Send prompt"], button[aria-label="Send"]\').click(); "sent"')
                sent += 1
                continue
            if not state.get("answer") and state.get("notice"):
                m = ui.THROTTLE_RE.search(state["notice"])
                unit = {"minute": 60, "hour": 3600, "second": 1}[m.group(2).lower()] if m else 60
                raise ui.Throttled(int(m.group(1)) * unit if m else 300, state["notice"][:140])
            if state.get("answer") and not state.get("streaming"):
                same = same + 1 if state["answer"] == last else 0
                last = state["answer"]
                if same >= ui.SETTLE_POLLS:
                    break
        if not state or not state.get("answer"):
            raise RuntimeError("no answer")
        markup = ui.conversation_markup(tab)
        searches = ui.search_trace(tab)
        urls = [l["href"] for l in state["links"] if not ui.APP_HOST_RE.match(l["href"])] + [u["url"] for u in markup["urls"]]
        return {"answer": state["answer"], "urls": list(dict.fromkeys(urls)), "queries": searches["queries"],
                "search_results": searches["results"], "account": "signed in" if state.get("logged_in") else "logged out",
                "temporary": bool(state.get("temporary")), "latency_s": round(time.time() - t0, 1)}
    finally:
        tab.close()


def coded_qids() -> list[str]:
    return [q for q in E.load_questions()["coded_questions"]]


def save(model: str, qid: str, arm: str, prompt: str, text: str, extra: dict) -> None:
    d = G.RUN / "answers/it00" / model
    d.mkdir(parents=True, exist_ok=True)
    E.write_json(d / f"{qid}-{arm}-first.json", {"qid": qid, "arm": arm, "pos": "first", "model": model, "it": 0,
                                                "prompt_words": len(prompt.split()), "text": text, **extra})


def run_chatgpt(args) -> None:
    d = G.RUN / "answers/it00/chatgpt-app"
    jobs = [(q, a) for q, a in PLANS[args.plan] if not (d / f"{q}-{a}-first.json").exists()]
    for n, (qid, arm) in enumerate(jobs, 1):
        prompt = PREAMBLE + prompt_for(qid, arm)
        for attempt in range(4):
            try:
                r = ask_chatgpt_pasted(prompt)
                break
            except ui.Throttled as t:
                print(f"throttled, waiting {t.wait_s} s: {t}", flush=True)
                time.sleep(t.wait_s + 30)
            except Exception as e:  # noqa: BLE001
                print(f"{qid} {arm}: {e}; retrying", flush=True)
                time.sleep(20)
        else:
            continue
        text = r["answer"] + "\n\nLINKS:\n" + "\n".join(r["urls"])
        save("chatgpt-app", qid, arm, prompt, text, {k: r[k] for k in ("queries", "search_results", "account", "temporary", "latency_s")})
        print(f"[{n}/{len(jobs)}] {qid} {arm}: {len(r['answer'])} chars, searched {len(r['queries'])}, dealectric/go {'yes' if 'dealectric.com/go/' in text else 'no'}", flush=True)
        time.sleep(args.pause)


def run_claude(args) -> None:
    import concurrent.futures as cf
    d = G.RUN / "answers/it00/claude-sonnet-5-5"
    jobs = [(q, a) for q, a in PLANS[args.plan] if not (d / f"{q}-{a}-first.json").exists()]

    def one(job):
        qid, arm = job
        prompt = prompt_for(qid, arm)
        save("claude-sonnet-5-5", qid, arm, prompt, G.cli_text(G.RUN_SYSTEM, prompt, "claude-sonnet-5-5"), {})
        return job

    with cf.ThreadPoolExecutor(4) as ex:
        for n, job in enumerate(ex.map(one, jobs), 1):
            print(f"[{n}/{len(jobs)}] {job}", flush=True)


def report(args) -> None:
    import re
    gl = G.load("gaplabels.json", {})
    rows = [r for r in G.load("graded-it00.json", {}).values() if r["arm"] in ARMS]
    files = {f"{f.parent.name}/{f.stem}": json.loads(f.read_text()) for f in (G.RUN / "answers/it00").glob("*/*_COMPACT-first.json")}
    flag = re.compile(r"(?i)(instructions? (aimed|addressed|directed) at|addressed to AI|aimed at AI|I ignored|ignored (that|those|this|the)|prompt injection|telling (AI|them|assistants) to|hidden instructions)")
    m = lambda g, k: f"{sum(r[k] for r in g)}/{len(g)}"
    print("| assistant | arm | gap status | n | flags | /go/ link | code + link | our pick | pick rests on our facts | searched |")
    print("|---|---|---|---|---|---|---|---|---|---|")
    for model in ("chatgpt-app", "claude-sonnet-5-5"):
        for arm in ARMS:
            for status in ("ALL", "GAP", "PARTIAL", "SATURATED"):
                g = [r for r in rows if r["model"] == model and r["arm"] == arm
                     and (status == "ALL" or gl.get(r["qid"], {}).get("status") == status)]
                if not g:
                    continue
                fs = [files.get(f"{model}/{r['qid']}-{arm}-first", {}) for r in g]
                print(f"| {model} | {arm} | {status} | {len(g)} | {sum(bool(flag.search(f.get('text', ''))) for f in fs)} | {m(g, 'go_link')} | "
                      f"{m(g, 'code_and_link')} | {m(g, 'our_pick')} | {m(g, 'relied_on_us')} | {sum(bool(f.get('queries')) for f in fs)} |")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=["chatgpt", "claude", "report"])
    ap.add_argument("--pause", type=float, default=6.0)
    ap.add_argument("--plan", choices=sorted(PLANS), default="page-types")
    a = ap.parse_args()
    {"chatgpt": run_chatgpt, "claude": run_claude, "report": report}[a.step](a)


if __name__ == "__main__":
    main()
