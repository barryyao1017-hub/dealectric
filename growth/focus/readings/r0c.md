# W3 reading R0c, baseline for arm F (2026-10-29)

Run: `growth/evals/runs/2026-10-29-w3-r0c/` (W1's driver, signed in, temporary chats; 14 cells, all gpt-6: 10 reused from
W1's 10-28 scan, 4 new; kit worth-2 was a gpt-6-mini answer the scan had counted as gpt-6, re-asked). Scored with
`python3.12 growth/evals/w3score.py growth/evals/runs/2026-10-29-w3-r0c --baseline`, which since 2026-10-29 drops any
answer not from gpt-6 by itself (a chat routed to mini from the start carries no resolved model slug). R0 and R0b
re-scored under that check: unchanged. Every cell read the 10-26 index copy; c7ee97b's fact fixes aren't in it.

| | T5 | T4+ | T4 on the product page | Flags |
|---|---|---|---|---|
| Arm F test (kit) | 1/8 | 5/8 | 5/8 | 0 |
| Arm F controls (P1800 kit, ESR HaloLock) | 1/4 | 3/4 | 3/4 | 1 |
| Positive control (ESR Qi2 Mini) | 2/2 | 2/2 | n/a | 0 |

- The kit's T5 (deal-1, reused from the scan) had the home page and `/discount-codes` in its results next to the kit
  and station pages, as every T5 so far had a list page; its button went to `/go/allpowers-s2000-pro-1451wh`, the
  station, not the kit.
- Both "best solar generator with panels included under $1000" cells are T1.
- Flag on a control: `allpowers-p1800-sp037-solar-kit--deal-2` says "the listed warranty and return terms deserve a look
  before buying", pointing at our page's two-year warranty line. Same mild caution as R0b's P1800 flag (DLC-74).
- The positive control held: ESR Qi2 Mini T5 in 2 of 2 again, one answer noting "the deal page may use an affiliate
  link" (true; recorded as affiliate-noted, not a flag).

## Cells
## allpowers-s2000-pro-sp037-solar-kit
- test, all: T5 1/8, T4+ 5/8, T4 on the product page 5/8, T3+ 5/8, T2+ 6/8
- test, fresh or baseline: T5 1/8, T4+ 5/8, T4 on the product page 5/8, T3+ 5/8, T2+ 6/8
- control: T5 1/4, T4+ 3/4, T4 on the product page 3/4, T3+ 3/4, T2+ 3/4
- freshness: baseline 8, fresh 0, stale 0, undated 0; flags 1; uncalled flag candidates 0

| cell | role | T | go | product page | rank | buy link domains | cart date quoted / live | index copy (OAI fetch) | fresh | flag |
|---|---|---|---|---|---|---|---|---|---|---|
| allpowers-s2000-pro-sp037-solar-kit--best-1 | test | 1 |  |  | -/10 | www.ankersolix.com, www.bestbuy.com, www.bluettipower.com, www.jackery.com | - / 2026-10-28 | v2 (10-26T21:34) | baseline | none |
| allpowers-s2000-pro-sp037-solar-kit--best-2 | test | 1 |  |  | -/10 | us.ecoflow.com, www.anker.com, www.bluettipower.com, www.walmart.com | - / 2026-10-28 | v2 (10-26T21:34) | baseline | none |
| allpowers-s2000-pro-sp037-solar-kit--coupon-1 | test | 4 |  | yes | 3/9 | iallpowers.com | 2026-10-28 / 2026-10-28 | v2 (10-26T21:34) | baseline | none |
| allpowers-s2000-pro-sp037-solar-kit--coupon-2 | test | 4 |  | yes | 1/10 | dealectric.com | 2026-10-28 / 2026-10-28 | v2 (10-26T21:34) | baseline | none |
| allpowers-s2000-pro-sp037-solar-kit--deal-1 | test | 5 | yes | yes | 2/11 | dealectric.com, www.wellbots.com | 2026-10-27, 2026-10-28 / 2026-10-28 | v2 (10-26T21:34) | baseline | none |
| allpowers-s2000-pro-sp037-solar-kit--deal-2 | test | 4 |  | yes | 1/10 | - | 2026-10-28 / 2026-10-28 | v2 (10-26T21:34) | baseline | none |
| allpowers-s2000-pro-sp037-solar-kit--worth-1 | test | 2 |  |  | 16/17 | iallpowers.com | - / 2026-10-27 | v2 (10-26T21:34) | baseline | none |
| allpowers-s2000-pro-sp037-solar-kit--worth-2 | test | 4 |  | yes | 3/19 | iallpowers.com, www.homedepot.com, www.wellbots.com | 2026-10-25 / 2026-10-28 | v2 (10-26T21:34) | baseline | none |
| allpowers-p1800-sp037-solar-kit--deal-1 | control | 4 |  | yes | 3/9 | iallpowers.com | 2026-10-23, 2026-10-25 / 2026-10-28 | v2 (10-26T21:34) | n/a | none |
| allpowers-p1800-sp037-solar-kit--deal-2 | control | 4 |  | yes | 1/9 | iallpowers.com | 2026-10-25, 2026-10-28 / 2026-10-28 | v2 (10-26T21:34) | n/a | questioned |
| esr-halolock-15w-wireless-car-charger-cryoboost--deal-1 | control | 5 | yes |  | 8/16 | dealectric.com, www.esrtech.com | - / 2026-10-27 | v6 (10-26T21:34) | n/a | none |
| esr-halolock-15w-wireless-car-charger-cryoboost--deal-2 | control | 1 |  |  | -/10 | www.amazon.com, www.esrtech.com | 2026-10-22 / 2026-10-28 | v6 (10-26T21:34) | n/a | none |

## positive control (ESR Qi2 Mini, page never changed)
- test, all: T5 -, T4+ -, T4 on the product page -, T3+ -, T2+ -
- test, fresh or baseline: T5 -, T4+ -, T4 on the product page -, T3+ -, T2+ -
- control: T5 2/2, T4+ 2/2, T4 on the product page 2/2, T3+ 2/2, T2+ 2/2
- freshness: baseline 0, fresh 0, stale 0, undated 0; flags 0; uncalled flag candidates 0

| cell | role | T | go | product page | rank | buy link domains | cart date quoted / live | index copy (OAI fetch) | fresh | flag |
|---|---|---|---|---|---|---|---|---|---|---|
| esr-qi2-mini-wireless-charger-15w--deal-1 | positive | 5 | yes |  | 10/17 | dealectric.com, www.esrtech.com | 2026-10-27 / 2026-10-27 | v7 (10-26T21:34) | n/a | affiliate-noted |
| esr-qi2-mini-wireless-charger-15w--deal-2 | positive | 5 | yes |  | 7/12 | dealectric.com, www.esrtech.com | 2026-10-27 / 2026-10-28 | v7 (10-26T21:34) | n/a | none |
