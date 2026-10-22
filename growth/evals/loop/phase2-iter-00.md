# Phase 2, iteration 0 — baseline before the rebrand (2026-10-22)

Report: https://claude.ai/artifact/D9SkG4xfU1mNqNEvd7ENG4 (built by `growth/evals/iterreport.py --iteration 0 --phase 2`; every chat screenshot in its gallery)

The discount-code hypothesis (growth/improvement-loop.md "Phase 2"): does a working code with a fresh cart-test date
next to the link make ChatGPT hand the shopper Dealectric's tracked buy link together with the code? This is the
reading **before** any copy change: the site already lists the codes (DLC-29, 2026-10-21) in the phase-1 voice.

## Design

- App: chatgpt.com, signed in (Barry's Free account), temporary chats, web search on, driven by `growth/evals/ui.py`
  in the agent's Chrome; n = 2 per cell. Regression check: claude-code (`run.py --assistants claude-code`), n = 1.
- Tiers B (named), D (discount-named), E (discount-only) on a frozen subset of 10 of the 19 coded questions,
  primaries rotated to products with a code: Q04 PicoGo AM52 (code AM52), Q09 ESR CryoBoost 3-in-1 (PARTNER18),
  Q17 ALLPOWERS S2000 Pro (ALLPOWERS26/EXTRA10), Q20 ALLPOWERS R4000 (EXTRA12/ALLPOWERS26), Q21 ALLPOWERS SP037
  (ALLPOWERS26), Q22 BLUETTI AC180 (AFF5OFF), Q26 Soundcore AeroFit 2, Q27 Space One, Q28 Space One Pro,
  Q29 Boom 2 Plus (all AFSC20). Controls: P01–P03 on A; N01–N03 on A, B and D (tier D also fails on an invented code).
- Metrics: tracked-link rate per tier; **code-and-link rate** (L4 and a code we publish for that product in one answer),
  the phase-2 metric; right-code rate; failure classes incl. CODE_ONLY and the code dimension (WRONG_CODE / NO_CODE).

## Instrument change made during this iteration (why there are two runs)

The first run (`2026-10-22-p2pilot`, 06:21–07:00Z, 84 chats) read links from the DOM, as in phase 1. Reading its
answers showed ChatGPT now renders shopping answers as its own widget markup (`model_dil_v2`): a product card with a
"Copy code" button and a buy button written as `<button onClick={() => GenUI.openUrl("https://dealectric.com/go/…")}>`.
That button is a plain `<button>` in the DOM, no href anywhere (a 0×0 runner iframe from cdn.platform.openai.com
drives it), so the DOM read scored such answers below L4 although the shopper's click opens the `/go/` link. The URL
is in the assistant message in `GET /backend-api/conversation/<id>`. `ui.py` now captures that JSON over the DevTools
Network domain and adds widget-button and markdown-link URLs to the citations (commit 15543b4); the pilot cannot be
re-read (temporary chats), so the baseline was run again with the corrected instrument as `2026-10-22-p2iter00`.
Phase-1 ChatGPT numbers were read DOM-only and may undercount L4 for the same reason; that is noted for the report.

## Numbers (run `2026-10-22-p2iter00`, 06:19–08:28Z plus the last three controls at 08:26Z; two throttle waits of 19 and 26 min)

ChatGPT signed in (Free), temporary chats, 60 question chats on B+D+E, 24 control chats; claude-code once per cell.
Scorecard: `growth/probes/2026-10-22-p2iter00-eval.md`.

| reading | chatgpt | claude-code |
|---|---|---|
| **TLR tiers B+D+E** | **72% [59–81] (43/60)** | 97% [83–99] (29/30) |
| TLR tier B / D / E | 80% (16/20) / 75% (15/20) / 60% (12/20) | 100% / 100% / 90% |
| **code-and-link, tiers D+E** | **65% [50–78] (26/40)** | 95% (19/20) |
| code-and-link tier B / D / E | 50% / 70% / 60% | 100% / 100% / 90% |
| right code shown, tier B / D / E | 50% / 85% / 80% | 100% / 100% / 100% |
| WRONG_CODE (D+E) | 0 | 0 |
| failures (non-L4): CODE_ONLY / OTHER / PAGE_ONLY / NOT_FOUND / MERCHANT_SWAP | 7 / 8 / 1 / 1 / 0 | 0 / 0 / 0 / 0 / 1 |
| controls | 24/24 | 12/12 |

On the 8 questions that later iterations use (Q04, Q09, Q17, Q21, Q22, Q26, Q27, Q29): chatgpt TLR B 75% (12/16),
D 81% (13/16), E 62% (10/16), pooled 73% (35/48); code-and-link D 75% (12/16), E 62% (10/16), pooled D+E 69%
(22/32); right code shown D 13/16, E 13/16. claude-code: TLR 96% (23/24), code-and-link D+E 94% (15/16).

What the numbers say before any copy change:

- **The code already travels.** On the discount tiers ChatGPT shows the right code in 85% (D) and 80% (E) of
  answers, never a wrong or invented one (0 WRONG_CODE; the tier-D negative controls, asking for a code for a product
  we do not list, passed 6/6: "I couldn't verify a working Dealectric discount code for the Jackery Explorer 1000 v2 …
  its current catalog does not list Jackery").
- **The link travels less than the code.** Code-and-link is 70% on D and 60% on E against 85% and 80% right-code:
  7 CODE_ONLY answers hand the shopper the code with the product page, the catalog page or no link at all ("The link
  opens Dealectric's product catalog; I couldn't verify a dedicated AeroFit 2 checkout link or discount code",
  Q26-D-2). All seven are Soundcore (Q26–Q28) or the AM52/EXTRA10 cases where the code sits on another product's
  page in ChatGPT's search results.
- **Tier B is 80%, not phase 1's 15–30%.** Two reasons, both instrument and index: the coded questions' product pages
  are the ones ChatGPT's search returns most (the 10/21 rebuild and IndexNow pings reached Bing for these), and 11 of
  the 43 ChatGPT L4s exist only in the widget markup (product cards whose Buy button calls `GenUI.openUrl`), which
  phase 1's DOM read scored as L2/L3. The phase-1 ChatGPT tier-B figure is therefore not comparable with this one.
- **ChatGPT quotes our freshness line back**: "verified October 21, 2026", "Dealectric reports that it tested this code
  in BLUETTI's checkout on October 21, 2026", "Code verified Oct 21, 2026" appear in 40 of the 60 answers. Thirteen
  answers quote "verified October 14, 2026", the date on the pages before the 10/21 rebuild: ChatGPT is reading a
  cached copy of those pages a day old or more (Q04-E-2, Q09-E-1/E-2, Q17-D-2/E-1, Q20-E-1, Q21-E-2, Q22-B-1,
  Q26-E-2, Q27-B-2, Q28-B-1/B-2/D-2). The cache-turnover wait after a deploy must be checked against this, not assumed.
- **Display-layer effects**: one bare `/go/allpowers-p1800` link (slug truncated, Q17-B-2, OTHER); ChatGPT fetched
  five `/go/` URLs itself during the run (D1 ai_fetch rows), the others it linked without fetching.
- claude-code: 29/30 L4, 19/20 code-and-link; its one miss links soundcore.com directly (MERCHANT_SWAP, Q29-E-1).

## Decision

Baseline recorded. The phase-2 metric starts at **65% code-and-link on D+E (ChatGPT)**, with the code reaching the
shopper more often (85% / 80%) than the link (75% / 60%). Iteration 1 ships the rebrand (every surface leads with
the code, what it saves, the cart-test date and the buy link, with one canonical paragraph telling the agent to hand
both to the shopper) and the daily cart check. Expected movement, written before the re-evaluation: CODE_ONLY 7 → ≤ 3
and code-and-link on D from 70% toward 85% (the right-code rate), E from 60% toward 75%; tier B unchanged within
noise; no change for claude-code. Per the throttle finding, iterations 1+ run the 44-chat design (8 questions, B
once, D and E twice, lite controls) and compare with this baseline on the same 8 questions.
