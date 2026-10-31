# Paste calibration (DLC-115, phase A)

Goal: make the fast loop's replay hand over our buy link (M1) about as often as real ChatGPT does, so that drafts can
be iterated on M1 (DLC-116). The replay pastes the shopper's question plus the result set a recorded real chat got
into a fresh Free temporary chat (search off) and asks for an answer; `fastloop.py pastecal` runs it,
`fastloop.py pastecalreport` scores it. Runs: `growth/evals/runs/2026-10-31-pastecal/<engine>-<fmt>-<paste>-<set>-r<rep>/`.

## Metrics

Over answers with at least one link:
- **M1, buy-link share:** answers that link our `dealectric.com/go/` link. This is the metric we optimise.
- **M2, our-page share:** answers that link dealectric.com at all.
- **M3, link share:** our links divided by all links.

What counts as a link:
- **Real side:** in-text links plus source pills. Shopping-card and image links are excluded.
- **Replay side:** every link written, plus any `turn0search<i>` citation the model writes, mapped to that result's
  URL.

## Calibration set

- **Pool:** recorded real chats that meet all of these:
  - signed in, answered by gpt-6, one search;
  - our page in the results;
  - the prompt doesn't name us;
  - the run's system prompt doesn't ask for links. This excludes the `2026-10-27-p3iter05` chats, whose system prompt
    said "give the shopper a clickable link to buy it".
- **The pool has 195 chats.**
- **Real M1 is rare: 9 of 195 (4.6%).** Real M2 is about 69%.

The set is stratified on real M1 (`runs/2026-10-31-pastecal/split.json`, seed 11):
- **Tuning set:** 6 real hand-overs plus 24 without.
- **Held-out set:** 3 hand-overs plus 8 without.

Every metric is reweighted to the pool's 4.6% base rate. The report also shows the replay's hand-over rate on real
hand-over chats (sensitivity) and on the others (false positives).

## What the replay model is shown: confirmed vs assumed

| Element | Status | Evidence |
|---|---|---|
| Page text from OpenAI's stored copy, not the ~200-character UI snippet | confirmed | needle tests, `growth/focus/context-probe.md` |
| One shared text budget per search: higher ranks get more, long pages cut to passages matching the query, ceiling ~16–23k characters | confirmed (approximate sizes) | budget and grid tests, same file |
| Result order = the order of the recorded `search_results` | confirmed | stream order |
| About 12 web results per search, sometimes news | confirmed | 324 chats |
| Results are cited internally as `turn<N>search<i>` | confirmed | the app's answer program (`<Cite refs={["turn407078search0"]}/>`) |
| Each source starts with a citation-marker line (`citeturn0search0`), then `Title:` / `URL:` / `Updated:`, then line-numbered text (`[L1]`, `[L2]`) | documented by OpenAI for developers; assumed to mirror ChatGPT's tool | developers.openai.com, Citation Formatting |
| Publish date shown per result | assumed | `pub_date` in the stream metadata |
| Results grouped by domain | unknown | the stream groups them for the UI; not included in v1 or v2 |
| Exact passage boundaries | approximated | 500-character chunks by query-word overlap |
| ChatGPT's system prompt and tool instructions | unknown | the paste's wording stands in |

Formats (`fastloop.py`, `FORMATS`):
- **v1:** `【i】 title` / `URL:` / passages, under a `Results for "<query>":` line.
- **v2:** OpenAI's documented layout: citation-marker line, Title, URL, Updated, `[L#]` lines, under
  `Search query: "<query>"`.

## Rounds (tuning set, 30 chats; metrics weighted to the 4.6% base rate)

Sensitivity is the replay's hand-over rate on the 6 real hand-overs. False positives is its rate on the 24 chats
without one.

| # | Engine | Change from the previous best | M1 real / replay | Sensitivity | False positives | M2 real / replay | M3 real / replay | Kept? |
|---|---|---|---|---|---|---|---|---|
| 0 | API (gpt-6.1-sol), paste as user message | baseline: v1 layout, c1 paste | 5% / 6% | 1/6 | 1/24 | 64% / 54% | 17% / 25% | baseline |
| 0b | same | repeat of round 0 (noise) | 5% / 5% | 1/6 | 1/24 | 64% / 45% | 17% / 22% | n/a |
| 1 | same | v2 layout (citation markers) | 5% / 1% | 1/6 | 0/24 | 64% / 96% | 17% / 28% | no: M2 overshoots (cited results mapped to our page) |
| 2 | same | Luna instead of Sol | 5% / 0% | 0/6 | 0/24 | 64% / 50% | 17% / 33% | no: links in only 2 of 30 answers |
| 3 | same | c2 paste (results framed as the model's own search) | 5% / 5% | 1/6 | 1/24 | 64% / 60% | 17% / 26% | no gain over noise (M2 per-chat agreement 53%) |
| 4 | API, results as the model's own web_search output, no system prompt | delivery mode | 5% / 0% | 0/6 | 0/24 | 64% / 40% | 17% / 20% | no |
| 0 | App (gpt-6, temporary chat) | baseline: v1 layout, c1 paste | 5% / 40% | 6/6 | 8/24 | 64% / 65% | 17% / 36% | baseline |
| 1 | App | v2 layout (24 of 30 so far) | 5% / 36% | 6/6 | 6/18 | 74% / 84% | 19% / 30% | pending |

Noise: two API runs of round 0 agree per chat on M1 30/30 and on M2 21/30 (70%). The app's own repeatability (live
re-asks of the 30 tuning questions with search on) is being measured: run `2026-11-01-pastecal-reask`,
`fastloop.py reaskreport`.

So far:
- **The API engine plateaus at round 0** (three rounds with no gain over 5 points). It matches real M1's rate, but
  only because it rarely hands over at all: it caught 1 of the 6 real hand-overs.
- **The app engine hands over about 8 times too often.** It hands over on every real hand-over chat and on a third of
  the others. Likely cause: pasted pages are the user's own text, so the model copies the `/go/` URLs freely, where a
  real search cites results as source pills.
