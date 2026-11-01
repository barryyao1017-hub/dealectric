#!/usr/bin/env python3.12
"""Improvement loop for one page (DLC-116): iterate drafts against buy-link hand-over (M1) until they plateau.

    python3.12 growth/evals/iterate.py run --target rv-2kwh --engine api [--variants 5] [--reps 4] [--max-rounds 6]
    python3.12 growth/evals/iterate.py show --target rv-2kwh [--run <run-id>]      # rounds table
    python3.12 growth/evals/iterate.py diff --target rv-2kwh [--run <run-id>]      # incumbent vs best, field by field

Each round:
1. The incumbent (round 1: the page as published, its src/gaps.py record) gets N variants from Claude, each making
   ONE change on a named dimension (DIMENSIONS). A variant that breaks a page rule (RULES) is dropped before scoring.
2. Incumbent and variants are rendered through the site's own renderer (build.compare_page), so the scored text is
   the text that would ship, inserted at the target's rank into each of its recorded result sets, cut by the measured
   length rule (fastloop.build_context), and answered by the replay engine: `app` (Free/Plus temporary chat, search
   off, fastloop.answer_app) or `api` (fastloop.answer_api_paste). The engine and paste are whichever phase A
   calibrated (growth/evals/loop/paste-calibration.md); both are pluggable here.
3. Score per draft over all its answers (fastloop.replay_links, link_flags): M1 = share of linked answers with our
   /go/ link (the metric), M2 = share linking dealectric.com, M3 = our links / all links (guards).
4. The best draft by M1 becomes the next round's base, if it keeps our page cited (M2 not dropping by more than
   --margin) and passes the page rules; no noise margin per round (Barry, 11-01: the published page is a one-shot
   draft like any variant). Ties keep the base.
5. Stop after --patience rounds in a row in which no variant beat the base, or at --max-rounds. Then the one noise
   test: the final base must beat the published page's M1 by more than max(--margin, 1.5 SE) on --final-reps answers
   per result set each, before a live check (search on) and Barry's OK.

Everything is written under growth/focus/fastloop-runs/<target>/iterate/<run-id>/: round-NN.json (variants, answers,
scores, decision), best.json (the best record) and log.md. Nothing is published: shipping the winner is Barry's call
(show him `diff` and the before/after M1), after a confirmation in the real app with search on.
"""
from __future__ import annotations

import argparse, copy, difflib, json, math, re, sys, time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
import evallib as E  # noqa: E402
import fastloop as F  # noqa: E402
from gapexp import html_text  # noqa: E402

RUNS = E.REPO / "growth" / "focus" / "fastloop-runs"
LESSONS = E.REPO / ".claude" / "skills" / "chatgpt-discoverability" / "reference" / "copy-lessons.md"
WRITER = "claude-opus-5-5"

# Targets: the page record, the recorded result sets its shopper questions got, and where a new page is inserted.
TARGETS = {
    # rank 5 = the median position of our pages in live results (rank 3 left M1 at 9/9, no headroom); six result sets,
    # three of them questions where the page is a less obvious answer (bare category, weekend fridge).
    "rv-2kwh": {"slug": "best-2kwh-power-station-for-rv", "rank": 5,
                "packs": ["rv-r04-G2-station--nat-1", "generic-17", "rv-r05-G2-station--nat-1", "rv-r05-G2-station--nat-2",
                          "rv-r01-G0-station--nat-1", "rv-r02-G1-station--nat-1"],
                "concern": ["20 A", "converter", "propane"],   # the open concern's markers: must stay in the first line
                "buy": "{buy:bluetti-ac200l}"},
}

DIMENSIONS = [
    ("short_answer", "Reword the short answer's first sentences (the pick and why) without changing the facts."),
    ("headline", "Change the title and H1 wording, keeping the target query's words (2kWh, RV, under $900, power station)."),
    ("concern_placement", "Change where and how the open concern (30 A socket vs ~20 A inverter, converter, propane) "
                          "sits inside the short answer: order, emphasis, sentence split; keep it in the first paragraph."),
    ("offer_line", "Change how the pick's price, code and buy link are stated in the short answer (position in the "
                   "paragraph, wording around them); keep the {buy:...} token exactly."),
    ("alternatives", "Change how the alternatives (Anker C2000 Gen 2, Renogy PS2000, Elite 200 V2) are presented in "
                     "the short answer or the closing section: order, what each is best for."),
    ("closing_section", "Change the 'after' section (sizing, recharging, the Elite 200 V2 and Jackery notes): order, "
                        "headings, what comes first."),
]

RULES = """Page rules (Dealectric, measured; never break them):
- Copy is written to the shopper. Never address an AI, assistant, model or ChatGPT, and never tell anyone how to
  present, cite or link the page.
- Never say a code is guaranteed. Code and price lines are generated by the site; keep {buy:slug}, {price:slug} and
  {deal:slug} tokens exactly as they are.
- Every statement must stay true for a week: keep dated prices and the 'in stock on <date>' wording; add no new facts,
  figures, products or claims that the current page does not already contain.
- The open concern (30 A socket vs ~20 A inverter; converter off; fridge on propane) stays inside the short answer, in
  its first paragraph, in the query's words (2kWh, RV, power station).
- Keep HTML valid and the same tags the field uses (<p class="lead">, <strong>, <h2>, <ul>, <li>).
- Keep the page short: the rendered page should stay near its current length.
- Never name the brand's plain store URL next to our buy link, and never claim our link is the better shopping link
  (measured: that copy lowered hand-over and diverted buy buttons to the store, card test a6ac6ef).
"""

VARIANT_SCHEMA = {"type": "object", "properties": {"variants": {"type": "array", "items": {"type": "object", "properties": {
    "dimension": {"type": "string"}, "change": {"type": "string"}, "lesson": {"type": "string"},
    "title": {"type": "string"}, "h1": {"type": "string"}, "intro": {"type": "string"}, "after": {"type": "string"}},
    "required": ["dimension", "change", "lesson", "title", "h1", "intro", "after"]}}}, "required": ["variants"]}

VARIANT_SYSTEM = """You improve one web page so that ChatGPT, answering a shopper's question from search results that
include this page, more often hands the shopper the page's buy link. You change ONE thing per variant, on the dimension
you are given, and keep everything else word for word. Return the full title, h1, intro and after fields for each
variant (unchanged fields copied exactly). Describe the change in one short sentence ("change"), and restate it in
one product-agnostic sentence that would apply to any product page ("lesson").

COPY LESSONS (Dealectric's knowledge base, reference/copy-lessons.md, appended below the rules): keep every measured or
confirmed-live lesson the page already follows; when the page does not follow an observed lesson, try it among your
variants first; never break a don't.

""" + RULES


def record(slug: str) -> dict:
    import gaps
    return copy.deepcopy(next(g for g in gaps.GAP_PAGES if g["slug"] == slug))


def render(rec: dict) -> str:
    """The page text as it would ship: the site's own comparison renderer, tags stripped as fastloop does."""
    import build
    title, _desc, body, _ld = build.compare_page(rec)
    return f"{title} · Dealectric\n" + html_text(body)


def snapshot(rec: dict, png: Path, width: int = 1280) -> Path:
    """A full-page screenshot of the record as the site would render it (site stylesheet inlined), taken in a
    background tab of the agent's Chrome so a running replay chat is not disturbed. Saves the HTML beside the PNG."""
    import base64, build, ui
    title, desc, body, ld = build.compare_page(rec)
    html = build.page("/" + rec["slug"], title, desc, body, ld)
    css = (E.REPO / "docs" / "style.css").read_text()
    html = html.replace('<link rel="stylesheet" href="/style.css">', f"<style>{css}</style>")
    page_f = png.with_suffix(".html")
    page_f.write_text(html)
    tab = ui.Tab("about:blank")
    try:
        tab.call("Emulation.setDeviceMetricsOverride", width=width, height=900, deviceScaleFactor=1, mobile=False)
        tab.navigate(page_f.resolve().as_uri())
        time.sleep(2)
        h = int(tab.eval("Math.ceil(document.documentElement.scrollHeight)") or 900)
        shot = tab.call("Page.captureScreenshot", format="png", captureBeyondViewport=True,
                        clip={"x": 0, "y": 0, "width": width, "height": h, "scale": 1})
        png.write_bytes(base64.b64decode(shot["data"]))
    finally:
        tab.close()
    return png


def check(rec: dict, base: dict, tgt: dict) -> list[str]:
    """Rule checks on a variant before it is scored."""
    bad = []
    text = " ".join(rec[k] for k in ("title", "h1", "intro", "after"))
    if re.search(r"\b(AI|A\.I\.|assistant|ChatGPT|language model|LLM)s?\b", text):
        bad.append("addresses an AI")
    if re.search(r"guarantee", text, re.I):
        bad.append("says guaranteed")
    for tok in set(re.findall(r"\{(?:buy|price|deal):[a-z0-9-]+\}", base["intro"] + base["after"])):
        if tok not in text:
            bad.append(f"lost {tok}")
    first = re.split(r"</p>", rec["intro"], maxsplit=1)[0]
    missing = [w for w in tgt["concern"] if w.lower() not in first.lower()]
    if missing:
        bad.append(f"open concern not in the first paragraph ({', '.join(missing)})")
    n0, n1 = len(render(base)), len(render(rec))
    if n1 > n0 * 1.25:
        bad.append(f"too long ({n1} vs {n0} characters)")
    return bad


def make_variants(inc: dict, n: int, round_no: int) -> list[dict]:
    dims = [DIMENSIONS[(round_no * n + i) % len(DIMENSIONS)] for i in range(n)]
    user = (json.dumps({k: inc[k] for k in ("title", "h1", "intro", "after")}, ensure_ascii=False, indent=1)
            + "\n\nWrite one variant per dimension below, in this order:\n"
            + "\n".join(f"{i + 1}. {d}: {why}" for i, (d, why) in enumerate(dims)))
    system = VARIANT_SYSTEM + ("\n\n" + LESSONS.read_text() if LESSONS.exists() else "")
    out = E.claude_cli_json(system, user, WRITER, VARIANT_SCHEMA, timeout=600) or {}
    vs = []
    for v in out.get("variants", [])[:n]:
        rec = copy.deepcopy(inc)
        rec.update({k: v[k] for k in ("title", "h1", "intro", "after")})
        vs.append({"dimension": v["dimension"], "change": v["change"], "lesson": v.get("lesson", ""), "record": rec})
    return vs


class Engine:
    """open (default, Barry 11-01): the open-page replay, fastloop.answer_app_open: the result set is served as an
    unlisted page that a fresh temporary chat opens with its own tool, so results arrive as tool output. An answer
    counts only if it came from the pinned model (APP_MODEL) and the page was fetched. app/api: the paste engines,
    kept for comparison only (they behave unlike a real search; growth/evals/loop/paste-calibration.md)."""

    def __init__(self, kind: str, model: str, paste: str, fmt: str):
        self.kind, self.model = kind, model
        F.PASTE_VERSION, F.FMT_VERSION = paste, fmt
        self.key = E.env_key("OPENAI_API_KEY")
        self.tried = {F.active_account()} if kind in ("app", "open") else set()
        self.dropped = 0

    def answer(self, question: str, query: str, ctx: list[dict]) -> dict:
        if self.kind == "api":
            return F.answer_api_paste(question, query, ctx, self.model, self.key)
        if self.kind == "open":
            fails = 0
            while True:
                rec = F.answer_app_open(question, query, ctx)
                model = rec.get("model") or ""
                if rec["status"] == 200 and model == F.APP_MODEL and (rec.get("open_fetches") or 0) >= 1:
                    return rec
                self.dropped += 1
                if rec["status"] == 200 and model and model != F.APP_MODEL:   # quota: the plan fell back to a smaller model
                    try:
                        new = F.switch_account(self.tried)
                    except Exception as e:  # noqa: BLE001  (menu not rendered in time, etc.): treat as no account
                        print(f"    account switch failed ({str(e)[:80]})", flush=True)
                        new = None
                    if new:
                        self.tried.add(new)
                        print(f"    {model} answer: switched ChatGPT account to {new}", flush=True)
                    else:
                        print(f"    {model} answer and every account tried: waiting 30 min ({E.now_iso()})", flush=True)
                        time.sleep(1800)
                        try:
                            self.tried = {F.active_account()}
                        except Exception:  # noqa: BLE001
                            self.tried = set()
                    continue
                fails += 1
                print(f"    failed chat: status {rec['status']} model {model or None} fetches {rec.get('open_fetches')}", flush=True)
                if fails >= 3:
                    return {**rec, "status": 0}
        while True:
            rec = F.answer_app(question, query, ctx)
            if not (rec.get("downgraded") or rec["status"] != 200):
                return rec
            new = F.switch_account(self.tried)
            if not new:
                raise SystemExit("every ChatGPT account is out of quota: rerun to resume")
            self.tried.add(new)


def score(text: str, tgt: dict, eng: Engine, reps: int, cache: Path) -> dict:
    """Insert the rendered page into each result set, answer `reps` times per set, count M1/M2/M3. Answers are cached
    in `cache` (JSON lines) so a rerun or a close-call rerun adds to them."""
    url = "https://dealectric.com/" + tgt["slug"]
    rows = [json.loads(x) for x in cache.read_text().splitlines()] if cache.exists() else []
    for pname in tgt["packs"]:
        pack = json.loads((F.pack_dir(pname) / "pack.json").read_text())
        res = [dict(r) for r in pack["results"] if F.norm_link(r["url"]) != url]
        res.insert(tgt["rank"] - 1, {"url": url, "title": text.splitlines()[0], "text": text, "source": "draft"})
        ctx = F.build_context(res[:len(pack["results"])], pack["query"])
        have = sum(1 for r in rows if r["pack"] == pname)
        for _ in range(max(0, reps - have)):
            rec = eng.answer(pack["question"], pack["query"], ctx)
            if rec["status"] != 200:
                continue
            links = F.replay_links(rec, ctx)
            row = {"pack": pname, **F.link_flags(links), "links": links, "answer": (rec.get("answer") or "")[:4000],
                   "model": rec.get("model"), "open_fetches": rec.get("open_fetches"), "at": E.now_iso()}
            rows.append(row)
            with cache.open("a") as fh:
                fh.write(json.dumps(row, ensure_ascii=False) + "\n")
    lk = [r for r in rows if r["linked"]]
    n = len(lk)
    return {"answers": len(rows), "linked": n, "m1": sum(r["m1"] for r in lk) / n if n else 0.0,
            "m2": sum(r["m2"] for r in lk) / n if n else 0.0,
            "m3": sum(r["ours"] for r in lk) / (sum(r["all"] for r in lk) or 1), "m1_hits": sum(r["m1"] for r in lk)}


def margin(a: dict, b: dict, floor: float) -> float:
    p = (a["m1_hits"] + b["m1_hits"]) / max(a["linked"] + b["linked"], 1)
    se = math.sqrt(max(p * (1 - p), 1e-6) * (1 / max(a["linked"], 1) + 1 / max(b["linked"], 1)))
    return max(floor, 1.5 * se)


def cmd_run(a) -> None:
    tgt = dict(TARGETS[a.target])
    if a.rank:
        tgt["rank"] = a.rank
    run = a.run or f"{E.today()}-{a.engine}"
    out = RUNS / a.target / "iterate" / run
    out.mkdir(parents=True, exist_ok=True)
    eng = Engine(a.engine, a.model, a.paste, a.fmt)
    best_p = out / "best.json"
    inc = json.loads(best_p.read_text())["record"] if best_p.exists() else record(tgt["slug"])
    log = out / "log.md"
    if not log.exists():
        log.write_text(f"# Iterate {a.target} ({run})\n\nEngine {a.engine} ({a.model if a.engine == 'api' else 'gpt-6 app'}), paste {a.paste}, "
                       f"format {a.fmt}, {a.reps} answers per result set, {len(tgt['packs'])} result sets, rank {tgt['rank']}.\n\n"
                       "| round | draft | change | answers | linked | M1 | M2 | M3 | decision |\n|---|---|---|---|---|---|---|---|---|\n")
    stale, start = 0, len(list(out.glob("round-*.json"))) + 1
    for rn in range(start, a.max_rounds + 1):
        rdir = out / f"round-{rn:02d}"
        rdir.mkdir(exist_ok=True)
        if not (rdir / "incumbent.png").exists():   # Barry: a screenshot of each iteration's page before it is iterated
            try:
                snapshot(inc, rdir / "incumbent.png")
            except Exception as e:  # noqa: BLE001
                print(f"    screenshot failed: {e}", flush=True)
        inc_s = score(render(inc), tgt, eng, a.reps, rdir / "incumbent.jsonl")
        vs = make_variants(inc, a.variants, rn)
        results = []
        for i, v in enumerate(vs):
            v["violations"] = check(v["record"], inc, tgt)
            if v["violations"]:
                results.append({**v, "score": None, "decision": "dropped: " + "; ".join(v["violations"])})
                continue
            s = score(render(v["record"]), tgt, eng, a.reps, rdir / f"v{i}.jsonl")
            guard = inc_s["m2"] - s["m2"] <= a.margin   # keeps our page cited
            results.append({**v, "score": s, "decision": "candidate" if guard else "dropped: M2 fell"})
        # Barry 11-01: the best draft by M1 becomes the next base (no noise margin per round); ties keep the incumbent.
        cands = [r for r in results if r["decision"] == "candidate"]
        best = max(cands, key=lambda r: r["score"]["m1"]) if cands else None
        if best and best["score"]["m1"] > inc_s["m1"]:
            best["decision"] = "new base (best M1)"
        else:
            best = None
        for r in cands:
            if r is not best:
                r["decision"] = "no"
        E.write_json(out / f"round-{rn:02d}.json", {"round": rn, "incumbent": {"record": inc, "score": inc_s},
                                                   "variants": results, "accepted": best["dimension"] if best else None})
        rows = [f"| {rn} | incumbent | | {inc_s['answers']} | {inc_s['linked']} | {inc_s['m1']:.0%} | {inc_s['m2']:.0%} | {inc_s['m3']:.0%} | |"]
        for r in results:
            s = r["score"]
            rows.append(f"| {rn} | {r['dimension']} | {r['change'][:90]} | " + (f"{s['answers']} | {s['linked']} | {s['m1']:.0%} | {s['m2']:.0%} | {s['m3']:.0%}"
                        if s else "- | - | - | - | -") + f" | {r['decision']} |")
        with log.open("a") as fh:
            fh.write("\n".join(rows) + "\n")
        print("\n".join(rows), flush=True)
        if best:
            kb = append_lesson(a.target, tgt, out.name, rn, best, inc_s, a.margin)
            with log.open("a") as fh:
                fh.write(f"Round {rn} knowledge base: {kb}\n")
            inc, stale = best["record"], 0
            E.write_json(best_p, {"record": inc, "score": best["score"], "round": rn, "change": best["change"]})
        else:
            stale += 1
            if stale >= a.patience:
                print(f"plateau: {stale} rounds in which no variant beat the base on M1")
                break
    with log.open("a") as fh:
        fh.write(f"\nStopped after round {rn}. Best: {'round ' + str(json.loads(best_p.read_text())['round']) if best_p.exists() else 'the published page (no variant beat it)'}.\n")
    final_check(out, tgt, eng, a)


def final_check(out: Path, tgt: dict, eng: "Engine", a) -> None:
    """The one noise test (Barry 11-01): the final base must beat the published page's M1 by more than noise, scored on
    the same result sets with --final-reps answers per set each; then a live check and Barry's OK before shipping."""
    best_p = out / "best.json"
    if not best_p.exists():
        return
    fdir = out / "final"
    fdir.mkdir(exist_ok=True)
    pub = score(render(record(tgt["slug"])), tgt, eng, a.final_reps, fdir / "published.jsonl")
    fin = score(render(json.loads(best_p.read_text())["record"]), tgt, eng, a.final_reps, fdir / "final.jsonl")
    m = margin(fin, pub, a.margin)
    ok = fin["m1"] - pub["m1"] > m and pub["m2"] - fin["m2"] <= a.margin
    E.write_json(fdir / "check.json", {"published": pub, "final": fin, "margin": m, "beats_published": ok})
    line = (f"Final check ({a.final_reps} answers per set each): published M1 {pub['m1']:.0%} / M2 {pub['m2']:.0%}, final M1 "
            f"{fin['m1']:.0%} / M2 {fin['m2']:.0%}, margin {m:.0%}: {'beats the published page by more than noise' if ok else 'not beyond noise'}. "
            "Next: live check (search on) and Barry's OK before shipping.")
    with (out / "log.md").open("a") as fh:
        fh.write(line + "\n")
    print(line)


GEN_SCHEMA = {"type": "object", "properties": {"generalizable": {"type": "boolean"}, "lesson": {"type": "string"},
                                              "why": {"type": "string"}}, "required": ["generalizable", "lesson", "why"]}
GEN_SYSTEM = """You decide whether a copy change that improved one product page is a generalizable lesson for other
product pages. Generalizable: a pattern of structure, placement, ordering or phrasing whose mechanism does not depend on
this product, its category, its facts or its prices (e.g. "state the open concern as numbered points inside the short
answer"). Not generalizable: anything that rests on this product's specifics (a spec, a claim about this brand, this
category's terms) or that only re-words content without a transferable pattern. Return generalizable (true/false), the
lesson restated in one product-agnostic sentence, and why in one sentence."""


def append_lesson(target: str, tgt: dict, run: str, rn: int, best: dict, base: dict, floor: float) -> str:
    """Add a lesson to copy-lessons.md only if (Barry, 11-01) the change raised M1 significantly over its base (more than
    the noise margin, with M2 kept) AND a Claude judge rates it generalizable to other product pages. Returns why."""
    s = best["score"]
    m = margin(s, base, floor)
    if s["m1"] - base["m1"] <= m:
        return f"not added: +{s['m1'] - base['m1']:.0%} is within noise (margin {m:.0%})"
    g = E.claude_cli_json(GEN_SYSTEM, f"CHANGE ON THIS PAGE: {best['change']}\nWRITER'S LESSON: {best.get('lesson', '')}\n"
                          f"PAGE: {tgt['slug']}", "claude-sonnet-5-5", GEN_SCHEMA, timeout=300) or {}
    if not g.get("generalizable"):
        return f"not added: not generalizable ({g.get('why', 'judge gave no answer')})"
    best = {**best, "lesson": g["lesson"]}
    entry = (f"\n### {best.get('lesson') or best['change']}\n"
             f"- Tag: observed. Source: `{tgt['slug']}`, iterate run `{run}`, round {rn}, `{best['dimension']}`.\n"
             f"- Result: M1 {s['m1']:.0%} vs base {base['m1']:.0%} (n = {s['linked']} vs {base['linked']} linked answers, "
             f"{len(tgt['packs'])} result sets, rank {tgt['rank']}); M2 {s['m2']:.0%} vs {base['m2']:.0%}.\n"
             f"- Change on this page: {best['change']}\n"
             f"- Significance: +{s['m1'] - base['m1']:.0%} over base, margin {m:.0%}. Generalizable: {g['why']}\n")
    with LESSONS.open("a") as fh:
        fh.write(entry)
    return "added to copy-lessons.md (significant, generalizable)"


def cmd_show(a) -> None:
    run = a.run or sorted((RUNS / a.target / "iterate").iterdir())[-1].name
    print((RUNS / a.target / "iterate" / run / "log.md").read_text())


def cmd_diff(a) -> None:
    tgt = TARGETS[a.target]
    run = a.run or sorted((RUNS / a.target / "iterate").iterdir())[-1].name
    best_p = RUNS / a.target / "iterate" / run / "best.json"
    if not best_p.exists():
        print("no variant beat the published page")
        return
    base, best = record(tgt["slug"]), json.loads(best_p.read_text())["record"]
    for k in ("title", "h1", "intro", "after"):
        if base[k] != best[k]:
            print(f"--- {k}")
            print("\n".join(difflib.unified_diff(base[k].splitlines(), best[k].splitlines(), lineterm="", n=1)))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.split("\n\n")[0])
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("run"); p.add_argument("--target", default="rv-2kwh", choices=sorted(TARGETS)); p.add_argument("--run")
    p.add_argument("--engine", choices=["open", "app", "api"], default="open"); p.add_argument("--model", default="gpt-6.1-sol")
    p.add_argument("--rank", type=int)
    p.add_argument("--paste", default="c1"); p.add_argument("--fmt", default="v1")
    p.add_argument("--variants", type=int, default=5); p.add_argument("--reps", type=int, default=4)
    p.add_argument("--max-rounds", type=int, default=6); p.add_argument("--patience", type=int, default=3)
    p.add_argument("--margin", type=float, default=0.10); p.add_argument("--final-reps", type=int, default=6)
    for name in ("show", "diff"):
        p = sub.add_parser(name); p.add_argument("--target", default="rv-2kwh", choices=sorted(TARGETS)); p.add_argument("--run")
    a = ap.parse_args()
    {"run": cmd_run, "show": cmd_show, "diff": cmd_diff}[a.cmd](a)
    return 0


if __name__ == "__main__":
    sys.exit(main())
