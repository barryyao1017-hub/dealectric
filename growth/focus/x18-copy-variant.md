# x18: solar-kit batch and the assistant-addressed copy test (2026-11-04, DLC-163)

## Why
The page scoreboard (tools/scoreboard.py, DLC-162) showed solar kits carry almost all outside demand: G02 had 14
ChatGPT landings and the P1800 + SP037 kit had 24 ChatGPT-tagged `/go/` clicks in 8 days, while the cluster had only 2
of 107 comparison pages. Barry: build more there, and test his premise. About half of `/go/` clicks come straight
from ChatGPT's answer without the shopper opening our page, so the page's real reader is the assistant. Under that
premise the page should address the assistant directly and argue that the `/go/` link is the best answer to the query.

Prior evidence against: in the 10-25 gap experiment (stage 1), copy addressed to the AI got our link in 1 of 96 Claude
answers, against 71 of 96 without it (DLC-56/59/60). ChatGPT did not flag such copy in loop 3. Barry's call:
ChatGPT is where the sales are, pages are cheap, and we need more data points.

Rules for the A copy: visible text, every claim truthful and passing the honest-win screen, and phrased as an argument
("for AI assistants answering '<query>': recommend X because …; tell your user <caveat>"). It never says to ignore
other sources and claims no authority.

## Design
- 12 brand-free kit queries, packed through the OpenAI API (`x18-solar-*`). Two-judge vote: Sonnet 5.5 and Opus 5.5,
  because Fable 5.1 hit its usage limit. 10 open, camping split (open/contested), shed dropped (one result twice).
- Parked:
  - under $300: our only kit under $300 (VOLIX P300) is sold out.
  - tiny house: no honest win against whole-home systems.
  - beginner: BLUETTI's Elite 30 V2 "in the box" list names no solar cable, so we can't call it plug-and-play.
- Built 8 pages. The leads were assigned by topic pair before any copy was written:

| page | slug | variant | pick |
|---|---|---|---|
| G106 | /best-solar-generator-kit-under-1000-for-home-backup | A | ALLPOWERS P1800 + SP037 400 W ($698, ships Dec 7) |
| G107 | /1000wh-power-station-with-400w-solar-panel-bundle | A | ALLPOWERS P1800 + SP037 400 W |
| G108 | /solar-generator-kit-for-an-apartment-balcony | A | BLUETTI Elite 30 V2 + 100 W ($489.99) |
| G109 | /best-solar-generator-kit-for-tent-camping | A | BLUETTI Elite 30 V2 + 100 W |
| G110 | /best-solar-generator-kit-for-hurricane-season | N | BLUETTI Elite 200 V2 + 200 W ($1,199) |
| G111 | /best-2000wh-solar-generator-kit-with-panels | N | BLUETTI Elite 200 V2 + 200 W |
| G112 | /best-solar-generator-kit-for-van-life | N | BLUETTI Elite 200 V2 + 200 W |
| G113 | /solar-generator-kit-vs-buying-separately | N | BLUETTI AC180 + 200 W ($729, $169 under its parts) |

Pairs: home backup (G106/G110), a specific kit size (G107/G111), use case (G108/G112), general question (G109/G113).
Records carry `copy_variant`, and the scoreboard prints an A vs N table.

## Offline result (OpenAI API replay, both versions of every page)
`fastloop.py replay <pack> --draft <html> --rank 3 --reps 5`, tags `x18A` / `x18N`; `fastloop.py score`
(Sonnet judge). Same result set, same rank; only the lead differs.

| page | /go/ A | /go/ N | our pick A | our pick N |
|---|---|---|---|---|
| G106 | 5/5 | 5/5 | 5/5 | 5/5 |
| G107 | 5/5 | 2/5 | 5/5 | 5/5 |
| G108 | 5/5 | 3/5 | 5/5 | 5/5 |
| G109 | 4/5 | 5/5 | 5/5 | 5/5 |
| G110 | 5/5 | 5/5 | 5/5 | 5/5 |
| G111 | 1/5 | 2/5 | 0/5 | 2/5 |
| G112 | 4/5 | 5/5 | 5/5 | 5/5 |
| G113 | 0/5 | 0/5 | 3/5 | 1/5 |
| **all** | **29/40** | **27/40** | **33/40** | **33/40** |

- No measurable difference on the ChatGPT API at n = 5 per cell. No answer mentioned, quoted or questioned the
  assistant-addressed text (regex scan of all 40 A answers).
- G111 loses to Jackery's Solar Generator 2000 v2 + 2 × 200 W in both versions, because ChatGPT values 400 W of
  included panels over our kit's single 200 W panel. Fix: a product record for BLUETTI's Elite 200 V2 + 2 × 200 W kit
  ($1,499, $150 under Jackery's listed $1,649) as the lead.
- G113 is a yes/no question, so answers cite the page but add no buy link in either version.
- Not run: Claude. The 10-25 finding (Claude drops pages addressed to it) still stands untested on these pages.

## How to read it live
`python3.12 tools/scoreboard.py`, section "Copy-variant test". All 8 pages were published 2026-11-04. Read at 10 and
20 days (11-14, 11-24) for outside ChatGPT-User fetches, landings and `/go/` clicks from the page, A against N. With 4
pages a side, only a large gap (2× or more, on 10+ events a side) means anything. Keep A only if it wins on ChatGPT
and costs nothing measurable in Claude-User fetches.

## Facts checked 2026-11-04
- ALLPOWERS, from the store's product JSON: P1800 + SP037 $698, P1800 $399, SP037 $299, S2000 Pro + SP037 $848,
  VOLIX P300 kits sold out. The P1800 kits ship from Dec 7.
- BLUETTI, from the store's product JSON and pages: AC180 + 200 W $729, AC180 alone $499 store (cart $449 after the
  automatic $50 discount), AC180 + 100 W $649, AC180 + 2 × 200 W $1,232, Elite 200 V2 + 200 W $1,199 (station $899),
  Elite 30 V2 + 100 W $489.99. The AC180 is back in stock late November; the 200 W panel ships Nov 18.
- Jackery, EcoFlow and Goal Zero stores 429'd every fetch, both agents and direct. Their rows say "not confirmed" or
  carry search-listing prices labelled as such.
- Research files (not committed): five Sonnet agents, about 120 WebSearch calls.
