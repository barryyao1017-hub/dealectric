# Void scan — do high-demand, thin-supply product queries exist? (2026-10-24)

Thesis (Barry, 2026-10-24): Dealectric can be a site for agentic product discovery in whatever category has an opening,
not only the brands we have affiliate deals with today: find product queries that people search a lot but that the
index answers poorly, write the page that answers them, then look for an affiliate program for the brands it names.
This scan tests only the first step: **do such openings exist?** Affiliate availability is out of scope.

## Definitions (fixed before looking at the data)

- **Universe**: US product-discovery queries, i.e. the searcher wants to choose a product (best X, best X for Y, X vs Y,
  X under $N, alternatives to X). Harvested, not invented: for about 90 consumer category nouns across electronics,
  home, kitchen, outdoor, fitness, baby, pet, auto and tools, every query Bing Webmaster Tools → Keyword Research lists as
  related, question or newly discovered for the noun and for "best <noun>". An LLM keeps the discovery-intent ones and
  drops navigational (brand or store), informational and support queries.
- **Demand**: Bing US searches over 2026-07-24 to 2026-10-21 (exact match, the figure the tool lists). Queries below
  Bing's reporting threshold never enter, so the universe is the head and mid tail, not the long tail.
- **Supply**: Bing's top 10 for the query, read from the live results page (`serp.py`'s fetcher; Keyword Research's
  top-URL list was the first choice but the tool's quota cannot carry it). Each result is labelled by an LLM from
  title and URL: whether it is **dedicated** (written to answer this query: a "best X for Y" list or "A vs B" page that
  matches the query's qualifiers, not a broad "best X" list or a store page) and its **source kind** (major publisher
  such as Wirecutter, RTINGS, Consumer Reports, CNET, Tom's Guide; niche site; retailer; brand; forum or video; other).
- **Opening**: demand at or above the median of the discovery universe, **and** dedicated results below the universe's
  mean, **and** no dedicated result from a major publisher.
- **Thesis holds** if at least 5% of discovery queries, and at least 10 queries, are openings, and a live check of a
  sample confirms them: the live Bing results agree, and an assistant asked the shopper question behind it searches and
  gets a result set no better than the scan says.

## What this cannot show

- Whether Dealectric could rank there. The 2026-10-24 narrowing test (query-pages.md) found a thin result set does not
  by itself get a new domain retrieved; an opening is necessary, not sufficient.
- How often the assistants issue these queries (nobody reports it). Bing demand is people typing into Bing.

## Result (first pass, 2026-10-24)

**Verdict: openings exist and are real when you look at them, but in electronics they are rare, cheap and small.** The
fixed rule passes on paper (13 of 117 scored discovery queries, 11%), but 9 of the 13 are artefacts. On a stricter
reading, 2 queries above median demand are openings (about 2%), short of the 5% bar. Coverage is 20 of the 90
categories, all electronics and home tech, which is the most publisher-saturated part of shopping, so this does not
yet test the thesis across categories.

What the pass covered: 20 seeds (wireless earbuds through video doorbell) → 877 queries with US Bing demand → 146
discovery queries (LLM-labelled) → 117 with at least 5 Bing results scored. 21 queries could not be fetched because
Bing closed the connection (all keyboards, gaming mice and portable monitors). Keyword Research then returned 429
TooManyRequests after about 120 calls and was still blocked 20 minutes later, which stopped the harvest at seed 20.

**Supply rises with demand.** Mean dedicated results in the top 10, by Bing US searches over 3 months: 5.2 (under 100),
6.1 (100–500), 7.5 (500–5,000). Major publishers per top 10: 4.2, 6.0, 7.2. Measurable head and mid-tail demand is
already served.

**The 13 rule-openings, inspected:**

| query | Bing US searches, 3 mo | dedicated | major publishers | verdict |
|---|---|---|---|---|
| fitbit watches for women | 709 | 3 | 1 | **opening**: 5 retailer pages, 3 small sites |
| vertical laptop stand | 348 | 1 | 1 | **opening**: 6 retailer pages |
| laptop stand for bed | 181 | 1 | 0 | **opening**, just under median: 7 retailer pages |
| foldable laptop stand / wooden laptop stand | 66 / 37 | 0 / 0 | 0 / 0 | opening, small: retailers and brands only |
| best headphones and earbuds, premium noise cancelling headphones, best buds, sound bar(s) for tv, best home security camera system | 216–104,272 | 0–2 | 3–9 | artefact: served by broader lists from major publishers that the strict "dedicated" label did not count |
| popular fitness trackers this season | 15,186 | 2 | 4 | artefact: an odd Bing-generated phrase, served by majors |
| tablets on sale / tablets for sale | 2,762 / 325 | 0 | 0 | transactional: retailers are the right answer |
| adjustable laptop stand, portable screen for laptop | 223 / 251 | 0 / 1 | 2 | borderline: retailer-heavy, but majors' broad lists rank |

**The assistant sees the void, and sees it as junk rather than emptiness.** I asked Claude (Sonnet 5.5, CLI with web
search, which is Brave-backed; n = 1 each; `runs/2026-10-24-voidscan/assistant/`) the shopper question behind three
openings and one saturated control:
- *Vertical laptop stand*: its search returned AI-written roundups on throwaway blog hosts (digitalpress.blog,
  mataroa.blog), a keyword-research page and broad "best laptop stand" lists. Its top pick cited one of those roundups,
  and prices came from Australian and Swiss shops and an old MSRP.
- *Fitbit for small wrists*: spam pages on hijacked domains (`?p=157182` on apperta.org, automerge.org,
  truckwriters.com), then retailer listings. Claude said its searches "turned up only partial information".
- *Laptop stand for bed*: two AI-written blogs, but also Reviewed.com and The Sleep Judge. It built its answer on
  Reviewed, so this one is thin but not empty.
- *Control, wireless earbuds*: RTINGS, What Hi-Fi, Tom's Guide, SoundGuys; a confident, well-sourced answer.

**Reading.** In electronics, openings sit where publishers don't bother: low-price accessories and qualifier variants
(laptop stands, Fitbit for women) whose Bing results are store listings. That is probably economics: a $30 stand pays
a publisher little commission, the same constraint we would face. On the assistant side the gap is a quality gap: the
agent finds pages, but they are generated spam, and it says so or quietly cites them. A dated, specific, honest
comparison page would be the best thing in that result set. Whether it would rank there is the separate question the
narrowing test left open.

**Next.** (1) Finish the other 70 categories (home, kitchen, outdoor, fitness, baby, pet, auto, tools) once Keyword
Research's quota resets; those are less covered by the big labs, so they are the real test. (2) Score with the stricter
rule (no more than 1 major publisher anywhere in the top 10, transactional queries out), set before the new data
comes in. (3) Run the assistant check on ChatGPT too, n = 2 per opening.

## Files

`growth/evals/voidscan.py` (harvest → supply → classify → report), run folder `growth/evals/runs/2026-10-24-voidscan/`.

## Log
- 2026-10-24: method fixed; `voidscan.py` written. Harvest stopped by Keyword Research's 429 quota at 20 of 90 seeds
  (877 queries). Intent: 146 discovery. Supply: live Bing pages (Keyword Research's top-URL list is under the same
  quota); Bing closed the connection on 54, a slower re-run filled 33. Labels: 3 Claude CLI passes, spot-checked on 4
  queries. Report: 13 rule-openings, 9 artefacts on inspection, 2 above median on a strict reading. Assistant check on 3
  openings plus 1 control (Claude CLI, n = 1).
- 2026-10-27: the stricter rule fixed in `report()` before new data (at most one major publisher anywhere in the top
  10, no transactional query); on the first pass it keeps 2 of 13 openings, the same 2 the inspection kept. Second
  harvest: 20 -> 51 of 89 seeds (2,173 queries) before the 429 quota, at "treadmill"; 38 seeds left, about two more
  days of quota. Scored together: 262 discovery queries, 19 openings by the original rule (7.3%), **4 by the strict
  rule (1.5%), below the 5% bar**: desk chairs for home (1,215 searches; only 5 retailer results came back, so
  probably a fetch artefact), fitbit watches for women (709), vertical laptop stand (348), extra screen for laptop
  (243; fits Mobile Pixels, an approved CJ program). ChatGPT check (signed in, n = 2, plus the earbuds control;
  `runs/2026-10-24-voidscan/assistant/chatgpt-*.json`): ChatGPT never searches the narrow query. It searches the head
  term ("best ergonomic office chairs 2026 ... reviews", "best portable monitors for laptop 2026"), and those results
  carry Tom's Guide, TechRadar, Wired, RTINGS, Consumer Reports and Tom's Hardware, so three of the four strict
  openings are not openings from ChatGPT's side. Vertical laptop stand stays thin (Wired, once also Tom's Guide).
  ChatGPT cited only stores and brands in every answer, the control included. Reading so far: the thesis does not
  hold on the strict rule, and assistants' query rewriting closes most gaps that exist at the query level.
