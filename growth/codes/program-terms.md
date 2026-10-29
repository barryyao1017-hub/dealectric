# Program terms on codes (DLC-53), read 2026-10-29

Read in the agent's Chrome from the CJ publisher dashboard (Partners → My Advertisers → Program Terms) and the Awin
advertiser profiles (Program Terms tab, Overview text, My Offers filtered by advertiser). The question: may we promote
each code we publish, and may the `/go/` hop put it in the cart (Shopify `/discount/<code>?redirect=`)?

None of the six programs says anything about applying a code from the link. What they do restrict is which codes.

| Program | Network | Rule on codes (quoted) | Our code(s) and where they come from | Verdict |
|---|---|---|---|---|
| ALLPOWERS | CJ | "Publishers may only use coupons and promotional codes that are provided exclusively through the affiliate program" | ALLPOWERS26, BULKRATE, EXTRA10, EXTRA12: CJ affiliate codes | OK |
| Aurzen | CJ | "may use any coupons or promotional codes that are provided through the affiliate program or otherwise available to the public" | CJ10: CJ exclusive | OK |
| Bluetti Global | CJ | same wording as Aurzen | AFF5OFF is a CJ code, but our BLUETTI links run through Awin | see BLUETTI US |
| BLUETTI US | Awin | "Coupon Codes: Only codes provided via the BLUETTI Affiliate Program may be promoted. Unauthorized code usage will result in commission reversal and possible removal from the program." (Overview, "Campaign Terms and Conditions") | AFF5OFF is **not** among the 13 codes in Awin My Offers for BLUETTI US | **Risk: reversal on every BLUETTI sale (DLC-72)** |
| Baseus (US) | Awin | No program terms, no documents, no offers published | AM52, FC41: printed on Baseus's own product pages (public) | OK as far as anything is written |
| ESR (US) | Awin | No program terms published | PARTNER18: in Awin My Offers, "Exclusive affiliate promotional code", to 2026-12-31 | OK |

BLUETTI US codes in Awin My Offers (2026-10-29): ELITE400AFF (6%, Elite 400 + bundles), NaAFF6 (6%, Pioneer Na),
EP6KAFF6 (6%, EnergyPro 6K), B500KAFF6 (6%, B500K), **ELITE300AFF (8%, Elite 300 + bundles, to 2026-12-31)**,
AFFD60L (5%, Charger 1), EB70S20 ($20, EB70S), RVAFF6 (6%, full-time RV setup), ELITE5OFF (5%, Elite 100 V2 + bundles),
AFFSALE ($8 off orders under $1,000), AFFX20 (10%, X20), AFFX60 ($50, X60), AFFX30 ($30, X30). None covers the AC200L,
AC180, Elite 30 V2 or Elite 200 V2. ELITE300AFF covers a product we list with no code.

## Link test (ESR, 2026-10-29 ~07:40Z, one click)

Real Awin link with clickref `test.dlc53` → `esrtech.com/discount/PARTNER18?redirect=/products/15w-mini-wireless-charger`:
landed on the product page with `awc` and Awin's utm parameters; `discount_code=PARTNER18` cookie set; in the cart the
ESR Magnetic Charging Pad went $19.99 → $16.40 (line discount titled PARTNER18). Cart emptied after. Earlier checks:
ALLPOWERS (CJ) and Baseus (Awin) on 2026-10-24, BLUETTI and Aurzen store side on 2026-10-28 (DLC-54).

## Other things the terms pages show

- Aurzen lists `aurzen` under "Prohibited Web Site URL Keywords" (and Domain Keywords). Our paths
  `/aurzen-discount-codes` and the three `/aurzen-…` product pages contain it. Usually aimed at lookalike domains, but
  the field says URL. Worth asking Aurzen's manager before it costs a reversal.
- Aurzen: 45-day referral period, 10% (12% on the ZIP item list). `links.json` says 30 days.
- ESR: Awin cookie 30 days (`links.json` says 60); payment level "Exposure Level 4" (over its credit limit and
  settlement terms), average payment time 92 days.
- Bluetti Global (CJ): 14-day referral period, 5% (2% on an item list); Awin BLUETTI US: 30 days, 5–10% tiered.
- ALLPOWERS prohibits "unauthorized coupon pages"; ours carry only its CJ codes.
