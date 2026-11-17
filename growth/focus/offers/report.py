#!/usr/bin/env python3.12
"""Builds report/offer-table.html from data/offers.json, landings.json, pageclicks.json, sales.json, clickers.json,
uncovered-kits.json and keywords.json (2026-11-17). Run offer_table.py, store_kits.py and platform_counts.py first.

    python3.12 growth/focus/offers/report.py
"""
import collections, html, json, re
from pathlib import Path
HERE = Path(__file__).resolve().parent
D = HERE / "data"
def load(n): return json.load(open(D / f"{n}.json"))
E = html.escape
offers = load("offers"); go = [o for o in offers if o["net"] != "amazon"]
slugs = {o["slug"] for o in offers}

def grp(o):
    ab = o["brand"] in ("ALLPOWERS", "BLUETTI")
    if ab and o["kit"]: return "ALLPOWERS and BLUETTI kits (station + panel)"
    if ab: return "ALLPOWERS and BLUETTI single products"
    if o["cat"] in ("power-station", "solar-kit", "solar-panel"): return "Other power-station brands"
    return "Every other category"
G = collections.defaultdict(list)
for o in go: G[grp(o)].append(o)
tot_answer = sum(o["answer"] for o in go)

def kind(p):
    if p in slugs: return "Product pages"
    if p.startswith(("black-friday", "cyber")): return "Deal pages"
    if p.endswith("discount-codes"): return "Code pages"
    if p in ("", "products", "compare", "agents", "about", "discount-codes"): return "Hub pages"
    if re.search(r"solar-generator|solar-kit|solar-panel-bundle", p): return "Solar kit comparison pages"
    return "Other comparison pages"
land = collections.Counter()
for r in load("landings"):
    if r["utm_source"] == "chatgpt.com": land[r["page"]] += r["n"]
pc = collections.Counter()
for r in load("pageclicks"):
    m = re.search(r"dealectric\.com/([^?#]*)", r["referrer"] or ""); pc[m.group(1).strip("/") if m else "?"] += r["n"]
PK = collections.defaultdict(lambda: [0, 0, 0])
for p, n in land.items(): PK[kind(p)][0] += 1; PK[kind(p)][1] += n
for p, n in pc.items(): PK[kind(p)][2] += n

clickers = load("clickers")
sales = load("sales")
kits = load("uncovered-kits")
kw = load("keywords") if (D / "keywords.json").exists() else {}

def rows_groups():
    out = []
    for k in ["ALLPOWERS and BLUETTI kits (station + panel)", "ALLPOWERS and BLUETTI single products", "Other power-station brands", "Every other category"]:
        v = G[k]; a = sum(o["answer"] for o in v)
        out.append(f"<tr><td>{E(k)}</td><td class=n>{len(v)}</td><td class=n>{sum(1 for o in v if o['answer'])}</td>"
                   f"<td class=n><b>{a}</b></td><td class=bar><i style='width:{100*a/tot_answer:.0f}%'></i></td>"
                   f"<td class=n>{sum(o['page'] for o in v)}</td><td class=n>{sum(o['sales'] for o in v)}</td></tr>")
    return "\n".join(out)

def rows_pages():
    out = []
    for k, v in sorted(PK.items(), key=lambda kv: -kv[1][1]):
        out.append(f"<tr><td>{E(k)}</td><td class=n>{v[0]}</td><td class=n>{v[1]}</td><td class=n>{v[2]}</td>"
                   f"<td class=n>{100*v[2]/v[1]:.0f}%</td></tr>")
    return "\n".join(out)

def rows_top(n=14):
    out = []
    for o in offers[:n]:
        out.append(f"<tr><td><a href='https://dealectric.com/{o['slug']}'>{E(o['slug'])}</a></td><td>{'kit' if o['kit'] else 'single'}</td>"
                   f"<td class=n>${o['price']:,.0f}</td><td class=n>{o['code']:.0f}%</td><td class=n>{o['pages']}</td>"
                   f"<td class=n><b>{o['answer']}</b></td><td class=n>{o['page']}</td><td class=n>{o['sales']}</td></tr>")
    return "\n".join(out)

def rows_kits():
    note = {"ALLPOWERS": "Same store and code as our best sellers. The 13 in stock are the first batch.",
            "BLUETTI": "Apex 200 and 300, Elite 100 V2, Elite 300 and AC200L sets. Price and stock need a read per page.",
            "Anker SOLIX": "We list 5 single units and no set. No code of ours yet.",
            "OSCAL": "10% code. Three sets in stock.",
            "Mango Power": "Home-backup and plug-in solar sets, $2,000 and up.",
            "Sun Gold Power": "Off-grid systems, $2,100 to $20,700. Our three have 0 clicks so far.",
            "Nature's Generator": "Only a refurbished panel set matched; its systems are sold as single listings."}
    out = []
    for b in dict.fromkeys(o["brand"] for o in kits):
        v = [o for o in kits if o["brand"] == b]; m = [o for o in v if not o["ours"]]
        st = sum(1 for o in m if o["stock"]) if any(o["price"] for o in m) else "not read"
        out.append(f"<tr><td>{E(b)}</td><td class=n>{len(v)}</td><td class=n>{len(v)-len(m)}</td><td class=n><b>{len(m)}</b></td>"
                   f"<td class=n>{st}</td><td>{E(note.get(b, ''))}</td></tr>")
    return "\n".join(out)

EARLIER = {"solar generators for home use": 5790, "solar generator with panels included": 401, "power station with solar panel": 51}  # same source, pulled 11-15 / 11-17

def rows_kw(kinds, n=12):
    v = [(k, x["n"], x.get("broad", 0)) for k, x in kw.items() if x["kind"] in kinds and (x.get("n") or x.get("broad"))]
    if "kit" in kinds: v += [(k, n_, None) for k, n_ in EARLIER.items()]
    v.sort(key=lambda r: (-(r[1] or 0), -(r[2] or 0)))
    return "\n".join(f"<tr><td>{E(k)}</td><td class=n>{a:,}</td><td class=n>{'' if b is None else format(b, ',')}</td></tr>" for k, a, b in v[:n])

def kwsum(kinds):
    v = [x for x in kw.values() if x["kind"] in kinds and x.get("n") is not None]
    return len(v), sum(1 for x in v if x["n"]), sum(x["n"] for x in v), sum(x.get("broad") or 0 for x in v)

def build(body_extra: dict):
    t = (HERE / "report/template.html").read_text()
    vals = dict(groups=rows_groups(), pages=rows_pages(), top=rows_top(), kits=rows_kits(),
                kw_kit=rows_kw({"kit", "brand-kit"}, 14), kw_deal=rows_kw({"deal", "brand-deal", "price"}, 12), kw_code=rows_kw({"code"}, 10),
                n_offers=len(offers), n_go=len(go), tot_answer=tot_answer, browsers=len(clickers),
                one_click=sum(1 for r in clickers if r["n"] == 1), **body_extra)
    for k, v in vals.items(): t = t.replace("{{" + k + "}}", str(v))
    left = re.findall(r"\{\{\w+\}\}", t)
    assert not left, left
    (HERE / "report/offer-table.html").write_text(t)
    print("wrote report/offer-table.html", len(t))

if __name__ == "__main__":
    pass

# ---- prose for the 2026-11-17 read (edit here, numbers above are computed) ----
def prose():
    nk, nk_v, _, _ = kwsum({"kit"}); nd, nd_v, _, _ = kwsum({"deal"}); nc, nc_v, _, _ = kwsum({"code"})
    ab = G["ALLPOWERS and BLUETTI kits (station + panel)"]; a = sum(o["answer"] for o in ab)
    miss = [o for o in kits if not o["ours"] and o["brand"] in ("ALLPOWERS", "BLUETTI")]
    lead = (f"Station-plus-panel kits from ALLPOWERS and BLUETTI are {len(ab)} of our {len(go)} tracked offers and take "
            f"{a} of the {tot_answer} buy-link clicks ChatGPT hands over. Those two stores show about {len(miss)} more kits we don't list, "
            f"and we have only 5 kit comparison pages.")
    sales_text = ("22 sales: BLUETTI 14, ALLPOWERS 7, Mobile Pixels 1. Seven arrived with a click of ours, four of them on kits. "
                  "Twelve BLUETTI sales had no click; nine of those equal one of our listed prices less exactly 5%, the size of our code, "
                  "and two ALLPOWERS sales carry the code DEALECTRIC10. So about half of all sales came through a code alone. "
                  "The amounts don't say whether the code buyers bought a kit or a single unit: one matches only a kit, three only a single unit, five match both.")
    counts_text = (f"Platforms can size the main phrases and nothing below them. Of {nk} kit variants (by size, use, brand and model) "
                   f"{nk_v} had any exact count; of {nd} deal phrases, {nd_v}; of {nc} brand code phrases, {nc_v}. "
                   "The countable ones are the heads: \"solar generator with panels included\" (about 4,200 searches on Microsoft Ads' scale, from the earlier pull), "
                   "\"solar generators for home use\", and the brand kit names below. "
                   "Our own pages get almost no organic search either: Bing showed the whole site 10 times, and the top Google query had 35 impressions in 28 days. "
                   "So platforms can pick the category, and our logs have to rank the pages inside it.")
    order = """<ol>
<li><strong>The 13 in-stock ALLPOWERS kits we don't list.</strong> Same store, same 10 to 12% code and same shoppers as our three best offers. Each needs a product record, a cart test and a product page, and then joins the kit comparison pages.</li>
<li><strong>BLUETTI's current kits</strong> (Apex 300 and 200, Elite 100 V2, Elite 300, AC200L with panels). About 70 pages; price and stock need reading first.</li>
<li><strong>More kit comparison pages.</strong> Five pages carry 95 visits at a 42% click rate. Cut new ones by size, budget and use (1,000 Wh, 3,000 Wh and up, under $1,000, under $1,500, home backup, RV, camping), about ten, each checked against the existing five so two pages never chase the same search. Platforms can't rank these, so the logs will after a week.</li>
<li><strong>Kits from a third brand, to test whether the pattern travels:</strong> OSCAL (three in stock, 10% code), then Anker SOLIX (113 sets, no code of ours; one where-to-buy chat each first, because a brand this large is likelier to be in ChatGPT's catalog).</li>
<li><strong>Jackery.</strong> "Jackery solar generator" is the largest kit phrase we can count, nine times BLUETTI's, and Jackery sells its kits under that very name. We only link Jackery on Amazon. A direct program is the biggest single lever here; the nudge is already drafted under DLC-140 and needs your yes.</li>
</ol>
<p>Not first: code pages and deal pages as search targets. Their phrases are below what Bing counts. Codes still matter as the way a sale gets credited, so a code in our name at each kit brand stays worth asking for.</p>"""
    return dict(lead=lead, sales_text=sales_text, counts_text=counts_text, order=order)

if __name__ == "__main__":
    build(prose())
