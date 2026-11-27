"""Step 1 of the weekly upkeep (growth/stock/README.md): read every listed product the way a shopper sees it.

Every record is opened in a background tab of the Agent Chrome (localhost:9222), several tabs at once:
- Shopify stores: the listing's product data (/products/<handle>.js, fetched inside the page so it carries the browser's
  cookies), the exact variant the record links (?variant=, else cart_variant, else matched by name and price), then
  that variant's rendered page: buy buttons and the text of the buy area, where stores print pre-order and ship notes.
- Amazon: the listing's buy box: price, availability line, delivery promise, seller, release date, Add to Cart.
- Other stores: the rendered page text.
Writes one JSON line per record to <out>; a record already in <out> is skipped, so a stopped run resumes.

    python3.12 tools/upkeep/read.py <out.jsonl> [--tabs 3] [--slugs a,b] [--brands BLUETTI,OSCAL]
"""
from __future__ import annotations

import json
import queue
import sys
import threading
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))
import codesweep as C  # noqa: E402  (Tab: one CDP tab of the Agent Chrome)
import pricecheck as PC  # noqa: E402  (pick_variant)

import re  # noqa: E402

STOCK_LINE = re.compile(r"pre-?order|ship(s|ping|ped)?\b|dispatch|deliver|sold ?out|out of stock|in stock|back ?order|"
                        r"available|notify me|coming soon|release|reserve|orders placed|restock|discontinued", re.I)


def page_parts(text: str, title: str | None) -> dict:
    """The text from the product's own title on (where the price, variant picker and ship notes sit), and every line on
    the page that talks about stock or shipping: stores print those notes in different places, and a page also
    carries other products' notes (add-ons, "you may also like"), which the classifier has to tell apart."""
    i = -1
    for t in [title or ""] + [title.split(" | ")[0] if title else "", (title or "")[:40]]:
        if t and len(t) > 6:
            i = text.find(t[:60])
            if i >= 0:
                break
    start = max(0, i) if i >= 0 else 0
    lines, seen = [], set()
    for l in text.split("\n"):
        l = l.strip()
        if 3 < len(l) < 260 and STOCK_LINE.search(l) and l not in seen:
            seen.add(l)
            lines.append(l)
    return {"buy_area": text[start:start + 5000], "stock_lines": lines[:80]}


JS_PAGE = r"""(()=>{
 const vis=e=>!!(e.offsetParent)&&e.getBoundingClientRect().width>0;
 const btns=[...document.querySelectorAll('button,input[type=submit],a[class*=btn],a[class*=button]')].filter(vis)
   .map(b=>(b.innerText||b.value||'').trim().replace(/\s+/g,' ')).filter(t=>t&&t.length<60&&/cart|buy|pre-?order|sold|notify|stock|unavailable|reserve|back ?order/i.test(t));
 return JSON.stringify({title:document.title,url:location.href,btns:[...new Set(btns)].slice(0,12),text:document.body?document.body.innerText:''});
})()"""

JS_AMAZON = r"""(()=>{const q=s=>{const e=document.querySelector(s);return e?e.innerText.trim().replace(/\s+/g,' '):null};
 let price=null;for(const s of ['#corePrice_feature_div .a-price .a-offscreen','#corePriceDisplay_desktop_feature_div .a-price .a-offscreen','#apex_desktop .a-price .a-offscreen','#price_inside_buybox','#newBuyBoxPrice']){const e=document.querySelector(s);if(e&&/\d/.test(e.textContent)){price=e.textContent.trim();break}}
 return JSON.stringify({title:q('#productTitle'),price,avail:q('#availability'),delivery:q('#mir-layout-DELIVERY_BLOCK')||q('#deliveryBlockMessage'),
  merchant:q('#merchantInfoFeature_feature_div')||q('#merchant-info')||q('#tabular-buybox'),
  cart:!!document.querySelector('#add-to-cart-button'),buynow:!!document.querySelector('#buy-now-button'),
  captcha:/captcha|not a robot/i.test(document.title+(document.body?document.body.innerText.slice(0,500):'')),url:location.href})})()"""


def kind(p: dict) -> str:
    if str(p.get("program", "")).startswith("amazon"):
        return "amazon"
    return "shopify" if "/products/" in (p.get("url") or "") else "other"


def settle(t, need: int = 800, cap: float = 25.0) -> None:
    """Wait until the page is loaded and its text has stopped growing (or `cap` seconds)."""
    t0, last = time.time(), -1
    while time.time() - t0 < cap:
        time.sleep(1.5)
        try:
            n = t.eval("document.readyState==='complete' ? (document.body ? document.body.innerText.length : 0) : -1")
        except Exception:
            continue
        if n is not None and n >= need and n == last:
            return
        last = n


def read_shopify(t, p: dict) -> dict:
    u = urllib.parse.urlsplit(p["url"])
    base = f"{u.scheme}://{u.netloc}{u.path}"
    want = urllib.parse.parse_qs(u.query).get("variant", [""])[0] or p.get("cart_variant")
    out: dict = {}
    t.call("Page.navigate", url=base)
    settle(t, need=300, cap=15)
    t.eval(f"window.__pj=null;fetch('{base.rstrip('/')}.js').then(r=>r.ok?r.json():null).then(j=>window.__pj=JSON.stringify(j)).catch(e=>window.__pj='null')")
    d = None
    for _ in range(12):
        time.sleep(1)
        d = t.eval("window.__pj")
        if d:
            break
    d = json.loads(d) if d and d != "null" else None
    v = how = None
    if d:
        vs = d.get("variants", [])
        if want:
            v = next((x for x in vs if str(x["id"]) == str(want)), None)
            how = "named" if v else "named variant missing from the listing"
        else:
            v, how = PC.pick_variant(p.get("name") or p["slug"], vs, p.get("price"))
        out["listing_title"] = d.get("title")
        if v:
            out.update(variant=v["id"], vtitle=v.get("title"), v_avail=bool(v.get("available")), v_price=v["price"] / 100,
                       v_compare=((v.get("compare_at_price") or 0) / 100) or None)
        out["variant_how"] = str(how)
    else:
        out["listing"] = "no product data (delisted or not Shopify)"
    if v:
        t.call("Page.navigate", url=f"{base}?variant={v['id']}")
        settle(t)
    page = json.loads(t.eval(JS_PAGE))
    out.update(final_url=page["url"], page_title=page["title"], btns=page["btns"], **page_parts(page["text"], out.get("listing_title")))
    return out


def read_other(t, p: dict) -> dict:
    t.call("Page.navigate", url=p["url"])
    settle(t)
    page = json.loads(t.eval(JS_PAGE))
    return {"final_url": page["url"], "page_title": page["title"], "btns": page["btns"], **page_parts(page["text"], page["title"])}


def read_amazon(t, p: dict) -> dict:
    t.call("Page.navigate", url=f"https://www.amazon.com/dp/{p['asin']}")
    r: dict = {}
    for _ in range(12):
        time.sleep(1.5)
        try:
            r = json.loads(t.eval(JS_AMAZON))
        except Exception:
            continue
        if r.get("captcha") or (r.get("title") and (r.get("price") or r.get("avail") or r.get("delivery"))):
            break
    return {"amazon": r}


def worker(q: "queue.Queue", out_path: Path, lock: threading.Lock) -> None:
    t = C.Tab("about:blank")
    t.call("Page.enable")
    try:
        while True:
            try:
                p = q.get_nowait()
            except queue.Empty:
                return
            k = kind(p)
            row = {"slug": p["slug"], "brand": p["brand"], "kind": k, "url": p.get("url"), "read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
            try:
                row.update(read_amazon(t, p) if k == "amazon" else read_shopify(t, p) if k == "shopify" else read_other(t, p))
            except Exception as e:   # a hung tab is replaced; the error row is re-read when the run resumes
                row["error"] = f"{type(e).__name__}: {e}"
                try:
                    t.close()
                except Exception:
                    pass
                t = C.Tab("about:blank")
                t.call("Page.enable")
            with lock:
                with out_path.open("a") as f:
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
            print(f"{p['slug'][:56]:56} {k:7} {row.get('v_avail', (row.get('amazon') or {}).get('avail', ''))!s:.40} {row.get('error', '')}", flush=True)
            time.sleep(1.0)
    finally:
        try:
            t.close()
        except Exception:
            pass


def read_all(products: list[dict], out_path: Path, tabs: int = 3) -> None:
    done = set()
    if out_path.exists():
        done = {json.loads(l)["slug"] for l in out_path.open() if l.strip() and "error" not in json.loads(l)}
    q: queue.Queue = queue.Queue()
    for p in products:
        if p["slug"] not in done and (p.get("url") or p.get("asin")):
            q.put(p)
    lock = threading.Lock()
    ts = [threading.Thread(target=worker, args=(q, out_path, lock), daemon=True) for _ in range(tabs)]
    for th in ts:
        th.start()
        time.sleep(2)
    for th in ts:
        th.join()


def select(products, slugs=None, brands=None):
    out = [p for p in products if (not slugs or p["slug"] in slugs) and (not brands or p["brand"] in brands)]
    return out


if __name__ == "__main__":
    from products import PRODUCTS, RETIRED
    a = sys.argv[1:]
    opt = lambda k: a[a.index(k) + 1] if k in a else None
    ps = select([p for p in PRODUCTS if p["slug"] not in RETIRED],
                set(opt("--slugs").split(",")) if opt("--slugs") else None, set(opt("--brands").split(",")) if opt("--brands") else None)
    read_all(ps, Path(a[0]), int(opt("--tabs") or 3))
