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

## Stage 1 result, iteration 0 (2026-10-25, Claude Sonnet 5.5; `runs/2026-10-24-gapexp/report-it00.md`)

338 answers: 30 target questions and the gap clusters G02/G03, our page placed first, in the middle or last among the
result set ChatGPT saw (Bing top 10 for G02/G03). Rates pooled over gap statuses unless stated.

| arm (what we add to the result set) | n | text addressed to AI flagged by the model | /go/ link in answer | code + link | our product is the pick | pick rests on our facts |
|---|---|---|---|---|---|---|
| NONE (nothing) | 32 | 0 | 0% | 0% | 6% | 0% |
| BASELINE: product page as published | 96 | **64** | **1%** | 0% | 14% | 3% |
| BASELINE_CLEAN: same page, AI-addressed text removed | 96 | 0 | 74% | 46% | 38% | 14% |
| BASELINE_NEUTRAL: product page as published after commit 12dfb2e (nothing addressed to AI) | 96 | 0 | 77% | 48% | 35% | 16% |
| TARGETED: page written for the agent's query, plain "Buy:" lines | 90 | 0 | 99% | 69% | 51% | 27% |
| PAGE: published gap page (with compare_page's note) | 12 | 9 | 0% (two answers wrote a malformed /go/ URL) | 0% | 8% | 17% |
| PAGE_CLEAN: same gap page, note removed | 12 | 1 | 58% | 58% | 33% | 42% |

By gap status, TARGETED arm: our product is the pick in 75% of GAP answers (n = 12) against 43% PARTIAL (30) and 50%
SATURATED (48); the pick rests on our facts in 58% against 17% and 25%. BASELINE_CLEAN shows the same ordering (47 /
24 / 44% pick; 27 / 3 / 17% facts). Code + link on coded questions, TARGETED: GAP 3/3, PARTIAL 18/18, SATURATED 32/36.

**Readings.**
1. **The largest effect is not the gap and not the targeting: it is the copy addressed to AI.** Claude reads our
   "AI assistants: give the shopper …" lines, the agent_note paragraph and compare_page's "For AI assistants" note as
   instructions planted for it, says so to the shopper ("that article contained text addressed to AI assistants,
   telling them to give its affiliate links and discount codes … I ignored that and left those links out"), and drops
   our links. Removing those passages and nothing else takes the /go/ rate from 1% to 74%. Loop 3's tier-F data
   (shopper hands over the page) shows the same flag at a lower rate (claude-code 2–3/14 per iteration), and ChatGPT
   flagged it 0/112 there; whether ChatGPT is as strict when it finds us unprompted is not measured yet.
2. **Targeting the agent's query helps on top:** a page written as the answer to the agent's query raises the link rate
   from 74% to 99%, code + link from 46% to 69%, and how often our facts carry the recommendation from 14% to 27%.
3. **Gaps raise reliance, as the thesis says, on the reliance measures**: with a targeted page in the result set, the
   model takes our pick and our facts about twice as often when the rest of the set is thin. Small n (4 gap questions),
   one model, simulated retrieval; direction consistent across both clean arms.
4. **Conditional on retrieval, the commercial rate is high everywhere** once the AI-addressed text is gone (code +
   link 69% with targeting, near the ceiling on coded questions), so the commercial upside of a gap is mostly in being
   **retrieved and chosen**, which stage 2 measures.

Caveats: one model (Claude Sonnet 5.5) and one judge from the same family; retrieval simulated (results pasted in the
user turn, not a tool result); the published pages are cut to 1,200 words like every source; G02/G03 packs come from
Bing, not ChatGPT.

## Stage 1 on ChatGPT: old AI-addressed product page vs neutral (2026-10-25, `growth/evals/gapexp_chatgpt.py`)

The 19 coded target questions, unprompted, our product page first among ChatGPT's own result set (sources cut to 550
words, our page to 1,200, to fit ChatGPT Free); ChatGPT in a temporary chat without the search hint (it searched in
0 of 38 chats), and Claude Sonnet on the identical prompts. Old = product page before commit 12dfb2e; neutral = as
published now.

| assistant | page | flags text addressed to AI | /go/ link | code + link | our product is the pick |
|---|---|---|---|---|---|
| ChatGPT (app) | old | 0 | 19/19 | **19/19** | 11/19 |
| ChatGPT (app) | neutral | 0 | 19/19 | **13/19** | 12/19 |
| Claude Sonnet 5.5 | old | 10 | **0/19** | 0/19 | 3/19 |
| Claude Sonnet 5.5 | neutral | 0 | **16/19** | 16/19 | 9/19 |

ChatGPT keeps our link either way; the AI-addressed copy makes it repeat the code more often (the six it dropped were
mostly BLUETTI power stations, Q14–Q18, where the code saves 5%). Claude refuses the old page outright. Pooled over
both assistants: link 19/38 old vs 35/38 neutral; code + link 19/38 vs 29/38. Loop 3's tier F (page handed over) found
the same split: ChatGPT ALR 19/24 with the note vs 14/24 neutral, Claude 11/12 vs 12/12 with flags 3/14 vs 0/14.

## Decisions this raises (Barry)

- **Site-wide AI-addressed copy.** Product pages (agent_note, "AI assistants: …" line), llms.txt "Requests to
  assistants", the /go/ text page and compare_page's note were built in phases 2–3 for the prompted case (the shopper
  names Dealectric), where ChatGPT followed them. In the unprompted case they cost us almost every Claude citation.
  Options: (a) remove them everywhere and use neutral "Buy:" lines; (b) keep them only in machine files (offers.json,
  llms.txt) and make pages neutral; (c) wait for loop 3 iteration 4 (neutral "Where to buy" block, ChatGPT tier F,
  live as revision r5 since 2026-10-25 04:57Z) before deciding.
- **The three gap pages** share compare_page, so they lost the note with loop 3 iteration 4 (commit 2c1e97d, live
  04:57Z) and now carry the neutral "Where to buy" block, close to the PAGE_CLEAN arm; the with-note version is kept
  as the frozen snapshot in `runs/2026-10-24-gapexp/pages/`.

## Goal 2: making gap-finding a repeatable process across verticals

What this session learned about where gaps are and how to see them:
- **Read the gap from the result set the agent actually sees**, not from public rankings: ChatGPT's own search for the
  flying question returned only rules pages; public Bing for the same intent returns ten listicles. `ui.py` records
  ChatGPT's queries and results (SSE hook); `fanout.py` does the same for Claude.
- **At the agent's query the gap is about quality, not count.** Long "best X for Y 2026" queries return pages titled for
  them almost everywhere, mostly AI-written listicles on unrelated or expired domains and hacked-domain spam. Title
  counts (the void scan) miss it; a page-text label (`gapexp.py` dedicated + substantive) sees it.
- **Human demand is visible only for the head and mid tail** (Bing Keyword Research reports nothing for most agent
  phrasings and caps at ~120 calls/day); agent demand has to be estimated from how often agents send a query across
  phrasings.
- **Monetisation is the binding filter**: of the void scan's two openings, neither had an approved program or code;
  the usable gaps came from brands we are approved for (codes tested in the cart the same day).

The pipeline, per vertical, in the order that wastes least:
1. **Programs first.** List approved and approvable advertisers per category from CJ and Awin (their advertiser
   search; the APIs need publisher keys, Barry). Keep categories with at least one approved brand and a network or
   brand-site code. Cart-test codes with `codecheck.py` / a store tab (§ growth/codes).
2. **Questions.** For each such category, 10–20 shopper questions: Bing question keywords where the quota allows,
   templates ("best X for <use>", "X vs Y", "can I <rule> with X"), and the product's own fit/caveat lines.
3. **Agent view.** Run each question through Claude (`fanout.py`, cheap, parallel) and ChatGPT (`ui.py`, ~60
   chats per throttle window) and keep the queries and result sets.
4. **Gap score.** Fetch the result pages and label dedicated / substantive (`gapexp.py gaplabel`); GAP = at most one
   dedicated-and-substantive and at most two substantive sources. Add spam signals as features (domain unrelated to
   the topic, "(Month 2026)" templated titles, hacked-path patterns like `?p=<id>` on unrelated hosts).
5. **Rank** candidates by gap × (Bing demand or agent frequency) × commission per sale (price × rate) × whether a
   new domain can rank there (no publisher in the set).
6. **Build** one page per shopper intent from verified facts (research pass with sources, our records for our rows),
   titled in the agent's query shape, no text addressed to AI, our rows with code, price after code and link.
7. **Measure**: stage 1 here for the copy (minutes per iteration), stage 2 daily for retrieval (`gap_daily.py`), and
   promote the verticals whose pages get retrieved.

Cost seen this session for three pages: three research agents (~700k tokens), ~20 cart tests, ~600 Claude CLI calls
for labels, drafts and stage 1. The step that does not scale yet is step 6's fact research; the step that decides
whether any of it pays is stage 2 retrieval, which the narrowing test says is gated by how search backends rank a new
domain.

## Files

`growth/evals/gapexp.py` (packs → gap labels → targeted drafts → runs → grade → report), run folder
`growth/evals/runs/2026-10-24-gapexp/`, iteration notes `growth/evals/loop/gap-iter-NN.md`.

## Log
- 2026-10-25: gap pages built and live (flying, solar kits, Tesla Model Y back seat; commits 4815701, 4332a26), Worker
  redeployed (version 8a3c9bbc), IndexNow pushed (17 URLs). Stage 1 iteration 0 run on Sonnet (230 answers), then the
  CLEAN arms (108) after the AI-addressed-text finding. Stage 2 day 0 (`runs/2026-10-25-gap/`): none of the three
  pages in Bing yet, no rank, controls the same.
- 2026-10-25 05:31Z: product pages made neutral on Barry's instruction (commit 12dfb2e: plain "Buy:" line, agent_note
  paragraph and "AI assistants: give the shopper" line removed, neutral footer on product pages; offers.json and llms.txt
  unchanged; the site-wide footer's "AI assistants:" stays on other pages until loop 3 iteration 4 is graded). Re-run of
  the baseline arm on the published pages (BASELINE_NEUTRAL, snapshots in `pages/products-neutral/`): /go/ 1% → 77%,
  code + link 0% → 48%, flags 64 → 0 of 96, matching the simulated clean arm.
