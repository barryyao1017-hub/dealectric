# ALLPOWERS P1800 (1,024 Wh): use-case math ("how long will it run my X")

Angle 4 (use-case math). Researched 2026-10-28. Every runtime here is an **ESTIMATE**. It is calculated from the inputs in the assumptions table, not measured. Formulas are shown so a reader can swap in their own appliance's number. Ranges run worst to best: worst = low efficiency + high idle draw + high appliance use; best = the reverse.

**Headline (estimates):** usable AC energy is about 820–920 Wh (base 870 Wh) of the 1,024 Wh. ALLPOWERS publishes no idle draw; we assume 8–18 W with the inverter on. With that:

- Full-size ENERGY STAR fridge: **9–19 h (base 12 h)**. Mini fridge: 15–29 h (base 21 h).
- ResMed AirSense 11 with humidifier and heated tube: **1.4–2.7 nights on AC (base 1.9)**, 1.7–3.1 on 12 V DC (base 2.3). Without the humidifier: 3.4–7.7 nights on AC (base 5.2), **5.9–11.6 on DC (base 8.6)**.
- Outage bundle (router + modem 24 h, 3 LED bulbs 5 h, 2 phone charges): 17–38 h (base 25 h). Add a full-size fridge: 6–14 h (base 9 h).
- 1,500 W space heater: **32–37 min**. 750 W: 64–73 min.
- It starts a full-size fridge easily (800–1,200 W start vs 1,800 W continuous) and runs a 1,000 W-cooking microwave (about 1,450 W draw) for about 36 min. A fridge compressor plus that microwave at the same moment can reach 1,850 W, just over the limit.
- One SP037 refills it in **3.4–4.4 hours of good sun**. In an average US day one panel puts 1.2–1.9 kWh into the battery. The **$731 kit (P1800 + 1× SP037)** covers only 22–70% of a fridge + heated-CPAP + router day, and the 1 kWh battery cannot carry that bundle through a 14-hour night even with more panels.

---

## Spec check against ALLPOWERS (what our math depends on)

Sources: US product page (S1), the VOLIX P1800 user manual linked from ALLPOWERS' EU store (S2; the manual covers both 100–120 V and 220–240 V units), the EU product page (S3), and the US kit page (S4). All fetched 2026-10-28.

| Our record | ALLPOWERS says | Match? |
|---|---|---|
| 1,024 Wh LiFePO4 | "1024Wh 51.2V⎓20Ah", LFP (manual) | yes |
| 1,800 W continuous, 3,600 W peak | "Rated Power1800W (peak3600W)", AC output ×4, (100–120) V (manual). Also **"Total AC+DC Output 1800W Max"** | yes. Note the 1,800 W cap is shared with USB and the car port |
| Solar 650 W, XT60, 11–60 V, 13 A | "MPPT(11-60)V⎓13A 650W Max" (manual). US page adds "95V Open-Circuit Voltage" | yes. The 95 V Voc figure appears only on the US page; the manual says keep the panel's voltage "within the range of 11- 60V to avoid damaging the product" |
| AC input up to 1,200 W | Fast 1,200 W / Standard 800 W / Silent 400 W, default Standard (manual). US page says Silent 500 W | yes for fast mode; silent mode differs (400 vs 500 W) |
| 2× USB-C up to 140 W | "5/9/12/15V⎓3A, 20/28⎓5A, 140W*2 Max" (manual, EU page) | yes. 20 V/5 A is supported, which matters for Starlink Mini |
| 12 V car port 120 W | "12V⎓10 A 120W Max" (manual, EU page) | yes |
| UPS | US page "≤10ms"; manual "within 20ms" | conflict. Use 20 ms for medical devices |
| Cycle life | US page "3000+ cycles, ≥70%"; manual "≥4000 cycles with≥70% State of Health" | conflict; not used in this math |
| Kit price | "P1800 + 1x SP037" variant $731.00 (compare-at $1,059.98) (S4) | yes |
| Idle / self-consumption, DoD, efficiency | Not published for the P1800. The R4000 page's FAQ gives ALLPOWERS' own runtime rule: "Runtime = Battery Capacity x Inverter Efficiency ÷ Rated Power", with 85% (S5) | used as our base case |

## Assumptions table (inputs, with sources)

Dates are publication dates where shown; otherwise "acc. 2026-10-28" (accessed).

| # | Input | Value used | Source |
|---|---|---|---|
| A1 | Battery | 1,024 Wh, 51.2 V 20 Ah | S2 VOLIX P1800 user manual, §2 Specifications: https://cdn.shopify.com/s/files/1/0747/3135/6467/files/ALLPOWERS_P1800_User_Manual.pdf?v=1785825984 (file stamped 2026-08-04; linked from S3) |
| A2 | AC conversion factor η (battery → AC, includes DoD) | worst 0.80 / **base 0.85** / best 0.90 | Base: ALLPOWERS' own rule, "3456Wh x 85% ÷ 700 ≈ 4hours", R4000 page FAQ (S5): https://iallpowers.com/products/allpowers-r4000-power-station (acc. 2026-10-28). 0.80 and 0.90 are **our assumption** (typical spread for LFP stations at low vs mid loads) |
| A3 | AC idle draw S (inverter on, no load) | worst 18 / **base 12** / best 8 W | **Our assumption.** ALLPOWERS publishes none and no review measured it. Anchor: BLUETTI's published 12–18 W for its 2,400 W AC200L (see our AC200L dossier, `growth/focus/bluetti-ac200l/research/4-usecase.md`, A6) |
| A4 | DC path (battery → 12 V port / USB-C) | 1,024 × 0.95 × (0.88 / **0.92** / 0.95); DC idle 6 / **4** / 3 W | **Our assumption** (no ALLPOWERS figure) |
| A5 | Full-size ENERGY STAR fridge, 18–28 ft³ | 363 / 549 / 685 kWh/yr (p10 / median / p90, n = 1,611) → 0.99 / 1.50 / 1.88 kWh/day. Medians by type: top-freezer 374, bottom-freezer 588, side-by-side 640 | ENERGY STAR Certified Residential Refrigerators: https://data.energystar.gov/resource/p5st-her9.json (dataset updated 2026-10-28; acc. 2026-10-28) |
| A6 | Mini fridge (compact refrigerator, 2.5–4.5 ft³) | 210 / 250 / 325 kWh/yr (n = 1,000) → 0.58 / 0.68 / 0.89 kWh/day | Same dataset |
| A7 | Fridge / mini-fridge running and starting watts | Fridge 150–400 W running, 800–1,200 W starting. Mini fridge 50–100 W running, 400–600 W starting | Champion Power Equipment, "Generator Wattage Chart", published 2026-04-17: https://www.championpowerequipment.com/generator-wattage-chart/ |
| A8 | AirSense 11 rated draw | 65 W supply, "Typical power consumption 56.1W (111.5VA)", "Peak power consumption 73.2W" | ResMed AirSense 11 user guide (Americas), 398133/2, 2021-10: https://document.resmed.com/documents/products/machine/airsense-11/user-guide/airsense11_user-guide_amer_mul.pdf |
| A9 | ResMed measured draw by setup (AirSense **10**, the closest ResMed-published measurement) | Device only 7 Wh per hour; + humidifier 22; + humidifier + ClimateLineAir 34 (AutoSet 8–15 cm H2O, humidity 6, tube 28 °C, Yokogawa WT110) | ResMed, "Power consumption of Air10 devices", 1018673/1, 2015-03: https://document.resmed.com/documents/products/machine/air10-lumis-series/Power+consumption+Air10+devices.pdf |
| A10 | CPAP draws used | No humidifier 7 / **9** / 12 W; + humidifier 20 / **22** / 30 W; + humidifier + heated tube 34 / **45** / 56 W. 8 h per night | A8 + A9; the ranges are **our assumption** bounded by them |
| A11 | Air11 DC/DC converter | Input "12V/24V 10A/5A", output "24 V, 3,75A"; powers the device with HumidAir and ClimateLineAir | ResMed shop: https://shop.resmed.com/cpap-spare-parts/airsense-11-converter/p/39231 (acc. 2026-10-28). DC draw assumed equal to the AC-side figure (converter loss offsets the AC brick's loss): **our assumption** |
| A12 | Router + modem; LED bulb | Router/modem 10 / **15** / 20 W combined; LED 8 / **10** / 15 W per bulb | Champion chart (A7): "Internet router/modem 10–20W", "LED lights (per bulb) 8–15W" |
| A13 | Phone charge | 15 / **17.5** / 20 Wh per charge, 2 per day | **Our assumption** (4,000–5,000 mAh × 3.85 V plus losses) |
| A14 | Space heater | 1,500 W high, 750 W low | Champion chart (A7), "Space heater 750–1,500W" |
| A15 | Electric blanket | Rated 150 W (Sunbeam Sleep Perfect queen BL5151, AU listing). Average after preheat: 40 / **75** / 150 W (worst = on high all night) | winnings.com.au listing, seen as a search-result snippet; the page blocked our fetch. The average is **our assumption** |
| A16 | Laptop | MacBook Pro 16-inch "100-watt-hour" (fast-charges at 140 W); 14-inch "72.4-watt-hour". Laptop charging efficiency 0.80 / **0.85** / 0.90 (**our assumption**) | Apple, MacBook Pro tech specs: https://www.apple.com/macbook-pro/specs/ (acc. 2026-10-28) |
| A17 | Starlink | Standard "Average: 75 - 100 W" (AC power supply). Mini "Average: 25-40 W", input 12–48 V 60 W, USB PD "100 W, 20V/5A Minimum" | Starlink spec sheets: https://www.starlink.com/public-files/specification_sheet_standard.pdf , https://www.starlink.com/public-files/specification_sheet_mini.pdf (acc. 2026-10-28) |
| A18 | Microwave draw | A "1,000 W" microwave is cooking (output) power. Input is higher: Vollrath 40819 "12.1 Amps for 1450 Watts of input power to produce 1000 Watts"; Winco EMW-1000ST 1,000 W cooking / 1,450 W input; GE JES1288SH 1,000 W output, 1,800 W nameplate at 120 V | Search-result snippets of restaurantsupply.com, chefsdeal.com and canadianappliance.ca (2026-10-28). Not fetched in full (bot wall). Used: 1,450 W |
| A19 | SP037 | 400 W; Vmp 37.4 V, Voc 45.3 V, Imp 10.6 A, Isc 11.45 A (page). Manual: Imp 10.69 A, Isc 11.7 A | https://iallpowers.com/products/allpowers-400w-portable-solar-panel ; manual https://cdn.shopify.com/s/files/1/0443/1223/2089/files/AP-SP-037_400W_Solar_Panel.pdf?v=1671926121 (file stamped 2022-12-24) |
| A20 | SP037 real-world output in good sun | 260 / **290** / 320 W | The SP037 manual's text layer carries "260-320W" next to its connection instructions (context not visible when rendered). Owner reviews on the SP037 page: "almost 300 watts output", "320 watts max … late May in southern Michigan" |
| A21 | Solar yield per SP037 | PVWatts v8 DC output, 0.4 kW, fixed 35° south, 14.08% losses (PVWatts default), NSRDB TMY: Phoenix, Los Angeles, Denver, Miami. Seven more cities from NASA POWER latitude-tilt irradiance × our derate fit (see the SP037 dossier §3) | https://developer.nlr.gov/api/pvwatts/v8.json (v8.5.0, called 2026-10-28; DEMO_KEY hit its rate limit after 4 cities). https://power.larc.nasa.gov/api/temporal/climatology/point (v2.10.1, 2001–2025 climatology) |
| A22 | MPPT + battery charge efficiency | 0.90 / **0.93** / 0.95 | **Our assumption** (not published) |
| A23 | Night length the battery must bridge | 14 h (base) | **Our assumption.** With a fridge running, solar exceeds the load only for the middle 8–12 h of the day |

### Three cases used throughout

- **Worst:** U = 1,024 × 0.80 = **819 Wh** AC; S = 18 W.
- **Base (ALLPOWERS' own 85% rule):** U = 1,024 × 0.85 = **870 Wh** AC; S = 12 W.
- **Best:** U = 1,024 × 0.90 = **922 Wh** AC; S = 8 W.
- DC: U_dc = 1,024 × 0.95 × (0.88 / 0.92 / 0.95) = **856 / 895 / 924 Wh**; S_dc = 6 / 4 / 3 W.

---

## 1. Usable energy (AC vs DC path)

**Formula (ESTIMATE):** hours = U ÷ (load W + S). For cycling loads: days = U ÷ (daily Wh + 24 × S).

| Path | Usable energy (ESTIMATE) | Idle draw (assumed) | Idle alone empties a full battery in |
|---|---|---|---|
| AC (inverter on) | 819–922 Wh (base 870) | 8–18 W (base 12) | 1.9–4.8 days (base 3.0) |
| DC (car port / USB-C, inverter off) | 856–924 Wh (base 895) | 3–6 W (base 4) | 5.9–12.8 days (base 9.3) |

**Generic AC runtime (ESTIMATE, hours = U ÷ (P + S)):**

| Load | Worst | Base | Best |
|---|---|---|---|
| 50 W | 12.1 h | 14.0 h | 15.9 h |
| 100 W | 6.9 h | 7.8 h | 8.5 h |
| 200 W | 3.8 h | 4.1 h | 4.4 h |
| 500 W | 1.6 h | 1.7 h | 1.8 h |
| 1,000 W | 48 min | 52 min | 55 min |
| 1,500 W | 32 min | 35 min | 37 min |
| 1,800 W | 27 min | 29 min | 31 min |

**What this means.** At small loads the assumed idle draw is a big share: 12 W is 24% on top of a 50 W load. Anything that can run from the 12 V port or USB-C (CPAP via the ResMed converter, Starlink Mini, laptops, a 12 V router) gets 10–60% more hours with the inverter off.

## 2. Refrigerator and mini fridge

**Formula:** days = U ÷ (daily Wh + 24 × S).

| Appliance | Daily use (p10 / median / p90) | Runtime, ESTIMATE |
|---|---|---|
| Full-size ENERGY STAR fridge (18–28 ft³) | 0.99 / 1.50 / 1.88 kWh | **9–19 h (base 12 h)** |
| Mini fridge (2.5–4.5 ft³) | 0.58 / 0.68 / 0.89 kWh | **15–29 h (base 21 h)** |

Worked example (full-size, base): 870 ÷ (1,504 + 24 × 12) = 870 ÷ 1,792 = 0.49 days = 11.7 h.

By style (base, median kWh/yr from A5): top-freezer 374 kWh/yr → 870 ÷ (1,025 + 288) = 0.66 days ≈ **16 h**; side-by-side 640 kWh/yr → 870 ÷ (1,753 + 288) = 0.43 days ≈ **10 h**.

**Can it start a full-size fridge?** Yes, with margin. The chart's 800–1,200 W starting figure (A7) is under the 1,800 W continuous rating, before the 3,600 W peak comes into play. Daily kWh is the limit here, not surge.

## 3. CPAP: nights at 8 h per night

**Formulas (ESTIMATE):**
- AC, station switched off between nights: nights = U ÷ ((P + S) × 8).
- AC, station left on 24 h: nights = U ÷ (P × 8 + S × 24).
- DC (car port → ResMed Air11 DC/DC converter): nights = U_dc ÷ ((P + S_dc) × 8). The car port's 120 W matches the converter's 12 V 10 A input (A11).

| AirSense 11 setup | Draw (A10) | AC, off between nights | AC, left on 24 h | DC via 12 V port |
|---|---|---|---|---|
| No humidifier | 7–12 W (base 9) | 3.4–7.7 (base 5.2) | 1.6–3.7 (base 2.4) | **5.9–11.6 (base 8.6)** |
| + humidifier | 20–30 W (base 22) | 2.1–4.1 (base 3.2) | 1.2–2.6 (base 1.9) | 3.0–5.0 (base 4.3) |
| + humidifier + heated tube | 34–56 W (base 45) | **1.4–2.7 (base 1.9)** | 0.9–2.0 (base 1.3) | 1.7–3.1 (base 2.3) |

**What this means.** Humidification is the big lever: turning it off roughly triples the nights. The DC path beats AC by 20–65%, because it skips the assumed inverter idle. Leaving the station on all day costs a third of the battery for nothing.

**UPS caveat.** The manual says the switch to battery happens "within 20ms"; the US page says ≤10 ms. ResMed does not say how long the AirSense 11 rides through a gap. For outages, running the CPAP from the battery all night is safer than relying on the UPS switchover. Not verified.

## 4. Outage bundle: router + modem + lights + phones

Daily Wh = router/modem × 24 h + 3 LED bulbs × 5 h + 2 phone charges.
Low / base / high = 240 + 120 + 30 = **390**; 360 + 150 + 35 = **545**; 480 + 225 + 40 = **745 Wh/day**.

| Bundle | Runtime, ESTIMATE |
|---|---|
| Router/modem + 3 LEDs + 2 phones | **0.70–1.58 days (base 1.04 days ≈ 25 h)** |
| Same + full-size fridge (1,385 / 2,049 / 2,622 Wh/day) | **6–14 h (base 9 h)** |

Many routers and modems run on 12 V DC. Powering them from the car port with DC cords saves the inverter idle (not tested here).

## 5. Heat: space heater and electric blanket

| Load | Runtime, ESTIMATE | Formula |
|---|---|---|
| 1,500 W space heater, continuous | **32–37 min (base 35 min)** | U ÷ (1,500 + S) |
| 1,500 W heater cycling 50% on its thermostat, or 750 W setting | 64–73 min (base 68 min) | U ÷ (750 + S) |
| Electric blanket (queen, rated 150 W) | **0.6–2.4 nights (base 1.3)** at 8 h | U ÷ ((avg W + S) × 8), avg 150 / 75 / 40 W |

A 1,500 W heater fits under the 1,800 W limit, but the battery lasts about half an hour. The blanket is the efficient way to stay warm on this unit.

## 6. Laptops and Starlink

| Load | Runtime, ESTIMATE | Formula |
|---|---|---|
| MacBook Pro 16 (100 Wh) via USB-C 140 W | **6.8–8.3 full charges (base 7.6)** | U_dc ÷ (100 ÷ η_laptop), η 0.80 / 0.85 / 0.90 |
| MacBook Pro 14 (72.4 Wh) | 9.5–11.5 charges (base 10.5) | same |
| Starlink Mini on USB-C (20 V/5 A PD) | **19–33 h (base 24.5 h)** | U_dc ÷ (40 / 32.5 / 25 W + S_dc) |
| Starlink Mini on AC | 14–28 h (base 20 h) | U ÷ (P + S) |
| Starlink Standard (AC only) | **6.9–11.1 h (base 8.8 h)** | U ÷ (100 / 87.5 / 75 W + S) |

Starlink Mini's spec asks for USB PD "100 W, 20V/5A Minimum"; each P1800 USB-C port lists 20 V/5 A and 140 W, so it qualifies on paper (not tested).

## 7. Surge questions: fridge and microwave

| Question | Numbers | Answer (ESTIMATE) |
|---|---|---|
| Start a full-size fridge? | 800–1,200 W starting (A7) vs 1,800 W continuous / 3,600 W peak | **Yes**, with margin |
| Run a 1,000 W microwave? | Cooking 1,000 W ≈ 1,450 W input (A18) vs 1,800 W | **Yes.** Battery lasts 0.56–0.63 h (base 36 min) of cooking. 10 min of reheating ≈ 240 Wh, about a quarter of the battery |
| Run a 1,200–1,250 W-cooking microwave? | Nameplates around 1,800 W at 120 V (A18) | **At the limit; may trip.** Check the label's input watts, not the cooking watts |
| Microwave while the fridge compressor runs? | 1,450 + 150–400 W = 1,600–1,850 W vs 1,800 W total AC+DC | **Usually fine, can trip** at the top of the range |
| 1,500 W space heater? | 1,500 W vs 1,800 W | Yes, for about 35 min |

ALLPOWERS does not say how long the 3,600 W peak can be held, so motor loads above 1,800 W running are out of scope.

## 8. Solar refill with SP037 (summary; full math in the SP037 dossier)

**Panels per input.** The P1800 has one XT60 input: 11–60 V, 13 A, 650 W.
- One SP037: Voc 45.3 V rises to about 51.6 V at −10 °C and 56.6 V at −40 °C (NEC Table 690.7 factors 1.14 and 1.25). Under 60 V. Fine.
- Two in series: Voc 90.6 V. That is over the manual's 60 V limit. The US page's "95V Open-Circuit Voltage" would also be exceeded on any morning below about 9 °C (at −0.30 %/°C) or below 15 °C using the NEC table's factors. **Don't.**
- Two in parallel: Voc 45.3 V, but Isc 22.9–23.4 A against a 13 A input. Works only if the input limits current rather than faulting. ALLPOWERS sells its SP039 (Isc 14.99 A, Imp 13.63 A) with the P1800, which suggests the input does limit; it never says so. Output caps near 13 A × 35–38 V ≈ **455–494 W**.

| Panels | Input in good sun | Hours of good sun, 0–100% (ESTIMATE) | Average US day (11-city mean) |
|---|---|---|---|
| 1 SP037 | 260–320 W | **3.4–4.4 h (base 3.8 h)** | 1.51 kWh into battery → 0.68 days |
| 2 SP037 in parallel | 455–494 W (13 A cap) | **2.2–2.5 h (base 2.3 h)** | 2.97 kWh → 0.35 days |
| 3 or 5 SP037 | still 455–494 W | no faster in good sun | not a configuration ALLPOWERS documents; skip |

Formula: hours = 1,024 ÷ (input W × η_c), η_c = 0.90 / 0.93 / 0.95.

## 9. Kit math: P1800 + 1× SP037 ($731)

**Daily need (battery side, base):** need = (fridge + CPAP + router 24 h + 24 × S) ÷ η.

| Day | Loads (base) | Need from battery | Overnight (14 h) from battery, AC side | Fits in 870 Wh? |
|---|---|---|---|---|
| A. Full-size fridge + heated CPAP + router | 1,504 + 360 + 360 + 288 Wh | **2,955 Wh/day** | 1,615 Wh | **No.** Empty after about 7.5 h of night |
| B. Top-freezer fridge + CPAP no humidifier + router | 1,025 + 72 + 360 + 288 | 2,053 Wh/day | 1,048 Wh | No |
| C. Mini fridge + CPAP no humidifier + router | 685 + 72 + 360 + 288 | **1,653 Wh/day** | 850 Wh | Just (base) |

**One SP037 into the battery (base, η_c 0.93), kWh/day by season, and the share of day A and day C it covers:**

| City (data) | Winter | Spring | Summer | Fall | Covers day A | Covers day C |
|---|---|---|---|---|---|---|
| Phoenix (PVWatts) | 1.76 | 2.08 | 1.89 | 1.90 | 59–70% | 106–126% |
| Los Angeles (PVWatts) | 1.56 | 1.85 | 1.99 | 1.84 | 53–67% | 95–120% |
| Denver (PVWatts) | 1.56 | 1.89 | 1.86 | 1.74 | 53–64% | 94–114% |
| Miami (PVWatts) | 1.63 | 1.75 | 1.51 | 1.61 | 51–59% | 91–106% |
| Dallas (NASA) | 1.28 | 1.54 | 1.68 | 1.49 | 43–57% | 77–102% |
| Atlanta (NASA) | 1.23 | 1.60 | 1.52 | 1.46 | 42–54% | 74–97% |
| Kansas City (NASA) | 1.17 | 1.50 | 1.64 | 1.41 | 39–56% | 71–99% |
| Chicago (NASA) | 0.90 | 1.43 | 1.56 | 1.22 | 31–53% | 55–94% |
| New York (NASA) | 1.04 | 1.47 | 1.52 | 1.24 | 35–51% | 63–92% |
| Minneapolis (NASA) | 1.11 | 1.48 | 1.61 | 1.22 | 38–54% | 67–97% |
| Seattle (NASA) | 0.66 | 1.28 | 1.62 | 1.06 | 22–55% | 40–98% |

Seasons are Dec–Feb, Mar–May, Jun–Aug, Sep–Nov. Coverage ranges span the four seasons. Panel-output uncertainty is about ±10% (NASA vs NSRDB differences, real-world foldable-panel losses), and η_c moves it ±3%.

**What this means for the kit.**
- With a full-size fridge and a heated CPAP, the kit is a **partial** solution everywhere: the panel replaces a third to two thirds of each day's use, and the battery runs out around 1–2 a.m. if it starts full at sunset.
- A second SP037 in parallel (≈ $299 more) lifts daily solar to 2.3–3.6 kWh (annual average by city). That meets day A's 2,955 Wh in Phoenix, Los Angeles, Denver, Miami and Dallas, not in the other six cities. It does not fix the night: day A needs 1,615 Wh after dark, almost twice the P1800's usable 870 Wh. **No number of panels makes a P1800 carry a full-size fridge plus CPAP through the night** (base case).
- What the kit *does* sustain: a mini fridge (or 12 V cooler) + CPAP without humidifier + router. One panel covers 91–126% of that day year-round in Phoenix, Los Angeles, Denver and Miami, 64–102% from spring to fall in the other seven cities, and 40–77% in their winters. Its night need (850 Wh) just fits the battery (base).

---

## Summary table (all ESTIMATES, base in bold)

| Use | Runtime / result |
|---|---|
| Usable energy | AC 819–922 Wh (**870**); DC 856–924 Wh (**895**) |
| Full-size ENERGY STAR fridge | 9–19 h (**12 h**) |
| Mini fridge | 15–29 h (**21 h**) |
| AirSense 11, no humidifier | AC 3.4–7.7 nights (**5.2**); DC 5.9–11.6 (**8.6**) |
| AirSense 11 + humidifier + heated tube | AC 1.4–2.7 nights (**1.9**); DC 1.7–3.1 (**2.3**) |
| Router + modem + 3 LEDs + phones | 17–38 h (**25 h**) |
| Same + full-size fridge | 6–14 h (**9 h**) |
| 1,500 W heater / 750 W | 32–37 min (**35**) / 64–73 min (**68**) |
| Electric blanket | 0.6–2.4 nights (**1.3**) |
| MacBook Pro 16 charges (USB-C) | 6.8–8.3 (**7.6**) |
| Starlink Mini (USB-C) / Standard (AC) | 19–33 h (**24.5**) / 6.9–11.1 h (**8.8**) |
| Microwave, 1,000 W cooking (≈1,450 W draw) | Runs; 34–38 min of cooking (**36**) |
| Start full-size fridge | Yes |
| 1× SP037 refill | 3.4–4.4 h of good sun (**3.8**); 0.5–0.9 average days by city |
| 2× SP037 (parallel) refill | 2.2–2.5 h of good sun (**2.3**) |
| $731 kit vs fridge + heated CPAP + router day | Covers 22–70% of the day; battery can't bridge the night |

## Open questions / couldn't verify

- **Idle draw and real efficiency.** ALLPOWERS publishes neither for the P1800, and no review with a measured capacity test turned up. Our 8–18 W idle and 80–90% factor are assumptions. One measured number (watt meter, AC on, no load) would tighten every runtime here, most of all the fridge and CPAP rows.
- **95 V Voc.** Only the US product page lists a 95 V open-circuit limit. The manual (and EU page) say 11–60 V. We treat 60 V as the rule.
- **Parallel panels on a 13 A input.** Whether the P1800 current-limits or faults when the array's Isc (23 A for 2× SP037) exceeds 13 A is not stated. The SP039 pairing suggests it limits. Ask ALLPOWERS support before publishing "two panels in parallel" as advice.
- **UPS switchover**: 10 ms (page) vs 20 ms (manual). AirSense 11 ride-through is not published by ResMed.
- **ECO / auto-off.** The P1800 manual pages we read show no power-saving timer. The R4000 has one (shuts off below 10 W after 1–6 h). If the P1800 has a similar default, a CPAP or a fridge between cycles could be cut off. Not verified.
- **AirSense 11 draw** uses ResMed's AirSense 10 measurements (7 / 22 / 34 Wh per hour) as a proxy. ResMed's AirSense 11 figure (56.1 W typical) is the top of our range.
- **Microwave and blanket figures** come from search-result snippets; the pages blocked direct fetches.
- **Solar for 7 of 11 cities** uses NASA POWER irradiance with a derate fitted to PVWatts (fit residual ±1.7%; annual totals within −6% to +6% of PVWatts for the 4 check cities). PVWatts' DEMO_KEY rate limit stopped us after 4 cities.
