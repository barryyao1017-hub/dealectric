# Query-targeted comparison pages (DLC-51) — plan, 2026-10-23

Idea (Barry, 2026-10-23): the next obstacle after phase 2 is being found at all. Unprompted, no assistant has ever
cited us (0/90 in phase 1, 0/30 ChatGPT tier A on 2026-10-23). Instead of waiting for the broad shopper question
("best portable power station for camping") to rank us against Wirecutter and RTINGS, aim at the **queries the
agents themselves type into their search backend**: the follow-up searches are narrow, spec-heavy and often
"X vs Y vs Z", and few pages answer them. A page whose title and first heading match such a query nearly word for
word, with a horizontal comparison across many products (ours and the brands we do not sell), should surface higher
in a thin result set, and from there be cited and carry the shopper to a `/go/` link.

## Hypothesis and metric

**H:** for a query the agents issue and that today returns few pages that answer it directly, a comparison page whose
title matches the query gets (a) indexed by Bing and Brave, (b) into the engine's top 10 for that query, and (c) cited
in an unprompted assistant answer to the shopper question behind it — while matched control queries with no new page
stay at 0.

Readings, per query cluster, daily:
1. **indexed**: `site:dealectric.com <page>` on Bing and Brave; GSC/Bing Webmaster coverage.
2. **rank**: `growth/evals/serp.py` position of the page for the target query on Bing and Brave (`dealectric_rank`).
3. **cited unprompted**: ChatGPT (app, tier A) and Claude as an agent (tier A) on the shopper question of the cluster,
   n = 2; grade with `grade.py` as before (L4 = `/go/` link in the answer; also record "page cited" = any
   dealectric.com URL in citations or `response.search_results`).
Success: at least one built cluster reaches (c) while all controls stay at 0 after the index has had a week. (b)
without (c) is the fallback finding (ranked but not chosen); (a) without (b) means the result set was not thin.

## Data

- **ChatGPT's own search queries**: since 2026-10-23 `ui.py` records them (`queries`) with the result list ChatGPT was
  shown (`response.search_results`), read from the SSE answer stream (`SSE_HOOK_JS`, metadata type
  `search_model_queries` / `search_result_group`). The conversation JSON fetched afterwards has them stripped. Run:
  `2026-10-23-queryprobe` (30 target questions, tier A, n = 1).
- **Claude's search queries**: `run.py` has recorded them from the start (`queries`); 144 distinct on tier A across the
  phase 1–2 runs, 68 after dropping buy/retailer/brand-site queries (`serp-claude.json`).
- **Result-set thinness**: `serp.py` fetches the Bing and Brave top results for a query through the agent's Chrome.
  Thinness is judged on the titles: how many of the top 10 are pages written to answer this query (a "best X with Y
  (2026)" or "A vs B" page) versus pages that merely mention it (manuals, store collections, forum threads, broad
  "best power stations" lists). ChatGPT's `search_results` give the same view from inside the app.

## Steps

1. Capture queries (done 2026-10-23: `ui.py` SSE hook; 30-question unprompted run).
2. Score: `serp.py --from-run 2026-10-23-queryprobe` and `--queries-file` of Claude's queries; cluster the queries by
   shopper question; pick about 4 clusters we have products for whose result sets are thin, and about 4 as controls
   (similar thinness, no page). Table below.
3. Build: one page per cluster under `src/` (generator, not hand-written HTML in `docs/`): URL slug and `<title>`/`<h1>`
   = the query in plain words; comparison table across every product the agents named in their searches (EcoFlow,
   Anker SOLIX, Jackery, Belkin, … included, with spec and list price, no link or an unaffiliated manufacturer link);
   our rows carry the code, the saving, the cart-test date and the `/go/` link in the canonical phase-2 paragraph;
   `rel="sponsored nofollow"`, disclosure, no JS. Add to sitemap, llms.txt, offers.json `pages`; push with
   `tools/indexnow.py`; request indexing in GSC.
4. Measure daily for a week (readings 1–3), controls alongside. Stop early if the pages are indexed and ranked top 10
   but never cited after n = 2 × 3 days (finding: ranking is not the gate), or never indexed after 7 days (finding:
   the index, not the page, is the gate).

## Clusters (step 2)

_To be filled from `serp-claude.json` and the queryprobe run._

| cluster | shopper question (Qnn) | agent query (verbatim) | engine | top-10 pages answering it | our products | build / control |
|---|---|---|---|---|---|---|

## Log

- 2026-10-23: SSE hook in `ui.py` (queries + result list per chat); `serp.py`; unprompted 30-question ChatGPT run and
  Bing/Brave scoring of 68 Claude queries started.
