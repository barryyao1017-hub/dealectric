# Demand audit, power stations and solar (2026-11-07)

Question (Barry): what is the one thing that brings more AI-agent traffic? Method: take real Bing search volumes
(Bing Webmaster keyword research, 2026-07-25..10-22, `growth/gapmine/runs/2026-11-05/volume.json`), group the
power-station / solar / home-backup queries into 35 shopper intents, rewrite each the way ChatGPT does
("best X 2026"), and read the top 10 in OpenAI's own index (`serpsources` source `openai`, one reading each, ~$0.40
total). Files: `queries.json` (groups and member queries), `readings.json` (top 10 per query), `../audit.py`.

## What we found

1. **We are in OpenAI's top 10 on 1 of 35 demand queries.** The 35 cover ~96,000 Bing searches in 3 months. The one
   is `/solar-generator-with-panels-included` (#8 on "best solar generator with panels 2026", 7,895 searches; #3 on
   the "...included" phrasing). That page is where 25 of ~75 real ChatGPT landings and most `/go/` clicks since
   10-28 came from.
2. **Our ~80 power-station pages aim below the demand.** They answer narrow questions (sump pump, pellet stove,
   reptile heat). No page of ours is written for the biggest intents: home battery backup system (14,964), best
   solar generator (6,999), solar generator for home use (6,972), portable power station (7,773), plug-in /
   balcony solar (7,447), or the brand-review queries (Jackery 9,293, BLUETTI 6,080).
3. **The head queries are not locked by big publishers.** On 26 of 35 queries, 4 or more of the 10 slots go to small
   independent sites, and big-publisher slots are often off-topic news (TechRadar and Tom's Guide articles about
   security cameras or Octopus Energy ranking for "best home battery backup system"). Example: OutageShield, a
   site like ours (no test lab, runtimes calculated from capacity, CJ BLUETTI and Rakuten Anker links, updated
   11-04), is #9 for that 15k query.
4. **Indexing is not the problem; ranking is.** OAI-SearchBot fetched every near-head page we have
   (`/best-solar-generator-for-power-outages` 11-02 and 11-06, `/best-2000wh-power-station` 11-07,
   `/best-2kwh-power-station-for-rv` daily), yet none is in the top 10 for its head query. The winner is re-fetched
   2-6 times a day. What lifts a new domain's page in OpenAI's ranking is not known; plausible factors are an exact
   head-query title, page age, and mentions elsewhere.
5. **"Best portable power station 2026" (7,773) is Reddit's.** 8 of 10 slots are Reddit threads, several of them
   listicle posts in small subs ("5 best portable power stations for camping, I tested"). A page will not get in; a
   Reddit presence might.

## Openings, ranked (volume x free slots x products we can link)

| # | Intent | Bing vol. | Small-site slots | Our page | We can link |
|---|---|---:|---:|---|---|
| 1 | Solar generator with panels | 7,895 | 7 | #8, strengthen | ALLPOWERS, BLUETTI kits |
| 2 | Home battery backup system (+ whole house, outages) | 16,397 | 4-6 | none | BLUETTI Apex 300, Anker SOLIX S5000, Nature's Generator L6000, Oscal 6000, Growatt Helios; EcoFlow DELTA via Amazon |
| 3 | Best solar generator / for home use / home backup | 14,454 | 2-4 | near miss (power-outages page) | same |
| 4 | Brand reviews: Jackery, BLUETTI, EcoFlow, Anker | 19,834 | 3-8 | none | Amazon (Jackery, EcoFlow, Anker), CJ BLUETTI, Rakuten Anker |
| 5 | 4Patriots review / alternatives | 3,116 | ~9 | none | cheaper LiFePO4 alternatives we sell |
| 6 | Mid-tail with 8-9 small-site slots: whole house (442), RV (260), 1000 W (301), 2000 W (247), 200 W / 400 W panel (655), fridge (218) | 2,123 | 8-9 | near misses | yes |
| 7 | Plug-in / balcony solar | 7,447 | 4-9 | apartment pages, not ranked | thin: no plug-in kit in the catalog (supply gap) |
| 8 | Portable power station | 7,773 | 0 (Reddit 8) | catalog guide | Reddit, not a page |
| - | Pecron review (2,699, 10 small-site slots) | | | | no program (Awin pending) |

## Caveats
- One reading per query. Phrasing moves ranks (#3 vs #8 for the same page), so treat single ranks as noisy.
- OpenAI's API index stands in for the ChatGPT app's results (same index, the app sees ~12 and writes its own query).
- Bing volumes are a floor for intent size, not ChatGPT's query mix, which we can't see.
- Brand-review pages (row 4) break the 10-31 rule against brand-named queries, which was written for gap scoring;
  using them for page building is Barry's call.

## What shipped (2026-11-07, Barry: "yes, incl. brand page")

| Target query (baseline rank) | Page | Change |
|---|---|---|
| best solar generator with panels 2026 (#8) | /solar-generator-with-panels-included | short answer moved first with the query words; competitor prices re-read |
| best solar generator for home use 2026 (–), for home backup (–) | /best-solar-generator-for-power-outages | title, H1, lead and link text retargeted; sold-out picks marked |
| best home battery backup system 2026 (–) | /best-home-battery-backup-system (G174) | new |
| bluetti power station review 2026 (–) | /best-bluetti-power-station (G175) | new, brand page |
| 4patriots solar generator review 2026 alternatives (–) | /best-4patriots-solar-generator-alternative (G176) | new |

All five pass `fastloop.py check` at ranks 1/3/6 on the OpenAI result sets above. New records: BLUETTI Elite 100 V2
(Awin), Anker SOLIX F3800 Plus (Rakuten). Re-reads: DLC-197 (11-10), DLC-198 (11-14), DLC-199 (11-17, verdict).

## Recommendation
Run a 10-day head-query test before building more long-tail pages: retitle and strengthen 2 near-miss pages (row 1,
row 3), build 3 new head pages (rows 2, 4 one brand, 5), and re-read these 35 queries on days 3, 7 and 10 (~$0.40 per
read, `audit.py` reruns into a new dated folder). Success = 2 of the 5 enter the top 10. If none do, the blocker is
off-site authority, and Reddit/YouTube (row 8) becomes the lever.
