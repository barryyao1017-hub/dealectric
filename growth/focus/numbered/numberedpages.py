#!/usr/bin/env python3.12
"""Numbered "best" pages, 2026-11-26 (Barry, DLC-363): "best <product> <number>" pages for portable monitors /
screen extenders (x1126), keyboards (k1126), dash cams (d1126) and power banks (p1126).

Why this shape: the 11-26 page-shape read (D1 since 10-28) had "best X" pages with a number in the slug at 1.88 ChatGPT
visits per page, the highest non-seasonal shape, and it carried over to dash cams, monitors and power banks.

Barry's rule for this run: the number a page features is not arbitrary. It is the figure buyers in the cluster actually
decide on, at a real breakpoint (researched per cluster on 11-26, notes in README.md), and every product the page
features is an honest recommendation for that question, starting from the products we link.

Same method as growth/focus/clusters/clusterpages.py (tools/abpage.py through openpage.py), with this run's rules.

    python3.12 growth/focus/numbered/numberedpages.py harvest  [folder...]
    python3.12 growth/focus/numbered/numberedpages.py research [folder...] [--workers 3] [--force]
    python3.12 growth/focus/numbered/numberedpages.py links    [folder...]
    python3.12 growth/focus/numbered/numberedpages.py apply    [folder...]
    python3.12 growth/focus/numbered/numberedpages.py status | table <k1126|d1126|x1126|p1126>
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
O.targets = lambda: {}   # openpage's 11-15 targets file lives on the retired work laptop; this run's pages carry their own query and chat files
RUN = "numbered-1126"
BATCHES = [("growth/focus/ab-harvest-new-2026-11-26-numbered.json", "2026-11-26-numbered-harvest")]
HERE = Path(__file__).resolve().parent
STORES = [ROOT / "growth/focus/clusters/stores-2026-11-21.json",   # partner stores' products with no record, read 11-21
          HERE / "stores-2026-11-26.json"]                         # the power bank partner products the 11-26 research named
KEEPFILE = HERE / "keep.json"              # folders kept after the harvest read (README.md says why each was kept)
STORE_SKIP = re.compile(r"\((IT|DE|ES|FR|CA|EU|UK)\)|Multilingual|Mystery|Side Dash Cam for|Micro USB|English Version", re.I)

PRICE_RULES = """## Prices on this page (read 2026-11-26, Black Friday week)
- Each of our rows shows the lowest price the shopper pays through our link on the date read: the store's sale price,
  less our code where the store takes the code on sale prices (the table below already carries cart-tested figures; use
  them as given). Black Friday prices end Nov 30 - Dec 1, 2026 at most stores: a claim that depends on a sale names its
  end date, and a budget page states that a row is under the budget only at the sale price when that is so.
  * Gamakay: Black Friday sale to Nov 30; its sale prices take no code. Never mention a Gamakay code.
  * Lofree: "Black Friday Month" takes 20% off keyboards in the cart with nothing to enter; the record carries the page
    price and the checkout total, and the price paid is the checkout total.
- Rows for products we list use their slug: the renderer prints the store price, the price through our link, the code
  and its cart-test date, so do not restate our prices in cells. In the after-section write our prices as
  {price:<slug>} (store price) or {after:<slug>} (price through our link) instead of a dollar figure.
- A partner store's product with no record yet may be added as a record only when it belongs in this page's table on the
  question's own terms; give the store's exact product URL, the variant, the price and the date read.
- Rival rows: the maker's US store price read TODAY, else its amazon.com listing, each with the date read. Match the
  exact model and variant, and read the page for pre-order, dispatch-date and sold-out notices before quoting a price.
- Never write "lowest price" or "cheapest anywhere": name only the sellers you read.
- Dealectric does not test units. Say so once, plainly, in the after-section."""

TYPE_RULES = {
    "numbered": """## This is a numbered "best" page (Barry 2026-11-26)
- The number in the question is the figure buyers in this category decide on, at a real breakpoint: {why}
- Open the after-section by saying, in one or two sentences, why that number is the line (the breakpoint and its source),
  so a shopper who is not sure they need it can tell. Keep the page to it: every row meets the number as its maker
  states it (say whose figure); name what was left out for being just short of it.
- The ranking inside the line uses the next two figures that matter most to buyers of this category (listed in the
  cluster rules), each with its source.
- A product we link is featured only where it is an honest top pick on these terms. If none of ours places in the top
  three, return status "skip" with the reason rather than bending the ranking.""",
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
    "k1126": {
        "name": "keyboards", "categories": ("keyboard",), "ours": r"gamakay|lofree|tk75|ns75|ns68|tk68|tk101|flow ?(2|lite|84|100)",
        "rules": """## Rules for this page (numbered pages, 2026-11-26)
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
    "d1126": {
        "name": "dash cams", "categories": ("dash-cam",), "ours": r"vantrue|nexus|n5s|n4 pro|ddpai|z90|n5 pro|botslab|g980h",
        "rules": """## Rules for this page (numbered pages, 2026-11-26)
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
    "x1126": {
        "name": "laptop screen extenders", "categories": ("portable-monitor",), "ours": r"mobile pixels|duex|trio 3|geminos|glance|fopo",
        "rules": """## Rules for this page (numbered pages, 2026-11-26)
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
- The page needs at least one row from the screens we link. If none fits the question, return status "skip"
  with the reason."""},
    "p1126": {
        "name": "power banks", "categories": ("power-bank",), "ours": r"aohi|baseus|ugreen|torras|anker|goal ?zero",
        "rules": """## Rules for this page (numbered pages, 2026-11-26)
- Capacity: give mAh and watt-hours as the maker states them (mAh at the cell voltage, usually 3.6-3.85 V); the FAA and
  TSA carry-on line is 100 Wh per battery without airline approval (101-160 Wh needs approval, two at most); a power
  bank never goes in checked bags. Where a reviewer measured delivered capacity, give it with the reviewer's name.
- Output: the most one port gives (and the PD version: PD 3.1 is needed above 100 W, i.e. 140 W for a 16-inch MacBook
  Pro), what the ports give when used together, and recharge input in watts. State which device draws what, from that
  device's maker. Built-in cables and Qi2 / Qi2.2 wireless (15 W or 25 W, and which phones get 25 W) when present.
- Weight in grams or ounces from the maker; size where it decides a pocket or carry-on question.
- Title and H1: the shopper's question in its own plain words, with its number in it; no model numbers and no power bank
  brand.
- Pick honestly: the power bank that wins the question, even when it is not ours; our product then wins the segment it
  honestly wins (say which). Among near-ties prefer a product we can link: an approved program, then amazon.com.
- The page needs at least one row from the power banks we link that belongs on the question's own terms. If none fits,
  return status "skip" with the reason."""},
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
    notes = ("## Research notes for this question (Dealectric's 11-26 desk research: leads to check, not facts to copy; read "
             "every price and spec again yourself)\n" + q["notes"]) if q.get("notes") else ""
    return "\n\n".join(x for x in [cl["rules"], TYPE_RULES[kind].format(brand=brand, why=q.get("why", "")), notes, PRICE_RULES] if x)


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
    for sf in STORES:
        if not sf.exists():
            continue
        rows = json.loads(sf.read_text())
        items = [r for r in rows["items"] if r["cluster"] in (cluster, cluster.replace("1126", "1121")) and r["available"]
                 and not STORE_SKIP.search(r["title"])]
        if not items:
            continue
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
    folders = [a for a in sys.argv[2:] if a in O.PAGES]   # a flag's value ("--workers 3") is not a folder
    if len(sys.argv) > 1 and sys.argv[1] in ("harvest", "research", "links", "apply") and not folders:
        mine = [f for f in (keep() or _questions()) if O.PAGES[f]["files"]]
        sys.argv[2:2] = mine   # default: this run's folders only, never openpage's own
    return O.main()


if __name__ == "__main__":
    sys.exit(main())
