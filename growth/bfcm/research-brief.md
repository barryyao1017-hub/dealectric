# Black Friday / Cyber Monday 2026 brand research brief (2026-11-10)

Dealectric (dealectric.com) is an affiliate deals site. We are building Black Friday and Cyber Monday 2026 deal pages
for the brands we sell through. Today is 2026-11-10. Black Friday is Fri 2026-11-27, Cyber Monday Mon 2026-11-30.

Your job: for each brand assigned to you, find what the brand's **official US store** is offering (or has announced)
for Black Friday / Cyber Monday 2026, and the most appealing current deal on the products we list.

Brand list with our products, prices (our last verified store price) and store URLs: `growth/bfcm/brands.json`.

## Rules
- Use WebSearch and WebFetch (or `curl -s -m 20 -A "Mozilla/5.0"`) only. Never open a browser. Skip a page that needs one and note it.
  Shopify stores answer `https://<store>/products/<handle>.json` and `https://<store>/products.json?limit=250` with live
  prices and compare-at prices; use that to read current prices for our products.
- Sources that count: the brand's own US site (sale landing pages, banners, product pages, announcement bars, blog/news
  posts, press releases, official social posts). Deal-news sites (9to5Toys, Slickdeals, CNET, Tom's Guide, The Verge)
  only as a pointer to what the brand announced, never as the source of a code.
- **Codes:** list a code only when it is printed on the brand's own US site (banner, product page, sale page) or in a
  brand press release. Never list codes from coupon sites (RetailMeNot, Knoji, Dealspotr, CouponBirds etc.). Don't
  claim a code works; we cart-test separately.
- Dates matter: give the sale's start and end dates as the brand states them, and whether it is live today
  (2026-11-10), announced for later, or only last year's pattern (2025) with nothing announced yet for 2026. Label each.
- If the brand ran a 2025 Black Friday sale and nothing for 2026 is out yet, record the 2025 sale (dates, headline
  discount) as `last_year`, clearly separated, so we can say "last year it ran X" without implying it's this year's.
- Prices: for each of our products whose current store price differs from our recorded price, give the current price
  and compare-at price with the URL you read it from and the time.
- Be efficient: ~3–6 tool calls per brand. Don't pad.

## Output
Write a JSON file at the path you were given: a list, one object per brand:

```json
{"brand": "Soundcore",
 "sale_2026": {"status": "live | announced | none_found", "name": "Black Friday Early Access", "start": "2026-11-09",
               "end": "2026-11-18", "headline": "Up to 46% off", "url": "https://...", "notes": "member flash deals..."},
 "phases": [{"name": "Black Friday", "start": "...", "end": "...", "headline": "...", "url": "..."}],
 "cyber_monday": {"status": "...", "start": "...", "end": "...", "headline": "...", "url": "..."},
 "last_year": {"name": "Black Friday 2025", "start": "2025-11-..", "end": "2025-12-..", "headline": "...", "url": "..."},
 "site_codes": [{"code": "BF20", "terms": "as printed", "where": "url", "seen": "2026-11-10"}],
 "product_prices": [{"slug": "...", "price": 79.99, "compare_at": 99.99, "url": "...", "read": "2026-11-10"}],
 "best_deal_now": "one sentence: the most appealing current deal on a product we list, with numbers and source",
 "confidence": "high | medium | low", "gaps": "what you couldn't verify"}
```

Return a 3–5 line summary in your final message (brands with a 2026 sale live or announced, any site codes found).
