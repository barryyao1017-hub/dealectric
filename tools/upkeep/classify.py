"""Step 2a of the weekly upkeep: turn each read into a status: ships now, pre-order (with the date its last item ships),
or sold out, plus the price as read.

Rules decide what they can: a Shopify variant the store marks unavailable is sold out; an Amazon listing that is
"Currently unavailable" is sold out and one "released on <date>" is a pre-order. A page with no pre-order, ship-date or
stock note ships now. Everything else (a page whose notes may belong to this product, a kit part, or another product
on the page; a store that is not Shopify) goes to a model in small batches, which must quote the note it relied on.

Status dict per slug:
    {"status": "now" | "pre" | "sold" | "unknown", "ships_text": "Jan 19" | "late January" | None,
     "ships_date": "2027-01-19" | None, "waiting_item": "the 200 W panel" | None, "price": 549.0 | None,
     "evidence": "<the note quoted>", "how": "rule" | "<model>"}
"""
from __future__ import annotations

import datetime as dt
import json
import re

import llm

NOTE = re.compile(r"pre-?order|expected to (begin )?ship|ships? (from|on|in|by|starting)|ship(ping)? starting|dispatch|"
                  r"coming soon|back ?order|sold ?out|out of stock|notify me|currently unavailable|reserve|"
                  r"will (be )?ship|available (from|on|in)|estimated (ship|deliver)", re.I)
GENERIC = re.compile(r"^(free (ground )?shipping\b.*|shipping( & returns| policy)?|shipping calculated at checkout\.?|"
                     r"\d.?\d? business days delivery.*|swift delivery|delivered in .*days|in stock.*|order now to ship in \d+ business days?)$", re.I)

SCHEMA = {"type": "object", "properties": {"items": {"type": "array", "items": {"type": "object", "properties": {
    "slug": {"type": "string"}, "status": {"type": "string", "enum": ["now", "pre", "sold", "unknown"]},
    "ships_text": {"type": ["string", "null"]}, "ships_date": {"type": ["string", "null"]},
    "waiting_item": {"type": ["string", "null"]}, "price": {"type": ["number", "null"]},
    "evidence": {"type": "string"}}, "required": ["slug", "status", "evidence"]}}}, "required": ["items"]}

PROMPT = """Today is {today}. For each product below, read its store page excerpts and say whether a shopper ordering
the EXACT product named (this variant or bundle) today gets it now, on pre-order, or cannot buy it.

Rules:
- status "sold": the store won't sell it (sold out, out of stock, notify me, unavailable, delisted).
- status "pre": orders are taken but ship later. ships_text: the date in this exact form: a day as "Jan 19" / "Dec 14"
  (three-letter month, no ordinal, no year), or a part of a month as "late January" / "mid-February" / "early
  December"; ships_date: your best ISO estimate (early=5th, mid=15th, late=25th of the month; a date with
  no year is the next one after today). For a bundle, the date is when its LAST item ships (e.g. a station ships now but
  its panel ships Jan 19: status pre, waiting_item "the 200 W panel" — a singular subject for "ships", lower case
  "the ..."). A dispatch date already in the past, with the
  pre-order label still up: status pre, ships_date null, ships_text "date passed, none given".
- status "now": nothing says it ships later. Generic shipping lines (free shipping, "2-5 business days except
  pre-sale", "ships in 1 business day") mean now.
- Pages also print notes for OTHER products (add-ons, other variants, "you may also need", old notices from past
  years). Ignore any note that is not about this product or one of its bundle items. If the page doesn't let you tell,
  status "unknown".
- price: the price shown for this exact variant, a number, or null when the excerpt doesn't show it.
- evidence: quote the note you relied on (or "no ship note for this product").

Products:
{items}

Answer with JSON {{"items": [...]}}, one entry per slug, same slugs."""


def _rule(r: dict) -> dict | None:
    if r.get("error"):
        return {"status": "unknown", "evidence": r["error"], "how": "rule"}
    if r["kind"] == "amazon":
        a = r.get("amazon") or {}
        price = float(re.sub(r"[^\d.]", "", a["price"])) if a.get("price") and re.search(r"\d", a["price"]) else None
        if a.get("captcha") or not a.get("title"):
            return {"status": "unknown", "evidence": "Amazon page did not load (captcha or no title)", "how": "rule"}
        av = (a.get("avail") or "")
        m = re.search(r"released on (\w+ \d{1,2}(, \d{4})?)", av, re.I)
        if m:
            return {"status": "pre", "ships_text": m.group(1), "ships_date": None, "price": price, "evidence": av, "how": "rule",
                    "delivery": a.get("delivery")}
        if re.search(r"currently unavailable|out of stock|unavailable", av, re.I) or not a.get("cart"):
            return {"status": "sold", "price": price, "evidence": av or "no Add to Cart button", "how": "rule"}
        return {"status": "now", "price": price, "evidence": av or "Add to Cart", "how": "rule", "delivery": a.get("delivery")}
    if r["kind"] == "shopify":
        if r.get("v_avail") is False:
            return {"status": "sold", "price": r.get("v_price"), "evidence": "store marks the variant unavailable", "how": "rule"}
        if "variant" not in r:
            return None   # no product data: let the page decide
        notes = [l for l in r.get("stock_lines", []) if NOTE.search(l) and not GENERIC.match(l.strip())]
        if not notes:
            return {"status": "now", "price": r.get("v_price"), "evidence": "no ship note on the page", "how": "rule"}
    return None


def _item_text(r: dict, p: dict) -> str:
    return json.dumps({"slug": r["slug"], "product": p["name"], "variant": r.get("vtitle"), "store_price": r.get("v_price"),
                       "buttons": r.get("btns"), "stock_lines": r.get("stock_lines", [])[:40],
                       "text_from_title": (r.get("buy_area") or "")[:2500]}, ensure_ascii=False)


def classify(reads: list[dict], by_slug: dict, batch: int = 10) -> dict:
    out, todo = {}, []
    for r in reads:
        s = _rule(r)
        if s:
            out[r["slug"]] = s
        elif r["slug"] in by_slug:
            todo.append(r)
    today = dt.date.today().isoformat()
    for i in range(0, len(todo), batch):
        chunk = todo[i:i + batch]
        res = llm.ask(PROMPT.format(today=today, items="\n".join(_item_text(r, by_slug[r["slug"]]) for r in chunk)), schema=SCHEMA)
        got = {x["slug"]: x for x in (res.get("items") or [])}
        for r in chunk:
            x = got.get(r["slug"]) or {"status": "unknown", "evidence": res.get("reason") or "no answer for this slug"}
            x["how"] = res.get("_model", "model")
            if x.get("price") is None and r.get("v_price") is not None:
                x["price"] = r["v_price"]
            out[r["slug"]] = x
        print(f"classified {min(i + batch, len(todo))}/{len(todo)} by model", flush=True)
    return out


def ship_line(s: dict) -> str:
    """The status phrase the alternative line and the record's stock caveat use: "sold out", "ships Jan 19",
    "the 200 W panel ships Jan 19", "pre-order, no current ship date"."""
    if s["status"] == "sold":
        return "sold out"
    if s["status"] != "pre":
        return ""
    t = s.get("ships_text")
    if not t or "passed" in t or "none" in t:
        return "pre-order, no current ship date"
    t = re.sub(r",? 20\d\d$", "", t)
    return f"{s['waiting_item']} ships {t}" if s.get("waiting_item") else f"ships {t}"


def far(s: dict, days: int = 14) -> bool:
    """Sold out, or a pre-order shipping more than `days` out (or with no date): the cases that get an alternative."""
    if s["status"] == "sold":
        return True
    if s["status"] != "pre":
        return False
    d = s.get("ships_date")
    if not d:
        return True
    try:
        return dt.date.fromisoformat(d) > dt.date.today() + dt.timedelta(days=days)
    except ValueError:
        return True
