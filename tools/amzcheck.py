#!/usr/bin/env python3
"""Read Amazon US listings with curl: exact title, current price and rating by ASIN, or the ASINs a search returns.

Used by the gap-page pipeline (growth/gapmine/daily-plan.md) to confirm an ASIN is the product the page names and to
compare Amazon's price with the maker's store before choosing the link. The prices the pages show come from
tools/amzprice.py (daily, src/amazon_prices.json), not from this script.

    python3.12 tools/amzcheck.py asin B0DKXDKBG5 [B0... ...]     # JSON lines: asin, title, price, rating, ratings
    python3.12 tools/amzcheck.py search "fiio dm13"               # JSON lines: asin, title
"""
from __future__ import annotations

import html
import json
import re
import subprocess
import sys
import urllib.parse

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130 Safari/537.36"


def _get(url: str) -> str:
    p = subprocess.run(["curl", "-s", "-4", "--compressed", "--max-time", "25", "-A", UA, "-H", "Accept-Language: en-US", url],
                       capture_output=True, text=True, errors="replace")
    return p.stdout


def listing(asin: str) -> dict:
    s = _get(f"https://www.amazon.com/dp/{asin}")
    t = re.search(r'id="productTitle"[^>]*>(.*?)</span>', s, re.S)
    price = re.search(r'class="a-offscreen">\$([0-9,.]+)<', s)
    hist = re.findall(r'aria-label="(\d+) percent of reviews have (\d) stars', s)
    n = re.search(r"([0-9,]+) ratings", s)
    return {"asin": asin, "found": bool(t), "title": html.unescape(t.group(1).strip()) if t else None,
            "price": float(price.group(1).replace(",", "")) if price else None,
            "five_star_pct": next((int(p) for p, st in hist if st == "5"), None),
            "ratings": int(n.group(1).replace(",", "")) if n else None,
            "blocked": "captcha" in s.lower() or len(s) < 5000}


def search(q: str, n: int = 8) -> list[dict]:
    s = _get("https://www.amazon.com/s?k=" + urllib.parse.quote(q))
    out: list[dict] = []
    for m in re.finditer(r'data-asin="(B0[A-Z0-9]{8})"', s):
        a = m.group(1)
        if a not in [x["asin"] for x in out]:
            seg = s[m.end(): m.end() + 6000]
            t = re.search(r'<h2[^>]*aria-label="([^"]+)"', seg) or re.search(r"<h2[^>]*>.*?<span[^>]*>(.*?)</span>", seg, re.S)
            out.append({"asin": a, "title": html.unescape(re.sub("<[^>]+>", "", t.group(1)))[:160] if t else ""})
        if len(out) >= n:
            break
    return out


if __name__ == "__main__":
    if len(sys.argv) >= 3 and sys.argv[1] == "asin":
        for a in sys.argv[2:]:
            print(json.dumps(listing(a)))
    elif len(sys.argv) == 3 and sys.argv[1] == "search":
        for r in search(sys.argv[2]):
            print(json.dumps(r))
    else:
        print(__doc__)
