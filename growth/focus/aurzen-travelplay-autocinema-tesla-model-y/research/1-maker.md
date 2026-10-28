# Aurzen TravelPlay AutoCinema Screen (Tesla Model Y): maker facts

Angle 1 of 5. Researched 2026-10-28 (all fetches between 01:20 and 02:00 PDT).

## Method

- Pulled the live Shopify JSON (`.js` and `.json`) and the full HTML of the product page, then extracted all visible text, the spec table, the FAQ, the safety notes and every image alt text. Same for the ZIP, ZIP "US Version", ZIP Pro, ZIP Pro landing page, MagPlay, and the full `products.json` catalog (35 products).
- The page's two manual links: the "English" link points to the wrong PDF (an EAZZE D1R Roku projector manual). The Spanish link is the real TravelPlay manual. I found the real English manual at an unlinked CDN URL by trying likely filenames, and confirmed it matches the Spanish one. Both PDFs are scanned images with no text layer, so I rendered them page by page and read them. The QR code in the manual resolves (via qrs.ly) back to the product page.
- Read Aurzen's warranty, return/refund, shipping, price-match, extend-warranty, about and terms pages, plus its blog feed (30 most recent posts).
- Price history: Wayback Machine CDX (no captures of the product URL; one capture of the screens collection on 2026-08-24).
- Amazon: four search queries via curl (not blocked) plus one product page.
- Web searches for press coverage (PR Newswire, Teslarati, Not a Tesla App, Drive Tesla Canada) and for company background.
- I did not open a cart and did not re-test CJ10.

Abbreviations for the sources used most:
- **PAGE** = https://aurzen.com/products/aurzen-travelplay-autocinema-screen-for-tesla-model-y (no date shown; accessed 2026-10-28)
- **JS** = https://aurzen.com/products/aurzen-travelplay-autocinema-screen-for-tesla-model-y.js (accessed 2026-10-28)
- **MAN-EN** = https://cdn.shopify.com/s/files/1/0720/5109/7892/files/Aurzen_TravelPlay_AutoCinema_Screen_User_Manual.pdf (undated; accessed 2026-10-28)
- **MAN-ES** = https://cdn.shopify.com/s/files/1/0720/5109/7892/files/Aurzen_Pantalla_de_AutoCinema_TravelPlay_User_Manual.pdf (undated; accessed 2026-10-28)
- **WARR** = https://aurzen.com/pages/warranty-policy (accessed 2026-10-28)
- **RET** = https://aurzen.com/pages/return-refund-policy (accessed 2026-10-28)

## Findings that contradict or extend our record

1. **Model-year range for the 2020-2024 fallback differs by language.** The English page and English manual say roof mode fits "Tesla Model Y 2020-2024". The Spanish manual says "Tesla Model Y 2022-2024". (source: PAGE, accessed 2026-10-28; MAN-EN p.3; MAN-ES p.3, accessed 2026-10-28.) Our record says 2020-2024, which matches the English sources. I can't tell which is right.
2. **The English manual link on the product page is broken.** It points to `Aurzen_EAZZE_D1R_Roku_TV_Projector-User-Manual-EN_V1.01.pdf?...&ref=DANNYBLACK`, a projector manual. The real English TravelPlay manual is at MAN-EN, which the page does not link. (source: PAGE HTML, accessed 2026-10-28.) This is worth a line on our page: shoppers who click "English" get the wrong document.
3. **Model number PJ005PS, SKU AU-PJ005PS-UNWH0.** (source: MAN-EN p.3; JS, accessed 2026-10-28.)
4. **Folded sizes: front 420 × 470 mm, rear 500 × 500 mm.** Not in our record. (source: MAN-EN p.3, accessed 2026-10-28.)
5. **The TravelPlay page itself names only the ZIP** ("Aurzen ZIP or other compatible portable projectors"). It does not name the ZIP Pro. The ZIP Pro pages do cross-sell TravelPlay. (source: PAGE; https://aurzen.com/pages/aurzen-zip-pro-tri-fold-full-hd-portable-projector, accessed 2026-10-28.)
6. **The MagPlay mount is still unavailable in the US store** today, as on 2026-10-25. The manual's rear-seat mode depends on it. Aurzen's newer **MagPlay Pro (for the ZIP Pro)** shows "Coming Soon" on aurzen.com but is listed on Amazon at $32.99, sold by Aurzen Store. (Details in section 3.)
7. **Rear-seat mode uses only the rear panel**, clipped to the front center armrest/storage box with both front seats pushed fully forward. It does not use both panels. (source: MAN-EN p.2, accessed 2026-10-28.)
8. **No price below $119.99 seen.** A Wayback capture of the screens collection on 2026-08-24, a week after publication, already shows $119.99 with a $129.99 compare-at. (source: https://web.archive.org/web/20260824020743/https://aurzen.com/collections/projector-screens, captured 2026-08-24.)
9. **No Amazon listing exists** for TravelPlay (four searches, 2026-10-28). See section 5.
10. **Shipping exclusions:** Aurzen does not ship to Alaska, Hawaii, Puerto Rico, Rhode Island, US territories or APO/FPO addresses. (source: https://aurzen.com/pages/shipping-policy, accessed 2026-10-28.)
11. **Cancellation fee:** canceling more than 24 hours after ordering but before delivery costs 2.6% (credit card) or 3.6% (PayPal). (source: RET, accessed 2026-10-28.)

No contradiction on price ($119.99, compare-at $129.99, in stock), panel sizes, 1 kg net weight, modes, clips, warranty length or the 30-day return terms. The Shopify variant weight is 2,000 g. That is the shipping weight; the page states 1 kg / 2.2 lbs net. (source: JS; PAGE, accessed 2026-10-28.)

## 1. Product page and manual details

### Live listing (verified today)
- Price $119.99, compare-at $129.99 ("Save 8%"), `available: true`, schema.org `InStock`. One variant ("Default Title"). (source: JS; PAGE JSON-LD, accessed 2026-10-28)
- Shopify product created 2026-08-06, published 2026-08-17. (source: JS, accessed 2026-10-28)
- Product type "Projection Screens". (source: JS, accessed 2026-10-28)
- "Note: This product is available in the U.S. only." (source: PAGE, accessed 2026-10-28)
- No review rating in the page's structured data. A reviews tab exists, filled in by a JavaScript app; I did not read it. (source: PAGE HTML, accessed 2026-10-28)

### Spec table (verbatim fields from PAGE, accessed 2026-10-28)
- Product Type: 2-in-1 Car Projector Screen & Sunshade
- Vehicle Compatibility: Tesla Model Y Refresh 2025–2026
- Screen Panels: Front Panel + Rear Panel
- Front Panel Size: 1098 × 590 mm; Rear Panel Size: 1031 × 685 mm; Approx. Screen Size: 47" + 50"
- Material: Steel, Polyester-Spandex Blend. The description says "flexible steel frame and polyester-spandex blend"; the manual says the screens "contain flexible steel rings".
- Installation Method: Tool-Free Clip-In Installation
- Net Weight: 1 kg / 2.2 lbs
- In the Box: Front Screen × 1, Rear Screen × 1, Carry Bag × 1, Side Clips × 8, Center Connect Clips × 2, Side Connect Clips × 2, User Manual × 1 (12 clips in total; the manual's box diagram matches)
- Recommended Use: Parked Vehicle Viewing, Camping, Tailgate Movie Nights, Portable Projection
- Safety Note: "Use only when the vehicle is parked. Do not use while driving."
- Page badges: "Fast, Free Delivery", "30-Day Money-Back Guarantee", "1-Year Warranty", "Lifetime Customer Support". Shipping tip: "Shipping begins within 1-3 days"; US 3-7 business days.

My arithmetic, not an Aurzen claim: the rectangles measure 49.1" (front) and 48.7" (rear) diagonally. The largest 16:9 image that fits is about 47.4" on the front panel and 46.6" on the rear panel. Aurzen's "47" + 50"" doesn't map cleanly onto either set of numbers.

### Surface, gain, sunshade claims
- Two sides. White side: "The white projection surface provides a clean viewing area for portable projector use." Silver side: "the silver-coated side helps block sunlight and reduce ambient light interference when placed along the panoramic roof". FAQ: "This makes it useful for both daytime shade and parked-car entertainment." (source: PAGE, accessed 2026-10-28)
- In sky-roof mode, "The silver side must face upward" (toward the glass). (source: MAN-EN p.2, accessed 2026-10-28)
- **Screen gain or reflectivity: not stated** anywhere on the page or in the manual.
- **Heat or UV blocking numbers (percent, degrees): not stated.** The only claim is the qualitative "helps block sunlight". (source: PAGE; MAN-EN, accessed 2026-10-28)
- FAQ: "For the best outdoor viewing experience, use the screen after sunset or in a low-light environment." (source: PAGE, accessed 2026-10-28)

### Modes: which panels, how mounted (source: MAN-EN p.2, accessed 2026-10-28, unless noted)
General steps: take out the 2 screens and 12 clips; identify the screens by their markings ("F: Front Screen; R: Rear Screen"); "For your safety, only use when the vehicle is stationary."

| Mode (manual name / page name) | Panels | Mounting per manual | Projector placement (manual text or drawing) |
|---|---|---|---|
| Starlight Roof Movie / Sky-Roof Theater | Front + rear, joined | "Align the screen frame with the mounting slots on the inner rim of the sunroof. The silver side must face upward." Secure both screens with the clips. Diagram: 4 side clips (A) on the front screen (2 top, 2 sides), 4 on the rear (2 sides, 2 at the bottom notch), joined by 2 center connect clips (B) and 2 side connect clips (C). "After installation, recline the rear seats to enjoy movies." | Drawing shows a viewer lying in the back with the projector on the floor, aimed up at the roof. |
| Rear-Seat Movie / Rear-Seat Theater | Rear (R) only | "Move the front seats (driver and passenger) fully forward." "Take out the rear screen (R) and clip it to the center armrest/storage box." | "Attach the MagPlay to the rear sunroof, then mount the ZIP projector onto the MagPlay." Tip: "attach MagPlay to the center of the rear sunroof." The drawing shows the projector hanging from the rear glass, aimed forward at the screen between the front seats. |
| Tailgate Camp Movie / Tailgate Theater | Rear (R) only | "Take out the rear screen (R) and attach it to the trunk for outdoor projection." Which clips go where is not specified. | Drawing shows the screen in the open liftgate area and the projector on a small stand outside, viewers in camp chairs. |

- Before installation: "remove the sunshade from the vehicle's sunroof." (source: MAN-EN p.1, accessed 2026-10-28.) This implies an owner's existing roof shade comes out first.
- On 2020-2024 cars the manual shows a drawing labeled "Rear screen on the Tesla Model Y 2020-2024" with a gap at the bottom edge. (source: MAN-EN p.3, accessed 2026-10-28)
- **Claimed setup time: none.** Aurzen says "Quick, Secure Clip-In Installation" and gives no minutes. (source: PAGE; MAN-EN, accessed 2026-10-28.) The "under a minute" figure in CES coverage is about the ZIP Cyber Edition demo, not TravelPlay (source: https://the-gadgeteer.com/2026/01/12/aurzen-zip-cyber-edition-brings-tri-fold-portable-projection-to-ev-road-trips-at-ces-2026/, 2026-01-12).

### Care, crease removal, storage
- "The screens contain flexible steel rings. Please unfold or fold them slowly to avoid injury." (source: MAN-EN p.1 and p.3, accessed 2026-10-28)
- Creases from shipping: hair dryer on hot, "2–3 cm from the crease on the silver side of the screen for 1–2 minutes". Don't hold it on one spot; don't do it while the screen is installed or hanging; let it cool about 15 minutes. (source: MAN-EN p.1, accessed 2026-10-28)
- Storage: remove all clips and fold each screen in four steps (twist-fold) into the carry bag. "If folding is difficult, use another part of your body (such as your leg)". (source: MAN-EN p.3, accessed 2026-10-28)
- Safety notes: improper installation "may cause the screen to fall"; "Ensure all clips are fully inserted into the inner rim"; "Do not scratch the screen with sharp objects, as this may damage the coating"; "Keep the white projection surface clean"; with MagPlay, keep the suction surface clean ("Dust, oil, or scratches may affect adhesion"). (source: PAGE; MAN-EN p.3, accessed 2026-10-28)
- No washing instructions. (source: PAGE; MAN-EN, accessed 2026-10-28)

### Image alt text (all 7 product images; source: JS media, accessed 2026-10-28)
"Aurzen TravelPlay portable screen, white, two-panel, for Tesla Model Y"; "...dual-panel car projector screen for Tesla Model Y"; "...with 2-in-1 projector screen and sunshade setup"; "2-in-1 projector screen and sunshade for Tesla Model Y panoramic roof viewing"; "Detachable front and rear projector screens for in-car and outdoor projection with Tesla Model Y"; "Quick secure clip-in installation..."; "Three viewing modes ... rear-seat, tailgate, and sky-roof theater setups". The featured image was replaced around 2026-10-20 (its `v=` timestamp is 1792564477, which is 2026-10-20 23:34 PDT); the others date from 2026-08-16.

### Manual PDFs
- English (unlinked): MAN-EN, 3 pages, scanned images.
- Spanish (linked): MAN-ES, 3 pages.
- Broken "English" link on the page: https://cdn.shopify.com/s/files/1/0720/5109/7892/files/Aurzen_EAZZE_D1R_Roku_TV_Projector-User-Manual-EN_V1.01.pdf (wrong product). The de/fr/it/pt/es versions of the page carry the same two links.
- Manual contact block: support@aurzen.com (North America/UK), support.eu@aurzen.com, support.jp@aurzen.com, +1-667-218-4830, Mon-Fri 9:00-17:00 EST. (source: MAN-EN p.3, accessed 2026-10-28)

## 2. Fit

- Page: "designed for Tesla Model Y Refresh 2025–2026". FAQ: "Fit may vary on earlier Tesla Model Y versions due to differences in vehicle design and interior layout." (source: PAGE, accessed 2026-10-28)
- Safety notes and the English manual: "Travelplay is designed for the Tesla Model Y Juniper 2025-2026. Due to model changes, it is compatible with the overall dimensions of the Tesla Model Y 2020-2024 in Starlight Roof Movie mode, but the rear screen cannot fully cover the window." (source: PAGE; MAN-EN p.3, accessed 2026-10-28)
- The Spanish manual says "2022-2024" instead of 2020-2024. (source: MAN-ES p.3, accessed 2026-10-28)
- **Trims (Performance, Long Range, Premium, Standard) and the Model Y L six-seater: Aurzen says nothing.** No page, manual or FAQ text mentions them. (source: PAGE; MAN-EN; site search for "tesla", https://aurzen.com/search/suggest.json?q=tesla, accessed 2026-10-28)
- Context from third parties, not Aurzen (fit is inference, unverified):
  - The Model Y Standard keeps a roof glass panel but hides it behind a fabric headliner, so it can't be seen from inside (source: https://www.motor1.com/news/775057/tesla-model-y-hides-glass-roof/, 2025-10-08). Every mode in the manual depends on the glass roof's inner rim (sky-roof) or a MagPlay on the rear glass (rear-seat), so the Standard is probably a poor fit. Unverified: Aurzen doesn't address it.
  - The Model Y L (six seats, longer wheelbase) launched in the US at $61,990 (source: https://m.arenaev.com/tesla_model_y_l_sixseater_officially_launches_in_the_us-news-6035.php, 2026-07-03). Whether its roof opening matches the regular Model Y: unverified.
- **Other vehicles:** the US catalog has exactly one TravelPlay product (Model Y). There's no Model 3, Cybertruck or other-car version; site search for "travelplay" and "tesla" returns only this product. (source: https://aurzen.com/products.json, 35 products; https://aurzen.com/search/suggest.json?q=travelplay, accessed 2026-10-28)

## 3. Recommended projectors, MagPlay, bundles (all live .js, accessed 2026-10-28)

| Item | Live price (compare-at) | Stock (US) | Key specs | Source |
|---|---|---|---|---|
| ZIP Tri-Fold (main listing), Titanium Gold / White | $259.99 ($499.99) | available | 720p native, 100 ANSI lumens, throw ratio 1.09:1, 20"-120", 5000 mAh battery, up to 1.5 h, 280 g, BT 5.4 incl. "Tesla audio systems", warranty "1 year included, +1 year with registration" | https://aurzen.com/products/aurzen-zip-tri-fold-portable-projector(.js) |
| ZIP Tri-Fold, Dark Gray | $439.99 ($499.99) | available | same | same |
| ZIP Tri-Fold, Cyber Edition | $499.99 | **unavailable in US** | same | same |
| ZIP Tri-Fold "US Version" listing, Titanium Gold / White (same SKUs as above) | **$199.99** ($499.99); Travel Bundle $239.99; Streaming Bundle $329.99; Streaming Travel Bundle $369.99 | available | same | https://aurzen.com/products/aurzen-zip-tri-fold-portable-mini-projector-usa.js |
| ZIP Pro | $579.99 ($629.99); + CastPlay Pro $649.99; Basquiat bundle $679.99 | **pre-order**; "Estimated Dispatch from October 30" (Basquiat from Nov 10) | 1080p native, 200 lm, throw ratio 1.2:1, projection distance 0.5-3 m, 38 Wh (10,000 mAh), up to 2.5 h (ECO), 586 g, "Car BT Mode is currently available for compatible Tesla audio systems only", "1+1 Year Warranty" | https://aurzen.com/products/aurzen-zip-pro-full-hd-portable-projector(.js); https://aurzen.com/pages/aurzen-zip-pro-tri-fold-full-hd-portable-projector |
| MagPlay Dual-Sided Mount (for ZIP) | $39.99 | **US variant `available: false`** (EU and UK true) | vacuum-suction plus N52 magnets, 56 g, 360°, fits ZIP and MagSafe iPhones | https://aurzen.com/products/magplay-dual-sided-mount-for-zip-projector.js |
| MagPlay Pro Vacuum Mount (for ZIP Pro) | "Coming Soon" on aurzen.com; **$32.99 on Amazon**, ASIN B0HK41P8ZW, "Ships from Amazon, Sold by Aurzen Store" | aurzen.com: not listed. Amazon: stock line not parsed (unverified). | not checked | https://aurzen.com/pages/aurzen-zip-pro-tri-fold-full-hd-portable-projector; https://www.amazon.com/dp/B0HK41P8ZW |

- The same ZIP SKU (AU-PJ-ZP001M-USGD0) sells for $199.99 on the "US Version" page and $259.99 on the main ZIP page. Both were live today.
- The ZIP Pro page: "Model Y-Ready AutoCinema Experience. Connect ZIP Pro to compatible Model Y speakers and pair it with the Aurzen TravelPlay AutoCinema Screen for immersive big-screen projection while parked". (source: ZIP Pro landing page, accessed 2026-10-28)
- The ZIP page calls TravelPlay "Your ZIP AutoCinema Setup ... Designed to pair with Aurzen ZIP". (source: https://aurzen.com/products/aurzen-zip-tri-fold-portable-projector, accessed 2026-10-28)
- **No screen-plus-projector bundle exists.** Neither the ZIP nor the ZIP Pro bundles, nor any other product in the catalog, include TravelPlay. (source: https://aurzen.com/products.json, accessed 2026-10-28)
- BOOM or EAZZE (D1) projectors are not linked or mentioned on the TravelPlay page. (source: PAGE, accessed 2026-10-28)
- My arithmetic, not Aurzen's: to fill the rear panel's width with a 16:9 image, the lens has to sit about 1.12 m away for the ZIP (1.09 × 1.031 m) or about 1.24 m for the ZIP Pro (1.2 × 1.031 m).

## 4. Warranty and returns (exact terms)

Warranty (source: WARR, accessed 2026-10-28):
- "Aurzen-branded hardware products come with a warranty ranging from 1 year to 2 years." The timeline table lists "All Aurzen Accessories 12 Mo." TravelPlay is not named; the product page badge says "1-Year Warranty".
- "Please register your product at 'Extend Warranty' immediately after receiving it to enjoy an additional year of coverage." The extend-warranty form accepts aurzen.com, Amazon, Best Buy, TikTok Shop, Mercado Libre and Walmart orders (source: https://aurzen.com/pages/extend-warranty, accessed 2026-10-28). Whether the extra year applies to accessories like TravelPlay is not stated (unverified).
- Not covered: "loss, theft, deliberate damage, or cosmetic damage"; misuse including "falls, using/storing product in extreme temperatures". The temperature clause matters for a screen left in a hot car. Also void outside the country of purchase.
- Defect remedy: "replaced with a factory refurbished model of equal value when available, otherwise a new item," or a partial refund based on usage time.
- Warranty claims "expire 90 days after opening a warranty claim."

Returns (sources: WARR and RET, accessed 2026-10-28):
- WARR: "Undamaged products can be returned for a full refund, regardless of the reason, within 30 days of purchase." Returns must include all accessories. "For non-quality related warranty claims, buyer is responsible for shipping costs." Only for aurzen.com orders. Bundle discounts mean bundles can only be refunded whole.
- RET: "If you receive a product with a quality issue, you are eligible for a full refund or exchange within 30 days of delivery." So the no-reason window counts from purchase (WARR) and the defect window from delivery (RET). The two pages use different clocks.
- Cancellation: free within 24 hours of ordering. After that, before delivery: 2.6% fee (card) or 3.6% (PayPal). "Orders cannot be canceled more than 30 days after they are shipped."
- Refund timing: about 3-7 business days (WARR) or about 7 business days (RET), to the original payment method.
- Damaged or lost package: report within 7 days of delivery or of the expected delivery date. (source: WARR, accessed 2026-10-28)
- Price guarantee: within 30 days of an aurzen.com order, Aurzen refunds the difference if a qualifying retailer sells the identical item for less. Exclusions include coupon or code prices and "Affiliate promotions". (source: https://aurzen.com/pages/price-match, accessed 2026-10-28)
- Shipping is free on all orders, via DHL, USPS, UPS or FedEx from US warehouses, 3-7 business days. No delivery to AK, HI, PR, RI, US territories or APO/FPO addresses. (source: https://aurzen.com/pages/shipping-policy, accessed 2026-10-28)

## 5. Price history and other retailers

- Published 2026-08-17 (source: JS). The earliest price evidence is $119.99 with a $129.99 compare-at on 2026-08-24 (source: Wayback capture https://web.archive.org/web/20260824020743/https://aurzen.com/collections/projector-screens, captured 2026-08-24). It's the same today (source: JS, accessed 2026-10-28). The Wayback Machine has no capture of the product URL itself, so the data is thin: a sale between those dates or a different launch-day price is unverified.
- No TravelPlay promotion in Aurzen's Halloween deals post (source: https://aurzen.com/blogs/news-discoveries/aurzen-halloween-projector-deals-2026, 2026-10-22).
- **Amazon: no listing found.** Searches for "Aurzen TravelPlay Tesla", "Aurzen projector screen Tesla Model Y", "Aurzen screen" and "Aurzen MagPlay" returned Aurzen projectors and the MagPlay Pro, but no TravelPlay (source: amazon.com/s, accessed 2026-10-28). No ASIN, so no Amazon price or rating count.
- Walmart, eBay, Best Buy, TikTok Shop: no listing found by web search (accessed 2026-10-28). Unverified beyond that search.

## 6. Aurzen as a company

- Legal entity on the US site: "Aurzen Inc. and/or its affiliates" (source: https://aurzen.com/policies/terms-of-service, accessed 2026-10-28).
- PR Newswire releases are datelined Irvine, California (source: CES release, https://www.prnewswire.com/news-releases/aurzen-introduces-ev-focused-and-ultra-portable-projection-concepts-at-ces-2026-302652810.html, 2026-01-05; IFA release via https://macaubusiness.com/aurzen-shines-at-ifa-2026-garnering-11-honors-across-its-projector-lineup-70/, 2026-09-08).
- CB Insights lists "Founded Year: 2022" and "Headquarters Location: Fullerton, California" (source: https://www.cbinsights.com/company/aurzen, accessed 2026-10-28). This is an aggregator; I found no primary source for the founding year.
- Manufacturer link: Aurzen hosts an EU Declaration of Conformity for its BOOM 3 projector (model F503), issued by **Shenzhen Neutop Optoelectronics Co., Ltd**, Nanshan District, Shenzhen, China (source: https://cdn.shopify.com/s/files/1/0720/5109/7892/files/Boom_3_Neutop_Declaration_of_Conformity.pdf, dated 2024-04-08). The TravelPlay page's HTML carries this link too. Search snippets say the same Neutop company owns AURZEN trademarks in Australia and Canada (Justia returned 403; unverified). Who makes TravelPlay itself is unverified.
- Selling projectors since at least the BOOM 3 (DoC dated April 2024). The MagPlay was published June 2025 and the ZIP March 2025 (source: their .js `published_at`, accessed 2026-10-28).
- About page: "Aurzen is the entertainment technology brand..."; claims SGS ANSI/ISO 21118 brightness certification. No founding date or address given. (source: https://aurzen.com/pages/about-aurzen, accessed 2026-10-28)
- US support: support@aurzen.com, +1-667-218-4830, Mon-Fri 9AM-5PM EST, "Lifetime Customer Support" badge. The terms page prints the phone as "+86 1-667-218-4830", a typo or a China prefix. (source: PAGE; ToS, accessed 2026-10-28)
- Press for the TravelPlay launch: **none found.** No Aurzen press release or blog post mentions TravelPlay (blog feed checked back to 2026-02-09: https://aurzen.com/blogs/news-discoveries.atom, accessed 2026-10-28). The IFA 2026 release doesn't mention it. Searches turned up nothing from Teslarati, Not a Tesla App or Drive Tesla Canada (accessed 2026-10-28).
- Precursor: at CES 2026 Aurzen showed a "Tesla Model Y–based in-car cinema demonstration" with the ZIP Cyber Edition, projecting from "the ceiling, the trunk, and standard seated positions". Neither source mentions a screen product. (source: CES release, 2026-01-05; https://the-gadgeteer.com/2026/01/12/aurzen-zip-cyber-edition-brings-tri-fold-portable-projection-to-ev-road-trips-at-ces-2026/, 2026-01-12)

## 7. In-motion use

Everything Aurzen says (source: PAGE; MAN-EN pp.2-3, accessed 2026-10-28):
- Spec table: "Safety Note: Use only when the vehicle is parked. Do not use while driving."
- Safety notes: "Projection function is for use only when the vehicle is stationary."
- FAQ: "Safety Note: Projection use is intended only when the vehicle is parked. Do not watch projected content while driving."
- Manual: "For your safety, only use when the vehicle is stationary."
- Marketing copy throughout says "parked" ("parked-car entertainment", "while parked").

Aurzen does not say whether the screen may stay clipped up as a roof sunshade while driving. The spec-table line "Do not use while driving" can be read as covering any use; the other three lines are limited to projection. Unverified either way. There's also the general warning that improper installation "may cause the screen to fall". (source: PAGE, accessed 2026-10-28)

## Open questions / couldn't verify

- Which model years the roof-mode fallback covers: 2020-2024 (English) or 2022-2024 (Spanish).
- Fit on the Model Y Standard (glass hidden behind a headliner) and the Model Y L: Aurzen is silent.
- Screen gain, reflectivity, and any heat or UV blocking figures: not published.
- Setup time: not published.
- Tailgate mode: where the clips attach in the liftgate opening isn't specified.
- Whether the "+1 year with registration" extension applies to TravelPlay (accessories).
- Whether the MagPlay Pro (Amazon, $32.99) works for TravelPlay's rear-seat mode with a ZIP Pro, and its Amazon stock status.
- When the US MagPlay will be back in stock.
- Price between 2026-08-17 and 2026-08-24 (no capture).
- Who manufactures TravelPlay (Neutop is confirmed only for Aurzen projectors).
- Reviews on aurzen.com (loaded by JavaScript; not read; outside this angle).
- I did not render the 5-page MagPlay manual (also scanned images), which might carry car-glass or heat warnings for the rear-seat mount.
