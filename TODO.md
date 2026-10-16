# Dealectric — TODO (as of 2026-10-16, MVP shipped)

Live: https://dealectric.com · Repo: github.com/barryyao1017-hub/dealectric · Local: ~/Desktop/dealectric · Status detail: launch-status.md (same file as ops/launch-status.md in the Claude project)

## Waiting on networks (nothing to do — 17 applications pending, checked 10/16)
- CJ (11): Audioengine, Baseus US Amazon, eufyMake, Jackery, KOSS, Marshall, Monoprice, NOMAD, SanDisk, Ugreen, ZAGG+mophie.
- Awin (6): Twelve South, Jackery US, SwitchBot, Wyze, PECRON, AUKEY.
- Declined so far: EcoFlow, Harman, OtterBox, Scosche, Sony, X-Sense (CJ); UGREEN (Awin); Impact Marketplace. Reapply to these once Cloudflare shows real traffic (~30–60 days).
- Anker invitation email unanswered.

## Needs Barry (credentials / accounts)
- [ ] (Optional) **Rakuten** publisher account — Anker (mid=43469) and Anker SOLIX (mid=53552) fallback while Impact is stalled.
- [ ] Register store accounts for refer-a-friend links: anker.com, soundcore.com, ankersolix.com; Jackery needs only an email.
- [ ] Delete `~/Desktop/_to_delete/` (a partial clone I couldn't remove).
- [ ] Awin: turn on two-step verification (Account → Security) and enter bank details under Payment Details — Awin commissions can't be paid out until then.
- [ ] Sign in to CJ and Awin when asked (sessions expire daily).

## Claude (runs as soon as the item above it is unblocked)
- [ ] Reply to BLUETTI US welcome questionnaire (Awin).
- [ ] Weekly: re-verify the 31 prices/stock on official pages, bump VERIFIED in src/products.py, rebuild, push.
- [ ] On each new approval (17 pending): add 3–5 products for that brand to src/products.py.
- [ ] Daily: check barrryyao@gmail.com for CJ/Awin approvals and Anker reply; on approval generate deep links and fill the packet tracker.
- [ ] Impact: appeal denied 10/12 — retry brand-direct links (Anker, SOLIX, eufy, Belkin) and email affiliate managers for invitations; reapply to Marketplace once Cloudflare shows traffic.
- [ ] Cloudflare `/go/<slug>` redirect Worker with sub-ID logging (step 6 of the plan) — once the first product pages with tracking links exist.
- [ ] Pull refer-a-friend links + terms into the tracker once store accounts exist.
- [ ] Offer schema v0.1 + first 20 product records (chargers / power banks / power stations) with JSON-LD and real tracking links.
- [ ] Weekly synthetic probes: ask ChatGPT / Claude / Perplexity / Gemini a fixed set of charging questions; log whether dealectric.com is cited.
- [ ] Reapply to Impact Marketplace in 30–60 days if the appeal fails.

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
