#!/usr/bin/env python3
"""Research-method pages (DLC-208, Barry 2026-11-08): the citation A/B test's group A and every new gap page from 11-08.

Plan: growth/evals/runs/2026-11-07-liveplain/page/citation-ab-plan.html. Evidence for the method:
growth/evals/runs/2026-11-07-liveplain/page/research-angles.html.

    python3.12 tools/abpage.py harvest  <slug>... [--runs <run dir>...]   # ChatGPT's searches, top 12, carousel, picks
    python3.12 tools/abpage.py research <slug>... [--workers 3]           # 6 angle agents -> compose -> verify -> draft
    python3.12 tools/abpage.py apply    <slug>... [--local]               # draft -> gaps.py record -> build -> gates
    python3.12 tools/abpage.py status

Per page, everything lives under growth/focus/ab/<slug>/:
    harvest.json   what ChatGPT did with the page's own query: its search words, the results, the products it showed
                   as catalog cards, its answer and which result each citation backed (from the saved app chats)
    angle-<X>.json one research agent per angle, all six run (Barry 11-08: "send research agents in all angles, then
                   decide on one in view of how it stands out from the competitor pages")
    compose.json   the agent that reads the six and the competitor pages, picks the angle and writes the page
    verify.json    a second agent that opens every source and drops what it can't confirm
    draft.json     the page and any new product records, ready for `apply`

Research runs in `claude -p` (plan usage): Fable 5.1 at high effort, and Opus 5.5 at high effort once Fable is out of
usage (Barry 11-08). The agents never edit files; this script writes src/ only in `apply`.
"""
from __future__ import annotations

import argparse
import ast
import concurrent.futures as cf
import datetime as _dt
import json
import re
import subprocess
import sys
import threading
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "growth" / "evals"))
sys.path.insert(0, str(ROOT / "tools"))
AB = ROOT / "growth/focus/ab"
RUNS = ROOT / "growth/evals/runs"
DEFAULT_RUNS = ["2026-11-07-liveplain", "2026-11-07-liveplain-rest"]
MODELS = [("claude-fable-5-1", "high"), ("claude-opus-5-5", "high")]
METHOD = "ab-2026-11"
_fable_out = threading.Event()   # set once Fable reports a usage limit; every later call goes straight to Opus
SLOTS = threading.Semaphore(6)   # claude -p processes at once, across pages

ANGLES = {
    "A": ("Normalise", "Specs the makers state differently, made comparable: cycle life to 80% vs 70%, surge vs continuous, "
          "cooking vs input watts, a feature that works on stock firmware vs only with a script. One table where the "
          "footnote is the finding."),
    "B": ("Derive", "The number the question is really asking, computed for every candidate from sourced inputs: Wh per lb, "
          "reheats per charge, hours at a stated duty cycle, refill hours from the kit's own panel, cost per usable Wh. "
          "The arithmetic must fit in one line per figure."),
    "C": ("Compatibility", "Exact pairings and limits: which accessory, cable, firmware, generation or region works with "
          "which model, with the maker's document for each cell and the exclusions the maker states."),
    "D": ("Mechanism", "The one physical, electrical or software reason that decides whether the shopper's plan works at "
          "all (flame rectification, PCIe lanes, a driver missing on stock firmware, USB passthrough limits), in the "
          "maker's, standard's or project's own words."),
    "E": ("Named measurements", "Measurements by named reviewers or labs (RTINGS, Notebookcheck, SoundGuys, a magazine's "
          "lab), collected side by side for the candidates, each with who measured it, the figure and the date."),
    "F": ("Whole category, priced", "Every model the shopper and ChatGPT would consider for this question (ChatGPT's own "
          "picks and catalog cards, our products, what the cited rival pages list), each priced from the maker's or "
          "the shown retailer's page today with the date, and the one reason each loses where it loses."),
}


def today() -> str:
    return _dt.date.today().isoformat()


def sh(*cmd, check=False, **kw) -> subprocess.CompletedProcess:
    return subprocess.run(list(cmd), cwd=ROOT, capture_output=True, text=True, check=check, **kw)


def pdir(slug: str) -> Path:
    d = AB / slug
    d.mkdir(parents=True, exist_ok=True)
    return d


def jload(p: Path, default=None):
    return json.loads(p.read_text()) if p.exists() else default


def jsave(p: Path, obj) -> None:
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- harvest

def _norm(u: str) -> str:
    return (u or "").split("?")[0].split("#")[0].rstrip("/").replace("www.", "")


def _chat_facts(c: dict) -> dict:
    r = c.get("response") or {}
    markup = "\n\n".join(r.get("markup") or [])
    cited = {_norm(x.get("url")) for x in (c.get("citations") or []) + (c.get("cite_pills") or [])}
    cited |= {_norm(u.get("url")) for u in r.get("markup_urls") or []}
    cited.discard("")
    res = []
    for i, x in enumerate(r.get("search_results") or [], 1):
        u = x.get("url") or ""
        pd = _dt.datetime.fromtimestamp(x["pub_date"], _dt.UTC).date().isoformat() if x.get("pub_date") else None
        res.append({"rank": i, "domain": (x.get("domain") or urlparse(u).netloc).replace("www.", ""), "title": x.get("title"),
                    "url": u, "dated": pd, "cited": _norm(u) in cited, "ours": "dealectric.com" in u})
    carousel = list(dict.fromkeys(re.findall(r'<Entity category="product"[^>]*value="([^"]+)"', markup)))
    return {"chat": c.get("qid"), "at": c.get("started_at"), "model": c.get("answer_model"), "typed": c.get("prompt"),
            "queries": c.get("queries") or [], "results": res, "carousel": carousel,
            "cited_elsewhere": sorted(u for u in cited if u and not any(_norm(x["url"]) == u for x in res)),
            "answer": (c.get("text") or "")[:8000]}


def harvest(slug: str, runs: list[str]) -> dict:
    chats = []
    for run in runs:
        for f in sorted((RUNS / run / "chatgpt").glob("*.json")):
            try:
                c = json.loads(f.read_text())
            except ValueError:
                continue
            if c.get("slug") == slug and (c.get("answer_model") or "").startswith("gpt-6") and not (c.get("answer_model") or "").endswith("mini"):
                chats.append(_chat_facts(c))
    old = jload(pdir(slug) / "harvest.json", {"chats": []})
    seen = {(x["chat"], x["at"]) for x in old["chats"]}
    allc = old["chats"] + [x for x in chats if (x["chat"], x["at"]) not in seen]
    tags = []
    for ch in allc:
        for q in ch["queries"]:
            q = re.sub(r"\b(January|February|March|April|May|June|July|August|September|October|November|December)\b\s*", "", q).strip()
            q = re.sub(r"\s{2,}", " ", q)
            if q and q.lower() not in {t.lower() for t in tags}:
                tags.append(q)
    h = {"slug": slug, "updated": today(), "chats": allc, "searched_as": tags[:6],
         "carousel": list(dict.fromkeys(p for ch in allc for p in ch["carousel"])),
         "cited_rivals": list(dict.fromkeys(x["url"] for ch in allc for x in ch["results"] if x["cited"] and not x["ours"]))}
    jsave(pdir(slug) / "harvest.json", h)
    return h


# ---------------------------------------------------------------- claude -p

def claude(prompt: str, tools: bool = True, timeout: int = 3600) -> dict:
    """One agent call. Fable at high effort first; on a usage-limit reply, Opus at high effort from then on."""
    import evallib as E
    t = str(ROOT / "tools")
    allowed = ["WebSearch", "WebFetch", f"Bash(python3.12 {t}/storecheck.py:*)", f"Bash(python3.12 {t}/amzcheck.py:*)"]
    last = None
    for model, effort in MODELS:
        if model.startswith("claude-fable") and _fable_out.is_set():
            continue
        cmd = [E.claude_cli(), "-p", prompt, "--model", model, "--effort", effort, "--output-format", "json"]
        cmd += (["--tools", "WebSearch,WebFetch,Bash", "--allowedTools", *allowed] if tools else ["--tools", ""])
        for attempt in range(4):   # transient 429 / overloaded: wait and retry the same model
            with SLOTS:
                p = subprocess.run(cmd + list(E.CLI_ISOLATION), capture_output=True, text=True, timeout=timeout, cwd=E.cli_cwd())
            try:
                d = json.loads(p.stdout)
            except ValueError:
                d = {"is_error": True, "result": (p.stderr or p.stdout)[-600:]}
            msg = str(d.get("result") or "")
            if d.get("is_error") and re.search(r"overloaded|\b429\b|rate limit|try again", msg, re.I) and not re.search(r"usage limit|limit reached|reached your \w+ limit|out of (extra )?usage|usage credits", msg, re.I):
                import time
                time.sleep(90 * (attempt + 1))
                continue
            break
        if d.get("is_error") and re.search(r"usage limit|limit reached|reached your \w+ limit|out of (extra )?usage|weekly limit|session limit|usage credits", msg, re.I):
            if model.startswith("claude-fable"):
                _fable_out.set()
                print(f"[abpage] Fable out of usage ({msg[:120]}); Opus 5.5 high from now on", flush=True)
            last = {"status": "error", "reason": msg[:400], "model": model}
            continue
        if d.get("is_error"):
            return {"status": "error", "reason": msg[:400], "model": model}
        out = None
        dec = json.JSONDecoder()
        for i in [m.start() for m in re.finditer(r"\{", msg)][:40]:   # the first complete JSON object in the reply
            try:
                obj, _ = dec.raw_decode(msg[i:])
            except ValueError:
                continue
            if isinstance(obj, dict) and len(json.dumps(obj)) > 40:
                out = obj
                break
        if out is None:
            out = {"status": "error", "reason": "no parsable JSON in the reply", "raw": msg[-2000:]}
        out["_meta"] = {"model": model, "effort": effort, "turns": d.get("num_turns"), "cost_usd_list": d.get("total_cost_usd")}
        return out
    return last or {"status": "error", "reason": "no model answered"}


# ---------------------------------------------------------------- prompts

def _ours_list() -> str:
    import products as P
    return "\n".join(f"{p['slug']} | {p['brand']} | {p['category']} | {p['program']} | {p['name']}" for p in P.PRODUCTS)


def _programs() -> str:
    import gappage
    return "\n".join(f"{k}: {v}" for k, v in gappage.programs().items())


def _existing(slug: str) -> dict | None:
    import gaps
    return next((g for g in gaps.GAP_PAGES if g["slug"] == slug), None)


def _harvest_text(h: dict) -> str:
    out = []
    for ch in h["chats"]:
        out.append(f"### Chat {ch['chat']} ({ch['at']}, {ch['model']})\nShopper typed: {ch['typed']}\nChatGPT searched: "
                   + " | ".join(ch["queries"]) + "\nResults it got (rank. domain | title | url | dated | cited?):\n"
                   + "\n".join(f"{r['rank']}. {r['domain']} | {r['title']} | {r['url']} | {r['dated'] or '-'} | "
                               f"{'CITED' if r['cited'] else ''}{' (ours)' if r['ours'] else ''}" for r in ch["results"])
                   + "\nProducts it showed as catalog cards: " + (", ".join(ch["carousel"]) or "none")
                   + "\nIts answer as the shopper saw it (card titles and prices included):\n" + ch["answer"][:6000])
    return "\n\n".join(out)


COMMON_RULES = """Rules for every agent on this project (Dealectric, dealectric.com, an affiliate site for consumer electronics):
- Every fact you report carries a source URL you actually opened and the date you read it. Never trust a search snippet
  for a price or for a spec that decides a pick: open the page. Maker's US product page first, then the manual or spec
  PDF, then a named reviewer with the number.
- If you can't source a figure after those three, leave it out and say in "unsourced" what you looked for. Never write
  "not confirmed", "not found" or "unknown" as a value.
- Prices: the maker's US store (or the retailer ChatGPT showed) today, with the date. Shopify stores:
  `python3.12 TOOLS/storecheck.py search <store home> "<words>"` / `product <url>`. Amazon: `TOOLS/amzcheck.py`
  (Amazon may wall it; then skip Amazon prices).
- Judgement is allowed only with a name on it ("Notebookcheck measured 14.8 W idle"), never "reviewers say".
- Spend about 25 tool calls at most. Your final message is ONE JSON object, nothing else."""


def angle_prompt(slug: str, letter: str, h: dict, query: str) -> str:
    name, what = ANGLES[letter]
    ex = _existing(slug)
    return "\n\n".join([
        COMMON_RULES.replace("TOOLS", str(ROOT / "tools")),
        f"## Your job: research ONE angle, \"{letter}. {name}\", for the shopper question below\n{what}",
        "The page this feeds must hold one fact the answer needs that none of the results ChatGPT got already states. "
        "So read the cited rival pages (and the top results) first, then research your angle for the candidate products, "
        "then judge how much your angle's best finding would stand out against those pages.",
        f"## Today\n{today()}",
        f"## The shopper question\n{query}",
        "## What ChatGPT did with it (saved app chats)\n" + _harvest_text(h),
        ("## Our current page for this question (being rebuilt)\n" + json.dumps({k: ex.get(k) for k in ("title", "h1", "columns", "rows")}, ensure_ascii=False)[:5000]) if ex else "",
        "## Products Dealectric already lists (slug | brand | category | program | name)\n" + _ours_list(),
        """## Output JSON
{"angle": "%s",
 "gap": "<one sentence: 'No result ChatGPT got states <X>.' X is your angle's best finding>",
 "standout": <0-3: 0 = a cited rival already has it, 1 = rivals have part of it, 2 = new and useful, 3 = new and it decides the pick>,
 "standout_why": "<which rival pages you compared against and what they lack>",
 "decides": "<how the finding changes or confirms the pick for this question>",
 "candidates": ["<brand model>", ...],
 "findings": [{"product": "<brand model or 'general'>", "label": "<what>", "value": "<value with unit>", "source": "<url>", "source_title": "<title>", "read": "YYYY-MM-DD", "note": "<method, conditions, arithmetic>"}],
 "unsourced": ["<what you looked for and could not source>"]}""" % letter,
    ])


def compose_prompt(slug: str, h: dict, query: str, angles: dict, new_page: bool) -> str:
    ex = _existing(slug)
    fixed = ("" if new_page else
             f"\n## Fixed for this page (A/B test: retrieval must not move)\nslug {slug}; title {ex['title']!r}; h1 {ex['h1']!r}; "
             f"desc may be rewritten. The first sentence of the answer must keep the question's own words.")
    return "\n\n".join([
        COMMON_RULES.replace("TOOLS", str(ROOT / "tools")),
        """## Your job: decide the page's angle and write the page
Six research agents each researched one angle for this question (below). Read them and the rival pages ChatGPT cited.
Pick the ONE angle whose finding (a) no result ChatGPT got already states, (b) the answer needs, and (c) is fully sourced.
Prefer the angle with the highest standout that is complete across the candidates. Angle F (category, priced) is not
chosen as the angle; its rows and prices go in every page's table.
Then write the page. Layout (the renderer adds the H1, an 'Updated <date>' line, the search-phrase tags, the method
line, the table's Price and Buy columns, sources and the disclosure):
- answer: ONE paragraph, at most 300 characters of text, as
  <p class="lead"><strong>Short answer.</strong> ...</p>
  It answers the question's mechanism in the question's own words, names the pick and carries the angle's deciding
  figure. Use as many of ChatGPT's own search words (listed under "ChatGPT searched") as read naturally: the length
  model ChatGPT applies keeps the passages that share the most words with its query. No link and no {buy:} token in
  it (the renderer puts the first row's buy link under the H1, so put the pick first in rows when it is ours).
- columns: 3-6 [key, label] pairs carrying the angle's finding and the deciding specs (not price: the renderer adds it).
- rows: 4-8 candidates, the pick first. Our products: {"slug", "model", "cells"}. Others: {"brand", "model", "url"
  (maker page), "cells"} and cells.price = "$X (maker, YYYY-MM-DD)". Every cell filled from a source; drop a column
  rather than leave cells empty. A short cell note may name its source ("Notebookcheck").
- after: HTML, 2-3 <h2> sections: "What the differences mean" (the derived figures with one line of arithmetic each,
  and a small 'which fits which use' table), the angle section (mechanism / compatibility detail / collected
  measurements), and "Not recommended" if one candidate is a trap. {buy:slug} may appear here, once per product at most.
- sources: 6-14 [claim, url] pairs, one per figure group, each a page you or the angle agents opened.
- The pick must truly win the question. If it isn't a product we list, say so and name it; our product then wins the
  segment it honestly wins. Earning routes: approved CJ/Awin/Rakuten brands (list below), Amazon Associates.
  Amazon records: no $ anywhere in their text (Amazon's rules).
- No copy addressed to AI assistants, never "guaranteed", no "not confirmed" / "not found" anywhere.
- The page is written for the shopper. Never mention ChatGPT, its answer, its search, "the results" or "other pages"
  in the page: what the rivals lack is your reason for the angle (why_angle), not page copy.""" + fixed + ("" if not new_page else
            "\n## Slug\nA new page slug for the question (e.g. best-power-bank-for-phone), lowercase words and hyphens, "
            "8-90 characters. Never a product slug."),
        f"## Today\n{today()}",
        f"## The shopper question\n{query}",
        "## What ChatGPT did with it\n" + _harvest_text(h),
        "## The six angle reports\n" + json.dumps(angles, ensure_ascii=False)[:60000],
        "## Approved programs\n" + _programs(),
        "## Products already on the site (reuse these slugs; add a product record only when needed)\n" + _ours_list(),
        """## Output JSON
{"status": "ok" | "skip", "reason": "<if skip>",
 "angle": "<A-E>", "why_angle": "<one or two sentences: what the cited rivals lack that this page now has>",
 "slug": "<slug>", "must": ["<exact phrase from the answer carrying the pick>", "<exact phrase carrying the deciding figure>"],
 "products": [<new product records only, keys as src/products.py: slug, brand, program, asin (Amazon), category, name, model, url, price (number; null for Amazon), verified, specs [[label, value]], warranty, returns, summary, fit, caveats [..]>],
 "page": {"title", "h1", "desc", "answer", "columns": [[key, label]], "rows": [...], "after", "sources": [[claim, url]]}}""",
    ])


def verify_prompt(draft: dict) -> str:
    return "\n\n".join([
        COMMON_RULES.replace("TOOLS", str(ROOT / "tools")),
        """## Your job: verify a page before it is published
Open every source URL in the draft below and check every figure in the answer, the table cells and the after-section
against them (and against the maker's page where a cell names no source). Prices: re-read today.
- A figure that its source doesn't support: correct it if the source gives the right value, otherwise remove it (drop
  the cell's column for all rows if it leaves a hole, or the row). Never invent a replacement.
- A source that loads but doesn't hold the claim: remove it from sources and re-check what relied on it.
- A source that won't load for you (HTTP 403/429, timeout, bot wall) is NOT a failed claim: try another copy of the
  same fact (the maker's manual, a retailer listing, an archived copy). If none loads, keep the figure as the research
  agents recorded it today and note it in the log as "not re-read: <why>". Remove a figure only when a page you could
  read contradicts it or holds something else.
- Rows with a "slug" are products Dealectric lists: their price and code come from Dealectric's own daily-checked
  records, not from the cells, so never remove such a row over a price you couldn't re-read.
- Keep everything else exactly as written: same keys, same HTML, same must phrases unless you had to change them (then
  keep them exact substrings of the answer).
Return the full corrected draft plus a log.""",
        f"## Today\n{today()}",
        "## Draft\n" + json.dumps(draft, ensure_ascii=False),
        """## Output JSON
{"draft": <the full corrected draft, same shape>, "checked": <number of figures checked>, "changed": [{"where": "...", "was": "...", "now": "...", "why": "..."}], "removed": [{"where": "...", "why": "..."}]}""",
    ])


def fix_prompt(draft: dict, errs: list[str]) -> str:
    return "\n\n".join([
        COMMON_RULES.replace("TOOLS", str(ROOT / "tools")),
        "## Your job: fix a page draft that failed its checks\nFix exactly these errors and nothing else. Missing facts "
        "(a product's warranty, returns, a spec) must be read from the maker's own page today, with the source added to "
        "the page's sources if it is a page figure. If a fact can't be sourced, drop what needs it (the product record and "
        "its row, or the cell's column) rather than invent it. Banned wording: rewrite the sentence for the shopper.",
        "## Errors\n" + "\n".join(f"- {e}" for e in errs),
        f"## Today\n{today()}",
        "## Draft\n" + json.dumps({k: v for k, v in draft.items() if k not in ("gate",)}, ensure_ascii=False),
        '## Output JSON\n{"draft": <the full corrected draft, same shape>, "log": ["<what you changed and from which source>"]}',
    ])


# ---------------------------------------------------------------- research

def query_for(slug: str, h: dict) -> str:
    for ch in h["chats"]:
        if ch.get("typed"):
            return ch["typed"]
    ex = _existing(slug)
    return ex["h1"] if ex else slug.replace("-", " ")


def research(slug: str, new_page: bool = False, force: bool = False) -> dict:
    d = pdir(slug)
    import os
    lock = d / ".lock"
    try:
        fd = os.open(lock, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, str(os.getpid()).encode()); os.close(fd)
    except FileExistsError:
        pid = lock.read_text().strip()
        if pid.isdigit() and Path(f"/proc/{pid}").exists() or (pid.isdigit() and subprocess.run(["kill", "-0", pid], capture_output=True).returncode == 0):
            return {"slug": slug, "status": "locked by another process"}
        lock.write_text(str(os.getpid()))   # stale lock from a stopped process
    try:
        return _research(slug, new_page, force, d)
    finally:
        lock.unlink(missing_ok=True)


def _research(slug: str, new_page: bool, force: bool, d: Path) -> dict:
    if not force and (d / "draft.json").exists():
        dr = jload(d / "draft.json", {})
        return {"slug": slug, "status": "drafted", "angle": dr.get("angle"), "model": "cached"}
    h = jload(d / "harvest.json")
    if not h or not h["chats"]:
        return {"slug": slug, "status": "no harvest"}
    q = query_for(slug, h)
    todo = [x for x in ANGLES if force or not (d / f"angle-{x}.json").exists() or jload(d / f"angle-{x}.json", {}).get("status") == "error"]
    with cf.ThreadPoolExecutor(max_workers=len(ANGLES)) as ex:
        for x, out in zip(todo, ex.map(lambda x: claude(angle_prompt(slug, x, h, q)), todo)):
            jsave(d / f"angle-{x}.json", out)
    angles = {x: {k: v for k, v in jload(d / f"angle-{x}.json", {}).items() if k != "_meta"} for x in ANGLES}
    if sum(1 for a in angles.values() if a.get("findings")) < 3:
        return {"slug": slug, "status": "error", "reason": "fewer than 3 angle reports came back"}
    comp = jload(d / "compose.json")
    if force or not comp or comp.get("status") not in ("ok", "skip"):
        comp = claude(compose_prompt(slug, h, q, angles, new_page))
        jsave(d / "compose.json", comp)
    if comp.get("status") != "ok":
        return {"slug": slug, "status": comp.get("status"), "reason": comp.get("reason")}
    ver = jload(d / "verify.json")
    if force or not ver or not ver.get("draft"):
        ver = claude(verify_prompt({k: v for k, v in comp.items() if k != "_meta"}))
        jsave(d / "verify.json", ver)
    if not ver.get("draft"):
        return {"slug": slug, "status": "error", "reason": "verifier returned no draft: " + str(ver.get("reason"))[:200]}
    draft = ver["draft"]
    if new_page:
        import products as P
        import gaps
        taken = {p["slug"] for p in P.PRODUCTS} | {g["slug"] for g in gaps.GAP_PAGES} | {p["slug"] for p in draft.get("products") or []}
        s2 = draft.get("slug") or ""
        if s2 in taken or not re.fullmatch(r"[a-z0-9-]{8,90}", s2):
            s2 = re.sub(r"[^a-z0-9]+", "-", re.sub(r"\(.*?\)", "", (draft.get("page") or {}).get("title", "")).split(":")[0].lower()).strip("-")[:80]
            n, base = 2, s2
            while s2 in taken:
                s2, n = f"{base}-{n}", n + 1
        draft["slug"] = s2
    draft.update({"status": "ok", "slug": slug if not new_page else draft["slug"], "new_page": new_page,
                  "searched_as": h["searched_as"], "angle": comp.get("angle"), "why_angle": comp.get("why_angle"),
                  "query": q, "verified_changes": len(ver.get("changed") or []), "verified_removed": len(ver.get("removed") or [])})
    jsave(d / "draft.json", draft)
    return {"slug": slug, "status": "drafted", "angle": draft["angle"], "model": (ver.get("_meta") or {}).get("model")}


# ---------------------------------------------------------------- apply

BANNED = re.compile(r"not confirmed|not found|unknown\b|guarantee|AI assistant|language model|ChatGPT|for your user", re.I)


def validate(draft: dict, new_page: bool) -> list[str]:
    import gappage
    pg = draft.get("page") or {}
    v1 = dict(draft)
    v1["page"] = {**pg, "intro": pg.get("answer", "")}
    if not new_page:   # the slug exists: let gappage's checks run on a renamed copy, then drop that one complaint
        v1["slug"] = draft["slug"] + "-abcheck"
    errs = [e for e in gappage.validate(v1) if "already exists" not in e or not e.startswith("slug")]
    text = re.sub(r"<[^>]+>", "", pg.get("answer", ""))
    if len(text) > 340:
        errs.append(f"answer is {len(text)} characters (max ~300)")
    if "{buy:" in pg.get("answer", ""):
        errs.append("buy token in the answer line")
    if BANNED.search(json.dumps(pg, ensure_ascii=False)):
        errs.append("banned wording: " + BANNED.search(json.dumps(pg, ensure_ascii=False)).group(0))
    for r in pg.get("rows") or []:
        for k, _ in pg.get("columns") or []:
            if not str((r.get("cells") or {}).get(k, "")).strip():
                errs.append(f"empty cell {k} in {r.get('slug') or r.get('model')}")
    if new_page and not any(r.get("slug") for r in pg.get("rows") or []):
        errs.append("NO_LISTED_PRODUCT: no row is a product we list, so the page has no buy link (recipe: skip)")
    if not new_page:
        ex = _existing(draft["slug"])
        if pg.get("title") != ex["title"] or pg.get("h1") != ex["h1"]:
            errs.append("title or h1 changed (fixed in the A/B test)")
    return errs


def pick_check(draft: dict) -> list[str]:
    """The answer's recommended product must be the table's first row, and the line under the H1 must not contradict
    the answer (11-08: a verifier dropped the pick's row and the page said 'Pick: Denon' under an answer for Yamaha)."""
    import products as P
    pg = draft.get("page") or {}
    names = []
    for r in (pg.get("rows") or [])[:4]:
        if r.get("slug"):
            p = next((p for p in P.PRODUCTS + (draft.get("products") or []) if p["slug"] == r["slug"]), {})
            names.append(f'{p.get("brand", "")} {r.get("model") or p.get("model") or p.get("name") or r["slug"]}')
        else:
            names.append(f'{r.get("brand", "")} {r.get("model", "")}')
    prompt = ("A buying page opens with this answer paragraph:\n" + re.sub(r"<[^>]+>", "", pg.get("answer", "")) +
              "\n\nIts comparison table's rows, in order:\n" + "\n".join(f"{i + 1}. {n}" for i, n in enumerate(names)) +
              '\n\nWhich product does the answer recommend overall? Is it row 1? Reply with ONE JSON object: '
              '{"pick": "<product the answer recommends>", "is_row_1": true|false}')
    r = claude(prompt, tools=False, timeout=600)
    if r.get("status") == "error" or "is_row_1" not in r:
        return []   # the check couldn't run; don't block on it
    return [] if r["is_row_1"] else [f"the answer recommends {r.get('pick')!r} but the table's first row is {names[0] if names else '-'!r}: "
                                     "the pick must be the first row (add its row, sourced, if it is missing)"]


def record_text(draft: dict, old: dict | None, gnum: int | None) -> str:
    pg = draft["page"]
    rec = {"slug": draft["slug"],
           "question": old["question"] if old else f"G{gnum} (gap mining daily {today()}, research method {METHOD}: {draft.get('query')})",
           "method": METHOD, "angle": draft.get("angle"), "searched_as": draft.get("searched_as") or [],
           "title": pg["title"], "h1": pg["h1"], "desc": pg["desc"], "answer": pg["answer"].strip(),
           "columns": [tuple(c) for c in pg["columns"]], "rows": pg["rows"], "after": "\n" + pg["after"].strip() + "\n",
           "sources": [tuple(s) for s in pg["sources"]],
           "published": old["published"] if old else today(), "checked": today(), "updated": today()}
    for k in ("video",):
        if old and k in old:
            rec[k] = old[k]
    body = ",\n ".join(f'"{k}": {v!r}' for k, v in rec.items())
    tag = f"G{gnum}: " if gnum else ""
    return f"# ---------------- {tag}{draft['slug']} (research method {METHOD}, {today()}) ----------------\n{{{body}}},\n"


def replace_record(slug: str, text: str) -> None:
    """Swap the existing gaps.py record for slug (found by parsing, not by text search) for `text`."""
    gp = ROOT / "src/gaps.py"
    src = gp.read_text()
    tree = ast.parse(src)
    for node in ast.walk(tree):
        if isinstance(node, ast.Dict):
            keys = [k.value for k in node.keys if isinstance(k, ast.Constant)]
            if "slug" in keys and "h1" in keys:
                v = node.values[keys.index("slug")]
                if isinstance(v, ast.Constant) and v.value == slug:
                    lines = src.splitlines(keepends=True)
                    start, end = node.lineno - 1, node.end_lineno   # end line holds "}," for our records
                    tail = lines[end - 1][node.end_col_offset:]
                    lines[start:end] = [lines[start][:node.col_offset] + text.rstrip().rstrip(",") + tail]
                    gp.write_text("".join(lines))
                    return
    raise KeyError(slug)


def pack_from_harvest(slug: str) -> str:
    """A fastloop result set from ChatGPT's own results for the page's query (titles only; the check needs rank shares)."""
    h = jload(pdir(slug) / "harvest.json")
    ch = h["chats"][-1]
    name = f"ab-{slug}"[:60]
    d = ROOT / "growth/evals/runs/fastloop" / name
    d.mkdir(parents=True, exist_ok=True)
    res = [{"url": r["url"], "title": r["title"] or "", "snippet": "", "text": r["title"] or "", "source": "chatgpt-app"}
           for r in ch["results"][:12] if not r["ours"]]
    jsave(d / "pack.json", {"question": ch["typed"], "query": (ch["queries"] or [""])[0], "from": "harvest", "results": res})
    return name


def apply(slug: str, local: bool) -> dict:
    import gappage
    d = pdir(slug)
    draft = jload(d / "draft.json")
    if not draft:
        return {"slug": slug, "status": "no draft"}
    new_page = bool(draft.get("new_page"))
    dirty = [l for l in sh("git", "status", "--porcelain", "src", "docs").stdout.splitlines()
             if not l.endswith(("docs/offers.json", "docs/price-history.json"))]   # rewritten with today's date on every build
    if dirty:
        return {"slug": slug, "status": "skipped", "reason": "src/ or docs/ has uncommitted changes"}
    h = jload(d / "harvest.json")
    if h and h.get("searched_as"):
        draft["searched_as"] = h["searched_as"]   # the latest harvest's search words (fresh chats after the research ran)
    for r in (draft.get("page") or {}).get("rows") or []:   # "Sony" + "Sony XAV-AX6000" rendered "Sony Sony ..."
        if r.get("brand") and str(r.get("model", "")).lower().startswith(r["brand"].lower() + " "):
            r["model"] = r["model"][len(r["brand"]) + 1:]
    errs = validate(draft, new_page)
    if any(e.startswith("NO_LISTED_PRODUCT") for e in errs):
        draft["gate"] = {"date": today(), "pass": False, "skipped": True, "errors": errs}
        jsave(d / "draft.json", draft)
        return {"slug": draft.get("slug"), "status": "skipped: no product we list"}
    errs += pick_check(draft)
    if errs and not draft.get("fix_pass"):   # one sourced fix pass, then re-check
        fx = claude(fix_prompt(draft, errs))
        if fx.get("draft"):
            keep = {k: draft[k] for k in ("new_page", "searched_as", "angle", "why_angle", "query", "slug") if k in draft}
            draft = {**fx["draft"], **keep, "status": "ok", "fix_pass": {"errors": errs, "log": fx.get("log")}}
            jsave(d / "draft.json", draft)
            errs = validate(draft, new_page) + pick_check(draft)
    if errs:
        draft["gate"] = {"date": today(), "pass": False, "errors": errs}
        jsave(d / "draft.json", draft)
        return {"slug": draft["slug"], "status": "failed", "errors": errs}
    before = set((ROOT / "src/img").glob("*.png")) | set((ROOT / "docs").rglob("*")) | set((ROOT / "src/dist").rglob("*"))
    # products first (gappage.insert writes products and, for a page, a v1 record we don't want: insert products only)
    gappage.insert({**draft, "status": "products_only"}, {})
    old = _existing(slug) if not new_page else None
    gnum = None if old else gappage.next_gnum()
    text = record_text(draft, old, gnum)
    if old:
        replace_record(slug, text)
    else:
        gp = ROOT / "src/gaps.py"
        g = gp.read_text()
        j = g.rstrip().rfind("]")
        gp.write_text(g[:j] + text + "\n" + g[j:])
    if draft.get("products"):
        sh("python3.12", "tools/images.py", *[p["slug"] for p in draft["products"]])
    errs = []
    r = sh("python3.12", "src/build.py")
    if r.returncode:
        errs.append("build: " + (r.stderr or r.stdout)[-400:])
    r = sh("python3.12", "tools/docsguard.py")
    if r.returncode:
        errs.append("docsguard: " + r.stdout[-200:])
    if not errs:
        cmd = ["python3.12", "growth/evals/fastloop.py", "check", f"docs/{draft['slug']}.html", "--packs", pack_from_harvest(slug), "--ranks", "1,3,6", "--research"]
        for m in draft["must"]:
            cmd += ["--must", m]
        r = sh(*cmd)
        if "PASS" not in r.stdout:
            errs.append("fastloop check: " + r.stdout[-500:])
    new_files = sorted((set((ROOT / "src/img").glob("*.png")) | set((ROOT / "docs").rglob("*")) | set((ROOT / "src/dist").rglob("*"))) - before)
    if errs:
        gappage.restore(new_files)
        draft["gate"] = {"date": today(), "pass": False, "errors": errs}
        jsave(d / "draft.json", draft)
        return {"slug": draft["slug"], "status": "failed", "errors": errs}
    draft["gate"] = {"date": today(), "pass": True, "g": gnum}
    jsave(d / "draft.json", draft)
    if local:
        sh("git", "add", "src/gaps.py", "src/products.py", "src/img", "docs", "worker/src/links-map.json", str(d),
           f"growth/evals/runs/fastloop/ab-{slug}"[:200])
        what = f"Gap page G{gnum} /{draft['slug']} (new, research method)" if gnum else f"A/B group A rebuild /{slug}"
        msg = (f"{what}: angle {draft.get('angle')}, {draft.get('why_angle') or ''}"[:250] +
               f"\n\nResearched by tools/abpage.py (six angle agents, compose, verify; DLC-208). Research in growth/focus/ab/{slug}/.\n\n"
               "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n")
        r = sh("git", "commit", "-q", "-m", msg)
        return {"slug": draft["slug"], "status": "committed" if r.returncode == 0 else "commit failed: " + (r.stderr or r.stdout)[-200:]}
    return {"slug": draft["slug"], "status": "passed (not committed)"}


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["harvest", "research", "apply", "status"])
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--runs", nargs="*", default=DEFAULT_RUNS)
    ap.add_argument("--new", action="store_true", help="research: these are new pages (slug, title and h1 are the agent's)")
    ap.add_argument("--force", action="store_true")
    ap.add_argument("--workers", type=int, default=2, help="pages researched at once (each runs six agents)")
    ap.add_argument("--local", action="store_true", help="apply: commit each passing page locally")
    a = ap.parse_args()
    if a.cmd == "status":
        for d in sorted(AB.glob("*/")):
            dr = jload(d / "draft.json", {})
            n = len(list(d.glob("angle-*.json")))
            print(f"{d.name:70} harvest {'y' if (d / 'harvest.json').exists() else '-'} angles {n} draft {'y' if dr else '-'} "
                  f"angle {dr.get('angle', '-')} gate {(dr.get('gate') or {}).get('pass', '-')}")
        return 0
    if a.cmd == "harvest":
        for s in a.slugs:
            h = harvest(s, a.runs)
            print(f"{s}: {len(h['chats'])} chats, tags {h['searched_as'][:3]}, carousel {h['carousel'][:4]}")
        return 0
    if a.cmd == "research":
        with cf.ThreadPoolExecutor(max_workers=a.workers) as ex:
            for r in ex.map(lambda s: research(s, a.new, a.force), a.slugs):
                print(json.dumps(r, ensure_ascii=False), flush=True)
        return 0
    if a.cmd == "apply":
        for s in a.slugs:
            print(json.dumps(apply(s, a.local), ensure_ascii=False)[:800], flush=True)
        return 0
    return 0


if __name__ == "__main__":
    sys.exit(main())
