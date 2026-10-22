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

_(commit `loop2-2`, pending: `src/build.py products_index` and the catalog page's title/lead; rebuilt, pushed, IndexNow;
no Worker change)_

## Proof that the assistant sees the new copy

_(copycheck.py on /products; a tier-C-style probe is not needed for a catalog-page change: the per-cell stale marker
does the gating)_

## Re-evaluation

_(pending)_

## Decision

_(pending)_
