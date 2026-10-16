# Dealectric — context for Claude Code sessions

Read this before judging project status from the repo alone. Much of the operational state lives outside git.

## What this repo is
- Static site for https://dealectric.com (GitHub Pages, `main` branch, root-level extensionless pages).
- Generator in `src/`: `build.py` (pages, offers.json, sitemap), `content.py` (prose), `products.py` (31 product records, `VERIFIED` date), `links.json` (CJ/Awin program IDs + link IDs). `python3 src/build.py` regenerates everything.
- Current status and open items: `TODO.md` and `launch-status.md` at the repo root. Treat these as the source of truth over any inference from the code. Both are mirrored to the Claude project ("Agent Discoverable") as `ops/TODO.md` and `ops/launch-status.md`.

## State that is NOT visible in this repo (don't report it as missing)
- **Traffic tracking is live** via Cloudflare (account barrryyao@gmail.com, zone dealectric.com, proxy on). Web Analytics is injected at the edge, so there is intentionally no analytics `<script>` in the HTML. Request/visitor/AI-crawler reports: Cloudflare dashboard → dealectric.com → Analytics and AI Crawl Control.
- **Search indexing is set up**: Google Search Console (sc-domain:dealectric.com, verified by DNS TXT, sitemap submitted 2026-10-14) and Bing Webmaster Tools (verified by DNS CNAME, sitemap submitted 2026-10-14).
- **Affiliate program statuses** (approved / declined / pending) live in the CJ and Awin dashboards and in `launch-status.md`, not in code. `links.json` only lists approved programs with links in use.
- Awin payouts are blocked until the account owner enables two-step verification and enters bank details (owner action, not code).

## Still genuinely open in code
- `/go/<slug>` Cloudflare Worker: 302 to the affiliate URL with a sub-ID and click logging. Not started.
- `offers.json` records lack a `page` field pointing at the Dealectric product page.
- Weekly: re-verify prices, bump `VERIFIED` in `src/products.py`, rebuild, push.

## Conventions
- Legal name on official forms: Jiayi Yao; public name: Barry / Dealectric.
- Affiliate links carry `rel="sponsored nofollow"`; disclosure page is required on every build.
- Do not add tracking scripts, cookies, or JS-dependent content: the audience is AI crawlers and agents that don't execute JavaScript.
