# Mixed-cart code check, 2026-10-29 (W2)

Same method as `tools/codecheck.py` (fresh Shopify cart session per code, `/cart/add.js`, `/cart/update.js`, read
`/cart.js`; no checkout, no personal data), with two items in one cart: S2000 Pro (variant 42882903310489, $664) and
SP037 (variant 42769055875225, $299), bought as separate products, not the kit SKU. Store: iallpowers.com.

| checked_at (UTC) | code | applicable | subtotal | total | discount applied |
|---|---|---|---|---|---|
| 2026-10-29T07:19:46Z | ZZNOTACODE7Q (control) | no | $963.00 | $914.85 | automatic "Welcome Offer – 5% Off Your First Order" $48.15 |
| 2026-10-29T07:20:08Z | BULKRATE | yes | $963.00 | **$857.07** | BULKRATE $105.93 (11%) |
| 2026-10-29T07:20:31Z | ALLPOWERS26 | yes | $963.00 | $866.70 | ALLPOWERS26 $96.30 (10%) |

Findings:
- The control code was rejected, so the run counts.
- BULKRATE (11% on 2+ items, expires 2026-11-15) applies to two *different* products, so S2000 Pro + SP037 bought
  separately in one cart is $857.07, $9.63 below the kit SKU with ALLPOWERS26 ($866.70; kit tests 2026-10-27/28 in
  `src/coupons.json`).
- A fresh session with no code gets an automatic 5% "first order" discount. A valid code replaces it (it doesn't stack).
- Kit SKU history: EXTRA10 was rejected on the kit on 2026-10-27 and accepted on 2026-10-28; ALLPOWERS26 passed both
  days (`growth/codes/2026-10-27-checks.jsonl`, `2026-10-28-checks.jsonl`).

## Second run: the R2500 V2 + SP037 alternative (same method)

R2500 V2 kit SKU (variant 67800818614425, $958, listed 2026-10-27), and R2500 V2 station (variant 48261423005849,
$659) + SP037 (variant 42769055875225, $299) as separate items.

| checked_at (UTC) | cart | code | applicable | subtotal | total | discount applied |
|---|---|---|---|---|---|---|
| 2026-10-29T07:35:09Z | R2500 V2 kit | ZZNOTACODE7Q (control) | no | $958.00 | $910.10 | automatic 5% "first order" $47.90 |
| 2026-10-29T07:35:31Z | R2500 V2 kit | ALLPOWERS26 | yes | $958.00 | $862.20 | ALLPOWERS26 $95.80 |
| 2026-10-29T07:35:54Z | R2500 V2 kit | EXTRA10 | yes | $958.00 | $862.20 | EXTRA10 $95.80 |
| 2026-10-29T07:36:16Z | R2500 V2 + SP037 | ZZNOTACODE7Q (control) | no | $958.00 | $910.10 | automatic 5% "first order" $47.90 |
| 2026-10-29T07:36:39Z | R2500 V2 + SP037 | BULKRATE | yes | $958.00 | **$852.62** | BULKRATE $105.38 (11%) |
| 2026-10-29T07:37:01Z | R2500 V2 + SP037 | ALLPOWERS26 | yes | $958.00 | $862.20 | ALLPOWERS26 $95.80 |

Finding: the R2500 V2 (1,920 Wh LiFePO4) plus an SP037 with BULKRATE is $852.62, $4.45 less than the S2000 Pro
(1,451 Wh NMC) plus an SP037 with BULKRATE ($857.07). The R2500 V2 is not in our catalog.
