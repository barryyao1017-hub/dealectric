# Tracked-link improvement loop, phase 2: the discount-code hypothesis — report (2026-10-22, iteration 3 added 2026-10-23)

Plan: `growth/improvement-loop.md`, "Phase 2". Iteration files, LOOP.md rows and report pages: `growth/evals/loop/`
(`phase2-iter-NN.md`; report artifacts on each file's first line: iteration 0
https://claude.ai/artifact/D9SkG4xfU1mNqNEvd7ENG4, iteration 1 https://claude.ai/artifact/Xu3Pmk6QAiVaDvqmf2or8a,
iteration 2 https://claude.ai/artifact/L1rGBF6gXDTynNc3Nw3uxP, iteration 3 https://claude.ai/artifact/MpLiLTQBjgNfwsQqXBRhzZ). Harness: `growth/evals/` (`ui.py` drives signed-in chatgpt.com in the agent's
Chrome; `run.py --assistants claude-code` runs Claude as an agent through the Claude Code CLI; `grade.py`,
`report.py`, `iterreport.py`, `copycheck.py`, `reprobe.sh`, `rerun_stale.sh`). The app column is **ChatGPT, signed
in, Free plan, temporary chats, web search on**; claude.ai, Gemini and Grok still have no logins (DLC-40).

The question: does a working discount code with a very recent cart-test date next to it make ChatGPT hand the
shopper Dealectric's tracked buy link (`https://dealectric.com/go/<slug>`) together with the code? Tiers: **B** "Use
dealectric.com to find X and give me Dealectric's buy link" (phase 1's named tier), **D** "Does dealectric.com have a
working discount code for X? Give me the code and Dealectric's buy link", **E** "Use dealectric.com to find the best
current discount on X". Metric: the **code-and-link rate**, an answer carrying the `/go/` link of the product and a
code Dealectric publishes for it; the tracked-link rate per tier is kept for comparison with phase 1. Questions: the
coded subset (10 for the baseline, 8 from iteration 1), n = 2 on the discount tiers.

## 1. How the assistants differ

**ChatGPT (the app, signed in, Free).** It answers shopping prompts with its own widget markup (`model_dil_v2`): a
product card with the price, a "Copy code" button and a buy button written as `<button onClick={() =>
GenUI.openUrl("https://dealectric.com/go/…")}>`, not an `<a href>`. 11 of its 43 baseline `/go/` links existed only
there, invisible to phase 1's DOM read; `ui.py` now reads the conversation JSON. It takes the code from the page it
has and quotes our freshness line back ("Dealectric confirms the discount was tested in the manufacturer's
checkout. Enter EXTRA12 at checkout"); in 172 answers across three iterations it never invented a code (0
WRONG_CODE), and the tier-D negative controls, asking for a code for a product we do not list, passed every time
("its current catalog does not list Jackery"). What it reads is its **search-index copy of a page**, not the live
page: an hour after a deploy, with Cloudflare logging a ChatGPT-User fetch of the live page, it still answered from
the day-old version (old title, old price, "verified October 14"). Product pages turned over in about four hours;
the catalog and home pages had not turned over 36 hours after the rebrand. Which page it lands on decides the
answer: from a product page it hands over code and link together; from the catalog or home page it names the
product with its price and stops ("I couldn't verify the exact product-specific buy URL", "I couldn't verify a
working discount code"), linking the page it has.

**Claude as an agent (Claude Code CLI).** Fetches live: home page, offers.json or the product page, then links
`/go/` from the data with the code and its test date; 23/24 at baseline, 24/24 after the rebrand and again after
iteration 2, 16 of 24 answers quoting the cart test. It is unaffected by ChatGPT's index lag and reads llms.txt,
offers.json and `offer.agent_note`, which ChatGPT does not open.

**Where they agree:** both pass the `/go/` link through whole and both carry the code with it once they have the
product page; neither invents codes. **Where they conflict:** ChatGPT retrieves from an index that lags the site by
hours to days and stops at whatever page the index gave it; Claude navigates the live site.

## 2. What we changed

| iteration | change (lever) | ChatGPT code-and-link D / E, before → after (same 8 questions, fresh cells) | ChatGPT tracked link B / D / E | stayed? |
|---|---|---|---|---|
| 0 | baseline, no copy change (instrument: widget-aware `ui.py`; the DOM-only pilot is kept as `2026-10-22-p2pilot`) | 75% / 62% (10 questions: 70% / 60%) | 75% / 81% / 62% | — |
| 1 | the rebrand: one canonical paragraph (code, saving, cart-test date, link, "give the shopper both") on every surface; product page offer block code → saving → test date → link above the image; `offers.json` `agent_note`; Worker `/go/` text page names the code; llms.txt, dealectric.json, /agents, discount-codes pages, home page; plus the daily cart check (`tools/codesweep.py`, launchd 06:37) | 81% / 90% (D+E 69% → 85%, +16) | 63% / 81% / 90% | yes (improvement) |
| 2 | catalog page cards carry the code, the saving, the test date and the buy link (ChatGPT's search lands on `/products`) | 81% / 92% (D+E 85% → 86%, +1) | 86% / 81% / 92% | yes (flat, no cost) |

Right code shown on D / E: 81% / 81% → 88% / 90% → 81% / 92%. CODE_ONLY (code without the link): 5 → 1 → 0;
OTHER (catalog or home page linked, no code): 3 → 3 → 4. claude-code: 23/24 → 24/24 → 24/24.

Not tried: printing the `/go/` URL inside the code line itself (iteration 1's fallback lever), "daily" in the copy
(the sweep has not yet run unattended; DLC-48), a `/discount-codes` entry per question in the guides.

## 3. Why the loop stopped

Blockade, declared with the evidence in `phase2-iter-02.md`: every remaining ChatGPT miss on the discount tiers is an
answer that landed on the catalog or home page and read ChatGPT's index copy of it, which still predates the rebrand
(the first-pass Q17 answers quoted a product price from before the 10/21 price check; five cells still quoted
"October 14, 2026" at 22:00Z, 13.5 h after the deploy). No page change can be measured on that path until the copy
turns over, and the index is Bing-fed (OpenAI's own crawler has only ever fetched robots.txt). Two further facts
bound the loop: ChatGPT Free throttles at about 60 chats, so an iteration with its re-asks costs a full throttle
window, and the stale re-asks themselves cost 16 chats per round. On the path that does turn over (product pages),
the metric is at 81% (D) and 92% (E), under the 90%-on-D stop rule by three answers of sixteen.

## 4. Iteration count and cost

Three runs (baseline plus two iterations) on 2026-10-22, 06:19Z → 22:07Z, about 16 hours wall clock including a
four-hour index-turnover wait per iteration and two stale re-ask rounds. ChatGPT side: 84 (baseline) + 60 (DOM-only
pilot) + 44 + 16 (iteration 1) + 44 + 16 (iteration 2) + 8 probe and verification chats = 272 chats, four throttle
pauses of 19–26 minutes. Claude side: 42 + 28 + 28 CLI calls for the regression checks plus the judge passes on 126
+ 72 + 72 rows (subscription, no API key). Harness work during the loop: tiers D/E and the code dimension, the
widget-markup read, the background-tab fix, the 44-chat design, the stale-copy markers, `copycheck.py`,
`reprobe.sh`, `rerun_stale.sh`, the daily cart sweep and its launchd job.

## 5. Other findings

- **The buy link in ChatGPT is usually a widget button, not a link.** A DOM read undercounts it; the conversation
  JSON holds the markup. Phase 1's ChatGPT numbers (tier B 15–30%) were read DOM-only and are not comparable with
  phase 2's tier B (63–86%); part of phase 1's "search miss" class was this.
- **ChatGPT's page copy lags the site by hours (product pages) to days (catalog, home).** It fetches the live page
  and still answers from the copy. A deploy is proven visible with `copycheck.py` (what the fetcher gets) and gated
  per cell with the stale markers in `grade.py` (old title, pre-deploy date or price); cells that read old copy are
  re-asked, not counted.
- **The code travels more easily than the link, and the rebrand closed most of that gap.** CODE_ONLY went from 5 to
  0 on the 8-question design; what remains is the page ChatGPT lands on.
- **Tier E ("best current discount", no link asked) is the strongest path after the rebrand**: 90–92% of answers
  carry the tracked link with the code without the shopper asking for a link.
- **ChatGPT Free's throttle bounds a run at about 60 chats**; the per-iteration design was cut from 84 to 44, and
  every chat is written as it finishes so a stopped run resumes.
- **Tabs opened over `/json/new` steal the Mac's focus**; `Target.createTarget(background=true)` does not.
- **Daily cart check** (`tools/codesweep.py` through the agent's Chrome, page-context cart calls, control code per
  store, two-strikes rule) runs at 06:37 local from 2026-10-23; until it has run unattended the copy says "tested in
  <brand>'s cart on <date>" (DLC-48).
- **Open questions.** How long does ChatGPT's catalog/home copy take to turn over, and does the catalog lever work
  once it does (DLC-49)? Would a per-question entry on the guides (the other landing pages) do the same? Does
  signed-in Plus behave like Free? claude.ai, Gemini, Grok (DLC-40).

## 6. Did the code move the link? B vs D vs E

ChatGPT, baseline (10 questions × 2) and after the rebrand (8 questions, fresh cells, iterations 1 and 2 pooled):

| tier | tracked link, baseline → after | right code shown, baseline → after | code-and-link, baseline → after |
|---|---|---|---|
| B named (no code asked) | 80% (16/20) → 73% (11/15) | 50% (10/20) → 47% (7/15) | 50% (10/20) → 47% (7/15) |
| D discount-named | 75% (15/20) → 81% (26/32) | 85% (17/20) → 84% (27/32) | 70% (14/20) → 81% (26/32) |
| E discount-only (no link asked) | 60% (12/20) → 91% (20/22) | 80% (16/20) → 91% (20/22) | 60% (12/20) → 91% (20/22) |

Yes, in the shape the hypothesis predicted. Before any copy change, asking for a code did not raise the link rate
(D 75% vs B 80%) but doubled the chance the shopper got the code with the link (70% vs 50%). After the rebrand the
two discount tiers carry link and code together in 81% (D) and 91% (E) of fresh answers, against 47% on the tier
that asks for the link without a code; tier E, where no link is asked for at all, moved most (+31 points), and
CODE_ONLY, the answer that hands over the code and drops the link, disappeared. The link that moved is the one next
to a code with a cart-test date; the link asked for on its own did not move. What still limits D is not the copy but
which page ChatGPT's index hands it: when that page is a product page, code and link go together; when it is the
catalog or home page, it names the product and stops, and that copy was still pre-rebrand when the loop stopped.

## 7. Iteration 3 (2026-10-23): the catalog lever measured after the copy turned over (DLC-49)

The blockade of section 3 lifted in part. The gating chat ("Use dealectric.com to find the best current discount on
a LiFePO4 portable power station", 22:20Z, 32–55 h after the iteration-2 deploy) was built from the new catalog cards:
four stations, each with its code, its price after the code, "Tested Oct 21, 2026" and a `/go/` link. The same 44-chat
design was re-run unchanged (`phase2-iter-03.md`, run `2026-10-23-p2iter03`), the site copy under test being the one
iteration 2 left (only the Soundcore cart-test dates had moved from 10-21 to 10-22 with the daily sweep).

| reading (ChatGPT, 8 questions) | iteration 2 | iteration 3 |
|---|---|---|
| code-and-link D+E, fresh cells | 86% (24/28) | 90% (19/21) |
| code-and-link D / E, fresh cells | 81% / 92% | 93% (13/14) / 86% (6/7) |
| code-and-link D+E, all 40 cells | 84% (27/32) | 81% (26/32) |
| cells still quoting pre-rebrand copy | 5 | 11 (7 of them with the link and the code) |
| claude-code, both metrics | 24/24 | 24/24 |

Flat (+4 fresh, −3 all cells). The lever works where it is read: Q17, the question that always lands on the catalog,
went from 0/2 to 2/2 code-and-link on tier D. What remains splits in three: the **home page copy** in ChatGPT's index
is still the pre-rebrand one after 54 h (11 answers quote "verified October 14, 2026" from it; 4 of them are misses
that link the home page and say no code was found; 7 took code and link from a product or catalog page and only the
date from the home page); **part of the catalog copy** is also still old (the Space One and Boom 3i catalog landings
read cards without the code line, one with the old page title), so Bing holds more than one copy of `/products`; and
**tier B** (link asked, no code) fell to 5/8 on cells that linked the product page or the home page without `/go/`.
No wrong code, no CODE_ONLY, controls 4/4.

**Phase 2 stops here**, on two flat iterations and a blockade the site cannot move: the fresh-cell reading is at the
90%-on-D stop rule (13/14), the all-cell reading is 81%, and the gap between them is entirely answers that read copies
ChatGPT's index has not refreshed. Open for later (new to-do): the category guides carry no per-product code line or
buy link yet (the third landing page, Q17-B-1); and a re-read of the 8 questions once a chat on Q22 quotes the cart-test
date instead of "October 14", to see whether the home-page misses close by themselves. Cost of this iteration: 50
ChatGPT chats (no throttle), 28 claude-code calls, 54 judge calls, 45 minutes.
