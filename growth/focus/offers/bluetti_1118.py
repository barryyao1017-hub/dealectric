#!/usr/bin/env python3.12
"""BLUETTI store items we did not list, prepared 2026-11-18 (DLC-321 phase 3). Records are composed from
data/bluetti-uncovered-2026-11-18.json (each item's /products/<handle>.js read that day: price, compare-at price, exact
variant; the page's dispatch notes and the store's own one-line spec for the variant), the parts' standalone prices read
the same day, the station facts of bluetti_kits_1117.py and our existing BLUETTI records.
Cart tests: data/cart-tests-2026-11-18-bluetti.jsonl (codecheck_browser.py on each exact variant, control run first).

    python3.12 growth/focus/offers/bluetti_1118.py apply [--keep slug,...] [--group 1,2]   # idempotent: products.py, coupons.json
    python3.12 growth/focus/offers/bluetti_1118.py print|slugs|cartfile <out>|report [--keep ...] [--group ...]

A record is written only when its cart test passed (control rejected, code applied on the exact variant at today's
price). `apply` rewrites its own marked block, so it can be re-run after a rebase.
"""
import json, re, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(HERE))
import bluetti_kits_1117 as K  # noqa: E402  (station, panel and expansion-battery facts)

DAY = "2026-11-18"
B = "https://www.bluettipower.com/products/"
ITEMS = {it["qid"]: it for it in json.load(open(HERE / "data" / "bluetti-uncovered-2026-11-18.json"))}
TESTS = HERE / "data" / "cart-tests-2026-11-18-bluetti.jsonl"
RET = K.RET
SEP = "BLUETTI's page says each unit is delivered separately."


def money(x):
    return f"${x:,.2f}".replace(".00", "")


def num(x):
    return f"{x:,.1f}".replace(".0", "")


# ---------------------------------------------------------------- stations: K.ST plus the families new to the catalog
ST = dict(K.ST)
ST["AC180"] = dict(wh=1152, w="1,800 W", battery="1,152 Wh LiFePO4; 3,500+ cycles to 80% (BLUETTI)",
    ac="1,800 W continuous; 2,700 W Power Lifting; 4 outlets", solar="500 W, 12–60 V, 10 A", cap=500,
    extra=[("AC input", "1,440 W in Turbo mode (1,000 W standard); 80% in 45 min"), ("UPS", "20 ms"), ("Weight", "Station about 16 kg (35.27 lb)")],
    war="5 years on the AC180 (BLUETTI US)", what="BLUETTI's 1.15 kWh, 1,800 W AC180",
    fit="Camping, car trips and short outages: a fridge, a coffee maker and laptops",
    cav=["StorageReview measured 1,030 Wh usable from the AC180's 1,152 Wh at a 350 W load."])
ST["FridgePower"] = dict(wh=2016, w="1,800 W", battery="2,016 Wh LiFePO4; expandable to about 8 kWh with BC200 batteries (BLUETTI)",
    ac="1,800 W continuous, 3,600 W peak (BLUETTI)", solar=None, cap=None,
    extra=[("UPS", "10 ms automatic switchover (BLUETTI)"), ("Form", "75 mm thick, made to stand beside a refrigerator or hang on a wall")],
    war="BLUETTI's product warranty period page did not list the FridgePower when we read it; check the term on the product page",
    what="BLUETTI's slim 2 kWh FridgePower backup battery",
    fit="Keeping a refrigerator, a sump pump or a fish tank running through an outage from a unit that stays plugged in behind the appliance",
    cav=["FridgePower is a new model; we found no independent capacity or runtime test of it."])
ST["Premium 100 V2"] = dict(wh=1024, w="2,000 W", battery="1,024 Wh LiFePO4; 4,000+ cycles (BLUETTI)",
    ac="2,000 W; 2,700 W Lifting Power; 9 ports", solar="1,000 W max (BLUETTI)", cap=1000,
    extra=[("Wall charging", "1,200 W TurboBoost, 80% in 45 min (BLUETTI)"), ("UPS", "15 ms"), ("Weight", "Station 25 lb; panel extra")],
    war="BLUETTI's page for the Premium 100 V2 did not state the warranty term in the text we read; its Premium 200 V2 page says 5 years",
    what="BLUETTI's 25 lb, 1 kWh Premium 100 V2",
    fit="Camping, car trips and short outages where a 2,000 W outlet is wanted from a 25 lb station",
    cav=["We found no independent capacity test of the Premium 100 V2."])
ST["Premium 200 V2"] = dict(wh=2073.6, w="2,700 W", battery="2,073.6 Wh LiFePO4",
    ac="2,700 W; 3,900 W Power Lifting", solar="1,000 W max, 12–60 V, 20 A", cap=1000,
    extra=[("AC input", "2,300 W max; 0 to 80% in 1 hour with 2,400 W of AC plus solar (BLUETTI)"), ("UPS", "within 15 ms"), ("Weight", "Station 53.35 lb (24.2 kg); panel extra")],
    war="5 years on the station (BLUETTI's Premium 200 V2 page)",
    what="BLUETTI's 2 kWh, 2,700 W Premium 200 V2",
    fit="Home backup for a fridge and essentials, or an RV or cabin weekend",
    cav=["We found no independent capacity test of the Premium 200 V2."])
ST["RV5"] = dict(wh=0, w="5,000 W", battery=None, ac="5,000 W continuous, 10,000 W surge",
    solar="50 V Voc limit, so panels go in parallel only (BLUETTI blog)", cap=None,
    extra=[("DC output", "1,620 W; regulated 12 V at 100 A (BLUETTI blog)"), ("Alternator charging", "PV2 doubles as the alternator input, up to 1,200 W")],
    war="5 years on the RV5 and B4810 (BLUETTI's product warranty period page)",
    what="BLUETTI's 48 V RV power hub, the RV5,",
    fit="RV owners who want the coach's own outlets, lights, pump and fans on a lithium system charged from shore power, the alternator or roof panels",
    cav=["Installation means wiring into the coach's 120 V and 12 V panels; this is not a plug-in power station.",
         "The 12 V output is 100 A. BLUETTI says leveling systems that draw more than 100 A at startup need a B1210 or the coach's existing 12 V lead-acid battery, and neither is in the box."])
PRICE_ST = {"Apex 200": 1099, "Apex 300": 1499, "Elite 100 V2": 499, "Elite 200 V2": 899, "Elite 300": 1199, "Elite 400": 1499,
            "Elite 100 mini": 429, "Elite 10": 129.99, "Pioneer Na": 700, "AC180": 549, "FridgePower": 949,
            "Premium 100 V2": 849, "Premium 200 V2": 1549, "RV5": 1299}
# BLUETTI's own station + battery bundles, when cheaper than the two bought singly, are the base of a parts comparison
BASE = {("Apex 200", "B300K"): 2199, ("Apex 200", "B500K"): 2749, ("Apex 300", "B300K"): 2599, ("Apex 300", "B500K"): 3299}

# ---------------------------------------------------------------- components: label, standalone price on DAY, spec row, role, caveats
C = {
 "B300K": dict(label="B300K", long="B300K expansion battery", price=1099, wh=2764.8, row=("Expansion battery", "B300K, 2,764.8 Wh LiFePO4{each}")),
 "B500K": dict(label="B500K", long="B500K expansion battery", price=1599, wh=5120.0, row=("Expansion battery", "B500K, 5,120 Wh LiFePO4{each}")),
 "BC200": dict(label="BC200", long="BC200 battery", price=899, wh=2016.0, row=("Add-on battery", "BC200 (BlueCell 200), 2,016 Wh, 4,000+ cycles (BLUETTI){each}")),
 "B4810": dict(label="B4810", long="B4810 battery", price=1699, wh=5120.0, row=("Battery", "B4810 LiFePO4, 51.2 V 100 Ah = 5,120 Wh{each}, self-heating, charges down to -4 °F")),
 "C1": dict(label="Charger 1", long="Charger 1 alternator charger", price=219, row=("Alternator charger", "Charger 1, 560 W from the vehicle's alternator (BLUETTI)"),
            role="charges from the vehicle's alternator while driving",
            cav=["Charger 1 must be wired to the vehicle's starter battery; a station whose DC input is below 560 W holds it under that figure."]),
 "C2": dict(label="Charger 2", long="Charger 2 alternator and solar charger", price=429, row=("Alternator + solar charger", "Charger 2, up to 1,200 W from the alternator and solar together (BLUETTI)"),
            role="charges from the vehicle's alternator and roof panels at the same time",
            cav=["Charger 2 is wired to the vehicle's starter battery, and its 1,200 W is BLUETTI's top figure: the station's own DC input sets what it actually takes."]),
 "DCHUB": dict(label="DC Hub", long="DC Hub for Charger 2", price=299, row=("DC hub", "DC Hub for Charger 2: up to 600 W of 12 V / 24 V output through Charger 2 (BLUETTI)"),
               role="feeds an RV's 12 V circuits"),
 "D1": dict(label="Hub D1", long="Hub D1 DC power hub", price=299, row=("DC hub", "Hub D1 for Apex 300: 700 W total DC, a 12 V / 50 A (24 V / 25 A) Anderson port, USB-A, USB-C, DC5521 and a car socket (BLUETTI)"),
            role="adds the USB and 12 V ports the Apex 300 lacks"),
 "A1": dict(label="Hub A1", long="Hub A1 parallel hub", price=699, alone="sold out on its own that day", row=("Parallel hub", "Hub A1 with parallel connection cables, to run the two stations as one system (BLUETTI)"),
            role="joins the two stations into one system"),
 "SX4K": dict(label="SolarX 4K", long="SolarX 4K solar charge controller", price=699, row=("Solar controller", "SolarX 4K: takes a 150–500 V panel string and up to 4,000 W, stepped down for the station (BLUETTI); Locking Terminal to P090D adapter cable included"),
              role="takes a high-voltage rooftop solar string of up to 4,000 W",
              cav=["A panel string under 150 V will not run the SolarX 4K, and a 600 V / 20 A PV disconnect is needed and not included (Notebookcheck).", "No solar panels are in this bundle."]),
 "HBK": dict(label="Home Backup Kit", long="Home Backup Kit", price=None, row=("Home backup kit", "Reliance 50 A transfer switch kit for connecting to the home's panel (BLUETTI's bundle line)"),
             role="connects to the home's electrical panel through a 50 A transfer switch",
             cav=["The home backup kit has to be installed by an electrician.", "BLUETTI sells its Apex 300 Home Integration Kit at $699 (single) and $799 (parallel); this bundle's listing does not say which kit it holds, so no parts comparison is made."]),
 "TROLLEY2": dict(label="Foldable Trolley 2", long="Foldable Trolley 2", price=249, alone="sold out on its own that day", row=("Trolley", "Foldable Trolley 2 for Apex 300 / Apex 200"), role="rolls the stack to where it is needed"),
 "CAB30TT": dict(label="30A TT-30 Cable", long="30 A TT-30 fast charging cable", price=79, row=("Charging cable", "30 A NEMA TT-30 fast charging cable"), role="charges from a 30 A RV pedestal or generator outlet"),
 "CAB30": dict(label="30A Cable", long="30 A AC charging cable", price=99, row=("Charging cable", "30 A AC charging cable for the Apex 300"), role="charges from a 30 A outlet"),
 "CAB50": dict(label="50A Cable", long="50 A AC charging cable", price=129, row=("Charging cable", "50 A AC charging cable for the Apex 300"), role="charges from a 50 A outlet"),
 "DISP1": dict(label="Display 1", long="Display 1 magnetic screen", price=99, row=("Display", "Display 1: magnetic external screen with a 2,000 mAh battery, 155 g (BLUETTI)"), role="shows the battery level without opening the app"),
 "BAG": dict(label="Carrying Bag", long="carrying bag", price=69, row=("Bag", "BLUETTI carrying case bag"), role="comes with a carrying bag"),
 "EPANEL": dict(label="Epanel", long="Epanel smart distribution panel", price=499, row=("Distribution panel", "Epanel smart distribution panel"), role=None),
 "EPAD": dict(label="Epad", long="Epad control screen", price=399, row=("Control screen", "Epad central control screen"), role=None),
}
C["TROLLEY"] = dict(label="Foldable Trolley", long="Foldable Trolley", price=249, row=("Trolley", "BLUETTI Foldable Trolley"), role="rolls the stack to where it is needed")
PANELS = {"P60": 60, "P100": 100, "P200": 200, "P350": 350, "P500": 500}
NUMW = {2: "two", 3: "three", 4: "four", 5: "five", 6: "six"}

# (qid, slug, station, number of stations, [(component, qty)], extra caveats)
G1 = [
 ("un049", "bluetti-2-apex-200-2-b300k-hub-a1-home-backup-kit", "Apex 200", 2, [("B300K", 2), ("A1", 1), ("HBK", 1)], []),
 ("un050", "bluetti-2-apex-300-2-b300k-hub-a1", "Apex 300", 2, [("B300K", 2), ("A1", 1)], []),
 ("un064", "bluetti-2-fridgepower-2-bc200", "FridgePower", 2, [("BC200", 2)], []),
 ("un103", "bluetti-ac180-350w-solar-kit", "AC180", 1, [("P350", 1)], []),
 ("un113", "bluetti-ac180-100w-solar-kit", "AC180", 1, [("P100", 1)], []),
 ("un104", "bluetti-ac180-charger-1-200w-solar-kit", "AC180", 1, [("C1", 1), ("P200", 1)], []),
 ("un108", "bluetti-ac180-charger-2-bundle", "AC180", 1, [("C2", 1)], []),
 ("un107", "bluetti-ac180-2-pack", "AC180", 2, [], []),
 ("un067", "bluetti-apex-200-2-b300k", "Apex 200", 1, [("B300K", 2)], []),
 ("un075", "bluetti-apex-200-b500k", "Apex 200", 1, [("B500K", 1)], []),
 ("un073", "bluetti-apex-200-b500k-30a-tt-30-cable", "Apex 200", 1, [("B500K", 1), ("CAB30TT", 1)], []),
 ("un097", "bluetti-apex-200-charger-2-bundle", "Apex 200", 1, [("C2", 1)], []),
 ("un080", "bluetti-apex-200-charger-2-2x200w-solar-kit", "Apex 200", 1, [("C2", 1), ("P200", 2)], []),
 ("un077", "bluetti-apex-200-charger-2-2x350w-solar-kit", "Apex 200", 1, [("C2", 1), ("P350", 2)], []),
 ("un071", "bluetti-apex-200-charger-2-2x500w-solar-kit", "Apex 200", 1, [("C2", 1), ("P500", 2)], []),
 ("un056", "bluetti-apex-300-2-b300k-solarx-4k", "Apex 300", 1, [("B300K", 2), ("SX4K", 1)], []),
 ("un069", "bluetti-apex-300-b300k-charger-1-bundle", "Apex 300", 1, [("B300K", 1), ("C1", 1)], []),
 ("un076", "bluetti-apex-300-b300k-30a-cable", "Apex 300", 1, [("B300K", 1), ("CAB30", 1)], []),
 ("un070", "bluetti-apex-300-b300k-50a-cable", "Apex 300", 1, [("B300K", 1), ("CAB50", 1)], []),
 ("un055", "bluetti-apex-300-b300k-charger-1-hub-d1-2x350w-solar-kit", "Apex 300", 1, [("B300K", 1), ("C1", 1), ("D1", 1), ("P350", 2)],
  ["The listing's address ends in \"free-2-pv-cable\"; its title and variant name list no PV cable."]),
 ("un053", "bluetti-apex-300-b300k-charger-2-dc-hub-2x350w-solar-kit", "Apex 300", 1, [("B300K", 1), ("C2", 1), ("DCHUB", 1), ("P350", 2)], []),
 ("un072", "bluetti-apex-300-b300k-hub-d1", "Apex 300", 1, [("B300K", 1), ("D1", 1)], []),
 ("un068", "bluetti-apex-300-b300k-trolley-2", "Apex 300", 1, [("B300K", 1), ("TROLLEY2", 1)], []),
 ("un048", "bluetti-apex-300-b500k-charger-2-dc-hub-2x350w-50a-kit", "Apex 300", 1, [("B500K", 1), ("C2", 1), ("DCHUB", 1), ("P350", 2), ("CAB50", 1)], []),
 ("un058", "bluetti-apex-300-b500k-solarx-4k", "Apex 300", 1, [("B500K", 1), ("SX4K", 1)], []),
 ("un088", "bluetti-apex-300-charger-1-bundle", "Apex 300", 1, [("C1", 1)], []),
 ("un084", "bluetti-apex-300-charger-1-hub-d1", "Apex 300", 1, [("C1", 1), ("D1", 1)], []),
 ("un091", "bluetti-apex-300-hub-d1", "Apex 300", 1, [("D1", 1)], []),
 ("un081", "bluetti-apex-300-solarx-4k", "Apex 300", 1, [("SX4K", 1)], []),
 ("un051", "bluetti-apex-300-2-b500k-solarx-4k", "Apex 300", 1, [("B500K", 2), ("SX4K", 1)], []),
 ("un065", "bluetti-apex-300-b500k", "Apex 300", 1, [("B500K", 1)], []),
 ("un057", "bluetti-apex-300-b500k-home-backup-kit", "Apex 300", 1, [("B500K", 1), ("HBK", 1)], []),
 ("un061", "bluetti-apex-300-b500k-hub-d1", "Apex 300", 1, [("B500K", 1), ("D1", 1)], []),
 ("un060", "bluetti-apex-300-b500k-trolley-2", "Apex 300", 1, [("B500K", 1), ("TROLLEY2", 1)], []),
 ("un116", "bluetti-elite-10-60w-solar-kit", "Elite 10", 1, [("P60", 1)], []),
 ("un111", "bluetti-pioneer-na-100w-solar-kit", "Pioneer Na", 1, [("P100", 1)], []),
 ("un102", "bluetti-premium-100-v2-200w-solar-kit", "Premium 100 V2", 1, [("P200", 1)], []),
 ("un098", "bluetti-premium-100-v2-350w-solar-kit", "Premium 100 V2", 1, [("P350", 1)], []),
 ("un087", "bluetti-premium-200-v2-200w-solar-kit", "Premium 200 V2", 1, [("P200", 1)], []),
 ("un083", "bluetti-premium-200-v2-350w-solar-kit", "Premium 200 V2", 1, [("P350", 1)], []),
 ("un085", "bluetti-apex-300-charger-2-bundle", "Apex 300", 1, [("C2", 1)], []),
 ("un062", "bluetti-apex-300-b300k-charger-2-dc-hub", "Apex 300", 1, [("B300K", 1), ("C2", 1), ("DCHUB", 1)], []),
 ("un079", "bluetti-apex-300-charger-2-dc-hub", "Apex 300", 1, [("C2", 1), ("DCHUB", 1)], []),
 ("un082", "bluetti-elite-100-v2-b300k-charger-2-dc-hub", "Elite 100 V2", 1, [("B300K", 1), ("C2", 1), ("DCHUB", 1)],
  ["BLUETTI's bundle line gives the B300K as power fed through Charger 2 rather than as an expansion battery plugged into the Elite 100 V2, which has no expansion port in our record of it; ask BLUETTI how the two connect before ordering."]),
 ("un066", "bluetti-elite-200-v2-b500k-charger-2-dc-hub", "Elite 200 V2", 1, [("B500K", 1), ("C2", 1), ("DCHUB", 1)],
  ["The Elite 200 V2 is not expandable in BLUETTI's own description of it; in this bundle the B500K feeds it through Charger 2, so ask BLUETTI how the two connect before ordering."]),
 ("un110", "bluetti-elite-100-v2-charger-2-bundle", "Elite 100 V2", 1, [("C2", 1)], []),
 ("un101", "bluetti-elite-200-v2-charger-2-bundle", "Elite 200 V2", 1, [("C2", 1)], []),
 ("un090", "bluetti-elite-400-charger-2-bundle", "Elite 400", 1, [("C2", 1)], []),
 ("un115", "bluetti-elite-100-mini-carrying-bag", "Elite 100 mini", 1, [("BAG", 1)], []),
 ("un114", "bluetti-elite-100-mini-charger-1-bundle", "Elite 100 mini", 1, [("C1", 1)], []),
 ("un112", "bluetti-elite-100-v2-charger-1-bundle", "Elite 100 V2", 1, [("C1", 1)], []),
 ("un099", "bluetti-elite-200-v2-charger-1-200w-solar-kit", "Elite 200 V2", 1, [("C1", 1), ("P200", 1)], []),
 ("un100", "bluetti-elite-300-charger-1-bundle", "Elite 300", 1, [("C1", 1)], []),
 ("un095", "bluetti-elite-300-charger-2-bundle", "Elite 300", 1, [("C2", 1)], []),
 ("un096", "bluetti-elite-400-charger-1-bundle", "Elite 400", 1, [("C1", 1)], []),
 ("un092", "bluetti-fridgepower-2-pack", "FridgePower", 2, [], []),
 ("un078", "bluetti-fridgepower-2-bc200", "FridgePower", 1, [("BC200", 2)], []),
 ("un063", "bluetti-fridgepower-3-bc200", "FridgePower", 1, [("BC200", 3)], []),
 ("un093", "bluetti-fridgepower-bc200", "FridgePower", 1, [("BC200", 1)], []),
 ("un089", "bluetti-fridgepower-bc200-display-1", "FridgePower", 1, [("BC200", 1), ("DISP1", 1)], []),
 ("un086", "bluetti-fridgepower-charger-2-dc-hub-200w-solar-kit", "FridgePower", 1, [("C2", 1), ("DCHUB", 1), ("P200", 1)], []),
 ("un094", "bluetti-fridgepower-charger-2-dc-hub", "FridgePower", 1, [("C2", 1), ("DCHUB", 1)], []),
 ("un105", "bluetti-fridgepower-display-1", "FridgePower", 1, [("DISP1", 1)], []),
 ("un109", "bluetti-pioneer-na-charger-1-bundle", "Pioneer Na", 1, [("C1", 1)], []),
 ("un106", "bluetti-pioneer-na-charger-2-bundle", "Pioneer Na", 1, [("C2", 1)], []),
 ("un052", "bluetti-10kwh-rv-kit", "RV5", 1, [("B4810", 2), ("EPANEL", 1), ("EPAD", 1)], []),
 ("un074", "bluetti-rv5-b4810", "RV5", 1, [("B4810", 1)], []),
 ("un059", "bluetti-5kwh-rv-kit", "RV5", 1, [("B4810", 1), ("EPANEL", 1), ("EPAD", 1)], []),
]
# group 2: the stations sold on their own. (qid, slug, station, name tail, category, summary, extra spec rows, extra caveats)
ST["X60"] = dict(wh=614, w="DC only", battery="614 Wh LiFePO4", ac=None, solar=None, cap=None,
    extra=[("DC outputs", "DC4017 12 V / 5 A, DC6530 16 V / 4 A, DC5525 24 V / 4 A"), ("USB", "USB-C up to 20 V / 5 A (100 W), USB-A 5 V / 3 A"),
           ("Input", "200 W / 8 A max, 12.5–26 V; pass-through charging"), ("Weight", "7 kg (15 lb)")],
    war="12 months (spec table on BLUETTI's X60 page)", what="BLUETTI's 614 Wh CPAP battery, the X60",
    fit="Running a CPAP machine through the night while camping or in an outage, from its DC input rather than an inverter",
    cav=["DC and USB outputs only: there is no AC outlet, so the CPAP needs a DC cord that matches one of its three DC ports.",
         "BLUETTI's spec table says it is not TSA compliant, so it cannot be carried on a flight.",
         "BLUETTI's \"up to 8 hours\" is its own figure and depends on the machine, the pressure and whether the humidifier is on."])
G2 = [
 ("un121", "bluetti-premium-100-v2", "Premium 100 V2", "Portable Power Station (1,024 Wh, 2,000 W)", "power-station",
  "A 25 lb, 1 kWh LiFePO4 station with a 2,000 W inverter, 1,200 W wall charging and a 1,000 W solar input.", [], []),
 ("un117", "bluetti-premium-200-v2", "Premium 200 V2", "Portable Power Station (2,073.6 Wh, 2,700 W)", "power-station",
  "A 2 kWh LiFePO4 station with a 2,700 W inverter, 2,300 W wall charging and a 1,000 W solar input, at 53 lb.", [], []),
 ("un122", "bluetti-x60-cpap-power-bank", "X60", "CPAP Power Bank (614 Wh, DC and USB outputs)", "power-bank",
  "A 614 Wh LiFePO4 battery built to run a CPAP machine from its DC input, with 12 V, 16 V and 24 V ports and USB-C; it has no AC outlet.", [], []),
 ("un123", "bluetti-elite-30-mini", "Elite 30 mini", "Portable Power Station (288 Wh, 300 W)", "power-station",
  "BLUETTI's 7 lb, 288 Wh station with a 300 W outlet and a built-in retractable 140 W USB-C cable.", [], []),
 ("un118", "bluetti-elite-400", "Elite 400", "Portable Power Station (3,840 Wh, 2,600 W)", "power-station",
  "BLUETTI's wheeled 3.84 kWh station with a 2,600 W inverter and a 1,000 W solar input, sold as a pre-order.", [],
  ["The store's own list shows a compare-at price ($1,399) below the selling price ($1,499) for this item, so no list price is given here."]),
 ("un120", "bluetti-fridgepower", "FridgePower", "Refrigerator Backup Battery (2,016 Wh, 1,800 W)", "power-station",
  "A 75 mm thick, 2 kWh LiFePO4 backup battery that stays plugged in beside a refrigerator and takes over in 10 ms when the power fails.", [],
  ["BLUETTI sells it with one to three BC200 add-on batteries and as a pair on separate listings."]),
 ("un119", "bluetti-rv5-power-hub", "RV5", "Power Hub for RVs (5,000 W, 48 V, battery sold separately)", "power-station",
  "BLUETTI's 48 V RV power hub: a 5,000 W inverter, a 12 V supply for the coach and solar and alternator charging in one unit, sold here without a battery.", [],
  ["No battery is included: the RV5 runs from BLUETTI's B4810 battery ($1,699 on 2026-11-18); BLUETTI's RV5 + B4810 bundle was $2,799 that day, $199 less than the two bought separately."]),
]
STATION_VARIANT_URL = {"un121", "un117"}


def station(qid, slug, st, tail, cat, summary, rows, extra):
    it, s = ITEMS[qid], ST[st]
    d = {"slug": slug, "brand": "BLUETTI", "program": "awin:bluetti_us", "asin": None, "category": cat, "_qid": qid,
         "name": f"BLUETTI {st} {tail}", "model": st,
         "url": B + it["handle"] + (f"?variant={it['variant_id']}" if qid in STATION_VARIANT_URL else ""), "price": it["price_now"]}
    if it["cmp_now"] and it["cmp_now"] > it["price_now"]:
        d["list_price"] = it["cmp_now"]
    notes = ship_notes(it, [])
    pre = preorder_of(notes)
    if pre:
        d["preorder"] = pre
    d["cart_variant"] = it["variant_id"]
    d["verified"] = DAY
    d["specs"] = ([("Battery", s["battery"])] if s.get("battery") else []) + ([("AC output", s["ac"])] if s.get("ac") else []) \
        + ([("Solar input", s["solar"])] if s.get("solar") else []) + rows + [(k, v.replace("; panels extra", "").replace("; panel extra", "")) for k, v in s["extra"]]
    d["warranty"] = s["war"]
    d["returns"] = RET
    d["summary"] = summary
    d["fit"] = s["fit"] + "."
    cav = ([("Pre-order: " if pre else "") + "BLUETTI's page says: " + "; ".join(notes) + f" (read {DAY})."] if notes else [])
    d["caveats"] = cav + [c for c in s["cav"] if "MC4-to-XT60" not in c] + extra
    return d


# group 3: kits and bundles of $6,000 and up. The EnergyPro systems (un037-un040, un042, un043, un045 and the $4,849 un054)
# are installed home systems and are not composed here yet.
G3 = [
 ("un047", "bluetti-2-apex-200-2-b500k-hub-a1", "Apex 200", 2, [("B500K", 2), ("A1", 1)], []),
 ("un046", "bluetti-2-apex-300-2-b500k-hub-a1", "Apex 300", 2, [("B500K", 2), ("A1", 1)], []),
 ("un044", "bluetti-2-apex-300-4-b300k-hub-a1", "Apex 300", 2, [("B300K", 4), ("A1", 1)], []),
 ("un041", "bluetti-2-apex-300-4-b300k-hub-a1-2-solarx-4k-trolley", "Apex 300", 2, [("B300K", 4), ("A1", 1), ("SX4K", 2), ("TROLLEY", 1)], []),
]
# group 4: expansion batteries and panels. (qid, slug, name, category, model, panel watts in the item, spec rows, warranty, summary, fit, caveats)
HOST = "BLUETTI lists this battery separately for each host station; this is the listing for the {h}, so check that its cable fits your unit before ordering."
B3 = [("Capacity", "2,764.8 Wh LiFePO4{each}"), ("Weight", "65.04 lb (29.5 kg){each} (BLUETTI)")]
B5 = [("Capacity", "5,120 Wh LiFePO4{each}")]
W5 = "5 years on the B300K (BLUETTI US, with proof of purchase from an official store)"
WB5 = "See BLUETTI's product warranty period page for the B500K's term"
NOAC = "On its own the battery has no AC outlets; it powers household loads only through a compatible BLUETTI station."
WP = "12 months on the solar panels (BLUETTI's product warranty period page)"


def _rows(rows, q):
    return [(k, (f"{q}× " if q > 1 else "") + v.format(each=" each" if q > 1 else "")) for k, v in rows]


def _bat(qid, slug, model, q, host, price1, extra_rows=(), extra_cav=(), acc=()):
    """A B300K or B500K listing: q batteries for a host family, with optional accessories (component keys)."""
    it = ITEMS[qid]
    big = model == "B500K"
    wh = (5120.0 if big else 2764.8) * q
    name = f"BLUETTI {f'{q}× ' if q > 1 else ''}{model} Expansion Battery" + "".join(f" + {C[k]['label']}" for k in acc) + (f" for {host}" if host else "") + f", {num(wh)} Wh"
    cav = []
    if q > 1 or acc:
        parts = round(q * price1 + sum(C[k]["price"] for k in acc), 2)
        ls = [f"{NUMW[q] if q > 1 else 'the'} {model}{'s' if q > 1 else ''} ({money(price1)}{' each' if q > 1 else ''})"] + [
            f"the {C[k]['label']} ({money(C[k]['price'])}{', ' + C[k]['alone'] if C[k].get('alone') else ''})" for k in acc]
        lst = ", ".join(ls[:-1]) + (" and " if len(ls) > 1 else "") + ls[-1]
        diff = round(parts - it["price_now"], 2)
        cav.append(f"Bought separately at BLUETTI's US store on {DAY}, {lst} came to {money(parts)}" + (f"; this listing saves {money(diff)}." if diff > 0.5 else
                   f", {money(-diff)} less than this listing." if diff < -0.5 else ", the same as this listing."))
    for k in acc:
        cav += C[k].get("cav", [])
    cav += [NOAC] + ([HOST.format(h=host)] if host else []) + list(extra_cav)
    roles = [C[k]["role"] for k in acc if C[k].get("role")]
    return (qid, slug, name, "expansion-battery", f"{q}× {model}" if q > 1 else model, [],
            _rows(B5 if big else B3, q) + [("Fits", host)] * bool(host) + [C[k]["row"] for k in acc] + list(extra_rows),
            (WB5 if big else W5),
            (f"{NUMW[q].capitalize() if q > 1 else 'One'} {model} expansion batter{'ies' if q > 1 else 'y'} ({num(wh)} Wh{' in all' if q > 1 else ''})"
             + (" with " + " and ".join(C[k]["long"] for k in acc) if acc else "") + (f", in BLUETTI's listing for the {host}" if host else "") + "."),
            (f"Adding stored energy to a BLUETTI {host.split(' / ')[0]}-family system" if host else "Adding stored energy to a compatible BLUETTI station")
            + (": the bundle " + " and ".join(roles) if roles else "") + ".",
            cav)


def _pan(qid, slug, w, q, model, name, extra_cav=()):
    it = ITEMS[qid]
    fx = model.startswith("PV100 FX")
    one = (329, "PV100 FX 100 W flexible panel (41.4 V open-circuit, 3.05 A short-circuit, MC4, IP67, 4.85 lb / 2.2 kg, 1,000 × 590 mm)") if fx else K.PANEL[w]
    voc = 41.4 if fx else {100: 24.62, 200: 24.6, 350: 44.0, 500: 49.1}[w]
    cav = []
    if fx and q > 2:
        cav.append(f"The set costs {money(it['price_now'])}, the same as {NUMW[q // 2]} sets of two at BLUETTI's US store on {DAY} ($329 each).")
    if q > 1 and not fx:
        cav.append(f"The set costs {money(it['price_now'])}, " + ("the same as" if abs(q * one[0] - it["price_now"]) < 0.5 else f"{money(abs(round(q * one[0] - it['price_now'], 2)))} {'less' if q * one[0] > it['price_now'] else 'more'} than")
                   + f" {NUMW[q]} single panels at BLUETTI's US store on {DAY} ({money(one[0])} each).")
    if q > 1 and not fx:
        cav.append(f"{NUMW[q].capitalize()} of these in series are {num(round(voc * q, 2))} V open-circuit" + (", inside a 12–60 V solar input." if voc * q <= 60 else
                   ", over the 60 V limit of BLUETTI's 12–60 V solar inputs, so on those stations they are wired in parallel or split across two inputs."))
    return (qid, slug, name, "solar-panel", f"{w} W {model}" if q == 1 else f"{q}× {w} W {model}", [w] * q,
            [("Rated power", f"{q} × {w} W ({q * w:,} W)" if q > 1 else f"{w} W"), ("Panel", one[1])], WP,
            (f"{NUMW[q].capitalize()} of BLUETTI's {w} W {model} panels sold as one set." if q > 1 else f"BLUETTI's {w} W {model} panel, sold on its own."),
            "Recharging a BLUETTI station whose solar input accepts this panel's voltage; check the station's voltage and current limits first.",
            cav + list(extra_cav))


FX = ["A flexible panel with no stand, made to be fixed to an RV or van roof.", "At 41.4 V open-circuit each, the panels are wired in parallel on BLUETTI's RV5, whose solar input is limited to 50 V."]
G4 = [
 _bat("un154", "bluetti-b300k-for-ac200l-ac300", "B300K", 1, "AC200L / AC300", 1099),
 _bat("un142", "bluetti-2-b300k-for-ac200l-ac300", "B300K", 2, "AC200L / AC300", 1099),
 _bat("un153", "bluetti-b300k-for-ac500", "B300K", 1, "AC500", 1189.99),
 _bat("un146", "bluetti-2-b300k-for-apex-300-200", "B300K", 2, "Apex 300 / Apex 200", 1099),
 _bat("un138", "bluetti-3-b300k-for-apex-300-200", "B300K", 3, "Apex 300 / Apex 200", 1099),
 _bat("un151", "bluetti-b500k-for-apex-300-200", "B500K", 1, "Apex 300 / Apex 200", 1599),
 _bat("un140", "bluetti-2-b500k-for-apex-300-200", "B500K", 2, "Apex 300 / Apex 200", 1599),
 _bat("un147", "bluetti-b500k-for-ac300-ac200l", "B500K", 1, "AC300 / AC200L", 1799),
 _bat("un139", "bluetti-2-b500k-for-ac300-ac200l", "B500K", 2, "AC300 / AC200L", 1799),
 _bat("un145", "bluetti-b500k-for-ac500", "B500K", 1, "AC500", 2049),
 _bat("un137", "bluetti-2-b500k-for-ac500", "B500K", 2, "AC500", 2049),
 _bat("un149", "bluetti-b500k-trolley-2", "B500K", 1, "", 1599, acc=("TROLLEY2",)),
 _bat("un143", "bluetti-b500k-hub-d1", "B500K", 1, "", 1599, acc=("D1",)),
 _bat("un144", "bluetti-b500k-charger-2", "B500K", 1, "", 1599, acc=("C2",)),
 _bat("un141", "bluetti-b500k-charger-2-dc-hub", "B500K", 1, "", 1599, acc=("C2", "DCHUB")),
 _bat("un152", "bluetti-b300k-charger-2", "B300K", 1, "", 1099, acc=("C2",)),
 _bat("un148", "bluetti-b300k-charger-2-dc-hub", "B300K", 1, "", 1099, acc=("C2", "DCHUB")),
 ("un150", "bluetti-b4810-51v-100ah", "BLUETTI B4810 LiFePO4 Battery, 51.2 V 100 Ah (5,120 Wh), self-heating", "lithium-battery", "B4810", [],
  [("Voltage / capacity", "51.2 V, 100 Ah = 5,120 Wh"), ("Cold charging", "Self-heating; charges down to -4 °F (BLUETTI)"), ("Fits", "BLUETTI's RV5 power hub")],
  "5 years on the B4810 (BLUETTI's product warranty period page)",
  "The 48 V, 5.12 kWh battery for BLUETTI's RV5 power hub, sold on its own.", "Adding a second battery to an RV5 system, or replacing one.",
  ["BLUETTI sold the RV5 + B4810 bundle at $2,799 on 2026-11-18, $199 less than the hub ($1,299) and this battery bought separately.",
   "BLUETTI's page text gives no maximum discharge current for it."]),
 ("un155", "bluetti-bc200-battery", "BLUETTI BC200 Add-on Battery for FridgePower, 2,016 Wh", "expansion-battery", "BC200", [],
  [("Capacity", "2,016 Wh, 4,000+ cycles (BLUETTI)"), ("Fits", "BLUETTI FridgePower; up to three per FridgePower for about 8 kWh in all (BLUETTI)")],
  "BLUETTI's product warranty period page did not list the BC200 when we read it; check the term on the product page",
  "The 2 kWh add-on battery (BlueCell 200) for BLUETTI's FridgePower backup unit, sold on its own.", "Extending a FridgePower's runtime through a longer outage.",
  ["BLUETTI sold the FridgePower + BC200 bundle at $1,699 on 2026-11-18, $149 less than the two bought separately.", "It is an add-on for the FridgePower, not a stand-alone power station."]),
 ("un156", "bluetti-b1232-12v-314ah", "BLUETTI B1232 LiFePO4 Battery, 12.8 V 314 Ah (4,019 Wh)", "lithium-battery", "B1232", [],
  [("Voltage / capacity", "12.8 V, 314 Ah (12.8 × 314 = 4,019 Wh)"), ("Monitoring", "Bluetooth (BLUETTI)")],
  "See BLUETTI's product warranty period page for the B1232's term",
  "BLUETTI's 12 V, 314 Ah LiFePO4 deep-cycle battery for RV and marine house banks.", "Replacing a 12 V lead-acid house bank in an RV or boat.",
  ["BLUETTI's page text gives no maximum continuous or surge discharge current, weight or cycle rating for it."]),
 _pan("un132", "bluetti-350w-solar-panel", 350, 1, "folding", "BLUETTI 350 W Folding Solar Panel"),
 _pan("un126", "bluetti-350w-solar-panel-2-pack", 350, 2, "folding", "BLUETTI 350 W Folding Solar Panel, Set of 2 (700 W)"),
 _pan("un124", "bluetti-350w-solar-panel-3-pack", 350, 3, "folding", "BLUETTI 350 W Folding Solar Panel, Set of 3 (1,050 W)"),
 _pan("un125", "bluetti-sora-500-solar-panel-2-pack", 500, 2, "SORA 500", "BLUETTI SORA 500 Solar Panel, Set of 2 (1,000 W)",
      ["The set's own line still reads \"ships from 11.28\"; the page's notice for orders placed on or after Nov. 18 says late January, which is the date used here."]),
 _pan("un134", "bluetti-200w-solar-panel", 200, 1, "folding", "BLUETTI 200 W Portable Solar Panel"),
 _pan("un129", "bluetti-200w-solar-panel-2-pack", 200, 2, "folding", "BLUETTI 200 W Portable Solar Panel, Set of 2 (400 W)"),
 _pan("un127", "bluetti-200w-solar-panel-3-pack", 200, 3, "folding", "BLUETTI 200 W Portable Solar Panel, Set of 3 (600 W)"),
 _pan("un136", "bluetti-sp100l-100w-solar-panel", 100, 1, "SP100L", "BLUETTI SP100L 100 W Solar Panel"),
 _pan("un133", "bluetti-sp100l-100w-solar-panel-2-pack", 100, 2, "SP100L", "BLUETTI SP100L 100 W Solar Panel, Set of 2 (200 W)"),
 _pan("un130", "bluetti-sp100l-100w-solar-panel-3-pack", 100, 3, "SP100L", "BLUETTI SP100L 100 W Solar Panel, Set of 3 (300 W)"),
 _pan("un135", "bluetti-pv100-fx-flexible-solar-panel-2-pack", 100, 2, "PV100 FX flexible", "BLUETTI PV100 FX 100 W Flexible Solar Panel, Set of 2 (200 W)", FX),
 _pan("un131", "bluetti-pv100-fx-flexible-solar-panel-4-pack", 100, 4, "PV100 FX flexible", "BLUETTI PV100 FX 100 W Flexible Solar Panel, Set of 4 (400 W)", FX),
 _pan("un128", "bluetti-pv100-fx-flexible-solar-panel-6-pack", 100, 6, "PV100 FX flexible", "BLUETTI PV100 FX 100 W Flexible Solar Panel, Set of 6 (600 W)", FX),
]
G4_VARIANT_URL = {"un134", "un129", "un127", "un136", "un133", "un130", "un135", "un131", "un128"}


def simple(qid, slug, name, cat, model, watts, rows, war, summary, fit, cav):
    it = ITEMS[qid]
    d = {"slug": slug, "brand": "BLUETTI", "program": "awin:bluetti_us", "asin": None, "category": cat, "_qid": qid, "name": name, "model": model,
         "url": B + it["handle"] + (f"?variant={it['variant_id']}" if qid in G4_VARIANT_URL else ""), "price": it["price_now"]}
    if it["cmp_now"] and it["cmp_now"] > it["price_now"]:
        d["list_price"] = it["cmp_now"]
    notes = ship_notes(it, [(next(k for k, v in PANELS.items() if v == w), 1) for w in set(watts)])
    pre = preorder_of(notes)
    if pre:
        d["preorder"] = pre
    d["cart_variant"] = it["variant_id"]
    d["verified"] = DAY
    d["specs"] = rows
    d["warranty"], d["returns"], d["summary"], d["fit"] = war, RET, summary + (" Sold as a pre-order." if pre else ""), fit
    d["caveats"] = ([("Pre-order: " if pre else "") + "BLUETTI's page says: " + "; ".join(notes) + f" (read {DAY})."] if notes else []) + cav
    return d


GROUPS = {1: ("record", G1), 2: ("station", G2), 3: ("record", G3), 4: ("simple", G4)}
HELD_OUT = {"un054": "EnergyPro 6K + AT1 ($4,849) is an installed home system: prepared with the EnergyPro group (group 3)"}
SKIP = {   # no record: the listing's own facts contradict each other or its dispatch date cannot be read from it
 "bluetti-ac180-350w-solar-kit": "the AC180 listing says the 350 W panel \"ships from Nov. 9th\" and, in the same notice, that it is out of stock with a restock expected late December",
 "bluetti-premium-100-v2-350w-solar-kit": "the listing gives the 350 W panel's dispatch as Nov. 9th, a date already past, while BLUETTI's other listings say that panel is out of stock until late December: no usable dispatch date",
 "bluetti-premium-200-v2-350w-solar-kit": "the listing gives the 350 W panel's dispatch as Nov. 9th, a date already past, while BLUETTI's other listings say that panel is out of stock until late December: no usable dispatch date",
}

# ---------------------------------------------------------------- dispatch notes -> pre-order date
WHEN = [  # (pattern, rank, text for the record's `preorder`); rank 0 = a date that is today or already past
 (r"nov(?:ember|\.)?\s*9|11\.0?9", 0, None), (r"nov(?:ember|\.)?\s*18|11\.18", 0, None),
 (r"late nov", 2, "late November 2026"), (r"12\.14|dec(?:ember|\.)?\s*14", 3, "Dec 14, 2026"), (r"mid-?\s*dec", 4, "mid-December 2026"),
 (r"12\.25|dec(?:ember|\.)?\s*25", 5, "Dec 25, 2026"), (r"late dec", 6, "late December 2026"), (r"12\.31", 7, "Dec 31, 2026"),
 (r"early jan", 8, "early January 2027"), (r"mid-?\s*jan", 9, "mid-January 2027"), (r"late jan", 10, "late January 2027"),
]
PANEL_WORD = {60: "60W", 100: "100W", 200: "200W", 350: "350W", 500: "500W"}


def _rank(note):
    """(rank, preorder text) of a dispatch note; the cut-off date in "for orders placed on or after ..." is not a ship date."""
    n = re.split(r"for orders placed", note, flags=re.I)[0]
    for pat, rank, text in WHEN:
        if re.search(pat, n, re.I):
            return rank, text
    return -1, None


def ship_notes(it, comps):
    """The dispatch sentences on the item's own page that apply to it: the station's, its variant's red notes, and the
    panel lines of pages that list several panels (only for panels in this bundle). One note per subject: where the page
    carries two dates for the same item (an older variant note beside the banner for orders placed now), the later one."""
    watts = {PANELS[k] for k, _ in comps if k in PANELS}
    best = {}
    for n in (it.get("page_notes") or []) + (it.get("variant_notes") or []) + [x.strip() for x in str(it.get("pre_in") or "").split(";")]:
        n = re.sub(r"^.*Shipping Update:\s*", "", re.sub(r"^(likely: |Order today—)", "", n.strip())).rstrip(".")
        if not n or n in ("False", "True") or "delivered separately" in n or not re.search(r"\bships?\b|restock", n, re.I):
            continue
        for p in [x.strip().rstrip(".") for x in re.split(r";|\.\s+(?=[A-Z]|\d+\s*W)", n) if x.strip()]:
            m = re.match(r"(?:The )?(\d+)\s*W\b", p)
            if (m and int(m.group(1)) not in watts) or re.match(r"All other", p) or "PV120" in p or not re.search(r"\bships?\b|restock", p, re.I):
                continue
            p = p[0].upper() + p[1:]
            subj = re.sub(r"[^a-z0-9]", "", re.split(r"\bships?\b|\bis expected\b|\bcurrently\b", re.sub(r"^the ", "", p.lower()))[0].replace("solar", ""))
            r = _rank(p)[0]
            if subj not in best or r > best[subj][0] or (r == best[subj][0] and len(p) > len(best[subj][1])):
                best[subj] = (r, p)
    return [p for _, p in best.values()]


def preorder_of(notes):
    best = max((_rank(n) for n in notes), default=(-1, None))
    return best[1] if best[0] > 0 else None


def hours(wh, watts):
    return K.hours(wh, watts)


def record(qid, slug, st, n_st, comps, extra):
    it, s = ITEMS[qid], ST[st]
    price, cmp_ = it["price_now"], it["cmp_now"]
    panels = [(PANELS[k], q) for k, q in comps if k in PANELS]
    others = [(k, q) for k, q in comps if k not in PANELS]
    tot = sum(w * q for w, q in panels)
    wh = s["wh"] * (1 if n_st == 1 or st in ("FridgePower", "AC180") else n_st) + sum(C[k]["wh"] * q for k, q in others if "wh" in C[k])
    sep_units = n_st > 1 and st in ("FridgePower", "AC180")
    lab = lambda k, q: (f"{q}× " if q > 1 else "") + (f"{PANELS[k]} W" if k in PANELS else C[k]["label"])
    title = (f"{n_st}× " if n_st > 1 else "") + st + "".join(f" + {lab(k, q)}" for k, q in comps)
    kind = "Solar Panel Kit" if panels else "Bundle" if comps else "Pack"
    whtxt = f"{n_st}× {num(s['wh'])} Wh" if sep_units else f"{num(wh)} Wh"
    wtxt = s["w"] if n_st == 1 or sep_units else {"Apex 300": "7,680 W", "Apex 200": "up to 6,000 W"}[st]
    d = {"slug": slug, "brand": "BLUETTI", "program": "awin:bluetti_us", "asin": None, "category": "solar-kit" if panels else "power-station",
         "_qid": qid, "model": title,
         # a long title is repeated in the page's opening line, so it drops the spec list to keep the buy link near the top
         "name": f"BLUETTI {title} {kind} ({whtxt}, {wtxt})" if len(title) <= 44 else f"BLUETTI {title} {'Kit' if panels else 'Bundle'}",
         "url": B + it["handle"] + (f"?variant={it['variant_id']}" if qid in VARIANT_URL else ""),
         "price": price}
    if cmp_ and cmp_ > price:
        d["list_price"] = cmp_
    notes = ship_notes(it, comps)
    pre = preorder_of(notes)
    if pre:
        d["preorder"] = pre
    d["cart_variant"] = it["variant_id"]
    d["verified"] = DAY
    specs = []
    if st == "RV5":
        specs.append(("AC output", s["ac"]))
    else:
        if sep_units:
            specs.append(("Battery", f"{n_st} separate {st} units, each {s['battery']}"))
        elif len([1 for k, _ in others if "wh" in C[k]]) or n_st > 1:
            specs.append(("Battery", f"{num(wh)} Wh LiFePO4 in all ({'two ' if n_st > 1 else ''}{st} {num(s['wh'])} Wh{' each' if n_st > 1 else ''}"
                          + "".join(f" + {('%d× ' % q) if q > 1 else ''}{C[k]['label']} {num(C[k]['wh'])} Wh{' each' if q > 1 else ''}" for k, q in others if "wh" in C[k]) + ")"))
        else:
            specs.append(("Battery", s["battery"]))
        specs.append(("AC output", s["ac"] + (f"; BLUETTI's bundle line gives {wtxt} for the two stations in parallel" if n_st > 1 and not sep_units else "")))
    for k, q in others:
        r = C[k]["row"]
        specs.append(((r[0][:-1] + "ies" if r[0].lower().endswith("battery") else r[0] + "s") if q > 1 and "wh" in C[k] else r[0], (f"{q}× " if q > 1 else "") + r[1].format(each=" each" if q > 1 else "")))
    for w, q in panels:
        specs.append(("Panels" if q > 1 else "Panel", f"{q}× BLUETTI {K.PANEL[w][1]}"))
    if s.get("solar"):
        specs.append(("Solar input", s["solar"]))
    if panels and s.get("cap") and wh:
        specs.append(("Solar recharge with this kit", hours(wh, min(tot, s["cap"]))))
    sl = (it.get("spec_line") or "").strip()
    if sl and "|" in sl and re.fullmatch(r"[\w ,.|+×/$₄&()%:-]+", sl):
        specs.append(("BLUETTI's line for this bundle", sl))
    d["specs"] = specs + s["extra"]
    wars = [s["war"]]
    if any(k in ("B300K", "B500K") for k, _ in others):
        wars.append("see BLUETTI's product warranty period page for the expansion battery")
    if panels:
        wars.append(K.PANEL_WAR)
    if any(k in ("C1", "C2") for k, _ in others):
        wars.append("2 years on Charger 1 per BLUETTI US; check the term for the other accessories on their own pages" if any(k == "C1" for k, _ in others)
                    else "check the term for Charger 2 and the other accessories on their own pages")
    d["warranty"] = "; ".join(wars)
    d["returns"] = RET
    # what it is for
    roles = [C[k]["role"] for k, _ in others if C[k].get("role")]
    plural = lambda x: x[:-1] + "ies" if x.endswith("battery") else x + "s"
    with_ = ", ".join(([f"{NUMW[q] if q > 1 else 'an' if C[k]['long'][0] in 'AEIOU' else 'a'} {plural(C[k]['long']) if q > 1 else C[k]['long']}" for k, q in others]
                       + [f"{'a' if q == 1 else NUMW[q]} {w} W solar panel{'s' if q > 1 else ''}" for w, q in panels]))
    with_ = re.sub(r", ([^,]*)$", r" and \1", with_)
    head = f"Two BLUETTI {st} {'units' if st in ('FridgePower',) else 'stations'}" if n_st > 1 else f"The BLUETTI {st}"
    d["summary"] = (f"{head}{' sold as a pair' if not comps else ' with ' + with_} in one BLUETTI listing{', as a pre-order' if pre else ''}"
                    + (f": the bundle {roles[0]}" + (f" and {roles[1]}" if len(roles) > 1 else "") + "." if roles else
                       f": {num(wh)} Wh in all." if wh and not sep_units and others else "."))
    pw = "panels" if sum(q for _, q in panels) > 1 else "panel"
    d["fit"] = s["fit"] + ("" if not panels else f". The {pw} can refill the battery in a day or two of good sun." if s.get("cap") and wh and wh / (min(tot, s["cap"]) * 0.75) <= 12
                           else f". The {pw} {'are' if pw == 'panels' else 'is'} a top-up, not a daily refill, for a battery this size.") + ("" if panels else ".")
    cav = []
    if notes:
        cav.append(("Pre-order: " if pre else "") + "BLUETTI's page says: " + "; ".join(notes) + f" (read {DAY}).")
    late = [n for n in notes if _rank(n)[0] == 0 and re.search(r"nov\S*\s*9", n, re.I)]
    if late and any(w == 350 for w, _ in panels):
        cav.append("This listing's 350 W panel date (Nov. 9) has passed; BLUETTI's other listings give Dec 25 for the 350 W panel, so check the delivery estimate at checkout.")
        if next((r for _, r, t in WHEN if t == pre), -1) < 5:
            d["preorder"] = "Dec 25, 2026"
    cav.append(parts_line(st, n_st, comps, price))
    for k, _ in others:
        cav += C[k].get("cav", [])
    if not panels and not any(k == "SX4K" for k, _ in others) and st != "RV5":
        cav.append("No solar panel in the box.")
    cav += [c for c in s["cav"] if not ("MC4-to-XT60" in c and not panels)] + extra
    if any("delivered separately" in n for n in it.get("page_notes") or []):
        cav.append(SEP)
    d["caveats"] = cav
    return d


VARIANT_URL = {"un103", "un113", "un104", "un108", "un107", "un102", "un098", "un087", "un083"}   # variants of a station's own listing


def parts_line(st, n_st, comps, price):
    """What the same items cost bought singly at BLUETTI's US store that day, and how the bundle compares."""
    if any(C[k]["price"] is None for k, _ in comps if k not in PANELS):
        return "No parts comparison is made for this bundle (see the note on its home backup kit)."
    bats = [(k, q) for k, q in comps if k in ("B300K", "B500K")]
    items, total = [], 0.0
    rest = list(comps)
    if n_st == 1 and len(bats) == 1 and bats[0][1] >= 1 and (st, bats[0][0]) in BASE and BASE[(st, bats[0][0])] < PRICE_ST[st] + C[bats[0][0]]["price"]:
        k = bats[0][0]
        items.append(f"BLUETTI's {st} + {k} bundle ({money(BASE[(st, k)])})"); total += BASE[(st, k)]
        rest = [(kk, q - 1 if kk == k else q) for kk, q in comps]
        rest = [(kk, q) for kk, q in rest if q > 0]
    else:
        items.append(f"{'two ' if n_st > 1 else 'the '}{st}{' units' if n_st > 1 else ''} ({money(PRICE_ST[st])}{' each' if n_st > 1 else ''})"); total += n_st * PRICE_ST[st]
    for k, q in rest:
        if k in PANELS:
            p, nm, alone = K.PANEL[PANELS[k]][0], f"{PANELS[k]} W panel", ""
        else:
            p, nm, alone = C[k]["price"], C[k]["label"], (f", {C[k]['alone']}" if C[k].get("alone") else "")
        items.append(f"{'the' if q == 1 else NUMW[q]} {nm}{'s' if q > 1 and not nm.endswith('s') else ''} ({money(p)}{' each' if q > 1 else ''}{alone})"); total += q * p
    total = round(total, 2)
    diff = round(total - price, 2)
    lst = ", ".join(items[:-1]) + (" and " if len(items) > 1 else "") + items[-1]
    if diff > 0.5:
        return f"Bought separately at BLUETTI's US store on {DAY}, {lst} came to {money(total)}; this bundle saves {money(diff)}."
    if diff < -0.5:
        return f"Bought separately at BLUETTI's US store on {DAY}, {lst} came to {money(total)}, {money(-diff)} less than this bundle."
    return f"The bundle price equals {lst} bought separately at BLUETTI's US store on {DAY}."


# ---------------------------------------------------------------- cart tests
def tests():
    """{variant id: (control run, code run)}: the last pair whose subtotal is the item's price and whose control was rejected."""
    out, ctl = {}, {}
    if not TESTS.exists():
        return out
    for line in open(TESTS):
        r = json.loads(line)
        if r.get("error") or r.get("void") or "variant_id" not in r or abs(r["subtotal"] - r["expected_price"]) > 0.01:
            continue
        if r["code"] == "ZZNOTACODE7Q":
            if not r["applicable"]:
                ctl[r["variant_id"]] = r
        elif r["variant_id"] in ctl:
            out[r["variant_id"]] = (ctl[r["variant_id"]], r)
    return out


def records(groups=None, keep=None, need_test=True):
    tv = tests()
    out, dropped = [], []
    for g in sorted(GROUPS):
        if groups and g not in groups:
            continue
        for row in GROUPS[g][1]:
            d = globals()[GROUPS[g][0]](*row)
            d["_group"] = g
            t = tv.get(d["cart_variant"])
            if keep is not None and d["slug"] not in keep:
                continue
            if d["slug"] in SKIP:
                dropped.append((d["slug"], SKIP[d["slug"]])); continue
            if need_test and not t:
                dropped.append((d["slug"], "no valid cart test yet")); continue
            if need_test and not (t[1]["applicable"] and t[1]["code_amount"] > 0):
                dropped.append((d["slug"], "code DEALECTRIC was rejected in the cart")); continue
            if t:
                d["_test"] = {"date": t[1]["checked_at"][:10], "product": d["slug"], "qty": 1, "subtotal": t[1]["subtotal"], "discount": t[1]["code_amount"]}
                if t[0]["total"] < t[0]["subtotal"] - 0.005:
                    d["_test"]["no_code_total"] = t[0]["total"]
                d["_runs"] = t
            out.append(d)
    return out, dropped


BEGIN = "# >>> DLC-321 phase 3, BLUETTI store items prepared 2026-11-18: generated by growth/focus/offers/bluetti_1118.py (re-run `apply`; do not edit by hand)\n"
END = "# <<< DLC-321 phase 3\n"
ANCHOR = "{\"slug\": 'bluetti-elite-200-v2-charger-1-bundle',"


def literal(d):
    lines = [f' "{k}": {v!r},' for k, v in d.items() if not k.startswith("_")]
    return "{" + "\n".join(lines)[1:].rstrip(",") + "},\n"


def apply(groups, keep, need_test=True):
    recs, dropped = records(groups, keep, need_test)
    path = ROOT / "src" / "products.py"
    s = open(path).read()
    i = s.find(BEGIN)
    if i >= 0:
        s = s[:i] + s[s.index(END, i) + len(END):]
    dup = [d["slug"] for d in recs if re.search(r"[\"']slug[\"']: [\"']" + re.escape(d["slug"]) + r"[\"']", s)]
    assert not dup, f"already in products.py: {dup}"
    assert s.count(ANCHOR) == 1
    if recs:
        s = s.replace(ANCHOR, BEGIN + "\n".join(literal(d) for d in recs) + END + ANCHOR)
    open(path, "w").write(s)
    path = ROOT / "src" / "coupons.json"
    Cj = json.load(open(path))
    code = next(c for c in Cj["codes"] if c["brand"] == "BLUETTI" and c["code"] == "DEALECTRIC")
    ours = {row[1] for _, rows in GROUPS.values() for row in rows}
    code["tests"] = [t for t in code["tests"] if t["product"] not in ours] + [d["_test"] for d in recs if "_test" in d]
    with open(path, "w") as f:   # the layout tools/codes_merge.py writes: one code per line
        f.write('{\n "_notes": ' + json.dumps(Cj["_notes"], ensure_ascii=False) + ',\n "checked": ' + json.dumps(Cj["checked"]) + ',\n "codes": [\n')
        f.write(",\n".join("  " + json.dumps(c, ensure_ascii=False) for c in Cj["codes"]) + "\n ]\n}\n")
    print(f"applied {len(recs)} records; not written: {dropped}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    keep = set(sys.argv[sys.argv.index("--keep") + 1].split(",")) if "--keep" in sys.argv else None
    groups = {int(x) for x in sys.argv[sys.argv.index("--group") + 1].split(",")} if "--group" in sys.argv else None
    if cmd == "apply":
        apply(groups, keep, "--untested" not in sys.argv)   # --untested: only to let the best-offer tools read a slug before its cart test lands; never commit that state
    elif cmd == "slugs":
        print(" ".join(d["slug"] for d in records(groups, keep, "--untested" not in sys.argv)[0]))
    elif cmd == "print":
        for d in records(groups, keep, need_test="--all" not in sys.argv)[0]:
            print(json.dumps({k: v for k, v in d.items() if k != "_runs"}, ensure_ascii=False, indent=1))
    elif cmd == "cartfile":
        with open(sys.argv[2], "w") as f:
            for d in records(groups, keep)[0]:
                f.write(json.dumps({"slug": d["slug"], "price": d["price"], "code": "DEALECTRIC", "runs": list(d["_runs"])}) + "\n")
    elif cmd == "report":
        recs, dropped = records(groups, keep)
        for d in recs:
            t = d["_test"]
            print(f"| {d['slug']} | {money(d['price'])} | {money(round(d['price'] - t['discount'], 2))} | {money(t['no_code_total']) if 'no_code_total' in t else '-'} | {d.get('preorder') or 'ships now'} |")
        for x in dropped:
            print("DROPPED", x)
