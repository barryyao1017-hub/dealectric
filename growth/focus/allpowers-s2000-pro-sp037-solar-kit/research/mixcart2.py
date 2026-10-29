"""Cart-only code checks on the R2500 V2 kit and R2500 V2 + SP037 as separate items (no checkout, no personal data)."""
import json, sys, time
sys.path.insert(0, "/Users/jiayiyao/Desktop/dealectric/tools")
from codecheck import session

BASE = "https://iallpowers.com"
CASES = [
    ("kit", [{"id": 67800818614425, "quantity": 1}], ["ZZNOTACODE7Q", "ALLPOWERS26", "EXTRA10"]),
    ("separate", [{"id": 48261423005849, "quantity": 1}, {"id": 42769055875225, "quantity": 1}], ["ZZNOTACODE7Q", "BULKRATE", "ALLPOWERS26"]),
]
for name, items, codes in CASES:
    for code in codes:
        call = session(True, 2.0)
        call(f"{BASE}/cart/add.js", {"items": items})
        call(f"{BASE}/cart/update.js", {"discount": code})
        cart = call(f"{BASE}/cart.js")
        dc = next((d for d in cart.get("discount_codes", []) if d["code"].upper() == code.upper()), None)
        apps = ([{"title": a.get("title"), "amount": a.get("total_allocated_amount", 0) / 100} for a in cart.get("cart_level_discount_applications", [])]
                + [{"title": a["discount_application"].get("title"), "amount": a["amount"] / 100} for it in cart["items"] for a in it.get("line_level_discount_allocations", [])])
        print(json.dumps({"checked_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()), "case": name, "code": code,
                          "items": [(i["title"][:45], i["quantity"], i["original_line_price"] / 100) for i in cart["items"]],
                          "applicable": bool(dc and dc.get("applicable")), "subtotal": cart["original_total_price"] / 100,
                          "total": cart["total_price"] / 100, "discount": cart["total_discount"] / 100, "applications": apps}))
        time.sleep(15)
