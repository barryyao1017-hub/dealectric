#!/usr/bin/env python3.12
"""Daily update for Barry's phone (North Star set 2026-10-30): progress to 10 credited outside sales in a rolling
30 days, the leading indicator (ChatGPT-tagged clicks on /go/ from real browsers), new sales, and the cart sweep's
health.

  python3.12 tools/dailyupdate.py            # one-line summary first, then details
  python3.12 tools/dailyupdate.py --no-cj    # skip the CJ API call

Sources:
- D1 `clicks` (wrangler, read-only): kind='redirect', bot_like=0, utm_source='chatgpt.com', minus user agents that
  are scanners or ours (REAL_UA below). A shopper is one (Pacific day, user agent) pair.
- CJ commissions API (commissions.api.cj.com, publisher CID 8096118, personal access token in the keychain item
  cj-api-token; since 2026-11-08, DLC-209: the Commission Detail page needed a CJ web session that kept signing out).
  Last 30 days by posting date; every row counts toward the North Star; a row posted in the last 26 h is NEW and gets
  matched to that brand's /go/ clicks.
- Awin: the Worker's D1 `sales` rows (network='awin', written by Awin's Transaction Notifications callback, with the
  voucher code since 2026-11-08). Awin has no cheap read API for us; the callback is the record.
- The sweep log's last 'codesweep end' line.

Nothing is written to the repo: commission and order IDs stay out of the public history.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import urllib.error
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
CJ_API = "https://commissions.api.cj.com/query"
CJ_CID = "8096118"          # the publisher *company* id the API authorizes (not the PID 101901491 used in links)
SWEEP_LOG = Path.home() / "Library/Logs/claude-automations/dealectric-codesweep.log"


def real_ua(ua: str) -> bool:
    """A browser a person uses: not the bare 'Mozilla/5.0 (compatible)' prober, not a short or stale scanner UA,
    not ours."""
    if len(ua) < 60 or ua == "Mozilla/5.0 (compatible)" or "dealectric-" in ua:
        return False
    return not any(s in ua for s in ("iPhone OS 13_2_3", "HeadlessChrome", "Nexus 5X"))


def pt_day(ts: str) -> str:
    return datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(PT).strftime("%Y-%m-%d")


def chatgpt_clicks(now: datetime, sources: tuple[str, ...] = ("chatgpt.com",)) -> tuple[list[dict], str | None]:
    since = (now - timedelta(days=8)).strftime("%Y-%m-%dT%H:%M:%S")
    src = ", ".join(f"'{s}'" for s in sources)
    rows, err = E.d1_query("SELECT ts, slug, user_agent, utm_source FROM clicks WHERE kind='redirect' AND bot_like=0 "
                           f"AND utm_source IN ({src}) AND ts >= '{since}' ORDER BY ts")
    return [r for r in rows if real_ua(r.get("user_agent") or "")], err


# Tags the edge Worker puts on our links in pages served to a verified agent browser (worker/src/index.js
# agentBrowser, DLC-146, since 2026-11-03): a shopper's tap on a link Muse handed over arrives with utm_source=muse.
AGENT_TAGS = ("muse", "chatgpt-agent", "signed-agent")


def keychain(service: str) -> str:
    r = subprocess.run(["security", "find-generic-password", "-s", service, "-w"], capture_output=True, text=True)
    return r.stdout.strip() if r.returncode == 0 else ""


def cj_sales(now: datetime) -> tuple[list[dict], str | None]:
    """CJ commissions posted in the last 30 days (the API's maximum window), newest last."""
    tok = keychain("cj-api-token")
    if not tok:
        return [], "no cj-api-token in the keychain (developers.cj.com -> Personal Access Tokens)"
    iso = lambda t: t.strftime("%Y-%m-%dT%H:%M:%SZ")  # noqa: E731
    q = ('{ publisherCommissions(forPublishers: ["%s"], sincePostingDate: "%s", beforePostingDate: "%s") '
         '{ count payloadComplete records { commissionId advertiserName actionStatus postingDate eventDate lockingDate '
         'pubCommissionAmountUsd saleAmountUsd correctionReason coupon shopperId orderId } } }'
         % (CJ_CID, iso(now - timedelta(days=30)), iso(now + timedelta(hours=1))))
    req = urllib.request.Request(CJ_API, data=json.dumps({"query": q}).encode(),
                                 headers={"authorization": "Bearer " + tok, "content-type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            body = json.load(r)
    except urllib.error.HTTPError as e:
        try:
            body = json.load(e)
        except Exception:  # noqa: BLE001
            return [], f"CJ API HTTP {e.code}"
    except Exception as e:  # noqa: BLE001
        return [], f"CJ API unreachable ({e.__class__.__name__}: {e})"
    if body.get("errors"):
        return [], "CJ API error: " + str(body["errors"][0].get("message", body["errors"][0]))[:160]
    rows = []
    for r in body["data"]["publisherCommissions"]["records"]:
        status = r.get("actionStatus") or "?"
        if r.get("correctionReason"):
            status += f" (corrected: {r['correctionReason']})"
        rows.append({"network": "CJ", "id": str(r["commissionId"]), "advertiser": r.get("advertiserName") or "?",
                     "sale": r.get("saleAmountUsd"), "commission": r.get("pubCommissionAmountUsd"), "status": status,
                     "posted": r.get("postingDate") or "", "event": r.get("eventDate") or "",
                     "locks": r.get("lockingDate") or "", "coupon": r.get("coupon") or "", "sub_id": r.get("shopperId") or ""})
    return sorted(rows, key=lambda x: x["posted"]), None


def awin_sales(now: datetime) -> tuple[list[dict], str | None]:
    """Awin transactions the Worker recorded in the last 30 days (D1 `sales`). Status is not known here: Awin
    validates within about 30 days and a reversal arrives as a negative-commission row."""
    since = (now - timedelta(days=30)).strftime("%Y-%m-%dT%H:%M:%S")
    rows, err = E.d1_query("SELECT ts, txn_id, advertiser, commission, sale, sub_id, event_date, voucher, click_time FROM sales "
                           f"WHERE network='awin' AND ts >= '{since}' ORDER BY ts")
    out = [{"network": "Awin", "id": str(r["txn_id"]), "advertiser": r.get("advertiser") or "?", "sale": r.get("sale"),
            "commission": r.get("commission"), "status": "recorded (Awin validates in ~30 days)",
            "posted": r["ts"], "event": r.get("event_date") or "", "locks": "", "coupon": r.get("voucher") or awin_code_credit(r),
            "sub_id": r.get("sub_id") or ""} for r in rows]
    return out, err


def awin_code_credit(r: dict) -> str:
    """Awin can't name the code on an order, but a sale credited by a code assigned to us (BLUETTI's DEALECTRIC)
    comes with no clickRef and a click time equal to the order time (DLC-209; click_time since 2026-11-13)."""
    ct, ev = r.get("click_time") or "", r.get("event_date") or ""
    return "our code (no link click)" if not r.get("sub_id") and ct and ct[:16] == ev[:16] else ""


def when(s: str) -> datetime | None:
    """CJ gives ISO 8601 UTC ('2026-10-29T15:30:36Z'); Awin's callback gives '2026-11-07 20:57:03' (UTC) and D1 ts
    is ISO UTC."""
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00").replace(" ", "T")).replace(
            tzinfo=timezone.utc) if "+" not in s and not s.endswith("Z") else datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def pt(s: str) -> str:
    d = when(s)
    return d.astimezone(PT).strftime("%Y-%m-%d %H:%M") if d else (s or "?")


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


def money(s) -> float:
    try:
        return float(str(s).replace("$", "").replace(",", ""))
    except ValueError:
        return 0.0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-cj", action="store_true", help="skip the CJ API call")
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

    agent_clicks, _ = chatgpt_clicks(now, AGENT_TAGS)
    agent_y = [c for c in agent_clicks if pt_day(c["ts"]) == yday]
    agent_w = [c for c in agent_clicks if pt_day(c["ts"]) in week]

    cj, cj_err = ([], "skipped") if args.no_cj else cj_sales(now)
    awin, awin_err = awin_sales(now)
    sales = cj + awin
    credited = [s for s in sales if money(s["commission"]) > 0]   # corrections (negative rows) don't count
    new = [s for s in sales if (t := when(s["posted"])) and now - t <= timedelta(hours=26)]
    brand_of = {p["slug"]: p["brand"].lower() for p in PRODUCTS}

    missing = [n for n, e in (("CJ", cj_err), ("Awin", awin_err)) if e]
    parts = [f"North Star {len(credited)}/{GOAL} (30d, CJ+Awin)" if not missing
             else f"North Star {len(credited)}+?/{GOAL} ({' and '.join(missing)} not read)",
             f"ChatGPT clicks yday {len(y)} ({len(shoppers_y)} shoppers), 7d {len(w)} ({len(shoppers_w)})"
             if not d1_err else "ChatGPT clicks ? (D1 error)"]
    if new:
        parts.append("NEW SALE: " + ", ".join(f"{s['advertiser']} ${money(s['commission']):.2f} ({s['network']})" for s in new))
    elif not missing:
        parts.append("no new sale")
    parts.append(sweep_health(today))
    print(" · ".join(parts))

    print(f"\nNorth Star: {len(credited)} of {GOAL} credited sales in the last 30 days (CJ {len(cj)}, Awin {len(awin)})"
          + (f", ${sum(money(s['commission']) for s in sales):.2f} commission." if sales else "."))
    if cj_err:
        print(f"  CJ: {cj_err}")
    if awin_err:
        print(f"  Awin (D1): {awin_err}")
    for s in sales:
        print(f"  {'NEW ' if s in new else ''}{s['network']} {s['advertiser']}: sale ${money(s['sale']):.2f}, "
              f"commission ${money(s['commission']):.2f}, {s['status']}, order {pt(s['event'])} PT, "
              f"seen {pt(s['posted'])} PT, code {s['coupon'] or 'none'}, sub-ID {s['sub_id'] or 'none'}"
              + (f", locks {pt(s['locks'])} PT" if s["locks"] else ""))
        if s in new:
            ev = when(s["event"])
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
    print(f"\nAgent-browser clicks (links Muse and other shopping agents handed over; Barry's own tests count too):"
          f" yesterday {len(agent_y)}, 7 days {len(agent_w)}.")
    for (src, slug), k in Counter((c["utm_source"], c["slug"]) for c in agent_w).most_common(8):
        print(f"  {k:3d}  {src}  /go/{slug}")
    print(f"\nSweep: {sweep_health(today)} ({SWEEP_LOG})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
