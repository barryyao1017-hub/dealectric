# FridgePower, B300K and panel alternatives (DLC-358), web read 2026-11-26

All prices and stock are web reads from 2026-11-26, to be re-read before publishing. Amazon was read through r.jina.ai (direct fetch returns 503). Best Buy and Home Depot pages could not be read.

## Facts that change the picture

- **FridgePower** ([BLUETTI](https://www.bluettipower.com/products/fridgepower-bc200)) is a 75 mm slim, wall-hung or fridge-side LiFePO4 UPS for refrigerators, freezers and sump pumps (home), with an RV mode through Charger 2 + DC Hub. It has 2,016 Wh, 1,800 W continuous (3,600 W surge), <10 ms switchover, and expands to 8,064 Wh with up to 3× BC200. Every FridgePower bundle says "expected to ship on January 11 for orders placed on or after Nov. 23". Amazon has the same listings (B0H82LT2HF, B0H45GF28P), sold by Bluetti, with delivery Jan 22, so Amazon is no faster.
- **Other BLUETTI stations in this class don't ship sooner**: Elite 200 V2 ships early January on BLUETTI and delivers Jan 14 on Amazon (B0DCJV9LTB), Elite 400 mid-January, AC200L sold out. **Elite 300 ships Dec 14** (UPS 10 ms, 3,014 Wh, 2,400 W, not expandable).
- **B300K** (all variants: single, ×2, ×3, + Charger 2, + DC Hub) says "Orders placed after Nov 20 will ship starting Jan 20." Our record `bluetti-b300k-expansion-battery` ("in stock") is stale. BLUETTI says the B300K works with AC200L, AC200MAX, AC300, Apex 300 and AC500, and the B500K with Apex 300, Apex 200, AC300, AC500, AC200L and AC200MAX ([B500K page](https://www.bluettipower.com/products/b500k2-foldable-trolley)). The B500K is therefore the in-brand substitute, and it shows no pre-order note.
- **Records found stale while checking candidates:**
  - Anker SOLIX S2000 now ships in 7–13 weeks.
  - Anker F3000 ships in 3–7 weeks.
  - The Growatt INFINITY 2000 extra battery and HELIOS 3600 extra battery are sold out.
  - Our FOSSiBOT F2400 ASIN B0H4W51ZMH is now a junk "Fossibot F2400 pink" listing at $2,999 from a third-party seller.
  - ALLPOWERS SP033 is sold out.
  - BLUETTI PV420 is discontinued in the US.

## A. FridgePower family

### Spec table (maker pages)

| Model | Wh | AC cont./surge | Chem / cycles | UPS/EPS | Solar in | Weight | 120/240 | Price (web read) | Stock |
|---|---|---|---|---|---|---|---|---|---|
| BLUETTI FridgePower (original) | 2,016 (to 8,064 w/ 3× BC200) | 1,800 / 3,600 | LFP / BC200 4,000+ | <10 ms | not published | not published ("very heavy", Reviewed) | 120 | $949; +BC200 $1,599.99 | ships Jan 11 |
| Growatt INFINITY 2000 PRO ([page](https://www.growattportable.com/products/growatt-infinity-2000-pro-portable-power-station)) | 2,048 | 2,400 / 4,800 | LFP / 4,000 to 80% | 20 ms (bullets say <15 ms) | 1,200 W, 12–60 V | ~51 lb | 120 | $799 | Available |
| Growatt HELIOS 3600 ([page](https://www.growattportable.com/products/growatt-helios-3600-portable-power-station)) | 3,686 | 3,600 / not listed | LFP / 4,000+ | 15–20 ms | 2,000 W, 12–60 V | ≈99 lb | 120 + 240 V outlet; 2 units = 240 V split | $1,399; ×2 + hub $2,899 | Available (both) |
| Mango Power E ([page](https://mangopower.com/products/mango-power-e-home-backup-and-portable-power-station)) | 3,533 (+3,533 battery) | 3,000 / 4,500–4,800 | CATL LFP / 6,000 to 70% | not specified | 2,000 W, 60–150 V | 100.1 lb | 120 (240 V with 2 units) | $1,499; battery $1,299 (record) | "allow an additional 1–2 weeks" |
| Anker SOLIX F3000 + BP3000 ([page](https://www.ankersolix.com/products/f3000)) | 6,144 | 3,600 / 7,200 | LFP / 4,000 | 20 ms | 2,400 W | 91.5 lb (F3000) | 120 (240 V with 2) | $2,059.99 | ships in 3–7 weeks |
| BLUETTI Elite 300 ([page](https://www.bluettipower.com/products/elite-300-portable-power-station)) | 3,014 | 2,400 / 4,800 lifting | LFP / 6,000+ | 10 ms | 1,200 W (record) | 57.98 lb (StorageReview) | 120 | $1,099; + Charger 2 $1,399.99; + 2×200 W $1,499.99 | ships Dec 14 |
| EcoFlow DELTA 2 Max + 800 W Alternator Charger ([Amazon B0D1CN8MLS](https://www.amazon.com/dp/B0D1CN8MLS)) | 2,048 | 2,400 | LFP | 30 ms (not confirmed here) | — | — | 120 | $1,249 | In Stock, delivery Dec 10 |
| EcoFlow DELTA 2 Max ([Amazon B0C4DW17PD](https://www.amazon.com/dp/B0C4DW17PD)) | 2,048 | 2,400 | LFP | — | — | — | 120 | $977 | delivery Dec 28 |

### Mapping

| Original | Price | Winner | Price | Runner-up |
|---|---|---|---|---|
| `bluetti-fridgepower-bc200` (4,032 Wh) | $1,599.99 | Growatt HELIOS 3600 | $1,399 (−13%) | Mango Power E $1,499 |
| `bluetti-fridgepower-2-bc200` (6,048 Wh) | $2,399 | HELIOS 3600 ×2 + Double Voltage Hub | $2,899 (+21%) | Mango E + battery $2,798 (two listings) |
| `bluetti-fridgepower-3-bc200` (8,064 Wh) | $3,429 | HELIOS 3600 ×2 + Double Voltage Hub | $2,899 (−15%) | Mango E + battery $2,798 |
| `bluetti-fridgepower-2-pack` (2× 2,016 Wh) | $1,599.99 | 2× Growatt INFINITY 2000 PRO | $1,598 (0%) | 2× EcoFlow DELTA 2 Max $1,954 (Dec 28) |
| `bluetti-2-fridgepower-2-bc200` (2× 4,032 Wh) | $3,099.99 | HELIOS 3600 ×2 + Double Voltage Hub | $2,899 (−6.5%) | 2× Mango E $2,998 |
| `bluetti-fridgepower-charger-2-dc-hub` | $1,699 | BLUETTI Elite 300 + Charger 2 (Dec 14) | $1,399.99 (−18%) | EcoFlow DELTA 2 Max + 800 W Alternator Charger $1,249 (−26.5%, just outside the band) |
| `bluetti-fridgepower-charger-2-dc-hub-200w-solar-kit` | $1,999 | BLUETTI Elite 300 + 2×200 W (Dec 14) | $1,499.99 (−24.96%) | Elite 300 + Charger 2 $1,399.99 (−30%, outside the band) |

**Bare 2 kWh (the 2-pack).** Two INFINITY 2000 PROs give the same capacity and more output (2,400 W vs 1,800 W) for $1,598 against $1,599.99, ship now, and earn through Awin. The DELTA 2 Max alternative costs 22% more and doesn't arrive until Dec 28. The INFINITY gives up FridgePower's <10 ms UPS (20 ms EPS) and the slim wall form. For now it can't be expanded either, because its extra battery is sold out.

**4 kWh (+BC200).** The HELIOS 3600 is the nearest ships-now LiFePO4 unit (−9% Wh, −13% price, Awin). Mango E is close but costs $100 more and warns of a 1–2 week delay. Anker F3000 + BP3000 would match capacity, but it ships in 3–7 weeks and is out of band for this size.

**6–8 kWh and 2× 4 kWh.** The only single listing that ships now is HELIOS 3600 ×2 + Double Voltage Hub (SKU PPS3600*2+PowerHub, Available). It is closest for 8 kWh (7,372 Wh, −15% price) and for two separate 4 kWh systems (−6.5%). For 6,048 Wh it overshoots (+22% Wh, +21% price, 7,200 W/240 V class). Mango E + battery is cheaper there, but it means two purchases and a shipping delay. The closest exact match, Anker F3000 + BP3000 ($2,059.99, 6,144 Wh), wins if 3–7 weeks becomes acceptable.

**RV bundles (Charger 2 + DC Hub).** BLUETTI says Charger 2 "works with all BLUETTI power stations". The Elite 300 + Charger 2 bundle ships Dec 14 (four weeks before FridgePower), costs 18% less, and has more battery and 10 ms UPS. The DC Hub is missing. EcoFlow DELTA 2 Max + 800 W Alternator Charger ships now but is 26.5% under, so it misses the ±25% band by 1.5 points. For the +200 W kit, no listing in the band that ships before Jan 11 has both an alternator charger and a panel. The winner keeps the panels (Elite 300 + 2×200 W, in band by 0.04%) and drops Charger 2. The runner-up keeps Charger 2 and drops the panel, at −30%. Barry's call which matters more.

**Reviews:**
- FridgePower: [APH Networks](https://aphnetworks.com/reviews/bluetti-fridgepower-bluecell-200-display-1/4) (85.7% of rated capacity, 8/10) and [TechRadar](https://www.techradar.com/pro/bluetti-fridgepower-review).
- HELIOS 3600: only a hands-on review ([batteryskills](https://batteryskills.com/growatt-helios-3600-portable-power-station-review/)), no independent capacity test found.
- INFINITY 2000 PRO: [batteryskills](https://batteryskills.com/growatt-infinity-2000-pro-portable-power-station-2048wh-review/) (fridge plus router for over 18 h), plus [Electrek](https://electrek.co/2024/05/22/growatt-infinity-2000-versatile-power-anywhere/) on the earlier INFINITY 2000.
- Elite 300: [StorageReview](https://www.storagereview.com/review/bluetti-elite-300-review-3014wh-2400w-and-an-8ms-ups-switchover-in-a-58-pound-box) (8 ms switchover, 57.98 lb), [Notebookcheck](https://www.notebookcheck.net/3-kWh-in-a-compact-package-Powerstation-Bluetti-Elite-300-review.1246185.0.html), and Cybershack (nearly 10 h at 1,000 W).

## B. B300K expansion batteries

| Item | Wh | Fits | Price (web read) | Stock |
|---|---|---|---|---|
| B300K ×2 (original, BLUETTI) | 5,529.6 | AC200L, AC200MAX, AC300, Apex 300, AC500 (+Apex 200 per listing name) | $2,398 | ships Jan 20 |
| B300K + Charger 2 (original) | 2,764.8 | same | $1,599 | Dec 14 (record) / B300K Jan 20 on page |
| B300K + Charger 2 + DC Hub (original) | 2,764.8 | same | $1,799 | same |
| B500K for Apex 200 & Apex 300 ([BLUETTI](https://www.bluettipower.com/products/b500k2-foldable-trolley)) | 5,120, LFP, 4,000+ cycles | Apex 300, Apex 200, AC300, AC500, AC200L, AC200MAX | $1,599 | no pre-order note, ships now |
| B500K + Charger 2 (`bluetti-b500k-charger-2`) | 5,120 | same | $2,199 | ships now |
| B500K + Charger 2 + DC Hub (`bluetti-b500k-charger-2-dc-hub`) | 5,120 | same | $2,399 | ships now |
| Amazon B300K ×2 for Apex 300 ([B0FZ87DKWC](https://www.amazon.com/dp/B0FZ87DKWC)) | 5,529.6 | CA90 cable is Apex 300-only; Apex 200 not listed | $1,999.99 | delivery Dec 28 |
| Amazon B300K for AC300 ([B09SXJXH5H](https://www.amazon.com/dp/B09SXJXH5H)) | 2,764.8 | AC-series; Apex 300 needs the $99 CA90 cable | $1,044 | In Stock, Dec 9 |
| Amazon "B500K for Apex 300" (set option on B0FZ87DKWC) | 5,120 | Apex 300 | $2,099 | In Stock (ASIN not confirmed) |

**Winners:**
- **2× B300K → B500K + Charger 2** ($2,199, −8%, ships now). The runner-up is the identical 2× B300K on Amazon ($1,999.99). It arrives Dec 28, which beats Jan 20 but isn't "ships now", and its cable is Apex 300-only.
- **B300K + Charger 2 → plain B500K** ($1,599, 0%, ships now). It has 85% more Wh, but Charger 2 isn't included. The runner-up is B500K + Charger 2 at +37.5%, outside the band.
- **B300K + Charger 2 + DC Hub → B500K + Charger 2** ($2,199, +22%). It has no DC Hub. The exact B500K + Charger 2 + DC Hub bundle is +33%, outside the band.

**Band flag for Barry.** The plain B500K ($1,599) is the cleanest like-for-like for 2× B300K (−7% Wh, $800 cheaper), but at −33% it falls outside the ±25% band. Under the band rule the winner pushes a $400 Charger 2 onto a shopper who only wanted a battery.

**Review:** [digitalreviews.net B500K](https://www.digitalreviews.net/reviews/lifestyle/bluetti-b500k-review-expansion-battery-australia/) (endurance tests in an Apex 300 + B300K + B500K stack; no full capacity test).

## C. Panels

| Panel | W | Type | Voc | Isc | Weight | Price (web read) | Stock |
|---|---|---|---|---|---|---|---|
| BLUETTI SORA 500 (original, BLUETTI) | 500 | folding, N-type, IP67 | 49.1 V | 13.31 A | 12.9 kg | $849 | late January |
| **SORA 500 on Amazon** ([B0GXTVVHS3](https://www.amazon.com/dp/B0GXTVVHS3)), sold by Bluetti, FBA | 500 | same item (model SORA 500) | 49.1 V | — | 28.4 lb | $899 | delivery Dec 3–7 |
| ALLPOWERS SP039 ([store](https://iallpowers.com/products/allpowers-sp039-600w-monocrystalline-portable-solar-panel)) | 600 | folding | 52.8 V | 14.99 A | 12.47 kg | $599 (Amazon B0GWL361NJ $399, pre-release Dec 3) | in stock (collection) |
| ALLPOWERS SP037 (original) | 400 | folding | 45.3 V | 11.45 A | 18.5 kg | $379.05 | pre-order, no date |
| **SP037 on Amazon** ([B0BG6ZTJB2](https://www.amazon.com/dp/B0BG6ZTJB2)), GiarideDirect, FBA | 400 | same (AP-SP-037) | 45.3 V | 11.45 A | 40.8 lb | $299 | release Dec 7, delivery Dec 11–17 |
| SP037 on Amazon ([B0FCMD8RDJ](https://www.amazon.com/dp/B0FCMD8RDJ)), POWISER STORE | 400 | same | — | — | — | $399 ($100 coupon shown) | release Dec 1, delivery Dec 8 |
| Renogy 400W Portable ([B0F4JR1PFM](https://www.amazon.com/dp/B0F4JR1PFM)) | 400 | folding | not confirmed | — | — | $469.99 | delivery Dec 8 |
| Anker SOLIX PS400 | 400 | folding | 57.6–60 V (too close to 60 V inputs) | — | — | ~$490–500 (older reads) | not read |
| BLUETTI PV100 FX 6-pack (original) | 6×100 | flexible, 240° | 41.4 V each | 3.05 A | 2.2 kg each | $987 | sold out |
| **PV100FX 2-pack on Amazon** ([B0FS67DKV5](https://www.amazon.com/dp/B0FS67DKV5)), Bluetti | 2×100 | same (model PV100FX) | 41.4 V | 3.0 A | 9.7 lb/pack | $279.99 ×3 = $839.97 | "Only 10 left", delivery Dec 9 |
| BougeRV Arch 2.0 200 W (`bougerv-arch2-200w`) | 200 | flexible, 270° | 28 V | 8.75 A | 8.8 lb | $207 ×3 = $621 (record) | not read |

**Winners (all the identical product on Amazon: same brand, earns with our tag):**
- **SORA 500 → Amazon B0GXTVVHS3** ($899, +6%, delivery Dec 3–7). The SP039 runner-up is 29% under, outside the band.
- **SP037 → Amazon B0BG6ZTJB2** ($299, −21%, release Dec 7). That is inside the 14-day window and sooner than the original's open date. Both Amazon SP037 listings are third-party sellers, not ALLPOWERS. Note that ALLPOWERS' own collection page lists SP037 as "In stock" at $379.05 while our record says pre-order, so re-read the product page.
- **PV100 FX 6-pack → 3× Amazon PV100FX 2-pack** ($839.97, −15%, delivery Dec 9). With only 10 left, stock is thin. BougeRV Arch 2.0 ×3 is 37% under, outside the band, and its 28 V Voc changes 48 V string design.

**Reviews:**
- SORA 500: [Impulse Gamer](https://www.impulsegamer.com/?p=274334) (also the source of our Voc/Isc figures).
- SP037: [The Gadgeteer](https://the-gadgeteer.com/2023/01/08/allpowers-400w-portable-solar-panel-review-more-power) (329 W on a cloudy day; review sample).
- PV100 FX: [backuppowerhub](https://backuppowerhub.com/?p=4373) (marketing-adjacent, no lab data).

## Open items / what I could not verify
- Best Buy and Home Depot FridgePower listings (Best Buy once listed $849) could not be read. If either shows the FridgePower in stock, it is the identical item but doesn't earn.
- The Amazon ASIN for "B500K for Apex 300" ($2,099, In Stock) wasn't found.
- Renogy 400W Voc wasn't confirmed.
- The BougeRV Arch price and stock weren't re-read.
- Mango Power E stock is only "allow an additional 1–2 weeks".
