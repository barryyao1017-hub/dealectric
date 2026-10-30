# Discount-code checks

DLC-29: the site publishes only discount codes that worked in the brand's own US store cart. This folder has the raw check logs. The curated result the build reads is `src/coupons.json`.

## How a code is checked

- **Shopify stores** (BLUETTI, Soundcore via `us.soundcore.com`, ALLPOWERS, Baseus, ESR): `python3 tools/codecheck.py <product URL> [--qty=N] CODE ...`
  - Each code gets a fresh cart session: add one product (`/cart/add.js`), apply the code (`/cart/update.js {"discount": CODE}`), then read `/cart.js`.
  - Shopify reports the code as applicable or not, plus the amount it took off each line. `code_amount` excludes automatic discounts such as Soundcore's "Buy More Save More".
  - No checkout, no personal data, no order.
- **Tenergy** (BigCommerce at `power.tenergy.com`): the storefront cart API refuses scripts (403), so codes go into the cart page's coupon box by hand. The store's message is recorded, e.g. "not valid", "disabled", "expired on …".
- **Controls:** every run includes a made-up code (`ZZNOTACODE7Q`). A run counts only if the control is rejected.
- **Rate limits:** Shopify answers 429 after a handful of cart calls from one IP, and ALLPOWERS stays limited for many minutes. Interleave stores, wait about 12 s between checks, and requeue on a 429. A 429 is never recorded as a rejection.

## Where codes come from, and what gets published

- **CJ:** Campaigns → Links & Products, Promotion Type = Coupons, My Advertisers Only.
- **Awin:** Toolbox → My Offers, filter by advertiser.
- **Coupon sites:** RetailMeNot, DealHack, PriceCheckHQ and the like.
- **Publishing (Barry, 2026-10-29):** only network-issued or brand-approved codes get `publish: true`. Brand-approved means the brand printed the code on its own site, approved it in writing, or its program terms allow public codes (CJ Bluetti Global and Aurzen do; see `program-terms.md`). Codes found only on coupon sites stay `publish: false` otherwise, and a program's own stricter terms always win. To get more codes, ask the brand for one (DLC-30) instead of sourcing them from coupon sites.
- **Rejected codes:** listed on the brand's page so shoppers and assistants don't keep trying them.

## Re-checking: the daily sweep (since 2026-10-22, DLC-46)

`tools/codesweep.py` re-tests every published code on every catalog product it applies to, every day, through the
agent's Chrome (a tab on each store, cart calls from the page's own context, so the store sees a normal browser
session; Soundcore's `us.soundcore.com` over plain HTTP, because a browser tab there is sent on to the non-Shopify
`www.soundcore.com`). Soundcore goes first and alone: no store tab opens until its checks are done or 15 min have
passed, since its first call 429'd for hours on every run where it came seconds after Chrome's calls to the other
stores (10-24 to 10-26). Pacing (DLC-48): stores otherwise interleaved, 30 s between a store's checks (ALLPOWERS 90 s,
Soundcore 60 s); after a 429
the store cools down for its Retry-After or 3, 6, 12, then 20 min, and its gap widens up to 5 min; a check is tried up
to 6 times, and a store still limited 3 h of awake time into the run leaves its remaining checks unanswered (the Mac's
sleep does not count; the run stops at 12 h by the clock). The Mac must be awake for the run: with the lid closed on
battery it sleeps through it whatever `caffeinate` asks (10-24, 10-26). A product URL with `?variant=<id>` is tested on
that variant. A price mismatch is logged when the page price matches neither the cart subtotal nor the cart total
after the store's automatic discounts. The run can take hours. It appends to
`<date>-checks.jsonl` here, folds the results into `src/coupons.json` (`tools/codes_merge.py`), rebuilds, commits
("codes: daily cart check <date>"), pushes, and redeploys the Worker when `worker/src/links-map.json` changed.
Scheduled by `~/Library/LaunchAgents/com.jiayiyao.dealectric.codesweep.plist` (copy in `tools/`) at 06:37 local via
`tools/codesweep.sh`, log `~/Library/Logs/claude-automations/dealectric-codesweep.log`.

Rules: the made-up control code must be rejected by each store or that store's checks are discarded; a code rejected
on every product in one sweep keeps its last passing date and gets `fail_streak: 1`; a second sweep in a row retires
it (`result: "rejected"`, off every page and out of offers.json); a 429 or a network error is never a rejection. A
strike needs a complete answer: if any of the code's checks went unanswered, the code is left exactly as it was that
day. A product the store could not put in the cart (sold out, quantity limit) is inconclusive: it tests nothing and
does not count either way (a sold-out control product moves the control to the store's next product). The
build shows a code on a product only when the latest test on that product passed, and shows the store's own amount
when it was recorded at the current price. `checked` is the date of the last sweep; page copy uses each code's own
test dates. Since 2026-10-27, after the first clean unattended run, the copy says "tested daily in <brand>'s cart, last
passed <date>": the claim is daily testing, and the date is the evidence. Never "guaranteed"; a brand with no published code
(Tenergy) makes no daily claim.

By hand: `python3.12 tools/codesweep.py --dry-run` lists the checks; `--no-push` checks, merges and rebuilds only.

## Product links: the daily link check (DLC-35)

After the cart checks and before it publishes, the sweep runs `tools/linkcheck.py` in its own process (15 min timeout;
a crash, hang or bad result is logged as "links: check failed" and the sweep publishes anyway). For every catalog
product it GETs the record's `url` as a browser would (redirects followed, 3 s between requests to one store, 6 s on
ALLPOWERS and Soundcore, 20 s on BLUETTI), reads the Shopify product JSON (`<url>.js`, Soundcore's on `us.soundcore.com`) or the page's
schema.org availability, and requests `dealectric.com/go/<slug>` without following it, to confirm the Location is the
deep link in `worker/src/links-map.json` with the `<slug>.<click id>` sub-ID. It flags BROKEN, MOVED, DELISTED, SOLD
OUT or BACK IN STOCK (against `in_stock`), a /go/ mismatch and a stale link map; a 429, a bot challenge or a network
error is UNANSWERED, never broken, and a store that refuses both tries gets no more requests that run. Results go to
`<date>-links.json` here and a "links:" line in the sweep's commit message. It only flags: the weekly price check
(DLC-9) edits `products.py`. Each /go/ check is one row in D1 `clicks` with user agent `dealectric-linkcheck-bot`
(`bot_like=1`, so the click counts in `worker/README.md` leave it out). Tenergy's store answers every non-browser client
with a Cloudflare challenge, so its five products come back unanswered every day (their /go/ links are still checked);
the script does not try to get past it. Not checked: CJ/Awin program status (visible
only in the network dashboards), and the tracking parameters on the store's landing page, since seeing those takes a
real click through the network.

## Logs

- `2026-10-21-checks.jsonl`: first sweep. One JSON object per check: code, store, product, subtotal, `code_amount`, the Shopify discount applications, and `checked_at`.
