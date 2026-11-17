#!/usr/bin/env python3.12
"""Open queries, second pass (Barry 2026-11-16/17 via the fork session: "Did we create pages for the open queries + the
semi demanded queries? if not build pages for them first"). Every query that stayed open in repeat chats gets a NEW page
(never a rebuild), one page per search: queries whose ChatGPT search matches another's are merged, and queries whose
search matches an existing page are left to that page (see SERVED). Built on growth/focus/open-pages/openpage.py and the
bluetti-four rules; research runs in-session while claude -p is at its weekly limit (growth/focus/open2/inses.py).

    python3.12 growth/focus/open2/pages2.py harvest|links|apply|status [folder...]
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[2]
sys.path.insert(0, str(ROOT / "growth/focus/bluetti-four"))
import pages as BP  # noqa: E402  (registers the bluetti pages and the openpage patches)
O = BP.O
RUN = "open2-1117"
T = {t["qid"]: t for t in json.loads(Path("/Users/j0y0825/code/dealectric/growth/focus/open-queries/targets-22.json").read_text())}
SL = "/Users/j0y0825/code/dealectric/growth/evals/runs/2026-11-15-shortlist/"


def files(*qids):
    out = []
    for q in qids:
        if q in T:
            out += [c["file"] for c in T[q]["chats"]]
        else:
            out += [str(p) for p in sorted(Path(SL).glob(q + "-*.json"))]
    return out


NONE = "no measured search demand (open in repeat chats of the discovery run)"
GENERIC = ("Its core is one table of the measured result the question asks for, per product, each figure with the named tester or "
           "the maker's stated figure (labelled) and the date read; arithmetic labelled with its one-line sum. Prefer products "
           "Dealectric lists or can link through a confirmed Amazon listing where they honestly win.")


def page(qids, query, demand, featured, extra, slug, existing_link=None):
    link = f" Link Dealectric's related page /{existing_link} once." if existing_link else ""
    return {"run": RUN, "flags": {"buy_by_name": True}, "query": query, "files": files(*qids), "qids": list(qids),
            "rules": BP.rules(query, demand, featured, f"This is a NEW page.{link} {GENERIC} {extra} Slug: {slug}.").format(
                brief="(no product brief: research the products directly)")}


PAGES = {
    # Group 1: some search demand
    "o2-car-charging-fastest": page(["pq006"], "which power station can charge the fastest from a car", "small: related 'solar generator for rv' 260; no direct count",
        "BLUETTI Elite 200 V2 + Charger 1 bundle (bluetti-elite-200-v2-charger-1-bundle) and other alternator-charger kits we list",
        "Measured result: watts or hours from a car, with and without a dedicated alternator charger; say which needs extra hardware.",
        "power-station-that-charges-fastest-from-a-car"),
    "o2-enclosed-printer-fastest-abs": page(["pn010"], "which enclosed 3d printer is the fastest at printing abs", "the 'enclosed 3d printer' cluster, 834",
        "QIDI's enclosed printers on our Awin program (qidi-plus5, qidi-max4, qidi-q2)",
        "Measured result: real ABS print time or measured speed on a stated test part, not the maker's top speed alone. Distinct from "
        "/enclosed-3d-printer-that-heats-up-fastest (heat-up time).", "enclosed-3d-printer-fastest-at-printing-abs", "enclosed-3d-printer-that-heats-up-fastest"),
    "o2-wifi-router-longest": page(["pm014", "pm015"], "which power station keeps a wifi router running the longest", "small; no direct count",
        "the BLUETTI Elite 30 V2 and other small stations we list",
        "Measured result: hours a router runs, which depends on idle draw on DC (USB and 12 V) vs AC; also answer the second question "
        "'which power station loses the least power when you only use the usb and 12 volt ports' in one after-section h2.",
        "power-station-that-keeps-a-wifi-router-running-longest", "small-power-station-to-keep-wifi-router-and-modem-on-in-an-outage"),
    "o2-biggest-appliances-for-size": page(["pm004"], "which power station can start the biggest appliances for its size", NONE,
        "the BLUETTI Elite 100 V2 and other stations we list", "Measured result: surge or overload watts held for a stated time, per pound "
        "(arithmetic), with which makers state durations.", "power-station-that-starts-the-biggest-appliances-for-its-size"),
    "o2-whole-house-backup-without-solar": page(["vq021", "dq004"], "whole house battery backup without solar", "'whole house battery backup without solar' 317; whole-house cluster 4,754",
        "plug-in home batteries we list or link (anker-solix-s5000, anker-solix-f3800-plus, bluetti-apex-300, jackery-explorer-5000-plus, ecoflow-titan-5000-plus)",
        "Measured result: energy delivered and recharge time from the grid (no solar) for a whole-house setup, and the cheapest set-up that "
        "runs a fridge, lights and a furnace fan (the second question) with arithmetic. Installed systems (Powerwall, FranklinWH) as context rows.",
        "whole-house-battery-backup-without-solar", "best-home-battery-backup-system"),
    "o2-rv-30-amp": page(["dq020"], "which solar generator is best for an rv with a 30 amp plug", "'solar generator with 30 amp rv plug' 113; 30 amp cluster 202",
        "stations with a TT-30 outlet we list or link", "Measured result: which units have a real TT-30R outlet, its rated amps/watts, and "
        "hours of RV loads (arithmetic from measured usable energy).", "solar-generator-for-an-rv-with-a-30-amp-plug"),
    "o2-new-2026-worth-it": page(["dq006"], "which solar generators that came out in 2026 are worth buying over older models", "'best solar generators 2026' 4,813; cluster 5,517",
        "2026 models we list (bluetti-pioneer-na, bluetti-elite-100-mini, ecoflow-delta-3-ultra, jackery-explorer-5000-plus, dji-power-1000-v2)",
        "Measured result: for each 2026 model, the measured gain over the older model it replaces (usable energy, idle draw, recharge "
        "time, weight), and where the older model is the better buy.", "solar-generators-released-in-2026-worth-buying"),
    # Group 2: open in repeat chats, no measured demand
    "o2-240v-one-unit-or-two": page(["fk010", "pq021"], "which power stations can run 240 volt appliances like a well pump from one unit", NONE,
        "240 V units we list or link (bluetti-apex-300, anker-solix-f3800-plus, anker-solix-s5000, jackery-explorer-5000-plus, ecoflow-titan-5000-plus)",
        "Measured result: 240 V watts from ONE unit and whether it starts a well pump (surge held, named test), and when two linked units are needed.",
        "power-stations-that-run-240-volt-appliances-from-one-unit", "solar-generator-that-can-run-a-well-pump"),
    "o2-pellet-stove-longest": page(["pm026"], "which power station runs a pellet stove the longest", NONE, "stations we list",
        "Measured result: hours of pellet-stove running (ignition + running watts from stove manuals) per station, arithmetic shown.",
        "power-station-that-runs-a-pellet-stove-the-longest", "power-station-to-run-a-pellet-stove-in-an-outage"),
    "o2-solar-recharge-fastest": page(["pp004", "pm022"], "which solar generator recharges fastest from solar panels in one day", NONE,
        "stations we list with high solar input", "Measured result: hours of sun to refill (battery Wh / usable solar input), with "
        "measured solar input where tested; also answer 'which power station takes the fewest hours of sun to refill with two panels' "
        "in one after-section h2. Distinct from the kits-with-panels page: this one compares bare stations by their maximum solar "
        "input with whatever panels the buyer adds, so the title must say so (for example 'with the panels you add' or 'by maximum "
        "solar input'), not 'panels included'.", "solar-generator-that-recharges-fastest-from-solar", "solar-generator-with-panels-included-fastest-recharge"),
    "o2-linked-together": page(["pq016"], "which power stations can be linked together for more power", NONE, "units we list that link or parallel",
        "Measured result: combined output and 240 V when two units are linked, with the exact kit or cable needed (maker document).",
        "power-stations-that-can-be-linked-together"),
    "o2-fan-most-nights": page(["pr006"], "which power station runs a fan all night for the most nights", NONE, "stations we list",
        "Measured result: nights of a fan (box, pedestal, DC fan; stated watts) per charge, from measured usable energy and idle draw.",
        "power-station-that-runs-a-fan-all-night-for-the-most-nights", "power-station-for-cpap"),
    "o2-charge-freezing": page(["pp006", "fm035"], "which power stations still charge in freezing weather", NONE,
        "bluetti-pioneer-na and other stations we list with low-temperature charging",
        "Measured result: lowest charging temperature (maker) and any named cold test; also answer 'which can charge from solar panels "
        "below freezing for winter camping' in one after-section h2.", "power-stations-that-charge-in-freezing-weather"),
    "o2-advertised-capacity": page(["pp002"], "which power station gives you the most of its advertised capacity in real use", NONE, "stations we list",
        "Measured result: usable Wh as a share of rated Wh from named discharge tests, same lab where possible.",
        "power-station-that-gives-the-most-of-its-advertised-capacity"),
    "o2-3d-scanner-car-part": page(["pn005"], "which 3d scanner is the fastest for scanning a big car part", NONE,
        "EINSTAR and Revopoint scanners we list (einstar-2, einstar-rockit, einstar-vega, revopoint-metrox-3d-scanner)",
        "Measured result: scan speed (points or frames per second, maker) and a named large-part test where one exists; professional "
        "scanners as context rows; our scanners win the consumer segment only if the figures say so.", "fastest-3d-scanner-for-a-big-car-part"),
    "o2-robot-mower-wet-grass": page(["ps003"], "which robot mower mows best in wet grass", NONE, "MOVA and ANTHBOT mowers we list (mova-lidax-ultra-1000, mova-lidax-ultra-2000, anthbot-n8, anthbot-m5-lidar)",
        "Measured or tested result in wet grass (named tests), drive type and rain sensor behaviour; if no mower we list has any wet-grass "
        "evidence, return status skip.", "robot-mower-that-mows-best-in-wet-grass"),
    # Group 3: different search from the DLC-272 test page it resembles
    "o2-fan-noise-fridge-night": page(["pq023"], "which power station makes the least fan noise when running a fridge at night", NONE, "stations we list",
        "Measured result: fan noise (dB, distance) at a fridge-sized low AC load, and whether the fan stays off; distinct from charging noise.",
        "power-station-with-the-least-fan-noise-running-a-fridge-at-night"),
}
SERVED = {"pr008": "1000wh-power-station-that-can-run-a-microwave (DLC-272 test page; same ChatGPT search, overlap 0.63)",
          "pm005": "portable-power-station-1000w and lightest-1000wh-lifepo4-power-station-for-car-camping (same search, overlap 0.74 / 0.61)",
          "vq014": "best-solar-generator-for-power-outages (same search as ac030)"}
O.PAGES.update(PAGES)
O.IN_SCOPE |= set(PAGES)

if __name__ == "__main__":
    sys.argv = [sys.argv[0], *sys.argv[1:]] if len(sys.argv) > 2 else [sys.argv[0], sys.argv[1], *PAGES]
    sys.exit(O.main())
