# Dealectric launch status — updated 2026-10-22 — MVP SHIPPED

## Live
- https://dealectric.com — GitHub Pages behind Cloudflare (proxy on, SSL Full, Web Analytics, AI Crawl Control). hello@dealectric.com forwards (Porkbun email forwarding) to barrryyao@gmail.com (changed from barryyao1017@gmail.com on 2026-10-20).
- **Catalog: https://dealectric.com/products — 30 products, 6 brands** (Baseus 5, ESR 4, Tenergy 4, BLUETTI 5, ALLPOWERS 5, Soundcore 7). Each page: normalized spec table, JSON-LD Product/Offer, verified price and stock (official US store, 2026-10-21), warranty/returns, caveats, working discount codes, and a tracked "Buy at <brand>" link (`/go/<slug>`). Retired 2026-10-21: Baseus Blade HD (→ Blade H1) and ESR MagSlim power bank (noindex "no longer sold" pages).
- **Machine feed: https://dealectric.com/offers.json** — every record with specs + `offer.link` (tracked) + coupon. Linked from llms.txt, footer and the agents page.
- Guides now cross-link the catalog (charging guide → chargers/banks/cables; power-station guide → comparison table of all 10 stations + solar panel).

## Traffic & indexing (where to look)
- Requests/visitors incl. bots: Cloudflare → dealectric.com → Analytics. AI crawlers by bot: AI Crawl Control → Overview. Page views: Account → Observability → Web analytics. First 3 days (10/14–10/16, Cloudflare API, checked 10/17): 7,334 requests, 62 real page views, 182 AI-crawler requests; most human-looking traffic was affiliate-network reviewers and scanners.
- **Google Search Console** (sc-domain:dealectric.com; owners: yaojiayi1017@gmail.com (verified 10/14 by TXT record in Cloudflare DNS) and, since 10/18, barrryyao@gmail.com, which is the account signed in to the agent's Chrome). sitemap.xml submitted and read — 42 pages discovered, but on 10/18 only 3 were indexed (home, /privacy, /agents). Indexing requests via URL Inspection are quota-limited to ~10/day; 9 done 10/18 (DLC-13 tracks the rest).
- **Bing Webmaster Tools** (dealectric.com, Google sign-in as barrryyao@gmail.com; verified 10/14 by CNAME `f303e07e…` → verify.bing.com in Cloudflare DNS). sitemap.xml: Success, 42 URLs discovered, but on 10/18 every page was 'Discovered but not crawled' and the home page carried a stale May-2025 DNS-failure record. All 42 URLs submitted 10/18 via URL Submission (quota 100/day) and via IndexNow (`tools/indexnow.py`; key file published by `build.py`). Bing feeds ChatGPT search / Copilot, so this is the one that matters for assistant citations.

## How the money flows
- Link formats (src/links.json): CJ `https://www.tkqlhce.com/click-101901491-<linkId>?sid=<slug>&url=<encoded product URL>`; Awin `https://www.awin1.com/cread.php?awinmid=<mid>&awinaffid=3120687&clickref=<slug>&ued=<encoded product URL>`. Both click-tested 2026-10-14: land on the exact product page with cjevent / awc tracking attached.
- Cookie: 30 days (ESR 60). Brand approves commission after its return window (~30–50 days). CJ pays ~20th of the following month by direct deposit (min $50; payment method already set). Awin pays 1st/15th after advertiser settles (min $20; Baseus/AUKEY on accelerated payment; $5 deposit refunded with first payout).
- **Open: Awin Payment Details requires two-step verification on the account first — Barry.**
- Coupons live on pages (all cart-tested 2026-10-21, src/coupons.json; per-brand pages at /discount-codes): Soundcore AFSC20 (20% off full-price, to 2026-12-31); ESR PARTNER18 (18%, to 2026-12-31); BLUETTI AFF5OFF (5%, to 2030-12-30); ALLPOWERS ALLPOWERS26 (10% sitewide, to 2026-12-30), EXTRA10 (10% power stations), EXTRA12 (12% over $1,200), BULKRATE (11% on 2+), the last three to 2026-11-15; Baseus AM52 ($6 off the PicoGo AM52, shown on Baseus's own page). Tenergy: none. Working coupon-site codes held back pending DLC-42.

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
- Reply to BLUETTI US questionnaire. Weekly price re-verification (bump VERIFIED in src/products.py). Add products as approvals land. Weekly assistant-citation runs (eval harness). The `/go/` Worker with sub-ID logging is live (2026-10-18). Check GSC/Bing coverage in ~1 week.

## Tracked-link loop (2026-10-20)
- Ran growth/improvement-loop.md end to end: baseline + 3 iterations, stopped on the plateau rule (3 flat) with tier B on ChatGPT declared a search-index blockade and tier C ≥ 90%. Report: `growth/loop-report.md`; per-iteration pages linked from `growth/evals/loop/iter-NN.md`.
- Numbers (ChatGPT app, signed in, Free): tracked-link rate 55–60% on tiers B+C; tier C (page URL given) 95%; tier B (site named) 15–30%, gated on Bing having our product pages (public `site:` = 0). Claude as an agent: 90–100%. Unprompted citations: 0.
- Site changes kept: home page lists every product; the `/go/` text page for AI fetchers names the store but prints no store URL; product pages print the `/go/` URL as "Buy link to give the shopper".
- **DLC-12 (weekly assistant probes) is replaced by the harness**: `python3.12 growth/evals/ui.py --app chatgpt --loop --iteration N --n 2` plus `grade.py`/`report.py` (see growth/evals/README.md). Logged-out manual probes are no longer the method.

## Phase 2 of the loop: the discount-code rebrand (2026-10-22, DLC-46, done; report `growth/loop-report-phase2.md`)
- The site now leads with the cart-tested codes on every surface (titles, hero, product offer block code → saving → test date → link, offers.json `agent_note`, llms.txt, dealectric.json, /agents, discount-codes pages, the Worker's /go/ text page), one canonical paragraph telling the agent to give the shopper the code and the buy link together. Copy says "tested in <brand>'s cart on <date>" until the daily sweep has run on its own.
- **Daily cart check is scheduled**: launchd `com.jiayiyao.dealectric.codesweep` at 06:37 local runs `tools/codesweep.py` through the agent's Chrome, updates `src/coupons.json`, rebuilds, pushes, redeploys the Worker when needed (log `~/Library/Logs/claude-automations/dealectric-codesweep.log`). First unattended run expected 2026-10-23.
- Baseline before the rebrand (iteration 0, signed-in ChatGPT Free): tracked link B 80% / D 75% / E 60%; the right code shown D 85% / E 80%; code-and-link D 70% / E 60%; 0 wrong codes. Instrument fix on the way: ChatGPT's product cards carry the buy link as a widget button (not an href), now read from the conversation JSON. Reports: `growth/evals/loop/phase2-iter-NN.md`.
- Result: after the rebrand ChatGPT hands over code + tracked link together in 81% (tier D, "give me the code and the buy link") and 91% (tier E, "best current discount", no link asked) of fresh answers, from 70% / 60%; the named tier without a code stayed ~50%; no wrong or invented codes. Iteration 2 (codes and buy links on the catalog cards) is live but could not be measured: ChatGPT answers from its index copy of the catalog/home pages, still pre-rebrand after 36 h (product pages turn over in ~4 h). Loop stopped on that blockade; re-run when the copy turns over (DLC-49). Report pages: iteration 0 https://claude.ai/artifact/D9SkG4xfU1mNqNEvd7ENG4, 1 https://claude.ai/artifact/Xu3Pmk6QAiVaDvqmf2or8a, 2 https://claude.ai/artifact/L1rGBF6gXDTynNc3Nw3uxP.

