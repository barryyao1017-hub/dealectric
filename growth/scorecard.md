# Weekly growth scorecard (DLC-28)

One row per week, Monday to Sunday UTC. North Star (DLC-33): a sale credited to us that isn't our own test.

Sources: Cloudflare GraphQL (`python3 tools/cf.py`, `verifiedBotCategory` and `userAgent`); D1 (`wrangler d1 execute
dealectric --remote`, queries in `worker/README.md`); `site:dealectric.com` read logged out in a clean browser on Google,
Bing and Brave; Google Search Console and Bing Webmaster Tools (agent Chrome, barrryyao); CJ and Awin dashboards.

| Week | AI crawlers | ChatGPT-User | Search crawlers | Google `site:` | Bing `site:` | Brave `site:` | GSC impr. / clicks | `/go/` clicks by shoppers | `ai_fetch` rows | Feedback rows | Sales |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 10-20 to 10-26 | 400 (GPTBot 177, Amazonbot 104) | 258 (mostly our evals) | 311 (Bingbot 18) | ~47 (33 on 10-23) | 0 | 0 | 32 / 0 (10-19 to 10-25) | 0 known | 149 | 3 | none known |

## Notes

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
</content>
</invoke>
