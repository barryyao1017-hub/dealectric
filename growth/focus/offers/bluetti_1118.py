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
 "CAB30TT": dict(label="30A TT-30 AC Charging Cable", long="30 A TT-30 fast charging cable", price=79, row=("Charging cable", "30 A NEMA TT-30 fast charging cable"), role="charges from a 30 A RV pedestal or generator outlet"),
 "CAB30": dict(label="30A AC Charging Cable", long="30 A AC charging cable", price=99, row=("Charging cable", "30 A AC charging cable for the Apex 300"), role="charges from a 30 A outlet"),
 "CAB50": dict(label="50A AC Charging Cable", long="50 A AC charging cable", price=129, row=("Charging cable", "50 A AC charging cable for the Apex 300"), role="charges from a 50 A outlet"),
 "DISP1": dict(label="Display 1", long="Display 1 magnetic screen", price=99, row=("Display", "Display 1: magnetic external screen with a 2,000 mAh battery, 155 g (BLUETTI)"), role="shows the battery level without opening the app"),
 "BAG": dict(label="Carrying Bag", long="carrying bag", price=69, row=("Bag", "BLUETTI carrying case bag"), role="comes with a carrying bag"),
 "EPANEL": dict(label="Epanel", long="Epanel smart distribution panel", price=499, row=("Distribution panel", "Epanel smart distribution panel"), role=None),
 "EPAD": dict(label="Epad", long="Epad control screen", price=399, row=("Control screen", "Epad central control screen"), role=None),
}
PANELS = {"P60": 60, "P100": 100, "P200": 200, "P350": 350, "P500": 500}

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
 ("un048", "bluetti-apex-300-b500k-charger-2-dc-hub-2x350w-50a-cable-solar-kit", "Apex 300", 1, [("B500K", 1), ("C2", 1), ("DCHUB", 1), ("P350", 2), ("CAB50", 1)], []),
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
GROUPS = {1: G1}
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
        n = re.sub(r"^(likely: |Order today—)", "", n.strip()).rstrip(".")
        if not n or n in ("False", "True") or "delivered separately" in n or not re.search(r"ship|restock", n, re.I):
            continue
        for p in [x.strip().rstrip(".") for x in re.split(r";|\.\s+(?=[A-Z]|\d+\s*W)", n) if x.strip()]:
            m = re.match(r"(?:The )?(\d+)\s*W\b", p)
            if (m and int(m.group(1)) not in watts) or re.match(r"All other", p) or not re.search(r"ship|restock", p, re.I):
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
         "_qid": qid, "name": f"BLUETTI {title} {kind} ({whtxt}, {wtxt})", "model": title,
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
    with_ = ", ".join(([f"{'two' if q == 2 else 'three' if q == 3 else 'an' if C[k]['long'][0] in 'AEIOU' else 'a'} {plural(C[k]['long']) if q > 1 else C[k]['long']}" for k, q in others]
                       + [f"{'a' if q == 1 else {2: 'two', 3: 'three'}[q]} {w} W solar panel{'s' if q > 1 else ''}" for w, q in panels]))
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
        items.append(f"{'the' if q == 1 else {2: 'two', 3: 'three'}[q]} {nm}{'s' if q > 1 and not nm.endswith('s') else ''} ({money(p)}{' each' if q > 1 else ''}{alone})"); total += q * p
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
        for row in GROUPS[g]:
            d = record(*row)
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


def apply(groups, keep):
    recs, dropped = records(groups, keep)
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
    ours = {row[1] for g in GROUPS.values() for row in g}
    code["tests"] = [t for t in code["tests"] if t["product"] not in ours] + [d["_test"] for d in recs]
    with open(path, "w") as f:   # the layout tools/codes_merge.py writes: one code per line
        f.write('{\n "_notes": ' + json.dumps(Cj["_notes"], ensure_ascii=False) + ',\n "checked": ' + json.dumps(Cj["checked"]) + ',\n "codes": [\n')
        f.write(",\n".join("  " + json.dumps(c, ensure_ascii=False) for c in Cj["codes"]) + "\n ]\n}\n")
    print(f"applied {len(recs)} records; not written: {dropped}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    keep = set(sys.argv[sys.argv.index("--keep") + 1].split(",")) if "--keep" in sys.argv else None
    groups = {int(x) for x in sys.argv[sys.argv.index("--group") + 1].split(",")} if "--group" in sys.argv else None
    if cmd == "apply":
        apply(groups, keep)
    elif cmd == "slugs":
        print(" ".join(d["slug"] for d in records(groups, keep)[0]))
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
