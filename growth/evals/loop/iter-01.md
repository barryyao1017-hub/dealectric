# Iteration 1 — home page names every product (2026-10-20)

## Diagnosis (from iteration 0)

The API assistant (claude-code) is at 100% L4 on tiers B+C, so nothing to fix there. The only non-L4 answers are
ChatGPT's two tier-B misses out of four (NOT_FOUND): its search returned the dealectric.com home page but not the
product page, and it answered "couldn't find a verifiable product listing". The home page named six brands and no
products. Cloudflare's request log shows ChatGPT-User opened the home page live once during the spot-check (00:05Z),
and OpenAI's search crawler (OAI-SearchBot) last fetched `/` on 2026-10-18 15:21Z.

## Hypothesis and expected movement

Lever 1 (wording and placement) applied to the home page: list every product by category with its name, verified
price, one-line summary and page link, generated from the same data as offers.json. If ChatGPT opens the home page
it finds the product; once OAI-SearchBot re-crawls `/`, the snippet names it. Expected: ChatGPT UI tier-B misses fall
(Q25-B, Q27-B become L3/L4) once the page is re-crawled; no change on claude-code (already 100%); no change on
tier C. Written before the change.

## Change

Commit `efd82c6` (`loop-1:`), 08:04Z: `src/build.py` `product_index_html()` + a "Every product live now" section in
`src/content.py`; rebuilt; `docs/offers.json` changed only its `generated` date; Worker unchanged (links map
identical), no deploy. Live on dealectric.com at 08:06Z.

## Re-evaluation design (re-centred on the apps, Barry 2026-10-20)

Primary: `ui.py --app chatgpt --loop --iteration 1 --n 2` (10 rotated questions × tiers B, C × 2 chats, plus the
controls) in the agent's Chrome, logged out. Direct before/after on the lever: Q25-B and Q27-B re-asked (×2), the two
iteration-0 misses. Regression check: `run.py --assistants claude-code --loop --iteration 1 --n 1`. Loop subset:
Q08, Q09, Q11, Q14, Q17, Q24, Q26, Q28, Q29, Q30 (all slugs fresh in D1). Wait: ≥ 2 h after 08:04Z.

## Re-evaluation

_(filled in after the wait)_
