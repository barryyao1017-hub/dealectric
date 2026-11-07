#!/usr/bin/env python3.12
"""Cart-test the codes that brand drafts list (growth/gapmine/drafts/*.json "codes") and add the results to
src/coupons.json (DLC-192, 2026-11-06). Only network-issued (Awin/CJ/Rakuten) or brand-site codes are listed by the
drafts, so a code that works is published (growth/codes/README.md "Publishing"); a rejected one is kept as rejected.

    python3.12 tools/codes_add.py [draft-key ...]     # default: every committed brand draft with codes

Shopify stores only (tools/codecheck.py: fresh cart, add one unit, apply the code, read /cart.js); each run includes
the control ZZNOTACODE7Q and counts only when the control is rejected. A 429 waits and retries (codecheck), never
counts as a rejection. Codes on non-Shopify stores are reported and left out. Raw results go to
growth/codes/<date>-checks.jsonl like the daily sweep's.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))
import codecheck  # noqa: E402

DRAFTS = ROOT / "growth/gapmine/drafts"
COUPONS = ROOT / "src/coupons.json"
CONTROL = "ZZNOTACODE7Q"
SOURCE = {"awin": "{b}'s affiliate code (Awin)", "cj": "{b}'s affiliate code (CJ Affiliate)",
          "rakuten": "{b}'s affiliate code (Rakuten Advertising)", "brand site": "printed on {b}'s own US site ({d})"}


def kind_value(terms: str) -> tuple[str, float] | None:
    m = re.search(r"(\d{1,2})\s?%", terms or "")
    if m:
        return "percent", float(m.group(1))
    m = re.search(r"\$\s?(\d+(?:\.\d\d)?)", terms or "")
    if m:
        return "fixed", float(m.group(1))
    return None


def main() -> int:
    import importlib
    import products as P
    importlib.reload(P)
    have = {p["slug"]: p for p in P.PRODUCTS}
    keys = sys.argv[1:] or [f.stem for f in DRAFTS.glob("brand-*.json")]
    today = _dt.date.today().isoformat()
    log = ROOT / f"growth/codes/{today}-checks.jsonl"
    cp = json.loads(COUPONS.read_text())
    known = {(c["brand"], c["code"].upper()) for c in cp["codes"]}
    added = []
    for k in keys:
        f = DRAFTS / f"{k}.json"
        if not f.exists():
            continue
        d = json.loads(f.read_text())
        for c in d.get("codes") or []:
            code, terms = (c.get("code") or "").strip(), c.get("terms") or ""
            slugs = [s for s in c.get("applies_to") or [] if s in have]
            if not code or not slugs:
                continue
            brand = have[slugs[0]]["brand"]
            if (brand, code.upper()) in known:
                continue
            kv = kind_value(terms)
            tests, ok_any, note = [], False, ""
            for s in slugs[:3]:
                url = have[s]["url"]
                if "/products/" not in url:
                    note = "not a Shopify product URL; not cart-tested"
                    break
                try:
                    ctl = codecheck.check(url, CONTROL)
                    if ctl.get("applicable"):
                        note = "control code applied; run void"
                        break
                    time.sleep(6)
                    r = codecheck.check(url, code)
                except Exception as e:  # noqa: BLE001  (store not Shopify, product gone, network)
                    note = f"cart check failed: {e!r}"[:160]
                    break
                with log.open("a") as fh:
                    fh.write(json.dumps({"date": today, "brand": brand, "product": s, **r}) + "\n")
                tests.append({"date": today, "product": s, "qty": 1, "subtotal": r["subtotal"], "discount": round(r["code_amount"] or r["discount"], 2)})
                ok_any = ok_any or (r["applicable"] and (r["code_amount"] or r["discount"]) > 0)
                time.sleep(12)
            if not tests:
                print(f"{brand} {code}: {note}", flush=True)
                continue
            if kv is None and ok_any:   # read the type/value off the cart when the terms don't state it
                t0 = next(t for t in tests if t["discount"] > 0)
                kv = ("percent", round(100 * t0["discount"] / t0["subtotal"])) if t0["subtotal"] else ("fixed", t0["discount"])
            src = SOURCE.get(c.get("source") or "", "{b}'s affiliate code").format(b=brand, d=today)
            rec = {"brand": brand, "code": code, "type": (kv or ("percent", 0))[0], "value": (kv or ("percent", 0))[1],
                   "terms": terms[:160] or "as stated by the brand", "source": src, "publish": bool(ok_any),
                   "result": "works" if ok_any else "rejected", "tests": tests}
            if c.get("expires"):
                rec["expires"] = c["expires"]
            if not re.search(r"site-?wide|all (products|orders|items)|everything|any order", terms, re.I):
                rec["slugs"] = slugs   # build.code_saving reads a top-level "slugs" scope; sitewide codes have none
            cp["codes"].append(rec)
            known.add((brand, code.upper()))
            added.append(rec)
            print(f"{brand} {code}: {rec['result']} " + ", ".join(f"{t['product']} -{t['discount']}" for t in tests), flush=True)
    cp["checked"] = today
    COUPONS.write_text(json.dumps(cp, indent=1, ensure_ascii=False) + "\n")
    print(f"added {len(added)} codes ({sum(1 for r in added if r['result'] == 'works')} work)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
