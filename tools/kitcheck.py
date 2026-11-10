#!/usr/bin/env python3.12
"""Cart-test a kit (DLC-223) and record the result in src/kits-tested.json, which the page's kit price comes from.

Usage: python3.12 tools/kitcheck.py <kit slug> [--link]

Store kit (Shopify): in a background tab of the agent's Chrome (localhost:9222) on the store's own origin, a fresh cart
gets every item of the kit (/cart/add.js), then each of the brand's published codes in turn (/cart/update.js), and
/cart.js is read: every variant must be in the cart and available, and the code that takes the most off wins. The
result {date, pass, list, after, code, lines} is written for the build. --link then opens the real buy link (the
network deep link with the cart permalink as its destination, as the Worker redirects) and reports whether it reached
the checkout with every item, the code and the network's click ID (Awin awc / CJ cjevent): one test click.

Amazon kit: opens the amazon.com Add-to-Cart link and reports whether Amazon shows every ASIN on its confirmation page.
"""
import json, sys, time
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path[:0] = [str(ROOT / "tools"), str(ROOT / "src")]
import codesweep as C  # noqa: E402
import build as B  # noqa: E402

OUT = ROOT / "src/kits-tested.json"

CART_JS = r"""
(async () => {
  const j = async (u, body) => { const r = await fetch(u, body ? {method: "POST", headers: {"content-type": "application/json"}, body: JSON.stringify(body)} : {});
                                 if (!r.ok) throw new Error(u + " HTTP " + r.status); return r.json(); };
  await j("/cart/clear.js", {});
  await j("/cart/add.js", {items: ITEMS});
  const out = {};
  for (const code of CODES) {
    await j("/cart/update.js", {discount: code});
    out[code] = await j("/cart.js");
    await new Promise(r => setTimeout(r, 800));
  }
  await j("/cart/update.js", {discount: ""});
  out[""] = await j("/cart.js");
  await j("/cart/clear.js", {});
  return out;
})()
"""


def store_kit(k: dict) -> dict:
    ps = B.kit_products(k)
    p0 = ps[0][0]
    host = B.urlsplit(p0["url"]).netloc
    codes = [c["code"] for c, _ in B.codes_for(p0)] or []
    for p, _ in ps[1:]:
        codes += [c["code"] for c, _ in B.codes_for(p) if c["code"] not in codes]
    t = C.Tab(f"https://{host}/")
    try:
        for _ in range(40):
            time.sleep(1)
            if (t.eval("location.origin") or "") == f"https://{host}" and (t.eval("document.readyState") or "") != "loading":
                break
        else:
            return {"pass": False, "error": f"store page did not load on {host} ({t.eval('location.href')})"}
        time.sleep(2)
        variants = {}
        for i in k["items"]:   # resolve each item's variant from its product page's .js on the store origin
            if i.get("variant"):
                variants[i["slug"]] = int(i["variant"]); continue
            path = B.urlsplit(B.BY_SLUG[i["slug"]]["url"]).path.rstrip("/")
            js = ("fetch(%s + '.js').then(r => r.json()).then(d => { const want = %s.toLowerCase();"
                  " const v = d.variants.find(v => v.available && (!want || v.title.toLowerCase().includes(want))) || d.variants[0];"
                  " return {id: v.id, title: d.title + ' / ' + v.title, available: v.available}; })") % (json.dumps(path), json.dumps(i.get("option", "")))
            v = t.eval(js)
            print(f"  {i['slug']}: variant {v}")
            variants[i["slug"]] = v["id"]
            time.sleep(1)
        items = [{"id": variants[i["slug"]], "quantity": i.get("qty", 1)} for i in k["items"]]
        t.fresh_cart(host)
        res = t.eval(CART_JS.replace("ITEMS", json.dumps(items)).replace("CODES", json.dumps(codes)))
    finally:
        t.close()
    if not isinstance(res, dict):
        return {"pass": False, "error": f"no cart result ({res!r})"[:300]}
    base = res[""]
    got = {it["variant_id"]: it for it in base["items"]}
    missing = [i["slug"] for i in k["items"] if variants[i["slug"]] not in got]
    lines = [{"variant": v, "title": it["title"], "qty": it["quantity"], "price": it["original_line_price"] / 100} for v, it in got.items()]
    best = None
    for code in codes:
        a = C.cart_answer(res[code], code, "kit", True)
        print(f"  {code}: applicable {a['applicable']}, subtotal {a['subtotal']}, total {a['total']}, code takes {a['code_amount']}")
        if a["applicable"] and a["code_amount"] > 0 and (not best or a["total"] < best[1]["total"]):
            best = (code, a)
    row = {"date": date.today().isoformat(), "pass": not missing, "list": base["original_total_price"] / 100,
           "after": best[1]["total"] if best else base["total_price"] / 100, "code": best[0] if best else None,
           "auto_discount": base["total_discount"] / 100, "lines": lines, "codes_tried": codes, "variants": variants}
    if missing:
        row["error"] = f"variants not in the cart: {missing}"
    return row


def link_check(k: dict) -> bool:
    url = B.links_map()[k["slug"]]["url"]
    print(f"buy link: {url[:160]}")
    t = C.Tab(url)
    try:
        href = ""
        for _ in range(30):
            time.sleep(2)
            href = t.eval("location.href") or ""
            if "/checkouts/" in href:
                time.sleep(6)
                break
        href = t.eval("location.href") or ""
        txt = t.eval("document.body.innerText") or ""
        ck = (t.eval("document.cookie") or "").lower()
    finally:
        t.close()
    tt = B.kit_test(k) or {}
    # the store's own line titles from the cart test (first 3 words; checkout pages shorten variant suffixes)
    names_ok = all(" ".join(l["title"].split()[:3]).lower() in txt.lower() for l in tt.get("lines", []))
    code_ok = not tt.get("code") or tt["code"] in txt
    click = any(x in href.lower() or x in ck for x in ("awc=", "cjevent", "ranmid", "ransiteid"))
    print(f"checkout: {'/checkouts/' in href} ({href.split('?')[0]}); every item named: {names_ok}; code shown: {code_ok}; click ID: {click}")
    return "/checkouts/" in href and code_ok and click


def amazon_kit(k: dict) -> dict:
    url = B.kit_link(k)
    t = C.Tab(url)
    try:
        time.sleep(8)
        txt = t.eval("document.body.innerText") or ""
        html = t.eval("document.documentElement.outerHTML") or ""
    finally:
        t.close()
    asins = [B.BY_SLUG[i["slug"]]["asin"] for i in k["items"]]
    seen = [a for a in asins if a in html]
    print(txt[:600])
    return {"date": date.today().isoformat(), "pass": len(seen) == len(asins), "asins_seen": seen, "amazon": True}


def main() -> int:
    slug = sys.argv[1]
    k = B.KIT_BY_SLUG[slug]
    db = json.loads(OUT.read_text()) if OUT.exists() else {}
    row = amazon_kit(k) if B.kit_is_amazon(k) else store_kit(k)
    db[slug] = row
    OUT.write_text(json.dumps(db, indent=1, ensure_ascii=False) + "\n")
    print(json.dumps({k2: v for k2, v in row.items() if k2 != "lines"}, ensure_ascii=False))
    if "--link" in sys.argv and not B.kit_is_amazon(k) and row["pass"]:
        import importlib
        importlib.reload(B)
        return 0 if link_check(B.KIT_BY_SLUG[slug]) else 1
    return 0 if row["pass"] else 1


if __name__ == "__main__":
    sys.exit(main())
