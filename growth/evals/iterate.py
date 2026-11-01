#!/usr/bin/env python3.12
"""Improvement loop for one page (DLC-116): iterate drafts against buy-link hand-over (M1) until they plateau.

    python3.12 growth/evals/iterate.py supervise --target rv-2kwh [--variants 3] [--reps 1] [--max-rounds 6]   # unattended; `run` takes the same arguments
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
   test: the final base must beat the published page's M1 by more than max(--margin, 1.5 SE) on about --final-answers
   answers per page (spread evenly over the result sets), before a live check (search on) and Barry's OK.

Sampling (11-01, after run rv-open-1): one answer per result set (--reps 1) over many result sets (18 for rv-2kwh), and
3 variants per round, so each draft gets 18 answers for ~72 chats a round. Two answers to the same result set agreed on
M1 72% of the time against 52% by chance, and M1 swings by result set (0% to 73%), so a second answer to a set adds
little; more distinct sets make a winner generalize and more answers per draft cut the noise. Build the target's result
sets (`fastloop.py pack`) before iterating.

Everything is written under growth/focus/fastloop-runs/<target>/iterate/<run-id>/: round-NN.json (variants, answers,
scores, decision), best.json (the best record) and log.md. Nothing is published: shipping the winner is Barry's call
(show him `diff` and the before/after M1), after a confirmation in the real app with search on.
"""
from __future__ import annotations

import argparse, collections, copy, difflib, json, math, re, sys, time
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
    # rank 5 = the median position of our pages in live results (rank 3 left M1 at 9/9, no headroom). 18 result sets,
    # one answer each per draft (--reps 1): the six of run rv-open-1 (harvest and pinned chats, 10-31) plus twelve
    # pinned app chats of 11-01 (rv-n01..n12, general questions, no brand; max URL overlap with any other set 0.25).
    # Six are questions where the page is a less obvious answer: bare category (r01), weekend fridge (r02), dry camping
    # (n09), quiet overnight power (n10), camping in general (n11), gas generator alternative (n12).
    "rv-2kwh": {"slug": "best-2kwh-power-station-for-rv", "rank": 5,
                "packs": ["rv-r04-G2-station--nat-1", "generic-17", "rv-r05-G2-station--nat-1", "rv-r05-G2-station--nat-2",
                          "rv-r01-G0-station--nat-1", "rv-r02-G1-station--nat-1",
                          "rv-n01", "rv-n02", "rv-n03", "rv-n04", "rv-n05", "rv-n06", "rv-n07", "rv-n08",
                          "rv-n09", "rv-n10", "rv-n11", "rv-n12"],
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


BLOCKS_JS = r"""(() => { const sel = 'h1,h2,h3,p,li,tr,dt,dd,caption,figcaption,summary';
  return [...document.querySelectorAll(sel)].filter(e => !e.querySelector(sel)).map(e => {
    const r = e.getBoundingClientRect();
    return {text: e.innerText.replace(/\s+/g, ' ').trim(), x: Math.round(r.left + scrollX), y: Math.round(r.top + scrollY),
            w: Math.round(r.width), h: Math.round(r.height)}; }).filter(b => b.text && b.w > 0 && b.h > 0); })()"""


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
        boxes = tab.eval(BLOCKS_JS) or []   # where each text block sits, for the winners report's change boxes
        E.write_json(png.with_suffix(".boxes.json"), {"width": width, "height": h, "blocks": boxes})
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


def make_variants(inc: dict, n: int, round_no: int, beat=None) -> list[dict]:
    dims = [DIMENSIONS[(round_no * n + i) % len(DIMENSIONS)] for i in range(n)]
    user = (json.dumps({k: inc[k] for k in ("title", "h1", "intro", "after")}, ensure_ascii=False, indent=1)
            + "\n\nWrite one variant per dimension below, in this order:\n"
            + "\n".join(f"{i + 1}. {d}: {why}" for i, (d, why) in enumerate(dims)))
    system = VARIANT_SYSTEM + ("\n\n" + LESSONS.read_text() if LESSONS.exists() else "")
    out = {}
    for attempt in range(3):   # a failed or empty writer call is retried; an empty round would read as a plateau
        if beat:
            beat(f"writing variants, attempt {attempt + 1}")
        try:
            out = E.claude_cli_json(system, user, WRITER, VARIANT_SCHEMA, timeout=600) or {}
        except Exception as e:  # noqa: BLE001  (CLI timeout, no JSON)
            print(f"    variant writer failed ({str(e)[:100]}), attempt {attempt + 1}", flush=True)
        if out.get("variants"):
            break
    else:
        raise Stall("the variant writer returned nothing three times")
    vs = []
    for v in out.get("variants", [])[:n]:
        rec = copy.deepcopy(inc)
        rec.update({k: v[k] for k in ("title", "h1", "intro", "after")})
        vs.append({"dimension": v["dimension"], "change": v["change"], "lesson": v.get("lesson", ""), "record": rec})
    return vs


class Stall(SystemExit):
    """The run cannot make progress now (quota spent past --max-wait, or chats failing after a health check). Exit code
    75; every answer so far is cached, so `supervise` (or a rerun) resumes exactly where it stopped."""

    def __init__(self, why: str):
        print(f"STALL: {why}", flush=True)
        super().__init__(75)


CAP_RE = re.compile(r"limit|reached|too many|try again later|usage cap", re.I)


class Engine:
    """open (default, Barry 11-01): the open-page replay, fastloop.answer_app_open: the result set is served as an
    unlisted page that a fresh temporary chat opens with its own tool, so results arrive as tool output. An answer
    counts only if the page was fetched and it came from an accepted model (--models). app/api: the paste engines,
    kept for comparison only (they behave unlike a real search; growth/evals/loop/paste-calibration.md).

    Accounts and quota (Barry, 11-01: no waiting on a dead component, both accounts used, no endless quota waits):
    - The URL pin does not choose the model; the account's quota does (11-01: Plus answered gpt-6 under &model=gpt-6-mini).
      So each answer's model is recorded and drafts are compared within model (stratified M1, `tally`).
    - Preferred model = the first of --models. After an answer on another model, the other account is tried next if it
      has not fallen back within the last PROBE_S, so both accounts' gpt-6 quota is spent before mini answers count.
    - An answer on a model outside --models is dropped (strict mode, e.g. --models gpt-6): try the other account, then
      wait in 10-minute steps; past --max-wait minutes the run stops with Stall (exit 75) instead of waiting longer.
    - A failed chat triggers a health check (Chrome up, signed in: fastloop.ensure_ready); a usage-cap notice moves to the
      other account. A slot that still fails is retried in a later pass of the round (`fill`), never silently skipped."""

    PROBE_S = 1800

    def __init__(self, kind: str, model: str, paste: str, fmt: str, models: list[str] | None = None,
                 max_wait_min: float = 60, heartbeat: Path | None = None):
        self.kind, self.model = kind, model
        F.PASTE_VERSION, F.FMT_VERSION = paste, fmt
        self.key = E.env_key("OPENAI_API_KEY") if kind == "api" else None
        self.models = models or [F.APP_MODEL]
        self.max_wait, self.waited = max_wait_min * 60, 0.0
        self.heartbeat = heartbeat
        self.fallback_at: dict[str, float] = {}   # account -> when it last answered off the preferred model
        self.capped_at: dict[str, float] = {}     # account -> when it last showed a usage-cap notice
        self.who = F.ensure_ready() if kind in ("app", "open") else None
        self.dropped = 0

    def beat(self, what: str) -> None:
        if self.heartbeat:
            self.heartbeat.write_text(json.dumps({"at": E.now_iso(), "what": what, "account": self.who}))

    def _other(self) -> str | None:
        """Switch to the account not in use; its email, or None."""
        new = None
        for attempt in range(2):   # the profile menu sometimes renders late (11-01): one retry
            try:
                new = F.switch_account({self.who})
                break
            except Exception as e:  # noqa: BLE001
                print(f"    account switch failed ({str(e)[:80]}), attempt {attempt + 1}", flush=True)
        if new:
            print(f"    switched ChatGPT account {self.who} -> {new}", flush=True)
            self.who = new
        return new

    def _other_fresh(self, within: dict) -> bool:
        now = time.time()
        known = set(self.fallback_at) | set(self.capped_at) | {self.who}
        others = [a for a in known if a != self.who]
        # an account never seen yet is fresh; a seen one is fresh once its mark is older than PROBE_S
        return not others or any(now - within.get(a, 0) > self.PROBE_S for a in others)

    def _wait(self, why: str) -> None:
        if self.waited >= self.max_wait:
            raise Stall(f"{why}; waited {self.waited / 60:.0f} min (cap --max-wait)")
        print(f"    {why}: waiting 10 min ({self.waited / 60:.0f} of {self.max_wait / 60:.0f} min used, {E.now_iso()})", flush=True)
        for _ in range(10):
            self.beat(f"quota wait: {why}")
            time.sleep(60)
        self.waited += 600
        self.fallback_at.clear()
        self.capped_at.clear()

    def answer(self, question: str, query: str, ctx: list[dict]) -> dict:
        if self.kind == "api":
            return F.answer_api_paste(question, query, ctx, self.model, self.key)
        if self.kind == "app":
            return F.answer_app(question, query, ctx)
        fails = 0
        while True:
            self.beat(f"chat: {query[:60]}")
            rec = F.answer_app_open(question, query, ctx)
            model = rec.get("model") or ""
            fetched = (rec.get("open_fetches") or 0) >= 1
            if rec["status"] == 200 and model and fetched:
                if model == self.models[0]:
                    self.fallback_at.pop(self.who, None)
                else:
                    self.fallback_at[self.who] = time.time()
                if model in self.models:
                    self.waited = 0.0
                    rec["account"] = self.who
                    if model != self.models[0] and self._other_fresh(self.fallback_at):
                        self._other()   # spend the other account's preferred-model quota first
                    return rec
                self.dropped += 1                         # strict mode: off-model answer
                print(f"    {model} answer dropped (accepted: {', '.join(self.models)})", flush=True)
                if not (self._other_fresh(self.fallback_at) and self._other()):
                    self._wait(f"every account answers {model}")
                continue
            self.dropped += 1
            fails += 1
            err = rec.get("error") or ""
            print(f"    failed chat: status {rec['status']} model {model or None} fetches {rec.get('open_fetches')} "
                  f"{err[:100]}", flush=True)
            if CAP_RE.search(err):                        # usage-cap notice: this account is out for now
                self.capped_at[self.who] = time.time()
                if not (self._other_fresh(self.capped_at) and self._other()):
                    self._wait("every account shows a usage cap")
                continue
            if fails in (2, 4):
                try:
                    who = F.ensure_ready()
                except RuntimeError as e:
                    raise Stall(str(e))
                if who != self.who:
                    print(f"    health check: now signed in as {who}", flush=True)
                self.who = who
            if fails >= 5:
                return {**rec, "status": 0}


def draft_ctx(text: str, tgt: dict, pname: str) -> tuple[dict, list[dict]]:
    """The result set `pname` with the draft inserted at the target's rank, cut by the length rule."""
    url = "https://dealectric.com/" + tgt["slug"]
    pack = json.loads((F.pack_dir(pname) / "pack.json").read_text())
    res = [dict(r) for r in pack["results"] if F.norm_link(r["url"]) != url]
    res.insert(tgt["rank"] - 1, {"url": url, "title": text.splitlines()[0], "text": text, "source": "draft"})
    return pack, F.build_context(res[:len(pack["results"])], pack["query"])


def load_rows(cache: Path) -> list[dict]:
    return [json.loads(x) for x in cache.read_text().splitlines()] if cache.exists() else []


def fill(drafts: dict[str, tuple[str, Path]], tgt: dict, eng: Engine, reps: int, passes: int = 3) -> None:
    """Answer every draft `reps` times per result set, interleaved (rep -> result set -> draft), so a change of model,
    account or time of day lands on all drafts alike. A slot that fails is retried in the next pass; a round that
    still has empty slots after `passes` passes stops with Stall (exit 75) rather than scoring on gaps."""
    for p in range(passes):
        missing = 0
        for rep in range(reps):
            for pname in tgt["packs"]:
                for name, (text, cache) in drafts.items():
                    if sum(1 for r in load_rows(cache) if r["pack"] == pname) > rep:
                        continue
                    pack, ctx = draft_ctx(text, tgt, pname)
                    rec = eng.answer(pack["question"], pack["query"], ctx)
                    if rec["status"] != 200:
                        missing += 1
                        continue
                    links = F.replay_links(rec, ctx)
                    row = {"pack": pname, **F.link_flags(links), "links": links, "answer": (rec.get("answer") or "")[:4000],
                           "model": rec.get("model"), "account": rec.get("account"), "open_fetches": rec.get("open_fetches"),
                           "at": E.now_iso()}
                    with cache.open("a") as fh:
                        fh.write(json.dumps(row, ensure_ascii=False) + "\n")
        if not missing:
            return
        print(f"    pass {p + 1}: {missing} slots failed; retrying them", flush=True)
    raise Stall(f"{missing} answer slots still failing after {passes} passes")


def tally(rows: list[dict], weights: dict[str, float] | None = None) -> dict:
    """M1/M2/M3 over linked answers. With `weights` (model -> share of the round's linked answers), M1 and M2 are
    standardized: each model's rate weighted by its share in the whole round, so a draft that happened to get more
    gpt-6-mini answers is not favoured or penalized for it. Raw rates are kept as m1_raw/m2_raw; m1_hits/linked
    stay raw for the noise margin."""
    lk = [r for r in rows if r["linked"]]
    n = len(lk)
    out = {"answers": len(rows), "linked": n, "m1_hits": sum(r["m1"] for r in lk),
           "m1_raw": sum(r["m1"] for r in lk) / n if n else 0.0, "m2_raw": sum(r["m2"] for r in lk) / n if n else 0.0,
           "m3": sum(r["ours"] for r in lk) / (sum(r["all"] for r in lk) or 1),
           "by_model": {m: {"linked": len(g), "m1": sum(r["m1"] for r in g) / len(g)}
                        for m in sorted({r.get("model") or "?" for r in lk})
                        for g in [[r for r in lk if (r.get("model") or "?") == m]]}}
    out["m1"], out["m2"] = out["m1_raw"], out["m2_raw"]
    if weights and n:
        ws = {m: w for m, w in weights.items() if any((r.get("model") or "?") == m for r in lk)}
        tot = sum(ws.values()) or 1
        for k in ("m1", "m2"):
            out[k] = sum(w / tot * (sum(r[k] for r in lk if (r.get("model") or "?") == m)
                                    / sum(1 for r in lk if (r.get("model") or "?") == m)) for m, w in ws.items())
    return out


def score_round(drafts: dict[str, tuple[str, Path]], tgt: dict, eng: Engine, reps: int) -> dict[str, dict]:
    """fill, then tally every draft standardized to the round's model mix."""
    fill(drafts, tgt, eng, reps)
    rows = {name: load_rows(cache) for name, (_t, cache) in drafts.items()}
    allr = [r for rs in rows.values() for r in rs if r["linked"]]
    weights = {m: sum(1 for r in allr if (r.get("model") or "?") == m) / len(allr)
               for m in {r.get("model") or "?" for r in allr}} if allr else None
    return {name: tally(rs, weights) for name, rs in rows.items()}


def margin(a: dict, b: dict, floor: float) -> float:
    p = (a["m1_hits"] + b["m1_hits"]) / max(a["linked"] + b["linked"], 1)
    se = math.sqrt(max(p * (1 - p), 1e-6) * (1 / max(a["linked"], 1) + 1 / max(b["linked"], 1)))
    return max(floor, 1.5 * se)


def run_dir(a) -> Path:
    return RUNS / a.target / "iterate" / (a.run or f"{E.today()}-{a.engine}")


def cmd_run(a) -> None:
    tgt = dict(TARGETS[a.target])
    if a.rank:
        tgt["rank"] = a.rank
    if a.packs:   # a subset of result sets (smoke tests); a real run uses the target's full list
        tgt["packs"] = a.packs.split(",")
    out = run_dir(a)
    out.mkdir(parents=True, exist_ok=True)
    eng = Engine(a.engine, a.model, a.paste, a.fmt, models=a.models.split(","), max_wait_min=a.max_wait,
                 heartbeat=out / "heartbeat.json")
    best_p = out / "best.json"
    inc = json.loads(best_p.read_text())["record"] if best_p.exists() else record(tgt["slug"])
    log = out / "log.md"
    if not log.exists():
        log.write_text(f"# Iterate {a.target} ({out.name})\n\nEngine {a.engine} ({a.model if a.engine == 'api' else 'gpt-6 app'}), paste {a.paste}, "
                       f"format {a.fmt}, {a.reps} answer(s) per result set × {len(tgt['packs'])} result sets = {a.reps * len(tgt['packs'])} "
                       f"answers per draft, {a.variants} variants per round, rank {tgt['rank']}.\n\n"
                       "| round | draft | change | answers | linked | M1 | M2 | M3 | decision |\n|---|---|---|---|---|---|---|---|---|\n")
    if a.final_only:   # re-run only the final check, e.g. strict on gpt-6 into final-gpt6/ (--final-tag gpt6)
        final_check(out, tgt, eng, a)
        return
    done = sorted(out.glob("round-*.json"))
    stale = 0
    for f in done:   # a resumed run counts its plateau from the rounds already on disk
        stale = 0 if json.loads(f.read_text()).get("accepted") else stale + 1
    start = rn = len(done) + 1
    rn -= 1
    for rn in range(start, a.max_rounds + 1):
        if stale >= a.patience:
            rn -= 1
            break
        rdir = out / f"round-{rn:02d}"
        rdir.mkdir(exist_ok=True)
        eng.beat(f"round {rn}: screenshot")
        if not (rdir / "incumbent.png").exists():   # Barry: a screenshot of each iteration's page before it is iterated
            try:
                snapshot(inc, rdir / "incumbent.png")
            except Exception as e:  # noqa: BLE001
                print(f"    screenshot failed: {e}", flush=True)
        vf = rdir / "variants.json"   # saved, so a resumed round scores the same variants its cached answers belong to
        if vf.exists():
            vs = json.loads(vf.read_text())
        else:
            eng.beat(f"round {rn}: writing variants")
            vs = make_variants(inc, a.variants, rn, eng.beat)
            for f in rdir.glob("v*.jsonl"):   # answers from variants of an earlier, unsaved attempt
                f.unlink()
            E.write_json(vf, vs)
        drafts = {"incumbent": (render(inc), rdir / "incumbent.jsonl")}
        for i, v in enumerate(vs):
            v["violations"] = check(v["record"], inc, tgt)
            if not v["violations"]:
                drafts[f"v{i}"] = (render(v["record"]), rdir / f"v{i}.jsonl")
        sc = score_round(drafts, tgt, eng, a.reps)
        inc_s = sc["incumbent"]
        results = []
        for i, v in enumerate(vs):
            if v["violations"]:
                results.append({**v, "score": None, "decision": "dropped: " + "; ".join(v["violations"])})
                continue
            s = sc[f"v{i}"]
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
        mix = collections.Counter(r.get("model") or "?" for _t, c in drafts.values() for r in load_rows(c) if r["linked"])
        rows.append(f"\nRound {rn} models: " + ", ".join(f"{m} {n}" for m, n in mix.most_common())
                    + " linked answers; M1 and M2 are standardized to that mix (each model's rate weighted by its share).\n")
        with log.open("a") as fh:
            fh.write("\n".join(rows) + "\n")
        print("\n".join(rows), flush=True)
        if best:
            try:
                kb = append_lesson(a.target, tgt, out.name, rn, best, inc_s, a.margin)
            except Exception as e:  # noqa: BLE001  (judge unavailable: the round stands, the lesson waits)
                kb = f"not judged ({str(e)[:80]})"
            with log.open("a") as fh:
                fh.write(f"Round {rn} knowledge base: {kb}\n")
            inc, stale = best["record"], 0
            E.write_json(best_p, {"record": inc, "score": best["score"], "round": rn, "change": best["change"]})
        else:
            stale += 1
    if stale >= a.patience:
        print(f"plateau: {stale} rounds in which no variant beat the base on M1", flush=True)
    if "Stopped after round" not in log.read_text():
        with log.open("a") as fh:
            fh.write(f"\nStopped after round {rn}. Best: {'round ' + str(json.loads(best_p.read_text())['round']) if best_p.exists() else 'the published page (no variant beat it)'}.\n")
    final_check(out, tgt, eng, a)


def final_check(out: Path, tgt: dict, eng: "Engine", a) -> None:
    """The one noise test (Barry 11-01): the final base must beat the published page's M1 by more than noise, scored on
    the same result sets, interleaved and standardized to one model mix; then a live check and Barry's OK before
    shipping. Sample: --final-reps answers per set if given, else enough per set for about --final-answers per page
    (36 ≈ the 31 linked answers per page of run rv-open-1, which used 6 sets × 6)."""
    reps = a.final_reps or math.ceil(a.final_answers / len(tgt["packs"]))
    best_p = out / "best.json"
    fdir = out / ("final" + (f"-{a.final_tag}" if a.final_tag else ""))
    if not best_p.exists() or (fdir / "check.json").exists():
        return
    fdir.mkdir(exist_ok=True)
    sc = score_round({"published": (render(record(tgt["slug"])), fdir / "published.jsonl"),
                      "final": (render(json.loads(best_p.read_text())["record"]), fdir / "final.jsonl")}, tgt, eng, reps)
    pub, fin = sc["published"], sc["final"]
    m = margin(fin, pub, a.margin)
    ok = fin["m1"] - pub["m1"] > m and pub["m2"] - fin["m2"] <= a.margin
    E.write_json(fdir / "check.json", {"published": pub, "final": fin, "margin": m, "beats_published": ok})
    line = (f"Final check{' [' + a.final_tag + ', models ' + a.models + ']' if a.final_tag else ''} ({reps} answer(s) per set × {len(tgt['packs'])} sets: {pub['linked']} vs {fin['linked']} linked): published M1 {pub['m1']:.0%} / M2 {pub['m2']:.0%}, final M1 "
            f"{fin['m1']:.0%} / M2 {fin['m2']:.0%}, margin {m:.0%}: {'beats the published page by more than noise' if ok else 'not beyond noise'}. "
            f"By model: published {json.dumps(pub['by_model'])}, final {json.dumps(fin['by_model'])}. "
            "Next: live check (search on) and Barry's OK before shipping.")
    with (out / "log.md").open("a") as fh:
        fh.write(line + "\n")
    print(line, flush=True)


SUPERVISE_ONLY = {"--stall-min": 1, "--budget-h": 1, "--max-restarts": 1}


def close_chat_tabs() -> None:
    """Close temporary-chat tabs a killed run left open in the agent's Chrome."""
    import urllib.request, ui
    try:
        for t in json.loads(urllib.request.urlopen(f"{ui.CDP}/json/list", timeout=10).read()):
            if t.get("type") == "page" and "temporary-chat=true" in t.get("url", ""):
                ui.browser_call("Target.closeTarget", targetId=t["id"])
    except Exception:  # noqa: BLE001
        pass


def cmd_supervise(a) -> int:
    """Run `run` end to end without anyone watching: restart it when it exits early (Stall = exit 75: quota or failing
    chats, retried after 10 min; a crash, after 1 min) and kill and restart it when its heartbeat goes quiet for
    --stall-min minutes (a hang nothing else caught). Every answer is cached, so a restart resumes where it stopped.
    Gives up after --max-restarts restarts or --budget-h hours, writing why to log.md."""
    import subprocess
    argv, skip = [], 0
    for x in sys.argv[2:]:
        if skip:
            skip -= 1
        elif x in SUPERVISE_ONLY:
            skip = SUPERVISE_ONLY[x]
        else:
            argv.append(x)
    cmd = [sys.executable, str(Path(__file__).resolve()), "run", *argv]
    out = run_dir(a)
    out.mkdir(parents=True, exist_ok=True)
    hb, t0, restarts = out / "heartbeat.json", time.time(), 0
    while True:
        started = time.time()
        print(f"supervise: starting run ({E.now_iso()})", flush=True)
        proc = subprocess.Popen(cmd)
        while proc.poll() is None:
            time.sleep(30)
            quiet = time.time() - max(hb.stat().st_mtime if hb.exists() else 0, started)
            if quiet > a.stall_min * 60:
                print(f"supervise: no heartbeat for {quiet / 60:.0f} min: killing the run", flush=True)
                proc.terminate()
                try:
                    proc.wait(30)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()
                close_chat_tabs()
                break
        rc = proc.returncode
        if rc == 0:
            print("supervise: run finished", flush=True)
            return 0
        restarts += 1
        hours = (time.time() - t0) / 3600
        if restarts > a.max_restarts or hours > a.budget_h:
            why = (f"\nSupervisor gave up ({E.now_iso()}): run exited {rc}, {restarts - 1} restarts, {hours:.1f} h. "
                   "Answers so far are cached; rerun `supervise` with the same arguments to resume.\n")
            with (out / "log.md").open("a") as fh:
                fh.write(why)
            print(why, flush=True)
            return rc or 1
        delay = 600 if rc == 75 else 60
        print(f"supervise: run exited {rc}; restart {restarts}/{a.max_restarts} in {delay // 60} min", flush=True)
        time.sleep(delay)


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


def _stage_shot(rec: dict, png: Path) -> dict:
    if not (png.exists() and png.with_suffix(".boxes.json").exists()):
        snapshot(rec, png)
    return json.loads(png.with_suffix(".boxes.json").read_text())


def _changed(before: list[dict], after: list[dict]) -> tuple[list[int], list[int], list[tuple[str, str]]]:
    """Text blocks that differ between two renders: indexes in each, and (before, after) text pairs."""
    sm = difflib.SequenceMatcher(None, [b["text"] for b in before], [b["text"] for b in after], autojunk=False)
    bi, ai, pairs = [], [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            continue
        bi += range(i1, i2)
        ai += range(j1, j2)
        pairs.append((" / ".join(b["text"] for b in before[i1:i2]), " / ".join(b["text"] for b in after[j1:j2])))
    return bi, ai, pairs


def _words(before: str, after: str) -> tuple[str, str]:
    """Word-level diff as HTML: removed words struck in `before`, added words marked in `after`."""
    import html as H
    bw, aw = before.split(), after.split()
    sm = difflib.SequenceMatcher(None, bw, aw, autojunk=False)
    bo, ao = [], []
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        bs, as_ = H.escape(" ".join(bw[i1:i2])), H.escape(" ".join(aw[j1:j2]))
        if op == "equal":
            bo.append(bs); ao.append(as_)
        else:
            if bs:
                bo.append(f"<del>{bs}</del>")
            if as_:
                ao.append(f"<ins>{as_}</ins>")
    return " ".join(bo), " ".join(ao)


def _svg(png: str, shot: dict, idx: list[int], view: tuple[int, int, int, int] | None = None) -> str:
    w, h = shot["width"], shot["height"]
    vx, vy, vw, vh = view or (0, 0, w, h)
    rects = "".join(f'<rect x="{b["x"] - 6}" y="{b["y"] - 5}" width="{b["w"] + 12}" height="{b["h"] + 10}" rx="4"/>'
                    for b in (shot["blocks"][i] for i in idx))
    return (f'<svg class="shot" viewBox="{vx} {vy} {vw} {vh}" role="img"><image href="{png}" width="{w}" height="{h}"/>'
            f"{rects}</svg>")


def _zoom(shot: dict, idx: list[int]) -> tuple[int, int, int, int] | None:
    if not idx:
        return None
    bs = [shot["blocks"][i] for i in idx]
    y0, y1 = min(b["y"] for b in bs) - 40, max(b["y"] + b["h"] for b in bs) + 40
    y1 = min(y1, y0 + 900)
    return (0, max(0, y0), shot["width"], y1 - max(0, y0))


def cmd_winners(a) -> None:
    """The winners report (Barry 11-01): a screenshot of the page each round ended with, the changes from the page
    before it boxed in red, and what changed and why it won. Writes <run>/winners/index.html plus its images; publish
    the folder as an artifact after each round."""
    import html as H
    tgt = TARGETS[a.target]
    out = run_dir(a) if a.run else sorted((RUNS / a.target / "iterate").iterdir())[-1]
    wd = out / "winners"
    wd.mkdir(exist_ok=True)
    rounds = [json.loads(f.read_text()) for f in sorted(out.glob("round-*.json"))]
    if not rounds:
        print("no rounds yet")
        return
    stages = [{"name": "published", "label": "The published page (round 1 base)", "rec": rounds[0]["incumbent"]["record"],
               "score": rounds[0]["incumbent"]["score"]}]
    for r in rounds:
        w = next((v for v in r["variants"] if str(v.get("decision", "")).startswith("new base")), None)
        if w:
            stages.append({"name": f"round-{r['round']:02d}", "label": f"Round {r['round']} winner: {w['dimension']}",
                           "rec": w["record"], "score": w["score"], "base": r["incumbent"]["score"], "change": w["change"],
                           "round": r["round"], "others": [v for v in r["variants"] if v is not w]})
    shots = [_stage_shot(st["rec"], wd / f"{st['name']}.png") for st in stages]
    fmt = lambda s: f"M1 {s['m1']:.0%} · M2 {s['m2']:.0%} · {s['linked']} linked"   # noqa: E731
    secs = []
    for k in range(1, len(stages)):
        st, prev = stages[k], stages[k - 1]
        bi, ai, pairs = _changed(shots[k - 1]["blocks"], shots[k]["blocks"])
        rows = "".join(f"<tr><td>{_words(b, t)[0] or '<i>(none)</i>'}</td><td>{_words(b, t)[1] or '<i>(removed)</i>'}</td></tr>"
                       for b, t in pairs)
        lost = "".join(f"<li>{H.escape(v['dimension'])}: {H.escape(v.get('decision', ''))}"
                       + (f" ({v['score']['m1']:.0%})" if v.get("score") else "") + "</li>" for v in st["others"])
        secs.append(f"""<section class="stage">
  <h2>{H.escape(st['label'])}</h2>
  <p class="change">{H.escape(st['change'])}</p>
  <p class="scores"><span>Base ({H.escape(prev['name'])}): {fmt(st['base'])}</span><span class="win">Winner: {fmt(st['score'])}</span></p>
  <h3>Close-up: red boxes mark the changed blocks</h3>
  <div class="pair"><figure><figcaption>Before</figcaption>{_svg(prev['name'] + '.png', shots[k - 1], bi, _zoom(shots[k - 1], bi))}</figure>
  <figure><figcaption>After</figcaption>{_svg(st['name'] + '.png', shots[k], ai, _zoom(shots[k], ai))}</figure></div>
  <h3>What changed, block by block</h3>
  <div class="tbl"><table><thead><tr><th>Before</th><th>After</th></tr></thead><tbody>{rows}</tbody></table></div>
  <details><summary>Full pages</summary><div class="pair full"><figure>{_svg(prev['name'] + '.png', shots[k - 1], bi)}</figure>
  <figure>{_svg(st['name'] + '.png', shots[k], ai)}</figure></div></details>
  <p class="others">Other variants this round:</p><ul class="others">{lost}</ul>
</section>""")
    if len(stages) == 1:
        secs.append('<p class="lede">No round has produced a winner yet. The published page is below.</p>'
                    f'<figure>{_svg("published.png", shots[0], [])}</figure>')
    status = "; ".join(f"round {r['round']}: " + (r["accepted"] or "base kept") for r in rounds)
    page = WINNERS_HTML.format(title=f"{tgt['slug']} round winners", run=H.escape(out.name), slug=H.escape(tgt["slug"]),
                               status=H.escape(status), body="\n".join(secs))
    (wd / "index.html").write_text(page)
    print(wd / "index.html")


WINNERS_HTML = """<title>Round Winners: {run}</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>
/* One section per winning round: the change, the scores, then before/after screenshots with the changed blocks boxed. */
:root {{ --bg:#f6f7f8; --surface:#fff; --fg:#1b2228; --muted:#5d6a74; --line:#dde2e6; --mark:#e0242b; --win:#157347;
  --sans: system-ui, -apple-system, "Segoe UI", sans-serif; }}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --bg:#12171b; --surface:#1a2126; --fg:#e6eaed;
  --muted:#97a3ad; --line:#2c353c; --mark:#ff4d52; --win:#4cc38a; color-scheme: dark }} }}
:root[data-theme="dark"] {{ --bg:#12171b; --surface:#1a2126; --fg:#e6eaed; --muted:#97a3ad; --line:#2c353c; --mark:#ff4d52;
  --win:#4cc38a; color-scheme: dark }}
body {{ background:var(--bg); color:var(--fg); font:15px/1.55 var(--sans); margin:0; }}
main {{ max-width:1120px; margin:0 auto; padding:28px max(16px, env(safe-area-inset-right, 0px)) 56px max(16px, env(safe-area-inset-left, 0px));
  display:grid; gap:36px; }}
h1 {{ font-size:26px; margin:0; }} h2 {{ font-size:20px; margin:0; }} h3 {{ font-size:13px; text-transform:uppercase;
  letter-spacing:.07em; color:var(--muted); margin:14px 0 8px; }}
.lede, .change {{ max-width:72ch; margin:0; }} .lede {{ color:var(--muted); }}
.stage {{ display:grid; gap:8px; }}
.scores {{ display:flex; flex-wrap:wrap; gap:6px 18px; font-variant-numeric:tabular-nums; color:var(--muted); margin:0; }}
.scores .win {{ color:var(--win); font-weight:600; }}
.pair {{ display:grid; grid-template-columns:1fr 1fr; gap:14px; }} .pair > * {{ min-width:0; margin:0; }}
figcaption {{ font-size:13px; color:var(--muted); margin-bottom:4px; }}
svg.shot {{ display:block; width:100%; height:auto; border:1px solid var(--line); border-radius:4px; background:#fff; }}
svg.shot rect {{ fill:none; stroke:var(--mark); stroke-width:4; }} .full svg.shot rect {{ stroke-width:9; }}
.tbl {{ overflow-x:auto; background:var(--surface); border:1px solid var(--line); border-radius:6px; }}
table {{ border-collapse:collapse; width:100%; font-size:14px; }} td, th {{ text-align:left; vertical-align:top;
  padding:8px 10px; border-bottom:1px solid var(--line); width:50%; }} th {{ font-size:12px; color:var(--muted); }}
del {{ color:var(--mark); }} ins {{ text-decoration:none; background:color-mix(in srgb, var(--win) 22%, transparent); border-radius:2px; }}
details summary {{ cursor:pointer; color:var(--muted); margin-top:8px; }}
.others {{ color:var(--muted); font-size:14px; margin:4px 0 0; }}
@media (max-width:720px) {{ .pair {{ grid-template-columns:1fr; }} }}
</style>
<main>
<header style="display:grid;gap:8px"><h1>Round winners: {slug}</h1>
<p class="lede">Iterate run {run}. Each section shows the page a round ended with next to the page it started from; red boxes mark the text blocks that changed, and the table marks removed words in red strike-through and added words in green. Rounds without a winner kept their base. {status}.</p></header>
{body}
</main>
"""


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
    for name in ("run", "supervise"):
        p = sub.add_parser(name); p.add_argument("--target", default="rv-2kwh", choices=sorted(TARGETS)); p.add_argument("--run")
        p.add_argument("--engine", choices=["open", "app", "api"], default="open"); p.add_argument("--model", default="gpt-6.1-sol")
        p.add_argument("--rank", type=int)
        p.add_argument("--packs", help="comma-separated result sets instead of the target's (smoke tests)")
        p.add_argument("--paste", default="c1"); p.add_argument("--fmt", default="v1")
        p.add_argument("--variants", type=int, default=3); p.add_argument("--reps", type=int, default=1)
        p.add_argument("--max-rounds", type=int, default=6); p.add_argument("--patience", type=int, default=3)
        p.add_argument("--margin", type=float, default=0.10); p.add_argument("--final-reps", type=int)
        p.add_argument("--final-answers", type=int, default=36, help="final check: answers per page, spread over the sets")
        p.add_argument("--models", default="gpt-6,gpt-6-mini",
                       help="accepted answer models, preferred first; one model = strict (off-model answers dropped)")
        p.add_argument("--max-wait", type=float, default=60, help="minutes of quota waiting before the run stops (exit 75)")
        p.add_argument("--final-only", action="store_true", help="skip the rounds; run only the final check")
        p.add_argument("--final-tag", help="write the final check to final-<tag>/ (a second check, e.g. on one model)")
        if name == "supervise":
            p.add_argument("--stall-min", type=float, default=30); p.add_argument("--budget-h", type=float, default=16)
            p.add_argument("--max-restarts", type=int, default=8)
    for name in ("show", "diff", "winners"):
        p = sub.add_parser(name); p.add_argument("--target", default="rv-2kwh", choices=sorted(TARGETS)); p.add_argument("--run")
    a = ap.parse_args()
    return {"run": cmd_run, "supervise": cmd_supervise, "show": cmd_show, "diff": cmd_diff, "winners": cmd_winners}[a.cmd](a) or 0


if __name__ == "__main__":
    sys.exit(main())
