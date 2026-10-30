# G04: /best-solar-generator-for-power-outages — how this page came about, and how to read its results

Built 2026-10-30 (commit 5923752) on Barry's go, as the first deliberate test of what we learned from the first sale.
Read this before crediting or blaming the page for anything it does later.

## Why this page exists (the evidence chain)

1. **First sale, 2026-10-29** (DLC-33): a ChatGPT shopper bought the ALLPOWERS P1800 + SP037 kit through
   `/go/allpowers-p1800-sp037-solar-kit`, almost certainly relayed from `/solar-generator-with-panels-included`
   two hours after OpenAI's crawler first fetched that page.
2. **Gap vs focus** (`gap-vs-focus.md`): on category questions the solar page was retrieved 5/6 and cited 4/6; focus
   product pages 0/8.
3. **Not a content gap** (`focus-gap.md`): the solar questions' result sets were as crowded as the focus ones.
4. **Not supply** (`growth/focus/supply/results.json`, a7c9084): other actionable sources per result set, solar 2.1 vs
   focus 2.0. The solar page was retrieved for 4 of 11 solar phrasings, none of the 5 general ones.
5. **What did separate them** (`growth/focus/compqual/results.json`, 98f54ec, blind Claude judge, 12 questions):
   - Retrieval tracked **title-word match** with ChatGPT's own search query: hits 0.5–1.0, misses 0.09–0.27,
     competitors ~0.25.
   - Once retrieved, the solar page was judged **#1 of 7 on content** every time (usefulness 5.0 vs 2.9): 15 models
     vs ~6, dated prices, cart-tested codes.
   - On the outage questions the solar page was still judged #1–3 on content but never retrieved (title match 0.1).

So the hypothesis this page tests: **a page titled in ChatGPT's own query words, whose content beats the result set it
lands in, gets retrieved and relied on.**

## What we did to the page, and why

| Choice | Reason |
|---|---|
| Title: "Best solar generator for power outages and home backup (2026): portable power stations compared on capacity, expandable batteries and solar charging" | Built from ChatGPT's recorded queries (below). Title-word match: 0.90 on the outage query (solar page 0.10), 0.55 on "which portable solar power station" (0.09), 0.36 on home backup (0.27; that query is mostly brand names, which the description and table carry). |
| Description names EcoFlow, Anker SOLIX, Jackery, BLUETTI, ALLPOWERS | ChatGPT appends these brands to its queries. |
| "Where to buy" rows first (name, price, buy link, code, test date) | The shape that relayed our `/go/` link on the solar page and in the ESR study (links come from list rows within the first ~200 characters). |
| Outage sizing first (fridge kWh/day, 85% usable AC, panel watts per sunny day, TT-30 vs L14-30 120/240 V) | Answers the question before the picks, as the solar page does. |
| Columns competitors lack together: expandable to, home hookup, switchover, max solar, **days of fridge backup**, dated store price, code | Fills what the competitor set is missing (next section). |
| 12 rows: 5 ours (Elite 300, R4000, Elite 200 V2, P1800+SP037 kit, AC180+200 W kit), 7 others (DELTA Pro 3, F3800 Plus, HomePower 3600 Plus, DELTA 3 Ultra, DELTA 2 Max, C2000 Gen 2, Explorer 2000 v2) | The others are the products ChatGPT itself recommended for these questions (supply test answers), so the table covers what the shopper will be weighing. Competitor figures read on the makers' US stores 2026-10-30 by a research pass with sources. |
| BLUETTI Elite 200 V2 station, not its 200 W kit | The sweep saw the kit at $1,099 in the cart vs our $1,199 on 10-29; weekly price check (DLC-9) owns that fix, so the page avoids a possibly stale price. |
| Link to the solar page at the end; our product pages link here automatically ("Compared side by side") | Internal links from pages OpenAI already holds, to speed the first crawl. |
| Neutral copy, nothing addressed to AI | Claude-line rules (DLC-59/60). |

## The competitor set it enters (ChatGPT's own result sets, 2026-10-30)

Questions and ChatGPT's queries:
- "What's the best solar generator for power outages?" → `best solar generators portable power stations for home power outages 2026 reviews capacity expandable solar charging`
- "What's a good solar generator with panels for home backup?" → `best solar generators for home backup 2026 EcoFlow Anker SOLIX BLUETTI battery capacity solar panels comparison`
- "Which portable solar power station should I buy?" → `best portable solar power stations 2026 comparison EcoFlow Anker SOLIX Jackery BLUETTI capacity price solar charging`

Who ranks there: Consumer Reports, OutdoorGearLab (14 units lab-tested), Good Housekeeping, Popular Mechanics,
TechRadar, poweroutage.us, thesolarlab.com, ecosolarkits.com, solarpowerauditor.com, offsetsolar.com, and maker pages.
**This is a stronger field than the solar kits question**: lab-tested publishers. What they lack (blind judge,
compqual): dated prices (4 of 24 pages), codes (2 of 24), outage-specific comparison across brands in one table.
What we lack: our own hands-on testing of the stations.

So this page mainly tests **retrieval by query wording**. If it is retrieved but not relied on, content against
lab-tested publishers is the weak link, not wording.

## Baseline before the page (2026-10-30, signed-in ChatGPT, gpt-6)

| Question | Our pages retrieved | Our page cited | /go/ link |
|---|---|---|---|
| outage (solar-general--outage-1) | no | no | no |
| home backup (solar-general--homebackup-1) | no | no | no |
| which station (solar-general--which-1) | no | no | no |

Runs: `growth/evals/runs/2026-10-30-gap-vs-focus/` (chatgpt/solar-general--*.json).

## How to read results later

1. **Gate: OpenAI's first fetch.** Until OAI-SearchBot fetches `/best-solar-generator-for-power-outages`, ChatGPT
   cannot retrieve it; a miss before that says nothing. Check Cloudflare (verified "Search Engine Crawler", Chrome/131
   UA, or OAI-SearchBot) or `growth/evals/storedcopy.py`.
2. **Reading after the fetch:** the three questions above plus 3 more phrasings (power outage backup for a fridge,
   whole-home backup with a transfer switch, solar generator for hurricane season), n=2, `visibility_scan.py`.
   Success bar (set 2026-10-30 before any reading): retrieved in ≥4/12 and cited in ≥3/12, and at least one outside
   ChatGPT-tagged `/go/` click on a product in this table within a week of the first fetch.
3. **Attribution:**
   - Retrieved and cited → wording + content worked; repeat this recipe.
   - Retrieved, not cited or cited below lab-tested publishers → wording works, content loses in a strong field;
     add what they have (measured runtimes, our own tests).
   - Not retrieved after the fetch → title wording alone is not enough; look at OpenAI's stored copy and snippet.
4. **Confounds to note in any reading:** the solar page also changed on 10-30 (camping wording, 9938bed) and now links
   here; Anker prices include a store code that expires in early November; competitor figures are not re-checked daily.
