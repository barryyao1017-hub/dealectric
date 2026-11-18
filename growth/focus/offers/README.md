# Offer table (2026-11-17)

Picks content by offer instead of by question: which live offers shoppers reach from ChatGPT, which partner kits we
don't list, and what search platforms can count. Plan: artifact "Content Targeting Plan"; result: artifact "Offer Table".

- `offer_table.py`: joins `src/products.py` and `src/coupons.json` to the D1 pulls in `data/` -> `data/offers.json`, prints cuts.
- `store_kits.py`: partner stores' kits with no product record -> `data/uncovered-kits.json` (store lists in `data/stores/`:
  Shopify `/products.json?limit=250`, or the product sitemap for BLUETTI and Anker SOLIX).
- `platform_counts.py`: Bing Webmaster exact and broad counts for kit, deal, price and brand-code phrases -> `data/keywords.json`
  (one caller only; a second caller in parallel gets the key throttled).
- `report.py`: builds `report/offer-table.html` from `report/template.html`.

D1 pulls (from `worker/`, `wrangler d1 execute dealectric --remote --json --command ...`, since 2026-10-29):
- `clicks.json`: `SELECT slug, kind, bot_like, CASE WHEN utm_source='chatgpt.com' THEN 'answer' WHEN referrer LIKE '%utm_source=chatgpt%' THEN 'page' WHEN utm_source<>'' THEN 'othertag' ELSE 'plain' END src, country='US' us, count(*) n, min(substr(ts,1,10)) first, max(substr(ts,1,10)) last FROM clicks WHERE ts>='2026-10-29' GROUP BY slug, kind, bot_like, src, us`
- `landings.json`: `SELECT page, utm_source, count(*) n FROM landings WHERE bot_like=0 AND verified_bot='' AND ts>='2026-10-29' GROUP BY page, utm_source`
- `pageclicks.json`: `SELECT referrer, slug, count(*) n FROM clicks WHERE kind='redirect' AND bot_like=0 AND referrer LIKE '%utm_source=chatgpt%' GROUP BY referrer, slug`
- `clickers.json`: answer-link clicks grouped by user agent, country and network; `sales.json`: `SELECT * FROM sales`.
- `gsc-queries-28d.txt`: Search Console's query report text, read in the Agent Chrome.

## New store products (2026-11-18, DLC-321)

`newproducts_1118.py`: 28 records for the ALLPOWERS kit variants and panels and the OSCAL PowerMax 6000 kits and panels
we did not list (input: the uncovered-items list of 2026-11-18, in-stock items of $150 or more), each with a cart test
of the code on the exact variant that day (`data/cart-tests-2026-11-18-newproducts.jsonl`).
`apply --keep <slugs>` writes its marked block into `src/products.py` and folds the kept slugs' cart tests into
`src/coupons.json`; it can be re-run after a rebase. Then `tools/images.py <slugs>`, the best-offer check
(`tools/buycheck.py`, `tools/bestoffer.py decide` with `growth/buylink/2026-11-18-bestoffer-hand-np.json`,
`growth/codes/2026-11-18-newproducts-carttests.jsonl` from the `cartfile` command and the ChatGPT price rows in
`growth/buylink/2026-11-18-chatgpt-prices-np.json`), which gives each page its opening, and the build.

Published 2026-11-18 (17): the 13 ALLPOWERS and 4 OSCAL items for which ChatGPT's where-to-buy answers
(growth/evals/runs/2026-11-18-uncovered) showed no confirmed same-item price below ours.
Held, records kept in the generator only (11):
- ChatGPT quoted a lower price: S2000 Pro + 2 SF100 ($747, a feed price), P1800 + 2 SF200 ($663), P1800 + 2 SE200
  ($677), P1800 + SE200 ($538.99), SP039 panel ($399). The store's own list still charged $890.15, $837, $798, $618.55
  and $599 when re-read at 12:15Z that day, so those lower figures are older or feed prices, not today's store price.
- near-tie: R2500 V2 + 2 SF200; parts cheaper: R2500 V2 + 2 SF100; unclear OSCAL from-prices: PM400 SE and PM200 SE
  panels; dispatch date only inferred: R2500 V2 + SE160; listing contradicts itself on wattage: SF400 2-pack.
Never given a record (9): 8 pre-orders whose store label read "dispatch: date to be confirmed" (S2000 + 1 to 4 SF100,
R1500 + 2 to 4 SF100, the SE200 panel alone), though their codes passed in the cart; the R3500 + 2 SP039 kit already
had a record.
