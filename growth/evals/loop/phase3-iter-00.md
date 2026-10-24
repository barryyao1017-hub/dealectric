# Phase 3, iteration 0 — baseline (2026-10-24)

Run `2026-10-24-p3iter00`; site commit 9674b72; design in `growth/improvement-loop.md` "Phase 3"; summary
`python3.12 growth/evals/p3summary.py --run-id 2026-10-24-p3iter00`.

## Numbers

| assistant | ALR (F01–F12) | our product named | code + link | controls X01/X02 |
|---|---|---|---|---|
| ChatGPT app (n = 2) | **12/24 (50%)** | 24/24 | 6/24 | 4/4 pass |
| claude-code (n = 1) | 12/12 (100%) | 12/12 | 9/12 | 2/2 pass |

## Diagnosis

ChatGPT never fetched the pages directly: it searched with the URL in the query ("dealectric.com/power-station-for-cpap
ResMed AirSense 11 …"), got the page in its search results (every chat), and answered from that copy. Of its 12 misses:

- **7 linked the brand's store for the product it took from our page** (MERCHANT_SWAP and OTHER with a merchant URL):
  F01-1 AC180 → checkout.bluettipower.com, F05-2 / F06-1 / F06-2 Elite 200 V2 → bluettipower.com, F07-1 / F07-2 SP037 →
  iallpowers.com, F10-2 TN480U → power.tenergy.com. It knows the product from the page and fills the link from its own
  catalogue; our `/go/` link sat in the last column of a wide table, away from the name.
- **3 recommended products we do not sell**, honestly (F04-1, F04-2 Anker C1000 Gen 2 / Jackery 1000 v2; F01-2
  Anker): not a copy problem, and not one we should steer.
- **2 gave no links at all** (F08-1, F08-2: a compatibility question, answered in prose).

## Hypothesis (iteration 1)

Proximity: if the `/go/` link sits next to every mention of our product (the table's model cell and the "Short answer"
prose, labelled "buy link to give the shopper" with the code), ChatGPT takes the link from the page with the product
instead of filling it from its catalogue. Expected: the 7 swap cases fall to ≤ 3, ALR ≥ 15/24; controls still pass.

## Change

Lever 1 (loop3-1): `buy_inline()` in `build.py`; `{buy:slug}` in the short answers and the solar page's station table;
the table's model cell carries "Buy link to give the shopper: <go link>", the last column keeps the code only; a
"Revision 2026-10-24 r1" line under each heading for the gating chat.
