"""Combo run, 11-14: withdraw the price lines whose seller cards were a different item (2x packs, a bundle, a Pro model,
other tripod models). Seen by re-running buycheck and reading the card titles."""
import json, re, sys
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
BAD = {"anker-solix-c1000-gen-2": "seller cards were 2x packs; the single unit is $529.99 at Anker and Best Buy too (a tie)",
       "anker-solix-s2000": "Best Buy card was the bundle with an alternator charger; Adorama price not confirmed as the single unit",
       "amazfit-t-rex-3": "the card was the T-Rex 3 Pro",
       "sirui-traveler-5c-carbon-travel-tripod": "B&H card was the AT-125, Newegg card the 5CX"}
pc_p = ROOT / "src/pricecheck.json"
pc = json.loads(pc_p.read_text())
log_p = ROOT / "growth/combo/price-log.json"
log = json.loads(log_p.read_text())
L = log.get("products") or log
for s, why in BAD.items():
    pc["products"].pop(s, None)
    L[s] = {"date": "2026-11-14", "result": "withdrawn: " + why, "entry": None}
pc_p.write_text(json.dumps(pc, ensure_ascii=False, indent=1) + "\n")
log_p.write_text(json.dumps(log, ensure_ascii=False, indent=1) + "\n")
import gaps
gp = ROOT / "src/gaps.py"
t = gp.read_text()
n = 0
for g in gaps.GAP_PAGES:
    if g.get("run") != "combo-1113" or not g.get("price_check"):
        continue
    if any(r.get("slug") in pc["products"] for r in g["rows"]):
        continue   # still has a checked product
    a = t.index("{\"slug\": %r," % g["slug"])
    b = t.find("# ----------------", a)
    b = len(t) if b < 0 else b
    rec = t[a:b]
    new = re.sub(r'"price_check": True,\s*', "", rec, count=1)
    assert new != rec, g["slug"]
    t = t[:a] + new + t[b:]
    n += 1
    print("flag removed:", g["slug"])
gp.write_text(t)
print(n, "pages")
