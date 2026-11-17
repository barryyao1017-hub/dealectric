#!/usr/bin/env python3.12
"""Apply a refresh pass's price and stock reads to src/products.py (DLC-221).

    python3.12 growth/bfcm/applyprices.py growth/bfcm/prices-2026-11-17.json

Input: [{"slug", "price"?, "list_price"?, "in_stock"?, "date"}]. Each given field is set in the record and "verified" is
stamped with the date; a list_price at or below the price is dropped (no strike-through without a saving).
"""
import json
import re
import sys
from pathlib import Path

P = Path(__file__).resolve().parents[2] / "src/products.py"


def setfield(rec, key, val):
    lit = repr(val) if not isinstance(val, bool) else str(val)
    pat = rf'"{key}": [^,\n]+,'
    if re.search(pat, rec):
        return re.sub(pat, f'"{key}": {lit},', rec, count=1)
    return re.sub(r'("price": [^,\n]+,)', rf'\1 "{key}": {lit},', rec, count=1)


def main():
    s = P.read_text()
    for ch in json.load(open(sys.argv[1])):
        slug = ch["slug"]
        i = next((k for k in (s.find(f"{{\"slug\": '{slug}',"), s.find(f'{{"slug": "{slug}",')) if k >= 0), -1)
        if i < 0:
            print(f"{slug}: not found"); continue
        j = s.find('\n{"slug": ', i + 1)
        j = len(s) if j < 0 else j
        rec = new = s[i:j]
        price = ch.get("price")
        if price is not None:
            new = setfield(new, "price", price)
        cur_price = price if price is not None else float(re.search(r'"price": ([0-9.]+)', new).group(1))
        if ch.get("list_price") is not None:
            if ch["list_price"] > cur_price:
                new = setfield(new, "list_price", ch["list_price"])
        if "in_stock" in ch:
            if ch["in_stock"] is False:
                new = setfield(new, "in_stock", False)
            else:
                new = re.sub(r' ?"in_stock": False,', "", new, count=1)
        new = setfield(new, "verified", ch["date"])
        if new != rec:
            s = s[:i] + new + s[j:]
            print(f"{slug}: " + ", ".join(f"{k}={v}" for k, v in ch.items() if k not in ("slug", "date")))
    P.write_text(s)


if __name__ == "__main__":
    main()
