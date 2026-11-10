#!/usr/bin/env python3.12
"""Hand-curated Black Friday / Cyber Monday 2026 brand entries for src/bfcm.json, from growth/bfcm/research-*.json
(brand-site reads, 2026-11-10) and the CJ / Awin offer reads (growth/bfcm/*-2026-11-10.json). Every phase is the
brand's own wording, shortened; "seen" marks a sale running with no published dates.

    python3.12 growth/bfcm/curated.py    # rewrites src/bfcm.json "brands"
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEEN = "2026-11-10"


def ph(name, start=None, end=None, headline=None, url=None):
    d = {"name": name, "start": start, "end": end, "headline": headline, "url": url}
    if not (start or end):
        d["seen"] = SEEN
    return {k: v for k, v in d.items() if v is not None}


def ly(name, start, end, headline, url=None):
    return {k: v for k, v in {"name": name, "start": start, "end": end, "headline": headline, "url": url}.items() if v}


B = {
    # ---- group 1
    "3DMakerpro": {},
    "AGM": {},
    "ALLPOWERS": {"phases": [ph("Black Friday codes from ALLPOWERS's affiliate program", "2026-10-28", "2026-12-14",
                                "APBF10 10% off sitewide; APBF12 12% off orders over $1,000", "https://iallpowers.com/")],
                  "last_year": ly("Biggest Black Friday Sale", "2025-11-24", None, "record-low prices on the R2500, R1500 and R1500 Lite",
                                  "https://www.prnewswire.com/news-releases/allpowers-launches-biggest-black-friday-sale-big-savings-on-portable-power-stations-and-solar-generators-302624646.html")},
    "AOHi": {"phases": [ph("Power Bank Week", "2026-11-09", "2026-11-14", "15% off all power banks", "https://www.iaohi.com/")]},
    "AOSU": {"phases": [ph("Early Black Friday Deals", None, None, "up to 65% off security cameras", "https://www.aosulife.com/pages/sales")]},
    "AV Access": {"last_year": ly("Black Friday and Cyber Monday", "2025-11-21", None, "4% off the iDock M10 at launch",
                                  "https://business.mammothtimes.com/mammothtimes/article/abnewswire-2025-11-21-av-access-unveils-idock-m10-a-4k-dual-monitor-kvm-docking-station-designed-for-macbook-users")},
    "Amazfit": {},
    "Anker SOLIX": {"phases": [ph("Black Friday Early Access", "2026-11-10", "2026-11-18", "up to 54% off, plus a free solar panel on large orders", "https://www.ankersolix.com/black-friday-pps")]},
    "Arenti": {"phases": [ph("Black Friday Early Access", "2026-11-05", "2026-12-03", "up to 77% off; $20 off orders over $150, $40 off over $250", "https://arenti.com/pages/deal")]},
    "Aurzen": {},
    "BIQU": {"phases": [ph("Black Friday Early Access", "2026-11-07", "2026-11-15", "up to 40% off", "https://biqu.equipment/pages/2026-biqu-shining-go-sale"),
                        ph("Black Friday Sale", "2026-11-16", "2026-12-02", "up to 60% off, free gifts", "https://biqu.equipment/pages/2026-biqu-shining-go-sale")]},
    "BLUETTI": {"phases": [ph("Black Friday Early Access", "2026-11-05", "2026-11-18", "$50 off orders over $2,000, $100 over $3,000, $150 over $4,000; Apex 200 at $1,099",
                              "https://www.bluettipower.com/pages/black-friday")],
                "last_year": ly("Black Friday", "2025-11-15", "2025-12-03", "up to about 56% off")},
    "Baseus": {},
    "Birdfy": {"phases": [ph("Black Friday", "2026-11-03", "2026-11-28", "up to 55% off, free lifetime Bird ID", "https://www.birdfy.com/pages/black-friday"),
                          ph("Christmas Sale", "2026-12-02", "2026-12-28", "up to 55% off", "https://www.birdfy.com/")]},
    "Blackview": {"phases": [ph("Black Friday", None, None, "\"lowest price of the year\" tags, about 14–34% off", "https://store.blackview.hk/en-us/collections/black-friday")]},
    "Botslab": {"phases": [ph("Black Friday / Cyber Monday Sale", None, None, "\"lowest price of the year\" sitewide; extra 20% off bundles at checkout", "https://www.botslab.com/pages/black-friday")]},
    "CarpuTech": {"phases": [ph("Black Friday Sale", None, None, "codes BLKSALE35 ($35 off $299+), BLKSALE65 ($65 off $599+), BLKSALE100 ($100 off $999+)", "https://www.carputech.com/")]},
    "EKSA": {},
    # ---- group 3
    "OM System": {"phases": [ph("Black Friday Pricing Now", "2026-11-04", "2026-11-26", "up to $400 off cameras, up to $600 off select lenses; TG-7 $579.99", "https://explore.omsystem.com/us/en/tg-7-black"),
                             ph("Holiday Deals", "2026-11-03", "2027-01-10", "holiday prices on cameras and lenses", "https://explore.omsystem.com/us/en/")]},
    "OSCAL": {"phases": [ph("Black Friday", None, None, "up to 50% off", "https://store.oscal.hk/pages/black-friday")],
              "last_year": ly("Black Friday", "2025-11-19", "2025-12-03", "up to 70% off")},
    "Petcube": {"last_year": ly("Black Friday", "2025-11-20", None, "up to 52% off; Bites 2 Lite $70", "https://9to5toys.com/2025/11/20/petcube-smart-cameras-gps-fountains-black-friday-from-26/")},
    "QIDI": {"phases": [ph("Black Friday Sale", "2026-11-02", "2026-12-06", "Max4 $1,049, Plus5 $699, Q2 $449; codes 30for700 ($30 off $700+) and 50for1000 ($50 off $1,000+)",
                           "https://qidi3d.com/pages/black-friday-sale")]},
    "Redodo": {"phases": [ph("Black Friday First Dibs", "2026-11-04", "2026-12-06", "up to 56% off LiFePO4 batteries", "https://www.redodopower.com/pages/redodo-batteries-black-friday-deals")],
               "last_year": ly("Black Friday", "2025-11-03", "2025-12-07", "up to 70% off", "https://www.redodopower.com/blogs/learn-about-lithium/redodo-black-friday-battery-deals-2025")},
    "Revopoint": {"phases": [ph("Black Friday Sale", "2026-11-09", "2026-11-30", "INSPIRE 2, MetroX and MetroX Pro 30% off, MINI 2 20% off; extra 5% with code REVOB5NEWS",
                                "https://www.revopoint3d.com/blogs/news/revopoint-black-friday-sale-is-here-save-up-to-50-on-3d-scanners")]},
    "SIRUI": {"phases": [ph("Early Bird Deal", "2026-11-09", "2026-11-15", "up to 80% off", "https://store.sirui.com/pages/sales-1"),
                         ph("BFCM Big Sale", "2026-11-16", "2026-11-30", "\"the biggest savings of the year\"", "https://store.sirui.com/pages/sales-1"),
                         ph("Black Friday affiliate code", "2026-11-01", "2026-12-31", "8% off with code AFFSRBFBO", "https://store.sirui.com/")]},
    "Soundcore": {"phases": [ph("Black Friday Early Access", "2026-11-09", "2026-11-18", "up to 46% off, members-only daily deals", "https://www.soundcore.com/best-deals"),
                             ph("Black Friday", "2026-11-19", "2026-11-30", "Black Friday prices for everyone", "https://www.soundcore.com/best-deals")]},
    "Sun Gold Power": {"phases": [ph("Black Friday Cyber Monday Sale", None, None, "up to 35% off", "https://sungoldpower.com/collections/special-offer")]},
    "Syncwire": {},
    "TEAC": {},
    "TESSAN": {"phases": [ph("Black Friday, step 2", "2026-11-14", "2026-11-20", "up to 20% off", "https://tessan.com/pages/black-friday"),
                          ph("Black Friday, step 1", "2026-11-01", "2026-11-13", "up to 15% off", "https://tessan.com/pages/black-friday"),
                          ph("Black Friday, step 3", "2026-11-21", "2026-11-26", "up to 25% off", "https://tessan.com/pages/black-friday"),
                          ph("Black Friday and Cyber Monday peak", "2026-11-27", "2026-12-04", "35–40% off, no code needed", "https://tessan.com/pages/black-friday")],
               "last_year": ly("Black Friday", "2025-11-20", "2025-12-04", "30% off")},
    "Tenergy": {},
    "UGREEN": {"phases": [ph("NAS Black Friday Early Deals", "2026-11-09", "2026-11-18", "up to 32% off NAS bundles", "https://nas.ugreen.com/pages/ugreen-nas-black-friday-deals"),
                          ph("NAS Black Friday", "2026-11-19", "2026-11-30", "DXP2800 $379.99, DXP480T Plus $799.99, DXP4800 Plus $656.99", "https://nas.ugreen.com/pages/ugreen-nas-black-friday-deals")]},
    "Vatrer": {"phases": [ph("Thanksgiving & Black Friday Sale", None, "2026-11-30", "up to $2,400 off; code VIPD2026", "https://www.vatrerpower.com/pages/vatrer-lithium-battery-special-deals")]},
    "Wasserstein": {},
    "Wuben": {"last_year": ly("Black Friday", "2025-11-21", None, "up to 60% off; E7 $23.99", "https://www.wubenlight.com/blogs/news/wuben-2025-black-friday-sale-exploring-the-best-deals-of-the-year")},
    "Xencelabs": {"phases": [ph("Black Friday & Cyber Monday Special", None, None, "up to 57% off", "https://www.xencelabs.com/us/store/pen-tablets")],
                  "last_year": ly("Black Friday", "2025-11-19", None, "up to 30% off", "https://www.xencelabs.com/community/creative-corner/black-friday-drawing-tablet-deals")},
    "Zowietek": {"phases": [ph("11.11 Sale", "2026-10-27", "2026-11-15", "up to 16% off, taken off at checkout", "https://zowietek.com/")]},
    # ---- from the networks only (group 2 adds the brand-site reads)
    "ESR": {"phases": [ph("Black Friday codes from ESR's affiliate program", "2026-11-05", "2026-11-18", "12% off one product, 20% off two, 25% off three", "https://www.esrtech.com/")]},
    "K&F Concept": {"phases": [ph("Black Friday 2026", "2026-11-09", "2026-11-30", "20% off sitewide with code KFDEAL20", "https://www.kentfaith.com/")]},
}

TESSAN_ORDER = ["Black Friday, step 1", "Black Friday, step 2", "Black Friday, step 3", "Black Friday and Cyber Monday peak"]
B["TESSAN"]["phases"].sort(key=lambda p: TESSAN_ORDER.index(p["name"]))


def main():
    extra = ROOT / "growth/bfcm/curated-extra.json"   # groups 2 and 4, written after their research lands
    if extra.exists():
        B.update(json.loads(extra.read_text()))
    bf = json.loads((ROOT / "src/bfcm.json").read_text())
    bf["brands"] = {b: {"checked": SEEN, **{k: v for k, v in d.items() if v}} for b, d in sorted(B.items())}
    bf["new_brands_joined"] = "Nov 8–10, 2026"
    (ROOT / "src/bfcm.json").write_text(json.dumps(bf, indent=1, ensure_ascii=False) + "\n")
    print(f"{len(B)} brands, {sum(1 for d in B.values() if d.get('phases'))} with a 2026 sale")


if __name__ == "__main__":
    main()
