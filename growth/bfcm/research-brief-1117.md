# Black Friday / Cyber Monday 2026 brand research: refresh pass (2026-11-17)

Dealectric (dealectric.com) is an affiliate deals site with Black Friday and Cyber Monday 2026 pages for the brands we
sell through. The first research pass ran on 2026-11-10. Today is **2026-11-17**. Black Friday is Fri 2026-11-27,
Cyber Monday Mon 2026-11-30. Many brands switch from "early access" to the main Black Friday phase between Nov 16 and
Nov 20, and on 11-10 many had nothing announced yet. Your job is to record what each assigned brand's **official US
store** runs or has announced **as of today**, and the current prices of our products.

Input: `growth/bfcm/brands-2026-11-17.json`. Per brand: store URL, our products (slug, name, our recorded price and
list_price, product URL, in_stock), and `current_bfcm_entry`: what our pages say now (phases with dates, headline,
source URL; `seen` marks an undated sale seen on that date; `last_year`). `null` means the brand is new to us since
11-10 and needs a full read.

## Rules
- Use `curl -s -m 20 -A "Mozilla/5.0" <url>` (works from this machine) and WebSearch. WebFetch may fail on this
  network; if it does, use curl. Never open a browser.
- Shopify stores answer `https://<store>/products/<handle>.json` and `https://<store>/products.json?limit=250` with
  live prices (`variants[].price`, `compare_at_price`); use that for prices. Read the home page / announcement bar /
  sale landing page (e.g. `/pages/black-friday`, `/collections/black-friday`, `/pages/sale`, `/pages/deals`) for the
  sale itself.
- Sources that count: the brand's own US site (sale pages, banners, announcement bars, product pages, blog/news,
  press releases, official social posts). Deal-news sites only as a pointer to what the brand announced, never as the
  source of a code.
- **Codes:** list a code only when it is printed on the brand's own US site or in a brand press release. Never from
  coupon sites. Don't claim a code works; we cart-test separately.
- Dates: give start and end as the brand states them. If a sale is live with no dates, say so (we will mark it
  "on when we checked, Nov 17"). Keep each phase the brand names separately (early access, main Black Friday, Cyber
  Monday, Cyber Week), including future phases it has announced.
- For brands with a `current_bfcm_entry`: confirm or correct each phase, add new phases, and note phases that ended
  early or changed. Don't re-research `last_year` unless the entry has none and a 2025 sale is easy to confirm.
- Prices: report only products whose live price, compare-at price or stock differs from our record.
- Budget ~3–5 tool calls per brand. Don't pad.

## Output
Write a JSON list to the path you were given, one object per brand:

```json
{"brand": "Soundcore",
 "status": "live | announced | none_found",
 "phases": [{"name": "Black Friday", "start": "2026-11-19", "end": "2026-11-30", "headline": "up to 50% off",
             "url": "https://...", "dated": true}],
 "cyber_monday": {"status": "live | announced | none_found | part_of_bf", "start": "...", "end": "...", "headline": "...", "url": "..."},
 "last_year": {"name": "...", "start": "2025-..", "end": "...", "headline": "...", "url": "..."},
 "site_codes": [{"code": "BF20", "terms": "as printed", "where": "url", "seen": "2026-11-17"}],
 "price_changes": [{"slug": "...", "price": 79.99, "compare_at": 99.99, "in_stock": true, "url": "...", "read": "2026-11-17"}],
 "changed_since_1110": "one line: what differs from current_bfcm_entry (or 'new brand')",
 "best_deal_now": "one sentence: the most appealing current deal on a product we list, with numbers and source",
 "confidence": "high | medium | low", "gaps": "what you couldn't verify"}
```

Headlines: short, in the brand's words ("up to 54% off, plus a free solar panel on large orders"). Return a 3–5 line
summary in your final message: brands with a 2026 sale live or announced, any new site codes, notable price changes.
