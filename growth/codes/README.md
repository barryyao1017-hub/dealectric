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

## Re-checking

Before each weekly price check (DLC-9):
1. Rerun every published code on at least one product per brand.
2. Update `tests` and `checked` in `src/coupons.json`.
3. Rebuild.

A code that fails twice in a row moves to `result: "rejected"`.

## Logs

- `2026-10-21-checks.jsonl`: first sweep. One JSON object per check: code, store, product, subtotal, `code_amount`, the Shopify discount applications, and `checked_at`.
