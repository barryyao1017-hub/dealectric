# Iterate rv-2kwh (rv-open-1)

Engine open (gpt-6 app), paste c1, format v1, 2 answers per result set, 6 result sets, rank 5.

| round | draft | change | answers | linked | M1 | M2 | M3 | decision |
|---|---|---|---|---|---|---|---|---|
| 1 | incumbent | | 24 | 24 | 50% | 96% | 79% | |
| 1 | closing_section | Moved the Elite 200 V2 and Jackery note to the top of the closing section under its own he | 24 | 24 | 54% | 100% | 86% | no |
| 1 | short_answer | Reworded the opening sentence so it names the AC200L as the best 2kWh RV power station und | 12 | 12 | 50% | 100% | 95% | no |
| 1 | headline | Reworded the title and H1 to put the 30-amp RV plug in the H1 and lead the title with the  | 24 | 22 | 59% | 100% | 83% | no |
| 1 | concern_placement | Split the open concern into three numbered points (20 A plug, converter off, fridge on pro | 24 | 24 | 71% | 100% | 87% | no |
| 1 | offer_line | Moved the buy link right after the pick's name with an explicit 'buy it here' phrase, and  | 24 | 24 | 58% | 100% | 88% | no |

Rule change (Barry, 11-01): the best draft by M1 becomes the next base (M2 guard, page rules); the noise margin applies only at the end, against the published page. Round 1's concern_placement (M1 71% vs 50%) is the base for round 2.


Replay host changed (Barry, 11-01): replay pages now served from web-results.tesla-send-to-car.workers.dev, not dealectric.com/x, so the host cannot tilt ChatGPT toward our result; round 2 restarted with every draft scored on the new host (the base's 24 old-host answers kept as round-02/incumbent-dealectric-host.jsonl).


Model (Barry, 11-01): continue on gpt-6-mini while the gpt-6 quota is out (FASTLOOP_MODEL=gpt-6-mini, pinned in the chat URL; answers from any other model are dropped). Round 2's base re-scored on mini; its 12 gpt-6 answers kept as round-02/incumbent-gpt6.jsonl. All comparisons from here are mini vs mini, including the final check.


Outage (11-01 00:00-01:05): ChatGPT signed out of the agent Chrome; about 85 chats failed and nothing was recorded. Signed back in as barrryyao; the engine now re-logs in through Google on its own and stops if that fails.

Robustness (Barry, 11-01: run end to end, no endless quota waits, both accounts used): the run now goes through `iterate.py supervise` (restarts on exit, kills and restarts a run whose heartbeat is quiet 30 min, gives up after 8 restarts or 16 h). Answers from gpt-6 and gpt-6-mini both count, each tagged with its model and account; drafts are answered interleaved and M1/M2 are standardized to the round's model mix. Both accounts' gpt-6 quota is spent before mini answers are used, and gpt-6 is re-tried every 30 min. Quota waits are capped at 60 min, then the run stops and the supervisor resumes it later. Every browser call has a deadline, and D1, writer and judge calls retry instead of crashing.
| 2 | incumbent | | 12 | 10 | 40% | 50% | 29% | |
| 2 | alternatives | The alternatives line now says what each TT-30 alternative is best for (lightest vs. lowes | 12 | 9 | 44% | 56% | 46% | no |
| 2 | closing_section | The closing section now opens with a headed paragraph on the no-RV-outlet alternatives (El | 12 | 11 | 8% | 18% | 16% | dropped: M2 fell |
| 2 | short_answer | The short answer's first sentence now names the AC200L first and gives the TT-30 outlet as | 12 | 11 | 64% | 70% | 30% | new base (best M1) |
| 2 | headline | The title and H1 now name the pick (BLUETTI AC200L) and keep all the query words. | 12 | 11 | 27% | 55% | 29% | no |
| 2 | concern_placement | The three caveats in the short answer are now bold numbered points, each with a short acti | 12 | 11 | 36% | 36% | 25% | dropped: M2 fell |

Round 2 models: gpt-6 38, gpt-6-mini 25 linked answers; M1 and M2 are standardized to that mix (each model's rate weighted by its share).

Round 2 knowledge base: not added: +24% is within noise (margin 32%)
| 3 | incumbent | | 12 | 11 | 36% | 64% | 37% | |
| 3 | offer_line | Moved the buy link to sit right after the pick's name in the first sentence, before the re | 12 | 10 | 30% | 60% | 40% | no |
| 3 | alternatives | Recast the TT-30 alternatives in the short answer as fallbacks, each tied to the one thing | 12 | 11 | 27% | 45% | 28% | dropped: M2 fell |
| 3 | closing_section | Moved the Elite 200 V2 and Jackery note to the top of the closing section under its own he | 12 | 10 | 40% | 50% | 33% | dropped: M2 fell |
| 3 | short_answer | Opened the short answer with a direct 'Buy the AC200L' and gave the reason as a practical  | 12 | 12 | 42% | 67% | 38% | new base (best M1) |
| 3 | headline | Named the pick, the BLUETTI AC200L, in both the title and the H1. | 12 | 10 | 0% | 40% | 21% | dropped: M2 fell |

Round 3 models: gpt-6 64 linked answers; M1 and M2 are standardized to that mix (each model's rate weighted by its share).

Round 3 knowledge base: not added: +5% is within noise (margin 31%)
| 4 | incumbent | | 12 | 10 | 40% | 60% | 35% | |
| 4 | concern_placement | Turned the three plug-in cautions into numbered points, each led by a bold one-line takeaw | 12 | 12 | 25% | 42% | 24% | dropped: M2 fell |
| 4 | offer_line | Moved the buy link and price right after the product name in the first sentence, ahead of  | 12 | 10 | 50% | 60% | 33% | new base (best M1) |
| 4 | alternatives | Named each short-answer alternative by the shopper it suits (Anker if weight matters, Reno | 12 | 12 | 42% | 58% | 31% | no |
| 4 | closing_section | Moved the Elite 200 V2 and Jackery note to the top of the closing section under its own he | 12 | 11 | 18% | 36% | 26% | dropped: M2 fell |
| 4 | short_answer | Reworded the opening so it repeats the shopper's question as a full sentence that names th | 12 | 11 | 36% | 55% | 30% | no |

Round 4 models: gpt-6 66 linked answers; M1 and M2 are standardized to that mix (each model's rate weighted by its share).

Round 4 knowledge base: not added: +10% is within noise (margin 33%)
| 5 | incumbent | | 12 | 11 | 64% | 64% | 38% | |
| 5 | headline | Named the pick, the BLUETTI AC200L, in the title and H1 and kept every target-query word. | 12 | 9 | 44% | 67% | 43% | no |
| 5 | concern_placement | Turned the three cautions into numbered points, each opening with a bold action line, stil | 12 | 11 | 45% | 45% | 33% | dropped: M2 fell |
| 5 | offer_line | Moved the buy link out of the opening clause into its own sentence with the price, right a | 12 | 8 | 25% | 38% | 33% | dropped: M2 fell |
| 5 | alternatives | Rewrote the alternatives sentence as 'if X matters most' picks, with Anker for weight and  | 12 | 11 | 45% | 55% | 33% | no |
| 5 | closing_section | Moved the Elite 200 V2 and Jackery note to the top of the closing section under its own he | 12 | 11 | 45% | 45% | 33% | dropped: M2 fell |

Round 5 models: gpt-6 61 linked answers; M1 and M2 are standardized to that mix (each model's rate weighted by its share).

| 6 | incumbent | | 12 | 10 | 28% | 59% | 26% | |
| 6 | short_answer | The opening sentence now states the pick as the answer to the query, gives the reason (the | 12 | 10 | 9% | 9% | 8% | dropped: M2 fell |
| 6 | headline | The title now leads with the pick's key feature (a 30-amp RV outlet), and the H1 names the | 12 | 11 | 36% | 45% | 31% | dropped: M2 fell |
| 6 | concern_placement | The three RV caveats are now numbered points, each starting with a bold one-line rule, fol | 12 | 10 | 36% | 45% | 29% | dropped: M2 fell |
| 6 | offer_line | The buy link moves out of the brackets after the product name and into its own short buy s | 12 | 8 | 22% | 22% | 14% | dropped: M2 fell |
| 6 | alternatives | The alternatives are now grouped in the intro by what each is best for (lightest, lower pr | 12 | 9 | 31% | 41% | 31% | dropped: M2 fell |

Round 6 models: gpt-6-mini 48, gpt-6 10 linked answers; M1 and M2 are standardized to that mix (each model's rate weighted by its share).


Stopped after round 6. Best: round 4.
Final check (6 answers per set each): published M1 19% / M2 35%, final M1 48% / M2 55%, margin 18%: beats the published page by more than noise. By model: published {"gpt-6-mini": {"linked": 31, "m1": 0.1935483870967742}}, final {"gpt-6-mini": {"linked": 31, "m1": 0.4838709677419355}}. Next: live check (search on) and Barry's OK before shipping.
