#!/usr/bin/env python3.12
"""tools/codecheck.py's cart test, run from inside the store's own page in a background tab of the Agent Chrome
(localhost:9222), for when a Shopify store answers 429 to plain HTTP from this network (2026-11-10: every store did,
all day, from the work laptop). Same sequence and same result fields as codecheck.check: clear the cart, add one unit
of the first available variant, apply the code through /cart/update.js, read /cart.js. Never checks out.

    python3.12 tools/codecheck_browser.py <product_url> CODE [CODE ...]

Each run includes the control ZZNOTACODE7Q first; a run whose control applies is reported void. The tab opens in the
background (Target.createTarget background=true) and closes at the end.
"""
from __future__ import annotations

import json
import sys
import time
from pathlib import Path
from urllib.parse import urlsplit

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "growth/evals"))
import ui  # noqa: E402

CONTROL = "ZZNOTACODE7Q"

JS = r"""
(async (handle, code) => {
  const j = async (u, body) => {
    const r = await fetch(u, body === undefined ? {credentials: 'include', headers: {Accept: 'application/json'}}
      : {method: 'POST', credentials: 'include', headers: {'Content-Type': 'application/json', Accept: 'application/json'}, body: JSON.stringify(body)});
    if (!r.ok) throw new Error(u + ' ' + r.status);
    return r.json();
  };
  await j('/cart/clear.js', {});
  await j('/cart/update.js', {discount: ''});
  const prod = await j('/products/' + handle + '.js');
  const v = prod.variants.find(x => x.available) || prod.variants[0];
  await j('/cart/add.js', {items: [{id: v.id, quantity: 1}]});
  await j('/cart/update.js', {discount: code});
  const cart = await j('/cart.js');
  await j('/cart/clear.js', {});
  await j('/cart/update.js', {discount: ''});
  const dc = (cart.discount_codes || []).find(d => d.code.toUpperCase() === code.toUpperCase());
  const apps = (cart.cart_level_discount_applications || []).map(a => ({title: a.title, amount: (a.total_allocated_amount || 0) / 100}))
    .concat(cart.items.flatMap(it => (it.line_level_discount_allocations || []).map(a => ({title: a.discount_application.title, amount: a.amount / 100, line: true}))));
  return {code, product: prod.title, variant_available: v.available, applicable: !!(dc && dc.applicable),
          subtotal: cart.original_total_price / 100, total: cart.total_price / 100, discount: cart.total_discount / 100,
          code_amount: Math.round(apps.filter(a => (a.title || '').toUpperCase() === code.toUpperCase()).reduce((s, a) => s + a.amount, 0) * 100) / 100,
          applications: apps};
})(%s, %s)
"""


def check_many(product_url: str, codes: list[str], pause: float = 3.0) -> list[dict]:
    s = urlsplit(product_url)
    handle = s.path.rstrip("/").split("/products/")[1]
    tab = ui.Tab(product_url)
    out = []
    try:
        time.sleep(8)
        for code in [CONTROL] + codes:
            try:
                r = tab.eval(JS % (json.dumps(handle), json.dumps(code)))
                r["store"] = s.netloc
            except Exception as e:  # noqa: BLE001
                r = {"code": code, "store": s.netloc, "error": repr(e)[:200]}
            out.append(r)
            if code == CONTROL and r.get("applicable"):
                out.append({"void": True, "reason": "control code applied"})
                break
            time.sleep(pause)
    finally:
        tab.close()
    return out


if __name__ == "__main__":
    url, *codes = sys.argv[1:]
    for r in check_many(url, codes):
        print(json.dumps(r))
