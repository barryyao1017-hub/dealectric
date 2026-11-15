"""Barry 11-14 (DLC-279): a comparison counts a retailer's own listing only, not a third-party seller on its marketplace.
Removes the four reseller prices found by the DLC-277 audit (merchant names in growth/combo/buycompare-audit.json)."""
import json
from pathlib import Path
p = Path(__file__).resolve().parents[2] / "src/buycompare.json"
d = json.loads(p.read_text()); P = d["products"]
for slug, seller, price in [("baseus-picogo-am52-qi2-2-10000mah-45w", "Newegg", 94.99),          # Newegg.com - PowerixDxz
                            ("ugreen-nexode-25000mah-200w-power-bank", "Newegg", 232.54),         # Newegg.com - dazella store
                            ("botslab-g980h-4-camera-dash-cam", "Newegg", 448.48),                # Newegg.com - TrustBasket
                            ("oscal-powermax-6000-3600wh-240v", "Walmart", 1899.0)]:              # Walmart - Hopetool
    n = len(P[slug]["sellers"])
    P[slug]["sellers"] = [s for s in P[slug]["sellers"] if not (s[0] == seller and abs(s[1] - price) < 0.005)]
    assert len(P[slug]["sellers"]) == n - 1, slug
    print(slug, P[slug]["sellers"])
p.write_text(json.dumps(d, indent=1) + "\n")
