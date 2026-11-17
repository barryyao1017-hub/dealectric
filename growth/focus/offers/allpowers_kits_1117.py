#!/usr/bin/env python3.12
"""The 12 ALLPOWERS solar generator kits added 2026-11-17 (DLC-293): product records composed from ALLPOWERS' US store
pages read that day in the Agent Chrome (data/stores/pages/*.txt: prices, variants, pre-order dispatch dates, spec
tables), today's store price list (data/stores/iallpowers.com.p1.json) and our existing station and panel records.

    python3.12 growth/focus/offers/allpowers_kits_1117.py <path to src/products.py>     # inserts the records once
"""
import sys
B = "https://iallpowers.com/products/"
RET = "30-day money-back for unused items in the original package; buyer pays return shipping unless defective (ALLPOWERS' refund page also says sale items can't be returned)"
SEP = "ALLPOWERS ships the station and the panel as separate parcels (note on the kit page)."
def late(d): return f"The page still labels this a pre-order with dispatch \"from {d}\", a date already past on 2026-11-17, so check the delivery estimate at checkout."

ST = {  # station facts: (battery, ac, solar, extra spec rows, warranty)
 "R3500": (("Battery", "3,168 Wh LiFePO4, over 3,500 cycles"),
           ("AC output", "3,200 W pure sine wave; 7,000 W peak in ALLPOWERS' feature list, 6,000 W surge in its spec table"),
           ("Solar input", "2,000 W max, 12–150 V, 40 A (XT60)"),
           [("AC input", "1,500 W max"), ("Expansion", "B3000 expansion battery")],
           "5-year limited warranty on the R3500 (ALLPOWERS' warranty policy lists it in the 5-year tier and says some products must be registered on iallpowers.com to get more than the default 24 months)"),
 "S2000": (("Battery", "1,500 Wh ternary lithium (NMC), not LiFePO4; 2,500+ cycles to 80% (ALLPOWERS)"),
           ("AC output", "2,000 W (4,000 W surge), 4 outlets"),
           ("Solar input", "500 W, 12–70 V, 18 A"),
           [("AC input", "400 W from the wall; ALLPOWERS gives 0–100% in 1.6 h with wall and solar together"), ("USB", "2× USB-C 100 W, 4× USB-A")],
           "The kit page shows a 5-year warranty badge. ALLPOWERS' warranty policy gives 24 months by default and 5 years to named models, some only after registration at iallpowers.com; we have not confirmed which applies to the S2000"),
 "R2500 V2": (("Battery", "1,920 Wh LiFePO4, 3,500+ cycles"),
              ("AC output", "2,500 W (4,000 W surge in the spec table)"),
              ("Solar input", "1,000 W, 12–150 V, 20 A"),
              [("AC input", "1,500 W max"), ("Weight", "Station 29 kg (63.9 lb); panel extra")],
              "Station 5 years per ALLPOWERS' product page"),
 "S2000 Pro": (("Battery", "1,451 Wh, ternary lithium (NMC), not LiFePO4"),
               ("AC output", "2,400 W (4,000 W surge); rated 2,000 W once the battery is below about 60% (ALLPOWERS told one reviewer 70%)"),
               ("Solar input", "1,000 W, 12–150 V, 13 A on current units"),
               [("AC input", "1,500 W"), ("Weight", "Station 13 kg; panel extra")],
               "Station 5 years if registered at iallpowers.com (24 months otherwise)"),
 "R1500": (("Battery", "1,152 Wh LiFePO4, 3,500+ cycles (ALLPOWERS)"),
           ("AC output", "1,800 W (3,000 W surge), 4 outlets"),
           ("Solar input", "650 W max, 12–60 V, 13 A"),
           [("AC input", "1,500 W max; 0–80% in 45 minutes (ALLPOWERS)"), ("UPS", "15 ms"), ("Weight", "Station 36.8 lb (16.7 kg) in ALLPOWERS' comparison table; panel extra")],
           "The kit page shows a 5-year warranty badge. ALLPOWERS' warranty policy gives 24 months by default and 5 years to named models, some only after registration at iallpowers.com; we have not confirmed which applies to the R1500"),
}
PN = {  # panel facts: (spec text, warranty text)
 "SP039": ("1× SP039 600 W folding (44 V, 27.5 lb folded, IP67; MC4 to XT60 cable included)", "SP039 panel 24 months (ALLPOWERS' panel page)"),
 "SP037": ("1× SP037 400 W folding", "SP037 2 years"),
 "SF200": ("1× SF200 200 W flexible monocrystalline (ETFE, IP68)", "panel warranty not stated on the kit page"),
 "SF100": ("1× SF100 100 W flexible monocrystalline (ETFE, IP68, 5.29 lb)", "panel warranty not stated on the kit page"),
 "SE200": ("1× SE200 200 W laminated folding panel (ETFE, IP68, built-in stand)", "panel warranty not stated on the kit page"),
 "SE100": ("1× SE100 100 W laminated folding panel (ETFE, IP68, built-in stand)", "panel warranty not stated on the kit page"),
}

def rec(slug, st, pn, watts, handle, variant, price, lst, pre, recharge, summary, fit, caveats, instead=None, wh=None, w=None, multi=True):
    b, ac, sol, extra, war = ST[st]
    d = {"slug": slug, "brand": "ALLPOWERS", "program": "cj:allpowers", "asin": None, "category": "solar-kit"}
    if instead: d["instead"] = instead
    d["name"] = f"ALLPOWERS {st} + {pn} {watts} W Solar Generator Kit ({wh}, {w})"
    d["model"] = f"{st} + 1× {pn}"
    d["url"] = B + handle + (f"?variant={variant}" if multi else "")
    d["price"] = price; d["list_price"] = lst
    if pre: d["preorder"] = pre
    d["verified"] = "2026-11-17"
    d["specs"] = [b, ac, ("Panel", PN[pn][0]), sol, ("Solar recharge with this kit", recharge)] + extra
    d["warranty"] = f"{war}; {PN[pn][1]}"
    d["returns"] = RET; d["summary"] = summary; d["fit"] = fit; d["caveats"] = caveats + [SEP]
    d["_variant"] = variant
    return d

R = [
 rec("allpowers-r3500-sp039-solar-kit", "R3500", "SP039", 600, "allpowers-r3500-solar-generator-power-station-3200w-3168wh-with-sp039-600w-solar-panel", 43451064287385, 1993.1, 2899.0, None,
     "About 7 hours of good sun with one SP039 (our estimate, at 75% of the panel's rating)",
     "ALLPOWERS' 3.2 kWh LiFePO4 home-backup station with its largest folding panel, 600 W, in one listing that was shipping, not on pre-order, on 2026-11-17.",
     "Home backup where the battery should refill in about a day of sun, and the buyer wants the pair in one order.",
     ["On 2026-11-17 the same store sold the R3500 alone at $1,199 and the SP039 alone at $599: $1,798 as two items, $195.10 less than this kit.",
      "One 600 W panel uses under a third of the R3500's 2,000 W solar input; ALLPOWERS sells a two-panel version of this kit at $2,562.15.",
      "ALLPOWERS gives the peak as 7,000 W in its feature list and 6,000 W in its spec table.", "No named lab-style discharge test of the R3500 has been published."],
     wh="3,168 Wh", w="3,200 W"),
 rec("allpowers-r3500-sf200-solar-kit", "R3500", "SF200", 200, "allpowers-r3500-solar-generator-power-station-3200w-3168wh-with-sf200-200w-flexible-solar-panel", 43450954350745, 1331.0, 2299.0, "Nov 9, 2026",
     "About 21 hours of good sun with one SF200, roughly four sunny days (our estimate, at 75% of the panel's rating)",
     "The 3.2 kWh R3500 with one 200 W flexible panel for $132 more than the station alone: a large battery with a panel that tops it up slowly.",
     "Buyers who mostly charge from the wall and want a light panel to stretch an outage, or to mount flat on an RV or shed roof.",
     [late("Nov 9, 2026"), "A 200 W panel is a tenth of the R3500's 2,000 W solar input, so a full refill from the sun takes about four sunny days.",
      "The SF200 is a flexible panel with no stand; it is made to be strapped or fixed to a surface.", "ALLPOWERS gives the peak as 7,000 W in its feature list and 6,000 W in its spec table."],
     wh="3,168 Wh", w="3,200 W"),
 rec("allpowers-r3500-sf100-solar-kit", "R3500", "SF100", 100, "allpowers-r3500-solar-generator-power-station-3200w-3168wh-with-sf100-100w-flexible-solar-panel", 43450923778201, 1298.99, 2199.0, "Nov 9, 2026",
     "About 42 hours of good sun with one SF100, more than a week of sunny days (our estimate, at 75% of the panel's rating)",
     "The 3.2 kWh R3500 with one 100 W flexible panel, priced at exactly the station ($1,199) plus the panel ($99.99) bought separately.",
     "Buyers who want the R3500 and a small flexible panel in one order; the panel keeps phones and lights going but will not refill this battery in an outage.",
     [late("Nov 9, 2026"), "A 100 W panel adds about 375 Wh on a good day, under an eighth of the battery.",
      "For $32.01 more, the same station comes with the 200 W SF200.", "The SF100 is a flexible panel with no stand."],
     instead=("allpowers-r3500-sf200-solar-kit", "For $32.01 more, ALLPOWERS sells the same R3500 with the 200 W SF200 panel, which refills the battery twice as fast."),
     wh="3,168 Wh", w="3,200 W"),
 rec("allpowers-r2500-v2-sp039-solar-kit", "R2500 V2", "SP039", 600, "allpowers-r2500-v2-600w-solar-panel-2500w-solar-generator-kit", 48908323750041, 1228.05, 2199.0, "Dec 11, 2026",
     "About 4–5 hours of good sun with the 600 W panel (our estimate, at 75% of the panel's rating)",
     "The 1.92 kWh LiFePO4 R2500 V2 with a 600 W folding panel, enough to refill the battery in one good day of sun, as a pre-order.",
     "Home backup, a cabin or a van where the station stays put and has to be refilled from the sun each day.",
     ["Pre-order: ALLPOWERS dispatches from Dec 11, 2026 (checked 2026-11-17).",
      "The listing says \"600W Solar Panel\" without a model; its SKU is ALLPOWERS' SP039, whose own page gives 44 V and 27.5 lb folded.",
      "Bought as two items on 2026-11-17, the station ($649) and the SP039 ($599) came to $1,248, so the kit saves $19.95.", "Station weighs 29 kg (63.9 lb) with no wheels."],
     wh="1,920 Wh", w="2,500 W", multi=False),
 rec("allpowers-r2500-v2-se200-solar-kit", "R2500 V2", "SE200", 200, "allpowers-r2500-v2-200w-solar-panel-2500w-solar-generator-kit", 48908282298521, 838.55, 1799.0, "Dec 11, 2026",
     "About 13 hours of good sun with one SE200, two to three sunny days (our estimate, at 75% of the panel's rating)",
     "The 1.92 kWh LiFePO4 R2500 V2 with one 200 W laminated folding panel, as a pre-order.",
     "Buyers who want a 2 kWh LiFePO4 station under $850 with a panel that stands on its own for camping or a patio.",
     ["Pre-order: ALLPOWERS dispatches from Dec 11, 2026 (checked 2026-11-17).",
      "Bought as two items on 2026-11-17, the station ($649) and the SE200 ($179.55) came to $828.55, $10 less than this kit.",
      "The same listing sells the kit with the flexible SF200 instead at $848.05.", "One 200 W panel uses a fifth of the station's 1,000 W solar input.", "Station weighs 29 kg (63.9 lb) with no wheels."],
     wh="1,920 Wh", w="2,500 W"),
 rec("allpowers-r2500-v2-se100-solar-kit", "R2500 V2", "SE100", 100, "allpower-r2500-plus-100w-solar-panel-2500w-solar-generator-kit-%E5%89%AF%E6%9C%AC", 48908029821081, 743.55, 1699.0, "Dec 11, 2026",
     "About 26 hours of good sun with one SE100, around five sunny days (our estimate, at 75% of the panel's rating)",
     "The cheapest way ALLPOWERS sells the 1.92 kWh R2500 V2 with a panel: one 100 W laminated folding panel, as a pre-order.",
     "Buyers who charge mostly from the wall and want a small panel for phones, lights and slow top-ups.",
     ["Pre-order: ALLPOWERS dispatches from Dec 11, 2026 (checked 2026-11-17).",
      "Bought as two items on 2026-11-17, the station ($649) and the SE100 ($84.55) came to $733.55, $10 less than this kit.",
      "A 100 W panel adds about 375 Wh on a good day, a fifth of the battery.", "Station weighs 29 kg (63.9 lb) with no wheels."],
     instead=("allpowers-r2500-v2-se200-solar-kit", "For $95 more, ALLPOWERS sells the same R2500 V2 with the 200 W SE200 panel, which refills the battery twice as fast."),
     wh="1,920 Wh", w="2,500 W"),
 rec("allpowers-s2000-pro-sf200-solar-kit", "S2000 Pro", "SF200", 200, "allpowers-s2000-pro-solar-generator-portable-power-station-2400w-1500wh-with-sf200-200w-flexible-solar-panel", 43450329661593, 681.0, 1499.0, "Nov 19, 2026",
     "About 10 hours of good sun with one SF200, about two sunny days (our estimate, at 75% of the panel's rating)",
     "The 2,400 W, 1.45 kWh S2000 Pro with a 200 W flexible panel for $16.95 more than the station alone ($664.05 on 2026-11-17), as a pre-order.",
     "Buyers who need a 2,400 W inverter for tools, a microwave or a well pump and want a panel thrown in for almost nothing.",
     ["Pre-order: ALLPOWERS dispatches from Nov 19, 2026 (checked 2026-11-17).", "NMC chemistry: about 2,500 cycles, fewer than LiFePO4.",
      "ALLPOWERS sells the same station and panel on a second listing at $853.10; this listing is the cheaper one.",
      "The SF200 is a flexible panel with no stand; it is made to be strapped or fixed to a surface.",
      "Usable capacity tested at about 1,250–1,380 Wh on 2026 units (reviewers)."],
     wh="1,451 Wh", w="2,400 W"),
 rec("allpowers-s2000-pro-se200-solar-kit", "S2000 Pro", "SE200", 200, "s2000-pro-200w-solar-panel", 46377149989017, 843.6, 1499.0, None,
     "About 10 hours of good sun with one SE200, about two sunny days (our estimate, at 75% of the panel's rating)",
     "The 2,400 W S2000 Pro with a 200 W laminated folding panel that has its own stand, shipping rather than on pre-order on 2026-11-17, at exactly the price of the two bought separately.",
     "Buyers who need the kit now and want a panel that stands on the ground at a campsite.",
     ["The kit price equals the station ($664.05) plus the SE200 ($179.55) bought separately on 2026-11-17.", "NMC chemistry: about 2,500 cycles, fewer than LiFePO4.",
      "The same station with the flexible SF200 panel costs $162.60 less on another ALLPOWERS listing, as a pre-order."],
     instead=("allpowers-s2000-pro-sf200-solar-kit", "If you can wait for a pre-order, ALLPOWERS sells the same S2000 Pro with its 200 W flexible SF200 panel for $681, $162.60 less; that panel has no stand."),
     wh="1,451 Wh", w="2,400 W"),
 rec("allpowers-s2000-pro-se100-solar-kit", "S2000 Pro", "SE100", 100, "s2000-pro-100w-solar-panel", 43450328678553, 748.6, 1399.0, None,
     "About 19 hours of good sun with one SE100, about four sunny days (our estimate, at 75% of the panel's rating)",
     "The 2,400 W S2000 Pro with a 100 W laminated folding panel, shipping rather than on pre-order on 2026-11-17, at exactly the price of the two bought separately.",
     "Buyers who need the kit now and only want a small panel for top-ups.",
     ["The kit price equals the station ($664.05) plus the SE100 ($84.55) bought separately on 2026-11-17.", "NMC chemistry: about 2,500 cycles, fewer than LiFePO4.",
      "A 100 W panel adds about 375 Wh on a good day, a quarter of the battery."],
     instead=("allpowers-s2000-pro-sf200-solar-kit", "If you can wait for a pre-order, ALLPOWERS sells the same S2000 Pro with a 200 W flexible panel for $681: twice the panel for $67.60 less."),
     wh="1,451 Wh", w="2,400 W"),
 rec("allpowers-s2000-sf200-solar-kit", "S2000", "SF200", 200, "allpowers-s2000-solar-generator-portable-power-station-2000w-1500wh-with-sf200-200w-flexible-solar-panel", 43450317176985, 681.0, 1499.0, "Nov 20, 2026",
     "About 10 hours of good sun with one SF200, about two sunny days (our estimate, at 75% of the panel's rating)",
     "ALLPOWERS' older 1.5 kWh S2000 with a 200 W flexible panel, at the same $681 as the newer S2000 Pro with the same panel.",
     "Buyers who specifically want the S2000; at this price the S2000 Pro kit is the stronger buy.",
     ["Pre-order: ALLPOWERS dispatches from Nov 20, 2026 (checked 2026-11-17).", "Wall charging is 400 W, against 1,500 W on the S2000 Pro.",
      "Solar input is 500 W at 12–70 V, half the S2000 Pro's.", "NMC chemistry: 2,500+ cycles to 80%, fewer than LiFePO4."],
     instead=("allpowers-s2000-pro-sf200-solar-kit", "For the same $681, ALLPOWERS' S2000 Pro kit has the same panel, a 2,400 W inverter instead of 2,000 W, 1,500 W wall charging instead of 400 W and twice the solar input, with 49 Wh less battery."),
     wh="1,500 Wh", w="2,000 W"),
 rec("allpowers-s2000-sp037-solar-kit", "S2000", "SP037", 400, "allpowers-s2000-solar-generator-portable-power-station-2000w-1500wh-with-sp037-400w-solar-panel", 43391394742425, 1043.1, 1999.0, "Nov 20, 2026",
     "About 5 hours of good sun with one SP037 (our estimate, at 75% of the panel's rating)",
     "ALLPOWERS' older 1.5 kWh S2000 with the 400 W SP037 folding panel, at the same $1,043.10 as the newer S2000 Pro with the same panel.",
     "Buyers who specifically want the S2000; at this price the S2000 Pro kit is the stronger buy.",
     ["Pre-order: ALLPOWERS dispatches from Nov 20, 2026 (checked 2026-11-17).", "Wall charging is 400 W, against 1,500 W on the S2000 Pro.",
      "One SP037 nearly fills the 500 W solar input, so there is no room for a second panel.", "NMC chemistry: 2,500+ cycles to 80%, fewer than LiFePO4."],
     instead=("allpowers-s2000-pro-sp037-solar-kit", "For the same $1,043.10, ALLPOWERS' S2000 Pro kit has the same panel, a 2,400 W inverter instead of 2,000 W, 1,500 W wall charging instead of 400 W and room for a second panel."),
     wh="1,500 Wh", w="2,000 W", multi=False),
 rec("allpowers-r1500-sf100-solar-kit", "R1500", "SF100", 100, "allpowers-solar-generator-kit-1800w-r1500-sf100-100w-flexible-solar-panel-1", 44309884895385, 548.0, 1028.0, "Oct 30, 2026",
     "About 15 hours of good sun with one SF100, about three sunny days (our estimate, at 75% of the panel's rating)",
     "A 1.15 kWh LiFePO4 station with an 1,800 W inverter and a 100 W flexible panel for $548; ALLPOWERS listed the R1500 on its own at $539 that day, sold out.",
     "Buyers who want a 1 kWh-class LiFePO4 station with fast wall charging and a small panel for under $550.",
     [late("Oct 30, 2026"), "A 100 W panel adds about 375 Wh on a good day, a third of the battery; the station takes up to 650 W of panels.",
      "The SF100 is a flexible panel with no stand.", "The two-, three- and four-panel versions of this kit showed no dispatch date on 2026-11-17."],
     wh="1,152 Wh", w="1,800 W"),
]

def literal(d):
    lines = []
    for k, v in d.items():
        if k.startswith("_"): continue
        lines.append(f' "{k}": {v!r},')
    return "{" + "\n".join(lines)[1:].rstrip(",") + "},\n"

if __name__ == "__main__":
    path = sys.argv[1]; s = open(path).read()
    assert "allpowers-r3500-sp039-solar-kit" not in s, "already inserted"
    anchor = "{\"slug\": 'bluetti-elite-200-v2-charger-1-bundle',"
    assert s.count(anchor) == 1
    block = "# ALLPOWERS kits added 2026-11-17 (DLC-293, offer table): store pages read that day, see growth/focus/offers/allpowers_kits_1117.py\n" + "\n".join(literal(d) for d in R) + "\n"
    open(path, "w").write(s.replace(anchor, block + anchor))
    print("inserted", len(R), "records")
