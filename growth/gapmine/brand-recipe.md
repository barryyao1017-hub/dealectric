# Brand mode (tools/gappage.py, item kind "brand"; Barry 2026-11-06, DLC-192)

This run is for ONE newly approved brand, named below with its program key, store and the codes its affiliate
network lists. Every brand we work with must be on the site with at least one product record. Follow the gap page
recipe above with these changes:

1. **Pick the query yourself.** Find one general shopper query (no brand or model name in it; US English, the way a
   shopper types it) where one of this brand's products sold in the US honestly wins a segment for a real buyer
   need, and where the pages that answer it today are thin (mostly store listings, forum threads or generic
   roundups). Prefer queries people actually search (autocomplete suggests them). Put it in `"query"`, with 3-6
   real phrasings in `"variants"`. Then write the page for that query exactly as the recipe says. The honesty rules
   stand: if a rival wins the main segment, say so in the lead and lead with it; the brand's product must still
   honestly win at least one named segment, or there is no page.
2. **Products.** Return 1-3 records of the brand's own products (program = the brand's key below), each verified on
   the brand's US store today (`storecheck.py` for Shopify stores, WebFetch otherwise): exact name, US price in
   dollars, availability, and the product URL on the store host given below (Awin and CJ links only credit that
   host). If the store sells only outside the US, or nothing ships to the US, return `"status": "skip"` with that
   reason and no products.
3. **No page possible?** If no general query exists where the brand honestly wins a segment, return
   `"status": "products_only"` with the product records (no `page`, no `slug`, no `must`): the brand still gets its
   product pages.
4. **Categories.** Use an existing category key when one fits. If none does, add `"new_categories": {"<key>":
   ["<Plural label>", "<one-sentence description>"]}` and use that key (lowercase, hyphenated, 3-20 chars).
5. **Codes.** List in `"codes"` every code the brand's network gave us (below) that applies to a US product you
   recorded, plus any code the brand prints on its own US site right now (banner, product page). For each give
   `{"code", "source": "awin" | "cj" | "brand site", "terms" (what it takes off and on what, as stated),
   "applies_to": [product slugs]}`. Do not include codes from coupon sites. Do not claim a code works: it is
   cart-tested later.

Output: the recipe's JSON object plus `"query"`, `"variants"`, `"codes"` and, when used, `"new_categories"`.
`"status"` is "ok" (page + products), "products_only" or "skip".
