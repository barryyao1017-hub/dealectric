#!/usr/bin/env python3
"""Check promo codes against a Shopify store's own cart, without checking out.

For each code: fresh cart session, add one product, apply the code via /cart/update.js,
then read /cart.js. Shopify reports each code as applicable or not, plus the discount.

  python3 tools/codecheck.py https://www.soundcore.com/products/a3874-aerofit-2-open-earbuds AFSC20 SAVE10
"""
import json, os, ssl, sys, time, urllib.error, urllib.request, http.cookiejar
from urllib.parse import urlsplit

# python.org's Python ships no CA bundle; macOS keeps one at /etc/ssl/cert.pem (seen 2026-10-22: every HTTPS call failed
# with CERTIFICATE_VERIFY_FAILED under python3.12 until this).
_CTX = ssl.create_default_context(cafile="/etc/ssl/cert.pem") if os.path.exists("/etc/ssl/cert.pem") else ssl.create_default_context()

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"


def session():
    jar = http.cookiejar.CookieJar()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar), urllib.request.HTTPSHandler(context=_CTX))

    def call(url, data=None):
        req = urllib.request.Request(url, data=json.dumps(data).encode() if data is not None else None,
                                     headers={"User-Agent": UA, "Accept": "application/json", "Content-Type": "application/json"})
        for wait in (15, 0):  # one short retry on Shopify's 429s
            try:
                with op.open(req, timeout=30) as r:
                    return json.loads(r.read())
            except urllib.error.HTTPError as e:
                if e.code != 429 or not wait:
                    raise
                time.sleep(wait)
    return call


def check(product_url, code, qty=1):
    s = urlsplit(product_url)
    base, handle = f"{s.scheme}://{s.netloc}", s.path.rstrip("/").split("/products/")[1]
    call = session()
    prod = call(f"{base}/products/{handle}.js")
    var = next((v for v in prod["variants"] if v.get("available")), prod["variants"][0])
    call(f"{base}/cart/add.js", {"items": [{"id": var["id"], "quantity": qty}]})
    call(f"{base}/cart/update.js", {"discount": code})
    cart = call(f"{base}/cart.js")
    dc = next((d for d in cart.get("discount_codes", []) if d["code"].upper() == code.upper()), None)
    apps = ([{"title": a.get("title"), "type": a.get("type"), "value": a.get("value"), "value_type": a.get("value_type"),
              "amount": a.get("total_allocated_amount", 0) / 100} for a in cart.get("cart_level_discount_applications", [])]
            + [{"title": a["discount_application"].get("title"), "amount": a["amount"] / 100, "line": True}
               for it in cart["items"] for a in it.get("line_level_discount_allocations", [])])
    return {"code": code, "store": s.netloc, "product": prod["title"], "variant_available": var.get("available"),
            "applicable": bool(dc and dc.get("applicable")),
            "subtotal": cart["original_total_price"] / 100, "total": cart["total_price"] / 100,
            "discount": cart["total_discount"] / 100,
            "code_amount": round(sum(a["amount"] for a in apps if (a.get("title") or "").upper() == code.upper()), 2),
            "applications": apps}


if __name__ == "__main__":
    url, *codes = sys.argv[1:]
    qty = 1
    if codes and codes[0].startswith("--qty="):
        qty = int(codes.pop(0).split("=")[1])
    for c in codes:
        try:
            print(json.dumps(check(url, c, qty)))
        except Exception as e:
            print(json.dumps({"code": c, "error": repr(e)}))
