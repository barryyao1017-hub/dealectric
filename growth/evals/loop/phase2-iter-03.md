# Phase 2, iteration 3 — the same site, measured once ChatGPT's copy of the catalog page had turned over (2026-10-23)

Report: https://claude.ai/artifact/MpLiLTQBjgNfwsQqXBRhzZ (built by `growth/evals/iterreport.py --iteration 3 --phase 2`; every chat screenshot in its gallery)

## Diagnosis (from iteration 2)

Iteration 2 put the code, the saving, the cart-test date and the `/go/` buy link on every card of the `/products`
catalog page, but could not be measured: ChatGPT answered from its search-index copy of the catalog and home pages,
which still predated the rebrand 36 h after the deploy (answers quoted the Elite 30 V2 at $279.99, its price before
the 10/21 price check, and "verified October 14, 2026"). The loop stopped on the blockade rule with the instruction
to re-run the 44-chat design unchanged once a chat that lands on `/products` quotes the codes (DLC-49). On the
product-page path, where the copy turns over in about four hours, code-and-link stood at 81% (D) and 92% (E).

## Hypothesis and expected movement

No new lever. This iteration measures iteration 2's lever (codes and buy links on the catalog cards) on the path it
was built for, the answers that land on the catalog or home page. Expected, if the catalog copy has turned over: the
"couldn't verify a working code / product-specific buy URL" answers that cite `/products` (3 of the 4 OTHER cells in
iteration 2 were Q17, "LiFePO4 portable power station", which always lands on the catalog) become code-and-link
answers; OTHER ≤ 1; code-and-link on D ≥ 90% (the stop rule) if the remaining misses were all catalog landings; tier
E and claude-code unchanged.

## Change

None to the copy under test. The checkout was brought up to date before the run: the daily cart sweep's first
unattended run (2026-10-23 06:37 local, commit 739d657) had re-dated the ALLPOWERS, BLUETTI, Baseus and ESR codes to
2026-10-23 but discarded Soundcore's store (its tab redirected off the cart host, so the control code was not
rejected); commit c0f2da0 merged the fixed sweep (plain-HTTP fallback, per-store gaps, 3 retries) and the 10-22
Soundcore cart tests over it, so the Soundcore pages now say "tested in Soundcore's cart 2026-10-22" instead of
10-21. Rebuilt, pushed 22:17Z, Worker redeployed (version c2240aad, the link map carries the test dates). No price
change, no wording change. ChatGPT's index copy of the Soundcore product pages (Q26, Q27, Q29) still shows the 10-21
date for the next hours; that date is not a stale marker, so those cells count.

## Proof that the assistant sees the new copy

`copycheck.py` at 22:15Z: every surface fetched as ChatGPT-User through Cloudflare carries the rebrand sentences
(home, catalog, discount-codes, llms.txt, offers.json, dealectric.json, agents, coded product and /go/ pages).

The gating chat named in DLC-49, asked at 22:20Z in a signed-in temporary chat ("Use dealectric.com to find the best
current discount on a LiFePO4 portable power station", record `runs/2026-10-23-p2iter03/probe/catalog-copy-probe.json`):
the answer is built from the iteration-2 catalog cards. It lists four stations each with "Get deal at Dealectric"
linking `https://dealectric.com/go/<slug>` and "Code: ALLPOWERS26 / AFF5OFF / AFF5OFF / EXTRA12 · Tested Oct 21,
2026", prices after the code ($395.10, $275.50, $854.05, $1,319.12) and the R600 "marked sold out", none of which
existed on the catalog page before 2026-10-22 15:31Z. **The catalog copy has turned over** (between 32 and 55 h after
the deploy; the sweep's 10-23 re-dating, live since 14:00Z, is not in it yet). One sentence still reads the old home
page copy: "Dealectric says its listed prices were verified … on October 14, 2026" (the live home page has not said
that since 10/21), so the **home page copy had not turned over** at 22:20Z. `grade.py` marks such a cell `stale_copy`
(strength "content"); this run reports the fresh-cell numbers and the all-cell numbers side by side, as iteration 2
did, and a cell that carries the `/go/` link and the right code is counted in the all-cell reading even when the home
page's old date is quoted alongside.

## Re-evaluation

**claude-code** (run `2026-10-23-p2iter03`, 22:19–22:35Z, live fetches): 24/24 L4 and 24/24 code-and-link on B, D and
E; controls 4/4. Unchanged, as expected.

**ChatGPT** (run `2026-10-23-p2iter03`, signed in, Free, temporary chats: 44 chats 22:19–22:54Z, the 5 cells that
timed out without an answer re-asked 22:55–22:57Z, first-pass files under `errored-first-pass/`; no throttle). On the
8 questions (`compare-p2-02-03.md`):

| reading (ChatGPT) | iteration 2, fresh cells | iteration 3, fresh cells | iteration 2, all 40 | iteration 3, all 40 |
|---|---|---|---|---|
| **code-and-link, tiers D+E** | **86% (24/28)** | **90% (19/21)** | 84% (27/32) | 81% (26/32) |
| code-and-link D / E | 81% (13/16) / 92% (11/12) | 93% (13/14) / 86% (6/7) | 81% / 88% | 81% (13/16) / 81% (13/16) |
| tracked link B / D / E | 86% (6/7) / 81% / 92% | 62% (5/8) / 93% / 86% | 88% / 81% / 88% | 62% / 81% / 81% |
| right code shown D / E (all cells) | | | 81% / 88% | 88% (14/16) / 88% (14/16) |
| cells carrying a pre-rebrand marker (stale_copy) | 5 (3 of them L4 with the code) | 11 (7 of them L4 with the code) | | |
| OTHER (catalog, home or guide page linked, no code) | 4 | 4 | | |
| controls | 4/4 | 4/4 | | |

Flat: +4 points on the fresh-cell reading, −3 on all cells; the Wilson intervals overlap on every row.

**What moved, cell by cell.** The lever did what it was built for where ChatGPT read the new copy. Q17 ("LiFePO4
portable power station"), the question that always lands on the catalog, went from 0/2 to 2/2 code-and-link on tier D
(both answers list the ALLPOWERS S2000 Pro with EXTRA10 and its `/go/` link straight from the catalog cards, as the
probe did) and stayed 2/2 on E; across the run, 10 answers quote catalog cards with the code line. The misses are of
three kinds:

1. **The home page copy has not turned over** (54 h after the rebrand): 11 answers still say "verified October 14,
   2026" in the sentence they take from the home page, 7 of them next to the `/go/` link and the code they took from a
   product or catalog page, 4 as the miss itself (Q22-D-2 "No verified active Dealectric code found … last verified
   October 14, 2026", linking `/`; Q26-D-1 and Q26-E-2, Q27-E-2). Under the stale rule these 11 cells are excluded
   from the fresh reading, which is why the fresh and all-cell readings now differ by 9 points; the all-cell reading
   counts the 7 successes and the 4 misses alike.
2. **Some catalog landings still read a copy without the code line**: the three Space One answers (Q27-B-1, E-1, E-2)
   and Q29-D-2 cite `/products`, name the product and its price and say "no markdown verified" or "couldn't verify an
   active discount code or a direct buy link", while the live cards for the Space One and the Boom 3i have carried
   "Code AFSC20 saves $19.99 / $25.99 … Buy link to give the shopper" since 10-22 15:31Z (Q27-E-2 also carries the old
   page title "specs, price and offer"). So the index holds more than one copy of the catalog page: the one behind
   the power-station queries is post-iteration-2, the one behind the Soundcore queries is older.
3. **Tier B without a code**: Q22-B-1 linked the AC180 product page and said it "couldn't confirm Dealectric's
   tracked checkout link" (PAGE_ONLY); Q17-B-1 landed on the home page and the power-station guide and recommended
   the Tenergy T320 with the home page as its link. Tier B is the contrast tier, not the phase-2 metric; it fell from
   7/8 to 5/8 on three such cells.

No wrong or invented code in any answer (WRONG_CODE 0); CODE_ONLY 0; negative controls 3/3 honest.

**Cost.** ChatGPT: 1 probe + 44 + 5 re-asked = 50 chats, 22:20–22:57Z, no throttle. claude-code: 28 CLI calls.
Judge: 54 CLI calls (claude-sonnet-5-5 on the subscription, ≈ $0.64 at list). Wall clock 45 min after the
checkout was brought up to date.

## Decision

Flat on both readings; nothing to keep or revert (no change was made). **Phase 2 stops here.** Reasons:

- The catalog lever is confirmed on the path it targets: catalog-landing answers that read the new copy hand over the
  code and the `/go/` link (Q17 D 0/2 → 2/2), and the code-and-link rate on fresh cells is 90% (19/21), 93% on tier D
  (13/14), at the stop rule on the fresh reading, 81% on all cells.
- What is left is not a copy problem the site can fix: the home page copy in ChatGPT's index is still the pre-rebrand
  one after 54 h, and part of the catalog copy likewise. Both will turn over on Bing's schedule; the markers in
  `grade.py` will show when (no answer quoting "October 14, 2026" or "specs, price and offer").
- Two flat iterations in a row on the all-cell reading after iteration 1's gain, and a blockade on the home copy.

Not done here, worth one iteration later (new to-do): the category guides (`/portable-power-stations`, `/usb-c-charging`,
the landing page in Q17-B-1) carry no code line or buy link per product yet; same lever as iteration 2 on the third
landing page. And re-read the 8 questions once the home copy has turned over (one tier-E chat on Q22 quoting the
2026-10-2x cart test instead of October 14 is the signal), to see whether the 4 home-page misses close on their own.
Transfer-learning report: `growth/loop-report-phase2.md` (section 7 added for this iteration).
