#!/usr/bin/env python3.12
"""Which brands a new page should serve first (Barry 2026-11-13, "steer new page building toward high-ticket,
code-carrying categories").

Evidence (growth/reports/2026-11-13-product-mix.html): from 10-29 to 11-13 the 348 non-solar products drew 71 of 151 page
visitors but 14 of 237 buy-link clicks and 0 of 10 sales; every sale was a $478-$1,791 ALLPOWERS or BLUETTI order
carrying a cart-tested code. So a page's worth is not its uncovered searches alone:

    value = uncovered searches x ticket x code multiplier x link multiplier

- ticket: median store price of the brand's products in docs/offers.json, clipped to [$20, $2,000]; a brand with no
  products yet counts as TICKET_UNKNOWN (neutral, never parked).
- code: x1.5 when any of the brand's products carries a published, cart-tested code.
- link: x0.5 when every product of the brand links to Amazon (no code, a few percent commission, clicks invisible to D1).

A cluster takes the best of its brands. Clusters whose best brand has a known ticket under TICKET_FLOOR are parked
(status "parked", kept in the queue, not built) instead of queued.

    python3.12 growth/evals/brandvalue.py            # brands ranked by value factor
"""
from __future__ import annotations

import json
import re
import statistics
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TICKET_FLOOR = 150.0      # below this median price a page is parked (no sale yet under $478)
TICKET_UNKNOWN = 150.0    # approved brand with no product records yet
CODE_MULT, AMAZON_MULT = 1.5, 0.5
# brands.json key -> offers.json brand, where squashing the name doesn't give the key
ALIAS = {"autelpilot": "autelrobotics", "omdigital": "omsystem"}
PARK_REASON = "parked 2026-11-13: brand ticket under $150 (Barry: steer pages to high-ticket, code-carrying categories)"


def _key(name: str) -> str:
    return re.sub(r"[^a-z0-9]", "", name.lower())


@lru_cache(maxsize=1)
def brands() -> dict[str, dict]:
    """Squashed brand name -> {ticket, code, amazon_only, products, factor}."""
    prods = json.loads((ROOT / "docs/offers.json").read_text())["products"]
    by: dict[str, list[dict]] = {}
    for p in prods:
        by.setdefault(_key(p["brand"]), []).append(p)
    out = {}
    for k, ps in by.items():
        prices = [p["offer"]["price"] for p in ps if p["offer"].get("price")]
        code = any(p["offer"].get("coupon") for p in ps)
        amazon_only = all("amazon.com" in (p["offer"].get("link") or "") for p in ps)
        ticket = statistics.median(prices) if prices else None
        out[k] = {"ticket": ticket, "code": code, "amazon_only": amazon_only, "products": len(ps)}
        out[k]["factor"] = factor(out[k])
    return out


def factor(b: dict | None) -> float:
    t = (b or {}).get("ticket") or TICKET_UNKNOWN
    f = min(max(t, 20.0), 2000.0)
    if b and b.get("code"):
        f *= CODE_MULT
    if b and b.get("amazon_only"):
        f *= AMAZON_MULT
    return round(f, 2)


def brand(name: str) -> dict | None:
    k = _key(name)
    return brands().get(ALIAS.get(k, k))


def score(item: dict) -> dict:
    """Value fields for a queue item ({'brands': [...], 'uncovered': n} or {'brand': ...}): value, ticket, code, park."""
    names = item.get("brands") or ([item["brand"]] if item.get("brand") else [])
    best, best_f = None, factor(None)
    for n in names:
        b = brand(n)
        if b and (best is None or b["factor"] > best_f):
            best, best_f = b, b["factor"]
    ticket = best["ticket"] if best else None
    return {"value": round((item.get("uncovered") or 0) * best_f), "ticket": ticket, "code": bool(best and best["code"]),
            "park": ticket is not None and ticket < TICKET_FLOOR}


def seed_order(brand_seeds: dict[str, dict]) -> list[str]:
    """brands.json brands -> their seeds, highest-value brand first (seed order kept within a brand)."""
    keys = sorted(brand_seeds, key=lambda k: -factor(brand(k)))
    return [s for k in keys for s in brand_seeds[k]["seeds"]]


if __name__ == "__main__":
    for k, b in sorted(brands().items(), key=lambda kv: -kv[1]["factor"]):
        t = f"${b['ticket']:,.0f}" if b["ticket"] else "  -"
        print(f"{b['factor']:>8.0f}  {t:>7}  {'code' if b['code'] else '    '}  {'amazon' if b['amazon_only'] else '      '}  "
              f"{'PARK' if b['ticket'] and b['ticket'] < TICKET_FLOOR else '    '}  {k}")
