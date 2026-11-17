#!/usr/bin/env python3.12
"""Offer table (2026-11-17): every live product record joined to what shoppers did with it, from D1 pulls saved under
growth/focus/offers/data/ (clicks.json, landings.json, pageviews.json, sales.json; see the queries in README.md).

    python3.12 growth/focus/offers/offer_table.py            # writes data/offers.json and prints the cuts

Columns per offer: answer = human clicks on a /go/ link ChatGPT wrote in its answer (utm_source=chatgpt.com on the click),
page = human clicks from one of our pages opened from ChatGPT, other = other human clicks, fetch / fetch_out = assistant
fetches of the /go/ link (all / from outside the US, which our own chats never are), land = ChatGPT landings on the
product page, sales = sales whose sub-ID names the slug. Amazon records have no /go/ link, so no click columns.
"""
import collections, json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
D = ROOT / "growth/focus/offers/data"
sys.path.insert(0, str(ROOT / "src"))
import products as P  # noqa: E402

def load(n): return json.load(open(D / f"{n}.json"))

def codes_by_brand():
    out = collections.defaultdict(list)
    for c in json.load(open(ROOT / "src/coupons.json"))["codes"]:
        if c.get("publish") and c.get("result") == "works":
            out[c["brand"]].append(c)
    return out

def best_code(p, codes):
    best = 0.0
    for c in codes.get(p["brand"], []):
        sc = c.get("products") or {}
        if sc:
            if p["slug"] not in (sc.get("slugs") or []) and p["category"] not in (sc.get("categories") or []):
                continue
        if p["slug"] in (p.get("codes_excluded") or []) or c["code"] in (p.get("codes_excluded") or []):
            continue
        price = p.get("price") or 0
        if c.get("min_order") and price and price < c["min_order"]:
            continue
        pct = c["value"] if c.get("type") == "percent" else (100 * c["value"] / price if price else 0)
        best = max(best, pct)
    return round(best, 1)

def is_kit(p):
    s = p["slug"]
    return p["category"] == "solar-kit" or bool(re.search(r"(^|-)(kit|bundle|combo)(-|$)", s))

def main():
    codes = codes_by_brand()
    retired = set(getattr(P, "RETIRED", []))
    docs = {f.stem: f.read_text(errors="ignore") for f in (ROOT / "docs").glob("*.html")}
    rows = {}
    for p in P.PRODUCTS:
        if p["slug"] in retired: continue
        needle = f"/go/{p['slug']}\"" if not p["program"].startswith("amazon") else f"/dp/{p.get('asin','?')}"
        rows[p["slug"]] = dict(slug=p["slug"], brand=p["brand"], cat=p["category"], net=p["program"].split(":")[0],
                               price=p.get("price"), kit=is_kit(p), code=best_code(p, codes), stock=p.get("in_stock", True),
                               pages=sum(1 for t in docs.values() if needle in t),
                               answer=0, page=0, other=0, fetch=0, fetch_out=0, land=0, sales=0, first=None)
    for r in load("clicks"):
        o = rows.get(r["slug"])
        if not o: continue
        if r["kind"] == "ai_fetch":
            o["fetch"] += r["n"]; o["fetch_out"] += r["n"] if not r["us"] else 0
        elif r["bot_like"] == 0:
            o[{"answer": "answer", "page": "page"}.get(r["src"], "other")] += r["n"]
            if r["src"] == "answer": o["first"] = min(filter(None, [o["first"], r["first"]]))
    for r in load("landings"):
        if r["utm_source"] == "chatgpt.com" and r["page"] in rows: rows[r["page"]]["land"] += r["n"]
    for s in load("sales"):
        slug = (s.get("sub_id") or "").split(".")[0]
        if slug in rows: rows[slug]["sales"] += 1
    out = sorted(rows.values(), key=lambda o: (-o["answer"], -o["fetch"]))
    json.dump(out, open(D / "offers.json", "w"), indent=0)

    def cut(title, key, rows_):
        g = collections.defaultdict(list)
        for o in rows_: g[key(o)].append(o)
        print(f"\n== {title}")
        print(f"{'group':34} offers  w/click  answer  page  fetch  fetch_out  land  sales")
        for k, v in sorted(g.items(), key=lambda kv: -sum(o['answer'] for o in kv[1])):
            print(f"{str(k)[:34]:34} {len(v):6} {sum(1 for o in v if o['answer']):8} {sum(o['answer'] for o in v):7} "
                  f"{sum(o['page'] for o in v):5} {sum(o['fetch'] for o in v):6} {sum(o['fetch_out'] for o in v):10} "
                  f"{sum(o['land'] for o in v):5} {sum(o['sales'] for o in v):6}")
    go = [o for o in out if o["net"] != "amazon"]
    print(len(out), "live offers,", len(go), "with a /go/ link")
    cut("kit vs not", lambda o: "kit" if o["kit"] else "single", go)
    cut("kit x brand", lambda o: (o["brand"], "kit" if o["kit"] else "single"),
        [o for o in go if o["brand"] in {b for b, n in collections.Counter(x["brand"] for x in go if x["kit"]).items()}])
    cut("category (top)", lambda o: o["cat"], go)
    cut("code size", lambda o: "no code" if not o["code"] else ("code <10%" if o["code"] < 10 else "code 10%+"), go)
    cut("price band", lambda o: "?" if not o["price"] else ("<150" if o["price"] < 150 else "150-499" if o["price"] < 500 else "500-1499" if o["price"] < 1500 else "1500+"), go)
    print("\n== top 30 offers")
    for o in out[:30]:
        print(f"{o['slug'][:46]:46} {o['brand'][:10]:10} {'kit' if o['kit'] else '   '} ${o['price'] or 0:>7.0f} code {o['code']:>4}% pages {o['pages']:>3} "
              f"answer {o['answer']:>3} page {o['page']:>2} fetch {o['fetch']:>3}/{o['fetch_out']:<2} land {o['land']:>2} sales {o['sales']}")

if __name__ == "__main__":
    main()
