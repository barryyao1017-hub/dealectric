# R4000 research, angle 1: maker facts

- **Angle:** 1, MAKER FACTS (what ALLPOWERS itself publishes, plus its store's own history)
- **Product:** ALLPOWERS R4000 portable power station, US listing https://iallpowers.com/products/allpowers-r4000-power-station
- **Date:** 2026-10-28
- **Method:** curl against the live Shopify store (`.js`, `products.json`, `search/suggest.json`, policy pages, 10 s between calls); the two R4000 user manual PDFs on iallpowers.com, read with PyMuPDF and rendered crops for the parts that are images; the EU store (iallpowers.eu) for the V2; 25 Wayback Machine snapshots of the US product page (2023-02 to 2026-08) for SKU, barcode, spec and price history; 12 web searches; Wellbots and FactoryPure Shopify `.js`. Walmart and Amazon returned bot checks, so I stopped there (not bypassed). Local copies are in `/private/tmp/claude-501/-Users-jiayiyao-Desktop-dealectric/44f11078-b8ab-412e-a42d-cf3b4ee1b7ef/scratchpad/research/r4000-maker/`.

## 1. Original R4000 or an "R4000 Plus" / V2? Discontinued?

**Answer: the US listing is the original R4000 (3,456 Wh, 45 kg, 120 V). There is no "R4000 Plus" product anywhere I could find. "PLUS" is only in the SKU. The R4000 is not discontinued in the US. ALLPOWERS has an R4000 V2, but it is a smaller 2,880 Wh, 230 V model sold only on the EU store, next to the original.**

Evidence:
- The same Shopify product (ID 7595728568473, created 2022-12-23, published 2022-12-27) and the same variant ID (43392815595673) have existed from the first Wayback snapshot to today (source: https://iallpowers.com/products/allpowers-r4000-power-station.js, accessed 2026-10-28; https://web.archive.org/web/20231023074709/https://iallpowers.com/products/allpowers-r4000-power-station.js, 2023-10-23).
- SKU history of that one variant: `AP-SS-011` (Feb to Jun 2023), then `AP-SS-011-US` (Sep 2023 to 2026-01-10), then `R4000-PLUS-US` (2026-03-02 onward). The UPC changed at the same time, from 782940087302 to 747165451215 (source: https://web.archive.org/web/20260110215621/https://iallpowers.com/products/allpowers-r4000-power-station, 2026-01-10; https://web.archive.org/web/20260302035616/https://iallpowers.com/products/allpowers-r4000-power-station, 2026-03-02; live `.js` accessed 2026-10-28). I can't tell from outside whether the new UPC marks a production change. The page's spec table was word-for-word identical before and after the switch (same two snapshots).
- The SKU suffix is a catalog convention. The S2000 Pro is `S2000-PLUS-US` and the S1500 is `S1500-PLUS-US`. On the EU store the original 3,456 Wh R4000 is `R4000-PLUS-EU`, while the V2 is `R4000-V2-EU` (source: https://iallpowers.com/products.json?limit=250, accessed 2026-10-28; https://iallpowers.eu/products/allpowers-r4000-portable-power-station-4000w-3600wh.js, accessed 2026-10-28).
- No "R4000 Plus" turned up in web search, and the US store has no product with that name (source: https://iallpowers.com/search/suggest.json?q=r4000, accessed 2026-10-28; https://iallpowers.com/products.json?limit=250, all 200 products, accessed 2026-10-28).
- **R4000 V2 (EU only):** "ALLPOWERS R4000 V2 Portable Power Station 4000W 2880Wh", created 2026-03-27, €1,799 (compare-at €3,599), SKU R4000-V2-EU. Specs: 2,880 Wh, 40.5 kg, AC input 220–240 V 10 A, AC output 220–240 V 4,000 W (6,000 W peak), solar 12–60 V 2,000 W, AC+solar 3,000 W. Its "Download Manual" link points to the same R4000 V3.0 manual as the US page (source: https://iallpowers.eu/products/r4000-v2 and `.js`, accessed 2026-10-28). It is not on the US store (`products.json` and `search/suggest.json`, accessed 2026-10-28). The EU store still sells the original R4000 at €1,899 (EU `.js` above).
- The US R4000 is live and in stock: $1,499, compare-at $3,299, available true. It sits in the site nav as "Heavy Duty R4000 4000W | 3456Wh" (source: live `.js` and page, accessed 2026-10-28). I found no discontinued or EOL notice.
- **Sibling, not successor:** R3500 (3,200 W, 3,168 Wh, $1,199, created 2023-06-08) is still sold in the US. The EU store has an "R3500 V2 3500W | 2880Wh" (source: `products.json`, accessed 2026-10-28; iallpowers.eu nav, accessed 2026-10-28). Searches for a 2026 ALLPOWERS flagship launch found only smaller products (VOLIX P300, launched 2025-10-24; R1500 Lite) (source: https://iallpowers.com/blogs/news/new-product-launch-volix-p300-portable-power-station, accessed 2026-10-28).
- **The R4000 has already been revised once, quietly.** The 2023 page described a different spec: "4000W, 3600Wh", "Expand the capacity from 3600Wh to 21600Wh with 5pcs R4000", EV-station charging, "Unique Voice Control", solar 12–150 V, AC+solar 4,000 W, RV output also at 220–240 V (source: https://web.archive.org/web/20230205071523/https://iallpowers.com/products/allpowers-r4000-power-station, 2023-02-05). Manual V3.0 (PDF created 2023-12-27) gives 3,456 Wh (48 V, 72 Ah), three XT60 solar inputs at 12–60 V, AC+solar 3,000 W and B3000 battery expansion, and the unit pairs over Bluetooth as "AP R4000 V3.0". The 5-unit parallel claim was gone from the page by 2023-12-06, and EV charging and voice control by 2024-05-22 (Wayback snapshots of those dates). The page title kept "4000W 3600Wh" until early 2026. Buyers of used or third-party units could get either generation (unverified which one a given listing ships).

## 2. Spec sheet: US page vs user manual

Sources:
- PAGE = https://iallpowers.com/products/allpowers-r4000-power-station, accessed 2026-10-28
- MANUAL = https://cdn.shopify.com/s/files/1/0443/1223/2089/files/allpowers_R4000-AP-R4000_USER_MANNUAL-V3.0-_compressed_1.pdf?v=1712547934 (the one linked from the product page; "R4000 V3.0", PDF created 2023-12-27, uploaded 2024-04-08), accessed 2026-10-28
- MANUAL2 = https://cdn.shopify.com/s/files/1/0443/1223/2089/files/ALLPOWERS_-AP-R4000_New_manual-V3.0-231229__compressed.pdf?v=1710316865 (linked from https://iallpowers.com/pages/user-guides), accessed 2026-10-28. Its text is outlined, so I rendered and checked the inputs, outputs, battery, temperatures and AC-charging section. All match MANUAL.

| Item | PAGE | MANUAL | Notes |
|---|---|---|---|
| Capacity | 3456Wh | 3456Wh (48 V, 72 Ah) | |
| Chemistry, cycles | LiFePO4, >80% after 3,500 cycles, >50% after 6,500 | LFP | |
| AC output, 120 V | "Inverter 3600W"; "4 x Pure Sine Wave 100V-120V 3600W (peak 6000W)". Title and feature list say "4000W" | "AC: 100-120V Total output 3600W Max (peak 6000W Max)"; 220–240 V version 4,000 W | The PAGE FAQ wrongly says US buyers can run devices "up to 4000W" |
| AC outlets | 4 AC + 1 RV | "AC Output *4 (US 20A Max)"; "RV Port 30A" | NEMA face type not named. The manual drawing shows the RV socket as a round 3-pin TT-30-style receptacle (rendered crop). No L14-30, no 240 V on the US unit |
| RV port rating | "RV output 100V-120V 3000W" | "RV Port 30A" | MANUAL calls 3,600 W the *total* AC output. Inference: the RV port shares that one inverter limit. Not stated outright |
| Surge | 6,000 W peak | 6,000 W peak | No surge duration published |
| USB-C | 2× 100 W, total 200 W | 2× (5/9/12/15 V 3 A, 20 V 5 A), 100 W each | |
| USB-A | 2× 18 W fast, 2× 12 W | same | |
| Car port | 12 V 10 A, 120 W | 12 V 10 A, 120 W | |
| AC input | "AC input voltage 100V 15A / 110-120V 12.5A"; "AC input 2000W max" | "AC: (100~120)V~15A / (220~240)V~10A Max". Fast Mode max input "100-120V 1500W / 220-240V 2000W"; Standard 1,000 W; Mute 650 W. **Default mode is Mute** | **US AC charging tops out at 1,500 W.** 2,000 W is the 230 V figure. 120 V × 12.5 A on the PAGE also comes to 1,500 W |
| AC recharge time | "0 to 100% in Just 1 Hour" (description); "2 hours with single AC high voltage input" (feature list) | not stated | "High voltage" means 230 V. At 1,500 W a full 3,456 Wh charge takes at least 2.3 h before losses (my arithmetic) |
| Solar input | "12-60V MPPT 40A Max, 2000W Max" and, in the same table, "Solar Charge 12-150V MPPT 40A Max"; FAQ "12~60V 13A" | "Solar*3: (12~60)V 13A, Single port 650W Max, three ports 2000W Max". Warning to keep each XT60 within 60 V | 12–150 V is left over from the 2023 hardware. 3 × 650 W = 1,950 W, so 2,000 W is a combined cap rather than a sum |
| AC + solar | 3,000 W, "MPPT input priority" | 3,000 W max | |
| Car charging input | listed as a charging method; "Product does not include car charger"; ALLPOWERS' XT60 car charger is listed "for R600/R1500/R2500/S2000PRO/S2000" | not in the input specs | Car charging of the R4000: unverified |
| Generator charging | not mentioned | not mentioned | Unverified. It would come in through the AC input, at 1,500 W in Fast mode |
| UPS / EPS | "UPS Supported" | Switches to battery "within 15ms". To make UPS work, AC load must not exceed 1,500 W at 100–120 V. Above that, grid and battery share the load "until the power station consumes to 5%" and AC output turns off. ALLPOWERS recommends one device at a time on UPS | 15 ms is not true online UPS. Fine for most appliances, marginal for some PCs (unverified per device) |
| Idle draw | not published | not published | Power-saving mode turns AC/DC off after 1, 2, 4 or 6 h below 10 W |
| Inverter efficiency | FAQ runtime example uses 85% | not stated | |
| Charge temp | 0–40 °C | 0–40 °C | No self-heating mentioned in either |
| Discharge temp | **−20 to 40 °C** | **−10 to 40 °C** | Conflict |
| Storage temp, humidity | not stated | −20 to 40 °C (20–30 °C recommended); 10–90% RH | |
| Noise | "QUIET MODE, No noise" | Mute charging mode ≤650 W | No dB figure published |
| Certifications | none listed | Manual shows UL, PSE, CE, FCC, RoHS, IC and UKCA marks (rendered crop) | No standard (e.g. UL 2743) and no UL file number given. One search found no UL directory listing. UL status unverified |
| Expansion battery | none on the page today | "3.5 Smart Extra Battery": "two or more extra battery" via the extra-battery connector, figure "R4000+B3000". Rated output unchanged | See below |
| Weight | 99.2 lb / 45 kg | "Approximately 45KG (106lbs)" | 45 kg is 99.2 lb, so the manual's 106 lb is wrong or is a shipping weight (unverified) |
| Size | 21.25 × 19.29 × 11.81 in | 540 × 490 × 300 mm | |
| Wheels, handle | "sturdy travel case-like casters"; holds up to 45 kg on top | drawing shows two rear wheels and a top handle | Customer review (2024-07-25, on PAGE): "the wheels and handle (both of which could be a little more sturdy)" |
| App | Wi-Fi + Bluetooth; app does "system upgrade" | app sets language, 50/60 Hz, power-saving timer, beep, Bluetooth, AC charge mode, Wi-Fi, brightness | |
| Home panel / transfer switch | not addressed. FAQ suggests wiring a balcony-PV charge controller to the DC input | not addressed | Transfer-switch use: unverified. One buyer reported "Issues w 30Amp connector not being recognized by RV" (Michael E., 3/5, 2024-10-10, on PAGE) |
| In the box | not stated | R4000, AC charging cable, user manual and warranty card | Solar cable and car charger not included (PAGE note) |

**Expansion battery status.** The B3000 (3,168 Wh, 39.5 kg, "For ALLPOWERS R2500/R3500/R4000 only") is still a live US page at $1,299, compare-at $2,299, SKU AP-EB-003-US, but it shows **available: false**. It isn't in `products.json` and the US "Expansion Battery" collection is empty (source: https://iallpowers.com/products/allpowers-b3000-expansion-battery-3168wh.js, accessed 2026-10-28; https://iallpowers.com/collections/expansion-battery/products.json, accessed 2026-10-28; B3000 manual https://cdn.shopify.com/s/files/1/0747/3135/6467/files/AP-B3000_user_manual-230712_compressed_1.pdf?v=1698109195, accessed 2026-10-28). B3000 was in the US site nav from at least 2024-05-22 to 2026-01-10 and gone by 2026-03-02 (Wayback snapshots of those dates). Reviews show buyers looking for it: "I need instructions on adding a battery bank" (2026-04-07) and "Worried about getting a cable for connecting second unit" (2024-01-13) (PAGE reviews, accessed 2026-10-28).

## 3. Warranty, returns, shipping (as ALLPOWERS US states them on 2026-10-28)

**Warranty.** There are three different numbers on three ALLPOWERS pages:
- Product page: "5-Year Full Warranty, 5-year warranty for power stations and 2-year for solar panels" (PAGE).
- Warranty page: "The warranty period is 24 months from the date of purchase", and registering on the official website extends "the warranty period of some products". The R4000 and B3000 are on the "5-Years Limited Warranty" list. Elsewhere the same page says the period "is calculated from the date of product arrival". Registration link: https://iallpowers.com/pages/warranty-register (source: https://iallpowers.com/pages/warranty-policy, accessed 2026-10-28). My reading: 24 months by default, 5 years after you register. ALLPOWERS doesn't spell out what happens if you never register.
- Returns-and-refunds page: "The warranty period is 18 months start from the date of purchase by customer" (source: https://iallpowers.com/pages/returns-and-refunds, accessed 2026-10-28).
- Other terms on the warranty page: covers the original purchaser only, not transferable. Needs an invoice or order email showing order number, product, price and sales channel. ALLPOWERS pays shipping for repairs inside 30 days of receipt, the buyer pays after that. The charging adapter isn't covered. Refurbished R4000: 2 years, official-website orders only.
- Exclusions (returns page) include "Commercial Use", "Cosmetic Damage", "Purchases from unauthorized resellers", "Repairs through 3rd parties", and claims on items taken outside the country of purchase (buyer pays shipping).

**Amazon / Walmart / other sellers.**
- The warranty page says ALLPOWERS sells through its global, DE and UK official websites. "If you buy from another online store or seller, we cannot guarantee the quality of the product, so it is not covered by the official manufacturer's warranty."
- The same page has a "Special Note": for orders "at other official platform stores", ALLPOWERS "will directly convey your warranty requirements to the corresponding platform for processing" (https://iallpowers.com/pages/warranty-policy, accessed 2026-10-28).
- The contact page routes "Amazon orders" to support@allpowers.com and eBay orders to sales@allpowers.com (https://iallpowers.com/pages/contact-us, accessed 2026-10-28).
- So an ALLPOWERS-run Amazon storefront appears to count as an official platform store, with warranty handled through Amazon. Walmart Marketplace sellers, Wellbots and FactoryPure are not named, and whether they are "authorized" is unverified. The 30-day money-back applies "only" to products bought directly from ALLPOWERS (returns page).

**Returns.**
- Product page: "30-Day Money Back. No questions asked."
- Returns page:
  - not for "items with open box or lack of accessories"
  - needs all accessories and the original packaging, plus an RMA number on the outer label
  - buyer pays return shipping for non-defect reasons
  - the 30 days count "from the original shipment date"
  - used, non-defective returns need ALLPOWERS' approval and carry "15%-50% depreciation" (the same page later says "10% to 50%"), and the outbound shipping cost "also needs to be paid by the customer"
- Shopify refund policy: "30 days after receiving your item"; "Unfortunately, we cannot accept returns on sale items or gift cards" (source: https://iallpowers.com/policies/refund-policy, accessed 2026-10-28).
- **What counts as a sale item:** neither page defines it. The sentence is Shopify's stock refund-policy template wording. Every R4000 is priced below its compare-at price ($1,499 vs $3,299, "Save 55%"). Read literally, the clause would cover every unit, and that contradicts "30-Day Money Back. No questions asked." How ALLPOWERS applies it in practice, and whether a code discount makes an item a "sale item": unverified. Best to get a written answer from service@allpowers.com before relying on the 30 days.

**Shipping.**
- Product page: "Free U.S. Shipping, 3-5 days delivery from U.S. warehouse". The same page further down says "Free 2–3 Day Shipping from US Warehouse".
- Shipping policy:
  - orders processed within 48 hours
  - power stations go by FedEx or UPS ("2-3 days")
  - free shipping only in the 48 contiguous states
  - no PO boxes or APO
  - AK, HI, PR and territories "will be contacted", with possible extra fees or cancellation
  - warehouses listed as "North America: USA" plus Saudi Arabia and UAE, no city given
  - kits ship as two packages
- Delivery estimates differ by page: "4-9 working days" (https://iallpowers.com/pages/shipping-policy, accessed 2026-10-28) vs "3-5 working days" (https://iallpowers.com/policies/shipping-policy, accessed 2026-10-28).
- A buyer reported their unit "came with about 67% charge" (Alanna G., 2026-03-01, PAGE reviews).

## 4. Price history

US product page, from Wayback snapshots (`https://web.archive.org/web/<timestamp>/https://iallpowers.com/products/allpowers-r4000-power-station`) unless noted. Snapshots are sparse, so lows between them are unknown.

| Date | Price | Compare-at | Note |
|---|---|---|---|
| 2022-12-23 / 12-27 | | | Shopify product created / published (live `.js`) |
| 2023-02-05 | $4,299 | $4,999 | Earliest price seen. SKU AP-SS-011, 3,600 Wh spec |
| 2023-05-01 | $3,599 | $3,799 | |
| 2023-06-01 | $3,599 | $3,799 | showing unavailable |
| 2023-08-30 | $2,799 on Amazon after an $800 coupon, "down from $3,600" | | 9to5Toys: "$200 cheaper than on ALLPOWERS' own website" (source: https://9to5toys.com/2023/08/30/allpowers-new-21600wh-power-station-sees-first-discount-to-2799-save-800/, 2023-08-30) |
| 2023-09-27 | $2,499 on Amazon after a $500 coupon | | 9to5Toys "new all-time low" (source: https://9to5toys.com/?p=1006369, 2023-09-27) |
| 2023-09-30 | $2,799 | $3,599 | |
| 2023-10-23 | $1,999 | $3,599 | `.js` snapshot |
| 2023-12-06 / 2024-01-12 | $1,999 | $3,599 / $3,299 | |
| 2024-02-22 | $2,599 | $3,299 | |
| 2024-05-22 to 2025-03-02 | $2,099 | $3,299 | five snapshots |
| 2025-03-28 | $1,499 refurbished | $3,299 | separate listing, SKU AP-SS-011-R (https://web.archive.org/web/20250328093705/https://iallpowers.com/products/allpowers-r4000-portable-power-station-3600w-3456wh-refurbished). That listing is now 404 (accessed 2026-10-28) |
| 2025-04-20 | $1,599 | $3,299 | |
| 2025-07-10 | $1,999 | $3,299 | |
| 2025-10-07 | $1,899 | $3,299 | |
| 2025-11-05 | $1,799 | $3,299 | |
| 2026-01-10 | $1,899 | $3,299 | last snapshot with SKU AP-SS-011-US |
| 2026-03-02 | **$1,399** | $3,299 | lowest new-unit price in the snapshots. SKU now R4000-PLUS-US |
| 2026-06-16 | $1,699 | $3,299 | |
| 2026-08-04 | $1,899 | $3,299 | |
| 2026-10-28 | $1,499 | $3,299 | live `.js` |

- Launch price: the earliest observed is $4,299 (Feb 2023). A formal launch MSRP or announcement date: unverified. 9to5Toys used $3,600 as the regular price in Aug 2023.
- Black Friday 2025 ran "mid-November through December 1". The release named the R4000 but gave no price. Dateline "DIAMOND BAR, Calif., Nov. 24, 2025" (source: https://tools.prnewswire.com/en-us/live/20813/release/20251124EN30646, 2025-11-24).
- **Black Friday 2026:** nothing announced that I could find (web search, 2026-10-28). The page currently runs "HALLOWEEN SAVINGS, Up to 65% Off" with "Bundle More, Save More" tiers: 5% off at $1,000, 7% at $1,500, 12% at $2,500 (PAGE, accessed 2026-10-28). A lone R4000 at $1,499 sits $1 under the 7% tier.
- camelcamelcamel, Slickdeals and Electrek: nothing R4000-specific found (search, 2026-10-28). Amazon's price chart: unverified.

## 5. Availability today (2026-10-28)

- **iallpowers.com:** in stock, $1,499 (live `.js`). Kits: R4000 + SP037 $2,198, + SP039 $2,468, + SF100 $2,012 (in stock); + SP029 and + SF200 unavailable (`products.json`, accessed 2026-10-28).
- **Wellbots:** "ALLPOWERS R4000 Portable Power Station | 3600W 3456Wh", $1,899, available, listed 2026-06-10, EAN 6975274260365 (source: https://www.wellbots.com/products/allpowers-r4000-portable-power-station-3600w-3456wh.js, accessed 2026-10-28).
- **FactoryPure:** $1,640, unavailable (source: https://factorypure.com/products/allpowers-r4000-portable-power-station-3600w-3456wh-smart-app-control-new.js, accessed 2026-10-28).
- **Walmart:** search results show R4000 listings (https://www.walmart.com/ip/9596356324; kits at https://www.walmart.com/ip/5032693196 and https://www.walmart.com/ip/5042919128), but the pages return a "confirm that you're human" check. Price, seller and stock: unverified.
- **Amazon:** sold there in 2023 (9to5Toys above). Today's listing, price and seller: unverified (bot check).
- **Home Depot:** no listing found (search, 2026-10-28). Unverified.
- **Refurbished:** ALLPOWERS' refurbished R4000 page is 404 (accessed 2026-10-28). It existed at $1,499 in March 2025.
- **EU:** original R4000 €1,899 and R4000 V2 €1,799 on iallpowers.eu (accessed 2026-10-28).

## 6. Firmware and app

- No public firmware release notes or changelog found on iallpowers.com or by search (2026-10-28).
- The page says the app over Wi-Fi does "power monitoring/function setting/remote control/system upgrade" (PAGE).
- The manual lists app language options as Chinese, English and Japanese (MANUAL).
- Known issues are user reports only:
  - "after about 5 minutes, the bluetooth disconnects", plus trouble getting the Wi-Fi app working (Angus C., 5/5, 2024-07-25, PAGE reviews)
  - a Trustpilot-style report of losing app connectivity in the field (search snippet via https://www.desertcart.sn/products/573645064-allpowers3456wh-3600w-lifepo4-portable-power-station-with-400w-portable-solar, unverified at source)
  - "Translation very poor" in setup material (Lynn Z., 2025-07-14, PAGE reviews)
- Manual fault table covers:
  - charge and discharge high/low temperature protection
  - AC+DC total overload, AC overload, AC short circuit and AC overcurrent (remove the load, then turn AC back on by hand)
  - PV input overvoltage
  - "Other faults = xx" fault numbers (refer to customer service)
  - a resettable AC-input overload protector button that trips above 32 A at 100–120 V (MANUAL)

## 7. ALLPOWERS as a company

- "ALLPOWERS is operated by Guangzhou Allpowers Energy Technology Co., Ltd.", 1-4 Floor, Building 2, No. 182, Kaiyuan Avenue, Science City, Huangpu District, Guangzhou. The contact page names "ALLPOWERS INC" as "U.S. Local Business Support" at 23555 Golden Springs Dr 4, Diamond Bar, CA 91765, and a Hong Kong office at Room 803, Chevalier House, 45-51 Chatham Road South, Tsim Sha Tsui. Hours Mon–Fri 9–5, replies in 24–48 business hours. After-sales: service@allpowers.com (source: https://iallpowers.com/pages/contact-us, accessed 2026-10-28).
- The About page instead names "HK ALLPOWERS TECH LIMITED" (source: https://iallpowers.com/pages/about-us, accessed 2026-10-28). The Terms of Service are governed by "the laws of HK" (source: https://iallpowers.com/pages/terms-of-service, accessed 2026-10-28).
- PR Newswire releases are datelined Diamond Bar, Calif. (2025-11-24 release above).
- US warehouse: "We have warehouses in these locations: North America: USA". No address given, and the Diamond Bar address isn't called a warehouse (shipping policy above).
- Not checked against the California Secretary of State or any HK/PRC registry: unverified.

## ChatGPT claims checked (W1 scan, 2026-10-28, `growth/evals/runs/2026-10-28-visibility/chatgpt/allpowers-r4000-3456wh--*.json`)

| Claim | Verdict | Evidence |
|---|---|---|
| "the official product page has also appeared at $1,899" (deal-1), "The manufacturer's pages have also shown $1,899" (worth-1) | **True historically, not today.** One US listing only, no second handle | The same US page was $1,899 on 2025-10-07, 2026-01-10 and 2026-08-04 (Wayback). Today it is $1,499. `products.json` has a single R4000 standalone product. Wellbots lists it at $1,899 today (worth-1 cites Wellbots), and the EU original is €1,899 |
| "a large, wheeled battery generator" | **True** | PAGE: "sturdy travel case-like casters"; manual drawing shows wheels and a top handle |
| "About 99 lb (45 kg)" | **True per the product page** | PAGE "99.2 lbs/45KG". The manual says "45KG (106lbs)", which doesn't add up (45 kg = 99.2 lb). The EU V2 is 40.5 kg, so the number only fits the US model |
| "lack of 240V output" | **True for the US unit** | US outputs are 100–120 V (4 outlets + 30 A RV port). The 220–240 V / 4,000 W spec in the manual is the EU version's. No L14-30 or split-phase |
| "Published output and solar-voltage figures vary across manufacturer materials ... conditions for the advertised five-year warranty" | **True** | Output: 4,000 W title vs 3,600 W at 120 V. Solar: 12–60 V vs 12–150 V on the same page; 13 A vs 40 A. Also AC input 2,000 W vs 1,500 W at 120 V; recharge 1 h vs 2 h; discharge temp −20 vs −10 °C. Warranty: 5 years (product page) vs 24 months plus registration (warranty page) vs 18 months (returns page) |
| (alt-1) "Recent listed price: about $1,709–$1,899" | Not about the R4000 | That line is the Jackery HomePower 3600 Plus |
| (worth-1) ALLPOWERS26 gives "12% discount for orders above $2,500" | Probably a mix-up with the site's bundle tiers (12% at $2,500). Code behaviour is another angle's job | PAGE "Bundle More, Save More" tiers |

## Mismatches vs our record (src/products.py, slug allpowers-r4000-3456wh)

1. **AC input "2,000 W; full in ~2 h".** On US 120 V power the manual gives Fast Mode 1,500 W (Standard 1,000 W, Mute 650 W, default Mute). 2,000 W is the 230 V figure. At 1,500 W a full charge takes at least ~2.3 h. Suggested: "AC input 1,500 W at 120 V (2,000 W is the 230 V rating); about 2.5 h to full; ships in 650 W Mute mode".
2. **Warranty "5 years".** ALLPOWERS' warranty page makes it 24 months from purchase, extended to 5 years by registering at iallpowers.com/pages/warranty-register. Its returns page still says 18 months. Suggested: "5 years after registering on iallpowers.com (24 months otherwise)".
3. **Returns.** Our text is accurate as far as it goes. Missing: RMA required; open-box returns refused; 30 days counted "from the original shipment date" on one page and from receipt on another; used, non-defective returns only with approval and 15–50% depreciation. "Sale item" is undefined, and every R4000 sells below compare-at.
4. **Solar "12–60 V, 13 A".** Matches the manual. The product page also shows 12–150 V and 40 A, so the existing caveat could name that conflict.
5. **Size/weight "45 kg".** Matches the page. The manual's "106lbs" is the odd one out. No change needed.
6. **SKU note.** "PLUS" is not a different model. It is the same Shopify variant, relabelled between 2026-01-10 and 2026-03-02 together with a new UPC. Worth one caveat: the EU-only R4000 V2 is 2,880 Wh, and older listings and used units may be the 2023 build (3,600 Wh claimed, 12–150 V solar, 5-unit parallel).
7. **Expansion.** We list none, which is right for today. The manual's B3000 expansion is sold out in the US and gone from the catalog. Suggested caveat: "Expansion battery (B3000) currently unavailable in the US."
8. **UPS.** Not in our record. 15 ms switchover, and UPS only holds with AC load at or below 1,500 W at 120 V. Worth adding.
9. **Summary "shipped from a US warehouse".** Supported (page and shipping policy). Location not disclosed.

Everything else in the record matches the page and manual: 3,456 Wh LiFePO4, 3,500+ cycles, 3,600 W / 6,000 W peak, 4 AC + RV, USB-C 2× 100 W, USB-A 2× 18 W + 2× 12 W, 12 V/10 A car port, 2,000 W solar over 3 XT60 at 650 W each, 3,000 W AC+solar, 540 × 490 × 300 mm, Wi-Fi + Bluetooth.

## Open questions / couldn't verify

- Why the UPC changed (782940087302 to 747165451215) in early 2026: new production revision, or catalog cleanup? Only ALLPOWERS can answer.
- UL listing: the manual shows a UL mark but names no standard or file number. UL Product iQ was not checked.
- How the "no returns on sale items" clause is applied, and whether a discount code makes an item a sale item.
- Whether the 5-year term applies without registration, and how Amazon purchases are handled in practice.
- Amazon and Walmart listings today (price, seller, stock): blocked by bot checks.
- NEMA type of the four AC outlets (the manual says "US 20A Max", which suggests 5-20, but doesn't say).
- Whether the RV port and the four outlets share the 3,600 W limit (likely, not stated).
- Idle draw, noise in dB, measured inverter efficiency, surge duration: none published.
- Car and generator charging on the R4000: not documented.
- Launch MSRP and exact US on-sale date (Shopify published 2022-12-27; first price seen $4,299 on 2023-02-05).
- Black Friday 2026: no announcement found as of 2026-10-28.
- Legal entity: the site names both Guangzhou Allpowers Energy Technology Co., Ltd. and HK ALLPOWERS TECH LIMITED, and ALLPOWERS INC in Diamond Bar. Not checked against registries.
