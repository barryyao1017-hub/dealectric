#!/usr/bin/env python3
"""Read a maker's Shopify store with curl: products matching a search (title, price, compare-at, availability, URL and
the description text), or one product page's variants. Free and keyless; Shopify answers /search/suggest.json even
when it rate-limits /products/<handle>.js (esrtech.com, 2026-11-05).

    python3.12 tools/storecheck.py search https://www.esrtech.com "geo wallet"
    python3.12 tools/storecheck.py product https://www.esrtech.com/products/geo-wallet-boost-halolock
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import urllib.parse

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"


def _get(url: str) -> tuple[int, str]:
    p = subprocess.run(["curl", "-s", "-4", "-L", "--max-time", "25", "-A", UA, "-w", "\n%{http_code}", url],
                       capture_output=True, text=True, errors="replace")
    body, _, code = p.stdout.rpartition("\n")
    return (int(code) if code.isdigit() else 0), body


def _text(h: str) -> str:
    return re.sub(r"\s+", " ", html.unescape(re.sub("<[^>]+>", " ", h or ""))).strip()


def search(home: str, q: str, n: int = 10) -> list[dict]:
    code, body = _get(home.rstrip("/") + "/search/suggest.json?" + urllib.parse.urlencode(
        {"q": q, "resources[type]": "product", "resources[limit]": n}))
    if code != 200:
        return [{"error": f"HTTP {code}"}]
    out = []
    for p in json.loads(body)["resources"]["results"].get("products") or []:
        out.append({"title": p["title"], "price": float(p["price"]), "compare_at": float(p.get("compare_at_price_max") or 0) or None,
                    "available": p.get("available"), "url": home.rstrip("/") + p["url"].split("?")[0],
                    "text": _text(p.get("body"))[:1500]})
    return out


def product(url: str) -> dict:
    code, body = _get(url.split("?")[0].rstrip("/") + ".js")
    if code != 200:
        return {"error": f"HTTP {code}"}
    p = json.loads(body)
    return {"title": p["title"], "available": p.get("available"),
            "variants": [{"id": v["id"], "title": v["title"], "price": v["price"] / 100,
                          "compare_at": (v.get("compare_at_price") or 0) / 100 or None, "available": v["available"]} for v in p["variants"]],
            "text": _text(p.get("description"))[:2000]}


if __name__ == "__main__":
    if len(sys.argv) == 4 and sys.argv[1] == "search":
        for r in search(sys.argv[2], sys.argv[3]):
            print(json.dumps(r))
    elif len(sys.argv) == 3 and sys.argv[1] == "product":
        print(json.dumps(product(sys.argv[2]), indent=1))
    else:
        print(__doc__)
