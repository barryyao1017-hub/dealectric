#!/usr/bin/env python3.12
"""Kit comparison pages, 2026-11-17 (DLC-293 step 3, Barry: "Yes, step 3"): size and budget variants of the kit pages
that draw ChatGPT visits. Of the kit pages published 11-02..11-04, the size and budget pages drew 27-33 ChatGPT visits
each by 11-17 and the use pages (tent camping, hurricane season, van life, balcony) drew none, so this run builds size
and budget pages only.

The research method is tools/abpage.py through growth/focus/open-pages/openpage.py (harvest from saved chats, research,
Amazon links for rows we have no program for, apply), unchanged. This file registers the run's folders and adds:

  * a table of the kits we link, read from src/products.py and src/coupons.json at prompt time: battery, store price, the
    price through our link (latest cart test), dispatch date, and what the same parts cost bought separately;
  * the run's rules: every row is a kit sold as one listing, within the question's budget or size, with its shipping state.

    python3.12 growth/focus/offers/kitpages.py harvest  [folder...]   # from growth/evals/runs/<HARVEST_RUN>
    python3.12 growth/focus/offers/kitpages.py research [folder...] [--workers 3] [--force]
    python3.12 growth/focus/offers/kitpages.py links    [folder...]
    python3.12 growth/focus/offers/kitpages.py apply    [folder...]
    python3.12 growth/focus/offers/kitpages.py status | kits
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "growth/focus/open-pages"))
import openpage as O  # noqa: E402  (patches abpage for per-folder rules, queries and record flags)

A = O.A
RUN = "kits-1117"
HARVEST_RUN = "2026-11-17-kits-harvest"
QUESTIONS = ROOT / "growth/focus/ab-harvest-new-2026-11-17-kits.json"

KIT_RULES = """## Rules for this page (kit comparison run, 2026-11-17)
- This is a KIT page. Every row is a power station sold together with its solar panels as ONE listing at ONE price (a
  kit or bundle), not a station plus panels the shopper assembles. A rival's row is that maker's own bundle listing
  (maker's US store, else its amazon.com listing), with the bundle's price and the date it was read.
- The question states a budget or a size, and the page keeps to it. Budget: every row's price on the date read is at or
  under the budget. For our kits use the price the shopper pays through our link ("link price" in the table "Kits we
  link" below, the cart-tested code price), and state the store price beside it. Size: battery within about 20% of the
  stated Wh, or AC output at or above the stated watts. Leave out kits outside the line and say in the after-section
  where the line was drawn.
- "Kits we link" below is today's read of the stores (price, link price, dispatch date, the same parts bought
  separately). Use these figures for our rows as given; do not replace them with a reviewer's or an older price.
- Shipping is part of the answer: many kits are pre-orders with a dispatch date. Give each row's shipping state in a
  column, with its source and date. The pick must ship now, unless nothing in the range does. When the best value is a
  pre-order, the short answer still names a kit that ships now as the pick and names the pre-order with its dispatch date
  as the cheaper or larger option for a shopper who can wait.
- Columns that suit kits: price per Wh at the link price; hours of full sun to refill from the kit's own panels at their
  rated output (battery Wh / panel W, labelled as arithmetic at rated output; real output is lower); what the kit saves
  or costs against the same parts bought separately at the same store on the same day.
- Dealectric does not test units. Say so once, plainly, in the after-section.
- Title and H1: the shopper's question in its own plain words with the budget or size in it; no model numbers.
- Pick honestly: the kit that wins the question at this budget or size, even when it is not ours; our kit then wins the
  segment it honestly wins (say which). Among near-ties prefer a kit we can link: an approved program, then amazon.com.
- Price correction: ALLPOWERS raised the R3500 + SP037 400 W kit to $1,803.10 on 2026-11-17 (the table below has it).
  Angle reports that price it at $1,498, $1,318.24 or about $0.42 per Wh were written from the old figure: recompute
  from the table, and leave the kit out where the new price puts it over the budget.
- The page needs at least two rows from the kits we link. If fewer than two of them fit the budget or size, return
  status "skip" with the reason."""


def _questions() -> dict:
    return {q["slug"]: q["prompt"] for q in json.loads(QUESTIONS.read_text())["questions"]}


def _chat_files(folder: str) -> list[str]:
    out = []
    for f in sorted((A.RUNS / HARVEST_RUN / "chatgpt").glob("*.json")):
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
        O.PAGES[folder] = {"qids": [], "query": prompt, "run": RUN, "files": _chat_files(folder), "rules": KIT_RULES}


# ---------------------------------------------------------------- the kits we link, for the prompts

def _num(s: str) -> float:
    return float(s.replace(",", ""))


def kits_table() -> str:
    import products as P
    import build as B   # the site's own price through the link: best published code, latest passing cart test on the product
    lines = []
    for p in P.PRODUCTS:
        if p.get("category") != "solar-kit" or p.get("in_stock") is False or p.get("price") is None \
                or str(p.get("program") or "").startswith("amazon") or p["slug"] in getattr(P, "RETIRED", ()):
            continue
        text = p["name"] + " " + " ".join(f"{a} {b}" for a, b in p.get("specs", []))
        wh = re.search(r"([\d,]+(?:\.\d+)?) ?Wh", text)
        ac = re.search(r"([\d,]+) ?W(?: continuous|\))", text)
        if not wh:
            continue
        price = float(p["price"])
        c, saving, after, tested = B.best_offer(p)
        link = f"${price:,.2f} (no code)"
        if c:
            t = B.last_test(c, p)
            on_this = bool(t and t["product"] == p["slug"])
            link = (f"${after:,.2f} with code {c['code']} applied by the link "
                    + (f"(cart test on this kit {tested})" if on_this else f"(code passed {tested} on another {p['brand']} product, not yet on this kit)"))
            if on_this and t.get("no_code_total"):
                link += f"; the store's own no-code discount made it ${t['no_code_total']:,.2f} without a code that day"
        ships = "ships now"
        if p.get("preorder"):
            ships = f"pre-order, store dispatch date {p['preorder']}"
            try:   # a record can keep a launch date that has passed: the store page decides whether it ships now
                import datetime as _dt
                if _dt.datetime.strptime(p["preorder"], "%b %d, %Y").date() < _dt.date.today():
                    ships = f"listed as a pre-order with dispatch date {p['preorder']}, which has passed: open the store page for its state today"
            except ValueError:
                pass
        vs = re.search(r"\$[\d,.]+ (?:more|less) than (?:the parts|the [^.]{0,90}) bought separately[^.]*|the same price as the parts[^.]*", p.get("summary", ""))
        lines.append((_num(wh.group(1)), price,
                      f"{p['slug']} | {p['name']} | battery {wh.group(1)} Wh" + (f" | AC {ac.group(1)} W" if ac else "")
                      + f" | store price ${price:,.2f} (read {p.get('verified', 'see record')}) | link price {link} | {ships}"
                      + (f" | vs parts: {vs.group(0)}" if vs else "")))
    lines.sort()
    return "\n".join(x[2] for x in lines)


def _patch() -> None:
    orig = A._ours_list

    def ours_list() -> str:
        return (orig() + "\n\n## Kits we link (station + panels as one listing; slug | name | battery | AC | store price | "
                "link price | shipping | vs parts), read " + A.today() + "\n" + kits_table())
    A._ours_list = ours_list

    orig_angle = A.angle_prompt

    def angle_prompt(slug, letter, h, query):
        t = orig_angle(slug, letter, h, query)
        return t + ("\n\n" + KIT_RULES if slug in _questions() else "")
    A.angle_prompt = angle_prompt


_patch()
register()


def main() -> int:
    if len(sys.argv) > 1 and sys.argv[1] == "kits":
        print(kits_table())
        return 0
    if len(sys.argv) > 1 and sys.argv[1] in ("harvest", "research", "links", "apply") and not [a for a in sys.argv[2:] if not a.startswith("-")]:
        mine = [f for f in _questions() if O.PAGES[f]["files"]]
        sys.argv[2:2] = mine   # default: this run's folders only, never openpage's own
    return O.main()


if __name__ == "__main__":
    sys.exit(main())
