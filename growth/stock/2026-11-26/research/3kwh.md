# 3–4 kWh class: alternatives for pre-order and sold-out originals (DLC-358)

Researched 2026-11-26. All price and stock reads are web reads made today through r.jina.ai (store HTML and Amazon pages). Shopify stores were rate-limiting direct requests, so I read each store's own per-variant JSON (inventory quantity, pre-order flag) from the page HTML. Amazon delivery dates are for the default ZIP the reader got (The Dalles, OR 97058). Mapping: `3kwh.json`.

## Key findings

- **Amazon doesn't get the BLUETTI items here sooner.** It lists them as "In Stock", but its delivery estimates are later than BLUETTI's own pre-order dates: Elite 300 (B0GKRTX336, $1,098.99) delivers Jan 8, Elite 300 + 2×200 W (B0GKRPD6GL, $1,519) Jan 22, and Elite 400 (B0G8Y8DCC1, $1,599) Jan 21. None of them qualifies.
- **Amazon is also slow for most rival 3 kWh stations:** EcoFlow DELTA 3 Ultra delivers Jan 4 (EcoFlow's store says it ships in late December), Anker F3000 + 400 W Jan 22 (Anker's store says 3–7 weeks), and Jackery HomePower 3600 Plus + 2×200 W Jan 12–14 (jackery.com says it is a pre-order that ships by Jan 6). The exception is the **Growatt HELIOS 3600 (B0DF7SZJWY): sold by Amazon.com at $1,139, In Stock, delivery Dec 9.**
- **The ALLPOWERS R3500 pre-order kits are pre-orders only because of the panel.** ALLPOWERS' variant data flags just the panel (SP037, SF200 or SF100) as pre-order and ships it separately; the R3500 station has stock (9–20 units per kit variant). The dispatch dates shown ("from Nov 9" for SF100/SF200, "from Nov 20" for SP037) have already passed, so the panels' real date is unknown. The R3500 alone (14 units) and the R3500 + SP039 kits (7 and 8 units) are not flagged pre-order and ship now.
- **The R4000 is sold out at ALLPOWERS** (0 units). Wellbots lists it as in stock at $1,454.03; that store doesn't earn us anything and may be running a stale drop-ship feed.

## Spec table: originals and candidates

| Product | Wh / chem | AC cont. / surge | Solar in | Cycles | Weight | 120/240 V | TT-30 | Source |
|---|---|---|---|---|---|---|---|---|
| **BLUETTI Elite 300** (orig.) | 3,014.4 LiFePO4 | 2,400 / 4,800 W lifting | 1,200 W, 12–60 V | 6,000+ | 26.3 kg (58 lb) | 120 | yes | bluettipower.com/products/elite-300-portable-power-station |
| **BLUETTI Elite 400** (orig.) | 3,840 (chem. on page: not confirmed) | 2,600 / 3,900 W lifting | 1,000 W, 12–60 V | not confirmed | 39 kg | 120 | not confirmed | bluettipower.com/products/elite-400 |
| **ALLPOWERS R4000** (orig.) | 3,456 LiFePO4 | 3,600 / 6,000 W | 2,000 W (3× XT60) | 3,500+ | 45 kg | 120 | yes | iallpowers.com/products/allpowers-r4000-power-station |
| **ALLPOWERS R3500** | 3,168 LiFePO4 | 3,200 / 6,000 W | 2,000 W, 12–150 V, 40 A | 3,500+ | 42 kg (93 lb) | 100–120 | maker table doesn't list it; BatterySkills review says yes | iallpowers.com R3500 page (read today) |
| **Growatt HELIOS 3600** | 3,686.4 LFP | 3,600 / 4,500 W (Watt+) | 2,000 W | 80% after 4,000 | 51 lb (Amazon listing) | 120; 240 V needs two units + hub | yes | growattportable.com product page; Amazon B0DF7SZJWY bullets |
| **Nature's Generator L3600** | 3,072 LiFePO4 | 3,600 W / surge not confirmed | 2,400 W | not confirmed | not confirmed | 120 | not confirmed | naturesgenerator.com/products/lithium-3600-power-station |
| **Mango Power E** | 3,533 CATL LFP | 3,000 / 4,500–4,800 W (10 s) | 2,000 W, 60–150 V (needs 2+ panels in series) | 6,000 to 70% | 100.1 lb | 120 (240 V paired) | 30 A RV port | mangopower.com product page |
| EcoFlow DELTA 3 Ultra | 3,072 LFP | 3,600 / 7,200 W | not confirmed | not confirmed | not confirmed | 120 | not confirmed | us.ecoflow.com DELTA 3 Ultra page |
| Anker SOLIX F3000 | 3,072 LFP | 3,600 / 7,200 W | 2,400 W (1,600 HV + 800 LV) | 4,000 | 91.5 lb | 120 (240 V paired) | yes | ankersolix.com/products/f3000 |
| Jackery HomePower 3600 Plus | 3,584 LiFePO4 | 3,600 W | not confirmed | 6,000 | not confirmed | 120 (240 V paired) | not confirmed | jackery.com/products/homepower-3600-plus |

## Price and stock reads (2026-11-26, web reads)

| Candidate | Where | Price | Stock as read |
|---|---|---|---|
| Growatt HELIOS 3600 | Amazon B0DF7SZJWY (sold by Amazon.com) | $1,139.00 | In Stock, delivery Dec 9 |
| Growatt HELIOS 3600 | growattportable.com (Awin) | $1,399.00 | available; HELIOS + 2×200 W kit unavailable |
| ALLPOWERS R3500 | iallpowers.com (CJ) | $1,199.00 | 14 units, not pre-order |
| R3500 + SP039 600 W | iallpowers.com | $1,993.10 | 7 units, not pre-order (panel and station ship separately) |
| R3500 + 2× SP039 | iallpowers.com | $2,562.15 | 8 units, not pre-order |
| R3500 + SP037 / 2× SP037 | iallpowers.com | $1,803.10 / $2,182.15 | panel pre-order, "from Nov 20" (passed) |
| R3500 + SF200 / 2× SF200 | iallpowers.com | $1,331 / $1,463 | panel pre-order, "from Nov 9" (passed) |
| R3500 + SF100 / 2× SF100 | iallpowers.com | $1,298.99 / $1,398.98 | panel pre-order, "from Nov 9" (passed) |
| ALLPOWERS R4000 | iallpowers.com | $1,499 | sold out (0 units) |
| ALLPOWERS R4000 | wellbots.com (no earnings) | $1,454.03 | available, "Ships in 1-3 Days" |
| Nature's Generator L3600 | naturesgenerator.com (Awin) | $1,399.99 | available |
| L3600 + 200 W folding / + 2×100 W / + 2×440 W | naturesgenerator.com | $1,849.99 / $1,899.99 / $2,499.99 | available |
| Mango Power E / Kit Pro (2×400 W) | mangopower.com (Awin) | $1,499 / $2,499 | available; "allow an additional 1–2 weeks for shipping"; Kit (2×200 W) and Kit Plus unavailable |
| EcoFlow DELTA 3 Ultra | us.ecoflow.com / Amazon B0FQVBFLHL | $1,369 / $1,369 | store: 10 units but "Ships in Late December"; Amazon: delivery Jan 4; all Ultra panel kits unavailable |
| Anker F3000 / + 400 W | ankersolix.com / Amazon B0GYP2LQQG | $1,699.99 / $2,169.99 | "all F3000 orders will ship within 3–7 weeks"; Amazon delivery Jan 22 |
| Jackery HP3600 Plus + 2×200 W | jackery.com / Amazon B0FMXCPWBN | $2,549 / $2,549 | "Pre-order · Ships by Jan. 6"; Amazon delivery Jan 12–14 |
| BLUETTI Elite 300 | Amazon B0GKRTX336 | $1,098.99 | delivery Jan 8 (later than BLUETTI's Dec 14) |
| BLUETTI Elite 300 + 2×200 W | Amazon B0GKRPD6GL | $1,519.00 | delivery Jan 22 |
| BLUETTI Elite 400 | Amazon B0G8Y8DCC1 | $1,599.00 | delivery Jan 21 |
| Pecron E3600LFP (all kits) | pecron.com | $999 unit | every variant unavailable |

Dropped: Pecron (sold out), OUPES Mega 3 (not in OUPES' US product feed), OSCAL PowerMax 6000 kits (our record says pre-order Dec 14; I couldn't re-read them), Anker F3800 Plus ($2,999 with no panels, over every band).

## Winner vs runner-up by configuration

**Bare Elite 300 ($1,099, ships Dec 14).** Winner: **Growatt HELIOS 3600 on Amazon, $1,139.** Runner-up: ALLPOWERS R3500, $1,199. Both ship now and fit the band. The HELIOS out-specs the Elite 300 (3,686 Wh, 3,600 W, TT-30) and is sold by Amazon.com with delivery on Dec 9. The R3500 is the closer capacity match and earns through CJ, but it costs $60 more and weighs 93 lb, so rule 3 (lower price) picks the HELIOS.

**Elite 300 + 2× 200 W ($1,499.99).** **None qualifies.** No kit that ships now has about 400 W of panels within $1,125–$1,875. The closest is Nature's Generator L3600 + 200 W at $1,849.99, which has half the panel wattage. R3500 + SP039 is 33% over the price band.

**Elite 300 + 350 W ($1,649) and + 500 W ($1,699.99).** Winner: **ALLPOWERS R3500 + SP039 600 W, $1,993.10.** Runner-up: Nature's Generator L3600 + 200 W, $1,849.99. The R3500 kit is about the same capacity, has more output, carries at least as much panel as the original, and ships now. The Nature's Generator kit has too little panel.

**Elite 400 + 350 W, + 500 W, + 2× 200 W.** Winner: **R3500 + SP039, $1,993.10.** Runner-up: Nature's Generator L3600 + 200 W for the 350 W and 2×200 W kits, and Mango Power E Kit Pro for the 500 W kit. Nothing at 3.8 kWh with panels ships now inside these bands. The R3500 kit gives up 17% of capacity but has more output, double the solar input and enough panel. For the 500 W kit, Mango is closer on capacity but $506 dearer with 800 W of panels; I judged the two equally suitable, so the cheaper R3500 kit wins.

**Elite 400 + 2× 350 W ($2,448).** Winner: **Mango Power E Kit Pro (2× 400 W), $2,499.** Runner-up: R3500 + SP039, $1,993.10. Mango is closer on both capacity (3,533 Wh) and panel wattage (800 W vs 700 W), and costs only 2% more. The R3500 kit is short on both counts.

**Elite 400 + Charger 1 / Charger 2.** **None.** No 3–4 kWh station with an alternator charger ships now within $1,200–$2,000. Anker F3000 + Alternator Charger costs $2,069.99 and ships in 3–7 weeks. BLUETTI's charger bundles that are in stock are 1–2 kWh units.

**R4000 ($1,499, sold out).** Winner: **Growatt HELIOS 3600 on Amazon, $1,139.** Runner-up: the identical R4000 at Wellbots, $1,454.03. The HELIOS matches or beats the R4000 on capacity, output, TT-30 and solar input, and it costs $315 less and earns. Wellbots earns nothing, and its stock may be stale. The same-brand R3500 ($1,199) is the fallback that earns, but it drops to 3,200 W.

**R3500 + SP037 ($1,803.10) and + 2× SP037 ($2,182.15).** Winner: **R3500 + SP039 600 W, $1,993.10.** It's the same station and brand, and the kit ships now. For the 2× SP037 kit, the runner-up is R3500 + 2× SP039 ($2,562.15). One 600 W panel is 25% under the original's 800 W and two are 50% over; I judged them equally suitable, so the cheaper kit wins.

**R3500 + SF200, + SF100, + 2× SF200, + 2× SF100.** **None.** No kit with panels that ships now fits these bands, which top out at $1,624–$1,829. On these kits the station already ships and only the small panel is a pre-order. An alternative line may matter less here than a note that the station ships now.

## Reviews

- Growatt HELIOS 3600: [BatterySkills review](https://batteryskills.com/growatt-helios-3600-portable-power-station-review/) (hands-on outage use; reads like affiliate content, with no measured capacity). Amazon has 4.2★ from 112 ratings. I found no lab test.
- ALLPOWERS R3500: [BatterySkills](https://batteryskills.com/allpowers-r3500-2-hour-charge-review/) (confirms the TT-30R outlet) and [exspenditure 30-day test](https://exspenditure.com/allpowers-portable-power-station-review/) (about 3,200 Wh delivered, 14-hour outage log; its rated figures are loose).
- Mango Power E: [StorageReview](https://www.storagereview.com/review/mango-power-e-portable-power-station) (measured 2.72 kWh at a 350 W load, 77% of rated) and [The Solar Lab](https://www.thesolarlab.com/review/mango-power-e-review).
