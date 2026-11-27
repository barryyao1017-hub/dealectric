"""Page index (growth/stock/README.md): every page and source line that mentions each product, rebuilt on every build.

The weekly upkeep (tools/upkeep) reads it to find where a product whose stock, ship date or price changed is written
about, so it can reread those pages whole and correct everything that depends on the product. Generated pages (product
pages, brand code pages, kit pages) follow the records by themselves; hand-written sources (src/gaps.py,
src/compare.py, src/focus.py, the record's own prose in src/products.py) are what a page rewrite has to touch.

Written to growth/stock/page-index.json:
    {"built": <date>, "products": {slug: [{"page": "/<path>", "source": "src/gaps.py", "lines": [a, b],
                                           "how": ["row", "buy", "name", ...]}, ...]},
     "unlisted": [{"page", "source", "lines", "brand", "model"}]}   # rows naming a brand we have a program with, no record
"""
from __future__ import annotations

import datetime
import json
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "growth", "stock", "page-index.json")
SLUG_KEY = re.compile(r"""["']slug["']\s*:\s*["']([a-z0-9-]+)["']""")


def _entry_lines(path: str) -> dict[str, list[int]]:
    """{entry slug: [first line, last line]} for a source file whose entries start with a "slug" key."""
    lines = open(os.path.join(ROOT, path), encoding="utf-8").read().split("\n")
    starts = []
    for i, l in enumerate(lines, 1):
        if l.startswith(("{\"slug\"", "{'slug'")):   # an entry opens at column 0 in all three files
            starts.append((i, SLUG_KEY.search(l).group(1)))
    out = {}
    for k, (i, s) in enumerate(starts):
        out.setdefault(s, [i, (starts[k + 1][0] - 1) if k + 1 < len(starts) else len(lines)])
    return out


def _name_pattern(p: dict) -> re.Pattern | None:
    m = (p.get("model") or "").strip()
    if len(m) < 3:
        return None
    return re.compile(r"(?<![A-Za-z0-9])" + re.escape(m).replace(r"\ ", r"[\s-]?") + r"(?![A-Za-z0-9])", re.I)


def build(products, gap_pages, comparisons, kits, buybox, compare_path, program_brands) -> dict:
    by = {p["slug"]: p for p in products}
    idx: dict[str, list[dict]] = {p["slug"]: [] for p in products}
    names = [(p["slug"], _name_pattern(p)) for p in products]
    names = [(s, pat) for s, pat in names if pat]
    unlisted = []

    def add(slug, page, source, lines, how):
        if slug not in idx:
            return
        for e in idx[slug]:
            if e["page"] == page and e["source"] == source:
                e["how"] = sorted(set(e["how"]) | set(how))
                return
        idx[slug].append({"page": page, "source": source, "lines": lines, "how": sorted(set(how))})

    for source, entries in (("src/gaps.py", gap_pages), ("src/compare.py", comparisons)):
        spans = _entry_lines(source)
        for c in entries:
            page, lines = "/" + c["slug"], spans.get(c["slug"])   # published extensionless at the root
            text = json.dumps(c, ensure_ascii=False)
            for r in c.get("rows") or []:
                if r.get("slug"):
                    add(r["slug"], page, source, lines, ["row"])
                elif r.get("kit"):
                    for it in (next((k for k in kits if k["slug"] == r["kit"]), {}) or {}).get("items", []):
                        add(it["slug"], page, source, lines, ["kit row"])
                elif r.get("brand") in program_brands and not r.get("asin"):
                    unlisted.append({"page": page, "source": source, "lines": lines, "brand": r["brand"], "model": r.get("model")})
            for s in re.findall(r"\{(?:buy|price|after|deal):([a-z0-9-]+)\}", text):
                add(s, page, source, lines, ["buy"])
            for s in re.findall(r"/(?:go|products)/([a-z0-9-]+)", text):
                add(s, page, source, lines, ["link"])
            for s, pat in names:
                if by[s]["brand"].lower() in text.lower() and pat.search(text):
                    add(s, page, source, lines, ["name"])
    pspans = _entry_lines("src/products.py")
    for p in products:
        add(p["slug"], f"/{p['slug']}", "src/products.py", pspans.get(p["slug"]), ["record"])
    for s in buybox or {}:
        add(s, f"/{s}", "src/focus.py", None, ["buybox"])
    return {"built": datetime.date.today().isoformat(), "products": idx, "unlisted": unlisted}


def write(index: dict) -> None:
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(index, f, ensure_ascii=False, indent=0, sort_keys=True)
        f.write("\n")
