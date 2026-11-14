"""Re-run the exact-item cart test (control + code) on every product in src/buycompare.json; writes
growth/buylink/carttest-refresh-<date>.json in the carttest-*.json shape."""
import datetime as dt, json, sys, time
from pathlib import Path
R = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(R / "src"), str(R / "tools")]
import products, codecheck_browser as C
P = {p["slug"]: p for p in products.PRODUCTS.values()} if isinstance(products.PRODUCTS, dict) else {p["slug"]: p for p in products.PRODUCTS}
codes = json.load(open(R / "src/coupons.json"))["codes"]
bc = json.load(open(R / "src/buycompare.json"))["products"]
out_path = R / f"growth/buylink/carttest-refresh-{dt.date.today()}.json"
out = json.load(open(out_path)) if out_path.exists() else {}
for slug in bc:
    if slug in out: continue
    p = P[slug]
    code = next((c["code"] for c in codes if c.get("publish") and any(t.get("product") == slug for t in c.get("tests", []))), None)
    if not code:
        print(slug, "no tested code", flush=True); continue
    url = p["url"] + (f"?variant={p['cart_variant']}" if p.get("cart_variant") and "variant=" not in p["url"] else "")
    try:
        res = C.check_many(url, [code])
    except Exception as e:
        res = [{"error": str(e)[:200]}]
    out[slug] = {"url": url, "code": code, "out": res}
    r = res[-1]
    print(slug, code, "ctrl", res[0].get("total"), "code", r.get("total"), r.get("applicable"), r.get("error", ""), flush=True)
    json.dump(out, open(out_path, "w"), indent=1)
    time.sleep(4)
