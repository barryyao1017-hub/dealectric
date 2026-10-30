# Are the focus products in content gaps? (2026-10-30)

Barry's step 1 for salvaging W2-W4. `growth/evals/focusgap.py` labels the top six non-Dealectric pages ChatGPT was
shown for each category question (W1 "best" cells, 10-28; gap-vs-focus run, 10-30) with gapexp.py's rule: GAP = at most
1 dedicated-and-substantive and at most 2 substantive; SATURATED = 3+ dedicated-and-substantive; PARTIAL between.
Judge: Claude Sonnet 5.5, one pass. Labels in `growth/focus/focus-gap/labels.json` (page texts kept local).

| group | product / page | question | ChatGPT's query | status | ded+sub | sub | of |
|---|---|---|---|---|---|---|---|
| focus | bluetti-ac200l | What's the best 2kWh portable power station for an RV under $900? | best 2000Wh portable power station under $900 RV 2026 price sale comparison | PARTIAL | 2 | 5 | 6 |
| focus | bluetti-ac200l | What's the best 2kWh portable power station for an RV? | best 2000Wh portable power station for RV 2026 comparison EcoFlow Delta 2 Max Anker Solix F2000 Bluetti AC200L Jackery 2000 v2 | SATURATED | 5 | 6 | 6 |
| focus | aurzen-travelplay-autocinema-tesla-model-y | What's the best back seat screen for a Tesla Model Y under $150? | best Tesla Model Y rear seat screen under $150 2026 reviews compatibility | PARTIAL | 2 | 2 | 6 |
| focus | aurzen-travelplay-autocinema-tesla-model-y | What's the best back-seat screen for a Tesla Model Y? | best Tesla Model Y rear seat screen aftermarket review installation 2026 | SATURATED | 3 | 3 | 6 |
| focus | allpowers-r4000-3456wh | What's the best home backup power station under $1500? | best home backup power stations under $1500 2026 EcoFlow Delta 2 Max Anker Solix F2000 Bluetti AC200L review price | PARTIAL | 2 | 3 | 6 |
| focus | allpowers-r4000-3456wh | What's the best 3 to 4 kWh portable power station for home backup? | best 3 to 4 kWh portable power station home backup comparison EcoFlow Delta Pro 3 Anker Solix F3800 Bluetti 2026 specs price review | PARTIAL | 2 | 3 | 6 |
| focus | allpowers-sp037-400w-solar-panel | What's the best 400W portable solar panel under $300? | best 400W portable solar panels under $300 2026 price review | PARTIAL | 1 | 6 | 6 |
| focus | allpowers-sp037-400w-solar-panel | What's the best 400W portable solar panel for a power station? | best 400W portable folding solar panels for power stations 2026 comparison EcoFlow Bluetti Jackery Renogy | SATURATED | 4 | 5 | 6 |
| focus | allpowers-p1800-1024wh | What's the best 1kWh portable power station under $450? | best 1kWh portable power stations under $450 2026 prices EcoFlow Delta 2 Bluetti AC180 Anker Solix C1000 Jackery 1000 v2 | SATURATED | 4 | 5 | 6 |
| focus | allpowers-p1800-1024wh | What's the best 1kWh LiFePO4 portable power station under $500? | best 1kWh LiFePO4 portable power station under $500 2026 price review comparison | SATURATED | 3 | 6 | 6 |
| focus | allpowers-s2000-pro-sp037-solar-kit | What's the best solar generator with panels included under $1000? | best solar generator with panels included under $1000 2026 review EcoFlow Bluetti Jackery Anker | PARTIAL | 2 | 4 | 6 |
| yardstick | solar-generator-with-panels-included | What's the best solar generator with solar panels included? | What's the best solar generator with solar panels included? | SATURATED | 5 | 6 | 6 |
| yardstick | solar-generator-with-panels-included | Best solar generator kit with panels for under $1,000? | best solar generator kits with solar panels under $1000 2026 reviews prices | PARTIAL | 2 | 4 | 6 |
| yardstick | solar-generator-with-panels-included | I want a portable power station that comes with a solar panel for camping. Which kit should I buy? | best portable power station solar panel kit for camping 2026 EcoFlow Jackery Bluetti comparison | SATURATED | 4 | 5 | 6 |
| yardstick | best-power-banks-for-flying | What's the best power bank to bring on a plane that airlines allow? | 2026 airline power bank rules FAA TSA 100Wh 160Wh carry-on restrictions 2026 | GAP | 0 | 0 | 6 |

## Reading

- No focus category is a gap: 5 PARTIAL, 5 SATURATED.
- The solar gap page's own questions are no emptier: 1 PARTIAL, 2 SATURATED. Yet our solar page ranked #1-2 whenever
  ChatGPT retrieved it (5 of 6 answers on 10-30), while no focus page was retrieved for its category (0 of 8).
- So gap status does not separate the page that won from the pages that lost. What does: for the solar questions we
  have a page written for the question (dedicated, with tested prices and codes); for the focus categories we have
  only single product pages, which the rule itself says are never dedicated.
- The one true GAP (flying) is a gap because ChatGPT turns the question into a rules search (FAA/TSA); our page there
  has never been crawled.
- Caveat: the judge counts templated listicle sites (gearranking, powerstationranking, buyersheet) as substantive; the
  10-25 work called those a quality gap. One judge pass, six sources per set.
