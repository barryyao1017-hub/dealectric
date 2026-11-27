# BLUETTI Apex 300 / Apex 200 families: researched alternatives (DLC-358), read 2026-11-26

All prices are web reads from 2026-11-26. We re-read price and stock the same day before publishing. Machine-readable mapping of all 50 records: `apex.json` (same folder).

## Status of the originals (read today)

| Original | Status read today | Source |
|---|---|---|
| Apex 300 (all bundles) | Sold out, "Temporarily out of stock / Notify Me", no ship date. Amazon B0FJ1WZJRY "Currently unavailable" | bluettipower.com/products/apex-300-home-battery-backup; amazon.com/dp/B0FJ1WZJRY (via r.jina.ai) |
| Apex 200 (all bundles) | Pre-order. Page now says "Orders placed on or after Nov. 25: Ships starting mid-February". Our records say late January, so they are stale | bluettipower.com/products/apex-200-expandable-power-station |
| B300K at BLUETTI | $999. "Orders placed after Nov 20 will ship starting Jan 20" | bluettipower.com/products/apex-300-b300k-expansion-battery |
| B300K on Amazon | In Stock, $1,199, ships from and sold by Bluetti. 2-pack option $1,999.99 (no stock line). "B500K for Apex 300" option $2,099, In Stock | amazon.com/dp/B0FJ3XHFXP |

Because the Apex 200 now ships mid-February, it cannot stand in for the Apex 300.

## What we could not get

- **Anker F3800 / F3800 Plus:** every variant at Anker's store reads "Sold Out", including the Smart Home Power Kit bundles. The F3800 on Amazon (B0C5C9HMQ2) is "Currently unavailable". This takes out the most obvious 120/240 V match.
- **EcoFlow DELTA Pro 3:** Amazon B0D14FMFZD is "Currently unavailable", and two price trackers report it sold out at EcoFlow. Its $2,799 price was above most bands in any case.
- **Jackery Explorer 5000 Plus:** buyable on Amazon at $3,499, but Amazon's delivery estimate is Jan 20–22. Jackery.com shows it sold out. The Solar Generator 5000 Plus + 2×200 W (B0GWM1V7P6) is unavailable.
- **OSCAL PowerMax 6000:** the standalone unit and the BP3600 bundle are sold out. The panel kits are a pre-sale: "Estimated shipping date for the power station: December 14th".
- **Stock of Amazon set options:** several picks are options on an Amazon listing, such as the TITAN with panels or SHP10, the 2×B300K pack, and the Elite 300 + Charger 2. Amazon shows these with a price but no stock line. They are marked "could not read".
- **Pecron E3600LFP:** 120 V only from one unit (240 V needs two units plus a box), so it doesn't qualify for the Apex 300.
- **Independent reviews:** none exist yet for the EcoFlow TITAN 5000 or TITAN Classic (launched Oct 2026, 3 Amazon ratings), and we found no independent hands-on test of the Nature's Generator L6000 or L3600. Those picks rest on maker specs, launch coverage and owner reviews.
- **Method:** Shopify stores rate-limited direct reads, so stock came from product JSON and pages fetched through r.jina.ai. Amazon was read the same way, with delivery estimates for ZIP 97058. Some reads were reused from the 3 kWh group's raw files (Growatt HELIOS on Amazon, R3500 kit inventory), and the JSON names them.

## Candidate spec table

Specs come from the maker page or manual unless noted. "nc" = not confirmed.

| Model | Capacity | AC cont. / surge | Chem. / cycles | Solar in | 120/240 V from one unit | Weight | Spec source |
|---|---|---|---|---|---|---|---|
| **BLUETTI Apex 300** (original) | 2,764.8 Wh | 3,840 W / 7,680 W lifting | LiFePO4, 6,000 to 80% | 2,400 W (2×XT60 12–60 V); 4 kW via SolarX 4K | Yes | 83.8 lb | bluettipower.com Apex 300 page + manual |
| **BLUETTI Apex 200** (original) | 2,560 Wh | 3,200 W / 5,400 W lifting | LiFePO4, 6,000 to 70% | 3,000 W | No (120 V) | 59.3 lb | bluettipower.com Apex 200 page |
| Nature's Generator L6000 | 3,840 Wh (+3,840 Wh Power Pods) | 6,000 W | LiFePO4, 3,000 (pv magazine) | 2,400 W | Yes | 112 lb | naturesgenerator.com/products/lithium-6000-power-station; pv-magazine.com 2025-08-13 |
| OSCAL PowerMax 6000 | 3,600 Wh | 6,000 W (5,000 W after 5 min) / 9,000 W | LiFePO4, 3,500 to 80% | 2,400 W | Yes | 101.4 lb | store.oscal.hk/products/oscal-powermax-6000-price |
| EcoFlow TITAN 5000 | 5,017 Wh | 7,200 W / nc | LFP, nc | 4,000 W | Yes | nc | amazon.com/dp/B0HN1MNNH3 bullets; ecoflow.com TITAN specs |
| EcoFlow TITAN 5000 Classic | 5,017 Wh | 4,000 W / nc | LFP, nc | 3,200 W | No (120 V) | nc | amazon.com/dp/B0HJZSDJZP; us.ecoflow.com TITAN Classic page |
| Jackery Explorer 5000 Plus | 5,040 Wh | 7,200 W / 14,400 W | LiFePO4, 4,000 to 70% | 4,000 W HV + 1,200 W LV | Yes | ~134 lb | jackery.com product page |
| Anker SOLIX E10 (PM + B6000) | 6,144 Wh per battery | 7,680 W / 10 kW turbo 90 min | LFP, nc | 9,000 W (2×4,500 W, 30–450 V) | Yes. **No plug-in outlets listed**; connects through a transfer switch or inlet box | PM 60.6 lb, battery ~130 lb | ankersolix.com/products/e10-b tech table |
| Growatt HELIOS 3600 | 3,686 Wh | 3,600 W / 4,500 W Watt+ | LiFePO4, 4,000 | 2,000 W | No. 240 V / 7,200 W needs two units + hub | ~51 lb | growattportable.com HELIOS 3600 page |
| ALLPOWERS R3500 | 3,168 Wh | 3,200 W / 6,000–7,000 W | LiFePO4, 3,500+ | 2,000 W, 12–150 V | No | nc | iallpowers.com R3500 page |
| Nature's Generator L3600 | 3,072 Wh (+3,072 Wh Pods) | 3,600 W / 7,200 W | LiFePO4, nc | 2,400 W | No | nc | naturesgenerator.com lithium-3600 page |
| Anker SOLIX F3000 + BP3000 | 3,072 + 3,072 Wh | 3,600 W / 7,200 W | LFP, 4,000 | 2,400 W | No | 91.5 lb (station) | ankersolix.com F3000 page |
| Mango Power E | 3,533 Wh | 3,000 W / 4,500–4,800 W 10 s | CATL LFP, 6,000 to 70% | 2,000 W, 60–150 V | No | 100.1 lb | mangopower.com |
| BLUETTI Elite 400 | 3,840 Wh | 2,600 W / 3,900 W lifting | LiFePO4, nc | 1,000 W | No | 86 lb | bluettipower.com Elite 400 page |

## Prices and stock read today

| Candidate | Price | Stock | Where (earns?) |
|---|---|---|---|
| NG L6000 | $2,249.99 | ships now | naturesgenerator.com (awin, our record) |
| NG L6000 + Power Pod (7,680 Wh) | $3,749.99 | ships now | naturesgenerator.com (awin) |
| NG L6000 + 2×200 W folding | $2,999.99 | ships now | naturesgenerator.com/products/lithium-6000-solar-generator (awin) |
| NG L6000 + 2×440 W rigid | $3,399.99 | ships now | same (awin) |
| NG L6000 + Pod + 4×440 W | $5,999.99 | ships now | same (awin) |
| NG L3600 + 200 W / + Pod / + Pod + 4×440 W | $1,849.99 / $2,689.99 / $4,799.99 | ships now | naturesgenerator.com (awin) |
| OSCAL PM6000 + 1/2/3/4× PM400 SE | $1,969.98 / $2,269.98 / $2,499.98 / $2,799.98 | pre-order Dec 14 | store.oscal.hk (awin, our records) |
| EcoFlow TITAN 5000 | $3,199 | buyable now, delivery est. Dec 17 | Amazon B0HN1MNNH3 |
| TITAN 5000 + 4×175 W / + 2×400 W / + SHP10 / + EB + SHP10 | $3,899 / $4,089 / $4,199 / $6,169 | could not read | Amazon B0HN1MNNH3 set options |
| EcoFlow TITAN 5000 Classic / + 4×175 W | $2,199 / $2,899 | In Stock | Amazon B0HJZSDJZP |
| EcoFlow TITAN 5000 Plus | $3,699 | In Stock | Amazon B0HN1WCQNZ |
| Jackery Explorer 5000 Plus | $3,499 | buyable, delivery est. Jan 20–22 | Amazon B0DFGLG35L |
| Anker E10 PM + 1 battery / + Smart Inlet Box | $3,799 / $4,099 | Add to Cart ("Limited Stock" on PM+1) | ankersolix.com/products/e10-b (rakuten) |
| Anker E10 PM + 2 batteries / + Smart Inlet Box | $5,799 / $6,099 | Add to Cart, "Limited Stock" | same (rakuten, our record) |
| Growatt 2× HELIOS 3600 + Double Voltage Hub | $2,899 | ships now | growattportable.com (awin) |
| Growatt HELIOS 3600 | $1,139 | In Stock, sold by Amazon | Amazon B0DF7SZJWY (3 kWh group read) |
| ALLPOWERS R3500 / + SP039 600 W | $1,199 / $1,993.10 | ships now (inventory 14 / 7) | iallpowers.com (cj, our records) |
| Anker F3000 + BP3000 + 400 W | $2,529.99 | Add to Cart | ankersolix.com (rakuten, our record) |
| Mango Power E Kit Pro / Kit Max | $2,499 / $3,399 | ships now (+1–2 weeks handling) | mangopower.com (awin) |
| BLUETTI Elite 400 + Charger 2 | $1,599.99 | pre-order mid-January (record; JSON available) | bluettipower.com (awin, our record) |
| BLUETTI Elite 300 + Charger 2 | $1,413 | could not read (base Elite 300 In Stock, delivery Jan 8) | Amazon B0GKRTX336 |
| BLUETTI 2×B300K / B500K for Apex 300 | $1,999.99 / $2,099 | could not read / In Stock | Amazon B0FJ3XHFXP |
| Anker F3800, F3800 Plus (all variants) | n/a | Sold out / unavailable | ankersolix.com; Amazon B0C5C9HMQ2 |
| EcoFlow DELTA Pro 3 | n/a | Currently unavailable | Amazon B0D14FMFZD |

## Winners by configuration

### Apex 300 family (needs 120/240 V from one unit)

**(a) Bare unit ($1,699; band $1,274–2,124).** Winner: **OSCAL PowerMax 6000 + 400 W panel**, $1,969.98, pre-order Dec 14. Runner-up: Nature's Generator L6000, $2,249.99, ships now.
The OSCAL kit is the only 120/240 V split-phase unit that fits the band: 3,600 Wh, 6,000 W, plus a free-standing 400 W panel. It is a pre-sale, but it ships Dec 14 and the Apex 300 has no date, so it qualifies under rule 2. The L6000 is the better product to link, since it ships now and has 3,840 Wh and 6,000 W. At +32% it sits outside the ±25% band, so it can win only if you relax the band.

**Apex 300 + Hub D1 ($1,899).** Winner: **NG L6000**, $2,249.99, +18%, ships now. Runner-up: the OSCAL kit (pre-sale).
The Hub D1 only adds the DC/USB ports the L6000 already has built in.

**Apex 300 + Charger 1/2 bundles (5 records).** **None.**
No 120/240 V station with an alternator charger ships now. The F3800 family is sold out, the DELTA Pro 3 is unavailable, and the stations that do ship (NG L6000, TITAN, Jackery, E10) have no vehicle-charger bundle. The nearest stand-in is listed as the runner-up in the JSON.

**(b) Apex 300 + 1×B300K (5.5 kWh): bare, + 50 A cable, + Hub D1 ($2,599–2,999).** Winner: **EcoFlow TITAN 5000** on Amazon, $3,199, delivery est. Dec 17. Runner-up: NG L6000, $2,249.99.
The TITAN gives 5,017 Wh, 7,200 W split-phase and 4 kW solar, so it matches on capacity. The L6000 is cheaper but holds 31% less. TITAN caveats: it is an indoor home battery (IP20) with AC outlets only (no USB or 12 V), and it has no independent review yet.

**Apex 300 + B300K + SolarX 4K ($3,299).** Winner: **TITAN 5000**, $3,199, with 4 kW solar input built in. Runner-up: Jackery Explorer 5000 Plus, $3,499.
The Jackery is equally capable and has The Solar Lab's review behind it, but it costs $300 more and Amazon's delivery estimate is Jan 20–22.

**(b2) Apex 300 + ~8 kWh: 2×B300K ($3,899), B500K ($3,699), and with SolarX ($4,498 / $3,999).** Winner: **NG L6000 + Power Pod**, $3,749.99, 7,680 Wh, 6,000 W split-phase in one unit, ships now. Runner-up: Anker E10 Power Module + 1 battery, $3,799.
The E10 has 6.1 kWh and 9 kW of solar input but no plug-in outlets. For the SolarX versions, note the L6000 takes 2.4 kW of solar, not 4 kW.

**(b3) Apex 300 + 2×B500K (13 kWh), with or without SolarX ($5,399 / $5,899).** Winner: **Anker E10, Power Module + 2×B6000**, $5,799: 12.3 kWh, 7,680 W split-phase, 9 kW solar. Runner-up: NG L6000 + Pod + 4×440 W, $5,999.99, 7.68 kWh.
The E10 is a whole-home system without plug-in outlets.

**(c) Apex 300 + panels.**
- 350 W ($2,348) and 2×200 W ($2,399): **OSCAL PM6000 + 400 W**, $1,969.98, ships Dec 14. For 2×200 W, the NG L6000 + 2×200 W ($2,999.99, ships now) is $1.24 over the +25% line. If you read the band loosely, it is the better link.
- 500 W ($2,499): **NG L6000 + 2×200 W folding**, $2,999.99, ships now. Runner-up: OSCAL + 2×400 W (pre-sale).
- 3×200 W and 2×350 W ($2,899 each) and 2×500 W ($3,299): **NG L6000 + 2×440 W rigid bifacial**, $3,399.99, 880 W. The panels are rigid, not folding. Runner-ups: OSCAL + 2×400 W or + 3×400 W.

**(d) Apex 300 + battery + panels.**
- B300K + 2×200 W / 500 W / 2×350 W ($3,499–3,998): **TITAN 5000 + 4×175 W** (Amazon set option), $3,899: 5 kWh and 700 W of panels. Its stock line could not be read, so re-read it before publishing. The fallback is the runner-up NG L6000 with panels, which ships now but holds 3.84 kWh.
- 2×B300K + 2×500 W ($5,499): **NG L6000 + Pod + 4×440 W**, $5,999.99: 7.68 kWh and 1,760 W of panels.
- B500K + 500 W ($4,399) and 2×B300K + 2×200 W ($4,599): **none**. No 120/240 V kit near 8 kWh that includes panels fits the band (NG Pod + 4×440 W is +30–36%). Nearest is NG L6000 + Pod without panels.

**(e) Home backup.**
- B300K + Home Backup Kit ($3,399) and B500K + Home Backup Kit ($4,099): **Anker E10 Power Module + 1 battery + Smart Inlet Box**, $4,099. It is the only in-band kit that includes home-connection hardware. For the B500K version it holds 22% less (6.1 vs 7.9 kWh). If you weigh capacity over the included switch, use the runner-up NG L6000 + Pod.
- 2×Apex 300 + 2×B300K + Hub A1 ($6,099): **E10 Power Module + 2 batteries**, $5,799. It matches the same 7,680 W at 120/240 V and holds 12.3 vs 11.1 kWh.
- 2×Apex 200 + 2×B300K + Hub A1 + Home Backup Kit ($5,699): **E10 Power Module + 2 batteries + Smart Inlet Box**, $6,099. Runner-up: TITAN + Extra Battery + SHP10, $6,169, stock unknown.

**Expansion batteries: 2×B300K ($2,398, ships Jan 20).** Winner: **the same 2×B300K on BLUETTI's Amazon listing** (B0FJ3XHFXP), $1,999.99. Runner-up: **B500K for Apex 300** on the same listing, $2,099, In Stock, 5,120 Wh.
The single B300K shows In Stock there. The 2-pack option shows no stock line.

### Apex 200 family (120 V; ships mid-February)

**Bare ($1,149).** Winner: **Growatt HELIOS 3600 on Amazon**, $1,139, sold by Amazon, In Stock: 3,686 Wh and 3,600 W. Runner-up: ALLPOWERS R3500, $1,199, 3,168 Wh and exactly 3,200 W.
The HELIOS wins on price (rule 3) and also has more capacity and 4,000 cycles. The 3 kWh group made the same pick for the Elite 300.

**+ 200 W ($1,499).** Winner: **NG L3600 + 200 W folding panel**, $1,849.99, ships now. Runner-up: BLUETTI Elite 300 + 2×200 W, $1,499.99.
The Elite 300 kit is cheaper and the same brand, but it is a pre-order (Dec 14) with only 2,400 W, so the ship-now L3600 wins under rule 2.

**+ 2×200 W ($1,799), + 350 W ($1,699), + 500 W ($1,849).** Winner: **ALLPOWERS R3500 + SP039 600 W**, $1,993.10: 3,168 Wh, 3,200 W, 7 kits in stock. Runner-ups: DELTA 3000 Gen4 + 400 W on Amazon ($1,899, stock not readable), or NG L3600 + 200 W.

**+ B300K ($2,199).** Winner: **EcoFlow TITAN 5000 Classic on Amazon**, $2,199, In Stock: 5,017 Wh and 4,000 W. Runner-up: NG L3600 + Power Pod, $2,689.99, 6,144 Wh.

**+ B500K, + B500K + TT-30 cable, + 2×B300K ($2,749–3,199).** Winner: **Growatt 2×HELIOS 3600 + Double Voltage Hub**, $2,899: 7,372 Wh and 7,200 W at 240 V. Runner-up: NG L3600 + Pod, 6,144 Wh, a single unit and $209 cheaper.
The Growatt is two stations joined by a hub rather than one station with batteries.

**+ B300K + 2×200 W ($2,799).** Winner: **Anker F3000 + BP3000 + 400 W**, $2,529.99, our Rakuten record: 6,144 Wh, 3,600 W, the same 400 W of panel. Runner-up: TITAN Classic + 4×175 W, $2,899, In Stock.

**+ B500K + 2×500 W ($4,196).** Winner: **NG L3600 + Pod + 4×440 W rigid**, $4,799.99: 6,144 Wh and 1,760 W of panels. Runner-up: Mango Power E Kit Max, $3,399, 3,533 Wh.

**+ Charger 2 ($1,598).** Winner: **BLUETTI Elite 400 + Charger 2**, $1,599.99: same brand, same charger, 3,840 Wh and 2,600 W. Runner-up: Elite 300 + Charger 2 on Amazon, $1,413, stock unknown.
The Elite 400 is a pre-order. It ships mid-January per our record (not re-read today), about a month ahead of the Apex 200, so it qualifies under rule 2.

**+ Charger 2 + panels (3 records).** **None.** No kit in the band has both a vehicle charger and panels.

## Reviews used
- OSCAL PowerMax 6000: geardiary.com/2026/07/31/oscal-powermax-6000-review/; batteryskills.com/oscal-powermax-6000-solar-generator-3600wh-review/
- Anker E10: ess-news.com/2026/05/21/anker-solix-e10-deep-dive-review-…; digitaltrends.com/home/anker-solix-e10-review/
- Growatt HELIOS 3600: batteryskills.com/growatt-helios-3600-portable-power-station-review/
- ALLPOWERS R3500: exspenditure.com/allpowers-portable-power-station-review/; batteryskills.com/allpowers-r3500-2-hour-charge-review/
- Anker F3000: notebookcheck.net (F3000 review); cleantechnica.com/2025/08/22/anker-solix-f3000-…-cleantechnica-tested/
- BLUETTI Elite 400: storagereview.com (Elite 400 review; 3.07 kWh delivered, 6 ms UPS); techradar.com/pro/bluetti-elite-400-review
- Jackery Explorer 5000 Plus: thesolarlab.com/review/jackery-explorer-5000-plus-review
- Mango Power E: storagereview.com/review/mango-power-e-portable-power-station
- Weak evidence. EcoFlow TITAN 5000 and TITAN Classic: popsci.com launch coverage plus 3 Amazon ratings. NG L6000: pv-magazine launch report only. NG L3600: Walmart owner reviews only. BLUETTI B300K: 187 Amazon ratings.

## Open decisions for the publisher
1. **Bare Apex 300:** under the strict ±25% band the winner is the OSCAL pre-sale. The ship-now NG L6000 is 32% over the band.
2. **Unreadable Amazon set options:** five configurations rest on Amazon set options whose stock could not be read. These are the TITAN with panels or SHP10, and the 2×B300K pack. Re-read them first; each has a ship-now runner-up.
3. **E10 picks:** E10 winners suit the home-backup configurations. Note on the page that the E10 is a whole-home battery with no plug-in outlets.
