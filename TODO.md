# Dealectric — TODO (as of 2026-10-10)

Live: https://dealectric.com · Repo: github.com/barryyao1017-hub/dealectric · Local: ~/Desktop/dealectric

## Needs Barry (credentials / accounts)
- [ ] Create **Awin** publisher account — https://ui.awin.com/publisher-signup (Company: Dealectric; tax residency US; promotional type: content/comparison; space: https://dealectric.com; $5 refundable deposit). Unlocks Ugreen, Satechi, Jackery, Bluetti, Baseus, 1MORE, Aukey, Sharge, Reolink, DJI.
- [ ] Create **CJ** publisher account — https://signup.cj.com/member/signup/publisher/ (email, password, country, captcha). Unlocks Soundcore (CID 7382109), Bluetti, Ugreen, Jackery.
- [ ] (Optional) **Rakuten** publisher account — Anker (mid=43469) and Anker SOLIX (mid=53552) fallback while Impact is stalled.
- [ ] Register store accounts for refer-a-friend links: anker.com, soundcore.com, ankersolix.com; Jackery needs only an email.
- [ ] Create **Cloudflare** account (free) — for traffic analytics, AI-crawler report, and the `/go/` sub-ID redirect worker.
- [ ] W-9 + payout details inside each network once approved.
- [ ] Delete `~/Desktop/_to_delete/` (a partial clone I couldn't remove).

## Claude (runs as soon as the item above it is unblocked)
- [ ] Awin: fill profile from the packet; apply to Ugreen, Satechi, Jackery, Bluetti, Baseus, 1MORE, Aukey, Sharge, Reolink.
- [ ] CJ: fill profile; apply to Soundcore, Bluetti, Ugreen, Jackery.
- [ ] Watch barrryyao@gmail.com for the Impact support ticket (Marketplace appeal) and Anker's reply; accept any program invitations.
- [ ] Cloudflare: add site, swap nameservers at Porkbun, proxy the records, enable Web Analytics beacon (add to `VERIFY`/head in build.py), turn on AI-crawler insights, deploy `/go/` redirect worker with sub-ID logging.
- [ ] Pull refer-a-friend links + terms into the tracker once store accounts exist.
- [ ] Google Search Console: verify dealectric.com, submit sitemap.xml.
- [ ] Offer schema v0.1 + first 20 product records (Anker chargers / power banks / cables) with JSON-LD on real product pages.
- [ ] Weekly synthetic probes: ask ChatGPT / Claude / Perplexity / Gemini a fixed set of charging questions; log whether dealectric.com is cited.
- [ ] Reapply to Impact Marketplace in 30–60 days if the appeal fails.

## Done
- [x] Vertical chosen (consumer electronics, charging/power first); affiliate program map; application packet.
- [x] Domain dealectric.com (Porkbun), DNS, hello@ forward.
- [x] Site built (generator in `src/`), deployed on GitHub Pages, HTTPS enforced.
- [x] Impact account + verified property; Marketplace appeal ticket filed; Anker invitation email sent.
- [x] Repo cloned to ~/Desktop/dealectric; generator source committed under `src/`.
