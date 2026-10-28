# ALLPOWERS SP037 400 W foldable solar panel, angle 1: maker facts

- **Angle:** 1, maker facts (what ALLPOWERS itself publishes: store pages, manuals, policies, its own marketplace listings)
- **Product:** ALLPOWERS SP037 400 W foldable solar panel, SKU `AP-SP-037-BLA`, plus the P1800 + SP037 kit
- **Date:** 2026-10-28
- **Method:** curl against the Shopify endpoints (`.js`, `products.json`) and the product pages of iallpowers.com (US) and iallpowers.eu. I downloaded both official SP037 manuals, rendered them with macOS PDFKit and read the English panels: V3.0, linked from the US page, and V5.0 "Monocrystalline", linked from the EU page. I also read the US product images, the US warranty, returns, refund and shipping pages, Wayback snapshots of the US page, the Amazon listings (static HTML), a Walmart search, Slickdeals and W1's ChatGPT scan JSON. Web searches are shared with the P1800 file (7 total). Raw files are in `/private/tmp/claude-501/-Users-jiayiyao-Desktop-dealectric/44f11078-b8ab-412e-a42d-cf3b4ee1b7ef/scratchpad/research/p1800-sp037-maker/`.

Short source names used below:
- **US page**: https://iallpowers.com/products/allpowers-400w-portable-solar-panel
- **V3.0 manual**: https://cdn.shopify.com/s/files/1/0443/1223/2089/files/AP-SP-037_400W_Solar_Panel.pdf?v=1671926121 (linked from the US page "Download Manual"; file stamp 2022-12-24; header "SP037 V3.0", model AP-SP-037-BLA)
- **V5.0 manual**: https://cdn.shopify.com/s/files/1/0770/6237/3669/files/ALLPOWERS_SP037_Monocrystalline_V5.0_-400W_Revised_Manual_compressed.pdf?v=1767929878 (linked from the EU page; file stamp 2026-01-09; "Model: AP-SP-037"; the header misprints "SP033 V5.0")
- **EU page**: https://iallpowers.eu/products/allpowers-sp037-portable-solar-panel-400w

## 1. Two hardware versions under one model number

The biggest finding: **a different SP037 exists.** ALLPOWERS' EU store lists "Cell Type: Monocrystalline (upgraded in May 2025)" and links a V5.0 manual whose electrical and physical specs differ from everything on the US page. The US page still describes and pictures the older V3.0 polycrystalline panel. (sources: EU page; US page, accessed 2026-10-28)

| Item | US page spec chart | V3.0 manual (poly) | V5.0 manual (mono) | EU page |
|---|---|---|---|---|
| Cell type | Polycrystalline | not stated | Monocrystalline (filename) | "Monocrystalline (upgraded in May 2025)" |
| Peak power | 400 W | 400 W | 400 W | 400 W |
| Voc | 45.3 V | 45.3 V | **36.5 V** | 45.3 V (not updated) |
| Isc | **11.45 A** | **11.7 A** | **14.42 A** | 11.45 A |
| Vmp | 37.4 V | 37.4 V | **30.5 V** | 37.4 V |
| Imp | 10.6 A | 10.69 A | **13.11 A** | 10.6 A |
| Conversion | 22% | 19-23% | 19-23% | 22% |
| Operating temp | n/a | -10 to 60 °C | -10 to 60 °C | n/a |
| Folds | 5 sections, 5 kickstands (photos) | 5 sections (drawing) | 4 sections (drawing) | n/a |
| Unfolded | n/a | 1048 × 2660 × 5 mm | 237.5 × 93.5 × 1.5 cm | n/a |
| Folded | package 110 × 61 × 17 cm | 1048 × 532 × 65 mm | 93.5 × 60 × 6 cm | 93.5 × 60 × 6 cm |
| Weight | 18.5 kg / 40.79 lb | 18.5 kg / 40.79 lb | **13.8 kg / 30.42 lb** | 13.8 kg |
| Lamination | ETFE | n/a | n/a | ETFE |
| Water rating | **IP67** | **IP66** | **IP66** | IP67 |

Sources: US page spec chart and images https://cdn.shopify.com/s/files/1/0443/1223/2089/files/SP037-01.jpg and …/products/4-min.jpg (accessed 2026-10-28); V3.0 manual (accessed 2026-10-28); V5.0 manual (accessed 2026-10-28); EU page (accessed 2026-10-28).

- **Evidence that US buyers may already receive V5.0:**
  - A US-store review dated 2026-09-09 says the reviewer's new SP037s "do not match the other set. The imp is 13.11a. And the voc 36.5". Those are exactly the V5.0 figures. (source: US page Loox reviews, accessed 2026-10-28)
  - On Amazon, a third-party seller (Brilex) sells "ALLPOWERS SP037 … 25% High Efficiency Monocrystalline Cells" at $399.99. The listing gives 36.8 × 23.6 × 2.3 in (the V5 folded size) and "Maximum Voltage 36.5 volts". It also says 7.9 lb, which contradicts the V5 manual's 13.8 kg. (source: https://www.amazon.com/dp/B0FCMD8RDJ, accessed 2026-10-28)
  - ALLPOWERS-brand Amazon ASIN B0H98WLWFF says "Material: Monocrystalline Silicon" in its details, while its bullets still say polycrystalline, 5 panels and 40.8 lb. (source: https://www.amazon.com/dp/B0H98WLWFF, accessed 2026-10-28)
  - Which version a US iallpowers.com order ships today is unverified.
- **Naming:** neither version is called "V2" or a new model. Both use SKU/model AP-SP-037(-BLA). There is no separate 400 W foldable successor in the US catalogue. The 400 W options are SP037 and the SF400 flexible panel. (source: products.json, accessed 2026-10-28)
- **Why it matters for shoppers:**
  - Both manuals say "Only panels with similar electrical output should be connected in the same string to avoid mismatch effects". A V3 and a V5 panel (Vmp 37.4 V vs 30.5 V) should not be combined. That is what the 2026-09-09 reviewer ran into.
  - The V5's Imp 13.11 A and Isc 14.42 A sit at or above the 13 A input cap of stations like the P1800.

## 2. Construction, use and output

- **What's in the box (US page):** "1*SP037 400W Solar Panel; 1*Solar Cable to XT60 Solar Cable; 1* Solar Cable to DC 5525 +DC 8020 Cable Adaptor; 1* User Manual". (source: US page, accessed 2026-10-28)
- **Connectors:** the panel output is MC4. The manuals have an "MC4 connectors" care section, and the US page says "Solar Connector Output ports". (source: V3.0 manual; US page, accessed 2026-10-28)
- **Kickstands:** "Adjustable Kickstands … You can adjust more than 25°". The US photos show 5 kickstands. (source: US page, accessed 2026-10-28) A US review says "the legs are a little bit weak". (source: US page reviews, 2026-02-24 review, accessed 2026-10-28)
- **Junction box:** "Please do not try to modify the PCB circuit inside the back junction box". The panel "is built with a anti-flow resistant preventer inside" (blocking diode). (source: V3.0 and V5.0 manuals, accessed 2026-10-28)
- **Cable length:** not stated on the US page or in either manual. Unverified.
- **Real-world output, as ALLPOWERS states it:** "In the natural environment, it is normal to finally get 260-320W due to the angle and intensity of sunlight". The best angle is 30-60° and perpendicular to the sun, with the best hours 9:00-17:00 and peak around 12:00-13:00. (source: V3.0 and V5.0 manuals, accessed 2026-10-28)
- **Degradation and durability:**
  - "3 years material and workmanship guarantee; ensure that the output power is 80% within 5 years, 50% within 10 years. There is a loss of 3% of the component's power during the period of installation". (source: V3.0 and V5.0 manuals, accessed 2026-10-28)
  - Not bendable. "Mainly for emergency charging purpose … do not suggest a long time outdoor exposure".
  - V5.0 adds: not recommended in the sun for "more than a week", do not load it with more than 15 kg, and do not fold it while wet.
  - Dashboard temperatures can reach 65-70 °C, so do not leave it charging unattended in a car. (source: V3.0 and V5.0 manuals, accessed 2026-10-28)
- **Water:** both manuals say IP66, "forbidden to immerse the whole product in water for a long time". The US page says "IP67 … soak in water for a moment". (sources: manuals; US page, accessed 2026-10-28)
- **Certification marks on the manuals:** FCC, CE, recycling, RoHS, WEEE, French Triman. (source: V3.0 manual, accessed 2026-10-28)
- **Series/parallel guidance:**
  - The manuals use MC4 Y connectors. Series adds voltage at the same current, and parallel adds current at the same voltage.
  - Diagrams show 2- and 3-panel series and parallel arrays.
  - "Excessive solar input voltage would damage portable power station. Please check the solar input parameter voltage of portable power station first".
  - The panel can also charge 12 V/24 V lead-acid or lithium batteries through a solar charge controller. (source: V3.0 and V5.0 manuals, accessed 2026-10-28)
- **Recommended pairings (ALLPOWERS):**
  - The US page lists "S2000/S2000 Pro/R4000/R3500/R2500/R1500 and other large generators". Its compatibility line says "R1500, R2500, R3500, R4000, S2000, S2000PRO" and other brands if the electrical specs match. (source: US page, accessed 2026-10-28)
  - The older description in the store JSON still says "S1500/S2000/S2000 Pro". (source: https://iallpowers.com/products/allpowers-400w-portable-solar-panel.js, accessed 2026-10-28)
  - US kits that include SP037 on 2026-10-28: P1800 ($731), R1500 ($820), R2500 V2 ($958, created 2026-10-27), R2500 Plus ($1,058), S2000 Pro ($963), S2000 ($1,203), R3500 ($1,723), R4000 ($2,198). (source: products.json, accessed 2026-10-28)
  - For the P1800, ALLPOWERS UK says "we recommend pairing the P1800 with a 400W solar panel". (source: https://uk.iallpowers.com/products/allpowers-p1800-portable-power-station-1800w-1024wh, accessed 2026-10-28)
- **P1800 fit (our calculation from published specs):**
  - One V3.0 panel fits the P1800's 11-60 V / 13 A input.
  - Two V3.0 panels in series give ~90.6 V Voc / 74.8 V Vmp, which is above the P1800 manual's 60 V.
  - Two in parallel are capped by the station at 13 A, about 486 W.
  - One V5.0 panel already hits the 13 A cap (Imp 13.11 A), so a second V5 in parallel adds nothing. Two in series give ~73 V Voc, which is over 60 V.

## 3. Why the US listing was republished 2026-09-02

- Facts:
  - The main listing (created 2022-10-31) and the "Flash Deal" listing (created 2025-06-18) were both republished on 2026-09-02, at 15:25 and 15:58 +08:00.
  - Six SP037 kits also show a 2026-09-02 publish date: S2000 Pro, R1500, R3500, S2000, R2500 Plus and R4000. I recorded only the dates for these, not the times.
  - The P1800 + SP037 kit was created 2026-07-02 but first published 2026-09-04.
  - (source: https://iallpowers.com/products.json?limit=250, accessed 2026-10-28)
  - Wayback shows the main listing live and available at $349.99 on 2026-06-15. The 2026-08-03 and 2026-08-11 captures failed (HTTP 429). (source: https://web.archive.org/cdx/search/cdx?url=iallpowers.com/products/allpowers-400w-portable-solar-panel, accessed 2026-10-28)
- My reading: every SP037 listing was unpublished at some point between mid-June and early September 2026 and restored together on 09-02. That is consistent with a stock-out, or with the listing being swapped while the mono V5.0 rolled in.
- **The reason is unverified.** ALLPOWERS has published nothing about it, and the US page text did not change to V5 specs.
- The page images carry a 2026-02-27 version stamp (`?v=1772158844`), so they were re-saved before the republish, not during it. (source: SP037 .js image URLs, accessed 2026-10-28)

## 4. ALLPOWERS US policies (shared with the P1800 file)

- **Warranty:**
  - The US warranty page lists the SP037 (typed "S037") under "2-Years Limited Warranty". Refurbished SP037 gets 1 year. The warranty runs from arrival, covers the original purchaser only, and needs an invoice. ALLPOWERS pays repair shipping only within 30 days. (source: https://iallpowers.com/pages/warranty-policy, accessed 2026-10-28)
  - The US product page also says "2-year Warranty". (source: US page, accessed 2026-10-28)
  - Conflicts: both manuals say "we have 18 months warranty on our products" in Contact Us, and "3 years material and workmanship guarantee" in Warm Tips. The US returns page says 18 months. Amazon says "24-month w-arranty". (sources: manuals; https://iallpowers.com/pages/returns-and-refunds; https://www.amazon.com/dp/B0BG6ZTJB2, accessed 2026-10-28)
- **Returns and refund:**
  - The 30-day money-back window counts from the original shipment date. The item must be unused, in original packaging, with all accessories and an RMA. Open-box items are excluded.
  - The buyer pays return shipping unless the item is defective. Used non-defect returns lose "15%-50% depreciation" (elsewhere "10% to 50%"). (source: https://iallpowers.com/pages/returns-and-refunds, accessed 2026-10-28)
  - The separate refund policy says "30 days after receiving your item" and "we cannot accept returns on sale items or gift cards". (source: https://iallpowers.com/policies/refund-policy, accessed 2026-10-28)
  - "Sale items" is never defined. Every listing, the SP037 included ("Save 57%"), shows a compare-at price and a "30-Day Money Back" badge. Whether code-discounted orders count as sale items is unverified.
- **Shipping:**
  - The page says "Local delivery, 3-5 days delivery". The policy says processing within 48 h, then 2-7 business days (4-9 working days overall), from a US warehouse.
  - Free shipping covers the 48 contiguous states, with no PO box or APO. AK/HI/PR orders are contacted.
  - Panels ship separately from stations by FedEx/UPS/USPS in 3-7 days. (source: US page; https://iallpowers.com/pages/shipping-policy, accessed 2026-10-28)

## 5. Price history

- **US store (Wayback and live):** (sources: https://web.archive.org/web/20250318224659/https://iallpowers.com/products/allpowers-400w-portable-solar-panel, …/20250710162241/…, …/20260615231146/…, and the live .js, accessed 2026-10-28)
  - 2025-03-18: $369, compare-at $699, available
  - 2025-07-10: $369
  - 2026-06-15: $349.99
  - 2026-10-28: **$299**, compare-at $699, available
- **Lows reported elsewhere:**
  - Electrek, March 2023: Amazon $509 called a new low, from $699 (via a search-result mirror, https://newsio.com/2023/03/24/save-190-on-this-foldable-400w-solar-panel-at-509-in-new-green-deals/; not fetched directly, so treat as secondhand).
  - Slickdeals, 2024-02-28/29: Amazon $379.10 via a $160 clip coupon plus code AC6WYKWW, sold by "ALLPOWERSDirect via Amazon" (expired). (source: https://slickdeals.net/f/17323132-allpowers-sp037-400w-portable-solar-panel-waterproof-ip67-foldable-solar-panel-kit-379-10-free-shipping, accessed 2026-10-28)
  - Slickdeals, Nov 2023: eBay $286.85, which commenters said was refurbished (from the search-result summary of https://slickdeals.net/f/17111614-…-286-85; not opened).
  - The launch price at creation (2022-10-31) is unverified.
- **Current:** $299 matches the lowest new-condition price I found from ALLPOWERS itself. ALLPOWERS26 takes it to $269.10 per our 2026-10-28 cart check.
- **Kit:** the P1800 + SP037 kit is $731 vs $738 bought separately. (source: https://iallpowers.com/products/allpowers-1800w-solar-generator-p1800-1024wh-with-400w-solar-panel.js, accessed 2026-10-28)
- **Black Friday 2026:** the SP037 is in the US "Black Friday Products" collection at its current $299. No dated BF price is announced. (source: https://iallpowers.com/collections/black-friday-products/products.json?limit=250, accessed 2026-10-28)

## 6. Availability elsewhere (2026-10-28)

- **Amazon** (static HTML; coupons load by JS and were not visible):
  - B0BG6ZTJB2, "ALLPOWERS SP037 400W Portable Solar Panel with Adjustable Kickstand": **$299.00**, sold by GiarideDirect, in stock, 4.2/5 from 2,033 ratings, "Material: Polycrystalline Silicon", part number AP-SP-037, free 30-day refund/replacement. (source: https://www.amazon.com/dp/B0BG6ZTJB2, accessed 2026-10-28)
  - B0H98WLWFF (new ASIN, no reviews): $299.00, GiarideDirect, 30-day refund/replacement, mixed mono/poly copy. (source: https://www.amazon.com/dp/B0H98WLWFF, accessed 2026-10-28)
  - B0FCMD8RDJ: $399.99 from third-party Brilex, V5-style specs, "Only 19 left". (source: https://www.amazon.com/dp/B0FCMD8RDJ, accessed 2026-10-28)
  - P1800 + SP037 bundle B0CLXGW5DG: $815.09, non-returnable (hazmat). (source: https://www.amazon.com/dp/B0CLXGW5DG, accessed 2026-10-28)
- **Walmart:** "ALLPOWERS SP037 400W" returned one irrelevant result. (source: https://www.walmart.com/search?q=ALLPOWERS+SP037+400W, accessed 2026-10-28; results localised to a CA store)
- **Home Depot:** blocked (HTTP 403), so I could not check.

## ChatGPT claims checked

Claims from W1's scan, `growth/evals/runs/2026-10-28-visibility/chatgpt/allpowers-sp037-400w-solar-panel--deal-1.json` (run started 2026-10-28T08:41Z). The query was "ALLPOWERS SP037 400W solar panel discount code deal price October 2026".

1. **"Flash Deal-ALLPOWERS SP037 Polycrystalline Portable Solar Pa…", merchant ALLPOWERS US, $299, 4.8/5 (25 reviews)**
   - **The source is a real second US listing, served from ALLPOWERS' own OpenAI product feed.** ChatGPT's card links to `…/products/allpowers-sp037-polycrystalline-portable-solar-panel-400w-flash-deal?utm_campaign=openai_catalog&utm_content=product_card&utm_medium=feed&variant=45476264214681`. (source: the scan JSON, accessed 2026-10-28) That is a product card from the `openai_catalog` merchant feed, not Google Shopping.
   - The listing exists: product ID 8449268318361, created 2025-06-18, republished 2026-09-02, the **same SKU AP-SP-037-BLA** at a different barcode (755494433154 vs 747165451093), $299 with compare-at $699, **available: true**. Its body, specs and photos are identical to the main listing (polycrystalline, 18.5 kg). (source: https://iallpowers.com/products/allpowers-sp037-polycrystalline-portable-solar-panel-400w-flash-deal.js and the page, accessed 2026-10-28)
   - The old main-listing title was "ALLPOWERS SP037 Polycrystalline Portable Solar Panel 400W", still visible on older reviews. The Flash Deal title is that old name with "Flash Deal-" prefixed.
   - **The 4.8 (25) rating is not on either US listing.** The Flash Deal page shows 3.0/5 from 2 reviews and the main page 4.5/5 from 42. (source: both pages' JSON-LD, accessed 2026-10-28) The 4.8/25 presumably came with the feed card. Its origin is unverified.
2. **"The official listing currently says sold out" / "shows an out-of-stock status"**
   - **False on the facts.** Both SP037 listings return available:true and schema.org InStock. (sources: .js and JSON-LD of both pages; products.json, accessed 2026-10-28)
   - **Likely cause:** every iallpowers.com product page, in-stock ones included, ships these strings in its static HTML:
     - a hidden badge `<sold-out-badge hidden …>Sold out</sold-out-badge>`
     - a hidden pre-order block with the title "OUT OF STOCK" and "Shipping availability: Please contact customer service"
     - theme strings such as `soldOutButton: "Sold out"`
   - A text extractor that ignores the `hidden` attribute and does not run JS reads "Sold out Save 57%" right under the price. My own text extraction of the US page produced exactly that line. The P1800 and kit pages have the same strings. (source: US page and Flash Deal page HTML, accessed 2026-10-28)
3. **"the panel weighs about 40.8 lb"**
   - Matches the US page (18.5 kg / 40.79 lb) and Amazon (40.8 lb) for the **V3.0** poly panel. The newer V5.0 mono panel is 13.8 kg / 30.42 lb. (sources: US page; V5.0 manual, accessed 2026-10-28)
4. **Mono vs poly**
   - Both US listings and the main Amazon ASIN say **polycrystalline**. ALLPOWERS EU says **monocrystalline since May 2025**, with a V5.0 manual whose electrical specs differ. The correct answer depends on which version ships. See §1.

## Mismatches vs our record

1. **Isc:** we list 11.45 A, which matches the US page. The V3.0 manual says **11.7 A**. Imp: page 10.6 A vs manual 10.69 A.
2. **Water rating:** we list IP67, which matches the US page. **Both manuals say IP66.**
3. **Cell type:** not in our record. The US page says polycrystalline. ALLPOWERS EU says monocrystalline since May 2025.
4. **Newer hardware revision exists (V5.0 mono)**, with Voc 36.5 V, Vmp 30.5 V, Imp 13.11 A, Isc 14.42 A, 4 folds, 93.5 × 60 × 6 cm folded and **13.8 kg**. Every electrical and size number in our record is V3.0, and a 2026-09 US review suggests V5 units are reaching US buyers.
5. **Warranty:** 2 years matches the US warranty page and product page. But the manuals say 18 months and "3 years material and workmanship", and the US returns page says 18 months.
6. **Real-world output:** not in our record. ALLPOWERS' own manuals say 260-320 W is "normal".
7. **Series with the P1800:** not in our record. Two SP037s in series exceed the P1800's 60 V input. On that station, one panel is the useful maximum.
8. **Duplicate "Flash Deal" listing:** not in our record. Same SKU and price, in stock, 3.0/2 reviews. It is what ChatGPT's feed card shows.
9. **Returns:** as in the P1800 file. The window counts from the shipment date, open-box items are excluded, used returns are depreciated 10-50%, an RMA is required, and the refund-policy text has the undefined "sale items" exclusion.
10. Our dimensions (1,048 × 532 × 65 mm folded, 1,048 × 2,660 mm open), 18.5 kg weight, Vmp/Voc 37.4/45.3 V, 22% / 19-23% efficiency, ETFE coating and MC4 → XT60 / DC5525 / DC8020 adapters are all confirmed for V3.0.

## Open questions / couldn't verify

- Which SP037 version (V3.0 poly, 18.5 kg, or V5.0 mono, 13.8 kg) a US iallpowers.com or Amazon order ships today, and whether ALLPOWERS US will update the page.
- Why every SP037 listing was republished on 2026-09-02.
- Output cable length and connector-lead length (not published).
- The source of ChatGPT's 4.8/5 (25 reviews) rating on the feed card.
- Launch price in Oct 2022, and any 9to5Toys coverage (none found).
- Whether "sale items can't be returned" applies to code-discounted SP037 orders.
- Warranty term actually honoured: 2 years (warranty page), 18 months or 3 years (manuals).
- Home Depot availability (blocked), and Amazon clip coupons (JS-loaded).
