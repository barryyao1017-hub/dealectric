#!/usr/bin/env python3.12
"""Best-offer check (DLC-320, Barry 2026-11-18): for each product, which offer should its page lead with?

    ours     the brand store's price today less our code (the same-day cart test in src/coupons.json)
    amazon   the same item on Amazon (hand-confirmed ASIN, price read by tools/amzprice.py), linked with our tag
    others   every other seller of the same item found that day: Google Shopping cards (tools/buycheck.py reports)
             and the sellers ChatGPT named in that day's where-to-buy chats (a prices.json extraction, optional)

It writes src/bestoffer.json, which src/build.py reads (amazon_lead, best_sellers, lowest_tail):
    ours lowest                    -> "sellers" listed, the page opens with our code price and the lowest-of-N line
    Amazon cheaper                 -> "asin" set; build.py leads with the tagged Amazon link while its daily price is lower
    a seller we cannot link cheaper -> "beaten": [seller, price]; the page claims nothing and links nothing new
    another seller within $1 or 1%  -> "tie": [seller, price]; the page opens with our code price, without the lowest line

    python3.12 tools/bestoffer.py decide --date 2026-11-18 --shop growth/buylink/<date>-cheapest-bo*.json \
        --hand growth/buylink/<date>-bestoffer-hand.json [--cart <carttests.jsonl>] [--chat <prices.json>] [slug ...]
    python3.12 tools/bestoffer.py table [slug ...]        # what each page does now, from src/bestoffer.json

The hand file is the same-item pass a person or model made over the cards the matcher let through:
    {slug: {"asin": "B0...", "drop": ["merchant substring", ...], "keep": ["merchant substring", ...],
            "beaten": ["seller", price], "add": [["seller", price], ...], "note": "..."}}
"drop" removes a merchant's cards for that product (a sibling model, a bundle, a deal blog that is not a seller, a
listing priced under 60% of the store's price at an unknown shop). Marketplace sellers (eBay, AliExpress, TikTok Shop,
third-party sellers on Walmart or Newegg) and used or open-box listings never count, as on the rest of the site.
For a kit or bundle no other seller's card counts unless "keep" names its merchant.
"""
from __future__ import annotations

import argparse, json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src")); sys.path.insert(0, str(ROOT / "tools"))
import build as B  # noqa: E402
import buycompare as BC  # noqa: E402

OUT = ROOT / "src" / "bestoffer.json"
MARKET = ("tiktok", "ebay", "aliexpress", "temu", "alibaba", "mercari", "poshmark", "facebook", "usually $", "pre-owned", "refurbished", "/ct")


def margin(x: float) -> float:
    return max(1.0, 0.01 * x)


def load_cards(reports: list[str]) -> dict[str, list[dict]]:
    out: dict[str, list[dict]] = {}
    for f in reports:
        for r in json.load(open(f)):
            if r.get("error"):
                continue
            seen = {(c["merchant"], c["price"], c["title"]) for c in out.get(r["slug"], [])}
            out.setdefault(r["slug"], []).extend(c for c in r.get("cards", []) if (c["merchant"], c["price"], c["title"]) not in seen)
            out.setdefault("__read__", []).append(r["slug"])
    return out


def load_cart(path: str | None) -> dict[str, dict]:
    """slug -> {"store": the cart's total with no code (the control run), "after": total with our code} for runs that put
    the record's own item in the cart (subtotal equal to the record's price) and whose control code did not apply."""
    out = {}
    for line in open(path) if path else []:
        row = json.loads(line)
        runs = [r for r in row["runs"] if not r.get("error") and not r.get("void")]
        if len(runs) < 2 or runs[0].get("applicable") or abs(runs[0]["subtotal"] - row["price"]) > 0.01:
            continue
        out[row["slug"]] = {"store": runs[0]["total"], "after": runs[1]["total"] if runs[1].get("applicable") else None,
                            "code": runs[1]["code"], "code_amount": runs[1].get("code_amount")}
    return out


def decide(p: dict, cards: list[dict], hand: dict, cart: dict, chat: dict | None, date: str) -> tuple[dict, dict]:
    """(bestoffer.json entry, report row) for one product."""
    ours = B.link_price(p)
    name = f"{p['brand']} {p['name']} {p['slug'].replace('-', ' ')}"
    drop = [d.lower() for d in hand.get("drop", [])]
    # a kit or bundle: Shopping's matcher returns every bundle built on the same station, so another seller's card counts
    # only when the hand pass names that merchant in "keep" (its title lists the same contents)
    kit = "kit" in p["slug"] or "bundle" in p["slug"] or "+" in B.short_name(p)
    only = [k.lower() for k in hand.get("keep", [])] if (kit or "keep" in hand) else None
    keep, dropped = [], []
    for c in cards:
        m = c["merchant"].lower()
        if (c["kind"] in ("used", "marketplace") or any(k in m for k in MARKET) or m.startswith("(")   # "(€250)": a foreign-currency listing
                or any(d in m for d in drop) or not BC.same_item(c["title"], name)
                or (only is not None and c["kind"] != "brand" and not any(k in m for k in only))):
            dropped.append(c)
        else:
            keep.append(c)
    # the brand's own storefront on a retailer ("Walmart - Baseus") is another seller we cannot link, not the brand store
    for c in keep:
        if c["kind"] == "brand" and " - " in c["merchant"] and BC.retailer(c["merchant"].split(" - ")[0]):
            c["kind"], c["merchant"] = "retailer", BC.retailer(c["merchant"].split(" - ")[0])
    brand_cards = [c["price"] for c in keep if c["kind"] == "brand" and c["price"] >= 0.85 * p["price"]]
    # "$1,424 with code": the brand's own code as its Google Shopping card advertises it, a price the shopper gets without us
    own_code = [float(m.group(1).replace(",", "")) for c in keep if c["kind"] == "brand"
                for m in [re.search(r"\$([\d,]+(?:\.\d\d)?) with code", c.get("promo") or "")] if m]
    brand_cards += [x for x in own_code if x >= 0.85 * p["price"]]
    if kit:   # the brand's cards for a kit mix every variant of the listing: take one only when it restates the cart's no-code
              # total or shows the brand's own code price level with ours (BLUETTI's Google Shopping code, 11-18)
        ref = [cart.get("store", p["price"])] + ([ours] if ours is not None else [])
        brand_cards = [x for x in brand_cards if any(abs(x - r) <= 0.015 * r for r in ref)]
    store = min([cart.get("store", p["price"])] + [x for x in brand_cards if x <= p["price"] + 0.01])
    sellers: dict[str, float] = {}
    for c in keep:
        n = BC.retailer(c["merchant"]) if c["kind"] == "retailer" else None
        if n and n != "Amazon" and c["price"] < sellers.get(n, 1e9):
            sellers[n] = c["price"]
    for n, x in hand.get("add", []):   # a seller read by hand that day (a retailer's own page, a ChatGPT-named store checked)
        sellers[n] = min(x, sellers.get(n, 1e9))
    # the cheapest same-item seller we hold no program with
    for c in keep:   # independent stores count as sellers too, by name
        if c["kind"] == "other" and c["price"] < sellers.get(c["merchant"], 1e9):
            sellers[c["merchant"]] = c["price"]
    rivals = [(c["merchant"], c["price"]) for c in keep if c["kind"] in ("retailer", "other") and BC.retailer(c["merchant"]) != "Amazon"]
    if chat and chat.get("lowest_other_same_item") == "yes" and chat.get("lowest_other_price"):
        s = str(chat.get("lowest_other_seller") or "")
        if not any(k in s.lower() for k in (p["brand"].lower(), "official", "dealectric", "amazon") + MARKET) and not any(d in s.lower() for d in drop):
            rivals.append((s + " (named in a ChatGPT answer)", float(chat["lowest_other_price"])))
    if hand.get("beaten"):
        rivals.append(tuple(hand["beaten"]))
    rivals += [(n, x) for n, x in hand.get("add", [])]
    amz = B.AMZ_PRICES.get(hand.get("asin") or "")
    if amz and amz.get("price") and amz.get("in_stock", True):
        sellers["Amazon"] = amz["price"]
    low = min(rivals, key=lambda r: r[1]) if rivals else None
    entry = {"date": date, **({"asin": hand["asin"]} if hand.get("asin") else {}),
             "sellers": [[n, x] for n, x in sorted(sellers.items(), key=lambda kv: kv[1])][:4] + [[f"{B.store_host(p)} without the link", store]]}
    if ours is not None and low and low[1] < ours - margin(ours):
        entry["beaten"] = [low[0], low[1]]
    elif ours is not None and low and low[1] <= ours + margin(ours):
        entry["tie"] = [low[0], low[1]]   # within $1 or 1% of ours: ours is as low as any, but not "the lowest"
    if ours is not None and sellers.get("Amazon") is not None and abs(sellers["Amazon"] - ours) <= margin(ours) and "beaten" not in entry:
        entry.setdefault("tie", ["Amazon", sellers["Amazon"]])   # level with Amazon: neither leads on price, ours stays first
    coded = bool(B.best_offer(p)[0])
    if coded and ours is not None and store <= ours + margin(ours) and "beaten" not in entry:
        entry["tie"] = [f"{B.store_host(p)}'s own price or code without the link", store]
    if not coded:   # no code: the store's price is the price through our link, so it is not listed as another seller
        entry["sellers"] = [x for x in entry["sellers"] if not x[0].endswith(" without the link")]
        if store < p["price"] - 0.005 and "beaten" not in entry:   # the brand's own Shopping card is below the record's price
            entry["beaten"] = [f"{B.store_host(p)}'s own listed price", store]
    a = sellers.get("Amazon")
    action = ("amazon leads" if a and (not B.in_stock(p) or (ours is not None and ours - a >= margin(ours)))
              else "sold out at the store" if not B.in_stock(p)
              else "beaten, no claim" if entry.get("beaten")
              else "tie, ours leads without the lowest line" if entry.get("tie")
              else "ours lowest")
    row = {"slug": p["slug"], "ours": ours, "store": store, "amazon": a, "asin": hand.get("asin"),
           "cheapest_unlinked": list(low) if low else None, "action": action, "dropped": [(c["merchant"], c["price"], c["title"][:70]) for c in dropped],
           "kept": [(c["kind"], c["merchant"], c["price"], c["title"][:70]) for c in keep]}
    return entry, row


def main() -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    d = sub.add_parser("decide")
    d.add_argument("slugs", nargs="*"); d.add_argument("--date", required=True); d.add_argument("--shop", nargs="+", required=True)
    d.add_argument("--hand", required=True); d.add_argument("--cart"); d.add_argument("--chat"); d.add_argument("--report")
    d.add_argument("--dry", action="store_true", help="print the decisions, write nothing")
    t = sub.add_parser("table"); t.add_argument("slugs", nargs="*")
    a = ap.parse_args()
    out = json.loads(OUT.read_text()) if OUT.exists() else {"products": {}}
    if a.cmd == "table":
        for s in a.slugs or sorted(out["products"]):
            p, b = B.BY_SLUG[s], out["products"].get(s) or {}
            al = B.amazon_lead(p)
            act = "amazon leads" if al else "ours lowest" if B.lowest_tail(p) else "tie, ours leads" if B.buy_first(p) and b.get("tie") else "no claim"
            print(f"{s:55} ours {B.link_price(p)}  amazon {(al or {}).get('price') or (B.AMZ_PRICES.get(b.get('asin') or '') or {}).get('price')}  "
                  f"beaten {b.get('beaten')}  -> {act}")
        return 0
    cards, hand = load_cards(a.shop), json.load(open(a.hand))
    cart = load_cart(a.cart)
    chat = {r["slug"]: r for r in json.load(open(a.chat))} if a.chat else {}
    read = set(cards.get("__read__", []))
    rows = []
    for s in a.slugs or sorted(read):
        if s not in read:
            print(f"{s}: no Google Shopping read in the reports given, skipped"); continue
        entry, row = decide(B.BY_SLUG[s], cards.get(s, []), hand.get(s, {}), cart.get(s, {}), chat.get(s), a.date)
        out["products"][s] = entry
        rows.append(row)
        print(f"{s:52} ours {row['ours']}  store {row['store']}  amazon {row['amazon']}  unlinked {row['cheapest_unlinked']}  -> {row['action']}")
        for k in row["kept"]:
            if k[0] != "brand" and row["ours"] is not None and k[2] <= row["ours"] + margin(row["ours"]):
                print(f"      at or below ours: {k[1]} ${k[2]} | {k[3]}")
    if not a.dry:
        OUT.write_text(json.dumps({"products": dict(sorted(out["products"].items()))}, indent=1) + "\n")
    if a.report:
        Path(a.report).write_text(json.dumps(rows, indent=1) + "\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
