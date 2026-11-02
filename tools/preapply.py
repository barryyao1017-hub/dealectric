#!/usr/bin/env python3.12
"""Check that a product's buy link can open the store's checkout with the code already applied, before setting the
product's `cart_variant` in src/products.py (Barry, 2026-11-01: "the code is pre-applied" is one of the two selling
points, said on the site whenever it is true; growth/codes/README.md "Selling points").

Usage: python3.12 tools/preapply.py <slug> [<variant id>]
  With no variant id, the Shopify variant is read from <product url>.js (the first available one).

Opens the affiliate deep link (CJ or Awin, the same one the Worker redirects to) with the Shopify cart permalink
/cart/<variant>:1?discount=<code> as its destination, in a background tab of the agent's Chrome (localhost:9222), and
reports: the landing page, whether the code shows as applied with the expected saving, and whether the network's click
ID (Awin awc / CJ cjevent) reached the store. Exit 0 only when all three hold. One test click goes to the network."""
import json, re, sys, time, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "src")]
import codesweep as C  # noqa: E402
import build as B  # noqa: E402


def first_variant(url: str) -> int:
    req = urllib.request.Request(url.split("?")[0] + ".js", headers={"User-Agent": "Mozilla/5.0"})
    d = json.loads(urllib.request.urlopen(req, timeout=20).read())
    return next((v["id"] for v in d["variants"] if v.get("available")), d["variants"][0]["id"])


def main() -> int:
    slug = sys.argv[1]
    p = dict(B.BY_SLUG[slug])
    p["cart_variant"] = int(sys.argv[2]) if len(sys.argv) > 2 else (p.get("cart_variant") or first_variant(p["url"]))
    c, saving, *_ = B.best_offer(p)
    if not c:
        print(f"{slug}: no passing code to pre-apply")
        return 1
    url, net, _ = B.tracked_link(p)
    print(f"variant {p['cart_variant']}; destination {B.buy_url(p)} via {net}")
    t = C.Tab(url)
    try:
        href = ""
        for _ in range(30):
            time.sleep(2)
            href = t.eval("location.href") or ""
            if "/checkouts/" in href:
                time.sleep(6)
                break
        href = t.eval("location.href") or ""
        txt = t.eval("document.body.innerText") or ""
        ck = (t.eval("document.cookie") or "").lower()
    finally:
        t.close()
    at_checkout = "/checkouts/" in href
    applied = c["code"] in txt and f"{saving:.2f}" in txt
    click_id = any(k in href.lower() or k in ck for k in ("awc=", "cjevent"))
    print(f"checkout: {at_checkout} ({href.split('?')[0]})")
    print(f"code {c['code']} applied with saving ${saving:.2f}: {applied}")
    print(f"network click ID at the store: {click_id}")
    if all((at_checkout, applied, click_id)):
        print(f'OK: set "cart_variant": {p["cart_variant"]} on {slug} in src/products.py')
        return 0
    return 1


if __name__ == "__main__":
    sys.exit(main())
