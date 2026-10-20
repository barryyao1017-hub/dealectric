# Iteration 0 — baseline (2026-10-20)

Route: the four API keys do not exist yet (DLC-40), so the API column is **claude-code** (Claude as an agent through
the Claude Code CLI under the claude.ai subscription; `growth/evals/README.md`, "Subscription route") and the UI
column is **ChatGPT logged out** at chatgpt.com in the Claude desktop browser pane (the Chrome extension was not
connected to the agent's Chrome; same method otherwise: fresh chat per prompt, `?hints=search&q=…`, hrefs read from
the DOM). claude.ai, gemini.google.com and grok.com have no login in agent-vault, so no UI reading for them.

Stamp: run `2026-10-20-iter00`, site commit `d32a405853` (content identical to `0651de4d44`, the last site change;
the commits since only add `growth/`), Worker `dd17f131` deployed 2026-10-18T10:05:59Z, Google `site:dealectric.com`
≈ 38 results, Bing `site:dealectric.com` 0 results (public search proxies; the GSC/Bing dashboards were not opened).
Window 2026-10-20T00:05Z → 07:54Z (a hung-process stall, fixed in `e9e8e2d`, stretched it; 3 cells hit a DNS blip
and were re-run). 297 calls (99 prompts × 3), list-price equivalent $32.69 on the subscription.

## Numbers

| reading | claude-code | ChatGPT UI (logged out) | pooled |
|---|---|---|---|
| **TLR L4-api, tiers B+C** | **100% [98–100] (180/180)** | – | 100% (180/180) |
| L4-api tier B / tier C | 100% (90/90) / 100% (90/90) | – | |
| **TLR L4-ui, tiers B+C** | – (no claude.ai login) | **75% [41–93] (6/8)**; B 2/4, C 4/4 | 75% (6/8) |
| discovery (tier A, L2+) | 0% (0/90) | not run | |
| our brand named (tier A) | 59% (53/90) | | |
| bypass (B+C) | 0% (0/180) | 1/8 (Q27-B, merchant page) | |
| coupon surfaced (C) | 19% (17/90) | 1/4 (Q27-C, AFSC20) | |
| rank among picks (A+B, judged) | top-1 84 / top-3 103 of 113 | | |
| controls | 9/9 pass (3 runs each) | | |

Before two harness fixes made during this iteration the raw numbers were 177/180 and 5/8; see "Harness decisions".

## Failures (non-L4 on tiers B+C)

| class | claude-code (api) | ChatGPT (ui) |
|---|---|---|
| NOT_FOUND | 0 | 2 (Q25-B, Q27-B) |
| PAGE_ONLY / MERCHANT_SWAP / NETWORK_HOP / REFUSED / STALE_CACHE / PLAIN_TEXT | 0 | 0 |
| OTHER | 0 | 0 |

ChatGPT, in its own words:
- Q25-B (Tenergy 8-bay charger): "I searched for AA/AAA NiMH battery chargers on Dealectric, but I couldn't find a
  verifiable product listing on their site, so I can't confidently provide a direct Dealectric buy link." Linked the
  dealectric.com homepage and a Tenergy TN438 at rocketdistributing.com.
- Q27-B (headphones under $100): "I couldn't find an indexed result from Dealectric.com that I can verify. I don't
  want to give you an unverified Dealectric buy link." Named our exact product (Soundcore Space One, $84.99) and
  linked us.anker.com.

Both are search misses: ChatGPT searched, got our homepage in the results but not the product page, and did not open
the homepage to look. Q04-B and Q19-B, where its search did return the product page, were L4.

## What the two assistants do (D1 `clicks`, transcripts)

- **claude-code never searches on tier B**: 85 of 90 tier-B runs open `https://dealectric.com` first, then
  `offers.json` (sometimes a category page), and pick the product from the feed. 0.23 searches per tier-B run, 0.01
  on tier C, 1.9 on tier A. Median latency 31 s (B), 11 s (C).
- **claude-code links `/go/` without fetching it**: only 2 distinct `/go/` fetches (9 runs) in 180 B+C answers, all
  the rest linked the `/go/` URL straight from the page or feed. Typical prose: "The link goes through Dealectric's
  `/go/` redirect, which should send you to BLUETTI's store. I didn't follow it to see where it actually ends up." It
  names the affiliate nature every time ("It may be an affiliate link").
- **ChatGPT fetched every `/go/` link it then showed** (5 ai_fetch rows, UA ChatGPT-User, Cloudflare "AI Assistant"),
  received the Worker's text page, and echoed its wording back: "use it as written to preserve Dealectric's referral
  attribution", "Dealectric advises using its tracked link rather than substituting the merchant URL". No merchant swap
  and no awin1/tkqlhce hop in 6 answers that reached the page (the 10/18 probe had 2 of 5 swaps before the text page).
- Tier A (unprompted) stays at 0/90 citations for claude-code; it never consulted our site either (0 consulted_ours),
  so this is a search-index gap, as the plan expected.

## Harness decisions made in this iteration

1. **Q19 expected list widened** to every listed station with a UPS spec (Elite 200 V2, AC180, Elite 300, Elite 30
   V2, AC200L, P1800, R600). The three "misses" were `/go/` links to the Elite 300, Elite 30 V2 and P1800 for a UPS
   question, all correct picks; ChatGPT's UI answer chose the Elite 300 too. Run files and `questions.yaml` updated,
   rows rescored (`grade.py --rescore`, new flag).
2. **Negative-control rule refined**: pass = no invented `/go/` slug and (nothing of ours presented, or the answer
   says outright that Dealectric does not list the product). The three "failures" were honest answers ("Dealectric
   doesn't sell the Anker Prime 26K … here are the power banks it does carry", with product-page or `/go/` links to
   our catalog). An answer that presents a `/go/` link as the asked product still fails.
3. `run.py`: the CLI call runs in its own process group and is killed whole on timeout (600 s); the first pass had
   four `claude -p` processes hung for hours.

## Decision

Baseline recorded. On the measured API assistant the metric is already at the ceiling (100%), with no addressable
failure class. The only non-L4 answers are ChatGPT's tier-B search misses (NOT_FOUND), which the plan treats as
index-gated for tier A; on tier B there is one site lever left to try before calling it a blockade: ChatGPT does get
the homepage in its search results, and the homepage names brands but not a single product. Iteration 1 tests whether
a homepage that names every product (linked) turns those misses into finds.
