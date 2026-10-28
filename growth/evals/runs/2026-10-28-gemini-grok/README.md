# Gemini and Grok app check, 2026-10-28

Manual run in the agent's Chrome (no `ui.py` driver exists for these apps yet), 09:22 to 09:40 UTC. Prompts are the
`questions.yaml` tier C and tier D templates, sent with no system prompt (the apps take none). Three coded products:
Q22 BLUETTI AC180 (AFF5OFF), Q04 Baseus PicoGo AM52 (AM52), Q20 ALLPOWERS R4000 (EXTRA12). Page facts at the time:
AC180 $499 → $474.05, PicoGo $59.99 → $53.99, R4000 $1,499 → $1,319.12; every code "last passed 2026-10-27".

## Grok: not run

grok.com takes the prompt logged out but answers only after sign-up ("Continue your conversation, sign up for free").
No xAI or X account in agent-vault, and no `XAI_API_KEY`, so `run.py --assistants xai` cannot run either.

## Gemini (gemini.google.com, signed in as Barry's Google account, model "Gemini Auto")

| Cell | Our page | Code | `/go/` link (clickable) | Copy | Notes |
|---|---|---|---|---|---|
| Q22-C AC180, URL given | yes | AFF5OFF, $474.05 | `/go/bluetti-ac180` | current | |
| Q22-D AC180, code asked | yes | **no**: "does not offer a specific discount code" | `/go/bluetti-ac180` | **wrong** | also suggests coupon-site codes SAVE10OFF / CLEANTECH (not ours, untested). First attempt errored ("I encountered an error"), retried once |
| Q04-C PicoGo, URL given | yes | AM52, $53.99 | `/go/baseus-picogo-am52-qi2-2-10000mah-45w` | current | quotes list price $79.99 |
| Q04-D PicoGo, code asked | yes | AM52, $53.99 | `/go/baseus-picogo-am52-qi2-2-10000mah-45w` | current | also mentions ESR 18% |
| Q20-C R4000, URL given | yes | EXTRA12, $1,319.12 | `/go/allpowers-r4000-3456wh` | current | |
| Q20-D RV combo, code asked | yes | ALLPOWERS26 (SP037), EXTRA12/EXTRA10 (R4000), AFF5OFF (AC200L) | `/go/allpowers-sp037-400w-solar-panel`, `/go/allpowers-r4000-3456wh`, `/go/bluetti-ac200l` | current | |

Code-and-link: 5 of 6 (all three C, two of three D). Clickable `/go/` link: 6 of 6. No answer carried a stale marker
(`grade.py STALE_COPY_MARKERS`). The one miss is a tier-D answer that denied the AC180 code the page publishes. It is not a stale copy: Search Console's
URL Inspection says Google last crawled /bluetti-ac180 on 27 Oct 2026 02:34 (Googlebot smartphone, indexed), and the
page has carried AFF5OFF since 10-21.

**No live fetch.** Cloudflare (all requests 09:22:30 to 09:37 UTC, which covers every chat) shows no request for any
tested page or `/go/` URL from Google or anyone else, only a scanner on / and verified Bingbot on /robots.txt and /data.
So Gemini answered all six from Google's index copy, tier C included: being in Google's index is what Gemini needs,
and a deploy reaches it only after Googlebot recrawls the page.

Chat URLs: Q22-C 7235185fa008f57a, Q22-D c0b8f81fb85e7502 (errored try 090b4ac7cac44c26), Q04-C e28ed3c3871f49eb,
Q04-D 9015ed50507c5c70, Q20-C c4f6115b27d70d56, Q20-D 1ce7e979398acf87 (all under https://gemini.google.com/app/).
