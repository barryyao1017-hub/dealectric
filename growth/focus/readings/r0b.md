# W3 reading R0b, baseline for arms C-E (2026-10-28)

Run: `growth/evals/runs/2026-10-28-w3-r0b/` (W1's driver, signed in, temporary chats; 32 cells answered by gpt-6, 11
reused from W1's scan, 2 gpt-6-mini answers re-asked and dropped). Scored with
`python3.12 growth/evals/w3score.py growth/evals/runs/2026-10-28-w3-r0b --baseline`; flag calls in
`readings/flags.json`. Every cell read the copy OAI-SearchBot fetched on 2026-10-26 (index copy column), so neither
df2d809 (fact fixes) nor DLC-76 (60ef1c3) reached these answers.

## Result

| Arm | Test T5 | Test T4+ | T4 on the product page | Controls T5 / T4+ | Flags |
|---|---|---|---|---|---|
| C, ALLPOWERS R4000 | 0/8 | 6/8 | 4/8 | 1/4 / 3/4 | 0 |
| D, ALLPOWERS P1800 | 0/8 | 4/8 | 4/8 | 1/4 / 3/4 | 1 |
| E, ALLPOWERS SP037 | 0/8 | 6/8 | 5/8 | 2/4 / 3/4 | 0 |

- The shared ESR HaloLock control was T5 once and T2 once. The VOLIX P300 kit control (arm E) was T5 once.
- All six "best ... under $X" cells are T1, as in R0.
- **Flag:** `allpowers-p1800-1024wh--deal-2` says "third-party coupon trackers and manufacturer pages sometimes show
  different warranty and return terms". It aims at trackers including us. Our page's 24-month warranty matches
  ALLPOWERS' US warranty page; its returns page says 18 months, which is DLC-74's question. No lever was in force, so
  nothing comes off; it's reported to Barry.

## What separates T5 from T4 (W1's question, from the 7 T5 answers in the scan, R0 and R0b)

- In every T5, ChatGPT presents the price after the code as our finding: "The discount-code tracker Dealectric
  reports that code PARTNER18 was tested ... $16.40", "the best verified deal I found ... through a deal tracker that
  tested the coupon at checkout". The deal is ours, so our link carries it.
- In the ALLPOWERS T4s, ChatGPT leads with "Official ALLPOWERS US store, $1,499" from its shopping results and adds
  our code as a tip. The button goes to the store ("Shop the R4000 at ALLPOWERS") and our page is a source link
  ("Dealectric's R4000 coupon testing").
- OpenAI's product-catalog card isn't the cause: 12 of 114 T4 answers carried an `openai_catalog` link, no T5 did.
- The consistent T5 (ESR Qi2 Mini, 2 of 2) has an 18% partner code only we publish and a $16 product. ALLPOWERS' codes
  are 10-12% sitewide codes.
- For the levers: lead the buy box with the price after the code as the offer (lever 1 does), and a link that applies
  the code itself (lever 2) would make the deal exist only through our link. For ALLPOWERS that needs DLC-53.

## Cells
## allpowers-p1800-1024wh
- test, all: T5 0/8, T4+ 4/8, T4 on the product page 4/8, T3+ 4/8, T2+ 6/8
- test, fresh or baseline: T5 0/8, T4+ 4/8, T4 on the product page 4/8, T3+ 4/8, T2+ 6/8
- control: T5 1/4, T4+ 3/4, T4 on the product page 1/4, T3+ 3/4, T2+ 4/4
- freshness: baseline 8, fresh 0, stale 0, undated 0; flags 0; uncalled flag candidates 10

| cell | role | T | go | product page | rank | buy link domains | cart date quoted / live | index copy (OAI fetch) | fresh | flag |
|---|---|---|---|---|---|---|---|---|---|---|
| allpowers-p1800-1024wh--best-1 | test | 1 |  |  | -/14 | www.bluettipower.com, www.ecoflow.com, www.microcenter.com | - / 2026-10-27 | v7 (10-26T21:35) | baseline | ? |
| allpowers-p1800-1024wh--best-2 | test | 1 |  |  | -/14 | us.ecoflow.com, www.lowes.com, www.microcenter.com | - / 2026-10-28 | v7 (10-26T21:35) | baseline | ? |
| allpowers-p1800-1024wh--coupon-1 | test | 4 |  | yes | 5/19 | - | 2026-10-25 / 2026-10-28 | v7 (10-26T21:35) | baseline | ? |
| allpowers-p1800-1024wh--coupon-2 | test | 2 |  |  | 13/17 | iallpowers.com, www.dealsishere.com, www.dontpayfull.com | - / 2026-10-28 | v7 (10-26T21:35) | baseline | ? |
| allpowers-p1800-1024wh--deal-1 | test | 4 |  | yes | 3/10 | dealectric.com, www.amazon.com | 2026-10-25 / 2026-10-27 | v7 (10-26T21:35) | baseline | ? |
| allpowers-p1800-1024wh--deal-2 | test | 4 |  | yes | 2/10 | - | 2026-10-25 / 2026-10-28 | v7 (10-26T21:35) | baseline | ? |
| allpowers-p1800-1024wh--worth-1 | test | 2 |  |  | 7/8 | iallpowers.com, www.amazon.com, www.bluettipower.com | - / 2026-10-27 | v7 (10-26T21:35) | baseline | ? |
| allpowers-p1800-1024wh--worth-2 | test | 4 |  | yes | 10/17 | iallpowers.com, www.amazon.com, www.walmart.com | - / 2026-10-28 | v7 (10-26T21:35) | baseline | ? |
| allpowers-r600-299wh--deal-1 | control | 4 |  |  | 3/8 | iallpowers.com | 2026-10-27 / 2026-10-27 | v7 (10-26T21:34) | n/a | ? |
| allpowers-r600-299wh--deal-2 | control | 4 |  |  | 3/10 | iallpowers.com | 2026-10-27 / 2026-10-28 | v7 (10-26T21:34) | n/a | ? |
| esr-halolock-15w-wireless-car-charger-cryoboost--deal-1 | control | 5 | yes |  | 8/16 | dealectric.com, www.esrtech.com | - / 2026-10-27 | v6 (10-26T21:34) | n/a | ? |
| esr-halolock-15w-wireless-car-charger-cryoboost--deal-2 | control | 2 |  |  | 6/12 | www.esrtech.com | - / 2026-10-28 | v6 (10-26T21:34) | n/a | ? |

## allpowers-r4000-3456wh
- test, all: T5 0/8, T4+ 6/8, T4 on the product page 4/8, T3+ 6/8, T2+ 6/8
- test, fresh or baseline: T5 0/8, T4+ 6/8, T4 on the product page 4/8, T3+ 6/8, T2+ 6/8
- control: T5 1/4, T4+ 3/4, T4 on the product page 3/4, T3+ 3/4, T2+ 4/4
- freshness: baseline 8, fresh 0, stale 0, undated 0; flags 0; uncalled flag candidates 10

| cell | role | T | go | product page | rank | buy link domains | cart date quoted / live | index copy (OAI fetch) | fresh | flag |
|---|---|---|---|---|---|---|---|---|---|---|
| allpowers-r4000-3456wh--best-1 | test | 1 |  |  | -/12 | us.anker.com, www.bestbuy.com, www.jackery.com | 2026-10-28 / 2026-10-28 | v6 (10-26T21:34) | baseline | ? |
| allpowers-r4000-3456wh--best-2 | test | 1 |  |  | -/15 | us.ecoflow.com, www.bestbuy.com, www.jackery.com | - / 2026-10-28 | v6 (10-26T21:34) | baseline | ? |
| allpowers-r4000-3456wh--coupon-1 | test | 4 |  | yes | 1/14 | - | 2026-10-25 / 2026-10-28 | v6 (10-26T21:34) | baseline | ? |
| allpowers-r4000-3456wh--coupon-2 | test | 4 |  |  | 4/16 | iallpowers.com | 2026-10-25 / 2026-10-28 | v6 (10-26T21:34) | baseline | ? |
| allpowers-r4000-3456wh--deal-1 | test | 4 |  | yes | 1/9 | dealectric.com, iallpowers.com | 2026-10-25 / 2026-10-27 | v6 (10-26T21:34) | baseline | ? |
| allpowers-r4000-3456wh--deal-2 | test | 4 |  | yes | 3/10 | dealectric.com, iallpowers.com | 2026-10-25 / 2026-10-28 | v6 (10-26T21:34) | baseline | ? |
| allpowers-r4000-3456wh--worth-1 | test | 4 |  |  | 16/22 | iallpowers.com, www.wellbots.com | 2026-10-27, 2026-10-28 / 2026-10-27 | v6 (10-26T21:34) | baseline | ? |
| allpowers-r4000-3456wh--worth-2 | test | 4 |  | yes | 5/9 | iallpowers.com, www.wellbots.com | 2026-10-27 / 2026-10-28 | v6 (10-26T21:34) | baseline | ? |
| allpowers-s2000-pro-1451wh--deal-1 | control | 4 |  | yes | 6/12 | iallpowers.com, www.wellbots.com | 2026-10-27 / 2026-10-27 | v7 (10-26T21:34) | n/a | ? |
| allpowers-s2000-pro-1451wh--deal-2 | control | 4 |  | yes | 3/7 | iallpowers.com, www.wellbots.com | 2026-10-25, 2026-10-28 / 2026-10-28 | v7 (10-26T21:34) | n/a | ? |
| esr-halolock-15w-wireless-car-charger-cryoboost--deal-1 | control | 5 | yes |  | 8/16 | dealectric.com, www.esrtech.com | - / 2026-10-27 | v6 (10-26T21:34) | n/a | ? |
| esr-halolock-15w-wireless-car-charger-cryoboost--deal-2 | control | 2 |  |  | 6/12 | www.esrtech.com | - / 2026-10-28 | v6 (10-26T21:34) | n/a | ? |

## allpowers-sp037-400w-solar-panel
- test, all: T5 0/8, T4+ 6/8, T4 on the product page 5/8, T3+ 6/8, T2+ 6/8
- test, fresh or baseline: T5 0/8, T4+ 6/8, T4 on the product page 5/8, T3+ 6/8, T2+ 6/8
- control: T5 2/4, T4+ 3/4, T4 on the product page 2/4, T3+ 3/4, T2+ 4/4
- freshness: baseline 8, fresh 0, stale 0, undated 0; flags 0; uncalled flag candidates 9

| cell | role | T | go | product page | rank | buy link domains | cart date quoted / live | index copy (OAI fetch) | fresh | flag |
|---|---|---|---|---|---|---|---|---|---|---|
| allpowers-sp037-400w-solar-panel--best-1 | test | 1 |  |  | -/9 | iallpowers.com, www.walmart.com | - / 2026-10-28 | v5 (10-26T21:35) | baseline | ? |
| allpowers-sp037-400w-solar-panel--best-2 | test | 1 |  |  | -/10 | ctolitypower.com, iallpowers.com, www.walmart.com | - / 2026-10-28 | v5 (10-26T21:35) | baseline | ? |
| allpowers-sp037-400w-solar-panel--coupon-1 | test | 4 |  | yes | 5/9 | iallpowers.com | 2026-10-21 / 2026-10-28 | v5 (10-26T21:35) | baseline | ? |
| allpowers-sp037-400w-solar-panel--coupon-2 | test | 4 |  | yes | 3/8 | - | 2026-10-21, 2026-10-27 / 2026-10-28 | v5 (10-26T21:35) | baseline | ? |
| allpowers-sp037-400w-solar-panel--deal-1 | test | 4 |  |  | 3/10 | iallpowers.com | 2026-10-21 / 2026-10-27 | v5 (10-26T21:35) | baseline | ? |
| allpowers-sp037-400w-solar-panel--deal-2 | test | 4 |  | yes | 2/8 | - | 2026-10-21 / 2026-10-28 | v5 (10-26T21:35) | baseline | ? |
| allpowers-sp037-400w-solar-panel--worth-1 | test | 4 |  | yes | 5/14 | iallpowers.com, www.ebay.com, www.prelectricdirect.com | 2026-10-21 / 2026-10-27 | v5 (10-26T21:35) | baseline | ? |
| allpowers-sp037-400w-solar-panel--worth-2 | test | 4 |  | yes | 5/20 | iallpowers.com, www.ebay.com, www.wellbots.com | - / 2026-10-28 | v5 (10-26T21:35) | baseline | ? |
| allpowers-volix-p300-100w-solar-kit--deal-1 | control | 4 |  |  | 4/11 | dealectric.com, iallpowers.com | 2026-10-25, 2026-10-28 / 2026-10-28 | v2 (10-26T21:35) | n/a | ? |
| allpowers-volix-p300-100w-solar-kit--deal-2 | control | 5 | yes | yes | 2/17 | - | 2026-10-25 / 2026-10-28 | v2 (10-26T21:35) | n/a | ? |
| esr-halolock-15w-wireless-car-charger-cryoboost--deal-1 | control | 5 | yes |  | 8/16 | dealectric.com, www.esrtech.com | - / 2026-10-27 | v6 (10-26T21:34) | n/a | ? |
| esr-halolock-15w-wireless-car-charger-cryoboost--deal-2 | control | 2 |  |  | 6/12 | www.esrtech.com | - / 2026-10-28 | v6 (10-26T21:34) | n/a | ? |
