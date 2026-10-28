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
     deep link in worker/src/links-map.json with the Worker's sub-ID (<slug>.<click id>) in it.

Findings: BROKEN (404/410, any other 4xx or a 5xx that repeats, a redirect loop, a "not found" page served as a 200),
MOVED (the final URL is on another path or another host; the query string and a trailing slash are ignored, a Shopify
product keeps its handle wherever /products/<handle> sits, and www.soundcore.com / us.soundcore.com and www./bare are
the same host), DELISTED (it lands on the store's home, a collection, search or pages URL, or the store's product JSON
no longer has the variant or the handle), SOLD OUT (no available variant while the record does not say in_stock False;
already recorded sold-outs are listed, not flagged), BACK IN STOCK (the record says in_stock False, the store has stock),
UNANSWERED (429, bot challenge or network error after one retry, never counted as broken; a store that answers a 429 or
a challenge to both tries gets no more requests that run, and its other products are unanswered), GO (the Worker's answer does
not match the link map), MAP (links-map.json is missing the product or names another merchant URL than products.py).

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
RETRY_AFTER_MAX = 60.0    # longest Retry-After honoured before the one retry after a 429
DEADLINE = 12 * 60        # seconds; past this every remaining request is left unanswered (the sweep kills us at 15 min)
MAX_BODY = 3_000_000
# Where a store's Shopify product JSON lives when it is not the product page's host (CART_HOST in tools/codesweep.py:
# www.soundcore.com is a non-Shopify front end whose /products/<handle>.js is its 404 page).
JSON_HOST = {"www.soundcore.com": "us.soundcore.com"}
SAME_HOST = [{"www.soundcore.com", "us.soundcore.com"}]
# CJ and Awin click hosts: never requested, never followed (a request there is a click on our account).
AFFILIATE = re.compile(r"(^|\.)(tkqlhce|anrdoezrs|dpbolvw|jdoqocy|kqzyfj|qksrv|emjcd|awin1|awin|zenaps)\.(com|net)$", re.I)
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
        raise Refused(f"not followed: {s.hostname} is a CJ/Awin click host (a request there counts as a click)")
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
        self.held: dict[str, str] = {}   # store -> why its remaining requests are not sent

    def get(self, url: str, accept: str) -> dict:
        """fetch() paced per store, with one retry after a 429 (its Retry-After, capped), a bot challenge, a network error
        or a 5xx. A store that answers a 429 or a bot challenge to both tries gets no more requests this run: the rest of
        its products are left unanswered rather than retried into a longer block (2026-10-28: BLUETTI answered urllib with
        429 Retry-After 60 from the first request, Tenergy with a Cloudflare challenge)."""
        host = urlsplit(url).hostname or ""
        key = store_key(host)
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
            if attempt == 2 or r.get("refused"):
                break
            if r["status"] == 429:
                time.sleep(min(retry_after_s(r.get("retry_after")), RETRY_AFTER_MAX))
            elif r.get("network") or r.get("challenged") or (r["status"] or 0) >= 500:
                time.sleep(RETRY_WAIT)
            else:
                break
        if r["status"] == 429 or r.get("challenged"):
            self.held[key] = (f"{key} answered 429 (Retry-After {r.get('retry_after')}) to both tries on {url}" if r["status"] == 429
                              else f"{key} answered a Cloudflare bot challenge (HTTP {r['status']}) to both tries on {url}")
        return r


# ---------------------------------------------------------------- one product

def unanswered_reason(r: dict) -> str | None:
    """Why a request told us nothing about the link (429, bot challenge, network, refused), else None."""
    if r.get("refused"):
        return r["error"]
    if r["status"] == 429:
        return "429 Too Many Requests twice"
    if r.get("challenged"):
        return f"HTTP {r['status']} bot challenge (Cloudflare) twice"
    if r.get("network"):
        return r["error"]
    return None


def judge_page(p: dict, r: dict) -> tuple[str, str]:
    """(verdict, detail) for the product page: ok, broken, delisted, moved or unanswered."""
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
    if not h:
        return None
    host = JSON_HOST.get(s.hostname or "", s.hostname or "")
    return f"https://{host}/products/{urllib.parse.quote(h)}.js"


def judge_stock(p: dict, page: dict, js: dict | None) -> dict:
    """{"available": True/False/None, "source", "store_price", "detail"} from the product JSON or the page's schema."""
    # a record with cart_variant sends /go/ to the store's cart permalink for that variant (DLC-71): its stock is the
    # cart link's, so SOLD OUT or a missing variant flags the day that link stops selling
    want = p.get("cart_variant") or variant_of(p["url"])
    if js is not None:
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
                v = next((x for x in variants if x.get("available")), variants[0] if variants else None)
                avail = bool(v and v.get("available"))
            price = (v.get("price") / 100) if v and isinstance(v.get("price"), (int, float)) else None
            return {"available": avail, "source": "product json" + (f" (variant {want})" if want else ""),
                    "store_price": price, "detail": ""}
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


def go_matches(location: str | None, entry: dict, slug: str) -> tuple[bool, bool, str]:
    """(matches, literal, detail): the Location is the map's deep link with the sub-ID set to <slug>.<10 hex click id>.

    The Worker sets the sub-ID with URLSearchParams.set (worker/src/index.js), which replaces the map's placeholder value
    in place, so the Location starts with the deep link up to the sub-ID key (`literal`). `matches` compares the parsed
    URL (scheme, host, path, every other query parameter) so an encoding difference alone is not a finding."""
    deep = entry.get("url") or ""
    if not location:
        return False, False, "no Location header"
    sub = "sid" if entry.get("network") == "cj" else "clickref"
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
    if r.get("error"):
        return "unanswered", r["error"]
    if r["status"] != 302:
        return "go", f"HTTP {r['status']} (expected a 302)" + ("; the Worker answered as it does to an AI fetcher" if r["status"] == 200 else "")
    ok, _, detail = go_matches(r["location"], entry, slug)
    return ("ok", detail) if ok else ("go", detail)


# ---------------------------------------------------------------- the run

def plan(slugs: list[str] | None) -> tuple[list[dict], list[str]]:
    products = [p for p in PRODUCTS if p["slug"] not in RETIRED and (not slugs or p["slug"] in slugs)]
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


def summary_line(rows: list[dict], findings: list[dict]) -> str:
    """One line for the sweep's commit message: "links: 41 ok" or "links: 40 ok, 1 moved (slug -> URL)"."""
    bad = {f["slug"] for f in findings}
    parts = [f"{sum(1 for r in rows if r['slug'] not in bad)} ok"]
    for kind in ("broken", "moved", "delisted", "sold out", "back in stock", "go", "map", "unanswered"):
        fs = [f for f in findings if f["kind"] == kind]
        if fs and kind == "unanswered":   # usually a whole store that would not answer: count by brand
            brands = [BRAND.get(f["slug"], f["slug"]) for f in fs]
            what = ", ".join(f"{b} {brands.count(b)}" for b in dict.fromkeys(brands))
        elif fs:
            what = ", ".join(f"{f['slug']} {f['detail']}" if kind == "moved" else f["slug"] for f in fs)
        if fs:
            label = {"go": "/go/ mismatch", "map": "link map stale"}.get(kind, kind)
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
              f"{GAP:.0f} s between requests to one store ({', '.join(f'{k} {v:.0f} s' for k, v in STORE_GAP.items())})")
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
    for p in order:
        r = client.get(p["url"], "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8")
        pages[p["slug"]] = r
        verdict, detail = judge_page(p, r)
        rows[p["slug"]].update(checked_at=now_utc(), status=r["status"], redirects=r["redirects"], final_url=r["final_url"],
                               hops=[h["status"] for h in r["hops"]], page=verdict, page_detail=detail)
    # 2. stock: the Shopify product JSON, or the page's schema
    for p in order:
        row, page = rows[p["slug"]], pages[p["slug"]]
        if row["page"] not in ("ok", "moved"):
            row["stock"] = {"available": None, "source": None, "detail": "not checked (page " + row["page"] + ")"}
            continue
        js_url = product_json_url(p, page["final_url"])
        js = client.get(js_url, "application/json") if js_url else None
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
            findings.append({"slug": s, "kind": "sold out", "detail": f"no available variant ({st.get('source')}); products.py does not say in_stock False"})
        elif st.get("available") is True and row["in_stock"] is False:
            findings.append({"slug": s, "kind": "back in stock", "detail": f"available ({st.get('source')}); products.py says in_stock False"})
        elif st.get("source") and st.get("available") is None and "unanswered" in st.get("detail", ""):
            findings.append({"slug": s, "kind": "unanswered", "detail": st["detail"]})
        g = row.get("go", {})
        if g.get("verdict") in ("go", "map", "unanswered"):
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
              "ok": sum(1 for r in row_list if r["slug"] not in {f["slug"] for f in findings})}
    for f in findings:
        counts[f["kind"]] = counts.get(f["kind"], 0) + 1
    out = Path(args.out) if args.out else OUT_DIR / f"{today}-links.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    doc = {"date": today, "started_at": started, "finished_at": now_utc(), "tool": "tools/linkcheck.py (DLC-35)",
           "summary_line": line, "counts": counts, "findings": findings, "rows": row_list, "retired_aliases": alias_rows}
    out.write_text(json.dumps(doc, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")

    print(f"linkcheck {today}: {len(row_list)} products, {counts['go_links']} /go/ links, {client.requests} store requests")
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
    return run(ap.parse_args())


if __name__ == "__main__":
    sys.exit(main())
