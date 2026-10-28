# ALLPOWERS P1800 (VOLIX P1800), angle 1: maker facts

- **Angle:** 1, maker facts (what ALLPOWERS itself publishes: store pages, manual, policies, its own marketplace listings)
- **Product:** ALLPOWERS P1800 portable power station, 1,024 Wh / 1,800 W, US SKU `VOLIX-P1800-US`, plus the P1800 + SP037 kit
- **Date:** 2026-10-28
- **Method:** curl against the Shopify endpoints (`.js`, `products.json`, `search/suggest.json`) and the product pages of iallpowers.com (US), uk.iallpowers.com and iallpowers.eu. I downloaded the only P1800 user manual I could find, which is on the EU store, rendered its English pages with macOS PDFKit and read them. I also read the 12 product images on the US page, the US warranty, returns, refund and shipping pages, Wayback snapshots, the Amazon listings (static HTML via curl), a Walmart search, pricehistory.app and Slickdeals. I used 7 web searches. Raw files are in `/private/tmp/claude-501/-Users-jiayiyao-Desktop-dealectric/44f11078-b8ab-412e-a42d-cf3b4ee1b7ef/scratchpad/research/p1800-sp037-maker/`.

Short source names used below:
- **US page**: https://iallpowers.com/products/allpowers-p1800-portable-power-station-1024wh-1800w
- **Manual**: "ALLPOWERS_P1800_User_Manual.pdf" at https://cdn.shopify.com/s/files/1/0747/3135/6467/files/ALLPOWERS_P1800_User_Manual.pdf?v=1785825984. The EU page links it, and the US user-guides page does not. Its file version stamp is 2026-08-04, it is titled "VOLIX P1800" and it covers both 100-120 V and 220-240 V units. Page numbers below are the manual's printed page numbers.
- **UK page**: https://uk.iallpowers.com/products/allpowers-p1800-portable-power-station-1800w-1024wh
- **EU page**: https://iallpowers.eu/products/p1800

## 1. Identity, launch and line

- The US store product was created and published 2026-06-29. Title "ALLPOWERS P1800 Portable Power Station 1024Wh | 1800W", vendor "ALLPOWERS US", SKU VOLIX-P1800-US, GTIN 662698641523. (source: https://iallpowers.com/products/allpowers-p1800-portable-power-station-1024wh-1800w.js, accessed 2026-10-28)
- UK listing (SKU VOLIX-P1800-UK) created 2026-08-20. EU listing (SKU VOLIX-P1800-EU) created 2026-08-04. (source: UK page .js and https://iallpowers.eu/products/p1800.js, accessed 2026-10-28)
- The P1800 belongs to ALLPOWERS' **VOLIX** line. The US images and the manual call it "VOLIX P1800", and the app lists it as "VOLIX P1800". (source: US page image 4_f31cc96b…webp; Manual p.3 and p.10, accessed 2026-10-28) The only other VOLIX product in the US store is the VOLIX P300 (300 W / 256 Wh, created 2025-10-16). (source: https://iallpowers.com/products.json?limit=250, accessed 2026-10-28)
- **Successor question:** ALLPOWERS does not call the P1800 a successor to anything. That is unverified. Circumstantial evidence:
  - The EU page's comparison table puts the P1800 between the R1500 LITE (1,056 Wh, 1,600 W) and the R1500 (1,152 Wh, 1,800 W). (source: EU page, accessed 2026-10-28)
  - On Amazon, the standalone P1800 listing B0CLM7YW6C still shows "Manufacturer Part Number: R1500 LITE" and carries 212 reviews (4.2/5). That is an old R1500 LITE ASIN reused for the P1800, so its reviews are inherited and are not P1800 reviews. (source: https://www.amazon.com/dp/B0CLM7YW6C, accessed 2026-10-28)
  - The US R1500 LITE (`R1500-LITE-US`, $389) and all its kits show available:false, while the R1500 is still in stock at $539. (source: products.json, accessed 2026-10-28)
  - My reading: the P1800 has taken the R1500 LITE's slot, at least on Amazon. Unverified as an official succession.
- **EOL:** nothing found suggesting the P1800 itself is end-of-life. It is new in all three regions.
- **Expansion battery:** none. The manual's port list is solar XT60, AC input, DC switch, 12 V car output, 2× USB-C, 2× USB-A and 4× AC. It has no expansion port, and the rear photo on the US page shows none either. (source: Manual pp.4-5; US page image p1800-_0024_2.webp, accessed 2026-10-28) The EU page's marketing line "1024Wh expandable energy capacity" contradicts this and is unsupported by the manual. (source: EU page, accessed 2026-10-28)

## 2. Spec sheet: US page vs manual vs other ALLPOWERS pages

| Item | US page spec table / text | US page images | Manual (Aug 2026) | Other ALLPOWERS pages |
|---|---|---|---|---|
| Capacity | 1,024 Wh LiFePO4 | 1,024 Wh | 1,024 Wh, 51.2 V 20 Ah, LFP | same |
| Cycle life | "3000+ cycles, ≥70% remaining capacity" | "4500+ cycles", "10+ years lifespan" | "≥4000 cycles with ≥70% State of Health (SoH)" | UK 3,000+ to ≥70%; EU table 4000+; EU description "3500 cycle life"; EU text "retains over 80%"; Amazon 4000+ |
| UPS | "≤10ms automatic switchover" | "15ms UPS" (2 images) | **20 ms**, stated twice (p.6 icon 12 and p.9 §3.6) | UK ≤10 ms; EU <10 ms / "Under 10ms"; Amazon "20ms" |
| AC output | 1,800 W rated, 3,600 W peak, 4 outlets | 4× outlets 1,800 W / peak 3,600 W | 4× AC, 100-120 V (or 220-240 V), rated 1,800 W (peak 3,600 W); **total AC+DC 1,800 W max** | UK: pure sine wave |
| AC outlet type (US) | not stated | product shots 1-3 show 4× NEMA 5-15 (3-prong); **at least 5 of the 8 infographics (images 5, 6, 9, 10, 12) show UK BS 1363 sockets** | n/a | UK page sells the UK-socket unit |
| USB-C | (140 W in bullets) | 2× 140 W | 2×, 5/9/12/15 V 3 A, 20/28 V 5 A, 140 W each max | same |
| USB-A | n/a | 2× 18 W | 2×, 5 V 3 A / 9 V 2 A / 12 V 1.5 A, 18 W each | same |
| Car port | n/a | 1× 120 W | 12 V 10 A, 120 W max | same |
| AC input | Fast 1,200 W / Standard 800 W / Silent 500 W | 1,200 W | 100-120 V 15 A max; fast up to 1,200 W, standard 800 W (default), **silent up to 400 W**, set in the app | EU description "1500w AC fast charging" (contradicts its own table, which says 1,200 W) |
| AC charge time | 0-80% in about 1 hour | 0-80% in 0.76 h | not stated | EU: "0-100% AC charging in 54 minutes" |
| Solar input | XT60, 650 W max, 11-60 V, **"95V Open-Circuit Voltage"**, 13 A max | 650 W; 0-80% in 1.4 h | MPPT 11-60 V, 13 A, 650 W max; "ensure that the output voltage specification of the solar panel is within the range of 11-60V to avoid damaging the product" | rear label: "SOLAR/CAR INPUT 11-60V 13A MAX." |
| Car charging | (AC / Solar / AC+Solar listed) | "110W Car Charging, fully charged in 8.28 hours" | via the same XT60 port; car cable sold separately | Amazon: 12 V/24 V car charging |
| Size | not stated | 14.7 × 11.7 × 8.2 in | **371 × 208 × 296 mm (W×D×H), 14.7 × 8.2 × 11.7 in** | EU 37.1 × 20.8 × 29.6 cm |
| Weight | not stated (Shopify weight field 0) | 28.66 lb | approx. 13 kg (28.66 lb) | UK approx. 13 kg; Amazon 28.7 lb |
| App | Bluetooth / Wi-Fi; monitor, control output, settings, firmware | app screenshot "VOLIX P1800" | Wi-Fi + Bluetooth | |
| Firmware | USB / OTA via the app | | | |
| Noise | not stated | | not stated | UK "30 dB"; EU "ultra-low 30 dB" (no test conditions given) |
| Efficiency | not stated | | not stated | UK FAQ runtime example uses "1024Wh × 85%" |

Sources: US page and its spec chart (accessed 2026-10-28); US page images https://cdn.shopify.com/s/files/1/0443/1223/2089/files/1_53ef7b8d-36a9-4240-a6b6-6764cc41442a.webp, …/2_5e01be19…webp, …/3_9f33ab59…webp, …/4_f31cc96b…webp, …/5_5d0ae7c1…webp, …/6_b4585f3f…webp, …/8_bc6c3092…webp, and product shots p1800-140024_2/150024_2/allpowers_2/_0024_2.webp (accessed 2026-10-28); Manual pp.3-9 (accessed 2026-10-28); UK page and EU page (accessed 2026-10-28); Amazon https://www.amazon.com/dp/B0CLM7YW6C (accessed 2026-10-28).

### Settling the conflicts

- **Cycles:** the manual is the only engineering document, and it says ≥4,000 cycles to ≥70% SoH. The US spec table's 3,000+ to ≥70% is the conservative floor. The US image's 4,500+ appears nowhere else and is the outlier. The end-point is 70%, not 80%: the manual and the US and UK tables all say 70%, and only the EU marketing paragraph says ">80%". **Recommendation:** publish "3,000+ cycles to 70% (US spec table); the manual rates ≥4,000 to 70% SoH". Drop 4,500.
- **UPS:** three numbers are in circulation, ≤10 ms (US/UK/EU spec tables), 15 ms (US images) and 20 ms (manual twice, Amazon bullets). The manual describes the actual behaviour ("automatically switch to the battery power supply mode within 20ms"). **Recommendation:** say "ALLPOWERS' spec table claims ≤10 ms; its own manual says 20 ms". Treat it as a switchover UPS that is unverified for sensitive PCs. An EU 1/5 review dated 2026-10-24 says the unit "restarted by itself" after three hours of UPS-type use. (source: EU page reviews, accessed 2026-10-28)
- **Size and weight:** 371 × 208 × 296 mm (W×D×H), about 13 kg / 28.66 lb (Manual p.3). The "373" in our record comes from converting 14.7 in. The manual says 371 mm.

### Other facts buyers ask about

- **Surge rules:** devices with a starting peak above 3,600 W are not supported. Total AC+DC output is capped at 1,800 W, and overload trips E202 ("turn off input"). (source: Manual p.3, p.14 FAQ 2, p.15, accessed 2026-10-28)
- **Idle draw:** not published. ECO mode "will automatically shut down when the output power is less than 3W". (source: Manual p.6 icon 11, accessed 2026-10-28)
- **Charge temperature:** charging 0-40 °C (32-104 °F), discharging -10 to 40 °C (14-104 °F), storage -20 to 45 °C (best 20-30 °C), humidity 10-90%. (source: Manual p.4, accessed 2026-10-28) **Self-heating: none mentioned.** The manual lists only low-temperature warnings and protection codes (E104 charging low temp, E106 discharging low temp). (source: Manual p.7 icon 23, p.15, accessed 2026-10-28)
- **Certifications (marks printed in the manual):** CE, RoHS, FCC, IC, the China 10-year EFUP mark, RCM, UN38.3, WEEE and French Triman/recycling marks. **No UL or ETL mark** appears in the manual or on the US page. (source: Manual p.4, accessed 2026-10-28) Whether any NRTL listing exists is unverified.
- **AC charging on a household circuit:** the manual warns that the circuit must sustain 15 A at 100-120 V when using UPS mode. (source: Manual p.9, accessed 2026-10-28)
- **App features:** backup-power ratio (reserve SoC), self-consumption / "Self Use" mode, scheduled tasks for AC charging, solar charging, AC/12 V/USB discharging, timers, charge-mode selection (fast/standard/silent), 50/60 Hz, key-tone on/off, Wi-Fi/Bluetooth (reset by holding the DC button 10 s). (source: Manual pp.6-7, 10 and 13; I did not read pp.11-12, accessed 2026-10-28)
- **Pass-through charging:** yes. **Airline travel:** "No". **Storage:** discharge to 30% and recharge to 60% every three months. Below 5%, charge within 24 h. (source: Manual p.7 and p.14, accessed 2026-10-28)
- **In the box:** the unit, an AC charging cable, and the user manual with warranty card. No solar cable and no car cable. (source: Manual p.16, accessed 2026-10-28) The EU page says the same: "Product does not include car charger and solar panel cable". (source: EU page, accessed 2026-10-28) The SP037 includes its own MC4-to-XT60 cable, so an SP037 buyer is covered.
- **Solar pairing that ALLPOWERS recommends:** "we recommend pairing the P1800 with a 400W solar panel". It also lists 100/200/400/600 W ALLPOWERS panels as compatible. (source: UK page FAQ 3, accessed 2026-10-28)
- **P1800 + SP037 electrical fit (our calculation from published specs, not an ALLPOWERS statement):**
  - One SP037 V3.0 (Vmp 37.4 V, Imp 10.6-10.69 A, Voc 45.3 V) fits inside 11-60 V / 13 A, so the full ~400 W STC is possible.
  - Two in series give Voc ~90.6 V and Vmp ~74.8 V. That is above the manual's 11-60 V range, even though the US page claims a 95 V OCV tolerance.
  - Two in parallel give ~21 A, so the station caps at 13 A, about 486 W.
  - The newer SP037 V5.0 (Vmp 30.5 V, Imp 13.11 A, Isc 14.42 A; see the SP037 file) is already at the 13 A cap with one panel. A second V5 in parallel adds nothing, and two in series give Voc ~73 V, which is over 60 V.
  - Bottom line: on the P1800, one SP037 is the useful maximum.

## 3. ALLPOWERS US policies

- **Warranty page:** the default is "24 months from the date of purchase". The 5-year list covers "R4000, R3500, R2500, R1500, R600, S2000 PRO, S2000, S700 … B3000, B1000". The 2-year list covers "S1500, S300, S200 … SP039, S037 [sic], SP035, SP033, SP029, SP027, SP026, SP020, SP012, SF100, SF200, SF400". **The P1800 is on neither list**, so a US store purchase falls to the 24-month default. The warranty runs from product arrival, covers the original purchaser only, and needs an invoice or order email. For repair returns, ALLPOWERS pays shipping within 30 days of receipt and the buyer pays after that. Refurbished units: 2 years for the large R/S stations, 1 year for the small ones and the panels. (source: https://iallpowers.com/pages/warranty-policy, accessed 2026-10-28)
- **Contradictions:**
  - The US "Returns and Refunds" page says "The warranty period is 18 months start from the date of purchase". (source: https://iallpowers.com/pages/returns-and-refunds, accessed 2026-10-28)
  - The US P1800 page shows no warranty line, only Shipping and Return, while the site header says "Up to 5-Year Warranty". (source: US page, accessed 2026-10-28)
  - The UK page says "Our power stations offer a 5-year warranty". The EU page shows a "5-year Warranty". Amazon's P1800 bullets say "Backed by a 5-year warranty". (sources: UK page, EU page, https://www.amazon.com/dp/B0CLM7YW6C, accessed 2026-10-28)
  - For a US store buyer, 24 months is the only figure backed by the US warranty page. Whether ALLPOWERS US would honour 5 years for the P1800 is unverified.
- **Warranty for marketplace purchases:** the page says purchases "from another online store or seller" are not covered, but that for "other official platform stores" ALLPOWERS will forward the claim to the platform. (source: warranty page, accessed 2026-10-28)
- **30-day money-back (Returns and Refunds page):**
  - The window counts from the **original shipment date**. The item must be unused, in original packaging, with all accessories and an RMA number. "Open box" items are not eligible.
  - The buyer pays return shipping unless the item is defective or damaged in shipping.
  - For a non-quality return after use, ALLPOWERS must agree first and "we will deduct 15%-50% depreciation". A later line says "a depreciation fee ranging from 10% to 50%", and that the original outbound shipping "also needs to be paid by the customer".
  - Contact: service@allpowers.com.
  - (source: https://iallpowers.com/pages/returns-and-refunds, accessed 2026-10-28)
- **Refund policy (/policies):**
  - It says "30 days after receiving your item", which conflicts with "from the original shipment date" above.
  - It says "Unfortunately, we cannot accept returns on sale items or gift cards" and "We also do not accept returns for hazardous materials". (source: https://iallpowers.com/policies/refund-policy, accessed 2026-10-28)
  - **What "sale items" means in practice is undefined.** Every ALLPOWERS listing carries a compare-at price, so everything displays as on sale: the P1800 shows "Save 59%". Every product page also shows a "30-Day Money Back" badge.
  - Neither page says whether an item bought with a discount code counts as a sale item. Unverified, and it would need an answer from ALLPOWERS support.
  - Read literally, the hazardous-materials line could also catch lithium power stations. Unverified how ALLPOWERS applies it.
- **Shipping:**
  - The product page says "Local delivery, 3-5 days delivery". (source: US page, accessed 2026-10-28)
  - The policy says orders are processed within 48 h, delivered in 2-7 business days after processing, "within 4-9 working days" overall, and ship from a US warehouse (also Saudi Arabia and UAE for those regions).
  - Free shipping covers the 48 contiguous states only, with no PO boxes or APO. AK/HI/PR orders are contacted about extra fees or cancellation.
  - A station and panel ship as two packages: the station by FedEx/UPS in 2-3 days, the panel by FedEx/UPS/USPS in 3-7 days. (source: https://iallpowers.com/pages/shipping-policy, accessed 2026-10-28)

## 4. Price history and bundles

- **US store:** $529.99 with compare-at $1,059.98 on 2026-07-18, about three weeks after launch. (source: https://web.archive.org/web/20260718220417/https://iallpowers.com/products/allpowers-p1800-portable-power-station-1024wh-1800w, accessed 2026-10-28) On 2026-10-28 it is **$439.00**, compare-at $1,059.98, available. (source: US page .js, accessed 2026-10-28) The page currently runs a "HALLOWEEN SAVINGS … Up to 65% Off" banner and bundle tiers of 5% at $1,000, 7% at $1,500 and 12% at $2,500. (source: US page, accessed 2026-10-28)
- **US kits (2026-10-28):** (source: products.json, kit .js and search/suggest.json, accessed 2026-10-28)
  - P1800 + 1× SP037 is $731 (compare-at $1,059.98), available. It was created 2026-07-02 but only published 2026-09-04.
  - P1800 + 200 W (SF200/SE200 variants) starts at $578-588 and is not available.
  - P1800 + SP039 600 W is $848, available.
  - Kit vs separate: $439 + $299 = $738, so the kit saves $7 before codes. Our arithmetic with the 10% codes gives separate $664.20 vs kit $657.90. Whether the codes apply to the kit SKU is unverified.
- **Amazon (2026-10-28, static HTML; seller on all P1800 listings is GiarideDirect):**
  - Standalone B0CLM7YW6C: **$419.00**, in stock, "**Non-returnable**. Transportation of this item is subject to hazardous materials regulation". (source: https://www.amazon.com/dp/B0CLM7YW6C, accessed 2026-10-28)
  - P1800 + 100 W: B0CLXSJ1YQ $488.00 (non-returnable) and B0CHYG5X89 $488.00 (30-day refund/replacement; Model Name P1800+SE100; part-number field "AP-SS-009-PRO(S2000 PRO)+SF200-US", another reused ASIN). (source: https://www.amazon.com/dp/B0CLXSJ1YQ and https://www.amazon.com/dp/B0CHYG5X89, accessed 2026-10-28)
  - P1800 + 200 W SE200: B0DC9Y38YC $536.00, "will be released on November 15, 2026. Pre-order now." (source: https://www.amazon.com/dp/B0DC9Y38YC, accessed 2026-10-28)
  - P1800 + SP037: B0CLXGW5DG $815.09, non-returnable. That is $84 more than ALLPOWERS' own $731 kit. (source: https://www.amazon.com/dp/B0CLXGW5DG, accessed 2026-10-28)
  - No coupon was visible in the static HTML of any of these. Amazon loads clip coupons dynamically, so unverified.
- **Lows:**
  - Slickdeals, 2026-07-23: Amazon $359.40 via clip coupon plus code OBP25A77, list $599, ASIN B09VL33L58 (expired). That ASIN now resolves to the VOLIX P300 listing. (source: https://slickdeals.net/f/19799412-allpowers-p1800-portable-power-station-1024wh-lifepo4-battery-backup-w-4-1800w-3600w-peak-ac-outlets-140w-usb-c-outpu-solar-generator-359-40, accessed 2026-10-28)
  - pricehistory.app, B0CHYG5X89 (P1800 + 100 W): $618 high on 2026-09-07, then $588→$488 on 2026-08-26, $618→$488 on 2026-09-13, and $488→$439.20 (10% off) on 2026-10-11. Low $439.20, average $525.38 over 87 days. Snapshot dated 2026-10-12. (source: https://pricehistory.app/p/allpowers-p1800-portable-power-station-100w-solar-x3e6uJSj, accessed 2026-10-28)
  - camelcamelcamel returned a Cloudflare challenge, so I could not read it.
  - 9to5Toys / Electrek P1800 coverage: none found (web search 2026-10-28).
- **Other regions (context only):** EU €549 (compare-at €1,099), with kits €629-999. UK £494.95 (compare-at £989), with a "15-Day Price Assurance" price-drop refund. (sources: EU page .js; UK page, accessed 2026-10-28)
- **Black Friday 2026:** no dated plan or price announced that I could find. The US store has a "Black Friday Products" collection of 24 items. It includes the SP037 at $299 and several R/S kits but **not the P1800**. (source: https://iallpowers.com/collections/black-friday-products/products.json?limit=250, accessed 2026-10-28) Amazon's P1800 + 200 W pre-order dated 2026-11-15 hints at a pre-BF bundle push. That is my inference, unverified.

## 5. Availability elsewhere (2026-10-28)

- **Amazon:** yes, five P1800 ASINs across two variation families (parents B0HD74V1VD and B0HDXNXR6S), all sold by GiarideDirect. Prices and ASINs are in §4. Ratings shown (4.2/212, 4.0/55) are inherited from reused ASINs. (sources above)
- **Walmart:** "0 results for 'ALLPOWERS P1800'". A search for "ALLPOWERS 1024Wh" returned only other brands. (source: https://www.walmart.com/search?q=ALLPOWERS+P1800, accessed 2026-10-28; results localised to a CA store)
- **Home Depot:** HTTP 403 to curl, so I could not check. (source: https://www.homedepot.com/s/ALLPOWERS%20P1800, accessed 2026-10-28)
- **Official US user-manual page:** has no P1800 manual. It lists manuals up to the R4000/R1500 LITE but nothing for the P1800. (source: https://iallpowers.com/pages/user-guides, accessed 2026-10-28)

## ChatGPT claims checked

Claims from W1's scan, `growth/evals/runs/2026-10-28-visibility/chatgpt/allpowers-p1800-1024wh--deal-1.json` (run started 2026-10-28T08:41Z).

- **Claim:** "P1800 + 100W solar panel $439.20 … Amazon price tracked October 2026; reported at a two-month low", linking https://www.amazon.com/dp/B0CHYG5X89 and citing pricehistory.app.
- **Verdict: stale.**
  - The listing exists: ASIN **B0CHYG5X89**, "ALLPOWERS P1800 Portable Power Station with 100W Solar Panel, 1024Wh, 1800W", Model Name P1800+SE100, seller **GiarideDirect**, in stock, 30-day refund/replacement.
  - On 2026-10-28 it shows **$488.00**, with no coupon visible in the static HTML. (source: https://www.amazon.com/dp/B0CHYG5X89, accessed 2026-10-28)
  - The $439.20 is pricehistory.app's **2026-10-12** snapshot: $488 minus 10%, logged as a drop on 2026-10-11 and labelled "Lowest in last 2 months". (source: https://pricehistory.app/p/allpowers-p1800-portable-power-station-100w-solar-x3e6uJSj, accessed 2026-10-28) ChatGPT presented a 16-day-old tracker reading as the current price.
  - A second 100 W bundle, B0CLXSJ1YQ, is also $488 but non-returnable.
  - The standalone P1800 on Amazon is $419 (B0CLM7YW6C), which ChatGPT did not mention.

## Mismatches vs our record

1. **UPS.** Our record says "≤10 ms (images say 15 ms)". The manual says **20 ms** twice, and Amazon says 20 ms. The conflict is 10/15/20 ms, not 10/15.
2. **Cycles.** The manual says **≥4,000 to ≥70% SoH**. US page 3,000+; image 4,500+; EU 3,500 and 4,000+. "To 70%" is confirmed. Our caveat should name the manual figure and drop 4,500 as the outlier.
3. **Silent-mode AC charging.** The manual says **400 W**. The US page says 500 W, which is what we list.
4. **Dimensions.** The manual says **371 × 208 × 296 mm (W×D×H)**. We list ~373 × 297 × 208 (inch-converted, different axis order). Weight 13 kg / 28.66 lb is confirmed by the manual, so it is no longer only "from images".
5. **Solar Voc.** The US page adds "95V Open-Circuit Voltage", but the manual and rear label say 11-60 V. We list 11-60 V, which is correct. Our page should warn that a series pair of SP037s exceeds 60 V.
6. **Warranty.** 24 months matches the US warranty page default. But the US returns page says 18 months, and the UK, EU and Amazon all say 5 years. Our "not on ALLPOWERS' 5-year list" is correct.
7. **Car charging.** The image says ~110 W input ("fully charged in 8.28 hours"). The car cable is not included, and neither is the solar cable when buying the P1800 alone.
8. **AC outlets.** The US unit has NEMA 5-15 outlets in the product shots, but at least 5 of the 12 US-page images are infographics showing UK sockets. Worth one line so shoppers aren't confused.
9. **No expansion battery support.** Not in our record. The manual shows no expansion port.
10. **Amazon undercuts the US store's list price** ($419 vs $439) but is **non-returnable**. That is a buyer-relevant fact our page does not state.
11. **Returns detail.** Our record says "30-day … unused … original package". The page adds that the window counts from the shipment date, open-box items are excluded, used returns lose 15-50% to depreciation, an RMA is required, and the separate policy text says it does not accept returns on "sale items" or "hazardous materials".

## Open questions / couldn't verify

- Whether "sale items can't be returned" applies to the P1800 (every listing is "on sale"), or to code-discounted orders. Needs ALLPOWERS support in writing.
- Whether US P1800 buyers get 24 months (US warranty page) or 5 years (UK/EU/Amazon copy).
- Real UPS switchover time: published claims are 10, 15 and 20 ms, with no independent test found.
- Idle (self-consumption) draw and inverter efficiency: not published. The 85% is only a UK FAQ example.
- Noise of 30 dB: no measurement conditions given.
- UL/ETL or other NRTL listing: no mark seen.
- Self-heating for cold charging: not mentioned, presumed absent.
- A US-specific P1800 manual. The one I read is the EU-hosted dual-voltage manual, and the US user-guides page has none.
- Amazon clip coupons, which load by JS and were not visible to curl. Home Depot was blocked (403). camelcamelcamel was blocked (Cloudflare).
- Whether ALLPOWERS considers the P1800 the R1500 LITE's replacement. The ASIN reuse is the only evidence.
- Black Friday 2026 prices or dates for the P1800.
