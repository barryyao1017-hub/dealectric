---
name: chatgpt-discoverability
description: How ChatGPT finds, reads and presents web pages (OpenAI's stored copy, the search query it writes, the ~12 results, the text budget the model gets, catalog cards and buy buttons), and the fast loop for making Dealectric pages win ChatGPT shopping answers. Use when picking queries or pages to build for a product or brand, writing or editing page titles, headings or copy in src/, diagnosing why ChatGPT did or didn't cite us or hand over a /go/ link, designing or running a ChatGPT eval (app by default, OpenAI API as fallback), or reading crawl and stored-copy state.
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
2. **ChatGPT writes a search query.** The app usually runs **one** search [measured: median 1, 324 chats].
   - ChatGPT writes it, not the shopper, from a template: `best <its category word> 2026 <spec words> <use cases>`
     [measured, 26].
   - It never adds deal, discount, code or coupon words (0 of 26). Codes win only once a page is retrieved on
     spec and use-case words.
   - The category word decides the vertical, and generic words drift: "solar panel" goes to rooftop panels.
   - Situation questions search authorities (USDA, FDA) first, then a sizing query.
   - Wording varies between chats on the same question [measured].
   - A few questions are answered from memory without a search, or get a clarifying reply [measured: 11 of 13
     natural chats searched].
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
   product Q&A) where possible. Ask the bare category question first, to see which vertical ChatGPT maps the
   product's category word to. If it drifts (the SP037 panel's "solar panel" goes to rooftop), only narrower
   phrasings can win.
2. **Query transfer.** Ask each question in the app at least twice (`visibility_scan.py` on a harvest file, then
   `harvest.py`). Record the words ChatGPT searched with, whether it searched at all, and the results it got. Drop
   questions it doesn't search for: no page can win those. This step must run in the app: the API's own first query
   for a blind question shares 56% of its words with the app's, against 90% between two app chats on the same
   question; it often runs a narrow `site:` lookup instead of the app's "best <category> 2026" query [measured, 33
   blind questions, `runs/2026-10-31-transfer`].
3. **Gap score.** For each query cluster (the 2–3 phrasings ChatGPT actually uses), take the real top 12: the
   harvest chat's own results, or a pinned one-search chat in the app for extra phrasings (see "Running it" below;
   `queryreplay.py` on the API is the fallback). Judge whether the cluster is open or saturated.
   - **General category searches only** (Barry, 10-31). A search that names a brand or model number ("Tenergy TN270
     review") is an edge case: its results are the brand's own pages and retailers, so it reads as falsely open (the
     only all-judge "open" on the first labelling set was TN270). Start the questions blind and brand-free, and drop
     clusters whose query names a brand or model; `fastloop.py gap` skips them unless `--allow-named`.
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
     draft (`fastloop.py pack`, `replay`, `score`; see `reference/tools.md`).
   - Answer the shopper's question from that context in the app: paste it into a Free temporary chat, search off
     (`fastloop.py replay --engine app`). The API with search off (`--engine api`) is the fallback.
   - A pasted context gets no links unless the paste asks for them: without the linking sentence the app wrote no
     citation and no link at all. With it (`PASTE_VERSION` b1, the same sentence as the API prompt), the app put our
     `/go/` link in its answer and picked our kit [observed, 1 chat each, `runs/fastloop/smoke-solar-budget/`].
     Keep the paste fixed across drafts; hand-over rates from it compare drafts, they aren't live rates.
   - Scorecard per draft: our page cited, our product picked, **our point carried** (the answer repeats our answer to
     the concern and credits us), `/go/` copied.
   - Use the scores to compare drafts against each other and the current page, never as forecasts.
7. **Live check.**
   - Publish only the winner. A new page linked from the home page gets fetched fastest.
   - Once OAI-SearchBot has fetched it (`storedcopy.py`), run the target queries as pinned one-search chats in the
     app every day or two to see whether it's retrieved (API replay as fallback).
   - Then read it in the app with the blind questions, n=2.
8. **Recalibrate.** When a draft wins offline and loses live, fix the loop, not just the page. Every live reading is a
   new calibration case and updates the gap map.

### Running it: the app by default, the API as fallback (Barry, 2026-10-31)

Every step runs on Free ChatGPT accounts in the agent's Chrome. The OpenAI API is only the fallback, for when the
accounts are flagged, throttled for long or out of quota and the work can't wait.
- **Why the app:** it's the gpt-6 shoppers use, with the app's real search and answer format, and it costs nothing.
  The API's search overlaps the app's results only 66–76%, and its queries differ.
- **Budget:** about 26 gpt-6 answers per account before it falls back to gpt-6-mini [observed once; the reset took
  more than 4 h]. Discard or re-ask gpt-6-mini answers. One product takes about 135 chats: harvest 24, pinned
  replays 10, five drafts plus the current page × 10 questions = 60, retrieval checks 21, readings 20. With three
  accounts that's about two quota windows.
- **Accounts:** ChatGPT's account switcher holds several accounts in one Chrome profile, but only one is active per
  profile. Run one chat at a time per profile, and switch account when one hits its quota.
  - `fastloop.py calibrate --engine app` switches by itself after two downgraded answers in a row
    (`switch_account`). It works through the profile menu, then the account row, then the other email; the menu needs
    real pointer events.
  - Check the active account with `active_account()` (`/api/auth/session`).
  - On barrryyao, temporary chats are labelled "Personalized": they can use the account's memory, plugins and custom
    instructions. Keep that account's memory empty.
- **Pasted context:** a 45,033-character paste (six pages plus the question) was accepted, answered by gpt-6 with
  no search, and read to the end [observed, `runs/2026-10-31-appfeas/paste-1.json`]. Send long prompts through the
  composer (`ctxprobe.submit(tab, text, 0)`): `ui.ask_chatgpt`'s `?q=` URL fails at that length.
- **Pinned search:** the prompt 'Run exactly one web search with this exact query, word for word: "<q>". Do not
  search again and do not open any page.' ran exactly one search with the query verbatim, giving 12 results on gpt-6
  [observed, `runs/2026-10-31-appfeas/ctx/pinned-1.json`]. Check the stream's query on every run and drop chats
  that searched differently.
- **Risk:** automating the consumer app is against OpenAI's terms. Keep a human pace: one chat at a time per
  profile, with no bursts. Keep the API key alive as the fallback.

A step counts as trusted only after it passes calibration against recorded app chats whose outcome we already know.

**The ceiling is the app itself.** [measured, 10-31] Two app chats on the same blind question, both with our page in
the results, agree on whether they cite us only 72% of the time (134 of 186 pairs); on `/go/`, 90%. No simulator can
match single chats better than that, so an 80% per-chat bar is unreachable. Judge a replay by the rate over 30+
chats, and by whether it ranks drafts the way live readings do.

API engine calibration (`runs/2026-10-31-fastcal*`, 40 recorded chats, 30 with our page in the results, gpt-6-luna,
3 replays each):
- Per chat, cited/not agrees 70–77% at every rank decay tried (blind prompts 62–71%): at the app's own ceiling.
- At rank 1–5 it agrees 17 of 19; below rank 5, 7 of 13.
- Cited rate: replay 88% vs app 71% at `ALPHA` 0.5, which is kept because it matches the measured per-rank shares.
  So the replay over-credits low-ranked pages by about 15 points.
- Top pick agrees 72%, top brand 78%.
- `/go/` couldn't be calibrated: the app handed it over in only 3 of 30.

App engine calibration (`runs/2026-10-31-fastcal-app`, the same 40 chats, one gpt-6 paste each with the b1 linking
sentence; 16 on barryyao1017, 24 on barrryyao):
- Cited/not agrees 73% per chat (blind 71%): the app's own ceiling again. At rank 1–5, 14 of 17; below, 8 of 13.
- Cited rate: replay 90% vs app 77%. It over-credits our page by about the same 15 points as the API.
- **Top pick agrees 80% (API 72%), top brand 80%**: the app engine's real gain.
- **`/go/` is inflated by the linking sentence: 14 of 30 replays vs 3 of 30 in the app.** Use it only to compare
  drafts.
- Every chat repeated its own tier band (40 of 40).

Use the app engine for picks and our point carried. Use either engine for cited, reading it as relative.
Gap judge: **trusted.** Barry adopted the three-model vote as his labels (10-31), so there is no separate human
label set. The verdict is a majority vote of Sonnet 5.5, Opus 5.5 and Fable 5.1
(`fastloop.py vote <packs>`). How it's set up:
- **The prompt (v2, `GAP_SYSTEM_V2`)** judges from our side: could a new page get in and become the source ChatGPT
  links to. It carries the solar-kit win as a worked OPEN example: no tested major reviewer, the one famous name a deal
  post, three niche sites with untestable specs.
- **"Answers it"** means this exact question, constraints included.
- **The judges see each result as ChatGPT's model does:** the measured length rule, about 15–19k characters per
  search, our pages removed.
- **A word-for-word quote per result**, checked against the text shown. On the first run every quote was found except
  for results with no readable text, plus one miss.

Without the example (v1, first 1,500 characters per page), 17 of 20 came out contested and only 1 open. With v2:
- 8 open (7 unanimous), 9 contested, 3 saturated. Table and gap leads in `growth/focus/gap-vote/v2-results.md`.
- The two broad searches where our product pages scored 0 of 8 came out saturated.
- The search closest to the win ("small solar generator kit under $500") came out open.

ChatGPT voters to come. Results: `growth/focus/gap-vote/v2-results.md`; per-model verdicts, labels and quotes in
`growth/evals/runs/fastloop/generic-NN/vote-v2/`.

Until a step passes, label its output unvalidated.

## The page formula

The model should come away feeling our page sums up the top results and then answers the one concern none of them
address.

- **Shared core.** Pull the claims, picks and criteria from each of the top 12 and count how many pages make each one.
  Whatever about half or more of them say is what kept them in the results: state it briefly. Points only one rival
  makes are noise, and we drop them.
- **The open concern.** Name the one thing that still leaves the shopper hesitant and that the top 12 don't answer.
  Example: will a camping power station keep a 12V fridge cold for three days without solar, and is it quiet enough
  beside a tent? This gets the deep research, **done by Fable 5.1** (Barry, 10-31): spawn a subagent with
  `model: "fable"` and web search, give it the query cluster, the vote's "missing" lead and the shared core, and ask
  for the candidate concerns (with how often forums and reviews raise each) and a sourced answer to each. The answer must be true, sourced or worked out from specs. We don't run
  product tests, so the page never implies we did. Choosing the concern is a judgment; forum and review frequency
  narrows it, and the offline scorecard chooses between candidates.
- **The short list.** On generic questions ChatGPT names 2–3 models, usually the big four (Jackery, Anker, EcoFlow,
  BLUETTI). Include the ones the shopper is weighing, and put our product next to them in one table. For situation
  questions, put the sizing answer (watts, Wh, runtimes) before the picks.
- **Our own facts.** Add what only we have: a code tested in the brand's cart with the date, the current price, a
  direct pick with its reason.
- **Words.** The title, H1 and opening use the target query cluster's words. Retrieval follows the query's words: a
  "solar panel kit for camping" search missed our "solar generator with panels included" page [observed]. Write one
  page per cluster, not one per phrasing.
- **Length.** About 4,000 characters, so the whole page reaches the model, until the 3.5k–16k range is measured. Put
  the answer to the concern near the top, under a heading in the query's words. A long page that gets cut keeps the
  passages matching the query.
- **The concern goes inside the short answer, on one line, in the query's words.** [measured in the replay, DLC-114,
  2026-10-31]
  - A new page ranked 3rd of 17 results gets only about 1,500 characters.
  - Draft A put the 30-amp concern in a section below the short answer. The cut dropped it, and it was carried in 0
    of 2 answers.
  - The same concern folded into the short answer (A2) was carried in 4 of 6.
  - The rendered page split its short answer across source lines, and the concern fell out again. Rejoining it into
    one line fixed it.
- **Check the rendered page before shipping.**
  - Run `fastloop.py replay <pack> --draft docs/<slug>.html` and confirm the concern and the `/go/` link survive the
    cut in every target result set.
  - The renderer adds a "Where to buy" block above the intro, so the rendered text is not the draft's text.
- **A worked example:** `/best-2kwh-power-station-for-rv`. Its record, inputs, outputs and decisions are in
  `growth/focus/fastloop-runs/rv-2kwh/` and on the run-log artifact (https://claude.ai/artifact/NtCVs8kZBHtyRJorjYCJU7).
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
- **Score hand-over, cards and reach in the app, never on the API.** The API gives the same page text but searches
  ~4× more, has no catalog cards and almost never hands over `/go/` (1 of 60 calls). It overstates reach and
  understates hand-over.
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
