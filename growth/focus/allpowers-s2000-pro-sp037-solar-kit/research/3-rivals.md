# ALLPOWERS S2000 Pro + SP037 kit: rivals (angle 3)

Researched 2026-10-29. Store checks ran from about 06:50 to 07:30 UTC. One of four parallel angles. This file covers which kits a shopper with about $800 to $1,200 weighs against this one, how they compare on verified specs and live US prices, and when to buy something else. Nothing was cart-tested here. The kit's own code prices (ALLPOWERS26 $866.70, BULKRATE $857.07) come from our record and `cart-check-2026-10-29.md`.

## Bottom line

- **The deciding spec is battery chemistry and cycle life per dollar.** The S2000 Pro is the only NMC ("Ternary lithium battery") station in the set, rated 2,500+ cycles to 80%. Every rival is LiFePO4, rated 3,500 to 6,000 cycles.
- **ALLPOWERS's own store undercuts it.** The R2500 V2 + SP037 kit went live on 2026-10-27 at $958, $5 under this kit's $963. It has the same 400 W panel, 1,920 Wh of LiFePO4 (32% more), a 2,500 W inverter and 1,000 W / 12-150 V / 20 A solar input. The catch is weight: the R2500 V2 is 29 kg against the S2000 Pro's 13 kg. Codes were not tested on the R2500 V2 kit.
- **Cross-brand, the closest threat is the Pecron E2400LFP + 2×200 W kit at $1,007.** It has 2,048 Wh LFP, 2,400 W, 400 W of panels and expansion to 9.7 kWh, about $150 over this kit's BULKRATE price. Against it: a 2+1-year warranty, and the kit "Ships after two weeks".
- **What the S2000 Pro kit still wins.**
  - The cheapest 2,400 W inverter here: $0.36 per continuous watt with BULKRATE.
  - The most rated panel watts per dollar outside ALLPOWERS's own store: $2.14 per panel watt.
  - A 13 kg station that one person can lift.
- **The weight case is weaker than it looks.**
  - The 18.5 kg SP037 makes the whole kit 31.5 kg, heavier than the Anker, EcoFlow and Jackery kits.
  - Anker's new SOLIX S2000 (LFP) packs more Wh per kg: 124 against the S2000 Pro's 112.
- **Name collision to flag.** Amazon now sells an "Anker SOLIX S2000 Portable Power Station with 400W Solar Panel" ($1,199.99, 2,010 Wh LFP). An assistant reading "S2000 + 400W panel" could mix the two up.

## Method

- **Which rivals.**
  - Four of the 15 allowed WebSearch calls: kit roundups for "400W panel under $1,200", "under $1,000 with panel", tested-roundup outlets, and "S2000 Pro vs".
  - Two roundups read in full: Outdoor Life's solar-generator picks and pwice.com's October 2026 "under $1,000" list.
  - Reddit through the PullPush archive: 100 comments and 100 posts matching "s2000 pro", plus 11 for "allpowers s2000", filtered to 80 relevant items. Most "s2000 pro" hits are Edifier speakers.
  - Amazon search pages for the kit and two rival kits.
- **Prices and stock.** Live maker-store data on 2026-10-29.
  - Shopify stores (iallpowers.com, us.ecoflow.com, jackery.com, bluettipower.com, pecron.com): `/search/suggest.json` to find kit handles, then `/products/<handle>.js` for each variant's price, compare_at_price and available. Displayed price, pre-order and shipping text came from each product page's HTML.
  - Anker (ankersolix.com, headless): the schema.org offer plus the embedded variant and discount-code data.
  - Amazon: search and product pages fetched with curl. These worked today and are not cart-tested.
- **Specs.** From each maker's US product or kit page, accessed 2026-10-29. Where today's page did not carry a figure, I reused our 2026-10-28 rival files and say so: `growth/focus/allpowers-p1800-1024wh/research/3-rivals.md` (P1800 file), `growth/focus/bluetti-ac200l/research/3-rivals.md` (AC200L file) and `growth/focus/allpowers-sp037-400w-solar-panel/research/3-rivals.md` (SP037 file).
- **Price history.** Slickdeals search results, newest first, with post dates and thread IDs (https://slickdeals.net/f/<id>). Station lows also come from backuppowerhub.com's tracker.
- **Derived figures.** $/Wh, $/panel W, $/inverter W, kit weight and Wh/kg are my arithmetic from the maker figures.
- **Raw files.** `/private/tmp/claude-501/-Users-jiayiyao-Desktop-dealectric/44f11078-b8ab-412e-a42d-cf3b4ee1b7ef/scratchpad/research/s2000-rivals/` (subfolders `js/`, `html/`, `sugg/`, `sd/`, `amz/`, `pp/`).

## The rival set and why

Reddit co-mentions inside the 80 relevant S2000 Pro items: EcoFlow 6, BLUETTI 5, Anker 4, Jackery 2, Pecron 1. That is thin. The S2000 Pro shows up mostly in giveaway posts and Ukrainian blackout threads. A Ukrainian review titled it "the most budget alternative to EcoFlow at 1.5 kWh" (https://reddit.com/r/Portable_PowerStation/comments/1ujgkmq/, 2026-06-30). So the set leans on 2026 roundups, Amazon's kit listings and what sits next to this kit in price.

| # | Rival kit | Why it's in the set |
|---|---|---|
| 1 | **ALLPOWERS R2500 V2 + SP037** (in-house) | It sits on the same store at the same price ($958 against $963), with the same panel. Listed 2026-10-27 (`.js` created_at). The R2500 already has a cross-brand comparison thread: "Which powerstation, Pecron E1500LFP vs Allpowers R2500" (https://reddit.com/r/camping/comments/1qt59sm/, comment 2026-02-01). |
| 2 | **Pecron E2400LFP + 2×200 W** | The cheapest 2 kWh LFP kit with 400 W of panels from a maker store today. Pecron came up in the same r/camping thread above. Earlier r/SolarDIY threads recommend Pecron as a value pick (AC200L file). Amazon sells the E2400LFP + 2×300 W kit at $1,187 (search result, accessed 2026-10-29). |
| 3 | **Anker SOLIX C1000 Gen 2 + 400 W Bifacial** | It matches the panel watts at $999.99. Outdoor Life names the C1000 Solar Generator "Best Portable Solar Generator" (https://www.outdoorlife.com/gear/best-solar-generators.md, published 2022-03-29, modified 2025-02-04, tested Gen 1). pwice.com's October 2026 list makes the C1000 + 200 W its Editor's Choice (https://www.pwice.com/best-solar-generators-under-1000-dollars/, 2026-10-07). Slickdeals has a "C1000 Gen 2 with 400W Solar Panel $799.99" deal (19675161, 2026-06-24). |
| 4 | **EcoFlow DELTA 3 Plus + 220 W** (and its + 400 W variant) | EcoFlow is the most co-mentioned brand. Roundups list the DELTA 3 family with a 220 W bifacial panel as "Best Bundled Panel" (pwice.com, above). Its 400 W variant matches this kit's panel watts. |
| 5 | **BLUETTI Elite 200 V2 + 200 W** (we carry) | A 2 kWh LFP kit at $1,099. BLUETTI is the 2nd most co-mentioned brand. We already carry it. |
| 6 | **Jackery Solar Generator 1000 v2 + SolarSaga 200 W** | The most-recommended kit in the 2026 roundups found: pwice.com #5, "the most frequently recommended" in search summaries, and Talk of the House. At $699 it sits at the bottom of the budget. |

Considered and moved to "Also worth knowing": EcoFlow DELTA 3 Max + 220 W ($1,199), Anker SOLIX S2000 + PS400 ($1,199.99, Amazon), Jackery Solar Generator 1500 v2 ($1,279), ALLPOWERS P1800 + SP037 (we carry), BLUETTI AC180 + 200 W (we carry).

Not researched: DJI Power kits (no DJI US store page, per the P1800 file), VTOMAN, Oukitel. None came up in the roundups or the Reddit sample.

## Comparison table

Prices come from each maker's US store on 2026-10-29 unless the cell says otherwise. "$/Wh" and "$/panel W" use the price in the first row, or the code price where one is given. Kit weight is station plus panel(s).

| | **ALLPOWERS S2000 Pro + SP037** | ALLPOWERS R2500 V2 + SP037 | Pecron E2400LFP + 2×PV200 | Anker SOLIX C1000 Gen 2 + 400 W Bifacial | EcoFlow DELTA 3 Plus + 220 W | BLUETTI Elite 200 V2 + 200 W | Jackery SG 1000 v2 + SolarSaga 200 W |
|---|---|---|---|---|---|---|---|
| Price today | $963 (compare-at $1,999), in stock | $958 (compare-at $1,799), in stock; kit listed 2026-10-27 | $1,007 (compare-at $2,297), available; page says "Ships after two weeks" | $1,399.99 list; **$999.99** with page code WSTDHALL60 (-$400, ends 2026-11-02 07:59 UTC); Amazon $999.99 (B0HJ285W9X) | $919 (page shows "Regular price $899", a $20 rise), **Pre-order, ships in November**; + 400 W panel $1,119, also pre-order | $1,099 (compare-at $1,199), available. Our brief said $1,199; the store is $100 lower today | $699 Black / $719 Dune White (compare-at $879 / $909); `.js` says available, static page HTML shows "Sold Out" labels; Amazon $879 (B0D2L1G66J) |
| After public code | ALLPOWERS26 **$866.70**; BULKRATE, station and panel bought separately, **$857.07** (our cart test 2026-10-29) | Not tested. ALLPOWERS26 would give $862.20 if it applies; BULKRATE on $659 + $299 would give $852.62. Both unverified | None found | Already in the $999.99 | None found | None found | None found |
| Battery Wh, chemistry | 1,451 Wh, **NMC** ("Ternary lithium battery") | 1,920 Wh LiFePO4 | 2,048 Wh LiFePO4 | 1,024 Wh LiFePO4 | 1,024 Wh LFP | 2,073.6 Wh LiFePO4 | 1,070 Wh LiFePO4 |
| Cycle rating, end point | 2,500+ to 80% | 3,500+, end point not stated | 3,500+ to 80% | 4,000 to ≥80% (P1800 file) | Kit page: "3000+ cycles" to 80%. Standalone page: 4,000 to 80%+ (P1800 file). Conflict | 6,000+ to 80% (AC200L file) | 4,000 to **70%+** |
| Continuous / surge | 2,400 W / 4,000 W | 2,500 W / 4,000 W in the spec table; 5,000 W peak in the feature list | 2,400 W / 4,000 W | 2,000 W / 3,000 W (P1800 file) | 1,800 W (2,200 W X-Boost) / 3,600 W (P1800 file) | 2,600 W / 3,900 W lifting (AC200L file) | 1,500 W / 3,000 W |
| Panel included; real-world | SP037 400 W, 18.5 kg, 2-yr. About 300-360 W at a good midday peak (SP037 file); brief says about 320 W | Same SP037 | 2 × PV200 200 W, about 6.9 kg each, Voc 41.4 V. No output test found | 400 W Bifacial (PS400 Bifacial per the SP037 file), 9.9 kg, 5-yr. No independent test found | NextGen 220 W bifacial (175 W rear), 7.0 kg, 12-month warranty. Outdoor Life measured an EcoFlow 220 W at 197 W in sun | SP200L 200 W, 8.14 kg, Voc 24.6 V, 12-month warranty. No test found | SolarSaga 200 W, 6.5 kg, 3+2 yr. Outdoor Life measured 184 W in full sun |
| Max solar input | Page contradicts itself: spec table 1,000 W, 12-150 V, 13 A; FAQ 650 W, 18-70 V, under 18 A | 1,000 W, 12-150 V, 20 A | 800 W total: GX16 port 32-95 V, 700 W, 15 A, plus DC5521 100 W | 600 W, 60 V max (P1800 file) | 1,000 W (2 × 500 W, 11-60 V) (P1800 file) | 1,000 W, 12-60 V, 20 A (AC200L file) | 400 W (2 × DC8020) |
| AC charge | 1,500 W in; "0-100% in 1.5 hours" with AC + solar. AC-only time not stated | 1,500 W in; 0-100% in about 1.5 h ("tested around 97 minutes") | 1,800 W in; full in 1.5 h | 1,600 W; full in 49 min (P1800 file) | 1,500 W; full in 56 min (P1800 file) | 1,800 W; 80% in 1.1 h (AC200L file) | 1.58 h; 1 h in emergency mode |
| Kit weight (station + panel) | 13 kg + 18.5 kg = **31.5 kg (69 lb)**. With the 13.8 kg mono SP037 revision, 26.8 kg | 29 kg + 18.5 kg = **47.5 kg (105 lb)** | 20.5 kg + 13.8 kg = 34.3 kg | 11.3 kg + 9.9 kg = **21.2 kg** | 12.5 kg + 7.0 kg = **19.5 kg** | 24.2 kg + 8.14 kg = 32.3 kg | 10.8 kg + 6.5 kg = **17.3 kg** |
| Station Wh per kg | 112 | 66 | 100 | 91 | 82 | 86 | 99 |
| Warranty, station / panel | 5 yr (page buy box; our record says if registered) / 2 yr | 5 yr (buy box) / 2 yr | **2+1 yr** / not stated | 5 yr / 5 yr | 5 yr / **12 months** | 5 yr / **12 months** | 3+2 yr at jackery.com / 3+2 yr |
| UPS switchover | Time not stated on the page | 15 ms | Time not stated ("UPS Power 1800W Max") | 10 ms | <10 ms (P1800 file) | 15 ms (AC200L file) | Not stated |
| Expandable | Not stated on the page | Not stated | Yes, up to 9,728 Wh (2 × EP3800) | No (P1800 file) | Yes, up to 5 kWh (P1800 file) | No | No |
| **$/Wh** | $0.66 list; **$0.59** BULKRATE | **$0.50** | **$0.49** | $0.98 | $0.90 | $0.53 | $0.65 |
| **$/included panel W** | $2.41 list; **$2.14** BULKRATE | $2.40 | $2.52 | $2.50 | $4.18 ($2.80 for the 400 W variant) | $5.50 ($3.25 for the 2 × 200 W kit at $1,299) | $3.50 |
| $/continuous W | $0.36 BULKRATE | $0.38 | $0.42 | $0.50 | $0.51 | $0.42 | $0.47 |

Column sources (all accessed 2026-10-29 unless noted):

- **S2000 Pro + SP037.**
  - https://iallpowers.com/products/allpowers-solar-generator-kit-2400w-s2000-pro-sp037-400w-solar-panel and `.js` (variant 44977510056089).
  - Station page https://iallpowers.com/products/allpowers-2400w-portable-power-station: spec table, "Ternary lithium battery", 13 kg / 28.66 lb, 2,500+ cycles, FAQ 650 W.
  - One store review says "Generator weights 32lbs" (Elictric J., 2023-03-12, on that page).
  - Panel figures from the SP037 file.
- **R2500 V2 + SP037.**
  - Kit: https://iallpowers.com/products/allpowers-r2500-v2-sp037-400w-solar-panel-2500w-solar-generator-kit and `.js` (variant 67800818614425; created 2026-10-27).
  - Station: https://iallpowers.com/products/allpowers-r2500-v2-portable-power-station-2500w-1920wh and `.js` ($659 standalone, in stock): spec table, 29 kg / 63.93 lb, 15 ms UPS, 3,500+ cycles.
- **Pecron E2400LFP.**
  - Kit: https://pecron.com/products/pecron-e2400lfp-solar-generator-kit and `.js` (variant 44357134713020, $1,007).
  - Station: https://pecron.com/products/pecron-e2400lfp-portable-power-station-2400w-2048wh ($649): spec table, 2+1 years.
  - Panel: https://pecron.com/products/pecron-aurora200-200w-36v-portable-solar-panel ($199, 6.9 kg, Voc 41.4 V).
- **Anker C1000 Gen 2 + 400 W.**
  - https://www.ankersolix.com/products/c1000-gen2: embedded variant G17631A2, "400W Bifacial Solar Panel", $1,399.99; discountCodeApp WSTDHALL60 -$400 to $999.99, 2026-10-23 to 2026-11-02; spec fields UPS 10 ms, warranty 5 years, 24.9 lb.
  - Amazon https://www.amazon.com/dp/B0HJ285W9X ($999.99 in search results).
- **EcoFlow DELTA 3 Plus + 220 W.**
  - Kit: https://us.ecoflow.com/products/delta-3-series-solar-generator-pv220w and `.js`: price, "Pre-order | Ships in November", "3000+ cycles", "12 months for the NextGen 220W".
  - 400 W variant: https://us.ecoflow.com/products/delta-3-series-solar-generator-pv400w ($1,119, pre-order, 12-month panel warranty).
  - Panel: https://us.ecoflow.com/products/nextgen-220w-bifacial-portable-solar-panel (7.0 kg, Voc 21.5 V, 12 months US).
- **BLUETTI Elite 200 V2 + 200 W.**
  - Kit: https://www.bluettipower.com/products/elite-200-v2-sp200l and `.js` ($1,099, compare-at $1,199); the same page shows 53.4 lb / 24.2 kg and a 5-year warranty.
  - Panel: https://www.bluettipower.com/products/bluetti-sp200l-solar-panel-200w (8.14 kg, 24.6 V OCV, 10.8 A Isc, "Warranty: 12 Months").
- **Jackery 1000 v2 + 200 W.**
  - https://www.jackery.com/products/jackery-solar-generator-1000-v2 and `.js`: tech specs, 4,000 cycles to 70%+, 10.8 kg, SolarSaga 200W 6.5 kg, 3+2 years, AC 1.58 h, solar 400 W max.
  - Outdoor Life measurements: https://www.outdoorlife.com/gear/best-solar-generators.md.

## Pair by pair: the spec that decides it

**vs ALLPOWERS R2500 V2 + SP037 ($958). Deciding spec: chemistry and capacity against station weight.** For $5 less, the R2500 V2 kit gives:

- 469 Wh more, in LiFePO4 rated 3,500+ cycles against 2,500.
- 100 W more inverter.
- 20 A solar input against 13 A.
- A stated 15 ms UPS.

It is also the same panel and the same store. The cost is 16 kg more station (29 kg against 13 kg).
> Buy the R2500 V2 kit instead if the station mostly stays put: home backup, a van, a cabin. Stay with the S2000 Pro only if you lift the station often and cycle it rarely. Check first that ALLPOWERS26 or BULKRATE works on the R2500 V2; I did not test it.

**vs Pecron E2400LFP + 2×200 W ($1,007). Deciding spec: LFP Wh per dollar against warranty.** For about $150 over the BULKRATE price you get:

- 597 Wh more, in LFP rated 3,500+ to 80%.
- The same 2,400 W inverter.
- Expansion to 9.7 kWh.
- Two 6.9 kg panels instead of one 18.5 kg panel.

It gives up: a 2+1-year warranty against 5, no stated UPS time, a 7 kg heavier station (20.5 kg), and a two-week ship time.
> Buy the Pecron instead if you want the most LFP capacity with 400 W of panels and might add a battery later, and a 3-year warranty is enough.

**vs Anker SOLIX C1000 Gen 2 + 400 W Bifacial ($999.99 with code to 11-02). Deciding spec: warranty and kit weight against capacity.** It is 1,024 Wh, about 30% less. Its 2,000 W inverter is 400 W less. In return:

- Both pieces carry 5 years.
- The kit is 21.2 kg against 31.5 kg.
- The battery is rated 4,000 cycles to 80%.
- It recharges from the wall in 49 min.

Solar input stops at 600 W and 60 V.
> Buy the Anker instead if you carry the kit, 1 kWh covers your loads, and you want the panel covered for 5 years rather than 2. Buy before 2026-11-02 07:59 UTC: after that the page code ends and the list price is $1,399.99.

**vs EcoFlow DELTA 3 Plus + 220 W ($919) or + 400 W ($1,119). Deciding spec: expandability and UPS against capacity and price.** EcoFlow gives:

- Extra-battery expansion to 5 kWh.
- Sub-10 ms UPS.
- 1,000 W of solar on two inputs.
- A 19.5 kg kit with the 220 W panel.
- A 5-year station warranty.

But it is 1,024 Wh with 1,800 W, both panels carry only 12 months, the 400 W kit costs $262 more than this kit's BULKRATE price, and both kits are pre-order until November.
> Buy EcoFlow instead if you will add a battery later or need its UPS for electronics, and can wait for November shipping.

**vs BLUETTI Elite 200 V2 + 200 W ($1,099). Deciding spec: cycle life and capacity against panel watts.** BLUETTI gives:

- 2,073.6 Wh of LFP rated 6,000+ cycles, the longest in the set.
- A 2,600 W inverter.
- 1,000 W solar input.

But the panel is half the watts (200 W, 12-month warranty), and the station weighs 24.2 kg. Matching 400 W costs $1,299 (Elite 200 V2 + 2×200 W).
> Buy the Elite 200 V2 instead if it is home backup that gets cycled often, and you want the battery that should outlast the rest. Budget for a second panel if solar matters.

**vs Jackery Solar Generator 1000 v2 + SolarSaga 200 W ($699). Deciding spec: price and weight against inverter and capacity.** Jackery gives:

- The lightest kit here: 17.3 kg.
- 3+2 years on both pieces when bought at jackery.com.
- A price $158 under this kit's BULKRATE price.

But it has 1,500 W continuous, a 400 W solar ceiling, 1,070 Wh, and a cycle end point of 70%.
> Buy the Jackery instead if your loads stay under 1,500 W, you carry it, and about $700 is the budget. Buy it at jackery.com: Amazon is $879 today.

**Buy the S2000 Pro + SP037 kit if** you need about 2,400 W of continuous output from a station one person can lift (13 kg), you'll run it occasionally rather than daily, and you want 400 W of panel for under $860 (BULKRATE, to 2026-11-15). Know the trade-offs:

- NMC chemistry and a 2,500-cycle rating, the weakest in the set.
- A 2-year panel warranty.
- A spec page that disagrees with itself on solar input (1,000 W vs 650 W).

## Deals before Black Friday (2026-11-27)

Calendar per backuppowerhub (https://backuppowerhub.com/black-friday-power-station-deals/, page dated 2026-09-27, prices checked 2026-10-28 23:29 ET):

- Black Friday is 2026-11-27 and Cyber Monday 2026-11-30.
- In 2025, early-November sales ran about Nov 4 to 12, and the deepest prices came around Nov 20.
- 2026 brand dates are not confirmed.

Deadlines inside the window:

- Anker's WSTDHALL codes end 2026-11-02 07:59 UTC (ankersolix.com page data).
- BULKRATE expires 2026-11-15 (our record).

| Kit (or its station) | Today, 2026-10-29 | Recent and notable lows (Slickdeals thread ID, post date, store) |
|---|---|---|
| **ALLPOWERS S2000 Pro + SP037** | $963; $857.07 with BULKRATE | No Slickdeals results for "allpowers s2000". Amazon sells only the S2000 Pro + 2 × 100 W kit, at $833.15 (https://www.amazon.com/dp/B09SWSGLQZ). No kit low found |
| ALLPOWERS R2500 (1,920 Wh) | Kit $958; station $659 | Station **$603** (19643778, 2026-06-18); 2,016 Wh R2500 $655 (19099405, 2026-01-14) |
| Pecron E2400LFP | Kit $1,007; station $649 | Station **$597** (18556021, 2025-08-26) |
| Anker C1000 Gen 2 + 400 W | $999.99 (code) | **$799.99** Amazon Prime (19675161, 2026-06-24). The + 200 W + bag kit was $669 (18798208, 2025-11-12; 19118881, 2026-01-20). Station alone: $349 Amazon 2025-11-20 and $469.99 2026-10-07 (P1800 file) |
| EcoFlow DELTA 3 Plus + 220 W | $919, pre-order | No 220 W kit low found. Costco "DELTA 3 Plus + 2 × 60 W" was $549.99-$560 (19035838, 2025-12-30; 19142395, 2026-01-27; 19280751, 2026-03-07). Station alone: $420 Costco 2026-07-14 (P1800 file); tracker low $669 on 2026-10-06 |
| BLUETTI Elite 200 V2 + 200 W | $1,099 | $1,099 Amazon (18403006, 2025-06-25), the same as today. Elite 200 V2 + 350 W $1,051.86 (18873091, 2025-11-25). Station alone **$749** (19671240, 2026-06-23); tracker low $849 on 2026-10-08 |
| Jackery SG 1000 v2 + 200 W | $699 at jackery.com; Amazon $879 | **$551** Amazon Prime (18900340, 2025-11-29); $559 with code (18774487, 2025-11-06); **$599.99** Amazon (19615206, 2026-06-10); $664 Prime Day (20113062, 2026-10-06) |
| EcoFlow DELTA 3 Max + 220 W (note) | $1,199 | **$949.05** Amazon (19310886, 2026-03-16) |

**Read.** Every rival kit with a history has sold $100 to $300 under today's price at a past sale. On that pattern, the Jackery and Anker kits are the likeliest to undercut this kit by Black Friday. I found no price history for the S2000 Pro kit itself, so I can't say whether ALLPOWERS will cut it further. That is an inference from past lows, not a forecast I can verify.

## Also worth knowing (not tabled)

- **EcoFlow DELTA 3 Max + 220 W, $1,199** (page shows "$50 OFF", in stock; the Max Plus variants are "Pre order, Ships in Late October").
  - 2,048 Wh LFP, 2,400 W, 500 W solar, 20.3 kg, 5 yr (3 + 2 with app registration). Its cycle rating is not on EcoFlow's US page (AC200L file).
  - Source: https://us.ecoflow.com/products/delta-3-max-solar-series-generator-pv220w and `.js`.
  - It is $0.59/Wh with a 2 kWh battery but only 220 W of panel. It was $949.05 on Amazon on 2026-03-16.
- **Anker SOLIX S2000 + PS400 Bifacial, $1,199.99 on Amazon** (sold by AnkerDirect, in stock).
  - 2,010 Wh LFP, "10,000-Cycle", 1,500 W / 3,000 W peak, 400 W solar input max, 35.7 lb (16.2 kg), <10 ms UPS, 5-year warranty, part number AS220.
  - Source: https://www.amazon.com/dp/B0GY4HNVWY. ankersolix.com/products/s2000 returns 404.
  - It is lighter per Wh than the S2000 Pro, but its inverter is 900 W smaller. Watch for the "S2000" name collision.
- **Jackery Solar Generator 1500 v2, $1,279** (Explorer 1500 v2 + 2 × SolarSaga 100 W Air; compare-at $1,439; station alone $849).
  - 1,536 Wh LFP, 2,000 W, 6,000+ cycles, 31.97 lb (14.5 kg), UPS "within 0.01 seconds", 0-80% AC in 53 min, 3+2 yr.
  - Source: https://www.jackery.com/products/jackery-solar-generator-1500-v2 and `.js` (available: true; the static HTML shows "Sold Out" labels).
  - It is the closest capacity twin, with LFP at about the S2000 Pro's weight. But the kit is $422 more than this kit's BULKRATE price, for half the panel watts. The station alone ($849) costs about what this whole kit costs with BULKRATE ($857.07), with no panel.
- **ALLPOWERS P1800 + SP037, $731** ($657.90 with ALLPOWERS26; we carry it). 1,024 Wh LiFePO4, 1,800 W. See the P1800 file.
  - It is the cheaper in-house LFP option when 1 kWh is enough.
  - Like the S2000 Pro, its warranty and cycle claims conflict across ALLPOWERS pages.
- **BLUETTI AC180 + 200 W, $769** (compare-at $899; available per `.js`). AC180 + 2 × 200 W is $1,232. Source: https://www.bluettipower.com/products/ac180.js.
- **ALLPOWERS R2500 Plus (2,016 Wh) + SP037, $1,058.** An older listing, now superseded by the $958 R2500 V2 kit. The standalone R2500 Plus shows unavailable (`r2500-400w-solar-panel.js`; suggest results).
- **Anker C2000 Gen 2 + 400 W.**
  - Amazon $1,499.99 (B0HJ31GH9Y, search result).
  - ankersolix.com $2,098.99 with code (variant G17831A8).
  - It was $1,179.99 on Slickdeals (19259131, 2026-02-28). Over budget.

## Open questions / couldn't verify

- **R2500 V2 kit codes.** I did not cart-test ALLPOWERS26 or BULKRATE on the R2500 V2 + SP037 kit or on its parts. The $862.20 and $852.62 figures are arithmetic only. Worth one `mixcart.py` run before we print a "buy this instead" line.
- **R2500 V2 specs.** I could not confirm the cycle end point ("3500+" with no percentage) or the surge figure (4,000 W in the spec table, 5,000 W in the feature list). Warranty is "5-year" in the buy box, the same generic banner the S2000 Pro shows. Registration terms were not checked.
- **S2000 Pro.**
  - The UPS switchover time is not on the page.
  - Weight: 13 kg / 28.66 lb in the spec table and "32lbs" in an owner review. A batteryskills.com review in a search summary says 42.3 lb; I did not fetch that page.
  - Expandability: not stated on the maker page. A search summary of batteryskills says it cannot take extra batteries; unverified.
  - Solar input: 1,000 W / 150 V (spec table) against 650 W / 70 V (FAQ), unresolved.
- **DELTA 3 Plus cycle rating.** The kit pages say "3000+ cycles" and the standalone page (P1800 file) says 4,000 to 80%+.
- **Panel output.** No independent output test was found for the Pecron PV200, the Anker 400 W Bifacial or the BLUETTI SP200L. The Outdoor Life figures for EcoFlow and Jackery panels are older tests, and the EcoFlow test was of the earlier 220 W bifacial.
- **Pecron.** UPS switchover time and panel warranty are not stated. "Ships after two weeks" sits next to the kit variants. The PV200 standalone page shows a "Notify Me When Available" control, so panel stock is unclear.
- **Jackery stock.** `.js` says every variant is available, but the static product HTML shows "Sold Out" labels (also seen 2026-10-28 on the 2000 v2). One browser check would settle it.
- **Anker codes.** WSTDHALL60 comes from the page's embedded discount data, and Amazon shows the same $999.99. Not cart-tested.
- **BLUETTI Elite 200 V2 + 200 W price.** The store is $1,099 today; our brief says $1,199. If our record still shows $1,199, it is stale.
- **Amazon.** Prices come from search and product pages fetched with curl, not the cart. No Amazon listing for the S2000 Pro + SP037 kit itself appeared in search.
- **Reddit.** The PullPush sample is small (80 relevant items after filtering) and full of giveaway posts. Brand co-mention counts are a weak signal.
- **Not researched:** DJI Power kits, VTOMAN, Oukitel, OUPES, and the third-party sellers on Amazon.
