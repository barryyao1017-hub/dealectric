"""Demand check for the open queries (2026-11-15): exact Bing US search counts for a few short keywords per topic, from
Bing Webmaster Tools' GetKeywordStats (gapmine.bwt), summed over the latest 13 weekly rows. A keyword with no rows is
below Bing's reporting threshold. Bing is a small share of search, so read the numbers as relative size between
topics, not as market size. The keywords are the short forms a searcher types, written by hand per topic."""
import json, sys, time
sys.path.insert(0, 'growth/evals')
import gapmine as G
T = {
 "ac030": ("best solar generator for home use", ["best solar generator for home use", "solar generators for home use", "solar generator for house", "home solar generator", "whole house solar generator"]),
 "fk010": ("240 volt well pump on a power station", ["well pump battery backup", "solar generator for well pump", "power station for well pump", "generator for well pump", "how to run well pump during power outage"]),
 "pm004": ("starts the biggest appliances for its size", ["solar generator to run refrigerator", "power station to run refrigerator", "what size solar generator to run refrigerator", "power station for air conditioner", "solar generator for air conditioner"]),
 "pm014": ("keeps a wifi router running the longest", ["battery backup for router", "ups for router", "mini ups for wifi router", "router battery backup", "power station for router"]),
 "pm022": ("recharges fastest from solar (two queries)", ["solar generator charging time", "how long to charge solar generator", "fastest charging solar generator", "fast charging power station", "fastest charging power station"]),
 "pm026": ("runs a pellet stove the longest", ["pellet stove battery backup", "battery backup for pellet stove", "pellet stove power outage", "pellet stove ups", "power station for pellet stove"]),
 "pq016": ("linked together for more power", ["parallel power station", "connect two power stations", "expandable power station", "expandable solar generator", "stackable power station"]),
 "pq023": ("least fan noise running a fridge at night", ["quietest power station", "quiet power station", "quiet solar generator", "silent generator", "quietest portable generator"]),
 "pq025": ("cpap for the most nights", ["cpap battery backup", "cpap battery", "power station for cpap", "cpap battery for camping", "portable cpap battery"]),
 "pr006": ("fan all night for the most nights", ["battery powered fan for power outage", "fan for power outage", "power station fan", "solar powered fan", "how to run a fan without electricity"]),
 "pr008": ("lightest that can run a microwave", ["power station for microwave", "can a power station run a microwave", "lightest power station", "lightweight power station", "solar generator to run microwave"]),
 "pp006": ("still charge in freezing weather (two queries)", ["power station cold weather", "solar generator in winter", "lifepo4 cold weather", "power station in freezing temperatures", "lifepo4 charging below freezing"]),
 "pm005": ("smallest 1,000 watt hour station", ["smallest 1000wh power station", "compact power station", "small power station", "smallest power station", "mini power station"]),
 "pm015": ("least power lost on usb and 12 volt", ["power station efficiency", "power station idle consumption", "12v power station", "power station dc output", "power station standby power"]),
 "pp002": ("most of its advertised capacity", ["power station usable capacity", "power station capacity", "power station actual capacity", "how long will a power station last", "power station runtime"]),
 "pq006": ("charges fastest from a car", ["alternator charger for power station", "charge power station from car", "power station car charger", "ecoflow alternator charger", "charge power station while driving"]),
 "pq021": ("240 volt appliances from one unit", ["240v power station", "240v solar generator", "240 volt solar generator", "power station 240v output", "solar generator for dryer"]),
 "pn010": ("enclosed 3D printer fastest at ABS", ["best 3d printer for abs", "enclosed 3d printer", "fastest 3d printer", "abs 3d printer", "best enclosed 3d printer"]),
 "pn005": ("3D scanner fastest for a big car part", ["3d scanner for car parts", "automotive 3d scanner", "3d scanner for large objects", "best 3d scanner for cars", "3d scanner for reverse engineering"]),
 "ps003": ("robot mower in wet grass", ["robot mower in rain", "robot lawn mower rain", "can robot mowers mow wet grass", "robotic mower wet grass", "robot mower rain sensor"]),
}
out = {"queries": {}}
for qid, (label, kws) in T.items():
    rows = []
    for k in kws:
        d = G.bwt("GetKeywordStats", q=k, country="us", language="en-US")
        time.sleep(0.9)
        if d is None:
            rows.append((k, None)); continue
        wk = sorted(d, key=lambda x: G._ms(x["Date"]))[-13:]
        rows.append((k, sum(x.get("Impressions") or 0 for x in wk)))
    tot = sum(v or 0 for _, v in rows)
    out["queries"][qid] = {"label": label, "keywords": rows, "searches_13wk": tot, "failed": sum(v is None for _, v in rows)}
    print(f"{qid} {label[:44]:44} {tot:6} | {rows}", flush=True)
json.dump(out, open('growth/focus/open-queries/report/demand.json', 'w'), indent=1)
