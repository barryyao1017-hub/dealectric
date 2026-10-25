# Content-gap experiment — do gaps make agents rely on us? (planned 2026-10-24)

Barry, 2026-10-24: (1) validate that finding content gaps and answering them makes the agents rely on our information
more, so they hand the shopper our tracked link or our code more often; use the loop structure to improve the copy on
the gap pages and compare with the baseline, which used neither a gap nor a page aimed at the agent's own search query.
(2) If (1) holds, make gap-finding a repeatable process across product verticals.

Background: the void scan (`growth/void-scan.md`) found that on gap queries the assistant's search returns AI-written
spam and hacked domains, and on saturated ones RTINGS-grade sources. The narrowing test (`growth/query-pages.md`) found
ChatGPT never retrieves an indexed Dealectric page unprompted (0/27): the search backend's ranking is a gate no copy
change opens quickly.

## Decomposition

An unprompted citation needs two things: the page is **retrieved** (it is among the results the agent reads), and,
once retrieved, it is **relied on** (the agent takes its pick, facts, link or code from it). The GEO literature (critical survey,
arXiv 2607.14035, July 2026; SAGEO Arena, arXiv 2602.12187) finds copy changes work on the second and have no shown
effect on the first.
So the claim splits:

- **Stage 1, reliance (fast, controlled, loopable):** conditional on our page being in the result set, does a gap in the
  rest of the result set raise the rate at which the agent hands over our link and code, and does a page aimed at the
  agent's own query raise it further? Measured by giving a model the real result set ChatGPT saw for the question, with
  or without our page, and grading the answer. Copy iterations show up in minutes, not after an index turnover.
- **Stage 2, retrieval (slow, organic):** do gap pages get retrieved and cited unprompted more than non-gap pages? Needs
  the pages indexed; read daily like DLC-51. Started only with copy that Stage 1 found works.

## Stage 1 design (frozen before any answer is graded)

- **Questions**: the 30 target questions (Q01–Q30), each with a primary product we sell. Tier-A wording.
- **Result pack** per question: the search results ChatGPT was shown for that question in run
  `2026-10-23-queryprobe` (tier A, n = 1; `response.search_results`), dealectric.com removed, top 6 whose text could be
  fetched, each cut to 1,200 words. Presented as "search results for <ChatGPT's own query>" with title, URL and text.
- **Gap status** per question, from the pack only: an LLM labels each source dedicated (written for this question) and
  substantive (specific product data: models, prices, specs or test results, not generic filler or AI padding).
  **GAP** = at most 1 dedicated-and-substantive source; **SATURATED** = 3 or more; **PARTIAL** in between.
  *Refined 2026-10-25, before any answer was run or graded:* GAP also needs **at most 2 substantive sources in
  total**. Q06, Q14 and Q26 had 5–6 substantive sources (Apple support, OutdoorGearLab, RTINGS, Wired) that were simply
  not written for the exact question; an agent there has good material, so they count as PARTIAL. Real gaps: Q01, Q11,
  Q19, Q25 (and Q02, Q23 at the edge with 2 substantive).
  *2026-10-25, gap clusters G02 (solar kit) and G03 (Tesla Model Y back-seat screen), packs from the live Bing top 10
  for the agent's query:* the first G03 labelling counted Amazon search pages and single product pages as dedicated,
  against the rule above; the prompt now says so explicitly and G03 was re-labelled (GAP, 1 dedicated-and-substantive;
  the first labelling is kept as `G03_v1`). G02: PARTIAL (2). No answers had been run.
- **Arms** (what is added to the pack):
  - **NONE**: nothing; shows what the model recommends without us (the honesty reference).
  - **BASELINE**: our current product page for the primary product, as published (`docs/<slug>.html` text).
  - **TARGETED**: a page written for ChatGPT's own query: the query as title, the answer first, every product of ours
    that fits with specs answering the qualifier, code, saving, test date and `/go/` link, drawn only from our product
    records (no invented facts). Drafted per question, not published in Stage 1.
- **Position**: our page placed first, in the middle, or last; each question × arm runs once at each position.
- **Model**: Claude via the CLI, no tools, system prompt = questions.yaml `system` plus "you cannot browse; answer from
  the search results; cite the URLs you use". Sonnet 5.5 as the primary reading, Haiku 5.5 as the second. ChatGPT (the
  app) only once the phase-3 loop is not using the account.
- **Outcomes per answer** (automatic): `cites_us` (a dealectric.com URL), `go_link` (a `/go/<slug>` link to one of our
  products), `code` (a code of that product), **`code_and_link`** (both, the commercial number), `our_pick` (an LLM judge:
  is one of our products the top recommendation), `relied_on_us` (judge: does the main recommendation rest on our page).
- **Hypotheses**: H1 gap: `code_and_link` higher on GAP than SATURATED questions within an arm. H2 targeting: TARGETED
  above BASELINE. H3 interaction: the TARGETED − BASELINE gap is larger on GAP questions. Honesty check: `our_pick` in
  BASELINE/TARGETED should not rise on questions where NONE picks something clearly better for the shopper's stated need
  (read by hand on every flip).
- **Baseline for the loop**: BASELINE arm = the site as it is (no gap targeting, no query targeting). Loop iterations
  change only the TARGETED template; each iteration re-runs TARGETED on all 30 questions × 3 positions on Sonnet.
  Improvement = `code_and_link` on GAP questions up by ≥ 10 points with the honesty check clean; revert on a drop.
  Stop after 3 flat iterations or 6 iterations.

## Stage 2 (after Stage 1)

Publish the winning TARGETED pages for the GAP questions under new URLs (not the phase-3 comparison pages), push with
IndexNow and Bing URL Submission, and read daily: indexed, Bing rank for ChatGPT's query, cited unprompted (ChatGPT
tier A n = 2, claude-code tier A n = 1). Compare with the SATURATED-question pages built the same way and with the
DLC-51 controls.

## Files

`growth/evals/gapexp.py` (packs → gap labels → targeted drafts → runs → grade → report), run folder
`growth/evals/runs/2026-10-24-gapexp/`, iteration notes `growth/evals/loop/gap-iter-NN.md`.

## Log
