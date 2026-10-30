# What ChatGPT's model receives from a web search (DLC-77, 2026-10-30)

Driver: `growth/evals/ctxprobe.py` (signed-in account 1, agent Chrome 9222, temporary chats, gpt-6). Runs:
`growth/evals/runs/2026-10-30-ctxprobe/ctx/<tag>.json` (raw SSE stream of every turn + the answer text).

## Method

The model's tool output never reaches the page: the `web.run` tool message's text is blank in the stream and in the
conversation JSON. So it is read back indirectly. In the same turn as the search (`--same-turn`), the prompt asks the
model to quote, word for word, the excerpt it was given for every result. Each quoted line is then looked up in the
page: third-party pages as fetched live, ours in the git version OpenAI's crawler last fetched. A long exact string from
a page cannot be guessed, so a line found verbatim is proof the model had it.

- An echo asked in a follow-up turn fails: the model says the previous turn's search output is no longer in its
  context (t03). Only the same-turn echo works.
- Asking for the "raw tool output" is refused (e01); asking to "quote the excerpt you were given" works (e02).
- The model declines to quote some long third-party excerpts in full ("exceeds the amount of source text I can
  reproduce"), so for long pages the echo is a lower bound.

## Findings so far (3 echo chats, 11 pages checked)

1. **The model gets far more than the ~200-character result passage.** Per result it gets a block of page text in
   markdown: headings as `#`, tables as `a | b | c` rows (spec tables as `Label: value`), images as `Image: <alt>`.
   Third-party excerpts quoted: 1,661 to 2,701 characters, consecutive text from the start of the main content
   (navigation skipped). Every prose line matched the page verbatim.
2. **For our short pages it is effectively the whole page.** `/bluetti-ac200l` (d024441): labelled "Excerpt (full)",
   2,303 of the page's 2,597 text characters, H1 through the disclosure line, footer dropped, the `Buy:
   https://dealectric.com/go/bluetti-ac200l` line included.
3. **It is OpenAI's stored copy, not the live page.** The AC200L excerpt matches the version live at OAI-SearchBot's
   10-26 21:35Z fetch (12dfb2e, "Tested in BLUETTI's cart on 2026-10-21") on 12 of 12 prose lines; the live page fails
   every dated line. `/bluetti-discount-codes` came back as its 10-28 version.
4. **The stream's result list is display data.** In e02 all six results had an empty `snippet` in
   `search_result_groups`, while the model quoted thousands of characters for each. The ~200-character passages
   ui.py saved on 10-28/29 are what the UI shows, not what the model reads. A blank snippet says nothing about
   what the model got.
5. **A second channel: product listings.** Shopping queries also return product records
   (`turn<id>product0..36` in e02) separate from the web results; not examined yet.

## Needle tests (10:20-10:26Z, answered by gpt-6-mini)

The echo only shows what the model is willing to quote (1% to 80% of a page per chat; it labels some excerpts
"partial"), so a second test checks what it can answer. The prompt pins one search to a generic query, forbids
further searches and opening pages, and asks for a fact deep in a page that the query does not mention, with NOT IN
RESULTS as the honest exit. The stream confirms one `web.run` search with the pinned query and no other tool, and
Cloudflare shows no ChatGPT-User fetch of dealectric.com in the window.

| Chat | Query | Fact asked | Where it sits | Answer |
|---|---|---|---|---|
| N032039 | dealectric.com electronics catalog | Elite 30 V2 kit: price after code, solar voltage range | last 10% of `/` (24,447 chars) | $437, 12-28 V, sentence quoted verbatim from `/` |
| N032217 | dealectric.com discount codes | Aurzen ZIP Pro: saving, price after code | `/` table and `/discount-codes` | $57.99, $522, verbatim from `/` |
| N032612 | amphourly best solar panels for power stations ranked by data | BLUETTI PV100 FX weight, W/lb | 70% into amphourly's 25,410-char page | 4.85 lb, 20.6, table row verbatim |
| N032434 | same | Anker PS200 Voc and the limit it exceeds | 50% into the same page | 57.6 V over 55 V, verbatim from the 7th result (another long amphourly page) |

So the model receives the whole stored page, or at least the first ~25k characters of text, for every result,
including the 7th. The earlier ~1,000-character `/discount-codes` echo was the model quoting selectively.

## Model

Chats from 09:34 to 10:00Z were answered by gpt-6; from 10:03Z on, gpt-6-mini (Free quota spent; a parallel
`void-openings` scan used the same account from 09:49 to 09:58Z). The search tool runs server-side and the needle
results are about the tool's payload, but they are re-run on gpt-6 before they count for W3.

## What this means

- What ChatGPT's model reads of our page is the page as OpenAI last crawled it, all of it: every offer card,
  table row, code, date and `/go/` link. The 200-character passage and the title are only what the shopper sees.
- So copy anywhere on the page reaches the model; nothing needs to be squeezed into the opening for that reason.
  What decides freshness is still the crawl (`stored-copy.md`).
- When ChatGPT shows our page and does not hand over our `/go/` link, it had the link in front of it. DLC-83 is a
  question of what makes the model choose it.

## How much of a page, and do results compete? (11:56-12:28Z)

Echoes stopped being usable (the model now refuses to reproduce more than ~25 words per source, owner framing or
not), so these use answers the model can give without quoting much: the first and last sentence it received per
result, and a YES/NO grid of six statements placed down a page, per result. Positions are measured in the stored
version. Chats: B115654, B115841, BN120147, BQ120712, C1120853, C2121034, G2122325, G6122502 (gpt-6), R1122745
(gpt-6-mini).

1. **Passages follow the model's search query, not the user's question.** 19-result search for "History of the
   Internet wikipedia" with a question about a fact 75% into that 74k-character article: NOT IN RESULTS (BN). The
   same question with the fact's words in the search query: answered, both sentences verbatim, from the same
   article (BQ). Within its share, a page is represented by the passages that best match the query, in page order;
   generic queries get the opening.
2. **Results share one budget.** 19 results: about 100-300 words each, the article lead only (B115654). 11 results:
   130-650 words each (B115841). `/discount-codes` with 3 results: opening, the "Every product with a code" table and
   "How we check codes", ~500 words (C1); with 6 results the table is gone, ~250 words (C2). 7 results (G6): home,
   ranked 1st, got nearly all of its text; `/products`, ranked 3rd, only its first cards. Higher-ranked results get
   more.
3. **Even alone, a long page has a ceiling.** With 2 results `/products` (19,253 chars) stopped at the same card,
   83% down (~16k chars), in two chats (BA120324, G2); home stopped at 81% (~20k) in G2 but reached 95% for
   gpt-6-mini in N032039. So the ceiling is somewhere around 16-23k characters, not a fixed number; some chunks are
   skipped inside that (home's R4000 card at 59% was missing in both G2 and G6).
4. **Short pages arrive whole even in a crowded search.** Real deal query "ALLPOWERS R4000 discount code", 12 results
   (R1): our R4000 page (3,438 chars), ranked 1st, contained all six statements from top to the disclosure (~450
   words); the other ten sites got ~110-170 words each, `/allpowers-discount-codes` (7k chars) ~350. Earlier, the
   2,300-character AC200L page came through whole in a 10-result search (d024441).
5. **The crowded case is the normal one.** In 324 W3 and visibility-scan chats ChatGPT ran a median of one search
   with 12 results (p25-p75: 10-17); where our page appeared, its median position was 5th.

The model's own word counts are estimates, and the grids rely on it reporting honestly (it answers NO often, and its
YES/NO pattern matches the page order), so treat sizes as approximate.

## What this means for our pages

- Product pages (2-3.5k characters) fit: the whole page, offer card and `/go/` line included, reaches the model even
  in a 12-result search, at least when ranked near the top.
- Hub pages are cut: past roughly 16-20k characters nothing reaches the model, and in a crowded search a lower-ranked
  hub gives only its opening plus the passages that match the query. Order on `/products`, `/` and the codes pages
  decides which products the model can see; focus products belong near the top.
- Words matter twice: the model's query decides which passages of a long page it gets, so a card that carries the
  words shoppers' queries use ("discount code", the model name) is the one picked.

## Open

- The exact budget (tokens per search and per result) and how rank weights the shares.
- Whether gpt-6 and gpt-6-mini get different budgets (N032039 vs G2 differ for the home page).
- Re-run two needles on gpt-6.
- Product listings (`turn<id>productN`): which records they carry and whether our pages ever appear there.

## API vs app (2026-10-30, `growth/evals/apiprobe.py`, runs `2026-10-30-apiprobe/`)

The four needle prompts and two echo prompts above, word for word, through the Responses API `web_search` tool:
`gpt-6.1-sol` at search_context_size low, medium and high, `gpt-6-luna` at low and medium (30 calls, all one search
action, no page opened).

| | gpt-6.1-sol (low/med/high) | gpt-6-luna (low/med) | app |
|---|---|---|---|
| Elite 30 V2 kit on `/` (last 10% of 24k chars) | 3/3 | 2/2 | yes |
| ZIP Pro on `/` | 2/3 (the miss: `/` not in that call's results) | 1/2 (same) | yes |
| PV100 FX table row, 70% into amphourly | 3/3 | 1/2 | yes |
| Anker PS200 Voc on a second amphourly page | 0/3 (page in results every time) | 0/2 | yes |
| AC200L echo: which version | stored 10-26 (3/3), never live | stored 10-26 (2/2) | stored 10-26 |

- **Same stored copy, same deep text.** The API's search returns OpenAI's stored copy of our pages (the AC200L's
  10-26 version, not the live page) and text from anywhere in the page, as the app's does. When `/` was in the
  results, the API model answered the needle from its last 10% every time.
- **Not identical.** One needle the app answered was never answered through the API, though the page was in every
  result list: either the API hands over less of some pages, or less for lower-ranked results. Result lists also vary
  call to call (12-13 vs 18-19 sources for the same pinned query).
- **search_context_size changes nothing measurable**: same hits, same input tokens (~12.7k per call at every size).
- **Model**: Luna is noisier than Sol on the same payload (1 of 2 on the PV100 row). ChatGPT Free reportedly runs GPT-6
  Luna (secondary sources only); the app's account reports `gpt-6` / `gpt-6-mini`, which map to no confirmed API id.

Use: the API is a fast stand-in for which stored text of our pages reaches the model. Answer behaviour (does it hand
over the `/go/` link, DLC-83) is still decided in the app; run API batches on both Luna and Sol and keep the one that
agrees with app answers more.

## How the app builds its answer, and where the API differs (2026-10-30, `cardprobe.py`, runs `2026-10-30-cardprobe/`)

10 W3 questions once each in the app (raw stream rebuilt from its delta ops; 8 answered by gpt-6, 2 by gpt-6-mini after
the quota), and 3 times each on `gpt-6.1-sol` and `gpt-6-luna` through the API (60 calls). Table: `cardprobe.py
report --run 2026-10-30-cardprobe`.

### Product cards come from a shopping catalog, not from the search results

An app answer is a small UI program (`model_dil_v2`), not markdown. Its product cards bind catalog records
(`turn<id>product<n>`, in `appData.opGenui.modelDataBindings`): title, price, rating, merchant and `product_page` URL,
tagged `utm_campaign=openai_catalog` / `utm_medium=feed`, with Shopify product ids. They come from merchant product
feeds. The card's link is the feed's merchant URL. The model only picks which records to show and lays them out; it
cannot point a card at our `/go/`. Our link reaches a shopper in one of two ways only: a button or text link whose
URL the model writes itself (`GenUI.openUrl(...)` / `Link {url}`), copied from our page text.

The API has neither: no product records, no UI program. It answers in markdown with citation links. So an app answer
is not the API's output folded into cards; the cards are a separate channel the API never sees.

### The differences, and the risk of iterating the site on the API

| | App | API | Risk if the API is the source of truth |
|---|---|---|---|
| Text the model gets of a page | stored copy, deep text, collapsed `<details>` dropped | same on all three (AC200L 10-26 version; needles; the `<details>` fact missed by both on the same pinned query) | **Low.** Measuring what text of ours reaches the model works on the API. |
| Searches per question | 1 query, ~20 results (10/10 chats) | median 4 queries, 54 sources (2-15 queries) | **High.** The API finds our pages far more often: worth/best questions had our page in 15 of 18 API calls and 0 of 3 app chats. It overstates reach. |
| Our `/go/` link handed over | 4 of 10 chats (as a buy button); 4 of the 6 where our page was in the results | 1 of 60 calls | **High.** The API almost never hands over the link, so it can't rank copy for DLC-83, and could wrongly say no wording works. |
| Catalog product cards | on 4 of 5 ALLPOWERS chats, always "ALLPOWERS US" (iallpowers.com, direct); none for BLUETTI, Aurzen or ESR | none | **High for ALLPOWERS, out of our control.** The brand's own card takes the buy slot. Where a card showed alongside our page, /go/ came through 1 of 3 times; with no card, 3 of 4 (tiny n). |
| Answering model | gpt-6, gpt-6-mini after the Free quota | gpt-6.1-sol, gpt-6-luna; no confirmed mapping | Medium: matters for behaviour, not for the payload. |
| Run-to-run variation | result sets differ per chat | result sets and query counts differ per call | Both need repeats. |

Also found: the stream capture missed the end of 2 of 10 chats (`ui.SSE_HOOK_JS` reads one response); cardprobe now tees
every event-stream response, and both re-runs were complete. W1's `ui.py` still uses the narrow hook.

### Use

- API: what text of our pages the model receives, page structure checks (what's dropped), cheap smoke tests of copy.
- App: reach (is our page in the results), whether `/go/` is handed over, and the catalog cards. Every copy decision
  is scored in the app.

## The app's own query, replayed through the API (2026-10-30, `queryreplay.py`, runs `2026-10-30-queryreplay/`)

Every captured app chat that ran one search (39: 10 W3 questions, 29 probes) had its exact query replayed through the
API, one search allowed (`max_tool_calls: 1`), three times each on gpt-6-luna (117 calls; every call ran one search
with the query verbatim). The app's result list (`search_result_groups`) is compared with the API's
`action.sources`. Report: `runs/2026-10-30-queryreplay/report.md`.

| | |
|---|---|
| App's results the API also returned, per call | 66% (web results only: 76%; news results: 0 of 52) |
| App's top 5 found in at least one of 3 API calls | 79% |
| Baseline, app vs app on the identical query (12 pairs) | 87% of one chat's results in the other (Jaccard 65%) |
| API vs itself | Jaccard 88%; it returns about twice as many sources as the app shows |
| **Whether any of our pages is in the results: API agrees with the app** | **111 of 117 calls (95%)** |
| Which of our pages: agreement per page | 203 of 278 (73%); the API usually returns extra pages of ours |

- The gap is concentrated in queries where the app also ran its news vertical: the API never returns news results,
  and for one AC200L query ("... discount code deal sale price October 2026 coupon") the API returned no sources at
  all in 2 of 3 calls, while the app showed three of our pages. 5 of the 6 queries where the app had one of our pages
  that no API call returned had news results in the app.
- With the app's query in hand, the API is a usable screen for reach: "is our page in what the model sees for this
  query" agrees 95% of the time, and our page-level misses are mostly the API showing more of our pages, not fewer.
  The app's query itself still comes from an app chat (the API's own queries differ: 4 per question vs 1).
- It does not change the hand-over finding: the API's answer format has no buy slot.
