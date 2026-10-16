# Dealectric launch status — updated 2026-10-16 — MVP SHIPPED

## Live
- https://dealectric.com — GitHub Pages behind Cloudflare (proxy on, SSL Full, Web Analytics, AI Crawl Control). hello@dealectric.com forwards to barryyao1017@gmail.com.
- **Catalog: https://dealectric.com/products — 31 products, 6 brands** (Baseus 5, ESR 5, Tenergy 4, BLUETTI 5, ALLPOWERS 5, Soundcore 7). Each page: normalized spec table, JSON-LD Product/Offer, verified price (official US store, 2026-10-14), warranty/returns, caveats, and a tracked "Buy at <brand>" link.
- **Machine feed: https://dealectric.com/offers.json** — every record with specs + `offer.link` (tracked) + coupon. Linked from llms.txt, footer and the agents page.
- Guides now cross-link the catalog (charging guide → chargers/banks/cables; power-station guide → comparison table of all 10 stations + solar panel).

## Traffic & indexing (where to look)
- Requests/visitors incl. bots: Cloudflare → dealectric.com → Analytics. AI crawlers by bot: AI Crawl Control → Overview. Page views: Account → Observability → Web analytics. First 3 days: ~300 requests, ~40 page views, mostly affiliate-network reviewers and scanners; 0 AI crawlers yet.
- **Google Search Console** (sc-domain:dealectric.com, under Google account yaojiayi1017@gmail.com; verified 10/14 by TXT record in Cloudflare DNS). sitemap.xml submitted and already read — 42 pages discovered. Indexing → Pages shows coverage; Performance shows impressions/clicks once indexed.
- **Bing Webmaster Tools** (dealectric.com, signed in with Google; verified 10/14 by CNAME `f303e07e…` → verify.bing.com in Cloudflare DNS). sitemap.xml submitted, status Processing. Bing feeds ChatGPT search / Copilot, so this is the one that matters for assistant citations.

## How the money flows
- Link formats (src/links.json): CJ `https://www.tkqlhce.com/click-101901491-<linkId>?sid=<slug>&url=<encoded product URL>`; Awin `https://www.awin1.com/cread.php?awinmid=<mid>&awinaffid=3120687&clickref=<slug>&ued=<encoded product URL>`. Both click-tested 2026-10-14: land on the exact product page with cjevent / awc tracking attached.
- Cookie: 30 days (ESR 60). Brand approves commission after its return window (~30–50 days). CJ pays ~20th of the following month by direct deposit (min $50; payment method already set). Awin pays 1st/15th after advertiser settles (min $20; Baseus/AUKEY on accelerated payment; $5 deposit refunded with first payout).
- **Open: Awin Payment Details requires two-step verification on the account first — Barry.**
- Coupons live on pages: Soundcore AFSC20 (20% off full-price, to 2026-12-31), ALLPOWERS ALLPOWERS26 (10% sitewide, to 2026-12-30).

## Affiliate programs (checked in both dashboards 2026-10-16): 10 approved, 7 declined, 17 pending
- **Approved (10):** CJ — Tenergy, Soundcore, Bluetti Global, ALLPOWERS, Aurzen, Amazfit US, Mobile Pixels. Awin — ESR (US), BASEUS TECHNOLOGY (US), BLUETTI US. Not yet in the catalog despite approval: Aurzen, Amazfit, Mobile Pixels (outside launch categories).
- **Declined (7):** CJ — EcoFlow, Harman, OtterBox, Scosche, Sony, X-Sense (all declined silently between 10/13 and 10/16, no email). Awin — UGREEN (Global), "unable to verify traffic". Impact Marketplace appeal denied 10/12.
- **Pending (17):** CJ (11) — Audioengine, Baseus US Amazon Marketplace, eufyMake, Jackery, KOSS, Marshall Headphones US, Monoprice, NOMAD Goods, SanDisk North America, Ugreen, ZAGG + mophie. Awin (6) — Twelve South, Jackery US, SwitchBot, Wyze Global, PECRON, AUKEY OFFICIAL.
- Unsolicited CJ offer waiting: GearUP (game-booster subscription, 70%) — off-vertical, ignore.
- Anker (Impact) invitation email unanswered.

## Clicks & sales (as of 2026-10-16)
- CJ this month: 2 clicks, 0 sales, $0. Awin October: 2 clicks, 0 transactions, $0 payable/approved/pending. The 4 clicks are our own link tests on 10/14. No purchases yet.

## Blocked on Barry
1. Awin 2FA + bank details (above).
2. Store accounts for refer-a-friend links (anker.com, soundcore.com, ankersolix.com) — optional.
3. Rakuten account — optional.

## Claude — next
- Reply to BLUETTI US questionnaire. Weekly price re-verification (bump VERIFIED in src/products.py). Add products as approvals land. `/go/` redirect Worker with sub-ID logging. Weekly assistant-citation probes. Check GSC/Bing coverage in ~1 week.
