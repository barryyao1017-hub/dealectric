#!/usr/bin/env python3.12
"""Refresh the Amazon prices our pages show (Barry 2026-11-12: Amazon gave written permission to display prices).

Every ASIN the site links (Amazon Associates product records in src/products.py and the "asin" rows of comparison
tables in src/gaps.py) is opened in a background tab of the agent's Chrome (localhost:9222) and the buy-box price and
stock line are read from the page. The result goes to src/amazon_prices.json:

    {"asins": {"B0...": {"price": 199.99, "at": "2026-11-12T06:50:12Z", "in_stock": true}, ...}}

src/build.py shows each price with the date it was read (Barry 11-12: no disclaimer or expiry; keep the prices current).
An ASIN with no price read on the latest run is dropped, so its page says "price on the Amazon page" instead of an old
price. Run daily by tools/codesweep.py before its rebuild; a failure there never stops the sweep.

    python3.12 tools/amzprice.py                 # all ASINs
    python3.12 tools/amzprice.py B0BFBTR94M ...  # just these (testing)
"""
from __future__ import annotations

import datetime as dt
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))
OUT = ROOT / "src" / "amazon_prices.json"

PAUSE_S = 3.0          # between pages: a human pace, one tab
LOAD_WAIT_S = 20.0     # longest wait for the buy box to render

JS_READ = r"""(()=>{
  const body = document.body ? document.body.innerText.slice(0, 800) : '';
  const captcha = /captcha|not a robot|Enter the characters you see/i.test(document.title + body);
  const sel = ['#corePrice_feature_div .a-price .a-offscreen', '#corePriceDisplay_desktop_feature_div .a-price .a-offscreen',
               '#apex_desktop .a-price .a-offscreen', '#price_inside_buybox', '#newBuyBoxPrice', '#tp_price_block_total_price_ww .a-offscreen'];
  let price = null;
  for (const s of sel) {   // the first element of a block can be an empty placeholder: take the first one holding a price
    const e = [...document.querySelectorAll(s)].find(x => /\$\s?[0-9]/.test(x.textContent || ''));
    if (e) { price = e.textContent.trim(); break; } }
  const av = document.querySelector('#availability');
  const title = document.querySelector('#productTitle');
  return {price, avail: av ? av.innerText.trim().slice(0, 120) : null, title: title ? title.innerText.trim().slice(0, 120) : null,
          captcha, ready: document.readyState};
})()"""


def all_asins() -> list[str]:
    from products import PRODUCTS
    import gaps
    out = [p["asin"] for p in PRODUCTS if p["program"].startswith("amazon:") and p.get("asin")]
    out += [r["asin"] for c in gaps.GAP_PAGES for r in c.get("rows", []) if r.get("asin")]
    return list(dict.fromkeys(out))


def parse_price(t: str | None) -> float | None:
    if not t:
        return None
    s = t.replace("$", "").replace(",", "").strip().split()[0]
    try:
        v = float(s)
    except ValueError:
        return None
    return v if v > 0 else None


def read_one(tab, asin: str) -> dict:
    tab.call("Page.navigate", url=f"https://www.amazon.com/dp/{asin}")
    end = time.monotonic() + LOAD_WAIT_S
    r: dict = {}
    while time.monotonic() < end:
        time.sleep(1.5)
        try:
            r = tab.eval(JS_READ) or {}
        except Exception:  # noqa: BLE001  (page between documents)
            continue
        if r.get("captcha") or r.get("price") or (r.get("ready") == "complete" and r.get("title")):
            if r.get("price") or r.get("captcha") or time.monotonic() > end - LOAD_WAIT_S + 6:
                break
    return r


def main(argv: list[str]) -> int:
    import codesweep
    if not codesweep.browser_ok():
        raise SystemExit("no browser on localhost:9222")
    asins = argv or all_asins()
    prev = json.loads(OUT.read_text()) if OUT.exists() else {"asins": {}}
    got, miss, blocked = 0, [], 0
    tab = codesweep.Tab("about:blank")
    try:
        for i, a in enumerate(asins):
            try:
                r = read_one(tab, a)
            except Exception as e:  # noqa: BLE001  (dead socket: reopen the tab once and go on)
                print(f"{a}: {type(e).__name__}: {e}", flush=True)
                try:
                    tab.close()
                except Exception:  # noqa: BLE001
                    pass
                tab = codesweep.Tab("about:blank")
                r = {}
            if r.get("captcha"):
                blocked += 1
            price = parse_price(r.get("price"))
            now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            if price:
                av = (r.get("avail") or "").lower()
                prev["asins"][a] = {"price": price, "at": now,
                                    "in_stock": not any(w in av for w in ("unavailable", "out of stock"))}
                got += 1
            else:
                prev["asins"].pop(a, None)   # no price read today: the page shows none rather than an old one
                miss.append(a)
            print(f"[{i + 1}/{len(asins)}] {a} {price} {(r.get('avail') or '')[:40]!r}{' CAPTCHA' if r.get('captcha') else ''}", flush=True)
            if blocked >= 5 and got == 0:
                print("captcha on every page: stopping", flush=True)
                break
            time.sleep(PAUSE_S)
    finally:
        tab.close()
    OUT.write_text(json.dumps(prev, indent=1, sort_keys=True) + "\n")
    print(f"prices {got}/{len(asins)}; no price {len(miss)}; captcha {blocked}", flush=True)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
