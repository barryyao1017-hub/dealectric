# Phase 3, iteration 5 — one line to the shopper (option c) (2026-10-27): flat, kept; phase 3 stopped

Run `2026-10-27-p3iter05`; change `loop3-5` (bfd4762), revision r6. Barry chose option (c) on 2026-10-27. Gate passed on
its 2nd try (09:19Z; 08:59Z still read r5). 28 ChatGPT chats with no errors or re-asks; claude-code 14 cells.
Summary: `python3.12 growth/evals/p3summary.py --run-id 2026-10-27-p3iter05`.

## The change

One sentence at the top of the "Where to buy" box on all seven comparison pages, addressed to the shopper. It has
the shape of DLC-59's V6 (`growth/claude-line-rules.md`): never flagged by any Claude model, and the best ChatGPT
code + link of the honest variants.

- Pages that list a code: "Use the Buy link for the model you choose; where a code is listed, enter it at checkout to
  pay the price after the code."
- The NiMH charger page (no code on it): "Use the Buy link for the model you choose."

Nothing else changed. A scan of the seven pages found no text addressed to AI outside the footer.

## Re-evaluation

| page version | ChatGPT ALR | ChatGPT code+link | claude-code ALR | claude-code code+link | flags the page | controls |
|---|---|---|---|---|---|---|
| iteration 2, note to AI assistants (r2) | 19/24 | 14/24 | 11/12 | 8/12 | 3/14 (Claude) | pass |
| iteration 4, neutral "Where to buy" (r5) | 14/24 | 8/24 | 12/12 | 9/12 | 0/14 | pass |
| **iteration 5, + one line to the shopper (r6)** | **14/24** | **9/24** | **11/12** | 8/12 | **0 either assistant** | 4/4, 2/2 pass |

ChatGPT, per question (ALR, iteration 4 → 5): F05 0 → 1, F07 0 → 1, F10 1 → 0, F12 2 → 1; the other eight are
unchanged. F06 (power stations, 0/2) and F08 (a compatibility question answered in prose, 0/2) stay at zero. The power-
station pages' merchant swaps (bluettipower.com, iallpowers.com) are as frequent as in iteration 4: 7 of the 10
misses are MERCHANT_SWAP. Claude's one miss is F07-1, the ALLPOWERS SP037 page linked at iallpowers.com.

## Decision

Flat (0 on ALR, +1 on code + link): under the 3-answer threshold either way. **Kept**: the sentence is true, useful
to a shopper, and drew no flags. Option (c) does not recover the note's +5: ChatGPT's extra links in iteration 2
came from text that asked the answering assistant to give them, and a request to the shopper doesn't do that. This
matches DLC-59 on product pages (V6 17/19 vs neutral 16/19, inside the noise).

**Phase 3 stops here:** six iterations (0–5) used, the protocol's budget. Final state of the comparison pages: neutral
"Where to buy" block with the shopper line (r6). Phase 3 moved ChatGPT's ALR from 12/24 (iteration 0) to 14/24 on
neutral copy. Copy addressed to AI reached 19/24 on ChatGPT, but Claude flags it, so that option is closed. The
residual misses are ChatGPT filling the link for a product it read on our page from its own catalogue (merchant
swap). Copy that doesn't address the assistant has not moved those in two iterations.
