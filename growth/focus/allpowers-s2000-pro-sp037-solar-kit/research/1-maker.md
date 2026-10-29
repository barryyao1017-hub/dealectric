# S2000 Pro + SP037 kit research, angle 1: maker facts

- **Angle:** 1, MAKER FACTS (what ALLPOWERS itself publishes, plus its store's own history)
- **Products:** ALLPOWERS S2000 Pro power station (https://iallpowers.com/products/allpowers-2400w-portable-power-station) and the S2000 Pro + SP037 400 W kit (https://iallpowers.com/products/allpowers-solar-generator-kit-2400w-s2000-pro-sp037-400w-solar-panel)
- **Date:** 2026-10-29
- **Method:** curl against the live Shopify stores (US `.js`, `products.json`, `search/suggest.json`, policy pages; EU and UK `search/suggest.json` and the EU S2000 Pro page), about 10 s between store calls, no cart endpoints. Three S2000 Pro manuals read with PyMuPDF and rendered crops (two are outlined text). 24 Wayback snapshots of the US station page (2022-06 to 2026-06), parsed for variant SKU, barcode, price, compare-at and spec lines. Product photos inspected. Amazon static HTML for ASIN B0CJ9T8L9B; Walmart returned a bot check, so I stopped (not bypassed). Wellbots `.js`. 8 web searches. ALLPOWERS-wide policy and company facts are reused from `../../allpowers-r4000-3456wh/research/1-maker.md` and SP037 facts from `../../allpowers-sp037-400w-solar-panel/research/1-maker.md`, re-checked only where this kit differs. Local copies: `/private/tmp/claude-501/-Users-jiayiyao-Desktop-dealectric/44f11078-b8ab-412e-a42d-cf3b4ee1b7ef/scratchpad/research/s2000-maker/`.

Short source names:
- **US page**: https://iallpowers.com/products/allpowers-2400w-portable-power-station (accessed 2026-10-29)
- **KIT page**: https://iallpowers.com/products/allpowers-solar-generator-kit-2400w-s2000-pro-sp037-400w-solar-panel (accessed 2026-10-29)
- **MANUAL V3.0**: https://cdn.shopify.com/s/files/1/0443/1223/2089/files/YPJSS0055-S2000PRO_V3.0_AP-SS-009-PRO_user_mannual.pdf?v=1716446947, the "Download Manual" link on both US pages. Header "S2000PRO V3.0", PDF created 2023-12-05, uploaded 2024-05-23 (accessed 2026-10-29)
- **MANUAL V3.3**: https://cdn.shopify.com/s/files/1/0747/3135/6467/files/YPJSS0079-S2000PRO_V3.3_AP-SS-009-PRO_user_manual_compressed.pdf?v=1735115619, linked from the EU page. PDF created 2024-10-28, uploaded 2024-12-25. Internal PDF title "S2000PRO+ V3.3" (accessed 2026-10-29)
- **MANUAL 2022**: https://cdn.shopify.com/s/files/1/0443/1223/2089/files/AP-SS-009-PRO_1500WH_2022-04-21_-_compressed.pdf?v=1651068422, still listed on https://iallpowers.com/pages/user-guides. Model "AP-SS-009-PRO (Monster X Pro)", PDF created 2022-04-21 (accessed 2026-10-29)
- **WB <date>**: Wayback snapshot `https://web.archive.org/web/<timestamp>/https://iallpowers.com/products/allpowers-2400w-portable-power-station`

## 1. Solar input: settled

**Answer: 12–150 V, 13 A, 1,000 W through one XT60 port on the current hardware. The FAQ's "18–70 V, under 18 A, 650 W" is the 2022 spec of the original S2000 Pro (the version with a 30 A RV outlet), left on the page after a hardware revision.**

Evidence:
- Current spec table on the US page: "Solar Input (12~150)V 13A, 1000W Max", and "1000W Max MPPT. Solar Input" in the feature list (US page; KIT page, accessed 2026-10-29).
- MANUAL V3.0 (US) and MANUAL V3.3 (EU) both give "Solar Input: (12~150)V 13A, 1000W Max" and "Car Charger Input: 12V/24V DC". Section 3.4 says to check that the panel is "within 150V, the maximum current is 13A, and the maximum charging power is within 1000W". It says to connect panels "in series as shown in the figure", and the figure shows a single 5-fold ALLPOWERS panel on the XT60 (rendered crops of both manuals, accessed 2026-10-29).
- The current US product photo prints the unit's own label next to the XT60 port: "SOLAR/CAR INPUT 12-150V 13A MAX." (source: https://cdn.shopify.com/s/files/1/0443/1223/2089/files/S2000PRO-US-01.jpg?v=1772000836, image dated 2026-02-25, accessed 2026-10-29).
- The FAQ on the same US page still says "maximum solar input of 650W" and, for third-party panels, "Voltage Range: 18-70V; Current Range: Under 18A; Maximum Power Input: 650W" (US page, accessed 2026-10-29).
- Where the 650 W figures come from:
  - MANUAL 2022 lists "Solar Input: 650W (18-70V, 18A Max.)", 14.5 kg, and shows a round RV socket on the front panel (rendered crop).
  - The US page said "Solar Input：18-70V, 18A 650W Max" and "NEMA TT-30 110V/30A port" from WB 2022-06-27 through WB 2024-02-20.
  - By WB 2024-06-24 the table read "(12~150)V 13A, 1000W Max", next to a new note: "The current S2000PRO version is an upgraded version (no RV output port)… We upgraded the S2000 Pro and removed the 30A RV output port." The note was still there on WB 2025-01-25 and gone by WB 2025-04-22. The EU page still carries it (https://iallpowers.eu/products/allpowers-s2000-pro-portable-power-station-2400w-1500wh, accessed 2026-10-29).
  - So the switch to 1,000 W happened between 2024-02-20 and 2024-06-24. The V3.0 manual PDF dates from 2023-12-05.
- ALLPOWERS EU contradicts itself in one FAQ answer: "The maximum input wattage of S2000 Pro is 1000W MPPT(12~150V ,13A)… Please remember that use the solar panels within the range(18V-70V)". Its charging-time answer still says "Solar charging, 650W" (EU page, accessed 2026-10-29).

**What one and two SP037s do on this input.** My arithmetic uses the SP037 figures from the SP037 dossier: V3.0 poly Voc 45.3 V, Vmp 37.4 V, Imp 10.69 A, Isc 11.7 A (page 11.45 A); V5.0 mono Voc 36.5 V, Vmp 30.5 V, Imp 13.11 A, Isc 14.42 A. The station limit is the manual's 12–150 V / 13 A / 1,000 W. ALLPOWERS' SP037 manuals say 260–320 W per panel is "normal" outdoors.

| Setup | Voc | Current | Fits the current S2000 Pro (12–150 V, 13 A)? | Ceiling at STC | Fits the 2022 RV-port unit (18–70 V, 18 A, 650 W)? |
|---|---|---|---|---|---|
| 1 × V3.0 | 45.3 V | Imp 10.69, Isc 11.7 A | Yes, fully | ~400 W (real world ~260–320 W) | Yes |
| 1 × V5.0 | 36.5 V | Imp 13.11, Isc 14.42 A | Voltage yes. Isc is above the manual's 13 A wording, Imp is right at the limit. The station draws at most 13 A, about 397 W, so nothing is lost. ALLPOWERS sells this pairing | ~397 W | Yes |
| 2 × V3.0 in series | 90.6 V | 10.69 A | **Yes.** Well under 150 V even with a cold-weather Voc rise (+20% would be ~109 V) | ~800 W (real world ~520–640 W) | **No.** 90.6 V is over 70 V, so expect an overvoltage fault (V3.0 manual code E301 "MPPT input overvoltage") |
| 2 × V3.0 in parallel | 45.3 V | Imp 21.4, Isc 23.4 A | Over 13 A. The station would cap near 13 A × 37.4 V ≈ 486 W. Outside the manual's limit, and worse than series | ~486 W | Isc over 18 A |
| 2 × V5.0 in series | 73.0 V | 13.11 A | Voltage yes. Current at the 13 A cap | ~793 W | No (73 V > 70 V) |
| 2 × V5.0 in parallel | 36.5 V | Imp 26.2, Isc 28.8 A | Over 13 A. The cap leaves ~397 W, so a second panel adds nothing | ~397 W | No |
| 1 × V3.0 + 1 × V5.0 in series | 81.8 V | limited to ~10.7 A | Voltage yes, but both SP037 manuals say not to mix unlike panels | ~726 W theoretical | No |

- **ALLPOWERS' own recommended configuration: one SP037 straight into the XT60.**
  - The kit ships one panel.
  - ALLPOWERS sells no "S2000 Pro + 2 × SP037" variant, while the R2500 Plus, R2500 V2, R3500 and R4000 each have one (source: https://iallpowers.com/products.json?limit=250, accessed 2026-10-29).
  - The US FAQ lists "SP037 400W Foldable" with no series count, while 100–200 W panels get "Up to 3/4 series" (US page).
  - The EU FAQ says "you could chooe ALLPOWERS SP037 400W solar panel".
  - The manual figure shows one panel.
- ALLPOWERS never says whether two SP037s in series are allowed on this station. The manual limits (and the unit's label) allow two V3.0 panels in series at ~800 W rated. The page's own FAQ forbids it (70 V, 650 W). Treat two in series as within the published V3.0/V3.3 hardware spec but not endorsed by ALLPOWERS. Never do it on a 2022–early 2024 unit with the round RV socket.
- **How to tell the hardware apart:** the old build has a round TT-30 RV socket on the front, to the right of the display. The current build has a printed circle there instead (photo above). The KIT page's lead image still shows the old RV-socket unit (source: https://cdn.shopify.com/s/files/1/0443/1223/2089/files/ALLPOWERSS2000Pro9_45355d7f-4537-4f00-8e72-e43d02cd4b22.jpg?v=1747378444, accessed 2026-10-29).

## 2. Spec sheet: US page vs manual

PAGE = US page spec table, feature list and FAQ. MANUAL = MANUAL V3.0. V3.3 matches V3.0 on every line below except the certification marks.

| Item | PAGE | MANUAL | Notes |
|---|---|---|---|
| Capacity | 1451Wh (title "1451Wh"; description "1451.5Wh") | 1451.6Wh (43.2 V, 33.6 Ah) | MANUAL 2022: "405405mAh 3.7V (1500Wh)". Older listings and the KIT JSON-LD still say 1,500 Wh |
| Chemistry | "Ternary lithium battery" | "Lithium battery"; FAQ Q1 "Ternary lithium battery" | NMC, not LiFePO4. Amazon's title says "LiFePO4 Battery", which is wrong (see §6) |
| Cycle rating | "Battery with 2,500+ Life Cycles to 80%" | no cycle figure | Only the page gives cycles. The old page added "lasts for almost 10 years (one cycle per day)" (WB 2023-09-26 to WB 2025-09-08) |
| AC output | "4x 100-120V，2400W Max (Surged 4000W)" | "2400W Max (Surged 4000W) (*When the battery drops to ≈60%, the rated AC output is 2000W Max.)"; "AC+DC Total Output: 2700W Max" | **The derate to 2,000 W below ~60% is in the manual and on Amazon, not on the US page** |
| Outlet types | "4 AC sockets" | "AC Output*4" drawing | US photo shows four NEMA 5-15R. No RV port on the current build (removed per the 2024 note). That photo's front circle reads "AC OUTPUT X 4 220-240V 2400W Max", an EU label left on the US render |
| USB-A | "4* USB A Output: USB1/USB2/USB3/USB4: 5V3A/9V2A/12V1.5A; USB1+USB3/USB2+USB4: 5V2.4A+5V2.4A" | "USB-A *2: 5V 2.4A, 12W Max"; "USB-A Fast charging *2: … 18W Max" | **PAGE is wrong.** MANUAL, V3.3, EU page and the port labels in the US photo ("USB-A 12W" ×2, "USB-A 18W" ×2) all say 2 × 12 W + 2 × 18 W |
| USB-C | "2* … 5V-20V/5A (PD 100W Max)" | "USB-C *2: 5/9/12/15V 3A, 20V 5A, 100W Max" | |
| Car port | "1* Car Output 12V 10A" | "12V 10A, 120W Max" | 2022 build was "13V10A" |
| AC input (120 V) | "AC Input 1500W" | "(100~120)V~15A 1500W Max" | Manual: plug straight into a wall socket that can carry 15 A, not an extension strip |
| AC charge time | "Recharge from 0-100% in 1.5 Hours (AC+solar input)" | not stated | Old page and KIT JSON-LD: 1.5 h on 1,500 W AC alone. Amazon: "0–80% in about 1 hour" on AC. EU FAQ: "AC+solar, 900W, 1.5h" and "AC charging: 400W, 1-2 hours" (the second is clearly wrong). Combined AC+solar maximum: not published anywhere |
| Solar input | "(12~150)V 13A, 1000W Max"; FAQ "650W", "18-70V", "Under 18A" | "(12~150)V 13A, 1000W Max" | See §1 |
| Car charging input | "Car to XT60 cable" needed, 12/24 V | "Car Charger Input: 12V/24V DC" via the shared XT60 | Car cable not included (Note 1). Sold as "XT60 Car Charger for R600/R1500/R2500/S2000PRO/S2000" (US page nav) |
| Pass-through | FAQ: when charging from AC "only the USB outings and AC outings are available", and it recommends not charging and discharging together "except in emergencies" | FAQ Q8: "Yes, the product supports simultaneous charging and discharging" | Conflict. EU FAQ: "yes" |
| UPS / EPS | "UPS will immediately supply battery backup power" | "within 15ms". UPS holds only if AC load ≤ 1,500 W at 100–120 V. Above that, grid and battery share the load "until the power station consumes to 5%", then AC turns off. Recommends one device at a time | Amazon title says "20ms UPS", its bullet says "<15ms" |
| Charge temp | not stated | 0–40 °C (32–104 °F) | |
| Discharge temp | not stated | −10–40 °C (14–104 °F) | MANUAL 2022: working −20–45 °C, charging over-temperature protection 55–65 °C |
| Storage | "do NOT store it in a humid environment" | −20–40 °C (20–30 °C recommended), 10–90% RH; for long storage discharge to 30% and recharge to 60% every three months | Not waterproof (PAGE FAQ). Not allowed on planes (MANUAL FAQ Q7) |
| Self-heating | none | none | No battery heater mentioned in any of the three manuals |
| Noise | "quiet in operation" | fan icon on the display; no dB figure | No noise figure published |
| Weight | "13kg / 28.66lb" | "Approximately 13KG (28.66lbs)" | Page said 14.5 kg / 31.97 lb from WB 2022-06-27 to WB 2025-04-22, and 13 kg from WB 2025-08-09. MANUAL 2022: 14.5 kg. The EU comparison table still says 14.5 kg. Amazon: 32 lb. Shopify variant shipping weight: 21,000 g (US `.js`) |
| Size | 37.5 × 24.5 × 25 cm | 375 × 245 × 250 mm | Same since 2022 |
| Certifications | none on the page | V3.0: UL, PSE, CE, FCC, RoHS, IC, UKCA plus recycling marks (rendered crop). **V3.3 (EU) shows the same row without the UL mark** | No UL standard (e.g. UL 2743) or file number in any manual. One search found no UL listing (2026-10-29). UL status: unverified |
| Expansion battery | none | no expansion port or section | EU FAQ: "the product could not support change the battery or expanded battery capacity". B1000 is offered only with the R2500 Plus (`products.json`) |
| App | "Bluetooth wireless connection… up to 10 meters" | Bluetooth only. Off by default: hold DC OUTPUT 3 s. Pairs as "AP S2000PRO V2.0". App shows battery, input/output power, AC/DC switches, frequency switch | No Wi-Fi. Old page FAQ (WB 2025-04-22 to WB 2026-01-02) mentions firmware ("code upgrade") prompts, and says to ignore them while the unit works |
| AC input socket | not shown | IEC-style inlet on the back (drawing) | |
| In the box | "Included: S2000 Pro, AC Adapter, User Manual" (`.js` description) | "ALLPOWERS S2000PRO, AC Charging cable, User Manual and Warranty Card" | The warranty page excludes the "Product charging adapter" from warranty |

## 3. End-of-life, successor, and what "PLUS" means

**Answer: no successor and no EOL notice. ALLPOWERS still sells the S2000 Pro in the US, EU and UK, puts it in the US Black Friday collection, and lists it under the 5-year warranty. There is no "S2000 Pro V2" or "S2000 Plus" product. The hardware was revised once in place, in early to mid 2024 (RV port removed, solar raised to 1,000 W). "PLUS" in the SKU is the same 2026 catalog relabel seen on the R4000.**

- **US:** in stock, $664, compare-at $1,399 (source: https://iallpowers.com/products/allpowers-2400w-portable-power-station.js, accessed 2026-10-29). Five S2000 Pro listings come up in store search (standalone, +100 W, +200 W, +SP037 kit, +SF200 kit) (source: https://iallpowers.com/search/suggest.json?q=s2000, accessed 2026-10-29).
- **Black Friday 2026:** the standalone S2000 Pro is in the "Black Friday Products" collection at $664. The S2000 Pro + SP037 kit is not (source: https://iallpowers.com/collections/black-friday-products/products.json?limit=250, 24 products, accessed 2026-10-29).
- **EU:** S2000 Pro €664 (compare-at €1,299, created 2023-04-04), plus a UK-plug version at €629. The S2000 Pro + SP037 kit is €949, and other S2000 Pro kits are listed (source: https://iallpowers.eu/search/suggest.json?q=s2000 and the EU `.js`, accessed 2026-10-29).
- **UK:** S2000 Pro £531.99; S2000 Pro + SP037 £873.05 (source: https://uk.iallpowers.com/search/suggest.json?q=s2000, accessed 2026-10-29).
- **Web search:** nothing on an S2000 Pro V2, S2000 Plus or discontinuation (2026-10-29).
- **R2500 V2 is not called a successor.** "ALLPOWERS R2500 V2 Portable Power Station | 2500W 1920Wh" (created 2026-06-25, $659, compare-at $1,599, SKU R2500-V2-US):
  - LiFePO4 ("3500+ Cycles"), 2,500 W (5,000 W peak in the feature list, 4,000 W in the table)
  - solar 12–150 V 20 A 1,000 W, AC+solar 2,000 W
  - Wi-Fi + Bluetooth, 29 kg (source: https://iallpowers.com/products/allpowers-r2500-v2-portable-power-station-2500w-1920wh, accessed 2026-10-29)
  - It replaces the R2500 Plus, whose standalone and +B1000 variants both show available: false (`products.json`). Its SP037 kit (created 2026-10-27) is $958 vs $963 for this S2000 Pro kit, and unlike the S2000 Pro kit it has a 2 × SP037 option ($1,257).
  - In practice the R2500 V2 is the same-money LiFePO4 alternative. ALLPOWERS doesn't present it as replacing the S2000 Pro, and both sit in the site nav (US page nav, accessed 2026-10-29).
- **"PLUS" in S2000-PLUS-US:**
  - Same Shopify product (ID 7294376411289, created 2022-02-16) and same variant ID (42882903310489) since Dec 2022.
  - SKU history: `AP-SS-009-PRO` (WB 2022-06-27 to 2022-10-02, an earlier variant ID 41830998343833), then `AP-SS-009-PRO-EU` on the US store (WB 2022-12-21 to 2023-04-02), then `AP-SS-009-PRO-US` (WB 2023-05-16 to WB 2026-01-02), then `S2000-PLUS-US` (WB 2026-06-16 onward).
  - The UPC changed from 782940087319 to 747165451413 at the same time (barcodes in WB 2025-09-08 and live `.js`).
  - This matches the R4000 relabel (R4000-PLUS-US, new 74716545xxxx UPC, early 2026), and the spec table was identical before and after (WB 2025-09-08 vs WB 2026-06-16).
  - The only other "plus" is the EU V3.3 manual's internal PDF title "S2000PRO+ V3.3" (Oct 2024). Inference: a catalog label, not a new model. Unverified from outside.
- **Amazon:** the 2022 ASIN B09VL33L58 (cited by manuals.plus) now lands on the VOLIX P300 listing, B0GN8T9VL3. The current S2000 Pro ASIN is B0CJ9T8L9B (source: https://www.amazon.com/dp/B09VL33L58 and https://www.amazon.com/dp/B0CJ9T8L9B, accessed 2026-10-29).
- **S2000 (non-Pro):** gone as a standalone US product, but its SP037 kit is still listed at $1,203 (`products.json`).

## 4. Kit specifics

- **Listing:** "ALLPOWERS Solar Generator Kit 2400W (S2000 Pro + SP037 400W Solar Panel)", product 8269325435033, one variant 44977510056089, SKU `AP-SS-009-PRO+AP-SP-037`, GTIN 759187229192, $963, compare-at $1,999, InStock. Created 2024-11-24, published 2026-09-02 (source: KIT `.js` and JSON-LD, accessed 2026-10-29).
- **A second, hidden US listing for the same pair costs $79 more.** "ALLPOWERS S2000 Pro + 400W Solar Panel SP037 | 2400W Solar Generator Kit":
  - handle `allpowers-s2000-pro-solar-generator-portable-power-station-2400w-1500wh-with-solar-panels`, product 7313931141273, created 2022-03-03, published 2026-07-15
  - SKU `S2000-PLUS-US + AP-SP-037`, **$1,042**, compare-at $1,999, available: true
  - the page carries `<meta name="robots" content="noindex,nofollow">` and is absent from `products.json` and store search (source: https://iallpowers.com/products/allpowers-s2000-pro-solar-generator-portable-power-station-2400w-1500wh-with-solar-panels and `.js`, accessed 2026-10-29)
  - It showed $899.99 in the store's menu data on WB 2026-06-16. A shopper reaching it from an old link or a review would overpay.
- **What's in the boxes.** The KIT page never lists kit contents. Pieced together:
  - Station box: S2000 Pro, AC charging cable, manual and warranty card (MANUAL §6).
  - Panel box: SP037, "Solar Cable to XT60", "Solar Cable to DC 5525 + DC 8020 Cable Adaptor", manual (SP037 dossier §2, from https://iallpowers.com/products/allpowers-400w-portable-solar-panel).
  - KIT page Note 1: "Purchase of power station and solar panel package includes solar cable and does not include car charger". So the MC4 → XT60 cable comes with the kit and plugs the panel straight into the station's XT60.
  - The panel version shipped in the kit (V3.0 poly or V5.0 mono) is not stated. The kit's hidden description says "Polycrystalline".
- **Ships as two packages:**
  - KIT page Note 2: "the solar panels and power station will be shipped separately".
  - Shipping policy: an order with a panel and a station is "divided into 2 packages"; station by FedEx/UPS (2–3 days), panel by FedEx/UPS/USPS (3–7 days) (source: https://iallpowers.com/pages/shipping-policy, accessed 2026-10-29).
  - A kit buyer on the page: "Solar panels were shipped separately. But came the same day, 2 different carriers. Generator arrived at 72% charged" (Elictric J., 2023-03-12, KIT page reviews).
- **The kit page's crawler-visible text describes a different kit.** The Shopify description, which is also the page's meta description and JSON-LD `description`, is copy from an old 2 × 200 W kit:
  - "2*ALLPOWERS 200W foldable solar panel"
  - "650W max, 3 hours to full"
  - "【30A RV Output】"
  - "24-month warranty"
  - "The conversion rate of polycrystalline silicon solar cells is about 60%"
  - a package list with MC-4 to Anderson cables and a waterproof bag (KIT page HTML `<meta name="description">` and `application/ld+json`, accessed 2026-10-29)
  - The visible page body is the station template. The second gallery image is a 200 W panel comparison table (Voc 22.2 V, Isc 12 A, 6.3 kg), not SP037 data (source: https://cdn.shopify.com/s/files/1/0443/1223/2089/products/16571850542661.png?v=1747378444).
  - AI assistants that read the meta or JSON-LD will get the wrong panel count, solar ceiling, port list and warranty.
- **Returns as a whole or per item:** not addressed in any ALLPOWERS policy.
  - The returns page requires "all accessories" and "original packaging", refuses "open box" items, needs an RMA, and counts 30 days "from the original shipment date" (source: https://iallpowers.com/pages/returns-and-refunds, accessed 2026-10-29).
  - The kit is one SKU at one price, so a partial return's refund amount is undefined.
  - Unverified. Ask service@allpowers.com before relying on it.
- **Warranty by component** (source: https://iallpowers.com/pages/warranty-policy, accessed 2026-10-29):
  - "5-Years Limited Warranty" list includes "S2000 PRO". The "2-Years Limited Warranty" list includes "S037" (SP037).
  - The base term is "24 months from the date of purchase", extended by registering at https://iallpowers.com/pages/warranty-register.
  - Refurbished S2000 Pro: 2 years.
  - The returns page still says 18 months. Kits aren't mentioned.
  - The KIT page badge says "5-year Warranty", which can only mean the station. Its hidden description says "24-month warranty".
- **Price vs separate items:** kit $963 vs $664 + $299 = $963 separately. Same money, and a two-item cart qualifies for BULKRATE (our cart check `cart-check-2026-10-29.md`).

## 5. Price history

**Station** (US page; WB snapshots unless noted; snapshots are sparse, so lows between them are unknown):

| Date | Price | Compare-at | SKU / note |
|---|---|---|---|
| 2022-02-16 | | | Shopify product created (live `.js`) |
| 2022-06-27 | $1,799 | $2,999 | AP-SS-009-PRO, 650 W solar, RV port, 14.5 kg |
| 2022-07-12 to 2022-12-21 | $1,999 | $2,499 (Dec) | from Dec, AP-SS-009-PRO-EU on the US store |
| 2023-02-07 to 2023-04-02 | $1,899 | | |
| 2023-05-16 / 06-01 | $1,299 | $2,199 | AP-SS-009-PRO-US |
| 2023-09-26 | $1,099 | | |
| 2023-11-24 | **$799** | $1,299 | Black Friday 2023: "$799 (Reg. $1299)", valid Nov 17–30 (source: https://prnewswire.co.uk/news-releases/allpowers-black-friday-deals-are-now-live-301997159.html, 2023-11-24) |
| 2023-12-04 | $899 | | |
| 2024-02-20 | $979 | | last 650 W spec snapshot |
| 2024-06-24 / 09-07 | $899 | $1,299 | 1,000 W spec, "no RV output port" note |
| 2025-01-25 | $879 | $1,299 | |
| 2025-04-22 | $699 | $1,299 | |
| 2025-08-09 | $714 | $1,299 | 13 kg spec now |
| 2025-09-08 / 2026-01-02 | $699 | $1,399 | |
| 2026-06-16 | **$549** | $1,399 | S2000-PLUS-US. Lowest US-store price seen |
| 2026-10-29 | $664 | $1,399 | live |

**S2000 Pro + SP037.** It was a variant of the station page until at least WB 2026-01-02, then a separate kit:

| Date | Price | Compare-at |
|---|---|---|
| 2022-12-21 | $2,799.99 | $3,299 |
| 2023-02-07 | $2,299.99 | |
| 2023-04-02 | $2,499 | |
| 2023-05-16 / 06-01 | $1,899 | $2,599 |
| 2023-09-26 | $1,499 | |
| 2023-11-24 / 12-04 | $1,238 | $1,999 |
| 2024-02-20 | $1,458 | |
| 2024-06-24 / 09-07 | $1,299 | $1,999 |
| 2025-01-25 | $1,259 | |
| 2025-04-22 | $1,069 | |
| 2025-08-09 / 09-08 | $1,090 | |
| 2026-01-02 | $1,098 | |
| 2026-06-16 | $899.99 | (hidden listing above, menu data) |
| 2026-10-29 | **$963** (main kit) / $1,042 (hidden listing) | $1,999 |

- The current kit URL has no Wayback captures (source: https://archive.org/wayback/available?url=iallpowers.com/products/allpowers-solar-generator-kit-2400w-s2000-pro-sp037-400w-solar-panel, accessed 2026-10-29).
- **Was the compare-at ever charged?**
  - Station $1,399: never seen as a selling price. Prices above it were charged only until April 2023 (old hardware).
  - Kit $1,999: never seen. $1,899 was charged in May–June 2023.
  - Both compare-ats have been in place since late 2023 (kit) and Sept 2025 (station), while selling prices ran 45–60% below.
- **Launch price:** unverified. The earliest seen is $1,799 (2022-06-27), four months after the product was created.
- **Amazon deals (9to5Toys):**
  - S2000 Pro + 200 W panel $1,249, "new all-time low" (https://9to5toys.com/2023/09/12/allpowers-s2000-pro-solar-generator-with-200w-panel-falls-to-new-all-time-low-for-1249/, 2023-09-12; headline plus search snippet giving a $250 coupon and $1,499 regular price; page not opened)
  - S2000 Pro + 100 W panel $749.50, reg. $1,499 (https://9to5toys.com/?p=1023446, 2023-12-18)
  - S2000 Pro + 200 W $999 (https://9to5toys.com/?p=1034551, 2024-02-21) and $849 (https://9to5toys.com/?p=1038958, 2024-03-13)
  - An "upgraded ALLPOWERS S2000" at $699 that quotes S2000 Pro specs, model ambiguous (https://9to5toys.com/?p=1027962, 2024-01-17)
- Electrek and Slickdeals: nothing S2000 Pro-specific found (search, 2026-10-29).

## 6. Availability elsewhere (2026-10-29)

- **Amazon B0CJ9T8L9B** (source: https://www.amazon.com/dp/B0CJ9T8L9B, static HTML, accessed 2026-10-29):
  - $549.00, In Stock, "Ships from and sold by GiarideDirect" (the seller of the ALLPOWERS-brand SP037 ASINs too)
  - "Amazon's Choice", 4.5/5 from 60 ratings, part number AP-SS-009-PRO
  - Return status "Non-returnable. Transportation of this item is subject to hazardous materials regulation"
  - Spec claims, correct or carried over: "1000W solar input", "<15ms" UPS, "0–80% in about 1 hour", 32 lb, "Warranty Description 6 Years"
  - Wrong vs ALLPOWERS' manual: title says "LiFePO4 Battery" and "20ms UPS"
  - Coupons load by JS and weren't visible. The page text shows "Get $50 off instantly", which looks like a payment-card offer (unverified).
- **Amazon bundles** (from search, not opened): SF200 (B0CHYG5X89), SE100 (B0CHYH3VT7), 2 × SE100 (B09SWSGLQZ), SE200 (B0CHYGHC3J), 2 × SE200 (B0GY7ZC8P6). No S2000 Pro + SP037 Amazon bundle turned up (search, 2026-10-29).
- **Wellbots:**
  - "ALLPOWERS S2000 PRO 2400W 1451.6WH portable power station", $564.91, available, no compare-at, listed 2026-06-10, EAN 6975274261201 (source: https://www.wellbots.com/products/allpowers-s2000-pro-2400w-1451-6wh-portable-power-station.js, accessed 2026-10-29)
  - The listing claims a "5-year warranty", "80% in 1 hour", 13 kg, and oddly "Frequency 50 Hz", "Voltage 30.0"
- **Walmart:** https://www.walmart.com/ip/1380317760 returned "Robot or human?". Not bypassed. A search snippet showed "S2000Pro … $559.00" with options to $958 (unverified at source).
- **EU / UK:** see §3.

## ChatGPT claims checked (W1 scan, 2026-10-28, `growth/evals/runs/2026-10-28-visibility/chatgpt/allpowers-s2000-pro-sp037-solar-kit--*.json`)

| Claim | Verdict | Evidence |
|---|---|---|
| (deal-1) "Wellbots listing $564.91", below ALLPOWERS' "$597.60 after coupon" | **Price true.** Warranty standing **unverified, likely not covered by ALLPOWERS directly** | Wellbots `.js` today: $564.91, available, listed 2026-06-10. ALLPOWERS $664 − 10% = $597.60 ✓. ALLPOWERS' warranty page: "If you buy from another online store or seller … it is not covered by the official manufacturer's warranty". It names only its global, DE and UK sites, plus "other official platform stores" whose claims it passes to the platform. The returns page excludes "Purchases from unauthorized resellers". Wellbots is not named anywhere on ALLPOWERS' pages, and no authorization was found by search. The 30-day money-back applies only to direct purchases. So Wellbots' own "5-year warranty" line is Wellbots' promise. Cheaper by $32.69 than ALLPOWERS-with-code, and not cheaper than Amazon ($549) |
| (deal-2, worth-1) "S2000 Pro with a 100W panel from $624 and with a 200W panel from $709" | **$624 true and buyable. $709 true as a listed "from" price but that variant is sold out** | `s2000-pro-100w-solar-panel` (created 2023-09-27): + SP027 **$624 available**; + SE100 $964 available (priced above the SP037 kit, likely an error); + 2 × SE100 $1,034 available; + SF100 $648 and + 2 × SF100 $747 unavailable. `s2000-pro-200w-solar-panel`: + SP033 **$709 unavailable**; + SF200 $718 unavailable (the variant ChatGPT's card linked, 46377150021785); + SE200 **$803 available**, which is the cheapest buyable 200 W kit. Separate SF200 kit listing: $833 / $1,001, unavailable (`.js` of each and `products.json`, accessed 2026-10-29). 100 W or 200 W on a 1,451 Wh station means 7–15 h of ideal sun for a full charge (my arithmetic) |
| (worth-1) "Recent listed prices for the power station alone: $549–$664"; "An independent price tracker listed Amazon at $549" | **True** | Amazon B0CJ9T8L9B $549 today (GiarideDirect). US store $664 today and $549 on 2026-06-16 (WB). Wellbots $564.91 sits inside the range |
| (worth-1, worth-2) "around 29 lb", "28.7 lb" | **True for the current spec** (13 kg = 28.66 lb on the US page and both V3 manuals). Older figure 14.5 kg / 31.97 lb (2022 manual; US page until at least 2025-04-22; EU comparison table today). Amazon says 32 lb. Our record's 13 kg is right | see §2 Weight |
| (worth-1) the S2000 Pro's alternatives "use LiFePO4 batteries", implying the S2000 Pro doesn't | **True** | ALLPOWERS says ternary lithium (NMC) on the page and in manual FAQ Q1. Amazon's "LiFePO4" title is wrong |

## Mismatches vs our records

1. **Solar.** Record "1,000 W, 12-150 V, 13 A per spec table and manual (FAQ says 650 W)" is right. Add why: the FAQ's 18–70 V / 18 A / 650 W is the original 2022 build's spec. The unit's own XT60 label reads "12-150V 13A MAX". The 1,000 W spec dates from the early-to-mid-2024 revision that removed the RV port. Suggested line: "One SP037 is ALLPOWERS' pairing. Two V3.0 SP037s in series (~90 V) fit the manual's 150 V limit but not the page FAQ, and never on a pre-2024 unit with the round RV socket. Don't parallel two (13 A cap)."
2. **USB-A.** Record (2 × 18 W + 2 × 12 W) matches the manual and the port labels. The US page table wrongly lists four 18 W ports.
3. **AC output.** Missing: "rated 2,000 W once the battery drops to about 60%" and "AC + DC total 2,700 W" (manual).
4. **"4 outlets".** Correct for current units (4 × NEMA 5-15R). Older units had a TT-30 30 A RV socket. The KIT page's lead photo and its JSON-LD description still show or describe the RV port. Worth a caveat: used or old-stock units may be the 650 W RV-port build.
5. **Weight 13 kg.** Correct per the page and V3 manuals. The 14.5 kg / 32 lb figures on Amazon and older pages are the 2022 spec (or a heavier build; unverified which).
6. **Chemistry / cycles.** NMC and "2,500+ cycles" are confirmed, with end point **80%** (page). The manual gives no cycle rating.
7. **AC input 1,500 W, "full in 1.5 h with AC + solar".** Matches the page. The manual states no time. The combined AC+solar maximum isn't published anywhere. Amazon says 0–80% in ~1 h on AC.
8. **App.** Bluetooth-only is confirmed. Bluetooth is off by default (hold DC OUTPUT 3 s).
9. **Warranty "5 years".** Same caveat as the R4000: 24 months unless registered, 18 months on the returns page. SP037 in the kit is 2 years. The kit's hidden description says 24 months.
10. **Not in our record:** UPS switchover 15 ms, holding only at AC load ≤ 1,500 W at 120 V. Charge 0–40 °C, discharge −10–40 °C. No self-heating. No expansion battery. Pass-through allowed per manual but discouraged per page FAQ.
11. **Kit listing.** Our URL, $963, $1,999 compare-at, SKU and the 2024-11-24 / 2026-09-02 dates all match. New: a second noindex US listing for the same pair at $1,042, which our page could warn about. The kit is not in the Black Friday collection, though the standalone station is.

## Open questions / couldn't verify

- Which SP037 version (V3.0 poly or V5.0 mono) the kit ships today. Neither kit page says, and the hidden description says polycrystalline.
- Whether any pre-2024 RV-port (650 W) S2000 Pro stock is still sold new, refurbished (EU lists a refurbished unit, not opened) or on Amazon. The two builds share one SKU family and model number AP-SS-009-PRO.
- Whether 14.5 kg → 13 kg reflects lighter hardware or a spec correction.
- UL listing: the V3.0 manual shows a UL mark with no standard or file number, and the EU V3.3 manual drops it. UL Product iQ not checked.
- Combined AC + solar input ceiling, idle draw, noise in dB, inverter efficiency, surge duration: not published.
- Whether ALLPOWERS endorses two SP037s in series on the current build. Its manual limits allow it, its FAQ doesn't.
- Kit returns: whole kit only, or per item, and how a partial refund is priced.
- Whether Wellbots is an authorized reseller for ALLPOWERS warranty purposes.
- Walmart price, seller and stock (bot check). Amazon coupon state (JS-loaded).
- Why the $1,042 kit listing is live but noindexed and absent from `products.json`.
- Launch MSRP (Feb 2022). Black Friday 2025 and 2026 S2000 Pro prices (the 2025-11-07 Wayback capture is empty; nothing announced for 2026 as of 2026-10-29).
