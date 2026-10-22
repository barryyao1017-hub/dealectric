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
(result rejected, so it leaves every page and offers.json); a 429 or a network error is never a rejection. No order
is ever placed and no personal data entered.

    python3.12 tools/codesweep.py                 # check, merge, rebuild, commit, push, deploy if needed
    python3.12 tools/codesweep.py --dry-run       # list the checks
    python3.12 tools/codesweep.py --no-push       # check, merge, rebuild; leave the commit to you

Scheduled daily by ~/Library/LaunchAgents/com.jiayiyao.dealectric.codesweep.plist via tools/codesweep.sh.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import math
import os
import subprocess
import sys
import time
import urllib.parse
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

import websocket  # websocket-client (python3.12 -m pip install --user websocket-client)

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))
from products import PRODUCTS, VERIFIED  # noqa: E402
import codes_merge  # noqa: E402

CDP = "http://localhost:9222"
COUPONS = ROOT / "src" / "coupons.json"
LOG_DIR = ROOT / "growth" / "codes"
CONTROL = "ZZNOTACODE7Q"
GAP_PER_STORE = 14.0     # seconds between two cart calls on the same store (Shopify 429s a burst from one client)
RETRY_WAIT = 90          # after a 429
# Where a brand's cart lives when it is not the host in products.py (Soundcore's US cart is us.soundcore.com).
CART_HOST = {"www.soundcore.com": "us.soundcore.com"}
BY_SLUG = {p["slug"]: p for p in PRODUCTS}

CHECK_JS = r"""
(async () => {
  const H = {'Content-Type': 'application/json', 'Accept': 'application/json'};
  const j = async (u, o) => { const r = await fetch(u, Object.assign({credentials: 'same-origin'}, o || {}));
    const t = await r.text(); let b = null; try { b = JSON.parse(t); } catch (e) {} return {status: r.status, body: b, text: t.slice(0, 200)}; };
  const prod = await j(`/products/${HANDLE}.js`);
  if (prod.status !== 200 || !prod.body) return {error: `product ${prod.status} ${prod.text}`};
  const v = prod.body.variants.find(x => x.available) || prod.body.variants[0];
  await j('/cart/clear.js', {method: 'POST', headers: H});
  await j('/cart/update.js', {method: 'POST', headers: H, body: JSON.stringify({discount: ''})});
  const add = await j('/cart/add.js', {method: 'POST', headers: H, body: JSON.stringify({items: [{id: v.id, quantity: QTY}]})});
  if (add.status >= 400) return {error: `add ${add.status} ${add.text}`, status: add.status};
  const upd = await j('/cart/update.js', {method: 'POST', headers: H, body: JSON.stringify({discount: CODE})});
  if (upd.status >= 400) return {error: `update ${upd.status} ${upd.text}`, status: upd.status};
  const cart = await j('/cart.js');
  if (cart.status !== 200 || !cart.body) return {error: `cart ${cart.status} ${cart.text}`, status: cart.status};
  await j('/cart/update.js', {method: 'POST', headers: H, body: JSON.stringify({discount: ''})});
  await j('/cart/clear.js', {method: 'POST', headers: H});
  return {product: prod.body.title, variant_available: !!v.available, cart: cart.body};
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

def run_check(tab: Tab, host: str, handle: str, code: str, qty: int) -> dict:
    tab.fresh_cart(host)
    js = CHECK_JS.replace("HANDLE", json.dumps(handle)).replace("QTY", str(qty)).replace("CODE", json.dumps(code))
    js = js.replace("`/products/${" + json.dumps(handle) + "}.js`", "`/products/" + handle + ".js`")
    r = tab.eval(js)
    if not isinstance(r, dict):
        return {"error": f"no result ({r!r})"}
    if r.get("error"):
        return r
    cart = r["cart"]
    dc = next((d for d in cart.get("discount_codes", []) if str(d.get("code", "")).upper() == code.upper()), None)
    apps = ([{"title": a.get("title"), "type": a.get("type"), "value": a.get("value"), "value_type": a.get("value_type"),
              "amount": (a.get("total_allocated_amount") or 0) / 100} for a in cart.get("cart_level_discount_applications", [])]
            + [{"title": (a.get("discount_application") or {}).get("title"), "amount": a["amount"] / 100, "line": True}
               for it in cart.get("items", []) for a in it.get("line_level_discount_allocations", [])])
    return {"product": r["product"], "variant_available": r["variant_available"],
            "applicable": bool(dc and dc.get("applicable")),
            "subtotal": cart["original_total_price"] / 100, "total": cart["total_price"] / 100, "discount": cart["total_discount"] / 100,
            "code_amount": round(sum(a["amount"] for a in apps if (a.get("title") or "").upper() == code.upper()), 2),
            "applications": apps}


def sweep(checks: list[dict], out: Path) -> list[dict]:
    """Run every check, one tab per store, round-robin across stores with GAP_PER_STORE between a store's calls."""
    by_store: dict[str, list[dict]] = {}
    for ch in checks:
        origin, host, handle = store_of(ch["url"])
        by_store.setdefault(origin, []).append({**ch, "host": host, "handle": handle})
    # the control code first on each store, on its first product
    queue: dict[str, list[dict]] = {}
    for origin, items in by_store.items():
        first = items[0]
        queue[origin] = [{**first, "code": CONTROL, "qty": 1, "control": True}] + items
    tabs: dict[str, Tab] = {}
    last_call: dict[str, float] = {}
    rows, retried = [], set()
    try:
        for origin in queue:
            tabs[origin] = Tab(origin + "/")
            time.sleep(2)
        time.sleep(4)
        while any(queue.values()):
            progressed = False
            for origin, items in queue.items():
                if not items:
                    continue
                wait = GAP_PER_STORE - (time.time() - last_call.get(origin, 0))
                if wait > 0:
                    continue
                ch = items.pop(0)
                progressed = True
                last_call[origin] = time.time()
                row = {"code": ch["code"], "brand": ch["brand"], "url": ch["url"], "qty": ch["qty"], "store": ch["host"],
                       "checked_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")}
                try:
                    res = run_check(tabs[origin], ch["host"], ch["handle"], ch["code"], ch["qty"])
                except Exception as e:  # noqa: BLE001
                    res = {"error": f"{type(e).__name__}: {e}"[:300]}
                if res.get("error"):
                    row["error"] = res["error"]
                    key = (origin, ch["code"], ch["slug"], ch["qty"])
                    if (res.get("status") == 429 or "429" in res["error"]) and key not in retried:
                        retried.add(key)
                        items.append(ch)                    # requeue once, after a longer pause
                        last_call[origin] = time.time() + RETRY_WAIT - GAP_PER_STORE
                        log(f"{ch['brand']} {ch['code']} on {ch['slug']}: 429, requeued")
                        continue
                    log(f"{ch['brand']} {ch['code']} on {ch['slug']}: ERROR {res['error'][:120]}")
                else:
                    row.update(res)
                    log(f"{ch['brand']} {ch['code']} on {ch['slug']} x{ch['qty']}: "
                        + (f"accepted, ${res['code_amount']:.2f} off ${res['subtotal']:.2f}" if res["applicable"] else f"rejected (subtotal ${res['subtotal']:.2f})"))
                if ch.get("control"):
                    row["control"] = True
                rows.append(row)
                with open(out, "a", encoding="utf-8") as f:
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
            if not progressed:
                time.sleep(1)
    finally:
        for t in tabs.values():
            t.close()
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
    # Two strikes: a code that was rejected on every product today keeps its last passing tests this once.
    held = []
    for (brand, code), c in by_key.items():
        mine = [r for r in usable if r["brand"] == brand and r["code"] == code]
        if not mine:
            continue
        if any(r["applicable"] for r in mine):
            c.pop("fail_streak", None)
            continue
        streak = int(c.get("fail_streak") or 0) + 1
        c["fail_streak"] = streak
        c["last_failed_at"] = today
        if streak < 2:
            held.append((brand, code))
            log(f"{brand} {code}: rejected on every product today (strike {streak}); kept with its last passing date, retired on a second strike")
        else:
            log(f"{brand} {code}: rejected on every product for the second sweep in a row; retired")
    kept_rows = [r for r in usable if (r["brand"], r["code"]) not in held]
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
    return {"usable": len(usable), "bad_stores": sorted(bad_stores), "held": held,
            "accepted": sum(r["applicable"] for r in usable), "rejected": sum(not r["applicable"] for r in usable)}


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
           + (f"; stores discarded (control not rejected): {', '.join(summary['bad_stores'])}" if summary["bad_stores"] else "")
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
        r = sh([sys.executable, "tools/indexnow.py", *urls[:200]])
        log("indexnow: " + (r.stdout or r.stderr).strip()[-200:])


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--no-push", action="store_true", help="check, merge and rebuild, but do not commit or push")
    ap.add_argument("--no-deploy", action="store_true", help="never run wrangler deploy")
    ap.add_argument("--brand", default=None, help="only this brand (testing)")
    args = ap.parse_args()
    today = dt.date.today().isoformat()
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
