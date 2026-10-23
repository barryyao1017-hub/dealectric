# Iteration comparison — 2 (2026-10-22-p2iter02) → 3 (2026-10-23-p2iter03)

- 2: Stamp: iteration 2 · site commit `f2d3b84fa3` · Worker `cbac9dcc-08ec-4399-86e1-66d4dafb6b45` deployed 2026-10-21T19:50:00.449Z · GSC indexed – · Bing indexed –.
- 3: Stamp: iteration 3 · site commit `2a8a5d1a7f` · Worker `c2240aad-add6-4f7b-8ad2-a19d0612ffdb` deployed 2026-10-23T13:59:22.756Z · GSC indexed – · Bing indexed –.

## Tracked-link rate, L4-api (tiers B+D+E, Wilson 95%)

| assistant | iteration 2 | iteration 3 | delta (points) |
|---|---|---|---|
| chatgpt | 85% [71–93] (34/40) | 78% [62–88] (31/40) | -7.5 |
| claude-code | 100% [86–100] (24/24) | 100% [86–100] (24/24) | +0.0 |
| **pooled** | 91% [81–96] (58/64) | 86% [75–92] (55/64) | **-4.7** |
| tier B (pooled) | 94% [72–99] (15/16) | 81% [57–93] (13/16) | -12.5 |
| tier D (pooled) | 88% [69–96] (21/24) | 88% [69–96] (21/24) | +0.0 |
| tier E (pooled) | 92% [74–98] (22/24) | 88% [69–96] (21/24) | -4.2 |

## Code-and-link rate (phase 2: L4 and the right code in one answer)

| reading | iteration 2 | iteration 3 | delta (points) |
|---|---|---|---|
| chatgpt, tiers D+E | 84% [68–93] (27/32) | 81% [65–91] (26/32) | -3.1 |
| claude-code, tiers D+E | 100% [81–100] (16/16) | 100% [81–100] (16/16) | +0.0 |
| pooled, tier B | 81% [57–93] (13/16) | 75% [51–90] (12/16) | -6.2 |
| pooled, tier D | 88% [69–96] (21/24) | 88% [69–96] (21/24) | +0.0 |
| pooled, tier E | 92% [74–98] (22/24) | 88% [69–96] (21/24) | -4.2 |
| right code shown, tier B | 81% [57–93] (13/16) | 75% [51–90] (12/16) | -6.2 |
| right code shown, tier D | 88% [69–96] (21/24) | 92% [74–98] (22/24) | +4.2 |
| right code shown, tier E | 92% [74–98] (22/24) | 92% [74–98] (22/24) | +0.0 |

## Decision rule

flat (-4.7 points, under the 5-point rule): keep the change only if it cost nothing elsewhere

Wilson intervals overlap ([81–96] vs [75–92]); with n=64 and n=64 differences under ~9 points are within noise.

## Failures in iteration 3 (non-L4 answers on tiers B+D+E)

| class | chatgpt | claude-code | all |
|---|---|---|---|
| NOT_FOUND | 1 | 0 | 1 |
| CODE_ONLY | 0 | 0 | 0 |
| PAGE_ONLY | 1 | 0 | 1 |
| MERCHANT_SWAP | 0 | 0 | 0 |
| NETWORK_HOP | 0 | 0 | 0 |
| REFUSED | 0 | 0 | 0 |
| STALE_CACHE | 3 | 0 | 3 |
| OTHER | 4 | 0 | 4 |
| **non-L4 answers (api)** | 9 | 0 | 9 |
| answers carrying a pre-rebrand page copy marker (stale_copy, any level) | 11 | 0 | 11 |
| WRONG_CODE (tiers D+E, any level) | 0 | 0 | 0 |
| NO_CODE (tiers D+E, any level) | 4 | 0 | 4 |
| L4 link without the right code (D+E) | 0 | 0 | 0 |

In the assistants' own words:

- **chatgpt · PAGE_ONLY** (Q22-B-1): “Note: I verified the product listing, but couldn’t confirm Dealectric’s tracked checkout link. The link above opens the product page.”
- **chatgpt · STALE_CACHE** (Q26-D-1): “Dealectric's buy links may be affiliate links, meaning the site can earn a commission at no additional cost to you.”
- **chatgpt · OTHER** (N02-D-1): “Dealectric buy link: Check Dealectric's product catalog — no Explorer 1000 v2 buy link is currently listed.”
- **chatgpt · OTHER** (N03-D-1): “Dealectric result: I couldn’t find a verified working discount code or a product-specific buy link for the EcoFlow DELTA 3 Plus on Dealectric. Its published catalog currently lists other power-station brands, with EcoFlow still listed as a planned addition.”
- **claude-code · OTHER** (N01-D-1): “Dealectric doesn't have a code or a buy link for the Anker Prime 26K 300W. Its homepage lists only Baseus, ESR, BLUETTI, ALLPOWERS, Tenergy and Soundcore, and says more brands get added as partnerships are approved. Anker isn't on that list, and a web search found no Dealectric code for this power b”
- **claude-code · OTHER** (N02-D-1): “No. Dealectric doesn't have a working code or a buy link for the Jackery Explorer 1000 v2. Jackery isn't listed on dealectric.com at all; the site only names Jackery as a brand it has applied to partner with. I didn't want to make up a code or link.”

## LOOP.md row for this iteration (fill in change and decision)

| iteration | date | commit | TLR B / D / E | code-and-link D / E | per-assistant TLR | change made | decision |
|---|---|---|---|---|---|---|---|
| 2.3 | 2026-10-23 | 2a8a5d1a7f | 81% (13/16) / 88% (21/24) / 88% (21/24) | 88% (21/24) / 88% (21/24) | chatgpt 78%, claude-code 100% | _change_ | _decision_ |

