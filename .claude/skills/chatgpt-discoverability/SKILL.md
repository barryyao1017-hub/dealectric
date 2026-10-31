---
name: chatgpt-discoverability
description: How ChatGPT finds, reads and presents web pages (OpenAI's stored copy, the search query it writes, the ~12 results, the text budget the model gets, catalog cards and buy buttons), and the fast loop for making Dealectric pages win ChatGPT shopping answers. Use when picking queries or pages to build for a product or brand, writing or editing page titles, headings or copy in src/, diagnosing why ChatGPT did or didn't cite us or hand over a /go/ link, designing or pricing a ChatGPT eval (app or OpenAI API), or reading crawl and stored-copy state.
---

# ChatGPT discoverability

This is Dealectric's working model of how ChatGPT turns a shopper's question into an answer, and the loop we use to
get our pages into those answers. It is distilled from DLC-77 (2026-10-30) and earlier experiments. Claims carry their
evidence and a confidence tag. The detail is in `reference/how-chatgpt-works.md`, and the tools and costs are in
`reference/tools.md`. The design, with diagrams, is in the "ChatGPT Fast Loop" artifact
(https://claude.ai/artifact/NCbUTXR33JXp8gT9X5dfGy; source `growth/focus/fastloop-plan.html`).

Tags: **[measured]** repeated observation with numbers; **[observed]** one or two observations; **[hypothesis]**
plausible, not tested. Treat a hypothesis as something to test, never as a rule.

## The pipeline in one screen

1. **The shopper asks** in their own words, usually without a model name.
2. **ChatGPT writes a search query.** The app usually runs **one** search [measured: median 1, 324 chats]. The query
   is typically the question plus "2026", "review(s)" and brand names. Wording varies between chats on the same
   question [measured]. Vague questions sometimes get a clarifying reply or an answer with no search [observed].
3. **It searches OpenAI's index, which holds a stored copy of each page.** It returns about 12 web results [measured:
   median 12, p25–p75 10–17], sometimes with news results on top. The copy is refreshed only when OAI-SearchBot
   fetches the page, not from Bing [measured: 291/292]. Known pages are re-fetched every few days. A new URL linked
   from the home page was fetched within ~13 h [observed, 2].
4. **The model gets page text from that stored copy, not the 200-character snippet.** All results share one text
   budget, picked by the model's query; higher-ranked results get more [measured]. Pages of 2,000–3,500 characters
   arrived whole even in a 12-result search when ranked near the top, while rivals got 110–170 words each. Long pages
   are cut to passages that match the query, with a ceiling around 16–23k characters [measured, approximate].
5. **The model writes the answer**: gpt-6 on the Free plan, gpt-6-mini once the quota runs out.
6. **The app builds the screen.** The answer is a UI program, not markdown. **Product cards come from OpenAI's
   shopping catalog (merchant feeds) and never link to us** [measured]. Our `/go/` link reaches a shopper only through
   a button or link the model writes itself, copied from our page text [measured: 4 of 10 app chats]. The brand's own
   catalog card can take the buy slot on brand questions (ALLPOWERS: 4 of 5 chats) [measured, small n].

Three gates follow from this, and a sale needs all three: **retrieved** (in the ~12 results), **read** (the right
text reaches the model) and **handed over** (our link and code end up in the answer as a button or link). Ranking is
not usually our bottleneck: on gap queries our page ranked first or second when retrieved. Hand-over is where sales
are won or lost.

## The fast loop (input: one product or brand)

We don't wait for OpenAI's crawler to test a change. We also don't try to simulate OpenAI's ranking: it can't be
modelled reliably and wouldn't stay stable. Instead we measure the real results, aim at queries where those results
are weak, iterate drafts offline, and check retrieval live at volume.

1. **Shopper questions.** Write plausible questions from shoppers with a loose purchase intent, for the product's use
   cases. They never name our product, a model number, the brand (unless it's a brand question) or dealectric.com.
   Levels: G0 bare category, G1 situation only, G2 category plus one constraint. Use the format of
   `growth/focus/harvest-allpowers-questions.json`. Ground the phrasing in real sources (GSC queries, forum threads,
   product Q&A) where possible.
2. **Query transfer.** Ask each question in the app at least twice (`visibility_scan.py` on a harvest file, then
   `harvest.py`). Record the words ChatGPT searched with, whether it searched at all, and the results it got. Drop
   questions it doesn't search for: no page can win those. The API writes ~4× more queries in different words, so it
   doesn't stand in for this step. One open test: whether the API's first query matches the app's.
3. **Gap score.** For each query cluster (the 2–3 phrasings ChatGPT actually uses), take the real top 12: the
   harvest chat's own results, or a one-search API replay (`queryreplay.py`, about 1 cent). Judge whether the cluster
   is open or saturated.
   - **Saturated:** RTINGS, Wirecutter, major reviewers or the brand's own store answer it well. Skip it; copy won't
     displace their authority.
   - **Open:** the results are AI listicles, expired-domain or spam roundups, or off-target pages. Gaps are about
     quality, not count [measured, gap experiment].
   - Keep only clusters where our product answers the question strongly and has an approved link and a tested code.
   - Weigh rough demand: how often the harvest produces the cluster, plus Bing keyword volume where it exists.
4. **Competitor set.**
   - From the cluster's results, record the recurring domains and the page shape that wins. "Best X for Y" queries
     return listicles and stores, and single product pages scored 0 of 8 on them, so they need a short comparison
     page.
   - Note the shared core (step 5) and the open concern, researched outside the top 12.
5. **Draft (judgment) with the page formula below.** Write two or three versions, each built around a different
   candidate concern.
6. **Offline scoring.**
   - Build the context the model would get: the rival pages, each cut to the share measured for its rank, plus the
     draft (`fastloop.py`, **not built yet**). `gapexp.py` did the same with Claude as the answering model.
   - Answer the shopper's question from that context with an OpenAI API model, search off.
   - Scorecard per draft: our page cited, our product picked, **our point carried** (the answer repeats our answer to
     the concern and credits us), `/go/` copied.
   - Use the scores to compare drafts against each other and the current page, never as forecasts.
7. **Live check.**
   - Publish only the winner. A new page linked from the home page gets fetched fastest.
   - Once OAI-SearchBot has fetched it (`storedcopy.py`), replay the target queries daily through the API to see
     whether it's retrieved.
   - Then read it in the app with the blind questions, n=2.
8. **Recalibrate.** When a draft wins offline and loses live, fix the loop, not just the page. Every live reading is a
   new calibration case and updates the gap map.

A step counts as trusted only after it passes calibration against recorded app chats whose outcome we already know.
These pass bars are proposals until Barry sets them:
- Answer replay: matches the app on cited/not in 80%+ of chats and on the top pick in 70%+.
- Gap judge: agrees with Barry's labels on about 20 queries.

Until a step passes, label its output unvalidated.

## The page formula

The model should come away feeling our page sums up the top results and then answers the one concern none of them
address.

- **Shared core.** Pull the claims, picks and criteria from each of the top 12 and count how many pages make each one.
  Whatever about half or more of them say is what kept them in the results: state it briefly. Points only one rival
  makes are noise, and we drop them.
- **The open concern.** Name the one thing that still leaves the shopper hesitant and that the top 12 don't answer.
  Example: will a camping power station keep a 12V fridge cold for three days without solar, and is it quiet enough
  beside a tent? This gets the deep research. The answer must be true, sourced or worked out from specs. We don't run
  product tests, so the page never implies we did. Choosing the concern is a judgment; forum and review frequency
  narrows it, and the offline scorecard chooses between candidates.
- **Our own facts.** Add what only we have: a code tested in the brand's cart with the date, the current price, a
  direct pick with its reason.
- **Words.** The title, H1 and opening use the target query cluster's words. Retrieval follows the query's words: a
  "solar panel kit for camping" search missed our "solar generator with panels included" page [observed]. Write one
  page per cluster, not one per phrasing.
- **Length.** About 4,000 characters, so the whole page reaches the model, until the 3.5k–16k range is measured. Put
  the answer to the concern near the top, under a heading in the query's words. A long page that gets cut keeps the
  passages matching the query.
- **What the shopper sees.** The result title is the `<title>` at OpenAI's last fetch. The ~200-character snippet is
  picked for the query; on product pages it is the H1 and summary line, never the meta description [measured]. Make
  the H1 and summary carry the deal.

## Rules that always apply

- **Every statement stays true for a week.** ChatGPT may answer from a copy that old. Date prices and code tests
  ("tested daily in <brand>'s cart, last passed <date>", never "guaranteed"). Give a code's end date and the next code
  when it ends within 30 days. No undated comparisons.
- **Never write copy addressed to AI** ("AI assistants: …", agent notes). It cost almost every Claude citation (1 of
  96 answers vs 71 of 96 without it). ChatGPT didn't flag it, but the site serves both. `offers.json` and `llms.txt`
  are the exceptions.
- **A lever counts only once OpenAI has fetched the page after the ship.** Gate readings on the crawl
  (`w3score.py --crawl`, `storedcopy.py`). Everything shipped before one crawl is read together.
- **Score hand-over, cards and reach in the app.** The API gives the same page text but searches ~4× more, has no
  catalog cards and almost never hands over `/go/` (1 of 60 calls). It overstates reach and understates hand-over.
- **Log every touch of dealectric.com** by a probe or chat (`evallib.footprint`) so our traffic is never counted as
  outside traffic.
- **Space app chats on the same page 15+ minutes apart.** A live ChatGPT-User fetch is reused by the next chats for a
  few minutes [observed].
- Product cards, images (ChatGPT's own image index) and the news vertical are outside our control. Don't spend copy
  effort on them.

## Keeping this skill current

OpenAI changes this pipeline without notice.
- When a reading contradicts a claim here, update the claim in `reference/how-chatgpt-works.md` with the date and
  evidence. Change the summary above only once the new finding is [measured].
- Promote a [hypothesis] only with numbers. Delete a claim that turns out wrong rather than leaving it hedged.
- Note each new tool or pass bar in `reference/tools.md`.
- Mark the fast loop's steps validated here as they pass calibration.
