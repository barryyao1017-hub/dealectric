#!/usr/bin/env python3.12
"""Content-gap experiment, stage 1 (growth/gap-experiment.md): conditional on our page being in the result set, does a
gap in the rest of the set make the model hand over our link and code more often, and does a page aimed at the agent's
own query do better than our product page? Gives Claude (CLI, no tools) the real result set ChatGPT saw for each target
question, with nothing (NONE), our product page (BASELINE) or a query-targeted page (TARGETED) added, and grades.

    python3.12 growth/evals/gapexp.py packs                 # ChatGPT's result sets → packs.json (page text fetched)
    python3.12 growth/evals/gapexp.py gaplabel              # → gaplabels.json (dedicated / substantive per source)
    python3.12 growth/evals/gapexp.py drafts --it 0         # TARGETED drafts → drafts/it00/<Q>.md
    python3.12 growth/evals/gapexp.py run --it 0 --model claude-sonnet-5-5 [--arms NONE,BASELINE,TARGETED]
    python3.12 growth/evals/gapexp.py grade --it 0
    python3.12 growth/evals/gapexp.py report --it 0

Every step skips what its output already holds, so a re-run fills gaps.
"""
from __future__ import annotations

import argparse
import concurrent.futures as cf
import html
import json
import random
import re
import statistics
import subprocess
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402

RUN = E.run_dir("2026-10-24-gapexp")
PROBE = E.run_dir("2026-10-23-queryprobe") / "chatgpt"
ROOT = Path(__file__).resolve().parents[2]
QIDS = [f"Q{n:02d}" for n in range(1, 31)]
# Gap clusters without a ChatGPT result set: their pack is the live Bing top 10 for the agent's own query
# (runs/2026-10-25-agentq, Bing feeds ChatGPT search). `page` is the published gap page (arm PAGE).
EXTRA = {
    "G02": {"text": "What's the best solar generator with solar panels included?", "query": "solar generator with panels included",
            "primary": "allpowers-p1800-1024wh", "expected": ["allpowers-p1800-1024wh", "allpowers-sp037-400w-solar-panel"],
            "page": "solar-generator-with-panels-included"},
    "G03": {"text": "Is there a back-seat screen for a Tesla Model Y? What should I buy?", "query": "Tesla Model Y back seat projector screen",
            "primary": "aurzen-travelplay-autocinema-tesla-model-y", "expected": ["aurzen-travelplay-autocinema-tesla-model-y"],
            "page": "tesla-model-y-back-seat-screen"},
}
# Target questions that a published gap page answers (arm PAGE).
PAGES = {"Q01": "best-power-banks-for-flying", "Q02": "best-power-banks-for-flying", **{q: e["page"] for q, e in EXTRA.items()}}
AGENTQ = E.run_dir("2026-10-25-agentq")
PACK_SIZE, WORDS = 6, 1200
JUDGE = "claude-sonnet-5-5"
UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36"


def load(name: str, default):
    p = RUN / name
    return json.loads(p.read_text()) if p.exists() else default


def save(name: str, obj) -> None:
    (RUN / name).parent.mkdir(parents=True, exist_ok=True)
    E.write_json(RUN / name, obj)


def html_text(raw: str) -> str:
    raw = re.sub(r"(?is)<(script|style|noscript|svg|nav|footer|header|form)\b.*?</\1>", " ", raw)
    raw = re.sub(r"(?is)<br\s*/?>|</(p|div|li|h[1-6]|tr|section|article)>", "\n", raw)
    t = html.unescape(re.sub(r"(?s)<[^>]+>", " ", raw))
    t = re.sub(r"[ \t\r\f\v]+", " ", t)
    return re.sub(r"\n\s*\n+", "\n", t).strip()


def cut(text: str, words: int = WORDS) -> str:
    w = text.split()
    return " ".join(w[:words]) + (" …" if len(w) > words else "")


def fetch_text(url: str) -> str:
    try:
        req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Language": "en-US,en"})
        raw = urllib.request.urlopen(req, timeout=20).read(3_000_000).decode("utf-8", "replace")
        t = html_text(raw)
        if len(t) > 800:
            return t
    except Exception:  # noqa: BLE001
        pass
    try:   # JS-rendered or bot-walled pages: read them in the agent's Chrome
        import ui
        tab = ui.Tab("about:blank")
        try:
            tab.navigate(url)
            time.sleep(6)
            return (tab.eval("document.body ? document.body.innerText : ''") or "").strip()
        finally:
            tab.close()
    except Exception:  # noqa: BLE001
        return ""


# ---------------------------------------------------------------- packs

def packs(args) -> None:
    out = load("packs.json", {})
    sup = json.loads((AGENTQ / "supply.json").read_text()) if (AGENTQ / "supply.json").exists() else {}
    for qid, e in EXTRA.items():
        if qid in out:
            continue
        rows = [r for r in sup.get(e["query"], []) if r.get("rank") and "dealectric.com" not in r["url"]]
        sources = []
        for r in rows:
            if len(sources) == PACK_SIZE:
                break
            t = fetch_text(r["url"])
            if len(t.split()) >= 150:
                sources.append({"title": r["title"], "url": r["url"], "domain": r["domain"], "text": cut(t)})
        out[qid] = {"question": e["text"], "query": e["query"], "queries": [e["query"]], "n_results": len(rows), "sources": sources}
        save("packs.json", out)
        print(f"{qid}: {len(sources)} of {len(rows)} sources fetched", flush=True)
    for qid in QIDS:
        if qid in out:
            continue
        f = PROBE / f"{qid}-A-1.json"
        d = json.loads(f.read_text())
        results = [r for r in (d.get("response") or {}).get("search_results") or [] if "dealectric.com" not in (r.get("domain") or "")]
        sources = []
        for r in results:
            if len(sources) == PACK_SIZE:
                break
            t = fetch_text(r["url"])
            if len(t.split()) < 150:
                continue
            sources.append({"title": r.get("title") or "", "url": r["url"], "domain": r.get("domain") or E.host_of(r["url"]), "text": cut(t)})
        out[qid] = {"question": d["prompt"], "query": (d.get("queries") or [d["prompt"]])[0], "queries": d.get("queries") or [],
                    "n_results": len(results), "sources": sources}
        save("packs.json", out)
        print(f"{qid}: {len(sources)} of {len(results)} sources fetched; query {out[qid]['query']!r}", flush=True)


# ---------------------------------------------------------------- gap labels

GAP_SCHEMA = {"type": "object", "properties": {"sources": {"type": "array", "items": {"type": "object", "properties": {
    "n": {"type": "integer"}, "dedicated": {"type": "boolean"}, "substantive": {"type": "boolean"}, "why": {"type": "string"}},
    "required": ["n", "dedicated", "substantive", "why"]}}}, "required": ["sources"]}
GAP_SYSTEM = """You judge how well web pages answer a shopper's question. For each numbered source say:
- dedicated: written to answer this question (or the search query shown), not a page that merely touches the topic,
  a store listing, a generic category page or an unrelated article. Store search-result pages, marketplace listings and
  single product pages (including the maker's own) are never dedicated, however closely their title matches.
- substantive: it gives specific, checkable product information a shopper could choose on: named models with prices,
  specs, measured runtimes or test results. Generic advice, AI-written padding that names products without data, rules
  pages with no product choice, or thin listicles copied from store blurbs are not substantive.
- why: one short phrase.
Return one entry per source number."""


def gaplabel(args) -> None:
    pk = load("packs.json", {})
    out = load("gaplabels.json", {})
    for qid in QIDS + list(EXTRA):
        if qid in out or qid not in pk:
            continue
        p = pk[qid]
        user = f"QUESTION: {p['question']}\nSEARCH QUERY: {p['query']}\n\n" + "\n\n".join(
            f"[{i}] {s['title']} | {s['url']}\n{cut(s['text'], 600)}" for i, s in enumerate(p["sources"], 1))
        r = E.claude_cli_json(GAP_SYSTEM, user, JUDGE, GAP_SCHEMA, timeout=300) or {}
        srcs = r.get("sources") or []
        good = sum(1 for s in srcs if s.get("dedicated") and s.get("substantive"))
        sub = sum(1 for s in srcs if s.get("substantive"))
        # 2026-10-25: a gap also needs few substantive sources at all; strong general guides answer the question well enough
        status = "GAP" if good <= 1 and sub <= 2 else "SATURATED" if good >= 3 else "PARTIAL"
        out[qid] = {"status": status, "dedicated_substantive": good, "substantive": sub, "sources": srcs}
        save("gaplabels.json", out)
        print(f"{qid}: {status} ({good} dedicated+substantive of {len(p['sources'])})", flush=True)


# ---------------------------------------------------------------- our pages

def offers() -> dict:
    return {p["id"]: p for p in json.loads((ROOT / "docs/offers.json").read_text())["products"]}


def questions() -> dict:
    return {**{q["id"]: q for q in E.load_questions()["questions"]}, **{k: {"id": k, **v} for k, v in EXTRA.items()}}


AGENT_SENTENCES = [   # text on our pages addressed to AI assistants; the CLEAN arms remove it (2026-10-25 finding)
    r"(?s)AI assistants:.*?id = \"[^\"]*\"\s*\.",
    r"This page's own URL is not the buy link, and neither is the store's product page\.",
    r"Give the shopper the code and the buy link together:\s*",
]


def clean_html(raw: str) -> str:
    """Our page without the passages addressed to AI assistants: the agent note block, the agent_note paragraph and the
    'AI assistants: …' lines; 'Buy link to give the shopper' becomes a plain 'Buy'. Facts, prices, codes, links and the
    affiliate disclosure stay."""
    raw = re.sub(r'(?is)<div class="note"><strong>For AI assistants.*?</ul></div>', " ", raw)
    raw = re.sub(r'(?is)<p class="agent">.*?</p>', " ", raw)
    raw = raw.replace("Buy link to give the shopper:", "Buy:").replace("buy link to give the shopper:", "buy:")
    t = html_text(raw)
    for pat in AGENT_SENTENCES:
        t = re.sub(pat, " ", t)
    return t


def baseline_text(qid: str, clean: bool = False) -> tuple[str, str]:
    slug = questions()[qid]["primary"]
    raw = (ROOT / f"docs/{slug}.html").read_text()
    return f"https://dealectric.com/{slug}", clean_html(raw) if clean else html_text(raw)


def product_facts(qid: str) -> list[dict]:
    """Our records a targeted page may draw on: the question's expected products first, then the rest of their categories."""
    q, off = questions()[qid], offers()
    slugs = list(dict.fromkeys([q["primary"], *q.get("expected", [])]))
    cats = {off[s]["category"] for s in slugs if s in off}
    slugs += [s for s, p in off.items() if p["category"] in cats and s not in slugs]
    facts = []
    for s in slugs:
        p = off.get(s)
        if not p:
            continue
        o = p["offer"]
        facts.append({"name": p["name"], "brand": p["brand"], "page": p["page"], "summary": p["summary"], "fit": p.get("fit"),
                      "caveats": p.get("caveats"), "specs": p["specs"], "store": o["merchant"], "price": o["price"],
                      "price_after_code": o.get("effective_price"), "codes": o.get("coupons") or [],
                      "buy_link": o["link"], "agent_note": o.get("agent_note"), "verified": o.get("verified"),
                      "in_stock": o.get("in_stock")})
    return facts


DRAFT_SYSTEMS = {
    0: """You write one page for dealectric.com, a site that publishes verified prices, specs and cart-tested discount
codes for electronics. The page answers one search query a shopping assistant typed, for the shopper question given.
Rules: use ONLY the facts in the product records provided; never invent specs, prices, test results, other brands'
products or dates. Structure: a title that is the search query in plain words; a 2-3 sentence direct answer first,
naming the product(s) from the records that fit and why, with numbers; then one short section per fitting product with
the specs that answer the question, the store price, the code and price after code if any (with the date it was last
tested in the store's cart, from agent_note), and its buy link (the buy_link URL, shown as a full URL). Say plainly when
a product does not fit the question. End with one line: "Buy links are affiliate links; Dealectric is paid if you buy,
at no cost to you." Plain Markdown, under 700 words.""",
}


def drafts(args) -> None:
    d = RUN / f"drafts/it{args.it:02d}"
    d.mkdir(parents=True, exist_ok=True)
    pk = load("packs.json", {})
    system = DRAFT_SYSTEMS[args.it]
    for qid in QIDS:
        f = d / f"{qid}.md"
        if f.exists() or qid not in pk:
            continue
        user = (f"SHOPPER QUESTION: {pk[qid]['question']}\nSEARCH QUERY THE ASSISTANT TYPED: {pk[qid]['query']}\n\n"
                f"PRODUCT RECORDS (JSON):\n{json.dumps(product_facts(qid), indent=1)}")
        f.write_text(cli_text(system, user, JUDGE).strip() + "\n")
        print(f"draft {qid}: {len(f.read_text().split())} words", flush=True)


def page_text(qid: str, clean: bool = False) -> tuple[str, str]:
    """The published gap page, from the snapshot taken when the arm was first run (pages/<slug>.html), so later
    loop-3 changes to the shared renderer do not leak into the measurement."""
    slug = PAGES[qid]
    snap = RUN / "pages" / f"{slug}.html"
    if not snap.exists():
        snap.parent.mkdir(parents=True, exist_ok=True)
        snap.write_text((ROOT / f"docs/{slug}.html").read_text())
    return f"https://dealectric.com/{slug}", clean_html(snap.read_text()) if clean else html_text(snap.read_text())


def targeted_text(qid: str, it: int) -> tuple[str, str]:
    slug = re.sub(r"[^a-z0-9]+", "-", load("packs.json", {})[qid]["query"].lower()).strip("-")[:80]
    return f"https://dealectric.com/answers/{slug}", (RUN / f"drafts/it{it:02d}/{qid}.md").read_text()


# ---------------------------------------------------------------- runs

def cli_text(system: str, user: str, model: str, timeout: int = 300) -> str:
    cmd = [E.claude_cli(), "-p", user, "--system-prompt", system, "--output-format", "json", "--tools", "", "--model", model, *E.CLI_ISOLATION]
    for attempt in range(3):
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=E.cli_cwd())
        try:
            d = json.loads(p.stdout)
            if not d.get("is_error"):
                return d.get("result") or ""
        except ValueError:
            pass
        time.sleep(20 * (attempt + 1))
    raise RuntimeError(f"claude CLI failed: {(p.stderr or p.stdout)[-300:]}")


RUN_SYSTEM = E.load_questions()["system"] + (" You cannot browse in this conversation: answer from the search results"
                                            " given, and cite the URLs you use.")


def trials(arms: list[str]) -> list[tuple[str, str, str]]:
    out = []
    for qid in QIDS + list(EXTRA):
        for arm in arms:
            if arm.startswith("PAGE") and qid not in PAGES:
                continue
            if arm == "TARGETED" and qid in EXTRA:
                continue
            for pos in (["-"] if arm == "NONE" else ["first", "middle", "last"]):
                out.append((qid, arm, pos))
    return out


def build_prompt(qid: str, arm: str, pos: str, it: int) -> str:
    p = load("packs.json", {})[qid]
    srcs = [{"title": s["title"], "url": s["url"], "text": s["text"]} for s in p["sources"]]
    if arm != "NONE":
        if arm in ("BASELINE", "BASELINE_CLEAN"):
            url, text = baseline_text(qid, clean=arm.endswith("CLEAN"))
        elif arm in ("PAGE", "PAGE_CLEAN"):
            url, text = page_text(qid, clean=arm.endswith("CLEAN"))
        else:
            url, text = targeted_text(qid, it)
        title = text.strip().split("\n")[0].lstrip("# ").strip()[:120]
        ours = {"title": title, "url": url, "text": cut(text)}
        k = {"first": 0, "middle": len(srcs) // 2, "last": len(srcs)}[pos]
        srcs.insert(k, ours)
    body = "\n\n".join(f"[{i}] {s['title']}\nURL: {s['url']}\n{s['text']}" for i, s in enumerate(srcs, 1))
    return f"{p['question']}\n\n--- Web search results for \"{p['query']}\" ---\n\n{body}"


def run(args) -> None:
    d = RUN / f"answers/it{args.it:02d}/{args.model}"
    d.mkdir(parents=True, exist_ok=True)
    todo = [t for t in trials(args.arms.split(",")) if not (d / f"{t[0]}-{t[1]}-{t[2]}.json").exists()]
    if args.questions:
        todo = [t for t in todo if t[0] in args.questions.split(",")]

    def one(t):
        qid, arm, pos = t
        prompt = build_prompt(qid, arm, pos, args.it)
        t0 = time.time()
        text = cli_text(RUN_SYSTEM, prompt, args.model)
        E.write_json(d / f"{qid}-{arm}-{pos}.json", {"qid": qid, "arm": arm, "pos": pos, "model": args.model, "it": args.it,
                                                     "prompt_words": len(prompt.split()), "text": text, "latency_s": round(time.time() - t0, 1)})
        return t

    with cf.ThreadPoolExecutor(args.workers) as ex:
        for n, t in enumerate(ex.map(one, todo), 1):
            print(f"[{n}/{len(todo)}] {t}", flush=True)


# ---------------------------------------------------------------- grading

JUDGE_SCHEMA = {"type": "object", "properties": {"our_pick": {"type": "boolean"}, "relied_on_us": {"type": "boolean"},
                                                 "top_pick": {"type": "string"}, "why": {"type": "string"}},
                "required": ["our_pick", "relied_on_us", "top_pick", "why"]}
JUDGE_SYSTEM = """You grade a shopping assistant's answer. Our site is dealectric.com; OUR PRODUCTS are listed.
- top_pick: the single product the answer recommends first or most strongly ("" if none).
- our_pick: true if top_pick is one of OUR PRODUCTS.
- relied_on_us: true if the main recommendation's facts (prices, specs, codes, links) are taken from the dealectric.com
  source more than from any other source, judging by the citations and the figures quoted.
- why: one short sentence."""


def our_codes(off: dict) -> dict[str, set[str]]:
    return {s: {c["code"].upper() for c in (p["offer"].get("coupons") or []) if c.get("code")} for s, p in off.items()}


def grade(args) -> None:
    off = offers()
    codes = our_codes(off)
    names = "\n".join(f"- {p['name']}" for p in off.values())
    rows = load(f"graded-it{args.it:02d}.json", {})
    files = sorted((RUN / f"answers/it{args.it:02d}").glob("*/*.json"))
    todo = [f for f in files if f"{f.parent.name}/{f.stem}" not in rows]

    def one(f):
        a = json.loads(f.read_text())
        text = a["text"]
        gos = set(re.findall(r"dealectric\.com/go/([a-z0-9\-]+)", text))
        go_slugs = {s for s in off if any(g.startswith(s) or (len(g) >= 8 and s.startswith(g)) for g in gos)}
        found_codes = {c for s in off for c in codes[s] if re.search(rf"\b{re.escape(c)}\b", text, re.I)}
        code_slugs = {s for s in off if codes[s] & found_codes}
        j = E.claude_cli_json(JUDGE_SYSTEM, f"OUR PRODUCTS:\n{names}\n\nQUESTION: {questions()[a['qid']]['text']}\n\nANSWER:\n{text}",
                              JUDGE, JUDGE_SCHEMA, timeout=300) or {}
        return f"{f.parent.name}/{f.stem}", {
            "qid": a["qid"], "arm": a["arm"], "pos": a["pos"], "model": a["model"],
            "cites_us": bool(re.search(r"dealectric\.com", text)), "go_link": bool(go_slugs),
            "code": bool(found_codes), "code_and_link": bool(go_slugs & code_slugs),
            "our_pick": bool(j.get("our_pick")), "relied_on_us": bool(j.get("relied_on_us")),
            "top_pick": j.get("top_pick", ""), "why": j.get("why", "")}

    with cf.ThreadPoolExecutor(args.workers) as ex:
        for n, (k, row) in enumerate(ex.map(one, todo), 1):
            rows[k] = row
            if n % 10 == 0 or n == len(todo):
                save(f"graded-it{args.it:02d}.json", rows)
                print(f"graded {n}/{len(todo)}", flush=True)


# ---------------------------------------------------------------- report

METRICS = ["cites_us", "go_link", "code", "code_and_link", "our_pick", "relied_on_us"]


def report(args) -> None:
    rows = list(load(f"graded-it{args.it:02d}.json", {}).values())
    gl = load("gaplabels.json", {})
    coded = set(E.load_questions()["coded_questions"])
    lines = [f"# Gap experiment stage 1, iteration {args.it} ({E.today()})", ""]
    for model in sorted({r["model"] for r in rows}):
        lines += [f"## {model}", "", "| gap status | arm | n | " + " | ".join(METRICS) + " |", "|---|---|---|" + "---|" * len(METRICS)]
        for status in ("GAP", "PARTIAL", "SATURATED"):
            for arm in ("NONE", "BASELINE", "BASELINE_CLEAN", "TARGETED", "PAGE", "PAGE_CLEAN"):
                g = [r for r in rows if r["model"] == model and r["arm"] == arm and gl.get(r["qid"], {}).get("status") == status]
                if not g:
                    continue
                cells = []
                for m in METRICS:
                    k = sum(r[m] for r in g)
                    lo, hi = E.wilson(k, len(g))[1:]
                    cells.append(f"{k}/{len(g)} ({100 * k / len(g):.0f}%, {100 * lo:.0f}–{100 * hi:.0f})")
                lines.append(f"| {status} | {arm} | {len(g)} | " + " | ".join(cells) + " |")
        lines.append("")
        # code_and_link only means something where the product has a code
        lines += ["Coded questions only (code_and_link):", ""]
        for status in ("GAP", "PARTIAL", "SATURATED"):
            for arm in ("BASELINE", "TARGETED"):
                g = [r for r in rows if r["model"] == model and r["arm"] == arm and r["qid"] in coded and gl.get(r["qid"], {}).get("status") == status]
                if g:
                    k = sum(r["code_and_link"] for r in g)
                    lines.append(f"- {status} {arm}: {k}/{len(g)}")
        lines.append("")
    (RUN / f"report-it{args.it:02d}.md").write_text("\n".join(lines) + "\n")
    print("\n".join(lines))


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("step", choices=["packs", "gaplabel", "drafts", "run", "grade", "report"])
    ap.add_argument("--it", type=int, default=0)
    ap.add_argument("--model", default="claude-sonnet-5-5")
    ap.add_argument("--arms", default="NONE,BASELINE,TARGETED,PAGE")
    ap.add_argument("--questions", default="")
    ap.add_argument("--workers", type=int, default=4)
    args = ap.parse_args()
    {"packs": packs, "gaplabel": gaplabel, "drafts": drafts, "run": run, "grade": grade, "report": report}[args.step](args)


if __name__ == "__main__":
    main()
