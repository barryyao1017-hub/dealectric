# Dealectric reference — accounts, links, money (updated 2026-11-07)

This is durable reference, not a status snapshot. Current status lives in the "Dealectric To-Dos" artifact (https://claude.ai/artifact/8eV4jpzzYbQVtotF5EmAkp) and the daily update; counts (products, brands, pages, clicks, sales) come from `src/products.py`, `docs/offers.json`, D1 and the network dashboards, never from this file. History of the experiments that shaped the site is in `growth/` (`loop-report.md`, `loop-report-phase2.md`, `focus/`, `gapmine/`, `evals/README.md`).

## Live
- https://dealectric.com — GitHub Pages behind Cloudflare (proxy on, SSL Full, Web Analytics, AI Crawl Control), with the `dealectric-edge` Worker routed in front (see CLAUDE.md). hello@dealectric.com forwards (Porkbun email forwarding) to barrryyao@gmail.com.
- Catalog https://dealectric.com/products: one page per product record with a normalized spec table, JSON-LD Product/Offer, verified price and stock (official US store), warranty/returns, caveats, the cart-tested discount code and a tracked "Buy at <brand>" link (`/go/<slug>`). Retired products keep a noindex "no longer sold" page. Per-brand code pages at /discount-codes; comparison pages (`src/gaps.py`, `src/compare.py`) linked from home, /products, /discount-codes and the guides.
- Machine feed https://dealectric.com/offers.json: every record with specs + `offer.link` (tracked) + coupon. Linked from llms.txt, the footer and /agents.

## Traffic & indexing (where to look)
- Requests/visitors incl. bots: Cloudflare → dealectric.com → Analytics. AI crawlers by bot: AI Crawl Control → Overview. Page views: Account → Observability → Web analytics. Scripted: `tools/cf.py` (read-only token, see memory).
- Google Search Console: sc-domain:dealectric.com; owners yaojiayi1017@gmail.com (verified 2026-10-14 by TXT record in Cloudflare DNS) and barrryyao@gmail.com (the account signed in to the Agent Chrome). URL Inspection indexing requests are quota-limited to ~10/day.
- Bing Webmaster Tools: dealectric.com, Google sign-in as barrryyao@gmail.com; verified 2026-10-14 by CNAME `f303e07e…` → verify.bing.com. URL Submission quota 100/day; IndexNow via `tools/indexnow.py` (key file published by `build.py`). Bing has crawled almost nothing of the site since launch (0 backlinks is the likeliest cause); OpenAI's own index (OAI-SearchBot) is what ChatGPT answers from, so Bing matters less than first thought.
- Shopper funnel: D1 `clicks` (`/go/`) and `landings` (utm-tagged page views) through the Worker; `tools/dailyupdate.py` and `tools/fetchwho.py` separate our own traffic from outside shoppers.

## How the money flows
- Link formats (`src/links.json`): CJ `https://www.tkqlhce.com/click-101901491-<linkId>?sid=<slug>&url=<encoded product URL>`; Awin `https://www.awin1.com/cread.php?awinmid=<mid>&awinaffid=3120687&clickref=<slug>&ued=<encoded product URL>`; Rakuten `https://click.linksynergy.com/deeplink?id=5ip7Zy3Dkto&mid=<mid>&murl=<encoded>&u1=<sub-ID>`; Amazon `https://www.amazon.com/dp/<ASIN>?tag=dealectric-20` placed directly on the page (never through `/go/`). The Worker sets the sub-ID to `<slug>.<clickid>`.
- Cookies: CJ/Awin 30 days (ESR 60), Rakuten per advertiser, Amazon 24 h. Brands approve commission after their return window (~30–50 days). CJ pays ~20th of the following month by direct deposit (min $50; payment method set). Awin pays 1st/15th after the advertiser settles (min $20) **once two-step verification and payment details are set (DLC-3, Barry)**. Amazon Associates pays ~60 days after month end, after the tax interview and payment method are set (DLC-157, Barry); the account closes without 3 qualifying sales by 2027-05-02.
- Codes live in `src/coupons.json`, rewritten by the daily cart sweep; published codes are network-issued or brand-approved only (coupon-site codes stay unpublished, DLC-42 decided).

## Affiliate programs
- Approved programs with links in use: `src/links.json`. Pending applications and new approvals: the CJ, Awin and Rakuten dashboards and the inbox (DLC-14 daily check; DLC-16 counts the pending set).
- Declined, 2026-10-12..16 (for DLC-18, reapply once traffic shows): CJ — EcoFlow, Harman, OtterBox, Scosche, Sony, X-Sense (silent); Awin — UGREEN Global ("unable to verify traffic"; UGREEN was later approved on CJ, 2026-11-03); Impact Marketplace appeal denied 2026-10-12. Anker (Impact) invitation unanswered (DLC-17).
- Amazon Associates (since 2026-11-03): store/tracking ID `dealectric-20`, site dealectric.com, payee Jiayi Yao; provisional until 3 qualifying sales in 180 days. Records carry `program: "amazon:us"`, a direct tagged link and no price (Amazon allows prices only from its own feed); the Associates statement is in every footer.
- Skimlinks (sub-network, 25% cut, ~90-day payout): application for dealectric.com submitted 2026-11-03, pending (DLC-158). Rakuten Advertising (since 2026-11-06): Anker SOLIX approved; site ID 613226, publisher id `5ip7Zy3Dkto`.
- Geo: US-only until North Star 1 is met or non-US real-browser landings pass ~20% (DLC-155).

## Accounts the project uses (all barrryyao@gmail.com unless noted)
Cloudflare, Porkbun (domain), GitHub `barryyao1017-hub/dealectric`, CJ (publisher 101901491), Awin (affiliate 3120687), Rakuten, Amazon Associates, Skimlinks, Google Search Console, Bing Webmaster Tools, OpenAI platform (barryyao1017@gmail.com, API keys in each Mac's keychain), YouTube channel @Dealectric-JY, Reddit u/Dealectric_. Logins go through agent-vault in the Agent Chrome; business entity Agentify LLC (WA, filed 2026-11-01).
