# Dealectric — TODO (mirror of the "Dealectric To-Dos" artifact, 2026-10-27)

Source of truth: https://claude.ai/artifact/8eV4jpzzYbQVtotF5EmAkp (IDs DLC-<n>; notes and history live there). This file is a read-only mirror; change rows in the artifact. Status detail: launch-status.md.

## Needs Barry (10)
- [ ] DLC-3 Decide how to get Awin payouts (high)
- [ ] DLC-7 Reply to the BLUETTI US welcome questionnaire (Awin) (high)
- [ ] DLC-30 Ask approved advertisers for Dealectric-exclusive coupon codes (high)
- [ ] DLC-38 Earn inbound links in person: 3–5 Reddit answers a week + outreach to the cited niche blogs (high, weekly)
- [ ] DLC-40 Logins for the consumer-app eval: claude.ai, gemini.google.com, grok.com in the agent Chrome (chatgpt.com already signed in) (high)
- [ ] DLC-4 Create store accounts for refer-a-friend links
- [ ] DLC-5 (Optional) Open a Rakuten publisher account
- [ ] DLC-36 Get dealectric.com into Brave's index (what Claude's search uses)
- [ ] DLC-42 Decide: publish working coupon-site codes (not issued through CJ/Awin)?
- [ ] DLC-53 Confirm CJ/Awin terms allow auto-applying codes from the buy link

## Waiting on others (4)
- [ ] DLC-31 Make sure Bing has indexed dealectric.com (high, due 2026-10-30)
- [ ] DLC-16 17 affiliate applications pending
- [ ] DLC-17 Anker invitation reply
- [ ] DLC-18 Reapply to declined programs once traffic shows (due 2026-11-15)

## Claude (22)
- [ ] DLC-13 Request Google indexing for the last 5 URLs (per-brand discount-code pages) (high, daily, due 2026-10-28)
- [ ] DLC-24 Build the first 3 question-answer comparison pages (high)
- [ ] DLC-32 Optimize pages for what agents actually see: text and search snippet (high)
- [ ] DLC-33 North Star: get our first conversion / commission (high)
- [ ] DLC-37 Agent feedback loop: /go/ click log + /feedback endpoint, then decide on MCP (high, due 2026-11-01)
- [ ] DLC-51 Query-targeted comparison pages: build pages that answer the agents' own narrow search queries and test whether they get cited unprompted (high)
- [ ] DLC-9 Re-verify the 30 prices and stock, bump VERIFIED, rebuild, push (weekly, due 2026-11-03)
- [ ] DLC-12 Weekly assistant-citation run (harness replaces the manual probes) (weekly, due 2026-11-03)
- [ ] DLC-14 Check email for CJ/Awin approvals and add 3–5 products per newly approved brand (daily)
- [ ] DLC-15 Retry Impact via brand-direct links
- [ ] DLC-26 Earn first outside links and mentions
- [ ] DLC-27 Ship a read-only offers API / MCP server and list it in MCP registries
- [ ] DLC-28 Weekly growth scorecard (weekly, due 2026-11-03)
- [ ] DLC-35 Auto-renew our affiliate links
- [ ] DLC-44 Monthly spec and policy re-audit of every product (monthly, due 2026-11-21)
- [ ] DLC-45 Own product images on the site; test whether ChatGPT shows them (due 2026-10-28)
- [ ] DLC-47 Optimize for ChatGPT product cards and images
- [ ] DLC-50 Loop iteration 4: measure the guide-page lever once ChatGPT's home-page copy has turned over (due 2026-10-30)
- [ ] DLC-54 Have the /go/ hop apply the current code in the cart (Baseus, ESR, ALLPOWERS)
- [ ] DLC-55 Void scan: finish the other 70 categories and check ChatGPT
- [ ] DLC-57 Gap pages stage 2: daily readings until indexed and cited (daily)
- [ ] DLC-62 Give /data a license, a citation line and CSV exports before the dataset outreach

## Done on 2026-10-27
- [x] DLC-6 Delete ~/Desktop/_to_delete/
- [x] DLC-52 Add the Tenergy TN438 16-bay AA/AAA charger to the catalog (CJ Tenergy program)
- [x] DLC-58 SP037 panel: product URL points to a sold-out listing
- [x] DLC-61 Keep the Mac awake for the 06:37 cart sweep, or pick another time
- [x] DLC-48 Check the daily cart sweep's first unattended run, then let the copy say 'daily'

## Traffic tracking plan (why Cloudflare)
Today nothing records visits: GitHub Pages has no logs or analytics, and the repo's Insights → Traffic counts repository views, not dealectric.com. Ordinary JS analytics would also miss the visitors that matter most — AI crawlers (GPTBot, ClaudeBot, PerplexityBot) and agent fetches don't execute JavaScript — so seeing agent traffic needs something that sees raw HTTP requests.

The cleanest free setup that covers both is to put the domain behind Cloudflare. Porkbun's DNS is already hosted on Cloudflare's infrastructure, but it's DNS only; switching the nameservers to a Cloudflare account of our own and turning on the proxy makes every request pass through Cloudflare, and the free plan then gives three things at once: request-level analytics for all traffic including bots; Cloudflare's AI crawler report that names which AI bots fetched which paths (exactly the "did ChatGPT read my site" question); and a cookie-free Web Analytics beacon for human visits. It also sets up the `/go/` redirect worker with sub-ID logging that the plan already calls for, since that runs on the same free tier. GitHub Pages keeps hosting the files; nothing about the site changes.

**DONE 2026-10-14** (steps 1–5). Cloudflare account: barrryyao@gmail.com (Google sign-in), account id 2edd290b…, zone dealectric.com on the Free plan, nameservers coraline/odin.ns.cloudflare.com, zone active within minutes. A records + www CNAME proxied; MX/SPF DNS-only (email forwarding unaffected). SSL/TLS: Full. Web Analytics: automatic beacon injection (no site code change). AI crawler policy: Search/Agent/Training all **Allow**; Bot Preference Sync **off** so our own robots.txt is served untouched.
Where to look:
- Human + bot requests: Cloudflare → dealectric.com → Analytics → Traffic (Requests / Visitors tabs).
- "Did ChatGPT/Claude/Perplexity read the site?": dealectric.com → AI Crawl Control → Overview (per-bot counts: GPTBot, ChatGPT-User, ClaudeBot, PerplexityBot, Googlebot, Bingbot, Applebot…).
- Page views by path: Account → Observability → Analytics → Web analytics.
- Search indexing: Google Search Console (sc-domain:dealectric.com, Google account yaojiayi1017@gmail.com, verified by TXT record; sitemap read, 42 pages discovered) → Indexing → Pages. Bing Webmaster Tools (dealectric.com, signed in via Google, verified by CNAME f303e07e…→verify.bing.com; sitemap submitted 10/14) → Site Explorer / Search Performance. Both show impressions + clicks once indexed (typically 1–2 weeks).
Remaining: 6. Workers: deploy `/go/<slug>` → 302 to the affiliate URL with a sub-ID (`?subId1=<page>-<ts>`), log click to Workers Analytics Engine / KV; route `dealectric.com/go/*` to the worker.
Expectation: near-zero for the first weeks; the first real signal is crawler hits after affiliate approvals and search indexing.

## Done
- [x] Vertical chosen (consumer electronics, charging/power first); affiliate program map; application packet.
- [x] Domain dealectric.com (Porkbun), DNS, hello@ forward.
- [x] Site built (generator in `src/`), deployed on GitHub Pages, HTTPS enforced.
- [x] Impact account + verified property; Marketplace appeal ticket filed; Anker invitation email sent.
- [x] Repo cloned to ~/Desktop/dealectric; generator source committed under `src/`.
- [x] 2026-10-11: CJ account activated (profile, property, W-9, payment) + 8 applications; Awin account approved (profile, logo) + 5 applications.
- [x] 2026-10-11: full CJ electronics-category sweep + Awin brand search → 35 applications total; 10 approved by 10/13.
- [x] 2026-10-14: Cloudflare live — proxy, SSL Full, Web Analytics, AI Crawl Control report. Visits are now recorded.
- [x] 2026-10-14: Google Search Console + Bing Webmaster Tools verified, sitemap.xml submitted to both.
- [x] 2026-10-14: **MVP shipped.** 31 products / 6 brands at /products, each with normalized specs, JSON-LD, a verified offer and a tracked link (CJ deep links + Awin cread links, click-tested end to end); /offers.json machine feed; guides cross-link the catalog. Source: src/products.py + src/links.json.
