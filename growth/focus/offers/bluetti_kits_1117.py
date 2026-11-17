#!/usr/bin/env python3.12
"""The 40 BLUETTI station-plus-panel kits added 2026-11-17 (DLC-293 step 2): product records composed from BLUETTI's US
store read that day. Prices, compare-at prices and variant ids come from each kit's /products/<handle>.js; dispatch notes,
the price list of the parts and the spec figures from the rendered kit, station and panel pages; warranty terms from
BLUETTI's product-warranty-period page; station facts we already carried from our own station records.

    python3.12 growth/focus/offers/bluetti_kits_1117.py <dir of <handle>.json> <path to src/products.py>   # inserts once
    python3.12 growth/focus/offers/bluetti_kits_1117.py <dir of <handle>.json> --print                     # show them
"""
import json, sys
from pathlib import Path

DAY = "2026-11-17"
B = "https://www.bluettipower.com/products/"
RET = "30-day money-back for unused items in the original package; buyer pays return shipping"
SEP = "BLUETTI's page says each unit is delivered separately."
PANEL_WAR = "12 months on the solar panels (BLUETTI's product warranty period page)"

# what each part cost on its own on BLUETTI's US store on DAY
PART = {"Apex 200": 1099, "Apex 300": 1499, "Elite 30 mini": 239.99, "Elite 10": 129.99, "Elite 100 mini": 429,
        "Elite 100 V2": 499, "Elite 200 V2": 899, "Elite 300": 1199, "Elite 400": 1499, "Pioneer Na": 700,
        "B300K": 1099, "B500K": 1599, "5kWh RV Kit": 3699,
        # bundles BLUETTI sells without panels: the cheapest way to buy the same batteries
        "Apex 200 + B300K": 2199, "Apex 200 + B500K": 2749, "Apex 300 + B300K": 2599, "Apex 300 + B500K": 3299}
PANEL = {  # watts: (price alone, text for the Panels row)
    60: (129, "60 W folding panel (BLUETTI's SORA 60 page: 27.5 V open-circuit, 2.76 A, IP65)"),
    100: (249, "100 W folding panel (BLUETTI's SP100L page: 24.62 V open-circuit, 5.13 A, MC4, 10.9 lb)"),
    200: (399, "200 W folding panel (BLUETTI's 200 W panel page: 24.6 V open-circuit, IP67, 17.15 lb)"),
    350: (649, "350 W folding panel (BLUETTI's 350 W panel page: 44 V open-circuit and 11.4 A short-circuit in its spec table, MC4, IP67, 32.4 lb)"),
    500: (849, "SORA 500, 500 W (49.1 V open-circuit, 13.31 A short-circuit, MC4)"),
    "fx": (329, "100 W panel (the kit page does not name the model; BLUETTI's RV panel is the PV100 FX)"),
}
EXP = {"B300K": 2764.8, "B500K": 5120.0}

ST = {
 "Apex 200": dict(wh=2560, w="3,200 W", battery="2,560 Wh LiFePO4; 6,000+ cycles to 70%",
    ac="3,200 W continuous, 120 V only; 5,400 W Power Lifting for resistive loads; 4× 120 V 20 A and a TT-30R RV outlet",
    solar="3,000 W max: XT60 port 1,000 W, 12–60 V, 25 A; MC4 port 2,000 W, 60–280 V, 16 A", cap=3000,
    extra=[("UPS", "15 ms or less; switched on in the BLUETTI app"), ("Weight", "Station 59.3 lb (26.9 kg); panels extra")],
    war="5 years on the station (BLUETTI US)", pre="late January 2027",
    prenote="Pre-order: BLUETTI's page says the Apex 200 is expected to ship in late January for orders placed on or after Nov. 14 (read 2026-11-17).",
    what="BLUETTI's 120 V home-backup station",
    fit="Home backup for 120 V essentials (fridge, freezer, furnace fan, router) and RVs with a 30 A inlet",
    cav=["No 240 V output: it cannot run a 240 V well pump, dryer or split-phase transfer switch; that needs the Apex 300."]),
 "Apex 300": dict(wh=2764.8, w="3,840 W", battery="2,764.8 Wh LiFePO4; 6,000+ cycles to 80%",
    ac="3,840 W, 120/240 V; 4× 120 V 20 A, TT-30R and a NEMA 14-50R 50 A outlet",
    solar="2,400 W: 2× XT60 ports, each 12–60 V, 20 A, 1,200 W (manual)", cap=2400,
    extra=[("UPS", "0 ms or 20 ms (BLUETTI)"), ("Weight", "Station 83.78 lb (38 kg); panels extra")],
    war="5 years on the station (BLUETTI's product warranty period page)", pre="late January 2027",
    prenote="Pre-order: BLUETTI's page says the Apex 300 is expected to ship in late January (read 2026-11-17).",
    what="BLUETTI's 120/240 V home-backup station",
    fit="Home backup that includes a 240 V load (well pump, dryer) through an electrician-installed transfer switch",
    cav=["No USB or 12 V ports on the Apex 300 without the $299 Hub D1; at 84 lb it lives in one place.",
         "The Apex 300 manual lists the MC4-to-XT60 solar charging cable as sold separately, so check the kit's box list before ordering."]),
 "Elite 30 mini": dict(wh=288, w="300 W", battery="288 Wh; 6,000+ cycles (BLUETTI)",
    ac="300 W (600 W Power Lifting), 7 ports, built-in retractable 140 W USB-C cable",
    solar="100 W max, 12–28 V, 8 A, XT60 (BLUETTI's FAQ)", cap=100,
    extra=[("Wall charging", "80% in 46 min, full in 103 min (BLUETTI)"), ("UPS", "Under 10 ms; 5 W standby draw"), ("Weight", "Station about 7.28 lb (3.3 kg); panel extra")],
    war="BLUETTI's product warranty period page did not list the Elite 30 mini when we read it on 2026-11-17; check the term on the kit page", pre=None, prenote=None,
    what="BLUETTI's 7 lb, 288 Wh station",
    fit="Laptops, phones, cameras, a router or a small fan on a desk, in a car or at a campsite; nothing that draws over 300 W",
    cav=["300 W output: no kettle, microwave or hair dryer."]),
 "Elite 10": dict(wh=128, w="200 W", battery="128 Wh LiFePO4; 3,000+ cycles to 80%",
    ac="200 W, 1 AC outlet plus 5 DC outputs",
    solar="100 W max, 12–28 V, 8.2 A", cap=100,
    extra=[("Wall charging", "Full in about 70 minutes (BLUETTI)"), ("UPS", "10 ms"), ("Weight", "Station 3.97 lb (1.8 kg); panel extra")],
    war="3 years on the station (spec table on BLUETTI's Elite 10 page)", pre=None, prenote=None,
    what="BLUETTI's palm-sized 128 Wh station",
    fit="A laptop, phone and camera kit for travel; BLUETTI says it is not waterproof",
    cav=["128 Wh is about two laptop charges; 200 W output runs no heating appliance."]),
 "Elite 100 mini": dict(wh=1004.8, w="700 W", battery="1,004.8 Wh LFP; 6,000+ cycles",
    ac="700 W total across 3 AC outlets; 9 ports in all",
    solar="Up to 350 W (BLUETTI)", cap=350,
    extra=[("UPS", "10 ms"), ("Weight", "Station 23.59 lb (10.7 kg); panel extra")],
    war="3 years on the station (BLUETTI's product warranty period page)", pre=None, prenote=None,
    what="BLUETTI's compact 1 kWh station",
    fit="Routers, laptops, a CPAP and light car camping; not for kitchen appliances or anything over 700 W",
    cav=["Rated 700 W in total; a reviewer's unit shut down at 900 W (There's A Trick For That, via The Cool Down)."]),
 "Elite 100 V2": dict(wh=1024, w="1,800 W", battery="1,024 Wh LiFePO4; 4,000+ cycles to 80%",
    ac="1,800 W continuous (2,700 W Power Lifting), 2 outlets",
    solar="1,000 W max, 12–60 V, 20 A", cap=1000,
    extra=[("Wall charging", "1,200 W, 0 to 80% in about 45 min"), ("UPS", "10 ms"), ("Weight", "Station 25 lb (11.5 kg); panel extra")],
    war="5 years on the station (BLUETTI's product warranty period page)", pre="mid-December 2026",
    prenote="Pre-order: BLUETTI's page says the Elite 100 V2 ships from mid-December for orders placed on or after Nov. 16 (read 2026-11-17).",
    what="BLUETTI's 1 kWh, 1,800 W station",
    fit="Camping, car trips and short outages: a coffee maker, electric cooler, CPAP and laptops",
    cav=["OutdoorGearLab measured 890 Wh delivered from the 1,024 Wh rating."]),
 "Elite 200 V2": dict(wh=2073.6, w="2,600 W", battery="2,073.6 Wh LiFePO4; 6,000+ cycles to 80%",
    ac="2,600 W continuous; 3,900 W Power Lifting",
    solar="1,000 W max, 12–60 V, 20 A", cap=1000,
    extra=[("UPS", "15 ms or less"), ("Expandable", "No"), ("Weight", "Station 24.2 kg; panels extra")],
    war="5 years on the station (BLUETTI's product warranty period page)", pre="Nov 26, 2026",
    prenote="Pre-order: BLUETTI's page says the Elite 200 V2 ships from November 26 (read 2026-11-17).",
    what="BLUETTI's 2 kWh LiFePO4 station",
    fit="Home backup for a fridge and essentials, or an off-grid cabin weekend",
    cav=["Not expandable: buy the Apex 200 if you may add batteries later."]),
 "Elite 300": dict(wh=3014.4, w="2,400 W", battery="3,014.4 Wh LiFePO4; 6,000+ cycles",
    ac="2,400 W continuous; 4,800 W Power Lifting; 4× 120 V and a TT-30 outlet",
    solar="1,200 W max, 12–60 V, 22 A", cap=1200,
    extra=[("UPS", "10 ms"), ("Expandable", "No"), ("Weight", "Station about 57.98 lb (26.3 kg); panels extra")],
    war="5 years on the station (BLUETTI's product warranty period page)", pre="late November 2026",
    prenote="Pre-order: BLUETTI's page says it ships from late November (read 2026-11-17).",
    what="BLUETTI's 3 kWh station",
    fit="Multi-day home backup or an RV with a 30 A inlet, where the station mostly stays in one place",
    cav=["Not expandable: BLUETTI says it cannot link to its expansion batteries."]),
 "Elite 400": dict(wh=3840, w="2,600 W", battery="3,840 Wh (BLUETTI's page gives no cycle rating in the text we read)",
    ac="2,600 W rated; 3,900 W Lifting Power; 9 outputs",
    solar="1,000 W max, 12–60 V, 20 A", cap=1000,
    extra=[("Wall charging", "80% in 1.9 h, full in 2.5 h on AC alone (BLUETTI)"), ("UPS", "15 ms"), ("Standby draw", "3 W (BLUETTI)"),
           ("Weight", "Station 85.98 lb (39 kg), with wheels and a handle; panels extra")],
    war="5 years on the station (BLUETTI's product warranty period page)", pre="mid-December 2026",
    prenote="Pre-order: BLUETTI's page says the Elite 400 ships from mid-December (read 2026-11-17).",
    what="BLUETTI's wheeled 3.84 kWh station",
    fit="Outage backup for a fridge, router and lights over several days, rolled to where it is needed",
    cav=["86 lb: it rolls on its own wheels but needs two people for stairs or a car boot."]),
 "Pioneer Na": dict(wh=900, w="1,500 W", battery="900 Wh sodium-ion; 4,000+ cycles",
    ac="1,500 W (2,250 W lifting power)",
    solar="500 W max, 12–60 V, 10 A", cap=500,
    extra=[("Cold limits", "Charges down to -15°C (5°F), discharges down to -25°C (-13°F)"), ("Standby loss", "1.5 W"), ("Weight", "Station 35.3 lb (16 kg); panels extra")],
    war="3 years on the station (BLUETTI's product warranty period page)", pre=None, prenote=None,
    what="BLUETTI's sodium-ion station for freezing conditions",
    fit="Unheated garages, cabins, work trucks and winter camping, where a lithium station can't be charged",
    cav=["In a mild climate a lithium unit stores more for less: the Elite 100 V2 was $499 for 1,024 Wh the same day.",
         "Below 14°F it recharges only to 60% (BLUETTI)."]),
}

# (handle, slug, station, expansions, [(count, watts)], summary tail, extra caveats, instead)
K = [
 ("apex-200-200w", "bluetti-apex-200-200w-solar-kit", "Apex 200", [], [(1, 200)], None, [], None),
 ("apex-200-2-x-200w", "bluetti-apex-200-2x200w-solar-kit", "Apex 200", [], [(2, 200)], None, [], None),
 ("apex-200-350w", "bluetti-apex-200-350w-solar-kit", "Apex 200", [], [(1, 350)], None, [], None),
 ("apex-200-500w", "bluetti-apex-200-500w-solar-kit", "Apex 200", [], [(1, 500)], None, [], None),
 ("apex-200-b300k-2-200w", "bluetti-apex-200-b300k-2x200w-solar-kit", "Apex 200", ["B300K"], [(2, 200)], None, [], None),
 ("apex-200-b500k-2-500w", "bluetti-apex-200-b500k-2x500w-solar-kit", "Apex 200", ["B500K"], [(2, 500)], None, [], None),
 ("apex-300-350w", "bluetti-apex-300-350w-solar-kit", "Apex 300", [], [(1, 350)], None, [], None),
 ("apex-300-500w", "bluetti-apex-300-500w-solar-kit", "Apex 300", [], [(1, 500)], None, [], None),
 ("apex-300-2-200w", "bluetti-apex-300-2x200w-solar-kit", "Apex 300", [], [(2, 200)], None, [], None),
 ("apex-300-3-200w", "bluetti-apex-300-3x200w-solar-kit", "Apex 300", [], [(3, 200)], None, [], None),
 ("apex-300-2-350w", "bluetti-apex-300-2x350w-solar-kit", "Apex 300", [], [(2, 350)], None, [], None),
 ("apex-300-2-500w", "bluetti-apex-300-2x500w-solar-kit", "Apex 300", [], [(2, 500)], None, [], None),
 ("apex-300-b300k-2-200w-1", "bluetti-apex-300-b300k-2x200w-solar-kit", "Apex 300", ["B300K"], [(2, 200)], None, [], None),
 ("apex-300-b300k-2-200w", "bluetti-apex-300-b300k-2x350w-solar-kit", "Apex 300", ["B300K"], [(2, 350)], None,
  ["The store address of this listing ends in \"b300k-2-200w\", but its title, variant and price are for the two 350 W panels."], None),
 ("apex-300-b300k-500w", "bluetti-apex-300-b300k-500w-solar-kit", "Apex 300", ["B300K"], [(1, 500)], None, [], None),
 ("apex-300-b500k-350w", "bluetti-apex-300-b500k-500w-solar-kit", "Apex 300", ["B500K"], [(1, 500)], None,
  ["The store address of this listing ends in \"b500k-350w\", but its title, variant and price are for the 500 W panel."], None),
 ("apex-300-2-b300k-2-200w", "bluetti-apex-300-2-b300k-2x200w-solar-kit", "Apex 300", ["B300K", "B300K"], [(2, 200)], None, [], None),
 ("bluetti-elite-30-mini-60w", "bluetti-elite-30-mini-60w-solar-kit", "Elite 30 mini", [], [(1, 60)], None,
  ["BLUETTI's Elite 10 page says its 60 W panel ships from December 25; this kit's page carried no dispatch note on 2026-11-17, so check the delivery estimate at checkout."], None),
 ("bluetti-elite-30-mini-100w", "bluetti-elite-30-mini-100w-solar-kit", "Elite 30 mini", [], [(1, 100)], None, [], None),
 ("elite-10-sp100l-pv", "bluetti-elite-10-100w-solar-kit", "Elite 10", [], [(1, 100)], None,
  ["BLUETTI sold the Elite 30 mini with a 60 W panel for $339.99 the same day: $28.01 less, with 288 Wh instead of 128 Wh.",
   "The same page sells the Elite 10 with a 60 W panel at $239."],
  ("bluetti-elite-30-mini-60w-solar-kit", "For $28.01 less, BLUETTI's Elite 30 mini + 60 W kit has more than twice the battery (288 Wh) and a 300 W outlet.")),
 ("elite-100-mini-100w", "bluetti-elite-100-mini-100w-solar-kit", "Elite 100 mini", [], [(1, 100)], None, [], None),
 ("elite-100-mini-200w-1", "bluetti-elite-100-mini-200w-solar-kit", "Elite 100 mini", [], [(1, 200)], None, [], None),
 ("elite-100-mini-200w", "bluetti-elite-100-mini-350w-solar-kit", "Elite 100 mini", [], [(1, 350)], None,
  ["The store address of this listing ends in \"200w\", but its title, variant and price are for the 350 W panel."], None),
 ("elite-100-v2-100w", "bluetti-elite-100-v2-100w-solar-kit", "Elite 100 V2", [], [(1, 100)], None, [], None),
 ("elite-100-v2-200w-solar", "bluetti-elite-100-v2-200w-solar-kit", "Elite 100 V2", [], [(1, 200)], None, [], None),
 ("elite-100-v2-350w-solar", "bluetti-elite-100-v2-350w-solar-kit", "Elite 100 V2", [], [(1, 350)], None, [], None),
 ("elite-200-v2-pv350", "bluetti-elite-200-v2-350w-solar-kit", "Elite 200 V2", [], [(1, 350)], None, [], None),
 ("elite-200-v2-2-pv350d", "bluetti-elite-200-v2-2x350w-solar-kit", "Elite 200 V2", [], [(2, 350)], None, [], None),
 ("elite-300-2-200w", "bluetti-elite-300-2x200w-solar-kit", "Elite 300", [], [(2, 200)], None, [], None),
 ("elite-300-350w", "bluetti-elite-300-350w-solar-kit", "Elite 300", [], [(1, 350)], None, [], None),
 ("elite-300-500w", "bluetti-elite-300-500w-solar-kit", "Elite 300", [], [(1, 500)], None, [], None),
 ("elite-400-350w", "bluetti-elite-400-350w-solar-kit", "Elite 400", [], [(1, 350)], None, [], None),
 ("elite-400-500w", "bluetti-elite-400-500w-solar-kit", "Elite 400", [], [(1, 500)], None, [], None),
 ("elite-400-2-200w", "bluetti-elite-400-2x200w-solar-kit", "Elite 400", [], [(2, 200)], None, [], None),
 ("elite-400-2-350w", "bluetti-elite-400-2x350w-solar-kit", "Elite 400", [], [(2, 350)], None, [], None),
 ("pioneer-na-200w", "bluetti-pioneer-na-200w-solar-kit", "Pioneer Na", [], [(1, 200)], None, [], None),
 ("pioneer-na-2-200w", "bluetti-pioneer-na-2x200w-solar-kit", "Pioneer Na", [], [(2, 200)], None, [], None),
 ("pioneer-na-350w", "bluetti-pioneer-na-350w-solar-kit", "Pioneer Na", [], [(1, 350)], None, [], None),
]
RV = [("rv5-b4810-epanel-epad-200w", "bluetti-5kwh-rv-kit-2x100w", 2), ("rv5-b4810-epanel-epad-2-200w", "bluetti-5kwh-rv-kit-4x100w", 4)]


def money(x):
    return f"${x:,.2f}".replace(".00", "")


def num(x):
    return f"{x:,.1f}".replace(".0", "")


def hours(wh, watts):
    h = wh / (watts * 0.75)
    days = h / 5
    span = ("under a sunny day" if days < 0.9 else "about one sunny day" if days < 1.3 else f"about {days:.0f} sunny days" if days >= 1.75 else "one to two sunny days")
    return f"About {h:.0f} hours of good sun, {span} (our estimate, at 75% of the panels' rating)" if h >= 10 else \
           f"About {h:.1f} hours of good sun, {span} (our estimate, at 75% of the panels' rating)".replace(".0 hours", " hours")


def fitnote(st, panels, exps):
    """What the stated voltages and currents say about plugging these panels into this station."""
    (n, w), s = panels[0], ST[st]
    tot = n * w
    out = []
    if st in ("Elite 30 mini", "Elite 10"):
        if w == 100:
            out.append(f"A 100 W panel is the most this station's solar input accepts ({s['solar'].split(' (')[0]}), so a bigger panel would not charge it faster.")
        else:
            out.append("The 60 W panel's 27.5 V open-circuit voltage sits just under the station's 28 V solar limit.")
    elif st == "Elite 100 mini":
        out.append("The 350 W panel is the most the station's solar input accepts." if w == 350 else f"The {w} W panel uses {'under a third' if w == 100 else 'over half'} of the station's 350 W solar input.")
    elif st == "Pioneer Na":
        if n == 2:
            out.append("The two 200 W panels go in series (49.2 V open-circuit, inside the 60 V limit); in parallel the pair would exceed the 10 A input limit.")
        elif w == 350:
            out.append("The 350 W panel's spec table gives 11.4 A short-circuit against the Pioneer Na's 10 A solar limit, so expect a little under 350 W at peak.")
        else:
            out.append("One 200 W panel uses under half of the station's 500 W solar input.")
    elif st == "Apex 200":
        if (n, w) == (2, 500):
            out.append("Two SORA 500 panels in series give 98.2 V open-circuit, which fits the Apex 200's 60–280 V MC4 solar port; in parallel their 26.6 A of short-circuit current would exceed the XT60 port's 25 A.")
        elif n == 2:
            out.append("Two 200 W panels in series are 49.2 V open-circuit, inside the XT60 port's 12–60 V range; that port takes up to 1,000 W.")
        else:
            out.append(f"One {w} W panel goes into the 1,000 W XT60 port (12–60 V); the 2,000 W MC4 port needs a string of 60 V or more.")
    elif st == "Apex 300":
        if (n, w) == (3, 200):
            out.append("Three 200 W panels fit as two in series on one port (49.2 V open-circuit) and one on the other; three in series would be 73.8 V, over the 60 V limit.")
        elif n == 2 and w == 200:
            out.append("Two 200 W panels go one per port, or in series on one port (49.2 V open-circuit, inside the 60 V limit).")
        elif n == 2:
            v = {350: "88 V", 500: "98.2 V"}[w]
            out.append(f"The two {w} W panels go one per solar port; in series they would be {v} open-circuit, over each port's 60 V limit.")
        else:
            out.append(f"One {w} W panel uses one of the two 1,200 W solar ports, so there is room to add a second panel later.")
    else:  # Elite 100 V2, 200 V2, 300, 400
        if n == 2 and w == 350:
            out.append(f"Two 350 W panels in series would be 88 V open-circuit (2 × 44 V, BLUETTI's panel spec table), over the station's 60 V solar limit, so they have to be wired in parallel; we did not find a parallel connector in the kit's listing.")
        elif n == 2:
            out.append("Two 200 W panels in series are 49.2 V open-circuit, inside the station's 60 V solar limit.")
        elif w == 500:
            out.append(f"The SORA 500's 49.1 V and 13.31 A fit the station's solar input ({s['solar']}).")
        else:
            frac = tot / s["cap"]
            out.append(f"One {w} W panel uses {'a tenth' if frac <= 0.11 else 'a fifth' if frac <= 0.21 else 'about a third' if frac <= 0.36 else 'under half'} of the station's {s['cap']:,} W solar input, so panels can be added later.")
    return out


def record(src, handle, slug, st, exps, panels, tail, extra_cav, instead):
    j = json.load(open(Path(src) / f"{handle}.json"))
    v = next(x for x in j["variants"] if x["available"])
    price, cmp_ = v["price"] / 100, (v["compare_at_price"] or 0) / 100
    s = ST[st]
    (n, w) = panels[0]
    tot = n * w
    wh = s["wh"] + sum(EXP[e] for e in exps)
    exp_txt = "".join(f" + {('2× ' if exps.count(e) == 2 else '')}{e}" for e in dict.fromkeys(exps))
    pan_txt = f"{'' if n == 1 else f'{n}× '}{w} W"
    base = st + exp_txt
    # the parts bought separately: the no-panel bundle where BLUETTI sells one, else the single items
    base_key = f"{st} + {exps[0]}" if len(exps) == 1 else None
    if base_key in PART:
        base_cost, base_desc = PART[base_key], f"the {base_key} bundle ({money(PART[base_key])})"
    else:
        base_cost = PART[st] + sum(PART[e] for e in exps)
        base_desc = f"the {st} ({money(PART[st])})" + "".join(f", {'two' if exps.count(e) == 2 else 'a'} {e} ({money(PART[e])} each)" for e in dict.fromkeys(exps))
    parts = base_cost + n * PANEL[w][0]
    pdesc = f"{'a' if n == 1 else {2: 'two', 3: 'three'}[n]} {w} W panel{'s' if n > 1 else ''} ({money(PANEL[w][0])}{' each' if n > 1 else ''})"
    diff = round(parts - price, 2)
    if diff > 0.5:
        cmp_line = f"Bought separately at BLUETTI's US store on {DAY}, {base_desc} and {pdesc} came to {money(parts)}; this kit saves {money(diff)}."
        verdict = f"{money(diff)} less than the parts bought separately"
    elif diff < -0.5:
        cmp_line = f"Bought separately at BLUETTI's US store on {DAY}, {base_desc} and {pdesc} came to {money(parts)}, {money(-diff)} less than this kit."
        verdict = f"{money(-diff)} more than the parts bought separately that day"
    else:
        cmp_line = f"The kit price equals {base_desc} plus {pdesc} bought separately at BLUETTI's US store on {DAY}."
        verdict = "the same price as the parts bought separately"
    pre = s["pre"]
    ship = [s["prenote"]] if s["prenote"] else []
    if w == 350:
        ship.append("BLUETTI's pages say the 350 W solar panel ships from December 25 (read 2026-11-17).")
        pre = pre if pre and "January" in pre else "Dec 25, 2026"
    if w == 200:
        ship.append("BLUETTI's pages say the 200 W solar panel ships from November 18 (read 2026-11-17).")
    eff = min(tot, s["cap"])
    d = {"slug": slug, "brand": "BLUETTI", "program": "awin:bluetti_us", "asin": None, "category": "solar-kit"}
    if instead:
        d["instead"] = instead
    d["name"] = f"BLUETTI {base} + {pan_txt} Solar Panel Kit ({num(wh)} Wh, {s['w']}{f', {tot:,} W of panels' if n > 1 else ''})"
    d["model"] = f"{base} + {pan_txt} panel{'s' if n > 1 else ''}"
    d["url"] = B + handle
    d["price"] = price
    if cmp_ > price:
        d["list_price"] = cmp_
    if pre:
        d["preorder"] = pre
    d["cart_variant"] = v["id"]
    d["verified"] = DAY
    battery = s["battery"] if not exps else f"{num(wh)} Wh LiFePO4 ({st} {num(s['wh'])} Wh" + "".join(f" + {'two ' if exps.count(e) == 2 else ''}{e} {num(EXP[e])} Wh{' each' if exps.count(e) == 2 else ''}" for e in dict.fromkeys(exps)) + ")"
    d["specs"] = [("Battery", battery), ("AC output", s["ac"]),
                  ("Panels" if n > 1 else "Panel", f"{n}× BLUETTI {PANEL[w][1]}"),
                  ("Solar input", s["solar"]), ("Solar recharge with this kit", hours(wh, eff))] + s["extra"]
    d["warranty"] = f"{s['war']}; {PANEL_WAR}"
    d["returns"] = RET
    d["summary"] = (f"{s['what']}{' with ' + ' and '.join(dict.fromkeys(('two B300K expansion batteries' if exps.count(e) == 2 else f'a {e} expansion battery') for e in exps)) if exps else ''} "
                    f"and {pdesc.split(' (')[0]} in one cart: {num(wh)} Wh for {money(price)} at BLUETTI's US store on {DAY}, {verdict}"
                    f"{', as a pre-order' if pre else ''}.")
    h = wh / (eff * 0.75)
    pw = "panels" if n > 1 else "panel"
    d["fit"] = s["fit"] + (f". The {pw} {'are' if n > 1 else 'is'} a top-up, not a daily refill, for a battery this size." if h > 12
                           else f". The {pw} can refill the battery in one good day of sun." if h <= 6
                           else f". The {pw} can refill the battery in a day or two of good sun.")
    d["caveats"] = ship + [cmp_line] + fitnote(st, panels, exps) + s["cav"] + extra_cav + [SEP]
    return d


def rv_record(src, handle, slug, n):
    j = json.load(open(Path(src) / f"{handle}.json"))
    v = next(x for x in j["variants"] if x["available"])
    price, cmp_ = v["price"] / 100, (v["compare_at_price"] or 0) / 100
    parts = PART["5kWh RV Kit"] + n * PANEL["fx"][0]
    d = {"slug": slug, "brand": "BLUETTI", "program": "awin:bluetti_us", "asin": None, "category": "solar-kit",
         "name": f"BLUETTI 5kWh RV Kit + {n} × 100W (RV5 Power Hub, B4810 51.2 V 100 Ah battery, Epanel, Epad, {n} × 100 W panels)",
         "model": f"RV5+B4810+Epanel+Epad+{n} × 100W", "url": B + handle, "price": price}
    if cmp_ > price:
        d["list_price"] = cmp_
    d["cart_variant"] = v["id"]
    d["verified"] = DAY
    d["specs"] = [("AC output", "5,000 W continuous, 10,000 W surge"), ("DC output", "1,620 W; regulated 12 V at 100 A (BLUETTI blog)"),
                  ("Battery", "B4810 LiFePO4, 51.2 V 100 Ah = 5,120 Wh, self-heating, charges down to -4 °F"),
                  ("Solar input", "50 V Voc limit, so panels go in parallel only (BLUETTI blog)"), ("Panels", f"{n} × 100 W ({n * 100} W)"),
                  ("Solar recharge with this kit", hours(5120, n * 100)),
                  ("Alternator charging", "PV2 doubles as the alternator input, up to 1,200 W"), ("Shore charging", "80% in 50 minutes (BLUETTI)")]
    d["warranty"] = f"5 years on the RV5 and B4810 (BLUETTI's product warranty period page); {PANEL_WAR}"
    d["returns"] = RET
    d["summary"] = (f"BLUETTI's 48 V RV system (RV5 hub, 5.12 kWh B4810 battery, Epanel and Epad) with {n * 100} W of panels in one cart: "
                    f"{money(price)} at BLUETTI's US store on {DAY}, {money(parts - price)} less than the 5kWh RV Kit ({money(PART['5kWh RV Kit'])}) plus {n} PV100 FX panels ({money(PANEL['fx'][0])} each) bought separately.")
    d["fit"] = ("RV owners who want the coach's own outlets, lights, pump and fans on a lithium system and mostly charge from shore power or the alternator, with the panels as a top-up."
                if n == 2 else "Boondockers who want the coach's own outlets, lights, pump and fans running from a lithium system that the roof can partly refill each day.")
    d["caveats"] = [f"{n * 100} W of panels adds about {n * 100 * 0.75 * 5 / 1000:.2f} kWh on a good day (5 sun hours at 75% of rating), against a 5.12 kWh battery; BLUETTI sells the same kit with six panels at $4,599.".replace("0 kWh", " kWh").replace(". kWh", " kWh"),
                    "The 12 V output is 100 A. BLUETTI says leveling systems that draw more than 100 A at startup need a B1210 or the coach's existing 12 V lead-acid battery, and neither is in the box.",
                    "Panels must be wired in parallel (PV100 FX 41.4 V open-circuit against the 50 V limit).",
                    "The kit page does not name the 100 W panel model, so PV100 FX figures are inferred from it being BLUETTI's RV panel.",
                    "Installation means wiring into the coach's 120 V and 12 V panels; this is not a plug-in power station."]
    return d


def literal(d):
    lines = [f' "{k}": {v!r},' for k, v in d.items() if not k.startswith("_")]
    return "{" + "\n".join(lines)[1:].rstrip(",") + "},\n"


def build(src):
    return [record(src, *k) for k in K] + [rv_record(src, *r) for r in RV]


if __name__ == "__main__":
    src, dest = sys.argv[1], sys.argv[2]
    R = build(src)
    if dest == "--print":
        for d in R:
            print(json.dumps(d, ensure_ascii=False, indent=1))
        sys.exit()
    s = open(dest).read()
    assert "bluetti-apex-200-200w-solar-kit" not in s, "already inserted"
    anchor = "{\"slug\": 'bluetti-elite-200-v2-charger-1-bundle',"
    assert s.count(anchor) == 1
    block = ("# BLUETTI kits added 2026-11-17 (DLC-293 step 2): store read that day, see growth/focus/offers/bluetti_kits_1117.py\n"
             + "\n".join(literal(d) for d in R) + "\n")
    open(dest, "w").write(s.replace(anchor, block + anchor))
    print("inserted", len(R), "records")
