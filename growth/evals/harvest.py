#!/usr/bin/env python3.12
"""Query harvest analysis (Barry, 2026-10-30): how does ChatGPT handle the vague questions shoppers actually type?

Reads a visibility_scan run made from a harvest question file (growth/focus/harvest-<brand>-questions.json: level G0
bare category / G1 situation only / G2 category + one constraint; type = the product type a good answer includes; mode
natural = ChatGPT decides whether to search, forced-search = hints=search). Per answer: did it search, the search
words it used, did it ask a clarifying question instead of recommending, which brands and products it picked, whether
our brand of interest appears, and whether a Dealectric page was retrieved, cited or linked. Then patterns by level and
mode, the words ChatGPT adds to the shopper's question, and the search phrasings grouped by shared head words.

    python3.12 growth/evals/harvest.py --run 2026-10-30-harvest-allpowers --brand ALLPOWERS
"""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402

JUDGE = "claude-sonnet-5-5"
SCHEMA = {"type": "object", "properties": {
    "clarifying": {"type": "boolean"}, "recommends_products": {"type": "boolean"},
    "products": {"type": "array", "items": {"type": "object", "properties": {"brand": {"type": "string"}, "model": {"type": "string"}},
                                            "required": ["brand", "model"]}},
    "answer_shape": {"type": "string"}}, "required": ["clarifying", "recommends_products", "products", "answer_shape"]}
SYSTEM = """You read a ChatGPT answer to a shopper's question. Report:
- clarifying: the answer mainly asks the shopper questions back (budget, needs) instead of recommending, even if it
  sketches options.
- recommends_products: it names specific products (brand + model) to buy.
- products: every brand + model it recommends, in order (empty if none). Use the brand as written (EcoFlow, Anker SOLIX, ...).
- answer_shape: one of "product picks", "category advice" (types of products, no models), "clarifying questions",
  "mixed"."""
STOP = set("a an and the for of to with in on is are which should i my me what whats what's do does it that how can".split())
BRANDS = ["EcoFlow", "Anker", "Jackery", "BLUETTI", "ALLPOWERS", "Goal Zero", "Renogy", "DJI", "OUPES", "VTOMAN", "Pecron",
          "Generac", "Champion", "Westinghouse", "Honda", "Tesla", "Rockpals", "Dabbsson", "Oukitel", "Point Zero", "Ampace"]


def words(s: str) -> list[str]:
    return [w for w in re.findall(r"[a-z0-9$]+", (s or "").lower()) if w not in STOP]


def judge(text: str) -> dict:
    return E.claude_cli_json(SYSTEM, text[:12000], JUDGE, SCHEMA, timeout=300) or {}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--run", required=True)
    ap.add_argument("--brand", required=True)
    ap.add_argument("--questions", default=None)
    args = ap.parse_args()
    run = E.RUNS_DIR / args.run
    qf = Path(args.questions) if args.questions else E.EVALS_DIR.parent / "focus" / f"harvest-{args.brand.lower()}-questions.json"
    qs = {q["qid"]: q for q in json.loads(qf.read_text())["questions"]}
    out = run / "harvest.json"
    res = json.loads(out.read_text()) if out.exists() else {}
    for f in sorted((run / "chatgpt").glob("*.json")):
        cell = f.stem
        d = json.loads(f.read_text())
        if d.get("downgraded"):          # only answers from the base model count; the scan re-asks the others
            res.pop(cell, None)
            continue
        if cell in res and res[cell].get("started_at") in (None, d.get("started_at")):
            continue
        q = qs[d["qid"]]
        sr = (d.get("response") or {}).get("search_results") or []
        j = judge(d.get("text") or "")
        res[cell] = {"qid": d["qid"], "level": q["level"], "type": q["type"], "mode": q["mode"], "prompt": q["prompt"],
                     "model": d.get("answer_model") or (d.get("models") or [None])[-1], "started_at": d.get("started_at"), "searched": bool(d.get("queries") or sr), "queries": d.get("queries") or [],
                     "n_results": len(sr), "ours_retrieved": any("dealectric.com" in (r.get("domain") or "") for r in sr),
                     "ours_linked": any("dealectric.com" in (c.get("url") or "") for c in d.get("citations") or []),
                     "result_domains": [r.get("domain") for r in sr][:12],
                     "brand_in_text": args.brand.lower() in (d.get("text") or "").lower(), **j}
        out.write_text(json.dumps(res, indent=1, ensure_ascii=False))
        print(f"{cell}: searched={res[cell]['searched']} shape={j.get('answer_shape')} products={len(j.get('products') or [])}", flush=True)

    rows = list(res.values())
    print(f"\n# Harvest {args.run}: {len(rows)} answers (model: {Counter(r['model'] for r in rows)})\n")
    print("| level | mode | n | searched | asked back | product picks | avg models | " + args.brand + " named | our page retrieved |")
    print("|---|---|---|---|---|---|---|---|---|")
    for lvl in ("G0", "G1", "G2"):
        for mode in ("natural", "forced-search"):
            g = [r for r in rows if r["level"] == lvl and r["mode"] == mode]
            if not g:
                continue
            n = len(g)
            print(f"| {lvl} | {mode} | {n} | {sum(r['searched'] for r in g)}/{n} | {sum(bool(r.get('clarifying')) for r in g)}/{n} | "
                  f"{sum(bool(r.get('recommends_products')) for r in g)}/{n} | {sum(len(r.get('products') or []) for r in g)/n:.1f} | "
                  f"{sum(r['brand_in_text'] for r in g)}/{n} | {sum(r['ours_retrieved'] for r in g)}/{n} |")
    bc = Counter()
    for r in rows:
        bc.update({p["brand"].split()[0].upper() for p in r.get("products") or []})
    print(f"\nBrands picked (answers naming each): {dict(bc.most_common(15))}")
    added = Counter()
    for r in rows:
        pw = set(words(r["prompt"]))
        for qq in r["queries"]:
            added.update(set(words(qq)) - pw)
    print(f"Words ChatGPT adds to the shopper's question in its searches: {dict(added.most_common(25))}")
    groups = defaultdict(list)
    for r in rows:
        for qq in r["queries"]:
            w = words(qq)
            head = " ".join(x for x in w if x not in {"best", "2026", "review", "reviews", "comparison", "price", "prices"})[:60]
            groups[head.split(" ")[0] if head else "?"].append(qq)
    print("\nSearch phrasings by cell:")
    for r in sorted(rows, key=lambda r: r["qid"]):
        print(f"- [{r['level']} {r['mode']} {r['type']}] {r['prompt']} -> {r['queries'] or '(no search)'} | {r.get('answer_shape')} | "
              f"{', '.join(p['brand'] + ' ' + p['model'] for p in (r.get('products') or [])[:6])}")


if __name__ == "__main__":
    main()
