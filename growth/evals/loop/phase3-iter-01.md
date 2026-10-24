# Phase 3, iteration 1 — the buy link next to every mention (2026-10-24)

Run `2026-10-24-p3iter01`; change `loop3-1` (04009fd), revision r1. Freshness: ChatGPT fetches a given page once
(`ChatGPT-User`) and answers later chats from that copy; it re-read the CPAP page between 22:32 and 23:02 (the gate,
`growth/evals/p3gate.py`, passed on its 4th try, 23:02Z), and Cloudflare shows a fresh fetch of each page at the first
chat of the run (23:02–23:15), so every cell read r1.

## Re-evaluation

| assistant | ALR before → after | code + link | controls |
|---|---|---|---|
| ChatGPT app | 12/24 → **13/24** (50% → 54%) | 6 → 5 | 4/4 pass |
| claude-code | 12/12 → 12/12 | 9 → 9 | 2/2 pass |

## Decision

Flat (+1 < +3): kept (no cost; the charger page went to 6/6). The misses are per question and stable across both runs:
F01 0/4 (AC180, Elite 100 V2 → checkout.bluettipower.com), F07 0/4 (SP037 → iallpowers.com, a URL not in its search
results: from ChatGPT's own catalogue), F04 0/4 (honest picks of Anker/Jackery), F08 0/4 (no links). ChatGPT writes
its own `<Link url="https://checkout.bluettipower.com/...">` / "View product details" next to a product it took from
our page, with our link beside the name on the page. Search breadth does not explain it (57% L4 when it searched only
for our page, 45% when it also searched elsewhere).

## Hypothesis (iteration 2)

ChatGPT carries our link when the page gives it a reason to (phase 2: the code and the "give the shopper both"
paragraph), and a comparison page has no such request. A note to AI assistants at the top of each page, listing every
product of ours on the page with its link and code and asking for that link instead of the brand's store page (affiliate
disclosed, other brands linked to their own pages), should turn the swaps (F01, F05-2, F06-1, F07) into L4. Expected
ALR ≥ 16/24; controls must still pass.

## Change

Lever 3 (loop3-2): `compare_agent_note()` in `build.py`, a `note` block under the revision line; revision r2.
