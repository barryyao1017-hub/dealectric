# ALLPOWERS P1800 (1,024 Wh): rivals

Angle 3 of 8. Research date: 2026-10-28. All prices were checked live on 2026-10-28 between about 11:18 and 11:32 PDT unless marked otherwise. Nothing was cart-tested here except the P1800 code price, which comes from our own record.

## Bottom line

The 1 kWh LiFePO4 class is crowded, and the base specs look almost the same: 1,024 Wh, 1,800-2,600 W, about 1 hour on AC, 10 ms UPS. **The spec that decides most pairs is warranty and battery end point per dollar.** The P1800 is the cheapest new unit in stock from a maker store today ($395.10 with code, $0.39/Wh). Against that, it carries the weakest terms in the set:

- **Warranty.** Our record says 24 months. Every big-brand rival offers 5 years: EcoFlow (3 + 2 with app registration on the Classic), Anker, BLUETTI, Jackery (only when bought at jackery.com), and DJI (only when bought from the DJI Store).
- **Battery end point.** The P1800 page rates 3,000+ cycles to 70% remaining. The DELTA 3 Plus, C1000 Gen 2, DJI Power 1000 V2 and Elite 100 V2 are rated 4,000 cycles to 80%.
- **Spec conflicts.** ALLPOWERS's own claims disagree with each other: UPS is ≤10 ms on the store page, 20 ms on the Amazon listing, and 15 ms in the images per our record.

The P1800's real advantages are narrow:

- Price today.
- 650 W solar input, more than the C1000 Gen 2, DELTA 3 Classic, Jackery 1000 v2 and AC180.
- Two 140 W USB-C ports, more than the 100 W units.
- Four AC outlets and a 3,600 W peak.

**Timing matters for Black Friday.** At sale time its price edge has usually disappeared. The C1000 Gen 2 hit $349 on 2025-11-20 and $399.99 on 2026-06-23. The DJI Power 1000 V2 is at $399.98 on Amazon today, and the DELTA 3 Classic hit $399 at Walmart on 2026-06-22. A shopper who can wait until 2026-11-27 will probably get a 5-year-warranty rival for about the P1800's price. That is an inference from past lows, not a forecast I can verify.

## Method

- **Maker prices and stock.** These came from Shopify JSON: `/products/<handle>.js` and `/search/suggest.json`, fetched with curl and a desktop user agent. The stores were iallpowers.com, us.ecoflow.com, jackery.com and pecron.com, plus us.anker.com, the Shopify backend named in Anker's own `agents.md`. Displayed prices were cross-checked against each product page's HTML or JSON-LD where one was served.
  - **BLUETTI** returned 429 or a bot check to curl, so its pages were read with WebFetch.
  - **DJI** has no US product page: www.dji.com/power-1000-v2 returns 404 from this US connection.
- **Specs.** These came from each maker's spec table where the HTML carried one (EcoFlow, Jackery, Pecron, ALLPOWERS). Where it did not, I used the maker's Amazon bullets and detail table: Anker weight, warranty and comparison chart, plus BLUETTI and DJI. The DJI spec sheet came from a New Zealand retailer that reproduces DJI's full sheet, because DJI's own spec page 404s in the US.
- **Amazon.** Prices came from product pages fetched with curl, not checked at the cart. The seller is named because it matters for warranty.
- **Price history.** This came from Slickdeals search results, parsed for title, store and post date. I also used backuppowerhub.com's Black Friday tracker for the 2026-10-06 to 10-08 lows. AliExpress, eBay and refurbished deals are listed separately: they are often grey-market or refurbished, with a different warranty.
- **Which rivals come up.**
  - Reddit came from the PullPush API. A direct query for "allpowers p1800" returned zero comments: the US unit only launched 2026-06-29, and PullPush rate-limited some calls.
  - I counted rival brands in the 100 most recent Reddit comments that mention "allpowers".
  - I also used the Outdoor Life 2026 test roundup, a few lower-trust affiliate roundups and Slickdeals thread volume.
- **Search budget.** 7 WebSearch calls were used.

## The rival set and why

| # | Rival | Evidence that shoppers weigh it against a ~1 kWh station like the P1800 |
|---|---|---|
| 1 | **EcoFlow DELTA 3 Plus** | The only direct "P1800 vs" question found: a r/caravanundcamping post asks owners to compare the P1800 and the DELTA 3 Plus (https://reddit.com/r/caravanundcamping/comments/1x2cfl5/, 2026-10-10). Caveat: that subreddit has three P1800 posts in a month in a similar style, and they may be seeded. EcoFlow is the brand mentioned most (13 of 100) in recent Reddit comments that mention ALLPOWERS (PullPush, accessed 2026-10-28). |
| 2 | **EcoFlow DELTA 3 Classic** | The same 1,024 Wh / 1,800 W / 10 ms UPS spec at $499 from a big brand. Slickdeals has 14 dated deals since 2025-12 (search accessed 2026-10-28). backuppowerhub's tracker lists it first among 1 kWh units (https://backuppowerhub.com/black-friday-power-station-deals/, 2026-09-27, tables checked to 2026-10-28). |
| 3 | **Anker SOLIX C1000 Gen 2** | Outdoor Life's tested roundup names the C1000 "Best for Solar Generators". It tested Gen 1, with Gen 2 "in testing" (https://www.outdoorlife.com/gear/best-portable-power-stations-2026.md, 2026-01-09). It has the most deal threads of any rival: 19 on Slickdeals from 2025-09 to 2026-10. It is #8 in Amazon's Outdoor Generators with 1,764 ratings (https://www.amazon.com/dp/B0FN7MSY4L, accessed 2026-10-28). |
| 4 | **Jackery Explorer 1000 v2** | Outdoor Life covers the 1000 line. An affiliate roundup calls it its editor's choice (https://www.mayfairfarms.com/?p=18754, date not shown, low trust). It has 3,715 Amazon ratings, the most in the set (seen on https://www.amazon.com/dp/B0FN7MSY4L, accessed 2026-10-28), and 20+ dated Slickdeals threads. |
| 5 | **BLUETTI Elite 100 V2** (AC180 as a note) | A 1,024 Wh / 1,800 W twin. We already carry the AC180, which Outdoor Life tested (85% delivered on its dehumidifier test, source above) and which a roundup calls "best overall value" (https://vettedai.netlify.app/reviews/best-portable-power-stations-2026, low trust). BLUETTI is the 2nd most mentioned brand (9 of 100) in Reddit's ALLPOWERS comments. |
| 6 | **DJI Power 1000 V2** | The same price as the P1800 today. Slickdeals has 16 dated DJI Power 1000 / V2 deals from 2026-05 to 2026-10, most at $349-$420. It is #26 in Amazon's Outdoor Generators with 809 ratings (https://www.amazon.com/dp/B0H2MFBDZL, accessed 2026-10-28). |

Left out:

- **Pecron E1000LFP.** The closest budget twin: 1,024 Wh, 1,800 W, $399. It is out of stock at pecron.com today, so it only gets a note. Pecron has 5 of 100 Reddit ALLPOWERS-comment mentions.
- **River 3 Plus.** It is 286 Wh, so it is outside the class.
- **Oukitel P1000 Plus and VTOMAN FlashSpeed 1000.** VTOMAN's US store lists the FlashSpeed 1000 only as "CANADA ONLY" (https://www.vtoman.com/products.json, accessed 2026-10-28), and neither came up in the sources above.
- **OUPES Mega 1 Lite (1,024 Wh, $489 on Amazon).** It appears in Amazon's "compare" strip on the P1800 page. Outdoor Life rated the Mega 1 "Best Value" but did not test the Lite. Unverified, not researched further.

## Comparison table

Prices are from the maker's US store on 2026-10-28, with Amazon in brackets when it differs. $/Wh uses the lowest new, in-stock, maker-authorized price found.

| | **ALLPOWERS P1800** | EcoFlow DELTA 3 Plus | EcoFlow DELTA 3 Classic | Anker SOLIX C1000 Gen 2 | Jackery Explorer 1000 v2 | BLUETTI Elite 100 V2 | DJI Power 1000 V2 |
|---|---|---|---|---|---|---|---|
| Price, 2026-10-28 | $439 at iallpowers.com; $395.10 with ALLPOWERS26 or EXTRA10 (our cart test); [Amazon $419, seller GiarideDirect] | $719 (was $799), **pre-order, ships late November** | $499 (was $599); [Amazon $499, EcoFlow Inc.] | $699.99 at anker.com; [Amazon $499.99 AnkerDirect; a second ASIN $439.99, "only 4 left"] | $519 Dune White / $559 Black; [Amazon $559] | $489 (was $499) at bluettipower.com; [Amazon $499, pre-order "released on November 12, 2026"] | No DJI US store page found; [Amazon $399.98, third-party seller "Yeehui Innovations"; $469.99 "Fly Image Tech"] |
| Capacity | 1,024 Wh | 1,024 Wh | 1,024 Wh | 1,024 Wh | 1,070 Wh | 1,024 Wh | 1,024 Wh |
| $/Wh | **$0.39** (code) / $0.43 | $0.70 | $0.49 | $0.49 (Amazon) / $0.43 (2nd ASIN) / $0.68 (anker.com) | $0.49 | $0.48 | $0.39 (3rd-party seller) |
| Continuous / surge | 1,800 W / 3,600 W | 1,800 W (2,200 W X-Boost) / 3,600 W | 1,800 W (2,600 W X-Boost) / 3,600 W (Amazon title) | **2,000 W** / 3,000 W | 1,500 W / 3,000 W | 1,800 W (2,700 W lifting) / 3,600 W (Amazon title) | **2,600 W** / 4,400 W peak on v1 sheet, V2 peak not captured |
| AC charge | 1,200 W fast mode, 0-80% in about 1 h | 1,500 W, 0-100% in 56 min | 1,400 W, 0-80% in 45 min | 1,600 W, 0-100% in 49 min (enable in app, cells above 20 °C) | 1.58 h standard; 0-100% in 1 h "Emergency Super Charge" | 1,200 W, 0-80% in about 45 min | 0-80% in 37 min, 0-100% in 56 min |
| Max solar | 650 W, XT60, 11-60 V (95 V Voc listed) | **1,000 W** (2 × 500 W, 11-60 V) | 500 W (voltage not on page) | 600 W, 60 V max | 400 W (2 × DC8020, 12-60 V) | **1,000 W**, built-in MPPT (voltage not stated) | **No built-in MPPT.** Needs the separately sold Solar Panel Adapter Module, or the 1.8 kW Solar/Car charger for up to 1,800 W |
| USB-C max | 2 × 140 W | 2 × 140 W | 100 W + 30 W | not found (unverified) | 100 W + 30 W | not stated (unverified) | 2 × 140 W |
| AC outlets | 4 | 6 | not on spec block | not found | 3 | not stated ("11 ports") | 4 (US model) |
| UPS | ≤10 ms on store page; **20 ms on Amazon listing**; 15 ms in images (our record) | <10 ms | 10 ms | <10 ms | not stated on page | 10 ms | 10 ms (Amazon bullet) |
| Cycle rating (end point) | 3,000+ to **≥70%** (store); "4,000+" on Amazon; 4,500 on page per our record | 4,000 to 80%+ | not stated ("10 years") | 4,000 to ≥80% | 4,000 to **70%+** | 4,000+ to 80% (Amazon bullet) | 4,000 to >80% |
| Weight | about 13 kg (our record); 28.7 lb on Amazon | 12.5 kg / 27.6 lb | 12.1 kg | 24.9 lb / 11.3 kg | **10.8 kg / 23.8 lb** | 25 lb | 14.2 kg |
| Warranty | **24 months (our record)**. Store banner says "Up to 5-Year Warranty" and Amazon says "5 year". Not reconciled | 5 years | 5 years (3 standard + 2 with app registration) | 5 years (Amazon detail) | 3 + 2 years ("5-Year Warranty ONLY at jackery.com") | 60 months (Amazon detail) | 3 + 2 years **only from the DJI Store**; Amazon listing says "1 Year Manufacturer" |
| Expandable | none listed | yes, 1-5 kWh with DELTA 3 / DELTA 2 / DELTA 2 Max / DELTA Pro 3 extra batteries | none listed | **no** (Anker FAQ: expansion removed) | none listed | not stated | yes, up to 5 × 2,048 Wh (11,264 Wh) |
| App | Bluetooth / Wi-Fi | app (TOU, storm alert) | Wi-Fi & Bluetooth | Anker app | yes (emergency charge mode needs it) | Wi-Fi & Bluetooth | DJI Home app |

Sources for the table, all accessed 2026-10-28:

- **ALLPOWERS P1800:** https://www.iallpowers.com/products/allpowers-p1800-portable-power-station-1024wh-1800w and its `.js` (published 2026-06-29). Amazon: https://www.amazon.com/dp/B0CLM7YW6C, which also shows "Manufacturer Part Number R1500 LITE", so the listing may share reviews with another model.
- **EcoFlow DELTA 3 Plus:** https://us.ecoflow.com/products/delta-3-plus-portable-power-station. The `.js` was republished 2026-10-20, and the page shows "Pre-order: Ships in late November".
- **EcoFlow DELTA 3 Classic:** https://us.ecoflow.com/products/delta-3-classic-portable-power-station. Amazon: https://www.amazon.com/dp/B0FQVC4RF5.
- **Anker SOLIX C1000 Gen 2:** https://www.anker.com/products/c1000-gen2 (JSON-LD price 699.99, FAQ on expansion) and https://us.anker.com/products/c1000-gen2.js. Amazon: https://www.amazon.com/dp/B0FN7MSY4L (bullets, weight in the comparison chart, warranty) and https://www.amazon.com/dp/B0H7BF7TH8.
- **Jackery Explorer 1000 v2:** https://www.jackery.com/products/jackery-explorer-1000-v2 (Tech Specs block) and its `.js`. Amazon: https://www.amazon.com/dp/B0D7PPG25F.
- **BLUETTI Elite 100 V2:** https://www.bluettipower.com/products/elite-100-v2-portable-power-station and its `.js` (published 2025-06-30). Amazon: https://www.amazon.com/dp/B0F42CSQWG.
- **DJI Power 1000 V2:** Amazon https://www.amazon.com/dp/B0H2MFBDZL and https://www.amazon.com/dp/B0FD9Z5F3S. The DJI spec sheet is reproduced at https://www.actiontech.co.nz/products/dji-power-1000-v2-portable-power-station.

**Notes on the other two:**

- **BLUETTI AC180 (we carry it).** Spec: 1,152 Wh, 1,800 W (2,700 W lifting), 1,440 W AC charging (0-80% in 45 min), 500 W solar, 3,500+ cycles (end point not on page), 35.3 lb, 5-year warranty. UPS is **20 ms** (Amazon bullet).
  - BLUETTI: $499, but "out of stock, expected restock: Late-November" (https://www.bluettipower.com/products/ac180, accessed 2026-10-28).
  - Amazon: $499, sold by Amazon.com and in stock (https://www.amazon.com/dp/B0C1SMJTDT).
- **Pecron E1000LFP.** Spec: 1,800 W / 3,000 W, 1,024 Wh, 1,000 W AC charging (80% in 1 h, full in 1.3 h), 600 W solar (XT60, 11-60 V), 100 W USB-C, UPS with no time stated, 3,500+ cycles to 80%, 13.5 kg, 2 + 1 year warranty, expandable to 4,864 Wh. Price $399 (was $799), **out of stock** (https://pecron.com/products/pecron-e1000lfp-portable-power-station-2000w-1024wh, accessed 2026-10-28).

## Pair by pair: the spec that decides it

**P1800 vs DELTA 3 Classic: warranty per dollar.** The core spec is the same: 1,024 Wh, 1,800 W, 3,600 W surge, 10 ms UPS. The Classic costs $104 more than the P1800 code price and adds 3 more years of warranty from a brand with US retail support (Costco, Walmart and Sam's Club deals). It gives up 150 W of solar (500 vs 650 W) and 40 W of USB-C (100 vs 140 W).
> Buy the DELTA 3 Classic instead if you want a 5-year warranty and will register it in the EcoFlow app. At $499 you pay about $35 per extra year of cover.

**P1800 vs DELTA 3 Plus: expandability and solar.** The Plus takes an extra battery up to 5 kWh, 1,000 W of solar on two inputs, and 1,500 W AC (full in 56 min). It is rated 4,000 cycles to 80%, has a 5-year warranty and 6 AC outlets. It costs $324 more and is pre-order only until late November.
> Buy the DELTA 3 Plus instead if you will ever add a second battery or run more than 650 W of panels.

**P1800 vs Anker SOLIX C1000 Gen 2: continuous output and price history.** The C1000 Gen 2 gives 2,000 W continuous and a 49-minute full recharge. It is rated 4,000 cycles to 80%, has a 5-year warranty and is about 4 lb lighter (24.9 lb). It has no expansion, like the P1800, and less solar (600 W at 60 V max). Amazon's $499.99 is $105 over the P1800 code price. It has repeatedly sold for less than the P1800 does today.
> Buy the C1000 Gen 2 instead if it is within about $50 of the P1800, which is likely around Black Friday. It also wins if a load sits between 1,800 and 2,000 W.

**P1800 vs Jackery Explorer 1000 v2: weight against output.** The Jackery is the lightest unit here (23.8 lb vs about 28.7 lb). It has a 5-year warranty only when bought at jackery.com. But it gives 1,500 W continuous, 3 AC outlets, 400 W solar and 100 W USB-C, and its cycle rating ends at 70%, the same as the P1800's. The P1800 out-specs it everywhere except weight and warranty.
> Buy the Jackery instead if you carry it a lot, your loads stay under 1,500 W, and you buy it from jackery.com for the 5 years.

**P1800 vs BLUETTI Elite 100 V2: solar input and warranty.** The Elite 100 V2 costs $94 more at BLUETTI. For that it adds 1,000 W of solar against 650 W and a 5-year warranty. It is rated 4,000+ cycles to 80% and weighs 25 lb. AC charging is the same class (1,200 W, 80% in 45 min).
> Buy the Elite 100 V2 instead if you charge mainly from panels, or you want the 5-year warranty and a 3-4 lb lighter box.

**P1800 vs DJI Power 1000 V2: output and charge speed against out-of-box solar and warranty channel.** The DJI gives 2,600 W continuous, 80% in 37 min, two 140 W USB-C ports and expansion to 11 kWh, at the same $399.98. But it has no built-in solar MPPT; panels need a separately sold adapter module. Today's Amazon price comes from a third-party seller whose listing says "1 Year Manufacturer". DJI's 3 + 2 year warranty applies to DJI Store purchases, and I found no DJI US store page.
> Buy the DJI instead if you need the most continuous watts or the fastest grid recharge, don't need solar out of the box, and can buy it from an authorized seller.

**Buy the P1800 if:** you want a new 1 kWh unit in stock now, at the lowest maker-store price ($395.10 with code), with more solar input than the Classic, C1000 Gen 2, Jackery or AC180, and with 140 W USB-C. You also need to be comfortable with these trade-offs:

- A 2-year warranty, per our record.
- A 70% battery end point.
- A thin owner record. Reddit has almost no P1800 owners, and the Amazon listing has 212 ratings that may be shared with another model.

## Where the P1800's warranty and 70% end point hurt it

**Warranty.** Five of the six rivals offer 5 years from the maker: EcoFlow, Anker, BLUETTI, and Jackery when bought at jackery.com. DJI offers 3 + 2 years when bought from the DJI Store. Pecron offers 2 + 1. The P1800 is the only unit in the table at 24 months, per our record. On a $400 battery that is meant to sit as home backup, years 3 to 5 are when cells and inverters fail. ALLPOWERS's own pages muddy this further:

- The US store banner says "Up to 5-Year Warranty".
- The Amazon listing says "5-Year Warranty".
- Our record says 24 months.

I could not find a P1800-specific warranty term in the store page's static HTML.

**Cycle end point.**

- "3,000 cycles to ≥70%" is a weaker claim than "4,000 cycles to 80%" (DELTA 3 Plus, C1000 Gen 2, Elite 100 V2, DJI V2). It allows more fade, over fewer cycles.
- Only the Jackery 1000 v2 shares the 70% end point, and it claims 4,000 cycles.
- The page's own figures conflict: 3,000 here, 4,500 elsewhere on the page per our record, and "4,000+" on Amazon.

**Owner sentiment on the brand (Reddit, not P1800-specific).**

- An r/Portable_PowerStation owner says an ALLPOWERS unit "works", but its app and support lag EcoFlow and Anker. They recommend checking Anker first (https://reddit.com/r/Portable_PowerStation/comments/1wo1or7/allpowers_oder_ecoflow_welche_option_passt_zu/pbjgi7c/, 2026-09-23).
- An r/Ecoflow_community commenter accuses ALLPOWERS of overstating performance (https://reddit.com/r/Ecoflow_community/comments/1sp7yuz/i_think_this_is_the_best_value_for_home_backup/oh1wdu9/, 2026-04-19).
- A r/festivals comment says an ALLPOWERS unit bought on Amazon "is already dead" within about two years (https://reddit.com/r/festivals/comments/1twj04b/camping_batterys/oppbkt3/, 2026-06-04).

These are anecdotes.

**UPS.**

- The store page says ≤10 ms, but the Amazon listing says "20ms UPS function".
- A Slickdeals commenter also quotes 20 ms and calls it "not good enough (<10ms preferable)" (https://slickdeals.net/f/19799412, comment 2026-07-28).
- Every rival except the AC180 (20 ms) claims 10 ms or under.

## Deals and launches before Black Friday (2026-11-27)

**Sale calendar, per backuppowerhub:**

- Prime Big Deal Days ran 2026-10-06 and 10-07.
- EcoFlow's fall sale ran 09-20 to 10-18.
- BLUETTI's early fall sale ran until 10-05, then 10-06 to 10-07.
- Jackery's early access ran from 09-21.
- In 2025, Black Friday sales opened about Nov 4-12 and hit their deepest prices around Nov 20 (https://backuppowerhub.com/black-friday-power-station-deals/, 2026-09-27). I found no confirmed 2026 Black Friday start dates per brand.

**New, US-authorized lows (Slickdeals post dates; thread URLs are https://slickdeals.net/f/<id>):**

| Model | Now (2026-10-28) | Recent and notable lows |
|---|---|---|
| **ALLPOWERS P1800** | $439 store / $395.10 with code; Amazon $419 | $359.40 Amazon with clip coupon + code OBP25A77, 2026-07-23 (19799412) |
| Anker C1000 Gen 2 | Amazon $499.99 (2nd ASIN $439.99); anker.com $699.99 | **$349 Amazon 2025-11-20** (18835957); $360 Anker 2025-11-19 (18833353); $399.99 Prime 2026-06-23 (19662933); $429 Amazon Jan-Apr 2026 (19132444, 19400115); $469.99 Amazon 2026-10-07 (20119926); backuppowerhub low $469.99 on 10-08 |
| EcoFlow DELTA 3 Classic | $499 | **$399 Walmart 2026-06-22** (19655739, still marked live); $379.98 Sam's Club bundle 2025-12-14 (18967828); $417 EcoFlow 2026-06-14 (19627269); $474.05 EcoFlow 2026-08-17 (19890912); backuppowerhub low $449 on 10-08 |
| EcoFlow DELTA 3 Plus | $719 (pre-order) | **$420 Costco members 2026-07-14** (19761279); $599 Amazon 2026-03-12 (19298607); backuppowerhub low $669 on 10-06 |
| Jackery Explorer 1000 v2 | $519 / $559; Amazon $559 (with extension cable $499, https://www.amazon.com/dp/B0F6YM7WK2) | $386 Amazon 2025-10-29 (18745831); **$399 Amazon 2026-01-13** (19095484); $399.99 Prime 2026-06-23 (19662963); backuppowerhub low $499 on 10-28 |
| BLUETTI Elite 100 V2 | $489 | **$371.27 Amazon 2026-06-24** (19677795); $375 BLUETTI 2026-04-23 (19450161) |
| DJI Power 1000 V2 | Amazon $399.98 (3rd party) | **$364 Prime 2026-06-23** (19662897); $386.10 2026-05-16 (19529859); $399.98 2026-10-16 (20166606, live). The older DJI Power 1000 (2,200 W) was $349 several times, 2026-06-23 to 08-24 (19662882, 19916850) |
| BLUETTI AC180 (carried) | $499 (BLUETTI OOS; Amazon in stock) | $389 Prime 2026-06-23 (19662954); $399 2026-02-05 (19179328); $409 BLUETTI 2026-03-18 (19320753); backuppowerhub low $449 on 10-06 |
| Pecron E1000LFP | $399, OOS | $303.05 Pecron 2025-11-21 (18849541) |

Grey-market and refurbished deals are not comparable on warranty, but they set the floor shoppers see:

- Jackery 1000 v2 $240-$379 on AliExpress, 2026-06 to 10 (e.g. 19582125, 20082876).
- AC180 $256-$443 on AliExpress, 2026-06 to 09.
- Elite 100 V2 refurbished $258-$340, 2026-08 to 10.
- DELTA 3 Classic refurbished $279-$360 on eBay, 2026-04 to 10, and new on AliExpress $309-$328.

**Read:** at every major sale in the last 12 months, at least one 5-year-warranty 1 kWh unit sold for $349-$420. That is the P1800's price band. Outside sales the P1800 is the cheapest in-stock maker-store option, but its edge over the C1000 Gen 2 on Amazon ($439.99 to $499.99) and the DJI ($399.98) is small.

**Launches and stock events before 2026-11-27:**

- **EcoFlow DELTA 3 Plus.** The standalone unit is on pre-order, "Ships in late November". Its product JSON was republished 2026-10-20. It is unclear whether this is a restock or a revision.
- **BLUETTI.** The Elite 100 V2 Amazon listing says "This item will be released on November 12, 2026" (pre-order, $499), while bluettipower.com sells it now at $489. The AC180 restocks at BLUETTI in late November.
- **Jackery HomePower 1000 v2.** A newer 1,024 Wh / 1,500 W model, shown as "NEW" in Jackery's menu. $549 in Jackery's search JSON (https://www.jackery.com/search/suggest.json?q=homepower%201000, handle `jackery-homepower-1000-v2`, accessed 2026-10-28). backuppowerhub shows $649 now and a $514 low on 10-07. These conflict.
- **Anker.** No new 1 kWh launch found. The C1000 Gen 2 backend listing was republished 2026-04-27.

## Open questions / couldn't verify

- **P1800 warranty.** 24 months (our record) vs "Up to 5-Year" (US store banner) vs "5 year" (Amazon B0CLM7YW6C). I found no P1800-specific term in the static HTML. This matters most for the honest comparison above.
- **P1800 UPS** (≤10 / 15 / 20 ms) and **cycle rating** (3,000 / 4,000 / 4,500). These need one source of truth, ideally the manual.
- **Amazon B0CLM7YW6C** lists "Manufacturer Part Number R1500 LITE", and its ASIN prefix predates the 2026-06-29 US launch. The 212 ratings may not all be P1800 ratings. The seller is "GiarideDirect", and I did not verify its link to ALLPOWERS.
- **Anker C1000 Gen 2.** USB-C max watts and AC outlet count were not found; anker.com renders its specs client-side. Also unverified: whether anker.com's $699.99 drops at checkout with an auto-discount, and whether the $439.99 ASIN B0H7BF7TH8 is the same unit.
- **BLUETTI Elite 100 V2.** Not found: solar voltage range, USB-C max and AC outlet count. bluettipower.com blocks curl.
- **DJI Power 1000 V2.** I found no DJI-run US store page (www.dji.com/power-1000-v2 404s). I could not confirm whether US buyers on Amazon get DJI's 3 + 2 years; the listing says "1 Year Manufacturer". The surge figure and the adapter module's price and solar voltage were not captured.
- **DELTA 3 Classic.** Cycle rating and AC outlet count are not in its spec block. Its 5 years needs app registration.
- **Jackery 1000 v2.** UPS switchover time is not on the spec block.
- **DELTA 3 Plus on Amazon.** The standalone unit was not in search results, only bundles.
- **Reddit.** PullPush returned no "allpowers p1800" comments and rate-limited some calls. The r/caravanundcamping P1800 posts read like seeded content.
- **Outdoor Life.** I found no independent capacity test of the P1800. Outdoor Life tested the DELTA 3, C1000 (Gen 1), AC180 and Jackery 1000 Plus, not the rivals' current versions.
- **ALLPOWERS R1500 LITE** (1,056 Wh, 1,600 W) is ALLPOWERS's own sibling, flagged "Most Chosen" in its US menu. Its standalone price was not in suggest results; kit bundles show as unavailable. Not researched.
