# Promote run, 2026-11-03: the 72 comparison pages built today (G16–G93)

Barry's call (2026-11-03 evening): run the Promote tiers of the fast loop (skill step 7b) for today's pages, since
Cloudflare showed OAI-SearchBot fetching every new product and code page within hours and none of the 72 comparison
pages, which nothing linked to.

## Tier 1, internal links (all 72 pages) — done, commit 3081acf
`build.py guides_index_html()` renders every comparison page, grouped by the category of the product it recommends and
linked with its own question as the anchor, on the four pages OAI-SearchBot fetches most: home (`/`), `/products/`,
`/discount-codes/` and the power-stations guide (`/portable-power-stations`, power categories only). IndexNow sent for
those four pages (HTTP 200). Check in `growth/focus/crawls/fetches.jsonl` how long the first comparison-page fetch takes
after the links went live (the RV page took about 11 h on 10-31).

## Tier 2, submissions
- IndexNow: all 72 pages submitted on publish (HTTP 200 each batch) plus the four linking pages after tier 1.
- Google Search Console "Request indexing": run from a background tab of the Agent Chrome (`scratchpad/gsc.py`, CDP:
  inspect bar, Enter, click the Request indexing button, wait for "Indexing requested") for the eight shortlisted
  pages below; GSC's daily quota is about 10 requests per property, so the other 64 rely on the sitemap. Results below.

## Tier 3, outreach (shortlist)
Shortlist rule (Barry, 11-03): our product is the first answer in the lead; the win is verified on first-party prices;
in stock with a working code; commission per sale pays for Barry's review time; live demand on a venue that allows a
disclosed link. Pages sent to research (one Fable agent each, `growth/focus/fastloop-briefs/outreach-brief.md`):

| Page | Why | Research output |
|---|---|---|
| /best-48v-lithium-golf-cart-battery-kit-with-charger-club-car | Vatrer kit beats every complete kit but LiTime on first-party price; $1,580 ticket at 3% | outreach-vatrer-golf-cart.md |
| /best-triple-screen-laptop-extender-16-inch-1920x1200 | Only 16-inch 1200p triple; $450 at 10% with code FOPO | outreach-fopo-s788.md |
| /solar-panel-for-blink-outdoor-4-without-a-camera-bundle | Blink's own mount excludes the Outdoor 4; recurring question | outreach-blink-outdoor-4-solar.md |
| /best-nas-under-500-for-docker-immich-home-assistant, /best-nas-for-immich-iphone-photo-backup | DXP2800 is the x86 8 GB box under $400 | outreach-dxp2800-immich-docker.md |
| /best-all-nvme-nas-under-900 (+ Thunderbolt 4 page) | DXP480T Plus near-unique all-flash TB4 at $900 | outreach-dxp480t-all-nvme.md |
| /best-usb-switch-two-computers-keyboard-mouse-ssd (+ KVM page) | $40.99 CM691, one-to-one query match | outreach-usb-switch.md |
| /power-station-to-run-a-refrigerator-for-24-hours (+ freezer, sump, furnace) | Elite 200 V2 with measured Wh; most-asked sizing question | outreach-fridge-power-station.md |

Instruction set for Barry: `promote-tier3-instructions.md` (one task per post, filled up to Submit in the Agent Chrome).
