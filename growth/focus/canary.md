# DLC-77 canary: what of a page does OpenAI's stored copy hold?

Question: does the copy ChatGPT reads (OpenAI's stored copy, refreshed by OAI-SearchBot) hold the page's text past
the title and opening, and is the passage a result carries picked by the query? Two cases on 2026-10-28 suggest yes
(`stored-copy-step2.md`, "What the stored copy holds"); this tests it.

## The line

Shipped 2026-10-28 as the last section of `/about` (the deepest text on the page: it starts 1,517 characters into the 1,848-character main
text), wording found nowhere else on the site. Title and description unchanged. True, dated, written for people:

> **How codes are re-tested.** Since 2026-10-27 the check has run unattended every morning at 06:37 Pacific time: each
> published code goes into the brand's own US cart on every product it applies to, next to a made-up control code
> the store must reject. A code the store rejects on two mornings in a row comes off every page the same day.

Why /about: it's in no W3 arm and on no arm's shared surface; OAI-SearchBot has crawled it (once, 2026-10-21); a known
query ("what is dealectric.com") retrieves it; and its 10-28 answer already relayed text from the middle of it.

## Reading (queue row 9, W1 runs it)

`growth/focus/canary-questions.json`, n=2, 6 chats, signed in, fresh temporary chat each, W1's driver
(`visibility_scan.py --questions growth/focus/canary-questions.json --n 2 --run-id <date>-canary`). At least 15
minutes between canary chats (ChatGPT reuses a page it fetched live for the next few minutes), interleaved with scan
cells. Gate: queue it once `python3.12 growth/evals/canary.py --gate` shows an OAI-SearchBot fetch of /about after the
ship. If none by 2026-11-04, run it anyway: a relay without that fetch would show another feed.

Score: `python3.12 growth/evals/canary.py growth/evals/runs/<date>-canary`. Only cells with no OpenAI request to
/about from 30 minutes before the chat to its end count.

## What each outcome means

- Clean cells relay the canary: the stored copy holds the page to its end; Step 2 has to make every section carry
  the deal on its own.
- /about in the results, snippet saved, canary in the snippet for `howtest`/`retire` and not for `whatis`: the
  passage is picked by the query.
- /about in the results, snippet is the opening for every query, no relay: only the opening reaches the model; the
  10-28 bio relay came from somewhere else; Step 2's title-and-opening draft is the whole job.
- ChatGPT fetches /about live in most cells: the questions draw a live fetch, so they test nothing about the stored
  copy; rephrase.

## Result

2026-10-29, before the canary reading: the snippets ui.py now saves answer most of the question. In 31 of our 116
results in W1's overnight scan (2026-10-28 23:30Z to 10-29 04:10Z), ChatGPT's result carried a snippet: about 200
characters (median 202, max 203), a passage picked for the query from anywhere in the page OpenAI crawled. On
`/products` the passages started 960, 5,398, 7,224 and 10,961 characters into the page; on `/discount-codes` 2,747;
on `/` 1,400 and 2,525 (each the card or table row for the product asked about). On product pages, deal and worth
questions got the opening of the page body (breadcrumb, H1, summary, start of the offer card), not the meta
description. So the stored copy holds the full text and the model sees the title plus one 200-character passage per
result. The canary reading still checks whether an answer can use text beyond that passage (gate: OAI-SearchBot
re-fetching /about, not yet as of 10-29 07:30Z).
