#!/usr/bin/env python3.12
"""Daily update for Barry's phone (North Star set 2026-10-30): progress to 10 credited outside sales in a rolling
30 days, the leading indicator (ChatGPT-tagged clicks on /go/ from real browsers), new sales, and the cart sweep's
health.

  python3.12 tools/dailyupdate.py            # one-line summary first, then details
  python3.12 tools/dailyupdate.py --no-cj    # skip CJ (no agent Chrome)

Sources:
- D1 `clicks` (wrangler, read-only): kind='redirect', bot_like=0, utm_source='chatgpt.com', minus user agents that
  are scanners or ours (REAL_UA below). A shopper is one (Pacific day, user agent) pair.
- CJ Commission Detail, Last 30 Days, read from the agent's Chrome over CDP (localhost:9222, signed in to CJ). Every
  row counts toward the North Star; a row posted in the last 26 h is NEW and gets matched to that brand's /go/ clicks.
  Awin is not read yet: its sales would be missing from the count.
- The sweep log's last 'codesweep end' line.

Nothing is written to the repo: commission and order IDs stay out of the public history.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
import time
import urllib.request
from collections import Counter
from datetime import datetime, timedelta, timezone
from pathlib import Path
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "growth" / "evals"))
sys.path.insert(0, str(ROOT / "src"))
import evallib as E  # noqa: E402
from products import PRODUCTS  # noqa: E402

PT = ZoneInfo("America/Los_Angeles")
GOAL = 10
CDP = "http://localhost:9222"
CJ_REPORT = "https://members.cj.com/member/app/redirect?view=pubTransactions"
SWEEP_LOG = Path.home() / "Library/Logs/claude-automations/dealectric-codesweep.log"
CJ_COLS = ["commission_id", "advertiser", "action_type", "sale", "discount", "commission", "corrected", "status",
           "action_name", "website", "ad_id", "posted", "event", "order_id", "coupon", "cross_device"]


def real_ua(ua: str) -> bool:
    """A browser a person uses: not the bare 'Mozilla/5.0 (compatible)' prober, not a short or stale scanner UA,
    not ours."""
    if len(ua) < 60 or ua == "Mozilla/5.0 (compatible)" or "dealectric-" in ua:
        return False
    return not any(s in ua for s in ("iPhone OS 13_2_3", "HeadlessChrome", "Nexus 5X"))


def pt_day(ts: str) -> str:
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(PT).strftime("%Y-%m-%d")


def chatgpt_clicks(now: datetime) -> tuple[list[dict], str | None]:
    since = (now - timedelta(days=8)).strftime("%Y-%m-%dT%H:%M:%S")
    rows, err = E.d1_query("SELECT ts, slug, user_agent FROM clicks WHERE kind='redirect' AND bot_like=0 "
                           f"AND utm_source='chatgpt.com' AND ts >= '{since}' ORDER BY ts")
    return [r for r in rows if real_ua(r.get("user_agent") or "")], err


def cdp_page(url: str, button: str, wait=(20, 15)) -> str:
    """Open `url` in a new tab of the agent's Chrome, click the button labelled `button`, return the page text."""
    import websocket  # websocket-client, as tools/codesweep.py
    tab = json.load(urllib.request.urlopen(urllib.request.Request(f"{CDP}/json/new?about:blank", method="PUT"), timeout=10))
    ws = websocket.create_connection(tab["webSocketDebuggerUrl"], timeout=60, suppress_origin=True)
    n = 0

    def call(method, **params):
        nonlocal n
        n += 1
        ws.send(json.dumps({"id": n, "method": method, "params": params}))
        while True:
            r = json.loads(ws.recv())
            if r.get("id") == n:
                return r.get("result", {})

    def ev(js):
        return call("Runtime.evaluate", expression=js, returnByValue=True, awaitPromise=True)["result"].get("value")

    try:
        call("Page.navigate", url=url)
        time.sleep(wait[0])
        ev("(()=>{const b=[...document.querySelectorAll('button')].filter(x=>x.innerText.trim()===%s).pop();"
           "if(b) b.click()})()" % json.dumps(button))
        time.sleep(wait[1])
        return ev("location.href + '\\n' + document.body.innerText") or ""
    finally:
        ws.close()
        urllib.request.urlopen(f"{CDP}/json/close/{tab['id']}", timeout=10)


def cj_sales() -> tuple[list[dict], str | None]:
    try:
        text = cdp_page(CJ_REPORT, "RUN REPORT")
    except Exception as e:  # noqa: BLE001 - any CDP failure means "CJ not read"
        return [], f"agent Chrome not reachable ({e.__class__.__name__}: {e})"
    if "members.cj.com" not in text.split("\n", 1)[0] or "Commission ID" not in text:
        return [], "CJ report not shown (signed out?): " + text.split("\n", 1)[0][:120]
    rows = []
    for line in text[text.index("Commission ID"):].splitlines():
        cells = [c.strip() for c in line.split("\t")]
        if len(cells) >= 15 and re.fullmatch(r"\d{6,}", cells[0]):
            rows.append(dict(zip(CJ_COLS, cells)))
    return rows, None


def cj_time(s: str) -> datetime | None:
    """CJ shows '29-Oct-2026 8:30' in the account's time zone, taken to be Pacific."""
    try:
        return datetime.strptime(s, "%d-%b-%Y %H:%M").replace(tzinfo=PT)
    except ValueError:
        return None


def sweep_health(today: str) -> str:
    try:
        marks = re.findall(r"===== (\d{4}-\d\d-\d\dT[\d:]+Z) codesweep (start|end \(exit (\d+)\))",
                           SWEEP_LOG.read_text(errors="replace"))
    except OSError:
        return "sweep log missing"
    if not marks:
        return "no sweep run logged"
    ts, kind, code = marks[-1]
    day = pt_day(ts)
    if kind == "start":
        return "sweep still running" if day == today else f"sweep never finished (started {day})"
    if code != "0":
        return f"sweep FAILED {day} (exit {code})"
    return "sweep ok" if day == today else f"sweep MISSED (last {day})"


def money(s: str) -> float:
    try:
        return float(s.replace("$", "").replace(",", ""))
    except ValueError:
        return 0.0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-cj", action="store_true", help="skip the CJ report (needs the agent's Chrome)")
    args = ap.parse_args()

    now = datetime.now(timezone.utc)
    today = now.astimezone(PT).strftime("%Y-%m-%d")
    yday = (now.astimezone(PT) - timedelta(days=1)).strftime("%Y-%m-%d")
    week = {(now.astimezone(PT) - timedelta(days=d)).strftime("%Y-%m-%d") for d in range(1, 8)}

    clicks, d1_err = chatgpt_clicks(now)
    y = [c for c in clicks if pt_day(c["ts"]) == yday]
    w = [c for c in clicks if pt_day(c["ts"]) in week]
    shoppers_w = {(pt_day(c["ts"]), c["user_agent"]) for c in w}
    shoppers_y = {c["user_agent"] for c in y}

    sales, cj_err = ([], "skipped") if args.no_cj else cj_sales()
    new = [s for s in sales if (t := cj_time(s["posted"])) and now - t <= timedelta(hours=26)]
    brand_of = {p["slug"]: p["brand"].lower() for p in PRODUCTS}

    parts = [f"North Star {len(sales)}/{GOAL} (30d, CJ)" if not cj_err else "North Star ?/10 (CJ not read)",
             f"ChatGPT clicks yday {len(y)} ({len(shoppers_y)} shoppers), 7d {len(w)} ({len(shoppers_w)})"
             if not d1_err else "ChatGPT clicks ? (D1 error)"]
    if new:
        parts.append("NEW SALE: " + ", ".join(f"{s['advertiser']} ${money(s['commission']):.2f}" for s in new))
    elif not cj_err:
        parts.append("no new sale")
    parts.append(sweep_health(today))
    print(" · ".join(parts))

    print(f"\nNorth Star: {len(sales)} of {GOAL} credited sales in CJ's last 30 days"
          + (f", ${sum(money(s['commission']) for s in sales):.2f} commission." if sales else ".")
          + " Awin not read yet.")
    if cj_err:
        print(f"  CJ: {cj_err}")
    for s in sales:
        print(f"  {'NEW ' if s in new else ''}{s['advertiser']}: sale {s['sale']}, commission {s['commission']}, "
              f"{s['status']}, event {s['event']} PT, posted {s['posted']} PT, coupon {s['coupon'] or 'none'}")
        if s in new:
            ev = cj_time(s["event"])
            adv = s["advertiser"].lower()
            near = [c for c in clicks if brand_of.get(c["slug"]) == adv and ev
                    and timedelta(0) <= ev - datetime.fromisoformat(c["ts"].replace("Z", "+00:00")) <= timedelta(days=30)]
            for c in near[-6:]:
                print(f"    ChatGPT click before it: {c['ts'][:16]}Z /go/{c['slug']} ({c['user_agent'][:60]})")
            if not near:
                print("    no ChatGPT-tagged click on this brand before it (an untagged or older click carried it)")

    print(f"\nLeading indicator: ChatGPT-tagged /go/ clicks from real browsers"
          f" (yesterday {yday} PT: {len(y)} clicks, {len(shoppers_y)} shoppers; 7 days: {len(w)} clicks, {len(shoppers_w)} shoppers).")
    if d1_err:
        print(f"  D1: {d1_err}")
    for slug, k in Counter(c["slug"] for c in w).most_common(8):
        print(f"  {k:3d}  /go/{slug}")
    print(f"\nSweep: {sweep_health(today)} ({SWEEP_LOG})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
