# ALLPOWERS S2000 Pro + SP037 400 W solar kit: use-case math ("how long will it run my X, and what does the panel add")

Angle 4 (use-case math). Researched 2026-10-29. Every runtime, refill time and coverage figure here is an **ESTIMATE**, calculated from the inputs in the assumptions table, not measured. Formulas are shown so a reader can swap in their own appliance's number. Ranges run worst to best: worst = the one lab-measured capacity (920 Wh) + high idle draw + high appliance use; best = the reverse. Method, appliance inputs and SP037 yields are reused from our P1800, R4000 and SP037 dossiers (2026-10-28); only the S2000 Pro inputs are new.

**Headline (estimates):** ALLPOWERS' own runtime rule (85%) gives about 1,234 Wh of usable AC energy from the 1,451.6 Wh battery. The only lab test we found measured 920 Wh (StorageReview, a 2023 unit). We use 920 / 1,234 / 1,306 Wh with an assumed 10–22 W idle draw. With that:

- Full-size ENERGY STAR fridge: **9–25 h (base 16 h)**. 7 ft³ chest freezer: 15–40 h (base 30 h).
- AirSense 11 with humidifier and heated tube: **1.5–3.7 nights on AC (base 2.6)**, 1.9–4.4 on the 12 V port (base 3.2). Without the humidifier on 12 V: **6.4–16 nights (base 12)**.
- Outage bundle (router + modem 24 h, 3 LEDs 5 h, 2 phone charges): 17–50 h (base 33 h). Add a full-size fridge: **7–19 h (base 12 h)**.
- 1,500 W space heater, kettle or microwave: **36–52 min (base 49 min)**. Loads above 2,000 W only get the top ~40% of the battery: the manual cuts rated output to 2,000 W once the battery is at about 60%.
- 120 V 1/2 HP sump pump starts (1,300–2,150 W vs 4,000 W peak) and pumps 0.9–1.6 h. A 1/2 HP 2-wire submersible well pump probably will not start: its locked-rotor current (64.4 A, about 7.7 kVA) is nearly twice the 4,000 W peak.
- 8,000 BTU ENERGY STAR window AC: **1.7–8.2 h (base 3.5 h)**.
- **Solar:** one SP037 refills the battery in **4.8–6.2 h of good sun (base 5.4 h)**, or 0.8 (Phoenix) to 1.25 (Seattle) average days. Two SP037 in series (90.6 V) are allowed only under the spec table's 12–150 V input: **2.4–3.1 h**. Under the FAQ's 18–70 V rule two panels are not allowed in series or in parallel.
- **Fridge + heated CPAP day:** one panel covers **44–73% on an average day** (Seattle to Phoenix), 20–65% in the worst month. Two in series cover 89–146%. The battery does **not** carry the 14 h night in the base case (it runs about 12 h); it does with the humidifier off or a top-freezer fridge.
- **NMC vs LFP:** 2,500 cycles = 6.8 years of daily cycling, 48 years at one cycle a week, so for backup use calendar aging decides the life. Sandia measured 200–2,500 cycles to 80% for NMC cells and 2,500–9,000 for LFP.

---

## Spec check against ALLPOWERS (what our math depends on)

Sources: US product page (PAGE, https://iallpowers.com/products/allpowers-2400w-portable-power-station, acc. 2026-10-29), its `.js` record (created 2022-02-16, SKU `S2000-PLUS-US`, $664.00, compare-at $1,399.00), the kit page (KIT, https://iallpowers.com/products/allpowers-solar-generator-kit-2400w-s2000-pro-sp037-400w-solar-panel, acc. 2026-10-29; created 2024-11-24, SKU `AP-SS-009-PRO+AP-SP-037`, $963.00, compare-at $1,999.00) and the manual linked from PAGE's "Download Manual" (MAN, "S2000PRO V3.0", https://cdn.shopify.com/s/files/1/0443/1223/2089/files/YPJSS0055-S2000PRO_V3.0_AP-SS-009-PRO_user_mannual.pdf?v=1716446947, file stamp 2024-05-23; English panels read with PDFKit text extraction and rendered images, acc. 2026-10-29).

| Brief's number | ALLPOWERS says | Match? |
|---|---|---|
| 1,451 Wh NMC | MAN: "Battery capacity: 1451.6Wh (43.2V 33.6Ah)"; FAQ Q1 "Ternary lithium battery". PAGE: "Ternary lithium battery", "1451Wh"; description "1451.5Wh" | yes (1,451.6 Wh used) |
| 2,500+ cycles | PAGE: "Battery with 2,500+ Life Cycles to 80%". MAN gives no cycle figure | page only |
| 2,400 W continuous, 4,000 W peak | MAN: "2400W Max (Surged 4000W)" **"(*When the battery drops to ≈60%, the rated AC output is 2000W Max.)"**; "AC+DC Total Output: 2700W Max" | yes, with a **derate PAGE omits** |
| 4 AC outlets | MAN drawing: "AC Output*4" | yes. Older pages and 2023–24 reviews also list a 30 A RV port; MAN V3.0 does not show one (see Open questions) |
| 2× USB-C 100 W | MAN: "USB-C *2: 5/9/12/15V 3A, 20V 5A, 100W Max" | yes |
| 12 V / 10 A car port | MAN: "Car port: 12V 10A,120W Max" | yes |
| Solar 1,000 W / 12–150 V / 13 A (table) vs 650 W / 18–70 V / under 18 A (FAQ) | MAN: "Solar Input: (12~150)V 13A, 1000W Max"; "confirm that the output voltage specification of the solar panel is within 150V, the maximum current is 13A, and the maximum charging power is within 1000W"; diagram text "Users can charge the product by connecting solar panels in series". PAGE spec table same. PAGE FAQ: "maximum solar input of 650W" and for third-party panels "Voltage Range: 18-70V", "Current Range: Under 18A" | **conflict on PAGE.** Wayback shows the 18–70 V / 18 A / 650 W spec on PAGE through 2024-02-20 and 12–150 V / 13 A / 1,000 W from 2024-06-24 (§3.1). We treat the FAQ as the older hardware's spec and model both |
| AC input 1,500 W | MAN: "(100~120)V~15A 1500W Max" | yes |
| 13 kg | MAN: "Approximately 13KG(28.66lbs)"; PAGE "13kg / 28.66lb". PAGE captures through 2025-04-22 said 14.5 kg | yes (current) |
| UPS | MAN: switches "within 15ms"; on 100–120 V mains the AC load "should not exceed 1500W" | not in brief |
| Temperatures | MAN: charge 0–40 °C; discharge −10–40 °C; storage −20–40 °C | not in brief |
| Idle draw, efficiency | Not published. PAGE FAQ: "Runtime = Battery Capacity x Inverter Efficiency ÷ Rated Power", "1451Wh * 85% / 120W ≈ 10.28 hours"; DC: "1415Wh* 86%" (typo for 1451) | used as our base case |
| Kit | $963 = station $664 + SP037 $299 exactly; one variant (1 panel). Note on KIT: "the solar panels and power station will be shipped separately" | yes |

## Assumptions table (inputs, with sources)

Dates are publication dates where shown; otherwise "acc." (accessed).

| # | Input | Value used | Source |
|---|---|---|---|
| A1 | Battery | 1,451.6 Wh | MAN (file 2024-05-23) |
| A2 | AC usable energy U | worst **920 Wh** (lab-measured) / base **1,234 Wh** (= 1,451.6 × 0.85) / best 1,306 Wh (× 0.90) | Worst: StorageReview "measured a discharge capacity of 920Wh with a 350W load"; the unit "powered off with 22 percent remaining" (2023-04-07, a 1,500 Wh-labelled unit with the older 18–70 V input): https://www.storagereview.com/review/allpowers-s2000-pro-portable-power-station-review . Base: ALLPOWERS' 85% FAQ rule (PAGE). Best: **our assumption** (as in the P1800/R4000 dossiers) |
| A3 | AC idle draw S (inverter on, no load) | 22 / **15** / 10 W | **Our assumption.** No ALLPOWERS figure, no measured review (search 2026-10-29). Anchor: BLUETTI AC200L, also a 2,400 W inverter, 12 W (manual) and 18 W (BLUETTI staff), from our AC200L dossier A6. NerdTechy says the S2000 Pro's fan runs whenever the AC output is on (2023-02-25, https://nerdtechy.com/allpowers-s2000-pro-review), which argues against the low end |
| A4 | DC path | U_dc 920 / **1,248** (× 0.86, ALLPOWERS' DC rule) / 1,306 Wh; S_dc 6 / **4** / 3 W | PAGE FAQ (86%); idle **our assumption** |
| A5 | Full-size ENERGY STAR fridge, 18–28 ft³ | 1.88 / **1.50** / 0.99 kWh/day (p90 / median / p10, n = 1,611). Top-freezer median 374 kWh/yr, side-by-side 640 | ENERGY STAR Certified Residential Refrigerators, https://data.energystar.gov/resource/p5st-her9.json (via P1800 dossier A5, acc. 2026-10-28) |
| A6 | Chest freezer | 21.7 ft³ 346 kWh/yr (0.95/day); 15.7 ft³ 277 (0.76); **7.0 ft³ 225 (0.62)**; 5.0 ft³ 196 (0.54). 49 chest models listed (40 compact, 9 full-size) | ENERGY STAR Certified Residential Freezers, https://data.energystar.gov/resource/8t9c-g3tn.json (acc. 2026-10-29). Rated at DOE test conditions |
| A7 | Running / starting watts | Fridge 150–400 / 800–1,200; freezer 100–500 / 500–1,000; sump 1/2 HP 800–1,050 / 1,300–2,150; well pump 1/2 HP 750–1,000 / 1,500–2,000; circular and miter saw 1,200–1,800 / 2,400–3,600; table saw 1,800–3,000 / 3,600–6,000; 1 HP compressor 1,500 / 4,500; 2 HP 2,500 / 7,500; 120 V welder 1,800–2,500 / 3,600–5,000; router/modem 10–20; LED 8–15 per bulb; space heater 750–1,500 | Champion Power Equipment, "Generator Wattage Chart", 2026-04-17, https://www.championpowerequipment.com/generator-wattage-chart/ (via R4000 dossier A8) |
| A8 | Submersible well pump start | Franklin Electric 2445049004S (1/2 HP, 115 V, 2-wire): full load 10 A, max SF 12 A, **locked rotor 64.4 A** | Supreme Water Sales listing, https://www.supremewatersales.com/2445049004.html, seen as a search-result snippet 2026-10-29 (the page returned 404 to WebFetch). Third-party listing, not Franklin's own table |
| A9 | CPAP | AirSense 11: no humidifier 12 / **9** / 7 W; + humidifier 30 / **22** / 20 W; + humidifier + heated tube 56 / **45** / 34 W; 8 h nights. Air11 DC/DC converter input 12 V 10 A | ResMed AirSense 11 user guide 398133/2 (2021-10), "Typical power consumption 56.1W"; ResMed "Power consumption of Air10 devices" 1018673/1 (2015-03); ResMed converter page (via P1800 dossier A8–A11) |
| A10 | Outage bundle | Router/modem 24 h + 3 LEDs 5 h + 2 phone charges = 745 / **545** / 390 Wh/day | P1800 dossier §4 (Champion chart + phone assumption) |
| A11 | Microwave | 1,000 W cooking ≈ 1,450 W input | P1800 dossier A18 (Vollrath, Winco listings) |
| A12 | Kettle | 1,500 W. Heating 1 L from 20 to 100 °C = 1 kg × 4.18 kJ/kg·K × 80 K = 0.093 kWh; kettle efficiency 0.80 / **0.85** / 0.90 (**our assumption**) → 116 / 109 / 103 Wh per litre | Water specific heat 4.1844 kJ/kg·K at 20 °C, Engineering ToolBox, https://www.engineeringtoolbox.com/specific-heat-capacity-water-d_660.html (acc. 2026-10-29) |
| A13 | 8,000 BTU window AC | ENERGY STAR units are all variable-speed; 8,000 BTU ÷ CEER 15.0 = 533 W rated. Running 533 / **450** / 300 W at duty 100 / **75** / 50% | ENERGY STAR Certified Room Air Conditioners, https://data.energystar.gov/resource/5xn2-dv4h.json (via R4000 dossier A12); running and duty **our assumption** |
| A14 | Job-site day | 2,260 / **1,210** / 710 Wh | R4000 dossier A20 (**assumption**) |
| A15 | SP037 electrical | V3.0 (poly): Vmp 37.4 V, Voc 45.3 V, Imp 10.6–10.69 A, Isc 11.45–11.7 A, 18.5 kg. V5.0 (mono, "upgraded in May 2025" on the EU page): Vmp 30.5 V, Voc 36.5 V, Imp 13.11 A, Isc 14.42 A, 13.8 kg | SP037 dossier 1-maker.md (US page, V3.0 and V5.0 manuals, acc. 2026-10-28) |
| A16 | SP037 output in good sun | 260 / **290** / 320 W | SP037 manuals: "it is normal to finally get 260-320W"; owner reviews (SP037 dossier A2) |
| A17 | SP037 daily yield by city | Table in §3.3 (DC at the panel, kWh/day, fixed south tilt) | SP037 dossier §3: PVWatts v8 (Phoenix, Los Angeles, Denver, Miami) and NASA POWER with a fitted derate (7 cities), called 2026-10-28 |
| A18 | MPPT + charge efficiency η_c | 0.90 / **0.93** / 0.95 | **Our assumption** (not published) |
| A19 | Voc cold rise | NEC Table 690.7 factors 1.06 (10 °C), 1.10 (0 °C), 1.14 (−10 °C), 1.21 (−30 °C), 1.25 (−40 °C); cross-check β_Voc −0.30 %/°C (**assumed**; ALLPOWERS publishes none) | Mike Holt sample pages, https://www.mikeholt.com/instructor2/img/product/pdf/14SOLB-1229-sample.pdf (via SP037 dossier A3) |
| A20 | Night the battery must bridge | 14 h | **Our assumption** (as in the P1800/R4000 dossiers) |
| A21 | Cycle life by chemistry | NMC 200–2,500, NCA 250–1,500, LFP 2,500–9,000 equivalent full cycles to 80% capacity across Sandia's test conditions | Preger et al., "Degradation of Commercial Lithium-ion Cells as a Function of Chemistry and Cycling Conditions", J. Electrochem. Soc. 167 (2020) 120532, SAND2020-8433J, https://www.osti.gov/pages/biblio/1650174 (acc. 2026-10-29) |

### Three cases used throughout

- **Worst:** U = **920 Wh** (lab-measured); S = 22 W. (The 920 Wh was measured at 350 W, so it already includes conversion loss at that load. Adding 22 W of idle on top is deliberately conservative for small loads.)
- **Base:** U = 1,451.6 × 0.85 = **1,234 Wh**; S = 15 W.
- **Best:** U = 1,451.6 × 0.90 = **1,306 Wh**; S = 10 W.
- DC: U_dc = **920 / 1,248 / 1,306 Wh**; S_dc = 6 / 4 / 3 W.

---

## 1. Usable energy (AC vs DC)

**Formula (ESTIMATE):** hours = U ÷ (load W + S). For cycling loads: days = U ÷ (daily Wh + 24 × S).

| Path | Usable energy (ESTIMATE) | Idle draw (assumed) | Idle alone empties a full battery in |
|---|---|---|---|
| AC (inverter on) | 920–1,306 Wh (base 1,234) | 10–22 W (base 15) | 1.7–5.4 days (base 3.4) |
| DC (car port / USB-C, inverter off) | 920–1,306 Wh (base 1,248) | 3–6 W (base 4) | 6.4–18 days (base 13) |

**Generic AC runtime (ESTIMATE, hours = U ÷ (P + S)):**

| Load | Worst | Base | Best |
|---|---|---|---|
| 50 W | 12.8 h | 19.0 h | 21.8 h |
| 100 W | 7.5 h | 10.7 h | 11.9 h |
| 200 W | 4.1 h | 5.7 h | 6.2 h |
| 500 W | 1.8 h | 2.4 h | 2.6 h |
| 1,000 W | 54 min | 73 min | 77 min |
| 1,500 W | 36 min | 49 min | 52 min |
| 2,000 W | 27 min | 37 min | 39 min |

**Loads above 2,000 W.** MAN: "When the battery drops to ≈60%, the rated AC output is 2000W Max." The Solar Lab saw its unit shut off "at 55% battery" with an overload error under 2,250 W, and says output is capped at 2,050 W below 70% (https://www.thesolarlab.com/review/allpowers-s2000-pro-review, undated, acc. 2026-10-29). So a 2,000–2,400 W load gets only the top 40–45% of the battery: 0.40–0.45 × 1,451.6 × 0.85 = **490–555 Wh, about 12–15 min at 2,250–2,400 W** (ESTIMATE). Plan heavy loads around 2,000 W.

**What this means.** The spread between worst and base is mostly the capacity question. ALLPOWERS' FAQ Q9 concedes "the actual output capacity of the product is lower than the capacity specified" (MAN). The only lab figure (920 Wh) came from a 2023 unit that showed calibration trouble (it quit at 22% and jumped from 56% to 100% "in fewer than 10 minutes" on recharge, StorageReview). Today's 1,451.6 Wh unit has not been lab-tested that we found.

## 2. Runtimes

### 2.1 Fridge and chest freezer

**Formula:** days = U ÷ (daily Wh + 24 × S).

| Appliance | Daily use | Runtime, ESTIMATE |
|---|---|---|
| Full-size ENERGY STAR fridge (p90 / median / p10) | 1.88 / 1.50 / 0.99 kWh | **9–25 h (base 16 h)** |
| Same, by style (base) | top-freezer 1.03 kWh / side-by-side 1.75 kWh | 21 h / 14 h |
| Chest freezer 21.7 / **7.0** / 5.0 ft³ | 0.95 / 0.62 / 0.54 kWh | **15–40 h (base 30 h)** |
| Chest freezer 15.7 ft³ (base S) | 0.76 kWh | 26 h |

Worked example (fridge, base): 1,234 ÷ (1,504 + 24 × 15) = 1,234 ÷ 1,864 = 0.66 days = 15.9 h.

**Surge.** Fridge 800–1,200 W and freezer 500–1,000 W starting (A7) sit far under 2,400 W continuous, before the 4,000 W peak is needed. PAGE's FAQ warns its runtime formula "is NOT suitable for inductive loads with compressors, like refrigerators"; our daily-kWh method avoids that problem because it uses measured annual energy.

### 2.2 CPAP (8 h nights)

**Formulas:** AC, station off between nights: nights = U ÷ ((P + S) × 8). AC left on 24 h: nights = U ÷ (P × 8 + S × 24). DC (car port → ResMed Air11 DC/DC converter, 12 V 10 A in; the car port gives 12 V 10 A, 120 W): nights = U_dc ÷ ((P + S_dc) × 8).

| AirSense 11 setup | Draw (A9) | AC, off between nights | AC, left on 24 h | DC via 12 V port |
|---|---|---|---|---|
| No humidifier | 7–12 W (base 9) | 3.4–9.6 (base 6.4) | 1.5–4.4 (base 2.9) | **6.4–16.3 (base 12.0)** |
| + humidifier | 20–30 W (base 22) | 2.2–5.4 (base 4.2) | 1.2–3.3 (base 2.3) | 3.2–7.1 (base 6.0) |
| + humidifier + heated tube | 34–56 W (base 45) | **1.5–3.7 (base 2.6)** | 0.9–2.6 (base 1.7) | 1.9–4.4 (base 3.2) |

**Caveats from ALLPOWERS' own texts.** PAGE's FAQ says that while recharging from the wall "only the USB outings and AC outings are available", and other ports "are not capable of charging and discharging at the same time". So the 12 V car-port route works on battery, not while the unit charges from AC. MAN Q8 says the opposite ("supports simultaneous charging and discharging"). MAN §7 says the product is not intended for "medical equipment". The UPS switch takes up to 15 ms; ResMed publishes no ride-through time, so for outages running the CPAP from the battery all night is safer than relying on the switchover (not verified).

### 2.3 Outage bundle

| Bundle | Daily Wh (high / base / low) | Runtime, ESTIMATE |
|---|---|---|
| Router/modem + 3 LEDs + 2 phones | 745 / 545 / 390 | **17–50 h (base 33 h)** |
| Same + full-size fridge | 2,625 / 2,049 / 1,380 | **7–19 h (base 12 h)** |
| Same + fridge + heated CPAP | 3,073 / 2,409 / 1,652 | 6–17 h (base 11 h) |

### 2.4 Heat, cooking

| Load | Runtime, ESTIMATE | Formula |
|---|---|---|
| 1,500 W space heater, continuous | **36–52 min (base 49 min)** | U ÷ (1,500 + S) |
| 750 W setting, or 1,500 W cycling 50% | 72–103 min (base 97 min) | U ÷ (750 + S) |
| Microwave, 1,000 W cooking (≈1,450 W draw) | **38–54 min of cooking (base 51 min)**; 10 min of reheating ≈ 250 Wh, a fifth of the battery | U ÷ (1,450 + S) |
| 1,500 W kettle | same minutes as the heater; **8–13 one-litre boils (base 11)**, about 4.4 min each | U ÷ boil Wh (A12), idle ignored |

The Gadgeteer's unit "estimated 45 minutes to empty from a full charge" on a 1,500 W heater (2024-01-11, https://the-gadgeteer.com/2024/01/11/allpowers-s2000-pro-portable-power-station-review-a-decent-1500-wh-power-station-with-rv-plug/), which sits inside our range. All of these are under 2,000 W, so the ≈60% derate does not cut them off. A 1,200–1,250 W-cooking microwave (nameplate about 1,800 W, P1800 dossier A18) also stays under 2,000 W.

### 2.5 Pumps

| Pump | Starts? (vs 2,400 W continuous / 4,000 W peak) | Runtime if it runs, ESTIMATE |
|---|---|---|
| 1/2 HP sump pump, 120 V | **Yes.** 1,300–2,150 W starting, 800–1,050 W running (A7) | 0.9–1.6 h of pumping (base 1.3 h). At 1 h/day pumping and nothing else: 0.6–1.3 days (base 1.0) |
| 1/2 HP well pump, 120 V, by the generic chart | Chart says 1,500–2,000 W starting, under the peak | 0.9–1.7 h of pumping (base 1.4 h) |
| 1/2 HP **2-wire submersible**, 115 V (Franklin 2445049004S) | **Probably not.** Locked rotor 64.4 A × 120 V ≈ 7.7 kVA, about 1.9× the 4,000 W peak (A8). The motor needs that current for a fraction of a second; whether the inverter rides through it is untested | n/a |
| 3-wire submersible with a control box | Lower inrush than 2-wire (start capacitor), but no locked-rotor figure checked. Unverified | n/a |
| 240 V well pump | **No.** US unit outputs 100–120 V only (MAN) | n/a |

ALLPOWERS does not say how long the 4,000 W peak lasts. Well and sump pumps are usually hardwired; running one from the station needs a plug-in pump or an electrician-installed transfer switch or inlet.

### 2.6 Power tools

| Tool (A7) | Running / starting W | vs 2,400 W (2,000 W below ≈60%) / 4,000 W |
|---|---|---|
| 7-1/4" circular saw, 10" miter saw | 1,200–1,800 / 2,400–3,600 | **yes** |
| Reciprocating saw, grinder, hammer drill | up to 1,800 / 3,600 | yes |
| 10" table saw | 1,800–3,000 / 3,600–6,000 | runs only up to 2,400 W running (2,000 W in the lower 60% of the battery); **start can exceed 4,000 W** |
| 1 HP air compressor | 1,500 / 4,500 | **start exceeds 4,000 W**: likely trips |
| 2 HP air compressor | 2,500 / 7,500 | no |
| 120 V welder | 1,800–2,500 / 3,600–5,000 | marginal; no at the top of the range |

Energy: a saw running continuously at 1,500 W lasts 30–65 min (base 49 min). A job-site day (A14) lasts **0.4–1.8 days (base 1.0)**.

### 2.7 8,000 BTU window AC

**Formula:** hours = U ÷ (running W × duty + S).

| Case | Running W × duty | Runtime, ESTIMATE |
|---|---|---|
| Worst | 533 W × 100% | 1.7 h |
| Base | 450 W × 75% | **3.5 h** |
| Best | 300 W × 50% | 8.2 h |
| Continuous compressor | 300–533 W | 1.7–4.2 h (base 2.7 h) |

ENERGY STAR window units are variable-speed (A13), so they ramp up instead of slamming on; the start fits easily. An older fixed-speed unit's start current was not checked here.

## 3. Solar with the kit

### 3.1 What the input accepts: two readings of ALLPOWERS' page

- **Spec-table / manual reading (S):** 12–150 V, 13 A, 1,000 W (MAN; PAGE spec table).
- **FAQ reading (F):** 18–70 V, "Under 18A", 650 W (PAGE FAQ, third-party panels).

The FAQ matches the older hardware. Wayback captures of PAGE show "Solar Input：18-70V, 18A 650W Max" from 2022-06-27 through 2024-02-20 and "(12~150)V 13A, 1000W Max" from 2024-06-24 onward (captures https://web.archive.org/web/20220627085055/…, …/20240220231508/…, …/20240624235133/…, …/20260616001553/https://iallpowers.com/products/allpowers-2400w-portable-power-station, acc. 2026-10-29). StorageReview (2023-04-07) and The Gadgeteer (2024-01-11) both quote "MPPT 18-70V, 18A 650W Max". The V3.0 manual (file 2024-05-23) carries the 150 V figure. The FAQ also contradicts itself: it lists ALLPOWERS' SP033 200 W as fine "Up to 3 series connections", and three SP033s (Voc 44.4 V each, https://iallpowers.com/products/allpowers-sp033-portable-polycrystalline-solar-panel-200w-flash-deal, acc. 2026-10-29) make 133 V, which only the 150 V input allows. So reading S fits units sold since mid-2024; reading F fits earlier units. Which one a given unit has is not printed anywhere we could check (Open questions).

### 3.2 Wiring options with SP037s

**Formula:** cold Voc = Voc × NEC factor (or × (1 + 0.0030 × (25 − T))). Parallel Isc = n × Isc.

| Configuration | Voc at 25 °C → −10 °C → −40 °C (NEC) | Current | Reading S (150 V, 13 A, 1,000 W) | Reading F (70 V, 18 A, 650 W) |
|---|---|---|---|---|
| 1 × SP037 V3.0 | 45.3 → 51.6 → 56.6 V | Imp 10.6 A | **OK.** 260–320 W real | **OK** |
| 1 × SP037 V5.0 | 36.5 → 41.6 → 45.6 V | Imp 13.11 A | OK; clips at 13 A ≈ 397 W at test conditions, no effect in real sun | OK |
| **2 × V3.0 in series** | **90.6 → 103.3 → 113.2 V** | 10.6 A | **OK**, 37 V of headroom even at −40 °C. 520–640 W real | **No.** Over 70 V at any temperature |
| 2 × V5.0 in series | 73.0 → 83.2 → 91.2 V | 13.11 A (clips at 13 A) | OK | **No.** 73 V is over 70 V even warm |
| 2 × V3.0 in parallel | 45.3 V | Isc 22.9–23.4 A, Imp 21.2 A | Over the 13 A input; relies on the input limiting current (not stated). Caps near 13 A × 35–38 V ≈ 455–494 W, worse than series | Over "Under 18A"; not within the FAQ either |
| 3 × V3.0 in series | 135.9 → 154.9 → 169.9 V | 10.6 A | **No.** Crosses 150 V below about 0 °C (NEC) or −10 °C (β −0.30 %/°C). One frosty morning can trip E212 "MPPT input overvoltage" or worse | No |
| Mixing V3.0 and V5.0 | n/a | n/a | Don't. Both SP037 manuals: "Only panels with similar electrical output should be connected in the same string" (SP037 dossier) | Don't |

**What this means.** The kit ships one panel. A second SP037 in series is the only sensible upgrade, and it is allowed only on a 150 V unit. On a pre-mid-2024 unit (70 V input), one SP037 is the limit, because its own FAQ excludes both series and parallel pairs. With SP037s the 1,000 W rating is out of reach either way: two panels give 520–640 W in real sun, and three in series are unsafe in winter.

### 3.3 Refill time

**Hours of good sun, 0–100% (ESTIMATE):** hours = 1,451.6 ÷ (input W × η_c).

| Panels | Input in good sun | Hours of good sun | Allowed under |
|---|---|---|---|
| 1 × SP037 (the kit) | 260–320 W (base 290) | **4.8–6.2 h (base 5.4 h)** | S and F |
| 2 × SP037 in series | 520–640 W (base 580) | **2.4–3.1 h (base 2.7 h)** | S only |
| 2 × SP037 in parallel | 455–494 W (13 A cap, if tolerated) | 3.1–3.5 h (base 3.3 h) | neither, strictly |
| AC wall charger | 1,500 W (MAN) | ≈1.0–1.1 h + taper; The Gadgeteer: "fully charges in about 90 minutes from empty" | n/a |

If a unit holds only about 1,000 Wh (the StorageReview case), each refill is about 30% shorter.

**Daily yield per SP037 (DC at the panel, kWh/day; SP037 dossier §3) and days to refill from empty:** days = 1,451.6 ÷ (daily kWh × panels × η_c). Base η_c 0.93. Two series panels are not current-clipped (10.6 A < 13 A; 800 W < 1,000 W), so they give 2.0× one panel.

| City (data) | Winter | Spring | Summer | Fall | Annual | Worst month | 1 panel: days, annual / worst month / summer | 2 in series: days, annual / worst month |
|---|---|---|---|---|---|---|---|---|
| Phoenix (PVWatts) | 1.89 | 2.24 | 2.03 | 2.04 | 2.05 | 1.83 Jan | **0.76** / 0.85 / 0.77 | 0.38 / 0.43 |
| Los Angeles (PVWatts) | 1.68 | 1.99 | 2.14 | 1.98 | 1.95 | 1.56 Dec | 0.80 / 1.00 / 0.73 | 0.40 / 0.50 |
| Denver (PVWatts) | 1.67 | 2.03 | 2.00 | 1.87 | 1.89 | 1.55 Dec | 0.83 / 1.01 / 0.78 | 0.41 / 0.50 |
| Miami (PVWatts) | 1.75 | 1.88 | 1.62 | 1.73 | 1.75 | 1.54 Jun | 0.89 / 1.01 / 0.96 | 0.45 / 0.51 |
| Dallas (NASA) | 1.38 | 1.65 | 1.81 | 1.60 | 1.61 | 1.32 Dec | 0.97 / 1.18 / 0.86 | 0.48 / 0.59 |
| Atlanta (NASA) | 1.32 | 1.72 | 1.63 | 1.56 | 1.56 | 1.20 Dec | 1.00 / 1.30 / 0.96 | 0.50 / 0.65 |
| Kansas City (NASA) | 1.25 | 1.61 | 1.76 | 1.51 | 1.54 | 1.14 Dec | 1.01 / 1.37 / 0.89 | 0.51 / 0.68 |
| Chicago (NASA) | 0.97 | 1.54 | 1.67 | 1.31 | 1.38 | 0.82 Dec | 1.13 / 1.90 / 0.93 | 0.57 / 0.95 |
| New York (NASA) | 1.11 | 1.57 | 1.63 | 1.33 | 1.41 | 0.93 Dec | 1.11 / 1.68 / 0.96 | 0.55 / 0.84 |
| Minneapolis (NASA) | 1.19 | 1.60 | 1.73 | 1.31 | 1.46 | 0.87 Dec | 1.07 / 1.79 / 0.90 | 0.53 / 0.90 |
| Seattle (NASA) | 0.71 | 1.37 | 1.75 | 1.13 | 1.25 | 0.57 Dec | **1.25** / 2.74 / 0.89 | 0.62 / 1.37 |

Seasons: Dec–Feb, Mar–May, Jun–Aug, Sep–Nov. Yields are for the V3.0 panel at a fixed south tilt; V5.0 is also rated 400 W and is assumed equal. Uncertainty about ±10% (data source, foldable-panel losses) and ±3% (η_c). A value under 1.0 means the battery fills partway through one average day.

### 3.4 Fridge + CPAP day: what share does the kit's panel cover?

**Daily need from the battery (base):** need = (fridge + CPAP + 24 × S) ÷ 0.85 = (1,504 + 360 + 360) ÷ 0.85 = **2,616 Wh/day** (worst 3,570, best 1,669). Share covered = daily kWh × panels × 0.93 ÷ need.

| City | 1 panel: annual avg / season range / worst month | 2 in series: annual avg / season range / worst month | Panels to break even: annual / worst month / summer |
|---|---|---|---|
| Phoenix | **73%** / 67–80% / 65% | 146% / 134–159% / 130% | 1.4 / 1.5 / 1.4 |
| Los Angeles | 69% / 60–76% / 55% | 139% / 119–152% / 111% | 1.4 / 1.8 / 1.3 |
| Denver | 67% / 59–72% / 55% | 134% / 119–144% / 110% | 1.5 / 1.8 / 1.4 |
| Miami | 62% / 58–67% / 55% | 124% / 115–134% / 109% | 1.6 / 1.8 / 1.7 |
| Dallas | 57% / 49–64% / 47% | 114% / 98–129% / 94% | 1.7 / 2.1 / 1.6 |
| Atlanta | 55% / 47–61% / 43% | 111% / 94–122% / 85% | 1.8 / 2.3 / 1.7 |
| Kansas City | 55% / 44–63% / 41% | 109% / 89–125% / 81% | 1.8 / 2.5 / 1.6 |
| Chicago | 49% / 34–59% / 29% | 98% / 69–119% / 58% | 2.0 / 3.4 / 1.7 |
| New York | 50% / 39–58% / 33% | 100% / 79–116% / 66% | 2.0 / 3.0 / 1.7 |
| Minneapolis | 52% / 42–61% / 31% | 104% / 85–123% / 62% | 1.9 / 3.2 / 1.6 |
| Seattle | **44%** / 25–62% / 20% | 89% / 50–124% / 41% | 2.3 / 4.9 / 1.6 |

With the CPAP humidifier off (need 2,278 Wh/day) each share rises by 15%.

**Does the battery carry the night?** Night need (14 h, AC side) = fridge × 14/24 + CPAP × 8 h + S × 14.

| Day | Night need (worst / base / best) | Usable U | Hours of a 14 h night carried, ESTIMATE |
|---|---|---|---|
| Full-size fridge + heated CPAP | 1,853 / **1,447** / 990 Wh | 920 / 1,234 / 1,306 | 7.0 / **11.9** / 14 (full) |
| Full-size fridge + CPAP with humidifier, no heated tube | 1,645 / 1,263 / 878 | same | 7.8 / 13.7 / 14 |
| Full-size fridge + CPAP, no humidifier | 1,501 / 1,159 / 774 | same | 8.6 / **14 (full)** / 14 |
| Top-freezer fridge + heated CPAP | 1,354 / 1,168 / 1,010 | same | 9.5 / **14 (full)** / 14 |

**What this means for the kit.**
- One SP037 replaces about half the energy of a fridge + heated CPAP day (44–73% on an average day). It is a slow-drain extender, not a self-sustaining setup, anywhere in the US.
- A second SP037 in series (if the unit has the 150 V input) breaks even on an average day everywhere except Chicago (98%) and Seattle (89%), with New York right at 100%. In the worst month it breaks even only in Phoenix, Los Angeles, Denver and Miami.
- The battery is the tighter limit at night. At base it falls about 2 hours short with a full-size fridge plus heated CPAP. Turning the humidifier off, or a top-freezer fridge, makes the night fit at base. In the lab-measured case (920 Wh) nothing in this table makes it through the night.

## 4. NMC vs LFP in numbers

| Question | Numbers | Source |
|---|---|---|
| ALLPOWERS' cycle claim | "2,500+ Life Cycles to 80%" (PAGE). Captures from 2023-09-26 to 2025-09-08 add "lasts for almost 10 years". MAN gives no figure | PAGE; Wayback captures above |
| 2,500 cycles at one cycle a day | 2,500 ÷ 365 = **6.8 years** to 80% (ESTIMATE, if the claim holds) | arithmetic |
| At one cycle a week | 2,500 ÷ 52 = **48 years**: cycling will not be the limit; calendar aging will | arithmetic |
| "Almost 10 years" | implies about 250 full cycles a year | arithmetic |
| Energy delivered over life | 2,500 × 1,234 Wh × ~0.9 (average retention between 100% and 80%) ≈ **2,780 kWh**, about $0.24/kWh on the $664 station (ESTIMATE) | arithmetic |
| Where 2,500 sits for NMC | Sandia's commercial NMC cells reached 80% after **200 to 2,500** equivalent full cycles depending on conditions; LFP **2,500 to 9,000**; NCA 250 to 1,500. "Most of the LFP cells had not reached 80% capacity by the conclusion" | Preger et al. 2020 (A21) |
| Depth of discharge | NMC and NCA cells "exhibited a stronger dependence on depth of discharge, with greater sensitivity to full SOC range cycling than LFP"; at the same cycle count, 0–100% cycling cost NMC 5–10% more capacity than partial cycling | Preger et al. 2020 |
| Calendar aging | "Irrespective of chemistry, in calendar aging studies, capacity fade consistently increased with SOC … NCA and NMC cells exhibited particularly rapid capacity fade at 100% SOC"; calendar fade "consistently decreased with decreasing temperature" | Preger et al. 2020 |
| Calendar aging, second source | Keil et al. stored NMC (Sanyo UR18650E), LFP (A123) and NCA cells at 16 SoC levels and 25 / 40 / 50 °C for 9–10 months. LFP faded "ca. 0.2 percentage points … per month at 25°C" (≈2.4 points a year) and 0.5 per month at 50 °C; NMC showed a "steep increase in capacity fade" at 100% SoC at 50 °C. Authors: high storage SoCs "should be avoided". We could not read NMC's numbers (figure only) | Keil et al., "Calendar Aging of Lithium-Ion Batteries: I. Impact of the Graphite Anode on Capacity Fade", J. Electrochem. Soc. 163(9), 2016-07-06, https://iopscience.iop.org/article/10.1149/2.0411609jes (abstract and text via WebFetch, acc. 2026-10-29) |
| ALLPOWERS' own storage advice | "discharge the battery to 30% and recharge to 60% every three months" (MAN Q6); "for battery life maintenance, it is recommended not to charge and discharge at ordinary times, except in emergencies" (PAGE FAQ) | MAN; PAGE |
| Weight payoff of NMC | 1,451.6 Wh ÷ 13 kg = **112 Wh/kg**. ALLPOWERS' LFP P1800: 1,024 Wh at 13 kg = 79 Wh/kg. ALLPOWERS' LFP R2500 V2: 1,920 Wh at 29 kg = 66 Wh/kg, "3500+ Cycles" | P1800 dossier 1-maker.md (manual, 13 kg); https://iallpowers.com/products/allpowers-r2500-v2-portable-power-station-2500w-1920wh (acc. 2026-10-29) |

**What this means.** For a backup unit that cycles a few times a year, 2,500 cycles is irrelevant; how long it sits at a high state of charge and how warm it is decide its life. That is the worst case for NMC: kept full on the wall as a UPS. ALLPOWERS itself advises storing it at 30–60% and not running it as a pass-through day to day. For daily solar cycling (the kit's use), 2,500 cycles is about 7 years to 80% if the claim holds, and Sandia's data put 2,500 at the top of what NMC cells reach. ALLPOWERS' own LFP units claim 3,000–4,000+ cycles (P1800 page and manual, R2500 V2 page) at 1.4–1.7× the weight per Wh.

---

## Summary table (all ESTIMATES, base in bold)

| Use | Runtime / result |
|---|---|
| Usable energy | AC 920–1,306 Wh (**1,234**); DC 920–1,306 (**1,248**). Only lab figure: 920 Wh (2023 unit) |
| Loads above 2,000 W | top 40–45% of the battery only (≈60% derate), about 12–15 min at 2,250–2,400 W |
| Full-size ENERGY STAR fridge | 9–25 h (**16 h**) |
| Chest freezer, 7 ft³ | 15–40 h (**30 h**) |
| AirSense 11 + humidifier + heated tube | AC 1.5–3.7 nights (**2.6**); 12 V DC 1.9–4.4 (**3.2**) |
| AirSense 11, no humidifier, 12 V DC | 6.4–16.3 nights (**12.0**) |
| Router + modem + 3 LEDs + phones | 17–50 h (**33 h**) |
| Same + full-size fridge | 7–19 h (**12 h**) |
| 1,500 W heater / kettle / 1,000 W microwave | 36–52 min (**49**) / 8–13 litre boils (**11**) / 38–54 min (**51**) |
| 1/2 HP sump pump | starts; 0.9–1.6 h of pumping (**1.3 h**) |
| 1/2 HP 2-wire submersible well pump | probably won't start (≈7.7 kVA inrush vs 4,000 W) |
| Circular/miter saw / table saw / 1 HP compressor | yes / start may exceed 4,000 W / likely trips |
| Job-site day | 0.4–1.8 days (**1.0**) |
| 8,000 BTU ENERGY STAR window AC | 1.7–8.2 h (**3.5 h**) |
| 1 × SP037 refill (the kit) | 4.8–6.2 h of good sun (**5.4 h**); 0.76 (Phoenix) to 1.25 (Seattle) average days, 2.7 in a Seattle December |
| 2 × SP037 in series | 2.4–3.1 h (**2.7 h**), only on the 12–150 V input; not allowed under the FAQ's 18–70 V |
| Fridge + heated CPAP day, 1 / 2 panels | 44–73% / 89–146% of the day on an average day; panels to break even 1.4–2.3 (annual), up to 4.9 (Seattle, Dec) |
| Battery through a 14 h night (fridge + heated CPAP) | no at base (≈12 h); yes with humidifier off or a top-freezer fridge |
| 2,500 cycles | 6.8 years daily, 48 years weekly; calendar aging governs backup use |

## Open questions / couldn't verify

- **Which solar input today's units have.** PAGE's spec table and the V3.0 manual say 12–150 V / 13 A / 1,000 W; PAGE's FAQ (and the page until early 2024) says 18–70 V / 18 A / 650 W. We found no label photo or ALLPOWERS statement tying an input range to a serial number, SKU or date. The SKU changed from `AP-SS-009-PRO-US` (captures to 2025-09-08) to `S2000-PLUS-US` (by 2026-06-16), while the kit's SKU still says `AP-SS-009-PRO`. Before publishing "two SP037 in series", get written confirmation from service@allpowers.com that the unit shipped in the kit accepts 90.6 V (113 V at −40 °C).
- **Which SP037 the kit ships** (V3.0 poly, Voc 45.3 V, or V5.0 mono, Voc 36.5 V). It changes the series Voc (90.6 vs 73 V), the weight (18.5 vs 13.8 kg) and whether an older owner's second panel will match.
- **Real usable capacity of current units.** The only lab test (920 Wh at 350 W) is a 2023 unit labelled 1,500 Wh. No test of today's 1,451.6 Wh unit turned up (search 2026-10-29).
- **Idle draw.** No published or measured figure; 10–22 W is an assumption. A watt-meter reading with AC on and no load would tighten every small-load row.
- **≈60% derate.** MAN says ≈60% → 2,000 W; The Solar Lab says 70% → 2,050 W and saw a shutoff at 55% under 2,250 W. Exact threshold unverified.
- **4,000 W peak duration.** Not published. It decides the table saw, 1 HP compressor and well pump rows.
- **Car port while charging.** PAGE FAQ says non-USB/AC ports don't work while charging from the wall; MAN Q8 says simultaneous charge and discharge works. Behavior while charging from solar is not stated.
- **Parallel panels.** Whether the 13 A input current-limits a 23 A pair. Not documented.
- **RV 30 A port.** NerdTechy (2023), The Gadgeteer (2024) and the kit description mention one; the V3.0 manual drawing shows only four AC outlets. Not checked on a current unit.
- **NMC calendar fade numbers** for these cells: no cell datasheet; Keil 2016's NMC values are in a figure we could not read.
- **Well pump start.** The 64.4 A locked-rotor figure is a retailer listing seen as a search snippet. Franklin's own AIM manual table was not read, and 3-wire pumps were not checked.
- **Solar yields for 7 of 11 cities** use NASA POWER with a derate fitted to PVWatts (SP037 dossier A12).
