"""Product research, third batch (fork session's final list, 2026-11-15): products with no catalog card and no panel
seller in ChatGPT's where-to-buy checks that we can link and that have no record yet. Same agent and output as
research2.py. Nature's Generator is on our Awin program; the rest are Amazon-only (brand's own listing, or skip)."""
import json, sys, concurrent.futures as cf
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
import research2 as R

R.PRODUCTS = {
    "natures-generator-powerhouse": ("Nature's Generator Powerhouse (7,200 W whole-home unit; ChatGPT typed \"Nature's Generator Powerhouse 7200W\")", "Powerhouse", "program",
        "Our Awin program awin:naturesgenerator (store https://www.naturesgenerator.com/, no active code). Find the current US "
        "Powerhouse listing on naturesgenerator.com (ChatGPT's results named 'Powerhouse V2 Whole Home Generator', $2,799.99 at a "
        "reseller), its price today and whether it is in stock. If naturesgenerator.com doesn't sell it, return record null."),
    "dabbsson-2000l": ("Dabbsson 2000L", "Dabbsson", "amazon", "Find Dabbsson's own Amazon listing (sold by Dabbsson or Amazon)."),
    "vtoman-flashspeed-1500": ("VTOMAN FlashSpeed 1500", "VTOMAN", "amazon", "Find VTOMAN's own Amazon listing."),
    "dji-power-1000": ("DJI Power 1000 (say whether the current model is the Power 1000 or Power 1000 V2)", "DJI Power 1000", "amazon",
        "We already link a DJI Power 1000 V2 Amazon listing B0H2MFBDZL as a table row. Find DJI's own Amazon listing for the model "
        "ChatGPT names; if it is the V2, confirm B0H2MFBDZL."),
    "goal-zero-yeti-1500x": ("Goal Zero Yeti 1500X", "Yeti 1500X", "amazon", "Find Goal Zero's own Amazon listing."),
    "ecoflow-titan-5000-plus": ("EcoFlow TITAN 5000 Plus", "TITAN", "amazon", "Find EcoFlow's own Amazon listing."),
}
R.DEMAND = R.DEMAND + "\nvtoman portable power station 185; vtoman power station 104; goal zero power station 247; dji power station 82. No volume found for Dabbsson, TITAN 5000 Plus or Nature's Generator Powerhouse."
_orig = R.prompt


def prompt(key):
    t = _orig(key)
    if R.PRODUCTS[key][2] == "program":
        t = (t.replace('"<bluetti-...>"', '"natures-generator-powerhouse-..."').replace('"BLUETTI", "program": "awin:bluetti_us"', '"Nature\'s Generator", "program": "awin:naturesgenerator"')
              .replace("<bluettipower.com product url>", "<naturesgenerator.com product url>").replace("from BLUETTI's page or manual", "from the maker's page or manual")
              .replace("<from BLUETTI's warranty page, with the page>", "<maker's warranty, with the page>").replace("<from BLUETTI's returns policy>", "<maker's returns policy>"))
    return t


R.prompt = prompt

if __name__ == "__main__":
    keys = sys.argv[1:] or list(R.PRODUCTS)
    with cf.ThreadPoolExecutor(max_workers=6) as ex:
        for r in ex.map(R.run, keys):
            print(json.dumps(r), flush=True)
    print("PRODUCT RESEARCH 3 DONE", flush=True)
