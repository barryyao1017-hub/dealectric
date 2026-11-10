#!/usr/bin/env python3.12
"""Set a product record's price (and optionally list_price) in src/products.py and stamp "verified".

    python3.12 growth/bfcm/setprice.py <slug> <price> [<list_price>|-] [--date 2026-11-10]
"""
import re
import sys
from pathlib import Path

P = Path(__file__).resolve().parents[2] / "src/products.py"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    date = sys.argv[sys.argv.index("--date") + 1] if "--date" in sys.argv else "2026-11-10"
    if "--date" in sys.argv:
        args.remove(date)
    slug, price = args[0], args[1]
    lp = args[2] if len(args) > 2 else "-"
    s = P.read_text()
    i = next(k for k in (s.find(f"{{\"slug\": '{slug}',"), s.find(f'{{"slug": "{slug}",')) if k >= 0)
    j = s.find("\n{\"slug\": ", i + 1)
    j = len(s) if j < 0 else j
    rec = s[i:j]
    new = re.sub(r'"price": [^,\n]+,', f'"price": {price},', rec, count=1)
    if lp != "-":
        new = (re.sub(r'"list_price": [^,\n]+,', f'"list_price": {lp},', new, count=1) if '"list_price"' in new
               else new.replace(f'"price": {price},', f'"price": {price}, "list_price": {lp},', 1))
    new = (re.sub(r'"verified": [\'"][0-9-]+[\'"]', f'"verified": \'{date}\'', new, count=1) if '"verified"' in new
           else new.replace(f'"price": {price},', f'"price": {price}, "verified": \'{date}\',', 1))
    if new == rec:
        print(f"{slug}: no change")
        return
    P.write_text(s[:i] + new + s[j:])
    print(f"{slug}: price {price}" + (f", list {lp}" if lp != "-" else ""))


if __name__ == "__main__":
    main()
