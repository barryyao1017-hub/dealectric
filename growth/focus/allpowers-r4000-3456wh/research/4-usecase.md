# ALLPOWERS R4000 (3,456 Wh): use-case math ("how long will it run my X")

Angle 4 (use-case math). Researched 2026-10-28. Every runtime here is an **ESTIMATE**. It is calculated from the inputs in the assumptions table, not measured. Formulas are shown so a reader can swap in their own appliance's number. Ranges run worst to best: worst = low efficiency + high idle draw + high appliance use; best = the reverse.

**Headline (estimates):** usable AC energy is about 2,770–3,110 Wh (base 2,940 Wh). ALLPOWERS publishes no idle draw; we assume 15–35 W for the 3,600 W inverter. With that:

- Full-size ENERGY STAR fridge: **24–55 h (base 34 h, 1.4 days)**. Fridge + router + lights + phones: 19–43 h (base 27 h).
- AirSense 11 with humidifier and heated tube: **3.8–7.9 nights on AC (base 5.2)**, 5.6–10.3 on 12 V DC (base 7.4). Without the humidifier on DC: 18–35 nights (base 25).
- Whole-house essentials, summer (fridge + freezer + 1/2 HP sump + router + lights): **10–27 h (base 15 h)**. Winter with a furnace blower instead of the sump: **4–18 h (base 8 h)**. Surges fit: the worst coincident start we model is about 4,700 W vs the 6,000 W peak.
- 13,500 BTU RV rooftop AC: **1.4–2.1 h of continuous compressor time (base 1.75 h)**, about 3.5 h at 50% duty. Its locked-rotor current (61–63 A, about 7.5 kVA) is above the 6,000 W peak, so **plan on a soft starter**.
- 1,500 W space heater: **1.8–2.1 h**. Induction cooktop at 1,800 W: 1.5–1.7 h, or 3–6 meals. EV Level 1 (1,440 W): about 2 h, **5.5–10.7 miles** (base 7.5).
- 120 V only. No 240 V well pumps, ranges or dryers. A 120 V 1/2 HP well pump runs 2.7–4.1 h of pumping.
- Solar: SP037 fits one per XT60 input in series terms (three inputs). Three panels refill it in **3.8–4.9 h of good sun**, or about 0.8 of an average US day. With SP037s it never gets near the 2,000 W solar rating: about 1,350–1,500 W is the ceiling with six panels in parallel pairs.

---

## Spec check against ALLPOWERS (what our math depends on)

Sources: US product page (S1) and the R4000 user manual V3.0 linked from it (S2). Both fetched 2026-10-28. The page contradicts itself in several places; where it does, we use the manual.

| Our record | ALLPOWERS says | Match? |
|---|---|---|
| 3,456 Wh LiFePO4 | "3456Wh (48V 72Ah)", LFP (manual); page same | yes |
| 3,600 W continuous at 120 V, 6,000 W peak | Manual: "AC : 100-120V Total output 3600W Max ( peak 6000W Max)"; 4,000 W applies to the 220–240 V version. Page title and FAQ say "4000W AC output (6000W peak)"; page spec table says "Inverter 3600W" | yes. **The page's "4000W" is the 230 V model**; US buyers get 3,600 W |
| 4 AC outlets + RV outlet | Manual figure: "AC Output *4 (US 20A Max)" and "RV Port 30A". The drawing shows a round three-slot receptacle consistent with a NEMA TT-30R; the manual never names the NEMA type. Page spec: "RV output 100V-120V 3000W" | yes. TT-30R is our reading of the drawing; the page caps the RV port at 3,000 W |
| Solar 2,000 W over 3 XT60, 650 W each, 12–60 V, 13 A | Manual: "Solar*3: (12~60)V 13A, Single port 650W Max, three ports 2000W Max"; "confirm that the output specification of the solar panel corresponding to a single XT60 interface is within 60V to avoid damage". Page also says "12 -150V MPPT 40A Max" in one row and "12 -60V" in another | yes. **The page's 12–150 V row is wrong per the manual**; use 60 V |
| AC input 2,000 W | Manual: Fast mode "100-120V 1500W / 220-240V 2000W"; Standard 1,000 W; Mute 650 W (default). Page: "AC input 2000W max" and "110-120V 12.5A" (= 1,500 W) | **differs for the US**: 1,500 W at 120 V |
| AC + solar | "AC+Solar: 3000W Max" | not in our record |
| UPS | "within 15ms". Pass-through on 100–120 V must stay ≤1,500 W, otherwise the battery supplements "until the power station consumes to 5%" | not in our record |
| DC outputs | USB-C ×2 "Single port 100W Max" (20 V 5 A); USB-A 2× 12 W + 2× 18 W; car port "12V 10A, 120W Max" | not in our record |
| Power-saving mode | "if the output power continues to be <10W, it will shut down after the set time (1 hour, 2 hours , 4 hours, 6 hours)"; normal mode never auto-shuts | not in our record. Use normal mode for a fridge or CPAP |
| Idle / DoD / efficiency | Not published. Page FAQ: "Runtime = Battery Capacity x Inverter Efficiency ÷ Rated Power", "3456Wh x 85% ÷ 700 ≈ 4hours" | used as our base case |
| Weight | Page 99.2 lb / 45 kg; manual "Approximately 45KG (106lbs)" | minor conflict |

## Assumptions table (inputs, with sources)

Dates are publication dates where shown; otherwise "acc. 2026-10-28" (accessed).

| # | Input | Value used | Source |
|---|---|---|---|
| A1 | Battery and ports | as in the spec check | S1 https://iallpowers.com/products/allpowers-r4000-power-station (acc. 2026-10-28); S2 manual V3.0: https://cdn.shopify.com/s/files/1/0443/1223/2089/files/allpowers_R4000-AP-R4000_USER_MANNUAL-V3.0-_compressed_1.pdf?v=1712547934 (file stamped 2024-04-08) |
| A2 | AC conversion factor η (battery → AC, includes DoD) | worst 0.80 / **base 0.85** / best 0.90 | Base: ALLPOWERS' FAQ rule on S1. 0.80 and 0.90 are **our assumption** |
| A3 | AC idle draw S | worst 35 / **base 25** / best 15 W | **Our assumption.** ALLPOWERS publishes none; two searches found no measurement. Anchor: BLUETTI's 12–18 W for a 2,400 W inverter (our AC200L dossier, A6); a 3,600 W inverter is assumed to idle higher |
| A4 | DC path | 3,456 × 0.95 × (0.88 / **0.92** / 0.95); DC idle 8 / **6** / 4 W | **Our assumption** |
| A5 | Full-size ENERGY STAR fridge, 18–28 ft³ | 363 / 549 / 685 kWh/yr (p10 / median / p90, n = 1,611) → 0.99 / 1.50 / 1.88 kWh/day | ENERGY STAR Certified Residential Refrigerators: https://data.energystar.gov/resource/p5st-her9.json (updated 2026-10-28) |
| A6 | Mini fridge (2.5–4.5 ft³) | 210 / 250 / 325 kWh/yr → 0.58 / 0.68 / 0.89 kWh/day | Same dataset |
| A7 | Freezer | Chest median 213 kWh/yr (n = 5, small sample); upright 5–15 ft³ median 396, p90 472 (n = 249). Used 0.58 / 1.09 / 1.29 kWh/day | ENERGY STAR Certified Residential Freezers: https://data.energystar.gov/resource/8t9c-g3tn.json (updated 2026-10-28) |
| A8 | Running / starting watts | Fridge 150–400 / 800–1,200. Freezer 100–500 / 500–1,000. Furnace fan 1/2 HP 300–800 / 800–1,600. Sump 1/2 HP 800–1,050 / 1,300–2,150. Well pump 1/2 HP 750–1,000 / 1,500–2,000. Window AC 5,000 BTU 450–600 / 900–1,200; 10,000 BTU 900–1,200 / 1,800–2,400. RV AC 13.5K 1,500–2,000 / 2,800–3,500; 15K 2,000–2,500 / 3,500–4,500. Induction cooktop 1,200–1,800. Router/modem 10–20; LED 8–15 per bulb. Tools: circular saw 1,200–1,800 / 2,400–3,600; table saw 10" 1,800–3,000 / 3,600–6,000; miter saw 1,200–1,800 / 2,400–3,600; 1 HP compressor 1,500 / 4,500; 2 HP 2,500 / 7,500; 120 V welder 1,800–2,500 / 3,600–5,000 | Champion Power Equipment, "Generator Wattage Chart", published 2026-04-17: https://www.championpowerequipment.com/generator-wattage-chart/ |
| A9 | Duty assumptions | Sump runs 0.5 / **1** / 2 h a day (wet weather). Furnace blower 6 / **10** / 14 h a day in a cold-weather outage. Well pump 0.5 / **1** / 1.5 h a day | **Our assumptions** |
| A10 | CPAP | AirSense 11 no humidifier 7 / **9** / 12 W; + humidifier 20 / **22** / 30 W; + humidifier + heated tube 34 / **45** / 56 W; 8 h nights | ResMed AirSense 11 user guide (398133/2, 2021-10): "Typical power consumption 56.1W", https://document.resmed.com/documents/products/machine/airsense-11/user-guide/airsense11_user-guide_amer_mul.pdf ; ResMed "Power consumption of Air10 devices" (1018673/1, 2015-03): 7 / 22 / 34 Wh per hour, https://document.resmed.com/documents/products/machine/air10-lumis-series/Power+consumption+Air10+devices.pdf |
| A11 | Air11 DC/DC converter | Input 12 V 10 A / 24 V 5 A; output 24 V 3.75 A | https://shop.resmed.com/cpap-spare-parts/airsense-11-converter/p/39231 (acc. 2026-10-28) |
| A12 | Window AC efficiency | Every ENERGY STAR 115–120 V window unit in 7,500–15,000 BTU is variable-speed; CEER median 15.0 (8,000 BTU: p10 13.7, p90 16.0). 8,000 BTU ÷ 15.0 = 533 W at rated load | ENERGY STAR Certified Room Air Conditioners: https://data.energystar.gov/resource/5xn2-dv4h.json (updated 2026-10-28) |
| A13 | Dometic Penguin II 13.5K | Compressor rated-load 12.5–12.6 A, **locked-rotor 61–63 A**; fan 2.6–3.5 A. Dometic's minimum generator "3.5 kW / 5.0 kW" | Dometic installation instructions, Form No. 3314438.000 8/18: https://www.dometic.com/externalassets/dometic-penguin-ii-13-5k_63522.pdf |
| A14 | RV AC running watts used | 13.5K: 1,450 / **1,650** / 2,000 W. 15K: 1,560 / **1,800** / 2,500 W | A8, A13 (15.1–16.1 A × 120 V × assumed PF 0.9). 1,450 W owner reading and Coleman Mach 15's 1,560–1,611 W come from our AC200L dossier (A23, A25; retailer and forum pages, not re-fetched here) |
| A15 | Soft starter | Micro-Air EasyStart: "Can reduce your current by up to 75%" | https://www.micro-air.com/products_easystart_364_softstarter_microair.cfm (acc. 2026-10-28) |
| A16 | EV efficiency | EPA combined kWh/100 mi, all 2025–2027 EV configurations (n = 818): p10 29.0, median 37.0, p90 45.5 (Model 3 LR RWD 24.6; Equinox EV FWD 31.2; Silverado EV ~48–52). Level 1 extra loss vs EPA's test: 0–10% (**our assumption**) | fueleconomy.gov, vehicles.csv: https://www.fueleconomy.gov/feg/epadata/vehicles.csv.zip (acc. 2026-10-28) |
| A17 | Space heater, induction meal | Heater 1,500 / 750 W (A8). A meal on a portable induction hob: 0.5 / **0.75** / 1.0 kWh (**our assumption**: 30–45 min at 1,000–1,300 W average) | A8; assumption |
| A18 | Electric blanket | Rated 150 W (Sunbeam queen BL5151, AU listing, search snippet); average 40 / **75** / 150 W | Assumption anchored on that listing |
| A19 | Laptop, Starlink | MacBook Pro 16 100 Wh, 14 72.4 Wh (Apple specs); Starlink Standard 75–100 W, Mini 25–40 W, Mini USB PD "100 W, 20V/5A Minimum" | https://www.apple.com/macbook-pro/specs/ ; Starlink spec sheets https://www.starlink.com/public-files/specification_sheet_standard.pdf , https://www.starlink.com/public-files/specification_sheet_mini.pdf |
| A20 | Job-site day | Saw on 20 / **30** / 60 min at 1,200–1,500 W; 3 / **4** / 6 tool-battery charges at 50 / **75** / 100 Wh; 2 LED work lights 20 W × 4 h. → 710 / **1,210** / 2,260 Wh | **Our assumption** |
| A21 | Solar | SP037 per-panel yield and the station input limits: see the SP037 dossier. η_c (MPPT + charge) 0.90 / **0.93** / 0.95, **our assumption** | PVWatts v8 (https://developer.nlr.gov/api/pvwatts/v8.json) and NASA POWER (https://power.larc.nasa.gov/api/temporal/climatology/point), both called 2026-10-28 |
| A22 | Rejected source | Exspenditure's "about 3,650Wh of usable power" from a station whose battery is 3,456 Wh is impossible, so we did not use it | https://exspenditure.com/allpowers-portable-power-station-review/ (2026; seen as a search result) |

### Three cases used throughout

- **Worst:** U = 3,456 × 0.80 = **2,765 Wh**; S = 35 W.
- **Base:** U = 3,456 × 0.85 = **2,938 Wh**; S = 25 W.
- **Best:** U = 3,456 × 0.90 = **3,110 Wh**; S = 15 W.
- DC: U_dc = **2,889 / 3,021 / 3,119 Wh**; S_dc = 8 / 6 / 4 W.

---

## 1. Usable energy (AC vs DC path)

**Formula (ESTIMATE):** hours = U ÷ (load W + S). Cycling loads: days = U ÷ (daily Wh + 24 × S).

| Path | Usable energy (ESTIMATE) | Idle draw (assumed) | Idle alone empties a full battery in |
|---|---|---|---|
| AC (inverter on) | 2,765–3,110 Wh (base 2,938) | 15–35 W (base 25) | 3.3–8.6 days (base 4.9) |
| DC (car port / USB-C) | 2,889–3,119 Wh (base 3,021) | 4–8 W (base 6) | 15–33 days (base 21) |

**Generic AC runtime (ESTIMATE):**

| Load | Worst | Base | Best |
|---|---|---|---|
| 50 W | 32.5 h | 39.2 h | 47.9 h |
| 100 W | 20.5 h | 23.5 h | 27.1 h |
| 200 W | 11.8 h | 13.1 h | 14.5 h |
| 500 W | 5.2 h | 5.6 h | 6.0 h |
| 1,000 W | 2.7 h | 2.9 h | 3.1 h |
| 1,500 W | 1.8 h | 1.9 h | 2.1 h |
| 3,000 W | 0.91 h | 0.97 h | 1.03 h |
| 3,600 W | 46 min | 49 min | 52 min |

At small loads the assumed 25 W idle is 50% on top of a 50 W load. If a measured idle comes in lower, the small-load rows (fridge, CPAP, router) improve most.

**ALLPOWERS' own use-case claims, checked.** The page says "Keep your fridge, 1 HP AC, and oxygen concentrator running for 48 hours" and "Powers 99% of Appliances for 24-48 Hours". With a 10,000 BTU window AC (900–1,200 W) cycling 50%, a fridge and a 120–300 W concentrator, the day uses 14.7–23.5 kWh, and the R4000 lasts **2.7–5.0 h**. A full-size fridge alone lasts 24–55 h. The 48-hour claim only works for very light loads.

## 2. Fridge, mini fridge, CPAP, outage bundle, heat, electronics

Same formulas and inputs as the P1800 dossier, with this unit's U and S.

| Load | Runtime, ESTIMATE |
|---|---|
| Full-size ENERGY STAR fridge (0.99 / 1.50 / 1.88 kWh/day) | **24–55 h (base 34 h)** |
| Mini fridge | 38–80 h (base 55 h) |
| Router/modem 24 h + 3 LEDs 5 h + 2 phones (390 / 545 / 745 Wh/day) | **1.7–4.2 days (base 2.6)** |
| Same + full-size fridge | **19–43 h (base 27 h)** |
| AirSense 11, no humidifier | AC 7.4–17.7 nights (base 10.8); **DC 18–35 (base 25)**; AC left on 24 h 3.0–7.5 (base 4.4) |
| AirSense 11 + humidifier | AC 5.3–11.1 (base 7.8); DC 9.5–16.2 (base 13.5) |
| AirSense 11 + humidifier + heated tube | **AC 3.8–7.9 (base 5.2)**; DC 5.6–10.3 (base 7.4); AC left on 24 h 2.1–4.9 (base 3.1) |
| Full-size fridge + heated CPAP (one day = 1,267 / 1,864 / 2,325 Wh) | 0.87–1.91 days (base 1.19) |
| 1,500 W space heater | **1.8–2.1 h (base 1.9 h)** |
| 1,500 W heater cycling 50%, or 750 W | 3.5–4.1 h (base 3.8 h) |
| Electric blanket (avg 150 / 75 / 40 W) | 1.9–7.1 nights (base 3.7) |
| MacBook Pro 16 via USB-C (100 W port) | 23–28 full charges (base 26) |
| Starlink Mini via USB-C (100 W, 20 V/5 A) | 60–108 h (base 79 h) |
| Starlink Standard (AC) | 20–35 h (base 26 h) |

Worked example (fridge, base): 2,938 ÷ (1,504 + 24 × 25) = 2,938 ÷ 2,104 = 1.40 days = 34 h.

The DC CPAP route works on paper: the car port gives 12 V 10 A (120 W) and the Air11 converter asks for 12 V 10 A. The USB-C ports are 100 W each, which meets Starlink Mini's minimum.

## 3. Whole-house essentials

**Formula:** days = U ÷ (Σ daily Wh + 24 × S). Daily Wh per load: fridge and freezer from ENERGY STAR (A5, A7); sump, furnace and router/lights from A8 × A9.

| Scenario | Daily Wh (low / base / high) | Runtime, ESTIMATE |
|---|---|---|
| Fridge + freezer + router/lights (no pumps) | 1,965 / 3,134 / 3,915 | 0.58–1.34 days (base 0.79, 19 h) |
| **Summer:** + 1/2 HP sump (800–1,050 W, 0.5–2 h/day) | 2,365 / 4,059 / 6,015 | **10–27 h (base 15 h)** |
| **Winter:** + furnace blower (300–800 W, 6–14 h/day) | 3,765 / 8,134 / 15,115 | **4–18 h (base 8 h)** |
| Both sump and furnace | 4,165 / 9,059 / 17,215 | 4–16 h (base 7 h) |

**Surge check (worst numbers from A8):**
- Everything running at once: 400 + 500 + 1,050 + 800 + 65 = **2,815 W**, under the 3,600 W continuous rating.
- Sump starting while the rest runs: 2,150 + 400 + 500 + 800 + 65 = **3,915 W**, under the 6,000 W peak.
- Sump and fridge starting in the same instant: 2,150 + 1,200 + 500 + 800 + 65 = **4,715 W**, still under 6,000 W.

**What this means.** The inverter can handle the essentials together. The battery is the limit: a furnace blower alone can use more than the whole usable battery in a cold day. For multi-day outages this is a 15–30 hour bridge, unless solar is added (§9).

**Wiring caveat.** Furnaces, sump pumps and well pumps are often hardwired or on a dedicated circuit. Running them from the R4000 needs a plug-in appliance, a transfer switch or an inlet installed by an electrician. Nothing in the R4000 box does this.

## 4. Air conditioning: window units and RV rooftop

**Formula:** hours = U ÷ (running W × duty + S).

| Unit | Running W | Starting W | Hours at 50–100% duty (ESTIMATE) | Continuous compressor |
|---|---|---|---|---|
| 5,000 BTU window, fixed-speed | 450–600 | 900–1,200 | 4.4–13.0 h (base 7.0 h at 75%) | 4.4–6.7 h |
| 8,000 BTU ENERGY STAR (variable-speed, 533 W rated) | 300–533 | low (inverter compressor) | 4.9–18.9 h (base 8.1 h) | 4.9–9.9 h |
| 10,000 BTU window, fixed-speed | 900–1,200 | 1,800–2,400 | 2.2–6.7 h (base 3.6 h) | 2.2–3.4 h |
| 13,500 BTU RV rooftop | 1,450–2,000 | chart 2,800–3,500; **LRA 61–63 A ≈ 7.3–7.6 kVA** | 2.7–4.2 h at 50% (base 3.5 h) | **1.4–2.1 h (base 1.75 h)** |
| 15,000 BTU RV rooftop | 1,560–2,500 | chart 3,500–4,500; LRA not published | 2.2–3.9 h at 50% (base 3.2 h) | 1.1–2.0 h (base 1.6 h) |

**Starting an RV AC.** Dometic's own sheet puts the 13.5K's locked-rotor current at 61–63 A (A13). At 120 V that is about 7.5 kVA for the first fraction of a second, above the 6,000 W peak. Generator charts quote lower "starting watts" (2,800–3,500 W) because the motor begins turning within cycles, so an unassisted start may work some of the time. It is not reliable on paper. A soft starter that cuts inrush "by up to 75%" (A15; we assume 65–75% in practice) brings the 13.5K to roughly 16–22 A (1.9–2.6 kVA), well inside 3,600 W and the RV port's 3,000 W. Micro-Air's own testimonial page has an owner whose 13.5K would not start on a 4,000 W generator until the soft starter went in. **Recommendation: soft starter for any rooftop unit, required for the 15K.**

ENERGY STAR window units are now all variable-speed (A12), which ramps the compressor up instead of slamming it on. They are the easy case.

## 5. The RV outlet (TT-30): what fits in 3,000 W

The page caps the RV port at 3,000 W (manual says 30 A; 30 A × 120 V would be 3,600 W). Every outlet shares one 3,600 W inverter. Treat 3,000 W as the RV limit.

| Can run (within 3,000 W) | Running W | Notes |
|---|---|---|
| 13.5K rooftop AC + RV fridge on AC + 12 V lights/fans via the RV converter | 1,450–2,000 + 150–600 + ~100–300 | Soft starter advised. Turn off the RV converter's battery charging; it can pull several hundred watts from the R4000 just to charge the RV battery |
| 15K rooftop AC alone | 1,560–2,500 | Soft starter; little headroom left at the top of the range |
| RV microwave (600–1,200 W chart, ~1,450 W for a 1,000 W-cooking unit) + fridge + lights | ~1,700–2,100 | Fine when the AC is off |

| Can't run | Why |
|---|---|
| AC + microwave together | 1,650 + 1,450 = 3,100 W, over 3,000 W |
| AC + electric water heater (1,200–1,500 W) | 2,850–3,500 W |
| Two rooftop ACs | 2,900–5,000 W running, double inrush |
| A 50 A RV's full panel | The R4000 supplies one 120 V leg; through a 30-to-50 adapter both legs share 3,000 W, and nothing at 240 V runs |

## 6. Pumps

| Pump | Can it run? | Runtime, ESTIMATE |
|---|---|---|
| 120 V 1/2 HP well pump (750–1,000 W running, 1,500–2,000 W starting per chart) | Yes, if its start current is under about 50 A (6,000 W ÷ 120 V). Check the pump's nameplate locked-rotor amps; submersible 2-wire pumps can be higher than chart values (not verified) | 2.7–4.1 h of pumping (base 3.3 h). At 0.5–1.5 h of pumping a day (375–1,500 Wh), part of the battery's 2.9 kWh |
| 240 V well pump (most 3/4 HP and larger submersibles) | **No.** The US R4000 outputs 100–120 V only (manual) | none |
| 1/2 HP sump pump | Yes (surge fits) | see §3 |

## 7. Cooking: induction and microwave

| Load | Runtime, ESTIMATE |
|---|---|
| Portable induction hob at full 1,800 W | **1.5–1.7 h (base 1.6 h)** |
| Same at 1,200 W | 2.2–2.6 h (base 2.4 h) |
| Meals at 0.5 / 0.75 / 1.0 kWh each | **2.8–6.2 meals (base 3.9)** |
| Microwave, 1,000 W cooking (~1,450 W draw) | 1.9–2.1 h of cooking (base 2.0 h) |

Full-size 240 V induction ranges cannot run. A portable 120 V hob (15 A plug) fits easily under 3,600 W, and so does a hob plus microwave (about 3,250 W) if both are needed at once.

## 8. EV Level 1 charging (12 A, 120 V, 1,440 W)

**Formulas:** hours = U ÷ (1,440 + S). Miles = U × L1 factor ÷ (kWh/100 mi × 10). EPA's kWh/100 mi is measured at the wall, so it already includes the car's normal charging loss; the L1 factor (0.90 / 0.95 / 1.00) covers L1's extra overhead (assumption).

| Case | kWh/100 mi | mi/kWh | Charging time | Miles added (ESTIMATE) |
|---|---|---|---|---|
| Worst (truck-like, p90) | 45.5 | 2.2 | 1.9 h | **5.5 mi** |
| Base (median 2025–27 EV) | 37.0 | 2.7 | 2.0 h | **7.5 mi** |
| Best (efficient sedan, p10) | 29.0 | 3.45 | 2.1 h | **10.7 mi** |

That is an emergency top-up. With three SP037s feeding it on an average US day (4.5 kWh into the battery), the R4000 could pass about 10 miles a day to a median EV (5 in a Chicago December, 12.5 in Phoenix). Charging an EV through a power station costs conversion losses twice; doing it from the wall directly is always better.

## 9. Job-site power tools

| Tool (A8) | Running / starting W | vs 3,600 W / 6,000 W |
|---|---|---|
| 7-1/4" circular saw | 1,200–1,800 / 2,400–3,600 | yes |
| 10" miter saw | 1,200–1,800 / 2,400–3,600 | yes |
| 10" table saw | 1,800–3,000 / 3,600–6,000 | runs; **start can hit the 6,000 W peak** |
| Reciprocating saw, grinder, hammer drill | up to 1,800 / 3,600 | yes |
| 1 HP air compressor | 1,500 / 4,500 | yes |
| 2 HP air compressor | 2,500 / 7,500 | **no** (start exceeds 6,000 W) |
| 120 V welder | 1,800–2,500 / 3,600–5,000 | yes, little margin |

Energy: a saw running continuously at 1,500 W lasts 1.5–2.6 h (base 1.9 h). A typical job-site day (A20: 0.71 / 1.21 / 2.26 kWh) lasts **0.9–2.9 days (base 1.6 days)**. At 45 kg (manual) the station rolls on its casters, but it is not something to carry up a ladder.

## 10. Solar refill with SP037 (summary; full math in the SP037 dossier)

**Panels per input.** Three XT60 inputs, each 12–60 V, 13 A, 650 W.
- One SP037 per input: cold Voc 51.6 V at −10 °C, 56.6 V at −40 °C (NEC Table 690.7). Safe.
- Two in series: Voc 90.6 V. **Over 60 V; the manual warns of damage.**
- Two in parallel per input: Voc 45.3 V, Isc about 23 A against 13 A. Works only if the input current-limits; ALLPOWERS' manual drawing labels its panels "Can be connected in parallel", and it recommends the SP039 (Imp 13.63 A) for the R4000, but no maximum Isc is stated. Caps near 455–494 W per input.

| SP037 count | Layout per input | Input in good sun | Hours of good sun, 0–100% (ESTIMATE) | Average US day (11-city mean) |
|---|---|---|---|---|
| 1 | 1 / – / – | 260–320 W | **11.4–14.8 h (base 12.8)** | 1.51 kWh/day → 2.3 days |
| 2 | 1 / 1 / – | 520–640 W | 5.7–7.4 h (base 6.4) | 3.02 kWh → 1.15 days |
| 3 | 1 / 1 / 1 | 780–960 W | **3.8–4.9 h (base 4.3)** | 4.53 kWh → 0.76 days |
| 4 | 2 / 1 / 1 | 975–1,134 W | 3.2–3.9 h (base 3.5) | not modeled |
| 5 | 2 / 2 / 1 | 1,170–1,308 W | **2.8–3.3 h (base 3.0)** | 7.44 kWh → 0.46 days |
| 6 | 2 / 2 / 2 | 1,365–1,482 W | 2.5–2.8 h (base 2.6) | 8.90 kWh → 0.39 days |

Formula: hours = 3,456 ÷ (input W × η_c). Layouts beyond three panels rely on the parallel assumption. **The 2,000 W solar rating is out of reach with SP037s** (it would take panels near 50 V and 13 A per input).

**Break-even for a fridge + heated CPAP day.** Need = (1,504 + 360 + 24 × 25) ÷ 0.85 = **2,899 Wh/day** from the battery. Night use (14 h): 1,587 Wh, well inside the 2,938 Wh usable, so the R4000 can carry it overnight.

| City | Panels needed, annual-average day / December / June (fractional) |
|---|---|
| Phoenix | 1.5 / 1.7 / 1.4 → **2 panels** year-round |
| Los Angeles, Denver | 1.6 / 2.0 / 1.5 → 2 (Denver's December needs 3 on the whole-panel count) |
| Miami | 1.8 / 1.9 / 2.0 → 2–3 (summer clouds) |
| Dallas, Atlanta, Kansas City | 1.9–2.0 / 2.4–2.7 / 1.7–1.9 → 2–3 |
| Chicago, New York, Minneapolis | 2.1–2.3 / 3.3–3.8 / 1.9 → **3 most of the year, 4 in December** (4 = one parallel pair; little clipping in December sun) |
| Seattle | 2.5 / 5.4 / 1.9 → 3, and 6 in December |

With three panels on an average US day, the battery gets about 4.5 kWh, which after η and idle covers about 3.2 kWh/day of AC loads: fridge + freezer + router/lights (3.1 kWh base) roughly breaks even, outside winter in the north.

---

## Summary table (all ESTIMATES, base in bold)

| Use | Runtime / result |
|---|---|
| Usable energy | AC 2,765–3,110 Wh (**2,938**); DC 2,889–3,119 (**3,021**) |
| Full-size ENERGY STAR fridge | 24–55 h (**34 h**) |
| Fridge + router + lights + phones | 19–43 h (**27 h**) |
| AirSense 11 + humidifier + heated tube | AC 3.8–7.9 nights (**5.2**); DC 5.6–10.3 (**7.4**) |
| AirSense 11, no humidifier, DC | 18–35 nights (**25**) |
| Summer essentials (fridge, freezer, sump, router, lights) | 10–27 h (**15 h**) |
| Winter essentials (fridge, freezer, furnace blower, router, lights) | 4–18 h (**8 h**) |
| 8,000 BTU ENERGY STAR window AC | 4.9–18.9 h (**8.1 h**) |
| 13.5K RV rooftop AC, continuous / 50% duty | 1.4–2.1 h (**1.75**) / 2.7–4.2 h (**3.5**); soft starter advised |
| 15K RV rooftop AC, continuous | 1.1–2.0 h (**1.6**); soft starter needed |
| 120 V 1/2 HP well pump | 2.7–4.1 h of pumping (**3.3**); 240 V pumps: no |
| 1,500 W space heater | 1.8–2.1 h (**1.9**) |
| Induction cooktop 1,800 W / meals | 1.5–1.7 h (**1.6**) / 2.8–6.2 meals (**3.9**) |
| EV Level 1 | ~2 h, 5.5–10.7 miles (**7.5**) |
| Job-site day | 0.9–2.9 days (**1.6**); 2 HP compressor won't start |
| 3× SP037 refill | 3.8–4.9 h of good sun (**4.3**); 0.6–1.0 average days by city |
| Fridge + heated CPAP solar break-even | 2 panels (sunny cities) to 3 (north); 4 in a northern December, 6 in Seattle's |

## Open questions / couldn't verify

- **Idle draw and efficiency.** No ALLPOWERS figure and no measured review. Our 15–35 W idle assumption swings the fridge and CPAP rows by ±30%. A watt-meter test with the AC on and no load would settle it.
- **RV port.** Manual says "30A"; page says 3,000 W. The NEMA type is read from a drawing (TT-30R shape). Confirm with a photo or ALLPOWERS support.
- **AC outlets.** "US 20A Max" suggests NEMA 5-20R; not confirmed.
- **Peak duration.** ALLPOWERS does not say how long 6,000 W can be held. That decides whether an RV AC starts without a soft starter.
- **Parallel panels.** Whether each 13 A input limits current or faults with a 23 A Isc array. Ask support before advising 4–6 panels.
- **AC charging 1,500 W vs 2,000 W.** The page's 2,000 W is the 230 V figure; US 120 V is 1,500 W per the manual. Our product record should change.
- **Solar voltage row.** The page lists both "12 -60V" and "12 -150V". The manual says 60 V and warns of damage above it. Our record (60 V) is right; the page is wrong.
- **Well pump start current.** Chart values are generic; real 2-wire submersible locked-rotor amps were not checked.
- **15K RV AC data** (Coleman Mach 15 running watts, the 1,450 W owner reading) come from our AC200L dossier's retailer and forum sources, not re-fetched here.
- **Solar for 7 of 11 cities** uses NASA POWER with a derate fitted to PVWatts; see the SP037 dossier.
