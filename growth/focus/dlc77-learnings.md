# DLC-77: what we learned about how ChatGPT reads our pages (stored-copy session, 2026-10-30)

Input for the discoverability skill; not the skill. The model-input findings (whole stored page, shared text budget,
16-23k ceiling, app vs API, shopping-catalog cards) are in `context-probe.md`. Solidity in brackets.

**Correction:** on 10-29 I wrote that the model sees the title plus a ~200-character passage. That passage is UI display
only; the model reads the stored page (`context-probe.md` needle tests). The canary (queue row 9) is superseded.

## Crawl and stored copy
- **ChatGPT reads OpenAI's stored copy, refreshed by OAI-SearchBot, not Bing.** [measured: 291/292 chats that showed an
  outdated version match OAI's last fetch; Bingbot 1/117] Exception [unexplained]: the four comparison pages appeared
  in results from 10-24, but OAI-SearchBot first fetched them on 10-29; only our ChatGPT-User probes had fetched them.
  Design: nothing changes for the model until a crawl.
- **Lag is days.** [measured] Focus pages last fetched 10-26 21:3xZ; none since as of 10-30 19:54Z. Copies seen 1 to
  6.5 days behind on 10-28. One sitemap read (10-22) preceded a full sweep (10-26); home and /portable-power-stations
  are re-fetched every few hours. Design: write for a copy up to a week old.
- **New URLs are fetched fast.** [2 observations: TN438 in 13 h, Marshall pages the next night] A new URL linked from
  the home page is the fastest route into the index.
- **Sitemap lastmod** is exact since 10-28. [effect unmeasured] No official OpenAI submission route found.
- **Part of OpenAI's crawl is unverified in Cloudflare since 10-28.** [one sweep] storedcopy.py counts unverified rows
  within 10 min of a verified fetch. Sampling is not an issue (sampleInterval 1).
- **A live ChatGPT-User fetch is reused by the next chats for minutes.** [one page, 4 cells] Evals: space chats
  15+ minutes or judge by a request window.

## What the shopper sees
- **Result title = `<title>` at OAI's last fetch.** [measured, n≈300]
- **UI snippet ≈ 200 characters, picked for the query from anywhere on the page;** on product pages it is the body
  opening (H1, summary, start of the offer card), never the meta description. [measured, 31 of ours] Design: H1 and
  summary should carry the deal and stay true for a week.

## Fact fixes for stale copies [shipped 1af4fbe, unmeasured]
Codes ending within 30 days carry the end date and the next code (R4000); the AC200L carries its phase-out. Rule:
every statement must be true a week later (dated prices, end dates, no undated comparisons).

## Scoring
A lever counts only once OAI has fetched the page after the ship (w3score index fields). Everything shipped before a
crawl lands together, so per-arm levers bundle. R1 (from 10-31) reads the 10-26 copy unless a crawl comes first:
gate it on `w3score.py --crawl`.
