# Daily $0 cluster discovery and page pipeline: plan (2026-11-05, DLC-168)

Barry, 11-05: "Build the cluster discovery function with zero cost, limiting each source to zero dollars, and we're
gonna automate this process to run every day and generate pages as well."

## Pipeline

    seeds (every approved brand's categories, brands.json)
      → expand: Google/Bing/Amazon autocomplete (free, paced)              gapmine.py expand
      → label + cluster: claude -p, no tools (plan usage, $0)                gapmine.py label
      → volume: Microsoft Ads Ad Insight, 1,000 keywords/call ($0, no campaigns)   gapmine.py msvolume
      → filter: cluster searches ≥ 500 / 3 months
      → coverage: capped free SERP sources (below), labelled by claude -p   gapmine.py supply --source auto
      → gate: coverage < 0.4, ranked by uncovered searches                   gapmine.py report → queue.json
      → page: research → verify against stores/Amazon → record → build → fastloop check → docsguard → push
      → measure: OAI-SearchBot fetch within 7 days, GSC indexed share, AI-referred landings per page

## Coverage sources and caps (each stops on its cap or on any 401/402/403/429/quota reply; never paid)

| source | free allowance (provider page, 2026-11-05) | renews | daily cap in code | engine |
|---|---|---|---|---|
| Claude WebSearch (`claude -p --tools WebSearch`) | plan usage, no $ | — | 60 queries | Anthropic's search (not Bing) |
| Tavily | 1,000 credits/month, no card; blocked at 0 | monthly | 30 (basic search = 1 credit) | own index |
| SerpApi | 250/month, 50/hour | monthly | 8 | `engine=bing` (real Bing results) |
| Serper | 2,500 queries on signup, no card | one-time | 100 until spent, stop at 2,400 | Google |
| Jina s.jina.ai | 10M tokens per key, ≥10k tokens/search (~1,000) | one-time | 50 until spent | own |
| Bing through the Agent Chrome | free, blocks after ~300 pages | — | 40, 6 s apart | Bing |

Renewing total ≈ 60 + 30 + 8 + 40 ≈ 140 readings a day; one-time Serper/Jina clear the 213-cluster backlog.
Every call is appended to `growth/gapmine/ledger.jsonl` (date, source, query, status, results); the daily log prints
used/cap per source. A source whose coverage doesn't track Bing's (Spearman < 0.5 on the 35 Bing-scored clusters) is
not used for gating.

## Conflicts to settle (Barry)

1. **The gap vote and `pack --engine api` are not $0**: they call the OpenAI API. The daily run drops the vote (coverage
   < 0.4 is the gate; the vote and coverage agreed on 11-05) and builds the check's result set from the free SERP
   reading instead of an API pack.
2. **Page research uses Claude plan usage.** Today's six pages took ~1.3M subagent tokens plus hand-checking. Unattended
   that is $0 but competes with Barry's other Claude usage. Proposed cap: 3 pages a day, raised if the plan's weekly
   limit holds.
3. **Unattended pages need the checks I did by hand today**, as code: maker-store price and spec re-read (Shopify
   `.js` / search endpoints), Amazon title check by ASIN, Amazon-vs-maker price comparison (link the cheaper honest
   route), no prices next to Amazon links, no duplicate price tokens. 11-05's research had three such errors.
4. **Auto-publish before evidence.** Volume-picked pages (x20, x21) are 0–1 days old; DLC-171/172 read them 11-15/16.
   Recommendation: run discovery daily now, queue pages as drafts, switch auto-publish on after the 11-16 reading.
5. **Schedule.** The charter says no new scheduled tasks. Proposal: no new job; `tools/codesweep.sh` on the old Mac
   calls `gapmine.py daily` after the sweep commits, inside its existing 06:37 run. Needs Barry's yes.
6. **Microsoft Ads token.** Scopes are `openid profile email` (non-sensitive), so publishing the Google OAuth app to
   "In production" needs no Google review and stops the 7-day expiry. Barry clicks Publish (steps in DLC row). Until
   then the daily run logs `msvolume: token expired` and skips volume (the daily report shows it).

## What is built (2026-11-05)

- `growth/evals/serpsources.py`: the six sources above with caps, keychain keys, ledger, stop-on-quota.
  `python3.12 growth/evals/serpsources.py status` prints used / cap per source.
- `gapmine.py seeds`: widened 42 brands from 80 to 489 seeds (Claude from the brand's range; Shopify `/products.json`
  answered 429 on the work laptop, so store titles weren't used there).
- `gapmine.py srccal --source <s>`: a source's coverage vs Bing's on the Bing-scored queries (Spearman, gate agreement).
- `gapmine.py daily`: seeds → 8 new seeds expanded → label → Ad Insight volume (logs a failure, doesn't stop) → capped
  coverage for the biggest unscored clusters ≥ 500 searches → gate (coverage < 0.4) → `growth/gapmine/queue.json` →
  `growth/gapmine/daily/<date>.md` with used/cap per source. Runs in `growth/gapmine/runs/pool`.
- `tools/gappage.py next [--publish]`: research (`claude -p`, Fable, WebSearch/WebFetch + read-only
  `tools/storecheck.py` / `tools/amzcheck.py`, recipe `growth/gapmine/page-recipe.md`) → JSON draft → code checks
  (approved program, ASIN title on Amazon, no Amazon prices, tokens resolve, must phrases in the lead) → insert →
  images → build → docsguard → `fastloop check` 1/3/6 on a pack built from the free reading. Without `--publish`
  the draft is stored in `growth/gapmine/drafts/` and src/ restored; with it, commit + push + Worker + IndexNow.
  Cap: 3 pages a day.

## First run, 2026-11-05 (work laptop)

- **Claude WebSearch can't gate.** On the 54 Bing-scored queries: Spearman 0.29, the < 0.4 gate agrees on 27/54 (chance),
  and it reads 37 clusters open against Bing's 18 (its results are spam-heavy roundups). Only Bing-backed sources gate
  (`serpsources.GATING`: SerpApi `engine=bing`, Agent Chrome Bing); the rest join after `srccal` ≥ 0.5 (DLC-176).
- **Free Bing capacity is the binding limit.** The Agent Chrome got 5 valid readings out of 39 (Bing cuts its pages
  to 2–5 results); DuckDuckGo's HTML endpoint answers with a bot challenge. Until SerpApi's key exists (DLC-173) the
  pipeline gets about 5 usable coverage readings a day, which at today's ~8% pass rate is a page every few days.
- **Microsoft suspended the Ads account** (401 code 105 on every call, user-level included; reinstatement and identity
  emails from adctr@microsoft.com on 11-05). Barry reinstates it (DLC-178). Until then `growth/gapmine/msads_blocked.json`
  stops the daily run from calling it, and new variants get Bing Webmaster counts × 5 (≤ 300 calls a day).
  **Never create a campaign on that account**: a $500 "when you spend" promo was redeemed; it is free only while no
  campaign exists.
- Daily pass: 8 seeds expanded and labelled (10 `claude -p` calls), 39 Bing readings, 3 clusters queued
  (bluetooth speaker for car, smartwatch standalone calls, mechanical vs membrane), log in `daily/2026-11-05.md`.

## Hook (applied 2026-11-05, Barry's yes; no new scheduled task)

`tools/codesweep.sh` on the old Mac runs, after `codesweep.py` and only when the sweep exited 0 with `src/`, `docs/`
and `worker/src` clean (gappage.py's restore uses `git checkout`, which would discard sweep work):

    gapmine.py daily  →  gappage.py next [--publish if growth/gapmine/AUTOPUBLISH exists]
    →  commit "gapmine: daily run <date>" of growth/gapmine + the new packs, push

The log gets `gapmine start` / `gapmine end (daily exit N, page exit N)` lines; the sweep's own end line and exit code
are unchanged, so `dailyupdate.py` reads the sweep as before. Auto-publish is off until Barry creates `AUTOPUBLISH`
(recommended after the 11-16 reading, DLC-172). The sweep reads `codesweep.sh` before its own `git pull`, so the first
run with the hook is the morning after the clone first pulls this commit (11-07 06:37 at the latest).

Not verified from the work laptop (DLC-177 checks it on the first hooked run): `claude` on launchd's PATH and logged in
on the old Mac, and the `bing-webmaster-api-key` keychain item there (without it the Webmaster fallback logs a failure
and volume is skipped). `dailyupdate.py` would add one line from `growth/gapmine/daily/<date>.md` (DLC-177).

## Barry's signup steps (never done by Claude; keys go in the keychain)

Tavily (tavily.com → Sign up → dashboard → copy API key), SerpApi (serpapi.com → Register → verify email → Dashboard
→ API key), Serper (serper.dev → Sign up → API key), Jina (jina.ai → API → "Get API key"). Then, per key:

    security add-generic-password -a dealectric -s tavily-api-key -w '<key>'
    security add-generic-password -a dealectric -s serpapi-api-key -w '<key>'
    security add-generic-password -a dealectric -s serper-api-key -w '<key>'
    security add-generic-password -a dealectric -s jina-api-key -w '<key>'

(on the old Mac too, since the daily run lives there).
