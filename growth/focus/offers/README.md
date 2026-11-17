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
