# Gap-page retrieval check, 2026-11-07 (Barry's request)

Each published gap page's own query (gapmine backfill title query, queue supply query, else the title) run as one
pinned OpenAI web search (`gapcheck.py`, Responses API web_search, gpt-6-luna, US): does dealectric.com come back?
159 of 173 calls ran a search (14 returned no search and are excluded).

| pages | searched | own page top 3 | own page top 12 | absent |
|---|---:|---:|---:|---:|
| solar / power | 68 | 50 | 62 | 5 |
| other | 91 | 31 | 58 | 31 |
| all | 159 | 81 | 120 | 36 |

By publish date: Nov 3 pages 71/72 in the top 12, Nov 4 24/24; Nov 5–7 pages 11/45 (newer, and gap-mining pages aim
at broad Bing head terms).

App calibration: 12 of them as pinned one-search chats in the ChatGPT app (Agent Chrome, packs
`runs/fastloop/gapapp-1107-00..11`). Presence agreed 12/12: the 9 the API found were rank 1 in the app; the 3 it
missed (best rechargeable aa batteries, travel router with vpn, iphone 17 25w wireless charging) were absent there too.

Reading: for the exact query a page was written for, retrieval is not the bottleneck. Contrast with 150 broad category
queries on 11-06 (`growth/gapmine/runs/pool/srccal_openai.json`): one dealectric.com hit in 1,500 results. So the open
questions are demand (do shoppers' questions become these queries?) and hand-over (does the answer give our link?).
