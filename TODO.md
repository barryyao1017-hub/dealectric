# Dealectric — TODO (as of 2026-10-10)

Live: https://dealectric.com · Repo: github.com/barryyao1017-hub/dealectric · Local: ~/Desktop/dealectric

## Needs Barry (credentials / accounts)
- [ ] Create **Awin** publisher account — https://ui.awin.com/publisher-signup (Company: Dealectric; tax residency US; promotional type: content/comparison; space: https://dealectric.com; $5 refundable deposit). Unlocks Ugreen, Satechi, Jackery, Bluetti, Baseus, 1MORE, Aukey, Sharge, Reolink, DJI.
- [ ] Create **CJ** publisher account — https://signup.cj.com/member/signup/publisher/ (email, password, country, captcha). Unlocks Soundcore (CID 7382109), Bluetti, Ugreen, Jackery.
- [ ] (Optional) **Rakuten** publisher account — Anker (mid=43469) and Anker SOLIX (mid=53552) fallback while Impact is stalled.
- [ ] Register store accounts for refer-a-friend links: anker.com, soundcore.com, ankersolix.com; Jackery needs only an email.
- [ ] Create **Cloudflare** account (free) — see "Traffic tracking plan" below.
- [ ] W-9 + payout details inside each network once approved.
- [ ] Delete `~/Desktop/_to_delete/` (a partial clone I couldn't remove).

## Claude (runs as soon as the item above it is unblocked)
- [ ] Awin: fill profile from the packet; apply to Ugreen, Satechi, Jackery, Bluetti, Baseus, 1MORE, Aukey, Sharge, Reolink.
- [ ] CJ: fill profile; apply to Soundcore, Bluetti, Ugreen, Jackery.
- [ ] Watch barrryyao@gmail.com for the Impact support ticket (Marketplace appeal) and Anker's reply; accept any program invitations.
- [ ] Cloudflare: execute the "Traffic tracking plan" below (nameservers → proxy → analytics → AI-crawler report → `/go/` worker).
- [ ] Pull refer-a-friend links + terms into the tracker once store accounts exist.
- [ ] Google Search Console: verify dealectric.com, submit sitemap.xml.
- [ ] Offer schema v0.1 + first 20 product records (Anker chargers / power banks / cables) with JSON-LD on real product pages.
- [ ] Weekly synthetic probes: ask ChatGPT / Claude / Perplexity / Gemini a fixed set of charging questions; log whether dealectric.com is cited.
- [ ] Reapply to Impact Marketplace in 30–60 days if the appeal fails.

## Traffic tracking plan (why Cloudflare)
Today nothing records visits: GitHub Pages has no logs or analytics, and the repo's Insights → Traffic counts repository views, not dealectric.com. Ordinary JS analytics would also miss the visitors that matter most — AI crawlers (GPTBot, ClaudeBot, PerplexityBot) and agent fetches don't execute JavaScript — so seeing agent traffic needs something that sees raw HTTP requests.

The cleanest free setup that covers both is to put the domain behind Cloudflare. Porkbun's DNS is already hosted on Cloudflare's infrastructure, but it's DNS only; switching the nameservers to a Cloudflare account of our own and turning on the proxy makes every request pass through Cloudflare, and the free plan then gives three things at once: request-level analytics for all traffic including bots; Cloudflare's AI crawler report that names which AI bots fetched which paths (exactly the "did ChatGPT read my site" question); and a cookie-free Web Analytics beacon for human visits. It also sets up the `/go/` redirect worker with sub-ID logging that the plan already calls for, since that runs on the same free tier. GitHub Pages keeps hosting the files; nothing about the site changes.

Steps once the account exists (Claude does all of these):
1. Cloudflare → Add site → dealectric.com (Free plan); it imports the existing A/CNAME/MX records.
2. Porkbun → Authoritative Nameservers → replace with the two Cloudflare nameservers. Propagation 1–2 h.
3. Cloudflare DNS: set the 4 A records and www CNAME to **Proxied**; keep MX/TXT (email forward) **DNS only**. SSL/TLS mode: Full.
4. Cloudflare Web Analytics → add site → put the beacon `<script>` in the page head via `VERIFY`/head in `src/build.py`; rebuild, push.
5. Analytics & Logs → Traffic / Security → bot report; AI Audit / AI Crawl Control → confirm AI crawlers are **allowed** (we want them) and the per-bot report is on.
6. Workers: deploy `/go/<slug>` → 302 to the affiliate URL with a sub-ID (`?subId1=<page>-<ts>`), log click to Workers Analytics Engine / KV; route `dealectric.com/go/*` to the worker.
Expectation: near-zero for the first weeks; the first real signal is crawler hits after affiliate approvals and search indexing.

## Done
- [x] Vertical chosen (consumer electronics, charging/power first); affiliate program map; application packet.
- [x] Domain dealectric.com (Porkbun), DNS, hello@ forward.
- [x] Site built (generator in `src/`), deployed on GitHub Pages, HTTPS enforced.
- [x] Impact account + verified property; Marketplace appeal ticket filed; Anker invitation email sent.
- [x] Repo cloned to ~/Desktop/dealectric; generator source committed under `src/`.
