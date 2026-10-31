# Open concern research: RV 2kWh under $900 (DLC-114, step 4b, 2026-10-31)

Researched by a Fable 5.1 subagent with web search (skill rule). Prices seen 2026-10-31; "store API" = the brand's
Shopify product JSON read the same day. Full source list at the end.

## Product facts

| Spec | BLUETTI AC200L | BLUETTI Elite 200 V2 |
|---|---|---|
| Capacity | 2,048 Wh LiFePO4 | 2,073.6 Wh LiFePO4 |
| Cycles to 80% | 3,000+ (BLUETTI listings via reviews; US page renders specs as images) | 6,000+ (manual) |
| AC continuous | 2,400 W: 4 × 120 V/20 A + 1 × TT-30 (shares the 2,400 W cap) | 2,600 W, 4 × NEMA 5-20 |
| Power Lifting (resistive only) | 3,600 W | 3,900 W |
| TT-30 RV outlet | **Yes**, but capped by the 2,400 W inverter (≈20 A) | **None** (needs a 5-20P to TT-30R adapter) |
| Solar input | 1,200 W, 12–145 V | 1,000 W, 12–60 V |
| Car input | 12/24 V port (W not stated) | 96 W (12 V) / 192 W (24 V) |
| AC charging | 2,400 W max, 0–80% in 45 min | 1,800 W, 80% in ~1.1 h |
| Weight | 62.4 lb | 53.4 lb |
| Expandable | Yes (B210/B230/B300K) | No |
| UPS switchover | 20 ms (UNVERIFIED on page text) | <15 ms |
| Warranty | 5 years | 5 years |
| Price bluettipower.com | $899 (compare-at $1,599), in stock | $899 |

AC200L status: not on BLUETTI's US discontinued list, still sold on the US store (in stock 10-31); BLUETTI Canada marks
it discontinued; one review site names the AC200PL as successor. Safe wording: "late in its life; no official
replacement named; in stock on bluettipower.com on <date>". Code AFF5OFF passed in BLUETTI's cart 2026-10-30 on both
(subtotal $899, discount $44.95 → $854.05; `src/coupons.json`).

## The field under $900 (1,800–2,330 Wh)

| Unit | Wh / AC W | TT-30 | Solar | Weight | Price (10-31) |
|---|---|---|---|---|---|
| BLUETTI AC200L | 2,048 / 2,400 | Yes | 1,200 W | 62.4 lb | $899 |
| BLUETTI Elite 200 V2 | 2,073.6 / 2,600 | No | 1,000 W | 53.4 lb | $899 |
| Anker SOLIX C2000 Gen 2 | 2,048 / 2,400 (4,000 peak), 10 ms UPS | Yes (TT-30R rated 20 A) | 800 W | 41.7 lb | $899.99 ankersolix.com |
| Renogy PowerStation 2000 | 2,048 / 2,400 (3,600 surge) | Yes ("up to 2,400 W") | 1,200 W | 51.8 lb | $849 renogy.com |
| Oukitel P2001 Plus | 2,048 / 2,400 | No | 500 W | 48.5 lb | $729 |
| Dabbsson DBS2300 Plus | 2,330 / 2,200 | No (only with 2 units in parallel) | 600 W | 53 lb | $899 |
| Jackery Explorer 2000 v2 | 2,042 / 2,200 | No | 400 W | 39.5 lb | $999 (over budget; Amazon sales seen $749) |
| EcoFlow DELTA 2 Max | 2,048 / 2,400 | No | 1,000 W | 50 lb | $1,049 (over budget; flash sales $799–$899) |
| ALLPOWERS R2500 | 2,016 / 2,500 | RV socket per owner (UNVERIFIED) | 1,000 W | 63.9 lb | $759, sold out |

Native TT-30 and buyable under $900 today: AC200L, Anker C2000 Gen 2, Renogy PS2000.

## Candidate open concerns, by frequency in owner discussions

1. **"Can I plug my 30 A shore cord in, and what runs?"** (the opening question of every thread found). With a native
   TT-30 the trailer behaves as on shore power (fridge, water pump, lights, coffee maker, microwave reported), but the
   socket does not deliver 30 A: 30 A × 120 V = 3,600 W, while every unit in this class caps at 2,200–2,600 W (~20 A;
   Anker rates its TT-30R at 20 A). At a real 2,000 W load a 2 kWh pack lasts about an hour. Units without TT-30 work
   with a 5-20P→TT-30R adapter, capped by that outlet.
2. **The converter loop.** The RV converter treats the station as shore power and charges the house battery from it;
   a 55 A converter at ~14 V draws close to 800 W (thecampingnerd). Switch the converter breaker off once the house
   battery is full (don't disconnect the house battery if the breakaway brake relies on it). A 2-/3-way fridge on AUTO
   switches to 120 V and pulls 300–450 W continuously (2.4–3.6 kWh/day, more than the whole pack): set it to propane.
3. **Rooftop AC (13.5–15k BTU).** Runs 1,300–1,900 W; start surge 2,800–3,500 W without a soft starter, ~2,000 W with
   one (Micro-Air). Once started, about 1 hour per 2 kWh. Not an AC solution.
4. **Fridge.** Measured 12 V compressor fridge ~700 Wh/day (Forest River shunt data; Dometic test 1.2–1.5 kWh/day at
   95°F) → a 2 kWh pack covers 2–3 days with nothing else. Absorption fridge on propane draws only its control board.
5. **Recharging on the road.** 12 V socket 96–120 W (a full day+); DC-DC alternator chargers 560–800 W (BLUETTI
   Charger 1 $219, EcoFlow 800 W $269); solar 400 W returns ~1–1.5 kWh on a good day; any 15/20 A pedestal outlet
   refills in ~1–1.5 h.
6. **Weight, placement, weather, theft.** 42–62 lb; none rated for rain; the shore cord forces the unit outside or a
   pass-through.
7. **Is 2 kWh enough for a weekend?** Fridge 700 Wh + furnace blower ~300–500 Wh/night + lights/phones/pump ~200 Wh ≈
   1.2–1.5 kWh/day: about 1.5 days with no sun, 2–3 days with 200–400 W of solar; no AC.

**Most important unanswered concern: #1 + #2, the TT-30 reality.** Every top result says "has a 30A RV outlet" and
stops. A page that says plainly that the socket is 30 A but the inverter ~20 A, that the converter and an AUTO fridge
quietly eat the pack, and what to switch off, is what no competing page does, and it picks a winner (native TT-30:
AC200L, Anker C2000 Gen 2, Renogy PS2000).

## Sources (selected; all read 2026-10-31)
- Elite 200 V2 US page incl. AC200L comparison table: https://www.bluettipower.com/products/elite-200-v2-portable-power-station
- AC200L US: https://www.bluettipower.com/products/ac200l · CA ("Discontinued"): https://shop-ca.bluettipower.com/products/ac200l
- BLUETTI discontinued models: https://www.bluettipower.com/pages/bluetti-discontinued-models
- Elite 200 V2 manual mirror: https://manuals.plus/asin/B0DP659FYP · StorageReview: https://www.storagereview.com/review/portable-power-meets-lab-grade-reliability-bluetti-elite-200-v2-review
- BLUETTI Charger 1: https://www.bluettipower.com/products/bluetti-charger-1
- Anker C2000 Gen 2: https://www.ankersolix.com/products/c2000-gen2
- Renogy PowerStation 2000: https://www.renogy.com/products/power-station-2000
- Oukitel P2001 Plus: https://us.oukitel.com/products/oukitel-p2001-plus-portable-power-station
- Dabbsson DBS2300 Plus: https://dabbsson.com/products/dbs2300plus-portable-power-station
- Jackery Explorer 2000 v2: https://www.jackery.com/products/jackery-explorer-2000-v2-portable-power-station
- EcoFlow DELTA 2 Max: https://us.ecoflow.com/products/delta-2-max-portable-power-station · 800 W alternator charger: https://us.ecoflow.com/products/800w-alternator-charger
- Forest River, power station with a 30 A outlet: https://www.forestriverforums.com/threads/using-a-portable-power-station-with-a-30-amp-rv-outlet.2192187/
- r/RVLiving built-in 30 amp plug: https://www.reddit.com/r/RVLiving/comments/1rginyw/ · r/traveltrailers power station and AC: https://www.reddit.com/r/traveltrailers/comments/1u0bqtm/
- r/GoRVing best RV power station: https://www.reddit.com/r/GoRVing/comments/1reb97i/ · under $1k: https://www.reddit.com/r/GoRVing/comments/1lhnkeg/
- Forest River 12 VDC compressor fridge data: https://www.forestriverforums.com/threads/12vdc-compressor-fridge-data.381473/
- thecampingnerd TT-30 guide (2026-10-21): https://thecampingnerd.com/power-stations-with-tt-30-rv-outlet/
- Mike Sokol, can a solar generator power an AC: https://rvelectricity.substack.com/p/can-a-solar-generator-power-an-air
- Micro-Air generator sizing: https://www.microair.net/blogs/news/what-size-generator-do-you-need-to-run-an-rv-air-conditioner
- rvacunit 13,500 BTU chart: https://www.rvacunit.com/how-many-watts-does-a-13500-btu-rv-ac-use/
