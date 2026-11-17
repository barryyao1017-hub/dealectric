#!/usr/bin/env python3.12
"""Freshness sweep (2026-11-17): sort the day's price reads into applied / held, and apply the applied ones.

Inputs: tools/pricecheck.py's report (our brand-store records) and tools/rivalprice.py's report (other brands' rows on
comparison pages). Amazon prices are not handled here: tools/amzprice.py writes src/amazon_prices.json with its own dates.

Rules
  our records   same price           -> src/price_reads.json (build.py dates the price to the read)
                moved <= 25%          -> products.py price + verified updated, unless a page's prose quotes the old
                                         price beside the model (then held: the table would contradict the text)
                moved > 25%, unread   -> held; the record keeps its price and its old date
  rival rows    same price           -> the price cell's date becomes the read date
                moved <= 25%          -> the cell's price and date updated, unless the row has other $ cells (per-Wh
                                         and the like, derived from the price) or the page's prose quotes the old price
                moved > 25%, unread   -> held, cell unchanged
  Pages in --skip-pages (being rewritten elsewhere) are left alone. Rival cells go to src/rival_reads.json, which
  build.py applies; src/gaps.py is never edited.

    python3.12 tools/freshapply.py --prices R --rivals R --out growth/codes/<date>-fresh.json [--skip-pages F] [--apply]
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
import gaps  # noqa: E402
from products import PRODUCTS  # noqa: E402

BY_SLUG = {p["slug"]: p for p in PRODUCTS}
MAX_MOVE = 0.25
RECVAR: dict = {}
MONEY = re.compile(r"\$\s?([\d,]+(?:\.\d\d)?)")


def money(x: float) -> str:
    return f"${x:,.2f}".replace(".00", "")


def _toks(t: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", str(t).lower()))


def pick_variant(model: str, variants: list[dict], shown: float | None):
    """The listing variant that is this model, as (variant, how) or (None, why). One variant: that one. Several: the
    variants whose titles fit the model best (model words present, extra words such as "Plus" or a bundle's panel count
    against); the one at the shown price among them if any (the price still holds), else the single best, else None."""
    if not variants:
        return None, "no variants read"
    if len(variants) == 1:
        return variants[0], "single variant"
    mt = _toks(model)
    def score(v):
        vt = _toks(v.get("title"))
        return len(mt & vt) - 0.5 * len(vt - mt)
    best = max(score(v) for v in variants)
    cands = [v for v in variants if score(v) == best]
    if shown is not None:
        same = [v for v in cands if abs(v["price"] - shown) < 0.01]
        if same:
            return same[0], "variant at the shown price"
    if len(cands) == 1 and len(mt & _toks(cands[0].get("title"))) > 0:
        return cands[0], "variant title matches the model"
    return None, f"ambiguous variant ({len(variants)} on the listing, titles don't single out the model)"


def prose(g: dict) -> str:
    return " ".join(str(g.get(k, "")) for k in ("answer", "intro", "after", "desc", "title"))


def quoted_old(old: float, words: list[str], pages: list[dict]) -> list[str]:
    """Pages whose prose has the old price within 160 characters of one of the model's words."""
    hits = []
    pat = re.escape(money(old))
    for g in pages:
        t = prose(g)
        for m in re.finditer(pat + r"(?![\d,])", t):
            near = t[max(0, m.start() - 160): m.end() + 160].lower()
            if any(w.lower() in near for w in words if len(w) >= 3):
                hits.append(g["slug"])
                break
    return hits


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--prices", required=True)
    ap.add_argument("--rivals", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--skip-pages", default=None)
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--record-variants", default=None, help="tools/rivalprice.py --records report for the moved records")
    a = ap.parse_args()
    skip = set(json.load(open(a.skip_pages))) if a.skip_pages else set()
    pages = [g for g in gaps.GAP_PAGES if g["slug"] not in skip]
    pr = json.load(open(a.prices))
    day = pr["date"]
    out = {"date": day, "ours": {"same": [], "applied": [], "held": [], "unread": []},
           "rivals": {"same": [], "applied": [], "held": [], "unread": []}}

    recvar = {r["slug"]: r for r in json.load(open(a.record_variants))["rows"]} if a.record_variants else {}
    RECVAR.update(recvar)
    reads = {}
    for r in pr["rows"]:
        p = BY_SLUG.get(r["slug"])
        if "skip" in r or p is None:
            continue
        if "live_price" not in r:
            out["ours"]["unread"].append({"slug": r["slug"], "why": r.get("error")})
            continue
        old, new = p.get("price"), r["live_price"]
        named = "variant=" in p.get("url", "") or p.get("cart_variant")
        if old is not None and abs(new - float(old)) >= 0.01 and not named:
            rv_ = recvar.get(r["slug"])
            if rv_ is None:
                out["ours"]["held"].append({"slug": r["slug"], "old": old, "first_variant_price": new,
                                            "why": "price moved and the listing's variants were not re-read"})
                continue
            v, how = pick_variant(p["name"], rv_.get("variants", []), float(old))
            if v is None:
                out["ours"]["held"].append({"slug": r["slug"], "old": old, "first_variant_price": new, "why": how})
                continue
            new = v["price"]
            r["live_available"] = v.get("available")
        reads[r["slug"]] = new
        if old is None or abs(new - float(old)) < 0.01:
            out["ours"]["same"].append(r["slug"])
            continue
        item = {"slug": r["slug"], "old": old, "new": new, "compare_at": r.get("live_compare"),
                "available": r.get("live_available"), "move": round((new - old) / old, 3)}
        why = None
        if p.get("verified") == day:
            why = f"the record was already updated today by another read (it says {old}); not overwritten"
        elif abs(new - old) / old > MAX_MOVE:
            why = f"moved {item['move']:+.0%}"
        else:
            words = [p.get("model", "")] + p.get("model", "").split()
            hits = quoted_old(float(old), words, pages)
            if hits:
                why = "old price quoted in the prose of " + ", ".join(hits)
        (out["ours"]["held"] if why else out["ours"]["applied"]).append({**item, **({"why": why} if why else {})})

    rv = json.load(open(a.rivals))
    by_page = {g["slug"]: g for g in gaps.GAP_PAGES}
    for r in rv["rows"]:
        if r["page"] in skip:
            continue
        key = {"page": r["page"], "row": r["row"], "model": r.get("model")}
        if "live_price" not in r or r.get("shown_price") is None:
            out["rivals"]["unread"].append({**key, "why": r.get("error") or "no price shown in the row"})
            continue
        old, new = r["shown_price"], r["live_price"]
        g = by_page[r["page"]]
        row = g["rows"][r["row"]]
        if r.get("variants") and not r.get("variant_named"):
            v, how = pick_variant(f'{row.get("brand", "")} {row.get("model", "")}', r["variants"], old)
            if v is None:
                out["rivals"]["held"].append({**key, "old": old, "why": how, "first_variant_price": new})
                continue
            new = r["live_price"] = v["price"]
            r["variant_title"], r["live_available"] = v.get("title"), v.get("available")
        if abs(new - old) < 0.01:
            out["rivals"]["same"].append(key)
            continue
        item = {**key, "old": old, "new": new, "move": round((new - old) / old, 3), "cell": r.get("price_cell")}
        why = None
        if r.get("live_available") is False:
            why = "sold out on the maker's store at the new price"
        elif abs(new - old) / old > MAX_MOVE:
            why = f"moved {item['move']:+.0%}"
        elif any(k != "price" and "$" in str(v) for k, v in row.get("cells", {}).items()):
            why = "other $ cells in the row are worked out from the price"
        elif quoted_old(old, [row.get("model", "")] + str(row.get("model", "")).split(), [g]):
            why = "old price quoted in the page's prose"
        (out["rivals"]["held"] if why else out["rivals"]["applied"]).append({**item, **({"why": why} if why else {})})

    for side in ("ours", "rivals"):
        out[side + "_counts"] = {k: len(v) for k, v in out[side].items()}
    Path(a.out).write_text(json.dumps(out, indent=1))
    print(json.dumps({"ours": out["ours_counts"], "rivals": out["rivals_counts"]}))

    if a.apply:
        apply(out, reads, day, rv, skip)
    return 0


def apply(out: dict, reads: dict, day: str, rv: dict, skip: set) -> None:
    src = ROOT / "src"
    # 1. our records: price + verified for the applied moves (text edit inside the record's own block)
    pp = src / "products.py"
    s = pp.read_text()
    for it in out["ours"]["applied"]:
        m0 = re.search(r'\{"slug": ["\']' + re.escape(it["slug"]) + r'["\']', s)
        assert m0, it["slug"]
        i = m0.start()
        m1 = re.compile(r'\{"slug": ["\']').search(s, i + 10)
        j = m1.start() if m1 else len(s)
        block = s[i:j]
        new_price = repr(int(it["new"])) if float(it["new"]).is_integer() else repr(it["new"])
        b2, n = re.subn(r'"price": [\d.]+(?=[,\s}])', f'"price": {new_price}', block, count=1)
        assert n == 1, it["slug"]
        if re.search(r'"verified": ["\']\d{4}-\d\d-\d\d["\']', b2):
            b2 = re.sub(r'"verified": ["\']\d{4}-\d\d-\d\d["\']', f'"verified": "{day}"', b2, count=1)
        else:
            b2 = b2.replace(f'"price": {new_price}', f'"price": {new_price}, "verified": "{day}"', 1)
        s = s[:i] + b2 + s[j:]
    pp.write_text(s)
    # 2a. stock: the daily read takes the first available variant, so on a listing with several variants a record whose own
    # variant is sold out reads "in stock". Where the variants were re-read, use the variant that is this record; where
    # that variant can't be singled out, drop the read and keep the record's own in_stock.
    sp = src / "stock.json"
    if sp.exists():
        st = json.loads(sp.read_text())
        for slug, rv_ in RECVAR.items():
            p = BY_SLUG.get(slug)
            if p is None or slug not in st["in_stock"] or len(rv_.get("variants", [])) < 2:
                continue
            v, _ = pick_variant(p["name"], rv_["variants"], p.get("price"))
            if v is None:
                st["in_stock"].pop(slug)
            else:
                st["in_stock"][slug] = bool(v.get("available"))
        sp.write_text(json.dumps(st, indent=1) + "\n")
    # 2. read dates for every price read (build.py uses one only where it matches the record)
    (src / "price_reads.json").write_text(json.dumps({"date": day, "prices": dict(sorted(reads.items()))}, indent=1) + "\n")
    # 3. rival rows: src/rival_reads.json {"date", "cells": {"<page>|<maker url>": {"from": old cell, "to": new cell}}};
    # build.py swaps the cell only while the page still shows "from", so a later rewrite of the row wins by itself.
    cells_out = {}
    cells = {(r["page"], r["row"]): r for r in rv["rows"]}
    for x, moved in [(x, False) for x in out["rivals"]["same"]] + [(x, True) for x in out["rivals"]["applied"]]:
        r = cells[(x["page"], x["row"])]
        cell = r["price_cell"]
        if moved:
            cell = MONEY.sub(lambda m: money(r["live_price"]), cell, count=1)
        cell = re.sub(r"20\d\d-\d\d-\d\d", day, cell, count=1) if re.search(r"20\d\d-\d\d-\d\d", cell) else f"{cell} (maker, {day})"
        if cell != r["price_cell"]:
            cells_out[f'{x["page"]}|{r["url"]}'] = {"from": r["price_cell"], "to": cell}
    (src / "rival_reads.json").write_text(json.dumps({"date": day, "cells": dict(sorted(cells_out.items()))},
                                                     indent=1, ensure_ascii=False) + "\n")
    done = len(cells_out)
    print(f"applied: {len(out['ours']['applied'])} record prices, {len(reads)} read dates, {done} rival cells")


if __name__ == "__main__":
    sys.exit(main())
