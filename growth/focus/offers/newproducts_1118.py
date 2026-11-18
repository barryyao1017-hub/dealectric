#!/usr/bin/env python3.12
"""Store products we did not list, prepared 2026-11-18 (DLC-321): ALLPOWERS kit variants and panels, OSCAL PowerMax 6000
kits and panels. Records are composed from each store's product list (/products.json: price, compare-at price, variant
id), the rendered store pages read that day in a background Agent Chrome tab (pre-order labels and dispatch dates, box
lists, spec tables), OSCAL's own panel pages (oscal.hk/pm400-se, /pm200-se) and the station facts we already carried.
Cart tests: data/cart-tests-2026-11-18-newproducts.jsonl (tools/codecheck_browser.py on each exact variant).

    python3.12 growth/focus/offers/newproducts_1118.py apply [--keep slug,slug,...] [--buy-first slug,...]   # idempotent: products.py, coupons.json, focus.py
    python3.12 growth/focus/offers/newproducts_1118.py print [--keep ...]

`apply` rewrites its own marked blocks, so it can be re-run after a rebase (take main's src files, then apply again).
With --keep only those slugs are written (phase 2: publish the confirmed ones); an `instead` pointer to a slug that is
neither kept nor already in products.py is dropped.
"""
import json, re, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DAY = "2026-11-18"
TESTS = Path(__file__).resolve().parent / "data" / "cart-tests-2026-11-18-newproducts.jsonl"
AP = "https://iallpowers.com/products/"
OS = "https://store.oscal.hk/products/"
RET = "30-day money-back for unused items in the original package; buyer pays return shipping unless defective (ALLPOWERS' refund page also says sale items can't be returned)"
SEP = "ALLPOWERS ships the station and the panels as separate parcels (note on the kit page)."
ORET = "30 days from delivery for unused items in the original packaging with proof of purchase; OSCAL covers return shipping when the item is faulty or damaged (store FAQ, read 2026-11-18)"


def money(x):
    return f"${x:,.2f}".replace(".00", "")


def late(d):
    return (f"The page still labels this a pre-order with dispatch \"from {d}\", a date already past on {DAY}, "
            "so check the delivery estimate at checkout.")


def pre_line(d, who="ALLPOWERS"):
    return f"Pre-order: {who} dispatches from {d} (checked {DAY})."


def hours(wh, watts):
    h = wh / (watts * 0.75)
    days = h / 5
    span = ("under a sunny day" if days < 0.9 else "about one sunny day" if days < 1.3 else "one to two sunny days" if days < 1.75
            else f"about {days:.0f} sunny days")
    hh = f"{h:.0f}" if h >= 10 else f"{h:.1f}".replace(".0", "")
    return f"About {hh} hours of good sun, {span} (our estimate, at 75% of the panels' rating)"


# ---------------------------------------------------------------- ALLPOWERS stations (facts carried from our records)
ST = {
 "R3500": dict(wh=3168, w="3,200 W", whtxt="3,168 Wh", price=1199.0, cap=2000,
    battery="3,168 Wh LiFePO4, over 3,500 cycles",
    ac="3,200 W pure sine wave; 7,000 W peak in ALLPOWERS' feature list, 6,000 W surge in its spec table",
    solar="2,000 W max, 12–150 V, 40 A (XT60)",
    extra=[("AC input", "1,500 W max"), ("Expansion", "B3000 expansion battery")],
    war="5-year limited warranty on the R3500 (ALLPOWERS' warranty policy lists it in the 5-year tier and says some products must be registered on iallpowers.com to get more than the default 24 months)",
    what="ALLPOWERS' 3.2 kWh LiFePO4 home-backup R3500", fit="Home backup for a fridge, freezer and other essentials",
    cav=["ALLPOWERS gives the peak as 7,000 W in its feature list and 6,000 W in its spec table."]),
 "R2500 V2": dict(wh=1920, w="2,500 W", whtxt="1,920 Wh", price=649.0, cap=1000,
    battery="1,920 Wh LiFePO4, 3,500+ cycles",
    ac="2,500 W (4,000 W surge in the spec table)",
    solar="1,000 W, 12–150 V, 20 A",
    extra=[("AC input", "1,500 W max"), ("Weight", "Station 29 kg (63.9 lb); panels extra")],
    war="Station 5 years per ALLPOWERS' product page",
    what="ALLPOWERS' 1.92 kWh LiFePO4 R2500 V2", fit="Home backup, a cabin or a van where the station stays put",
    cav=["Station weighs 29 kg (63.9 lb) with no wheels."]),
 "S2000 Pro": dict(wh=1451, w="2,400 W", whtxt="1,451 Wh", price=664.05, cap=1000,
    battery="1,451 Wh, ternary lithium (NMC), not LiFePO4",
    ac="2,400 W (4,000 W surge); rated 2,000 W once the battery is below about 60% (ALLPOWERS told one reviewer 70%)",
    solar="1,000 W, 12–150 V, 13 A on current units",
    extra=[("AC input", "1,500 W"), ("Weight", "Station 13 kg; panels extra")],
    war="Station 5 years if registered at iallpowers.com (24 months otherwise)",
    what="ALLPOWERS' 2,400 W, 1.45 kWh S2000 Pro", fit="Buyers who need a 2,400 W inverter for tools, a microwave or a well pump",
    cav=["NMC chemistry: about 2,500 cycles, fewer than LiFePO4."]),
 "S2000": dict(wh=1500, w="2,000 W", whtxt="1,500 Wh", price=None, cap=500,
    battery="1,500 Wh ternary lithium (NMC), not LiFePO4; 2,500+ cycles to 80% (ALLPOWERS)",
    ac="2,000 W (4,000 W surge), 4 outlets",
    solar="500 W, 12–70 V, 18 A",
    extra=[("AC input", "400 W from the wall; ALLPOWERS gives 0–100% in 1.6 h with wall and solar together"), ("USB", "2× USB-C 100 W, 4× USB-A")],
    war="The kit page shows a 5-year warranty badge. ALLPOWERS' warranty policy gives 24 months by default and 5 years to named models, some only after registration at iallpowers.com; we have not confirmed which applies to the S2000",
    what="ALLPOWERS' older 1.5 kWh S2000", fit="Buyers who specifically want the S2000",
    cav=["Wall charging is 400 W, against 1,500 W on the S2000 Pro.", "NMC chemistry: 2,500+ cycles to 80%, fewer than LiFePO4."]),
 "P1800": dict(wh=1024, w="1,800 W", whtxt="1,024 Wh", price=439.0, cap=650,
    battery="1,024 Wh LiFePO4; 3,000+ cycles to 70% (ALLPOWERS' spec table)",
    ac="1,800 W (3,600 W peak), 4 outlets",
    solar="650 W max, 11–60 V, 13 A (XT60)",
    extra=[("UPS", "20 ms per ALLPOWERS' manual (its spec table says ≤10 ms)"), ("Weight", "Station 13 kg (manual); panels extra")],
    war="Station 24 months on ALLPOWERS' US warranty page (the P1800 is not on its 5-year list)",
    what="ALLPOWERS' 1 kWh LiFePO4 P1800", fit="Short outages, camping and car trips on a 1 kWh station",
    cav=["Station warranty is 24 months, shorter than ALLPOWERS' 5-year stations."]),
}
# panels: watts, price alone on DAY (None = not sold alone), spec text, warranty text, kind
PN = {
 "SP037": dict(w=400, price=379.05, alone="", kind="fold",
    spec="SP037 400 W folding (45.3 V open-circuit, 10.6 A at maximum power, 18.5 kg)", war="SP037 2 years",
    desc="400 W SP037 folding panel"),
 "SF200": dict(w=200, price=132.0, alone=" (the SF200 was sold out on its own that day)", kind="flex",
    spec="SF200 200 W flexible monocrystalline (38.4 V open-circuit, 6.25 A at maximum power, ETFE, IP68, 9.03 lb)",
    war="SF200 2 years (warranty badge on ALLPOWERS' panel page)", desc="200 W SF200 flexible panel"),
 "SF100": dict(w=100, price=99.99, alone="", kind="flex",
    spec="SF100 100 W flexible monocrystalline (30.6 V open-circuit, 4.17 A at maximum power, ETFE, IP68, 5.29 lb)",
    war="SF100 2 years (warranty badge on ALLPOWERS' panel page)", desc="100 W SF100 flexible panel"),
 "SE200": dict(w=200, price=179.55, alone="", kind="lam",
    spec="SE200 200 W laminated folding panel (48.96 V open-circuit, 4.8 A at maximum power, ETFE, IP68, built-in stand, 7.16 kg)",
    war="panel warranty not stated on the kit page", desc="200 W SE200 laminated folding panel"),
 "SE100": dict(w=100, price=84.55, alone="", kind="lam",
    spec="SE100 100 W laminated folding panel (24.48 V open-circuit, 4.8 A at maximum power, ETFE, IP68, built-in stand, 3.8 kg)",
    war="panel warranty not stated on the kit page", desc="100 W SE100 laminated folding panel"),
 "SE160": dict(w=160, price=149.0, alone="", kind="plain",
    spec="SE160 160 W panel (the kit listing gives no voltage, size or weight for it)",
    war="panel warranty not stated on the kit page", desc="160 W SE160 panel"),
}
BOX2 = "The kit's box list names one solar PV connection cable and no parallel (Y) connector."
# what the stated voltages and currents say about wiring the kit's panels into its station (our arithmetic)
WIRE = {
 ("R3500", "SP037", 2): ["Two SP037 panels in series are 90.6 V open-circuit, inside the R3500's 12–150 V solar range; 800 W uses 40% of its 2,000 W solar input, so there is room for more panels."],
 ("R3500", "SF200", 2): ["Two SF200 panels in series are 76.8 V open-circuit, inside the R3500's 12–150 V solar range; 400 W is a fifth of its 2,000 W solar input, so a full refill from the sun takes about two sunny days."],
 ("R3500", "SF100", 2): ["200 W of panels is a tenth of the R3500's 2,000 W solar input: about 750 Wh on a good day, under a quarter of the battery."],
 ("R2500 V2", "SP037", 2): ["The two SP037 panels go in series (90.6 V open-circuit, inside the 150 V limit); in parallel their 21.2 A would exceed the station's 20 A solar input.",
                            "800 W of panels uses most of the station's 1,000 W solar input."],
 ("R2500 V2", "SF200", 2): ["Two SF200 panels in series are 76.8 V open-circuit, inside the station's 12–150 V solar range; 400 W uses 40% of its 1,000 W input."],
 ("R2500 V2", "SE200", 2): ["Two SE200 panels in series are 97.92 V open-circuit, inside the station's 12–150 V solar range; 400 W uses 40% of its 1,000 W input."],
 ("R2500 V2", "SF100", 2): ["200 W of panels uses a fifth of the station's 1,000 W solar input."],
 ("R2500 V2", "SE100", 2): ["200 W of panels uses a fifth of the station's 1,000 W solar input."],
 ("R2500 V2", "SF200", 1): ["One 200 W panel uses a fifth of the station's 1,000 W solar input."],
 ("R2500 V2", "SF100", 1): ["A 100 W panel adds about 375 Wh on a good day, a fifth of the battery."],
 ("R2500 V2", "SE160", 1): ["A 160 W panel adds about 600 Wh on a good day, under a third of the battery; the station takes up to 1,000 W of panels."],
 ("S2000 Pro", "SF100", 2): ["200 W of panels uses a fifth of the station's 1,000 W solar input; in series the pair is 61.2 V open-circuit, inside the 150 V limit."],
 ("S2000 Pro", "SE100", 2): ["200 W of panels uses a fifth of the station's 1,000 W solar input; in series the pair is 48.96 V open-circuit, inside the 150 V limit."],
 ("S2000 Pro", "SF200", 2): ["Two SF200 panels in series are 76.8 V open-circuit, inside the 150 V limit; in parallel their 12.5 A at maximum power sits just under the station's 13 A input."],
 ("S2000 Pro", "SF100", 1): ["A 100 W panel adds about 375 Wh on a good day, a quarter of the battery."],
 ("S2000", "SF200", 2): ["The two SF200 panels have to be wired in parallel: in series they are 76.8 V open-circuit, over the S2000's 70 V solar limit. In parallel they draw 12.5 A, inside its 18 A input.",
                         "400 W of panels uses most of the S2000's 500 W solar input, so there is no room for a third panel."],
 ("P1800", "SF200", 2): ["The two SF200 panels have to be wired in parallel: in series they are 76.8 V open-circuit, over the P1800's 60 V solar limit. In parallel their 12.5 A at maximum power is just inside its 13 A input. " + BOX2],
 ("P1800", "SE200", 2): ["The two SE200 panels have to be wired in parallel: in series they are 97.92 V open-circuit, over the P1800's 60 V solar limit. In parallel they draw 9.6 A, inside its 13 A input. " + BOX2],
 ("P1800", "SE200", 1): ["One SE200 (48.96 V open-circuit) fits the P1800's 11–60 V solar input and uses under a third of its 650 W; a second SE200 would have to go in parallel."],
}
FLEX = "The {pn} is a flexible panel with no stand; it is made to be strapped or fixed to a surface."

# (slug, station, panel, n, handle, variant id, price, compare-at, pre-order date or None, extra caveats, instead)
D11 = "Dec 11, 2026"
KITS = [
 ("allpowers-r3500-2x-sp037-solar-kit", "R3500", "SP037", 2, "allpowers-r3500-solar-generator-power-station-3200w-3168wh-with-sp037-400w-solar-panel", 43451053211801, 2182.15, 2699.0, "Nov 20, 2026",
  ["ALLPOWERS sells the R3500 with one 600 W SP039 panel at $1,993.10 and with two (1,200 W) at $2,562.15 on other listings."], None),
 ("allpowers-r3500-2x-sf200-solar-kit", "R3500", "SF200", 2, "allpowers-r3500-solar-generator-power-station-3200w-3168wh-with-sf200-200w-flexible-solar-panel", 43450954383513, 1463.0, 2399.0, "Nov 9, 2026", [], None),
 ("allpowers-r3500-2x-sf100-solar-kit", "R3500", "SF100", 2, "allpowers-r3500-solar-generator-power-station-3200w-3168wh-with-sf100-100w-flexible-solar-panel", 43450923810969, 1398.98, 2299.0, "Nov 9, 2026", [],
  ("allpowers-r3500-2x-sf200-solar-kit", "For $64.02 more, ALLPOWERS sells the same R3500 with two 200 W SF200 panels, which refill the battery twice as fast.")),
 ("allpowers-r2500-v2-2x-sp037-solar-kit", "R2500 V2", "SP037", 2, "allpowers-r2500-v2-sp037-400w-solar-panel-2500w-solar-generator-kit", 67800818647193, 1417.1, 2099.0, D11, [], None),
 ("allpowers-r2500-v2-2x-sf200-solar-kit", "R2500 V2", "SF200", 2, "allpowers-r2500-v2-200w-solar-panel-2500w-solar-generator-kit", 48908282396825, 1037.1, 1799.0, D11, [],
  ("allpowers-r2500-v2-2x-se200-solar-kit", "For $19 less, ALLPOWERS sells the same R2500 V2 with two 200 W SE200 panels, which fold and stand on their own.")),
 ("allpowers-r2500-v2-2x-se200-solar-kit", "R2500 V2", "SE200", 2, "allpowers-r2500-v2-200w-solar-panel-2500w-solar-generator-kit", 48908282331289, 1018.1, 1799.0, D11,
  ["For $19.95 more, ALLPOWERS sells the R2500 V2 with one 400 W SP037 folding panel: the same wattage in one heavier panel."], None),
 ("allpowers-r2500-v2-2x-sf100-solar-kit", "R2500 V2", "SF100", 2, "allpower-r2500-plus-100w-solar-panel-2500w-solar-generator-kit-%E5%89%AF%E6%9C%AC", 48908029919385, 885.1, 1699.0, D11, [],
  ("allpowers-r2500-v2-se200-solar-kit", "For $46.55 less, ALLPOWERS sells the same R2500 V2 with one 200 W SE200 panel: the same panel wattage, in a folding panel with its own stand.")),
 ("allpowers-r2500-v2-2x-se100-solar-kit", "R2500 V2", "SE100", 2, "allpower-r2500-plus-100w-solar-panel-2500w-solar-generator-kit-%E5%89%AF%E6%9C%AC", 48908029853849, 828.1, 1699.0, D11,
  ["For $10.45 more, ALLPOWERS sells the R2500 V2 with one 200 W SE200 panel: the same wattage in one panel."], None),
 ("allpowers-r2500-v2-sf200-solar-kit", "R2500 V2", "SF200", 1, "allpowers-r2500-v2-200w-solar-panel-2500w-solar-generator-kit", 48908282364057, 848.05, 1799.0, D11, [],
  ("allpowers-r2500-v2-se200-solar-kit", "For $9.50 less, ALLPOWERS sells the same R2500 V2 with the 200 W SE200 panel, which folds and stands on its own.")),
 ("allpowers-r2500-v2-sf100-solar-kit", "R2500 V2", "SF100", 1, "allpower-r2500-plus-100w-solar-panel-2500w-solar-generator-kit-%E5%89%AF%E6%9C%AC", 48908029886617, 772.05, 1699.0, D11, [],
  ("allpowers-r2500-v2-se100-solar-kit", "For $28.50 less, ALLPOWERS sells the same R2500 V2 with the 100 W SE100 panel, which folds and stands on its own.")),
 ("allpowers-r2500-v2-se160-solar-kit", "R2500 V2", "SE160", 1, "allpowers-r2500-v2-se160-160w-solar-panel-solar-generator-kit", 48262935150745, 799.0, None, "Dec 25, 2026",
  ["This listing's spec table gives the station's weight as about 24.5 kg; ALLPOWERS' R2500 V2 page gives 29 kg (63.9 lb).",
   "The listing's box list names the R2500 and an AC charging cable only, and gives no specifications for the SE160 panel."],
  ("allpowers-r2500-v2-se200-solar-kit", "For $39.55 more, ALLPOWERS sells the same R2500 V2 with the 200 W SE200 panel, whose voltage, size and weight it publishes.")),
 ("allpowers-s2000-pro-2x-sf100-solar-kit", "S2000 Pro", "SF100", 2, "s2000-pro-100w-solar-panel", 46377155362969, 890.15, 1299.0, "Nov 16, 2026", [],
  ("allpowers-s2000-pro-2x-sf200-solar-kit", "For $77.15 less, ALLPOWERS sells the same S2000 Pro with two 200 W SF200 panels: twice the panel wattage, as a pre-order.")),
 ("allpowers-s2000-pro-2x-se100-solar-kit", "S2000 Pro", "SE100", 2, "s2000-pro-100w-solar-panel", 46377155297433, 833.15, 1299.0, None,
  ["ALLPOWERS sells the same S2000 Pro with one 200 W SE200 panel at $843.60, also shipping now, and with two 200 W SF200 flexible panels at $813 as a pre-order."], None),
 ("allpowers-s2000-pro-2x-sf200-solar-kit", "S2000 Pro", "SF200", 2, "allpowers-s2000-pro-solar-generator-portable-power-station-2400w-1500wh-with-sf200-200w-flexible-solar-panel", 43450329694361, 813.0, 1699.0, "Nov 19, 2026",
  ["Usable capacity tested at about 1,250–1,380 Wh on 2026 units (reviewers)."], None),
 ("allpowers-s2000-pro-sf100-solar-kit", "S2000 Pro", "SF100", 1, "s2000-pro-100w-solar-panel", 46377155330201, 777.1, 1299.0, "Nov 16, 2026", [],
  ("allpowers-s2000-pro-sf200-solar-kit", "For $96.10 less, ALLPOWERS sells the same S2000 Pro with a 200 W SF200 flexible panel: twice the panel, as a pre-order.")),
 ("allpowers-s2000-2x-sf200-solar-kit", "S2000", "SF200", 2, "allpowers-s2000-solar-generator-portable-power-station-2000w-1500wh-with-sf200-200w-flexible-solar-panel", 43450317209753, 813.0, 1699.0, "Nov 20, 2026", [],
  ("allpowers-s2000-pro-2x-sf200-solar-kit", "For the same $813, ALLPOWERS' S2000 Pro kit has the same two panels, a 2,400 W inverter instead of 2,000 W, 1,500 W wall charging instead of 400 W and a 150 V solar input that takes the pair in series, with 49 Wh less battery.")),
 ("allpowers-p1800-2x-sf200-solar-kit", "P1800", "SF200", 2, "allpowers-1800w-solar-generator-p1800-1024wh-with-200w-solar-panel", 48279218061465, 837.0, 1059.98, "Dec 15, 2026", [],
  ("allpowers-p1800-sp037-solar-kit", "For $139 less, ALLPOWERS sells the same P1800 with one 400 W SP037 folding panel: the same wattage on a single cable, with a stand.")),
 ("allpowers-p1800-2x-se200-solar-kit", "P1800", "SE200", 2, "allpowers-1800w-solar-generator-p1800-1024wh-with-200w-solar-panel", 48279217995929, 798.0, 1059.98, "Dec 15, 2026", [],
  ("allpowers-p1800-sp037-solar-kit", "For $100 less, ALLPOWERS sells the same P1800 with one 400 W SP037 folding panel: the same wattage on a single cable.")),
 ("allpowers-p1800-se200-solar-kit", "P1800", "SE200", 1, "allpowers-1800w-solar-generator-p1800-1024wh-with-200w-solar-panel", 48279217963161, 618.55, 1059.98, "Dec 15, 2026",
  ["The same listing sells the P1800 with the flexible SF200 instead at $638."], None),
]
PRE_NOTE = {  # where the dispatch date does not come from a plain label on the kit's own variant row
 "allpowers-r2500-v2-se160-solar-kit": "Pre-order: this kit listing carried no dispatch label on 2026-11-18, but ALLPOWERS' R2500 V2 page lists the same R2500 V2 + SE160 bundle as a pre-order dispatching from Dec 25, 2026, and the station is a pre-order on every listing.",
 "allpowers-p1800-2x-sf200-solar-kit": "Pre-order: ALLPOWERS dispatches the P1800 from Dec 15, 2026 (checked 2026-11-18).",
 "allpowers-r3500-2x-sp037-solar-kit": "Pre-order: ALLPOWERS dispatches the SP037 panels from Nov 20, 2026 (checked 2026-11-18).",
 "allpowers-s2000-pro-2x-sf200-solar-kit": "Pre-order: ALLPOWERS dispatches the SF200 panels from Nov 19, 2026 (checked 2026-11-18).",
 "allpowers-s2000-2x-sf200-solar-kit": "Pre-order: ALLPOWERS dispatches the SF200 panels from Nov 20, 2026 (checked 2026-11-18).",
 "allpowers-r2500-v2-2x-sp037-solar-kit": "Pre-order: ALLPOWERS dispatches the R2500 V2 from Dec 11, 2026 (checked 2026-11-18); sold on its own, the SP037 panel was a pre-order from Nov 20.",
}


def allpowers_kit(slug, st, pn, n, handle, variant, price, lst, pre, extra, instead):
    s, p = ST[st], PN[pn]
    tot = n * p["w"]
    d = {"slug": slug, "brand": "ALLPOWERS", "program": "cj:allpowers", "asin": None, "category": "solar-kit"}
    if instead:
        d["instead"] = instead
    cnt = "" if n == 1 else f"{n}× "
    d["_variant"] = variant
    d["name"] = f"ALLPOWERS {st} + {cnt}{pn} {p['w']} W Solar Generator Kit ({s['whtxt']}, {s['w']})"
    d["model"] = f"{st} + {n}× {pn}"
    d["url"] = AP + handle + f"?variant={variant}"
    d["price"] = price
    if lst:
        d["list_price"] = lst
    if pre:
        d["preorder"] = pre
    d["verified"] = DAY
    eff = min(tot, s["cap"])
    d["specs"] = [("Battery", s["battery"]), ("AC output", s["ac"]), ("Panels" if n > 1 else "Panel", f"{n}× {p['spec']}"),
                  ("Solar input", s["solar"]), ("Solar recharge with this kit", hours(s["wh"], eff))] + s["extra"]
    d["warranty"] = f"{s['war']}; {p['war']}"
    d["returns"] = RET
    h = s["wh"] / (eff * 0.75)
    pw = "panels" if n > 1 else "panel"
    how = ("enough panel to refill the battery in about one good day of sun" if h <= 6.5
           else f"the {pw} can refill the battery in about two sunny days" if h <= 11
           else f"the {pw} {'top' if n > 1 else 'tops'} the battery up rather than {'refill' if n > 1 else 'refills'} it each day")
    d["summary"] = (f"{s['what']} with {'one' if n == 1 else 'two'} {p['desc']}{'s' if n > 1 else ''}{f' ({tot} W in all)' if n > 1 else ''}, "
                    f"sold as one variant of ALLPOWERS' kit listing{' and as a pre-order' if pre else ', shipping rather than on pre-order when we checked'}: {how}.")
    use = {"flex": f"with flexible {pw} fixed flat to an RV, van or shed roof", "lam": f"with {'folding panels that stand' if n > 1 else 'a folding panel that stands'} on {'their' if n > 1 else 'its'} own at a campsite or on a patio",
           "fold": f"with folding {pw} set out in the sun each day", "plain": "with a small panel for slow top-ups"}[p["kind"]]
    d["fit"] = f"{s['fit']}, {use}."
    cav = []
    if pre:
        import datetime
        past = datetime.datetime.strptime(pre, "%b %d, %Y").date() < datetime.date.fromisoformat(DAY)
        cav.append(PRE_NOTE.get(slug) or (late(pre) if past else pre_line(pre)))
    if s["price"] is None:
        cav.append(f"ALLPOWERS did not list the {st} station on its own on {DAY}, so there is no separate-parts price to compare this kit with.")
    else:
        parts = round(s["price"] + n * p["price"], 2)
        diff = round(parts - price, 2)
        each = f"{'one' if n == 1 else 'two'} {pn} ({money(p['price'])}{' each' if n > 1 else ''})"
        if diff > 0.5:
            cav.append(f"Bought as separate items at ALLPOWERS' US store on {DAY}, the {st} ({money(s['price'])}) and {each} came to {money(parts)}; this kit saves {money(diff)}{p['alone']}.")
        elif diff < -0.5:
            cav.append(f"Bought as separate items at ALLPOWERS' US store on {DAY}, the {st} ({money(s['price'])}) and {each} came to {money(parts)}, {money(-diff)} less than this kit{p['alone']}.")
        else:
            cav.append(f"The kit price equals the {st} ({money(s['price'])}) plus {each} bought separately at ALLPOWERS' US store on {DAY}{p['alone']}.")
    cav += WIRE[(st, pn, n)]
    if p["kind"] == "flex":
        cav.append(FLEX.format(pn=pn))
    d["caveats"] = cav + extra + s["cav"] + [SEP]
    return d


# ---------------------------------------------------------------- ALLPOWERS panels
def allpowers_panels():
    base = {"brand": "ALLPOWERS", "program": "cj:allpowers", "asin": None, "category": "solar-panel"}
    return [
     {"slug": "allpowers-sf400-400w-flexible-solar-panel-2-pack", "_variant": 43939446947993, **base,
      "name": "ALLPOWERS SF400 400 W Flexible Solar Panel, 2-Pack (800 W)", "model": "2× SF400",
      "url": AP + "allpowers-sf400-flexible-solar-panel-400w", "price": 1099.99, "list_price": 1499.0, "verified": DAY,
      "specs": [("Rated power", "2 × 400 W (±5%)"), ("Cells", "Monocrystalline with an ETFE surface, 23% (ALLPOWERS)"),
                ("Vmp / Voc", "63.1 V / 74.46 V per panel"), ("Imp / Isc", "6.34 A / 6.85 A per panel"),
                ("Weather", "IP68; ALLPOWERS says it withstands up to 50 kg when installed flat"),
                ("Size / weight", "1,762 × 1,162 × 3 mm and 7.9 kg (17.3 lb) per panel"), ("Operating temperature", "-20 to 85 °C")],
      "warranty": "2 years (warranty badge on ALLPOWERS' SF400 page)", "returns": RET,
      "summary": "Two 400 W flexible ETFE panels for a roof, RV or boat, sold only as a pair. Each panel's 74.46 V open-circuit voltage suits ALLPOWERS' 150 V solar inputs and is too high for its 60 V and 70 V ones.",
      "fit": "Fixed mounting on an RV roof, shed or boat that feeds an R2500 V2, R3500 or S2000 Pro (12–150 V solar inputs).",
      "caveats": ["Each panel is 74.46 V open-circuit: above the 60 V solar limit of the P1800 and R1500 and the 70 V limit of the S2000.",
                  "Two in series are 148.9 V at the rated figure and the spec allows +5%, which passes the 150 V limit of the R2500 V2, R3500 and S2000 Pro, so the pair goes in parallel (12.7 A at maximum power).",
                  "At $1,099.99 for 800 W it costs more per watt than ALLPOWERS' folding panels: two 400 W SP037 panels were $758.10 on 2026-11-18.",
                  "The listing's \"What You Get\" line reads \"2*SF400 200W Solar Panel\", while its title, variant name and spec table give 400 W per panel; that line lists a user manual and no adapter cable.",
                  "A flexible panel with no stand; each one is 1.76 m long."]},
     {"slug": "allpowers-sp039-600w-solar-panel", "_variant": 43170165555353, **base,
      "name": "ALLPOWERS SP039 600 W Foldable Solar Panel", "model": "SP039",
      "url": AP + "allpowers-sp039-600w-monocrystalline-portable-solar-panel", "price": 599.0, "list_price": 899.0,
      "preorder": "Nov 23, 2026", "verified": DAY,
      "specs": [("Rated power", "600 W"), ("Cells", "Monocrystalline, about 23% (ALLPOWERS)"), ("Vmp / Voc", "44 V / 52.8 V"),
                ("Imp / Isc", "13.63 A / 14.99 A"), ("Connector", "MC4-style; MC4-to-XT60 cable and a 1.5 m extension cable included"),
                ("Weather", "IP67"), ("Size / weight", "83.7 × 71.4 × 0.4 in open, 35.7 × 23.6 × 1.9 in folded; 12.5 kg (27.5 lb)"),
                ("Operating temperature", "-10 to 60 °C")],
      "warranty": "24 months (ALLPOWERS' SP039 page)", "returns": RET,
      "summary": "ALLPOWERS' largest folding panel: 600 W in six sections at 27.5 lb. Its 52.8 V open-circuit voltage fits a 12–60 V solar input, and it delivers its full current only to inputs rated above 13.6 A.",
      "fit": "Refilling an R3500 or R2500 V2 in a day of sun from one panel; on the S2000 Pro and P1800 the 13 A solar input caps it a little under 600 W.",
      "caveats": [pre_line("Nov 23, 2026"),
                  "It gives 13.63 A at maximum power, so a station with a 13 A solar input (S2000 Pro, P1800) caps it at about 570 W (13 A × 44 V, our arithmetic).",
                  "Too high-voltage (52.8 V open-circuit) for stations with a 28 V solar limit, such as BLUETTI's Elite 30 V2.",
                  "Open, it covers about 2.1 × 1.8 m; ALLPOWERS supplies six buckle ropes and hooks to tie it down.",
                  "ALLPOWERS also sells it in kits with the R3500, R2500 V2 and P1800."]},
     {"slug": "allpowers-sp033-200w-solar-panel", "_variant": 45476263526553, **base,
      "name": "ALLPOWERS SP033 200 W Foldable Solar Panel", "model": "SP033",
      "url": AP + "allpowers-sp033-portable-polycrystalline-solar-panel-200w-flash-deal", "price": 199.0, "list_price": 299.0, "verified": DAY,
      "specs": [("Rated power", "200 W (±5%)"), ("Cells", "Monocrystalline in the spec table (the listing title says polycrystalline), 19–22%"),
                ("Vmp / Voc", "36.6 V / 44.4 V"), ("Imp / Isc", "5.45 A / 5.95 A"),
                ("Connector", "MC4-style; MC4-to-XT60 and MC4-to-DC5521 cables and three adapters included"), ("Weather", "IP66 (ALLPOWERS)"),
                ("Size / weight", "2,230 × 650 mm open, 650 × 515 mm folded; 6.3 kg (13.9 lb)")],
      "warranty": "2 years (warranty badge on ALLPOWERS' page)", "returns": RET,
      "summary": "A 200 W folding panel with a kickstand and adapter cables for most power stations, in stock when ALLPOWERS' other 200 W panels were pre-orders or sold out.",
      "fit": "Buyers who need a 200 W folding panel that ships now, for a station whose solar input takes 44.4 V or more.",
      "caveats": ["This is ALLPOWERS' \"Flash Deal\" listing at $199; its regular SP033 listing showed $118.99 and sold out on 2026-11-18.",
                  "ALLPOWERS' newer SE200 (200 W, IP68, 7.16 kg) was $179.55 the same day, as a pre-order with no dispatch date.",
                  "The listing title says polycrystalline; its spec table says monocrystalline.",
                  "Too high-voltage (44.4 V open-circuit) for stations with a 28 V solar limit, such as BLUETTI's Elite 30 V2.",
                  "IP66 against the IP67 and IP68 of ALLPOWERS' newer panels."]},
    ]


# ---------------------------------------------------------------- OSCAL
O_STATION = 1659.99   # PowerMax 6000 alone on store.oscal.hk on DAY (sold out that day)
O_PANEL = 369.98
O_KIT = "oscal-solar-generator-kit-6000wpowermax-6000-pm-400se-solar-panel"
OKITS = [(1, 68036591714524, 1969.98, 2699.98), (2, 68036591747292, 2269.98, 3199.98), (3, 68036591780060, 2499.98, 3699.98), (4, 68036591812828, 2799.98, 3999.98)]
O_PANEL_WAR = "OSCAL's warranty table lists no term for solar panels, so ask OSCAL support for the panel's term before buying"


def oscal_kit(n, variant, price, lst):
    tot = n * 400
    slug = f"oscal-powermax-6000-{'' if n == 1 else f'{n}x-'}pm400-se-solar-kit"
    parts = round(O_STATION + n * O_PANEL, 2)
    words = {1: "one", 2: "two", 3: "three", 4: "four"}[n]
    d = {"slug": slug, "cart_variant": variant, "brand": "OSCAL", "program": "awin:oscal", "asin": None, "category": "solar-kit",
         "name": f"OSCAL PowerMax 6000 + {'' if n == 1 else f'{n}× '}PM400 SE 400 W Solar Generator Kit (3,600 Wh, 6,000 W)",
         "model": f"PowerMax 6000 + {n}× PM400 SE",
         "url": OS + O_KIT + f"?variant={variant}", "price": price, "list_price": lst, "preorder": "Dec 14, 2026", "verified": DAY}
    d["specs"] = [("Battery", "3,600 Wh LiFePO4, 3,500+ cycles to 80%; expandable with BP3600 packs"),
                  ("AC output", "6,000 W continuous (drops to 5,000 W after 5 min), 9,000 W surge; 120 V / 240 V split-phase (US version)"),
                  ("Panels" if n > 1 else "Panel", f"{n}× PM400 SE 400 W folding (43.2 V open-circuit, 11.1 A at maximum power, MC4, IP67, 11 kg{' each' if n > 1 else ''})"),
                  ("Solar input", "2,400 W max (OSCAL's pages give no voltage range in text)"),
                  ("Solar recharge with this kit", hours(3600, tot)),
                  ("AC input", "2,200 W max, about 2 h to full"), ("UPS switchover", "5 to 8 ms"),
                  ("Weight", f"Station 101.4 lb (46 kg), wheels and pull handle; panel{'s' if n > 1 else ''} 11 kg{' each' if n > 1 else ''}")]
    d["warranty"] = f"5 years (60 months) on the power station per OSCAL's warranty table; {O_PANEL_WAR}"
    d["returns"] = ORET
    d["summary"] = (f"OSCAL's 120/240 V split-phase PowerMax 6000 with {words} 400 W PM400 SE folding panel{'s' if n > 1 else ''} as one variant of its kit listing, sold as a pre-sale: "
                    + ("one panel stretches the 3.6 kWh battery rather than refilling it each day." if n == 1 else
                       f"{tot:,} W of panels can put back {'about half of' if n == 2 else 'most of' if n == 3 else 'all of'} the 3.6 kWh battery on a good day of sun."))
    d["fit"] = ("Outage backup that includes a 240 V load (well pump, dryer, mini-split), " +
                ("charged mostly from the wall or a generator, with one panel to stretch a long outage." if n == 1 else
                 f"with {words} panels set out in the yard to recharge it between outage days."))
    d["caveats"] = [
        "Pre-sale: OSCAL's kit page gives December 14 as the estimated shipping date for the power station and says the solar panels ship first, the station later (read 2026-11-18).",
        f"OSCAL listed the PowerMax 6000 alone at {money(O_STATION)} (sold out on {DAY}) and the PM400 SE at {money(O_PANEL)}; at those prices the parts come to {money(parts)}, so this kit saves {money(round(parts - price, 2))}.",
        ("OSCAL's pages give the station's solar input as 2,400 W max with no voltage range in text, so confirm the limit in the manual before wiring panels in series"
         + (f" ({n} PM400 SE panels in series would be {43.2 * n:.1f} V open-circuit).".replace(".0 V", " V") if n > 1 else ".")),
        "OSCAL does not name the 240 V receptacle type. Confirm NEMA 14-50 versus L14-30 with support before buying an inlet cord or transfer switch.",
        "A lab test measured about 2,960 Wh usable (82% of rated) on average from the PowerMax 6000, and only 66% at a slow 100 W AC load.",
        "The code is OSCAL's first-order discount, so it works once per customer.",
        "OSCAL's warranty table covers the station for 60 months and does not list solar panels."]
    return d


def oscal_panels():
    base = {"brand": "OSCAL", "program": "awin:oscal", "asin": None, "category": "solar-panel"}
    src = "OSCAL's US store page shows the electrical figures only as images; the numbers here are from OSCAL's own {m} page (oscal.hk), read 2026-11-18."
    return [
     {"slug": "oscal-pm400-se-400w-solar-panel", "cart_variant": 67900139733212, **base,
      "name": "OSCAL PM400 SE 400 W Portable Solar Panel", "model": "PM400 SE",
      "url": OS + "oscal-pm400-se?variant=67900139733212", "official_page": "https://www.oscal.hk/pm400-se",
      "price": 369.98, "list_price": 459.98, "verified": DAY,
      "specs": [("Rated power", "400 W (+10%)"), ("Cells", "Monocrystalline, ETFE lamination, 24.6% cell efficiency (OSCAL)"),
                ("Vmp / Voc", "36 V / 43.2 V"), ("Imp / Isc", "11.1 A / 13.3 A"), ("Connector", "MC4"), ("Weather", "IP67"),
                ("Stand", "4 tilt angles: 30°, 40°, 50°, 80°"),
                ("Size / weight", "2,555 × 959 × 21 mm open, 959 × 674 × 50 mm folded; 11 kg"), ("Operating temperature", "-10 to 65 °C")],
      "warranty": O_PANEL_WAR[0].upper() + O_PANEL_WAR[1:] + " (power stations get 60 months)", "returns": ORET,
      "summary": "A 400 W folding panel at 11 kg with MC4 leads and a four-angle stand. Its 43.2 V open-circuit voltage suits power stations with a 12–60 V solar input.",
      "fit": "Charging an OSCAL PowerMax station, or another brand's station that accepts MC4 panels of at least 44 V and 11 A.",
      "caveats": [src.format(m="PM400 SE"),
                  "It gives 11.1 A at maximum power, so a station input limited to 10 A caps it at about 360 W (10 A × 36 V, our arithmetic).",
                  "The store listing's text names no adapter cable, so check the box list against the station's connector (many use XT60).",
                  "OSCAL sells it in kits with the PowerMax 6000; the one-panel kit was $1,969.98 on 2026-11-18, as a pre-sale.",
                  "The code is OSCAL's first-order discount, so it works once per customer."]},
     {"slug": "oscal-pm200-se-200w-solar-panel", "cart_variant": 67900074328284, **base,
      "name": "OSCAL PM200 SE 200 W Portable Solar Panel", "model": "PM200 SE",
      "url": OS + "oscal-pm200-se?variant=67900074328284", "official_page": "https://www.oscal.hk/pm200-se",
      "price": 229.98, "list_price": 399.98, "verified": DAY,
      "specs": [("Rated power", "200 W (+10%)"), ("Cells", "Monocrystalline, ETFE lamination, 24.6% cell efficiency (OSCAL)"),
                ("Vmp / Voc", "18 V / 21.6 V"), ("Imp / Isc", "11.1 A / 13.3 A"), ("Connector", "MC4"), ("Weather", "IP67"),
                ("Stand", "Adjustable tilt"),
                ("Size / weight", "2,195 × 591 × 21 mm open, 991 × 585 × 50 mm folded; 7.4 kg"), ("Operating temperature", "-10 to 65 °C")],
      "warranty": O_PANEL_WAR[0].upper() + O_PANEL_WAR[1:] + " (power stations get 60 months)", "returns": ORET,
      "summary": "A 200 W folding panel at 7.4 kg with MC4 leads. It is a low-voltage, high-current panel (18 V, 11.1 A at maximum power), so how much of the 200 W a station takes depends on its solar input's current limit.",
      "fit": "A station whose solar input starts at 18 V or lower and accepts 11 A, or two panels in series (43.2 V open-circuit) on a 12–60 V input.",
      "caveats": [src.format(m="PM200 SE"),
                  "At 18 V it needs 11.1 A for full power: a station input limited to 8 A takes about 144 W from it and one limited to 10 A about 180 W (our arithmetic).",
                  "OSCAL's 400 W PM400 SE was $369.98 on 2026-11-18, $140 more for twice the wattage.",
                  "The store listing's text names no adapter cable, so check the box list against the station's connector (many use XT60).",
                  "The code is OSCAL's first-order discount, so it works once per customer."]},
    ]


def records():
    return [allpowers_kit(*k) for k in KITS] + allpowers_panels() + [oscal_kit(*k) for k in OKITS] + oscal_panels()


# ---------------------------------------------------------------- cart tests -> coupons.json
AUTO = ("welcome offer", "spend $")   # the store's own automatic discounts seen in control runs


def tests_by_variant():
    """{variant id: {"control": run, CODE: run}} from the raw jsonl; the last complete, valid set per variant wins."""
    out = {}
    if not TESTS.exists():
        return out
    cur = None
    for line in open(TESTS):
        r = json.loads(line)
        if r.get("error") or r.get("void") or "variant_id" not in r:
            continue
        if abs(r["subtotal"] - r["expected_price"]) > 0.01:      # another cart user's item was in the cart: not our test
            continue
        v = out.setdefault(r["variant_id"], {})
        if r["code"] == "ZZNOTACODE7Q":
            if r["applicable"] or any(not a["title"].lower().startswith(AUTO) for a in r["applications"]):
                continue
            v["control"] = r
        else:
            v[r["code"]] = r
    return out


def code_tests(recs):
    """[(brand, code, test dict)] for the kept records; a code the cart rejected gets discount 0."""
    tv, rows = tests_by_variant(), []
    for d in recs:
        vid = d.get("cart_variant") or d["_variant"]
        runs = tv.get(vid) or {}
        ctl = runs.get("control")
        for code, r in runs.items():
            if code == "control" or not ctl:
                continue
            t = {"date": DAY, "product": d["slug"], "qty": 1, "subtotal": r["subtotal"], "discount": r["code_amount"] if r["applicable"] else 0}
            if r["applicable"] and ctl["total"] < ctl["subtotal"] - 0.005:
                t["no_code_total"] = ctl["total"]
            rows.append((d["brand"], code, t))
    return rows


# ---------------------------------------------------------------- apply
BEGIN = "# >>> DLC-321 new store products, prepared 2026-11-18: generated by growth/focus/offers/newproducts_1118.py (re-run `apply`; do not edit by hand)\n"
END = "# <<< DLC-321\n"
ANCHOR = "{\"slug\": 'bluetti-elite-200-v2-charger-1-bundle',"
F_BEGIN = "    # >>> DLC-321 (2026-11-18): new ALLPOWERS and OSCAL product pages open with where to buy (generated by newproducts_1118.py)\n"
F_END = "    # <<< DLC-321\n"


def literal(d):
    lines = [f' "{k}": {v!r},' for k, v in d.items() if not k.startswith("_")]
    return "{" + "\n".join(lines)[1:].rstrip(",") + "},\n"


def strip_block(s, b, e):
    i = s.find(b)
    if i < 0:
        return s
    j = s.index(e, i) + len(e)
    return s[:i] + s[j:]


def apply(keep=None, buy_first=()):
    recs = records()
    if keep is not None:
        recs = [d for d in recs if d["slug"] in keep]
    slugs = [d["slug"] for d in recs]
    # products.py
    path = ROOT / "src" / "products.py"
    s = strip_block(open(path).read(), BEGIN, END)
    known = set(re.findall(r"[\"']slug[\"']: [\"']([a-z0-9-]+)[\"']", s)) | set(slugs)
    dup = [x for x in slugs if re.search(r"[\"']slug[\"']: [\"']" + re.escape(x) + r"[\"']", s)]
    assert not dup, f"already in products.py outside our block: {dup}"
    for d in recs:
        if d.get("instead") and d["instead"][0] not in known:
            del d["instead"]
    assert s.count(ANCHOR) == 1
    if recs:
        s = s.replace(ANCHOR, BEGIN + "\n".join(literal(d) for d in recs) + END + ANCHOR)
    open(path, "w").write(s)
    # focus.py: BUY_FIRST
    path = ROOT / "src" / "focus.py"
    s = strip_block(open(path).read(), F_BEGIN, F_END)
    i = s.index("BUY_FIRST = {")
    j = s.index("\n}\n", i) + 1
    # the opening comes from the best-offer check (src/bestoffer.json, build.buy_first); BUY_FIRST is only the fallback for a
    # kept slug that check could not read (--buy-first)
    first = [x for x in slugs if x in buy_first]
    if first:
        s = s[:j] + F_BEGIN + "".join(f'    "{x}",\n' for x in first) + F_END + s[j:]
    open(path, "w").write(s)
    # coupons.json: today's tests on the kept slugs replace any earlier test of ours on them; OSCAL's code lists its slugs
    path = ROOT / "src" / "coupons.json"
    C = json.load(open(path))
    ours = {d["slug"] for d in records()}
    for c in C["codes"]:
        c["tests"] = [t for t in c["tests"] if t["product"] not in ours]
        if c.get("slugs"):
            c["slugs"] = [x for x in c["slugs"] if x not in ours]
    n = 0
    for brand, code, t in code_tests(recs):
        c = next(c for c in C["codes"] if c["brand"] == brand and c["code"] == code)
        c["tests"].append(t)
        n += 1
        if "slugs" in c and t["discount"] > 0 and t["product"] not in c["slugs"]:
            c["slugs"].append(t["product"])
    with open(path, "w") as f:   # the layout tools/codes_merge.py writes: one code per line
        f.write('{\n "_notes": ' + json.dumps(C["_notes"], ensure_ascii=False) + ',\n "checked": ' + json.dumps(C["checked"]) + ',\n "codes": [\n')
        f.write(",\n".join("  " + json.dumps(c, ensure_ascii=False) for c in C["codes"]) + "\n ]\n}\n")
    print(f"applied {len(recs)} records, {n} cart tests")
    return recs


if __name__ == "__main__":
    cmd = sys.argv[1]
    keep = set(sys.argv[sys.argv.index("--keep") + 1].split(",")) if "--keep" in sys.argv else None
    if cmd == "print":
        for d in records():
            if keep is None or d["slug"] in keep:
                print(json.dumps(d, ensure_ascii=False, indent=1))
    elif cmd == "slugs":
        print(" ".join(d["slug"] for d in records() if keep is None or d["slug"] in keep))
    elif cmd == "cartfile":   # the cart tests in the shape tools/bestoffer.py --cart reads: one row per slug, control run + best code run
        tv = tests_by_variant()
        with open(sys.argv[2], "w") as f:
            for d in records():
                runs = tv.get(d.get("cart_variant") or d["_variant"]) or {}
                best = max((r for k, r in runs.items() if k != "control" and r["applicable"]), key=lambda r: r["code_amount"], default=None)
                if (keep is None or d["slug"] in keep) and runs.get("control") and best:
                    f.write(json.dumps({"slug": d["slug"], "price": d["price"], "code": best["code"], "runs": [runs["control"], best]}) + "\n")
    elif cmd == "apply":
        apply(keep, set(sys.argv[sys.argv.index("--buy-first") + 1].split(",")) if "--buy-first" in sys.argv else ())
