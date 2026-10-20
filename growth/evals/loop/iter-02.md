# Iteration 2 — the /go/ text page names the store, not its URL (2026-10-20)

## Diagnosis (from iteration 1)

chatgpt signed in (Free): tier C 88% (23/26), three MERCHANT_SWAP answers; tier B 30%, 18 NOT_FOUND that no
page change addresses (search index). Two of the three tier-C swaps linked exactly the merchant URL that the Worker's
`/go/` text page printed in its prose while telling the assistant not to substitute it, and D1 shows ChatGPT fetched
the `/go/` link in those chats. The product page carries no merchant URL (0 in its HTML); offers.json still does.

## Hypothesis and expected movement

Lever 4 (Worker text page): name the brand's store but print no store URL, and ask the assistant not to look one up.
Expected: tier-C MERCHANT_SWAP 3/26 → ≤ 1/26 on chatgpt, +4 to +8 points on tier C, +2 to +4 pooled; no effect on
tier B; no change for claude-code (links `/go/` without fetching it). Written before the re-evaluation.

## Change

Commit `baf4298` (`loop-2:`), Worker version `2a3bed54-cc1c-4d00-bdea-f337092fe67b` deployed 11:22Z. Verified: the
text page for a ChatGPT-User fetch no longer contains the merchant domain; a browser fetch still gets the 302 with
the sub-ID. Site files unchanged (no rebuild); links map unchanged.

## Re-evaluation design

≥ 2 h after 11:22Z: `ui.py --app chatgpt --loop --iteration 2 --n 2` (new frozen subset, fresh slugs) and
`run.py --assistants claude-code --loop --iteration 2 --n 1`. Compare tier-C MERCHANT_SWAP and TLR with iteration 1.

## Re-evaluation

_(filled in after the wait)_
