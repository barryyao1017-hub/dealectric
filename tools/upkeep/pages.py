"""Step 4 of the weekly upkeep: correct every page that mentions a product whose stock, ship date, price or alternative
changed this run (Barry, 11-27: reread the entire page and change everything about that product that depends on its
stock, price or ship status, not just the sentence that states them).

For each hand-written page source the page index (growth/stock/page-index.json) lists for a changed product (a
comparison entry in src/gaps.py or src/compare.py, a buy box in src/focus.py, the product's own record prose in
src/products.py), one `claude -p` call (llm.DEEP) gets the page's whole source entry, the page as published, and the
week's changes for the products on it, and returns exact text replacements. Each replacement must match exactly once
inside that entry; the file must still parse afterwards, or the page's edits are dropped and it is listed for a hand
pass. Picks, row order and the page's structure stay as they are.
"""
from __future__ import annotations

import ast
import datetime as dt
import html
import json
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import llm

ROOT = Path(__file__).resolve().parents[2]
SLUG_KEY = re.compile(r"""^\{["']slug["']\s*:\s*["']([a-z0-9-]+)["']""")

SCHEMA = {"type": "object", "properties": {"edits": {"type": "array", "items": {"type": "object", "properties": {
    "old": {"type": "string"}, "new": {"type": "string"}, "why": {"type": "string"}}, "required": ["old", "new"]}},
    "notes": {"type": "string"}}, "required": ["edits"]}

PROMPT = """You maintain one page of Dealectric, a shopping site whose pages are read by shoppers and by AI assistants.
Today is {today}. This week's store reads changed facts about products on this page:

{changes}

Below is the page's SOURCE (a Python dict literal from {source}; strings may hold HTML and placeholders such as
{{buy:slug}} that the build fills from the product records with today's price, code and stock) and the page as it was
last published.

Read the ENTIRE page and correct everything about the changed products that depends on their stock, ship date or
price: stated prices and the date they were read, stock and ship-date statements, "ships now" / "can wait" framing,
advice or comparisons that relied on the old status or price, and numbers computed from the price (price per Wh,
savings, totals). Rules:
- Keep which product the page picks, the table rows and their order, and the page structure. Change only what the new
  facts make wrong or stale.
- Write for the shopper, in the third person; never address an AI assistant.
- State dates as the page already does (e.g. "(read {today})" or "on {today}"). Don't touch other products' facts.
- Placeholders ({{buy:...}}, {{price:...}}) already update themselves: leave them as they are.
- Keep the source valid Python: the text you return goes inside the same string literal, so match its quoting and
  escaping exactly as it appears in the source.
- If nothing on the page depends on the changes, return no edits.

Return JSON: {{"edits": [{{"old": "<exact text copied from the SOURCE, unique within it>", "new": "<replacement>",
"why": "<short>"}}], "notes": "<anything you were unsure about>"}}.

SOURCE ({source}, entry "{entry}"):
{src}

PUBLISHED PAGE TEXT:
{page}"""


def _entry_span(lines: list[str], entry: str) -> tuple[int, int] | None:
    starts = [(i, m.group(1)) for i, l in enumerate(lines) if (m := SLUG_KEY.match(l))]
    for k, (i, s) in enumerate(starts):
        if s == entry:
            end = starts[k + 1][0] if k + 1 < len(starts) else len(lines)
            return i, end
    return None


def page_text(page: str) -> str:
    f = ROOT / "docs" / (page.strip("/") + ".html")
    if not f.exists():
        return "(not published yet)"
    t = re.sub(r"(?s)<(script|style|head)\b.*?</\1>", "", f.read_text(errors="ignore"))
    t = re.sub(r"</(p|li|tr|h[1-6]|div)>|<br ?/?>", "\n", t)
    t = re.sub(r"</t[dh]>", " | ", t)
    return re.sub(r"[ \t]+", " ", html.unescape(re.sub(r"<[^>]+>", "", t))).strip()[:30000]


def targets(changed: dict, index: dict) -> dict:
    """{(source, entry, page): [slug, ...]} for every hand-written source that mentions a changed product."""
    out: dict = {}
    for slug in changed:
        for e in index["products"].get(slug, []):
            if e["source"] not in ("src/gaps.py", "src/compare.py", "src/products.py", "src/focus.py"):
                continue
            entry = e["page"].strip("/").split("/")[-1] if e["source"] != "src/focus.py" else slug
            out.setdefault((e["source"], entry, e["page"]), []).append(slug)
    return out


def describe(slug: str, items: list[str]) -> str:
    return f"- {slug}: " + "; ".join(items)


def _ask(key, slugs, changed, today) -> tuple:
    source, entry, page = key
    lines = (ROOT / source).read_text().split("\n")
    if source == "src/focus.py":
        src = "\n".join(l for l in lines if entry in l)[:20000] or "(no buy box text for this product)"
    else:
        sp = _entry_span(lines, entry)
        if not sp:
            return key, {"status": "error", "reason": f"entry {entry} not found in {source}"}
        src = "\n".join(lines[sp[0]:sp[1]])
    ch = "\n".join(describe(s, changed[s]) for s in sorted(set(slugs)))
    res = llm.ask(PROMPT.format(today=today, changes=ch, source=source, entry=entry, src=src[:60000], page=page_text(page)),
                  models=llm.DEEP, schema=SCHEMA)
    return key, res


def run(changed: dict, index: dict, workers: int = 3) -> dict:
    """changed: {slug: ["stock: in stock → sold out", "price: 549 → 499", "alternative line added: ...", ...]}."""
    today = dt.date.today().isoformat()
    tg = targets(changed, index)
    report = {"pages": [], "failed": []}
    with ThreadPoolExecutor(max_workers=workers) as ex:
        results = list(ex.map(lambda kv: _ask(kv[0], kv[1], changed, today), tg.items()))
    for (source, entry, page), res in results:
        if res.get("status") == "error":
            report["failed"].append({"page": page, "source": source, "why": res.get("reason", "")[:200]})
            continue
        edits = res.get("edits") or []
        if not edits:
            continue
        f = ROOT / source
        txt = f.read_text()
        lines = txt.split("\n")
        if source == "src/focus.py":
            a, b = 0, len(txt)
        else:
            sp = _entry_span(lines, entry)
            a = len("\n".join(lines[:sp[0]])) + (1 if sp[0] else 0)
            b = len("\n".join(lines[:sp[1]]))
        seg, bad = txt[a:b], []
        for e in edits:
            if seg.count(e["old"]) != 1:
                bad.append(e["old"][:80])
                continue
            seg = seg.replace(e["old"], e["new"], 1)
        new = txt[:a] + seg + txt[b:]
        try:
            ast.parse(new)
        except SyntaxError as err:
            report["failed"].append({"page": page, "source": source, "why": f"edits broke the file ({err.msg}); dropped"})
            continue
        f.write_text(new)
        report["pages"].append({"page": page, "source": source, "edits": len(edits) - len(bad), "skipped": bad,
                                "notes": res.get("notes", ""), "log": [{"old": e["old"][:300], "new": e["new"][:300], "why": e.get("why", "")} for e in edits if e["old"][:80] not in bad]})
    return report
