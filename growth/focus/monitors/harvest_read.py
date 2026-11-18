#!/usr/bin/env python3.12
"""Read of the 2026-11-18 monitors harvest (DLC-290): per question, what ChatGPT searched, the results it got (which
were cited), the catalog cards it showed, and whether a Mobile Pixels or FOPO product or a Dealectric page was in it.

    python3.12 growth/focus/monitors/harvest_read.py [--full]
"""
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "growth/focus/monitors"))
import monitorpages as M  # noqa: E402

A = M.A
OURS = re.compile(r"mobile pixels|duex|trio 3|geminos|fopo", re.I)


def main() -> int:
    full = "--full" in sys.argv
    for folder, prompt in M._questions().items():
        files = M._chat_files(folder)
        print(f"\n=== {folder}: {prompt}  ({len(files)} chats)")
        doms, cited = Counter(), Counter()
        for f in files:
            ch = A._chat_facts(json.loads(Path(f).read_text()))
            ours = [(r["rank"], r["url"].split("dealectric.com/")[-1], "CITED" if r["cited"] else "") for r in ch["results"] if r["ours"]]
            named = sorted({m.group(0).lower() for m in OURS.finditer(ch["answer"])})
            print(f"  searched: {' | '.join(ch['queries'])}")
            print(f"  results {len(ch['results'])}; ours {ours or 'not retrieved'}; cards: {', '.join(ch['carousel'][:8]) or 'none'}")
            print(f"  answer names: {named or 'none of ours'}")
            for r in ch["results"]:
                doms[r["domain"]] += 1
                if r["cited"]:
                    cited[r["domain"]] += 1
            if full:
                for r in ch["results"]:
                    print(f"    {r['rank']:>2}. {r['domain']} | {r['title'][:80]} | {r['dated'] or '-'} {'CITED' if r['cited'] else ''}")
                print("    ANSWER: " + re.sub(r"\s+", " ", ch["answer"])[:1500])
        print(f"  cited domains: {dict(cited.most_common(8))}")
        print(f"  result domains: {dict(doms.most_common(12))}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
