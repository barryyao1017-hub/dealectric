# Iteration comparison — 1 (2026-10-22-p2iter01) → 2 (2026-10-22-p2iter02)

- 1: Stamp: iteration 1 · site commit `500482cbb8` · Worker `cbac9dcc-08ec-4399-86e1-66d4dafb6b45` deployed 2026-10-21T19:50:00.449Z · GSC indexed – · Bing indexed –.
- 2: Stamp: iteration 2 · site commit `f2d3b84fa3` · Worker `cbac9dcc-08ec-4399-86e1-66d4dafb6b45` deployed 2026-10-21T19:50:00.449Z · GSC indexed – · Bing indexed –.

## Tracked-link rate, L4-api (tiers B+D+E, Wilson 95%)

| assistant | iteration 1 | iteration 2 | delta (points) |
|---|---|---|---|
| chatgpt | 80% [65–90] (32/40) | 85% [71–93] (34/40) | +5.0 |
| claude-code | 100% [86–100] (24/24) | 100% [86–100] (24/24) | +0.0 |
| **pooled** | 88% [77–94] (56/64) | 91% [81–96] (58/64) | **+3.1** |
| tier B (pooled) | 81% [57–93] (13/16) | 94% [72–99] (15/16) | +12.5 |
| tier D (pooled) | 88% [69–96] (21/24) | 88% [69–96] (21/24) | +0.0 |
| tier E (pooled) | 92% [74–98] (22/24) | 92% [74–98] (22/24) | +0.0 |

## Code-and-link rate (phase 2: L4 and the right code in one answer)

| reading | iteration 1 | iteration 2 | delta (points) |
|---|---|---|---|
| chatgpt, tiers D+E | 84% [68–93] (27/32) | 84% [68–93] (27/32) | +0.0 |
| claude-code, tiers D+E | 100% [81–100] (16/16) | 100% [81–100] (16/16) | +0.0 |
| pooled, tier B | 62% [39–82] (10/16) | 81% [57–93] (13/16) | +18.8 |
| pooled, tier D | 88% [69–96] (21/24) | 88% [69–96] (21/24) | +0.0 |
| pooled, tier E | 92% [74–98] (22/24) | 92% [74–98] (22/24) | +0.0 |
| right code shown, tier B | 62% [39–82] (10/16) | 81% [57–93] (13/16) | +18.8 |
| right code shown, tier D | 92% [74–98] (22/24) | 88% [69–96] (21/24) | -4.2 |
| right code shown, tier E | 92% [74–98] (22/24) | 92% [74–98] (22/24) | +0.0 |

## Decision rule

flat (+3.1 points, under the 5-point rule): keep the change only if it cost nothing elsewhere

Wilson intervals overlap ([77–94] vs [81–96]); with n=64 and n=64 differences under ~7 points are within noise.

## Failures in iteration 2 (non-L4 answers on tiers B+D+E)

| class | chatgpt | claude-code | all |
|---|---|---|---|
| NOT_FOUND | 1 | 0 | 1 |
| CODE_ONLY | 0 | 0 | 0 |
| PAGE_ONLY | 0 | 0 | 0 |
| MERCHANT_SWAP | 0 | 0 | 0 |
| NETWORK_HOP | 0 | 0 | 0 |
| REFUSED | 0 | 0 | 0 |
| STALE_CACHE | 1 | 0 | 1 |
| OTHER | 4 | 0 | 4 |
| **non-L4 answers (api)** | 6 | 0 | 6 |
| answers carrying a pre-rebrand page copy marker (stale_copy, any level) | 5 | 0 | 5 |
| WRONG_CODE (tiers D+E, any level) | 0 | 0 | 0 |
| NO_CODE (tiers D+E, any level) | 5 | 0 | 5 |
| L4 link without the right code (D+E) | 0 | 0 | 0 |

## LOOP.md row for this iteration (fill in change and decision)

| iteration | date | commit | TLR B / D / E | code-and-link D / E | per-assistant TLR | change made | decision |
|---|---|---|---|---|---|---|---|
| 2.2 | 2026-10-22 | f2d3b84fa3 | 94% (15/16) / 88% (21/24) / 92% (22/24) | 88% (21/24) / 92% (22/24) | chatgpt 85%, claude-code 100% | _change_ | _decision_ |

