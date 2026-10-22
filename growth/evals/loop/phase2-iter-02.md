# Phase 2, iteration 2 — the catalog page hands over the code and the buy link too (planned 2026-10-22)

Report: _(artifact URL, added when published)_

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

**ChatGPT, first pass** (run `2026-10-22-p2iter02`, 19:30–19:58Z, 44 chats; the positive control and Q21-D-1 timed
out and are re-asked): on the fresh cells, code-and-link D 10/13, E 9/9, D+E 19/22 (86%; iteration 1: 85%), tier B
3/5; tracked link D 10/13, E 9/9. **Flat on the fresh cells.** 14 of 39 answers read a pre-deploy copy: the tier-E
and some tier-B cells still quote "October 14, 2026", and the Q17 tier-D answers that link `/products` quote the
Elite 30 V2 at $279.99, its price before the 10/21 price check, i.e. ChatGPT's index copy of the catalog page
predates not only this iteration but the rebrand itself (36 h+). Those are exactly the cells this iteration's change
targets, so the first pass cannot see the lever either way. A tier-C chat on an opened product page (the Elite 200
V2, 20:05Z) reads the current code and link, so product pages are fresh in the index while the catalog and home
pages are not. The stale and timed-out cells are re-asked at 22:00Z.

## Decision

_(pending)_
