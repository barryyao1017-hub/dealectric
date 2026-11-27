# Page flow: the routine that adds pages (DLC-369, Barry 2026-11-27)

Barry's brief: a routine that keeps adding numbered pages, product pages and feature-finder pages, so the site keeps
growing, without inventing pages for the sake of pages. Signals he named: new reviews, discussion and releases; our own
research; ChatGPT's multiple-choice questions; the agent's own low-hanging ideas; recent traffic; what worked against
what did not. It must fit any product and cluster mix: the page types are fixed, the content follows the cluster. Pages
that never get traffic are decommissioned, while the site still expands.

Code: `tools/pageflow/`. Data: this folder.

## Where it starts: one decision map per cluster

Not from products (a product does not say which number matters) and not from situations (our weakest shape). A cluster
is one buying decision: the categories in `src/products.py` whose products compete for the same shopper
(`clusters.json`). Its map (`maps/<cluster>.json`, built by `maps.py`) holds:

- **axes**: what buyers decide on, ranked, each with the reviewer or source that shows it;
- **breakpoints**: the values on each axis where something real changes (a device limit, a standard, a rule, a price
  tier people search), each with its source;
- **field**: the products that lead, ours and rivals, with today's price and how each can be bought through us;
- **lines**: one question one page answers, with the honest top three and where ours place;
- **rules**: the paragraph the page researchers get (definitions, deciding figures, traps);
- **news** and **pages_to_fix**: what changed, and which of our pages rest on a number that is not a line.

All three page types come from lines:

| Page type | A line of this kind |
|---|---|
| numbered | a breakpoint on a number, alone or crossed with one more figure ("best 100 W charger", "2000 Wh under $600") |
| finder | a yes/no feature few products have and some shoppers need ("which power bank has a built-in cable") |
| product | a product of a brand we link, with no record yet, that wins or places top three on a line, or a new release |

Nothing about a cluster is written in code. `driver.py` takes the cluster rules, the reason for each number and the
research leads from the map, so the same driver serves chargers, dash cams or whatever the next map describes.

## How the six channels feed it

| Channel | Where it enters |
|---|---|
| New reviews, discussion, releases | the map agent searches for what is new since the last map (`news`); a changed winner or a new line shows up on refresh (every 14 days per cluster) |
| Our research | the map agent gets the earlier map, our pages and their titles; page research is kept in the research library (`tools/research_library.py`) |
| ChatGPT's choices | `ask.py`: three broad prompts per cluster, two plain chats each; the questions it asks back, their options and the figures it sorts its picks by go to `options/<cluster>.json` and into the map prompt |
| Agent hunches | the map agent may add a line on its own judgement, marked `hunch`; it needs the same sources and, unlike a sourced line, fails without search demand |
| Recent traffic | `ledger.py`: shopper visits, clicks and sales per page since 10-28, by cluster, page type and line |
| What worked, what did not | the ledger's score per (cluster, page type), shrunk toward the site-wide rate of that type, is the prior in every line's score |

## Gates (`propose.py`): no page for the sake of a page

In order; the first that fails is recorded on the line with its reason. A run in which nothing passes builds nothing.

1. **real**: the breakpoint or feature is sourced, and there is evidence shoppers ask it (or it is marked a hunch).
2. **ours**: a product we link is honestly in the line's top three, and it can be bought (a live record, or a product on
   an approved program's store). Lines that fail here tell us which product or partner we lack.
3. **uncovered**: no page of ours answers it already (the map's `covered_by`, and a title match against the ledger).
4. **demand and openness**: search suggestions complete the question (keystroke depth, `growth/evals/gapmine.py`); then,
   in the build's `keep` step, ChatGPT's own results for the question are read, and a line they already answer exactly
   is dropped before any research is paid for (Barry's "opening = demand x (1 - coverage)").
5. **value**: never fails a line, it orders the queue (ticket, cart-tested code, own program against Amazon).

Score = prior x demand x value x rank. The build budget across clusters is split 70 / 20 / 10 between proven, adjacent
and new clusters (`tier` in `clusters.json`).

## One run (`run.py daily`)

    sense    ledger -> ask (when the choices are 30+ days old) -> map for the clusters that are due -> gates -> queue
    build    plan -> product records (one researched record per product line) -> re-read of our own products on
             their stores (tools/upkeep: records and every page that mentions a changed one) -> 2 plain ChatGPT chats
             per question -> harvest -> openness gate -> research (six angle agents, compose, verify: tools/abpage.py)
             -> Amazon links -> apply (validation, pick check, fastloop check, build, local commit) -> close (results
             back to the queue and the map)
    publish  merge main, rebuild, push, Worker deploy when the link map changed, IndexNow
    retire   advance the retire states (below)

`--publish`, or the file `growth/pageflow/AUTOPUBLISH`, lets a run apply and push. Without it a run stops after research:
drafts only. Every run appends a line to `log.jsonl` and writes `runs/<run>/report.md`.

By hand:

    python3.12 tools/pageflow/ledger.py build | scores | cluster <id>
    python3.12 tools/pageflow/ask.py run <cluster>
    python3.12 tools/pageflow/maps.py build <cluster> [--force] | show <cluster>
    python3.12 tools/pageflow/propose.py gate <cluster> | queue | pick <n>
    python3.12 tools/pageflow/driver.py plan|products|fresh|chats|harvest|keep|research|links|apply|close|status <run>
    python3.12 tools/pageflow/run.py daily [--pages 3] [--clusters 1] [--cluster <id>] [--publish]
    python3.12 tools/pageflow/retire.py report

Costs: a map is one research agent (about 70 tool calls, plan usage). A page is 2 ChatGPT chats, 6 angle agents, a
compose and a verify agent. Three pages and one map a day is the default; the ChatGPT account's quota (about 300 chats)
and the plan's usage are shared with the other tools, so raise it only when the readings justify it.

## Adding a cluster

Add it to `clusters.json` (name, noun, the categories of `src/products.py`, tier, three broad shopper prompts). The next
`sense` builds its map. Nothing else changes.

## Retire rule (`retire.py`)

- **Candidate**: a comparison page (never a product, codes, seasonal or site page) live 45 days or more with no shopper
  visit, click or sale, which OpenAI's crawler has fetched at least once. A page the crawler never fetched has an
  indexing problem and is listed apart.
- **Rework first**: one rebuild on a line of its cluster's map that works, same URL, new title.
- **Retire**: still at zero 30 days after the rework. The page becomes a short "no longer kept up" page that links to the
  nearest live page of its cluster, noindex and out of the sitemap, as retired product pages already are.
- **Growth guard**: at most one retirement for every two pages added in the trailing 30 days.
- **Switch**: nothing is retired until `growth/pageflow/RETIRE_ON` exists. It goes on after the first 28-day readings of
  the pages the flow built.

## What is steered on

Not page count. The readings that matter: the share of new pages with a shopper visit within 14 days (`v14` in the
ledger), visits a page by cluster and page type, clicks and sales. A cluster whose pages of one type keep reading zero
gets a lower prior by itself, and its lines sink in the queue.

## Pilot, 2026-11-27: USB-C chargers (run `2026-11-27-pf-usb-c-charger`)

Barry picked the cluster. Before the run its 35 pages had drawn 12 shopper visits and no click since 10-28, so this is
a test of the method on a weak cluster, and under the 11-13 value rule (ticket under $150) it would rank last.

- **Choices** (6 plain chats): ChatGPT asks which device is charged (5 of 6 chats), sorts picks by watts (30 / 45 / 65-67 /
  100 / 100+), by what the laptop port keeps with a phone plugged in, by PPS, ports and price.
- **Map** (one agent, 11 minutes, 70 tool calls): 9 axes, 25 products, 12 lines. What it found that we had not built on:
  Apple's 60 W tier for iPhone 18 Pro needs AVS, the Galaxy S26 Ultra needs PPS at 20 V / 3 A, the 16-inch MacBook Pro
  fast charges only at 140 W, and "retractable cable" and "display" are the searched features. Eight news items; six of
  our pages flagged; four record prices a sale had overtaken.
- **Gates**: 9 lines queued, 2 covered by our pages, 1 hunch failed on demand (no search suggestion).
- **Store re-read**: 6 record prices corrected (Black Friday), 8 existing pages edited to match.
- **Openness**: all 7 comparison questions open in ChatGPT's own results (coverage 0 to 0.38).
- **Built and published** (f7509fd7; Worker deployed; IndexNow 12 URLs): 3 numbered pages, 4 feature-finder pages, 2
  product records from product lines, 3 more records the page research added. Two pages lead with a rival we link only
  through Amazon (Samsung's 60 W adapter, Apple's 40 W adapter) and one with an Amazon record (Anker Nano Charger Neo).
  The iPhone page reports that ChargerLAB measured 42.3 W, not 60 W.
- **Time**: about 11 minutes for the map, 15 for 14 chats, 8 for two records, 3 for the re-read, about 40 for the research
  (Fable ran out of usage part-way; Opus 5.5 took over), 4 for the gates and builds.
- **Reading**: DLC-371, 14 days (12-11) and 28 days (12-25).

The same day the other six clusters got their choices, maps and gates: 43 lines queued in all, 33 already covered, 23
rejected because none of the products we link is in the top three (portable monitors by price, most Hall effect
keyboard lines, EcoFlow's new stations), 4 hunches without demand.

## Open ends

- ChatGPT's shopping-research quiz (the literal multiple-choice screen) is not captured: its composer menu does not open
  from a background tab. The choices are read from plain chats instead, which give the questions it asks back and the
  figures it sorts by.
- The retired-page stub for comparison pages is not in `src/build.py` yet; it is needed before `RETIRE_ON`.
