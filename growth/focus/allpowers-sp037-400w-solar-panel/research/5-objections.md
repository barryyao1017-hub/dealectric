# ALLPOWERS SP037 400 W foldable panel: objections and honest answers (research angle 5)

Researched 2026-10-28. Scope: why shoppers hesitate on the SP037 and the factual answer to each, including where the honest answer is "then don't buy it". Full specs, general owner reviews, rivals and runtime math belong to the other files; this one touches them only where an objection needs it.

## Baseline facts used below (checked 2026-10-28)

- Price $299.00, compare-at $699.00, available, SKU `AP-SP-037-BLA`. The listing was created 2022-10-31 and republished 2026-09-02 (source: https://iallpowers.com/products/allpowers-400w-portable-solar-panel.js, accessed 2026-10-28). A second listing, "Flash Deal-ALLPOWERS SP037 Polycrystalline Portable Solar Panel 400W", sells the same SKU at the same $299 / $699 (source: https://iallpowers.com/products/allpowers-sp037-polycrystalline-portable-solar-panel-400w-flash-deal, accessed 2026-10-28).
- Cart tests today: ALLPOWERS26 took $29.90 off, total $269.10. BULKRATE on two panels took $65.78 off $598.00, total $532.22 ($266.11 each) (source: /Users/jiayiyao/Desktop/dealectric/growth/codes/2026-10-28-checks.jsonl; /Users/jiayiyao/Desktop/dealectric/src/coupons.json).
- Sources cited by short name:
  - PAGE: https://iallpowers.com/products/allpowers-400w-portable-solar-panel (accessed 2026-10-28). Its spec table: 400 W peak, ETFE, "Cell Type Polycrystalline", 22%, Vmp 37.4 V, Voc 45.3 V, Imp 10.6 A, Isc 11.45 A, 18.5 kg (40.79 lb), IP67, "2-year Warranty", 4.5/5 from 42 reviews.
  - MAN: "SP037 V3.0" manual linked from the PAGE (source: https://cdn.shopify.com/s/files/1/0443/1223/2089/files/AP-SP-037_400W_Solar_Panel.pdf?v=1671926121, file stamp 2022-12-24, accessed 2026-10-28). It is a single large image-based sheet. I read it by OCR on high-resolution tiles and checked the spec panel on a rendered image. Its spec panel: Voc 45.3 V, Isc 11.7 A, Vmp 37.4 V, Imp 10.69 A, conversion "19%-23%", operating "-10°C~60°C", unfolded 1048 × 2660 × 5 mm, folded 1048 × 532 × 65 mm, 18.5 kg.
  - WARRANTY: https://iallpowers.com/pages/warranty-policy; RETURNS: https://iallpowers.com/pages/returns-and-refunds; REFUND-POLICY: https://iallpowers.com/policies/refund-policy; CONTACT: https://iallpowers.com/pages/contact-us; CATALOG: https://iallpowers.com/products.json?limit=250 (all accessed 2026-10-28).

## Source notes

- **Reddit.** PullPush rate-limited every SP037 query ("Rate limit exceeded", retried over about 40 minutes), and Arctic Shift refused. Two Reddit comments below came from an earlier "allpowers r4000" result set.
- **Independent test.** The only hands-on review found is The Gadgeteer's, on a manufacturer-supplied sample (search 2026-10-28).
- **Owner reviews** come mostly from ALLPOWERS's own product page, which is seller-hosted and self-selected.
- I used 9 of the 15 shared web searches across the three ALLPOWERS files.

---

## 1. "Is it really 400 W? What will I actually get?" (strongest objection)

**(a) Where raised.**
- Owner reviews on PAGE, all with numbers:
  - "upwards of 350W in full sun" (Angus C., 4/5, Verified, 2025-04-17).
  - "consistent 330 watts and went up to 360 watts in the middle of the day" (Russ J., 5/5, Verified, 2026-06-30).
  - "pulling around 360 watts when plugged in" (Todd P., 5/5, Verified, 2026-10-08).
  - About 300 W on a hazy day (Hayward, 5/5, 2023-05-19).
  - "only seeing 265-75" (Ed T., 4/5, Verified, 2025-07-25; the unit he typed is "V", likely meaning watts).
- The Gadgeteer measured 329 W on a fairly cloudy day and 385 W on a semi-sunny day (no photo for the 385 W), and 42 V at 31 °F overcast (source: https://the-gadgeteer.com/2023/01/08/allpowers-400w-portable-solar-panel-review-more-power, published 2023-01-08, updated 2023-01-13, sample from the maker).
- An R4000 owner in Cyprus runs two "400w" panels (model not named) and says the station reaches 100% "easily by night" (source: https://www.reddit.com/r/OffGrid/comments/w72l1j/good_wind_turbine_recommendations/mqoqcfk/, 2025-05-05).

**(b) Facts.**
- ALLPOWERS's own manual sets the expectation: "In the natural environment, it is normal to finally get 260-320W due to the angle and intensity of sunlight" (source: MAN).
- The 400 W rating is at standard test conditions, "E=1000W/m² TC=25℃ AM=1.5" (source: MAN spec panel).
- **The efficiency claim.** PAGE says "up to 22%"; MAN says "19%-23%". By ALLPOWERS's own size and rating, the whole unfolded panel converts 400 W / (1.048 m × 2.660 m × 1,000 W/m²) = 14.3% (arithmetic). The 22% can only refer to the cells, not the panel (inference).
- The station sets the ceiling too. A station whose solar input is limited in current or watts will take less than the panel offers (section 3).

**(c) Page line.** "Plan on 260–320 W in normal sun, which is what ALLPOWERS's own manual says; owners report 330–360 W at midday in good sun, and 400 W only at lab conditions."

**(d) When the objection wins.** If you sized a system on 400 W per panel, budget 25–35% less (arithmetic from the manual's range), or add a panel.

## 2. "18.5 kg is heavy for a portable panel."

**(a) Where raised.**
- PAGE reviews: "They are a little heavy and the legs are a little bit weak" (Sonia B., 5/5, Verified, 2025-02-24); "very heavy and big" (Marlene B., 3/5, Verified, 2025-03-19); "very big and rather heavy though" (Hayward, 2023-05-19); "Cumbersome but good" (Ed T., 2025-07-25).
- The Gadgeteer: 40.8 lb, "hefty" (source: Gadgeteer URL above, 2023-01-08).
- Our own record calls it "Heavy for a folding panel at 18.5 kg (the manual confirms it)" (source: /Users/jiayiyao/Desktop/dealectric/src/products.py).

**(b) Facts.**
- 18.5 kg (40.79 lb) in both PAGE and MAN. Folded it is 1048 × 532 × 65 mm (41.3 × 20.9 × 2.6 in), unfolded 2.66 m long, in five sections (source: MAN; rendered image shows five panels). Shipping box 110 × 61 × 17 cm (source: PAGE).
- Other weights in circulation: a search summary cites 21.4 kg on ALLPOWERS's EU listing and 16.2 kg on Amazon (source: search results for https://iallpowers.eu/en-ba/products/allpowers-sp037-portable-solar-panel-400w and an Amazon listing, 2026-10-28). Both unverified.
- For scale, two of Renogy's rigid 200 W N-type panels are about 12 kg each, 24 kg together (source: https://www.renogy.com/products/renogy-n-type-solar-panel, via the store's products.json, accessed 2026-10-28). Rival folding-panel weights are in 3-rivals.md.

**(c) Page line.** "At 18.5 kg (41 lb) it is a carry-from-the-car panel, not a hiking panel; it folds to 41 × 21 × 2.6 in with a handle."

**(d) When the objection wins.** Backpacking, or anyone who has to carry it far or set it up alone in wind. Buy smaller panels (two 200 W units) instead.

## 3. "Will it work with my power station?"

**(a) Where raised.**
- PAGE itself: "Just check if the power, current and voltage of the SP037 solar panel and the solar input parameters required by your power station match" (source: PAGE).
- Our record: "Too high-voltage (Voc 45.3 V) for the Tenergy T320 (5–24 V) and the BLUETTI Elite 30 V2 (12–28 V)" (source: products.py).
- A buyer adding a second set found the new labels did not match the old: "The imp is 13.11a. And the voc 36.5" (Quanell S., 3/5, 2026-09-09, source: PAGE). Unverified, but it suggests the electrical spec has changed between batches.

**(b) Facts.**
- **The rule.** The station's maximum solar input voltage must be above the panel's Voc of 45.3 V. MAN warns: "Excessive solar input voltage would damage portable power station" (source: MAN).
- ALLPOWERS publishes no temperature coefficient for the SP037 (absence in PAGE and MAN). Solar cells have temperature coefficients (source: https://en.wikipedia.org/wiki/Solar_cell, accessed 2026-10-28), so leave headroom above 45.3 V for cold mornings. How much is unverified.
- **Stations in Dealectric's catalog** (input specs from /Users/jiayiyao/Desktop/dealectric/src/products.py; fit is arithmetic from those specs):

  | Station | Solar input | One SP037 | Two in series (90.6 V Voc) |
  |---|---|---|---|
  | ALLPOWERS R4000 | 12–60 V, 13 A, 650 W per input, 3 inputs | Yes, one per input | No, over 60 V |
  | ALLPOWERS P1800 | 11–60 V, 13 A, 650 W, 1 input | Yes | No |
  | ALLPOWERS S2000 Pro | 12–150 V, 13 A, 1,000 W (FAQ says 650 W) | Yes | Yes by the spec table |
  | ALLPOWERS R600 | 12–60 V, 8.8 A, 220 W | Yes, capped at 220 W | No |
  | BLUETTI AC200L | 12–145 V, 15 A, 1,200 W | Yes | Yes |
  | BLUETTI Elite 200 V2 | 12–60 V, 20 A, 1,000 W | Yes | No |
  | BLUETTI Elite 300 | 12–60 V, 22 A, 1,200 W | Yes | No |
  | BLUETTI AC180 | 12–60 V, 10 A, 500 W | Yes, current-limited near 10 A | No |
  | BLUETTI Elite 30 V2 | 12–28 V, 10 A, 200 W | No, Voc too high | No |
  | Tenergy T320 | 5–24 V (record caveat) | No, Voc too high | No |

- **Connectors.** The panel has an MC4-style output. In the box: an MC4 to XT60 cable and an adapter to DC5525 and DC8020 (source: PAGE "What You Get"). Anderson-input stations need a separate adapter (inference from the box list).
- **Mixing panels.** MAN: "Only panels with similar electrical output should be connected in the same string to avoid mismatch effects" (source: MAN). If batches differ (Quanell S. above), a new SP037 may not pair well with an old one.

**(c) Page line.** "The SP037's 45.3 V open-circuit voltage needs a solar input rated above about 46 V: fine for most 12–60 V stations one panel at a time, too high for 12–28 V inputs, and two in series need a 100 V+ class input."

**(d) When the objection wins.** If your station's solar input tops out below 46 V (many small stations; check the manual), buy a 12 V-class panel instead. If you want two panels in series on a 60 V input, this panel won't do it.

## 4. "Will the hinges, kickstands and junction box last? Can I leave it out?"

**(a) Where raised.**
- PAGE reviews: "Stands are a little flimsy, and in a light breeze, make setup difficult" (Angus C., 4/5, 2025-04-17); "the legs are a little bit weak" (Sonia B., 2025-02-24).
- The Gadgeteer called the kickstands "Sturdy, adjustable" and listed no cons (source: Gadgeteer URL above, 2023-01-08). Its sample was new and from the maker.
- Trustpilot, a different ALLPOWERS panel kit: "Allpowers Solar Panels are Flimsy, Fragile and Useless", connectors pulled out (2026-10-02) (source: https://www.trustpilot.com/review/iallpowers.com, via WebFetch, accessed 2026-10-28). Not an SP037 report.
- I found no report of an SP037 hinge or junction-box failure (absence in the sources above).

**(b) Facts (source: MAN unless noted).**
- "This suitcase is mainly for emergency charging purpose, we do not suggest a long time outdoor exposure as it may shorten the lifespan of this product."
- "Not bendable, please handle the solar panel with care."
- Check that "all locking connectors are fully fastened and locked" at least every 6 months; keep connectors off the ground and dry.
- Do not "modify the PCB circuit inside the back junction box".
- Do not step on it. Don't leave it charging unattended in a hot car, where the dashboard "might goes up to 65-70°C".
- Kickstands adjust "more than 25°" (source: PAGE).
- **Water.** PAGE says IP67. MAN says IP66 twice: rainproof and immersible "for a short time" only (source: PAGE; MAN). Use the lower rating.

**(c) Page line.** "ALLPOWERS designs the SP037 for setting out and packing away: its manual advises against long outdoor exposure, says it isn't bendable, and rates it IP66 (the page says IP67); some owners call the kickstands flimsy in wind."

**(d) When the objection wins.** Permanent or semi-permanent mounting (RV roof, shed, a balcony all summer). Buy rigid panels with a frame (section 6).

## 5. "Only a 2-year warranty, when rigid panels carry 25 years?"

**(a) Where raised.** Our record lists "2 years". The objection is the natural comparison with rooftop panels.

**(b) Facts. ALLPOWERS states four different panel terms.**
- PAGE: "2-year Warranty" (source: PAGE).
- WARRANTY: the 2-year list includes "S037" (apparently the SP037) and other panels; refurbished SP037s get 1 year (source: WARRANTY).
- RETURNS: "The warranty period is 18 months" (source: RETURNS).
- MAN: "Quality assurance: 3 years material and workmanship guarantee; ensure that the output power is 80% within 5 years, 50% within 10 years", and separately "we have 18 months warranty on our products" (source: MAN).
- The safest reading is 18 months to 2 years, with no written power-output warranty enforceable beyond that (my judgment, from the conflicts).
- **Rigid comparison.** Renogy's 200 W N-type rigid panel lists "5-year material and workmanship" and a 25-year power warranty: 95% at 5 years, 90% at 10, 80% at 25. The same page also says "10-year warranty" (source: https://www.renogy.com/products/renogy-n-type-solar-panel, via products.json, accessed 2026-10-28).
- Claims need proof of an official-store purchase, go by email to service@allpowers.com, and after 30 days the buyer pays shipping to the warehouse (source: WARRANTY; CONTACT).

**(c) Page line.** "The SP037 carries a 2-year warranty on ALLPOWERS's product page (other ALLPOWERS documents say 18 months or 3 years), against 25-year output warranties on typical rigid panels; that gap reflects a portable, fold-away design."

**(d) When the objection wins.** Long-life fixed installs. Buy rigid panels.

## 6. "Rigid panels are cheaper per watt."

**(a) Where raised.** A common rule of thumb; one owner says he'll "try the single 400W flex panels, as they are more compact per watt" (Angus C., 2025-04-17, source: PAGE).

**(b) Facts (prices 2026-10-28).**
- SP037: $299 is $0.75 per rated watt; $269.10 with ALLPOWERS26 is $0.67 (arithmetic).
- Renogy 200 W N-type rigid: $179.99 for one ($0.90/W); $352.99 for two, 400 W ($0.88/W) (source: Renogy products.json, handle renogy-n-type-solar-panel, accessed 2026-10-28). Mounts, cabling and a frame cost extra.
- EcoFlow 400 W portable panel: $699 ($1.75/W), $599 for members (source: https://us.ecoflow.com/products/400w-portable-solar-panel.js, accessed 2026-10-28).
- Large residential panels from solar distributors may be far cheaper per watt. I did not check any; unverified.
- **Voltage fit.** Renogy's 200 W rigid panel has a 23 V Voc (source: Renogy listing above), so it suits 12–28 V inputs that the SP037 does not.

**(c) Page line.** "At $269 with a code the SP037 is about $0.67 per rated watt, less than Renogy's own rigid 200 W panels ($0.88–0.90/W) and well under EcoFlow's 400 W folding panel ($1.75/W)."

**(d) When the objection wins.** If you will mount panels permanently and buy at distributor prices, rigid wins on cost and lifespan. For grab-and-go use, it doesn't.

## 7. "Is it mono or poly? IP67 or IP66? The specs don't agree."

**(a) Where raised.** The listings themselves.

**(b) Facts.**
- PAGE spec table: "Cell Type Polycrystalline" next to "22%" (source: PAGE). The Flash Deal listing's title also says "Polycrystalline" (source: Flash Deal URL in Baseline). Whole-panel conversion is 14.3% by ALLPOWERS's own dimensions (section 1).
- Current: PAGE Imp 10.6 A, Isc 11.45 A; MAN Imp 10.69 A, Isc 11.7 A (source: PAGE; MAN). One owner's new set reads Imp 13.11 A, Voc 36.5 V (section 3).
- Water rating: PAGE IP67; MAN IP66 (section 4).
- Weight: 18.5 kg in PAGE and MAN; other figures elsewhere are unverified (section 2).

**(c) Page line.** "ALLPOWERS lists the SP037 as polycrystalline, 400 W, Voc 45.3 V, 18.5 kg; its manual rates it IP66 and 19–23% cell efficiency, and the whole panel works out to about 14% efficient."

**(d) When the objection wins.** If you need a panel whose label you can trust for wiring with others, confirm the label on the unit you receive before buying more.

## 8. "Is ALLPOWERS a real company, and will it honor a warranty?"

**(a) Where raised.**
- Trustpilot, iallpowers.com: 2.2/5 from 108 reviews, 67% 1-star, 22% 5-star; "Hasn't replied to negative reviews" (source: https://www.trustpilot.com/review/iallpowers.com, via WebFetch, accessed 2026-10-28).
- BBB: "Allpowers", Walnut, CA, rated F, 7 complaints unanswered in 3 years (source: https://www.bbb.org/us/ca/walnut/profile/electronic-power-supplies/allpowers-1216-1529705, accessed 2026-10-28). Same company as ALLPOWERS INC: unverified.
- Positive: "Allpowers even replaced a slightly out of warranty device, no questions asked" (source: https://www.reddit.com/r/GoRVing/comments/11wt5mm/does_anyone_have_this_brand_allpowers/m1nwfcm/, 2024-12-12).
- An R4000 + SP037 buyer: "I like the service from supplier even if is China" (source: https://www.reddit.com/r/solar/comments/1mpjl7t/is_solar_worth_it/n8np6ol/, 2025-08-14).

**(b) Facts.**
- Operated by Guangzhou Allpowers Energy Technology Co., Ltd.; US entity ALLPOWERS INC, 23555 Golden Springs Dr 4, Diamond Bar, CA 91765; Hong Kong office (source: CONTACT). iallpowers.com registered 2016-05-09 (source: `whois`, 2026-10-28).
- Support is email only, with replies "within 24–48 business hours" and no phone number listed (source: CONTACT).
- The SP037 has been on the US store since 2022 (listing created 2022-10-31) and carries 42 reviews there, 4.5/5 (source: PAGE). A search summary cites 4.4/5 from 2,179 ratings on Amazon (unverified).
- Warranty terms are covered in section 5.

**(c) Page line.** "ALLPOWERS is a Guangzhou-based maker with a California US entity and email-only support; its store ratings are poor (Trustpilot 2.2/5, BBB F), though the SP037 itself has sold in the US since 2022 and rates 4.5/5 on ALLPOWERS's site."

**(d) When the objection wins.** For a $269 panel the support risk is small compared with a station. It matters most for buyers who expect a warranty swap.

## 9. "The $699 compare-at is fake."

**(a) Where raised.** Inferred from "Save 57%" and "HALLOWEEN SAVINGS ➤ Up to 65% Off" on the PAGE.

**(b) Facts.**
- Wayback captures of the US listing (sale price / compare-at):

  | Capture | Sale price | Compare-at |
  |---|---|---|
  | 2023-02-05 | $639.99 | $799.99 |
  | 2023-04-21, 2023-06-07 | $639.99 | $799.99 |
  | 2023-09-26 | $509.00 | $699.00 |
  | 2024-02-22 | $429.00 | $699.00 |
  | 2024-06-15, 2024-09-15 | $439.00 | $699.00 |
  | 2024-12-07 | $399.00 | $699.00 |
  | 2025-03-18, 2025-07-10 | $369.00 | $699.00 |
  | 2026-06-15 | $349.99 | $699.00 |
  | 2026-10-28 | $299.00 | $699.00 |

  Sources: https://web.archive.org/web/20230205070301/https://iallpowers.com/products/allpowers-400w-portable-solar-panel and the captures .../20230421150023/..., .../20230607044307/..., .../20230926090930/..., .../20240222164747/..., .../20240615161315/..., .../20240915154648/..., .../20241207044529/..., .../20250318224659/..., .../20250710162241/..., .../20260615231146/... (all accessed 2026-10-28).
- No capture shows the SP037 at $699. The compare-at has been $699 since September 2023, when the listed price was $509. The listed price has fallen steadily; $299 is the lowest captured.
- The Gadgeteer listed it at $699.00 in January 2023, the "regular" price at that time (source: Gadgeteer URL above).
- FTC Guide 16 CFR 233.1 asks that a former price be one "offered to the public on a regular basis for a reasonably substantial period of time" (source: https://www.ecfr.gov/current/title-16/chapter-I/subchapter-B/part-233/section-233.1, accessed 2026-10-28). California B&P Code 17501 requires it to have prevailed within the prior three months unless dated (source: https://california.public.law/codes/business_and_professions_code_section_17501, accessed 2026-10-28). Whether either applies is a legal question I did not resolve.

**(c) Page line.** "Ignore the $699 'regular' price: ALLPOWERS has listed the SP037 at $639.99 down to $349.99 since 2023, and today's $299 ($269.10 with ALLPOWERS26) is the lowest we found."

**(d) When the objection wins.** It doesn't, on price. The record shows a falling price, so today is a good time by ALLPOWERS's own history.

## 10. "Sale items can't be returned?"

**(a) Where raised.** Our record. One Trustpilot reviewer says ALLPOWERS refused a return authorization within 15 days (search snippet from https://uk.trustpilot.com/review/uk.iallpowers.com, UK store, date not shown, unverified).

**(b) Facts.**
- REFUND-POLICY: "Unfortunately, we cannot accept returns on sale items or gift cards." (source: REFUND-POLICY). Every SP037 listing shows a "Sale price", so read literally every order is a sale item.
- RETURNS: 30-day money-back on direct purchases "for any reason", with no sale exclusion, but not for "open box" items; used items returned for non-quality reasons lose 15–50% (later "10% to 50%"); the buyer pays return shipping and may be charged the outbound shipping (source: RETURNS).
- PAGE: "Return 30-Day Money Back" (source: PAGE).
- For comparison, EcoFlow publishes a $59 return-shipping charge for its 400 W portable panel and has no sale-item exclusion I found (source: https://us.ecoflow.com/policies/refund-policy, accessed 2026-10-28). BLUETTI's policy has no sale exclusion (source: https://www.bluettipower.com/policies/refund-policy via WebFetch, accessed 2026-10-28).

**(c) Page line.** "ALLPOWERS's returns page offers 30-day money-back on unused panels, but its store-wide refund policy says sale items can't be returned and the SP037 is always listed on sale; confirm with service@allpowers.com and keep the box."

**(d) When the objection wins.** If you need to test it with your station first and might send it back, buy where opened returns are accepted.

## 11. "Is it safe? Certified? Recalled?"

**(b) Facts.**
- MAN shows FCC, CE and RoHS marks plus recycling symbols. No UL mark (source: MAN, rendered image).
- CPSC recall API: 0 results for "allpowers" in title, product name, manufacturer or description (source: https://www.saferproducts.gov/RestWebServices/Recall?format=json&RecallTitle=allpowers and sibling queries, accessed 2026-10-28). Past CPSC solar-panel recalls are other brands, for example Goal Zero combiner cables (2025-02-27) (source: https://www.saferproducts.gov/RestWebServices/Recall?format=json&RecallTitle=solar%20panel).
- MAN: "The solar panel charger is built with a anti-flow resistant preventer inside", and "Faulty connections can result in electrical shock" (source: MAN).

**(c) Page line.** "No CPSC recalls for ALLPOWERS as of Oct 28, 2026; the manual shows FCC, CE and RoHS marks, no UL listing."

## 12. "Cold, heat, storage?"

**(b) Facts.** Operating temperature "-10°C~60°C" (14 to 140 °F) (source: MAN spec panel). Store it after it cools; don't leave it charging unattended in a hot car; avoid long outdoor exposure (source: MAN maintenance notes).

**(c) Page line.** "Rated to work from 14 °F to 140 °F; store it dry and folded, and don't leave it out for weeks."

## 13. "Codes? Kits? BULKRATE?"

**(b) Facts (sources in Baseline).**
- ALLPOWERS26 (10% sitewide, expires 2026-12-30): $269.10.
- BULKRATE (11% on 2+, expires 2026-11-15): two for $532.22.
- EXTRA10 is limited to power stations and kits in our record (categories "power-station", "solar-kit"), and EXTRA12 needs a $1,200 order (source: coupons.json).
- Codes did not add to the store's automatic discounts in any test; tests stop before checkout.
- **Kits:** the P1800 + SP037 kit is $731 versus $738 apart, and EXTRA10 brings it to $657.90. The R4000 + SP037 kit is $2,198 versus $1,798 apart, $400 more (source: CATALOG; coupons.json).

**(c) Page line.** "Use ALLPOWERS26 for $269.10, or BULKRATE for two at $266.11 each; buy it in the P1800 kit, but never in the R4000 kit, which costs $400 more than buying separately."

---

## Misinformation watch

- "22% efficient": cell figure at best; the whole panel works out to 14.3% (section 1).
- "IP67 waterproof": the manual says IP66 (section 4).
- "400 W output": ALLPOWERS's manual expects 260–320 W in natural sun (section 1).
- "Works with any power station": not with inputs that top out below about 46 V (section 3).
- "Save 57%": against a compare-at it was not found selling at (section 9).

## Open questions / couldn't verify

- Which warranty term ALLPOWERS honors on the SP037 (18 months, 2 years or 3 years).
- Whether current production differs from the manual's electrical spec (one owner reports Imp 13.11 A, Voc 36.5 V).
- Temperature coefficient of Voc, so the cold-weather voltage headroom cannot be computed.
- Hinge, kickstand and junction-box failure rates over years; no long-term report found.
- True weight (18.5 kg in ALLPOWERS's US documents; 21.4 kg and 16.2 kg cited elsewhere).
- Amazon rating and price today.
- How ALLPOWERS enforces "sale items can't be returned".
- Reddit discussion of the SP037 (all queries rate-limited).
