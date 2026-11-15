"""DLC-277 (11-14): corrections from growth/combo/buycompare-audit.json, each read by hand against the card titles and the
11-13 exact-item cart tests. Store prices that came from cart tests are left alone."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[2]
def edit(f, fn):
    p = ROOT / f; d = json.loads(p.read_text()); fn(d["products"]); p.write_text(json.dumps(d, indent=1) + "\n")
def drop(P, slug, seller):
    n = len(P[slug]["sellers"]); P[slug]["sellers"] = [s for s in P[slug]["sellers"] if s[0] != seller]; assert len(P[slug]["sellers"]) == n - 1, (slug, seller)
def pilot(P):
    drop(P, "ugreen-nexode-25000mah-200w-power-bank", "Best Buy")       # card was the model with 2 built-in cables
    drop(P, "esr-halolock-15w-wireless-car-charger-cryoboost", "Newegg")  # card was a dashboard-mount charger, CryoBoost not stated
    drop(P, "ugreen-40gbps-nvme-enclosure-cooling-fan", "Newegg")       # card was the fanless cooling-fin enclosure
def ab(P):
    drop(P, "ugreen-40gbps-nvme-enclosure-cooling-fan", "Newegg")
    s = P["bluetti-ac180-2x200w-solar-kit"]["sellers"]                    # $999 was the one-panel kit; the 11-13 cart test charged $1,232
    assert s == [["bluettipower.com without the link", 999.0]], s
    s[0][1] = 1232
    P.pop("3dmakerpro-seal-3d-scanner")                                   # Newegg card and the store price were both the Seal Lite
edit("src/buycompare.json", pilot); edit("src/buycompare_ab.json", ab); print("edited")
