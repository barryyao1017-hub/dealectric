#!/usr/bin/env python3.12
"""Amazon Associates numbers for the daily update, read from Associates Central's own JSON (stopgap, 2026-11-26).

Amazon has no reporting API for Associates website accounts (PA-API / the Creators API are product data only). This
opens the earnings report in a background tab of the agent's Chrome (localhost:9222, signed in to
affiliate-program.amazon.com as barrryyao@gmail.com), captures the auth headers the page sends with its own
`/reporting/summary` request (Authorization, X-CSRF-Token, customerId, ...; without them the endpoint answers 401) and
repeats that request for the last 30 days. The answer holds one record per day with clicks, ordered items, ordered
revenue, shipped items and earnings.

It is undocumented and will break when Amazon changes the page or the session signs out. When it fails for more than
a day or two, the fallback is the S3 data feed Associates support can turn on (see the Dealectric To-Dos).

Limits: every tracking ID is lumped into one total, so test-tag clicks (dealectrictest-20, tools/kitcheck.py) are
counted with shoppers'. The per-item table (`/reporting/table`, group_by purchased_asin) answered 400 even to Amazon's
own page on 11-26, so which products sold is not read here.

    python3.12 tools/amzsales.py          # human summary
    python3.12 tools/amzsales.py --json   # the parsed numbers
"""
from __future__ import annotations

import json
import sys
import time
from datetime import date, timedelta
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

STORE = "dealectric-20"
HOST = "https://affiliate-program.amazon.com"
PAGE = f"{HOST}/p/reporting/earnings"
KEEP = ("Accept", "Authorization", "X-CSRF-Token", "X-Requested-With", "customerId", "language", "locale",
        "marketplaceId", "programId", "roles", "storeId")
FIELDS = ("clicks", "ordered_items", "ordered_revenue", "shipped_items", "shipped_revenue", "returned_items",
          "total_earnings")


def summary_url(start: str, end: str) -> str:
    return (f"{HOST}/reporting/summary?query[start_date]={start}&query[end_date]={end}&query[type]=commission"
            f"&query[storeId]={STORE}&query[locale]=US&store_id={STORE}")


def num(v) -> float:
    try:
        return float(str(v).replace(",", "").replace("$", ""))
    except ValueError:   # Amazon writes "-" for a field it doesn't fill
        return 0.0


def capture_headers(tab, wait_s: float = 40.0) -> dict | None:
    """Load the earnings page and return the headers of its own /reporting/summary request."""
    tab.call("Network.enable")
    tab.call("Page.navigate", url=PAGE)
    end = time.monotonic() + wait_s
    while time.monotonic() < end:
        tab.ws.settimeout(max(0.1, end - time.monotonic()))
        try:
            m = json.loads(tab.ws.recv())
        except Exception:  # noqa: BLE001  (timeout)
            break
        if m.get("method") == "Network.requestWillBeSent":
            r = m["params"]["request"]
            if "/reporting/summary" in r["url"] and r.get("headers", {}).get("Authorization"):
                return {k: v for k, v in r["headers"].items() if k in KEEP}
    return None


def read(days: int = 30) -> tuple[dict | None, str | None]:
    """({'days': {day: {field: number}}, 'total': {...}, 'yesterday': {...}, 'updated': str}, error)."""
    import codesweep
    if not codesweep.browser_ok():
        return None, "no Agent Chrome on localhost:9222"
    today = date.today()
    start, end = (today - timedelta(days=days)).isoformat(), (today - timedelta(days=1)).isoformat()
    tab = codesweep.Tab("about:blank")
    try:
        hdr = capture_headers(tab)
        if not hdr:
            href = tab.eval("location.href") or ""
            if "/ap/signin" in href or "signin" in href:
                return None, "Associates Central signed out in the Agent Chrome (log in through agent-vault)"
            return None, f"earnings page sent no summary request (page {href[:80]})"
        js = ("(async()=>{const r=await fetch(%s,{headers:%s,credentials:'include'});"
              "return [r.status, await r.text()]})()") % (json.dumps(summary_url(start, end)), json.dumps(hdr))
        status, body = tab.eval(js)
    finally:
        tab.close()
    if status != 200:
        return None, f"summary endpoint answered {status}"
    try:
        d = json.loads(body)
    except ValueError:
        return None, "summary endpoint answered non-JSON"
    per_day = {r["day"]: {f: num(r.get(f)) for f in FIELDS} for r in d.get("records", []) if r.get("day")}
    tot = (d.get("total") or {}).get("table") or {}
    total = {f: num(tot.get(f)) for f in FIELDS} if tot else {f: sum(v[f] for v in per_day.values()) for f in FIELDS}
    zero = {f: 0.0 for f in FIELDS}
    return {"start": start, "end": end, "days": per_day, "total": total, "yesterday": per_day.get(end, zero),
            "updated": d.get("last_updated", "")}, None


def line(r: dict) -> str:
    t, y = r["total"], r["yesterday"]
    return (f"Amazon {r['start']}..{r['end']}: {t['clicks']:.0f} clicks, {t['ordered_items']:.0f} items ordered "
            f"(${t['ordered_revenue']:.2f}), {t['shipped_items']:.0f} shipped, ${t['total_earnings']:.2f} earned; "
            f"yesterday {y['clicks']:.0f} clicks, {y['ordered_items']:.0f} ordered, ${y['total_earnings']:.2f}"
            + (f" (Amazon data as of {r['updated']})" if r.get("updated") else ""))


def main(argv: list[str]) -> int:
    r, err = read()
    if err:
        print(f"Amazon: {err}")
        return 1
    if "--json" in argv:
        print(json.dumps(r, indent=1))
        return 0
    print(line(r))
    for day, v in sorted(r["days"].items()):
        if v["ordered_items"] or v["total_earnings"]:
            print(f"  {day}: {v['ordered_items']:.0f} ordered (${v['ordered_revenue']:.2f}), "
                  f"{v['shipped_items']:.0f} shipped, ${v['total_earnings']:.2f} earned, {v['clicks']:.0f} clicks")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
