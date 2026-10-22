# Tracked-link improvement loop, phase 2: the discount-code hypothesis — report (draft, 2026-10-22)

Plan: `growth/improvement-loop.md`, "Phase 2". Iteration files, LOOP.md rows and report pages: `growth/evals/loop/`
(`phase2-iter-NN.md`; report artifacts linked on each file's first line; iteration 0:
https://claude.ai/artifact/D9SkG4xfU1mNqNEvd7ENG4). Harness: `growth/evals/` (`ui.py` drives signed-in chatgpt.com in
the agent's Chrome; `run.py --assistants claude-code` runs Claude as an agent through the Claude Code CLI; `grade.py`,
`report.py`, `iterreport.py`, `copycheck.py`, `reprobe.sh`). The app column is **ChatGPT, signed in, Free plan,
temporary chats, web search on**; claude.ai, Gemini and Grok are still without logins (DLC-40).

The question: does a working discount code with a very recent cart-test date next to it make ChatGPT hand the
shopper Dealectric's tracked buy link (`https://dealectric.com/go/<slug>`) together with the code? Tiers: **B** "Use
dealectric.com to find X and give me Dealectric's buy link" (phase 1's named tier), **D** "Does dealectric.com have a
working discount code for X? Give me the code and Dealectric's buy link", **E** "Use dealectric.com to find the best
current discount on X". Metric: the **code-and-link rate**, an answer with the `/go/` link of the product and a code
Dealectric publishes for it, plus the tracked-link rate per tier for comparison with phase 1.

## 1. How the assistants differ

_(to be completed after the iterations; what is already established:)_

**ChatGPT (the app, signed in, Free).** Answers shopping prompts with its own widget markup (`model_dil_v2`): a
product card with the price, a "Copy code" button and a buy button that is `<button onClick={() => GenUI.openUrl(
"https://dealectric.com/go/…")}>`, not an href. 11 of its 43 baseline `/go/` links existed only there. It takes the
code from the page it has, quotes our freshness line back ("Dealectric reports that it tested this code in BLUETTI's
checkout on October 21, 2026") and never invented a code (0 WRONG_CODE in 60 answers; the three negative controls
on tier D, asking for a code for a product we do not list, passed 6/6). What it reads is its **search-index copy of
a page**, not the live page: an hour after a deploy, with Cloudflare showing a ChatGPT-User fetch of the live page,
it still answered from the version a day old (old title, old price, "verified October 14"). 13 of 60 baseline
answers carried the same pre-10/21 date.

**Claude as an agent (Claude Code CLI).** Fetches live: home page, offers.json or the product page, then links
`/go/` from the data, with the code and its test date; 23/24 (baseline) and 24/24 (after the rebrand) on the same
questions, 16 of 24 post-rebrand answers quoting the cart test. It is unaffected by ChatGPT's index lag: the day's
copy is what it reads.

**After the rebrand, ChatGPT** hands over code and link together when it reaches a product page ("Discount code:
PARTNER18 — saves $17.99. Reported tested in ESR's checkout today … Buy link"); its remaining misses come from
landing on the home page, the catalog page or a guide and stopping there ("I couldn't verify the exact
product-specific buy URL"), which iteration 2 addresses on the catalog page.

## 2. What we changed

| iteration | change (lever) | ChatGPT code-and-link D / E before → after | tracked link B / D / E | stayed? |
|---|---|---|---|---|
| 0 | baseline, no copy change (instrument: widget-aware `ui.py`) | 70% / 60% (on the 8-question subset 75% / 62%) | 80% / 75% / 60% | — |
| 1 | the rebrand: one canonical paragraph (code, saving, test date, link, "give both") on every surface, offer block first on the product page, Worker `/go/` text page names the code; plus the daily cart check | 75% / 62% → 81% / 90% (D+E 69% → 85%, 8 questions, fresh cells) | 63% / 81% / 90% | yes (improvement; 6 stale tier-E cells excluded) |
| 2 | the catalog page's cards carry the code, the saving, the test date and the buy link (ChatGPT's search lands on `/products`) | _(pending)_ | | |

## 3. Why the loop stopped

_(pending)_

## 4. Iteration count and cost

_(pending; so far: baseline 84 ChatGPT chats + 60-chat DOM-only pilot + 5 probe chats, two throttle waits; claude-code 42 + 28 calls;
judge passes on 126 rows; harness work: tiers D/E and the code dimension, the widget-markup read, the background-tab
fix, the 44-chat design, copycheck/reprobe, the daily cart sweep.)_

## 5. Other findings

- **The buy link in ChatGPT is often a widget button, not a link.** Any DOM-based reading undercounts it; the
  conversation JSON (`/backend-api/conversation/<id>`) holds the markup. Phase 1's ChatGPT tier-B figures (15–30%)
  were read DOM-only and are not comparable with phase 2's 80%.
- **ChatGPT's page copy lags days behind the site.** It fetches the live page (Cloudflare logs it) and still answers
  from its index copy. A copy change cannot be measured until that copy turns over; `copycheck.py` proves what the
  fetcher gets, `reprobe.sh` waits for the index, and `stale_copy` marks cells that read old copy.
- **The code travels more easily than the link.** Before the rebrand ChatGPT showed the right code in 85% (D) and
  80% (E) of answers but gave the tracked link with it in 70% / 60%; the gap is CODE_ONLY answers (code with the
  product page, the catalog page or no link).
- **ChatGPT Free's throttle bounds a run at about 60 chats**; the per-iteration design was cut from 84 to 44 chats
  (8 questions, tier B once, D and E twice, lite controls) so a run fits one window, and every chat's result is
  written as it finishes so a stopped run resumes.
- **Tabs opened over /json/new steal the Mac's focus**; `Target.createTarget(background=true)` does not.

## 6. Did the code move the link (B vs D vs E)

_(pending; baseline side by side, ChatGPT, 10 questions × 2:)_

| tier | tracked link | right code shown | code-and-link |
|---|---|---|---|
| B named (no code asked) | 80% (16/20) | 50% (10/20) | 50% (10/20) |
| D discount-named | 75% (15/20) | 85% (17/20) | 70% (14/20) |
| E discount-only (no link asked) | 60% (12/20) | 80% (16/20) | 60% (12/20) |

Before any copy change, asking for a code did not raise the link rate (D 75% vs B 80%) but doubled the chance the
shopper gets the code with it (code-and-link 70% vs 50%); asking only for a discount (E) still produced the tracked
link 60% of the time without the shopper asking for one.
