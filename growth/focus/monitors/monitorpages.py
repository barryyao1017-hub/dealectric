#!/usr/bin/env python3.12
"""Laptop screen extender / stacked monitor pages, 2026-11-18 (DLC-290, Barry 11-17: "focus on this cluster").

Evidence for the cluster: the first non-solar sale (2026-11-15, Mobile Pixels Duex Float 2 Pro through our CJ link), and
every human click on a Mobile Pixels link came from ChatGPT. This run asks the cluster's general questions plainly
(growth/focus/ab-harvest-new-2026-11-18-monitors.json, two chats each, no brand or model in the question) and builds a
page for each question where the answers were weak and a product we link honestly wins or places.

The research method is tools/abpage.py through growth/focus/open-pages/openpage.py, unchanged (harvest from the saved
chats, six angle agents, compose, verify, Amazon links for rows with no program, apply with the gates). This file
registers the run's folders and adds:

  * a table of the screens we link (src/products.py, category portable-monitor) with the store price, the price through
    our link and the code's cart-test date, plus the partner stores' other screens read today (no record yet), so a
    research agent can add a record for one that is a real pick;
  * the run's rules.

    python3.12 growth/focus/monitors/monitorpages.py harvest  [folder...]   # from growth/evals/runs/<HARVEST_RUN>
    python3.12 growth/focus/monitors/monitorpages.py research [folder...] [--workers 3] [--force]
    python3.12 growth/focus/monitors/monitorpages.py links    [folder...]
    python3.12 growth/focus/monitors/monitorpages.py apply    [folder...]
    python3.12 growth/focus/monitors/monitorpages.py status | screens
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "growth/focus/open-pages"))
import openpage as O  # noqa: E402  (patches abpage for per-folder rules, queries and record flags)

A = O.A
RUN = "monitors-1118"
BATCHES = [("growth/focus/ab-harvest-new-2026-11-18-monitors.json", "2026-11-18-monitors-harvest")]
STORES = Path(__file__).resolve().parent / "stores-2026-11-18.json"   # partner stores' screens with no record, read today
# Folders kept after the harvest read (see growth/focus/monitors/README.md for why each one was kept or dropped).
KEEP: list[str] = ["m1118-extender", "m1118-under-300", "m1118-triple-under-400", "m1118-16-extender", "m1118-17-extender",
                   "m1118-no-driver"]

RULES = """## Rules for this page (laptop screen extender / stacked monitor run, 2026-11-18)
- The category is screens that travel with a laptop: extenders that attach to or stand behind the lid (one, two or three
  added screens), stacked screens that sit above the laptop's own display, and freestanding portable monitors. A desk
  monitor is in scope only when the question asks for a stacked desk setup.
- Every row is one product a shopper can order today, priced from the maker's US store (else its amazon.com listing)
  with the date read. The question's own limit is kept: a budget means every row's price on the date read is at or under
  it; a laptop size means the maker states that size in its fit range (say whose range it is); a count of screens means
  that count. Say in the after-section where the line was drawn and what was left out.
- "Screens we link" below is today's read of our records and the partner stores. Use those figures for our rows as
  given. Rows for products we list use their slug: the renderer prints the store price, the price through our link, the
  code and its cart-test date, so do not restate our prices in cells. In the after-section write our prices as
  {price:<slug>} (store price) or {after:<slug>} (price through our link) instead of a dollar figure, and do not build
  arithmetic on our price that would go stale when a sale ends: both stores run timed sales.
- The partner stores' screens with no record yet are listed too. Add a product record for one only when it belongs in
  this page's table on the question's own terms (for example the cheapest screen that meets the budget); give the
  record the store's exact product URL, variant, price and the date read.
- Other sellers often show a higher price for the same model than the maker's store does during its sale (the saved
  chats show retailer cards for Mobile Pixels screens above the maker's own price). Where you open another seller's
  listing for the exact same model and the price through our link is lower on the date read, say so once in the
  after-section with both prices, both sellers and the date. Never write "lowest price" or "cheapest anywhere": name
  only the sellers you read.
- What decides most questions here is whether the screen works on the shopper's laptop at all: native video (USB-C
  DisplayPort Alt Mode, one video-capable port per added screen) against a display driver (DisplayLink or the maker's
  own), and how many external displays the laptop itself drives (base M1, M2 and M3 MacBooks drive one with the lid
  open). State each row's video path and its source; never write that a screen "works with any laptop".
- Dealectric does not test units. Say so once, plainly, in the after-section.
- Title and H1: the shopper's question in its own plain words, with its size, budget or screen count in it; no model
  numbers and no brand of screen.
- Pick honestly: the screen that wins the question, even when it is not ours; our product then wins the segment it
  honestly wins (say which). Among near-ties prefer a product we can link: an approved program, then amazon.com.
- The page needs at least two rows from the screens we link. If fewer than two fit the question, return status "skip"
  with the reason."""


def _questions() -> dict:
    out = {}
    for qf, _ in BATCHES:
        if (ROOT / qf).exists():
            out.update({q["slug"]: q["prompt"] for q in json.loads((ROOT / qf).read_text())["questions"]})
    return out


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


def register() -> None:
    for folder, prompt in _questions().items():
        O.PAGES[folder] = {"qids": [], "query": prompt, "run": RUN, "files": _chat_files(folder), "rules": RULES,
                           "flags": {"buy_by_name": True}}


# ---------------------------------------------------------------- the screens we link, for the prompts

def screens_table() -> str:
    import products as P
    import build as B
    lines = []
    for p in P.PRODUCTS:
        if p.get("category") != "portable-monitor" or p.get("in_stock") is False or p.get("price") is None \
                or p["slug"] in getattr(P, "RETIRED", ()):
            continue
        price = float(p["price"])
        c, saving, after, tested = B.best_offer(p)
        link = f"${price:,.2f} through our link (no code for this brand today)"
        if c:
            t = B.last_test(c, p)
            on_this = bool(t and t["product"] == p["slug"])
            link = (f"${after:,.2f} with code {c['code']} applied by the link "
                    + (f"(cart test on this product {tested})" if on_this else f"(code passed {tested} on another {p['brand']} product)"))
        specs = "; ".join(f"{a}: {b}" for a, b in p.get("specs", [])[:5])
        lines.append((price, f"{p['slug']} | {p['name']} | store price ${price:,.2f} (read {p.get('verified', 'see record')}) | "
                             f"link price {link} | {specs[:420]}"))
    lines.sort()
    out = "\n".join(x[1] for x in lines)
    if STORES.exists():
        rows = json.loads(STORES.read_text())
        out += ("\n\n## Partner stores' other screens, no record yet (program | product | variant | price | list price | "
                "in stock | url | variant id), read " + rows["read"] + "\n"
                + "\n".join(f"{r['program']} | {r['title']} | {r['variant']} | ${r['price']} | ${r['list']} | "
                            f"{'yes' if r['available'] else 'no'} | {r['url']} | {r['variant_id']}" for r in rows["items"]))
    return out


def _patch() -> None:
    orig = A._ours_list

    def ours_list() -> str:
        return (orig() + "\n\n## Screens we link (slug | name | store price | link price | specs), read " + A.today() + "\n"
                + screens_table())
    A._ours_list = ours_list

    orig_angle = A.angle_prompt

    def angle_prompt(slug, letter, h, query):
        t = orig_angle(slug, letter, h, query)
        return t + ("\n\n" + RULES if slug in _questions() else "")
    A.angle_prompt = angle_prompt


_patch()
register()


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "screens":
        print(screens_table())
        return 0
    if len(sys.argv) > 1 and sys.argv[1] in ("harvest", "research", "links", "apply") and not [a for a in sys.argv[2:] if not a.startswith("-")]:
        mine = [f for f in (KEEP or _questions()) if O.PAGES[f]["files"]]
        sys.argv[2:2] = mine   # default: this run's folders only, never openpage's own
    return O.main()


if __name__ == "__main__":
    sys.exit(main())
