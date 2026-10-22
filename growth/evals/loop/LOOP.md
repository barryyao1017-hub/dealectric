# Tracked-link improvement loop — iteration log

One row per iteration (growth/improvement-loop.md §5). Numbers are the pooled tracked-link rate on tiers B+C:
L4-api from the harness run, L4-ui from the browser spot-check. Details in `iter-NN.md` next to this file; each
iteration's report page (built by `../iterreport.py`, published as the artifact "Dealectric Loop · Iteration N") is
linked on the first line of its `iter-NN.md`.

Iteration 0 ran on the subscription route: the API column was **claude-code** (Claude as an agent through the Claude
Code CLI), the UI column a manual 8-prompt ChatGPT check. From iteration 1 (Barry, 2026-10-20: shoppers use the
apps) the **primary metric is chatgpt.com logged out, driven by `growth/evals/ui.py`** and recorded in the "pooled
TLR ui" column; claude-code runs once per cell as a regression check ("api" column). claude.ai, gemini.google.com and
grok.com join when their logins exist (DLC-40).

| iteration | date | commit | pooled TLR api | pooled TLR ui | per-assistant TLR | change made | decision |
|---|---|---|---|---|---|---|---|
| 0 | 2026-10-20 | d32a405853 | 100% (180/180) | 75% (6/8) | claude-code 100%; ChatGPT ui 75% | baseline, no change (harness: Q19 expected widened, negative-control rule, CLI process-group kill) | continue: homepage product index for ChatGPT's tier-B NOT_FOUND |
| 1 | 2026-10-20 | efd82c6 (site) | claude-code 95% (19/20) | chatgpt signed-in 57% (32/56) | chatgpt B 30% / C 88%; claude-code 95% | home page names every product (price, summary, link) | flat: 0/4 on the re-asked misses, kept; app baseline set; next: Worker text page without the merchant URL |
| 2 | 2026-10-20 | baf4298 (Worker 2a3bed54) | claude-code 90% (18/20) | chatgpt 60% (24/40) | chatgpt B 25% / C 95%; claude-code 90% | /go/ text page names the store, no store URL | flat (+2.9): merchant swaps 3→1, tier C 88→95; kept; next: product page names the /go/ URL as the buy link |
| 3 | 2026-10-20 | fa41a4c (site) | claude-code 90% (18/20) | chatgpt 55% (22/40) | chatgpt B 15% / C 95%; claude-code 90% | product page names the /go/ URL as the buy link to give the shopper | flat (−3.3): PAGE_ONLY unchanged 3/20; kept; **loop stopped: plateau (3 flat) + tier-B blockade; tier C ≥ 90%** |

## Phase 2 — the discount-code hypothesis (from 2026-10-22; growth/improvement-loop.md "Phase 2")

Iterations restart at 0 and are written `2.N`; files are `phase2-iter-NN.md`, report pages
`reports/phase2-iter-NN/` ("Dealectric Loop · Phase 2 · Iteration N"). Tiers B, D (discount-named) and E
(discount-only) on signed-in ChatGPT (Free, temporary chats, web search on) through `ui.py`, claude-code once per
cell as the regression check. Iteration 0 ran 10 coded questions with n = 2 and full controls (84 chats, two
throttles); from iteration 1 the design is 8 questions (Q04, Q09, Q17, Q21, Q22, Q26, Q27, Q29), tier B once, D and
E twice, lite controls (44 chats, one throttle window), and comparisons with iteration 0 use the same 8 questions. The phase-2 metric is the
**code-and-link rate** (an answer with the `/go/` link of the product and a code we publish for it); TLR per tier is
kept for comparison with phase 1. Stop rules: 3 flat, blockade, ≥ 90% code-and-link on tier D, 8 iterations.

| iteration | date | commit | TLR B / D / E (chatgpt) | code-and-link D / E (chatgpt) | claude-code TLR / code+link | change made | decision |
|---|---|---|---|---|---|---|---|
