#!/usr/bin/env python3.12
"""Cluster pages, 2026-11-21 (Barry: "create new pages for these three clusters"): keyboards (k1121), dash cams (d1121)
and laptop screen extenders (x1121), the three non-solar clusters with a sale each (Gamakay 11-21, ESR/Vantrue traffic,
Mobile Pixels 11-15).

Barry's brief: 20 candidate questions per cluster in the mix 10 by size or budget, 4 brand-launch, 4 "best X for Y",
2 question pages; the harvest gate decides which become pages, with a floor of twelve pages per cluster. Prices: the
store's Black Friday price today, less our code where the code stacks, and always the lowest price the shopper can pay
through our link (README.md has the per-brand cart reads of 2026-11-21).

The research method is tools/abpage.py through growth/focus/open-pages/openpage.py, unchanged (harvest from the saved
chats, six angle agents, compose, verify, Amazon links for rows with no program, apply with the gates). This file
registers the run's folders and adds, per cluster:

  * a table of the products we link in the cluster's categories (store price, price through our link, code and its
    cart-test date), plus the partner stores' other products read today (no record yet), so a research agent can add a
    record for one that is a real pick;
  * the run's rules: the price rule above, the page type's rule and the cluster's own.

    python3.12 growth/focus/clusters/clusterpages.py harvest  [folder...]   # from growth/evals/runs/<HARVEST_RUN>
    python3.12 growth/focus/clusters/clusterpages.py research [folder...] [--workers 3] [--force]
    python3.12 growth/focus/clusters/clusterpages.py links    [folder...]
    python3.12 growth/focus/clusters/clusterpages.py apply    [folder...]
    python3.12 growth/focus/clusters/clusterpages.py status | table <k1121|d1121|x1121>
"""
from __future__ import annotations

import json
import re
import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "growth/focus/open-pages"))
import openpage as O  # noqa: E402  (patches abpage for per-folder rules, queries and record flags)

A = O.A
RUN = "clusters-1121"
BATCHES = [("growth/focus/ab-harvest-new-2026-11-21-clusters.json", "2026-11-21-clusters-harvest")]
HERE = Path(__file__).resolve().parent
STORES = HERE / "stores-2026-11-21.json"   # partner stores' products with no record, read today
KEEPFILE = HERE / "keep.json"              # folders kept after the harvest read (README.md says why each was kept)
STORE_SKIP = re.compile(r"\((IT|DE|ES|FR|CA|EU|UK)\)|Multilingual|Mystery|Side Dash Cam for|Micro USB|English Version", re.I)

PRICE_RULES = """## Prices on this page (Barry 2026-11-21)
- Every brand here is running a Black Friday sale. Each of our rows shows the lowest price the shopper pays through our
  link on the date read: the store's sale price, less our code where the store takes the code on sale prices. The
  partner reads of 2026-11-21 (the tables below already carry these figures; use them as given):
  * Gamakay: Black Friday sale Nov 19-30, 2026. Its sale prices take no code (GK10, New and GK12 were each rejected in
    the cart on 2026-11-21), so the sale price is the price paid. Never mention a Gamakay code.
  * Lofree: its "Black Friday Month" sale takes 20% off keyboards in the cart with nothing to enter; the product page
    still shows the higher price. Our records carry the page price and the checkout total, and the renderer prints both.
    The price paid (for a budget, and for any comparison) is the checkout total. When a Lofree board is in the table, say
    this once in the after-section with both figures and the date.
  * Vantrue and Mobile Pixels: sale prices on the store, no code. Mobile Pixels' prices change with timed sales (the Trio
    3 Pro was $367.99 on 2026-11-18 and $407.99 on 2026-11-21).
  * DDPAI: Black Friday Mega Sale Nov 16-30; code SAVEBIGBF takes a further 12% off (cart-tested 2026-11-21) and ends
    2026-11-30.
  * Botslab: code AA18 takes 18% off (cart-tested 2026-11-21). FOPO: code FOPO takes 10% off (cart-tested 2026-11-21).
- Rows for products we list use their slug: the renderer prints the store price, the price through our link, the code
  and its cart-test date, so do not restate our prices in cells. In the after-section write our prices as
  {price:<slug>} (store price) or {after:<slug>} (price through our link) instead of a dollar figure, and do not build
  arithmetic on our price that would go stale when a sale ends. A claim that depends on a sale names its end date.
- A partner store's product with no record yet is listed below with the price paid today ("pay"). Add a product record
  for one only when it belongs in this page's table on the question's own terms. The record's price is that "pay" figure
  (for Lofree give the page price as the record's price: the checkout total is added to the record when the page is
  applied); give the store's exact product URL, the variant, the price and the date read.
- Rival rows: the maker's US store price read TODAY (these are Black Friday prices; do not reuse an older figure), else
  its amazon.com listing, each with the date read. Match the exact model and variant, and read the page for pre-order,
  dispatch-date and sold-out notices before quoting a price.
- Never write "lowest price" or "cheapest anywhere": name only the sellers you read. Where you open another seller's
  listing for the exact same model and the price through our link is lower on the date read, say so once in the
  after-section with both prices, both sellers and the date.
- Dealectric does not test units. Say so once, plainly, in the after-section."""

TYPE_RULES = {
    "size": """## This is a size-or-budget page
- The question states a budget, a size (layout, channel count, laptop size, screen count) or both, and the page keeps to
  it. Budget: every row's price paid on the date read is at or under it; for our rows that is the price through our link.
  Size: the maker states that size or count (say whose figure it is). Say in the after-section where the line was drawn
  and what was left out for being just over it.""",
    "brand": """## This is a brand-launch page for {brand}
- The question was chosen because {brand}, a brand we link, has a product that may honestly win or place on it. Answer
  the general question as asked: the pick is the product that wins it, even when it is not {brand}'s. If no {brand}
  product belongs in the top three on the question's own terms, return status "skip" with the reason.""",
    "bestfor": """## This is a "best X for Y" page
- The use in the question decides the criteria. State the two or three figures that matter for that use and where each
  comes from, then rank on them.""",
    "question": """## This is a question page
- The title and H1 are the shopper's question. The answer's first sentence answers it directly (yes, no, or the
  number), then says which product to buy if they go ahead.""",
}

CLUSTERS = {
    "k1121": {
        "name": "keyboards", "categories": ("keyboard",), "ours": r"gamakay|lofree|tk75|ns75|ns68|tk68|tk101|flow ?(2|lite|84|100)",
        "rules": """## Rules for this page (keyboard cluster run, 2026-11-21)
- The category is mechanical and Hall effect (magnetic switch) keyboards. Layout words mean key counts: 60% (61 keys),
  65% (about 68), 75% (about 82-84), TKL / 80% (87), 96-98% (about 98-101, with a number pad), full size (104+).
- What decides most questions here: for Hall effect boards, rapid trigger with its minimum step, polling rate and scan
  rate as the maker states them, measured latency from a named reviewer where one exists, the switch that ships, and
  which connection modes keep rapid trigger and the high polling rate (many boards drop to 1,000 Hz or lose features on
  2.4 GHz or Bluetooth: say what each maker states). For low-profile boards: switch height and travel, total height,
  layout, battery, Mac support and remapping software.
- Title and H1: the shopper's question in its own plain words, with its size or budget in it; no model numbers and no
  keyboard brand.
- Pick honestly: the board that wins the question, even when it is not ours; our product then wins the segment it
  honestly wins (say which). Among near-ties prefer a product we can link: an approved program, then amazon.com.
- The page needs at least one row from the keyboards we link that belongs on the question's own terms. If none fits,
  return status "skip" with the reason."""},
    "d1121": {
        "name": "dash cams", "categories": ("dash-cam",), "ours": r"vantrue|nexus|n5s|n4 pro|ddpai|z90|n5 pro|botslab|g980h",
        "rules": """## Rules for this page (dash cam cluster run, 2026-11-21)
- A channel is one camera recording at the same time: 1-channel is front only, 2-channel is front plus rear or front
  plus cabin (say which), 3-channel is front, cabin and rear, 4-channel adds a fourth view. State each row's channel
  count and what each camera sees, from the maker's page.
- What decides most questions here: resolution and frame rate per channel when all channels record together (makers
  often quote the front camera alone), the image sensor named by the maker, parking mode and what it needs (a hardwire
  kit or battery pack, sold with the camera or separately: give its price and date), storage (card size supported, or
  built-in memory), heat (supercapacitor against battery) and GPS. Never write that a camera "records in 4K" without
  saying which channel and in which mode.
- Title and H1: the shopper's question in its own plain words, with its channel count or budget in it; no model numbers
  and no dash cam brand.
- Pick honestly: the camera that wins the question, even when it is not ours; our product then wins the segment it
  honestly wins (say which). Among near-ties prefer a product we can link: an approved program, then amazon.com.
- The page needs at least one row from the dash cams we link that belongs on the question's own terms. If none fits,
  return status "skip" with the reason."""},
    "x1121": {
        "name": "laptop screen extenders", "categories": ("portable-monitor",), "ours": r"mobile pixels|duex|trio 3|geminos|glance|fopo",
        "rules": """## Rules for this page (laptop screen extender run, 2026-11-21)
- The category is screens that travel with a laptop: extenders that attach to or stand behind the lid (one, two or three
  added screens), stacked screens that sit above the laptop's own display, and freestanding portable monitors.
- The question's own limit is kept: a laptop size means the maker states that size in its fit range (say whose range it
  is); a count of screens means that count ("dual screen" and "triple" are both read by shoppers as two added screens:
  say which you mean).
- What decides most questions here is whether the screen works on the shopper's laptop at all: native video (USB-C
  DisplayPort Alt Mode, one video-capable port per added screen) against a display driver (DisplayLink or the maker's
  own), and how many external displays the laptop itself drives (base M1, M2 and M3 MacBooks drive one with the lid
  open). State each row's video path and its source; never write that a screen "works with any laptop".
- Title and H1: the shopper's question in its own plain words, with its size, budget or screen count in it; no model
  numbers and no brand of screen.
- Pick honestly: the screen that wins the question, even when it is not ours; our product then wins the segment it
  honestly wins (say which). Among near-ties prefer a product we can link: an approved program, then amazon.com.
- The page needs at least two rows from the screens we link. If fewer than two fit the question, return status "skip"
  with the reason."""},
}


def _all_questions() -> list[dict]:
    out = []
    for qf, _ in BATCHES:
        if (ROOT / qf).exists():
            out += json.loads((ROOT / qf).read_text())["questions"]
    return out


def _questions() -> dict:
    return {q["slug"]: q["prompt"] for q in _all_questions()}


def cluster_of(folder: str) -> str:
    return folder.split("-", 1)[0]


def keep() -> list[str]:
    return json.loads(KEEPFILE.read_text())["keep"] if KEEPFILE.exists() else []


def _chat_files(folder: str) -> list[str]:
    out = []
    for _, run in BATCHES:
        for f in sorted((A.RUNS / run / "chatgpt").glob("*.json")):
            try:
                c = json.loads(f.read_text())
            except ValueError:
                continue
            m = c.get("answer_model") or ""
            if c.get("slug") == folder and m.startswith("gpt-6") and not m.endswith("mini"):
                out.append(str(f))
    return out


def rules_for(q: dict) -> str:
    cl = CLUSTERS[cluster_of(q["slug"])]
    pt = q.get("ptype", "bestfor")
    kind, _, brand = pt.partition(":")
    return "\n\n".join([cl["rules"], TYPE_RULES[kind].format(brand=brand), PRICE_RULES])


def register() -> None:
    for q in _all_questions():
        kind = q.get("ptype", "bestfor").partition(":")[0]
        O.PAGES[q["slug"]] = {"qids": [], "query": q["prompt"], "run": RUN, "files": _chat_files(q["slug"]),
                              "rules": rules_for(q), "flags": {"buy_by_name": True, "ptype": kind}}


# ---------------------------------------------------------------- the products we link, for the prompts

def table(cluster: str) -> str:
    import products as P
    import build as B
    cl = CLUSTERS[cluster]
    lines = []
    for p in P.PRODUCTS:
        if p.get("category") not in cl["categories"] or p.get("in_stock") is False or p.get("price") is None \
                or p["slug"] in getattr(P, "RETIRED", ()):
            continue
        price = float(p["price"])
        c, saving, after, tested = B.best_offer(p)
        link = f"${price:,.2f} through our link (no code applies today)"
        d = B.deal(p) or {}
        if d.get("auto_total") is not None and d["auto_total"] < price:   # the store's sale comes off at checkout by itself
            link = (f"${d['auto_total']:,.2f} at checkout through our link: {p['brand']}'s {d['name']} sale takes it off in the cart "
                    "with nothing to enter (cart read 2026-11-21); the product page shows the store price")
        if c:
            t = B.last_test(c, p)
            on_this = bool(t and t["product"] == p["slug"])
            link = (f"${after:,.2f} with code {c['code']} applied by the link "
                    + (f"(cart test on this product {tested})" if on_this else f"(code passed {tested} on another {p['brand']} product)"))
        lst = f", list ${float(p['list_price']):,.2f}" if p.get("list_price") else ""
        specs = "; ".join(f"{a}: {b}" for a, b in p.get("specs", [])[:5])
        lines.append((price, f"{p['slug']} | {p['name']} | store price ${price:,.2f}{lst} (read {p.get('verified', 'see record')}) | "
                             f"link price {link} | {specs[:420]}"))
    lines.sort()
    out = "\n".join(x[1] for x in lines)
    if STORES.exists():
        rows = json.loads(STORES.read_text())
        items = [r for r in rows["items"] if r["cluster"] == cluster and r["available"] and not STORE_SKIP.search(r["title"])]
        out += (f"\n\n## Partner stores' other {cl['name']}, no record yet (program | product | variant | listed price | list "
                "price | pay today before any code | in stock | url | variant id), in-stock items only, read " + rows["read"] + "\n"
                + "\n".join(f"{r['program']} | {r['title']} | {r['variant']} | ${r['price']} | {('$' + r['list']) if r['list'] else '-'} | "
                            f"${r['pay']} | {'yes' if r['available'] else 'no'} | {r['url']} | {r['variant_id']}" for r in items))
    return out


def _patch() -> None:
    orig = A._ours_list
    current = threading.local()   # research builds prompts for several folders at once

    def ours_list() -> str:
        cl = getattr(current, "cluster", None)
        if not cl:
            return orig()
        return (orig() + f"\n\n## {CLUSTERS[cl]['name'].capitalize()} we link (slug | name | store price | link price | specs), read "
                + A.today() + "\n" + table(cl))
    A._ours_list = ours_list

    qs = {q["slug"]: q for q in _all_questions()}
    orig_angle = A.angle_prompt

    def angle_prompt(slug, letter, h, query):
        current.cluster = cluster_of(slug) if slug in qs else None
        t = orig_angle(slug, letter, h, query)
        return t + ("\n\n" + rules_for(qs[slug]) if slug in qs else "")
    A.angle_prompt = angle_prompt

    orig_compose = A.compose_prompt

    def compose_prompt(slug, h, query, angles, new_page):
        current.cluster = cluster_of(slug) if slug in qs else None
        return orig_compose(slug, h, query, angles, new_page)
    A.compose_prompt = compose_prompt


_patch()
register()


def main() -> int:
    if len(sys.argv) > 2 and sys.argv[1] == "table":
        print(table(sys.argv[2]))
        return 0
    if len(sys.argv) > 1 and sys.argv[1] in ("harvest", "research", "links", "apply") and not [a for a in sys.argv[2:] if not a.startswith("-")]:
        mine = [f for f in (keep() or _questions()) if O.PAGES[f]["files"]]
        sys.argv[2:2] = mine   # default: this run's folders only, never openpage's own
    return O.main()


if __name__ == "__main__":
    sys.exit(main())
