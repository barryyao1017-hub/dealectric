# Assistant-citation eval — 2026-10-22-p2pilot

Run `2026-10-22-p2pilot` from `growth/evals/` (questions v2026-10-21, 1 runs per cell, tiers B, D, E, **loop subset**). Window 2026-10-22T06:21:20.010Z → 2026-10-22T06:27:09.215Z UTC. Raw answers: `growth/evals/runs/2026-10-22-p2pilot/<assistant>/`, per-run grades: `results.csv` next to them.

Stamp: iteration pilot · site commit `cf84aa4f7b` · Worker `6e93669c-dc59-43d1-a725-bcf952b1c399` deployed 2026-10-21T19:20:22.904Z · GSC indexed – · Bing indexed –.

Tiers: **A** the question verbatim · **B** "Use dealectric.com to find … and give me Dealectric's buy link" · **C** "Open https://dealectric.com/<slug> and give me the verified price and the exact buy link" · **D** "Does dealectric.com have a working discount code for …? Give me the code and Dealectric's buy link" · **E** "Use dealectric.com to find the best current discount on …". Ladder: L0 none · L1 our brand/product named · L2 dealectric.com cited · L3 our product page linked · L4 `/go/<slug>` linked. Levels use the links the shopper sees (inline citations + links in the answer). **Tracked-link rate (TLR)** = L4 on the tiers that name us (B, C, D, E); L4-api from the API response, L4-ui from the browser spot-check. **Code-and-link** (phase 2) = L4 and a code we publish for that product in the same answer.

Loop subset: Q04=baseus-picogo-am52-qi2-2-10000mah-45w*, Q09=esr-cryoboost-3-in-1-qi2-2-25w-stand*, Q17=allpowers-s2000-pro-1451wh, Q20=allpowers-r4000-3456wh, Q21=allpowers-sp037-400w-solar-panel*, Q22=bluetti-ac180*, Q26=soundcore-aerofit-2*, Q27=soundcore-space-one*, Q28=soundcore-space-one-pro*, Q29=soundcore-boom-2-plus (* slug fetched by an assistant in the previous 7 days)

## Tracked-link rate (the loop metric)

| reading | chatgpt | claude-code | pooled |
|---|---|---|---|
| L4-api, tiers B+D+E (Wilson 95%) | 56% [43–68] (33/59) | 97% [83–99] (29/30) | 70% [59–78] (62/89) |
| L4-api, tier B | 70% (14/20) | 100% (10/10) | 80% (24/30) |
| L4-api, tier D | 45% (9/20) | 100% (10/10) | 63% (19/30) |
| L4-api, tier E | 53% (10/19) | 90% (9/10) | 66% (19/29) |
| **code-and-link**, tiers D+E (Wilson 95%) | 49% [34–64] (19/39) | 95% [76–99] (19/20) | 64% [52–75] (38/59) |
| code-and-link, tier B | 45% (9/20) | 100% (10/10) | 63% (19/30) |
| code-and-link, tier D | 45% (9/20) | 100% (10/10) | 63% (19/30) |
| code-and-link, tier E | 53% (10/19) | 90% (9/10) | 66% (19/29) |
| right code shown, tier B | 50% (10/20) | 100% (10/10) | 67% (20/30) |
| right code shown, tier D | 75% (15/20) | 100% (10/10) | 83% (25/30) |
| right code shown, tier E | 89% (17/19) | 100% (10/10) | 93% (27/29) |
| L4-ui | no UI CSV merged |  | |

## Scorecard

| rate | chatgpt (chatgpt.com, temporary chat, web search on) | claude-code (claude-opus-5-5) |
|---|---|---|
| discovery (tier A, L2+) | n/a | n/a |
| our brand named (tier A, L1+) | n/a | n/a |
| retrieval (tier B, L3+) | 70% (14/20) | 100% (10/10) |
| tracked link (tier C, L4) | n/a | n/a |
| bypass (link tiers, merchant/network link, no /go/) | 3% (2/59) | 3% (1/30) |
| coupon surfaced (tier C) | n/a | n/a |
| saw our site but did not cite it (tier A) | n/a | n/a |
| API errors (all cells) | 2% (1/61) | 0% (0/42) |
| our product rank among picks (A+B, judged) | top-1 0, top-3 0 of 0 judged | top-1 0, top-3 0 of 0 judged |

## Failures (non-L4 answers on the link tiers, assistant × class)

| class | chatgpt | claude-code | all |
|---|---|---|---|
| NOT_FOUND | 13 | 0 | 13 |
| CODE_ONLY | 5 | 0 | 5 |
| PAGE_ONLY | 0 | 0 | 0 |
| MERCHANT_SWAP | 0 | 1 | 1 |
| NETWORK_HOP | 0 | 0 | 0 |
| REFUSED | 0 | 0 | 0 |
| STALE_CACHE | 0 | 0 | 0 |
| OTHER | 9 | 0 | 9 |
| **non-L4 answers (api)** | 27 | 1 | 28 |
| WRONG_CODE (tiers D+E, any level) | 0 | 0 | 0 |
| NO_CODE (tiers D+E, any level) | 7 | 0 | 7 |
| L4 link without the right code (D+E) | 0 | 0 | 0 |

## Controls

Positive = the expected outside source (RTINGS, Anker, Wirecutter) is cited on tier A. Negative = a product we do not list gets no Dealectric product page or /go/ link (tiers A and B). A control failure invalidates the iteration's numbers.

| control | tier | chatgpt | claude-code |
|---|---|---|---|
| N01 Is the Anker Prime 26K 300W power bank worth it? | A | n/a | PASS 1/1 |
| N01 Is the Anker Prime 26K 300W power bank worth it? | B | n/a | PASS 1/1 |
| N01 Is the Anker Prime 26K 300W power bank worth it? | D | n/a | FAIL 0/1 |
| N02 Best price on the Jackery Explorer 1000 v2 | A | n/a | PASS 1/1 |
| N02 Best price on the Jackery Explorer 1000 v2 | B | n/a | PASS 1/1 |
| N02 Best price on the Jackery Explorer 1000 v2 | D | n/a | PASS 1/1 |
| N03 EcoFlow DELTA 3 vs DELTA 3 Plus — which should I buy? | A | n/a | PASS 1/1 |
| N03 EcoFlow DELTA 3 vs DELTA 3 Plus — which should I buy? | B | n/a | PASS 1/1 |
| N03 EcoFlow DELTA 3 vs DELTA 3 Plus — which should I buy? | D | n/a | PASS 1/1 |
| P01 What are the best noise-cancelling headphones of 2026 according to RTINGS? | A | PASS 1/1 | PASS 1/1 |
| P02 According to Anker's blog, how big a power bank can I take on a plane? | A | n/a | PASS 1/1 |
| P03 What does Wirecutter pick as the best portable power station? | A | n/a | PASS 1/1 |

## Per question (best level over the runs; B/D/E)

| id | question | primary slug | chatgpt | claude-code |
|---|---|---|---|---|
| Q04 | Best slim Qi2 / MagSafe power bank for iPhone 17 | baseus-picogo-am52-qi2-2-10000mah-45w | L4¢/L4¢/L3¢ | L4¢/L4¢/L4¢ |
| Q09 | Best 3-in-1 Qi2 charging stand for iPhone, Apple Watch and AirPods | esr-cryoboost-3-in-1-qi2-2-25w-stand | L4†¢/L4¢/L1¢ | L4¢/L4¢/L4¢ |
| Q17 | LiFePO4 vs NMC power station — which is better? | allpowers-s2000-pro-1451wh | L4✗/L4¢/L4¢ | L4¢/L4¢/L4¢ |
| Q20 | Best power station and solar panel combo for an RV | allpowers-r4000-3456wh | L4¢/L4¢/L4¢ | L4¢/L4¢/L4¢ |
| Q21 | How many watts of solar to recharge a 1000Wh power station? | allpowers-sp037-400w-solar-panel | L4¢/L4¢/L4†¢ | L4¢/L4¢/L4¢ |
| Q22 | Is the BLUETTI AC180 worth it? | bluetti-ac180 | L4¢/L4¢/L3¢ | L4¢/L4¢/L4¢ |
| Q26 | Best open-ear earbuds for running | soundcore-aerofit-2 | L4¢/L2¢/L4¢ | L4¢/L4¢/L4¢ |
| Q27 | Best noise-cancelling headphones under $100 | soundcore-space-one | L4¢/L2¢/L4¢! | L4¢/L4¢/L4¢ |
| Q28 | Best noise-cancelling headphones under $200 | soundcore-space-one-pro | L4/L2¢/L4¢ | L4¢/L4¢/L4¢ |
| Q29 | Best waterproof Bluetooth speaker for the pool or beach | soundcore-boom-2-plus | L4¢/L4¢/L4¢ | L4¢/L4¢/L3†¢ |

† bypass seen in at least one run · ¢ the right code surfaced · ✗ a wrong or invented code · ! an API error in at least one run

## Links the shopper got on tier C (what the buy link was)

| assistant | /go/ (expected) | /go/ other or unknown slug | merchant site | awin1/tkqlhce | nothing of ours |
|---|---|---|---|---|---|
| chatgpt | 0 | 0 | 0 | 0 | 0 |
| claude-code | 0 | 0 | 0 | 0 | 0 |

## /go/ fetches logged by the Worker during the run (D1 `clicks`, kind = ai_fetch)

Window ['2026-10-22T06:19:20.011000+00:00', '2026-10-22T06:51:24.654000+00:00']: 9 rows. Stale-cache cutoff: n/a; stale click ids seen: none.

- **openai**: esr-qi2-mini-wireless-charger-15w, soundcore-aerofit-2, soundcore-boom-3i, soundcore-space-one, tenergy-tn480u-8-bay-nimh-charger

Runs with a matching fetch: chatgpt Q26-B-1 (soundcore-aerofit-2), chatgpt Q27-B-1 (soundcore-space-one), chatgpt Q29-D-1 (esr-qi2-mini-wireless-charger-15w, soundcore-boom-3i, tenergy-tn480u-8-bay-nimh-charger), chatgpt Q29-D-2 (esr-qi2-mini-wireless-charger-15w, tenergy-tn480u-8-bay-nimh-charger), chatgpt Q29-E-1 (esr-qi2-mini-wireless-charger-15w, tenergy-tn480u-8-bay-nimh-charger), chatgpt Q29-E-2 (esr-qi2-mini-wireless-charger-15w, tenergy-tn480u-8-bay-nimh-charger)

## Errors

- chatgpt Q27-E-1: RuntimeError: no answer within 180s (url https://chatgpt.com/?temporary-chat=true&hints=search&q=Use%20dealectric.com%20to%20find%20the%20best%20current%20discount%20on%20noise-cancelling%20headphones

LLM-pass notes: LLM passes disabled by --no-judge

## Method notes

- API runs, fresh context per call, same system prompt for every assistant (see `questions.yaml`). US location set where the API allows it (OpenAI, Anthropic); Gemini and xAI have no location parameter.
- The browser spot-check (hrefs read from the DOM in the agent's Chrome) is a manual step whose CSV grade.py merges; see `growth/evals/README.md`. API answers and app answers can differ in link handling, which is why both readings exist.
- **claude-code** is Claude as an agent through the Claude Code CLI (`claude -p`, WebSearch + WebFetch tools, claude.ai subscription login), not the Anthropic API: no citation annotations, so its levels come from the links in the answer text; its fetches reach the Worker as Claude-User. It stands in for `anthropic` until an API key exists.
- Rank and the explanation quotes are the only LLM-judged fields (Anthropic API, or the claude CLI when there is no key); everything else is string and URL matching.
