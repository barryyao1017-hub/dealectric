"""Kits (DLC-223, Barry 2026-11-10): researched bundles behind one buy link that opens a filled cart.

A kit is a set of products from src/products.py that are bought together for one need and sold through ONE cart:
- one brand's own Shopify store (network cj / awin / rakuten): /go/<kit slug> opens the store's checkout with every
  item in the cart (Shopify cart permalink /cart/<variant>:<qty>,...) and, when it passed the cart test, the code applied;
- or Amazon (every item `program: "amazon:us"`, any brand): one amazon.com Add-to-Cart link with our tag that puts every
  item in the shopper's Amazon cart after one confirmation click (no /go/ hop: Amazon pays nothing through a redirect).
A link that opens two stores' affiliate links from one click is a forced click (CJ, Awin, Rakuten rules), so a kit never
spans two stores.

Fields:
  slug       the kit's id: /go/<slug> for a store kit
  name       short name for the line on the page ("CPAP camping kit")
  items      [{"slug": <product slug>, "qty": 1, "variant": <Shopify variant id> (store kits), "role": "why it is in the kit"}]
  page       the gap page slug that sells it
Cart test results (what the cart showed, the code, the date) live in src/kits-tested.json, written by tools/kitcheck.py;
the page states a kit price only from a passing test.
"""

KITS = [
]
