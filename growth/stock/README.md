# Weekly catalog upkeep (all brands)

Barry, 2026-11-27: the ALLPOWERS/BLUETTI stock fix (DLC-358, 2026-11-26) as a routine for every brand. It keeps three
things true on every page: each product's stock state, ship date and price; everything a page says that depends on
them; and, for a product shoppers can't get soon, one researched alternative that ships now.

## What it keeps

- **The product list**, `src/products.py`, as before. Each record also holds its chosen alternative in `"alt"`:
  `{"slug", "checked", "status", "reason", "alt_ships"?, "note"}`, or `{"none": "<why nothing qualified>", "checked"}`.
  `build.py` shows the alternative as one line under the product on every page type (product card, table rows, the
  page's pick, Where-to-buy lists, brand code tables, offers.json) while the product is sold out or a pre-order
  shipping more than 14 days out, and only while the alternative itself still ships (now, or sooner when `alt_ships`
  says so). The product's own buy link always opens the product itself (the DLC-201 redirect is off).
- **The page index**, `growth/stock/page-index.json`, written by every build (`src/pageindex.py`): for each product,
  every page and source line that mentions it (table rows, `{buy:}` placeholders, links, kit items, its name in the
  text, its own record), plus rows that name a brand we have a program with but no product record (`unlisted`).

## When and where it runs

Sundays, as a stage of the daily cart sweep (`tools/codesweep.sh`, launchd 06:37, in `~/code/dealectric`), after the
code tests and gap mining. No new scheduled task. It is a long job (the reads alone take about 40 minutes for ~750
products in three tabs; research and page rewrites add more), and caffeinate keeps the Mac awake. Create
`growth/stock/UPKEEP_OFF` to skip it. By hand: `python3.12 tools/upkeep/run.py [--brands A,B] [--slugs x,y] [--no-push]`.

## Each run (`tools/upkeep/run.py`)

1. **Read every listed product** (`read.py`), in background tabs of the Agent Chrome, the way a shopper sees it:
   - Shopify stores: the listing's product data for the exact variant we link (available, price, compare-at), then
     that variant's rendered page: buy buttons, the text from the product title on, and every line on the page about
     stock, shipping or pre-orders.
   - Amazon: the buy box: price, availability, delivery promise, seller, release date, Add to Cart.
   - Other stores: the rendered page, the same way.
2. **Status** (`classify.py`): rules where they decide (unavailable variant = sold out; Amazon "Currently unavailable"
   = sold out, "released on" = pre-order; no ship note = ships now); otherwise a model reads the notes and must quote
   the one it relied on. A bundle's ship date is its last item's ("the 200 W panel ships Jan 19").
3. **Records** (`apply.py`): in_stock, preorder, price, list_price (where kept), verified, and the managed caveat
   "Checked <date> on <store>: <status>." Amazon reads go to `src/amazon_prices.json`.
4. **Alternatives** (`alts.py`, rules in `growth/stock/RULES.md`):
   - a new sold-out item, or a pre-order over 14 days out, gets research with the full proof and the one-line addition;
   - an alternative already on a record is re-checked, and researched again only if it sold out, became a long
     pre-order or left the ±25% band; "none" verdicts are retried every 4 weeks;
   - an original that ships again loses its alternative.
   The winner is read live before it is used. A winner we don't list gets a minimal record when Amazon or a store we
   have a program with sells it; otherwise it is "pending" for a hand-added record. A pick the research itself calls provisional is not published. At most 15 researches a
   run; the rest carry over to the next week.
5. **Pages** (`pages.py`): for every product whose stock, ship date, price or alternative changed, each hand-written
   page the index lists (comparison entries in `src/gaps.py` / `src/compare.py`, buy boxes in `src/focus.py`, the
   record's own prose) is reread whole, and everything about that product that depends on its stock, price or ship
   status is corrected: prices and their dates, stock and ship-date statements, "ships now" / "can wait" framing,
   advice and comparisons that relied on the old facts, numbers computed from the price. Picks, rows and structure stay.
   Edits are exact replacements that must match once inside the page's own entry; a page whose edits would break the
   file is left alone and listed.
6. **Publish**: rebuild under the repo lock, docs guard, commit, push, deploy the Worker when the link map changed,
   check every changed `/go/` link answers 302, IndexNow the changed pages.
7. **Report**: `growth/stock/<date>/CHANGES.md` (and `report.json`), which the daily update quotes the next morning:
   flags changed; alternatives added, replaced or removed, each with its reason; products with no qualifying
   substitute; pending items; pages edited or failed; products a page mentions that aren't in the list; clicks
   landing on sold-out products in the last 7 days (what keeping the original link costs); model token use.
   Proof for each alternative: `growth/stock/<date>/research/<slug>.md`.

## Costs and limits

- Reads, records, build and publish use no model tokens. The model reads unclear stock notes (cheap model, batches of
  10), researches alternatives and rewrites pages (Fable high, Opus 5.5 high when Fable is out of usage); `report.json`
  records the token use of each run.
- Research and page rewrites need the `claude` CLI signed in on this Mac. When it isn't, the run still reads and
  updates records and lists everything else as pending.
- The daily stock read (`tools/pricecheck.py --stock-out`, DLC-201's flip) keeps running every day between upkeeps.
