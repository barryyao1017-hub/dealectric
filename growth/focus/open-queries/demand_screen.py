"""Demand screen for the discovery queue (Barry 2026-11-15: shortlist by demand before spending ChatGPT quota).

Each pending question is matched to the real searches we already hold counts for: growth/gapmine/runs/pool/volume.json
(Microsoft Ads Ad Insight counts for 11,865 pool keywords, Bing Webmaster counts for 5,635; both are Bing US searches
over 3 months; Webmaster counts run about a fifth of the Ads counts, so they are scaled up to the Ads scale).
A keyword matches a question when it names the same kind of product and the same use (appliance, place, property),
i.e. its words are a subset of the question's words plus product words. Demand = the sum of the top matching keywords.
No ChatGPT chats and no new API calls.

    python3.12 growth/focus/open-queries/demand_screen.py            # writes demand-screen.json, prints the table
    python3.12 growth/focus/open-queries/demand_screen.py --apply 300   # reorder queue.jsonl, park questions under the floor
"""
import json, re, sys, os, collections
from pathlib import Path
HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent.parent
V = json.loads((ROOT / "growth/gapmine/runs/pool/volume.json").read_text())
STOP = set("""a an the and or of to in on at by for from with without my your our their its it is are be can will do does did i you we they me
which what how who when where why should would could that this these those than then as if so not no just only even still also very really
most least more less best good great top one two much many long longer longest fast faster fastest big bigger biggest small smaller smallest
cheap cheaper cheapest light lighter lightest need needs want buy get use using used run runs running keep keeps power powered powers powering
during while after before all any some each every per out up down into over under about actually really without someone anything something
day days night nights hour hours week weeks month year years time times charge charges charging charged recharge recharges full size sized
there here has have had make makes made work works working take takes last lasts go goes thing things way kind type new old own right""".split())
SYN = {"fridge": "refrigerator", "fridges": "refrigerator", "refrigerators": "refrigerator", "freezers": "freezer", "rvs": "rv", "camper": "rv", "campers": "rv",
       "motorhome": "rv", "trailer": "rv", "ac": "conditioner", "wi-fi": "wifi", "internet": "wifi", "router": "wifi", "modem": "wifi", "outages": "outage",
       "blackout": "outage", "panels": "panel", "batteries": "battery", "generators": "generator", "stations": "station", "kits": "kit", "bundle": "kit",
       "bundles": "kit", "pumps": "pump", "tents": "tent", "vans": "van", "campervan": "van", "homes": "home", "house": "home", "houses": "home",
       "apartments": "apartment", "condo": "apartment", "mowers": "mower", "scanners": "scanner", "printers": "printer", "screens": "screen",
       "dehumidifiers": "dehumidifier", "carts": "cart", "appliances": "appliance", "heaters": "heater", "fans": "fan", "stoves": "stove", "tvs": "tv",
       "television": "tv", "laptops": "laptop", "phones": "phone", "tools": "tool", "cars": "car", "truck": "car", "trucks": "car", "vehicle": "car",
       "ev": "electric car", "camping": "camp", "camper van": "van", "winter": "cold", "freezing": "cold", "frozen": "cold", "quietest": "quiet",
       "silent": "quiet", "noise": "quiet", "loud": "quiet", "portable": "", "best": ""}
PRODUCT = {"solar": "station generator solar battery backup kit panel bank ups inverter".split(),
           "other": "scanner mower dehumidifier screen projector battery lithium printer conditioner inverter cart trolling cooler".split()}
BRAND = re.compile(r"jackery|ecoflow|bluetti|anker|goal zero|generac|honda|champion|predator|westinghouse|ryobi|dewalt|milwaukee|harbor|costco|walmart|amazon|home depot|lowes|near me|tesla|duracell|patriot|oupes|pecron|\bego\b|renogy|vtoman|allpowers|oscal|revopoint|einstar|creality|bambu|qidi|husqvarna|segway|mammotion|vividstorm|alorair|aprilaire|vatrer|redodo|litime|battle born|zero breeze|ecovacs|reddit|review")


def toks(s: str) -> list[str]:
    out = []
    for w in re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)?", s.lower()):
        w = SYN.get(w, w)
        for x in w.split():
            if x and x not in STOP and len(x) > 1:
                out.append(x[:-1] if x.endswith("s") and len(x) > 4 and not x.endswith("ss") else x)
    return out


# keyword -> count on the Ads scale
vol = {}
for k, n in (V.get("ms") or {}).items():
    if isinstance(n, (int, float)) and n > 0:
        vol[k] = float(n)
for k, n in (V.get("volumes") or {}).items():
    if k not in vol and n:
        vol[k] = n / 0.203
KW = [(k, n, set(toks(k))) for k, n in vol.items() if not BRAND.search(k)]
KW = [(k, n, t) for k, n, t in KW if t]


# A keyword counts only if it names a product of the right kind as a phrase; the rest of its words are the "use".
PHRASE = {"solar": r"power stations?|solar (powered )?generators?|solar (power )?kits?|solar panel kits?|battery backups?|backup batter(y|ies)|home batter(y|ies)|backup power|portable power|battery generators?",
          "3d printer": r"3d printers?", "3d scanner": r"3d scanners?", "mower": r"robot(ic)? (lawn ?)?mowers?|lawn ?mowers?", "dehumidifier": r"dehumidifiers?",
          "screen": r"projector screens?|projection screens?", "golf": r"golf cart batter(y|ies)|golf cart lithium batter(y|ies)|lithium golf cart batter(y|ies)",
          "trolling": r"trolling motor batter(y|ies)", "lithium": r"(rv )?lithium batter(y|ies)|lifepo4 batter(y|ies)", "air": r"(portable |tent |battery (powered )?)?air conditioners?|portable ac( units?)?",
          "inverter": r"(solar |off grid |all in one )?inverters?"}
CAT = [("3d printer", r"3d print"), ("3d scanner", r"3d scan"), ("mower", r"mower"), ("dehumidifier", r"dehumidifier"), ("screen", r"projector|screen"),
       ("golf", r"golf cart"), ("trolling", r"trolling"), ("air", r"air condition"), ("inverter", r"inverter"), ("lithium", r"lithium|lifepo4")]
PW = set(toks("power station solar generator kit panel battery backup home bank portable generators 3d printer scanner robot robotic lawn mower dehumidifier projector projection screen golf cart lithium trolling motor lifepo4 air conditioner ac unit inverter off grid"))


def category(q: dict) -> str:
    if q.get("group") == "solar":
        return "solar"
    for c, rx in CAT:
        if re.search(rx, q["prompt"].lower()):
            return c
    return "solar"


SPLIT = {}
for c, rx in PHRASE.items():
    lst = []
    for k, n, _t in KW:
        m = re.search(r"\b(" + rx + r")\b", k)
        if m:
            use = set(toks(k[:m.start()] + " " + k[m.end():])) - (PW - {"home"} if c == "solar" else PW)
            if use:
                lst.append((k, n, use))
    SPLIT[c] = lst
DF = {c: collections.Counter(w for _k, _n, u in lst for w in u) for c, lst in SPLIT.items()}


def demand(q: dict) -> dict:
    """Searches for keywords that name the right kind of product and whose remaining words are all in the question.
    `demand` counts only keywords that contain the question's most specific use word (the rarest of its words that
    searchers type next to this product); `broad` counts the other matching keywords (same product, a general use
    such as "for home")."""
    c = category(q)
    qt = set(toks(q["prompt"])) - (PW - {"home"} if c == "solar" else PW)
    use = [w for w in qt if DF[c][w] > 0]
    if not use:
        return {"demand": 0, "broad": 0, "matches": [], "use_word": None}
    key = min(use, key=lambda w: (DF[c][w], w))
    spec, broad = [], []
    for k, n, u in SPLIT[c]:
        if u <= qt:
            (spec if key in u else broad).append((n, k))
    spec.sort(reverse=True); broad.sort(reverse=True)
    close = max((len(u) / max(1, len(qt)) for k, n, u in SPLIT[c] if u <= qt and key in u), default=0)
    return {"demand": round(sum(n for n, _ in spec[:5])), "broad": round(sum(n for n, _ in broad[:3])), "closeness": round(close, 2),
            "matches": [(k, round(n)) for n, k in spec[:5]], "broad_matches": [(k, round(n)) for n, k in broad[:3]], "use_word": key}


SKIP_WORDS = {"filament", "volt", "plug", "charger", "phone", "transfer", "storage", "large", "system"}   # use words whose keywords mean something else
SKIP_QIDS = {"au062", "fo067", "fk062"}       # bounce house, gun room, battery replacement: matched on a word used in another sense
MEMORY = re.compile(r"^(can|will|is|are|does|do|should|how long|how many|how much|how big)\b")   # forms ChatGPT mostly answers without searching


def rank_in_cluster(x: dict) -> tuple:
    p = x["prompt"].lower()
    tier = 0 if x["qid"].startswith("vq") else 1 if re.search(r"\b(which|what should i|what .* should i|best|what kind|what size)\b", p) else 3 if MEMORY.search(p) else 2
    return (tier, -x.get("closeness", 0), -x["demand"], len(p))


def shortlist(out: list[dict], floor: int, per: int) -> tuple[list, list, list]:
    cl = collections.defaultdict(list)
    for x in out:
        if x["demand"] > 0 and x["use_word"] not in SKIP_WORDS and x["qid"][:5] not in SKIP_QIDS:
            cl[(x["group"], x["use_word"])].append(x)
    clusters, keep = [], []
    for (g, u), v in cl.items():
        d = max(x["demand"] for x in v)
        v.sort(key=rank_in_cluster)
        # the searched keyword itself, plus questions that stay close to it (at least half their use words are in a searched keyword)
        chosen = [x for x in v if x["qid"].startswith("vq") or x.get("closeness", 0) >= 0.5][:per] if d >= floor else []
        kws = max(v, key=lambda x: x["demand"])["matches"][:4]
        clusters.append({"group": g, "use": u or "general", "demand": d, "keywords": kws, "queued": len(v), "ask": [x["qid"] for x in chosen],
                         "ask_prompts": [x["prompt"] for x in chosen]})
        keep += [(d, x) for x in chosen]
    clusters.sort(key=lambda c: -c["demand"])
    keep.sort(key=lambda dx: (-dx[0], rank_in_cluster(dx[1])))
    kept_ids = {x["qid"] for _, x in keep}
    return clusters, [x for _, x in keep], [x for x in out if x["qid"] not in kept_ids]


def main():
    rows = [json.loads(l) for l in (HERE / "queue.jsonl").read_text().splitlines() if l.strip()]
    done = {json.loads(l)["qid"] for l in (ROOT / "growth/evals/runs/2026-11-14-openq/scan.jsonl").read_text().splitlines()}
    pend = [r for r in rows if r["qid"] not in done]
    out = []
    for r in pend:
        d = demand(r)
        if r.get("volume"):     # the volume-backed batch carries its own Bing Webmaster count
            d["demand"] = max(d["demand"], round(r["volume"] / 0.203))
            d["matches"] = [(r["prompt"], round(r["volume"] / 0.203))] + [m for m in d["matches"] if m[0] != r["prompt"]][:4]
        out.append({**{k: r[k] for k in ("qid", "prompt", "group", "source")}, **d})
    out.sort(key=lambda x: -x["demand"])
    (HERE / "demand-screen.json").write_text(json.dumps(out, indent=1))
    bands = collections.Counter("0" if x["demand"] == 0 else "<300" if x["demand"] < 300 else "300-999" if x["demand"] < 1000 else "1,000-4,999" if x["demand"] < 5000 else "5,000+" for x in out)
    print(len(out), "pending;", dict(bands))
    floor = int(sys.argv[sys.argv.index("--floor") + 1]) if "--floor" in sys.argv else 500
    per = int(sys.argv[sys.argv.index("--per") + 1]) if "--per" in sys.argv else 4
    clusters, keep_rows, park_rows = shortlist(out, floor, per)
    (HERE / "shortlist.json").write_text(json.dumps({"floor": floor, "per_cluster": per, "clusters": clusters, "ask": len(keep_rows), "parked": len(park_rows)}, indent=1))
    print("clusters with demand:", len(clusters), "| at or above the floor:", sum(c["demand"] >= floor for c in clusters), "| questions to ask:", len(keep_rows), "| parked:", len(park_rows))
    if "--apply" in sys.argv:
        byq = {r["qid"]: r for r in pend}
        head = [r for r in rows if r["qid"] in done]
        kept = [{**byq[x["qid"]], "demand": x["demand"], "demand_cluster": x["use_word"], "demand_matches": x["matches"][:3]} for x in keep_rows]
        parked = [{**byq[x["qid"]], "demand": x["demand"]} for x in park_rows]
        tmp = (HERE / "queue.tmp"); tmp.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in head + kept) + "\n"); os.replace(tmp, HERE / "queue.jsonl")
        (HERE / "queue-parked.jsonl").write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in parked) + "\n")
        print("kept", len(kept), "parked", len(parked))
    return out


if __name__ == "__main__":
    out = main()
    for x in out[:int(sys.argv[sys.argv.index("--show") + 1]) if "--show" in sys.argv else 60]:
        print(f"{x['demand']:7} {x.get('broad', 0):7} {x['qid'][:5]} {x['prompt'][:58]:58} | {x.get('use_word')} | {x['matches'][:2]}")
