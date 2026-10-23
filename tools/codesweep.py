#!/usr/bin/env python3.12
"""Daily cart check of every published discount code, through the agent's Chrome.

For each code the site publishes (src/coupons.json: publish true, result works, not expired) and every catalog
product it applies to, the script opens the brand's own Shopify store in a tab of the agent's Chrome (DevTools
protocol on localhost:9222, the same browser growth/evals/ui.py drives) and, from the page's own context, puts one
unit (or the code's minimum quantity) in a fresh cart, applies the code and reads the cart back. The store's answer,
accepted with the amount it took off or rejected, is appended to growth/codes/<date>-checks.jsonl in the shape
tools/codecheck.py writes, then folded into src/coupons.json (tools/codes_merge.py), the site is rebuilt, and the
result is committed, pushed and, when the Worker's link map changed, deployed.

Rules: a made-up control code must be rejected by each store or that store's checks are discarded; a code that fails
on every product in one sweep keeps its last passing date and gets a strike; two strikes in a row retire it
(result rejected, so it leaves every page and offers.json); a 429 or a network error is never a rejection, and a code
with any unanswered check gets no strike that day; a product the store cannot put in the cart (sold out) is
inconclusive. Pacing is per store, with backoff on 429 (see GAP_PER_STORE). No order is ever placed and no personal
data entered.

    python3.12 tools/codesweep.py                 # check, merge, rebuild, commit, push, deploy if needed
    python3.12 tools/codesweep.py --dry-run       # list the checks
    python3.12 tools/codesweep.py --no-push       # check, merge, rebuild; leave the commit to you

Scheduled daily by ~/Library/LaunchAgents/com.jiayiyao.dealectric.codesweep.plist via tools/codesweep.sh.
"""
from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import json
import math
import os
import re
import subprocess
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

import websocket  # websocket-client (python3.12 -m pip install --user websocket-client)

sys.path.insert(0, str(Path(__file__).resolve().parent))
import codecheck  # noqa: E402  (plain-HTTP cart check, the fallback when a store's tab leaves its cart origin)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))
from products import PRODUCTS, VERIFIED  # noqa: E402
import codes_merge  # noqa: E402

CDP = "http://localhost:9222"
COUPONS = ROOT / "src" / "coupons.json"
LOG_DIR = ROOT / "growth" / "codes"
CONTROL = "ZZNOTACODE7Q"
# Pacing (DLC-48). Shopify answers 429 to a burst from one client, and some stores (ALLPOWERS, BLUETTI, ESR) stay
# limited for many minutes: on 2026-10-22 and -23 only 6-9 of 32 checks got an answer at 14 s between a store's calls
# with one or three short requeues. Now: a slower base gap, and after a 429 the store cools down (the store's
# Retry-After when it sends one, else an exponential backoff) and its gap widens for the rest of the run. A check is
# tried up to MAX_TRIES times; a store that is still limited STORE_DEADLINE after the sweep started gives up its
# remaining checks. Unanswered checks are never rejections (see merge()).
GAP_PER_STORE = 30.0      # seconds between two checks on the same store
STORE_GAP = {"iallpowers.com": 90.0}   # ALLPOWERS stays limited for minutes after a burst
GAP_MAX = 300.0           # a store's gap widens x1.5 after each 429, up to this
BACKOFF_BASE = 180.0      # cool-down after a store's first 429 in a row; doubles with each further 429 in a row
BACKOFF_MAX = 1200.0
MAX_TRIES = 6             # attempts per check before it is logged as unanswered
STORE_DEADLINE = 3 * 3600  # seconds after the sweep starts; a store still rate-limiting then gives up its remaining checks
REQ_PAUSE_MS = 600        # between the few cart calls inside one check
# Where a brand's cart lives when it is not the host in products.py (Soundcore's US cart is us.soundcore.com).
CART_HOST = {"www.soundcore.com": "us.soundcore.com"}
# Cart hosts checked over plain HTTP (tools/codecheck.py) instead of a browser tab: a browser tab opened on
# us.soundcore.com is sent on to www.soundcore.com, a non-Shopify front end whose /products/<handle>.js is its 404
# page, so every in-tab lookup (the control code too) read "product 404" and the whole store was discarded on 10-22
# and 10-23. The handles themselves are right (us.soundcore.com/products/<handle>.js is a 200 for all seven).
PLAIN_HTTP = {"us.soundcore.com"}
BY_SLUG = {p["slug"]: p for p in PRODUCTS}

# Five cart calls per check (the product lookup only on a handle's first check; its variant is cached), a short pause
# between them, and each failure carries its HTTP status and the store's Retry-After header.
CHECK_JS = r"""
(async () => {
  const H = {'Content-Type': 'application/json', 'Accept': 'application/json'};
  const pause = () => new Promise(r => setTimeout(r, PAUSE));
  const j = async (u, o) => { await pause(); const r = await fetch(u, Object.assign({credentials: 'same-origin'}, o || {}));
    const t = await r.text(); let b = null; try { b = JSON.parse(t); } catch (e) {}
    return {status: r.status, retry_after: r.headers.get('Retry-After'), body: b, text: t.slice(0, 200)}; };
  const fail = (step, x) => ({error: `${step} ${x.status} ${x.text}`, status: x.status, retry_after: x.retry_after});
  let v = VARIANT;
  if (!v) {
    const prod = await j(`/products/HANDLE.js`);
    if (prod.status !== 200 || !prod.body) return fail('product', prod);
    const pv = prod.body.variants.find(x => x.available) || prod.body.variants[0];
    v = {id: pv.id, available: !!pv.available, title: prod.body.title};
  }
  const out = {variant: v, product: v.title, variant_available: v.available};
  if (!v.available) return Object.assign(out, {soldout: true, error: 'sold out (no available variant)'});
  await j('/cart/clear.js', {method: 'POST', headers: H});
  const add = await j('/cart/add.js', {method: 'POST', headers: H, body: JSON.stringify({items: [{id: v.id, quantity: QTY}]})});
  if (add.status >= 400) return Object.assign(out, fail('add', add));
  const upd = await j('/cart/update.js', {method: 'POST', headers: H, body: JSON.stringify({discount: CODE})});
  if (upd.status >= 400) return Object.assign(out, fail('update', upd));
  const cart = await j('/cart.js');
  if (cart.status !== 200 || !cart.body) return Object.assign(out, fail('cart', cart));
  await j('/cart/clear.js', {method: 'POST', headers: H});
  return Object.assign(out, {cart: cart.body});
})()
"""


def log(msg: str) -> None:
    print(f"{dt.datetime.now(dt.timezone.utc).strftime('%H:%M:%S')} {msg}", flush=True)


# ---------------------------------------------------------------- the agent's Chrome

def browser_call(method: str, **params):
    """One command on the browser-level DevTools socket (the URL in /json/version); a fresh connection each time."""
    v = json.loads(urllib.request.urlopen(f"{CDP}/json/version", timeout=10).read())
    ws = websocket.create_connection(v["webSocketDebuggerUrl"], timeout=30, suppress_origin=True)
    try:
        ws.send(json.dumps({"id": 1, "method": method, "params": params}))
        while True:
            msg = json.loads(ws.recv())
            if msg.get("id") == 1:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})
    finally:
        ws.close()


class Tab:
    """A tab opened in the background (Target.createTarget background=true, closed with Target.closeTarget), so the
    sweep never brings Chrome's window to the front; /json/new and /json/close would."""

    def __init__(self, url: str):
        self.target_id = browser_call("Target.createTarget", url=url, background=True)["targetId"]
        self.info = None
        for _ in range(50):
            for t in json.loads(urllib.request.urlopen(f"{CDP}/json/list", timeout=10).read()):
                if t.get("id") == self.target_id and t.get("webSocketDebuggerUrl"):
                    self.info = t
            if self.info:
                break
            time.sleep(0.1)
        if not self.info:
            raise RuntimeError("new background tab not found in /json/list")
        self.ws = websocket.create_connection(self.info["webSocketDebuggerUrl"], timeout=60, suppress_origin=True)
        self._id = 0

    def call(self, method: str, **params):
        self._id += 1
        self.ws.send(json.dumps({"id": self._id, "method": method, "params": params}))
        while True:
            msg = json.loads(self.ws.recv())
            if msg.get("id") == self._id:
                if "error" in msg:
                    raise RuntimeError(f"{method}: {msg['error']}")
                return msg.get("result", {})

    def eval(self, js: str):
        r = self.call("Runtime.evaluate", expression=js, returnByValue=True, awaitPromise=True)
        if "exceptionDetails" in r:
            raise RuntimeError(f"JS: {r['exceptionDetails'].get('text')} {str(r['exceptionDetails'].get('exception', {}).get('description', ''))[:200]}")
        return r.get("result", {}).get("value")

    def fresh_cart(self, host: str):
        """Drop the store's cart cookies so the next call starts a new cart with no discount attached."""
        for name in ("cart", "cart_sig", "cart_ts", "cart_currency", "discount_code", "cart_ver"):
            for dom in (host, "." + host, host.split(".", 1)[-1] if host.count(".") > 1 else host, "." + host.split(".", 1)[-1]):
                try:
                    self.call("Network.deleteCookies", name=name, domain=dom)
                except Exception:
                    pass

    def close(self):
        try:
            self.ws.close()
        finally:
            try:
                browser_call("Target.closeTarget", targetId=self.target_id)
            except Exception:
                pass


def browser_ok() -> str | None:
    try:
        return json.loads(urllib.request.urlopen(f"{CDP}/json/version", timeout=5).read()).get("Browser")
    except Exception:
        return None


# ---------------------------------------------------------------- what to check

def live_published(codes: list[dict], today: str) -> list[dict]:
    return [c for c in codes if c.get("publish") and c.get("result") == "works" and not (c.get("expires") and c["expires"] < today)]


def in_scope(c: dict, p: dict) -> bool:
    if p["brand"] != c["brand"] or p["price"] is None:
        return False
    if c.get("categories") and p["category"] not in c["categories"]:
        return False
    if c.get("slugs") and p["slug"] not in c["slugs"]:
        return False
    return True


def plan_checks(codes: list[dict]) -> list[dict]:
    """One check per (code, product, qty) the code applies to; min_order codes only on products that reach it."""
    checks = []
    for c in codes:
        qty = int(c.get("min_qty") or 1)
        for p in PRODUCTS:
            if not in_scope(c, p):
                continue
            if c.get("min_order") and p["price"] * qty < c["min_order"]:
                continue
            checks.append({"brand": c["brand"], "code": c["code"], "slug": p["slug"], "url": p["url"], "qty": qty})
    return checks


def store_of(url: str) -> tuple[str, str, str]:
    """(cart origin, cart host, product handle) for a Shopify product URL."""
    s = urlsplit(url)
    host = CART_HOST.get(s.netloc, s.netloc)
    handle = s.path.rstrip("/").split("/products/")[1]
    return f"{s.scheme}://{host}", host, handle


# ---------------------------------------------------------------- one check

def cart_answer(cart: dict, code: str, product: str, available) -> dict:
    dc = next((d for d in cart.get("discount_codes", []) if str(d.get("code", "")).upper() == code.upper()), None)
    apps = ([{"title": a.get("title"), "type": a.get("type"), "value": a.get("value"), "value_type": a.get("value_type"),
              "amount": (a.get("total_allocated_amount") or 0) / 100} for a in cart.get("cart_level_discount_applications", [])]
            + [{"title": (a.get("discount_application") or {}).get("title"), "amount": a["amount"] / 100, "line": True}
               for it in cart.get("items", []) for a in it.get("line_level_discount_allocations", [])])
    return {"product": product, "variant_available": available,
            "applicable": bool(dc and dc.get("applicable")),
            "subtotal": cart["original_total_price"] / 100, "total": cart["total_price"] / 100, "discount": cart["total_discount"] / 100,
            "code_amount": round(sum(a["amount"] for a in apps if (a.get("title") or "").upper() == code.upper()), 2),
            "applications": apps}


def plain_check(host: str, handle: str, code: str, qty: int) -> dict:
    """The plain-HTTP cart check (tools/codecheck.py) against the cart host; HTTP errors come back with their status."""
    try:
        r = codecheck.check(f"https://{host}/products/{handle}", code, qty, wait_on_429=False, pause=REQ_PAUSE_MS / 1000)
    except urllib.error.HTTPError as e:
        try:
            body = e.read()[:200].decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            body = ""
        return {"error": f"HTTP {e.code} {body}", "status": e.code, "retry_after": e.headers.get("Retry-After") if e.headers else None}
    r.pop("code", None)
    r.pop("store", None)
    return r


def run_check(tab: "Tab | None", host: str, handle: str, code: str, qty: int, variants: dict) -> dict:
    if tab is None or host in PLAIN_HTTP:
        return plain_check(host, handle, code, qty)
    # A store that moves the tab off its cart host would make the relative fetches below hit the wrong host.
    origin = tab.eval("location.origin")
    if origin != f"https://{host}":
        return plain_check(host, handle, code, qty)
    cached = variants.get((host, handle))
    if cached and not cached.get("available"):
        return {"soldout": True, "error": "sold out (no available variant)", "product": cached.get("title"),
                "variant_available": False, "network": False}
    tab.fresh_cart(host)
    js = (CHECK_JS.replace("HANDLE", urllib.parse.quote(handle)).replace("QTY", str(int(qty))).replace("PAUSE", str(REQ_PAUSE_MS))
          .replace("CODE", json.dumps(code)).replace("VARIANT", json.dumps(cached)))   # VARIANT last: it holds a product title
    r = tab.eval(js)
    if not isinstance(r, dict):
        return {"error": f"no result ({r!r})"[:300], "transient": True}
    if r.get("variant"):
        variants[(host, handle)] = r.pop("variant")
    if r.get("error"):
        return r
    return cart_answer(r["cart"], code, r["product"], r["variant_available"])


def classify(res: dict) -> str:
    """ok (the store answered: accepted or rejected), rate (429), soldout (the item could not be put in the cart: sold out
    or a quantity limit, so the code is untested), transient (network, 5xx, tab trouble) or error (anything else)."""
    if not res.get("error"):
        return "ok"
    err, status = str(res["error"]), res.get("status")
    if status == 429 or (status is None and re.search(r"\b429\b|Too Many Requests", err[:120])):
        return "rate"
    if res.get("soldout") or status == 422 or re.search(r"\b422\b|sold out", err[:200], re.I):
        return "soldout"
    if res.get("transient") or (isinstance(status, int) and status >= 500) or status is None:
        return "transient"
    return "error"


def retry_after_s(v) -> float | None:
    """Seconds from a Retry-After header (delta-seconds or an HTTP date); None when absent or unreadable."""
    if not v:
        return None
    try:
        return max(0.0, float(v))
    except (TypeError, ValueError):
        pass
    try:
        return max(0.0, (email.utils.parsedate_to_datetime(v) - dt.datetime.now(dt.timezone.utc)).total_seconds())
    except Exception:  # noqa: BLE001
        return None


def sweep(checks: list[dict], out: Path) -> list[dict]:
    """Run every check, stores interleaved, with each store's own pacing (see GAP_PER_STORE and below).

    Every planned check ends as exactly one row: answered (applicable true/false), inconclusive (the store could not
    put the item in the cart), or unanswered (429s or errors until it gave up). Only answered rows count in merge()."""
    by_store: dict[str, list[dict]] = {}
    for ch in checks:
        origin, host, handle = store_of(ch["url"])
        by_store.setdefault(origin, []).append({**ch, "host": host, "handle": handle})
    # the control code first on each store, on its first product (moved to another product if that one is sold out)
    queue: dict[str, list[dict]] = {}
    for origin, items in by_store.items():
        first = items[0]
        queue[origin] = [{**first, "code": CONTROL, "qty": 1, "control": True}] + items
    t0 = time.time()
    state = {o: {"next": 0.0, "gap": STORE_GAP.get(urlsplit(o).netloc, GAP_PER_STORE), "streak": 0} for o in queue}
    tabs: dict[str, Tab | None] = {}
    variants: dict = {}
    soldout_handles: set = set()
    rows, tries = [], {}

    def record(ch: dict, row: dict) -> None:
        if ch.get("control"):
            row["control"] = True
        rows.append(row)
        with open(out, "a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")

    def base_row(ch: dict) -> dict:
        return {"code": ch["code"], "brand": ch["brand"], "url": ch["url"], "qty": ch["qty"], "store": ch["host"],
                "checked_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}

    try:
        for origin in queue:
            tabs[origin] = None if urlsplit(origin).netloc in PLAIN_HTTP else Tab(origin + "/")
            time.sleep(2)
        time.sleep(4)
        while any(queue.values()):
            progressed = False
            for origin, items in queue.items():
                st = state[origin]
                if not items or time.time() < st["next"]:
                    continue
                progressed = True
                if time.time() - t0 > STORE_DEADLINE:
                    log(f"{origin}: still limited {STORE_DEADLINE // 60} min into the sweep; {len(items)} checks left unanswered")
                    for ch in items:
                        record(ch, {**base_row(ch), "error": "unanswered: store deadline passed (rate limited)", "unanswered": True})
                    items.clear()
                    continue
                ch = items.pop(0)
                key = (origin, ch["code"], ch["slug"], ch["qty"], bool(ch.get("control")))
                row = base_row(ch)
                try:
                    res = run_check(tabs[origin], ch["host"], ch["handle"], ch["code"], ch["qty"], variants)
                except Exception as e:  # noqa: BLE001  (tab or socket trouble: reopen the tab and try again)
                    res = {"error": f"{type(e).__name__}: {e}"[:300], "transient": True}
                    if tabs.get(origin) is not None:
                        try:
                            tabs[origin].close()
                        except Exception:  # noqa: BLE001
                            pass
                        try:
                            tabs[origin] = Tab(origin + "/")
                            time.sleep(4)
                        except Exception as e2:  # noqa: BLE001
                            log(f"{origin}: could not reopen the tab ({e2}); plain HTTP from here")
                            tabs[origin] = None
                kind = classify(res)
                now = time.time()
                if res.get("network", True):
                    st["next"] = now + st["gap"]
                if kind == "rate":
                    tries[key] = tries.get(key, 0) + 1
                    st["streak"] += 1
                    ra = retry_after_s(res.get("retry_after"))
                    cool = max(ra or 0.0, min(BACKOFF_BASE * 2 ** (st["streak"] - 1), BACKOFF_MAX))
                    st["next"] = now + cool
                    st["gap"] = min(st["gap"] * 1.5, GAP_MAX)
                    if tries[key] < MAX_TRIES:
                        items.insert(0, ch)
                        log(f"{ch['brand']} {ch['code']} on {ch['slug']}: 429 (try {tries[key]}/{MAX_TRIES}); store cools down "
                            f"{cool:.0f} s" + (f" (Retry-After {res.get('retry_after')})" if ra is not None else "") + f", gap now {st['gap']:.0f} s")
                        continue
                    row.update(error=f"unanswered: 429 on {tries[key]} tries ({str(res['error'])[:200]})", unanswered=True)
                    log(f"{ch['brand']} {ch['code']} on {ch['slug']}: UNANSWERED after {tries[key]} 429s (not a rejection)")
                    record(ch, row)
                    continue
                st["streak"] = 0
                if kind == "transient":
                    tries[key] = tries.get(key, 0) + 1
                    if tries[key] < MAX_TRIES:
                        items.insert(0, ch)
                        log(f"{ch['brand']} {ch['code']} on {ch['slug']}: {str(res['error'])[:120]} (try {tries[key]}/{MAX_TRIES}), retrying")
                        continue
                    row.update(error=f"unanswered: {str(res['error'])[:250]}", unanswered=True)
                    log(f"{ch['brand']} {ch['code']} on {ch['slug']}: UNANSWERED ({str(res['error'])[:120]}; not a rejection)")
                    record(ch, row)
                    continue
                if kind == "soldout":
                    soldout_handles.add((ch["host"], ch["handle"], ch["qty"]))
                    if ch.get("control"):
                        nxt = next((x for x in items if (x["host"], x["handle"], 1) not in soldout_handles and x["handle"] != ch["handle"]), None)
                        if nxt:
                            log(f"{ch['brand']} control: {ch['slug']} could not be put in the cart ({str(res['error'])[:80]}); control moves to {nxt['slug']}")
                            items.insert(0, {**nxt, "code": CONTROL, "qty": 1, "control": True})
                            continue
                    row.update(error=str(res["error"])[:300], inconclusive="the store could not put the item in the cart (sold out or quantity limit); the code is untested on it")
                    log(f"{ch['brand']} {ch['code']} on {ch['slug']} x{ch['qty']}: INCONCLUSIVE, {str(res['error'])[:120]} (not a rejection)")
                    record(ch, row)
                    continue
                if kind == "error":
                    row["error"] = str(res["error"])[:300]
                    log(f"{ch['brand']} {ch['code']} on {ch['slug']}: ERROR {row['error'][:120]} (not a rejection)")
                    record(ch, row)
                    continue
                res = {k: v for k, v in res.items() if k not in ("network", "status", "retry_after")}
                row.update(res)
                price = BY_SLUG[ch["slug"]]["price"]
                if ch["qty"] == 1 and price is not None and abs(res["subtotal"] - price) >= 0.01:
                    row["price_mismatch"] = {"page": price, "store": res["subtotal"]}
                    log(f"PRICE MISMATCH {ch['slug']}: page ${price:.2f}, store cart ${res['subtotal']:.2f} (fix in the weekly price check, DLC-9)")
                log(f"{ch['brand']} {ch['code']} on {ch['slug']} x{ch['qty']}: "
                    + (f"accepted, ${res['code_amount']:.2f} off ${res['subtotal']:.2f}" if res["applicable"] else f"rejected (subtotal ${res['subtotal']:.2f})"))
                record(ch, row)
            if not progressed:
                time.sleep(1)
    finally:
        for t in tabs.values():
            if t is not None:
                t.close()
    log(f"sweep took {(time.time() - t0) / 60:.0f} min")
    return rows


# ---------------------------------------------------------------- merge with the two-strikes rule

def merge(rows: list[dict], log_path: Path, today: str) -> dict:
    data = json.load(open(COUPONS, encoding="utf-8"))
    by_key = {(c["brand"], c["code"]): c for c in data["codes"]}
    # Stores whose control code was accepted (or never answered) prove nothing: drop their rows.
    bad_stores = set()
    for r in rows:
        if r.get("control") and (r.get("error") or r.get("applicable")):
            bad_stores.add(r["store"])
            log(f"control code not rejected on {r['store']} ({r.get('error') or 'accepted'}); that store's checks are discarded")
    usable = [r for r in rows if not r.get("control") and r["store"] not in bad_stores and not r.get("error")]
    # Two strikes: a code that was rejected on every product today keeps its last passing tests this once. A strike
    # needs a complete answer: every product the code was planned on either answered (rejected) or could not be put in
    # the cart (sold out / quantity limit, which tests nothing). If any of its checks went unanswered (429s, errors),
    # nothing changes for that code today, no strike and no new tests: on 2026-10-23 BULKRATE took a strike from one
    # real rejection while its other four products had all 429'd.
    held, incomplete = [], []
    for (brand, code), c in by_key.items():
        mine = [r for r in usable if r["brand"] == brand and r["code"] == code]
        if not mine:
            continue
        if any(r["applicable"] for r in mine):
            c.pop("fail_streak", None)
            continue
        open_ = [r for r in rows if not r.get("control") and r["store"] not in bad_stores and r["brand"] == brand
                 and r["code"] == code and r.get("error") and not r.get("inconclusive")]
        if open_:
            incomplete.append((brand, code))
            log(f"{brand} {code}: rejected on {len(mine)} product(s), {len(open_)} unanswered (429 or error); no strike, "
                f"kept as it was (fail_streak {int(c.get('fail_streak') or 0)})")
            continue
        streak = int(c.get("fail_streak") or 0) + 1
        c["fail_streak"] = streak
        c["last_failed_at"] = today
        if streak < 2:
            held.append((brand, code))
            log(f"{brand} {code}: rejected on every product today (strike {streak}); kept with its last passing date, retired on a second strike")
        else:
            log(f"{brand} {code}: rejected on every product for the second sweep in a row; retired")
    kept_rows = [r for r in usable if (r["brand"], r["code"]) not in held and (r["brand"], r["code"]) not in incomplete]
    # codes_merge rebuilds each code's tests from a log file: write the rows it should see.
    merge_log = log_path.with_suffix(".merge.jsonl")
    with open(merge_log, "w", encoding="utf-8") as f:
        for r in kept_rows:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
    # Persist the strike bookkeeping before codes_merge rewrites the file (it keeps unknown fields per code).
    with open(COUPONS, "w", encoding="utf-8") as f:
        f.write('{\n "_notes": ' + json.dumps(data["_notes"], ensure_ascii=False) + ',\n "checked": ' + json.dumps(data["checked"]) + ',\n "codes": [\n')
        f.write(",\n".join("  " + json.dumps(c, ensure_ascii=False) for c in data["codes"]) + "\n ]\n}\n")
    if kept_rows:
        codes_merge.main([str(merge_log)])
    merge_log.unlink(missing_ok=True)
    data = json.load(open(COUPONS, encoding="utf-8"))
    if usable:
        data["checked"] = max(r["checked_at"][:10] for r in usable)
    with open(COUPONS, "w", encoding="utf-8") as f:
        f.write('{\n "_notes": ' + json.dumps(data["_notes"], ensure_ascii=False) + ',\n "checked": ' + json.dumps(data["checked"]) + ',\n "codes": [\n')
        f.write(",\n".join("  " + json.dumps(c, ensure_ascii=False) for c in data["codes"]) + "\n ]\n}\n")
    return {"usable": len(usable), "bad_stores": sorted(bad_stores), "held": held, "incomplete": incomplete,
            "unanswered": sum(1 for r in rows if not r.get("control") and r.get("error") and not r.get("inconclusive")),
            "inconclusive": sum(1 for r in rows if not r.get("control") and r.get("inconclusive")),
            "accepted": sum(r["applicable"] for r in usable), "rejected": sum(not r["applicable"] for r in usable),
            "mismatch": sorted({f"{r['url'].rsplit('/', 1)[-1]}: page ${r['price_mismatch']['page']:.2f} vs store ${r['price_mismatch']['store']:.2f}"
                                for r in usable if r.get("price_mismatch")})}


# ---------------------------------------------------------------- publish

def sh(cmd: list[str], **kw) -> subprocess.CompletedProcess:
    log("$ " + " ".join(cmd))
    return subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True, **kw)


def publish(today: str, summary: dict, push: bool, deploy: bool) -> None:
    before = (ROOT / "worker" / "src" / "links-map.json").read_bytes()
    r = sh([sys.executable, "src/build.py"])
    if r.returncode != 0:
        raise SystemExit(f"build failed: {r.stderr[-800:]}")
    log(r.stdout.strip().splitlines()[-1])
    map_changed = (ROOT / "worker" / "src" / "links-map.json").read_bytes() != before
    st = sh(["git", "status", "--porcelain", "--", "src/coupons.json", "docs", "worker/src/links-map.json", "growth/codes"]).stdout
    if not st.strip():
        log("nothing changed; no commit")
        return
    if not push:
        log("changes left uncommitted (--no-push)")
        return
    sh(["git", "add", "src/coupons.json", "docs", "worker/src/links-map.json", "growth/codes"])
    msg = (f"codes: daily cart check {today}\n\n{summary['accepted']} checks accepted, {summary['rejected']} rejected"
           + (f"; held on a first strike: {', '.join(c for _, c in summary['held'])}" if summary["held"] else "")
           + (f"; {summary['unanswered']} unanswered (429 or error, not rejections)" if summary.get("unanswered") else "")
           + (f"; {summary['inconclusive']} inconclusive (sold out or quantity limit)" if summary.get("inconclusive") else "")
           + (f"; unchanged for lack of answers: {', '.join(c for _, c in summary['incomplete'])}" if summary.get("incomplete") else "")
           + (f"; stores discarded (control not rejected): {', '.join(summary['bad_stores'])}" if summary["bad_stores"] else "")
           + (f"; PRICE MISMATCH for the weekly check: {'; '.join(summary['mismatch'])}" if summary.get("mismatch") else "")
           + ". Run by tools/codesweep.py through the agent's Chrome.\n\nCo-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>")
    r = sh(["git", "commit", "-q", "-m", msg])
    if r.returncode != 0:
        raise SystemExit(f"commit failed: {r.stderr[-400:]}")
    r = sh(["git", "push", "-q", "origin", "HEAD:main"])
    if r.returncode != 0:
        raise SystemExit(f"push failed: {r.stderr[-400:]}")
    log("pushed")
    if map_changed and deploy:
        tok = subprocess.run(["security", "find-generic-password", "-a", "dealectric", "-s", "cloudflare-workers-token", "-w"],
                             capture_output=True, text=True).stdout.strip()
        if not tok:
            log("Worker link map changed but no Cloudflare token in the keychain; deploy by hand")
        else:
            r = subprocess.run(["npx", "--yes", "wrangler", "deploy"], cwd=ROOT / "worker", text=True, capture_output=True,
                               env={**os.environ, "CLOUDFLARE_API_TOKEN": tok})
            log("worker deployed" if r.returncode == 0 else f"worker deploy failed: {(r.stderr or r.stdout)[-400:]}")
    changed_pages = [l.split()[-1] for l in st.splitlines() if l.split()[-1].startswith("docs/") and l.split()[-1].endswith(".html")]
    urls = ["https://dealectric.com/" + p[len("docs/"):-len(".html")].replace("index", "") for p in changed_pages]
    if urls:
        time.sleep(90)   # let GitHub Pages publish before IndexNow fetches
        r = sh([sys.executable, "tools/indexnow.py", *urls[:200]])   # indexnow.py brings its own CA bundle (certifi or macOS's)
        log("indexnow: " + (r.stdout or r.stderr).strip()[-200:])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-push", action="store_true", help="check, merge and rebuild, but do not commit or push")
    ap.add_argument("--no-deploy", action="store_true", help="never run wrangler deploy")
    ap.add_argument("--brand", default=None, help="only this brand (testing)")
    args = ap.parse_args()
    today = dt.datetime.now(dt.timezone.utc).date().isoformat()   # UTC, like the checked_at stamps and the build
    data = json.load(open(COUPONS, encoding="utf-8"))
    codes = live_published(data["codes"], today)
    if args.brand:
        codes = [c for c in codes if c["brand"].lower() == args.brand.lower()]
    checks = plan_checks(codes)
    log(f"{len(codes)} published codes, {len(checks)} checks across {len({store_of(c['url'])[1] for c in checks})} stores")
    if args.dry_run:
        for ch in checks:
            print(f"  {ch['brand']:10s} {ch['code']:12s} x{ch['qty']} {ch['slug']}")
        return 0
    if not browser_ok():
        raise SystemExit("no browser on localhost:9222; start it: uv --directory ~/Desktop/agent-vault run agent-vault browser")
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    out = LOG_DIR / f"{today}-checks.jsonl"
    rows = sweep(checks, out)
    summary = merge(rows, out, today)
    log(f"merged: {summary}")
    publish(today, summary, push=not args.no_push, deploy=not args.no_deploy)
    return 0


if __name__ == "__main__":
    sys.exit(main())
