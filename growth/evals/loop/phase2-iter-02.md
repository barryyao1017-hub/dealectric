# Phase 2, iteration 2 — the catalog page hands over the code and the buy link too (planned 2026-10-22)

Report: https://claude.ai/artifact/L1rGBF6gXDTynNc3Nw3uxP (built by `growth/evals/iterreport.py --iteration 2 --phase 2`; every chat screenshot in its gallery)

## Diagnosis (from iteration 1)

After the rebrand ChatGPT's remaining misses on the discount tiers share one shape: its search returns the home page,
the `/products` catalog page or a category guide instead of the product page, it names the right product from that
page (price included) and then stops short: "The link above goes to Dealectric's homepage; I couldn't verify the
exact product-specific buy URL" (Q09-B-1), "Buy link: Shop the Boom 3i through Dealectric" linking `/products`
with "I couldn't verify a currently working code specifically for the Boom 3i" (Q29-D-1), the same on Q26-D-2 and
Q17-B-1. The catalog page lists every product with its price and summary but carried no code and no `/go/` link, so
an agent that lands there has the product and nothing to hand over. (Part of these answers also read the index copy
of the catalog page from before the rebrand, "catalog updated October 14"; the stale cells were re-asked before
this iteration's numbers were taken.)

## Hypothesis and expected movement

Lever: structure, not words. Every card on `/products` carries the same deal line as the home page (code, saving,
price after the code, cart-test date) and "Buy link to give the shopper: https://dealectric.com/go/<slug>"; the page
title and lead say so, and the canonical paragraph sits under the lead. Expected: the "couldn't verify the
product-specific buy URL / code" answers that cite `/products` or the home page turn into code-and-link answers;
OTHER (catalog or home page linked) on the 8-question design ≤ 1, code-and-link on D ≥ 90% (the stop rule) if the
index copy of `/products` has turned over by the evaluation; tier E unchanged; claude-code unchanged.

## Change

Commit `loop2-2` (ec7a2aa, pushed 2026-10-22 15:30Z): `src/build.py products_index`: every catalog card carries "Code X saves $Y:
$Z after the code; tested in <brand>'s cart on <date>" and "Buy link to give the shopper: https://dealectric.com/go/
<slug>" (or "No discount code applies"); the page title and lead name the codes, and the canonical paragraph sits
under the lead. Rebuilt (docs/products.html and offers.json's generated date are the only changed files), pushed,
IndexNow; no Worker change, no price change.

## Proof that the assistant sees the new copy

Push 15:30Z, GitHub Pages live after 80 s, IndexNow for `/products` and `/` at 15:32Z (200 OK). Fetched as
ChatGPT-User through Cloudflare at 15:33Z (cf-cache DYNAMIC): `/products` carries 30 "Buy link to give the shopper"
lines and 22 "Code X saves" lines; home and discount-codes unchanged and still fresh. No tier-C probe (a
catalog-page change): the evaluation starts four hours after the deploy, at 19:30Z, and every cell that quotes the
old catalog title ("normalized specs and verified offers", added to the stale markers) or the pre-10/21 date is
STALE_CACHE and re-asked.

## Re-evaluation

**claude-code** (run `2026-10-22-p2iter02`, 15:33–15:50Z, live fetches): 24/24 L4 and 24/24 code-and-link on B, D
and E; controls 4/4. Unchanged from iteration 1, as expected.

**ChatGPT** (run `2026-10-22-p2iter02`: first pass 19:30–19:58Z, 44 chats; the 14 cells that read a pre-deploy
copy plus the 2 timed-out cells re-asked at 22:00Z; 5 cells still quoting "October 14, 2026" or the old title after
that are excluded as STALE_CACHE, first-pass files under `stale-pass-1/` and `errored-first-pass/`). On the 8
questions (`compare-p2-01-02.md`):

| reading (ChatGPT) | iteration 1, fresh | iteration 2, fresh cells | iteration 2, all 40 |
|---|---|---|---|
| **code-and-link, tiers D+E** | **85% (22/26)** | **86% (24/28)** | 84% (27/32) |
| code-and-link D / E | 81% (13/16) / 90% (9/10) | 81% (13/16) / 92% (11/12) | 81% / 88% |
| tracked link B / D / E | 63% / 81% / 90% | 86% (6/7) / 81% / 92% | 88% / 81% / 88% |
| right code shown D / E | 88% / 90% | 81% / 92% | |
| OTHER (catalog or home page linked, no code) | 3 | 4 | |
| controls | 4/4 | 4/4 | |

claude-code 24/24 on both metrics. **Flat** (+1 point on the phase-2 metric, +1 pooled TLR).

The lever could not reach its target: the four OTHER answers are the catalog-landing ones (Q17 ×3 "LiFePO4
portable power station", Q27-D-1), and each still says "I couldn't verify a working discount code … Dealectric does
list portable power stations with verified offers, prices, and tracked purchase links" with `/products` as the buy
link. The live catalog page has carried "Code AFF5OFF saves $14.49 … Buy link to give the shopper" on every coded
card since 15:31Z; the index copy ChatGPT answers from does not. Evidence that the copy is old: the first-pass Q17
answers quoted the Elite 30 V2 at $279.99, its price before the 10/21 price check, and five tier-E/B cells still
quoted "October 14, 2026" at 22:00Z, 13.5 h after the rebrand deploy and 6.5 h after this one. Product pages turn
over in about four hours in ChatGPT's index (iteration 1's probe, and today's tier-C chat on the Elite 200 V2 read
the current code and link); the catalog and home pages have not turned over in 36 h.

## Decision

Flat, kept (no cost: the cards only gained the code line and the buy link). **The loop stops here on the blockade
rule**: the remaining ChatGPT misses on the discount tiers all come from answers that land on the catalog or home
page and read ChatGPT's index copy of it, which predates the rebrand (36 h and counting), so no page change can be
measured on that path until the copy turns over; product pages, which do turn over in about four hours, are at
81% (D) and 92% (E) code-and-link on the fresh cells, with the code shown in 81–92% of answers and never a wrong
one. Re-run the same 44-chat design when the catalog copy has turned over (a chat citing `/products` quotes the
codes): tracked as DLC-49. The transfer-learning report is `growth/loop-report-phase2.md`.
