# ALLPOWERS S2000 Pro + SP037 kit: objections and honest answers (research angle 5)

Researched 2026-10-29. Scope: why shoppers hesitate on the S2000 Pro + SP037 400 W kit, the factual answer to each, and when the honest answer is "then don't buy it". Runtime and solar math are in 4-usecase.md; ALLPOWERS-wide warranty, returns, ratings and compare-at findings are reused from the R4000 file (`growth/focus/allpowers-r4000-3456wh/research/5-objections.md`, 2026-10-28) and only re-checked where the kit differs.

## Baseline facts used below (checked 2026-10-29)

- **Kit:** "ALLPOWERS Solar Generator Kit 2400W (S2000 Pro + SP037 400W Solar Panel)", $963.00, compare-at $1,999.00, one variant, SKU `AP-SS-009-PRO+AP-SP-037`, created 2024-11-24, republished 2026-09-02 (source: https://iallpowers.com/products/allpowers-solar-generator-kit-2400w-s2000-pro-sp037-400w-solar-panel.js, acc. 2026-10-29).
- **Station alone:** $664.00, compare-at $1,399.00, SKU `S2000-PLUS-US`, created 2022-02-16 (source: https://iallpowers.com/products/allpowers-2400w-portable-power-station.js, acc. 2026-10-29). **SP037 alone:** $299.00, compare-at $699.00 (source: https://iallpowers.com/products/allpowers-400w-portable-solar-panel.js, via SP037 dossier, acc. 2026-10-28).
- **Cart tests 2026-10-29** (source: `growth/focus/allpowers-s2000-pro-sp037-solar-kit/research/cart-check-2026-10-29.md`; kit tests 2026-10-27/28 in `src/coupons.json`): kit + ALLPOWERS26 $866.70; station + SP037 as separate items + BULKRATE **$857.07**; the R2500 V2 (1,920 Wh LiFePO4) + SP037 + BULKRATE $852.62. A fresh cart gets an automatic 5% first-order discount that a valid code replaces.
- Short names, all acc. 2026-10-29 unless noted:
  - PAGE: https://iallpowers.com/products/allpowers-2400w-portable-power-station
  - KIT: the kit page above (same body text, spec table, FAQ and 52 reviews as PAGE)
  - MAN: "S2000PRO V3.0" manual from PAGE's "Download Manual", https://cdn.shopify.com/s/files/1/0443/1223/2089/files/YPJSS0055-S2000PRO_V3.0_AP-SS-009-PRO_user_mannual.pdf?v=1716446947 (file stamp 2024-05-23). Read with PDFKit; certification row and drawings read from rendered images; app QR codes decoded with macOS Vision.
  - WARRANTY: https://iallpowers.com/pages/warranty-policy
  - RETURNS: https://iallpowers.com/pages/returns-and-refunds
  - REFUND-POLICY: https://iallpowers.com/policies/refund-policy (via R4000 file, acc. 2026-10-28)
  - WAYBACK: captures of PAGE, https://web.archive.org/web/<timestamp>/https://iallpowers.com/products/allpowers-2400w-portable-power-station, timestamps 20220627085055 to 20260616001553 (20 captures, list from the CDX API)
- **Reviews used:** StorageReview, 2023-04-07, https://www.storagereview.com/review/allpowers-s2000-pro-portable-power-station-review ; The Gadgeteer (Matt Gregersen), 2024-01-11, https://the-gadgeteer.com/2024/01/11/allpowers-s2000-pro-portable-power-station-review-a-decent-1500-wh-power-station-with-rv-plug/ ; NerdTechy, 2023-02-25, https://nerdtechy.com/allpowers-s2000-pro-review ; The Solar Lab, undated, https://www.thesolarlab.com/review/allpowers-s2000-pro-review . All read through WebFetch; figures are as that tool reported them.

## Source notes

- Web searches used: 7 of the 15 shared. Reddit came from PullPush (two queries answered). No independent test of a current (1,451.6 Wh, 150 V-input) unit turned up.
- Seller-hosted reviews on PAGE/KIT (Loox, 4.6/5 from 52) are self-selected and some are from non-US stores. Desertcart listings mirror marketplace reviews; they reached us only as search snippets, so they are marked unverified.
- PAGE and KIT print "Sold out" and "OUT OF STOCK" in their static HTML, as every iallpowers.com page does (SP037 dossier). The `.js` records say `available: true`.

---

## 1. "It's NMC, not LiFePO4. Is it safe, and how long will it last?"

**(a) Where raised.**
- The Gadgeteer (2024-01-11): the reviewer prefers LiFePO4 for longevity and doubts ALLPOWERS' claim that ternary cycle life is "nearly the same".
- StorageReview (2023-04-07) lists the NCM chemistry among its reasons it is "difficult to recommend this model".
- A Ukrainian test video bills it as the first 1.5 kWh station on "потрійному літії (NCM)" (ternary lithium) the reviewer tested (ProstoMob, 2026-06-29, https://www.youtube.com/watch?v=LlSho0Ks_Aw; Reddit cross-post https://www.reddit.com/r/ProstoMob/comments/1ulfe7t/ , 2026-07-02).
- ALLPOWERS frames the trade itself: its R2500 page says LiFePO4 "is heavier than ternary Li-ion batteries, but has excellent cycle times" (source: https://iallpowers.com/products/allpowers-r2500-v2-portable-power-station-2500w-1920wh).

**(b) Facts.**
- **Chemistry.** MAN Q1: "Ternary lithium battery". 1,451.6 Wh (43.2 V 33.6 Ah) (source: MAN).
- **Cycle claim.** PAGE: "Battery with 2,500+ Life Cycles to 80%". WAYBACK captures from 2023-09-26 to 2025-09-08 add "lasts for almost 10 years". MAN gives no cycle figure.
- **What 2,500 means (ESTIMATE, 4-usecase.md §4):** 6.8 years at one full cycle a day; 48 years at one a week, so for backup use calendar aging sets the life.
- **How it compares.** Sandia cycled commercial cells for years: NMC reached 80% after 200 to 2,500 equivalent full cycles depending on conditions, LFP after 2,500 to 9,000, NCA 250 to 1,500; NMC was more sensitive to full 0–100% cycling (source: Preger et al., J. Electrochem. Soc. 167 (2020) 120532, https://www.osti.gov/pages/biblio/1650174). So ALLPOWERS' 2,500 sits at the top of the NMC range Sandia saw.
- **Calendar aging.** "NCA and NMC cells exhibited particularly rapid capacity fade at 100% SOC", and fade rises with temperature (source: Preger 2020). Keil et al. advise that high storage SoCs "should be avoided" (J. Electrochem. Soc. 163(9), 2016-07-06, https://iopscience.iop.org/article/10.1149/2.0411609jes). ALLPOWERS' own storage advice is 30% to 60% every three months (MAN Q6), and its FAQ says "it is recommended not to charge and discharge at ordinary times, except in emergencies" (PAGE).
- **Thermal behavior.** In Golubkov et al.'s tests, as summarized by Lei et al., "The onset temperatures and amount of released gas of LFP, NMC, and LCO/NMC were 195 °C and 50 mmol, 170 °C and 150 mmol, 150 °C and 270 mmol". In Lei et al.'s own ARC tests of 18650 cells the NMC cell peaked at 731 °C and the LFP cell at 259 °C; the NMC cell had twice the capacity (source: Lei et al., "Experimental Analysis of Thermal Runaway in 18650 Cylindrical Li-Ion Cells Using an Accelerating Rate Calorimeter", Batteries 3 (2017) 14, published 2017-04-12, https://publikationen.bibliothek.kit.edu/1000079077/6013714). Laptops and many EVs use NMC; the difference is in how hot and how much gas a failing cell produces, which is the BMS's and the enclosure's job to prevent.
- **Recalls.** CPSC's recall API returns no recalls for "allpowers" in recall title or product name (source: https://www.saferproducts.gov/RestWebServices/Recall?format=json&RecallTitle=allpowers and `ProductName=allpowers`, acc. 2026-10-29).
- **Certification marks.** MAN's "Certification" row shows a UL mark, a PSE mark, CE, FCC, RoHS, IC and UKCA (read from the rendered manual). See 6d: no UL file number or standard is given.
- **The upside.** NMC is why it is light: 112 Wh/kg against 79 Wh/kg for ALLPOWERS' LFP P1800 (1,024 Wh, also 13 kg) and 66 Wh/kg for the LFP R2500 V2 (1,920 Wh, 29 kg) (4-usecase.md §4).
- MAN's fire note: "In case of fire, dry powder fire extinguisher can be used or immersed in water" (source: MAN §1).

**(c) Page line.** "The S2000 Pro uses NMC (ternary) cells rated for 2,500 cycles to 80%, about 7 years of daily cycling; NMC packs more energy per pound than LiFePO4 but ages faster when kept full and runs hotter if a cell fails, so store it at 30–60% as ALLPOWERS advises."

**(d) When the objection wins.** Daily solar cycling for 10+ years, or a unit kept full on the wall all year as a UPS, or storage in a living space where you want the more forgiving chemistry. If weight is not the limit, ALLPOWERS' own R2500 V2 is LiFePO4, 1,920 Wh, "3500+ Cycles", at 29 kg instead of 13 kg. With an SP037 and BULKRATE it came to $852.62 in our 2026-10-29 cart test, $4.45 less than the S2000 Pro + SP037 (source: R2500 V2 page; cart check). Other rivals: 3-rivals.md.

## 2. "Its own page says 1,000 W and 650 W of solar. Which is it, and can I use two panels?" (strongest objection)

**(a) Where raised.**
- PAGE itself: spec table "Solar Input (12~150)V 13A, 1000W Max"; description "1000W Max Solar Input in 1.5 hours"; FAQ "maximum solar input of 650W" and, for third-party panels, "Voltage Range: 18-70V", "Current Range: Under 18A" (source: PAGE; KIT identical).
- Reviews quote the old figure: "MPPT 18-70V, 18A 650W Max" (StorageReview, 2023-04-07; The Gadgeteer, 2024-01-11). NerdTechy (2023-02-25) says "up to 650W".
- Owners run panels in series: The Gadgeteer's two 200 W panels "wired in series"; "2000 PRO+ 2 200W panels" (Steve H., 2023-03-18, PAGE review).
- The kit description adds a third story: "supports to be charged by 2* solar panel 200W in parallel (400W max). You also can connect more panels to get more power( 650W max, 3 hours to full)" (source: KIT `.js` description).

**(b) Facts.**
- **The spec changed in 2024.** WAYBACK shows "Solar Input：18-70V, 18A 650W Max" on every capture from 2022-06-27 to 2024-02-20, and "(12~150)V 13A, 1000W Max" on every capture from 2024-06-24 to today. The FAQ's third-party block (present in the 2026-06-16 capture; the 2026-01-02 capture did not parse) repeats the old numbers.
- **The current manual says 150 V.** MAN (V3.0, file 2024-05-23): "Solar Input: (12~150)V 13A, 1000W Max"; "Before connecting the solar panel, please confirm that the output voltage specification of the solar panel is within 150V, the maximum current is 13A, and the maximum charging power is within 1000W"; the diagram caption is "Users can charge the product by connecting solar panels in series as shown in the figure"; the Chinese label adds "(可多个串并联)" (several can be connected in series or parallel). Overvoltage shows as fault E212 "MPPT input overvoltage" (source: MAN).
- **The FAQ contradicts itself.** It lists ALLPOWERS' SP033 200 W as compatible "Up to 3 series connections". Three SP033s (Voc 44.4 V each) make 133 V, which only a 150 V input accepts (source: PAGE FAQ; SP033 page https://iallpowers.com/products/allpowers-sp033-portable-polycrystalline-solar-panel-200w-flash-deal). It lists the SP037 with no series count.
- **Two SP037s (ESTIMATE, 4-usecase.md §3.2):** in series, V3.0 panels reach 90.6 V at 25 °C and 113 V at −40 °C: inside 150 V, outside 70 V. V5.0 panels reach 73 V, also outside 70 V. In parallel, short-circuit current is about 23 A, above both 13 A (manual) and "Under 18A" (FAQ). Three V3.0 in series pass 150 V on mornings below about 0 °C to −10 °C.
- **What you get:** one SP037 gives 260–320 W in good sun and refills in 4.8–6.2 h; two in series give 520–640 W and 2.4–3.1 h. Neither reaches 1,000 W or 650 W (4-usecase.md §3.3). The SP037 manual itself says "it is normal to finally get 260-320W" (SP037 dossier).
- **Which unit you have.** No document we found ties the input range to a serial, date or label. The station SKU changed from `AP-SS-009-PRO-US` (captures to 2025-09-08) to `S2000-PLUS-US` (by 2026-06-16); the kit SKU still reads `AP-SS-009-PRO` (source: WAYBACK; `.js` records). Units bought before mid-2024, or old stock from other sellers, may have the 70 V input. Unverified.

**(c) Page line.** "Plan on one SP037 (about 260–320 W, a full refill in 5–6 sunny hours); the current manual allows a second SP037 in series (90 V on a 12–150 V input) for about 520–640 W, but the same page's FAQ still lists an older 18–70 V limit, so confirm your unit's input range with ALLPOWERS before wiring two."

**(d) When the objection wins.** If you need more than about 300 W of solar and cannot confirm the 150 V input on your unit, this kit is capped at one panel. Anyone who wants 1,000 W of real solar input should not count on reaching it with SP037s; it would take three or more panels in series, which cold mornings push past 150 V. Get the input range in writing (service@allpowers.com) or look at a station whose solar limits are stated once and consistently (3-rivals.md).

## 3. "Why buy the kit if it costs the same as buying the two separately?"

**(a) Where raised.** Our own cart tests (Baseline). KIT advertises "Save 52%" against a $1,999 compare-at.

**(b) Facts.**
- **Same list price.** $963.00 = $664.00 + $299.00 (source: `.js` records). The kit's compare-at ($1,999) is below the two compare-ats added ($1,399 + $699 = $2,098).
- **Separates are cheaper with a code.** Kit + ALLPOWERS26 = $866.70; station + SP037 as two line items + BULKRATE (11% on 2+ items, expires 2026-11-15) = $857.07, $9.63 less. Codes replace the automatic 5% first-order discount; they did not stack in any test (source: cart check).
- **You lose nothing in the box.** KIT Note 1: the kit "includes solar cable". The SP037 sold alone includes "1*Solar Cable to XT60 Solar Cable" and a DC5525/DC8020 adapter (source: SP037 US page via SP037 dossier 1-maker.md). The station alone includes "S2000 Pro, AC Adapter, User Manual" (source: PAGE description).
- **Shipping is the same.** Kit buyers get two packages anyway: "the solar panels and power station will be shipped separately" (KIT Note 2). An owner: "Solar panels were shipped separately. But came the same day, 2 different carriers" (Robert E., 2023-03-14, PAGE review).
- **No 2-panel kit.** The S2000 Pro + SP037 kit has one variant. A second SP037 bought with the station makes three items at $1,262; BULKRATE at 11% would make it $1,123.18. That is arithmetic, untested at the cart.
- **Same hardware?** The kit SKU names `AP-SS-009-PRO`; the station sold alone is `S2000-PLUS-US`. Whether they are the same build is unverified (see objection 2).
- **Returns (inference).** Two line items may be simpler to return one at a time than one kit SKU, which RETURNS would treat as "lack of accessories" if the panel came back alone (see 4). Whether removing one BULKRATE item claws back the discount is unverified.

**(c) Page line.** "The kit costs exactly the station plus the panel ($963), so buy them as two items with BULKRATE ($857.07 on Oct 29, until Nov 15) instead of the kit with ALLPOWERS26 ($866.70); the panel still comes with its XT60 cable."

**(d) When the objection wins.** Always, while BULKRATE lasts. After 2026-11-15 the kit with a 10% code and the separates with a 10% code cost the same; then the kit is a convenience SKU only.

## 4. "Warranty: 5 years or 24 months? And can I return 'sale items'?"

**(a) Where raised.**
- KIT shows a "5-year Warranty" badge while its own description says "24-month warranty and friendly customer service" (source: KIT `.js` description). The site header says "Up to 5-Year Warranty".
- Support complaints on PAGE: "bought this through Amazon, and no less than a week later, it won't turn on. I've tried to get a hold of customer service, and its seems like no one's there" (Eric L., 3/5, 2026-10-12); an AC charging port failure, return label issued, no word after two weeks (Bill T., 3/5, 2025-02-23); "Cannot get it it charge or come on" (Randy V., 2/5, Verified, 2026-01-11). Positive: "thank you for replacing my S2000 Pro so quickly" (Ronald F., 5/5, 2026-10-18).
- The Solar Lab says its test email went unanswered (undated).
- Brand-wide (R4000 file, acc. 2026-10-28): Trustpilot 2.2/5 from 108 reviews, "Hasn't replied to negative reviews"; BBB "Allpowers" (Walnut, CA) rated F for "Failure to respond to 7 complaint(s)".

**(b) Facts.**
- **Station: 5 years, panel: 2 years.** WARRANTY lists "S2000 PRO" under "A) 5-Years Limited Warranty" and the SP037 (printed "S037") under "B) 2-Years Limited Warranty" with the other panels. So the kit carries two terms. Refurbished S2000 PRO: 2 years; refurbished SP037: 1 year (source: WARRANTY).
- **Registration.** "The warranty period is 24 months from the date of purchase, but ALLPOWERS only needs to register the product on the official website to extend the warranty period of some products" (source: WARRANTY). Read plainly, the station's 5 years may require registration at https://iallpowers.com/pages/warranty-register. RETURNS gives a third base term: "The warranty period is 18 months". Which governs is unverified (same conflict as the R4000).
- **The panel's own manual says 3 years.** SP037 manuals: "3 years material and workmanship guarantee; ensure that the output power is 80% within 5 years" (SP037 dossier 1-maker.md). The policy page says 2.
- **Shipping for repairs.** ALLPOWERS pays return freight within 30 days of receipt; after that, "the shipping cost of returning the product to the warehouse for repair will be borne by the buyer" (source: WARRANTY). The station is 13 kg and 1,451.6 Wh; USPS caps mailed lithium batteries at 100 Wh, so it goes by ground carrier (USPS bulletin via R4000 file; inference).
- **Where you buy matters.** Only the official US, DE and UK sites are covered; "If you buy from another online store or seller ... it is not covered by the official manufacturer's warranty". Orders on other "official platform stores" are passed to that platform (source: WARRANTY). Eric L.'s Amazon unit falls in that path.
- **Returns.** RETURNS: 30-day money back for direct purchases, but "not applicable for items with open box or lack of accessories"; "Returns must include all accessories"; "Items must include original packaging"; subjective returns pay their own freight; used units returned for non-quality reasons lose "15%-50% depreciation"; RMA required; the clock runs "from the original shipment date". REFUND-POLICY: "we cannot accept returns on sale items or gift cards", and every listing, the kit included, shows a sale price (source: RETURNS; REFUND-POLICY via R4000 file).
- **Kit-specific.** Two packages arrive on different days from different carriers; the 30-day window runs from the original shipment date (RETURNS), so the later package shortens it. Returning only the panel from a kit SKU would be a return with a "lack of accessories" (inference; unverified how ALLPOWERS handles it). Commercial use is excluded (source: RETURNS).

**(c) Page line.** "ALLPOWERS lists a 5-year limited warranty on the S2000 Pro (register it) but only 2 years on the SP037, pays repair freight only in the first 30 days, covers only official-store orders, and its returns page excludes opened boxes; keep both boxes until both parts are tested."

**(d) When the objection wins.** Buyers who need dependable support (sole medical backup, business use) or who would buy from a marketplace seller. Within ALLPOWERS nothing changes the support picture; see 3-rivals.md for brands with phone support.

## 5. "A 40 lb panel plus a 29 lb station: how portable is this?"

**(a) Where raised.**
- On the SP037: "very good quality, quite heavy so not easy to move about easily" (Christine R., 2023-01-29, SP037 page review).
- On the station, positive: "present battery pack is much heavier with half the power" (Antonio N., 4/5, Verified, 2026-07-16, PAGE). "Generator weights 32lbs" (Robert E., 2023-03-14, PAGE).
- The Gadgeteer: the raised handles and weather cover make it awkward to pick up and to stack on (2024-01-11).

**(b) Facts.**
- **Station:** 13 kg / 28.66 lb, 37.5 × 24.5 × 25 cm (MAN; PAGE). Earlier units were 14.5 kg / 32 lb (WAYBACK captures to 2025-04-22; The Gadgeteer).
- **Panel:** SP037 V3.0 18.5 kg / 40.79 lb, folded 1,048 × 532 × 65 mm, 2.66 m long unfolded. V5.0 13.8 kg / 30.42 lb, folded 93.5 × 60 × 6 cm (SP037 dossier 1-maker.md). Which version the kit ships is unknown.
- **Kit total (arithmetic):** 31.5 kg / 69 lb with a V3.0 panel; 26.8 kg / 59 lb with V5.0. Two separate carries.
- **Comparison.** ALLPOWERS' LFP P1800 also weighs 13 kg with 1,024 Wh; the LFP R2500 V2 weighs 29 kg with 1,920 Wh (P1800 dossier; R2500 V2 page). For 1.45 kWh the S2000 Pro is the light option.
- **Lighter panel options from ALLPOWERS:** SP033 200 W at 6.3 kg, Voc 44.4 V (SP033 page). Two in series (89 V) need the 150 V input, as in objection 2. Price and stock not checked.
- PAGE FAQ: "the S2000 Pro is not waterproof". MAN: "Please do not expose the product to rain and snow."

**(c) Page line.** "The station is a one-hand 13 kg (29 lb) carry; the SP037 is the heavy part at up to 18.5 kg (41 lb) folded to about 105 × 53 cm, so the kit moves in two trips."

**(d) When the objection wins.** Hiking-in camping, a single person carrying both pieces any distance, or a small car trunk. Buy the station with smaller panels (two 200 W panels, if your unit has the 150 V input) or a smaller station (3-rivals.md).

## 6. Shorter objections

### 6a. "The app is Bluetooth-only"

- **(a)** The Gadgeteer: the app requires an account, adds nothing beyond the screen except switching AC frequency, and "works only within Bluetooth range" (2024-01-11). StorageReview: Bluetooth "would not fully connect during the first half of charging" (2023-04-07). NerdTechy: the Android app could not pair (2023-02-25).
- **(b)** MAN: "Bluetooth: Support"; no Wi-Fi. Bluetooth is "turned off by factory default"; hold "DC OUTPUT" for 3 seconds to turn it on (MAN Q10). App screens: remaining time, battery, input and output power, AC and DC switches, frequency (MAN §3.6.3). PAGE: "up to 10 meters away". The manual's QR code opens "ALLPOWERS2" (App Store id1612734937; Google Play com.allpowers.aipower), rated 1.6/5 from 34 ratings, version 2.0.2 of 2026-10-27 (source: decoded MAN QR; https://itunes.apple.com/search?term=allpowers&entity=software&country=us, acc. 2026-10-29). Its store text mentions Wi-Fi, which this station lacks. ALLPOWERS' R2500 V2 lists "Wi-Fi / Bluetooth" (R2500 V2 page).
- **(c)** "The S2000 Pro's app works over Bluetooth only (about 10 m, off by default), so there is no remote monitoring from away; the front screen shows everything the app does."
- **(d)** Wins if you want to watch an outage or a cabin from your phone away from home: a Wi-Fi model (the R2500 V2, or rivals).

### 6b. "How fast is the UPS? Can it sit on my fridge, PC or CPAP all the time?"

- **(a)** PAGE: "UPS will immediately supply battery backup power. Excellent for refrigerators, gaming consoles, computers". Owner: "it can act as a pass-through/UPS so I can keep my fridge plugged into it" (Jennifer C S., 5/5, Verified, 2025-07-09, SP037 kit).
- **(b)** MAN §3.5: switches "within 15ms"; "the maximum power of the AC output ports should not exceed 1500W when the mains voltage range is 100~120V", otherwise grid and battery share the load "until the power station consumes to 5%"; "It is recommended to use only one device". PAGE FAQ: "for battery life maintenance, it is recommended not to charge and discharge at ordinary times, except in emergencies"; while wall-charging only USB and AC outputs work. ATX 3.1 asks PC power supplies to hold up 12 ms (Seasonic, via R4000 file), so 15 ms may drop some PCs (inference). MAN §7 excludes medical equipment. NMC fades fastest held at 100% (objection 1).
- **(c)** "UPS switchover is up to 15 ms with a 1,500 W limit, and ALLPOWERS itself advises against routine pass-through use; fine for a fridge in an outage, not a substitute for a real UPS on a PC or CPAP."
- **(d)** Wins for anything that must not blink or must sit on the wall for years: a dedicated UPS, or an LFP station built for always-on pass-through.

### 6c. "Can it handle cold weather?"

- **(a)** No dated shopper thread found. An owner ran the panels at "20 degrees outside" and saw them "charging at over 90% efficiency" (Steve H., 2023-03-18, PAGE; the station's location is not stated).
- **(b)** MAN: charge 0 to 40 °C (32–104 °F); discharge −10 to 40 °C (14–104 °F); storage −20 to 40 °C, "recommend: 20~30℃". Faults E102 "Charging low temperature protection" and E104 "Discharge low temperature protection". No battery heater is mentioned (inferred from absence). Sandia: NMC cells degraded more as cycling temperature fell, and "LFP cells are more suited for lower temperature applications" (Preger 2020). Panels: one SP037 stays under 57 V at −40 °C; two in series stay under 114 V (4-usecase.md §3.2).
- **(c)** "It won't charge below freezing (32 °F) or run below 14 °F and has no self-heating, so in winter keep the station indoors and run only the panel's cable outside."
- **(d)** Wins for an unheated garage, van or cabin that must recharge from solar below freezing: buy a self-heating model (3-rivals.md).

### 6d. "Is it UL listed or otherwise certified?"

- **(a)** General category worry; our search for a UL listing found nothing (search 2026-10-29).
- **(b)** MAN's certification row shows a round UL mark with no file number, no standard and no "C US" text, plus PSE, CE, FCC, RoHS, IC and UKCA. PAGE claims no certification. A search turned up no UL 2743 or other UL listing for the S2000 Pro (2026-10-29); UL Product iQ was not checked (login). CPSC: no ALLPOWERS recalls (objection 1). The R4000's manual showed no UL mark at all (R4000 file).
- **(c)** "The manual prints a UL logo but no file number or standard, and we found no UL listing for the S2000 Pro; treat it as uncertified until ALLPOWERS supplies a UL file number."
- **(d)** Wins if an insurer, landlord, HOA or workplace requires a listed product (UL 2743 or similar).

### 6e. "Is the $1,999 compare-at price real?"

- **(a)** KIT: "Regular price $1,999.00", "Save 52%"; PAGE "Save 53%"; "HALLOWEEN SAVINGS ➤ Up to 65% Off".
- **(b)** The kit URL has no Wayback captures (CDX query 2026-10-29 returned none). Station listing on WAYBACK (sale / compare-at): 2022-06-27 $1,799 / $2,999; 2022-10-02 $1,999 / $2,999; 2022-12-21 and 2023-02-07 $1,500 / $2,499; 2023-09-26 $1,099 / $1,299; 2023-11-24 $799 / $1,299; 2024-02-20 $979 / $1,299; 2024-06-24 and 2024-09-07 $899 / $1,799; 2025-01-25 $879 / $1,299; 2025-04-22 $699 / $1,299; 2025-08-09 $714 / $1,299; 2025-09-08 $699 / $1,399; 2026-06-16 **$549** / $1,399; today $664 / $1,399. No capture since 2023 shows the station near its compare-at, and the SP037 has never been captured at its $699 compare-at (SP037 dossier). The kit's $1,999 is the sum of two compare-ats neither part has sold at recently. FTC Guide 16 CFR 233.1 on former-price comparisons and California B&P 17501: see R4000 file objection 2.
- **(c)** "Ignore the $1,999 'regular' price: the kit is simply $664 + $299, the station has listed between $549 and $1,099 since late 2023, and today's best net is $857.07 for the two items with BULKRATE."
- **(d)** If you can wait: the station listed at $549 in June 2026, $115 below today, and Black Friday is 2026-11-27. Waiting buys a chance, not a sure saving.

## 7. Other objections shoppers raise

### 7a. "Will I really get 1,451 Wh?"

- **(a)** StorageReview "measured a discharge capacity of 920Wh with a 350W load"; the unit "powered off with 22 percent remaining" and went "from 56 percent complete to 100 percent in fewer than 10 minutes" on recharge, which it calls calibration trouble (2023-04-07, a 1,500 Wh-labelled unit). Desertcart buyer snippets report a unit at about 595 Wh after cycles and one dropping from above 50% to 0% (undated, unverified). Owner: "touchy accepting charge especially below 60% charged" (Stacey C., 4/5, 2025-04-03, PAGE).
- **(b)** MAN Q9: "the actual output capacity of the product is lower than the capacity specified". ALLPOWERS' rule is 85% for AC (1,234 Wh). No test of a current unit found. The power-station category typically delivers 80–90% (our P1800/R4000 assumption).
- **(c)** "Expect about 1,200 Wh from the wall outlets by ALLPOWERS' own 85% rule; the one lab test we found (2023 unit) measured 920 Wh."
- **(d)** Wins if a run-time number is critical (medical, fridge through a known outage length): size up, or buy where you can return an opened unit.

### 7b. "Is it really 2,400 W?"

- **(a)** The Solar Lab: its unit shut off "at 55% battery" under 2,250 W with an overload error, and it calls the 2,400 W rating false advertising because output is capped near 2,050 W below 70% (undated).
- **(b)** MAN: "(*When the battery drops to ≈60%, the rated AC output is 2000W Max.)"; "AC+DC Total Output: 2700W Max". PAGE does not mention the derate. Surge 4,000 W, duration not stated.
- **(c)** "It delivers 2,400 W only while the battery is above about 60%; below that the limit is 2,000 W, so plan heavy loads at 2,000 W or less."
- **(d)** Wins for a load that runs above 2,000 W for long (large heaters at 120 V top out at 1,500 W, so mostly tools and combined loads).

### 7c. "Reliability: units that won't turn on or stop charging"

- **(a)** PAGE reviews quoted in 4(a); "Unit does NOT power up ... Has only worked twice" (Darel B., 2024-01-10); on the SP037 page: "we've had 3 of the power stations and all have failed to do what they're supposed to do" (Christine R., 2023-01-29, a "monster pro s2000"). Reddit: an owner left a new S2000 Pro "connected for a few days" to solar and found it "totally bricked" (2024-07-24, https://www.reddit.com/r/allpowerssolar/comments/17p0d19/rallpowerssolar_ask_anything_thread/lericay/).
- **(b)** These are owner reports, not failure rates. MAN lists fault codes E102–E301 with recovery steps; "Other faults ... Please consult customer service". MAN Q6 storage advice: 30% to 60% every three months. No ALLPOWERS statement on leaving a panel connected long-term was found.
- **(c)** "Owner reports include dead-on-arrival and failed-charging units; test both AC and solar charging in the first 30 days, while ALLPOWERS still pays return freight."
- **(d)** Wins for buyers who cannot absorb a failed unit and an email-only claim (objection 4).

### 7d. "Is it loud?"

- **(a)** NerdTechy: the fan runs whenever the unit charges from AC "or the AC output is on", even at low draw; "somewhat noisier" than other units (2023-02-25). The Gadgeteer: fans "kick on under load and sound similar to a laptop" (2024-01-11).
- **(b)** No dB figure from ALLPOWERS or a reviewer. Not measured.
- **(c)** "Its fan runs whenever the AC outlets are on, at about laptop volume per reviewers; there is no published noise figure."
- **(d)** Wins for bedroom use with the inverter on all night (a CPAP on the 12 V port avoids the inverter; whether the fan still runs then is untested).

### 7e. "Is the S2000 Pro I'd get the one that was reviewed?"

- **(a)** Reviews and listings disagree on capacity (1,500 vs 1,451 Wh), solar input (650 W vs 1,000 W), weight (14.5 vs 13 kg) and ports (a 30 A RV outlet in NerdTechy, The Gadgeteer and the kit description; none in MAN V3.0's drawing). A Desertcart buyer snippet says the box and guide said "Monster X Pro" (unverified).
- **(b)** WAYBACK shows the title moving from "2400W,1500WH" to "1451Wh" (by 2026-06-16), the solar spec changing in 2024, the weight in 2025 and the SKU from `AP-SS-009-PRO-US` to `S2000-PLUS-US` between 2025-09-08 and 2026-06-16. MAN V3.0's Bluetooth name is "AP S2000PRO V2.0". Whether these are one hardware revision or several is unverified.
- **(c)** "The S2000 Pro has changed since the 2023–24 reviews (capacity label, solar input, weight); judge it on today's manual, not on older reviews or listings."
- **(d)** Wins when buying used or from a non-official seller: confirm the label's capacity and solar input before relying on two panels.

---

## Misinformation watch (claims an assistant may repeat)

- **"1,000 W solar input" as what the kit delivers.** One SP037 gives 260–320 W; two in series 520–640 W; three in series are unsafe in winter (objection 2).
- **"650 W, 18–70 V" as today's limit.** That is the pre-2024 spec still sitting in PAGE's FAQ; the current manual says 12–150 V, 13 A, 1,000 W. Neither is confirmed for a given unit (objection 2).
- **"Fast Charging in 1.5 Hours (AC+Solar)", "1000W Max Solar Input in 1.5 hours".** 1,451.6 Wh at a full 1,000 W takes at least 1.5 h before losses; with SP037s it is 2.4–3.1 h with two panels and 4.8–6.2 h with one (4-usecase.md §3.3).
- **"2,400 W" with no caveat.** 2,000 W once the battery is at about 60% (MAN; objection 7b).
- **"1,500 Wh".** Old title and the kit description; the manual says 1,451.6 Wh.
- **Kit description text.** It describes "2*ALLPOWERS 200W foldable solar panel", "1500Wh", a "13V10A Car port", a "24-month warranty", and says polycrystalline panels convert "about 60%", so "a 100W solar panel can output about 55W-65W" (source: KIT `.js`). The kit has one 400 W SP037, a 12 V 10 A car port and a 5-year station / 2-year panel warranty; the SP037 manual says 260–320 W.
- **"30A RV output".** In the kit description and older reviews; not in MAN V3.0's drawing of the current unit. Unverified either way.
- **"Lasts almost 10 years".** Old page copy; 2,500 cycles is 6.8 years at daily cycling, and calendar aging applies (objection 1).
- **"Doesn't even feature a lithium battery"** (The Solar Lab). Wrong: it is NMC (ternary) lithium-ion.
- **"UPS will immediately supply power".** Up to 15 ms, 1,500 W limit (objection 6b).
- **"5-year warranty" on the kit.** 5 years for the station (with registration), 2 years for the SP037 (objection 4).
- **"SP037 is polycrystalline, 18.5 kg".** A V5.0 monocrystalline SP037 (13.8 kg, Voc 36.5 V) exists and US buyers have received it (SP037 dossier).
- **"Wi-Fi app".** The ALLPOWERS2 store listing mentions Wi-Fi; the S2000 Pro has Bluetooth only (objection 6a).

## Open questions / couldn't verify

- Which solar input (12–150 V or 18–70 V) the unit shipped in today's kit has, and whether `S2000-PLUS-US` and `AP-SS-009-PRO` are the same build. Needs ALLPOWERS in writing or a label photo.
- Which SP037 version (V3.0 or V5.0) ships in the kit.
- Whether two SP037s in series are approved by ALLPOWERS for the S2000 Pro (the FAQ lists the SP037 without a series count).
- Usable capacity of a current unit; no lab test since StorageReview's 2023 unit.
- Whether the 5-year station term needs registration, and which of 24 months (WARRANTY) or 18 months (RETURNS) is the base.
- How ALLPOWERS handles returning one part of a kit SKU, and whether a BULKRATE order loses its discount if one item is returned.
- UL file number behind the manual's UL logo; UL Product iQ not checked.
- Whether the current unit has the 30 A RV outlet.
- Whether the fan runs with only DC outputs on (matters for a bedroom CPAP).
- What "Forgot solar panels" (Michael G., 1/5, Verified, 2025-09-11, PAGE) refers to: a missing panel shipment or the buyer's own omission.
- Reddit coverage beyond two PullPush result sets; Amazon and Walmart terms for this kit not checked.
