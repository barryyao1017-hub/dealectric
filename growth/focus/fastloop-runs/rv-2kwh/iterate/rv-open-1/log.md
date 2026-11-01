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
