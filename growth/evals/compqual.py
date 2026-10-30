#!/usr/bin/env python3.12
"""Why did the solar page win? Competitor quality vs ours, on the result sets ChatGPT actually saw (2026-10-30).

Per question: our page (the version OpenAI had stored: solar page at d1c89e4, crawled 10-29 07:12Z; focus product
pages as of 10-26 21:34Z, their last OAI-SearchBot fetch) plus the six competitor pages from growth/focus/focus-gap/
packs.json, shown to the judge blind (letters, no URL). The judge rates each page on a rubric and ranks them all for
the shopper's question. From ChatGPT's own result list: each result's title-word match with ChatGPT's search query,
and OpenAI's pub_date.

Groups: solar-hit (ChatGPT retrieved our solar page), solar-miss (it didn't; our solar page is inserted to ask "would
it have won on content?"), focus (category questions, our product page inserted).

    python3.12 growth/evals/compqual.py            # judge what's missing, print the summary
    python3.12 growth/evals/compqual.py --report
"""
import argparse
import datetime as dt
import json
import random
import re
import statistics
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import focusgap as F  # noqa: E402
import gapexp as G  # noqa: E402

OUT = F.ROOT / "growth" / "focus" / "compqual"
SOLAR = "solar-generator-with-panels-included"
CELLS = ([("solar-hit", SOLAR, f"gap-solar--{c}") for c in ("best-1", "best-2", "budget-1", "budget-2")]
         + [("solar-miss", SOLAR, c) for c in ("gap-solar--camping-1", "solar-general--outage-1", "solar-general--which-1",
                                                "solar-general--homebackup-1")]
         + [("focus", s, c) for s, c in (("allpowers-p1800-1024wh", "focus-p1800--category-1"),
                                         ("allpowers-sp037-400w-solar-panel", "focus-sp037--category-1"),
                                         ("allpowers-r4000-3456wh", "focus-r4000--category-1"),
                                         ("bluetti-ac200l", "focus-ac200l--category-1"))]
         + [(f.stem.split("--")[0], None, f) for f in F.VOID_CELLS])   # no page of ours: competitors only
STOP = set("a an and the for of to with in on best what whats what's is are which should i my me buy good under vs 2026 review reviews "
           "comparison compared price prices specs".split())

RUB_SCHEMA = {"type": "object", "properties": {"pages": {"type": "array", "items": {"type": "object", "properties": {
    "id": {"type": "string"}, "latest_date": {"type": "string"}, "models_compared": {"type": "integer"},
    "dated_prices": {"type": "boolean"}, "own_testing": {"type": "boolean"}, "codes": {"type": "boolean"},
    "templated": {"type": "boolean"}, "answers_directly": {"type": "integer"}, "usefulness": {"type": "integer"},
    "why": {"type": "string"}}, "required": ["id", "latest_date", "models_compared", "dated_prices", "own_testing", "codes",
                                             "templated", "answers_directly", "usefulness", "why"]}},
    "ranking": {"type": "array", "items": {"type": "string"}}}, "required": ["pages", "ranking"]}
RUB_SYSTEM = """Today is 2026-10-30. A shopper asked the question below. You see web pages, each under a letter, with no
site name. For each page report:
- latest_date: the most recent date the page shows for its content or prices (YYYY-MM-DD, YYYY-MM, or "none").
- models_compared: how many distinct products it recommends or compares with specs.
- dated_prices: it gives prices and says when they were checked.
- own_testing: it claims its own hands-on or in-store testing (of products, prices or codes), not just specs.
- codes: it gives discount codes.
- templated: it reads like an AI-written or templated listicle (generic praise, filler, no specific data that would
  have needed real checking).
- answers_directly: 1-5, how directly it answers this exact question.
- usefulness: 1-5, how useful it is to this shopper deciding what to buy today.
- why: one short phrase.
Then `ranking`: all page letters, most useful first, for this shopper."""


def our_text(slug: str) -> str:
    rev = "d1c89e4" if slug == SOLAR else subprocess.run(
        ["git", "rev-list", "-1", "--before=2026-10-26T21:34:00Z", "HEAD", "--", f"docs/{slug}.html"],
        cwd=F.ROOT, capture_output=True, text=True).stdout.strip()
    raw = subprocess.run(["git", "show", f"{rev}:docs/{slug}.html"], cwd=F.ROOT, capture_output=True, text=True).stdout
    raw = re.sub(r"<nav.*?</nav>|<footer.*?</footer>", "", raw, flags=re.S)
    return G.cut(G.html_text(raw))


def words(s: str) -> set[str]:
    return {w for w in re.findall(r"[a-z0-9]+", (s or "").lower()) if w not in STOP and not w.isdigit()}


def title_match(query: str, title: str) -> float:
    q = words(query)
    return round(len(q & words(title)) / len(q), 2) if q else 0.0


def judge(question: str, pages: list[tuple[str, str]]) -> dict:
    user = f"QUESTION: {question}\n\n" + "\n\n".join(f"[{pid}]\n{G.cut(t, 900)}" for pid, t in pages)
    return E.claude_cli_json(RUB_SYSTEM, user, G.JUDGE, RUB_SCHEMA, timeout=400) or {}


def run_cell(group: str, slug: str, cell: str, packs: dict) -> dict:
    d = json.loads((cell if isinstance(cell, Path) else F.GVF / f"{cell}.json").read_text())
    cell = cell.stem if isinstance(cell, Path) else cell
    query = (d.get("queries") or [d["prompt"]])[0]
    sr = (d.get("response") or {}).get("search_results") or []
    results = [{"domain": r.get("domain"), "title": r.get("title"), "ours": "dealectric.com" in (r.get("domain") or ""),
                "pub_date": dt.datetime.fromtimestamp(r["pub_date"], dt.timezone.utc).date().isoformat() if r.get("pub_date") else None,
                "title_match": title_match(query, r.get("title") or "")} for r in sr]
    p = packs[cell]
    srcs = [("comp", s["domain"], s["text"]) for s in p["sources"]] + ([("ours", "dealectric.com", our_text(slug))] if slug else [])
    random.Random(cell).shuffle(srcs)
    ids = [chr(65 + i) for i in range(len(srcs))]
    r = judge(d["prompt"], [(i, s[2]) for i, s in zip(ids, srcs)])
    by = {x["id"]: x for x in r.get("pages") or []}
    pages = [{"id": i, "who": s[0], "domain": s[1], **{k: v for k, v in by.get(i, {}).items() if k != "id"}} for i, s in zip(ids, srcs)]
    rank = r.get("ranking") or []
    ours_id = next((i for i, s in zip(ids, srcs) if s[0] == "ours"), None)
    title = next((x["title"] for x in results if x["ours"]), None)
    return {"group": group, "slug": slug, "question": d["prompt"], "query": query, "results": results, "pages": pages,
            "ranking": rank, "our_judged_rank": rank.index(ours_id) + 1 if ours_id in rank else None, "of": len(srcs),
            "our_chatgpt_rank": next((i for i, x in enumerate(results, 1) if x["ours"]), None),
            "our_title_match": None if not slug else title_match(query, title) if title else title_match(query, (
                "Best solar generator with panels included (2026): 15 kits compared on battery, inverter, solar input and price"
                if slug == SOLAR else slug.replace("-", " ")))}


def summary(res: dict) -> None:
    for group in dict.fromkeys(v["group"] for v in res.values()):
        rows = [v for v in res.values() if v["group"] == group]
        if not rows:
            continue
        ours = [p for v in rows for p in v["pages"] if p["who"] == "ours"]
        comp = [p for v in rows for p in v["pages"] if p["who"] == "comp"]
        def m(ps, k):
            vals = [p.get(k) for p in ps if isinstance(p.get(k), (int, float)) and not isinstance(p.get(k), bool)]
            return f"{statistics.mean(vals):.1f}" if vals else "-"
        def share(ps, k):
            return f"{sum(1 for p in ps if p.get(k))}/{len(ps)}"
        comp_tm = [x["title_match"] for v in rows for x in v["results"] if not x["ours"]]
        print(f"\n## {group} ({len(rows)} questions)")
        print(f"- judged rank of our page among {rows[0]['of']}: {[v['our_judged_rank'] for v in rows]}; ChatGPT's rank: "
              f"{[v['our_chatgpt_rank'] for v in rows]}")
        print(f"- usefulness 1-5: ours {m(ours, 'usefulness')}, competitors {m(comp, 'usefulness')}; answers directly: ours "
              f"{m(ours, 'answers_directly')}, competitors {m(comp, 'answers_directly')}")
        print(f"- models compared: ours {m(ours, 'models_compared')}, competitors {m(comp, 'models_compared')}; dated prices: ours "
              f"{share(ours, 'dated_prices')}, competitors {share(comp, 'dated_prices')}; codes: ours {share(ours, 'codes')}, "
              f"competitors {share(comp, 'codes')}; own testing: ours {share(ours, 'own_testing')}, competitors "
              f"{share(comp, 'own_testing')}; templated: competitors {share(comp, 'templated')}")
        print(f"- title-word match with ChatGPT's query: ours {[v['our_title_match'] for v in rows]}, competitors' mean "
              f"{statistics.mean(comp_tm):.2f}" if comp_tm else "")
        dates = [x["pub_date"] for v in rows for x in v["results"] if not x["ours"] and x["pub_date"]]
        print(f"- competitors' OpenAI pub_date: {sum(1 for x in dates if x >= '2026-10-01')} of {len(dates)} dated in October")
        for v in rows:
            print(f"  - {v['question']} | query: {v['query']}")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    rf = OUT / "results.json"
    res = json.loads(rf.read_text()) if rf.exists() else {}
    packs = json.loads((F.OUT / "packs.json").read_text())
    if not args.report:
        for group, slug, cell in CELLS:
            k = cell.stem if isinstance(cell, Path) else cell
            if k in res or k not in packs:
                continue
            res[k] = run_cell(group, slug, cell, packs)
            rf.write_text(json.dumps(res, indent=1))
            print(f"{k}: our judged rank {res[k]['our_judged_rank']} of {res[k]['of']}", flush=True)
    summary(res)


if __name__ == "__main__":
    main()
