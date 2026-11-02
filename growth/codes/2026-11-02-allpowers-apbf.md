# ALLPOWERS APBF12 / APBF10 — first cart test (2026-11-02, DLC-139)

Codes from CJ: Links & Products → ALLPOWERS, "Extra 12% OFF Sitewide with Code: APBF12 - All Markets" and the APBF10
(10%) twin, schedule 2026-10-28 to 2026-12-14, network-issued. Tested with `tools/codecheck.py` over plain HTTP on
iallpowers.com (fresh cart each, add → /cart/update.js {discount} → /cart.js). Control ZZNOTACODE7Q: rejected.

| cart | subtotal | APBF12 | APBF10 |
|---|---|---|---|
| S2000 Pro | $549 | not applicable | −$54.90 (10%) |
| P1800 + SP037 kit | $698 | not applicable | — |
| S2000 Pro + SP037 kit | $848 | not applicable | — |
| P1800 + 2× SP037 panel | $997 | not applicable | — |
| P1800 + SF200 kit + 21 W panel | $999.99 | not applicable | — |
| P1800 + 2× SP037 panel + extension cable | $1,016.99 | −$122.03 (12%) | — |
| 2× P1800 + SF200 kit | $1,062 | −$127.44 (12%) | — |
| 2× S2000 Pro | $1,098 | −$131.76 (12%) | — |
| R4000 | $1,499 | −$179.88 (12%) | −$149.90 (10%) |

Findings:
- **APBF12 is not sitewide in the US cart: it needs a $1,000 order** (rejected at $999.99, accepted at $1,016.99).
  Recorded as `min_order: 1000`, "12% off orders over $1,000". Of our single-unit products only the R4000 qualifies.
  There it ties EXTRA12 (12%, ends 11-15) and outlasts it to 12-14; after 12-14 the R4000 falls back to ALLPOWERS26.
- **APBF10 works, 10% sitewide**, the same as ALLPOWERS26, which runs to 12-30. Held (`publish: false`): it would add
  daily checks on ALLPOWERS' rate-limited cart for no saving.
- With no code, the cart applies an automatic "Welcome Offer – 5% Off Your First Order"; an accepted code replaces it.
