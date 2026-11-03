# Weekly growth scorecard (DLC-28)

One row per week, Monday to Sunday UTC. North Star (DLC-102, since 2026-10-30): 10 credited outside sales in a rolling
30 days; before that (DLC-33) the first one.

Sources: Cloudflare GraphQL (`python3 tools/cf.py`, `verifiedBotCategory` and `userAgent`); D1 (`wrangler d1 execute
dealectric --remote`, queries in `worker/README.md`); `site:dealectric.com` read logged out in a clean browser on Google,
Bing and Brave; Google Search Console and Bing Webmaster Tools (agent Chrome, barrryyao); CJ and Awin dashboards.

| Week | AI crawlers | ChatGPT-User | Search crawlers | Google `site:` | Bing `site:` | Brave `site:` | GSC impr. / clicks | `/go/` clicks by shoppers | `ai_fetch` rows | Feedback rows | Sales |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10-20 to 10-26 | 400 (GPTBot 177, Amazonbot 104) | 258 (mostly our evals) | 311 (Bingbot 18) | ~47 (33 on 10-23) | 0 | 0 | 32 / 0 (10-19 to 10-25) | 0 known | 149 | 3 | none known |
| 10-27 to 11-02 | 290 (ClaudeBot 147, Amazonbot 124, GPTBot 16) | 447 (verified) | 424 (OAI-SearchBot 177, Googlebot 160, Bingbot 57) | no total shown (GSC: 46 indexed, report of 10-22) | not read (challenge page) | 0 | 76 / 2 (avg position 33.6) | 19 ChatGPT shoppers (45 tagged clicks) | 92 | 1 | 1 (CJ, ALLPOWERS, $33.63, New) |

## Notes

**10-27 to 11-02** (read 2026-11-03 on the work laptop).
- Sales: CJ shows one commission, the first sale (ALLPOWERS P1800 + SP037 kit, event 10-29 07:42 PT, sale $672.52,
  commission $33.63, status New, coupon APS87Q7FQHHT). Awin not read (it had 0 transactions in October).
- `/go/`: 45 redirects from real browsers tagged `utm_source=chatgpt.com`, 19 shoppers by (Pacific day, user agent):
  18 clicks on 10-29, 18 on 10-30, then 2-4 a day. 24 of the 45 went to the ALLPOWERS P1800 + SP037 kit, 10 to the
  VOLIX P300 kit, 6 to the Elite 30 V2 kit, 3 to the AC180 kit. The 452 untagged real-UA redirects are mostly
  scanners. `tools/fetchwho.py`: of the 92 `ai_fetch` rows, 63 are crawlers, 16 ours, 12 outside or outside-likely, 1
  ambiguous. Tagged page landings: 91 (86 chatgpt.com).
- Feedback: one row, `missing_product` "Anker Prime 250W power bank" (10-31), the same Anker ask as before.
- Bing (DLC-31) moved: verified Bingbot fetched inner pages for the first time, 13 distinct ones from 10-28 (/data) on,
  faster from 11-01: /bluetti-ac200l, /bluetti-ac180, /best-2kwh-power-station-for-rv, /allpowers-p1800-1024wh,
  /soundcore-aerofit-2, /baseus-gan5-pro-65w-2c-u, /bluetti-elite-200-v2, /agents, /contact, /products (all 200).
  The public `site:` count could not be read (Bing served a challenge page in the browser pane) and Bing Webmaster
  was signed out in the Agent Chrome.
- GSC: 76 impressions, 2 clicks, average position 33.6 (32 / 0 the week before). The Page indexing report is still
  dated 10-22 (46 indexed, 17 not). Google's `site:` no longer shows a total, so that column is GSC's from now on.
- Brave `site:dealectric.com`: no results ("too few matches").


**10-20 to 10-26** (read 2026-10-27).
- `/go/` clicks: 219 redirects carry `bot_like=0`, but none looks like a shopper. 98 come from Windows Chrome UAs in 6
  countries, 59 from an "iPhone OS 13_2_3 ... App" UA that walks the catalog from 9 countries about every 10 minutes
  (a scanner), 46 from `Mozilla/5.0 (compatible)` (37 of them with `utm_source=chatgpt.com`, i.e. ChatGPT opening the
  buy link during our evals), 12 Android, 3 iOS 17, 1 Mac. The `bot_like` flag misses the scanner; worth tagging it.
- Feedback: three `missing_product` rows, all Anker ("Anker Prime 250W power bank" on 10-21 and 10-24, "Anker" on
  10-23), no agent name. The only product agents have asked for is one we can't link (Impact stalled, DLC-15).
- Sales: no sale or commission email from CJ or Awin; the dashboards were not read this week.
- GSC: 46 pages indexed, 17 excluded on purpose (12 noindex, 3 redirects, 2 404s), none left "Discovered, not
  indexed" as of the 10-25 report; the pages added since 10-23 are not in it yet (11 requested 10-27). 32 impressions,
  0 clicks, average position 38.6; top query "allpowers kod rabatowy" (5). Merchant listings: 22 invalid for a missing
  `image`, all crawled before the spec-card images went live on 10-21 (validation started 10-27). Bing WMT not read.

**Search crawlers by name** (read 2026-10-28; Cloudflare, 10-14 to 10-28). A bot's name in the UA proves nothing:
count only requests Cloudflare marks with a `verifiedBotCategory`, and check the paths against the sitemap.
- OAI-SearchBot (builds ChatGPT's own search index): 182 verified requests, first real page 10-21, covering 53 of the
  75 sitemap URLs plus 41 `/go/` links. Another 300 requests carry its UA but are scanners (`.env` and key-file probes).
- Claude-SearchBot: never visited. All 296 requests with its UA are unverified and hit 0 site pages (secret-file
  probes). Claude's index is Brave, still 0 pages.
- PerplexityBot: never visited. All 273 requests with its UA are unverified scanners, 0 site pages.
- Bingbot: 28 verified requests 10-20 to 10-28, all 200, only sitemap, home, robots, `/products` and assets; Bing
  Webmaster shows 0 backlinks (DLC-31).
- Googlebot 199 and Google-InspectionTool 177 verified requests since 10-21; Amazonbot 125, Applebot 43.
