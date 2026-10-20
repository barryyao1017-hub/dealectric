# Iteration 3 — the product page names the /go/ URL as the buy link (2026-10-20)

## Diagnosis (from iteration 2)

chatgpt: tier C 95%; tier B 25% with 11 NOT_FOUND (search index, not addressable on the page) and 3 PAGE_ONLY. In
two of the three PAGE_ONLY answers ChatGPT fetched the product page and its `/go/` link one second apart and still
gave the product page as "Dealectric's buy link". The page showed the `/go/` URL only as the button's href, and its
assistant note sat at the bottom saying "present the link above".

## Hypothesis and expected movement

Lever 1 (wording and placement): the offer block now prints the `/go/` URL in text as "Buy link to give the shopper",
says that neither the page URL nor the store page is the buy link, and carries the assistant note next to the offer.
Expected: PAGE_ONLY on tier B 3/20 → ≤ 1/20, +5 to +10 points on tier B, +3 to +5 pooled; no change on tier C or for
claude-code. If flat, the plateau rule (three flat iterations) stops the loop. Written before the re-evaluation.

## Change

Commit `loop-3:` (site rebuilt, 31 product pages changed; offers.json, links map, prices, disclosure and
rel=sponsored unchanged; no Worker deploy). Live on dealectric.com and pinged to IndexNow.

## Re-evaluation design

≥ 2 h after the push: `ui.py --app chatgpt --loop --iteration 3 --n 2` and `run.py --assistants claude-code --loop
--iteration 3 --n 1`; compare PAGE_ONLY and tier B with iteration 2.

## Re-evaluation

_(filled in after the wait)_
