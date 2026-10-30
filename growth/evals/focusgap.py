#!/usr/bin/env python3.12
"""Are the focus products in content gaps? (Barry, 2026-10-30, salvaging W2-W4.)

Takes the search results ChatGPT itself was shown for category questions (W1's "best" cells and the 2026-10-30
gap-vs-focus run), fetches the top six non-Dealectric pages, and labels each with gapexp.py's rule: dedicated (written
for this question) and substantive (named models with prices, specs or tests). GAP = at most 1 dedicated-and-
substantive and at most 2 substantive; SATURATED = 3 or more dedicated-and-substantive; PARTIAL in between. The solar
gap page's questions run through the same labeller as the yardstick.

    python3.12 growth/evals/focusgap.py            # fetch, label, print the table
    python3.12 growth/evals/focusgap.py --report   # table only, from growth/focus/focus-gap/labels.json
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402
import gapexp as G  # noqa: E402

ROOT = Path(__file__).resolve().parents[2]
RUNS = ROOT / "growth" / "evals" / "runs"
OUT = ROOT / "growth" / "focus" / "focus-gap"
W1, GVF = RUNS / "2026-10-28-visibility" / "chatgpt", RUNS / "2026-10-30-gap-vs-focus" / "chatgpt"

# (group, product or page, cell file)
CELLS = [
    ("focus", "bluetti-ac200l", W1 / "bluetti-ac200l--best-1.json"),
    ("focus", "bluetti-ac200l", GVF / "focus-ac200l--category-1.json"),
    ("focus", "aurzen-travelplay-autocinema-tesla-model-y", W1 / "aurzen-travelplay-autocinema-tesla-model-y--best-1.json"),
    ("focus", "aurzen-travelplay-autocinema-tesla-model-y", GVF / "gap-tesla--best-1.json"),
    ("focus", "allpowers-r4000-3456wh", W1 / "allpowers-r4000-3456wh--best-1.json"),
    ("focus", "allpowers-r4000-3456wh", GVF / "focus-r4000--category-1.json"),
    ("focus", "allpowers-sp037-400w-solar-panel", W1 / "allpowers-sp037-400w-solar-panel--best-1.json"),
    ("focus", "allpowers-sp037-400w-solar-panel", GVF / "focus-sp037--category-1.json"),
    ("focus", "allpowers-p1800-1024wh", W1 / "allpowers-p1800-1024wh--best-1.json"),
    ("focus", "allpowers-p1800-1024wh", GVF / "focus-p1800--category-1.json"),
    ("focus", "allpowers-s2000-pro-sp037-solar-kit", W1 / "allpowers-s2000-pro-sp037-solar-kit--best-1.json"),
    ("yardstick", "solar-generator-with-panels-included", GVF / "gap-solar--best-1.json"),
    ("yardstick", "solar-generator-with-panels-included", GVF / "gap-solar--budget-1.json"),
    ("yardstick", "solar-generator-with-panels-included", GVF / "gap-solar--camping-1.json"),
    ("yardstick", "best-power-banks-for-flying", GVF / "gap-flying--best-1.json"),
]


def pack(f: Path) -> dict:
    d = json.loads(f.read_text())
    results = [r for r in (d.get("response") or {}).get("search_results") or [] if "dealectric.com" not in (r.get("domain") or "")]
    sources = []
    for r in results:
        if len(sources) == G.PACK_SIZE:
            break
        t = G.fetch_text(r["url"])
        if len(t.split()) < 150:
            continue
        sources.append({"title": r.get("title") or "", "url": r["url"], "domain": r.get("domain") or E.host_of(r["url"]), "text": G.cut(t)})
    return {"question": d["prompt"], "query": (d.get("queries") or [d["prompt"]])[0], "n_results": len(results), "sources": sources}


def label(p: dict) -> dict:
    user = f"QUESTION: {p['question']}\nSEARCH QUERY: {p['query']}\n\n" + "\n\n".join(
        f"[{i}] {s['title']} | {s['url']}\n{G.cut(s['text'], 600)}" for i, s in enumerate(p["sources"], 1))
    r = E.claude_cli_json(G.GAP_SYSTEM, user, G.JUDGE, G.GAP_SCHEMA, timeout=300) or {}
    srcs = r.get("sources") or []
    good = sum(1 for s in srcs if s.get("dedicated") and s.get("substantive"))
    sub = sum(1 for s in srcs if s.get("substantive"))
    status = "GAP" if good <= 1 and sub <= 2 else "SATURATED" if good >= 3 else "PARTIAL"
    return {"status": status, "dedicated_substantive": good, "substantive": sub, "sources": srcs}


def report(labels: dict) -> None:
    print("| group | product / page | question | ChatGPT's query | status | ded+sub | sub | of |")
    print("|---|---|---|---|---|---|---|---|")
    for group, slug, f in CELLS:
        k = f.stem
        if k not in labels:
            continue
        x = labels[k]
        print(f"| {group} | {slug} | {x['question']} | {x['query']} | {x['status']} | {x['dedicated_substantive']} | {x['substantive']} | {x['n_sources']} |")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--report", action="store_true")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    lf, pf = OUT / "labels.json", OUT / "packs.json"
    labels = json.loads(lf.read_text()) if lf.exists() else {}
    packs = json.loads(pf.read_text()) if pf.exists() else {}
    if not args.report:
        for group, slug, f in CELLS:
            k = f.stem
            if k in labels:
                continue
            if k not in packs:
                packs[k] = pack(f)
                pf.write_text(json.dumps(packs, indent=1))
            p = packs[k]
            x = label(p)
            labels[k] = {"group": group, "slug": slug, "question": p["question"], "query": p["query"],
                         "n_sources": len(p["sources"]), "urls": [s["url"] for s in p["sources"]], **x}
            lf.write_text(json.dumps(labels, indent=1))
            print(f"{k}: {x['status']} ({x['dedicated_substantive']} dedicated+substantive, {x['substantive']} substantive, "
                  f"of {len(p['sources'])})", flush=True)
    report(labels)


if __name__ == "__main__":
    main()
