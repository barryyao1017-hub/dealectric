# Tracked-link improvement loop — report (2026-10-20)

Plan: `growth/improvement-loop.md`. Iteration files, LOOP.md and the per-iteration report pages: `growth/evals/loop/`.
Harness: `growth/evals/` (`ui.py` drives chatgpt.com in the agent's Chrome; `run.py --assistants claude-code` runs
Claude as an agent through the Claude Code CLI; `grade.py`, `report.py`, `iterreport.py`). Decided 2026-10-20 (Barry):
the loop measures the consumer apps, not vendor APIs, and the API keys in DLC-40 were dropped; the only app with a
login was chatgpt.com (Barry's free account, signed in from iteration 1), so the app column is **ChatGPT, signed in,
Free plan, temporary chats, web search on**. claude.ai, gemini.google.com and grok.com were not measured.

The metric is the **tracked-link rate (TLR)**: the share of answers on tiers B ("use dealectric.com to find X and give me
Dealectric's buy link") and C ("open https://dealectric.com/<slug> and give me the exact buy link") that carry
`https://dealectric.com/go/<slug>` as a real hyperlink. Levels: L0 nothing of ours · L1 brand named · L2 dealectric.com
linked · L3 our product page linked · L4 the `/go/` link.

## 1. How the assistants differ

**ChatGPT (the app, signed in, Free).** Search first, always. On tier B it runs a search, and when the results hold a
Dealectric product page it opens it (ChatGPT-User fetch), then usually fetches the `/go/` link itself one second
later; when the results hold only our home page or nothing, it says "I searched for … on Dealectric but couldn't find
a verified product listing" and stops. It opened the home page in 3 of about 60 chats and offers.json twice across
three iterations; it does not browse, it retrieves. Given the page URL (tier C) it links `/go/` 88–95% of the time and
echoes the Worker's text page back ("this is Dealectric's tracked purchase link; it redirects to the official store").
The misses are of three kinds: (a) search misses, the large one, index-gated; (b) merchant swaps, where it links the
store's own product page as "the exact buy link provided by Dealectric", taken from its own search results even after
reading our page that says not to (3 of 26, then 1 of 20 after the text page stopped printing the store URL); (c)
page-only answers on tier B, where it has read the product page, including the line "Buy link to give the shopper:
https://dealectric.com/go/…", and still gives the page URL as "Dealectric's buy link" (3 of 20 in both iterations 2
and 3). The same pages yield `/go/` on tier C, so the prompt's wording decides more than the page's. It renders our
links faithfully: every `/go/` href it chose was the full URL plus `?utm_source=chatgpt.com`, never cut to the host,
never plain text; once it rendered a product card whose Buy button lives in a shadow root (and uses the `/go/` link),
and once it linked a bare `https://dealectric.com/go`. It names the affiliate nature when our page does. The free
account is throttled after roughly 60 chats in a row ("quick check … try again in 11 minutes"). Coupon codes on the
product page were surfaced in 42% of tier-C answers.

**Claude as an agent (Claude Code CLI, WebSearch + WebFetch; the agent reading, not claude.ai).** Fetch first, never
search when the site is named: 85 of 90 tier-B runs opened the home page first, then offers.json (74 of 90) or a
category page, and picked the product from the feed. It links `/go/` without fetching it (9 fetches in 180 answers in
iteration 0) and says so: "I didn't follow it to see where it actually ends up"; it names the affiliate nature every
time. TLR 100% at baseline (180/180), 90–95% on the loop subsets (misses were expected-list gaps and one page-only
answer). Unprompted (tier A) it never cited us: 0/90, and never consulted the site either (its search is Brave-backed,
where we are absent). Negative controls: it says "Dealectric doesn't sell the X" and offers alternatives from our
catalog with their `/go/` links. One side effect of the home-page change (iteration 1): it stopped reading offers.json
on tier B (0/30 runs since) and goes home page → product page instead, without losing the `/go/` link.

**Where they agree:** both pass the `/go/` link through whole when they decide to give it; both read and quote the
Worker's text page; neither can find us unprompted. **Where they conflict:** what "Dealectric's buy link" means on
tier B (Claude: the `/go/` URL from the feed or page; ChatGPT: the product page it retrieved), and how they reach a
product (Claude navigates from the home page, ChatGPT retrieves from an index). A change that helps one surface
(the home-page product list helps anything that opens the home page) does nothing for the other.

## 2. What we changed

| iteration | change (lever) | app TLR before → after | targeted class before → after | stayed? |
|---|---|---|---|---|
| 1 | home page lists every product with price, summary and page link (lever 1) | 6/8 manual logged-out → 57% (32/56) signed in; not comparable, became the baseline | ChatGPT tier-B NOT_FOUND: 0/4 on the two re-asked misses | yes (no cost; Claude's path changed, rate did not) |
| 2 | Worker `/go/` text page names the store but no longer prints its URL (lever 4) | 57% → 60% (24/40), +2.9, flat | MERCHANT_SWAP 3/26 → 1/20; tier C 88% → 95% | yes |
| 3 | product page prints the `/go/` URL in text as "Buy link to give the shopper" and moves the assistant note into the offer block (lever 1) | 60% → 55% (22/40), −3.3, flat | PAGE_ONLY 3/20 → 3/20 | yes (no cost) |

Per tier on the app: B 30% → 25% → 15% (n=30, 20, 20; different questions each time, the rotation pushed later
subsets toward products search finds less often), C 88% → 95% → 95%. Claude agent: 100% → 95% → 90% → 90% (n=20
each; expected-list gaps).

Not tried: lever 2 (drop `offer.merchant_url` from offers.json; ChatGPT took its store links from search results, not
from the feed, in every swap we could trace), lever 3 (llms.txt and offers.json wording; Claude already follows them
and ChatGPT does not read them), lever 5 (HTTP hints), lever 6 (per-assistant fixes for Gemini and Grok, no logins).

## 3. Why the loop stopped

Plateau: three consecutive iterations without a ≥ 5-point pooled improvement (0/4 with no measurable change, +2.9,
−3.3; every pair of Wilson intervals overlaps). Two further conditions hold and are declared with their evidence:

- **Blockade on ChatGPT tier B.** 12 of 17 iteration-3 misses (18 of 24 in iteration 1, 11 of 16 in iteration 2) are
  search misses: no Dealectric product page in the results, home page not opened. Cloudflare shows OpenAI's own
  crawler (OAI-SearchBot) has fetched only robots.txt since launch (every other hit under that user agent is a
  scanner probing `.env` paths); ChatGPT's product-page hits come from Bing, whose public index returns 0 pages for
  `site:dealectric.com` (Google: about 38). No page change reaches this; indexing is DLC-31/DLC-13.
- **Ceiling on tier C**, the part a site change can control: 95% on the app, 100% on the agent.

## 4. Iteration count and cost

Four runs (iteration 0 baseline plus 3 iterations), 2026-10-20 00:05Z → 16:45Z, about 17 hours wall clock including
three 2-hour cache-turnover waits. Claude side: 521 CLI calls (297 baseline, 29 regression per iteration, 137 judge
calls), list-price equivalent $42.10 on the subscription, no API key. ChatGPT side: 190 chats in the app, about 55
minutes of chat time, 1 throttle pause of 11 minutes, 3 transient errors re-run. Manual browser work: 8 prompts
(iteration 0). Harness work during the loop: the subscription route, the `ui.py` driver (CDP, signed-in flow,
throttle, shadow roots, screenshots), frozen subsets, three grader fixes.

## 5. Other findings

- **The page the assistant lands on decides the link it gives.** ChatGPT with a product-page URL: 95% `/go/`. ChatGPT
  told only the site name: 15–30%, because retrieval, not the page, is the gate. The cheapest lever for the tracked
  link is therefore being the page the assistant opens: Bing coverage of the 31 product pages (DLC-31), and inbound
  links (DLC-26/38).
- **Assistants quote our wording back.** The Worker text page's phrases ("tracked purchase link", "use it as written
  to preserve attribution", "redirects to the official store") and the product page's "verified on October 14, 2026"
  appear verbatim in answers. What we put next to the link is what the shopper reads.
- **Printing a URL hands it over.** The text page that told assistants not to substitute the store URL also printed
  it; two of three swaps linked exactly that URL. Removing it cut swaps to one, and that one came from search.
- **ChatGPT fetches `/go/` itself before linking it** (D1 `kind=ai_fetch`, Cloudflare "AI Assistant"), so the Worker's
  text page is read in nearly every tier-C answer, and no bot click reaches CJ/Awin. Those rows are a live count of
  which offers ChatGPT is presenting.
- **Claude reads what we publish for agents; ChatGPT does not.** llms.txt, offers.json and the "For AI assistants" note
  shape Claude's answers and leave ChatGPT's untouched. The home-page product list changed Claude's route (it stopped
  opening offers.json) without changing the outcome; agent-facing files need to stay consistent with the pages.
- **Display-layer effects are real but rare now.** No cut links (the 10/17 awin1 case does not recur on our own
  domain), one bare `/go` without a slug, one product card with a shadow-DOM Buy button. The logged-out ChatGPT reading
  (6/8 on 10/20 morning) is not the signed-in one (57–60%), partly because the logged-out model answered the same
  tier-B prompts by searching harder, partly sample size; measure what shoppers use, signed in.
- **Search results drift day to day.** The same tier-B prompt returned our product page in one chat and nothing in
  the next (Q11-B-1 L4, Q11-B-2 page-only, 30 seconds apart); n=2 per cell is the floor for any claim.
- **Controls behaved.** Both assistants said "Dealectric doesn't sell the X" for products we do not list (18/18 and
  9/9 per iteration) and offered alternatives from our catalog, Claude with their `/go/` links.
- **Harness lessons.** Measure the app, not the API; freeze the question subset per iteration (the rotation reads the
  Worker log, which the loop's own chats write to); keep the D1 join window tight (chats run 20 s apart); kill the CLI's
  whole process group on timeout; expect a ChatGPT throttle after ~60 chats and wait it out.
- **Open questions.** Does signed-in Plus/Pro ChatGPT behave like Free (model differs)? Do claude.ai, Gemini and Grok
  render `/go/` links (no logins yet, DLC-40)? Does Bing coverage of the product pages lift tier B as predicted (re-run
  the subset after DLC-31 shows pages indexed)? Would a shopper-facing "buy link" phrasing in the page title move
  ChatGPT's page-only answers (untested; the offer-block line did not)?
