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

## Uncovered BLUETTI items (2026-11-18, DLC-321 phase 3)

`bluetti_1118.py` composes 109 records from `data/bluetti-uncovered-2026-11-18.json` (the 121 queued items' price, compare-at
price, exact variant, dispatch notes and one-line spec, read on BLUETTI's US store that day); code DEALECTRIC passed in the
cart on all 121 variants (`data/cart-tests-2026-11-18-bluetti.jsonl`). `apply [--group N] [--keep slugs]` writes its marked
block into `src/products.py` and the tests into `src/coupons.json`; it always keeps the slugs in `data/bluetti-live.txt`.
Best-offer entries come from `tools/buycheck.py` (three `growth/buylink/2026-11-18-cheapest-bl*.json` reports),
`bluetti_bestoffer.py hand` and `tools/bestoffer.py decide`. Every entry is a tie with no lowest line: BLUETTI's store
offers a first-time buyer the same 5% for signing up.

Publish rule (coordinator, 2026-11-18): the ChatGPT where-to-buy verdict (run growth/evals/runs/2026-11-18-uncovered,
prices-b/c/d.json) is ours_lowest, the Google Shopping read shows no cheaper seller of the same single item, the listing
does not contradict itself, and a listing that costs more than its parts says so near the top.

Live since 2026-11-18 (55, slugs with prefix `bluetti-`): apex-300-b500k-charger-2-dc-hub-2x350w-50a-kit; 2-apex-200-2-b300k-hub-a1-home-backup-kit; 2-apex-300-2-b300k-hub-a1; apex-300-2-b500k-solarx-4k; 10kwh-rv-kit; apex-300-b300k-charger-2-dc-hub-2x350w-solar-kit; apex-300-2-b300k-solarx-4k; apex-300-b500k-home-backup-kit; apex-300-b500k-solarx-4k; 5kwh-rv-kit; apex-300-b300k-charger-2-dc-hub; fridgepower-3-bc200; 2-fridgepower-2-bc200; apex-300-b500k; apex-200-2-b300k; apex-300-b300k-50a-cable; apex-200-charger-2-2x500w-solar-kit; apex-300-b300k-hub-d1; apex-200-b500k-30a-tt-30-cable; rv5-b4810; apex-200-b500k; apex-200-charger-2-2x350w-solar-kit; fridgepower-2-bc200; apex-300-charger-2-dc-hub; apex-200-charger-2-2x200w-solar-kit; apex-300-solarx-4k; apex-300-charger-1-hub-d1; fridgepower-charger-2-dc-hub-200w-solar-kit; elite-400-charger-2-bundle; apex-300-hub-d1; fridgepower-2-pack; fridgepower-bc200; fridgepower-charger-2-dc-hub; elite-400-charger-1-bundle; apex-200-charger-2-bundle; elite-200-v2-charger-1-200w-solar-kit; elite-200-v2-charger-2-bundle; premium-100-v2-200w-solar-kit; ac180-charger-1-200w-solar-kit; pioneer-na-charger-2-bundle; ac180-2-pack; ac180-charger-2-bundle; elite-100-v2-charger-2-bundle; pioneer-na-100w-solar-kit; ac180-100w-solar-kit; elite-100-mini-charger-1-bundle; elite-30-mini; pv100-fx-flexible-solar-panel-6-pack; 2-b500k-for-ac300-ac200l; b500k-charger-2-dc-hub; b500k-charger-2; 2-b300k-for-apex-300-200; b300k-charger-2-dc-hub; b500k-trolley-2; b300k-charger-2.

Held (54 composed records, not in main; re-check when prices move). Prices are our link price on 2026-11-18.
- ChatGPT verdict beaten (24): apex-300-b300k-charger-1-bundle (un069: RV Parts Giant $2,526.09 vs ours $2,849.05); apex-300-b300k-charger-1-hub-d1-2x350w-solar-kit (un055: Power Fit Shop $3,953 vs ours $4,366.20); apex-300-b300k-trolley-2 (un068: RV Parts Giant $2,484.13 vs ours $2,895.60); elite-10-60w-solar-kit (un116: Walmart $219 vs ours $227.05); premium-200-v2-200w-solar-kit (un087: US Solar Supplier $1,099 vs ours $1,850.60); apex-300-charger-2-bundle (un085: RV Parts Giant $1,758.97 vs ours $1,994.05); elite-100-v2-charger-1-bundle (un112: RV Parts Giant $648.99 vs ours $664.05); elite-300-charger-1-bundle (un100: RV Parts Giant $1,298.99 vs ours $1,329.05); elite-300-charger-2-bundle (un095: RV Parts Giant $1,438.98 vs ours $1,519.05); fridgepower-bc200-display-1 (un089: BLUETTI Official Store $1,649 vs ours $1,756.55); fridgepower-display-1 (un105: RV Parts Giant $899.68 vs ours $949.05); premium-100-v2 (un121: Torven Power $499 vs ours $806.55); premium-200-v2 (un117: Ampere Authority $878.40 vs ours $1,471.55); x60-cpap-power-bank (un122: Outbound Power $359.10 vs ours $379.05); elite-400 (un118: Smart Frontier US $1,399 vs ours $1,424.05); fridgepower (un120: The Outdoor Rescue $569.40 vs ours $901.55); 2-b300k-for-ac200l-ac300 (un142: RV Parts Giant $2,164.19 vs ours $2,278.10); b500k-hub-d1 (un143: RV Parts Giant $1,867.27 vs ours $2,183.10); b4810-51v-100ah (un150: RV Parts Giant $1,498 vs ours $1,614.05); bc200-battery (un155: Footloose Solar $849 vs ours $854.05); 350w-solar-panel (un132: Outstanding Power (PV350D) $549 vs ours $616.55); 350w-solar-panel-2-pack (un126: Marine Parts Giant $1,171.44 vs ours $1,233.10); sp100l-100w-solar-panel (un136: PayMore Great Hills $159.99 vs ours $236.55); pv100-fx-flexible-solar-panel-2-pack (un135: US Solar Supplier $309 vs ours $312.55).
- ChatGPT verdict unsure (12): apex-300-b300k-30a-cable (un076, ours $2,564.05); apex-300-charger-1-bundle (un088, ours $1,804.05); b300k-for-ac500 (un153, ours $1,130.50); 3-b300k-for-apex-300-200 (un138, ours $3,417.15); b500k-for-ac500 (un145, ours $1,946.55); 350w-solar-panel-3-pack (un124, ours $1,849.65); 200w-solar-panel (un134, ours $379.05); 200w-solar-panel-2-pack (un129, ours $758.10); 200w-solar-panel-3-pack (un127, ours $1,137.15); sp100l-100w-solar-panel-2-pack (un133, ours $473.10); sp100l-100w-solar-panel-3-pack (un130, ours $709.65); pv100-fx-flexible-solar-panel-4-pack (un131, ours $625.10).
- ChatGPT verdict tie (3): elite-100-mini-carrying-bag (un115, ours $455.05); pioneer-na-charger-1-bundle (un109, ours $854.05); 2-apex-200-2-b500k-hub-a1 (un047, ours $5,889.05).
- Verdict ours_lowest, but the Google Shopping read shows a cheaper seller of the same single item (5): rv5-power-hub (un119: Outbound Power $1,197.44 vs ours $1,234.05); b300k-for-ac200l-ac300 (un154: RV Parts Giant $871.99 vs ours $1,044.05); b500k-for-apex-300-200 (un151: RV Parts Giant $1,499 vs ours $1,519.05); b500k-for-ac300-ac200l (un147: RV Parts Giant $1,613.34 vs ours $1,709.05); b1232-12v-314ah (un156: Your Tech Haven $749 vs ours $759.05).
- Verdict ours_lowest, but two singles at a seller in the Shopping read cost less than our pack price (2): 2-b500k-for-apex-300-200 (un140, ours $3,038.10); 2-b500k-for-ac500 (un137, ours $3,893.10).
- ChatGPT points to a promo price for the exact bundle or a variant of it (2): apex-300-b500k-hub-d1 (un061, ours $3,324.05); apex-300-b500k-trolley-2 (un060, ours $3,419.05).
- The page has to tell the buyer to ask BLUETTI how the parts connect (a non-expandable station with a B300K or B500K through Charger 2) (2): elite-100-v2-b300k-charger-2-dc-hub (un082, ours $2,089.05); elite-200-v2-b500k-charger-2-dc-hub (un066, ours $3,134.05).
- The listing carries two dispatch dates, "ships from 11.28" and late January (1): sora-500-solar-panel-2-pack (un125, ours $1,613.10).
- Verdict ours_lowest, not in a publish list yet: the two-station bundles of $7,199 and up, each $304 to $404 more than its parts at BLUETTI's own store (3): 2-apex-300-2-b500k-hub-a1 (un046, verdict ours_lowest); 2-apex-300-4-b300k-hub-a1 (un044, verdict ours_lowest); 2-apex-300-4-b300k-hub-a1-2-solarx-4k (un041, verdict ours_lowest).

No record (12):
- The listing's own facts contradict each other or give no usable dispatch date (3): AC180 + 350 W (un103: the 350 W panel "ships from Nov. 9th" and "out of stock, restock late December" in one notice), Premium 100 V2 + 350 W (un098) and Premium 200 V2 + 350 W (un083): the listing's 350 W panel date, Nov. 9th, has passed.
- Not composed, too few facts in the page text (9): the EnergyPro systems un037, un038, un039, un040, un042, un043, un045, un054 (installed home systems sold by consultation) and the MultiCooler fridge un157. Their cart tests passed.

Also on record: the Elite 400's own listing shows a compare-at price ($1,399) below its price ($1,499) and BLUETTI's Google Shopping card shows $1,329.05; long bundle names drop their spec list so the buy link stays near the top (one page, apex-300-b500k-charger-2-dc-hub-2x350w-50a-kit, still ends its buy link at character 436).
