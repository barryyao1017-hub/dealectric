# BLUETTI AC200L: use-case math ("how long will it run my X")

Angle 4 of 5. Researched 2026-10-28. Every runtime below is an **ESTIMATE**: it is calculated from the inputs in the assumptions table. It is not a measurement. Formulas are shown so a reader can swap in their own appliance's number.

**Headline (estimates):** usable AC energy is about 1,700–1,900 Wh of the 2,048 Wh, with 12–18 W of idle draw while the inverter is on. That gives a full-size ENERGY STAR fridge about 18–41 h (base 28 h), and an AirSense 11 with heated humidifier and heated tube 3–5 nights (base 4). A 1,500 W space heater gets about 68–75 min. A 13.5K BTU RV air conditioner gets about 0.9–1.3 h of continuous compressor time; it needs a soft starter to start reliably. The fridge + router + lights outage bundle lasts about 13–30 h (base 20 h), and about 3 days with one B500K.

## Spec check against BLUETTI (what our math depends on)

Checked against the BLUETTI US user manual (V3.0, the PDF linked from BLUETTI's US support page) and BLUETTI's US store and support FAQs. The product page itself renders its specs with JavaScript, so its spec text could not be read directly.

| Our record | BLUETTI says | Match? |
|---|---|---|
| 2,048 Wh LiFePO4 | "2,048Wh (40Ah)", LiFePO4 | yes |
| 2,400 W continuous AC | "2,400W in total", 120 VAC, 20 A | yes. All AC outlets **share** 2,400 W, the TT-30 included |
| 3,600 W Power Lifting | Resistive loads only, "between 2,400W–3,600W". "Actual operating power remains at 2,400W." Off by default | yes, but it is a voltage-limiting mode. It does not give 3,600 W of real output |
| Surge | Overload: 2,520–3,000 W for 2 min; 3,000–3,600 W for 5 s; >3,600 W for 0.5 s | not in our record; this is what the motor-start math uses |
| 4× 120 V + 1× TT-30 | "20A AC Outlet ×4", "30A AC Outlet ×1 … NEMA TT-30" | yes |
| 2× USB-C 100 W | PD 3.0, up to 20 V/5 A each | yes |
| 12 V/10 A car port | "12V/10A … 12V DC appliances up to 120W" | yes |
| also | 48 V DC port, 44.8–57.6 V / 8 A; 2× USB-A 18 W | not in our record |
| Solar 1,200 W, 12–145 V, 15 A | "12V to 145VDC", "15A Max.", "1,200W Max." | yes |
| AC charging 2,400 W | Turbo 2,400 W max. The manual text says "80% … in just 45 minutes"; its spec table says "0%-80% in 60 minutes". **Default max grid input current is 15 A** (≈1,800 W at 120 V). Raising it to 20 A needs a password from BLUETTI support | partly. On a normal 15 A US outlet, Turbo is capped near 1,800 W by default |
| Car charging | "maximum of 96W" (US manual). UK reviewers saw 120 W | our record has no figure; use 96 W for the US |
| 20 ms UPS | "Switching time ≤20ms" | yes. The manual also disclaims liability for use with devices that need a "high-performance" UPS, "medical equipment" included |
| B300K 2,764.8 Wh | B300K "for AC200L/AC300", 2,764.8 Wh. Up to 2× B300K → 7,577.6 Wh | yes |
| B500K / "AC200L + B500K" 7,168 Wh | B500K = 5,120 Wh. "AC200L + B500K: 2,400W, 7,168Wh". Up to 2× B500K → 12,288 Wh (P090A cable) | yes |
| Runtime formula | "Operation time = Battery Capacity (Wh) × DoD × η ÷ (Load Power + AC200L Self-consumption)", DoD 95%, η "typically over 93%", self-consumption "approximately 12W" | used as our base case |

Note: the US manual still lists only B210/B230/B300 as expansion options. The B300K and B500K compatibility figures come from BLUETTI's support FAQs. The two FAQs disagree on mixing: the B300K FAQ says the "AC200L can only mix with B300 and B300K", while the B500K FAQ says "You can only mix with B300, B300K, and B500K".

## Assumptions table (inputs, with sources)

Dates are publication dates where shown; otherwise "acc. 2026-10-28" (accessed).

| # | Input | Value used | Source |
|---|---|---|---|
| A1 | Battery | 2,048 Wh | BLUETTI US user manual V3.0, spec table: https://s4.bluettipower.com/bluetti_lgf/support/2025/05/cca63f10-4c44-4b89-9e33-d235f2c19f93.pdf (uploaded 2025-05, linked from https://support.bluettipower.com/en-us/products/ac200l; acc. 2026-10-28) |
| A2 | DoD | 95% | Same manual, Appx. 1 |
| A3 | Inverter efficiency η | base 0.93 (BLUETTI); low 0.88 (**our assumption** for a 120 V unit with compressor loads; not measured) | Manual Appx. 1 |
| A4 | Measured AC energy delivered (UK 230 V unit) | 1.77 kWh at ~2.4 kW; **1.90 kWh at 1,050 W**; 1.76 kWh at 200 W | Trusted Reviews, Simon Handby, 2024-04-19: https://www.trustedreviews.com/reviews/bluetti-ac200l |
| A5 | Measured efficiency range | 85–93% depending on load (UK unit) | The Ambient, Paul Lamkin, 2024-09-17: https://www.the-ambient.com/reviews/bluetti-ac200l-expandable-power-station-review/ |
| A6 | AC self-consumption | 12 W (manual); **18 W** ("AC output no-load power consumption 18W") | Manual Appx. 1; BLUETTI staff, forum 2023-12-13: https://community.bluettipower.com/t/200l-ac-and-dc-watt-draw-while-turned-on-with-no-load/26730 (now redirects to forum.bluettipower.com; read from the web.archive.org snapshot of 2026-01-20) |
| A7 | DC self-consumption | 8 W ("DC output no-load power consumption 8W") | Same BLUETTI staff post |
| A8 | DC path efficiency (battery → 12 V port / USB-C) | 0.88–0.95, **our assumption** (BLUETTI publishes none) | none found |
| A9 | Real-world owner result | AC200L + B300K (4,812.8 Wh), fridge + freezer + network gear at ~191–194 W: "about 18 hrs" (≈3.5 kWh, ≈73% of nameplate) | Forum post 2025-01-06: https://community.bluettipower.com/t/actual-available-kwh/35454 (web.archive.org snapshot 2026-04-15). BLUETTI_CARE reply in the same thread confirms "DOD … 95%, and n is 93%. The self-consumption when the AC is on is 18W" |
| A10 | Full-size ENERGY STAR fridge | 297 / 457 / 685 kWh/yr (p10 / median / p90; n = 2,987 non-compact models) → 0.81 / 1.25 / 1.88 kWh/day | ENERGY STAR Certified Residential Refrigerators dataset (updated 2026-10-27): https://data.energystar.gov/resource/p5st-her9.json (acc. 2026-10-28). By type, medians: top-freezer 363, bottom-freezer 556, side-by-side 640 kWh/yr |
| A11 | Mini fridge (compact, ≤4.5 ft³) | 197 / 227 / 320 kWh/yr → 0.54 / 0.62 / 0.88 kWh/day (n = 1,349) | Same dataset |
| A12 | Chest freezer | Compact chest: 172 / 196 / 225 kWh/yr (n = 40). Full-size chest: 201 / 218 / 346 (n = 9). Used 172 / 213 / 346 → 0.47 / 0.58 / 0.95 kWh/day | ENERGY STAR Certified Residential Freezers: https://data.energystar.gov/resource/8t9c-g3tn.json (updated 2026-10-27; acc. 2026-10-28) |
| A13 | Fridge / freezer running and starting watts | Fridge 150–400 W running, 800–1,200 W starting. Freezer 100–500 W running, 500–1,000 W starting | Champion Power Equipment generator wattage chart, 2026-04-17: https://www.championpowerequipment.com/generator-wattage-chart/ |
| A14 | ResMed AirSense 11 | 65 W power supply. "Typical power consumption 56.1W (111.5VA)", "Peak power consumption 73.2W" (spec for the device with humidifier tub and tubing) | AirSense 11 user guide (Americas), 398133/2, 2021-10: https://document.resmed.com/documents/products/machine/airsense-11/user-guide/airsense11_user-guide_amer_mul.pdf |
| A15 | ResMed measured draw by configuration (AirSense **10**, used as the closest ResMed-published proxy for 11) | Device only 7 Wh per hour; + humidifier 22; + humidifier + ClimateLineAir 34 (APAP 8–15 cm H2O, humidity 6, tube 28 °C; Yokogawa power meter) | ResMed, "Power consumption of Air10 devices", 1018673/1, 2015-03: https://document.resmed.com/documents/products/machine/air10-lumis-series/Power+consumption+Air10+devices.pdf |
| A16 | AirSense 11 DC/DC converter | Input "12V/24V 10A/5A"; output "24 V, 3,75A" (90 W); powers the device with HumidAir humidifier + ClimateLineAir tube; cigarette-lighter plug | ResMed shop: https://shop.resmed.com/cpap-spare-parts/airsense-11-converter/p/39231 (acc. 2026-10-28) |
| A17 | Philips DreamStation 2 | No published watt draw. "An 80W power supply is required to support humidification". AC input 100–240 VAC, 2.0–1.0 A. DC operation only with a Philips Respironics DC cord | DreamStation 2 instructions for use: https://www.documents.philips.com/assets/Instruction%20for%20Use/20211202/7e52e95bb1a343a4a223adf201582311.pdf (asset dated 2021-12-02) |
| A18 | DreamStation 2 draw used | Without heat 10–30 W; with humidifier + heated tube 40–80 W. **Our assumption**, bounded by the 80 W supply and the ResMed figures; not measured | none found. The Champion chart's generic CPAP figures (30–60 W without heat, 60–120 W with heated humidifier) look high next to ResMed's measured 7–34 W |
| A19 | Philips US availability | US sales of new CPAPs stopped in 2024 under the FDA consent decree; not resumed as of March 2026 | Gouveia & Capasso, "Philips Respironics is Returning to CPAP", 2026-03-11: https://sleepdocs.substack.com/p/philips-respironics-is-returning |
| A20 | Space heater | 750–1,500 W | Champion chart (A13) |
| A21 | Electric blanket | 50–100 W, as given in the brief. **Not verified** against a manufacturer this session | none fetched |
| A22 | Dometic Penguin II 13.5K (640315 series) | Compressor rated-load amps 12.5–12.6 A, **locked-rotor amps 61–63 A**; fan rated-load 2.6–3.5 A, fan LRA 8.5–10 A. Minimum generator 3.5 kW | Dometic installation instructions, Form 3314438.000, 8/18: https://www.dometic.com/externalassets/dometic-penguin-ii-13-5k_63522.pdf |
| A23 | Coleman-Mach 15K | 14.2 A "High" cooling, "Running Watts Standard: 1611" (Camping World item 163138); 14.8 A, 1,560 W (Overton's item 122255). No LRA published | https://www.campingworld.com/coleman-mach-15000-btu-roughneck-air-conditioner-with-updated-shroud-white-163138.html ; https://overtons.com/coleman-mach-15-air-conditioner-122255.html (retailer pages, acc. 2026-10-28) |
| A24 | RV AC generator-chart figures | 13.5K: 1,500–2,000 W running, 2,800–3,500 W starting. 15K: 2,000–2,500 W running, 3,500–4,500 W starting | Champion chart (A13) |
| A25 | Owner reports of the AC200L on an RV AC | 13.5K "runs at 1450Watts"; it "faulted almost immediately" from the TT-30. Starting the fan first, then the compressor, worked. Another owner: "Mine runs 15,000 btu with the SoftStart". Advice to turn off the converter/charger breaker. 12K boat AC ~1,250 W, "about 90 minutes" | BLUETTI forum thread, 2024-07-29 to 2024-08-06: https://community.bluettipower.com/t/ac200l-and-13-5k-btu-air-conditioner/32048 (web.archive.org snapshot 2026-04-10) |
| A26 | Soft starter | Micro-Air EasyStart: "Can reduce your current by up to 75%". Retailer listings quote 65–75% vs. LRA (seen in search results, not fetched) | https://www.micro-air.com/products_easystart_364_softstarter_microair.cfm (acc. 2026-10-28) |
| A27 | Sump pumps, furnace blower | 1/3 HP sump: 500–800 W running, 1,000–1,600 W starting. 1/2 HP sump: 800–1,050 running, 1,300–2,150 starting. Furnace fan (1/2 HP): 300–800 running, 800–1,600 starting | Champion chart (A13) |
| A28 | Router/modem; LED bulb; TV | Router/modem 10–20 W; LED bulb 8–15 W each; TV (portable/camping) 50–150 W; RV fridge 150–600 W | Champion chart (A13) |
| A29 | Starlink | Standard: "Average: 75 - 100 W". Mini: "Average: 25-40 W", input 12–48 V 60 W, USB PD "100 W, 20V/5A Minimum" | Starlink spec sheets: https://www.starlink.com/public-files/specification_sheet_standard.pdf , https://www.starlink.com/public-files/specification_sheet_mini.pdf (acc. 2026-10-28) |
| A30 | Solar yield | PVWatts v8, 1 kW fixed array, 30° tilt, south-facing, default 14% system losses, NSRDB TMY. DC kWh/day per kW of panels: Phoenix 5.13 avg (4.42 Dec / 5.91 best month); Denver 4.71 (3.71–5.31); Houston 4.09; Atlanta 4.08; Chicago 3.83 (2.21 Dec); Seattle 3.21 (1.28 Dec) | PVWatts API (NREL is now the "National Laboratory of the Rockies"; endpoint developer.nlr.gov): https://developer.nlr.gov/api/pvwatts/v8.json ; defaults: https://pvwatts.nlr.gov/pvwatts.php (acc. 2026-10-28) |
| A31 | Solar charge efficiency (MPPT → battery) | 0.95, **our assumption** (not published) | none found |
| A32 | Wall charge, measured (UK unit) | Standard 1,200 W: 2 h 06 min, 2.35 kWh from the wall (87.3%). Silent: just under 3 h (87.6%). Turbo: 75 min after cooling (first try throttled to 1,200 W after ~15%), 2.4 kWh (85.3%) | Trusted Reviews (A4). The Ambient (A5): ~87 min Turbo, ~2 h Standard, just over 3 h Silent |
| A33 | RV 12 V loads (furnace blower 36–48 W at 30–50% duty; water pump 60–96 W for 15–30 min; LED lights 20–40 W for 4–5 h; RV converter efficiency 80–85%) | **Our assumptions**, not verified against Suburban/Atwood/Shurflo documents this session | none |
| A34 | Phone charge | 15–20 Wh per full charge (typical 4,000–5,000 mAh × 3.85 V, plus losses). **Our assumption** | none |

### Three efficiency cases used throughout

- **Low:** usable AC energy U = 2,048 × 0.95 × 0.88 = **1,712 Wh**; idle S = 18 W.
- **Base (BLUETTI's own formula):** U = 2,048 × 0.95 × 0.93 = **1,809 Wh**; S = 12 W.
- **High (anchored to Trusted Reviews' measured 1.90 kWh):** U = **1,900 Wh**; S = 12 W.

The low case pairs with the high end of each appliance's consumption; the high case with the low end. That gives honest low–high ranges.

---

## 1. Usable energy (AC path vs DC path)

**Formula (BLUETTI):** hours = U ÷ (load W + self-consumption W), where U = 2,048 × DoD × η.

| Path | Usable energy (ESTIMATE) | Idle draw with nothing plugged in | Idle alone empties a full battery in (ESTIMATE) |
|---|---|---|---|
| AC (inverter on) | 1,712–1,900 Wh (base 1,809) | 12 W (manual) to 18 W (BLUETTI staff) | 4.0–6.6 days (1,712 ÷ 18 ÷ 24 to 1,900 ÷ 12 ÷ 24) |
| DC (12 V port / USB-C) | 1,712–1,848 Wh (2,048 × 0.95 × 0.88–0.95, A8) | 8 W | 8.9–9.6 days |

**Generic runtime by load, AC path (ESTIMATE, hours = U ÷ (P + S)):**

| Load | Low | Base | High |
|---|---|---|---|
| 50 W | 25.2 h | 29.2 h | 30.6 h |
| 100 W | 14.5 h | 16.2 h | 17.0 h |
| 200 W | 7.9 h | 8.5 h | 9.0 h |
| 500 W | 3.3 h | 3.5 h | 3.7 h |
| 1,000 W | 1.7 h | 1.8 h | 1.9 h |
| 1,500 W | 1.1 h | 1.2 h | 1.3 h |
| 2,400 W | 0.71 h | 0.75 h | 0.79 h (measured at ~2.4 kW: 49 min, 1.77 kWh, A4) |

**What this means:**
- Idle draw matters a lot at small loads. At 50 W, 12–18 W of idle is 24–36% overhead. Below about 100 W, running DC loads from the 12 V port or USB-C with the inverter off buys back hours.
- BLUETTI's formula is a little conservative against Trusted Reviews' measurement on a UK 230 V unit. Our US 120 V unit may run closer to the formula, since higher current means more loss; this is not verified. The forum owner's real-world fridge/freezer/network test (A9) came in about 11% under the base formula: 18 h observed vs 20.2 h predicted = 4,812.8 × 0.95 × 0.93 ÷ (192 + 18). Treat the low case as realistic for cycling compressor loads.
- **ECO-mode gotcha.** The AC-ECO and DC-ECO modes are on by default. Per the manual, the outlet "will automatically turn off" if the load stays below a threshold for a set time, and BLUETTI says to "disable ECO Mode when charging a small device that consumes less than 60W". That covers a CPAP (7–56 W) and a fridge between compressor cycles (near 0 W). **Turn AC-ECO off before relying on the unit overnight or in an outage.** The manual gives no threshold or timer.

## 2. Refrigerator, mini fridge, chest freezer

**Formula:** days = U ÷ (daily kWh × 1,000 + 24 × S). Average watts = daily Wh ÷ 24. Compressor duty cycle = average W ÷ running W.

| Appliance | Daily use (p10 / median / p90) | Avg draw | Duty cycle at 150 W running (100–400 W range) | Runtime, ESTIMATE (low / base / high) |
|---|---|---|---|---|
| Full-size ENERGY STAR fridge | 0.81 / 1.25 / 1.88 kWh | 34 / 52 / 78 W | ~35% (13–52%) | **0.74 / 1.17 / 1.72 days** (18 / 28 / 41 h) |
| Mini fridge (≤4.5 ft³) | 0.54 / 0.62 / 0.88 kWh | 23 / 26 / 37 W | ~17% (6–26%) | **1.31 / 1.99 / 2.30 days** (31 / 48 / 55 h) |
| Chest freezer | 0.47 / 0.58 / 0.95 kWh | 20 / 24 / 40 W | ~16% (6–24%) | **1.24 / 2.08 / 2.50 days** (30 / 50 / 60 h) |

Worked example (full-size, base): 1,809 ÷ (1,252 + 24 × 12) = 1,809 ÷ 1,540 = 1.17 days.

**Startup surge vs the inverter.** The generator chart puts fridge starting at 800–1,200 W and freezer starting at 500–1,000 W (A13). Even both starting in the same instant (≤2,200 W) is under the 2,400 W continuous rating. Surge is not the limit for a fridge on this unit; daily kWh is.

**Caveats.**
- ENERGY STAR kWh/yr comes from DOE's standardized lab test. Real use shifts with room temperature, door openings and age. A pre-2010 fridge, or one in a hot garage, can use far more.
- The ENERGY STAR median varies widely by style. A top-freezer at 363 kWh/yr gets about 1.4 days base; a side-by-side at 640 kWh/yr gets about 0.9 days.
- BLUETTI's manual example uses a "40W refrigerator … about 34.7 hours". That is roughly a top-freezer ENERGY STAR model, not a typical bottom-freezer or side-by-side.

## 3. CPAP: nights at 8 h/night

**Formulas (ESTIMATE):**
- AC, unit switched off between nights: nights = U ÷ ((P + S) × 8)
- AC, unit left on 24 h (idle all day): nights = U ÷ (P × 8 + S × 24)
- DC (12 V port → CPAP's own DC converter or cord): nights = U_dc ÷ ((P + 8) × 8). We assume the CPAP's DC draw is about its AC-side figure, because the DC converter's losses stand in for the AC brick's losses. This is our assumption.

| Machine and setting | Draw used | AC, off between nights | AC, left on 24 h | DC via 12 V port |
|---|---|---|---|---|
| AirSense 11, device only (no humidifier) | 7–10 W (base 8.5) | **7.6–12.5** (base 11.0) | 3.3–5.5 (base 5.1) | **11.9–15.4** (base 13.5) |
| AirSense 11 + humidifier | 20–30 W (base 22) | **4.5–7.4** (base 6.7) | 2.5–4.2 (base 3.9) | 5.6–8.3 (base 7.4) |
| AirSense 11 + humidifier + ClimateLineAir heated tube | 34–56 W (base 45) | **2.9–5.2** (base 4.0) | 1.9–3.4 (base 2.8) | 3.3–5.5 (base 4.2) |
| DreamStation 2, no heat (assumed) | 10–30 W (base 20) | 4.5–10.8 (base 7.1) | 2.5–5.2 (base 4.0) | 5.6–12.8 (base 7.9) |
| DreamStation 2 + humidifier + heated tube (assumed) | 40–80 W (base 60) | 2.2–4.6 (base 3.1) | 1.6–3.1 (base 2.4) | 2.4–4.8 (base 3.3) |

Worked example (AirSense 11 with heated humidifier and tube, base, AC): 1,809 ÷ ((45 + 12) × 8) = 1,809 ÷ 456 = 4.0 nights.

**Notes.**
- Draw sources: AirSense 11 "typical 56.1 W" is ResMed's figure for the full humidified setup (A14). The 7 / 22 / 34 W split is ResMed's measured AirSense **10** data (A15); ResMed does not publish the same split for the 11, so we use the 10 as a proxy. Pressure, humidity and tube temperature settings move these a lot.
- **DC is better for CPAP mainly because of idle draw** (8 W vs 12–18 W). That roughly doubles nights for a device-only setup. With heated humidification the gap narrows to about 5–10%.
- DC hardware: the ResMed Air11 DC/DC converter takes 12 V at up to 10 A (A16), which exactly fits the AC200L's 12 V/10 A, 120 W port. Philips says to use only a Philips Respironics DC cord with the DreamStation 2 (A17).
- Leaving the AC on all day roughly halves CPAP nights. Turn the unit, or at least the inverter, off in the morning.
- Disable AC-ECO / DC-ECO (section 1), or the outlet may shut off mid-night under a light load.
- BLUETTI's manual disclaims liability for use with devices needing a "high-performance" UPS, "medical equipment" included. The 20 ms switchover is fine for most CPAPs, but say plainly that the unit is not a medical-grade backup.
- DreamStation 2: Philips stopped selling new CPAPs in the US in 2024 (A19). DS2 figures are for existing owners; new US buyers will mostly have ResMed.

## 4. Space heater and electric blanket

**Formula:** minutes = U ÷ (P + S) × 60.

| Load | Runtime, ESTIMATE (low / base / high) |
|---|---|
| Space heater on high, 1,500 W | **68 / 72 / 75 min** |
| Space heater on low, 750 W | **2.2 / 2.4 / 2.5 h** (134 / 142 / 150 min) |
| Electric blanket, 50 W | 25 / 29 / 31 h → about 3.6 nights at 8 h (base, unit off between nights) |
| Electric blanket, 100 W | 14.5 / 16.2 / 17.0 h → about 2.0 nights at 8 h (base) |

Worked example: 1,809 ÷ (1,500 + 12) = 1.20 h = 72 min. A thermostat that cycles the heater stretches wall-clock time; these figures are for continuous heating.

**Power Lifting's role: none for a normal US space heater.** BLUETTI's Power Lifting is only for resistive loads rated 2,400–3,600 W, and "actual operating power remains at 2,400W". It runs an oversize heater or kettle at reduced voltage; it does not add energy or output. A US plug-in heater tops out at 1,500 W (750–1,500 W, A20), which is already under 2,400 W. Leave Power Lifting off. Trusted Reviews saw it hold a 3,050 W kettle + toaster combo to about 2,000 W on the UK unit (A4).

**The efficient alternative:** a 1,500 W heater burns as much in 1 hour as a 50–100 W electric blanket does in 15–30 hours. For an outage night, a blanket (or heated mattress pad) plus a sleeping bag beats a space heater by more than 10×. The blanket wattage (A21) is the brief's range; we did not verify it against a manufacturer.

## 5. RV: the TT-30 outlet and rooftop air conditioners

**What the TT-30 can and can't do.** The outlet is a real NEMA TT-30 receptacle, so a 30 A RV cord plugs straight in. It is fed by the same 2,400 W (120 V, 20 A) inverter as the household outlets, and the total is shared. A 30 A shore pedestal supplies up to 3,600 W (30 A × 120 V); the AC200L supplies 2/3 of that, with short overload allowances (2,520–3,000 W for 2 min, 3,000–3,600 W for 5 s).

| Can (ESTIMATE, within 2,400 W) | Can't (over 2,400 W sustained) |
|---|---|
| Run the RV's 120 V panel: outlets, lights via converter, TV, fans, a residential or compact fridge | Rooftop AC **plus** microwave (1,450–1,930 W AC + 600–1,200 W microwave = 2,050–3,130 W) |
| Run **one** 13.5K or 15K rooftop AC alone, which uses about 60–80% of the inverter | RV electric water heater (1,200–1,500 W, A24 chart) at the same time as the AC |
| Feed the RV converter to charge the house battery, at a cost (see below) | Two rooftop ACs |

**Running watts (inputs):**
- 13.5K: Dometic rated-load amps are 12.5–12.6 A compressor + 2.6–3.5 A fan ≈ 15.1–16.1 A ≈ 1,810–1,930 W at 120 V (worst-case rated load). One owner saw 1,450 W. Champion chart: 1,500–2,000 W. Used: **1,450–1,930 W, base 1,700**.
- 15K: Coleman-Mach retailer listings give 1,560–1,611 W standard running, 14.2–14.8 A on high. Champion chart: 2,000–2,500 W; its top end would exceed the inverter. Used: **1,560–2,000 W, base 1,650**.

**Starting (ESTIMATE):**
- Without a soft starter: Dometic compressor LRA is 61–63 A. With the fan already running (~3.5 A), the inrush is about 64.5–66.5 A × 120 V ≈ **7,700–8,000 VA** for a fraction of a second. That is about twice the AC200L's ">3,600W @ 0.5s" overload tier, and BLUETTI does not publish its peak current limit. Owner evidence is mixed: one 13.5K faulted the AC200L on the first try, then started when the fan was switched on first (A25). Expect "maybe, unit-dependent".
- With a soft starter (EasyStart, "up to 75%"; retailers say 65–75%): 61–63 A × 0.25–0.35 + 3.5 A fan ≈ 19–26 A ≈ **2,250–3,070 W**. That fits the 2,520–3,000 W / 2-minute overload band, with the top end touching the 5-second band. One owner runs a 15K with a SoftStart on an AC200L (A25). **Likely starts; recommend a soft starter as a requirement, not an option.**
- Also turn off the RV converter/charger breaker before starting the AC. The converter can draw enough while charging the house battery to block the start (owner advice, A25).

**Hours of AC (ESTIMATE):** hours = U ÷ (AC W × duty + S).

| Setup | 13.5K, continuous compressor | 13.5K at 50% duty | 15K, continuous | 15K at 50% duty |
|---|---|---|---|---|
| AC200L alone | **0.9–1.3 h** (base 1.1) | 1.7–2.6 h (base 2.1) | **0.85–1.2 h** (base 1.1) | 1.7–2.4 h (base 2.2) |
| + 1× B300K (4,812.8 Wh) | 2.1–3.1 h (base 2.5) | ~2× | 2.0–2.8 h (base 2.6) | ~2× |
| + 1× B500K (7,168 Wh) | 3.1–4.5 h (base 3.7) | ~2× | 3.0–4.2 h (base 3.8) | ~2× |
| + 2× B300K (7,577.6 Wh) | 3.3–4.8 h (base 3.9) | ~2× | 3.1–4.5 h (base 4.0) | ~2× |
| + 2× B500K (12,288 Wh) | 5.3–7.8 h (base 6.3) | ~2× | 5.1–7.3 h (base 6.5) | ~2× |

Worked example (13.5K, base): 1,809 ÷ (1,700 + 12) = 1.06 h. That is consistent with the owner's 12K boat AC lasting "about 90 minutes" at ~1,250 W (A25). An overnight of RV air conditioning is not realistic on the base unit. Even 2× B500K covers only part of a hot night without a generator or a large array.

**Typical RV overnight load (no AC).** These inputs are mostly our assumptions (A33); treat this as order-of-magnitude.

| Item | Assumption | Wh/day |
|---|---|---|
| Furnace blower (12 V, via the RV converter) | 36–48 W × 30–50% × 10 h | 110–240 |
| Water pump (12 V) | 60–96 W × 0.25–0.5 h | 15–48 |
| LED lights (12 V) | 20–40 W × 4–5 h | 80–200 |
| TV (120 V) | 50–150 W × 3 h (A28) | 150–450 |
| 12 V items ÷ converter efficiency 0.80–0.85 | | adds ~15–20% to the 12 V items |
| **Total, fridge on propane** | | **≈390–1,060 Wh/day** |
| + compact/residential electric fridge (A11/A10 medians) | 0.62–1.25 kWh | ≈1,010–2,310 Wh/day |

Runtime (ESTIMATE): fridge on propane, **1.2–2.8 days** (base about 1.8); fridge on electric, **0.6–1.5 days**. An absorption RV fridge in electric mode can draw 150–600 W (A28). Keep it on propane when running from the AC200L.

## 6. Home outage bundle

**Core bundle (ESTIMATE):**

| Item | Low | Base | High |
|---|---|---|---|
| Full-size ENERGY STAR fridge (A10) | 814 Wh | 1,252 Wh | 1,877 Wh |
| Router + modem, 24 h (A28) | 10 W → 240 Wh | 15 W → 360 Wh | 20 W → 480 Wh |
| 4 LED bulbs (A28) | 4 × 8 W × 4 h = 128 Wh | 4 × 9 W × 5 h = 180 Wh | 4 × 15 W × 6 h = 360 Wh |
| Phones (A34) | 30 Wh | 40 Wh | 60 Wh |
| **Total per day** | **1,212 Wh** | **1,832 Wh** | **2,777 Wh** |
| **Runtime, AC200L alone** | **30.4 h** (high-efficiency case) | **20.5 h** | **12.8 h** (low-efficiency case) |

Formula: hours = U ÷ (daily Wh ÷ 24 + S). Base: 1,809 ÷ (76.3 + 12) = 20.5 h.

With expansion (days, ESTIMATE, low / base / high): +1 B300K 1.3 / 2.0 / 3.0; +1 B500K 1.9 / 3.0 / 4.4; +2 B300K 2.0 / 3.2 / 4.7; +2 B500K 3.2 / 5.1 / 7.6.

**Add-ons (ESTIMATE, each on its own unless noted):**
- **Starlink Standard** (75–100 W average, A29): alone **14.5–21.8 h** (base 18.2). Added to the base bundle, the day total is 3.93 kWh and the runtime drops to **about 10 h**. Starlink Standard alone uses about a full AC200L per day.
- **Starlink Mini** (25–40 W): on AC 29.5–51.4 h (base 40.7). Better: on a **USB-C port** (the AC200L's USB-C does 20 V/5 A = 100 W, meeting the Mini's "100 W, 20V/5A minimum"), 36–56 h (base 44) with the inverter off.
- **Sump pump.** Start: 1/3 HP 1,000–1,600 W; 1/2 HP 1,300–2,150 W (A27). Both are under 2,400 W. A 1/2 HP start coinciding with a fridge start (800–1,200 W) gives 2,100–3,350 W, which falls in the 2-minute / 5-second overload bands: probably fine, but marginal. Runtime depends on how often it cycles. Continuous pumping: 1/3 HP 2.1–3.7 h (base 2.7); 1/2 HP 1.6–2.3 h (base 1.9). As cycles, assuming 20 s per cycle (base):

  | Cycles per hour | 1/3 HP (650 W) | 1/2 HP (925 W) |
  |---|---|---|
  | 6/h (light) | ~54 h | ~42 h |
  | 20/h (steady rain) | ~21 h | ~16 h |
  | 60/h (storm) | ~8 h | ~5.6 h |

  Formula: average W = cycles × 20 s × running W ÷ 3,600; hours = U ÷ (average W + S). The 20-second cycle length is our assumption; time one cycle of your own pump.
- **Furnace blower (gas furnace)**, 300–800 W running, 800–1,600 W starting (A27): 17.7 h at 300 W × 30% duty; **6.3 h at 550 W × 50%** (base); 3.2 h at 800 W × 70%. The core bundle plus a blower at 550 W × 50% runs **about 5 h**. Most furnaces are hard-wired, so feeding one needs a transfer switch or inlet installed by an electrician. The inducer fan and igniter add draw we did not model.

## 7. Expansion: fridge + CPAP outage bundle

Bundle: full-size ENERGY STAR fridge (0.81 / 1.25 / 1.88 kWh/day) + AirSense 11 for 8 h, inverter on 24 h. Formula: days = U × (total Wh ÷ 2,048) ÷ (fridge Wh + CPAP W × 8 + 24 × S). We apply the same 95% DoD and η to the expansion batteries; BLUETTI's staff apply the same formula to AC200L + B300K (A9).

| Configuration (BLUETTI-confirmed) | Total Wh | Fridge + AirSense 11 **device only**, days (low / base / high) | Fridge + AirSense 11 **with heated humidifier + tube**, days (low / base / high) |
|---|---|---|---|
| AC200L alone | 2,048 | 0.7 / **1.1** / 1.6 | 0.6 / **1.0** / 1.4 |
| + 1× B300K | 4,812.8 | 1.7 / **2.6** / 3.9 | 1.5 / **2.2** / 3.2 |
| + 2× B300K (max per BLUETTI FAQ) | 7,577.6 | 2.7 / **4.2** / 6.1 | 2.3 / **3.5** / 5.1 |
| + 1× B500K ("AC200L + B500K" bundle) | 7,168 | 2.5 / **3.9** / 5.7 | 2.2 / **3.3** / 4.8 |
| + 2× B500K (max per BLUETTI FAQ) | 12,288 | 4.3 / **6.8** / 9.8 | 3.7 / **5.7** / 8.3 |

Worked example (1× B500K, heated humidifier, base): 1,809 × (7,168 ÷ 2,048) ÷ (1,252 + 360 + 288) = 6,332 ÷ 1,900 = 3.3 days.

Compatibility per BLUETTI's US support FAQs: "The AC200L supports up to 2 B300K for up to 7,577.6Wh capacity using the P090D cable" (https://support.bluettipower.com/en-us/products/b300k). For the B500K: "Up to 2 B500K batteries via the P090A cable, for 12,288 Wh capacity. You can only mix with B300, B300K, and B500K" (https://support.bluettipower.com/en-us/products/b500k). Both acc. 2026-10-28. The B300K FAQ's mixing note is narrower (B300 and B300K only); see the spec-check note.

## 8. Recharging

**Energy to refill 0→100%:** 2,048 Wh ÷ 0.95 charge efficiency (A31) ≈ 2,156 Wh into the solar input. From the wall, Trusted Reviews measured 2.34–2.40 kWh per full charge (A32).

**Wall (US 120 V):**

| Mode | Hours 0→100% |
|---|---|
| Turbo 2,400 W | Measured 75–87 min on UK 230 V units (A32). **In the US, the default 15 A input limit caps it near 1,800 W** (manual §9.9) → ESTIMATE ≈ 2,048 ÷ 0.87 ÷ 1,800 ≈ **1.3 h** plus taper, about 1.4–1.6 h. Full 2,400 W needs a 20 A circuit and a BLUETTI-supplied password |
| Standard 1,200 W | Measured 2 h 06 min (A32); ESTIMATE 2,048 ÷ 0.87 ÷ 1,200 = 1.96 h |
| Silent 800 W | Measured just under to just over 3 h (A32); ESTIMATE 2.9 h |

**Car (12 V outlet):** 96 W max (US manual) → 2,156 ÷ 96 ≈ **22.5 h** of driving (ESTIMATE). That is a top-up source, not a refill source.

**Solar, ESTIMATE.** Two views: hours at a good midday output, and days using PVWatts daily yield for real locations.

| Array (nameplate) | Midday output (70–85% of nameplate, our assumption) | Hours of good sun, 0→100% | kWh/day at 3.2–5.1 kWh per kW (Seattle avg to Phoenix avg, A30) | Days to full, average location (4.0 kWh/kW/day) | Days to full, Seattle in December (1.28) |
|---|---|---|---|---|---|
| 400 W | 280–340 W | 6.3–7.7 h | 1.28–2.05 | **1.35 days** | 4.2 days |
| 800 W | 560–680 W | 3.2–3.8 h | 2.56–4.10 | **0.67 days** (one decent day) | 2.1 days |
| 1,200 W (input max) | 840–1,020 W | 2.1–2.6 h (BLUETTI: "about 2.4 hours" if panels **hold** 1,200 W) | 3.84–6.16 | **0.45 days** | 1.4 days |

Formula: days = 2,156 Wh ÷ (array kW × PVWatts DC kWh per kW per day). PVWatts already includes 14% system losses and temperature effects, for a fixed array tilted 30° to the south. Portable panels laid flat or re-aimed by hand will differ. Wire the panels so the string's open-circuit voltage stays at or under 145 V, with the cold-weather rise included, and the current at or under 15 A.

**Break-even solar for a fridge + CPAP day (ESTIMATE).** This is the battery draw per day with the inverter on 24 h, divided by solar yield per watt:

battery Wh/day = (fridge Wh + CPAP W × 8 + 24 × S) ÷ η; panel W = battery Wh/day ÷ 0.95 ÷ (kWh per kW per day)

| Case | Battery Wh/day | Panel W at 5.13 (Phoenix avg) | at 4.0 (typical) | at 3.21 (Seattle avg) | at 1.28 (Seattle Dec) |
|---|---|---|---|---|---|
| Efficient: p10 fridge + AirSense 11 device only | 1,245 | 255 W | 330 W | 410 W | 1,020 W |
| **Base: median fridge + AirSense 11 heated humidifier + tube** | **2,043** | 420 W | **540 W** | 670 W | 1,680 W (over the 1,200 W input cap) |
| Heavy: p90 fridge + 56 W CPAP | 2,810 | 580 W | 740 W | 920 W | 2,310 W (not achievable) |

So **about 400–700 W of panels** covers a typical fridge + CPAP day in most of the US for most of the year. In a northern winter, no array this unit accepts breaks even. Pass-through (UPS/PV-priority) use would shave the inverter-to-battery round trip in daytime; we did not model it.

---

## Summary table (all ESTIMATES; base value with low–high range)

| Use case | AC200L alone (2,048 Wh) | With 1× B500K (7,168 Wh) |
|---|---|---|
| Usable AC energy | 1,809 Wh (1,712–1,900) | ~6,330 Wh (5,990–6,650) |
| Idle drain, inverter on, nothing plugged in | 6.3 days (4.0–6.6) | ~22 days |
| Full-size ENERGY STAR fridge | 28 h (18–41) | ~4.1 days (2.6–6.0) |
| Mini fridge | 48 h (31–55) | ~7 days |
| Chest freezer | 50 h (30–60) | ~7.3 days |
| AirSense 11, device only, AC / DC | 11.0 / 13.5 nights | ~38 / ~47 nights |
| AirSense 11 + heated humidifier + tube, AC / DC | 4.0 / 4.2 nights (2.9–5.5) | ~14 nights |
| 1,500 W space heater | 72 min (68–75) | ~4.2 h |
| 750 W space heater | 2.4 h (2.2–2.5) | ~8.3 h |
| 50–100 W electric blanket | 16–29 h | 2–4 days |
| 13.5K RV AC, compressor running continuously | 1.1 h (0.9–1.3); start needs a soft starter | 3.7 h (3.1–4.5) |
| 15K RV AC, compressor running continuously | 1.1 h (0.85–1.2) | 3.8 h (3.0–4.2) |
| RV overnight, fridge on propane | 1.8 days (1.2–2.8) | ~6 days |
| Outage: fridge + router + lights + phones | 20.5 h (12.8–30.4) | 3.0 days (1.9–4.4) |
| Same + Starlink Standard | ~10 h | ~1.5 days |
| Starlink Mini on USB-C | 44 h (36–56) | n/a (DC) |
| Fridge + AirSense 11 (heated humidifier + tube) | 1.0 day (0.6–1.4) | 3.3 days (2.2–4.8) |
| Refill: wall, US default 15 A / Standard / Silent | ~1.4–1.6 h / ~2.1 h / ~3 h | ~3.5× longer |
| Refill: 400 / 800 / 1,200 W solar, average US site | 1.35 / 0.67 / 0.45 days | ~3.5× longer |
| Refill: car 12 V | ~22.5 h | not practical |
| Solar to break even on fridge + CPAP | ~540 W (330–740 W; up to 1,680 W in a Seattle December) | same daily need |

The B500K column scales the base case by 7,168 ÷ 2,048 = 3.5×, except where the cell gives its own range.

## Open questions / couldn't verify

1. **The web-search budget for this session ran out partway through.** Searches still owed: a measured AC200L US (120 V) capacity/efficiency test, HOBOTECH's AC200L numbers (referenced on the BLUETTI forum as covering standby draw), Coleman-Mach 15K LRA, and RV 12 V load specs (Suburban/Atwood furnace blower amps, Shurflo pump amps).
2. **No US 120 V measured capacity test found.** Both measured tests (Trusted Reviews, The Ambient) used UK 230 V units. The US unit may be a few percent less efficient. Our low case (η 0.88) covers this by assumption, not by measurement.
3. **Idle draw is 12 W or 18 W.** The manual says ~12 W; BLUETTI staff twice say 18 W with AC on. One owner measured ~120 W of overhead at low load (forum thread 33228, 2024-09). BLUETTI staff treated that as abnormal; we did not use it.
4. **AC-ECO threshold and timer are not published.** We could not confirm whether a CPAP or a cycling fridge will trip it. The manual's own advice (disable ECO under 60 W) is the safe instruction.
5. **Peak inverter current for motor starts is not published.** The ">3,600W @ 0.5s" tier doesn't say how far above 3,600 W the inverter can go. Whether a 13.5K/15K RV AC starts without a soft starter is owner-anecdote only, and the anecdotes are mixed.
6. **AirSense 11 draw by configuration:** ResMed publishes only "typical 56.1 W" / "peak 73.2 W" for the 11. The 7 / 22 / 34 W split is the AirSense 10. A Dometic support page reportedly lists the Penguin II 13.5K at "1,731 W" cooling power consumption; it returned 404 when fetched, so we used the installation-manual amps instead.
7. **DreamStation 2 has no published watt draw.** Our 10–30 W / 40–80 W ranges are assumptions bounded by the 80 W supply.
8. **Electric blanket wattage (50–100 W)** was not verified against a manufacturer. DOE's Energy Saver appliance-wattage page (https://www.energy.gov/energysaver/estimating-appliance-and-home-electronic-energy-use) returned 404 on 2026-10-28, and the federal eCFR (DOE test procedure) redirected to a bot check.
9. **Expansion-battery idle draw** (B300K/B500K) is not published. We assumed the same DoD and η as the main unit. The one owner data point (AC200L + B300K) ran about 11% under the formula.
10. **B300K/B500K mixing** is stated differently on BLUETTI's two FAQs. The manual (V3.0) predates both batteries.
11. **Solar charge efficiency (MPPT)** and **DC-port conversion efficiency** are not published. We assumed 0.95 and 0.88–0.95 respectively.
12. **Forum sources:** the BLUETTI community forum (community.bluettipower.com) now redirects to forum.bluettipower.com's home page. The quoted posts were read from web.archive.org snapshots (dates in A6, A9, A25). Re-link them if the threads reappear on the new forum.
