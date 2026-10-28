# BLUETTI AC200L: maker facts (research angle 1 of 5)

- **Angle:** Maker facts: what BLUETTI itself publishes, plus live store state.
- **Product:** BLUETTI AC200L portable power station (US model, SKU AC200L-US-GY-BL-SPFUS-00, Shopify product 8131806462171, UPC 193022001879).
- **Date:** 2026-10-28.
- **Method:**
  - Shopify `.js` endpoints, `search/suggest.json` and `collections/all/products.json` on bluettipower.com, fetched with curl and a desktop UA. Prices last re-checked 2026-10-28 08:36–08:39 UTC.
  - The canonical AC200L page's tech-spec table, embedded in its server HTML.
  - US user manual PDF (V3.0) from BLUETTI's support site, text extracted with pypdf.
  - BLUETTI support FAQs, read from the support site's embedded data.
  - Policy pages on bluettipower.com.
  - Amazon, Walmart and Home Depot pages loaded in a real browser.
  - Press and deal posts fetched directly.
  - Old BLUETTI forum threads read from Wayback copies, because the forum now redirects.
- **Gaps:** The WebSearch budget ran out near the end, so a few items stayed unverified. They are marked below.

**BLUETTI US has two AC200L listings, both with SKU AC200L-US-GY-BL-SPFUS-00.**

1. **`/products/ac200l`** (the one we link):
   - Created 2023-10-31, republished 2026-02-24, tagged with a promo-price tag.
   - Shows $899 / compare-at $1,599, available, schema.org InStock.
   - Carries `<meta name="robots" content="noindex,nofollow">`.
   - Is absent from `/collections/all/products.json` (413 products checked).
   - Its body did not render in curl, WebFetch or a real browser (header, footer and banners only), and its `.js` description field is empty.
2. **`/products/ac200l-portable-power-station`**:
   - Created 2024-12-15; canonical, server-rendered, and the URL BLUETTI's own menu links to.
   - Shows available:false, schema.org OutOfStock, and a red "Discontinued" label on the base unit and every bundle.
   - Has a variant metafield `sales_status_discontinued` = "true".
   - Has a full tech-spec table.

Sources: both URLs plus `.js`, and https://www.bluettipower.com/collections/all/products.json?limit=250, all accessed 2026-10-28 08:39 UTC. This confirms the coordinator's 08:37–08:45 UTC check.

Below, "**BLUETTI spec page**" means listing 2's tech-spec table.

---

## 1. Spec sheet (manual V3.0 + BLUETTI support) and mismatches with our record

Primary source is the US user manual "AC200L Portable Power Station User Manual V3.0" (source: https://s4.bluettipower.com/bluetti_lgf/support/2025/05/cca63f10-4c44-4b89-9e33-d235f2c19f93.pdf, file path dated 2025-05, accessed 2026-10-28). It is linked as "User Manual" from https://support.bluettipower.com/products/ac200l (accessed 2026-10-28). Page numbers below refer to the printed manual.

### Core numbers
| Item | BLUETTI figure | Source |
|---|---|---|
| Capacity / chemistry | 2,048 Wh (40 Ah), LiFePO4 | manual p.25 |
| Cycle life | **3,000+ cycles to 80% of original capacity** (BLUETTI spec page). Not in the manual. Amazon says only "3000+ Cycles" | https://www.bluettipower.com/products/ac200l-portable-power-station, accessed 2026-10-28; Amazon B0CLGZB3L6 |
| AC output | 120 V, 20 A, 2,400 W total, pure sine, 50/60 Hz switchable | manual p.11, 26 |
| Overload behaviour | 2,520–3,000 W for 2 min; 3,000–3,600 W for 5 s; >3,600 W for 0.5 s | manual p.26 |
| AC + DC output with no grid | 2,500 W max | manual p.25 |
| Power Lifting | Off by default. For resistive loads of 2,400–3,600 W only (kettles, hair dryers, heaters). Real output power stays at 2,400 W | manual p.21 |
| AC outlets | 4× "20A AC Outlet" + 1× "30A AC Outlet" (NEMA TT-30). All AC shares the 20 A / 2,400 W inverter limit, so the TT-30 does not deliver 30 A | manual p.12, 19, 26 |
| USB-C | 2×, PD 3.0, 100 W max each (5/9/12/15/20 V 3 A, 20 V 5 A) | manual p.19, 26 |
| USB-A | 2×, QC 3.0, 18 W each | manual p.19, 26 |
| 12 V car port | 1×, 12 V / 10 A (120 W) | manual p.19, 26 |
| 48 V DC port | 1×, 44.8–57.6 V / 8 A (for the D40 regulator, RV batteries) | manual p.19, 26 |
| Output ports total | 11 per the manual and Amazon's bullets. Amazon's "Special Feature" line says "13 Versatile Ports" | manual p.19; Amazon, accessed 2026-10-28 |
| Solar / DC input | One 2-pin aviation socket: 12–145 V (Voc), 15 A max, 1,200 W max. Panels go in series. MC4 panels via the included cable | manual p.2, 16, 26, 31 |
| Solar charge time | ~2.4 h to 100% at a sustained 1,200 W | manual p.16 |
| AC input | 2,400 W max. The spec table says "0%–80% in 60 minutes @ 25 °C" | manual p.26 |
| AC Turbo charging | "80% in just 45 minutes" at 25 °C with Turbo enabled in the app (§7.1). This contradicts the 60 min in the same manual's spec table | manual p.16 |
| Charging modes | Standard: AC 1,200 / PV 1,200 / AC+PV 1,200 W. Turbo: AC 2,400 / PV 1,200 / AC+PV 2,400 W. Silent: 800 W in each case | manual p.20 |
| Dual charging (AC + solar) | 2,400 W combined max (Turbo mode only) | manual p.20; support FAQ "AC200L vs AC200MAX", accessed 2026-10-28 |
| Grid input current limit | Default 15 A. Up to 20 A allowed, but raising it above 15 A needs a password from BLUETTI Customer Service. The included AC cable is labelled 15 A | manual p.9, 23 |
| 2,400 W wall charging needs a 20 A cord | BLUETTI spec page: "*Optional 20A plug to achieve 2400W (US/Canada only)". A "20A AC Charging Cable For AC200L" ($49) is listed but unavailable today | spec page; https://www.bluettipower.com/collections/all/products.json, accessed 2026-10-28 |
| AC charge times (spec page) | AC 2,400 W: 1.5 h full. Solar 1,200 W: 2.5 h. AC + solar: ≈1.5 h. 12/24 V car at 100/200 W: ≈10 or 20 h | spec page, accessed 2026-10-28 |
| Car charging | 96 W max per the manual (stops below 10.5 V). The spec page says "12/24V" car input at 100 W / 200 W | manual p.17; spec page |
| Other charging | Generator (Grid Self-adaption mode in the app); lead-acid battery via optional cable | manual p.17–18, 23 |
| UPS | Switching time ≤20 ms. Four UPS modes: Standard, Time Control, PV Priority, Customized. The manual excludes devices that need a "high-performance" UPS (servers, workstations, medical equipment) | manual p.5, 22, 26; support FAQ "Can I use AC200L as a UPS?" |
| Self-consumption (idle) | ~12 W | manual p.30 (Appx. 1) |
| Inverter efficiency | Manual: "typically over 93%", at 95% DoD. Spec page: "AC efficiency up to 92%" | manual p.30; spec page |
| ECO mode | AC-ECO and DC-ECO are on by default. Disable them for small loads under 60 W, or the outlets may shut off | manual p.21 |
| Charging temperature | 0–40 °C (32–104 °F) | manual p.25; support FAQ |
| Discharging temperature | −20 to 40 °C (−4 to 104 °F) | manual p.25 |
| Storage | −20 to 45 °C for ≤1 month; −20 to 30 °C for ≤3 months; −20 to 25 °C for ≤12 months. Store at 40–60% SoC and cycle every 3 months | manual p.2, 8, 25 |
| Self-heating | **None documented.** The manual has a low-temperature alert (internal temperature < −20 °C) and FAQ guidance not to recharge below freezing | manual p.15; support FAQ |
| Noise | 50 dB max | manual p.25; support FAQ (≤50 dB) |
| Humidity / altitude | 10–90% / 2,000 m | manual p.25 |
| Size / weight | 420 × 280 × 366.5 mm (16.5 × 11 × 14.4 in); 28.3 kg / 62.4 lb. Amazon lists 61.4 lb | manual p.25; Amazon |
| Connectivity | Wi-Fi + Bluetooth 5.0/5.1. Through the BLUETTI app you can change modes and upgrade firmware | manual p.22, 26; support FAQ "Does the AC200L support app control?" |
| Waterproof | No | support FAQ |
| Pass-through charging | Yes | manual p.31; support FAQ |
| Certifications | **UL2743, UKCA, TELEC, RCM, FCC ID, CE, PSE, NTC** (spec page). The manual shows FCC Part 15 Class B and ISED ICES-003 Class B | spec page; manual p.32–33 |
| Grid-tie / home panel | The manual says the unit is "for off-grid use only" and the AC output must not connect to the grid. Two AC200Ls cannot be bonded for 240 V split phase. The spec page's marketing says the UPS is "ideal for mobile use or paired with a home sub-panel", but gives no wiring method. No BLUETTI transfer-switch or Smart Home Panel product is listed for the AC200L | manual p.2, 11; support FAQ "Can I connect two AC200L units together for 240V…": "No."; spec page |

Support source for the FAQ rows: https://support.bluettipower.com/products/ac200l (accessed 2026-10-28).

Recommended panels per the support FAQ: 6× PV120 ≈3.5 h, 5× PV200 ≈2.5 h, 3× PV350 ≈2.5 h. Panels must be MC4, 12–145 V Voc, 1,200 W max.

### Mismatches vs our record (src/products.py, verified 2026-10-27)
0. **Status: the product is being phased out** (see §7). Our record's "in stock" is true only for the noindex listing at /products/ac200l. BLUETTI's canonical listing marks the AC200L "Discontinued" and out of stock.
1. **Expansion: "Expandable to 8,192 Wh (2× B300)" is out of date, and BLUETTI's sources disagree on the maximum.**
   - The B300 is "End of Sale" (source: https://www.bluettipower.com/pages/bluetti-discontinued-models, accessed 2026-10-28).
   - The BLUETTI spec page says "Expandable w/ Up to 2 x B210, 1 x B230 or 2 x B300, B300K", headlined "2kWh to 7.6kWh" (7,577.6 Wh with 2× B300K).
   - BLUETTI's B500K FAQ says the AC200L takes up to 2× B500K via the P090A cable, for **12,288 Wh** (source: https://support.bluettipower.com/en-us/products/b500k, accessed 2026-10-28). BLUETTI sold an "AC200L + B500K" bundle and still sells "B500K for AC300/AC200L".
   - **Safe line:** 7,577.6 Wh with 2× B300K. Mention 12,288 Wh with 2× B500K as "per BLUETTI's B500K FAQ".
2. **"80% in 45 min"** is BLUETTI's Turbo-mode claim (manual §7.1, spec page, Amazon). The manual's own spec table says **0–80% in 60 min** at 25 °C. The spec page adds that **2,400 W needs the optional 20 A plug (US/Canada)**. With the included 15 A cable the default grid-input limit is 15 A (manual §9.9; about 1,800 W at 120 V).
3. **"Full ~1.5 h" (AC)** is confirmed by the spec page ("AC (2,400W): 1.5 Hours"). It carries the same 20 A plug condition.
4. **"3,000+ cycles to 80%"** is confirmed by the spec page.
5. **Solar full charge:** the spec page says 2.5 h at 1,200 W; the manual says about 2.4 h.
6. **Height 366 mm** → the manual says 366.5 mm (trivial).
7. **UPS 20 ms** matches the manual and the support FAQ. BLUETTI's own Amazon listing says "≤10ms UPS" (Amazon B0CLGZB3L6, accessed 2026-10-28), and TechRadar repeats 10 ms (2026-02-23). Keep 20 ms and note the conflict.
8. **TT-30 outlet:** There is no separate 30 A rating. It shares the 20 A / 2,400 W inverter limit. Our record does not say this.
9. **Returns wording:** see §4. The policy says the buyer bears "double shipping cost", more than just return shipping.

Everything else in our record matches the manual: 2,048 Wh LFP; 2,400 W / 3,600 W Power Lifting; 4× 120 V + 1× TT-30; 2× USB-C 100 W; 2× USB-A 18 W; 12 V/10 A; 48 V/8 A; solar 1,200 W, 12–145 V, 15 A; AC in 2,400 W; 28.3 kg; app.

---

## 2. Expansion batteries

BLUETTI-stated compatibility. The manual (V3.0) lists B210, B230 and B300 only; B300K and B500K come from the later support FAQs.

| Battery | Capacity | Max with AC200L | System total | Cable | Status / price today (2026-10-28) |
|---|---|---|---|---|---|
| B500K | 5,120 Wh | 2 | 12,288 Wh (2×) | P090A | **Sold.** "B500K for AC300/AC200L" (SKU B500K1-UN-GY-SPFUS-00) $1,799, compare-at $1,999, available. "2*B500K for AC300/AC200L" $3,998, available |
| B300K | 2,764.8 Wh | 2 | 7,577.6 Wh (2×) | P090D | **Sold.** "B300K for AC200L/AC300" $1,099 (cmp $1,199), available. "BLUETTI B300K Expansion Battery" $1,099 (cmp $1,699), available. "2*B300K for AC200L/AC300" $2,398 (cmp $3,198), available |
| B300 | 3,072 Wh | 2 | 8,192 Wh (2×) | n/a | End of Sale (replaced by B300K). Store page $1,399, sold out |
| B210 | 2,150 Wh | 2 | 6,348 Wh (2×) | B210 expansion cable | Store page $1,499, sold out. Not on the discontinued list |
| B230 | 2,048 Wh | 1 | 4,096 Wh | n/a | End of Sale (replaced by B300K). Store page $999, sold out |

- **Mixing rules (BLUETTI FAQs):**
  - The AC200L can mix only B300 and B300K (source: https://support.bluettipower.com/en-us/products/b300k, accessed 2026-10-28).
  - The B500K FAQ says the AC200L can mix only with B300, B300K and B500K (source: https://support.bluettipower.com/en-us/products/b500k, accessed 2026-10-28).
  - The manual caps it at two packs (two B210/B300, or one B230; manual p.24).
  - The screen shows up to two battery icons (manual p.15).
- Third-party batteries are not compatible (support FAQ, https://support.bluettipower.com/products/ac200l, accessed 2026-10-28).
- **Conflict:** the BLUETTI spec page lists only B210 / B230 / B300 / B300K ("2kWh to 7.6kWh"). It omits the B500K that the B500K FAQ and the store's "B500K for AC300/AC200L" SKU support. Connecting a B210 needs a separately sold P090D-to-aviation cable (spec page).
- Capacity table source: support FAQ "How many expansion batteries can I connect with the AC200L?" (2× B210 = 6,348 Wh; 1× B230 = 4,096; 2× B300 = 8,192; 2× B300K = 7,577.6). Same URL.
- **Store sources:**
  - Each product: `https://www.bluettipower.com/products/<handle>.js` for b500k-for-ac300-ac200l, b500k-2-for-ac300-ac200l, b300k, bluetti-b300k-expansion-battery, bluetti-b300k-expansion-battery-5-529-6wh, b300, b210, b230-battery-pack.
  - Product search: https://www.bluettipower.com/search/suggest.json?q=AC200L.
  - All accessed 2026-10-28.
- **AC200L bundles on BLUETTI US today, all sold out:**
  - "AC200L + B500K" (7,168 Wh), variant 47914969039067, $2,699.
  - "AC200L+2*B300K" $2,999.
  - "AC200L + Charger 2" $1,149 (cmp $1,299).
  - A second standalone listing, handle `ac200l-portable-power-station`, at $899.
  - Source: `/variants/47914969039067.js` and `/products/<handle>.js`, accessed 2026-10-28.
- B300K product copy: "3+1 Years Warranty", with a registration link for the extra year, and "4,000+ Life Cycles" (source: https://www.bluettipower.com/products/bluetti-b300k-expansion-battery.js, accessed 2026-10-28). The warranty table lists the B300K at 48 months.
- Whether the P090A / P090D cable is included with the "for AC300/AC200L" B500K / B300K SKUs: **unverified**.

---

## 3. Firmware and app

- **No public changelog was found** on bluettipower.com or the support site.
  - Firmware is delivered through the BLUETTI app (support FAQ). Sometimes support pushes it to a specific serial number on request.
  - One owner reports the BMS/DSP upgrade appears only over Bluetooth, not over Wi-Fi/cloud (forum, 2024-05-24).
- **Known issues and fixes**, all from BLUETTI's old community forum. It now redirects to forum.bluettipower.com, so the threads were read from Wayback copies:
  - **PV relay clicking at sunrise/sunset (US unit).** BLUETTI_CARE told the owner to update to **DSP 2098.15** "for a relay switch issue" (2024-05-20).
  - **Fan cycling on ~25 s every minute at low load.** BLUETTI_CARE: "no suitable firmware" for this yet (2024-05-31). Versions reported in that thread: DSP v2098.10, BMS v1043.11, ARM v1034.03, IoT v9041.06.
  - Source for both: https://web.archive.org/web/20250803091758/https://community.bluettipower.com/t/ac200l-pv-relay-and-fan-turning-on-every-minute/28804 (posts dated 2024-05-14 to 2024-05-31).
  - **App statistics outage ("503 … blue-iot data").** BLUETTI said a new IoT firmware fixes it. It was pushed to an Australian unit on IoT v9041.09, and the owner confirmed the fix (source: https://web.archive.org/web/20260120032249/https://community.bluettipower.com/t/ac200l-bluetti-stats-issue/33207, 2024-09-12).
  - **Firmware currency.** BLUETTI_CARE said ARM v2131.04 "is already a very recent firmware" for low-voltage (US) regions. Later 2025 and 2026 requests for current firmware got no public reply (source: https://web.archive.org/web/20260618015931/https://community.bluettipower.com/t/request-for-new-ac200l-firmware/30421, posts 2024-07-01 to 2026-03-09).
  - **B300 compatibility.** A thread reports that B300 packs needed firmware updates one by one to work with the AC200L. The source thread (community.bluettipower.com/t/26732) has no Wayback copy, so this is **unverified**.
- **Connectivity:** Wi-Fi + Bluetooth 5.0/5.1 (manual p.22, 26).
- **App-gated settings:** Turbo/Silent charging, UPS modes, Grid Self-adaption, grid input current (above 15 A needs a CS password) (manual p.20–23).
- **Discontinued-model support:** BLUETTI says some discontinued models can still be upgraded by app or firmware package (source: https://www.bluettipower.com/pages/bluetti-discontinued-models, accessed 2026-10-28). Relevant if the AC200L is later retired.

---

## 4. Warranty and returns (BLUETTI US, read 2026-10-28)

### Warranty length
**AC200L / AC200P L: 60 months.** The same table lists the Elite 200 V2 at 60 months, the B300K at 48, the B230/B300 at 48 and the AC200MAX at 24+24 (source: https://www.bluettipower.com/pages/product-warranty-period, accessed 2026-10-28). The B500K is not in the table.

### Warranty terms
Source for all bullets: https://www.bluettipower.com/pages/warranty-policy, accessed 2026-10-28.
- The warranty covers the original consumer purchaser from the purchase date.
- **Proof of purchase:** a BLUETTI official-store order number, **or** a sales invoice or confirmation email showing the product, price and **sales channel**.
- **Exclusions** include "Purchased from unauthorized resellers", gifts, normal wear and tear, and exposure to excessive heat, cold or liquids.
- The warranty is limited to the country of purchase and is void if the item is taken abroad.
- A claim may be met by repair or by a replacement, which can be refurbished. The replacement carries the remaining warranty or 30 days, whichever is longer.

### Amazon / Walmart purchases
- The policy does not explicitly say that Amazon or Walmart buyers get the same 5 years. It accepts an invoice naming the sales channel and excludes only *unauthorized* resellers.
- BLUETTI's registration form lists Amazon, Walmart, eBay, Home Depot and others as purchase channels (source: https://www.bluettipower.com/pages/register-product, which is where /pages/warranty-extend redirects; accessed 2026-10-28).
- Walmart's AC200L listings were "Sold and shipped by Bluetti Official" (per reviews), and the Amazon listing is BLUETTI's store.
- *Inference:* buyers from those official storefronts get the same 60 months. A third-party seller may not.

### Registration extension
- **None for the AC200L.** The policy says the warranty extension "is now only applicable" to the AC200MAX, AC200P and B230 (warranty-policy page).
- The registration page markets a generic "2-6 year warranty" (register-product page).

### Returns
Source for all bullets: https://www.bluettipower.com/policies/refund-policy, accessed 2026-10-28.
- **30-day money-back.** Items must be complete, unused and in the original package. The buyer is "responsible for the double shipping cost".
  - Option 1: a BLUETTI RMA, with return shipping deducted from the refund.
  - Option 2: a self-paid return.
- Used products may be refused.
- After 30 days, quality issues may get only a partial refund, based on usage time.
- Cancellation within 48 h. A **$25 intercept fee** applies if the order already shipped.
- Refunds are issued within 14 business days of the warehouse receiving the item.
- Distributor purchases follow the distributor's policy.

### Price guarantee
The current sale page says "Find a lower price within 30 days? We'll refund the difference" (source: https://www.bluettipower.com/pages/bluetti-discount, which is where /pages/black-friday redirects; accessed 2026-10-28). The terms were not read in full: **unverified scope**.

---

## 5. Launch and price history

### Launch
- **Created in BLUETTI's US Shopify store** 2023-10-31; current listing republished 2026-02-24 (source: https://www.bluettipower.com/products/ac200l.js, accessed 2026-10-28).
- **US launch:** early-bird price **$1,499**, Nov 17–30, 2023.
  - $1,399 with a publisher code; $2,999 with a B300.
  - Sources: https://9to5toys.com/2023/11/17/bluetti-black-friday-power-station-deals-ac200l/ (2023-11-17) and https://electrek.co/?p=334028 (2023-11-17, marked "Sponsored Post").
  - Neither states an MSRP.
- **Reference prices quoted later:** "recently going for $1,999" (9to5Toys, Aug 2024; **search-result summary only**, page not fetched). $1,599 "regular" (see below). BLUETTI's compare-at today is $1,599.

### Dated price points (standalone unless noted)
| Date | Price | Where | Source |
|---|---|---|---|
| 2023-11-17 | $1,499 early bird ($1,399 with code) | BLUETTI US | 9to5Toys / Electrek, above |
| 2024-08 | $1,139.05 with code | BLUETTI | 9to5Toys, https://9to5toys.com/2024/08/08/bluettis-ac200l-lifepo4-portable-power-station-hits-new-1139-low-860-off-in-latest-sale-more-from-149/. **Search summary only, not fetched** |
| 2024-10-02 | $1,199 | n/a | 9to5Toys, https://9to5toys.com/2024/10/02/bluettis-ac200l-2048wh-lifepo4-power-station-returns-to-1199-low-in-early-fall-prime-day-sale-save-800-more/. **Search summary only** |
| 2025-08-18 | $898.98 (reg. $1,599); the second time at $899, after July 2025 Prime Day | Amazon (BLUETTI storefront) | https://9to5toys.com/2025/08/18/bluetti-ac200l-portable-power-station-899/ (2025-08-18) |
| 2025-12-30 | $799 sale, $751 with code BLUE6OFF | bluettipower.com | https://slickdeals.net/f/19036495-bluetti-ac200l-portable-power-station-2-400w-2-048wh-portable-power-759 (2025-12-30) |
| 2026-02-20 | $749 (reg. $1,599); ~$711.55 with 9TO5TOYS5OFF | BLUETTI member sale | https://9to5toys.com/2026/02/20/bluetti-4-day-member-sale-power-stations-from-399/ (2026-02-20) |
| 2026-02-23 | $749 ("was $1600") | Amazon | https://www.techradar.com/pro/if-youre-looking-for-a-portable-power-station-to-handle-storm-outages-and-camping-trips-i-recommend-the-bluetti-ac200l-its-better-than-half-price-at-under-usd750 (2026-02-23) |
| 2026-06-16 | **$749 (reg. $899), "matched at Amazon"** | BLUETTI Early Prime Day | https://9to5toys.com/2026/06/16/bluetti-early-prime-day-sale-2074wh-elite-200-v2-power-station-759-more/ (2026-06-16). **Confirms the ChatGPT-cited "$749, June 2026, 9to5Toys"** |
| 2026-06-24 | **$699 (reg. $899)**, listed under "clearance deals"; sale ran "through Friday" | BLUETTI direct | https://electrek.co/2026/06/24/bluetti-prime-day-power-stations-segway-navimow-robot-mower-more/ (2026-06-24) |
| 2026-07-20 | $854.05 with 9TO5TOYS5OFF (base $899) | BLUETTI | https://9to5toys.com/2026/07/20/bluetti-july-member-day-sale-exclusive-power-stations-batteries-solar-panels-from-189/ (2026-07-20) |
| 2026-10-28 | **$899, compare-at $1,599, available** on the noindex listing. The canonical listing shows $899 / cmp $899 and "Discontinued" | BLUETTI US | https://www.bluettipower.com/products/ac200l.js; …/ac200l-portable-power-station.js (accessed 2026-10-28, 08:36–08:39 UTC) |

- **Lowest standalone price found:** $699 (BLUETTI direct, 2026-06-24).
- **camelcamelcamel:** returned 403, so not verified. A search summary said it showed a $699 third-party low on 2026-06-23 and $899 on 2026-08-04 (https://camelcamelcamel.com/product/B0CLGZB3L6).
- **Keepa:** not checked.
- **Bundle lows for context:**
  - AC200L + 200 W panel: $999 on Amazon, 2026-06-24 (https://slickdeals.net/f/19675383-bluetti-solar-generator-ac200l-with-200w-solar-panel-999, deal marked expired). Also $1,029 at the Nov 12, 2025 early Black Friday sale (https://9to5toys.com/2025/11/12/bluetti-early-black-friday-sale-new-lows-from-209/).
  - AC200L + B500K (7,168 Wh): $2,298 on 2026-06-16 (9to5Toys link above).

### Black Friday 2026
- **No BLUETTI announcement found** as of 2026-10-28.
- https://www.bluettipower.com/pages/black-friday currently redirects to the Halloween Sale page: "Oct. 24–31 (PDT)", free gifts with $1,000+ orders, 2X Bucks, price guarantee (accessed 2026-10-28). The AC200L is not featured there.
- 2025 precedent: early Black Friday prices posted 2025-11-12 (9to5Toys above). Other dates from search summaries only: BLUETTI's press release gave Nov 15–28, 2025; trackers said Nov 15–Dec 3. **Unverified.**

---

## 6. Availability today (2026-10-28)

| Channel | Status | Source |
|---|---|---|
| BLUETTI US, `/products/ac200l` (noindex, outside the catalog) | **Buyable**: $899 (cmp $1,599), available:true. Free shipping. Policy says 5–7 working days; the site banner says "2–5 Business Days". UPS/FedEx. No shipping to AK, HI, PR, VI, Guam or Majuro. Ship-from location **not stated** ("Free Local Shipping" banner only) | https://www.bluettipower.com/products/ac200l.js; https://www.bluettipower.com/pages/shipping-policy (accessed 2026-10-28) |
| BLUETTI US, canonical `/products/ac200l-portable-power-station` | **"Discontinued"**, OutOfStock, $899 (cmp $899) | `.js` and HTML, accessed 2026-10-28 08:39 UTC |
| BLUETTI US AC200L bundles | **All unavailable:** +B500K ($2,699), +2×B300K ($2,999), +200W ($1,199), +2×200W ($1,598), +350W ($1,499), +Charger 1 ($999), +Charger 2 ($1,149), +200W+Charger 1 ($1,448), +D40 ($1,098), +D40+200W ($1,497). The "20A AC Charging Cable For AC200L" ($49) is also unavailable | https://www.bluettipower.com/collections/all/products.json?limit=250 (accessed 2026-10-28) |
| Amazon (B0CLGZB3L6, BLUETTI Store) | **"Currently unavailable. We don't know when or if this item will be back in stock."** 4.8★ from 534 ratings | https://www.amazon.com/dp/B0CLGZB3L6 (accessed 2026-10-28) |
| Walmart, new (item 5073550009) | **Out of stock.** Reviews say "Sold and shipped by Bluetti Official" | https://www.walmart.com/ip/5073550009 (accessed 2026-10-28) |
| Walmart, Restored (item 5226252728) | **Out of stock** | https://www.walmart.com/ip/5226252728 (accessed 2026-10-28) |
| Home Depot | AC200L **not in search results** for "bluetti ac200l" (first page of 89; Elite 200 V2 shown at $899) | https://www.homedepot.com/s/bluetti%20ac200l (accessed 2026-10-28) |
| Costco | **Unverified**: no listing surfaced in one web search; costco.com not checked directly | n/a |
| Refurbished (US) | None on BLUETTI US (store search "refurbished" returns no AC200L). Walmart Restored is out of stock. A UK refurbished listing exists (shop.bluettipower.com/uk/…) but is not US | https://www.bluettipower.com/search/suggest.json?q=refurbished (accessed 2026-10-28) |

---

## 7. End-of-life status and lineup position

**The AC200L is being phased out by BLUETTI US.** Confirmed 2026-10-28 08:39 UTC; this matches the coordinator's check.

### Status on the store
- **Canonical listing** (https://www.bluettipower.com/products/ac200l-portable-power-station; created 2024-12-15; the URL BLUETTI's own menu and support-site navigation link to):
  - available:false, schema.org OutOfStock;
  - a red **"Discontinued"** label on the base unit and on all 11 bundle options shown;
  - variant metafield `sales_status_discontinued` = "true".
- **Remaining stock is on a hidden page.** The only buyable unit is the older `/products/ac200l` listing: $899, compare-at $1,599, available. That page is `noindex,nofollow`, absent from `/collections/all`, and its product body does not render. *Inference:* this is remaining stock on a page BLUETTI is no longer promoting. It could go out of stock or be removed without notice. **Our /go/ link and AFF5OFF cart test (2026-10-27) use this page.**
- **Bundles:** every AC200L bundle in `/collections/all/products.json` is unavailable (§6).
- **Other retailers:** Amazon (B0CLGZB3L6) shows "Currently unavailable… don't know when or if this item will be back in stock". Walmart new and Restored listings are both out of stock (§6, accessed 2026-10-28).
- **Earlier signals:**
  - The base unit was listed under **"clearance deals"** at $699 on 2026-06-24 (https://electrek.co/2026/06/24/bluetti-prime-day-power-stations-segway-navimow-robot-mower-more/).
  - The manual stayed at V3.0 (file dated 2025-05), and the spec page never added the B500K.
- **Not yet reflected everywhere:** BLUETTI's discontinued-models page does not list the AC200L as of today. It still names the AC200L as the recommended replacement for the AC200P (https://www.bluettipower.com/pages/bluetti-discontinued-models, accessed 2026-10-28).
- **No public BLUETTI statement found** announcing end of sale, by press release, support answer or forum post. WebSearch budget ran out, so this was not searched exhaustively. The old community forum now redirects to forum.bluettipower.com, which did not render for fetches.

### Successor
**BLUETTI Apex 200.**
- **Launch timing:** early access opened 2026-10-21. The press release says the US launch is **Nov 5** and final pricing will be announced then (https://technode.global/?p=995704, 2026-10-21). BLUETTI's own page FAQ says it "is planned to go on sale **November 4, 2026**" (https://www.bluettipower.com/pages/apex-200-expandable-power-station, accessed 2026-10-28).
- **Price:** not announced. The page offers "early pricing details" for subscribers only.
- **Specs:** 2,560 Wh LFP, 3,200 W standalone (up to 3,600 W with expansion or input), B300K/B500K expansion to ~33.3 kWh, up to 3,000 W solar, about 27 kg.
- **RV fit:** built-in **TT-30R** and 12 V/30 A Anderson outputs.
- **What BLUETTI says about the AC200L:** nothing. Neither the press release nor the Apex 200 page mentions the AC200L or uses the word "replacement". The successor reading rests on the overlap (expandable ~2 kWh class, B300K/B500K, TT-30, similar weight) and on the timing next to the AC200L's "Discontinued" status. It is not a BLUETTI statement.

### Not confirmed
- No "AC200L V2" was found.

### Elite 200 V2 at the same price
- **Specs and price:** BLUETTI US $899 (compare-at $899), in stock; 2,600 W, 2,073.6 Wh; 60-month warranty (source: https://www.bluettipower.com/products/elite-200-v2-portable-power-station.js; warranty table above; accessed 2026-10-28).
- **Lineup role:** BLUETTI names it the replacement for the AC200MAX (discontinued page). The AC200L's Amazon copy calls the AC200L the "Upgraded Version of AC200MAX".
- **Status difference:** the Elite 200 V2 is a current, in-stock, indexed product. The AC200L is marked "Discontinued" on its canonical page.
- **AC200L's edge vs Elite 200 V2 at $899:**
  - expansion to 7,577.6 Wh (2× B300K), or 12,288 Wh per the B500K FAQ;
  - TT-30 and 48 V DC outputs;
  - 2,400 W AC + solar input.
- **Elite 200 V2's edge:** 200 W more output (2,600 W) and continuing sale. The AC200L's $1,599 compare-at is a reference price only; both sell at $899.
- Elite 200 V2 expansion and ports: not researched here (another angle).

---

## 8. Side question: who publishes AFF5OFF, and under which network

Our record (src/coupons.json) says: source "BLUETTI's affiliate code (CJ Affiliate)", expires 2030-12-30.

### Public evidence (all accessed 2026-10-28)
- **Feedico coupon aggregator** (https://coupons.feedico.io/bluetti; page data synced 2026-10-28 ~07:30 UTC) lists AFF5OFF three times:
  1. **provider `cj_affiliate`, merchant "Bluetti Global"**, title "Bluetti US EXTRA ENJOY 5% OFF ON SITEWIDE USE CODE:AFF5OFF", ends **2030-12-30** 16:00 UTC. This end date matches our record exactly.
  2. Provider `takedeals`, merchant "BLUETTI US", region US, ends 2030-01-01.
  3. Provider `takeads`, merchant "BLUETTI AU", titled "Baseline Discount".
- **AllCampsAndParks** article dated 2026-04-11 (https://www.allcampsandparks.com/articles/death-valley-backcountry-camping-guide-everything-first-timers-need-to-know):
  - A "Sponsored" block says to use AFF5OFF for an extra 5% off sitewide.
  - It links to a **CJ** tracking URL, `tkqlhce.com/click-101802682-16981946-…`, tagged `data-affiliate-network="cj"` and `data-affiliate-advertiser="bluetti"`. CJ ad ID 16981946's timestamp decodes to 2026-05-29.
- **DIY Solar Forum** mention: AFF5OFF took $20 off an Elite 100 V2 preorder, about mid-2025. The page returned 403, so this is a **search summary only**.
- **No public page attributes AFF5OFF to Awin.**
- **Store tracking:** BLUETTI's US store page loads Awin's Shopify integration (`awin-shopify-integration-code.js?aid=59271`; Awin MID 59271 = BLUETTI US in our links.json) and an Impact `im_ref` cookie handler. No CJ tag is visible in the server HTML (from the HTML of https://www.bluettipower.com/products/ac200l, accessed 2026-10-28).

### Conclusion
- The public trail ties AFF5OFF to **CJ's "Bluetti Global" coupon feed** (plus coupon-feed resellers Takedeals and Takeads), not to Awin. So the "CJ Affiliate" label correctly names where the code is published.
- The real mismatch is that we publish a CJ-feed code next to Awin-tracked links.
- **Cannot be settled from public pages:**
  - whether Awin's BLUETTI US program also lists AFF5OFF in its promotions/voucher feed;
  - whether BLUETTI credits a sale by code or by last click when an Awin click carries a CJ code.
- **Next step:** check the Awin BLUETTI US "Promotions/Vouchers" tab and CJ Bluetti Global's coupon links in the dashboards, or ask the BLUETTI US program manager.

---

## Open questions / couldn't verify
- **End-of-sale statement:** no explicit BLUETTI statement found (press, support, forum). The phase-out rests on the store data in §7. How long the noindex $899 listing stays buyable is unknown.
- **Turbo charging setup:** BLUETTI's spec page says 2,400 W needs the optional 20 A plug. Whether the in-app grid-current limit must also be raised from 15 A (manual §9.9, which needs a CS password) is unconfirmed.
- **Turbo charge time:** the manual contradicts itself, 45 min (§7.1) vs 60 min (spec table) for 0–80%.
- **Expansion maximum:** 7,577.6 Wh on the spec page vs 12,288 Wh in the B500K FAQ.
- **UPS switchover time:** ≤20 ms (manual, support FAQ) vs ≤10 ms (BLUETTI's Amazon listing).
- **Expansion cables:** whether the P090A / P090D cables come with the "for AC300/AC200L" B500K and B300K SKUs.
- **B500K details:** the B500K's warranty term is not in BLUETTI's warranty table.
- **Home integration:** any BLUETTI-sanctioned transfer-switch or home-panel path for the AC200L. None found, and searches ran out.
- **Ship-from location** for BLUETTI US orders.
- **Costco:** listing status (not checked directly).
- **Price history gaps:** 2024 lows ($1,139.05 Aug 2024; $1,199 Oct 2024) and the camelcamelcamel figures are from search summaries, not fetched pages.
- **Black Friday 2026:** dates or AC200L pricing not announced. The 2025 dates come from search summaries.
- **Firmware:** no official changelog exists publicly. The B300-compatibility firmware thread (26732) is not archived.
- **AFF5OFF attribution:** the Awin-side status and how BLUETTI credits the code need a dashboard check (§8).
- **Search budget:** WebSearch ran out late in this session. Items above marked "search summary only" or "unverified" may resolve with a few more searches.
