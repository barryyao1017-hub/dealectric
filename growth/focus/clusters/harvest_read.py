#!/usr/bin/env python3.12
"""Read of the 2026-11-21 cluster harvest: per question, what ChatGPT searched, the results it got (which were cited),
the catalog cards it showed, and whether a product of a partner brand or a Dealectric page was in it.

    python3.12 growth/focus/clusters/harvest_read.py [k1121|d1121|x1121] [--full] [--json out.json]
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "growth/focus/clusters"))
import clusterpages as M  # noqa: E402

A = M.A
BIG = re.compile(r"rtings|wirecutter|nytimes|tomsguide|tomshardware|pcmag|pcgamer|wired\.|theverge|techradar|cnet|"
                 r"zdnet|macworld|pcworld|consumerreports|engadget|digitaltrends|popularmechanics|caranddriver|"
                 r"motortrend|ign\.com|gamesradar|howtogeek|xda-developers|androidauthority|bestbuy|amazon\.|reddit", re.I)


def main() -> int:
    args = [a for a in sys.argv[1:] if a in M.CLUSTERS]
    full = "--full" in sys.argv
    out = []
    for q in M._all_questions():
        folder = q["slug"]
        if args and M.cluster_of(folder) not in args:
            continue
        ours_rx = re.compile(M.CLUSTERS[M.cluster_of(folder)]["ours"], re.I)
        files = M._chat_files(folder)
        row = {"folder": folder, "ptype": q.get("ptype"), "prompt": q["prompt"], "chats": len(files), "searched": 0, "retrieved": 0,
               "cited_us": 0, "named": [], "cards": [], "cited_big": 0, "cited_other": 0, "big_results": 0, "results": 0}
        print(f"\n=== {folder} [{q.get('ptype')}]: {q['prompt']}  ({len(files)} chats)")
        doms, cited = Counter(), Counter()
        for f in files:
            ch = A._chat_facts(json.loads(Path(f).read_text()))
            ours = [(r["rank"], r["url"].split("dealectric.com/")[-1], "CITED" if r["cited"] else "") for r in ch["results"] if r["ours"]]
            named = sorted({m.group(0).lower() for m in ours_rx.finditer(ch["answer"])})
            row["searched"] += bool(ch["queries"]); row["retrieved"] += bool(ours); row["cited_us"] += any(o[2] for o in ours)
            row["named"] = sorted(set(row["named"]) | set(named)); row["cards"] = list(dict.fromkeys(row["cards"] + ch["carousel"]))[:10]
            print(f"  searched: {' | '.join(ch['queries']) or 'NO SEARCH'}")
            print(f"  results {len(ch['results'])}; ours {ours or 'not retrieved'}; cards: {', '.join(c[:40] for c in ch['carousel'][:6]) or 'none'}")
            print(f"  answer names: {named or 'none of ours'}")
            for r in ch["results"]:
                if r["ours"]:
                    continue
                doms[r["domain"]] += 1; row["results"] += 1; row["big_results"] += bool(BIG.search(r["domain"]))
                if r["cited"]:
                    cited[r["domain"]] += 1
                    row["cited_big" if BIG.search(r["domain"]) else "cited_other"] += 1
            if full:
                for r in ch["results"]:
                    print(f"    {r['rank']:>2}. {r['domain']} | {r['title'][:80]} | {r['dated'] or '-'} {'CITED' if r['cited'] else ''}")
                print("    ANSWER: " + re.sub(r"\s+", " ", ch["answer"])[:1500])
        print(f"  cited domains: {dict(cited.most_common(8))}")
        print(f"  result domains: {dict(doms.most_common(12))}")
        row["cited_domains"] = dict(cited.most_common(8)); row["result_domains"] = dict(doms.most_common(10))
        out.append(row)
    if "--json" in sys.argv:
        Path(sys.argv[sys.argv.index("--json") + 1]).write_text(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
