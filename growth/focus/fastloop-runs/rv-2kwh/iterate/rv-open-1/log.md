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

