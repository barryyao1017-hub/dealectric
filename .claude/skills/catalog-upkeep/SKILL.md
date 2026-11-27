---
name: catalog-upkeep
description: How Dealectric keeps product stock, ship dates, prices and ships-now alternatives true on every page (the weekly upkeep in tools/upkeep, rules in growth/stock). Use when changing a product's stock or pre-order state, adding or replacing an alternative, editing a page because a product sold out or moved its ship date, running or debugging the weekly upkeep, or reading its report.
---

# Catalog upkeep

The routine is written up in `growth/stock/README.md`; the alternative rules are `growth/stock/RULES.md`. Read both
before acting. In short:

- **Records hold the truth.** `src/products.py`: `in_stock`, `preorder` (the date the product's LAST item ships, e.g.
  "Jan 19, 2027 (the 200 W panel)"), `price`, `verified`, the managed caveat "Checked <date> on <store>: ...", and
  `"alt"` (the chosen alternative, or `{"none": why, "checked"}`). Never hand-edit `docs/`.
- **Read the way a shopper sees it**, on the exact variant we link: product data plus the rendered page in the Agent
  Chrome (localhost:9222), never curl alone for pre-order state (stores mark pre-orders "available").
- **Alternatives**: sold out, or a pre-order more than 14 days out, gets one researched alternative. Order: best
  substitute (same use) → ships now beats a pre-order (a pre-order only if it ships sooner) → lower price within ±25% →
  same brand → earns (our programs or Amazon with our tag). Proof per choice in `growth/stock/<date>/research/`.
  The original's own buy link always opens the original.
- **Pages**: when a product's stock, ship date, price or alternative changes, find every page that mentions it in
  `growth/stock/page-index.json` and reread each page whole. Correct everything about that product that depends on
  those facts (prices and dates, stock lines, "ships now" framing, advice, numbers computed from the price), not just
  the sentence that states them. Keep picks, rows and structure; write for the shopper in the third person.
- **Publish** as the repo's CLAUDE.md says: build under `tools/repolock.py`, commit, push, `bash worker/deploy.sh` when
  the link map changed, check `/go/` links with `curl -A dealectric-linkcheck-bot` (302 expected).

Tools: `python3.12 tools/upkeep/run.py [--brands A,B] [--slugs x,y] [--no-push] [--max-research N]` runs it all;
`read.py`, `classify.py`, `apply.py`, `alts.py`, `pages.py` are its steps. The Claude scheduled task
`dealectric-weekly-upkeep` runs it on Sundays at 10:00.
