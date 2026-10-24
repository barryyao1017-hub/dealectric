# Query-targeted comparison pages (DLC-51) — plan, 2026-10-23

Idea (Barry, 2026-10-23): the next obstacle after phase 2 is being found at all. Unprompted, no assistant has ever
cited us (0/90 in phase 1, 0/30 ChatGPT tier A on 2026-10-23). Instead of waiting for the broad shopper question
("best portable power station for camping") to rank us against Wirecutter and RTINGS, aim at the **queries the
agents themselves type into their search backend**: the follow-up searches are narrow, spec-heavy and often
"X vs Y vs Z", and few pages answer them. A page whose title and first heading match such a query nearly word for
word, with a horizontal comparison across many products (ours and the brands we do not sell), should surface higher
in a thin result set, and from there be cited and carry the shopper to a `/go/` link.

## Hypothesis and metric

**H:** for a query the agents issue and that today returns few pages that answer it directly, a comparison page whose
title matches the query gets (a) indexed by Bing and Brave, (b) into the engine's top 10 for that query, and (c) cited
in an unprompted assistant answer to the shopper question behind it — while matched control queries with no new page
stay at 0.

Readings, per query cluster, daily:
1. **indexed**: `site:dealectric.com <page>` on Bing and Brave; GSC/Bing Webmaster coverage.
2. **rank**: `growth/evals/serp.py` position of the page for the target query on Bing and Brave (`dealectric_rank`).
3. **cited unprompted**: ChatGPT (app, tier A) and Claude as an agent (tier A) on the shopper question of the cluster,
   n = 2; grade with `grade.py` as before (L4 = `/go/` link in the answer; also record "page cited" = any
   dealectric.com URL in citations or `response.search_results`).
Success: at least one built cluster reaches (c) while all controls stay at 0 after the index has had a week. (b)
without (c) is the fallback finding (ranked but not chosen); (a) without (b) means the result set was not thin.

## Data

- **ChatGPT's own search queries**: since 2026-10-23 `ui.py` records them (`queries`) with the result list ChatGPT was
  shown (`response.search_results`), read from the SSE answer stream (`SSE_HOOK_JS`, metadata type
  `search_model_queries` / `search_result_group`). The conversation JSON fetched afterwards has them stripped. Run:
  `2026-10-23-queryprobe` (30 target questions, tier A, n = 1).
- **Claude's search queries**: `run.py` has recorded them from the start (`queries`); 144 distinct on tier A across the
  phase 1–2 runs, 68 after dropping buy/retailer/brand-site queries (`serp-claude.json`).
- **Result-set thinness**: `serp.py` fetches the Bing and Brave top results for a query through the agent's Chrome.
  Thinness is judged on the titles: how many of the top 10 are pages written to answer this query (a "best X with Y
  (2026)" or "A vs B" page) versus pages that merely mention it (manuals, store collections, forum threads, broad
  "best power stations" lists). ChatGPT's `search_results` give the same view from inside the app.

## Steps

1. Capture queries (done 2026-10-23: `ui.py` SSE hook; 30-question unprompted run).
2. Score: `serp.py --from-run 2026-10-23-queryprobe` and `--queries-file` of Claude's queries; cluster the queries by
   shopper question; pick about 4 clusters we have products for whose result sets are thin, and about 4 as controls
   (similar thinness, no page). Table below.
3. Build: one page per cluster under `src/` (generator, not hand-written HTML in `docs/`): URL slug and `<title>`/`<h1>`
   = the query in plain words; comparison table across every product the agents named in their searches (EcoFlow,
   Anker SOLIX, Jackery, Belkin, … included, with spec and list price, no link or an unaffiliated manufacturer link);
   our rows carry the code, the saving, the cart-test date and the `/go/` link in the canonical phase-2 paragraph;
   `rel="sponsored nofollow"`, disclosure, no JS. Add to sitemap, llms.txt, offers.json `pages`; push with
   `tools/indexnow.py`; request indexing in GSC.
4. Measure daily for a week (readings 1–3), controls alongside. Stop early if the pages are indexed and ranked top 10
   but never cited after n = 2 × 3 days (finding: ranking is not the gate), or never indexed after 7 days (finding:
   the index, not the page, is the gate).

## Clusters (step 2)

Chosen 2026-10-23 from the queryprobe run. What ChatGPT's queries look like: the shopper's question plus "2026",
"review(s)" and two or three brand names ("best portable power station for camping 2026 review Jackery EcoFlow Bluetti
Anker"); one or two searches per chat; on the questions below its whole result set was small niche sites (no
Wirecutter, RTINGS, Tom's Guide, Wired), which is the opening: a site of our size ranks there. Claude's queries are
narrower and more numerous (up to 20 per answer), often "X vs Y vs Z" or a spec list. Public Bing had one of our pages
indexed on 2026-10-23 (`site:dealectric.com` → the home page), Brave none; ChatGPT's own Bing-fed index has more (it
lands on product pages on tier B), so reading 3 is the one that counts.

| cluster | Qnn | ChatGPT's query (verbatim) | ChatGPT's result set | Bing US demand, 3 mo (exact / broad) | our products | build / control |
|---|---|---|---|---|---|---|
| LiFePO4 vs NMC | Q17 | "portable power station LiFePO4 NMC battery chemistry manufacturer comparison 2026"; "LiFePO4 vs NMC portable power station battery chemistry cycle life energy density safety comparison" | 13 small sites, all titled "LiFePO4 vs NMC …", no product table | none reported (also "lifepo4 vs nmc", "lifepo4 (portable) power station") | 10 stations (9 LFP, 1 NMC) | **build**: `/compare/lifepo4-vs-nmc-power-stations/` |
| CPAP | Q16 | "best portable power station for CPAP machine 2026 runtime humidifier pure sine wave" | 12 small sites | none reported (also "(best) (portable) power station for cpap"); head: "cpap battery backup" 156, "cpap battery" 78 / 252 | Elite 30 V2, R600, T320, P1800, AC180 | **build**: `/compare/power-station-for-cpap/` |
| solar to recharge 1 kWh | Q21 | "how many watts solar panel to recharge 1000Wh portable power station solar charging losses peak sun hours" | 12 small sites and calculators | none reported (also "solar panel for (portable) power station", "how many solar panels to charge a power station"); head: "solar generator" 3,197 / 11,428 | SP037 400 W + the stations' solar inputs | **build**: `/compare/solar-watts-to-recharge-power-station/` |
| many AA/AAA at once | Q25 | "best high capacity AA AAA NiMH battery charger 8 bay 16 bay independent channels 2026 reviews" | 12 results, 6 from one small site | none reported (also "8/16 bay battery charger"); head: "aa battery charger" 214, "rechargeable battery charger" 133, "nimh battery charger" 33 | TN480U, Premium Pro AA | **build**: `/compare/aa-aaa-nimh-battery-charger-8-bay-16-bay/` |
| fridge sizing | Q15 | "portable power station refrigerator backup sizing watt hours runtime inverter surge manufacturer guide" | 23 small sites (+ Anker, EnergySage) | none reported (also "(portable) power station for refrigerator"); head: "battery backup for refrigerator" 16 | AC200L, Elite 200 V2, P1800 | control |
| backup under $1,000 | Q18 | "best home backup power stations under $1000 2026 reviews price battery capacity" | 9 small sites + Home Depot | none reported (also "home backup power station"); head: "home battery backup" 657 / 1,426, "portable power station for home" 317 | AC180, AC200L, P1800 | control |
| UPS | Q19 | "portable power station UPS transfer time computer manufacturer guidance EcoFlow Anker Bluetti" | makers' FAQs + small sites | none reported (also "portable power station ups", "power station with/as ups") | AC180, Elite 200 V2 | control |
| RV + solar combo | Q20 | "best RV portable power station solar panel combo 2026 comparison EcoFlow Bluetti Jackery specs" | 22 small sites + Popular Mechanics | none reported (also "rv power station", "portable power station for rv", "rv solar generator") | R4000 + SP037, Elite 300 | control |

Demand column (2026-10-24, `runs/2026-10-24-bingkw/volumes.json`): Bing Webmaster Tools → Keyword Research, US,
2026-07-24 to 2026-10-21, searches on Bing by people (not ChatGPT's backend queries, which nobody reports); one number
means exact = broad. "None reported" = Bing returns no data for the phrase in any country, i.e. below its reporting
threshold. For scale: "portable power station" 3,263 / 10,351, "best portable power station" 614 / 787, and the brand
names far above the category ("ecoflow" 20,861, "jackery" 18,833, "bluetti" 8,965). Reading: every verbatim ChatGPT
query and nearly every two-to-four-word version of the eight questions is below Bing's threshold, so on Bing the
cluster queries are thin on demand as well as on supply; only the broad head terms ("solar generator", "home battery
backup", "cpap battery backup") show measurable demand. This does not measure how often the assistants issue these
queries, which is the demand that matters for DLC-51.

Not chosen: the audio questions (Q26–Q30: RTINGS, Tom's Guide and What Hi-Fi hold the result sets), the charging
questions (Q03–Q13: Wired, Macworld, Apple, the WPC), and the power-bank airline questions (FAA, IATA).

## Log

- 2026-10-23: SSE hook in `ui.py` (queries + result list per chat); `serp.py`; unprompted 30-question ChatGPT run and
  Bing/Brave scoring of 68 Claude queries started.
- 2026-10-23 (evening): the four pages built and deployed (`src/compare.py` records, `compare_page()` in `build.py`;
  `/compare/` index; llms.txt section; sitemap). Other brands' figures from four research passes over the makers' US
  pages (EcoFlow, Anker SOLIX, Jackery, Goal Zero, DJI, Panasonic, Powerex, EBL, XTAR, La Crosse, SkyRC, Renogy,
  BLUETTI models we do not list, ResMed, Philips). IndexNow pushed. Day 0 of the readings.
- 2026-10-23, day 0 (`runs/2026-10-23-qp/`): Bing top 10 for all eight ChatGPT queries holds no Wirecutter/RTINGS-class
  domain and none of our pages (rank None everywhere); `site:dealectric.com` on Bing = the home page only. Brave could
  not be read: after about ten queries in a row it shows a "Verifying you're not a bot" check (not solved; the script
  records the page text), so Brave is dropped from the automated readings and Claude's Brave-backed search is read
  through the claude-code tier-A run instead. ChatGPT unprompted on the eight questions (queryprobe, n = 1): 0 of 8
  cite us. Bing/Brave result sets for all 36 ChatGPT and 68 Claude queries are in `runs/2026-10-23-queryprobe/
  serp.json` and `serp-claude.json`: on the power-station and battery questions the top 10 is small sites throughout;
  the audio, charging and airline questions have RTINGS, Wired, Macworld, Apple, the FAA or the WPC in them.
- 2026-10-24: **narrowing test** (`growth/evals/narrowing.py`, run `2026-10-24-narrowing`, stopped by Barry after 27 of
  32 chats): four products whose pages ChatGPT's index already holds (BLUETTI AC180, Baseus PicoGo AM52, Soundcore
  Space One, ALLPOWERS R4000), unprompted questions in four rungs from category to "exact model + a discount code that
  works at checkout". dealectric.com was in ChatGPT's search results in **0 of 27** chats, at every rung (rung 4: 0/7),
  although the AC180 page answers rung 4 almost word for word and is cited when the prompt names dealectric.com.
  Reading: narrowing the query alone does not surface an indexed Dealectric page; the gate is the search backend's
  ranking of a new domain (or ChatGPT's filtering of it), not the number of competing pages. Not run: the Bing rank of
  ChatGPT's queries, which would tell Bing from ChatGPT.
- 2026-10-24: Bing Webmaster Tools → URL Submission: `/compare` and the four comparison pages submitted ("Success: 5
  URLs submitted"; quota 100/day). The 2026-10-18 submissions of the product pages are still listed.
- 2026-10-24: **demand** from Bing Webmaster Tools → Keyword Research (US, 3 months; `runs/2026-10-24-bingkw/volumes.json`,
  demand column above): all eight verbatim ChatGPT queries and their short forms are below Bing's reporting threshold;
  only head terms register ("solar generator" 3,197, "home battery backup" 657, "cpap battery backup" 156, "aa battery
  charger" 214). Brand discount-code searches are small too ("jackery discount code" 36, "anker discount code" 19,
  "bluetti discount code" 18, "ecoflow discount code" 12). Bing's figures are people searching Bing, not the
  assistants' fan-out queries.
