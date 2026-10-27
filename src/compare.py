# Comparison pages aimed at the search queries the assistants themselves issue (DLC-51, growth/query-pages.md).
# Each page answers one narrow question with a horizontal table across the products the agents name in their
# searches, ours and the brands we do not sell. Our rows carry the price, the code and the buy link from products.py
# and coupons.json (filled by build.py); the other rows carry the manufacturer's published figures with the source URL.
# Figures for the other brands were read from the makers' own US store pages, manuals or FAQs on `checked`; they are
# not re-verified by the daily sweep, so the page says when they were read.
#
# Record: slug (the page lives at /compare/<slug>/, published as /<slug>), question (the target-questions.md id and
# the agent query the page answers), title, h1, desc, intro (HTML), columns [(key, header)], rows, after (HTML after the
# table), sources [(claim, url)], published, checked. Row: {"slug": our product slug or None, "brand", "model",
# "url" (maker page, for rows that are not ours), "cells": {key: HTML}, "note" (optional, shown under the model)}.

# Revision shown under each page's heading; each loop-3 iteration bumps it, and the gating chat asks ChatGPT to read
# it back before the re-evaluation counts (stale copy check).
COMPARE_REV = "2026-10-27 r6"

COMPARISONS = [

# ---------------- Q25: a lot of AA/AAA NiMH cells at once ----------------
# Agent queries seen: "best high capacity AA AAA NiMH battery charger 8 bay 16 bay independent channels 2026 reviews"
# (ChatGPT), "best 8 bay 16 bay AA AAA NiMH charger individual channels 2026", "16 bay AA AAA NiMH battery charger",
# "Powerex MH-C800S 8 cell charger", "Panasonic eneloop 8 position charger BQ-CC" (Claude).
{"slug": "aa-aaa-nimh-battery-charger-8-bay-16-bay", "question": "Q25",
 "title": "Best charger for a lot of AA and AAA NiMH batteries at once: 8-bay and 16-bay chargers with independent channels compared (2026)",
 "h1": "Best charger for a lot of AA and AAA NiMH batteries at once: 8-bay and 16-bay chargers compared",
 "desc": "Twelve AA/AAA NiMH chargers with 8 or 16 independent bays (Tenergy, Panasonic eneloop, Powerex, EBL, XTAR, BONAI, La Crosse, SkyRC): charge current per bay, time to fill a 2,000–2,800 mAh AA, how each one stops, and the price on the maker's own store.",
 "intro": """
<p class="lead">For a household or a camera bag with dozens of AA and AAA NiMH cells, the charger that matters is one with <strong>8 or 16 bays, each on its own channel</strong>, so a tired cell in slot 3 does not stop slot 4 from filling. The table compares every such charger sold in the US today, including the brands Dealectric does not list, on the figures the makers publish: current per bay, time for a full AA, how the charger decides a cell is full, and what else it does (refresh, per-slot display, USB-C power).</p>
<p><strong>Short answer.</strong> Sixteen bays at once: the <strong>Tenergy TN438</strong> ({buy:tenergy-tn438-16-bay-nimh-charger}, 500 mA per AA, Delta-V cut-off plus a safety timer, refresh mode) or the cheaper BONAI 16-bay (LEDs only, 250–500 mA). Eight bays, fast: the <strong>Powerex MH-C800S</strong> (1 A per bay, conditioning cycle) or the 1-hour MH-C801D (2 A). Eight bays, cheap and USB-C powered: the <strong>Tenergy TN480U</strong> ({buy:tenergy-tn480u-8-bay-nimh-charger}, 500 mA per AA, per-slot LCD) or the EBL C9008. Eight bays for eneloop owners who want Panasonic's own charger: the BQ-CC63, which Panasonic does not sell in the US. Anything with 4 bays (La Crosse BC1000, SkyRC MC3000, eneloop BQ-CC65) is here for reference only: better per-cell data, far fewer cells per session.</p>
<p>How to read the current column: NiMH cells charge well at 0.3–1 C (300–1,000 mA for a 2,000 mAh AA; 100–300 mA for a 800 mAh AAA). Below 0.3 C the end-of-charge signal is too weak for the charger to detect and a timer has to stop it; above 1 C only cells rated for it (most 2,000 mAh+ AAs) should be used. Chargers that end on <em>−ΔV</em> (the small voltage dip when a NiMH cell is full) stop on the cell's own signal; those with a timer alone stop on the clock.</p>
""",
 "columns": [("bays", "Bays"), ("cells", "Cells"), ("indep", "Independent channels"), ("current", "Charge current, AA / AAA"),
             ("time", "Time for a 2,000–2,800 mAh AA"), ("stop", "How it stops"), ("extras", "Display, modes"), ("power", "Power")],
 "rows": [
  {"slug": "tenergy-tn480u-8-bay-nimh-charger", "model": "Tenergy TN480U",
   "cells": {"bays": "8", "cells": "AA, AAA (mixed)", "indep": "Yes", "current": "500 mA / 250 mA", "time": "about 4–6 h (not published)",
             "stop": "−ΔV, bad-cell detection", "extras": "Per-slot LCD", "power": "USB-C or micro-USB, 5 V 2 A (adapter not included)"}},
  {"slug": "tenergy-tn438-16-bay-nimh-charger", "model": "Tenergy TN438 16-bay",
   "cells": {"bays": "16", "cells": "AA, AAA NiMH/NiCd", "indep": "Yes", "current": "500 mA / 250 mA", "time": "~5.2 h (2,000 mAh), 6.5 h (2,500 mAh)",
             "stop": "Delta-V cut-off + safety timer; overheat, short, reverse protection", "extras": "Two backlit LCDs; refresh (discharge at 200–300 mA)",
             "power": "AC adapter 12 V 2 A and car adapter included", "price": "$57.99 (power.tenergy.com)"}},
  {"brand": "Panasonic eneloop", "model": "BQ-CC63", "url": "https://www.panasonic.com/global/energy/products/eneloop/en/lineup/charger-bq-cc63.html",
   "note": "Panasonic's only 8-bay; sold in Europe, China, Taiwan and the CIS, not by Panasonic US",
   "cells": {"bays": "8", "cells": "AA, AAA", "indep": "Yes", "current": "not published", "time": "5 h (1,900–2,000 mAh), 6 h (2,450–2,550 mAh)",
             "stop": "−ΔV; dry-cell and bad-insert detection shuts the slot off", "extras": "8 single-colour LEDs", "power": "AC 100–240 V cord",
             "price": "No US list price"}},
  {"brand": "Powerex (Maha Energy)", "model": "MH-C800S", "url": "https://mahaenergy.com/mh-c800s/",
   "cells": {"bays": "8", "cells": "AA, AAA NiMH/NiCd", "indep": "Yes", "current": "1,000 mA / 1,000 mA (soft mode 500 mA)", "time": "1–2 h rapid, 2–4 h soft",
             "stop": "Not named in the manual (pulse charging)", "extras": "LCD per bay; conditioning cycle (charge–discharge–recharge, up to 16 h)",
             "power": "18 V 1 A adapter, AC 100–240 V", "price": "$49.95 (mahaenergy.com; out of stock on 2026-10-23)"}},
  {"brand": "Powerex (Maha Energy)", "model": "MH-C801D", "url": "https://mahaenergy.com/mh-c801d/",
   "note": "Maha now points to the MH-C980 as its successor",
   "cells": {"bays": "8", "cells": "AA, AAA NiMH/NiCd", "indep": "Yes", "current": "2,000 mA / 700 mA (soft 1,000 / 350 mA)", "time": "1 h rapid, 2 h soft",
             "stop": "Not named in the manual; the manual says not to rapid-charge AAs under 2,000 mAh or AAAs under 700 mAh",
             "extras": "LCD; conditioning cycle", "power": "18 V 2 A adapter, AC 100–240 V", "price": "$74.95 (mahaenergy.com)"}},
  {"brand": "EBL", "model": "C9008 8-bay LCD", "url": "https://www.eblofficial.com/products/c9008-8-bay-battery-charger",
   "cells": {"bays": "8 (AA/AAA) or 4 (C/D)", "cells": "AA, AAA, C, D", "indep": "Yes", "current": "not published", "time": "2.5–3 h for one 2,300–2,800 mAh cell (EBL's listing)",
             "stop": "−ΔV with MCU control, then trickle; overheat, over-current, short and alkaline detection", "extras": "LCD (charging / error)",
             "power": "USB-C or micro-USB 5 V 2 A (adapter not included)", "price": "$19.99 (eblofficial.com)"}},
  {"brand": "EBL", "model": "808U (C9041UW) 8-bay", "url": "https://www.eblofficial.com/products/upgraded-808u-8-bay-battery-charger",
   "note": "EBL sells no 16-bay charger today; its indexed 16-slot pages are gone",
   "cells": {"bays": "8", "cells": "AA, AAA NiMH/NiCd", "indep": "Yes", "current": "1,000 mA / 500 mA", "time": "not published",
             "stop": "−ΔV", "extras": "LEDs; two USB-A 5 V 2 A outputs", "power": "AC 100–240 V cord, 15 W", "price": "$16.99 (eblofficial.com, sale)"}},
  {"brand": "BONAI", "model": "16-bay AA/AAA charger", "url": "https://www.amazon.com/dp/B09NW28R66",
   "note": "No manufacturer site; figures from the brand's Amazon listing",
   "cells": {"bays": "16", "cells": "AA, AAA NiMH only", "indep": "Yes", "current": "250–500 mA (a range, not per size)", "time": "2–6 h for one 1,300–2,800 mAh cell (listing)",
             "stop": "Not named; overcharge, over-voltage, overheat, short and reverse protection claimed", "extras": "LED per bay (red/green; flashing = bad cell)",
             "power": "AC 100–240 V cord", "price": "$29.44 (Amazon, 2026-10-23)"}},
  {"brand": "XTAR", "model": "BC8", "url": "https://www.xtar.cc/product/xtar-bc8-charger-190.html",
   "cells": {"bays": "8", "cells": "AA, AAA: 1.2 V NiMH and 1.5 V Li-ion", "indep": "not stated", "current": "500 mA / 500 mA", "time": "not published",
             "stop": "Automatic cut-off (method for NiMH not stated); 0 V activation", "extras": "Six protections; no display per bay",
             "power": "USB-C, 18 W QC 3.0 adapter sold separately", "price": "$19.90 charger only, $29.99 with adapter (xtardirect.com)"}},
  {"brand": "La Crosse Technology", "model": "BC1000 Alpha Power", "url": "https://www.lacrossetechnology.com/products/bc1000",
   "note": "4 bays, for reference",
   "cells": {"bays": "4", "cells": "AA, AAA NiMH/NiCd", "indep": "Yes", "current": "200 / 500 / 700 / 1,000 mA selectable (1,500 / 1,800 mA with two cells)", "time": "depends on the setting",
             "stop": "Not named; stops on overheat, trickle after FULL", "extras": "Charge, discharge, refresh and test modes; LCD with V, mA, time and mAh per bay",
             "power": "AC adapter 3 V 4 A", "price": "$89.95 (lacrossetechnology.com)"}},
  {"brand": "SkyRC", "model": "MC3000", "url": "https://www.skyrc.com/MC3000_Charger",
   "note": "4-bay analyzer, for reference",
   "cells": {"bays": "4", "cells": "AA, AAA, C, 18650 and more; NiMH, NiCd, NiZn, Li-ion, LiFePO4, LTO", "indep": "Yes", "current": "50–3,000 mA settable", "time": "depends on the setting",
             "stop": "−ΔV or 0ΔV, plus temperature, timer and capacity cut-offs; optional trickle", "extras": "Discharge 0.05–2 A, cycle, break-in, refresh, internal resistance, Bluetooth, PC link",
             "power": "DC 11–18 V 4 A adapter", "price": "No price on skyrc.com"}},
  {"brand": "Panasonic eneloop", "model": "BQ-CC65", "url": "https://www.panasonic.com/global/energy/products/eneloop/en/lineup/charger-bq-cc65.html",
   "note": "4 bays, for reference",
   "cells": {"bays": "4", "cells": "AA, AAA", "indep": "Yes", "current": "not published", "time": "1.5 h for 1–2 cells, 3 h for 3–4 (2,000 mAh)",
             "stop": "Voltage detection, stops before overflow", "extras": "3-inch LCD (time left, voltage, capacity bars, end-of-life warning); refresh; 5 V USB out",
             "power": "AC 100–240 V cord", "price": "No US list price"}},
 ],
 "after": """
<h2>Which one, for which pile of cells</h2>
<ul>
<li><strong>Sixteen or more cells in one go</strong> (a houseful of remotes, flashlights and toys): the Tenergy TN438, if you want a display, a refresh mode and a stated cut-off; the BONAI if LEDs are enough. Both run at 500 mA or less per AA, so a full set takes an evening.</li>
<li><strong>Eight cells fast, for cameras or flashes</strong>: the Powerex MH-C800S or MH-C801D. They charge at 1–2 A, which is only for AAs of 2,000 mAh and up; the manual says to use soft mode for smaller cells.</li>
<li><strong>Eight cells from a USB-C port</strong>: the Tenergy TN480U or the EBL C9008. Both need a 5 V 2 A supply, which with eight bays limits them to 500 mA per AA; plan on several hours.</li>
<li><strong>Cell health over speed</strong>: the La Crosse BC1000 or the SkyRC MC3000 measure capacity and internal resistance per cell, which is how you find the one bad cell that keeps draining the rest. Four bays, so they complement an 8- or 16-bay charger rather than replace it.</li>
</ul>
<h2>The cells</h2>
<p>A high-capacity AA to charge in bulk: the <a href="/products/tenergy-premium-pro-aa-2800mah-20-pack/">Tenergy Premium Pro AA, 2,800 mAh, 20-pack</a> ({price:tenergy-premium-pro-aa-2800mah-20-pack}; 1,200 cycles, 85% charge after a year on the shelf). {deal:tenergy-premium-pro-aa-2800mah-20-pack} Panasonic's eneloop (2,000 mAh standard, 2,550 mAh Pro) remains the reference for low self-discharge: Panasonic states up to 70% charge after 10 years of storage and up to 2,100 recharges (IEC 61951-2:2011 method).</p>
""",
 "sources": [
  ("Battery University BU-408, charging NiMH: fast chargers use about 1 C; below 0.3 C the end-of-charge signal is indistinct and a timer must stop the charge; good chargers combine −ΔV, voltage plateau, dT/dt, temperature threshold and time-out", "https://batteryuniversity.com/article/bu-408-charging-nickel-metal-hydride"),
  ("Panasonic eneloop FAQ: recharge when about 70–75% is used; Smart Charge shuts off a slot just before it overflows", "https://www.panasonic.com/global/energy/products/eneloop/en/faq.html"),
  ("Panasonic: eneloop retains up to 70% of its charge after 10 years in storage (IEC 61951-2 7.3.2, 20 °C) and recharges up to 2,100 times", "https://www.panasonicbatteryproducts.com/?p=4839"),
  ("Tenergy TN438 16-bay product page", "https://power.tenergy.com/tenergy-tn438-16-bay-aa-aaa-nimh-lcd-smart-battery-charger/"),
  ("Tenergy TN480U product page", "https://power.tenergy.com/tenergy-tn480u-8-bay-nimh-battery-lcd-display-fast-charger-micro-usb-type-c-input/"),
  ("Panasonic eneloop BQ-CC63 (global lineup)", "https://www.panasonic.com/global/energy/products/eneloop/en/lineup/charger-bq-cc63.html"),
  ("Maha Energy MH-C800S and MH-C801D pages and manuals", "https://mahaenergy.com/mh-c800s/"),
  ("EBL C9008 and 808U product pages", "https://www.eblofficial.com/products/c9008-8-bay-battery-charger"),
  ("XTAR BC8 product page", "https://www.xtar.cc/product/xtar-bc8-charger-190.html"),
  ("La Crosse BC1000 page and manual", "https://www.lacrossetechnology.com/products/bc1000"),
  ("SkyRC MC3000 page and manual v1.17", "https://www.skyrc.com/MC3000_Charger"),
 ],
 "published": "2026-10-23", "checked": "2026-10-23"},

# ---------------- Q17: LiFePO4 vs NMC ----------------
# Agent queries seen: "portable power station LiFePO4 NMC battery chemistry manufacturer comparison 2026", "LiFePO4 vs NMC
# portable power station battery chemistry cycle life energy density safety comparison" (ChatGPT), "best LiFePO4 portable
# power station 2026" (Claude). ChatGPT's result set for it was 13 small sites with the same title and no product table.
{"slug": "lifepo4-vs-nmc-power-stations", "question": "Q17",
 "title": "LiFePO4 vs NMC portable power stations: cycle life, energy density, safety and 25 current models compared (2026)",
 "h1": "LiFePO4 vs NMC power stations: which is better? Cycle life, energy density and 25 current models compared",
 "desc": "What LiFePO4 (LFP) and NMC battery chemistry change in a portable power station (cycle life, Wh per kg, heat tolerance, warranty), with a table of 25 models from BLUETTI, EcoFlow, Anker SOLIX, Jackery, ALLPOWERS, Goal Zero, DJI and Tenergy: chemistry, Wh, rated cycles, weight, Wh/kg and price on the maker's own store.",
 "intro": """
<p class="lead"><strong>LiFePO4 (LFP) is the better chemistry for almost every portable power station bought today</strong>: the makers rate LFP packs at 3,000–6,000 cycles to 80% capacity against about 500 for the NMC packs still on sale, LFP cells tolerate heat better, and every LFP model in the table below carries a 5-year warranty where the NMC models carry 2. NMC's one advantage, more energy per kilogram, barely shows at the product level: the best NMC station here reaches 112 Wh/kg, and three LFP stations (Jackery Explorer 2000 v2, BLUETTI Elite 300, Anker SOLIX C2000 Gen 2) match or beat it, because the inverter, case and ports weigh the same whatever the cells. The market has already decided: of the 25 current models below, 21 are LFP, and the four NMC ones are either sold out or discontinued on their makers' stores.</p>
<h2>What the chemistry changes</h2>
<div class="scroll"><table>
<tr><th></th><th>LiFePO4 (LFP, lithium iron phosphate)</th><th>NMC (lithium nickel manganese cobalt)</th></tr>
<tr><td>Cycle life (cell level)</td><td>2,000–3,000 cycles (PNNL); "2,000 and higher" (Battery University)</td><td>300–1,000 cycles (PNNL); 1,000–2,000 (Battery University)</td></tr>
<tr><td>Cycle life, as the station makers rate it</td><td>3,000–6,000 cycles to 80% (BLUETTI, EcoFlow, Anker, ALLPOWERS); 4,000 to 70% (Jackery, DJI)</td><td>500 cycles (Jackery Explorer 1000, Goal Zero Yeti X); 2,500 claimed by ALLPOWERS for the S2000 Pro</td></tr>
<tr><td>Energy density (cell level)</td><td>90–120 Wh/kg</td><td>150–220 Wh/kg</td></tr>
<tr><td>Energy density, whole station</td><td>53–115 Wh/kg in the table below</td><td>69–112 Wh/kg in the table below</td></tr>
<tr><td>Thermal runaway onset</td><td>about 270 °C</td><td>about 210 °C; a high state of charge promotes it</td></tr>
<tr><td>Cobalt, nickel</td><td>None</td><td>Both</td></tr>
<tr><td>Typical warranty on current stations</td><td>5 years</td><td>2 years</td></tr>
<tr><td>Where NMC still wins</td><td colspan="2">Cold-weather charging below 0 °C (LFP packs refuse to charge; the station's heater or BMS limits apply either way) and the last few hundred grams when the pack dominates the weight, as in small DC-only units.</td></tr>
</table></div>
<p>In practice: a station used daily (van, off-grid cabin, daily UPS) at one full cycle a day wears out an NMC pack rated 500 cycles in under two years and an LFP pack rated 3,500 in about ten. A station used a few weekends a year will not reach either limit; calendar ageing and the warranty matter more, and there LFP's 5 years still wins. The one current NMC model worth considering is the ALLPOWERS S2000 Pro, which ALLPOWERS rates at 2,500 cycles and sells at the lowest price per Wh in the 1.4 kWh class.</p>
<h2>25 current models</h2>
<p>Wh/kg is the station's rated capacity divided by its weight, computed from the makers' figures. "Cycles" is the maker's rating with the end-of-life capacity it states. Prices are the makers' own US store prices (sale price in parentheses) on the date in the note below the table.</p>
""",
 "columns": [("chem", "Chemistry"), ("wh", "Wh"), ("ac", "AC continuous"), ("cycles", "Rated cycles"), ("kg", "Weight"), ("whkg", "Wh/kg"), ("warranty", "Warranty")],
 "rows": [
  {"slug": "bluetti-elite-30-v2", "model": "BLUETTI Elite 30 V2",
   "cells": {"chem": "LiFePO4", "wh": "288", "ac": "600 W", "cycles": "3,000+", "kg": "4.3 kg", "whkg": "67", "warranty": "5 years"}},
  {"brand": "EcoFlow", "model": "RIVER 3 Plus", "url": "https://us.ecoflow.com/products/ecoflow-river-3-plus-portable-power-station-flash-sale",
   "cells": {"chem": "LiFePO4", "wh": "286", "ac": "600 W", "cycles": "3,000 to 80%", "kg": "4.7 kg", "whkg": "61", "warranty": "5 years", "price": "$299"}},
  {"brand": "Anker SOLIX", "model": "C300 DC", "url": "https://us.anker.com/products/c300-dc", "note": "DC only, no AC outlet; sold out on ankersolix.com",
   "cells": {"chem": "LiFePO4", "wh": "288", "ac": "none (300 W DC)", "cycles": "up to 3,000", "kg": "not published", "whkg": "—", "warranty": "3 years", "price": "$249.99"}},
  {"brand": "Jackery", "model": "Explorer 300D", "url": "https://www.jackery.com/products/jackery-explorer-300d-portable-power-station", "note": "DC only (140 W USB-C); the Explorer 300 v2 (288 Wh, 300 W AC, 3.7 kg, $279) is sold out",
   "cells": {"chem": "LiFePO4", "wh": "288", "ac": "none", "cycles": "4,000+ to 70%", "kg": "2.5 kg", "whkg": "115", "warranty": "not stated", "price": "$249 ($209)"}},
  {"slug": "allpowers-r600-299wh", "model": "ALLPOWERS R600",
   "cells": {"chem": "LiFePO4", "wh": "299", "ac": "600 W", "cycles": "3,500+", "kg": "5.6 kg", "whkg": "53", "warranty": "5 years"}},
  {"slug": "tenergy-t320-300wh-power-station", "model": "Tenergy T320",
   "cells": {"chem": "LiFePO4", "wh": "300", "ac": "200 W", "cycles": "~2,000", "kg": "3.7 kg", "whkg": "81", "warranty": "2 years"}},
  {"brand": "Goal Zero", "model": "Yeti 1000X", "url": "https://goalzero.com/products/goal-zero-yeti-1000x-portable-power-station", "note": "NMC; sold out on goalzero.com",
   "cells": {"chem": "NMC", "wh": "997", "ac": "1,500 W", "cycles": "500 to 80%", "kg": "14.4 kg", "whkg": "69", "warranty": "2 years", "price": "$999.95"}},
  {"brand": "Jackery", "model": "Explorer 1000 (original)", "url": "https://www.jackery.com/blogs/jackery-faqs/explorer-1000-basic-information", "note": "NMC; listed at $999 but unavailable, the page now sells the v2",
   "cells": {"chem": "NMC (Jackery: NCM)", "wh": "1,002", "ac": "1,000 W", "cycles": "500", "kg": "10.6 kg", "whkg": "95", "warranty": "not stated", "price": "$999 (unavailable)"}},
  {"slug": "allpowers-p1800-1024wh", "model": "ALLPOWERS P1800",
   "cells": {"chem": "LiFePO4", "wh": "1,024", "ac": "1,800 W", "cycles": "3,000+ to 70%", "kg": "~13 kg", "whkg": "79", "warranty": "2 years"}},
  {"brand": "EcoFlow", "model": "DELTA 3", "url": "https://us.ecoflow.com/products/delta-3-portable-power-station",
   "cells": {"chem": "LiFePO4", "wh": "1,024", "ac": "1,800 W", "cycles": "4,000 to 80%+", "kg": "12.5 kg", "whkg": "82", "warranty": "5 years", "price": "$699 ($629)"}},
  {"brand": "EcoFlow", "model": "DELTA 3 Plus", "url": "https://us.ecoflow.com/products/delta-3-plus-portable-power-station",
   "cells": {"chem": "LiFePO4", "wh": "1,024", "ac": "1,800 W", "cycles": "4,000 to 80%+", "kg": "12.5 kg", "whkg": "82", "warranty": "5 years", "price": "$799 ($719)"}},
  {"brand": "Anker SOLIX", "model": "C1000 Gen 2", "url": "https://us.anker.com/products/c1000-gen2",
   "cells": {"chem": "LiFePO4", "wh": "1,024", "ac": "2,000 W", "cycles": "4,000 to 80%", "kg": "11.3 kg", "whkg": "91", "warranty": "5 years", "price": "$699.99"}},
  {"brand": "DJI", "model": "Power 1000", "url": "https://www.dji.com/power-1000/specs", "note": "Out of stock on store.dji.com; the Power 1000 V2 is not sold in the US yet",
   "cells": {"chem": "LiFePO4", "wh": "1,024", "ac": "2,200 W", "cycles": "4,000 to 70%+", "kg": "13 kg", "whkg": "79", "warranty": "3 + 2 years", "price": "$999 ($699)"}},
  {"brand": "Jackery", "model": "Explorer 1000 v2", "url": "https://www.jackery.com/products/jackery-explorer-1000-v2",
   "cells": {"chem": "LiFePO4", "wh": "1,070", "ac": "1,500 W", "cycles": "4,000 to 70%+", "kg": "10.8 kg", "whkg": "99", "warranty": "3 + 2 years", "price": "$559 ($499)"}},
  {"slug": "bluetti-ac180", "model": "BLUETTI AC180",
   "cells": {"chem": "LiFePO4", "wh": "1,152", "ac": "1,800 W", "cycles": "3,500+", "kg": "~16 kg", "whkg": "72", "warranty": "5 years"}},
  {"slug": "allpowers-s2000-pro-1451wh", "model": "ALLPOWERS S2000 Pro", "note": "The one current NMC model with a long cycle rating",
   "cells": {"chem": "NMC", "wh": "1,451", "ac": "2,400 W", "cycles": "2,500+", "kg": "13 kg", "whkg": "112", "warranty": "5 years"}},
  {"brand": "Goal Zero", "model": "Yeti 1500X", "url": "https://goalzero.com/products/goal-zero-yeti-1500x-portable-power-station", "note": "NMC; sold out on goalzero.com",
   "cells": {"chem": "NMC", "wh": "1,516", "ac": "2,000 W", "cycles": "500 to 80%", "kg": "20.7 kg", "whkg": "73", "warranty": "2 years", "price": "$1,499.95 ($1,124.89)"}},
  {"brand": "Jackery", "model": "Explorer 2000 v2", "url": "https://www.jackery.com/products/explorer-2000-v2-portable-power-station",
   "cells": {"chem": "LiFePO4", "wh": "2,042", "ac": "2,200 W", "cycles": "4,000 to 70%+", "kg": "17.9 kg", "whkg": "114", "warranty": "3 + 2 years", "price": "$999 ($899)"}},
  {"slug": "bluetti-ac200l", "model": "BLUETTI AC200L",
   "cells": {"chem": "LiFePO4", "wh": "2,048 (expandable to 8,192)", "ac": "2,400 W", "cycles": "3,000+ to 80%", "kg": "28.3 kg", "whkg": "72", "warranty": "5 years"}},
  {"brand": "Anker SOLIX", "model": "C2000 Gen 2", "url": "https://us.anker.com/products/c2000-gen2",
   "cells": {"chem": "LiFePO4", "wh": "2,048", "ac": "2,400 W", "cycles": "4,000 to 80%", "kg": "18.9 kg", "whkg": "108", "warranty": "5 years", "price": "$1,499"}},
  {"slug": "bluetti-elite-200-v2", "model": "BLUETTI Elite 200 V2",
   "cells": {"chem": "LiFePO4", "wh": "2,074", "ac": "2,600 W", "cycles": "6,000+ to 80%", "kg": "24.2 kg", "whkg": "86", "warranty": "5 years"}},
  {"slug": "bluetti-elite-300", "model": "BLUETTI Elite 300",
   "cells": {"chem": "LiFePO4", "wh": "3,014", "ac": "2,400 W", "cycles": "6,000+", "kg": "26.3 kg", "whkg": "115", "warranty": "5 years"}},
  {"slug": "allpowers-r4000-3456wh", "model": "ALLPOWERS R4000",
   "cells": {"chem": "LiFePO4", "wh": "3,456", "ac": "3,600 W", "cycles": "3,500+", "kg": "45 kg", "whkg": "77", "warranty": "5 years"}},
  {"brand": "Goal Zero", "model": "Yeti PRO 4000", "url": "https://goalzero.com/products/yeti-pro-4000-power-station",
   "cells": {"chem": "LiFePO4", "wh": "3,994", "ac": "3,600 W", "cycles": "4,000+ (80% DoD)", "kg": "52 kg", "whkg": "77", "warranty": "5 years", "price": "$3,999.95"}},
  {"brand": "EcoFlow", "model": "DELTA Pro 3", "url": "https://us.ecoflow.com/products/delta-pro-3-portable-power-station", "note": "4,000 W is the 120/240 V combined rating",
   "cells": {"chem": "LiFePO4", "wh": "4,096", "ac": "4,000 W", "cycles": "4,000 to 80%", "kg": "51.5 kg", "whkg": "80", "warranty": "5 years", "price": "$3,299 ($2,799)"}},
 ],
 "after": """
<h2>How to choose between them</h2>
<ul>
<li><strong>Daily use, home backup kept for years, anything on a UPS duty cycle</strong>: LFP, and prefer the makers who state the end-of-life capacity with the cycle count (to 80%: BLUETTI, EcoFlow, Anker SOLIX, Goal Zero; to 70%: Jackery, DJI, ALLPOWERS P1800). 4,000 cycles to 70% and 3,000 cycles to 80% describe similar packs.</li>
<li><strong>Weight is the constraint</strong>: compare Wh/kg at the station level rather than the chemistry. At 1 kWh the lightest are the Jackery Explorer 1000 v2 (99 Wh/kg) and Anker SOLIX C1000 Gen 2 (91), both LFP; at 2 kWh the Jackery Explorer 2000 v2 (114) and Anker C2000 Gen 2 (108). The NMC Yeti 1000X and 1500X are heavier per Wh than every LFP unit of their size.</li>
<li><strong>Lowest price per Wh in the catalog</strong>: the ALLPOWERS S2000 Pro (NMC, 1,451 Wh for {buy:allpowers-s2000-pro-1451wh}) and the BLUETTI AC200L and Elite 200 V2 (LFP, about 2 kWh for {buy:bluetti-ac200l}). {deal:allpowers-s2000-pro-1451wh} {deal:bluetti-elite-200-v2}</li>
<li><strong>Small LFP station for a weekend</strong>: BLUETTI Elite 30 V2 ({buy:bluetti-elite-30-v2}, 140 W USB-C), ALLPOWERS R600 ({buy:allpowers-r600-299wh}) or Tenergy T320 ({buy:tenergy-t320-300wh-power-station}). {deal:bluetti-elite-30-v2}</li>
</ul>
<p>Every power station in the Dealectric catalog is on the <a href="/guides/portable-power-stations/">portable power stations guide</a> with its full spec sheet, verified price, code and buy link.</p>
""",
 "sources": [
  ("PNNL-33984 (US DOE), An Introductory Guide to Energy Storage: LFP 2,000–3,000 cycles, NMC 300–1,000 depending on depth of discharge; LFP 'the safest and most common lithium-ion battery', operates safely at higher temperatures", "https://www.pnnl.gov/main/publications/external/technical_reports/PNNL-33984.pdf"),
  ("Battery University BU-205: LFP 90–120 Wh/kg, 2,000+ cycles, thermal runaway about 270 °C; NMC 150–220 Wh/kg, 1,000–2,000 cycles, about 210 °C", "https://batteryuniversity.com/article/bu-205-types-of-lithium-ion"),
  ("US DOE Storage Innovations 2030, lithium-ion technology strategy assessment: LFP has no cobalt or nickel and is forecast to be the major chemistry by 2030", "https://www.energy.gov/sites/default/files/2023-09/2_Technology%20Strategy%20Assessment%20-%202%20Lithium-ion_508.pdf"),
  ("EcoFlow US product pages (RIVER 3 Plus, DELTA 3, DELTA 3 Plus, DELTA Pro 3) and warranty policy", "https://us.ecoflow.com/pages/warranty-policy"),
  ("Anker SOLIX US product pages (C300 DC, C1000 Gen 2, C2000 Gen 2) and warranty policy", "https://us.ankersolix.com/pages/anker-portable-power-station-warranty-policy"),
  ("Jackery product pages (Explorer 300D, 1000 v2, 2000 v2) and the Explorer 1000 FAQ", "https://www.jackery.com/products/jackery-explorer-1000-v2"),
  ("Goal Zero product pages (Yeti 1000X, 1500X, PRO 4000)", "https://goalzero.com/products/yeti-pro-4000-power-station"),
  ("DJI Power 1000 specifications", "https://www.dji.com/power-1000/specs"),
 ],
 "published": "2026-10-23", "checked": "2026-10-23"},

# ---------------- Q16: CPAP ----------------
# Agent queries seen: "best portable power station for CPAP machine 2026 runtime humidifier pure sine wave" (ChatGPT),
# "best portable power station for CPAP 2026" (Claude). ChatGPT's result set: 12 small sites, no runtime table.
{"slug": "power-station-for-cpap", "question": "Q16",
 "title": "Best portable power station for a CPAP machine (2026): nights per charge with and without the humidifier, 17 models compared",
 "h1": "Best portable power station for a CPAP machine: nights per charge, with and without the humidifier",
 "desc": "How many 8-hour nights 17 current power stations (BLUETTI, EcoFlow, Anker SOLIX, Jackery, Goal Zero, DJI, ALLPOWERS, Tenergy) run a ResMed or Philips CPAP, computed from ResMed's measured draw (7 W machine only, 22 W with humidifier, 34 W with heated tube) and the makers' 0.85 inverter rule; plus the 12 V port, UPS switchover, noise and price of each.",
 "intro": """
<p class="lead">A CPAP machine draws far less than most buyers expect: ResMed measured its AirSense 10 at <strong>7 W with the humidifier off, 22 W with the humidifier on and 34 W with the humidifier and heated tube</strong>. So a 300 Wh station runs the machine alone for three nights and a 1,000 Wh station for ten; turning the humidifier on costs two-thirds of that. The table gives the nights per charge for each station at those three settings, computed with the rule the station makers themselves publish (capacity × 0.85 for inverter losses ÷ watts ÷ 8 hours), together with the features that matter for a bedside machine: a 12 V port for the CPAP maker's DC converter, the UPS switchover time if it sits between the wall and the machine, and fan noise.</p>
<p><strong>Short answer.</strong> For one or two nights with the humidifier (camping, a power cut): a 300 Wh station such as the <strong>BLUETTI Elite 30 V2</strong> ({buy:bluetti-elite-30-v2}, ≤10 ms UPS, 12 V port) or the EcoFlow RIVER 3 Plus. For a week of nights, or several nights with humidifier and heated tube: a 1 kWh station such as the <strong>ALLPOWERS P1800</strong> ({buy:allpowers-p1800-1024wh}, the cheapest 1 kWh here), <strong>BLUETTI AC180</strong> ({buy:bluetti-ac180}, 1,152 Wh, 20 ms UPS) or the Jackery Explorer 1000 v2. For nightly use at home as a UPS, pick a station whose switchover is stated (≤10–20 ms) and whose fan is quiet: EcoFlow, Anker SOLIX and DJI publish 20–30 dB; BLUETTI's AC70 publishes 45 dB in silent charging mode. <strong>Use the 12 V port where you can</strong>: ResMed's Air10 and Air11 DC/DC converters and Philips' DC cord run the machine from the station's 12 V socket, skipping the inverter and its idle draw, which at a 7–22 W load is a real share of the night.</p>
<p>How the nights are computed: nights = Wh × 0.85 ÷ W ÷ 8 h, rounded down to one decimal. 10 W stands for the machine alone (ResMed's 7 W plus margin), 25 W for the humidifier on, 35 W for humidifier plus heated tube; Philips does not publish a watt figure for the DreamStation 2 (its label says 1.0–2.0 A at 100–240 V AC), and ResMed's AirSense 11 spec sheet gives a 56 W typical rating, which is a power-supply rating rather than a measured night: real nights fall between the 25 W and 35 W columns for most users. Stations above 1.2 kWh are left out; a CPAP does not need them.</p>
""",
 "columns": [("wh", "Wh"), ("ac", "AC continuous"), ("dc", "12 V port"), ("usbc", "USB-C"), ("ups", "UPS switchover"), ("noise", "Noise (maker)"), ("kg", "Weight"),
             ("nights", "Nights: 10 W / 25 W / 35 W")],
 "rows": [
  {"brand": "EcoFlow", "model": "RIVER 3 Plus", "url": "https://us.ecoflow.com/products/ecoflow-river-3-plus-portable-power-station-flash-sale",
   "cells": {"wh": "286", "ac": "600 W", "dc": "not listed", "usbc": "100 W", "ups": "<10 ms", "noise": "<30 dB", "kg": "4.7 kg", "nights": "3.0 / 1.2 / 0.8", "price": "$299"}},
  {"brand": "Anker SOLIX", "model": "C300 (AC)", "url": "https://www.ankersolix.com/products/c300", "note": "Sold out on ankersolix.com",
   "cells": {"wh": "288", "ac": "300 W", "dc": "not listed", "usbc": "140 W", "ups": "10 ms", "noise": "25 dB at 1 m", "kg": "not published", "nights": "3.0 / 1.2 / 0.8", "price": "not shown (sold out)"}},
  {"brand": "Jackery", "model": "Explorer 300 v2", "url": "https://www.jackery.com/products/jackery-explorer-300-v2-portable-power-station", "note": "Sold out on jackery.com",
   "cells": {"wh": "288", "ac": "300 W", "dc": "not listed", "usbc": "not itemized", "ups": "not stated", "noise": "not published", "kg": "3.7 kg", "nights": "3.0 / 1.2 / 0.8", "price": "$299 ($279)"}},
  {"slug": "bluetti-elite-30-v2", "model": "BLUETTI Elite 30 V2",
   "cells": {"wh": "288", "ac": "600 W", "dc": "12 V car port + 2× DC5521", "usbc": "140 W + 100 W", "ups": "≤10 ms", "noise": "not published", "kg": "4.3 kg", "nights": "3.0 / 1.2 / 0.8"}},
  {"slug": "allpowers-r600-299wh", "model": "ALLPOWERS R600",
   "cells": {"wh": "299", "ac": "600 W", "dc": "12 V / 10 A", "usbc": "2× 100 W", "ups": "≤10 ms", "noise": "not published", "kg": "5.6 kg", "nights": "3.1 / 1.2 / 0.9"}},
  {"slug": "tenergy-t320-300wh-power-station", "model": "Tenergy T320",
   "cells": {"wh": "300", "ac": "200 W pure sine", "dc": "12 V / 10 A + 2× DC5521", "usbc": "45 W", "ups": "not stated", "noise": "not published", "kg": "3.7 kg", "nights": "3.1 / 1.2 / 0.9"}},
  {"brand": "Goal Zero", "model": "Yeti 500", "url": "https://www.goalzero.com/products/yeti-500-portable-power-station-lfp-battery",
   "cells": {"wh": "499", "ac": "500 W", "dc": "12 V aux 162 W + 6 mm 135 W", "usbc": "100 W", "ups": "pass-through; time not stated", "noise": "not published", "kg": "7.3 kg", "nights": "5.3 / 2.1 / 1.5", "price": "$499.95"}},
  {"brand": "DJI", "model": "Power 500", "url": "https://store.dji.com/product/dji-power-500",
   "cells": {"wh": "512", "ac": "1,000 W", "dc": "none (SDC Lite port instead)", "usbc": "2× 100 W (page also says 140 W)", "ups": "not stated", "noise": "23 dB", "kg": "7.3 kg", "nights": "5.4 / 2.1 / 1.5", "price": "$499 ($299)"}},
  {"brand": "Goal Zero", "model": "Yeti 700", "url": "https://www.goalzero.com/products/yeti-700-portable-power-station-lfp-batteries",
   "cells": {"wh": "677", "ac": "600 W", "dc": "12 V aux 162 W + 6 mm 135 W", "usbc": "100 W", "ups": "pass-through; time not stated", "noise": "not published", "kg": "9.2 kg", "nights": "7.1 / 2.8 / 2.0", "price": "$699.95"}},
  {"brand": "BLUETTI", "model": "AC70", "url": "https://www.bluettipower.com/products/ac70", "note": "Not in the Dealectric catalog",
   "cells": {"wh": "768", "ac": "1,000 W", "dc": "12 V / 10 A regulated", "usbc": "2× 100 W", "ups": "20 ms", "noise": "45 dB (silent charging mode)", "kg": "10.2 kg", "nights": "8.1 / 3.2 / 2.3", "price": "$359"}},
  {"slug": "allpowers-p1800-1024wh", "model": "ALLPOWERS P1800",
   "cells": {"wh": "1,024", "ac": "1,800 W", "dc": "12 V car port 120 W", "usbc": "2× (140 W max)", "ups": "≤10 ms (images say 15 ms)", "noise": "not published", "kg": "~13 kg", "nights": "10.8 / 4.3 / 3.1"}},
  {"brand": "EcoFlow", "model": "DELTA 3 Plus", "url": "https://us.ecoflow.com/products/delta-3-plus-portable-power-station",
   "cells": {"wh": "1,024", "ac": "1,800 W", "dc": "12.6 V / 10 A, 126 W", "usbc": "2× 140 W", "ups": "<10 ms", "noise": "<30 dB under 600 W", "kg": "12.5 kg", "nights": "10.8 / 4.3 / 3.1", "price": "$799 ($719)"}},
  {"brand": "Anker SOLIX", "model": "C1000 Gen 2", "url": "https://www.ankersolix.com/products/c1000-gen2", "note": "Anker's page names CPAP machines for its UPS mode",
   "cells": {"wh": "1,024", "ac": "2,000 W", "dc": "12 V / 10 A, 120 W", "usbc": "140 W", "ups": "10 ms", "noise": "20 dB", "kg": "11.3 kg", "nights": "10.8 / 4.3 / 3.1", "price": "$699.99"}},
  {"brand": "BLUETTI", "model": "Elite 100 V2", "url": "https://www.bluettipower.com/products/elite-100-v2-portable-power-station", "note": "Not in the Dealectric catalog; ships Nov 12",
   "cells": {"wh": "1,024", "ac": "1,800 W", "dc": "not itemized (11 ports)", "usbc": "not itemized", "ups": "≤10 ms", "noise": "30 dB", "kg": "11.5 kg", "nights": "10.8 / 4.3 / 3.1", "price": "$499"}},
  {"brand": "DJI", "model": "Power 1000", "url": "https://store.dji.com/product/dji-power-1000", "note": "Out of stock on store.dji.com",
   "cells": {"wh": "1,024", "ac": "2,200 W", "dc": "none", "usbc": "140 W", "ups": "not stated", "noise": "~23 dB", "kg": "13 kg", "nights": "10.8 / 4.3 / 3.1", "price": "$999 ($699)"}},
  {"brand": "Jackery", "model": "Explorer 1000 v2", "url": "https://www.jackery.com/products/jackery-explorer-1000-v2",
   "cells": {"wh": "1,070", "ac": "1,500 W", "dc": "12 V / 10 A", "usbc": "100 W + 30 W", "ups": "bypass mode; time not published", "noise": "30 dB", "kg": "10.8 kg", "nights": "11.3 / 4.5 / 3.2", "price": "$559 ($499)"}},
  {"slug": "bluetti-ac180", "model": "BLUETTI AC180",
   "cells": {"wh": "1,152", "ac": "1,800 W", "dc": "12 V / 10 A", "usbc": "100 W", "ups": "20 ms", "noise": "not published", "kg": "~16 kg", "nights": "12.2 / 4.8 / 3.4"}},
 ],
 "after": """
<h2>The CPAP side of the equation</h2>
<div class="scroll"><table>
<tr><th>Machine</th><th>Power supply</th><th>Measured or rated draw</th><th>DC option</th></tr>
<tr><td>ResMed AirSense 10</td><td>90 W, 24 V 3.75 A</td><td>Measured per hour: 7 W device only, 22 W with humidifier, 34 W with humidifier and ClimateLineAir heated tube, 5 W standby (ResMed, AutoSet 8–15 cmH2O, humidity 6, tube 28 °C). Spec sheet: 53 W typical, 104 W peak.</td><td>Air10 DC/DC converter, 12 V or 24 V input, sold by ResMed</td></tr>
<tr><td>ResMed AirSense 11</td><td>65 W, 24 V 2.71 A</td><td>Spec sheet: 56 W typical, 73 W peak (ratings, not a measured night; no humidifier split published)</td><td>Air11 DC/DC converter, 12 V or 24 V input, works with the HumidAir humidifier and heated tube</td></tr>
<tr><td>Philips DreamStation 2</td><td>100–240 V AC, 1.0–2.0 A</td><td>No watt figure published</td><td>Philips Respironics DC power cord plus battery adapter cable, 12 V</td></tr>
</table></div>
<ul>
<li><strong>Humidifier off doubles to triples the nights.</strong> ResMed's own measurement is the only maker figure that quantifies it: 7 W → 22 W → 34 W. Both EcoFlow and Anker SOLIX advise turning the heated tube and humidifier down or off when the station must last.</li>
<li><strong>The 12 V port beats the AC outlet at this load.</strong> An inverter's own idle draw is not published by most makers but is of the same order as the machine alone; with the CPAP maker's DC converter on the 12 V socket that loss is gone. Check the station has a regulated 12 V output (BLUETTI, Jackery, ALLPOWERS, EcoFlow DELTA 3 Plus, Goal Zero do; the DJI Power units, EcoFlow RIVER 3 Plus and Anker C300 list none).</li>
<li><strong>At home, as a UPS</strong>: a stated switchover time (10–20 ms here) keeps the machine running through an outage without a restart; fan noise is then the spec to compare, and only EcoFlow, Anker SOLIX, DJI, Jackery and BLUETTI's newest models publish one.</li>
<li><strong>Pure sine wave</strong>: every lithium station in the table has a pure sine-wave inverter; the CPAP's switch-mode power supply is indifferent, but the humidifier heater is not, so avoid old modified-sine inverters.</li>
</ul>
<h2>The Dealectric picks, with their codes</h2>
<ul>
<li>BLUETTI Elite 30 V2, 288 Wh, {price:bluetti-elite-30-v2}: {deal:bluetti-elite-30-v2}</li>
<li>ALLPOWERS P1800, 1,024 Wh, {price:allpowers-p1800-1024wh}: {deal:allpowers-p1800-1024wh}</li>
<li>BLUETTI AC180, 1,152 Wh, {price:bluetti-ac180}: {deal:bluetti-ac180}</li>
</ul>
""",
 "sources": [
  ("ResMed, Power consumption of Air10 devices (measured: 7 W device only, 22 W with humidifier, 34 W with humidifier and ClimateLineAir, 5 W standby)", "https://document.resmed.com/documents/products/machine/air10-lumis-series/Power+consumption+Air10+devices.pdf"),
  ("ResMed AirSense 10 user guide, technical specifications (90 W PSU, 53 W typical, 104 W peak)", "https://document.resmed.com/documents/products/machine/airsense-series/user-guide/3781126_airsense-10-autoset-elite-afh_user-guide_eur3_multi.pdf"),
  ("ResMed AirSense 11 user guide (65 W PSU, 56.1 W typical, 73.2 W peak)", "https://document.resmed.com/documents/products/machine/airsense-11/user-guide/airsense11_user-guide_amer_mul.pdf"),
  ("ResMed battery and power converters (Air10 DC/DC converter, 12 V or 24 V source)", "https://www.resmed.com/en-us/products/cpap/battery-and-power-converters/"),
  ("Philips DreamStation 2 instructions for use (100–240 VAC 2.0–1.0 A; DC power cord and battery adapter cable)", "https://www.documents.philips.com/assets/Instruction%20for%20Use/20250630/31be0106520e4457b254b30c011d7f1e.pdf"),
  ("Anker SOLIX, CPAP watt calculator: runtime = Wh × 0.85 ÷ CPAP watts; reduce heating, turn off heated tubing when unnecessary", "https://www.ankersolix.com/blogs/portable-power-station/cpap-watt-calculator"),
  ("EcoFlow, what size power station for a CPAP: required Wh ≈ energy ÷ 0.85; heated humidifiers and tubing reduce runtime", "https://www.ecoflow.com/au/blog/what-size-power-station-do-i-need-for-cpap-machine"),
  ("Station pages: EcoFlow RIVER 3 Plus and DELTA 3 Plus, Anker SOLIX C300 and C1000 Gen 2, Jackery Explorer 300 v2 and 1000 v2, Goal Zero Yeti 500 and 700, DJI Power 500 and 1000, BLUETTI AC70 and Elite 100 V2 (US stores, 2026-10-23)", "https://www.ankersolix.com/products/c1000-gen2"),
 ],
 "published": "2026-10-23", "checked": "2026-10-23"},

# ---------------- Q21: solar watts to recharge 1,000 Wh ----------------
# Agent queries seen: "how many watts solar panel to recharge 1000Wh portable power station solar charging losses peak sun
# hours" (ChatGPT), "best 200W 400W portable solar panel for power station 2026" (Claude). ChatGPT's result set: 12 small
# sites and calculators.
{"slug": "solar-watts-to-recharge-power-station", "question": "Q21",
 "title": "How many watts of solar to recharge a 1,000 Wh power station? 15 portable panels and 10 stations' solar inputs compared (2026)",
 "h1": "How many watts of solar does it take to recharge a 1,000 Wh power station?",
 "desc": "Sizing a solar panel for a 1 kWh portable power station: hours of strong sun to refill 1,000 Wh with each of 15 current panels (ALLPOWERS, EcoFlow, Jackery, Anker SOLIX, BLUETTI, Goal Zero, Renogy, DJI) at 70% of rated output, the solar input limit and voltage range of 10 stations, and the makers' own recharge-time claims.",
 "intro": """
<p class="lead"><strong>Rule of thumb: 300 W of rated panel refills a 1,000 Wh station in one good day; 600 W in half a day.</strong> A portable panel delivers about 70–80% of its rated watts in real sun (Jackery's own figure; Goal Zero and Anker say the same without a number), so a 200 W panel gives about 140 W and needs seven hours of strong sun for 1,000 Wh, a 400 W panel about 3.6 hours. Two limits cap the answer: the station's <strong>maximum solar input</strong> (400 W on a Jackery Explorer 1000 v2 or DJI Power 1000, 500–650 W on a BLUETTI AC180, EcoFlow DELTA 3 or ALLPOWERS P1800, 1,000 W on a DELTA 3 Plus) and its <strong>input voltage range</strong>: a 400 W panel's open-circuit voltage is 45–48 V, fine for a 60 V input and too high for the DJI Power 1000 (30 V) or the small 300 Wh stations (24–28 V).</p>
<p><strong>Short answer.</strong> One panel, one day: the <strong>ALLPOWERS SP037 400 W</strong> ({buy:allpowers-sp037-400w-solar-panel}, Voc 45.3 V, MC4 with XT60 and DC adapters included), the cheapest 400 W panel here and within the input range of every 60 V station; the EcoFlow 400W and Anker SOLIX PS400 Bifacial do the same job at $600–700. Lighter, slower: a 200–220 W panel (EcoFlow 220W Bifacial, Jackery SolarSaga 200, Anker PS200, BLUETTI SP200L) at 6.5–7 hours for 1,000 Wh, or two of them in parallel if the station's input allows. A 100 W panel takes two days.</p>
<p>How the hours are computed: hours = 1,000 Wh ÷ (rated W × 0.7). That is hours of strong, direct sun with the panel facing it; a day gives roughly four to six such hours in most of the US in summer and fewer in winter, and PVWatts (pvwatts.nlr.gov) gives the figure for a location. Add about 10% for the station's charging loss. The makers' own recharge-time claims are in the second table for comparison.</p>
<h2>15 portable panels: hours of strong sun to put 1,000 Wh into a station</h2>
""",
 "columns": [("w", "Rated W"), ("voc", "Voc"), ("conn", "Connector"), ("fold", "Folded"), ("kg", "Weight"), ("ip", "Weather"), ("hours", "Hours for 1,000 Wh (70% output)")],
 "rows": [
  {"slug": "allpowers-sp037-400w-solar-panel", "model": "ALLPOWERS SP037 400 W",
   "cells": {"w": "400", "voc": "45.3 V (Vmp 37.4 V)", "conn": "MC4; MC4→XT60, DC5525, DC8020 adapters included", "fold": "1,048 × 532 × 65 mm", "kg": "18.5 kg", "ip": "IP67, ETFE", "hours": "3.6 h"}},
  {"brand": "EcoFlow", "model": "400W Portable", "url": "https://us.ecoflow.com/products/400w-portable-solar-panel", "note": "Electrical figures from an EcoFlow support reply on the page, not a spec table",
   "cells": {"w": "400", "voc": "48 V (Vmp 41 V)", "conn": "MC4-type; solar-to-XT60 cable included", "fold": "1,058 × 620 × 25 mm", "kg": "16 kg", "ip": "IP68", "hours": "3.6 h", "price": "$699 (members $599)"}},
  {"brand": "Anker SOLIX", "model": "PS400 Bifacial", "url": "https://www.ankersolix.com/products/ps400-bifacial-portable-solar-panel", "note": "Voc not published; the original PS400 (sold out) was 57.6 V",
   "cells": {"w": "400", "voc": "not published (Vmp 48 V)", "conn": "Solar cables + XT-60i", "fold": "22.3 × 38.7 × 3.2 in", "kg": "9.9 kg", "ip": "IP68", "hours": "3.6 h", "price": "$599.99 (list $699.99)"}},
  {"brand": "BLUETTI", "model": "350W Solar Panel", "url": "https://www.bluettipower.com/products/350w-solar-panel", "note": "Spec table says 44 V Voc; the page's marketing copy says 33 V",
   "cells": {"w": "350", "voc": "44 V (Vmp 37 V)", "conn": "MC4", "fold": "745 × 785 × 50 mm", "kg": "14.7 kg", "ip": "IP67", "hours": "4.1 h", "price": "$649 (members $569)"}},
  {"brand": "EcoFlow", "model": "NextGen 220W Bifacial", "url": "https://us.ecoflow.com/products/nextgen-220w-bifacial-portable-solar-panel",
   "cells": {"w": "220 (+175 rear)", "voc": "21.5 V (Vmp 18.4 V)", "conn": "MC4-type; solar-to-XT60 cable included", "fold": "615 × 590 × 32 mm", "kg": "7.0 kg", "ip": "IP68", "hours": "6.5 h", "price": "$399 (2-pack $769)"}},
  {"brand": "Jackery", "model": "SolarSaga 200W (bifacial)", "url": "https://www.jackery.com/products/solarsaga-200w-solar-panel",
   "cells": {"w": "200 (225 bifacial)", "voc": "22 V (Vmp 18 V)", "conn": "DC8020; DC8020→DC7909 adapter included", "fold": "600 × 597 × 40 mm", "kg": "6.5 kg", "ip": "IP68", "hours": "7.1 h", "price": "$379 (was $429)"}},
  {"brand": "Anker SOLIX", "model": "PS200 Bifacial", "url": "https://www.ankersolix.com/products/ps200-bifacial-portable-solar-panel",
   "cells": {"w": "200", "voc": "not published (Vmp 48 V)", "conn": "Solar cables + XT-60i", "fold": "27.0 × 31.2 × 1.8 in", "kg": "4.8 kg", "ip": "IP68", "hours": "7.1 h", "price": "$399.99 (list $499.99)"}},
  {"brand": "BLUETTI", "model": "SP200L 200 W", "url": "https://www.bluettipower.com/products/bluetti-sp200l-solar-panel-200w",
   "cells": {"w": "200", "voc": "24.6 V", "conn": "MC4", "fold": "585 × 608 × 45 mm", "kg": "8.1 kg", "ip": "not stated", "hours": "7.1 h", "price": "$399 (members $329)"}},
  {"brand": "Goal Zero", "model": "Nomad 200", "url": "https://www.goalzero.com/products/nomad-200-solar-panel",
   "cells": {"w": "200", "voc": "23.0 V (Vmp 19.1 V)", "conn": "Goal Zero HPP (14–23 V, up to 14 A)", "fold": "716 × 566 × 50 mm", "kg": "10 kg", "ip": "not stated", "hours": "7.1 h", "price": "$599.95"}},
  {"brand": "Goal Zero", "model": "Boulder 200 Briefcase", "url": "https://www.goalzero.com/products/boulder-200-solar-panel-briefcase", "note": "Rigid glass panels",
   "cells": {"w": "200", "voc": "21.8 V", "conn": "Goal Zero HPP (14–22 V, up to 14 A)", "fold": "1,016 × 700 × 89 mm", "kg": "19 kg", "ip": "not stated", "hours": "7.1 h", "price": "$599.95"}},
  {"brand": "Renogy", "model": "200 W 12 V N-Type Suitcase Kit", "url": "https://www.renogy.com/200-watt-12-volt-monocrystalline-foldable-solar-suitcase/", "note": "A 12 V battery kit with a PWM controller and alligator clips, not a power-station panel; pre-order, ships Oct 30",
   "cells": {"w": "200", "voc": "21.5 V (Vmp 18.7 V)", "conn": "MC4-compatible to alligator clips, 20 A PWM controller fitted", "fold": "870 × 580 × 80 mm", "kg": "12.9 kg", "ip": "not stated", "hours": "7.1 h", "price": "$322.99"}},
  {"brand": "EcoFlow", "model": "NextGen 160W", "url": "https://us.ecoflow.com/products/nextgen-160w-portable-solar-panel",
   "cells": {"w": "160", "voc": "21.3 V (Vmp 18.6 V)", "conn": "MC4-type + XT60 cable", "fold": "600 × 572 × 32 mm", "kg": "5.6 kg", "ip": "IP68", "hours": "8.9 h", "price": "$369"}},
  {"brand": "Jackery", "model": "SolarSaga 100 Prime", "url": "https://www.jackery.com/products/jackery-solarsaga-100-prime-solar-panel", "note": "Rigid, not foldable; the SolarSaga 100W is no longer in Jackery's catalog",
   "cells": {"w": "100 (108 bifacial)", "voc": "22.7 V (Vmp 18.7 V)", "conn": "Anderson; Anderson→DC8020 adapter included", "fold": "986 × 552 × 29 mm", "kg": "6.0 kg", "ip": "IP68", "hours": "14.3 h", "price": "$199 (was $249)"}},
  {"brand": "DJI", "model": "Zignes 100W", "url": "https://store.dji.com/product/zignes-100w-solar-panel", "note": "Proprietary connector; needs DJI's $59 MPPT adapter module to feed a Power station",
   "cells": {"w": "100", "voc": "up to 29 V", "conn": "DJI proprietary (adapter module has an XT60 input)", "fold": "343 × 532 × 50 mm", "kg": "4.1 kg", "ip": "IP65", "hours": "14.3 h", "price": "$209"}},
 ],
 "after": """
<h2>10 stations: what solar they accept, and the makers' own recharge claims</h2>
<div class="scroll"><table>
<tr><th>Station</th><th>Wh</th><th>Max solar input</th><th>Voltage range</th><th>Maker's recharge claim</th><th>Price</th></tr>
<tr><td><a href="/products/bluetti-elite-30-v2/">BLUETTI Elite 30 V2</a></td><td>288</td><td>200 W, 10 A</td><td>12–28 V</td><td>—</td><td>{buy:bluetti-elite-30-v2}</td></tr>
<tr><td><a href="/products/allpowers-r600-299wh/">ALLPOWERS R600</a></td><td>299</td><td>220 W, 8.8 A</td><td>12–60 V</td><td>—</td><td>{buy:allpowers-r600-299wh}</td></tr>
<tr><td><a href="/products/tenergy-t320-300wh-power-station/">Tenergy T320</a></td><td>300</td><td>MPPT, 60 W panel suggested</td><td>5–24 V</td><td>about 7 h with the suggested panel</td><td>{buy:tenergy-t320-300wh-power-station}</td></tr>
<tr><td><a href="https://www.jackery.com/products/jackery-explorer-1000-v2" rel="nofollow noopener">Jackery Explorer 1000 v2</a></td><td>1,070</td><td>400 W over 2× DC8 mm, 21 A total</td><td>12–60 V (10.5 A per port)</td><td>7.5 h with one SolarSaga 200W</td><td>$559 ($499)</td></tr>
<tr><td><a href="https://store.dji.com/product/dji-power-1000" rel="nofollow noopener">DJI Power 1000</a></td><td>1,024</td><td>400 W via the MPPT adapter module, 200 W per channel</td><td>12–30 V (panel Voc under 30 V)</td><td>3 Zignes 100W: 3.6–7.2 h; 2: 5–10 h</td><td>$999 ($699), out of stock</td></tr>
<tr><td><a href="https://us.ecoflow.com/products/delta-3-portable-power-station" rel="nofollow noopener">EcoFlow DELTA 3</a></td><td>1,024</td><td>500 W</td><td>11–60 V</td><td>2 h at 500 W (internal testing)</td><td>$699 ($629)</td></tr>
<tr><td><a href="/products/bluetti-ac180/">BLUETTI AC180</a></td><td>1,152</td><td>500 W, 10 A</td><td>12–60 V</td><td>2.8–3.3 h at 500 W (prime sunshine, ideal orientation)</td><td>{buy:bluetti-ac180}</td></tr>
<tr><td><a href="https://www.ankersolix.com/products/c1000-gen2" rel="nofollow noopener">Anker SOLIX C1000 Gen 2</a></td><td>1,024</td><td>600 W</td><td>11–28 V at 8.2 A; 29–60 V at 14.5 A</td><td>1.8 h at 600 W</td><td>$699.99</td></tr>
<tr><td><a href="https://www.goalzero.com/products/goal-zero-yeti-1000x-portable-power-station" rel="nofollow noopener">Goal Zero Yeti 1000X</a></td><td>997</td><td>600 W (HPP) + 150 W (8 mm)</td><td>14–50 V</td><td>200 W: 6–12 h; 400 W: 4–8 h; 600 W: 2–4 h</td><td>$999.95, sold out</td></tr>
<tr><td><a href="/products/allpowers-p1800-1024wh/">ALLPOWERS P1800</a></td><td>1,024</td><td>650 W (XT60), 13 A</td><td>11–60 V</td><td>—</td><td>{buy:allpowers-p1800-1024wh}</td></tr>
<tr><td><a href="https://us.ecoflow.com/products/delta-3-plus-portable-power-station" rel="nofollow noopener">EcoFlow DELTA 3 Plus</a></td><td>1,024</td><td>1,000 W over 2 ports, 500 W each</td><td>11–60 V</td><td>70 min at 1,000 W; about 6 h with one 220W panel</td><td>$799 ($719)</td></tr>
</table></div>
<h2>Matching panel to station</h2>
<ul>
<li><strong>Voltage first, watts second.</strong> The panel's open-circuit voltage (Voc, cold morning, no load) must sit inside the station's input range. A 400 W panel at 45–48 V Voc fits every 60 V input above (ALLPOWERS, BLUETTI AC180, EcoFlow, Anker, Jackery) and the Yeti 1000X's 50 V, but not the DJI Power 1000 (30 V) or the 300 Wh stations with 24–28 V inputs, which take a 100–200 W panel at 21–23 V. Panels in series add their Voc; in parallel they add current, so check the amp limit too.</li>
<li><strong>Connectors.</strong> MC4 is the common ground (ALLPOWERS, EcoFlow, BLUETTI, Anker's cables terminate in XT60); Jackery uses DC8020, Goal Zero its HPP plug, DJI a proprietary plug that needs the adapter module. Adapters exist for all of them; the ALLPOWERS SP037 ships with XT60, DC5525 and DC8020 adapters, which covers most stations in this table out of the box.</li>
<li><strong>The makers' recharge claims assume full sun and the maximum input.</strong> BLUETTI says so in its footnote ("prime sunshine, ideal orientation and low temperature"); EcoFlow's are "internal testing". Goal Zero's ranges (6–12 h for 200 W into 1,000 Wh) match the 70% rule within a factor of two, which is the realistic spread between a clear June day and a hazy October one.</li>
<li><strong>Weight versus speed.</strong> The two 400 W fold-outs from ALLPOWERS and EcoFlow weigh 16–18.5 kg; Anker's PS400 Bifacial does 400 W at 9.9 kg. At 200 W, 4.8–8 kg is the norm and the 19 kg Boulder 200 is a fixed-site panel.</li>
</ul>
<p>The Dealectric panel: <a href="/products/allpowers-sp037-400w-solar-panel/">ALLPOWERS SP037 400 W</a>, {price:allpowers-sp037-400w-solar-panel}. {deal:allpowers-sp037-400w-solar-panel} It pairs with the <a href="/products/allpowers-p1800-1024wh/">ALLPOWERS P1800</a> (650 W input; {deal:allpowers-p1800-1024wh}) and the <a href="/products/bluetti-ac180/">BLUETTI AC180</a> (500 W input; {deal:bluetti-ac180}). More on inputs and chemistry in the <a href="/guides/portable-power-stations/">power stations guide</a>.</p>
""",
 "sources": [
  ("Jackery: real-world solar output sits at 70–80% of rated wattage; a 200 W panel often gives 140–160 W", "https://www.jackery.com/blogs/buying-advice/portable-solar-panels-for-camping-the-2026-summer"),
  ("Goal Zero Yeti 1000X: rated watts are what the panel produces in perfect conditions with no cable losses; recharge 6–12 h with 200 W, 4–8 h with 400 W, 2–4 h with 600 W", "https://www.goalzero.com/products/goal-zero-yeti-1000x-portable-power-station"),
  ("Anker SOLIX PS200/PS400 FAQ: actual power may be lower than rated with sunlight, orientation and angle", "https://www.ankersolix.com/products/ps400-bifacial-portable-solar-panel"),
  ("PVWatts calculator (National Laboratory of the Rockies) for solar radiation by location", "https://pvwatts.nlr.gov/"),
  ("EcoFlow DELTA 3 Plus solar generator bundle with one 220W panel: within 6 h; DELTA 3 Plus full in 70 min at 1,000 W; DELTA 3 in 2 h at 500 W", "https://us.ecoflow.com/products/delta-3-series-solar-generator-pv220w"),
  ("Jackery Solar Generator 1000 v2 with SolarSaga 200W: 7.5 h solar charging", "https://www.jackery.com/products/jackery-solar-generator-1000-v2"),
  ("Anker SOLIX C1000 Gen 2: 600 W solar, full in 1.8 h; input 11–28 V at 8.2 A, 29–60 V at 14.5 A", "https://www.ankersolix.com/products/c1000-gen2"),
  ("BLUETTI AC180: 500 W solar in about 2.8–3.3 h with prime sunshine", "https://www.bluettipower.com/products/ac180"),
  ("DJI Power solar panel adapter module (MPPT): 12–30 V, 200 W per channel, 400 W per station; 300W set recharge times", "https://store.dji.com/product/dji-power-solar-panel-adapter-module-mppt"),
  ("Panel pages: EcoFlow 400W, NextGen 220W Bifacial and 160W; Jackery SolarSaga 200W and 100 Prime; Anker SOLIX PS200 and PS400 Bifacial; BLUETTI 350W and SP200L; Goal Zero Nomad 200 and Boulder 200; Renogy 200W suitcase; DJI Zignes 100W (US stores, 2026-10-23)", "https://us.ecoflow.com/products/400w-portable-solar-panel"),
 ],
 "published": "2026-10-23", "checked": "2026-10-23"},

]
