# Content-gap pages (growth/gap-experiment.md, growth/gap-targets.md). Each answers a shopper question whose search
# results, as the assistants see them, hold few pages with real data: rules pages with no product choice, or AI-written
# listicles on unrelated domains. Same record shape and renderer as compare.py (build.compare_page), so the loop-3 changes
# to compare_page apply here too; the gap experiment measures frozen snapshots of the rendered HTML.
#
# Record: slug (published as /<slug>), question (gap cluster id and the agent queries it answers), title, h1, desc,
# intro (HTML; {buy:slug}, {price:slug}, {deal:slug} filled by build.py), columns, rows, after, sources, published,
# checked. Other brands' figures were read from the makers' own US pages on `checked` and are not re-checked daily.

GAP_PAGES = [

# ---------------- G01: power banks for flying (target questions Q01, Q02) ----------------
# Agent queries seen: "best power bank for airplane travel 2026 airline lithium battery carry-on rules TSA FAA" (ChatGPT,
# whose own result set held only FAA, IATA and airline rules pages); "best power bank for flying carry-on airline approved
# 2026", "TSA power bank rules carry-on 100Wh limit airline power bank use ban 2026", "airlines banning power bank use in
# flight 2026 rules", "best 20000mAh power bank airline-friendly 2026" (Claude). The page answers the rule and the pick.
{"slug": "best-power-banks-for-flying", "question": "G01 (Q01, Q02)",
 "title": "Best power banks for flying (2026): airline rules and picks under 100 Wh",
 "h1": "Best power banks for flying (2026): the airline rules, and picks under 100 Wh",
 "desc": "Which power bank you can take on a plane in 2026 and which to buy: FAA and ICAO limits (100 Wh, two per person, no recharging on board), each airline's in-flight use rules, and eleven power banks under 100 Wh compared (Baseus, Anker, UGREEN, INIU, Nitecore, EcoFlow).",
 "intro": """
<p class="lead">Any power bank <strong>under 100 Wh</strong> (about 27,000 mAh) can fly in your <strong>carry-on</strong> in the US; none may go in checked bags. What changed in 2026 is using it: since 27 March 2026 the ICAO rules say <strong>no more than two power banks per person</strong> and <strong>no recharging them on board</strong>, and many airlines now ban using one in flight at all. The FAA has not adopted the ICAO change; US airlines set their own rules (table below).</p>
<p><strong>Short answer.</strong> To charge a laptop and a phone from one carry-on bank: the <strong>Baseus EnerFill FC41</strong>, 25,000 mAh (91.25 Wh) with two built-in USB-C cables and 140 W from one port ({buy:baseus-enerfill-fc41-25000mah-145w}).
A flat laptop bank with a display: <strong>Baseus Blade H1</strong>, 20,000 mAh (74 Wh, 100 W) ({buy:baseus-blade-h1-100w-20000mah}).
Phone only, the lightest option: <strong>Baseus PicoGo AM52</strong>, a 10,000 mAh (≈37 Wh) Qi2.2 magnetic bank ({buy:baseus-picogo-am52-qi2-2-10000mah-45w}).
Elsewhere: Anker's Prime 26K (99.75 Wh, $229.99) is the most power you can carry without airline approval; INIU's Cougar 20,000 mAh (73 Wh, $46.99) is the cheapest laptop-capable bank we found on a maker's US store.</p>
<p><strong>The rules in one paragraph.</strong> FAA: spare lithium batteries, power banks included, go in carry-on only; under 100 Wh there is no FAA limit for personal use; 101–160 Wh needs the airline's approval, two at most; over 160 Wh is forbidden. Watt-hours = mAh × 3.7 ÷ 1,000 (American Airlines' formula): 10,000 mAh ≈ 37 Wh, 20,000 mAh ≈ 74 Wh, 25,000 mAh ≈ 92.5 Wh, 27,000 mAh ≈ 99.9 Wh. Airlines may be stricter than the FAA, and from 2027 IATA's rulebook drops the 100–160 Wh allowance for power banks. Recalled banks may not fly at all; Anker recalled models A1647, A1652, A1681, A1689, A1257 and the PowerCore 10000 in June 2025.</p>
""",
 "columns": [("cap", "Capacity"), ("out", "Max output"), ("ports", "Ports / cables"), ("laptop", "Charges a laptop (60 W+)?"), ("weight", "Weight"), ("fly", "Flight notes")],
 "rows": [
  {"slug": "baseus-enerfill-fc41-25000mah-145w", "model": "Baseus EnerFill FC41 25,000 mAh 145 W",
   "cells": {"cap": "25,000 mAh / 91.25 Wh", "out": "145 W total; 140 W from USB-C1", "ports": "2 built-in USB-C cables; 4 devices at once", "laptop": "Yes (140 W)", "weight": "Not published", "fly": "Under 100 Wh"}},
  {"slug": "baseus-blade-h1-100w-20000mah", "model": "Baseus Blade H1 20,000 mAh 100 W",
   "cells": {"cap": "20,000 mAh / ≈74 Wh", "out": "100 W USB-C PD", "ports": "2× USB-C, 2× USB-A; 100 W cable included", "laptop": "Yes (100 W)", "weight": "≈451 g", "fly": "Under 100 Wh; flat 18 mm"}},
  {"slug": "baseus-picogo-am52-qi2-2-10000mah-45w", "model": "Baseus PicoGo AM52 Qi2.2 10,000 mAh",
   "cells": {"cap": "10,000 mAh / ≈37 Wh", "out": "45 W USB-C; 25 W Qi2.2 magnetic", "ports": "1× USB-C + magnetic pad", "laptop": "No (45 W)", "weight": "—", "fly": "Under 100 Wh"}},
  {"brand": "Anker", "model": "Prime Power Bank 26K 300 W (A110A)", "url": "https://www.anker.com/products/a110a-anker-prime-26k-300w-power-bank",
   "cells": {"cap": "26,250 mAh / 99.75 Wh", "out": "300 W total; 140 W per USB-C", "ports": "2× USB-C, 1× USB-A", "laptop": "Yes", "weight": "600 g", "fly": "0.25 Wh under the limit", "price": "$229.99"}},
  {"brand": "Anker", "model": "Prime Power Bank 20K 220 W (A110B)", "url": "https://www.anker.com/products/a110b-anker-prime-20k-220w-power-bank",
   "cells": {"cap": "20,100 mAh / 72.36 Wh", "out": "220 W total; 140 W per USB-C", "ports": "2× USB-C, 1× USB-A", "laptop": "Yes", "weight": "510 g", "fly": "Under 100 Wh", "price": "$179.99"}},
  {"brand": "Anker", "model": "Nano Power Bank 10K, built-in cable (A1259)", "url": "https://www.anker.com/products/a1259-built-in-cable-power-bank-10000mah",
   "cells": {"cap": "10,000 mAh / ≈37 Wh", "out": "30 W", "ports": "Built-in USB-C cable + USB-C + USB-A", "laptop": "No", "weight": "215 g", "fly": "Under 100 Wh", "price": "$49.99"}},
  {"brand": "UGREEN", "model": "Nexode 25,000 mAh 200 W (35525)", "url": "https://us.ugreen.com/products/ugreen-nexode-power-bank-25000mah-200w-with-smart-digital-display",
   "cells": {"cap": "25,000 mAh / 90 Wh", "out": "200 W; USB-C1 140 W", "ports": "2× USB-C, 1× USB-A", "laptop": "Yes", "weight": "609 g", "fly": "Under 100 Wh", "price": "$129.99 ($89.95 with UGREEN's page code UL35525)"}},
  {"brand": "UGREEN", "model": "Nexode 20,000 mAh 130 W (35524)", "url": "https://us.ugreen.com/products/ugreen-nexode-power-bank-20000mah-130w",
   "cells": {"cap": "20,000 mAh / 72 Wh", "out": "130 W; USB-C1 100 W", "ports": "2× USB-C, 1× USB-A", "laptop": "Yes", "weight": "476 g", "fly": "Under 100 Wh", "price": "$89.99 ($59.99 with UGREEN's page code UL35524)"}},
  {"brand": "INIU", "model": "Cougar 20,000 mAh 65 W (P62-E1)", "url": "https://iniushop.com/products/iniu-p62-e1-power-bank-smallest-20000mah-65w",
   "cells": {"cap": "20,000 mAh / 73 Wh", "out": "65 W from one USB-C", "ports": "2× USB-C, 1× USB-A", "laptop": "Yes (65 W)", "weight": "≈324 g", "fly": "Under 100 Wh", "price": "$46.99"}},
  {"brand": "Nitecore", "model": "NB20000 Gen3", "url": "https://www.nitecore.com/product/nb20000Gen3",
   "cells": {"cap": "20,000 mAh at 3.6 V / 72 Wh", "out": "22.5 W per USB-C", "ports": "2× USB-C; IPX5", "laptop": "No", "weight": "291 g", "fly": "Under 100 Wh", "price": "$99.95 at nitecorestore.com (Nitecore's site does not sell it)"}},
  {"brand": "EcoFlow", "model": "RAPID Pro 27,650 mAh 300 W", "url": "https://us.ecoflow.com/products/ecoflow-rapid-pro-power-bank-27650mah-300w-140w-built-in-cable",
   "cells": {"cap": "27,650 mAh / 99.54 Wh", "out": "300 W; 140 W cable + 140 W USB-C", "ports": "Built-in cable + 3× USB-C", "laptop": "Yes", "weight": "699 g", "fly": "0.46 Wh under the limit; American's page names EcoFlow among banned large power sources, so expect questions", "price": "$175.99"}},
 ],
 "after": """
<h2>In-flight rules by airline (checked October 2026)</h2>
<div class="scroll"><table>
<tr><th>Airline</th><th>Rule</th><th>Overhead bin</th><th>Since</th></tr>
<tr><td>Southwest</td><td>One power bank per customer, 100 Wh max; must be visible when in use; may not charge it from seat power</td><td>Not allowed</td><td>One-per-customer from 20 Apr 2026</td></tr>
<tr><td>American</td><td>Two per passenger, 100 Wh each; keep it within reach and visible while in use; no recharging it from seat outlets</td><td>Not allowed</td><td>—</td></tr>
<tr><td>Delta</td><td>Two per passenger, 100 Wh each, "no exceptions"; under the seat or in the seatback pocket; no recharging on board</td><td>Not allowed</td><td>—</td></tr>
<tr><td>United</td><td>Carry-on only; up to two batteries up to 160 Wh each; no in-flight use rule on its page</td><td>—</td><td>—</td></tr>
<tr><td>JetBlue</td><td>Two per customer; not charged from seat power; should not power other devices in flight</td><td>Not allowed</td><td>—</td></tr>
<tr><td>Emirates</td><td>One power bank under 100 Wh, rating printed on it; no use on board</td><td>Not allowed</td><td>1 Oct 2025</td></tr>
<tr><td>Lufthansa Group</td><td>Two at most; not used or charged on board; 100–160 Wh needs approval</td><td>Not allowed</td><td>15 Jan 2026</td></tr>
<tr><td>Korean Air, Asiana, Jin Air, Air Busan, Air Seoul</td><td>No use on board at all</td><td>Not allowed</td><td>26 Jan 2026</td></tr>
<tr><td>Qantas, Jetstar</td><td>No use or charging on board; two at most, 160 Wh each</td><td>Only if seat pocket or under-seat is impossible</td><td>15 Dec 2025</td></tr>
<tr><td>Cathay Pacific</td><td>Two at most; no use or recharging on board</td><td>Not allowed</td><td>Updated 30 Mar 2026</td></tr>
<tr><td>Singapore Airlines</td><td>Two at most; no charging from seat power or USB</td><td>Should not</td><td>15 Apr 2026</td></tr>
<tr><td>KLM</td><td>Two at most, capacity printed; no use or charging on board</td><td>Not allowed</td><td>—</td></tr>
<tr><td>All flights in Japan (MLIT)</td><td>Two at most, 160 Wh; no charging from aircraft power; do not use to charge devices</td><td>Do not</td><td>24 Apr 2026</td></tr>
</table></div>
<p>What it means for the choice: on most international carriers the bank charges your devices at the gate and the hotel, not in your seat, so capacity per gram matters more than in-flight convenience. On US carriers that allow use, keep it visible and out of the overhead bin. If you fly abroad with two banks, both must be under 100 Wh on most airlines, and three is too many almost everywhere.</p>
""",
 "sources": [
  ("FAA PackSafe: lithium batteries (updated 11 Aug 2026)", "https://www.faa.gov/hazmat/packsafe/lithium-batteries"),
  ("FAA: airline passengers and batteries (updated 2 Oct 2026)", "https://www.faa.gov/hazmat/packsafe/airline-passengers-and-batteries"),
  ("TSA: power banks, carry-on yes, checked no", "https://www.tsa.gov/travel/security-screening/whatcanibring/items/power-banks"),
  ("IATA guidance on ICAO power bank changes (31 Mar 2026)", "https://www.iata.org/contentassets/90f8038b0eea42069554b2f4530f49ea/guidance-to-operators---power-banks.pdf"),
  ("American Airlines restricted items (Wh formula, portable chargers)", "https://www.aa.com/web/i18n/travel-info/baggage/restricted-items.html"),
  ("Southwest: lithium batteries", "https://support.southwest.com/helpcenter/article/Traveling-with-lithium-batteries-e-cigarettes-and-lighters"),
  ("Delta: battery-powered items", "https://www.delta.com/us/en/baggage/prohibited-or-restricted-items/battery-or-fuel-powered"),
  ("United: dangerous items", "https://www.united.com/en/us/fly/baggage/dangerous-items.html"),
  ("JetBlue: batteries", "https://www.jetblue.com/help/batteries"),
  ("Emirates power bank rule", "https://www.emirates.com/media-centre/emirates-makes-changes-to-safety-rules-for-customer-usage-of-power-banks-onboard/"),
  ("Lufthansa Group power bank rule", "https://business.lufthansagroup.com/eg/en/program/experts/news/power-banks-on-board--updated-regulations-from-january-2026"),
  ("Qantas and Jetstar power bank rule", "https://www.qantasnewsroom.com.au/media-releases/qantas-and-jetstar-to-introduce-new-safety-measures-for-power-banks-on-all-flights"),
  ("Cathay Pacific power bank restrictions", "https://www.cathaypacific.com/cx/en_HK/latest-news/security-and-operational-changes/restrictions-on-the-carriage-of-lithium-battery-power-banks.html"),
  ("Singapore Airlines power bank advisory", "https://www.singaporeair.com/en_UK/sg/corporate/newsroom/newsalert-listing/advisory-on-the-carriage-of-power-banks-on-board-sia-flights-/"),
  ("KLM restricted hand-baggage items", "https://www.klm.com/information/baggage/restricted-items-hand-baggage"),
  ("Japan MLIT power bank rules (English)", "https://www.mlit.go.jp/koku/content/001998101.pdf"),
  ("Anker product recalls", "https://www.anker.com/product-recalls"),
  ("Baseus EnerFill FC41 25,000 mAh", "https://www.baseus.com/products/enerfill-fc41-power-bank-with-cables-25000mah-145w"),
 ],
 "published": "2026-10-25", "checked": "2026-10-24"},

# ---------------- G02: solar generator with panels included ----------------
# Bing US demand 402 searches / 3 months (runs/2026-10-25-codedscan); live Bing top 10: six store pages and two thin
# guides, no publisher (runs/2026-10-25-agentq). Kit prices read on each maker's US store 2026-10-24 US time.
{"slug": "solar-generator-with-panels-included", "question": "G02",
 "title": "Best solar generator with panels included (2026): 15 kits compared on battery, inverter, solar input and price",
 "h1": "Best solar generator with panels included (2026): 15 kits compared",
 "desc": "Power station and folding solar panel kits sold on the makers' US stores (ALLPOWERS, BLUETTI, Jackery, EcoFlow, Anker SOLIX, Goal Zero), compared on battery size and chemistry, inverter, panel watts, the station's solar input, and price, with the codes that worked in the stores' carts.",
 "intro": """
<p class="lead">A "solar generator with panels included" is a portable power station sold together with one or more folding panels. Judge it on four numbers: the <strong>battery</strong> (Wh, and LiFePO4 if you want thousands of cycles), the <strong>inverter</strong> (W it can run), the <strong>panel watts</strong> in the box, and the station's <strong>maximum solar input</strong>, which caps how much more panel you can add later. A folding panel delivers roughly 60–75% of its rating in good sun, so a 200 W panel puts back about 600–750 Wh on a clear day with five peak-sun hours.</p>
<p><strong>Short answer.</strong> Best value at 1 kWh: the <strong>ALLPOWERS P1800 + SP037 400 W</strong> kit, a 1,024 Wh LiFePO4 station with twice the panel most 1 kWh kits include ({buy:allpowers-p1800-sp037-solar-kit}).
The 1 kWh alternatives with a 200–220 W panel: <strong>BLUETTI AC180 + 200 W</strong> ({buy:bluetti-ac180-200w-solar-kit}), Jackery Solar Generator 1000 v2 ($699), EcoFlow DELTA 3 Classic + 220 W ($699) and Anker SOLIX C1000 Gen 2 + 200 W ($739.99).
For 2 kWh of home backup: <strong>BLUETTI Elite 200 V2 + 200 W</strong> ({buy:bluetti-elite-200-v2-200w-solar-kit}), which takes up to 1,000 W of panel later; Jackery's 2000 v2 comes with two 200 W panels ($1,399) and Anker's C2000 Gen 2 with a 400 W panel ($1,399.99).
Most inverter per dollar: <strong>ALLPOWERS S2000 Pro + SP037</strong>, 2,400 W, on an NMC battery ({buy:allpowers-s2000-pro-sp037-solar-kit}).
Smallest budgets: <strong>ALLPOWERS VOLIX P300 + 100 W</strong> ({buy:allpowers-volix-p300-100w-solar-kit}) or <strong>BLUETTI Elite 30 V2 + 100 W</strong> ({buy:bluetti-elite-30-v2-100w-solar-kit}).</p>
<p><strong>One kit to skip:</strong> ALLPOWERS' R4000 + SP037 kit costs $2,198, about $400 more than the R4000 ($1,499) and an SP037 ($299) bought separately. And a kit is not always cheaper than its parts: ALLPOWERS' P1800 kit saves $7 over the two items, its S2000 Pro kit saves nothing.</p>
""",
 "columns": [("battery", "Battery"), ("chem", "Chemistry"), ("ac", "AC output"), ("panel", "Panels in the box"), ("solar", "Station's max solar input"), ("recharge", "Maker's solar recharge figure")],
 "rows": [
  {"slug": "allpowers-p1800-sp037-solar-kit", "model": "ALLPOWERS P1800 + SP037 400 W",
   "cells": {"battery": "1,024 Wh", "chem": "LiFePO4", "ac": "1,800 W (3,600 W peak)", "panel": "1 × 400 W (SP037)", "solar": "650 W, 11–60 V", "recharge": "Not published"}},
  {"slug": "bluetti-ac180-200w-solar-kit", "model": "BLUETTI AC180 + 200 W",
   "cells": {"battery": "1,152 Wh", "chem": "LiFePO4", "ac": "1,800 W (2,700 W Power Lifting)", "panel": "1 × 200 W", "solar": "500 W, 12–60 V", "recharge": "Not published (3 h at 500 W)"}},
  {"slug": "bluetti-elite-200-v2-200w-solar-kit", "model": "BLUETTI Elite 200 V2 + 200 W",
   "cells": {"battery": "2,073.6 Wh", "chem": "LiFePO4", "ac": "2,600 W (3,900 W Power Lifting)", "panel": "1 × 200 W (ships from Oct 29)", "solar": "1,000 W, 12–60 V", "recharge": "Not published"}},
  {"slug": "allpowers-s2000-pro-sp037-solar-kit", "model": "ALLPOWERS S2000 Pro + SP037 400 W",
   "cells": {"battery": "1,451 Wh", "chem": "NMC (ternary lithium)", "ac": "2,400 W (4,000 W surge)", "panel": "1 × 400 W (SP037)", "solar": "Page says 1,000 W and 650 W", "recharge": "Not published"}},
  {"slug": "bluetti-elite-30-v2-100w-solar-kit", "model": "BLUETTI Elite 30 V2 + 100 W",
   "cells": {"battery": "288 Wh", "chem": "LiFePO4", "ac": "600 W (1,500 W Power Lifting)", "panel": "1 × 100 W", "solar": "200 W, 12–28 V", "recharge": "5.5 h with the 60 W kit; 100 W not published"}},
  {"slug": "allpowers-volix-p300-100w-solar-kit", "model": "ALLPOWERS VOLIX P300 + 100 W",
   "cells": {"battery": "256 Wh", "chem": "LiFePO4", "ac": "300 W (600 W surge)", "panel": "1 × 100 W (SE100)", "solar": "110 W, 11–30 V", "recharge": "Not published"}},
  {"brand": "Jackery", "model": "Solar Generator 1000 v2 (Explorer 1000 v2 + SolarSaga 200 W)", "url": "https://www.jackery.com/products/jackery-solar-generator-1000-v2",
   "cells": {"battery": "1,070 Wh", "chem": "LiFePO4", "ac": "1,500 W (3,000 W surge)", "panel": "1 × 200 W", "solar": "400 W, 12–60 V", "recharge": "\"7.5 hours\" (setup not stated)", "price": "$699 (list $879)"}},
  {"brand": "Jackery", "model": "Solar Generator 2000 v2 (Explorer 2000 v2 + 2 × SolarSaga 200 W)", "url": "https://www.jackery.com/products/jackery-solar-generator-2000-v2",
   "cells": {"battery": "2,042 Wh", "chem": "LiFePO4", "ac": "2,200 W (4,400 W surge)", "panel": "2 × 200 W", "solar": "400 W, 11–60 V", "recharge": "\"7.5 hours\" (setup not stated)", "price": "$1,399 (list $1,649)"}},
  {"brand": "EcoFlow", "model": "DELTA 3 Classic Solar Generator (PV220W)", "url": "https://us.ecoflow.com/products/delta-3-classic-solar-generator-pv220w",
   "cells": {"battery": "1,024 Wh", "chem": "LiFePO4", "ac": "1,800 W (3,600 W surge)", "panel": "1 × 220 W bifacial", "solar": "500 W", "recharge": "Not published (2.5 h at 500 W)", "price": "$699"}},
  {"brand": "EcoFlow", "model": "DELTA 3 Solar Generator, 220 W", "url": "https://us.ecoflow.com/products/ecoflow-delta-3-solar-generator",
   "cells": {"battery": "1,024 Wh", "chem": "LFP", "ac": "1,800 W (3,600 W surge)", "panel": "1 × 220 W", "solar": "500 W, 11–60 V", "recharge": "Within 6 h", "price": "$869"}},
  {"brand": "EcoFlow", "model": "DELTA 3 Plus Solar Generator (PV220W)", "url": "https://us.ecoflow.com/products/delta-3-series-solar-generator-pv220w",
   "cells": {"battery": "1,024 Wh", "chem": "LFP", "ac": "1,800 W (3,600 W surge)", "panel": "1 × 220 W bifacial", "solar": "2 × 500 W, 11–60 V", "recharge": "Within 6 h", "price": "$919 (pre-order, ships in November)"}},
  {"brand": "Anker SOLIX", "model": "C1000 Gen 2 + 200 W solar panel", "url": "https://www.ankersolix.com/products/c1000-gen2?variant=61869573308746",
   "cells": {"battery": "1,024 Wh", "chem": "Not named (4,000 cycles to 80%)", "ac": "2,000 W (3,000 W peak)", "panel": "1 × 200 W", "solar": "600 W, 60 V max", "recharge": "Not published (1.8 h at 600 W)", "price": "$739.99 as an option on the station page"}},
  {"brand": "Anker SOLIX", "model": "C2000 Gen 2 + 400 W solar panel", "url": "https://www.ankersolix.com/products/c2000-gen2-400w-solar-panel",
   "cells": {"battery": "2,048 Wh", "chem": "LFP", "ac": "2,400 W (4,000 W peak)", "panel": "1 × 400 W (PS400)", "solar": "800 W, 11–60 V", "recharge": "Not published (3 h at 800 W)", "price": "$1,399.99 (list $1,999.99)"}},
  {"brand": "Goal Zero", "model": "Yeti 500 + Boulder 100 Briefcase", "url": "https://www.goalzero.com/products/yeti-500-boulder-100-bc-solar-generator",
   "cells": {"battery": "499.2 Wh", "chem": "LiFePO4", "ac": "500 W (1,000 W surge)", "panel": "1 × 100 W briefcase", "solar": "200 W, 12.3–28 V", "recharge": "Under 6 h", "price": "$809.95 (list $899.95)"}},
  {"brand": "ALLPOWERS", "model": "R4000 + SP037 400 W kit (not recommended)", "url": "https://iallpowers.com/products/allpowers-r4000-solar-generator-4000w-3600wh-portable-power-station-with-solar-panels",
   "note": "Costs about $400 more than the R4000 and an SP037 bought separately; see the R4000's own page for its code and link",
   "cells": {"battery": "3,456 Wh", "chem": "LiFePO4", "ac": "3,600 W (page also says 4,000 W)", "panel": "1 × 400 W (2-panel version $2,497)", "solar": "2,000 W", "recharge": "Not published", "price": "$2,198 (cart takes 7% off over $1,500)"}},
 ],
 "after": """
<h2>How to pick</h2>
<ul>
<li><strong>Size the battery to the load, then the panel to the battery.</strong> A fridge drawing about 1–1.5 kWh a day needs a 2 kWh station to ride through a night, and 400 W or more of panel to refill it in a day; a CPAP, phones and lights fit a 256–500 Wh station and a 100 W panel.</li>
<li><strong>Check the voltage, not only the watts.</strong> Small stations with 12–28 V solar inputs (BLUETTI Elite 30 V2, Goal Zero Yeti 500) cannot take the big 40 V+ folding panels; the kits pair them with low-voltage panels for that reason.</li>
<li><strong>Room to grow.</strong> The station's solar input is the ceiling: the Elite 200 V2 takes 1,000 W, the AC180 500 W, Jackery's 1000 v2 and 2000 v2 400 W.</li>
<li><strong>Codes.</strong> Our rows carry the code that worked in each store's cart; Jackery, EcoFlow, Anker and Goal Zero rows show the store's own price with no code.</li>
</ul>
""",
 "sources": [
  ("ALLPOWERS P1800 + SP037 kit", "https://iallpowers.com/products/allpowers-1800w-solar-generator-p1800-1024wh-with-400w-solar-panel"),
  ("ALLPOWERS S2000 Pro + SP037 kit", "https://iallpowers.com/products/allpowers-solar-generator-kit-2400w-s2000-pro-sp037-400w-solar-panel"),
  ("ALLPOWERS VOLIX P300 + 100 W kit", "https://iallpowers.com/products/volix-p300-100w-solar-panel"),
  ("ALLPOWERS R4000 + SP037 kit", "https://iallpowers.com/products/allpowers-r4000-solar-generator-4000w-3600wh-portable-power-station-with-solar-panels"),
  ("BLUETTI AC180 kits", "https://www.bluettipower.com/products/ac180?variant=45427542491355"),
  ("BLUETTI Elite 200 V2 + 200 W", "https://www.bluettipower.com/products/elite-200-v2-sp200l"),
  ("BLUETTI Elite 30 V2 + 100 W", "https://www.bluettipower.com/products/bluetti-elite-30-v2-portable-power-station-600w-288wh"),
  ("Jackery Solar Generator 1000 v2", "https://www.jackery.com/products/jackery-solar-generator-1000-v2"),
  ("Jackery Solar Generator 2000 v2", "https://www.jackery.com/products/jackery-solar-generator-2000-v2"),
  ("EcoFlow DELTA 3 Classic Solar Generator", "https://us.ecoflow.com/products/delta-3-classic-solar-generator-pv220w"),
  ("EcoFlow DELTA 3 Solar Generator", "https://us.ecoflow.com/products/ecoflow-delta-3-solar-generator"),
  ("EcoFlow DELTA 3 Plus Solar Generator", "https://us.ecoflow.com/products/delta-3-series-solar-generator-pv220w"),
  ("Anker SOLIX C1000 Gen 2", "https://www.ankersolix.com/products/c1000-gen2?variant=61869573308746"),
  ("Anker SOLIX C2000 Gen 2 + 400 W", "https://www.ankersolix.com/products/c2000-gen2-400w-solar-panel"),
  ("Goal Zero Yeti 500 + Boulder 100", "https://www.goalzero.com/products/yeti-500-boulder-100-bc-solar-generator"),
 ],
 "published": "2026-10-25", "checked": "2026-10-24"},

# ---------------- G03: Tesla Model Y back-seat screen ----------------
# Agent query seen: "Tesla Model Y back seat projector screen headrest mount rear seat entertainment" (Claude). Live Bing
# top 10 on 2026-10-25: seven store listings and two brand pages, no editorial page (runs/2026-10-25-agentq).
{"slug": "tesla-model-y-back-seat-screen", "question": "G03",
 "title": "Tesla Model Y back-seat screen (2026): rear displays, roof projector screen and tablet mounts compared by model year",
 "h1": "Tesla Model Y back-seat screen: every option compared by model year (2026)",
 "desc": "Back-seat entertainment for the Tesla Model Y, by model year: add-on rear displays (Teslahubs, TESERY, Tlyard, Hansshow), Hansshow's 18.5-inch flip-down, Aurzen's clip-in roof projector screen, and seat-back tablet mounts, with what fits 2025–2026 (Juniper) cars.",
 "intro": """
<p class="lead">What fits depends on the model year. Most add-on rear displays are made for the <strong>2020 to early-2025 Model Y</strong>; the refreshed <strong>2025–2026 Model Y (Juniper)</strong> has far fewer options, because most trims already come with Tesla's own 8-inch rear touchscreen and the add-on displays below were made for the older console.</p>
<p><strong>Short answer.</strong> On a <strong>2025–2026 Model Y</strong>, for a big picture while parked (camping, charging stops), the
<strong>Aurzen TravelPlay AutoCinema</strong> screen clips into the glass roof for lie-back movies, or stands one panel at the front console for the back seat or in the open liftgate, as a 47-inch screen for a portable projector
({buy:aurzen-travelplay-autocinema-tesla-model-y}); pair it with the Aurzen ZIP ({buy:aurzen-zip-tri-fold-mini-projector}) or the 1080p ZIP Pro ({buy:aurzen-zip-pro-tri-fold-1080p-projector}).
For a screen that works while driving, a Juniper Standard without a rear screen can take Hansshow's H86 ($399.99), and any Juniper except the Standard can take Hansshow's 18.5-inch flip-down ($1,049).
The cheapest fix on any year is a seat-back tablet mount: TESERY's fits the seat gap for $19.99.
On a <strong>2020 to early-2025 Model Y</strong>, the plug-in rear displays are the usual choice: Teslahubs Rear Display Ultra ($269.99, 2019–2024), TESERY 8.66-inch ($359, to 2025.03) or Tlyard H86 ($359, to 2025.02).</p>
<p>A projector screen and a rear display solve different problems: the projector setup is for parked movies (the screen lines the roof or stands in front of the back seat with the front seats slid forward, and Aurzen says not to use it while driving); a rear display or tablet works on the road.</p>
""",
 "columns": [("what", "What it is"), ("size", "Screen"), ("years", "Model Y years"), ("install", "Install"), ("plays", "What it plays"), ("use", "Power / when")],
 "rows": [
  {"slug": "aurzen-travelplay-autocinema-tesla-model-y", "model": "Aurzen TravelPlay AutoCinema Screen",
   "cells": {"what": "Clip-in fabric projector screen + roof sunshade", "size": "≈47\" front + ≈50\" rear panels", "years": "2025–2026 (Juniper); 2020–2024 roof mode only",
             "install": "Tool-free clips into the roof rim", "plays": "Whatever your projector plays (needs a projector; not included)", "use": "No power; parked only"}},
  {"slug": "aurzen-zip-tri-fold-mini-projector", "model": "Aurzen ZIP projector (to pair with the screen)",
   "cells": {"what": "Folding 720p mini projector, 100 ANSI lm", "size": "40–60\" recommended", "years": "Any (portable)",
             "install": "Stand or mount; Bluetooth audio to the car's speakers", "plays": "Phone mirroring without Wi-Fi; no apps", "use": "Battery up to 1.5 h; 24 W USB-C"}},
  {"slug": "aurzen-zip-pro-tri-fold-1080p-projector", "model": "Aurzen ZIP Pro projector (to pair with the screen)",
   "cells": {"what": "Folding 1080p projector, 200 ANSI lm", "size": "60–80\" recommended", "years": "Any (portable)",
             "install": "Stand or mount; Bluetooth audio to the car's speakers", "plays": "AirPlay, Google Cast, Miracast, USB-C video; no apps", "use": "Battery up to 2.5 h; 65 W USB-C; pre-order, ships from 2026-10-30"}},
  {"brand": "Hansshow", "model": "H86 Rear Entertainment Screen for Model Y Juniper Standard",
   "url": "https://www.hansshow.com/products/model-y-juniper-standard-rear-entertainment-screen-h86-android-smart-display-upgrade-for-tesla",
   "cells": {"what": "Add-on rear console display, Android 12", "size": "8.66\" HD", "years": "Model Y Juniper Standard (2025.11+) only",
             "install": "Plug-and-play (Hansshow installs in Santa Ana, CA)", "plays": "Android apps, wireless CarPlay; rear climate and seat controls", "use": "Car power; usable while driving", "price": "$399.99"}},
  {"brand": "Hansshow", "model": "18.5\" Overhead Flip-Down Screen (Model Y / Juniper)",
   "url": "https://www.hansshow.com/products/model-y-y-juniper-18-5-overhead-screen-electric-flip-down-wifi-android-11-roof-mount-tv-rear-entertainment-monitor",
   "cells": {"what": "Motorized roof-mounted monitor, Android 11", "size": "18.5\" 1920×1080 touchscreen", "years": "2020–2025.02 and Juniper 2025.03+; not the Standard trim",
             "install": "Headliner mount with a vehicle harness, no cutting (pro install available)", "plays": "Android apps over Wi-Fi, phone mirroring, HDMI, USB", "use": "Car power; usable while driving", "price": "$1,049"}},
  {"brand": "Teslahubs", "model": "Rear Display Screen ULTRA", "url": "https://teslahubs.com/products/rear-display-ultra",
   "cells": {"what": "Add-on rear console display, Android", "size": "8\" HD", "years": "2019–2024 only",
             "install": "Plug-and-play, no wire cutting", "plays": "Netflix, YouTube, Disney+; Bluetooth headphones; rear climate and seat heat", "use": "Car power; usable while driving", "price": "$269.99 (list $449.99)"}},
  {"brand": "TESERY", "model": "8.66\" Android Rear Entertainment Display", "url": "https://www.tesery.com/products/tesery-8-66-inch-rear-entertainment-display-screen-for-tesla",
   "cells": {"what": "Add-on rear console display, Android 12", "size": "8.66\" HD", "years": "2020–2025.03",
             "install": "DIY, instructions provided", "plays": "Android apps, CarPlay; rear climate, seat heat and massage", "use": "Car power; usable while driving", "price": "$359 (list $409)"}},
  {"brand": "Tlyard", "model": "H86 8.66\" Rear Entertainment Display", "url": "https://www.tlyard.com/products/model-3-y-8-6-inch-rear-entertainment-lcd-display-h86-back-screen",
   "cells": {"what": "Add-on rear console display, Android 13", "size": "8.66\" HD", "years": "2020–2025.02",
             "install": "Plug-and-play (more involved on some 2023 Standard Range cars)", "plays": "Google Play apps, wireless Android Auto; Disney+ no longer supported after an update", "use": "Car power; usable while driving", "price": "$359 Wi-Fi / $409 4G (4G not on US networks)"}},
  {"brand": "TESERY", "model": "Seat-back iPad / phone mount", "url": "https://www.tesery.com/products/tablet-holder-headrest-holder-for-tesla-model-3-model-y",
   "cells": {"what": "Tablet holder that slides into the seat-back gap", "size": "Your tablet (not the 12.9\" iPad Pro)", "years": "2020–2024 and Juniper; not Juniper Performance or Standard",
             "install": "Tool-free, seconds", "plays": "Whatever the tablet plays", "use": "Tablet battery; usable while driving", "price": "$19.99"}},
 ],
 "after": """
<h2>Which one, by situation</h2>
<ul>
<li><strong>Kids watching on the road, 2020–2024 car:</strong> a plug-in rear display. Teslahubs is cheapest ($269.99); TESERY and Tlyard add CarPlay or Android Auto. Check the year range before buying; none of these three fits the 2025 refresh.</li>
<li><strong>2025–2026 Juniper with Tesla's rear screen:</strong> you already have a rear screen; for a bigger or second screen on the road, a $19.99 seat-back tablet mount is the simple add-on (check your trim against TESERY's list).</li>
<li><strong>Juniper Standard (no rear screen):</strong> Hansshow's H86 for the Standard ($399.99), or the tablet mount.</li>
<li><strong>Movie nights while parked or camping in the car:</strong> the Aurzen TravelPlay screen ({buy:aurzen-travelplay-autocinema-tesla-model-y}) with a portable projector; sound goes to the car's speakers over Bluetooth from either Aurzen projector. It needs no wiring and doubles as a roof sunshade.</li>
</ul>
<p class="small">Aurzen's MagPlay suction mount, which Aurzen suggests for rear-seat projection, showed as unavailable in its US store when we checked; a small tripod on the console or the rear-seat floor works with either ZIP model.</p>
""",
 "sources": [
  ("Aurzen TravelPlay AutoCinema: panels, fit, install, price", "https://aurzen.com/products/aurzen-travelplay-autocinema-screen-for-tesla-model-y"),
  ("Aurzen ZIP Pro: 1080p, 200 ANSI lm, 38 Wh, pre-order date", "https://aurzen.com/products/aurzen-zip-pro-full-hd-portable-projector"),
  ("Aurzen ZIP (US): 720p, 100 ANSI lm, 1.5 h", "https://aurzen.com/products/aurzen-zip-tri-fold-portable-mini-projector-usa"),
  ("Tom's Guide review of the Aurzen ZIP (4/5)", "https://www.tomsguide.com/tvs/aurzen-zip-tri-fold-portable-projector-review"),
  ("2025 Model Y refresh adds an 8-inch rear touchscreen", "https://www.autoguide.com/auto/manufacturers/tesla-manufacturers/tesla-unveils-redesigned-2025-model-y-juniper-44615593"),
  ("Hansshow H86 for Model Y Juniper Standard", "https://www.hansshow.com/products/model-y-juniper-standard-rear-entertainment-screen-h86-android-smart-display-upgrade-for-tesla"),
  ("Hansshow 18.5-inch overhead flip-down", "https://www.hansshow.com/products/model-y-y-juniper-18-5-overhead-screen-electric-flip-down-wifi-android-11-roof-mount-tv-rear-entertainment-monitor"),
  ("Teslahubs Rear Display ULTRA", "https://teslahubs.com/products/rear-display-ultra"),
  ("TESERY 8.66-inch rear display", "https://www.tesery.com/products/tesery-8-66-inch-rear-entertainment-display-screen-for-tesla"),
  ("Tlyard H86 rear display", "https://www.tlyard.com/products/model-3-y-8-6-inch-rear-entertainment-lcd-display-h86-back-screen"),
  ("TESERY seat-back tablet mount", "https://www.tesery.com/products/tablet-holder-headrest-holder-for-tesla-model-3-model-y"),
 ],
 "published": "2026-10-25", "checked": "2026-10-25"},

]
