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
- **Publishing:** only codes from the affiliate networks or the brand's own site get `publish: true`. Codes that work but appear only on coupon sites stay `publish: false` until Barry decides. Many affiliate terms allow only network-issued codes, and some coupon-site codes are newsletter or "next order" codes the brand may not want posted.
- **Rejected codes:** listed on the brand's page so shoppers and assistants don't keep trying them.

## Re-checking: the daily sweep (since 2026-10-22, DLC-46)

`tools/codesweep.py` re-tests every published code on every catalog product it applies to, every day, through the
agent's Chrome (a tab on each store, cart calls from the page's own context, so the store sees a normal browser
session; Soundcore's `us.soundcore.com` over plain HTTP, because a browser tab there is sent on to the non-Shopify
`www.soundcore.com`). Pacing (DLC-48): stores interleaved, 30 s between a store's checks (ALLPOWERS 90 s); after a 429
the store cools down for its Retry-After or 3, 6, 12, then 20 min, and its gap widens up to 5 min; a check is tried up
to 6 times, and a store still limited 3 h into the run leaves its remaining checks unanswered. The run can take hours. It appends to
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
test dates ("tested in the brand's cart on <date>"), never "daily" or "guaranteed" until the sweep has a track record.

By hand: `python3.12 tools/codesweep.py --dry-run` lists the checks; `--no-push` checks, merges and rebuilds only.

## Logs

- `2026-10-21-checks.jsonl`: first sweep. One JSON object per check: code, store, product, subtotal, `code_amount`, the Shopify discount applications, and `checked_at`.
