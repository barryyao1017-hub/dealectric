# Gap mining: finding openings structurally (2026-11-05)

Barry, 2026-11-05: stop guessing which queries might be gaps and testing them one at a time. An opening is the
product of how much a topic is searched and how little of that search the current pages serve:

    opening = demand × (1 − coverage)

A query nobody searches scores near zero however open it is. A heavily searched query can still be an opening when
the pages that exist serve only part of it. Scale across clusters ranked by that product.

## Why the earlier funnel produced one winner (G02)

- G02 "solar generator with panels included" was picked on 2026-10-25 using **measured demand**: 402 Bing searches
  in 3 months, plus a top 10 with no publisher (`growth/gap-targets.md`). It drew 14 landings in 8 days.
- G01 (flying) and G03 (Tesla screen), built the same day with the same recipe, had demand below Bing's reporting
  threshold. They drew 1 landing each.
- The later funnel (G05–G117, 2026-11-01..04) judged **openness** (an LLM vote on ChatGPT-style result sets) and
  estimated demand from forum thread counts. Demand was never measured, so the gate passed long-tail needs
  ("pellet smoker overnight", "reptile heat in an outage") that are open because almost nobody asks them.
- `backfill.md` in each run measures the demand score of every published gap page's own title query (step `backfill`).

## Pipeline (`growth/evals/gapmine.py`, one folder per run under `runs/`)

Nothing starts from a query we made up. Seeds are the category nouns our approved brands sell (`brands.json`).
Every candidate is something an engine, a forum or a brand's news produced.

| step | source | what it gives |
|---|---|---|
| `expand` | Google, Bing and Amazon autocomplete over 15 shopper stems plus "for a…z" per seed | the queries people actually type, and how hard each engine pushes them |
| `reddit` | old.reddit search, top of the month per seed (Agent Chrome; the JSON API is blocked on this network) | questions people are asking now |
| `news` → `launches` | Google News RSS per brand, last 45 days → new model names (Claude) → autocomplete of "<model> vs / or / review / alternative" | the launch lane: new products whose queries few pages target yet |
| `label` | Claude per seed | intent, brand-named, cluster label, whether one of our pages already covers it |
| `depth` | keystroke depth of each cluster's lead queries | demand (below) |
| `supply` | live Bing top 10 for each cluster's lead query, labelled by voidscan's labeller | coverage (below) |
| `report` | | clusters ranked by opening |

**Demand (keystroke depth).** Engines rank suggestions by query volume. The fewer characters of a query's tail a
searcher must type before the engine offers the whole query, the more it is searched. Calibrated against Bing
Webmaster volumes (`calibrate`, 61 long-tail queries of 4+ words, firefox client): Spearman 0.40. Mean score 0.13 at
under 30 searches per 3 months, 0.38 at 30–100, about 0.6 at 100+, and flat above that. It is a gate, not a
ruler: it separates "nobody searches this" from "people search this" but cannot rank big clusters against each
other. Bing Webmaster Keyword Research gives real counts and should replace it once the Agent Chrome on the work
laptop is signed in (Google wants a passkey or device prompt from Barry).

**Coverage.** Position-weighted share of the Bing top 10 that already serves the query: a page written for the query
counts by source kind (major publisher 1.0, niche site 0.5, forum/video 0.35, other 0.2, retailer/brand 0.1), a page
not written for it a quarter of that. Bing's top 10 is a proxy for what ChatGPT retrieves, not the same set;
shortlisted clusters still go through `fastloop.py pack --engine api` + `vote` before a page is built.

**Brand-named queries.** Barry's 10-31 rule keeps brand and model names out of gap scoring (the brand's own pages make
them read falsely open). The general lanes follow it. The launch lane is the exception he asked for on 11-05: it is
reported separately and its coverage counts independent pages only.

## Network notes (work laptop)

- Google autocomplete `suggestqueries…client=firefox` 403'd after about 5,000 calls on 11-05;
  `www.google.com/complete/search?client=chrome` still answers. Google is paced at 0.4 s per call. A failed call is
  retried on the next run, never recorded as "no suggestions".
- Reddit refuses curl and its `.json` endpoints here; old.reddit HTML works in the Agent Chrome. Sitewide search
  matched seed words anywhere (AITA threads for "power strip"), so the lane reads each category's own subreddits
  (`brands.json` "subs"), top of the month.
- urllib threads hung in DNS/connect past their timeout and froze the pool, so `_get` shells out to curl with
  `--max-time`.
- Bing closed the connection to the Agent Chrome after about 300 results pages on 11-05 ("This site can't be
  reached"), and the later pages came back cut short. A reading with fewer than 6 organic results is discarded and
  fetched again on the next `supply` run. Plain curl gets decoy results (for "best" alone), so it is no substitute.
- Coverage is read on "best <lead>" when the lead has no choosing word. A bare noun ("hdmi extender") returns store
  pages and read as open, but ChatGPT rewrites shopper questions to "best <product> 2026".

## Run 2026-11-05 (first)

80 seeds → 59,856 suggested queries → 12,424 labelled → 3,235 buying-intent clusters (242 already covered by a page of
ours) → demand on 200 lead queries → coverage on 146, of which 33 are valid so far (Bing block). Shortlist and next
steps: DLC-168 in the to-do list; `runs/2026-11-05/report.md`. The three-model gap vote called 8 of 9 shortlisted
clusters open. It passes nearly everything (12 of 13 on 11-04), so demand and coverage do the selecting now and the
vote is only a last check against saturated results.

## Which pages to build first: value, not volume (2026-11-13, Barry)

From 10-29 to 11-13 the non-solar catalog (348 of 397 products) drew 71 of 151 page visitors but 14 of 237 buy-link
clicks and 0 of 10 sales; every sale was a $478-$1,791 ALLPOWERS or BLUETTI order carrying a cart-tested code
(`growth/reports/2026-11-13-product-mix.html`). Barry: steer new page building toward high-ticket, code-carrying
categories. `growth/evals/brandvalue.py` scores a cluster as uncovered searches x brand ticket (median store price in
`docs/offers.json`, clipped $20-$2,000) x 1.5 with a published code x 0.5 when the brand is Amazon-only, best brand
of the cluster. `gapmine.py daily` expands high-value brands' seeds first and queues clusters by value; a cluster
whose best brand's median price is under $150 is queued as `parked`, not built. `gappage.py next/research` build
`new` items in value order. Hand-picked clusters (abpage new-cluster harvests, brand onboarding) follow the same
rule: check `python3.12 growth/evals/brandvalue.py` before picking. The ticket is the brand's, not the cluster's
product, so a high-ticket brand's cheap accessory cluster still ranks high: skip those by hand.

## Running it

    python3.12 growth/evals/gapmine.py expand  --run <date>
    python3.12 growth/evals/gapmine.py reddit  --run <date>
    python3.12 growth/evals/gapmine.py news    --run <date> && python3.12 growth/evals/gapmine.py launches --run <date>
    python3.12 growth/evals/gapmine.py label   --run <date>
    python3.12 growth/evals/gapmine.py depth   --run <date> --top 150
    python3.12 growth/evals/gapmine.py supply  --run <date> --top 60
    python3.12 growth/evals/gapmine.py report  --run <date>

Each step resumes from its own output. Re-running `news` → `launches` weekly keeps the launch lane fresh. The general
lanes change slowly, so a monthly full run is enough.

## Search volumes (2026-11-05)

`report` ranks by **uncovered searches** = Bing US searches over the last 3 complete months, summed over the cluster's
variants, × (1 − coverage). Clusters below the reporting threshold, or without a coverage reading, follow by the proxy.

- **Source: Microsoft Advertising Ad Insight** (`gapmine.py msvolume`, client `tools/msads.py`): `GetHistoricalSearchCount`,
  1,000 keywords per call, all devices, US English. 11,865 queries in 12 calls, no throttling. Account: customer
  255121540 / ad account 187335032, no campaigns (nothing bills). Auth is Google OAuth (`IdentityProvider: Google`);
  the refresh token comes from `tools/msads_auth.py` and lasts 7 days while the Google app is in testing mode. Keychain:
  `msads-developer-token`, `google-oauth-msads-client-id`, `-client-secret`, `-refresh-token`.
- **Bing Webmaster Keyword Research API** (`gapmine.py volume`): same Bing data as impressions, one query per call.
  An undocumented daily cap stopped it after ~700 calls on 11-05 ("ThrottleUser" for 2.5 h+), so it is a cross-check only.
- **Calibration** (`gapmine.py volcal`): 3,175 queries both report. Spearman 0.83, log-Pearson 0.83, Webmaster ≈ 0.20 ×
  Ad Insight. The ranking uses one source (Ad Insight); don't mix raw counts from the two.
- Gap on 11-05: only 35 clusters have a coverage reading, while 213 clusters with >1,000 searches have none. Coverage
  (Bing top 10 through the Agent Chrome) is now the bottleneck, not volume.
