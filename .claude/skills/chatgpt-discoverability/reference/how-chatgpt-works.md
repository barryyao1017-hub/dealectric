# How ChatGPT works behind the scenes: findings and evidence

Each claim has a tag, the evidence and the date it was last checked. Tags: **[measured]** repeated observation with
numbers; **[observed]** one or two observations; **[hypothesis]** not tested. Source files are under `growth/focus/`
unless a path says otherwise. The app is the Free plan, signed in, temporary chats, agent Chrome (port 9222, profile
1), US.

## 1. Crawl and stored copy (`stored-copy.md`, `dlc77-learnings.md`, `crawls/fetches.jsonl`)

- **ChatGPT answers from OpenAI's stored copy of a page, refreshed by OAI-SearchBot fetches.** [measured, 10-30]
  291 of 292 chats that showed an outdated version matched OpenAI's last fetch; Bingbot 1 of 117. Nothing we ship
  changes ChatGPT's answers until that crawl.
- **Known pages lag by days.** [measured, 10-30] The focus pages were last fetched 10-26 21:3xZ, with none since as
  of 10-30 19:54Z. Copies were seen 1 to 6.5 days behind live on 10-28. Home and `/portable-power-stations` are
  re-fetched every few hours. One sitemap read (10-22) came before a full sweep (10-26).
- **New URLs get fetched fast.** [observed, 2] TN438 in 13 h; the Marshall pages the next night. The solar gap page's
  first fetch was 10-29 07:12Z, four days after launch (it was linked later). A new URL linked from the home page is
  the fastest route in.
- **Sitemap `lastmod`** has been exact since 10-28. [effect unmeasured] No official OpenAI URL-submission route was
  found.
- **Part of OpenAI's crawl shows as unverified in Cloudflare** since 10-28. [observed, one sweep] `storedcopy.py`
  counts unverified rows within 10 minutes of a verified fetch. Scanners spoof the user agent; those rows have
  count 10, while real crawl rows have count 1.
- **There may be a second index feed.** [hypothesis, one observation] The four comparison pages appeared in results
  ~160 times from 10-24, but OAI-SearchBot first fetched them on 10-29. Only our ChatGPT-User probes had fetched them
  before. Possibly live fetches seed the index. Untested.
- **A live ChatGPT-User fetch is reused by later chats for a few minutes.** [observed: one page, 4 chats]

## 2. The query (`readings/gap-vs-focus.md`, `context-probe.md`, `growth/query-pages.md`)

- **The app usually runs one search per answer.** [measured: median 1, 324 W3 and visibility chats; 10 of 10 in the
  card probe] The API runs a median of 4 (2–15) for the same question.
- **Query shape:** the question plus "2026", "review(s)" and brand names. [measured, 10-23 and 10-30] Examples: "best
  1kWh LiFePO4 portable power station under $500 2026"; "portable power station solar panel kit for camping".
- **Wording varies between chats on the same question** [measured], which is why the camping phrasing missed our
  page once.
- **Vague questions may not search**; they get a clarifying question or an answer from memory. [observed, harvest
  10-30] `harvest.py` measures this per level (G0/G1/G2) and mode (natural vs forced search).

## 3. The results (`context-probe.md`, `growth/evals/runs/2026-10-30-queryreplay/report.md`)

- **About 12 web results** [measured: median 12, p25–p75 10–17], sometimes with a news group (~20 refs in all).
  Where our page appeared, its median position was 5th.
- **Results vary between app chats on the same query**: 87% of one chat's results appear in the other (Jaccard 65%,
  12 pairs). [measured] This is the ceiling on any prediction of the result set.
- **On gap queries a small site ranks.** [measured, small n] The solar gap page ranked first or second in all 5
  chats where it was retrieved. On "best X" queries, single product pages were not retrieved (0 of 8).
- **The API's one-search results resemble the app's.** [measured, 117 calls]
  - 66% of the app's results per call; web results 76%, news 0 of 52.
  - 91% of shared results sit in the API's top 12; median rank correlation 0.86.
  - "Any of our pages present" agrees 111 of 117.
  - The API returns about twice as many sources as the app shows; it never returns news.
  - One deal query returned no API sources in 2 of 3 calls.
  - About 30% of the difference is unexplained. [hypothesis] Location, the news vertical and index servers are
    suspects.

## 4. What the model receives (`context-probe.md`: needle tests, budget tests)

- **The stored page text, not the snippet.** [measured: 4 needle tests, facts 50–90% deep in pages, answered
  verbatim with no page open] The ~200-character snippet in the stream (`search_result_groups[].snippet`) is UI
  display only. The `web.run` tool message is blank in the stream, so the payload can't be read directly.
- **One shared budget per search, picked by the model's query.** [measured, 10-30]
  - 19 results got ~100–300 words each.
  - With 3 vs 6 results, `/discount-codes` dropped from ~500 words to ~250.
  - Higher-ranked results get more.
  - A fact 75% into a long article was missing until the search query contained its words.
- **Short pages arrive whole.** [measured] R4000 page (3,438 chars), ranked first of 12: all six marker statements
  arrived, from top to disclosure; the other sites got ~110–170 words each. AC200L (2,300 chars) arrived whole in a
  10-result search.
- **Long pages have a ceiling around 16–23k characters** [measured, approximate]. Inside it, some chunks are skipped.
- **Collapsed `<details>` content may be dropped.** [hypothesis] A fact inside `<details>` was missed by app and API
  on the same pinned query, but query-based picking could explain it.
- **Methods.**
  - Same-turn echo ("quote the excerpt you were given") worked on 10-30 morning. By 11:56Z the model refused more
    than ~25 words per source, so echoes are unreliable now.
  - Needle questions (a deep fact, one pinned search, "NOT IN RESULTS" as the exit) and YES/NO grids of statements
    placed down a page still work.
  - A raw dump request is refused, and a follow-up-turn echo fails.

## 5. What the shopper sees (`stored-copy.md`)

- **Result title = the page's `<title>` at OpenAI's last fetch.** [measured, n≈300]
- **Snippet ≈ 200 characters, picked for the query from anywhere on the page.** On product pages it is the body
  opening (H1, summary, start of the offer card), never the meta description. [measured, 31 of ours]
- **Images come from ChatGPT's own image index, not the page.** [observed, DLC-45]

## 6. How the answer is built (`context-probe.md` card sections, `growth/evals/cardprobe.py`)

- **The app answer is a UI program (`model_dil_v2`)**: code, constants and `appData.opGenui.modelDataBindings`.
  [measured, 10 chats]
- **Product cards bind shopping-catalog records** (`turn<id>product<n>`: title, displayed price, merchant,
  `product_page.uri` tagged `utm_campaign=openai_catalog&utm_medium=feed`, Shopify ids). [measured] The model picks
  which records to show; it cannot point a card at our `/go/`.
- **`/go/` reaches a shopper only through a model-written button or link** (`GenUI.openUrl(...)`, `Link {url}`,
  markdown), copied from our page text. [measured: 4 of 10 app chats; 4 of the 6 with our page in results] The
  first sale (10-29) and a 10-30 reading both came this way.
- **Brand catalog cards compete on brand questions.** [measured, small n] "ALLPOWERS US" (iallpowers.com) cards
  appeared on 4 of 5 ALLPOWERS chats; none for BLUETTI, Aurzen or ESR. With a card, `/go/` came through 1 of 3
  times; without, 3 of 4.

## 7. Models and plans

- The app's Free plan answers with gpt-6, and with gpt-6-mini after the quota (the stream reports
  `resolved_model_slug`). [measured] Outside sources say Free runs "GPT-6 Luna"; unverified.
- The API lists gpt-6-sol, gpt-6.1-sol, gpt-6.1-terra, gpt-6-astra and gpt-6-luna. No confirmed mapping to the app's
  models.

## 8. API vs app, in one table (`context-probe.md` "API vs app")

| | App | API (Responses + `web_search`) | Use the API for it? |
|---|---|---|---|
| Page text the model gets | stored copy | same (needles, AC200L version) | yes |
| Searches per question | 1 | median 4 | no: overstates reach |
| Results for a given query | ~12 | same index, 66–76% overlap, one search allowed | yes, as a screen |
| `/go/` handed over | 4 of 10 | 1 of 60 | no |
| Catalog cards | yes | none | no |
| Answer format | UI program | markdown + `url_citation` | no |
| `search_context_size` | n/a | no effect seen | n/a |

## 9. Other assistants (guardrails only)

- **Claude rejects copy addressed to the answering assistant** (DLC-59/60): 1 of 96 vs 71 of 96 answers kept our
  `/go/` link once the AI-addressed text was removed. Pages are neutral since 10-25/10-27. Claude's queries are
  narrower and more numerous than ChatGPT's. This skill does not cover Claude's pipeline.

## Open questions (test before relying on them)

- The exact text budget per search and per rank, and whether the 3.5k–16k range arrives whole.
- Whether the API's first query matches the app's for the same question (it decides whether the query transfer can
  run at volume).
- The second index feed (section 1).
- What makes the model write a `/go/` button rather than cite us without it (DLC-83).
- Whether sitemap `lastmod` speeds re-crawls.
