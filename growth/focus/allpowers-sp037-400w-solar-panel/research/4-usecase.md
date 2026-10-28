# ALLPOWERS SP037 (400 W foldable panel): use-case math ("how fast will solar refill it")

Angle 4 (use-case math). Researched 2026-10-28. Every refill time and yield here is an **ESTIMATE**, calculated from the inputs below, not measured. Formulas are shown. Ranges run worst to best unless marked.

**Headline (estimates):**

- In good sun one SP037 delivers about **260–320 W** (ALLPOWERS' manual text and owner reports), consistent with PVWatts.
- On an average day it puts **1.2–1.9 kWh into a battery** depending on the city (11-city mean 1.5 kWh; Seattle in December 0.5 kWh, Phoenix in April 2.2 kWh).
- **P1800 (1,024 Wh):** 1 panel refills it in **3.4–4.4 h of good sun**, or within one average day in every city we modeled except winter in Chicago, New York, Minneapolis and Seattle. 2 panels (parallel only) take 2.2–2.5 h.
- **R4000 (3,456 Wh):** 1 panel 11–15 h of good sun (about 2.3 average days); **3 panels (one per input) 3.8–4.9 h**; 5 panels 2.8–3.3 h. The R4000's 2,000 W solar rating is out of reach with SP037s.
- **Wiring rule:** one SP037 per XT60 input in series terms. Two in series (Voc 90.6 V) are over the 60 V limit of both stations. Two in parallel stay at 45 V but push 23 A of short-circuit current into a 13 A input; that relies on the input limiting current (implied by ALLPOWERS, never stated).
- **Fridge + CPAP day:** 2 panels break even in sunny cities, 3 in the north, more in December. On a P1800 no panel count is enough, because the battery can't carry that load through the night.

---

## Spec check against ALLPOWERS (what our math depends on)

| Our record | ALLPOWERS product page (S1) | SP037 manual V3.0 (S2) | Match? |
|---|---|---|---|
| 400 W | "Peak Power 400W" | "400W" | yes |
| Vmp 37.4 V | 37.4 V | 37.4 V | yes |
| Voc 45.3 V | 45.3 V | 45.3 V | yes |
| Imp 10.6 A | 10.6 A | **10.69 A** | close; manual slightly higher |
| Isc 11.45 A | 11.45 A | **11.7 A** | close; we use 11.7 A for safety margins |
| 18.5 kg | "18.5KG 40.79lb" | 18.5 kg | yes |
| also | "22%" efficiency; cell type "Polycrystalline"; IP67 | "19%-23%"; operating −10 °C to 60 °C; STC 1,000 W/m², 25 °C, AM1.5; **IP66** in the English text | conflicts on IP rating and cell type; neither affects the math |
| Temperature coefficients | not published | not published | **gap**: we use an assumption and the NEC table |

The manual's diagrams show both series and parallel wiring, and its Japanese/Chinese text says the included MC4 cable is 14 AWG (2.5 mm²) rated 20 A max.

## Assumptions table (inputs, with sources)

| # | Input | Value used | Source |
|---|---|---|---|
| A1 | SP037 electrical specs | as above | S1 https://iallpowers.com/products/allpowers-400w-portable-solar-panel (acc. 2026-10-28); S2 https://cdn.shopify.com/s/files/1/0443/1223/2089/files/AP-SP-037_400W_Solar_Panel.pdf?v=1671926121 (file stamped 2022-12-24) |
| A2 | Real-world output in good sun | 260 / **290** / 320 W | S2's text layer carries "260-320W" beside its connection steps (the context is not visible in the rendered page). Owner reviews on S1: "almost 300 watts output", "320 watts max without fine tuning to the sun angle" (late May, southern Michigan), another sees "265-75" |
| A3 | Voc temperature rise | NEC Table 690.7 factors: 1.06 (10–14 °C), 1.10 (0–4 °C), 1.14 (−6 to −10 °C), 1.21 (−26 to −30 °C), 1.25 (−36 to −40 °C). Cross-check with **assumed** β_Voc = −0.30 %/°C (typical crystalline module; ALLPOWERS publishes none) | Mike Holt, *Illustrated Guide to NEC Requirements for Solar PV*, sample pages, Table 690.7: https://www.mikeholt.com/instructor2/img/product/pdf/14SOLB-1229-sample.pdf (acc. 2026-10-28) |
| A4 | P1800 solar input | 1 XT60, "MPPT(11-60)V⎓13A 650W Max"; "ensure that the output voltage … is within the range of 11- 60V". US page adds "95V Open-Circuit Voltage" | P1800 manual: https://cdn.shopify.com/s/files/1/0747/3135/6467/files/ALLPOWERS_P1800_User_Manual.pdf?v=1785825984 ; US page https://iallpowers.com/products/allpowers-p1800-portable-power-station-1024wh-1800w |
| A5 | R4000 solar input | 3 XT60, "(12~60)V 13A, Single port 650W Max, three ports 2000W Max"; stay "within 60V to avoid damage"; drawing labels panels "Can be connected in parallel" | R4000 manual V3.0: https://cdn.shopify.com/s/files/1/0443/1223/2089/files/allpowers_R4000-AP-R4000_USER_MANNUAL-V3.0-_compressed_1.pdf?v=1712547934 |
| A6 | ALLPOWERS pairs over-13 A panels with 13 A inputs | SP039: Imp 13.63 A, Isc 14.99 A; sold as a P1800 kit and recommended for the R4000 | https://iallpowers.com/products/allpowers-sp039-600w-monocrystalline-portable-solar-panel ; R4000 page FAQ |
| A7 | BLUETTI AC180 input | "500W Max., VOC 12-60VDC, 10A"; 1,152 Wh | https://www.bluettipower.com/products/ac180 (acc. 2026-10-28) |
| A8 | BLUETTI Elite 200 V2 input | "1,000W Max., 12V to 60V, 20A Max."; 2,073.6 Wh | https://www.bluettipower.com/products/elite-200-v2-portable-power-station (acc. 2026-10-28) |
| A9 | Current cap per input | 13 A × 35 / 36.5 / 38 V = **455 / 475 / 494 W** (P1800, R4000); AC180 10 A → 350–380 W; Elite 200 V2 20 A → 700–760 W | **Our assumption** on operating voltage when the input limits current |
| A10 | Solar yield, PVWatts cities | 0.4 kW, standard module, fixed open rack, **35° tilt, south**, 14.08% losses (PVWatts default), NSRDB TMY. Phoenix, Los Angeles, Denver, Miami | PVWatts v8.5.0 API: https://developer.nlr.gov/api/pvwatts/v8.json (called 2026-10-28; DEMO_KEY rate-limited after 4 cities) |
| A11 | Solar yield, NASA cities | Dallas, Atlanta, Kansas City, Chicago, New York, Minneapolis, Seattle: NASA POWER monthly irradiance on a latitude-tilt south surface × 0.4 kW × derate | NASA POWER Climatology API v2.10.1, 2001–2025: https://power.larc.nasa.gov/api/temporal/climatology/point (parameters SI_EF_TILTED_SURFACE, T2M; called 2026-10-28) |
| A12 | Derate for NASA cities | derate = 0.8604 − 0.00315 × T (monthly mean air temp, °C). Fitted on 48 PVWatts city-months (DC kWh ÷ plane-of-array kWh/m² × 0.4); residual SD 0.017 | Our fit. Check: NASA method vs PVWatts, annual: Phoenix −0.9%, Denver −1.2%, Los Angeles +5.5%, Miami −6.3%. Against PVWatts values in our AC200L dossier (30° tilt), our NASA figures run 2–10% low for Chicago, Atlanta and Seattle (conservative) |
| A13 | MPPT + battery charge efficiency η_c | 0.90 / **0.93** / 0.95 | **Our assumption** (no station publishes one) |
| A14 | Daily-profile model for parallel pairs | Half-sine power curve over the tilted surface's sunlit hours (8.3–12.3 h by city and month), capped at A9 | **Our assumption.** Using average days overstates parallel-pair energy slightly; on a clear day a capped pair gives 1.75× one panel, on average days 1.84–2.0× |
| A15 | Loads for break-even | Full-size ENERGY STAR fridge 1.50 kWh/day (median, 18–28 ft³); AirSense 11 + humidifier + heated tube 45 W × 8 h; station idle P1800 12 W, R4000 25 W (assumed); η 0.85 | ENERGY STAR dataset https://data.energystar.gov/resource/p5st-her9.json ; ResMed figures and idle assumptions as in the P1800 and R4000 dossiers |

---

## 1. How many SP037 per input: series, parallel and cold mornings

**Formula:** cold Voc = Voc × NEC factor (or × (1 + 0.0030 × (25 − T))). Parallel Isc = n × 11.7 A.

| Temperature | 1 panel Voc (NEC / −0.30 %/°C) | 2 in series Voc (NEC / −0.30 %/°C) |
|---|---|---|
| 25 °C | 45.3 / 45.3 V | 90.6 / 90.6 V |
| 10 °C | 48.0 / 47.3 V | 96.0 / 94.7 V |
| 0 °C | 49.8 / 48.7 V | 99.7 / 97.4 V |
| −10 °C | 51.6 / 50.1 V | 103.3 / 100.1 V |
| −30 °C | 54.8 / 52.8 V | 109.6 / 105.5 V |
| −40 °C | 56.6 / 54.1 V | 113.2 / 108.3 V |

| Station input | 1 SP037 | 2 in series | 2 in parallel | 3+ in parallel |
|---|---|---|---|---|
| P1800 (11–60 V, 13 A, 650 W; 1 input) | **OK** at any US temperature (≤56.6 V) | **No.** 90.6 V > 60 V. Even the US page's 95 V Voc is exceeded below about 9 °C (β assumed) or 15 °C (NEC) | Voltage OK. Isc 23.4 A vs 13 A: **relies on current limiting** (A6). Caps at 455–494 W | No gain in good sun; not documented; skip |
| R4000 (12–60 V, 13 A, 650 W; 3 inputs) | **OK**; up to 3 panels, one per input | **No** (manual warns of damage over 60 V) | Same as P1800, per input → up to 6 panels | skip |
| BLUETTI AC180 (12–60 V Voc, 10 A, 500 W) | OK. Imp 10.69 A is just over 10 A at full sun: slight clip (≈374 W max) | No | Voc OK; caps at 350–380 W | no |
| BLUETTI Elite 200 V2 (12–60 V, 20 A, 1,000 W) | OK | No | Voc OK; Isc 23.4 A vs 20 A, mild clip at full sun (≈740 W) | no |

**What this means.** With SP037s, no station here gets more than about 475 W per input, because the panel's 37 V cannot be stacked under a 60 V limit. That is why 2,000 W of R4000 solar input is unreachable with this panel: 650 W per input needs a panel near 50 V Vmp at 13 A.

## 2. Output in good sun

ALLPOWERS' manual text and owners agree on **260–320 W** in good sun (A2). PVWatts' default losses (14.08%) plus a warm cell give about 400 × 0.86 × 0.92 ≈ 316 W at 1,000 W/m², the top of that range. We use 260 / 290 / 320 W for "good sun" refill hours.

"Hours of good sun" means hours when a south-facing SP037 delivers 260–320 W: roughly 10 a.m. to 2 p.m. on a clear day.

## 3. Daily yield per SP037 (DC at the panel, kWh/day)

Fixed south tilt (35° for PVWatts cities, latitude tilt for NASA cities), no re-aiming. Re-aiming through the day adds more (not modeled). Into the battery = these × η_c (0.93 base).

| City (data) | Winter | Spring | Summer | Fall | Annual avg | Worst month | Best month |
|---|---|---|---|---|---|---|---|
| Phoenix, AZ (PVWatts) | 1.89 | 2.24 | 2.03 | 2.04 | 2.05 | 1.83 (Jan) | 2.33 (Apr) |
| Los Angeles, CA (PVWatts) | 1.68 | 1.99 | 2.14 | 1.98 | 1.95 | 1.56 (Dec) | 2.24 (Aug) |
| Denver, CO (PVWatts) | 1.67 | 2.03 | 2.00 | 1.87 | 1.89 | 1.55 (Dec) | 2.07 (Mar) |
| Miami, FL (PVWatts) | 1.75 | 1.88 | 1.62 | 1.73 | 1.75 | 1.54 (Jun) | 2.04 (Mar) |
| Dallas, TX (NASA POWER) | 1.38 | 1.65 | 1.81 | 1.60 | 1.61 | 1.32 (Dec) | 1.83 (Jul) |
| Atlanta, GA (NASA POWER) | 1.32 | 1.72 | 1.63 | 1.56 | 1.56 | 1.20 (Dec) | 1.79 (Apr) |
| Kansas City, MO (NASA POWER) | 1.25 | 1.61 | 1.76 | 1.51 | 1.54 | 1.14 (Dec) | 1.79 (Jul) |
| Chicago, IL (NASA POWER) | 0.97 | 1.54 | 1.67 | 1.31 | 1.38 | 0.82 (Dec) | 1.71 (Jul) |
| New York, NY (NASA POWER) | 1.11 | 1.57 | 1.63 | 1.33 | 1.41 | 0.93 (Dec) | 1.67 (Jul) |
| Minneapolis, MN (NASA POWER) | 1.19 | 1.60 | 1.73 | 1.31 | 1.46 | 0.87 (Dec) | 1.81 (Jul) |
| Seattle, WA (NASA POWER) | 0.71 | 1.37 | 1.75 | 1.13 | 1.25 | 0.57 (Dec) | 1.84 (Jul) |
| **11-city mean** | | | | | **1.62** | | |

Seasons: Dec–Feb, Mar–May, Jun–Aug, Sep–Nov. Uncertainty about ±10% (data source and foldable-panel losses).

## 4. Refill: hours of good sun and average days

**Hours of good sun, 0–100% (ESTIMATE):** hours = capacity Wh ÷ (input W × η_c), input W = Σ per input of min(panels × 260–320 W, cap).

| Station | 1 SP037 | 2 SP037 | 3 SP037 | 5 SP037 |
|---|---|---|---|---|
| P1800, 1,024 Wh | **3.4–4.4 h (base 3.8)** | 2.2–2.5 h (base 2.3), parallel | no faster than 2 | no faster than 2 |
| R4000, 3,456 Wh | 11.4–14.8 h (base 12.8) | 5.7–7.4 h (base 6.4) | **3.8–4.9 h (base 4.3)** | 2.8–3.3 h (base 3.0), layout 2+2+1 |

**Average days to refill from empty, base (annual-average day / December day / June day):**

| Station × panels | Phoenix | Los Angeles | Denver | Miami | Dallas | Atlanta | Kansas City | Chicago | New York | Minneapolis | Seattle |
|---|---|---|---|---|---|---|---|---|---|---|---|
| P1800 × 1 | 0.5 / 0.6 / 0.5 | 0.6 / 0.7 / 0.5 | 0.6 / 0.7 / 0.5 | 0.6 / 0.7 / 0.7 | 0.7 / 0.8 / 0.6 | 0.7 / 0.9 / 0.7 | 0.7 / 1.0 / 0.6 | 0.8 / 1.3 / 0.7 | 0.8 / 1.2 / 0.7 | 0.8 / 1.3 / 0.7 | 0.9 / 1.9 / 0.7 |
| P1800 × 2 | 0.3 / 0.3 / 0.3 | 0.3 / 0.4 / 0.3 | 0.3 / 0.4 / 0.3 | 0.3 / 0.3 / 0.4 | 0.3 / 0.4 / 0.3 | 0.4 / 0.5 / 0.3 | 0.4 / 0.5 / 0.3 | 0.4 / 0.7 / 0.3 | 0.4 / 0.6 / 0.3 | 0.4 / 0.6 / 0.3 | 0.4 / 1.0 / 0.3 |
| R4000 × 1 | 1.8 / 2.0 / 1.7 | 1.9 / 2.4 / 1.8 | 2.0 / 2.4 / 1.8 | 2.1 / 2.3 / 2.4 | 2.3 / 2.8 / 2.1 | 2.4 / 3.1 / 2.2 | 2.4 / 3.3 / 2.1 | 2.7 / 4.5 / 2.2 | 2.6 / 4.0 / 2.3 | 2.5 / 4.3 / 2.2 | 3.0 / 6.5 / 2.3 |
| R4000 × 2 | 0.9 / 1.0 / 0.9 | 1.0 / 1.2 / 0.9 | 1.0 / 1.2 / 0.9 | 1.1 / 1.1 / 1.2 | 1.2 / 1.4 / 1.0 | 1.2 / 1.5 / 1.1 | 1.2 / 1.6 / 1.0 | 1.3 / 2.3 / 1.1 | 1.3 / 2.0 / 1.1 | 1.3 / 2.1 / 1.1 | 1.5 / 3.2 / 1.1 |
| R4000 × 3 | 0.6 / 0.7 / 0.6 | 0.6 / 0.8 / 0.6 | 0.7 / 0.8 / 0.6 | 0.7 / 0.8 / 0.8 | 0.8 / 0.9 / 0.7 | 0.8 / 1.0 / 0.7 | 0.8 / 1.1 / 0.7 | 0.9 / 1.5 / 0.7 | 0.9 / 1.3 / 0.8 | 0.8 / 1.4 / 0.7 | 1.0 / 2.2 / 0.8 |
| R4000 × 5 | 0.4 / 0.4 / 0.4 | 0.4 / 0.5 / 0.4 | 0.4 / 0.5 / 0.4 | 0.4 / 0.5 / 0.5 | 0.5 / 0.6 / 0.4 | 0.5 / 0.6 / 0.4 | 0.5 / 0.7 / 0.4 | 0.5 / 0.9 / 0.4 | 0.5 / 0.8 / 0.5 | 0.5 / 0.9 / 0.4 | 0.6 / 1.3 / 0.5 |

Formula: days = capacity ÷ (daily panel kWh × panels, capped per A14, × η_c). A value under 1.0 means the battery fills partway through one average day. Worst/best cases shift these by about −3% to +3% (η_c) and ±10% (yield).

## 5. Break-even: panels for a fridge + CPAP day

**Formula:** need from the battery = (fridge Wh + CPAP Wh + 24 × idle) ÷ η. Panels = need ÷ (daily panel kWh × η_c). The battery must also bridge the night: night need (14 h) = fridge × 14/24 + CPAP + idle × 14.

| Station | Daily need (base) | Night need vs usable | Panels, annual-average day | Panels, December | Panels, June |
|---|---|---|---|---|---|
| P1800 | 2,532 Wh | 1,405 Wh vs 870 Wh: **fails** | 1.3 (Phoenix) to 2.2 (Seattle) | 1.5 to 4.8 (max 2 fit) | 1.3 to 1.8 |
| R4000 | 2,899 Wh | 1,587 Wh vs 2,938 Wh: OK | 1.5 (Phoenix) to 2.5 (Seattle) → **2–3** | 1.7 to 5.4 → **2–4, Seattle 6** | 1.4 to 2.0 → **2** |

Loads: full-size ENERGY STAR fridge median 1,504 Wh/day; AirSense 11 + humidifier + heated tube 45 W × 8 h = 360 Wh; idle 12 W (P1800) or 25 W (R4000), assumed.

**What this means.** For a P1800 the limit is the battery, not the panels: even two panels can't help a 1 kWh battery through 14 hours of fridge + heated CPAP. It does work with a top-freezer ENERGY STAR fridge (about 1.0 kWh/day) and the CPAP's humidifier off: night need 838 Wh vs 870 Wh usable (base), with 0.9–1.4 panels needed by city on an average day (daily need 1,629 Wh). On an R4000, two SP037s cover the day in the Sun Belt for most of the year; the northern half of the country needs three, and four in December.

## 6. Other stations with 1–2 SP037 (short table)

| Station | Input limit | 1 SP037: good-sun hours / average-US-day days | 2 SP037 (parallel): good-sun hours / days | Notes |
|---|---|---|---|---|
| BLUETTI AC180, 1,152 Wh | 12–60 V Voc, 10 A, 500 W | **3.8–4.9 h** (base 4.3) / 0.76 days (0.6 Phoenix to 1.0 Seattle; 2.2 in a Seattle December) | 3.2–3.7 h (base 3.4) / 0.43 days | 10 A caps a pair near 365 W; the second panel mostly helps mornings, evenings and cloud |
| BLUETTI Elite 200 V2, 2,073.6 Wh | 12–60 V, 20 A, 1,000 W | **6.8–8.9 h** (base 7.7) / 1.37 days (1.1 to 1.8) | **3.4–4.4 h** (base 3.8) / 0.69 days | 20 A takes a pair almost unclipped; 2S is still over 60 V |
| ALLPOWERS P1800, 1,024 Wh | 11–60 V, 13 A, 650 W | 3.4–4.4 h / 0.68 days | 2.2–2.5 h / 0.35 days | see §4 |
| ALLPOWERS R4000, 3,456 Wh | 3 × (12–60 V, 13 A, 650 W) | 11.4–14.8 h / 2.29 days | 5.7–7.4 h / 1.15 days (one per input) | see §4 |

Average-day figures use the 11-city mean (1.62 kWh/day per panel at the panel, 1.51 into the battery). Parallel pairs on the AC180 and Elite 200 V2 rely on those inputs limiting current, as with ALLPOWERS.

## 7. Kit math: P1800 + 1× SP037 ($731)

Full table in the P1800 dossier §9. In short, base case: one panel puts 0.66–2.08 kWh/day into the P1800 by city and season. A full-size fridge + heated CPAP + router day needs 2,955 Wh, so the panel covers **22–70%** of it, and the battery runs out about 7.5 hours into the night. A mini fridge + CPAP without humidifier + router day (1,653 Wh) is covered 91–126% year-round in Phoenix, Los Angeles, Denver and Miami, 64–102% from spring to fall in the other seven cities, and 40–77% in their winters. Its night need (850 Wh) just fits the battery.

---

## Summary table (all ESTIMATES)

| Question | Answer |
|---|---|
| Real output in good sun | 260–320 W |
| Daily yield per panel at the panel | 0.57 kWh (Seattle, Dec) to 2.33 kWh (Phoenix, Apr); 11-city mean 1.62 |
| Panels per XT60 input | 1 in series terms; 2 in parallel only if the input current-limits |
| Max useful SP037 input per station | P1800 ≈ 475 W (2 panels); R4000 ≈ 1,425 W (6 panels); AC180 ≈ 365 W; Elite 200 V2 ≈ 520–740 W (2 panels) |
| P1800 refill, 1 / 2 panels | 3.4–4.4 h / 2.2–2.5 h of good sun |
| R4000 refill, 1 / 2 / 3 / 5 panels | 11.4–14.8 / 5.7–7.4 / 3.8–4.9 / 2.8–3.3 h of good sun |
| AC180 refill, 1 / 2 panels | 3.8–4.9 h / 3.2–3.7 h |
| Elite 200 V2 refill, 1 / 2 panels | 6.8–8.9 h / 3.4–4.4 h |
| Fridge + heated CPAP break-even | R4000: 2–3 panels (4 in a northern December). P1800: battery can't bridge the night |

## Open questions / couldn't verify

- **Temperature coefficients.** ALLPOWERS publishes none for the SP037. The NEC table is conservative; our −0.30 %/°C cross-check is an assumption. Neither changes the conclusion: one panel stays under 60 V at −40 °C; two in series exceed 60 V at any temperature.
- **Parallel pairs on 13 A inputs.** No ALLPOWERS document states a maximum Isc. The SP039 pairing and the manual drawing imply current limiting. Before publishing "two in parallel per input" advice, get it in writing from ALLPOWERS.
- **"260-320W" in the SP037 manual** sits in the PDF's text layer but does not show in the rendered page, so its exact wording is unknown. The owner reviews back the range.
- **IP rating.** Page IP67; manual IP66.
- **PVWatts coverage.** The DEMO_KEY was rate-limited after 4 cities (Phoenix, Los Angeles, Denver, Miami). The other 7 use NASA POWER with a fitted derate (A12). A personal NREL key would let us rerun all 11 on PVWatts.
- **Clear-day vs average-day.** Days-to-refill use average days. On a run of clear days refills are faster; on cloudy days a panel can give a third of the average or less.
- **Re-aiming.** Owners who turn the panel toward the sun two or three times a day will see more than these fixed-tilt figures. Not modeled.
