"""Cart-test DEALECTRIC on each BLUETTI product the bluetti-four pages feature (exact variant), with the control code."""
import json, subprocess, sys, time
from pathlib import Path
ROOT = Path(__file__).resolve().parents[3]
sys.path.insert(0, str(ROOT / "src"))
import products as P
out = Path(sys.argv[1])
for slug in sys.argv[2:]:
    p = next(x for x in P.PRODUCTS if x["slug"] == slug)
    u = p["url"] + (f"?variant={p['cart_variant']}" if p.get("cart_variant") else "")
    r = subprocess.run(["python3.12", "tools/codecheck_browser.py", u, "DEALECTRIC"], cwd=ROOT, capture_output=True, text=True, stdin=subprocess.DEVNULL, timeout=600)
    for l in r.stdout.strip().splitlines()[-2:]:
        try:
            d = json.loads(l)
        except ValueError:
            d = {"raw": l[-300:]}
        with out.open("a") as f:
            f.write(json.dumps({"slug": slug, "listed": p["price"], "r": d}) + "\n")
        print(slug, d.get("code"), d.get("variant", "")[:40], d.get("subtotal"), d.get("total"), d.get("code_amount"), d.get("error", ""), flush=True)
    time.sleep(4)
