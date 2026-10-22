# Iteration comparison — 0 (2026-10-22-p2iter00) → 1 (2026-10-22-p2iter01)

- 0: Stamp: iteration 0 · site commit `f75e90b4da` · Worker `6e93669c-dc59-43d1-a725-bcf952b1c399` deployed 2026-10-21T19:20:22.904Z · GSC indexed – · Bing indexed –.
- 1: Stamp: iteration 1 · site commit `500482cbb8` · Worker `cbac9dcc-08ec-4399-86e1-66d4dafb6b45` deployed 2026-10-21T19:50:00.449Z · GSC indexed – · Bing indexed –.

## Tracked-link rate, L4-api (tiers B+D+E, Wilson 95%)

| assistant | iteration 0 | iteration 1 | delta (points) |
|---|---|---|---|
| chatgpt | 73% [59–83] (35/48) | 80% [65–90] (32/40) | +7.1 |
| claude-code | 96% [80–99] (23/24) | 100% [86–100] (24/24) | +4.2 |
| **pooled** | 81% [70–88] (58/72) | 88% [77–94] (56/64) | **+6.9** |
| tier B (pooled) | 83% [64–93] (20/24) | 81% [57–93] (13/16) | -2.1 |
| tier D (pooled) | 88% [69–96] (21/24) | 88% [69–96] (21/24) | +0.0 |
| tier E (pooled) | 71% [51–85] (17/24) | 92% [74–98] (22/24) | +20.8 |

## Code-and-link rate (phase 2: L4 and the right code in one answer)

| reading | iteration 0 | iteration 1 | delta (points) |
|---|---|---|---|
| chatgpt, tiers D+E | 69% [51–82] (22/32) | 84% [68–93] (27/32) | +15.6 |
| claude-code, tiers D+E | 94% [72–99] (15/16) | 100% [81–100] (16/16) | +6.2 |
| pooled, tier B | 67% [47–82] (16/24) | 62% [39–82] (10/16) | -4.2 |
| pooled, tier D | 83% [64–93] (20/24) | 88% [69–96] (21/24) | +4.2 |
| pooled, tier E | 71% [51–85] (17/24) | 92% [74–98] (22/24) | +20.8 |
| right code shown, tier B | 67% [47–82] (16/24) | 62% [39–82] (10/16) | -4.2 |
| right code shown, tier D | 88% [69–96] (21/24) | 92% [74–98] (22/24) | +4.2 |
| right code shown, tier E | 88% [69–96] (21/24) | 92% [74–98] (22/24) | +4.2 |

## Decision rule

**improvement**: pooled L4-api +6.9 points (≥ 5), no UI reading to check against

Wilson intervals overlap ([70–88] vs [77–94]); with n=72 and n=64 differences under ~8 points are within noise.

## Failures in iteration 1 (non-L4 answers on tiers B+D+E)

| class | chatgpt | claude-code | all |
|---|---|---|---|
| NOT_FOUND | 2 | 0 | 2 |
| CODE_ONLY | 1 | 0 | 1 |
| PAGE_ONLY | 0 | 0 | 0 |
| MERCHANT_SWAP | 1 | 0 | 1 |
| NETWORK_HOP | 0 | 0 | 0 |
| REFUSED | 0 | 0 | 0 |
| STALE_CACHE | 1 | 0 | 1 |
| OTHER | 3 | 0 | 3 |
| **non-L4 answers (api)** | 8 | 0 | 8 |
| answers carrying a pre-rebrand page copy marker (stale_copy, any level) | 6 | 0 | 6 |
| WRONG_CODE (tiers D+E, any level) | 0 | 0 | 0 |
| NO_CODE (tiers D+E, any level) | 4 | 0 | 4 |
| L4 link without the right code (D+E) | 0 | 0 | 0 |

In the assistants' own words:

- **chatgpt · CODE_ONLY** (Q09-D-2): “The link leads to ESR's official US store through Dealectric's tracked buying link.”
- **chatgpt · OTHER** (Q17-B-1): “Note: The link above opens Dealectric's website; I couldn't verify the T320's exact product-specific tracked buy URL from the available results.”
- **chatgpt · OTHER** (Q29-D-1): “Dealectric says its offers are verified, but discounts can change. Its product catalog is the safest starting point to check for an updated offer. Dealectric's links may be affiliate links, meaning it can earn a commission at no extra cost to you.”

## LOOP.md row for this iteration (fill in change and decision)

| iteration | date | commit | TLR B / D / E | code-and-link D / E | per-assistant TLR | change made | decision |
|---|---|---|---|---|---|---|---|
| 2.1 | 2026-10-22 | 500482cbb8 | 81% (13/16) / 88% (21/24) / 92% (22/24) | 88% (21/24) / 92% (22/24) | chatgpt 80%, claude-code 100% | _change_ | _decision_ |

