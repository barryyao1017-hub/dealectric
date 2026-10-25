# Phase 3, iteration 2 — a note to AI assistants on each comparison page (2026-10-25)

Run `2026-10-25-p3iter02`; change `loop3-2` (dc8acc3), revision r2. Gate passed on its 2nd try (00:37Z; the 00:17Z
try still read r1, so ChatGPT's copy of a given page lives 75–95 minutes). F07-2 timed out on the first pass and was
re-asked (`errored-F07-F-2.json` kept).

## Grader and Worker fix found in this iteration

ChatGPT wrote `https://dealectric.com/go/allpowers-sp037-400w` (the id shortened; it is
`allpowers-sp037-400w-solar-panel`) in all four F09 answers of iterations 1 and 2. The Worker answered 404: a dead buy
link handed to the shopper. Fixed on 2026-10-25 (Worker version 297fe362): `/go/<slug>` resolves to the one offer whose
id starts with the slug when the slug is ≥ 8 characters and matches exactly one id (`bluetti-ac` stays a 404).
`evallib.resolve_go_slug` applies the same rule, and iterations 0–2 were re-scored with it (`grade.py --rescore`).

## Re-evaluation (re-scored)

| assistant | iteration 0 | iteration 1 | iteration 2 | code + link (it. 2) | controls |
|---|---|---|---|---|---|
| ChatGPT app | 12/24 | 14/24 | **19/24 (79%)** | 14/24 | 4/4 pass |
| claude-code | 12/12 | 12/12 | 11/12 | 8/12 | 2/2 pass |

Before the re-score the same runs read 12 → 13 → 16; the decision is the same either way.

## Decision

Improvement (+5 over iteration 1): kept. The note turned the power-station swaps into links: F01 0/4 → 2/2, F05 and
F06 2/2. claude-code F11 linked Tenergy's combo page once (11/12; noise at n = 1). What remains on ChatGPT: F04-1 an
honest Anker pick; F07-1 a Renogy panel recommended; F08 ×2 a compatibility answer with no links at all; F12-2
Tenergy's own store page.

## Hypothesis (iteration 3)

The remaining misses are answers to "will X work / which one for this job" that end in prose. A "Picks" list near the
top of each page, one line per job the page answers (the honest pick for each, ours with code and link, others named
with no link), gives ChatGPT a ready line to quote with its link for questions like F08 and F07. Expected ≥ 21/24;
controls must still pass (the CPAP picks name the Anker C1000 Gen 2 as the quietest, the charger picks the Powerex
MH-C801D as the fastest and the EBL C9008 as the cheapest USB-C 8-bay).

## Change

Lever 2 (loop3-3): `picks` on each record in `src/compare.py`, rendered by `compare_page()` under the assistant note;
revision r3.
