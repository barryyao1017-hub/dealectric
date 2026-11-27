# 1 kWh class: researched alternatives (DLC-358), read 2026-11-26

All prices below are web reads. We re-read price and stock the same day before publishing.

## What I could and could not read

- **BLUETTI US store, read today.** The Elite 100 V2 page says "expected to ship on 12.25 for orders placed on or after 11.20". The AC180 page says "AC180 currently out of stock, expected restock: Late-November" and "AC180 ships from 12.24". BLUETTI's 350 W panel is the bottleneck for every 350 W kit: the Elite 100 mini page says "350W Solar Panel ships from 12.25". The 200 W panel "ships from 11.18", a date that has already passed. The Pioneer Na page (base unit and all bundles) shows no pre-order text, only "2–5 Business Days Delivery (Except for pre-sale products)". The Premium 100 V2 page says "All others ship as normal".
- **Amazon pages return 503 to WebFetch, and camelcamelcamel returns 403.** I could not read Amazon stock or price directly. Where I give an Amazon price, it comes from one of these:
  (a) our own `src/amazon_prices.json` read of 2026-11-26 22:13–22:16Z, which records price and in_stock for Amazon records we carry;
  (b) our 2026-11-18 best-offer read (`growth/buylink/2026-11-18-bestoffer-*.json`);
  (c) dated deal pages: PopSci, pulled from BLUETTI's Amazon storefront on 2026-11-10; Bob Vila's "early Black Friday Nov 2026" list.
  PopSci lists several BLUETTI Amazon bundles as "pre-order, release Nov 12" or "Nov 18". Those Amazon release dates have passed, while BLUETTI's own store still shows Dec 24–25. **The identical BLUETTI item on Amazon is the strongest candidate for most of this group, but its stock is "could not read" and must be confirmed.**
- **iallpowers.com, growattportable.com and jackery.com returned 429 on every try.** ALLPOWERS dates come from our records. ankersolix.com shows "Price Loading" with no price, and both C1000 Gen 2 kit pages say "Due to high demand, orders are esstimated to ship in early December"; the 200 W bifacial kit also shows "Sold Out".
- **The P1800 bare unit, + SP037 and + 600 W are pre-orders for Dec 7 in our records.** That is inside the 14-day window (before Dec 10), so under RULES they may not need an alternative line at all. I mapped them anyway, in case the date has slipped.

## Candidate specs (maker pages / our records)

| Product | Capacity | Chemistry, cycles | AC cont. / surge | Solar input | Weight | 120/240 V | Spec source |
|---|---|---|---|---|---|---|---|
| BLUETTI Elite 100 V2 (original) | 1,024 Wh | LiFePO4, 4,000+ to 80% | 1,800 W / 2,700 W lifting | 1,000 W, 12–60 V, 20 A | 11.5 kg | 120 V | bluettipower.com/products/elite-100-v2-portable-power-station |
| BLUETTI AC180 (original) | 1,152 Wh | LiFePO4, 3,500+ to 80% | 1,800 W / 2,700 W lifting | 500 W, 12–60 V, 10 A | ~16 kg | 120 V | bluettipower.com/products/ac180 |
| ALLPOWERS P1800 (original) | 1,024 Wh | LiFePO4, 3,000+ to 70% (manual ≥4,000) | 1,800 W / 3,600 W | 650 W XT60, 11–60 V, 13 A | 13 kg | 120 V | iallpowers.com P1800 page + manual (our record) |
| BLUETTI Pioneer Na (original) | 900 Wh | **Sodium-ion**, 4,000+ | 1,500 W / 2,250 W lifting | 500 W, 12–60 V, 10 A | 16 kg | 120 V | bluettipower.com/products/sodium-ion-battery-pioneer-na |
| BLUETTI Elite 100 mini (original) | 1,004.8 Wh | LFP, 6,000+ | 700 W total | 350 W | 10.7 kg | 120 V | bluettipower.com/products/elite-100-mini-portable-power-station |
| Anker SOLIX C1000 Gen 2 | 1,024 Wh | LiFePO4, ≥80% after 4,000 | 2,000 W / 3,000 W | 600 W XT60i, 11–60 V | 11.3 kg | 120 V | ankersolix.com/products/c1000-gen2 |
| DJI Power 1000 V2 | 1,024 Wh | LFP, >80% after 4,000 | 20 A at 120 V (~2,400 W; Amazon title 2,600 W) | SDC input, solar needs DJI adapter | 14.2 kg | 120 V | dji.com Power 1000 V2 specs (our record) |
| Jackery Explorer 1000 v2 | 1,070 Wh | LiFePO4, 4,000 to 70% | 1,500 W / 3,000 W | 400 W (2× DC8020, 16–60 V) | ~10.8 kg | 120 V | jackery.com/products/jackery-explorer-1000-v2 |
| BLUETTI Premium 100 V2 | 1,024 Wh | LiFePO4, 4,000+ to 80% | 1,800 W AC (2,000 W AC+DC) / 3,600 W surge* | 1,000 W, 12–60 V, 20 A | 11.5 kg | 120 V | bluettipower.com/products/bluetti-premium-100-v2-portable-power-station (read today) |
| Growatt INFINITY 2000 PRO | 2,048 Wh | LiFePO4, 4,000 to 80% | 2,400 W / 4,800 W | 1,200 W, 12–60 V | ~23 kg | 120 V (TT-30) | growattportable.com (our record) |

\*Our record for Premium 100 V2 + 200 W says "AC output 2,000 W". BLUETTI's page read today says 1,800 W AC continuous, with 2,000 W only as the AC+DC total. Fix the record.

Chargers: BLUETTI Charger 1 = 560 W alternator charger. Charger 2 = up to 1,200 W from alternator and solar together (BLUETTI).

## Prices and stock read

| Item | Price (web read) | Stock | Source |
|---|---|---|---|
| Anker SOLIX C1000 Gen 2, Amazon B0FN7MSY4L | $469.99 | in stock | our amazon_prices.json, 2026-11-26 22:15Z |
| DJI Power 1000 V2, Amazon B0H2MFBDZL | $469.99 | in stock | same, 22:14Z |
| Jackery Explorer 1000 v2, Amazon B0D7PPG25F | $559 | in stock | same, 22:15Z |
| DYNESS 1536 Wh, Amazon B0GYD6V3JW | $499.99 | in stock | same |
| EcoFlow DELTA 3 / DELTA 3 Plus, Amazon | $599 / $719 | in stock | same (outside ±25% for most originals) |
| BLUETTI Elite 100 V2, Amazon B0F42CSQWG | $498.99 (11-10), $549 (11-18) | could not read; Amazon release Nov 12 | PopSci 11-10; our 11-18 read |
| BLUETTI Elite 100 V2 + 100 W, Amazon B0F4253JB6 | $628.99 | could not read; release Nov 12 | PopSci 11-10 |
| BLUETTI Elite 100 V2 + 200 W, Amazon B0FD3V9LF9 | $729 | could not read | Bob Vila, Nov 2026 |
| BLUETTI Elite 100 V2 + 2×200 W, Amazon B0F42KVW3D | $999 (Nov 2025, no 2026 read) | could not read | PopSci 2025-11-23 |
| BLUETTI Elite 100 V2 + Charger 1, Amazon B0FD3YKV3Q | $699.98 | could not read (no pre-order note) | PopSci 11-10 |
| BLUETTI Elite 100 V2 + Charger 2, Amazon B0G8VZB47Z | $798.99 | could not read; release Nov 12 | PopSci 11-10 |
| BLUETTI Elite 100 mini + 350 W, Amazon B0HCZ6BTLD | $899.99 | could not read (no pre-order note) | PopSci 11-10 |
| BLUETTI AC180, Amazon B0C1SMJTDT (also B0CG3D72QC) | $549 (11-18) / $499 (Bob Vila) | could not read | our 11-18 read; Bob Vila |
| BLUETTI AC180 + 200 W, Amazon B0C2ZCPTNB | $999 (11-18) | could not read | our 11-18 read (+30% vs $769: fails price) |
| BLUETTI AC180 + Charger 2, Amazon B0G8VP3CY8 | $899 | could not read (no note) | PopSci 11-10 |
| BLUETTI AC180 + 200 W + Charger 1, Amazon B0FB8TZDSD | $999.99 | could not read; release Nov 18 | PopSci 11-10 |
| ALLPOWERS P1800, Amazon B0CLM7YW6C | $419 (11-18) | could not read | our 11-18 read |
| Jackery 1000 v2 + 100 W, Amazon B0GVN8VBWS | $639 | could not read | Bob Vila, Nov 2026 |
| Jackery 1000 v2 + 2×100 W, Amazon B0FQJ29HVZ | $749 | could not read | Bob Vila, Nov 2026 |
| Anker C1000 Gen 2 + 2×100 W bifacial (Rakuten) | $809.99 (record 11-21, BF price to 11-30); page shows no price today | ships early December | ankersolix.com page today |
| BLUETTI Premium 100 V2 + 200 W | $1,248 | ships now ("All others ship as normal"; the 200 W panel date has passed) | bluettipower.com today |
| BLUETTI Pioneer Na + 100 W / + 200 W / + 2×200 W / + Charger 1 / + Charger 2 | $849 / $999 / $1,498 / $899 / $999 | ships now (no pre-order text) | bluettipower.com today |
| BLUETTI Elite 100 mini + 100 W / + 200 W / + Charger 1 | $529.99 / $609.99 / $599.99 | ships now | bluettipower.com today (700 W output disqualifies them below) |

## Configuration verdicts

The ±25% band is measured against our record price for each original.

### Bare ~1 kWh unit (Elite 100 V2 $449.99, AC180 $549, P1800 $439)

**Winner: the identical item on Amazon** (BLUETTI Elite 100 V2 B0F42CSQWG; BLUETTI AC180 B0C1SMJTDT; ALLPOWERS P1800 B0CLM7YW6C), provided Amazon shows it shipping now. These rank first under the rules: an identical match, same brand, and it earns. Prices are within band: $498.99–549 is +11–22% on the Elite 100 V2; $549 is 0% on the AC180; $419 is −5% on the P1800.

**Runner-up, and the pick if Amazon shows a later date: Anker SOLIX C1000 Gen 2** (B0FN7MSY4L, $469.99, in stock on our 11-26 read). It beats the DJI Power 1000 V2, which is in stock at the same $469.99. Both are 1,024 Wh LFP rated 4,000 cycles to 80%. The Anker takes 600 W of solar on a standard XT60 port, as the originals do, so a buyer's panels plug straight in. It also has 5 AC outlets at 2,000 W and weighs 11.3 kg. The DJI needs DJI's own SDC adapters for solar or car charging and weighs 14.2 kg. On price, the Anker is +4% against the Elite 100 V2, −14% against the AC180 and +7% against the P1800.

Why not the others: Jackery 1000 v2 is $559 with 1,500 W output; DYNESS 1536 is 1.5 kWh; EcoFlow DELTA 3 and DELTA 3 Plus are $599–719, outside the band for the $439–449 originals. For the AC180, if its Amazon listing is out of stock, the Amazon Elite 100 V2 (same brand, $498.99–549) beats the Anker on rule 4, if it ships now.

Reviews: Anker C1000 Gen 2, tested by CleanTechnica, OutdoorGearLab and Notebookcheck. Elite 100 V2: OutdoorGearLab measured 87% usable; techreviewer.de measured 946 Wh at 500 W. AC180: StorageReview measured 1,030 Wh at 350 W. For the P1800 I found no independent capacity test.

### Unit + ~100 W panel (Elite 100 V2 + 100 W $599.99; AC180 + 100 W $679)

**Winner for both: BLUETTI Elite 100 V2 + 100 W on Amazon** (B0F4253JB6, $628.99; Amazon release Nov 12). That is +5% on the Elite kit, the identical item. On the AC180 kit it is −7%: same brand, 1,800 W, 1 kWh LFP, and BLUETTI sells no AC180 + 100 W on Amazon that I could find.

**Runner-up: Jackery Explorer 1000 v2 + 100 W** (Amazon B0GVN8VBWS, $639). It is +7% and −6% against the two originals, 1,070 Wh LFP and in Amazon's catalog, but it has 1,500 W of output against 1,800 W, and its kit stock could not be read.

Disqualified, ships now: Elite 100 mini + 100 W ($529.99) has 700 W output, too far below 1,800 W. Pioneer Na + 100 W ($849) is +41% and +25.04%, just outside the band, and sodium-ion. Disqualified on price: the Anker C1000 Gen 2 + 2×100 W kit ($809.99) is +35% on the Elite kit. On the AC180 kit it is +19% and ships early December, so it would be the pick if both Amazon listings fail.

### Unit + ~200 W panel (Elite 100 V2 + 200 W $649.99; AC180 + 200 W $769; P1800 + SF200 $638)

**Winner for all three: BLUETTI Elite 100 V2 + 200 W on Amazon** (B0FD3V9LF9, $729 on Bob Vila's Nov 2026 list). That is +12%, +14% and −5% against the three originals: the identical item for the Elite kit, and the same 1,800 W / 1 kWh LFP class for the other two. The AC180 + 200 W's own Amazon listing (B0C2ZCPTNB) read $999 on 11-18, +30%, so it fails the price rule.

**Runner-up: Jackery Explorer 1000 v2 + 2×100 W** (Amazon B0FQJ29HVZ, $749). It is +15%, −3% and +17%, with 200 W of panels but 1,500 W of output.

The Anker C1000 Gen 2 + 2×100 W ($809.99, early December) is the best non-Amazon option for the Elite kit (+25%, at the edge) and the AC180 kit (+5%). It ships sooner than Dec 22/24, so it qualifies as an earlier pre-order. For the P1800 + SF200 it is +27% and fails. For the P1800 + SF200, the original ships Dec 15 and no third-party kit I could verify ships sooner within $478–797. The winner and runner-up rest on Amazon stock I could not read.

### Unit + 350–400 W of panels

- **Elite 100 V2 + 350 W ($1,099, Dec 25).** Winner: **BLUETTI Premium 100 V2 + 200 W** ($1,248, +13.6%). It ships now from BLUETTI, which earns through Awin. It is the same 1,024 Wh LFP and 1,800 W AC with the same 1,000 W solar input: effectively the Elite 100 V2's sibling, though its panel is 200 W instead of 350 W. Runner-up: **Elite 100 V2 + 2×200 W on Amazon** (B0F42KVW3D). It is a better match (the same station, 400 W of panels), but I found no 2026 price ($999 in Nov 2025) and could not read stock. If it reads ≤ $1,374 and ships now, it should replace the winner. A BLUETTI 350 W kit can't stand in, because BLUETTI's 350 W panel itself ships Dec 25. The Elite 100 V2 + 350 W Amazon ASIN (B0FHWFXYM5) is ambiguous: PopSci 2026 lists that ASIN as "Elite 100 V2 with solar charging cable" at $498.99. Do not use it without checking the listing title.
- **Elite 100 mini + 350 W ($999, Dec 25).** Winner: **the identical kit on Amazon** (B0HCZ6BTLD, $899.99, no pre-order note on 11-10, −10%). BLUETTI's own store is waiting on the 350 W panel, so check that Amazon really ships it now. Runner-up: **Premium 100 V2 + 200 W** ($1,248, +24.9%, ships now from BLUETTI). It has more output (1,800 W against 700 W) and the same capacity, but a smaller panel. The Anker C1000 Gen 2 + 2×100 W ($809.99, −19%) ships early December. That beats Dec 25, but ships-now goes first.
- **AC180 + 2×200 W ($1,232, Dec 24).** Winner: **Premium 100 V2 + 200 W** ($1,248, +1%, ships now, same brand, LFP, 1,024 Wh, 1,800 W). Runner-up: **Pioneer Na + 2×200 W** ($1,498, +21.6%, ships now). It matches the 400 W of panels but is sodium-ion, 900 Wh and 1,500 W. I ranked the battery and inverter match (capacity, output, chemistry) above panel wattage, since a second 200 W panel can be added later. Check first: Elite 100 V2 + 2×200 W on Amazon (B0F42KVW3D). It matches on everything, if its price and stock read well.
- **P1800 + SP037 400 W ($698, Dec 7).** Winner: **Elite 100 V2 + 200 W on Amazon** (B0FD3V9LF9, $729, +4%; same 1,800 W and 1,024 Wh LFP, half the panel). Runner-up: Jackery 1000 v2 + 2×100 W ($749, +7%). The Anker kit's "early December" date is not demonstrably sooner than Dec 7, so it does not qualify. The original ships inside the 14-day window, so keeping it with no alternative line is defensible.
- **P1800 + 600 W ($798, Dec 7). None.** No ~1 kWh kit with 400–600 W of panels that I could verify ships now within $599–998. The Elite 100 V2 + 2×200 W on Amazon was $999 in Nov 2025, which is +25.2%, and it has no 2026 read. The nearest 200 W kits (Elite 100 V2 + 200 W at $729; Jackery + 2×100 W at $749) carry a third of the panel wattage. The original ships Dec 7, inside the window.

### Charger bundles

- **Elite 100 V2 + Charger 2 ($759.99; Elite ships 12/25).** Winner: **the identical bundle on Amazon** (B0G8VZB47Z, $798.99, +5%, Amazon release Nov 12). Runner-up: **AC180 + Charger 2 on Amazon** (B0G8VP3CY8, $899, +18%; same brand, same 1,200 W Charger 2, 1,152 Wh). Its stock could not be read, and BLUETTI's own AC180 is out of stock. No verified ships-now option fits: Pioneer Na + Charger 2 ($999) is +31%, and the Elite 100 mini + Charger 1 is 700 W.
- **AC180 + Charger 2 ($899).** Winner: **the identical bundle on Amazon** (B0G8VP3CY8, $899). Runner-up: **Elite 100 V2 + Charger 2 on Amazon** (B0G8VZB47Z, $798.99, −11%, LFP, same charger). If neither Amazon listing ships now, the verified fallback is **Pioneer Na + Charger 2** from BLUETTI ($999, +11%, ships now; sodium-ion, 900 Wh, 1,500 W).
- **AC180 + Charger 1 ($748).** I found no AC180 + Charger 1 on Amazon. Winner: **Elite 100 V2 + Charger 1 on Amazon** (B0FD3YKV3Q, $699.98, −6%, no pre-order note; same brand, same 560 W Charger 1, 1,024 Wh, 1,800 W). Runner-up, verified to ship now: **Pioneer Na + Charger 1** from BLUETTI ($899, +20%; sodium-ion, 900 Wh, 1,500 W; no pool record, but the BLUETTI store earns through Awin).
- **AC180 + Charger 1 + 200 W ($1,018).** Winner: **the identical bundle on Amazon** (B0FB8TZDSD, $999.99, −2%, Amazon release Nov 18). Runner-up: **Elite 100 V2 + 200 W + Charger 1 on Amazon** (B0FD3VVPS3). I have no 2026 price for it ($999 in Nov 2025), and its stock could not be read.

### Two-unit pack (AC180 × 2, $998). None.

No two-unit 1 kWh pack from any brand ships now that I could find; Jackery's 2-packs are 2 kWh-class and gone. The nearest product is a single 2 kWh LFP station: **Growatt INFINITY 2000 PRO** ($799 record, −20%, in stock per our record; 2,048 Wh, 2,400 W, TT-30). It is one unit, though. It covers the total capacity, not the two-places-at-once use, so I list it only as a runner-up for you to judge. Its stock was not re-read today (429).

### Pioneer Na + 350 W ($1,199, Dec 25): sodium-ion

**No other sodium-ion portable power station is sold in the US.** Searches turned up only BLUETTI's Pioneer Na; the one other US sodium-ion maker found (Syntropic Power) makes stationary storage. So the substitute stays inside the Pioneer Na line. The original is late only because BLUETTI's 350 W panel ships Dec 25.

**Winner: Pioneer Na + 2×200 W** ($1,498, +24.9%, ships now). It has the same station, the same chemistry, and 400 W of panels against 350 W, inside the 500 W input limit. **Runner-up: Pioneer Na + 200 W** ($999, −17%, ships now), with less panel. A LiFePO4 kit would not be a fair substitute for a buyer who chose sodium-ion. The point of the Pioneer Na is cold-weather operation: it charges down to −15 °C and discharges at −25 °C with 80% of capacity. LFP stations generally won't charge below 0 °C. So I would not offer LFP here while a same-chemistry kit ships now.

Reviews: TechRadar (Pioneer Na review), PopSci first impressions, Scotsman test.

## Sources

- https://www.bluettipower.com/products/elite-100-v2-portable-power-station (ship 12.25 text, bundle prices, read 11-26)
- https://www.bluettipower.com/products/ac180 (out of stock, ships from 12.24; panel dates)
- https://www.bluettipower.com/products/elite-100-mini-portable-power-station (350 W panel ships from 12.25)
- https://www.bluettipower.com/products/sodium-ion-battery-pioneer-na (bundle prices, no pre-order text)
- https://www.bluettipower.com/products/bluetti-premium-100-v2-portable-power-station (specs, $849 / $1,248 / $1,498)
- https://www.ankersolix.com/products/c1000-gen2-100w-bifacial-solar-panel-2 ("ship in early December")
- https://www.ankersolix.com/products/c1000-gen2-with-200w-bifacial-solar-panel ("Sold Out")
- https://www.popsci.com/?p=793560 (BLUETTI Amazon storefront prices and ASINs, 2026-11-10)
- https://www.bobvila.com/reviews/amazon-early-black-friday-power-station-deals-nov-2026/ (Amazon prices and ASINs, Nov 2026)
- https://www.popsci.com/gear/bluettie-solar-generators-portable-power-station-black-friday-deals-amazon/ (2025 BLUETTI Amazon ASINs)
- https://the-gadgeteer.com/?p=547476 (BLUETTI Amazon prices, updated 2026-11-19)
- Reviews: https://www.outdoorgearlab.com/reviews/camping-and-hiking/power-station/bluetti-elite-100-v2 · https://en.techreviewer.de/bluetti-elite-100-v2-test/ · https://www.popsci.com/gear/bluetti-elite-100-v2-portable-solar-power-station-review/ · https://cleantechnica.com/2025/09/24/the-anker-solix-c1000-gen-2-portable-power-station-cleantechnica-tested/ · https://www.outdoorgearlab.com/reviews/camping-and-hiking/power-station/anker-solix-c1000-gen-2 · https://www.storagereview.com/review/bluetti-ac180-portable-power-station-review · https://www.outdoorgearlab.com/reviews/camping-and-hiking/power-station/jackery-explorer-1000-v2 · https://www.thesolarlab.com/review/bluetti-elite-100-mini · https://www.techradar.com/pro/bluetti-pioneer-na-review · https://www.scotsman.com/recommended/bluetti-review-sodium-ion-pioneer-na-power-5426902
- Sodium-ion market: https://dev.to/sunsee/lifepo4-won-the-power-station-wars-sodium-ion-wants-a-rematch-14nk
