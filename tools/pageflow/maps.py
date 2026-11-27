#!/usr/bin/env python3.12
"""Decision map of a cluster (page flow, DLC-369): what its buyers decide on, where the real breakpoints are, and who
wins each line, with the products we link placed on it. Every page the flow builds answers one line of a map.

    python3.12 tools/pageflow/maps.py build <cluster> [--force]   # research agent -> growth/pageflow/maps/<cluster>.json
    python3.12 tools/pageflow/maps.py show <cluster>
    python3.12 tools/pageflow/maps.py prompt <cluster>            # print the prompt, run nothing

One research agent per cluster (claude -p with WebSearch / WebFetch / storecheck / amzcheck, the same runner as
tools/abpage.py). It gets the channels Barry named on 2026-11-27 as inputs: what is new (reviews, releases, discussion:
it searches for them), our own research (the earlier map and the pages' findings), the choices ChatGPT offers shoppers
(growth/pageflow/options/<cluster>.json), its own hunches (marked as such), and traffic (the ledger: which page types
and lines drew shoppers in this cluster and which never did). A refresh hands it the earlier map and asks what changed.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402
import ledger as L  # noqa: E402

REFRESH_DAYS = 14   # a map older than this is refreshed before the cluster's next proposals

SCHEMA = """{"cluster": "%(cid)s",
 "summary": "<three sentences: how this category is bought, and what changed lately>",
 "axes": [{"id": "<short key, e.g. watts>", "label": "<what it is, in shopper words>", "kind": "number" | "price" | "feature" | "fit",
           "unit": "<W, mAh, $, ...; empty for a feature>", "rank": <1 = decides most purchases>,
           "why": "<why buyers decide on it, with the reviewer or source that shows it>", "sources": ["<url>"],
           "breakpoints": [{"value": "<65>", "why": "<what changes at this value: a device limit, a standard, a rule, a price tier people search>", "source": "<url>"}]}],
 "rules": "<120-200 words for the people who will research this cluster's pages: the definitions that are easy to get wrong, the figures that decide most questions and whose statement of each counts, and the traps (maker figures that are not comparable). Plain third person.>",
 "field": [{"product": "<brand model>", "brand": "<brand>", "ours": "<our slug, or ''>",
            "link": "program" | "store-no-record" | "amazon" | "none", "url": "<maker or listing page>",
            "price": "<$X>", "price_read": "YYYY-MM-DD", "figures": {"<axis id>": "<value>"}, "tested_by": ["<reviewer: what they measured, url>"]}],
 "lines": [{"id": "<short key, e.g. 100w-under-50>", "ptype": "numbered" | "finder" | "product",
            "question": "<the shopper's words, as typed into an assistant: no brand, no model>",
            "axes": {"<axis id>": "<value>"},
            "why": "<the breakpoint and its source in one or two sentences; a page opens with this>", "sources": ["<url>"],
            "asked": "<the evidence shoppers ask this: a search suggestion, a choice ChatGPT offered, a reviewer's section, a forum thread, with its url>",
            "hunch": <true when it rests on your judgement and not on evidence that shoppers ask it>,
            "top3": [{"product": "<brand model>", "why": "<the figures that put it there>"}],
            "ours": ["<our slug, or the store URL of a partner product with no record>"], "ours_rank": <1-3, or 0 when none of ours places>,
            "covered_by": "<slug of the page of ours that already answers this line, or ''>",
            "notes": "<leads for the page's researchers: ours and the rivals with prices read today, what to check, traps>",
            "product": {"brand": "", "name": "", "url": "", "variant": "", "price": "", "program": ""}}],
 "news": [{"date": "YYYY-MM-DD", "what": "<release, review, recall, standard change>", "source": "<url>", "effect": "<the axis or line it changes>"}],
 "pages_to_fix": [{"page": "<slug>", "why": "<its number is not a real line, its pick no longer wins, or a product on it is gone>"}],
 "unsourced": ["<what you looked for and could not source>"]}"""


def _pages_text(led: dict, cid: str) -> str:
    rows = [(s, p) for s, p in led["pages"].items() if p["cluster"] == cid and p["kind"] != "product"]
    rows.sort(key=lambda x: (-x[1]["visits"], x[0]))
    return "\n".join(f"/{s} | {p['ptype']} | {p['title'][:110]} | published {p['published'] or '?'} | {p['visits']} visits, "
                     f"{p['clicks']} buy-link clicks, {p['sales']} sales" for s, p in rows) or "(none)"


def _scores_text(led: dict, cid: str) -> str:
    row = led["scores"].get(cid, {})
    site = led["scores"].get("_site", {})
    out = [f"{pt}: {c['pages']} pages, {c['visited']} visited, {c['per_page']} visits a page (site-wide for this type: "
           f"{site.get(pt, {}).get('per_page', '?')})" for pt, c in sorted(row.items(), key=lambda x: -x[1]["visits"])]
    return "\n".join(out) or "(no page of this cluster is a week old yet)"


def _options_text(cid: str) -> str:
    o = C.jload(C.OPTIONS / f"{cid}.json")
    if not o or not o.get("choices"):
        return "(not read yet)"
    return "\n".join(f"- {c['question']} -> " + " | ".join(c["options"]) + f"   (asked in {c['chats']} of {o['chats']} chats)" for c in o["choices"]) \
        + ("\nFigures it used to split its picks: " + "; ".join(o.get("split_by") or []) if o.get("split_by") else "")


def _prev_text(prev: dict | None) -> str:
    if not prev:
        return ""
    keep = {"built": prev.get("built"), "axes": [{k: a.get(k) for k in ("id", "label", "rank", "breakpoints")} for a in prev.get("axes", [])],
            "lines": [{k: l.get(k) for k in ("id", "ptype", "question", "ours_rank", "covered_by", "status")} for l in prev.get("lines", [])]}
    return ("## The earlier map (built %s). Keep what still holds, correct what changed, and add what is new since then. "
            "Keep a line's id when the line is the same.\n" % prev.get("built")) + json.dumps(keep, ensure_ascii=False)[:14000]


def prompt(cid: str) -> str:
    import abpage as A
    c = C.clusters()[cid]
    led = C.jload(C.LEDGER) or L.build()
    prev = C.jload(C.MAPS / f"{cid}.json")
    since = (prev or {}).get("built") or "the last 60 days"
    progs = C.cluster_programs(cid)
    rules = A.COMMON_RULES.replace("TOOLS", str(C.ROOT / "tools")).replace("about 25 tool calls", "about 70 tool calls")
    return "\n\n".join(x for x in [
        rules,
        f"""## Your job: the decision map for {c['name']}
Dealectric (dealectric.com) is an affiliate site whose pages are read mostly through AI assistants. It adds a page only
where the page helps a shopper decide and one of the products it links is an honest recommendation. Three page types:
- numbered: "best <product> <number>", where the number is a real breakpoint on a figure buyers decide on (a device's
  limit, a standard, a rule, a price tier people search), alone or crossed with one more figure (2000 Wh under $600);
- finder: "which <product> has <feature>", for a yes/no feature that few products have and that decides the purchase
  for the shoppers who need it;
- product: a page for one product of a brand we link that has no record yet, when it wins or places in the top three on
  at least one line, or is a new release shoppers will ask about.
The map is what those pages are drawn from. Build it in this order:
1. What buyers decide on, ranked. Read named reviewers' buying guides and tests for this category (which figures they
   rank on and where they draw lines), what completes "best {c['noun']} ..." in search suggestions, and the choices
   ChatGPT offers shoppers (below). Ours and the rivals' spec sheets come second: a figure matters when buyers choose by
   it, not because makers print it.
2. The breakpoints on each figure: the values where something real changes, each with its source.
3. What is new since {since}: releases, reviews, recalls, standard changes, price moves that change who wins a line.
   Search for them; list them under "news" with the line each changes.
4. The field: the 12-25 products that lead the lines you found, ours and rivals, with today's price and where each can
   be bought through us (an approved program, a partner store product with no record yet, amazon.com, or nowhere).
   Check the partner stores below for products we do not list yet.
5. The lines. A line is one question one page answers. For each: the top three on the line's own terms with the figures
   that put them there, and where ours place. Mark a line our existing page already answers with covered_by.
Rules for lines:
- Honest ranking first. ours_rank is 0 when no product we link is in the top three; list the line anyway when it is a
  strong line (it tells us which partner or product we lack).
- No line to fill a count: a cluster may honestly have two open lines or none. A line needs evidence shoppers ask it
  ("asked"); a line that rests on your own judgement is allowed, marked "hunch": true, and needs the same sources.
- A number that is not a breakpoint (a round figure nobody decides on) is not a line. Say so under pages_to_fix when one
  of our pages is built on one.
- Use traffic as evidence of what works here, not as the reason for a line: a page type or figure that drew shoppers in
  this cluster is worth more lines; one that never did needs a reason to try again.
- The question is in plain shopper words with its number or feature in it, no brand and no model.""",
        f"## Today\n{A.today()}",
        "## Products we link in this cluster (slug | name | program | store price | price through our link | specs)\n" + C.ours_table(cid),
        "## Partner stores to check for products with no record (approved programs)\n" + "\n".join(f"{k}: {v}" for k, v in progs.items())
        + "\namazon.com: any product, through our Associates tag (lower commission, no code; a fair second choice)",
        "## Our pages in this cluster and what shoppers did with them (visits since 2026-10-28, from assistants' links)\n" + _pages_text(led, cid),
        "## Visits per page by page type in this cluster\n" + _scores_text(led, cid),
        "## Choices ChatGPT offered shoppers on broad questions about this category\n" + _options_text(cid),
        _prev_text(prev),
        "## Output JSON\n" + SCHEMA % {"cid": cid},
    ] if x)


def build(cid: str, force: bool = False) -> dict:
    import abpage as A
    path = C.MAPS / f"{cid}.json"
    prev = C.jload(path)
    if prev and not force and C.days_between(prev["built"], C.today()) < REFRESH_DAYS:
        return prev
    out = A.claude(prompt(cid), timeout=5400)
    if out.get("status") == "error" or not out.get("lines"):
        return {"status": "error", "reason": out.get("reason") or "no lines in the reply", "raw": out.get("raw")}
    old = {l["id"]: l for l in (prev or {}).get("lines", [])}
    for l in out["lines"]:   # a line keeps what the flow did with it (queued, built, skipped) across refreshes
        for k in ("status", "page", "run", "skipped", "first_seen"):
            if k in old.get(l["id"], {}):
                l[k] = old[l["id"]][k]
        l.setdefault("first_seen", C.today())
    out["built"] = C.today()
    out["name"] = C.clusters()[cid]["name"]
    if prev:
        hist = C.MAPS / "history" / f"{cid}-{prev['built']}.json"
        if not hist.exists():
            C.jsave(hist, prev)
    C.jsave(path, out)
    return out


def show(cid: str) -> None:
    m = C.jload(C.MAPS / f"{cid}.json")
    if not m:
        print("no map yet")
        return
    print(f"{m.get('name')} (built {m['built']}): {m.get('summary', '')}\n")
    for a in sorted(m["axes"], key=lambda a: a.get("rank", 99)):
        print(f"{a.get('rank')}. {a['label']} [{a['kind']}]: " + ", ".join(str(b["value"]) for b in a.get("breakpoints", [])))
    print()
    for l in m["lines"]:
        state = l.get("status") or ("covered: /" + l["covered_by"] if l.get("covered_by") else "open")
        print(f"{l['ptype']:8s} | ours #{l.get('ours_rank', 0)} | {'hunch ' if l.get('hunch') else ''}{state:28s} | {l['question']}")
    for n in m.get("news", []):
        print(f"news {n.get('date')}: {n.get('what')} -> {n.get('effect')}")


def main() -> int:
    cmd, cid = (sys.argv + ["", ""])[1:3]
    if cid not in C.clusters():
        print("clusters:", ", ".join(C.clusters()))
        return 1
    if cmd == "prompt":
        print(prompt(cid))
    elif cmd == "build":
        m = build(cid, "--force" in sys.argv)
        if m.get("status") == "error":
            print("map failed:", m.get("reason"), (m.get("raw") or "")[:500])
            return 2
        print(f"map for {cid}: {len(m['axes'])} axes, {len(m['field'])} products, {len(m['lines'])} lines "
              f"({sum(1 for l in m['lines'] if not l.get('covered_by') and l.get('ours_rank'))} open with ours in the top three)")
    elif cmd == "show":
        show(cid)
    return 0


if __name__ == "__main__":
    sys.exit(main())
