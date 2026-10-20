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

## Re-evaluation (run `2026-10-20-iter03`, 15:56–16:45Z)

Frozen subset Q10, Q11, Q12, Q13, Q14, Q15, Q16, Q17, Q20, Q29. chatgpt signed in (Free), temporary chats, 40
question chats on B+C plus 18 controls; claude-code once per cell.

| reading | chatgpt | claude-code | iteration 2 |
|---|---|---|---|
| **TLR tiers B+C** | **55% [40–69] (22/40)** | 90% [70–97] (18/20) | 60% (24/40) · 90% |
| tier B | 15% (3/20) | 80% (8/10) | 25% · 80% |
| tier C | 95% (19/20) | 100% (10/10) | 95% · 100% |
| PAGE_ONLY | 3 | 2 | 3 · 2 |
| MERCHANT_SWAP | 1 | 0 | 1 · 0 |
| NOT_FOUND | 12 | 0 | 11 · 0 |
| controls | 18/18 | 9/9 | |

chatgpt −5.0 points, pooled −3.3: **flat** (intervals overlap). The targeted class did not move: PAGE_ONLY stayed at
3 of 20 on tier B. Cloudflare shows ChatGPT fetched the rebuilt product pages in two of the three (Q11-B-2 at
15:57:36Z, Q12-B-1 at 15:58:32Z), read the new "Buy link to give the shopper: https://dealectric.com/go/…" line, and
still answered "Buy link: View product on Dealectric" with the page URL. On tier C, where the prompt itself says
"the exact buy link Dealectric gives", the same pages yield the `/go/` link 95% of the time: the prompt's wording
decides more than the page's. Tier B's other misses are the same search-index class as before (12 NOT_FOUND).

claude-code's two PAGE_ONLY answers (Q15-B-1, Q16-B-1) both contain a `/go/` link for a sibling product that the
question's expected list does not include (AC180 for "home backup under $1,000", T320 for a CPAP): expected-list
gaps, not lost links. One real side effect of iteration 1 shows in its transcripts: since the home page lists every
product, claude-code goes home page → product page and no longer reads offers.json on tier B (74/90 runs did in
iteration 0, 0/30 since); it still finds the `/go/` link on the page, so the tracked-link rate did not move.

## Decision

Flat, kept (no cost). **Third flat iteration in a row: the plateau rule stops the loop** (growth/improvement-loop.md
§6). Also declared, with the evidence above and in iterations 1 and 2: tier B on chatgpt is a **blockade** (12 of 17
misses are search-index misses that no page change reaches; the home page is not opened; OpenAI's own crawler has
only ever fetched robots.txt; Bing's public index has 0 of our pages), and tier C is at or above 90% on both readings
(chatgpt 95%, claude-code 100%). The transfer-learning report is `growth/loop-report.md`.
