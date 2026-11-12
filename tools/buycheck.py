#!/usr/bin/env python3.12
"""Buy-link cheapest check (DLC-237): is the price through our link the lowest price a shopper can get from a seller
ChatGPT trusts? Reads Google Shopping (udm=28) for each product in the Agent Chrome (localhost:9222), keeps the cards
whose title names the model, and compares the lowest trusted seller's price with our price after the link's discount.

Trusted sellers: the brand's own store and major US retailers (Amazon, Walmart, Best Buy, Newegg, Home Depot, Lowe's,
Target, B&H, Costco, Micro Center, Adorama, REI). Marketplace resellers (eBay, AliExpress, Temu) and used, renewed or
open-box listings are listed but not counted. Read-only: it only writes the report. Amazon prices are read to choose
pilot products and are never published (Amazon allows prices only from its own feed).

    python3.12 tools/buycheck.py [--out growth/buylink/<date>-cheapest.json] [--pace 12] [slug ...]
"""
from __future__ import annotations

import argparse, datetime as dt, json, re, sys, time, urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "growth/evals"))
import build as B  # noqa: E402
import ui  # noqa: E402

TRUSTED = ["amazon", "walmart", "best buy", "bestbuy", "newegg", "home depot", "lowe's", "lowes", "target", "b&h",
           "costco", "micro center", "adorama", "rei", "sam's club"]
UNTRUSTED = ["ebay", "aliexpress", "temu", "alibaba", "mercari", "poshmark", "facebook"]
USED = re.compile(r"\b(renew|renewed|refurb|refurbished|used|open[- ]box|pre-owned|for parts)\b", re.I)
GENERIC = {"portable", "power", "station", "solar", "panel", "kit", "generator", "with", "and", "the", "for", "battery",
           "wireless", "charger", "bluetooth", "headphones", "earbuds", "case", "camera", "usb", "usb-c", "w", "wh"}
PRICE = re.compile(r"^\$([\d,]+(?:\.\d\d)?)$")


def norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def model_tokens(p: dict) -> list[str]:
    name = re.split(r"[(,]", B.short_name(p))[0]
    words = [w for w in re.findall(r"[A-Za-z0-9+]+", name)]
    brand = norm(p["brand"])
    toks = [norm(w) for w in words if norm(w) and norm(w) != brand and w.lower() not in GENERIC]
    return [brand] + toks[:3]


def kit_tokens(p: dict) -> list[str]:
    """A kit card must also name the add-on's wattage, e.g. '200w' for '+ 200 W Solar Panel'."""
    tail = B.short_name(p).split("+", 1)[1] if "+" in B.short_name(p) else ""
    return [norm(m) + "w" for m in re.findall(r"(\d+)\s*W\b", tail)][:1]


def parse_cards(text: str) -> list[dict]:
    lines = [l.strip() for l in text.split("\n") if l.strip()]
    cards = []
    for i, l in enumerate(lines):
        m = PRICE.match(l)
        if not m or i == 0 or len(lines[i - 1]) < 18 or PRICE.match(lines[i - 1]):
            continue
        j, was = i + 1, None
        while j < len(lines) and (re.match(r"^\$?[\d,]+(\.\d\d)?$", lines[j]) or lines[j].startswith("Was")):
            if lines[j].startswith("Was"):
                was = lines[j]
            j += 1
        merchant = lines[j] if j < len(lines) else ""
        promo = lines[j + 1] if j + 1 < len(lines) else ""
        cards.append({"title": lines[i - 1], "price": float(m.group(1).replace(",", "")), "was": was,
                      "merchant": merchant, "promo": promo if re.search(r"code|off", promo, re.I) else ""})
    return cards


def seller_kind(merchant: str, brand: str) -> str:
    m = merchant.lower()
    if norm(brand) in norm(merchant) or "official" in m:
        return "brand"
    if any(u in m for u in UNTRUSTED):
        return "marketplace"
    if any(t in m for t in TRUSTED):
        return "retailer"
    return "other"


def check(p: dict, tab) -> dict:
    o = B.best_offer(p)
    after, list_price = (o[2], p.get("price")) if o and o[0] else (p.get("price"), p.get("price"))
    q = re.split(r"[(]", B.short_name(p))[0].strip()
    tab.navigate("https://www.google.com/search?" + urllib.parse.urlencode({"q": q, "udm": "28", "gl": "us", "hl": "en"}))
    time.sleep(9)
    text = tab.eval("document.body.innerText") or ""
    if "unusual traffic" in text or "not a robot" in text:
        return {"slug": p["slug"], "error": "google-captcha"}
    toks = model_tokens(p)
    kit = "kit" in p["slug"] or "+" in B.short_name(p)
    cards = []
    for c in parse_cards(text):
        t = norm(c["title"])
        if not all(k in t for k in toks):
            continue
        if kit != bool(re.search(r"panel|kit|bundle|\+", c["title"], re.I)):
            continue
        if kit and not all(w in t for w in kit_tokens(p)):
            continue
        c["kind"] = "used" if USED.search(c["title"]) else seller_kind(c["merchant"], p["brand"])
        cards.append(c)
    trusted = [c for c in cards if c["kind"] in ("brand", "retailer")]
    best = min(trusted, key=lambda c: c["price"]) if trusted else None
    brand_cards = [c for c in cards if c["kind"] == "brand"]
    verdict = "no-match"
    if best:
        gap = best["price"] - after
        verdict = "cheapest" if gap >= max(1.0, 0.01 * after) else ("tie" if gap > -max(1.0, 0.01 * after) else "beaten")
    return {"slug": p["slug"], "query": q, "tokens": toks, "after": after, "list": list_price,
            "code": o[0]["code"] if o and o[0] else None, "best_trusted": best, "verdict": verdict,
            "brand_shown": min((c["price"] for c in brand_cards), default=None), "cards": cards[:12]}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slugs", nargs="*")
    ap.add_argument("--out", default=f"growth/buylink/{dt.date.today()}-cheapest.json")
    ap.add_argument("--pace", type=float, default=12)
    a = ap.parse_args()
    ps = [B.BY_SLUG[s] for s in a.slugs] if a.slugs else [p for p in B.PRODUCTS if B.link_offer(p)]
    out = Path(ROOT / a.out); out.parent.mkdir(parents=True, exist_ok=True)
    rows = json.loads(out.read_text()) if out.exists() else []
    done = {r["slug"] for r in rows if not r.get("error")}
    rows = [r for r in rows if r["slug"] in done]
    tab = ui.Tab("about:blank")
    try:
        for i, p in enumerate(ps, 1):
            if p["slug"] in done:
                continue
            try:
                r = check(p, tab)
            except Exception as e:  # noqa: BLE001
                r = {"slug": p["slug"], "error": repr(e)[:200]}
                if "WebSocket" in repr(e):  # tab or Chrome restarted: open a fresh tab, keep going
                    try:
                        tab.close()
                    except Exception:  # noqa: BLE001
                        pass
                    tab = ui.Tab("about:blank")
            rows.append(r)
            out.write_text(json.dumps(rows, indent=1))
            b = r.get("best_trusted") or {}
            print(f"{i}/{len(ps)} {p['slug']:55} {r.get('verdict', r.get('error'))} ours={r.get('after')} "
                  f"best={b.get('price')} {b.get('merchant', '')}", flush=True)
            if r.get("error") == "google-captcha":
                print("Google asked for a CAPTCHA; stopping (never solved by tools).", flush=True)
                break
            time.sleep(a.pace)
    finally:
        tab.close()


if __name__ == "__main__":
    main()
