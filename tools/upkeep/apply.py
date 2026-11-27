"""Step 2b of the weekly upkeep: write each status into its product record (src/products.py) and Amazon's reads into
src/amazon_prices.json. Structured fields only: in_stock, preorder, price, list_price (when the record keeps one),
verified, and the one managed caveat "Checked <date> on <store>: <status>." The record's prose (summary, fit, other
caveats) is reread and corrected by the page step (pages.py), like every other page that mentions the product.

Returns the list of changes: [{"slug", "field", "old", "new"}].
"""
from __future__ import annotations

import datetime as dt
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
PRODUCTS_PY = ROOT / "src" / "products.py"
AMAZON = ROOT / "src" / "amazon_prices.json"
MANAGED = re.compile(r"^Checked 20\d\d-\d\d-\d\d on ")


def record_span(txt: str, slug: str) -> tuple[int, int]:
    m = re.search(r'\{"slug": [\'"]%s[\'"]' % re.escape(slug), txt)
    if not m:
        raise KeyError(slug)
    end = txt.find('\n{"slug"', m.start())
    return m.start(), (end if end > 0 else txt.rfind("\n]"))


def preorder_text(s: dict) -> str | None:
    if s["status"] != "pre":
        return None
    t, d = s.get("ships_text") or "", s.get("ships_date")
    if not d:
        return "an unannounced date; the store's dispatch date has passed" if "passed" in t else "no date given"
    day = dt.date.fromisoformat(d)
    base = f"{t} {day.year}" if re.match(r"(early|mid|late)", t, re.I) else f"{day:%b} {day.day}, {day.year}"
    base = base.replace("mid ", "mid-")
    return f"{base} ({s['waiting_item'].removeprefix('the ')})" if s.get("waiting_item") else base


def store_name(p: dict) -> str:
    if str(p.get("program", "")).startswith("amazon"):
        return "Amazon"
    b = p["brand"]
    return f"{b}' US store" if b.endswith("s") else f"{b}'s US store"


def caveat(p: dict, s: dict, today: str) -> str:
    import classify
    if s["status"] == "sold":
        body = "sold out."
    elif s["status"] == "pre":
        body = f"pre-order; the page says {classify.ship_line(s)}." if classify.ship_line(s).startswith(("ships", "the ")) else f"{classify.ship_line(s)}."
    else:
        body = "ships now (no pre-order label or ship date on the page)."
    return f"Checked {today} on {store_name(p)}: {body}"


def _set(block: str, key: str, val) -> str:
    pat = re.compile(r'"%s": (\'(?:[^\'\\]|\\.)*\'|"(?:[^"\\]|\\.)*"|[-\d.]+|True|False|None)' % key)
    if val is None:
        return re.sub(r', "%s": (\'(?:[^\'\\]|\\.)*\'|"(?:[^"\\]|\\.)*"|[-\d.]+|True|False|None)' % key, "", block, count=1)
    if pat.search(block):
        return pat.sub(lambda m: f'"{key}": {val!r}', block, count=1)
    return re.sub(r'("price": (?:[-\d.]+|None))', lambda m: m.group(1) + f', "{key}": {val!r}', block, count=1)


def apply(products: list[dict], statuses: dict, reads: dict, today: str | None = None) -> list[dict]:
    today = today or dt.date.today().isoformat()
    txt = PRODUCTS_PY.read_text()
    amz = json.loads(AMAZON.read_text())
    changes = []
    for p in products:
        s = statuses.get(p["slug"])
        if not s or s["status"] == "unknown":
            continue
        a, b = record_span(txt, p["slug"])
        block = new = txt[a:b]
        was_in, was_pre, was_price = p.get("in_stock", True), p.get("preorder"), p.get("price")
        now_in = s["status"] != "sold"
        now_pre = preorder_text(s)
        if was_in != now_in:
            new = _set(new, "in_stock", None if now_in else False)
            changes.append({"slug": p["slug"], "field": "stock", "old": "in stock" if was_in else "sold out", "new": "in stock" if now_in else "sold out"})
        if (was_pre or None) != (now_pre or None):
            new = _set(new, "preorder", now_pre)
            changes.append({"slug": p["slug"], "field": "ship date", "old": was_pre or "ships now", "new": now_pre or "ships now"})
        price = s.get("price")
        if str(p.get("program", "")).startswith("amazon"):
            if p.get("asin") and price is not None:
                old = (amz["asins"].get(p["asin"]) or {}).get("price")
                amz["asins"][p["asin"]] = {"at": reads.get(p["slug"], {}).get("read_at", today + "T00:00:00Z"), "in_stock": now_in, "price": price}
                if old != price:
                    changes.append({"slug": p["slug"], "field": "price", "old": old, "new": price})
        elif price is not None and was_price is not None and abs(float(price) - float(was_price)) >= 0.01:
            new = _set(new, "price", float(price))
            changes.append({"slug": p["slug"], "field": "price", "old": was_price, "new": float(price)})
            r = reads.get(p["slug"], {})
            if "list_price" in p:
                cmp_ = r.get("v_compare")
                new = _set(new, "list_price", cmp_ if cmp_ and cmp_ > float(price) else None)
        if price is not None or s["status"] == "sold":
            new = re.sub(r'"verified": [\'"][\d-]+[\'"]', f'"verified": {today!r}', new, count=1)
        # the managed caveat: replace last week's, else put it first
        cav = caveat(p, s, today)
        olds = [c for c in p.get("caveats") or [] if MANAGED.match(c)]
        if olds:
            for c in olds:
                for lit in (repr(c), '"' + c.replace('"', '\\"') + '"', "'" + c.replace("'", "\\'") + "'"):
                    if lit in new:
                        new = new.replace(lit, repr(cav), 1)
                        break
        elif s["status"] != "now" or was_pre or not was_in:
            new = re.sub(r'"caveats": \[', lambda m: '"caveats": [' + repr(cav) + (", " if p.get("caveats") else ""), new, count=1)
        if new != block:
            txt = txt[:a] + new + txt[b:]
    PRODUCTS_PY.write_text(txt)
    AMAZON.write_text(json.dumps(amz, indent=1, sort_keys=True) + "\n")
    return changes
