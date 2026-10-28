# BLUETTI AC200L: objections and honest answers (research angle 5 of 5)

Researched 2026-10-28. Scope: the reasons shoppers hesitate and the factual answer to each, including where the honest answer is "then don't buy it". Full specs, general owner reviews, rivals and runtime math are in files 1 to 4. This file touches them only where an objection needs it.

## Baseline facts used below (checked today)

- Price $899.00, compare-at $1,599.00, available. BLUETTI's product record was created 2023-10-31 (source: https://www.bluettipower.com/products/ac200l.js, accessed 2026-10-28).
- AFF5OFF passed in BLUETTI's cart on the AC200L at $899: $44.95 off, so $854.05 (source: /Users/jiayiyao/Desktop/dealectric/src/coupons.json, cart test dated 2026-10-27).
- Warranty: 60 months for "AC200L/AC200P L" (source: https://www.bluettipower.com/pages/product-warranty-period, accessed 2026-10-28).
- **Being phased out (this corrects the brief's "not discontinued").** Checked 2026-10-28 08:43 UTC:
  - The indexed listing that BLUETTI's own menu links to shows "Discontinued" next to US$899.00. Its structured data says `"availability":"https://schema.org/OutOfStock"` and `sales_status_discontinued: true`, for the same SKU AC200L-US-GY-BL-SPFUS-00 (source: https://www.bluettipower.com/products/ac200l-portable-power-station, and https://www.bluettipower.com/products/ac200l-portable-power-station.js showing `available: false`, price 899.00, compare-at 899.00, accessed 2026-10-28).
  - The standalone page that sells the unit at $899 carries `<meta name="robots" content="noindex,nofollow">` and shows InStock (source: https://www.bluettipower.com/products/ac200l, accessed 2026-10-28).
  - The AC200L is not yet on BLUETTI's discontinued-models list. That page still says AC200P → AC200L (source: https://www.bluettipower.com/pages/bluetti-discontinued-models, accessed 2026-10-28).
  - Details are in section A.

## Source notes (read before reusing anything here)

- **Manual.** The only AC200L manual I could download is "User Manual V3.0", the UK/EU edition (230 V) (source: https://s4.bluettipower.com/bluetti_lgf/support/2025/08/662dc639-483f-4d92-9a90-f9c2605b7abf.pdf, file posted 2025-08, linked from https://support.bluettipower.com/en-gb/products/ac200l-power-station, accessed 2026-10-28). Below it is cited as "MAN". Its temperature, noise, charging-mode and safety text applies to the whole model. Its voltage and overload figures do not apply to the US 120 V unit. The US support page did not show a PDF link without JavaScript.
- **US spec and FAQ.** BLUETTI's US product page renders by JavaScript and returned no spec text. BLUETTI Canada's AC200L page carries the 120 V / TT-30 North American spec and a 16-question FAQ (source: https://www.bluettipower.ca/pages/ac200l, accessed 2026-10-28). Cited below as "CA page".
- **Reddit.** No search returned a Reddit thread. Frequency below comes from review cons lists, deal threads, Trustpilot, BBB and BLUETTI's own forum. BLUETTI's forum moved to forum.bluettipower.com and old thread URLs now redirect to its home page. I read one thread through its web.archive.org copy.
- **Search budget.** The shared web-search budget ran out near the end. Items marked "unverified" could not be checked further.
- **Weak sources.** Several "review" sites state false specs (see "Misinformation watch" at the end). I cite them only for clearly labeled weak evidence.

---

## A. "Is it being discontinued? Should I wait for the Apex 200?" (strongest objection this week)

**(a) Where raised.**
- BLUETTI's own site: the indexed AC200L listing reads "Discontinued", and every page carries the banner "Apex 200 Coming Soon | Unlock Pre-Launch Exclusives" (source: https://www.bluettipower.com/products/ac200l-portable-power-station, accessed 2026-10-28).
- One ChatGPT answer called the AC200L discontinued (our record). That answer was early, not wrong.

**(b) Facts.**
- **Status.**
  - The indexed listing is "Discontinued" and OutOfStock.
  - The same SKU still sells at $899 (compare-at $1,599) on a noindex page.
  - The AC200L is not yet on BLUETTI's discontinued-models list.
  - Sources and timestamps are in "Baseline facts" above.
  - The coordinator also reports that every AC200L bundle is unavailable. I did not re-check the bundles. The bundle links in BLUETTI's menu all point to the discontinued listing (source: navigation data in https://www.bluettipower.com/pages/bluetti-discontinued-models, accessed 2026-10-28).
- **What discontinued means for owners.** BLUETTI's discontinued-models page says (source: https://www.bluettipower.com/pages/bluetti-discontinued-models, accessed 2026-10-28):
  - "We will continue to provide warranty service for discontinued products."
  - In warranty, "we will provide free repair or replacement services". Out of warranty, it offers "paid repair programs or discounted upgrade programs".
  - "In some cases, discontinued products may be replaced with a successor or equivalent model."
  - Accessories and "extended batteries" can still be bought "depending on stock availability".
  - App-enabled discontinued products "can still be connected to the App normally".
  - Firmware updates for discontinued models are case by case ("confirm the latest support status through customer service").
  - Discontinued models are "removed from the official website and authorized channels after they were sold out".
  - Discontinuation is "usually due to product iteration or market update", not a product problem (BLUETTI's own claim).
  - The 60-month warranty term itself is unchanged (warranty period page above).
- **The successor.** BLUETTI Apex 200 (source: https://www.bluettipower.com/pages/apex-200-expandable-power-station, accessed 2026-10-28):
  - 2.56 kWh and 3,200 W continuous; up to 3,600 W "when a compatible expansion battery is connected".
  - Built-in TT-30R and a 12V/30A Anderson output.
  - Up to 3,000 W solar (2,000 W high-voltage + 1,000 W low-voltage).
  - Silent / Standard / Turbo AC charging.
  - About 59.5 lb (27 kg), versus 62.4 lb for the AC200L.
  - Up to six B300K or B500K batteries, to 33.28 kWh.
  - "UPS mode is disabled by default and must be enabled in the BLUETTI app".
  - Launch: "planned to go on sale November 4, 2026". The coordinator was told Nov 5; BLUETTI's page says Nov 4.
  - Price: not announced; the page offers "early pricing details" for subscribers.
  - Not published: cycle rating, UPS switch-over time, warranty length, self-heating. Unverified.
  - "Early access since Oct 21" (coordinator): not shown on the page. Unverified.
- **Do batteries bought now carry over?** Yes, per BLUETTI:
  - The Apex 200 FAQ Q5 says it "supports compatible BLUETTI B300K and B500K expansion batteries" (Apex 200 page above).
  - The B300K page lists compatibility as "AC200L, AC200MAX, AC300, AC500, Apex 300". It ships with a CA90 Battery Connection Cable and costs $1,079 today (source: https://www.bluettipower.com/products/b300k, accessed 2026-10-28). The Apex 200 is not yet on that list.
  - The B500K page says it "works with old, existing, or future BLUETTI power stations". It ships with a CA90 cable and costs $1,789 today (source: https://www.bluettipower.com/products/b500k-expansion-battery, accessed 2026-10-28).
  - Whether the Apex 200 uses the same CA90 cable is unverified.
- **Will $899 fall further as end-of-run stock?** No source answers this.
  - Bundles are gone and the indexed listing is out of stock. BLUETTI's practice is to remove discontinued models "after they were sold out". The remaining units sit on a page hidden from search.
  - Together that looks like quiet sell-through more than a clearance sale (inference). The stock could run out before Black Friday (2026-11-27).
  - Past lows were $751 (BLUETTI, 2025-12-30) and $748.99 (Amazon, 2026-02-23); see section 4.
  - BLUETTI's 30-day price guarantee refunds a same-store drop, "Excludes flash sales and special promotions" (source: https://bluettipower.com/pages/how-to-buy, accessed 2026-10-28). It would cover a plain markdown within 30 days. Whether it covers a Black Friday or launch-week promotion is unverified.
- **Is waiting a week the honest advice?** Mostly yes, for anyone who can wait (inference from the dated facts above):
  - The Apex 200 goes on sale in 7 days, with more capacity, more output, a lower weight, the same batteries and the same RV outlet.
  - Its price is the one unknown. The AC200L itself launched at a $1,499 early-bird price in Nov 2023 (search-result summary of Electrek/9to5Mac launch coverage, unverified detail). The Apex 200 could well launch above $899, but that is unverified.
  - The risk of waiting: the AC200L may sell out at $899.
  - A buyer who orders now keeps a fallback. BLUETTI's 30-day money-back covers an unused unit in its original box, minus return shipping (source: https://www.bluettipower.com/policies/refund-policy, accessed 2026-10-28; §5 below).

**(c) Page line.** "BLUETTI is phasing out the AC200L (its main listing says Discontinued) and launches the Apex 200 on Nov 4, 2026 with more capacity and output and the same B300K/B500K batteries; BLUETTI says warranty service continues for discontinued models, so the AC200L at $899 is a good buy only if you need power now or the Apex 200 comes in well above it."

**(d) When the objection wins.**
- Anyone who can wait a week should see the Apex 200's price first.
- Anyone planning a large expandable system should look at the newer unit, which takes up to six batteries.
- The AC200L still makes sense if you need it before Nov 4, or if the Apex 200 launches well above $899 and 2 kWh and 2,400 W are enough.

## 1. "62 lb with no wheels. Can I actually move it?"

**(a) Where raised.** Weight appears in the cons of almost every review:
- Trusted Reviews lists "Very difficult to move around" (source: https://www.trustedreviews.com/reviews/bluetti-ac200l, 2024-04-19).
- The Ambient lists "Bulky and heavy" (source: https://www.the-ambient.com/reviews/bluetti-ac200l-expandable-power-station-review/, 2024-09-17).
- The Gadgeteer lists "Heavy (62.4 pounds)" (source: https://the-gadgeteer.com/2023/12/11/bluetti-ac200l-portable-power-station-review-a-powerful-one-for-all-solution-to-meet-your-daily-electricity-needs/, 2023-12-11).
- Notebookcheck calls it "difficult to manoeuvre" (source: https://www.notebookcheck.net/Bluetti-AC200L-hands-on-review-Fast-charging-power-station-delivers-convincing-results.869738.0.html, 2024-08-05, updated 2026-02-18).
- OffGrid Benchmark calls it "a two-person lift" (source: https://www.offgridbenchmark.com/portable-power-stations/reviews/bluetti-ac200l/, updated 2026-04-08).

**(b) Facts.**
- It weighs 28.3 kg / 62.4 lb and measures 420 × 280 × 366.5 mm (source: MAN spec table, accessed 2026-10-28).
- It has two fixed top handles and no wheels (source: Notebookcheck URL above, 2024-08-05).
- Trusted Reviews says it is too heavy for one person to lift for any distance. It notes that the Anker SOLIX F2000 has wheels and a telescopic handle (source: Trusted Reviews URL above, 2024-04-19).
- BLUETTI's handling table recommends 2 people for items of 18 to 32 kg. It suggests "mechanical assistance such as carts" if needed (source: MAN §1.4, accessed 2026-10-28).
- Keep it upright. The CA page FAQ Q14 says laying it on its side "may damage the internal structure" and tells you to keep it upright when stored or moved (source: https://www.bluettipower.ca/pages/ac200l, accessed 2026-10-28). The manual says "Do not move the product while operating" (source: MAN §1.2, accessed 2026-10-28).
- **Cart.** I found no BLUETTI trolley that lists the AC200L as compatible.
  - BLUETTI's Folding Trolley (330 lb load) is listed for the AC200MAX, AC300 and AC500 (source: https://www.walmart.com/ip/BLUETTI-Folding-Trolley-330lbs-Load-Capacity-Foldable-Hand-Truck-with-360-Universal-Front-Wheel-and-Foot-Brake-System-for-AC200MAX-AC300-AC500/3620008126, listing title from search result, accessed 2026-10-28).
  - The BLUETTI Trolley Cart lists AC200P/AC200MAX/AC300/B300/B230/EB70/EB55/EB150 (source: https://bluettipower.eu/products/bluetti-folding-hand-truck, search-result summary only, accessed 2026-10-28).
  - Whether either fits the AC200L is unverified.
- The Elite 200 V2 costs the same $899 and weighs 53.4 lb (source: https://shop.bluettipower.com/ca/product/bluetti-elite-200-v2, search-result summary, accessed 2026-10-28). Details are in 3-rivals.md.

**(c) Page line.** "At 62.4 lb with two handles and no wheels, it is a two-person lift or a hand-truck job; it is built to be moved now and then, not carried every day."

**(d) When the objection wins.** Don't buy it if you:
- will carry it alone often, up stairs, or away from the vehicle at a campsite; or
- have any lifting limit.

A lighter or wheeled unit fits those buyers better.

## 2. "Is the fan loud? Is there a silent charging mode?"

**(a) Where raised.**
- OffGrid Benchmark's cons say "≤50 dB noise level is audible under heavy load" (source: https://www.offgridbenchmark.com/portable-power-stations/reviews/bluetti-ac200l/, updated 2026-04-08).
- Boondocking Magazine's cons say "Fans noticeable under high loads" (source: https://boondockingmagazine.com/bluetti-ac200l-portable-power-station-reviewbluetti-ac200l-review-real-world-off-grid-power-you-can-count-onbluetti-ac200l-portable-power-station-review/, 2025-10-08).
- Most reviews praise it as quiet. Trusted Reviews lists "Quiet and efficient, even at high loads" as a pro (source: https://www.trustedreviews.com/reviews/bluetti-ac200l, 2024-04-19).

**(b) Facts.**
- BLUETTI's spec says "50dB Max." (source: MAN spec table, accessed 2026-10-28). The CA page says "≤50dB" and quieter than the AC200MAX, with no measuring distance given (source: https://www.bluettipower.ca/pages/ac200l, accessed 2026-10-28).
- **Charging modes** (source: MAN §9.3, accessed 2026-10-28):
  - Standard: up to 1,200 W.
  - Turbo: up to 2,400 W.
  - Silent: up to 800 W, described as "a quiet, low-power operation for long battery life".
  - You can pick the mode on the unit's screen (setting P03), so the app is not needed (source: MAN §13, accessed 2026-10-28).
- **Measured dB.** I found no trustworthy independent measurement.
  - One site reports 44 dB at 1 m under full load (source: https://solargeneratorwholehouse.com/bluetti-ac200l-portable-power-station-review/, 2023-12-25). The same page also gets basic specs wrong ("248Wh" battery, "built-in 1400W AC charger"), so treat the reading as unreliable.
  - A "40 dB low / 48 dB high at 3 ft" figure surfaced in a search summary, but I could not find its source. Unverified.
  - No idle dB figure was found. Unverified.
- **Qualitative reports.**
  - Trusted Reviews says Silent charging "is a misnomer, as the fan will operate occasionally". It also says the unit stayed "quite quiet" even charging flat out, and was quieter than the Anker SOLIX F2000 at maximum output (source: Trusted Reviews URL above, 2024-04-19).
  - The Ambient found the fan noticeable at full tilt but quieter than the EcoFlow Delta 2 Max and the Anker F2000. A Silent-mode recharge took "just over three hours" (source: https://www.the-ambient.com/reviews/bluetti-ac200l-expandable-power-station-review/, 2024-09-17).
  - The Gadgeteer found the fans "barely audible" when charging in Standard mode (source: The Gadgeteer URL in §1, 2023-12-11).
  - Boondocking Magazine says the fans start above about 600 W (source: Boondocking URL above, 2025-10-08).
- **Turbo slows down when warm.** Trusted Reviews saw Turbo drop from 2,400 W to 1,200 W after about 15%. It held 2,400 W only after the unit cooled, and a full recharge took 75 minutes (source: Trusted Reviews URL above, 2024-04-19).

**(c) Page line.** "BLUETTI rates it at 50 dB max, and reviewers call it quiet for its size; an 800 W Silent charging mode cuts fan use, though the fan still runs at times."

**(d) When the objection wins.** Noise-sensitive buyers who will run heavy loads or Turbo-charge in a bedroom. Nobody has published a measured idle or Silent-mode level, so "silent" cannot be promised.

## 3. "Only 3,000 cycles when the Elite 200 V2 has 6,000 at the same price? How long will it really last, and is capacity loss covered?"

**(a) Where raised.**
- OffGrid Benchmark's cons list "3,000-cycle life, lower than some 4,000-cycle competitors" (source: https://www.offgridbenchmark.com/portable-power-stations/reviews/bluetti-ac200l/, updated 2026-04-08).
- BLUETTI's own store shows the 6,000-cycle Elite 200 V2 at the same $899 (our record; coupons.json cart test 2026-10-27, subtotal $899).

**(b) Facts.**
- **Ratings.** The AC200L is rated "3,000+ Cycles to 80% Original Capacity" (source: https://www.bluettipower.ca/pages/ac200l, accessed 2026-10-28). The Elite 200 V2 is rated "6,000+ cycles to 80% original capacity" (source: https://shop.bluettipower.com/ca/product/bluetti-elite-200-v2, search-result summary, accessed 2026-10-28). Both use the same 80% end point, so the comparison is like for like.
- **In years** (arithmetic): 3,000 full cycles last 8.2 years at one full cycle per day, and 57 years at one per week. An outage-only owner will not reach the cycle rating. Calendar aging is then the likely limit (inference).
- **Calendar aging.** BLUETTI publishes no calendar-life figure. Battery research on LFP/graphite cells finds that most capacity fade comes from lost lithium inventory. Higher temperature and higher state of charge both speed it up, and cycling at a lower average charge level extends life (source: Zsoldos et al., J. Electrochem. Soc. 171 080527, https://doi.org/10.1149/1945-7111/ad6cbd, published 2024-08-21). I did not find a reliable percent-per-year figure for 25 °C. Unverified.
- **Storage guidance.** BLUETTI says to store at 40 to 60% charge, powered off, and to "Fully cycle the product every 3 months" (source: MAN Warning 5 and §1.5, accessed 2026-10-28). The CA page says instead "Recharge to 80% Every 3-6 Months" (source: CA page, accessed 2026-10-28). The two conflict.
- **UPS tension.** Standard UPS mode keeps the battery charged from grid or solar (source: MAN §9.7). That means a high average charge level. Customized UPS mode lets you "set battery SoC limits" (source: MAN §9.7). Using it to cap the charge level should help, based on the research above (inference).
- **Warranty and capacity.**
  - BLUETTI's US warranty covers "defect in workmanship and material".
  - It excludes "Product wear and tear through the usage of time" and damage from "exposure to excessive heat, cold".
  - It states no capacity-retention percentage (source: https://www.bluettipower.com/pages/warranty-policy, accessed 2026-10-28).
  - BLUETTI does put a 70%-capacity guarantee on its B500 home battery in Australia. That is a different product (source: https://solarquotes.com.au/wp-content/uploads/2024/05/EP760-Warranty.pdf, search-result summary, 2024-05).
  - So normal fade is not covered. A failed cell within 5 years would be a defect (inference). How BLUETTI judges abnormal fade is unverified.
- **Not user-replaceable.** The built-in battery cannot be replaced: CA page FAQ Q16 says "No." Third-party expansion batteries are not supported: FAQ Q3 says "No." (source: CA page, accessed 2026-10-28).

**(c) Page line.** "Rated for 3,000 cycles to 80%, about 8 years of daily full cycles; the same-price Elite 200 V2 is rated for 6,000, and BLUETTI's warranty does not promise any capacity level."

**(d) When the objection wins.** Daily cyclers should take the 6,000-cycle Elite 200 V2 unless they need the AC200L's add-on batteries or TT-30 outlet. That means off-grid cabins, daily solar time-shifting and full-time vans. For outage backup, neither cycle rating is likely to be the limit.

## 4. "Should I wait for a sale? Wasn't it $749?"

**(a) Where raised.**
- Deal threads track it, for example Slickdeals (source: https://slickdeals.net/f/19036495-bluetti-ac200l-portable-power-station-2-400w-2-048wh-portable-power-759, 2025-12-30).
- One ChatGPT answer cited $749 from June 2026 (our record).

**(b) Facts. Dated price points:**

| Date | Price | Where | Source |
|---|---|---|---|
| 2024-10-02 | $1,199 ("returns to $1,199 low") | BLUETTI / Amazon | https://9to5toys.com/2024/10/02/bluettis-ac200l-2048wh-lifepo4-power-station-returns-to-1199-low-in-early-fall-prime-day-sale-save-800-more/ (headline only) |
| 2025-08-18 | $899, second time at the July 2025 Prime Day low; "normally" $1,599, with discounts "mostly" $975 to $999 | Amazon | https://9to5toys.com/2025/08/18/bluetti-ac200l-portable-power-station-899/ |
| 2025-12-30 | $799 sale, then $751 with BLUETTI's code BLUE6OFF | bluettipower.com | https://slickdeals.net/f/19036495-bluetti-ac200l-portable-power-station-2-400w-2-048wh-portable-power-759 |
| 2026-02-23 | $748.99 ("was $1600") | Amazon | https://www.techradar.com/pro/if-youre-looking-for-a-portable-power-station-to-handle-storm-outages-and-camping-trips-i-recommend-the-bluetti-ac200l-its-better-than-half-price-at-under-usd750 |
| 2026-06-23 | $699 lowest third-party new; $899 on 2026-08-04 | Amazon third-party | https://camelcamelcamel.com/product/B0CLGZB3L6 (search-result snippet only; the page is behind a Cloudflare challenge; unverified) |
| 2026-10-28 | $899, or $854.05 with AFF5OFF | bluettipower.com | ac200l.js and coupons.json (above) |

- **The $749 claim.** $749 was a real Amazon price on 2026-02-23. A June 2026 price of exactly $749 is unverified. A $699 third-party listing was recorded that month (snippet only).
- **Refurbished units** have been posted at $549 and $639 (Slickdeals thread titles https://slickdeals.net/f/18477460-refurbished-bluetti-ac200l-2400w-2048wh-portable-power-station-solar-generator-549 and https://slickdeals.net/f/19048951-refurbished-bluetti-ac200l-2400w-2048wh-portable-power-station-solar-generator-for-road-trip-639; dates unverified).
- **Black Friday 2026.** BLUETTI has not announced dates. Black Friday falls on 2026-11-27. In 2025, early prices went live Nov 12 and the main sale ran Nov 15 to Dec 3 (source: https://backuppowerhub.com/bluetti-black-friday-deals/, updated 2026-09-27, prices checked 2026-10-27/28). Today the US site banner reads "Halloween Sale | Free Gifts with $1,000+ Orders" (source: https://www.bluettipower.com/products/ac200l, accessed 2026-10-28).
- **Code stacking.**
  - AFF5OFF stacked on today's $899 sale price (coupons.json, 2026-10-27).
  - In the same run it took $0 off the Elite 300, so it does not apply to every product (coupons.json, 2026-10-27).
  - BLUETTI's own codes stacked on sale prices in 2025 (BLUETTI5OFF/BLUETTI6OFF per https://backuppowerhub.com/bluetti-black-friday-deals/, updated 2026-09-27; BLUE6OFF on $799 per the Slickdeals thread, 2025-12-30).
  - Whether AFF5OFF will stack with Black Friday prices is unverified.
- **Price protection.** "If the price decreases on the same platform within 30 days of purchase, we'll refund the difference. Excludes flash sales and special promotions." (source: https://bluettipower.com/pages/how-to-buy, accessed 2026-10-28). Thirty days from 2026-10-28 is 2026-11-27, Black Friday itself. Whether BLUETTI treats a Black Friday price as an excluded "special promotion" is unverified.

**(c) Page line.** "With the code it is $854.05, about $100 above its lowest dated prices ($751 at BLUETTI in Dec 2025, $748.99 at Amazon in Feb 2026); BLUETTI refunds a same-store price drop within 30 days, except flash sales and special promotions."

**(d) When the objection wins.** If you don't need it before late November and price is the deciding factor, waiting is reasonable. Sub-$800 prices have appeared around past holidays, but none are guaranteed. If you face storm or winter outage risk now, the likely saving is about $100 (inference from the table).

The phase-out cuts both ways (section A). Remaining stock may sell out before Black Friday. The Apex 200's Nov 4 launch price is the more useful thing to wait for.

## 5. "What does it cost to send back a 62 lb battery?"

**(a) Where raised.** I found no review or thread raising it directly. This objection is inferred from the policy, and it is real.

**(b) Facts.**
- **BLUETTI US policy** (source: https://www.bluettipower.com/policies/refund-policy, accessed 2026-10-28):
  - 30-day money-back for returns with no quality issue.
  - The item must be complete, unused and in its original package, and "we reserve the rights to refuse the return" for used products.
  - The customer pays "double shipping". With BLUETTI's RMA label, the return shipping cost is deducted from the refund. A self-paid return is the other option.
  - No restocking fee is listed.
  - A $25 intercept fee applies if you cancel after the order ships.
  - Refunds come within 14 business days after the warehouse receives the unit. After 30 days there is no full refund.
- Outbound shipping is free (source: https://bluettipower.com/pages/how-to-buy, accessed 2026-10-28). The dollar amount of the return deduction is not published. Unverified.
- **Shipping it yourself is hard.**
  - USPS caps mailed lithium-ion batteries at 100 Wh each (source: https://about.usps.com/postal-bulletin/2017/pb22474/html/updt_001.htm, effective 2017-08-17). The AC200L is 2,048 Wh.
  - UPS and FedEx terms for a consumer shipping a 2 kWh battery are unverified (UPS's hazmat page returned Access Denied).
  - In practice BLUETTI's RMA label is the realistic route (inference). Keep the box, since the policy requires the original package.
- **"Unused" limits real testing.** You cannot load-test it on your RV air conditioner or PC and count on a money-back return (inference from the policy text).
- **Other stores.**
  - BLUETTI's policy says purchases from distributors follow the distributor's policy (refund-policy URL above).
  - Amazon's return terms for this listing are unverified. A Slickdeals post quoted Amazon's "full refund or replacement within 30 days of delivery" for a BLUETTI product, but I saw that only as a search snippet.
  - I found no current US listing of the AC200L at Home Depot, Costco, Lowe's or Walmart (searches 2026-10-28; absence of a result, unverified). So their return windows are moot unless it is listed there.

**(c) Page line.** "BLUETTI takes returns within 30 days only if unused and in the original box, and deducts the return shipping cost from your refund; it does not publish what that costs."

**(d) When the objection wins.** If you are unsure whether it will run your specific device (RV AC, well pump, desktop PC) and you are not willing to pay unknown return freight, check the device's starting watts first or buy where you can return after testing.

## 6. "Will BLUETTI actually honor the warranty?"

**(a) Where raised.**
- Trustpilot 1 to 2 star reviews in Aug to Oct 2026 describe slow RMAs and warranty delays.
- BBB shows an F rating.
- A Slickdeals poster reported "71 days of zero warranty support" (search snippet only; unverified).

**(b) Facts.**
- **Terms** (source: https://www.bluettipower.com/pages/warranty-policy, accessed 2026-10-28):
  - Proof of purchase is a BLUETTI official-store order number, or an invoice showing the product, price and sales channel.
  - Exclusions include "Purchased from unauthorized resellers".
  - Coverage is limited to the country of purchase.
  - A replacement may be a refurbished model of equal value. It ships within 7 business days after BLUETTI receives and confirms the defective unit.
  - The replacement carries the remaining warranty or 30 days, whichever is greater.
  - Claims go to service@bluettipower.com.
  - The policy does not say who pays to ship the defective unit in, or how long repairs take. Unverified.
- **Length:** 60 months for the AC200L (source: https://www.bluettipower.com/pages/product-warranty-period, accessed 2026-10-28).
- **Third-party purchases.**
  - The policy does not define "authorized".
  - BLUETTI's product registration form offers Amazon, eBay, Walmart, ShopSolarKit, Home Depot and AliExpress as purchase channels (source: https://www.bluettipower.com/pages/register-product, accessed 2026-10-28).
  - Whether every marketplace seller counts as authorized is unverified.
- **Trustpilot** (source: https://www.trustpilot.com/review/bluettipower.com, accessed 2026-10-28):
  - 4.5/5 from 756 reviews; 79% 5-star and 7% 1-star.
  - The company "Hasn't replied to negative reviews".
  - The visible 1 to 2 star reviews (Sep to Oct 2026) describe dead-on-arrival units, days of waiting for return authorization, and late warranty replacements. None were for the AC200L.
- **BBB** (source: https://www.bbb.org/search?find_country=USA&find_text=bluetti, search-result data, accessed 2026-10-28):
  - "Bluetti Power Inc", 6185 S Valley View Blvd, Las Vegas NV, is rated F and is not a BBB member.
  - A separate "BLUETTI" listing in Denver, CO is rated D-. Whether it is the same company is unverified.
  - Complaint counts and reasons are unverified, because the profile pages are behind a bot check.
- BLUETTI Australia offers a 90-day express replacement that includes the AC200L (source: https://www.techradar.com/coupons/bluetti-au, search-result summary). Not verified for the US.

**(c) Page line.** "Five-year warranty when bought from BLUETTI's store with proof of purchase; replacements may be refurbished, and owner reports on claims are mixed (Trustpilot 4.5/5 from 756 reviews; BBB rating F)."

**(d) When the objection wins.**
- Buyers who need a guaranteed fast swap, because the unit is business-critical or medical.
- Buyers planning to buy from an unknown marketplace seller, since the warranty excludes unauthorized resellers.

## 7. "Is a 20 ms UPS safe for my PC, NAS, CPAP or sump pump?"

**(a) Where raised.**
- An owner asked how to set up UPS use for a pellet stove (source: https://www.thebarefootnomad.com/travel-tips/bluetti-ac200l-review-is-this-powerful-solar-generator-worth-it/, comment dated 2024-09-26).
- Homelab guides compare power stations with UPSes (source: https://computingforgeeks.com/power-station-vs-ups-homelab/, updated 2026-10-19).

**(b) Facts.**
- The switch-over time is "Switching time ≤20ms" (source: MAN spec table). CA page FAQ Q5 says "Within 20ms switching time" (source: CA page, accessed 2026-10-28).
- **BLUETTI's own exclusion.** The manual says BLUETTI is not liable for damage from "Usage of the product with devices that require a high-performance Uninterruptible Power Supply (UPS), including but not limited to data servers, workstations, medical equipment" (source: MAN §1.1, accessed 2026-10-28).
- **Desktop PCs.**
  - ATX 3.1 requires a power supply to hold up for 12 ms at full load, with 17 ms recommended at 80% load. ATX 3.0 required 17 ms (source: https://knowledge.seasonic.com/article/79-comparison-atx-3-0-vs-atx-3-1-standards, updated 2025-10-15).
  - 20 ms is longer than either spec guarantees. Computingforgeeks says 20 ms units may drop PCs that a faster unit would not (source: computingforgeeks URL above, 2026-10-19).
  - Many PCs may ride through at light load. That is unverified for any specific build, so test with a pulled plug.
- **NAS.**
  - The manual's port list shows no USB or serial UPS signaling port (source: MAN spec table). A NAS therefore cannot auto-shutdown when the battery runs low (inference).
  - Computingforgeeks recommends a line-interactive UPS for storage (source: computingforgeeks URL above, 2026-10-19).
  - An owner on OzBargain runs a small CyberPower UPS downstream of an AC200L to cover the gap (search snippet from https://www.ozbargain.com.au/node/889248; unverified).
- **CPAP.**
  - The manual's medical-equipment exclusion applies.
  - I found no test of any CPAP riding through a 20 ms gap. Unverified.
  - Running a CPAP directly from the battery is a separate question; see the runtime file. The unit has a 12 V/10 A car outlet (source: CA page).
- **Sump pump.**
  - The gap matters less than the motor's starting surge. On the US unit, the CA page lists "Surge Power: 4,800W" and Power Lifting 3,600 W (source: CA page).
  - The UK manual's overload table lists 2,520 to 3,000 W for 2 min, 3,000 to 3,600 W for 5 s, and over 3,600 W for 0.5 s (source: MAN spec table). The two conflict, so check the pump's starting watts.
- **UPS modes.** Four modes (Standard, Time Control, PV Priority, Customized) are chosen in the app (source: MAN §9.7).
- **Watch out:** TechRadar wrote that switch-over is "at or below 10ms" (source: TechRadar URL in §4, 2026-02-23). That contradicts BLUETTI's ≤20 ms.

**(c) Page line.** "UPS switch-over is up to 20 ms: fine for lights, fridges, routers and many PCs, but not guaranteed for desktops, and BLUETTI's manual excludes servers, workstations and medical equipment."

**(d) When the objection wins.** If you need zero interruption for a NAS, server or workstation, or for any life-sustaining medical device, buy a dedicated UPS, or put one between the AC200L and the device.

## 8. "Can I keep it in a cold garage or RV over winter? Does it self-heat?"

**(a) Where raised.** BLUETTI answers it in its own FAQ (Q10 on the CA page), which suggests buyers ask it often. I found no other dated thread for the AC200L.

**(b) Facts.**
- **Temperature limits.** Charging works from 0 to 40 °C (32 to 104 °F). Discharging works from -20 to 40 °C (-4 to 104 °F) (source: MAN spec table). The CA page FAQ Q10 says "avoid recharging it below freezing" (source: CA page, accessed 2026-10-28).
- Error E086 means "Charging temperature too low". A low-temperature alert shows when the inside of the unit drops below -20 °C (source: MAN §6 and §14).
- **No self-heating** is listed in the manual or spec table. That absence is what I found; that the unit has no heater at all is unverified.
- **Storage limits.**
  - The manual allows -20 to 45 °C for up to 1 month, -20 to 30 °C for up to 3 months, and -20 to 25 °C for up to 12 months (source: MAN spec table).
  - The CA page instead lists storage at 14 to 113 °F (-10 to 45 °C) (source: CA page). The low limits conflict; the safe reading is 14 °F.
- The warranty excludes damage from "exposure to excessive heat, cold" (source: https://www.bluettipower.com/pages/warranty-policy, accessed 2026-10-28).
- The manual says low temperature reduces run time (source: MAN Appx 1).

**(c) Page line.** "It can power devices down to -4 °F but will not recharge below 32 °F and lists no self-heating, so in a winter garage or RV it needs warming above freezing before it will charge."

**(d) When the objection wins.**
- Winter campers or RVers who must recharge from solar in sub-freezing conditions.
- Anyone storing it in an unheated space that drops below 14 °F.

They should look for a self-heating model (see 3-rivals.md).

## 9. "Is it a fire risk indoors? Is it UL listed? Any recalls?"

**(a) Where raised.** This is a general category worry after several power-station recalls (listed below). I found no AC200L-specific thread.

**(b) Facts.**
- The cells are lithium iron phosphate (LiFePO4) (source: MAN spec table).
- **Certifications.** BLUETTI lists "UL2743, UKCA, TELEC, RCM, FCC ID, CE, PSE, NTC" (source: CA page, accessed 2026-10-28). I did not confirm the UL listing in UL's own database (it needs a login, and the search budget ran out), so independent confirmation is unverified. No UL 1973 listing is claimed.
- **CPSC recalls.**
  - CPSC's recall API returns 0 recalls for "bluetti" in recall title, product name, manufacturer and description, and 0 for manufacturer "PowerOak" (source: https://www.saferproducts.gov/RestWebServices/Recall?format=json&RecallTitle=bluetti and the same endpoint with ProductName=, Manufacturer=, RecallDescription=, Manufacturer=PowerOak, accessed 2026-10-28).
  - The same API lists power-station recalls by other brands: Goal Zero YETI 3000X (2026-08-20), EcoFlow Delta Max 2000 (2025-10-09), Harbor Freight Predator 2000 (2025-07-03), HALO 1000 (2024-08-29) and Klein Tools (2023-12-21) (source: https://www.saferproducts.gov/RestWebServices/Recall?format=json&RecallTitle=power%20station, accessed 2026-10-28).
- A news search found no reported BLUETTI fires (2026-10-28). That is an absence of results, not proof.
- **Indoor use, per the manual** (source: MAN §1.2 and §1.5, accessed 2026-10-28):
  - Charge it in a well-ventilated area and do not restrict ventilation.
  - Store it away from flammable materials.
  - Use a dry-powder extinguisher.
  - Temperatures above 80 °C (176 °F) "may cause an explosion".
- It is not waterproof (source: CA page FAQ Q8).

**(c) Page line.** "LiFePO4 chemistry, BLUETTI lists UL 2743 certification, and CPSC's recall database shows no BLUETTI recalls as of Oct 28, 2026."

**(d) When the objection wins.**
- Buyers who need a third-party-confirmed UL listing before buying should check UL Product iQ themselves (not done here).
- Not for wet or unventilated locations.

## 10. "Do I need the app? Does it work offline? What does it collect?"

**(a) Where raised.**
- Trusted Reviews says its "AC ports, app, and screen could be a little easier to use" (source: https://www.trustedreviews.com/reviews/bluetti-ac200l, 2024-04-19).
- Notebookcheck notes that settings are spread across pages and there is no touchscreen (source: Notebookcheck URL in §1, 2024-08-05).
- OffGrid Benchmark calls the app "not as polished as EcoFlow's" (source: OffGrid Benchmark URL, updated 2026-04-08).

**(b) Facts.**
- **The app is optional.** Frequency, charging mode, Power Lifting, ECO, Bluetooth and Wi-Fi are all set with the unit's buttons (source: MAN §9 and §13). The Gadgeteer calls the app optional and notes that the unit's screen shows time-to-empty, which the app lacked (source: The Gadgeteer URL in §1, 2023-12-11).
- **App-only features:**
  - choosing among the four UPS modes (MAN §9.7);
  - separate AC and DC ECO toggles (MAN §9.5);
  - Grid Self-adaption mode (MAN §9.8);
  - firmware upgrades (CA page FAQ Q4).
  - The manual contradicts itself on Turbo: §7.1 says to enable it in the app, while §9.3 lists it as a screen setting.
- Raising max grid input above the default needs a password from customer service (MAN §9.9).
- The radios are 2.4 GHz Wi-Fi and Bluetooth 4.2 (MAN spec table).
- **Offline.** BLUETTI says Bluetooth Direct works "without an internet connection or account binding" (source: https://bluettipower.com/blogs/knowledge/bluetti-app-features-guide, 2026-10-06). Some owners on BLUETTI's old forum reported needing a login or internet in some app versions (search-result summary only; threads moved; unverified).
- **Data collected.** The BLUETTI app privacy policy covers name, email, country, address, phone number, device data, device location and phone model. Data "may be" stored outside your country (source: https://gw.bluettipower.com/agreements/en-US/privacy_policy.html, accessed 2026-10-28, no date shown).

**(c) Page line.** "Everything basic works from the front panel with no app; the app (Bluetooth or 2.4 GHz Wi-Fi) is needed only to pick a UPS mode or update firmware, and BLUETTI says Bluetooth control works offline without an account."

**(d) When the objection wins.** Buyers who will not install any app but need a non-default UPS mode or firmware updates.

## 11. "Can it run my RV air conditioner, or my whole RV, from the TT-30?"

**(a) Where raised.** BLUETTI forum thread "AC200L and 13.5K BTU air conditioner", 2024-07-29 to 2024-08-06 (source: https://community.bluettipower.com/t/ac200l-and-13-5k-btu-air-conditioner/32048, read via the web.archive.org copy because the forum moved).

**(b) Facts.**
- **Outlets.** It has 4 × 120 V/20 A outlets plus 1 × 120 V/30 A NEMA TT-30, with "2,400W In Total" (source: CA page). It is 120 V only; there is no 240 V split-phase (CA page FAQ Q7).
- **The 30 A label overstates it.** The TT-30 is a 30 A receptacle, but 2,400 W is 20 A at 120 V (arithmetic). The RV's 30 A panel can ask for more than the unit supplies, and an overload shuts the output off (E001, MAN §14).
- **Air conditioner draw.** A 13,500 BTU RV unit runs at about 1,500 W and can draw up to 2,800 W starting. Micro-Air says a soft starter cuts the starting surge by as much as 70% (source: https://www.microair.net/blogs/news/what-size-generator-do-you-need-to-run-an-rv-air-conditioner, 2025-04-07).
- **Owner reports** (forum thread above, 2024-07-29 to 2024-08-06):
  - One owner's 13.5k BTU unit on the 30 A port "faulted almost immediately". It worked after starting the fan first and the compressor second.
  - Others recommend a soft start, and turning off the RV's converter/charger breaker so it doesn't load the unit.
  - One owner runs a 12k BTU boat AC for about 90 minutes per charge.
- Runtime numbers are in the runtime file.

**(c) Page line.** "It can power a 30-amp RV's 120 V circuits up to 2,400 W total and can run one RV air conditioner for roughly an hour and a half, usually only with a soft starter or by starting the fan first; it is not a replacement for shore power."

**(d) When the objection wins.** RVers who want to boondock with air conditioning overnight, or who expect to run the AC plus a microwave or water heater at once. They need far more battery plus charging, or a generator.

## 12. "Who is BLUETTI? Will they be around to service this?"

**(a) Where raised.** I found no review raising it directly. It is inferred from the BBB grade and Trustpilot complaints.

**(b) Facts.**
- The manual's copyright holder is Shenzhen PowerOak Newener Co., Ltd. (source: MAN p.3).
- **BLUETTI's own timeline** (source: https://www.bluettipower.com/pages/about-us, accessed 2026-10-28):
  - R&D team formed 2009.
  - First lithium home-backup storage station 2011.
  - PS10B 2013.
  - Own factory 2017.
  - "BLUETTI Power inc Founded" 2021.
- Wikipedia says BLUETTI was "established in 2009 in Shenzhen, China" and had subsidiaries in the US, UK, Japan and Germany as of 2024. The article carries a maintenance tag for leaning on affiliated sources (source: https://en.wikipedia.org/wiki/Bluetti, accessed 2026-10-28).
- **US contact:** +1 909-570-0909, Mon to Sat 6:00 to 17:00 PDT, and service@bluettipower.com (source: https://www.bluettipower.com/policies/refund-policy and https://support.bluettipower.com/en-us/products/ac200l-power-station, accessed 2026-10-28). BBB lists Bluetti Power Inc at a Las Vegas address (BBB URL in §6).
- Warranty service is "Repaired by BLUETTI service center" or replaced (source: warranty-policy URL). A US service-center location is unverified.
- **Debunk:** A retailer page called BLUETTI "a subsidiary of Anker Innovations" (industry-electronics.com, search snippet). That conflicts with the manual and Wikipedia; treat it as false.
- The AC200L has been on BLUETTI's US store since 2023-10-31 (ac200l.js). It is now being phased out for the Apex 200 (section A). BLUETTI's discontinued-models page still names it as the AC200P's replacement, but that does not mean it is current.

**(c) Page line.** "BLUETTI is a Shenzhen brand (PowerOak) with roots in 2009 and a US company since 2021; support is by phone and email with mail-in repair or replacement."

**(d) When the objection wins.** Buyers who want walk-in retail service or local repair.

## 13. Added: "Can it back up my house panel?"

**(a) Where raised.** Inferred from the "home backup" positioning. BLUETTI's own FAQ answers the 240 V question (CA page FAQ Q7).

**(b) Facts.**
- The manual says "The unit is for off-grid use only. Do not connect its AC output to the grid." It repeats this as a "Danger" note (source: MAN Warning 4 and §3).
- It is 120 V only, with no split-phase bonding ("No. Need 240V power source", CA page spec and FAQ Q7). So it cannot run 240 V well pumps, dryers or central AC.
- Whether BLUETTI approves feeding a home circuit through an electrician-installed inlet and transfer switch is unverified.

**(c) Page line.** "A 120 V plug-in backup for individual appliances; BLUETTI says not to connect its output to the grid, and it cannot run 240 V loads."

**(d) When the objection wins.** Anyone who wants whole-home or 240 V backup.

## 14. Added: "Will it drain sitting in a closet?"

**(b) Facts.**
- Self-consumption is "approximately 12W" (source: MAN Appx 1). That is about 288 Wh a day if left on, roughly 14% of 2,048 Wh (arithmetic).
- AC and DC ECO auto-off are on by default (MAN §9.5).
- For storage, BLUETTI says to charge to 40 to 60%, power off, and cycle every 3 months (MAN §1.5).

**(c) Page line.** "Left on with nothing plugged in it uses about 12 W, around 14% of the battery a day, so switch it off or keep it on the charger, and top it up every few months in storage."

**(d) When the objection wins.** Buyers who want to forget it in a closet for a year. It needs attention about every 3 months.

## 15. Added: "Is it outdated next to the Elite 200 V2?"

**(b) Facts.**
- It has been on sale since late 2023 (ac200l.js) and is now being phased out; see section A for the Apex 200.
- At the same $899, BLUETTI's Elite 200 V2 is rated for 6,000 cycles and weighs 53.4 lb (source: Elite 200 V2 URL in §3, search-result summary). It cannot be expanded with extra batteries (our record).
- The AC200L's case rests on expansion batteries and the TT-30 outlet. Full comparison is in 3-rivals.md.

**(c) Page line.** "The same-price Elite 200 V2 is lighter with double the cycle rating, so pick the AC200L only when you want add-on batteries or the TT-30 RV outlet, and check the Apex 200 first."

**(d) When the objection wins.**
- Buyers who will never add a battery or plug in an RV.
- Buyers who want add-on batteries or the TT-30 and can wait until Nov 4 for the Apex 200 (section A).

## 16. Minor: outlet layout

Trusted Reviews' cons say "Top mains power sockets are compromised" because the top two sockets are inverted (source: https://www.trustedreviews.com/reviews/bluetti-ac200l, 2024-04-19). Notebookcheck found that the silicone flaps can stop plugs seating fully (source: Notebookcheck URL, 2024-08-05). Both reviewed UK units. Whether the US outlet panel has the same problem is unverified.

---

## Misinformation watch (claims an AI assistant may repeat)

| Claim | Source | Correct per BLUETTI |
|---|---|---|
| UPS switch-over "at or below 10ms" | TechRadar, 2026-02-23 (URL in §4) | ≤20 ms (MAN spec; CA page FAQ Q5) |
| "built-in wireless charging pad"; "Warranty 6 years" | https://powerstation.pro/articles/bluetti-ac200l-review, 2026-02-26 | The Gadgeteer lists "No wireless charging pad" as a con (2023-12-11); warranty is 60 months (product-warranty-period) |
| "No Wi-Fi or expandable capacity option" | Boondocking Magazine, 2025-10-08 (URL in §2) | Wi-Fi 2.4 GHz and Bluetooth 4.2; expandable (MAN spec and §10) |
| "248Wh" battery, "1400W AC charger" | solargeneratorwholehouse.com, 2023-12-25 | 2,048 Wh; 2,400 W Turbo AC charging (MAN) |
| Max solar 500 W in body text (1,200 W in its own spec box) | OffGrid Benchmark, updated 2026-04-08 | 1,200 W (MAN §7.2) |
| "subsidiary of Anker Innovations" | industry-electronics.com (search snippet) | PowerOak / Shenzhen (MAN; Wikipedia) |
| "Discontinued" | ChatGPT answer (our record) | Essentially right: BLUETTI's indexed listing says Discontinued and OutOfStock. The same SKU still sells at $899 on a noindex page (section A). |
| "$749" as a current price | ChatGPT answer (our record) | $899 today; $748.99 was an Amazon price on 2026-02-23 |

## Open questions / couldn't verify

1. **Noise.** No trustworthy measured dB figure at idle, while charging, or under load. The only figure (44 dB at 1 m, full load) comes from a site with wrong specs. The "40/48 dB at 3 ft" figure has no traceable source.
2. **Return cost.** The dollar amount BLUETTI deducts for an RMA return of a 62 lb lithium unit. UPS and FedEx consumer rules for shipping a 2 kWh battery (UPS page returned Access Denied).
3. **Amazon.** Current AC200L availability and seller (first-party vs third-party), return window and return shipping fees. The camelcamelcamel history (the $699 low on 2026-06-23 and $899 on 2026-08-04) is from a search snippet only; the page is behind a bot check.
4. **June 2026 at $749.** Unverified. $749 is verified only for 2026-02-23 (Amazon, TechRadar).
5. **Black Friday 2026.** Dates, and whether AFF5OFF stacks with Black Friday prices. Whether the 30-day price guarantee covers Black Friday prices, given its "special promotions" exclusion.
6. **UL 2743.** Not confirmed in UL Product iQ (login required; search budget exhausted). FCC ID not looked up (fccid.io returned 403).
7. **Self-heating.** None is listed. That it definitely has none is unverified.
8. **Storage temperature.** The manual (-20 °C) and CA page (-10 °C / 14 °F) conflict on the low limit. Storage charge advice also conflicts: the manual says 40 to 60% and cycle every 3 months; the CA page says recharge to 80% every 3 to 6 months.
9. **Warranty details.**
   - Who pays shipping on warranty claims, and repair turnaround.
   - Whether Amazon or other marketplace purchases count as "authorized".
   - How abnormal capacity fade is judged.
   - Whether the Australian 90-day express replacement exists in the US.
10. **BBB.** Complaint count and themes (profile pages behind a bot check). Whether the Denver "BLUETTI" D- listing is the same company.
11. **Reddit.** No Reddit threads were retrieved for any objection.
12. **US surge and overload.** The CA page says "Surge Power: 4,800W". The UK manual's overload table tops out at 3,600 W for 5 s and over 3,600 W for 0.5 s. The specs/runtime files should settle the US figure.
13. **Expansion batteries.** The CA page and manual list up to 2 × B210, 1 × B230 or 2 × B300. Our record says B300K/B500K. The specs file should reconcile this.
14. **Trolley fit.** Whether BLUETTI's trolleys fit the AC200L.
15. **CPAP and desktop PC ride-through** on a 20 ms switch-over for specific models. No tests found.
16. **App offline.** Whether Bluetooth-only use works without ever creating an account in the current app version. BLUETTI says yes; owner reports were seen only as search snippets.
17. **US service center.** Its location is unverified.
18. **Apex 200.** Price, cycle rating, UPS switch-over time, warranty length and self-heating are not published.
    - Launch date: BLUETTI's page says Nov 4, 2026; the coordinator was told Nov 5.
    - "Early access since Oct 21" is not visible on the page.
    - Whether it uses the same CA90 cable as the AC200L for B300K/B500K is unknown.
19. **AC200L end of run.**
    - Whether the remaining stock gets a clearance price or simply sells out.
    - When BLUETTI adds the AC200L to its discontinued-models list.
    - Whether the 30-day price guarantee covers a launch-week or Black Friday markdown.
    - I did not re-check the AC200L bundles; I am relying on the coordinator for "all bundles unavailable".
20. **Search cut-off.** The web-search budget was exhausted before the discontinuation correction arrived. Section A rests only on BLUETTI pages fetched directly, with no third-party coverage of the Apex 200 launch.
