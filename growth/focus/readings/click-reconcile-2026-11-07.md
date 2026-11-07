# /go/ clicks against CJ and Awin click reports (DLC-86), 2026-11-07

D1 `clicks` (kind='redirect', 2026-10-18 to 11-07) against CJ's Performance by Website (daily clicks, last 30 days;
CJ shows no per-SID click report) and Awin's Click References report (year to date, per clickref), both read in the
Agent Chrome on 11-07.

**Verdict: the chain works on both networks, and neither loses clicks systematically. Most gaps trace back to bot
filtering, duplicate filtering, or our own test traffic. One device's 5 clicks are unexplained (below).**

## CJ (daily totals; D1 days in Pacific time)

On quiet days CJ's count equals D1's real-browser count, give or take one or two: 10-20 15/15, 10-26 12/12,
10-28 8/8, 10-29 25/24, 11-01 20/19, 11-02 76/72. CJ counts fewer on scanner-heavy days: 10-22 22 vs 60,
10-24 4 vs 19, 10-30 170 vs 218, 11-03 84 vs 171. That is CJ discarding repeat and robotic clicks, and it matches the
scanner traffic the 10-27 read found in D1. On 11-06 CJ counts more (45 vs 24 real-browser), which means D1's
`bot_like` flag marks some real browsers as bots that day. The one CJ sale (10-29) carries our sub-ID in Commission
Detail.

## Awin (per clickref, so this match is exact)

- Awin shows 363 click references and 370 clicks year to date. D1 has 755 Awin redirects, 465 of them from real browsers.
- 230 of the 465 real-browser D1 clicks appear in Awin under their exact `<slug>.<clickid>`. 21 more appear under a
  truncated ref.
- **ChatGPT-tagged real-browser clicks: 30 of 40 appear in Awin.** The 10 that don't:
  - 5 are ChatGPT's own backend fetches (`Mozilla/5.0 (compatible)`, which `bot_like` misses).
  - 5 come from one iPhone (iOS 18.7): 3 within 4 minutes on 10-29 (Elite 30 V2 kit) and 2 within 3 minutes on
    11-05 (AC180 kit). **Unexplained:** Awin doesn't show even the first click of either burst. It may be one person
    (possibly one of ours) whom Awin filters. Worth checking whether Barry tapped those links himself.
- 47 of 290 bot-like D1 clicks also appear in Awin, so Awin's bot filter differs from ours.
- 83 Awin refs (90 clicks) are a bare slug with no click ID. These are **our own test clicks**: `tools/preapply.py`
  opens the raw deep link from `build.py` `tracked_link` (clickref=<slug>), and so did the new-brand checks. They are
  easy to drop: a ref with no `.` is ours.
- BLUETTI real-browser clicks reach Awin every day we checked: 11-04 17/26, 11-05 18/26, 11-06 4/4, 11-07 5/7.

## Follow-ups (small, not done here)

- Count ChatGPT-tagged clicks with user agent `Mozilla/5.0 (compatible)` as bots: `tools/dailyupdate.py` already
  drops them; the Worker's `bot_like` doesn't.
- Awin sales: still none (no transactions), so the sale end of the Awin chain is untested.
