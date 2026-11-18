#!/usr/bin/env python3.12
"""Check that every product link still lands on its product, and that /go/<slug> still sends shoppers there (DLC-35).

The CJ/Awin deep link renews itself: src/build.py rebuilds it from the record's `url` on every build. What nothing
caught before this script is a store that moves, redirects, 404s or delists the product page behind that `url`, and a
Worker that sends /go/<slug> somewhere other than the link map says. For every catalog product (src/products.py; retired
slugs are not in PRODUCTS) this script

  1. GETs the record's `url` as a browser would (browser User-Agent, cookie jar, redirects followed, 30 s timeout) and
     records the status, the number of redirects and the final URL;
  2. on a Shopify store, reads `<product URL without query>.js` (the store's public product JSON; Soundcore's lives on
     us.soundcore.com, as in CART_HOST in tools/codesweep.py) for whether the variant is available; elsewhere (Tenergy's
     BigCommerce) it reads the schema.org availability on the page itself;
  3. requests https://dealectric.com/go/<slug> without following the redirect and checks that the Location header is the
     deep link in worker/src/links-map.json with the Worker's sub-ID (<slug>.<click id>) in it, in the network's own
     sub-ID parameter (CJ sid, Awin clickref, Rakuten u1).

Findings: BROKEN (404/410, any other 4xx or a 5xx that repeats, a redirect loop, a "not found" page served as a 200),
MOVED (the final URL is on another path or another host; the query string and a trailing slash are ignored, a Shopify
product keeps its handle wherever /products/<handle> sits, and www.soundcore.com / us.soundcore.com and www./bare are
the same host), DELISTED (it lands on the store's home, a collection, search or pages URL, or the store's product JSON
no longer has the variant or the handle), SOLD OUT (the record's variant is not available, matched as tools/pricecheck.py
matches it, while the record does not say in_stock False;
already recorded sold-outs are listed, not flagged), BACK IN STOCK (the record says in_stock False, the store has stock),
THROTTLED (the store answered 429 and r.jina.ai could not read the URL either: "throttled, not checked", never counted
as broken), UNANSWERED (bot challenge or network error after one retry, never counted as broken; a store that answers a
challenge to both tries gets no more requests that run, and its other products are unanswered), GO (the Worker's answer
does not match the link map), MAP (links-map.json is missing the product or names another merchant URL than products.py).

Throttling (DLC-306: after the daily sweeps the stores answer this script with 429s). Requests are spread: each one goes
to the store that has waited longest (spread()), never sooner than GAP / STORE_GAP after the last request to that store,
so a slow store holds up only its own products. A 429 is not waited out: the URL is read through https://r.jina.ai/<url>
instead (pricecheck.jina(), which reports the store's own status and the final URL), and so are that store's next
requests until its Retry-After has passed; a second 429 after that sends the rest of its requests there for the run.
r.jina.ai answers 20 requests a minute, so those reads are paced at JINA_GAP. /go/ links are never read through
r.jina.ai (it would follow the redirect, which is a click); a 429 from the Worker is "throttled, not checked" too.

A record with `cart_variant` (DLC-71: the AC200L, whose product page sells nothing) has its /go/ link pointed at the
store's cart permalink; step 2 then reads that variant's availability, so SOLD OUT or DELISTED marks the day the cart
link stops working.

It never edits products.py (the weekly price check, DLC-9, applies fixes), never calls a cart endpoint and never follows
a CJ/Awin click URL (that would count as a click). Each /go/ request logs one row in our own D1 clicks table: the
User-Agent below contains "bot", so the Worker stores it with bot_like=1 (worker/src/index.js looksLikeBot()), which the
click counts in worker/README.md leave out, and it matches none of the AI fetcher patterns, so the Worker answers with its
302 rather than the text page. The X-Dealectric-Check header is sent too, but the Worker does not store request headers;
the user_agent column is what identifies these rows.

Writes growth/codes/<date>-links.json (one row per product, plus the findings and the one-line summary the daily sweep
puts in its commit message) and prints one line per finding. Exits 0 with findings; non-zero only on a crash.

    python3.12 tools/linkcheck.py               # check everything, write growth/codes/<UTC date>-links.json
    python3.12 tools/linkcheck.py --dry-run     # list what it would request
    python3.12 tools/linkcheck.py --slug bluetti-ac180 --out /tmp/x.json   # a few products, elsewhere (testing)

Run daily by tools/codesweep.py after the cart checks (in its own process, 15 min timeout).
"""
from __future__ import annotations

import argparse
import collections
import datetime as dt
import http.client
import http.cookiejar
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))
from products import PRODUCTS, RETIRED  # noqa: E402
import codecheck  # noqa: E402  (its browser User-Agent and the CA bundle python.org's Python needs on this Mac)
import pricecheck  # noqa: E402  (jina(): the read through r.jina.ai the price check falls back to on a 429)

LINKS_MAP = ROOT / "worker" / "src" / "links-map.json"
OUT_DIR = ROOT / "growth" / "codes"
SITE_HOST = "dealectric.com"
UA = codecheck.UA
CHECK_UA = "Mozilla/5.0 (compatible; dealectric-linkcheck-bot/1.0)"   # "bot" -> bot_like=1 in D1; no AI_UA match -> a 302
TIMEOUT = 30
GAP = 3.0                 # seconds between two requests to one store (pages and product JSON alike)
# Slower stores. ALLPOWERS and Soundcore were quickest to 429 in tools/codesweep.py. BLUETTI answered this script's
# urllib GETs with 429 Retry-After 60 at about 6 s apart on 2026-10-28 (4 pages answered, then the store was held);
# 20 s is a guess not yet confirmed by a run.
STORE_GAP = {"iallpowers.com": 6.0, "soundcore.com": 6.0, "bluettipower.com": 20.0}
# Tenergy (power.tenergy.com) answers every non-browser client with a Cloudflare challenge (403, cf-mitigated:
# challenge): its products come back unanswered every run. This script does not try to get past the challenge.
GO_GAP = 1.0              # between two /go/ requests to our own Worker
RETRY_WAIT = 10.0         # before the one retry after a network error or a 5xx
RETRY_AFTER_MAX = 60.0    # longest Retry-After honoured before the one direct retry after a 429 (r.jina.ai reads meanwhile)
JINA_KEY = "r.jina.ai"
JINA_GAP = 3.5            # seconds between two reads through r.jina.ai (20 requests a minute without a key)
JINA_FAILS_MAX = 3        # reads in a row r.jina.ai could not make before it gets no more requests this run
NOT_CHECKED = "throttled, not checked"
DEADLINE = 12 * 60        # seconds; past this every remaining request is left unanswered (the sweep kills us at 15 min)
MAX_BODY = 3_000_000
# Where a store's Shopify product JSON lives when it is not the product page's host (CART_HOST in tools/codesweep.py:
# www.soundcore.com is a non-Shopify front end whose /products/<handle>.js is its 404 page).
JSON_HOST = {"www.soundcore.com": "us.soundcore.com"}
SAME_HOST = [{"www.soundcore.com", "us.soundcore.com"}]
# Stores with /products/<handle> pages but no Shopify product JSON at all (<page>.js is a 404 while the page answers 200):
# stock comes from the page's schema.org availability, and the missing JSON is not read as "delisted" (Creality, 2026-11-17).
NO_JSON = {"store.creality.com"}
# CJ, Awin and Rakuten click hosts: never requested, never followed (a request there is a click on our account).
AFFILIATE = re.compile(r"(^|\.)(tkqlhce|anrdoezrs|dpbolvw|jdoqocy|kqzyfj|qksrv|emjcd|awin1|awin|zenaps|linksynergy)\.(com|net)$", re.I)
# The query parameter each network carries our sub-ID in, as worker/src/index.js sets it; any other network is Awin's.
SUB_KEY = {"cj": "sid", "rakuten": "u1"}
LISTING = re.compile(r"^(/[a-z]{2}(-[a-z]{2})?)?(/(collections|collection|products|search|pages|shop|category|categories|catalog)(/.*)?)?$", re.I)
NOT_FOUND_TITLE = re.compile(r"<title[^>]*>[^<]*(\b404\b|not found|page not found|no longer available)[^<]*</title>", re.I)
AVAIL = re.compile(r"schema\.org/(InStock|OutOfStock|SoldOut|Discontinued|PreOrder|PreSale|BackOrder|LimitedAvailability|OnlineOnly|InStoreOnly)", re.I)
BRAND = {p["slug"]: p["brand"] for p in PRODUCTS}
CHALLENGE = re.compile(r"Just a moment\.\.\.|challenge-platform|cf-chl-|Attention Required! \| Cloudflare|captcha", re.I)


class Refused(Exception):
    """A URL this script must not request: an affiliate click host or a cart endpoint."""


def guard(url: str) -> None:
    s = urlsplit(url)
    if AFFILIATE.search(s.hostname or ""):
        raise Refused(f"not followed: {s.hostname} is a CJ/Awin/Rakuten click host (a request there counts as a click)")
    if re.search(r"/cart(\.js|/|$)", s.path):
        raise Refused(f"not requested: {s.path} is a cart endpoint")


def now_utc() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def store_key(host: str) -> str:
    """The store a host belongs to, for pacing: its last two labels (us.soundcore.com and www.soundcore.com are one store)."""
    return ".".join((host or "").lower().split(".")[-2:])


def norm_host(host: str) -> str:
    h = (host or "").lower()
    for pair in SAME_HOST:
        if h in pair:
            return min(pair)
    return h[4:] if h.startswith("www.") else h


def handle_of(path: str) -> str | None:
    """The Shopify product handle in a path (/products/<h>, /collections/x/products/<h>, /en-us/products/<h>), else None."""
    m = re.search(r"/products/([^/?#]+)", path or "")
    return urllib.parse.unquote(m.group(1)).lower() if m else None


def norm_path(path: str) -> str:
    return urllib.parse.unquote(path or "").rstrip("/").lower()


def variant_of(url: str) -> int | None:
    v = urllib.parse.parse_qs(urlsplit(url).query).get("variant", [""])[0]
    return int(v) if v.isdigit() else None


class Pacer:
    """At least GAP (or the store's STORE_GAP) seconds between the end of one request to a store and the next."""

    def __init__(self):
        self.last: dict[str, float] = {}

    def wait(self, key: str, gap: float) -> None:
        t = self.last.get(key)
        if t is not None and (d := t + gap - time.monotonic()) > 0:
            time.sleep(d)

    def done(self, key: str) -> None:
        self.last[key] = time.monotonic()

    def ready_at(self, key: str, gap: float) -> float:
        """The monotonic time from which a request to this store does not have to wait (0.0: never requested)."""
        t = self.last.get(key)
        return 0.0 if t is None else t + gap


class _Hops(urllib.request.HTTPRedirectHandler):
    """Follows redirects like the default handler, records each hop, and refuses affiliate hosts and cart URLs."""

    def __init__(self):
        super().__init__()
        self.hops: list[dict] = []

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        guard(newurl)
        self.hops.append({"status": code, "to": newurl})
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def fetch(url: str, jar, accept: str) -> dict:
    """One GET with redirects followed. Never raises for HTTP or network trouble; the answer says what happened."""
    hops = _Hops()
    op = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(jar),
                                     urllib.request.HTTPSHandler(context=codecheck._CTX), hops)
    req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept": accept, "Accept-Language": "en-US,en;q=0.9"})
    out = {"url": url, "status": None, "final_url": url, "redirects": 0, "hops": hops.hops, "body": "", "error": None}
    try:
        guard(url)
        with op.open(req, timeout=TIMEOUT) as r:
            out.update(status=r.status, final_url=r.geturl(), body=r.read(MAX_BODY).decode("utf-8", "replace"),
                       content_type=r.headers.get("Content-Type", ""))
    except Refused as e:
        out.update(error=str(e), refused=True)
    except urllib.error.HTTPError as e:
        try:
            body = e.read(MAX_BODY).decode("utf-8", "replace")
        except Exception:  # noqa: BLE001
            body = ""
        h = e.headers or {}
        out.update(status=e.code, final_url=e.geturl() or url, body=body, error=f"HTTP {e.code}",
                   retry_after=h.get("Retry-After"), challenged=bool(h.get("cf-mitigated") or (e.code in (403, 503) and CHALLENGE.search(body[:20000]))))
    except (urllib.error.URLError, http.client.HTTPException, OSError, ValueError) as e:
        out.update(error=f"{type(e).__name__}: {getattr(e, 'reason', e)}"[:300], network=True)
    out["redirects"] = len(hops.hops)
    return out


def retry_after_s(v) -> float:
    try:
        return max(0.0, float(v))
    except (TypeError, ValueError):
        return 20.0


class Client:
    def __init__(self, deadline: float):
        self.jar = http.cookiejar.CookieJar()
        self.pacer = Pacer()
        self.deadline = deadline
        self.requests = 0
        self.jina_requests = 0
        self.held: dict[str, str] = {}        # store -> why its remaining requests are not sent (bot challenge twice)
        self.throttled: dict[str, dict] = {}  # store -> {"why", "strikes", "retry_at"}: it answered 429, r.jina.ai reads it
        self.jina_fails = 0                   # reads in a row r.jina.ai could not make
        self.jina_off: str | None = None      # why r.jina.ai gets no more requests this run

    def _via_jina(self, key: str) -> bool:
        """This store's next request goes through r.jina.ai: it answered 429 and its Retry-After has not passed, or it
        answered 429 again after that."""
        t = self.throttled.get(key)
        return bool(t) and (t["strikes"] >= 2 or time.monotonic() < t["retry_at"])

    def ready_at(self, url: str | None) -> float:
        """When the next request for this URL can go out without waiting (for spread()); 0.0 when nothing would be sent."""
        if not url:
            return 0.0
        key = store_key(urlsplit(url).hostname or "")
        if key in self.held:
            return 0.0
        if self._via_jina(key):
            return self.pacer.ready_at(JINA_KEY, JINA_GAP)
        return self.pacer.ready_at(key, STORE_GAP.get(key, GAP))

    def get(self, url: str, accept: str, kind: str = "page") -> dict:
        """One answer for `url` (kind "page" or "json"): from the store, paced per store, or, once the store has answered
        429, through r.jina.ai. A 429 is never the answer by itself: if r.jina.ai cannot read the URL either the answer
        carries `throttled` ("throttled, not checked: ..."), which no verdict counts as broken."""
        key = store_key(urlsplit(url).hostname or "")
        if not self._via_jina(key):
            r = self._direct(url, accept, key)
            if r["status"] != 429:
                return r
            t = self.throttled.setdefault(key, {"strikes": 0})
            t["strikes"] += 1
            t["retry_at"] = time.monotonic() + min(retry_after_s(r.get("retry_after")), RETRY_AFTER_MAX)
            t["why"] = f"{key} answered 429 (Retry-After {r.get('retry_after')})"
        return self._jina(url, kind, self.throttled[key]["why"])

    def _direct(self, url: str, accept: str, key: str) -> dict:
        """fetch() paced per store, with one retry after a bot challenge, a network error or a 5xx. A 429 comes back at
        once (get() reads the URL through r.jina.ai instead of waiting out the Retry-After). A store that answers a bot
        challenge to both tries gets no more requests this run: the rest of its products are left unanswered rather than
        retried into a longer block (2026-10-28: Tenergy answers urllib with a Cloudflare challenge)."""
        gap = STORE_GAP.get(key, GAP)
        r = None
        for attempt in (1, 2):
            if time.monotonic() > self.deadline or key in self.held:
                why = self.held.get(key) or f"run deadline ({DEADLINE // 60} min) passed"
                return {"url": url, "status": None, "final_url": url, "redirects": 0, "hops": [], "body": "",
                        "error": f"not requested: {why}", "network": True}
            self.pacer.wait(key, gap)
            r = fetch(url, self.jar, accept)
            self.pacer.done(key)
            self.requests += 1
            if attempt == 2 or r.get("refused") or r["status"] == 429:
                break
            if r.get("network") or r.get("challenged") or (r["status"] or 0) >= 500:
                time.sleep(RETRY_WAIT)
            else:
                break
        if r.get("challenged"):
            self.held[key] = f"{key} answered a Cloudflare bot challenge (HTTP {r['status']}) to both tries on {url}"
        return r

    def _jina(self, url: str, kind: str, why: str) -> dict:
        """The same answer shape as fetch(), read through r.jina.ai (up to two tries): the store's own status and final
        URL as r.jina.ai reports them, and the page's HTML or the product JSON's text. `throttled` when it cannot be read."""
        out = {"url": url, "status": None, "final_url": url, "redirects": 0, "hops": [], "body": "", "error": None, "via": JINA_KEY}
        try:
            guard(url)
        except Refused as e:
            return {**out, "error": str(e), "refused": True}

        def not_checked(detail: str) -> dict:
            return {**out, "status": 429, "error": "HTTP 429", "throttled": f"{NOT_CHECKED}: {why}; {detail}"}

        data, code = None, 0
        for attempt in (1, 2):
            if self.jina_off:
                return not_checked(self.jina_off)
            if time.monotonic() > self.deadline:
                return not_checked(f"run deadline ({DEADLINE // 60} min) passed before the r.jina.ai read")
            self.pacer.wait(JINA_KEY, JINA_GAP * attempt)   # the retry waits twice as long
            code, body = pricecheck.jina(url, "html" if kind == "page" else "text", meta=True)
            self.pacer.done(JINA_KEY)
            self.jina_requests += 1
            try:
                data = json.loads(body).get("data") if code == 200 else None
            except (ValueError, AttributeError):
                data = None
            if isinstance(data, dict):
                break
            data = None
        if data is None:
            self.jina_fails += 1
            if self.jina_fails >= JINA_FAILS_MAX:
                self.jina_off = f"r.jina.ai could not read {JINA_FAILS_MAX} URLs in a row (last: HTTP {code}); not asked again this run"
            return not_checked(f"r.jina.ai could not read it (HTTP {code})")
        self.jina_fails = 0
        st = data.get("httpStatus") if isinstance(data.get("httpStatus"), int) else 200
        if st == 429:
            return not_checked("the store answered r.jina.ai with a 429 too")
        text = str(data.get("html") or data.get("text") or data.get("content") or "")[:MAX_BODY]
        if kind == "json" and (i := text.find("{")) > 0:
            text = text[i:]
        out.update(status=st, final_url=data.get("finalUrl") or data.get("url") or url, body=text)
        if st >= 400:
            out.update(error=f"HTTP {st}", challenged=bool(st in (403, 503) and CHALLENGE.search(text[:20000])))
        return out


# ---------------------------------------------------------------- one product

def throttled_reason(r: dict) -> str | None:
    """The "throttled, not checked: ..." detail when all a request got is a 429 with no r.jina.ai read, else None."""
    if r.get("throttled"):
        return r["throttled"]
    return f"{NOT_CHECKED}: HTTP 429" if r.get("status") == 429 else None


def unanswered_reason(r: dict) -> str | None:
    """Why a request told us nothing about the link (bot challenge, network, refused), else None. A 429 is
    throttled_reason()'s, checked first by every caller."""
    if r.get("refused"):
        return r["error"]
    if r.get("challenged"):
        return f"HTTP {r['status']} bot challenge (Cloudflare)" + (" answered to r.jina.ai" if r.get("via") else " twice")
    if r.get("network"):
        return r["error"]
    return None


def judge_page(p: dict, r: dict) -> tuple[str, str]:
    """(verdict, detail) for the product page: ok, broken, delisted, moved, throttled or unanswered."""
    if (why := throttled_reason(r)):
        return "throttled", why
    why = unanswered_reason(r)
    if why:
        return "unanswered", why
    st = r["status"]
    if 300 <= st < 400:
        return "broken", f"HTTP {st} that could not be followed after {r['redirects']} redirects (a loop, too many, or no Location)"
    if st >= 400:
        return "broken", f"HTTP {st}" + (f" at {r['final_url']}" if r["final_url"] != p["url"] else "")
    a, b = urlsplit(p["url"]), urlsplit(r["final_url"])
    same_host = norm_host(a.hostname) == norm_host(b.hostname)
    if same_host and LISTING.match(norm_path(b.path)) and not handle_of(b.path):
        home = re.fullmatch(r"(/[a-z]{2}(-[a-z]{2})?)?", norm_path(b.path))
        return "delisted", f"lands on the store's {'home' if home else 'listing'} page {r['final_url']}"
    if NOT_FOUND_TITLE.search(r["body"][:200000]):
        return "broken", f"HTTP {st} but the page title says not found ({r['final_url']})"
    ha, hb = handle_of(a.path), handle_of(b.path)
    same_path = (ha == hb) if (ha and hb) else norm_path(a.path) == norm_path(b.path)
    if not same_host or not same_path:
        if not same_host and LISTING.match(norm_path(b.path)) and not hb:
            return "delisted", f"sent to another site's home or listing page {r['final_url']}"
        return "moved", f"-> {r['final_url']}"
    return "ok", ""


def product_json_url(p: dict, final_url: str) -> str | None:
    """`<URL without query>.js` on the store's Shopify host, for the page the product now lands on."""
    s = urlsplit(final_url)
    h = handle_of(s.path)
    if not h or (s.hostname or "") in NO_JSON:
        return None
    host = JSON_HOST.get(s.hostname or "", s.hostname or "")
    return f"https://{host}/products/{urllib.parse.quote(h)}.js"


def judge_stock(p: dict, page: dict, js: dict | None) -> dict:
    """{"available": True/False/None, "source", "store_price", "detail"} from the product JSON or the page's schema."""
    # a record with cart_variant sends /go/ to the store's cart permalink for that variant (DLC-71): its stock is the
    # cart link's, so SOLD OUT or a missing variant flags the day that link stops selling
    want = p.get("cart_variant") or variant_of(p["url"])
    if js is not None:
        if (why := throttled_reason(js)):
            return {"available": None, "source": "product json", "throttled": True, "detail": f"product JSON {why}"}
        why = unanswered_reason(js)
        if why:
            return {"available": None, "source": "product json", "detail": f"product JSON unanswered: {why}"}
        if js["status"] == 404:
            return {"available": None, "source": "product json", "gone": True,
                    "detail": f"the store's product JSON {js['url']} is a 404 though the page answers {page['status']}"}
        try:
            data = json.loads(js["body"])
            variants = data["variants"]
        except (ValueError, KeyError, TypeError):
            data = None
        if data is not None:
            if want:
                v = next((x for x in variants if x.get("id") == want), None)
                if v is None:
                    return {"available": None, "source": "product json", "gone": True,
                            "detail": f"variant {want} is no longer on {js['url'][:-3]}"}
                avail = bool(v.get("available"))
            else:
                # the record's own variant, matched by name and price as the daily stock read does (DLC-306); the first
                # available one only where the record can't be matched or the JSON lacks what the match needs
                try:
                    v, how = pricecheck.record_variant(p, variants)
                except (KeyError, TypeError, AttributeError):
                    v, how = next((x for x in variants if x.get("available")), variants[0] if variants else None), ""
                avail = bool(v and v.get("available"))
            price = (v.get("price") / 100) if v and isinstance(v.get("price"), (int, float)) else None
            return {"available": avail, "source": "product json" + (f" (variant {want})" if want else f" ({how})" if how else "")
                    + (" via r.jina.ai" if js.get("via") else ""), "store_price": price, "detail": ""}
    # No Shopify product JSON: the page's own schema.org availability (the first one on the page is the product's).
    m = AVAIL.search(page.get("body") or "")
    if m:
        word = m.group(1).lower()
        if word == "discontinued":
            return {"available": None, "source": "page schema", "gone": True, "detail": "the page's schema.org availability says Discontinued"}
        return {"available": word not in ("outofstock", "soldout"), "source": f"page schema ({m.group(1)})", "detail": ""}
    return {"available": None, "source": None, "detail": "no stock signal on this store"}


# ---------------------------------------------------------------- /go/<slug>

def go_request(slug: str) -> dict:
    """GET https://dealectric.com/go/<slug> without following the redirect."""
    conn = http.client.HTTPSConnection(SITE_HOST, timeout=TIMEOUT, context=codecheck._CTX)
    try:
        conn.request("GET", f"/go/{urllib.parse.quote(slug)}",
                     headers={"User-Agent": CHECK_UA, "X-Dealectric-Check": "linkcheck", "Accept": "text/html,*/*;q=0.8"})
        r = conn.getresponse()
        r.read(4000)
        return {"status": r.status, "location": r.getheader("Location")}
    except (http.client.HTTPException, OSError, ValueError) as e:
        return {"status": None, "location": None, "error": f"{type(e).__name__}: {e}"[:300]}
    finally:
        conn.close()


def sub_key(entry: dict) -> str:
    return SUB_KEY.get(entry.get("network"), "clickref")


def map_slot(entry: dict) -> str | None:
    """Why the map's deep link is wrong before any request: it has no slot for the sub-ID in its network's parameter."""
    sub = sub_key(entry)
    if sub not in {k for k, _ in urllib.parse.parse_qsl(urlsplit(entry.get("url") or "").query, keep_blank_values=True)}:
        return f"the deep link in links-map.json has no {sub}= parameter for the {entry.get('network')} sub-ID (rebuild)"
    return None


def go_matches(location: str | None, entry: dict, slug: str) -> tuple[bool, bool, str]:
    """(matches, literal, detail): the Location is the map's deep link with the sub-ID set to <slug>.<10 hex click id>.

    The sub-ID sits in the network's own query parameter (SUB_KEY: CJ sid, Rakuten u1, Awin clickref; DLC-306, every
    Rakuten link used to be flagged for having no clickref). The Worker sets it with URLSearchParams.set
    (worker/src/index.js), which replaces the map's placeholder value in place, so the Location starts with the deep link
    up to the sub-ID key (`literal`). `matches` compares the parsed URL (scheme, host, path, every other query parameter)
    so an encoding difference alone is not a finding. A Location with no sub-ID in that parameter, or with it in another
    network's parameter, is a finding."""
    deep = entry.get("url") or ""
    if not location:
        return False, False, "no Location header"
    sub = sub_key(entry)
    L, D = urlsplit(location), urlsplit(deep)
    if (L.scheme, L.netloc, L.path) != (D.scheme, D.netloc, D.path):
        return False, False, f"goes to {L.scheme}://{L.netloc}{L.path}, the map says {D.scheme}://{D.netloc}{D.path}"
    lq = urllib.parse.parse_qsl(L.query, keep_blank_values=True)
    dq = urllib.parse.parse_qsl(D.query, keep_blank_values=True)
    subs = [v for k, v in lq if k == sub]
    if len(subs) != 1 or not re.fullmatch(re.escape(slug) + r"\.[0-9a-f]{10}", subs[0]):
        return False, False, f"sub-ID {sub}={subs} is not {slug}.<click id>"
    rest_l, rest_d = sorted((k, v) for k, v in lq if k != sub), sorted((k, v) for k, v in dq if k != sub)
    if rest_l != rest_d:
        diff = sorted(set(rest_l) ^ set(rest_d))
        return False, False, f"query differs from the map: {diff}"[:300]
    i = deep.find(sub + "=")
    literal = i >= 0 and location.startswith(deep[: i + len(sub) + 1])
    return True, literal, "" if literal else "same link, encoded differently"


def judge_go(slug: str, entry: dict | None, r: dict) -> tuple[str, str]:
    if entry is None:
        return "map", "no entry in worker/src/links-map.json"
    if (why := map_slot(entry)):
        return "map", why
    if r.get("error"):
        return "unanswered", r["error"]
    if r["status"] == 429:   # never read through r.jina.ai: it would follow the redirect, and that is a click
        return "throttled", f"{NOT_CHECKED}: the Worker answered HTTP 429"
    if r["status"] != 302:
        return "go", f"HTTP {r['status']} (expected a 302)" + ("; the Worker answered as it does to an AI fetcher" if r["status"] == 200 else "")
    ok, _, detail = go_matches(r["location"], entry, slug)
    return ("ok", detail) if ok else ("go", detail)


# ---------------------------------------------------------------- the run

def plan(slugs: list[str] | None) -> tuple[list[dict], list[str]]:
    # Amazon Associates records (program "amazon:us", DLC-159) are left out: amazon.com answers a plain client with a
    # bot wall or 503, so a verdict here would be noise; their listings are checked by hand with the weekly price pass.
    products = [p for p in PRODUCTS if p["slug"] not in RETIRED and (not slugs or p["slug"] in slugs)
                and not p["program"].startswith("amazon:")]
    aliases = [] if slugs else sorted(s for s, (_, new, _) in RETIRED.items() if new)   # retired slugs the Worker still serves
    return products, aliases


def interleave(products: list[dict]) -> list[dict]:
    """Round-robin over stores, so a store's requests are spread out and the per-store gap rarely has to wait."""
    by: dict[str, list[dict]] = {}
    for p in products:
        by.setdefault(store_key(urlsplit(p["url"]).hostname), []).append(p)
    out, queues = [], list(by.values())
    while any(queues):
        for q in queues:
            if q:
                out.append(q.pop(0))
    return out


def spread(products: list[dict], client: Client, url_of):
    """Yield the products one request at a time, each time from the store whose next request has waited longest
    (client.ready_at of url_of(product); r.jina.ai counts as the host of every store it is reading for). Two requests
    in a row go to different hosts whenever more than one host has work that is ready, and a slow store (STORE_GAP)
    or a throttled one holds up only its own products. The per-host gap itself is kept by Client.get()."""
    queues: dict[str, collections.deque] = {}
    for p in products:
        queues.setdefault(store_key(urlsplit(p["url"]).hostname), collections.deque()).append(p)
    while queues:
        key = min(queues, key=lambda k: client.ready_at(url_of(queues[k][0])))
        p = queues[key].popleft()
        if not queues[key]:
            del queues[key]
        yield p


def summary_line(rows: list[dict], findings: list[dict]) -> str:
    """One line for the sweep's commit message: "links: 41 ok" or "links: 40 ok, 1 moved (slug -> URL)"."""
    bad = {f["slug"] for f in findings}
    parts = [f"{sum(1 for r in rows if r['slug'] not in bad)} ok"]
    for kind in ("broken", "moved", "delisted", "sold out", "back in stock", "go", "map", "throttled", "unanswered"):
        fs = [f for f in findings if f["kind"] == kind]
        if fs and kind in ("throttled", "unanswered"):   # usually a whole store that would not answer: count by brand
            brands = [BRAND.get(f["slug"], f["slug"]) for f in fs]
            what = ", ".join(f"{b} {brands.count(b)}" for b in dict.fromkeys(brands))
        elif fs:
            what = ", ".join(f"{f['slug']} {f['detail']}" if kind == "moved" else f["slug"] for f in fs)
        if fs:
            label = {"go": "/go/ mismatch", "map": "link map stale", "throttled": NOT_CHECKED}.get(kind, kind)
            parts.append(f"{len(fs)} {label} ({what})")
    known = [r["slug"] for r in rows if r.get("stock", {}).get("available") is False and r.get("in_stock") is False]
    line = "links: " + ", ".join(parts) + (f"; sold out as recorded: {', '.join(known)}" if known else "")
    return line if len(line) <= 1200 else line[:1190] + " …(see the log)"


def run(args) -> int:
    today = args.date or dt.datetime.now(dt.timezone.utc).date().isoformat()   # UTC, like the sweep's file names
    products, aliases = plan(args.slug)
    lmap = json.loads(LINKS_MAP.read_text(encoding="utf-8"))
    if args.dry_run:
        print(f"linkcheck {today}: {len(products)} products, {len(products) + len(aliases)} /go/ links, "
              f"{GAP:.0f} s between requests to one store ({', '.join(f'{k} {v:.0f} s' for k, v in STORE_GAP.items())}), "
              f"{JINA_GAP:.1f} s between reads through r.jina.ai (a store that answers 429)")
        for p in interleave(products):
            js = product_json_url(p, p["url"])
            print(f"  {p['slug']}\n      page {p['url']}\n      {'json ' + js if js else 'stock from the page schema'}"
                  f"\n      go   https://{SITE_HOST}/go/{p['slug']}" + ("" if p["slug"] in lmap else "   (NOT IN links-map.json)"))
        for s in aliases:
            print(f"  {s} (retired; the Worker serves the replacement's link)\n      go   https://{SITE_HOST}/go/{s}")
        return 0

    started = now_utc()
    client = Client(time.monotonic() + DEADLINE)
    rows = {p["slug"]: {"slug": p["slug"], "brand": p["brand"], "url": p["url"], "in_stock": p.get("in_stock")} for p in products}
    order = interleave(products)
    # 1. product pages
    pages = {}
    for p in spread(order, client, lambda p: p["url"]):
        r = client.get(p["url"], "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
        pages[p["slug"]] = r
        verdict, detail = judge_page(p, r)
        if r.get("via") and verdict not in ("ok", "throttled"):
            detail += " (read through r.jina.ai)"
        rows[p["slug"]].update(checked_at=now_utc(), status=r["status"], redirects=r["redirects"], final_url=r["final_url"],
                               hops=[h["status"] for h in r["hops"]], page=verdict, page_detail=detail,
                               **({"via": r["via"]} if r.get("via") else {}))

    # 2. stock: the Shopify product JSON, or the page's schema
    def js_url_of(p: dict) -> str | None:
        return product_json_url(p, pages[p["slug"]]["final_url"]) if rows[p["slug"]]["page"] in ("ok", "moved") else None

    for p in spread(order, client, js_url_of):
        row, page = rows[p["slug"]], pages[p["slug"]]
        if row["page"] not in ("ok", "moved"):
            row["stock"] = {"available": None, "source": None, "detail": "not checked (page " + row["page"] + ")"}
            continue
        js_url = js_url_of(p)
        js = client.get(js_url, "application/json", kind="json") if js_url else None
        row["stock"] = {**judge_stock(p, page, js), **({"json_url": js_url} if js_url else {})}
    # 3. the Worker
    alias_rows = []
    for i, slug in enumerate([p["slug"] for p in order] + aliases):
        entry = lmap.get(slug)
        if entry is None:
            r = {"status": None, "location": None}
        elif time.monotonic() > client.deadline:
            r = {"status": None, "location": None, "error": f"run deadline ({DEADLINE // 60} min) passed before this request"}
        else:
            if i:
                time.sleep(GO_GAP)
            r = go_request(slug)
        verdict, detail = judge_go(slug, entry, r)
        go = {"status": r.get("status"), "location": r.get("location"), "verdict": verdict, "detail": detail}
        if entry is not None and r.get("location"):
            go["literal_prefix"] = go_matches(r["location"], entry, slug)[1]
        if slug in rows:
            rows[slug]["go"] = go
            mu = (entry or {}).get("merchant_url")
            if entry is not None and mu != rows[slug]["url"]:
                rows[slug]["map"] = f"links-map.json has merchant_url {mu}; products.py has {rows[slug]['url']} (rebuild)"
        else:
            alias_rows.append({"slug": slug, "go": go})

    # findings, one per (product, kind)
    findings = []
    for row in rows.values():
        s = row["slug"]
        if row["page"] != "ok":
            findings.append({"slug": s, "kind": row["page"], "detail": row["page_detail"]})
        st = row.get("stock", {})
        if st.get("gone"):
            findings.append({"slug": s, "kind": "delisted", "detail": st["detail"]})
        elif st.get("available") is False and row["in_stock"] is not False:
            findings.append({"slug": s, "kind": "sold out", "detail": f"not available ({st.get('source')}); products.py does not say in_stock False"})
        elif st.get("available") is True and row["in_stock"] is False:
            findings.append({"slug": s, "kind": "back in stock", "detail": f"available ({st.get('source')}); products.py says in_stock False"})
        elif st.get("throttled"):
            findings.append({"slug": s, "kind": "throttled", "detail": st["detail"]})
        elif st.get("source") and st.get("available") is None and "unanswered" in st.get("detail", ""):
            findings.append({"slug": s, "kind": "unanswered", "detail": st["detail"]})
        g = row.get("go", {})
        if g.get("verdict") in ("go", "map", "throttled", "unanswered"):
            findings.append({"slug": s, "kind": g["verdict"], "detail": "/go/: " + g["detail"]})
        if row.get("map"):
            findings.append({"slug": s, "kind": "map", "detail": row["map"]})
    for a in alias_rows:
        if a["go"]["verdict"] != "ok":
            findings.append({"slug": a["slug"], "kind": a["go"]["verdict"], "detail": "/go/ (retired slug): " + a["go"]["detail"]})
    # one entry per (slug, kind): a page that 404s and a JSON that 404s are one delisting
    seen, uniq = set(), []
    for f in findings:
        if (f["slug"], f["kind"]) not in seen:
            seen.add((f["slug"], f["kind"]))
            uniq.append(f)
    findings = uniq
    for f in findings:
        f["line"] = f"{f['kind'].upper()} {f['slug']}: {f['detail']}"
    row_list = [rows[p["slug"]] for p in products]
    line = summary_line(row_list, findings)
    counts = {"products": len(row_list), "go_links": len(row_list) + len(alias_rows), "requests_to_stores": client.requests,
              "requests_through_jina": client.jina_requests,
              "ok": sum(1 for r in row_list if r["slug"] not in {f["slug"] for f in findings})}
    for f in findings:
        counts[f["kind"]] = counts.get(f["kind"], 0) + 1
    out = Path(args.out) if args.out else OUT_DIR / f"{today}-links.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = {"date": today, "started_at": started, "finished_at": now_utc(), "tool": "tools/linkcheck.py (DLC-35)",
           "summary_line": line, "counts": counts, "throttled_stores": {k: t["why"] for k, t in client.throttled.items()},
           "findings": findings, "rows": row_list, "retired_aliases": alias_rows}
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(f"linkcheck {today}: {len(row_list)} products, {counts['go_links']} /go/ links, {client.requests} store requests, "
          f"{client.jina_requests} reads through r.jina.ai ({len(client.throttled)} stores answered 429)")
    for f in findings:
        print("  " + f["line"])
    print(line)
    print(f"wrote {out.relative_to(ROOT) if out.is_relative_to(ROOT) else out}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--dry-run", action="store_true", help="list what would be requested; no network")
    ap.add_argument("--date", default=None, help="the date in the output file name (default: today, UTC)")
    ap.add_argument("--out", default=None, help="write here instead of growth/codes/<date>-links.json")
    ap.add_argument("--slug", action="append", default=None, help="only this product (repeatable; testing)")
    ap.add_argument("--deadline-min", type=int, default=None, help="run deadline in minutes (default 12, for the daily sweep)")
    a = ap.parse_args()
    if a.deadline_min:
        global DEADLINE
        DEADLINE = a.deadline_min * 60
    return run(a)


if __name__ == "__main__":
    sys.exit(main())
