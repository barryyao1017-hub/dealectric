#!/usr/bin/env python3.12
"""Print a research draft for review before apply: python3.12 growth/focus/monitors/draft_read.py <folder>..."""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
for f in sys.argv[1:]:
    d = json.loads((ROOT / f"growth/focus/ab/{f}/draft.json").read_text())
    pg = d.get("page") or {}
    print("=====", f, "->", d.get("slug"), "| angle", d.get("angle"), "| status", d.get("status"), d.get("reason") or "")
    if not pg:
        continue
    print("WHY:", d.get("why_angle"))
    print("TITLE:", pg["title"]); print("H1:", pg["h1"]); print("DESC:", pg["desc"])
    print("ANSWER:", re.sub(r"<[^>]+>", "", pg["answer"]))
    print("MUST:", d.get("must"))
    print("COLS:", pg["columns"])
    for r in pg["rows"]:
        print(" ROW:", json.dumps(r, ensure_ascii=False)[:900])
    print("NEW PRODUCTS:", [(p["slug"], p.get("program"), p.get("price"), p.get("url")) for p in d.get("products") or []])
    print("AFTER:", pg["after"])
    print("SOURCES:")
    for s in pg["sources"]:
        print("  ", s)
