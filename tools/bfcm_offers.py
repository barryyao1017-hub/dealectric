#!/usr/bin/env python3.12
"""List the coupon codes and sales our joined advertisers publish on CJ and Awin, and flag codes not yet in
src/coupons.json (Black Friday / Cyber Monday 2026, Barry 2026-11-10). Read-only: it never edits coupons.json.

    python3.12 tools/bfcm_offers.py            # CJ only (link-search API, token in keychain item cj-api-token)
    python3.12 tools/bfcm_offers.py --awin     # also Awin My Offers, read in a background tab of the Agent Chrome
                                               # (localhost:9222, must already be signed in to ui.awin.com)

Writes growth/bfcm/offers-<date>.json: [{network, brand_key, code, name, start, end, new}] and prints the new codes
and the sales whose name mentions Black Friday, Cyber Monday or holiday. New codes still need a cart test
(tools/codecheck.py) before they are published.
"""
from __future__ import annotations

import datetime as _dt
import json
import re
import subprocess
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINKS = json.loads((ROOT / "src/links.json").read_text())
HAVE = {c["code"].upper() for c in json.loads((ROOT / "src/coupons.json").read_text())["codes"]}
CJ_PID = "101901491"
AWIN_PUB = "3120687"
SEASON = re.compile(r"black|cyber|bfcm|\bBF\b|holiday|christmas|double 11|singles", re.I)


def cj() -> list[dict]:
    tok = subprocess.run(["security", "find-generic-password", "-s", "cj-api-token", "-w"], capture_output=True, text=True).stdout.strip()
    out = []
    for key, v in LINKS["cj"].items():
        page = 1
        while True:
            url = "https://link-search.api.cj.com/v2/link-search?" + urllib.parse.urlencode(
                {"website-id": CJ_PID, "advertiser-ids": v["cid"], "records-per-page": 100, "page-number": page})
            req = urllib.request.Request(url, headers={"Authorization": "Bearer " + tok})
            links = ET.fromstring(urllib.request.urlopen(req, timeout=60).read()).find("links")
            got = [{c.tag: (c.text or "") for c in l} for l in links.findall("link")]
            for d in got:
                if d.get("promotion-type") in ("", "N/A"):
                    continue
                out.append({"network": "cj", "brand_key": key, "code": d.get("coupon-code", ""), "name": d.get("link-name", ""),
                            "start": d.get("promotion-start-date", "")[:10], "end": d.get("promotion-end-date", "")[:10]})
            if page * 100 >= int(links.get("total-matched", "0")) or not got:
                break
            page += 1
    return out


def awin() -> list[dict]:
    sys.path.insert(0, str(ROOT / "growth/evals"))
    import ui  # noqa: E402  (the Agent Chrome CDP client; background tabs only)
    tab = ui.Tab(f"https://ui.awin.com/awin/affiliate/{AWIN_PUB}/promotion")
    time.sleep(12)
    if "login" in (tab.eval("location.href") or ""):
        tab.close()
        raise SystemExit("Awin is signed out in the Agent Chrome: sign in through agent-vault, then re-run with --awin")
    out = []
    try:
        for key, v in LINKS["awin"].items():
            if not isinstance(v, dict) or not v.get("mid"):
                continue
            for page in range(1, 8):
                path = (f"/awin/affiliate/{AWIN_PUB}/promotion/xhr-list-promotions/promotionType//categoryIds//regionIds//"
                        f"advertiserIds/{v['mid']}/membershipStatus//promotionStatus//page/{page}/")
                h = tab.eval(f"fetch('{path}',{{credentials:'include',headers:{{'X-Requested-With':'XMLHttpRequest'}}}}).then(r=>r.text())")
                rows = tab.eval("(h=>{const d=new DOMParser().parseFromString(h,'text/html');return [...d.querySelectorAll('tr')]"
                                ".map(tr=>[...tr.querySelectorAll('td')].map(td=>td.innerText.replace(/\\s+/g,' ').trim())).filter(r=>r.length>5)})("
                                + json.dumps(h) + ")") or []
                for c in rows:
                    dates = re.findall(r"(\d{1,2})/(\d{1,2})/(\d{4})", c[5] if len(c) > 5 else "")
                    iso = [f"{y}-{int(m):02d}-{int(d):02d}" for m, d, y in dates]
                    out.append({"network": "awin", "brand_key": key, "code": "" if c[2] == "Promotion" else c[2], "name": c[3][:200],
                                "start": iso[0] if iso else "", "end": iso[1] if len(iso) > 1 else ""})
                if len(rows) < 10:
                    break
                time.sleep(0.5)
    finally:
        tab.close()
    return out


def main() -> int:
    today = _dt.date.today().isoformat()
    offers = cj() + (awin() if "--awin" in sys.argv else [])
    seen = set()
    for o in offers:
        o["new"] = bool(o["code"]) and o["code"].upper() not in HAVE and (not o["end"] or o["end"] >= today)
    (ROOT / f"growth/bfcm/offers-{today}.json").write_text(json.dumps(offers, indent=1, ensure_ascii=False) + "\n")
    for o in offers:
        k = (o["network"], o["brand_key"], o["code"] or o["name"])
        if k in seen or (o["end"] and o["end"] < today):
            continue
        seen.add(k)
        if o["new"] or SEASON.search(o["name"]):
            print(f"{'NEW ' if o['new'] else '    '}{o['network']:4} {o['brand_key']:16} {o['code'] or '(sale)':14} {o['start']}→{o['end'] or '–'}  {o['name'][:110]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
