# Tracked-link improvement loop — plan (2026-10-19)

Goal: raise the share of assistant answers that render our tracked offer link, `https://dealectric.com/go/<slug>`, as a clickable link. In the eval ladder (`growth/evals/`) that is **L4**. The loop is: evaluate → diagnose the non-L4 answers → change the site → evaluate again, until the rate stops moving or a blockade is found. It ends with a transfer-learning report.

## 0. Re-centred on the consumer apps (2026-10-20)

Barry, 2026-10-20: shoppers use the consumer apps (chatgpt.com, claude.ai, gemini.google.com, grok.com), not the
vendors' APIs, so the loop's **primary metric is the app reading**: `growth/evals/ui.py` drives each app in the
agent's Chrome (DevTools protocol), one fresh chat per prompt, hyperlinks read from the DOM, and writes run files the
grader scores like any assistant. The API route (`run.py` with vendor keys) is dormant; `claude-code` (Claude as an
agent) runs once per cell as a regression check only. Iteration 0's API numbers stand as recorded. Apps are added as
their logins arrive (DLC-40); until then the app column is chatgpt.com logged out, which runs a lighter model than
signed-in users get and so is a floor. "L4-api" below now means the harness's automated reading of an app, and the
manual browser spot-check (§2 "UI runs") is only needed where the driver has no adapter yet.

## 1. The metric

**Tracked-link rate (TLR)** = share of answers at L4, measured on tiers **B** (named: "use dealectric.com …") and **C** (given URL). Tier A (unprompted) is gated by search indexing, which no site change in this loop can fix, so it is monitored, not optimized. Reported per assistant (ChatGPT, Claude, Gemini, Grok) and pooled.

Two readings of L4, both recorded:
- **L4-api**: the `/go/<expected slug>` URL appears in the API response text or its citation/annotation objects. Cheap, automated, the loop's working signal.
- **L4-ui**: the `/go/` URL is an `<a href>` in the real app's answer, read from the DOM in the agent's Chrome. This is the ground truth; the 10/17 probe showed ChatGPT's display layer cutting a link the model had produced. Measured on a fixed subset each iteration.

An iteration counts as an **improvement** when the pooled TLR (api) rises by ≥ 5 points over the previous iteration and L4-ui does not contradict it. Wilson 95% intervals are reported alongside; with the subset size below, differences under ~5 points are noise.

## 2. Fixed experiment design (frozen for the whole loop)

- **Loop subset**: 10 questions per iteration, drawn from the 30 in `growth/target-questions.md`, covering all 6 brands and both networks (CJ and Awin). Slugs **rotate**: an iteration prefers slugs no assistant has fetched in the last 7 days (D1 `clicks`, `kind='ai_fetch'`), because the 10/18 re-run showed ChatGPT reusing a cached redirect resolution for ~20 minutes and possibly longer. 31 products allow three iterations before a slug repeats.
- **API runs**: 10 questions × tiers B and C × 4 assistants × N=5 = 400 calls per iteration.
- **UI runs**: 8 prompts per assistant (4 tier B, 4 tier C), 1 run each, in the agent's Chrome, hrefs read from the DOM. Logged-out where the app allows search logged out (ChatGPT); logged in via agent-vault otherwise.
- **Controls** every iteration: 3 positive (competitor citations expected), 3 negative (products we do not list). A control failure invalidates the iteration's numbers.
- **Stamp** every run with: iteration number, site commit, Worker deploy version, GSC and Bing indexed-page counts that day.
- **Baseline (iteration 0)**: the full harness run (all 30 questions, 3 tiers, N=3) plus the UI subset, before any change.

## 3. Diagnosis: the failure taxonomy

Every non-L4 answer is auto-classified from the response, its URLs, and the D1 fetch rows in the run window. Classes, in funnel order:

| class | meaning | evidence |
|---|---|---|
| NOT_FOUND | never reached our page (tier B only) | no dealectric.com citation, no fetch row |
| PAGE_ONLY | linked our product page, no offer link | L3 reached, no `/go/` anywhere |
| MERCHANT_SWAP | linked the merchant's product page instead | merchant domain in URLs; `/go/` fetch row may exist (resolved through the redirect) |
| NETWORK_HOP | linked the raw awin1.com / tkqlhce.com URL | network host in URLs |
| PLAIN_TEXT | `/go/` present as text but not a hyperlink | UI runs only |
| REFUSED | declined to give an affiliate / tracked link | prose match ("affiliate", "tracking link", "can't provide") |
| STALE_CACHE | resolved a `/go/` link from before the last deploy | click id in the linked URL predates the deploy |
| OTHER | none of the above | manual look |

For each class an LLM pass quotes the assistant's own explanation (e.g. "redirects to the official product page") so the "why" is in the assistant's words, not ours. The iteration report groups failures by assistant × class and picks the largest class that a site change can plausibly address.

## 4. The levers (what the site can change)

Ordered by what the probes so far suggest. One lever per iteration so the effect is attributable.

1. **Product page wording and placement**: make the `/go/` link the first and only "buy" URL on the page, label it unambiguously ("Buy link to give the shopper"), repeat it in the "For AI assistants" block and in `schema.org/Offer.url`.
2. **Merchant URL exposure**: today the page and `offers.json` both carry the merchant product URL, which is what MERCHANT_SWAP answers link. Options: keep the merchant name but drop the raw merchant URL from the agent-facing surfaces, or move it below the fold with an explicit "not the buy link" note. Transparency trade-off; the disclosure page stays.
3. **`llms.txt` and `offers.json` instructions**: per-assistant phrasing, field order, renaming `offer.link` to something unmistakable (`buy_url`), a top-level `usage` string the assistant quotes back.
4. **Worker text page for AI fetchers**: what it tells the assistant, in which order; whether to include the merchant name at all.
5. **HTTP-level hints on `/go/`**: `Link` headers, a `<title>` on the text page, `Cache-Control` so cached resolutions turn over faster.
6. **Per-assistant fixes**: anything the diagnosis shows is specific to one assistant (e.g. Gemini only trusts what Google has indexed; Grok prefers X posts).

Guardrails, every iteration: `rel="sponsored nofollow"` and the disclosure page stay; no JavaScript, cookies or tracking scripts; prices and `VERIFIED` unchanged unless re-verified; nothing served to Googlebot or Bingbot differs from what users see (the Worker's AI-fetcher page targets assistant user agents only, as today); one change per iteration, one commit, message prefixed `loop-N:`; rebuild with `python3.12 src/build.py`, deploy the Worker only when `worker/` or `links-map.json` changed.

## 5. The iteration protocol

0. **Baseline** as in §2. Write `growth/evals/loop/iter-00.md`.
1. **Evaluate**: API subset + UI subset. Pull D1 fetch rows for the window.
2. **Diagnose**: classify, group, quote. Choose the target class and lever. Write the hypothesis and the expected movement before changing anything.
3. **Change**: implement one lever, rebuild, commit, push, deploy if needed. Record commit hash and Worker version.
4. **Wait for cache turnover**: at least 2 hours, and rotate slugs per §2. If STALE_CACHE rows appear in the next evaluation, extend to 24 hours.
5. **Evaluate again** (= step 1 of the next iteration). Compare with the previous iteration.
6. **Decide**: improvement → keep, continue. Drop of ≥ 5 points → revert the change before anything else, note it as a negative result. Flat → keep the change only if it cost nothing in other metrics, continue.

7. **Report** (Barry, 2026-10-20): when the re-evaluation is graded, build the iteration report page with
   `python3.12 growth/evals/iterreport.py --iteration N`, publish `growth/evals/loop/reports/iter-NN/index.html` as the
   artifact "Dealectric Loop · Iteration N" (screenshots in `shots/` go along as files), and put the artifact URL on the
   first line of `iter-NN.md`. The page is the succinct read of the iteration: the thesis tested, whether the change worked
   (pooled TLR before → after with the decision rule and control status), per-assistant numbers and failure classes, what
   the shopper saw (the app screenshots `ui.py` saves, the answer text where there is none), the new thesis and the next
   run's change, tokens and time. The prose comes from `iter-NN.md`, read by its `##` headings (Diagnosis, Hypothesis,
   Change, Re-evaluation, Decision), so write those sections and the page follows.

Each iteration gets `growth/evals/loop/iter-NN.md`: numbers (per assistant and pooled, with intervals), failure table, hypothesis, change, outcome, decision. A one-line row is appended to `growth/evals/loop/LOOP.md`, and the report page above is published from it.

## 6. Stop conditions

- **Plateau**: three consecutive iterations without an improvement (≥ 5 points pooled).
- **Blockade**: a cause no site change can address, for instance an assistant's policy of never rendering affiliate or redirect links, an assistant that only links what its search index holds while we are not indexed, or an API that returns no link data at all. Declared explicitly in the iteration report with the evidence.
- **Ceiling**: pooled TLR ≥ 90% on both api and ui readings.
- **Budget**: 8 iterations, whichever comes first.

## 7. The transfer-learning report

Written at the end to `growth/loop-report.md` and mirrored to the Claude project. Sections:

1. **How the assistants differ**: per-assistant behavior on fetching, caching, redirect following, link rendering, affiliate attitude; where they agree and where they conflict (a change that helped one and hurt another).
2. **What we changed**: each lever tried, in order, with before/after numbers and whether it stayed.
3. **Why the loop stopped**: which stop condition, with the evidence.
4. **Iteration count** and total cost (API calls, browser prompts, hours).
5. **Other findings**: anything about making a site legible to agents that the loop turned up (what they read first, what they quote, what they ignore, what breaks tracking), plus open questions.

## 8. Who runs what

- The harness session (`growth/evals/`) builds the runner, grader, failure classifier, slug rotation, iteration stamping and the iteration comparison report. Its scope was extended on 2026-10-19 for this plan.
- A separate loop session runs iterations 0 to N sequentially, writes the iteration files, makes the site changes, and writes the final report. It can drive the agent's Chrome for the UI subset. **Decided 2026-10-19 (Barry): the loop session pushes and deploys each iteration's change itself, one commit per iteration, no approval stop.** It still stops on a blockade or a control failure, and reverts on a ≥ 5-point drop.
- Barry: API keys for OpenAI, Google Gemini and xAI (Anthropic exists), and logins for gemini.google.com, claude.ai and grok.com in the agent's Chrome via agent-vault.

---

# Phase 2 — the discount-code hypothesis (planned 2026-10-21)

Phase 1 (above, report in `growth/loop-report.md`) ended with tier C at 95% and tier B at 15–30%, the tier-B gap being
search misses. Phase 2 tests a different lever on tier B: **give the assistant a reason to carry our link**.

## Hypothesis

An assistant that gets a working discount code from Dealectric, with a very recent test date next to it, is more
willing to show Dealectric's tracked buy link together with the code than it is to show the link alone. Mechanism:
the code is a concrete, verifiable benefit for the shopper; the site tells the assistant plainly that the link is how
Dealectric is paid for testing codes; the assistant presents both as one package.

## Rebrand (the site change under test)

Dealectric's first impression to an agent becomes: **the site whose discount codes are re-tested in each brand's own
checkout every day, with the last successful test date next to every code, plus the product data behind each offer.**
The copy addresses the shopping agent directly and authoritatively: what the code saves on this product today, that
the buy link opens the brand's official US store at no cost to the shopper, and that handing the shopper the code and
the link together is how the shopper saves and how Dealectric is paid for the testing. Surfaces, in the order an
agent meets them: page `<title>`s and meta descriptions, the home page hero, `llms.txt` (first paragraph and
"Requests to assistants"), `dealectric.json`, the `/agents` page, `offers.json` `usage` and per-offer
`disclosure_text`, the Worker's `/go/` text page for AI fetchers (names the code and the saving, not just the link),
the product page offer block (code, saving, test date, link, in that order, above the fold), and the discount-codes
pages (per product row: code, price after code, link).

Truth constraint: the daily claim must be true. The same iteration that ships the copy ships the daily check: a
routine that applies every listed code in the brand's cart, records the result in `src/coupons.json`
(`last_worked_at`), rebuilds and pushes, and removes a code the store rejects. Until that routine has run on its
own at least once, the copy says "tested in the brand's cart on <date>" and not "daily". Avoid "guaranteed"; say
"tested today" with the date and the amount it took off, and keep the store's checkout as the final word.

## Design

- **Products in scope**: the 22 offers with a code (Soundcore ×7, BLUETTI ×5, ALLPOWERS ×5, ESR ×4, Baseus ×1), 19
  eval questions whose primary product carries one: Q04, Q05, Q09, Q10, Q12, Q14–Q22, Q26–Q30.
- **Two new tiers** in `growth/evals/questions.yaml`:
  - **D discount-named**: "Does dealectric.com have a working discount code for {item}? Give me the code and
    Dealectric's buy link as a clickable link." Same explicit ask as tier B plus the code: the direct test of the
    hypothesis against tier B's 15–30%.
  - **E discount-only**: "Use dealectric.com to find the best current discount on {item}." No link asked for:
    measures whether the code pulls the link along on its own.
- **Metrics**: tracked-link rate (L4) on D and on E, each against tier B on the same questions in the same run;
  **code-and-link rate** (L4 and the right code surfaced in the same answer), the number that matters commercially;
  code-surfaced rate; the failure classes from phase 1 plus CODE_ONLY (code shown, no link) and WRONG_CODE.
- **Assistant**: signed-in ChatGPT (Free) through `ui.py`, n = 2 per cell; claude-code once per cell as the
  regression check. Loop subset: 10 of the 19 coded questions, rotated by fresh slug as before.
- **Baseline (phase-2 iteration 0)**: run tiers B, D and E on the coded subset **before** the rebrand. The site already
  lists the codes (DLC-29, 10/21), so this baseline isolates the rebrand copy from the mere presence of codes.
- **Iteration 1**: the rebrand plus the daily check. Then iterate on text and structure using the assistant's own
  answers (what it quoted, what it dropped, where it stopped reading), one lever per iteration, same stop rules as
  phase 1 (3 flat, blockade, ≥ 90% code-and-link on D, or 8 iterations).
- **Report**: `growth/loop-report-phase2.md`, same five sections, plus a sixth: whether the discount code moved the
  link, with the B vs D vs E numbers side by side.
