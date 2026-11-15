"""DLC-277 (11-14): re-read the seller cards behind src/buycompare.json and src/buycompare_ab.json with the same-item check
(combopage.amazon_verify). buycheck's word match let through 2x packs, bundles and sibling models in the combo run.
  plan  -> growth/combo/buycompare-audit.json   (no file changed)
  apply -> rewrites the two json files from the verified cards (no build, no commit)"""
import json, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools")); sys.path.insert(0, str(ROOT / "src"))
import build as B
import buycompare as BCMP
import combopage as C
OUT = ROOT / "growth/combo/buycompare-audit.json"
FILES = {"src/buycompare.json": ["2026-11-13-cheapest-pilot.json", "2026-11-11-cheapest.json", "2026-11-11-cheapest-loose.json"],
         "src/buycompare_ab.json": ["2026-11-13-cheapest-ab.json", "2026-11-13-cheapest-pilot.json", "2026-11-11-cheapest.json", "2026-11-11-cheapest-loose.json"]}


def sellers_from(cards, p, r):
    best = {}
    for c in cards:
        n = BCMP.retailer(c["merchant"])
        if n and c["kind"] in ("retailer", "brand") and c["price"] < best.get(n, (1e9,))[0]:
            best[n] = (c["price"], c["title"])
    return best


def plan():
    out = {}
    for f, reports in FILES.items():
        cur = json.loads((ROOT / f).read_text())["products"]
        reps = {}
        for name in reports:
            for r in json.loads((ROOT / "growth/buylink" / name).read_text()):
                reps.setdefault(r["slug"], []).append((name, r))
        res = {}
        for s, e in cur.items():
            p = B.BY_SLUG.get(s)
            if not p:
                res[s] = {"status": "no product record"}; continue
            src = None
            for name, r in reps.get(s, []):   # the report whose cards reproduce the stored retailer prices
                got = {n: v[0] for n, v in sellers_from(r["cards"], p, r).items()}
                stored = {n: x for n, x in e["sellers"] if not n.endswith("without the link") and n != "Amazon"}
                if all(abs(got.get(n, -1) - x) < 0.005 for n, x in stored.items()):
                    src = (name, r); break
            if not src:
                res[s] = {"status": "no report reproduces the stored prices", "stored": e["sellers"], "reports": [n for n, _ in reps.get(s, [])]}
                continue
            name, r = src
            cards = [c for c in r["cards"] if c["kind"] in ("retailer", "brand")]
            ok = C.amazon_verify([{"i": i, "brand": p["brand"], "model": B.short_name(p), "title": c["title"]} for i, c in enumerate(cards)])
            for i, c in enumerate(cards):
                c["same"], c["why"] = ok.get(i, (False, "no verdict"))
            good = [c for c in cards if c["same"]]
            best = sellers_from(good, p, r)
            amz = B.amz_price(p["asin"]) if p.get("asin") else None
            new = {n: v[0] for n, v in best.items()}
            if amz and amz[2]:
                new["Amazon"] = amz[0]
            elif any(n == "Amazon" for n, _ in e["sellers"]) and "Amazon" not in new:
                pass
            sellers = sorted(new.items(), key=lambda x: x[1])[:4]
            brand = [c["price"] for c in good if c["kind"] == "brand"]
            wl = next(([n, x] for n, x in e["sellers"] if n.endswith("without the link")), None)
            shown = min(brand) if brand else float(p["price"])
            sellers.append((f"{B.store_host(p)} without the link", shown))
            new_s = [[n, x] for n, x in sellers]
            res[s] = {"status": "same" if new_s == e["sellers"] else "changed", "report": name, "after": r.get("after"), "old": e["sellers"], "new": new_s,
                      "rejected": [[c["merchant"], c["price"], c["title"][:140], c["why"]] for c in cards if not c["same"]],
                      "kept": [[c["merchant"], c["price"], c["title"][:100]] for c in good]}
            print(f, s, res[s]["status"], "| rejected", len(res[s]["rejected"]), flush=True)
            out[f] = res
            OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))
        out[f] = res
    OUT.write_text(json.dumps(out, ensure_ascii=False, indent=1))


if __name__ == "__main__":
    plan()
