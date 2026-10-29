"""Mixed-cart code check: S2000 Pro + SP037 in one cart (cart only, no checkout, no personal data)."""
import json, sys, time
sys.path.insert(0, "/Users/jiayiyao/Desktop/dealectric/tools")
from codecheck import session

BASE = "https://iallpowers.com"
ITEMS = [{"id": 42882903310489, "quantity": 1},   # S2000 Pro, $664
         {"id": 42769055875225, "quantity": 1}]   # SP037, $299
out = []
for code in ["ZZNOTACODE7Q", "BULKRATE", "ALLPOWERS26"]:
    call = session(True, 2.0)
    call(f"{BASE}/cart/add.js", {"items": ITEMS})
    call(f"{BASE}/cart/update.js", {"discount": code})
    cart = call(f"{BASE}/cart.js")
    dc = next((d for d in cart.get("discount_codes", []) if d["code"].upper() == code.upper()), None)
    apps = ([{"title": a.get("title"), "amount": a.get("total_allocated_amount", 0) / 100} for a in cart.get("cart_level_discount_applications", [])]
            + [{"title": a["discount_application"].get("title"), "amount": a["amount"] / 100} for it in cart["items"] for a in it.get("line_level_discount_allocations", [])])
    r = {"checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "code": code, "items": [(i["title"][:40], i["quantity"], i["original_line_price"] / 100) for i in cart["items"]],
         "applicable": bool(dc and dc.get("applicable")), "subtotal": cart["original_total_price"] / 100,
         "total": cart["total_price"] / 100, "discount": cart["total_discount"] / 100, "applications": apps}
    print(json.dumps(r)); out.append(r)
    time.sleep(15)
