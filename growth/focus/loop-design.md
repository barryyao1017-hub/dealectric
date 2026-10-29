# W3 copy loop: frozen design (DLC-69, 2026-10-28)

The plan is `growth/first-sale-plan.md` W3. This file fixes how every reading is run and scored for the whole loop, so
lever results stay comparable. Change it only by adding a dated line under "Changes", never by editing a rule in place.

## Arms

One arm per focus product. Each carries one lever at a time, in parallel, because a copy change takes days to reach
ChatGPT's stored copy.

| Arm | Product page | Network, code | Other surfaces |
|---|---|---|---|
| A | `/bluetti-ac200l` | Awin, AFF5OFF (5% off) | `/bluetti-discount-codes`, `/discount-codes`, catalog card, `offers.json`, CSVs, `/go/` text page, spec card |
| B | `/aurzen-travelplay-autocinema-tesla-model-y` | CJ, CJ10 (10% off) | `/tesla-model-y-back-seat-screen`, `/aurzen-discount-codes`, `/discount-codes`, catalog card, `offers.json`, CSVs, `/go/` text page, spec card |
| C | `/allpowers-r4000-3456wh` | CJ, EXTRA12 (12% off, to 11-15), then ALLPOWERS26 (10%) | `/allpowers-discount-codes`, `/discount-codes`, catalog card, `offers.json`, CSVs, `/go/` text page, spec card |
| D | `/allpowers-p1800-1024wh` | CJ, ALLPOWERS26 (10% off) | as C |
| E | `/allpowers-sp037-400w-solar-panel` | CJ, ALLPOWERS26 (10% off) | as C |
| F | `/allpowers-s2000-pro-sp037-solar-kit` | CJ, ALLPOWERS26 (10% off); BULKRATE on the station + panel as two items | as C |

A product W1 adds to the focus set later gets its own arm, with its questions and controls added here under "Changes"
before its baseline reading.

## Questions (frozen in `growth/focus/loop-questions.json`)

Four test questions and two controls per arm. None names Dealectric.

| Arm | qid | Role | Prompt |
|---|---|---|---|
| A | `bluetti-ac200l--deal` | test (discovery prompt) | Is there a discount code or a good deal on the BLUETTI AC200L right now? |
| A | `bluetti-ac200l--worth` | test | Is the BLUETTI AC200L worth buying? Where's the best place to buy it? |
| A | `bluetti-ac200l--coupon` | test | BLUETTI AC200L coupon code |
| A | `bluetti-ac200l--best` | test | What's the best 2kWh portable power station for an RV under $900? |
| A | `bluetti-elite-200-v2--deal` | control | Is there a discount code or a good deal on the BLUETTI Elite 200 V2 right now? |
| A | `baseus-blade-h1-100w-20000mah--deal` | control | Is there a discount code or a good deal on the Baseus Blade H1 power bank right now? |
| B | `aurzen-travelplay--discovery` | test (discovery prompt) | Is the Aurzen TravelPlay a good back seat screen for a Tesla Model Y? Where can I buy one? |
| B | `aurzen-travelplay-autocinema-tesla-model-y--deal` | test | Is there a discount code or a good deal on the Aurzen TravelPlay AutoCinema for Tesla Model Y right now? |
| B | `aurzen-travelplay-autocinema-tesla-model-y--best` | test | What's the best back seat screen for a Tesla Model Y under $150? |
| B | `aurzen-travelplay--kids` | test | How can my kids watch movies in the back seat of a Tesla Model Y? |
| B | `aurzen-zip-pro-tri-fold-1080p-projector--deal` | control | Is there a discount code or a good deal on the Aurzen ZIP Pro projector right now? |
| B | `baseus-gan5-pro-65w-2c-u--deal` | control | Is there a discount code or a good deal on the Baseus GaN5 Pro 65W charger right now? |

- The discovery prompts are the two 2026-10-28 questions where ChatGPT showed us unprompted. The rest come from W1's
  bank (same text, so W1 scan cells count) plus one search-style and one use-case phrasing. A test question that stays
  T1 in the baseline stays in the set: it measures reach, and a lever may move it.
Arms C-E (added 2026-10-28, frozen in `growth/focus/loop-questions-allpowers.json`, so each reading request names one
file): per arm the W1 bank's deal and worth questions, "<product> coupon code", and the bank's "best ... under $X"
question, where W2 found us absent. Controls: a same-brand sibling per arm (`allpowers-s2000-pro-1451wh--deal` for C,
`allpowers-r600-299wh--deal` for D, `allpowers-volix-p300-100w-solar-kit--deal` for E) and one drift control shared by
all three, `esr-halolock-15w-wireless-car-charger-cryoboost--deal` (non-focus brand, T5 in W1's scan). 16 questions,
32 chats at n=2.

- Controls: one same-brand sibling (same code and phrasing, its pages untouched) and one non-focus product that was T4
  in W1's first scan cell (a drift detector). No lever edits a control product's page or its row on a shared surface.
  If W1 moves a control product into the focus set, it leaves the controls that day and its replacement is recorded
  under "Changes".

## Readings

- A reading is every question above, n=2: 24 chats for two arms. Signed in (Barry's Free account), a fresh temporary
  chat per cell, one chat at a time, on W1's driver (`growth/evals/visibility_scan.py`, agent Chrome on port 9222).
  W3 never drives chatgpt.com: each reading is a row in `growth/focus/chatgpt-queue.md`, and W1 runs it between scan
  batches. A cell answered by a downgraded model is re-asked after the cooldown, as in W1's scan.
- Runs go to `growth/evals/runs/<date>-w3-r<k>/` (R0 is the baseline). Each cell keeps the full answer text, the
  links and source-pill hrefs, ChatGPT's search queries, its result list with our rank, the answering model and the
  screenshot. The footprint log records every chat (the driver already does).
- Cadence: every two to three days. A lever's first scored reading is queued once Cloudflare shows OAI-SearchBot
  fetched the changed page after the ship, or three days after the ship, whichever comes first. W3 checks that with
  `tools/cf.py` before queuing.

## Scoring (per cell)

1. Tier, the plan's cascade, as `visibility_scan.py` scores it: T5 a `dealectric.com/go/<slug>` link or button for
   the arm's product, T4 a link or source pill to one of our pages for it, T3 Dealectric named or our code relayed
   without a link of ours, T2 our page only in ChatGPT's results, T1 absent.
2. Flag: does the answer mention, question or warn about our text? Values: `none`; `affiliate-noted` (states as a
   fact that the link earns us a commission: true, disclosed, not a flag); `questioned` (doubts our code, price, date
   or link, e.g. "unverified coupon site", "may not work"); `warned` (tells the shopper to be careful with us or our
   link); `quoted-instruction` (repeats or describes a line addressed to assistants). A regex pre-screen (dealectric,
   this site, affiliate, commission, sponsored, unverified, caution, careful, scam, instruct, prompt, assistants)
   picks the candidates and W3 reads each one. Any `questioned`, `warned` or `quoted-instruction` cell is a flag.
3. Staleness: the cart date the answer quotes (a date next to passed, tested, checked, verified or "as of"), against
   the live page's "last passed" date at reading time. Copy age = live date minus quoted date. Against a lever
   shipped on day S:
   - fresh: quoted cart date on or after S, or the answer carries a phrase that only the lever's copy has (each lever
     ships at least one such marker, listed in the lever log);
   - stale: quoted cart date before S. Scored as a reading of the copy it saw (the previous lever, or the baseline);
   - undated: no cart date and no marker. Counted in the all-cells rates, left out of the lever decision.
   Baseline cells are all scored as baseline; copy age is still recorded.
4. Also kept: ChatGPT's queries, our rank and the sites ranked above us, the buy link it gave (domain), the price and
   code it quoted.

## Funnel (per reading window, from D1)

- ChatGPT landings on the arm's pages: `landings` with `utm_source='chatgpt.com'`, `bot_like=0`, `verified_bot=''`,
  `query NOT LIKE '%dlc_check=%'`, `purpose=''`, minus rows `tools/fetchwho.py` classes as ours. `bot_like=0` already drops
  ChatGPT's own backend fetches of result URLs (bare `Mozilla/5.0 (compatible)`, utm tag on, during a chat).
- `/go/` clicks after a landing: `clicks` with `kind='redirect'` and `referrer LIKE '%utm_source=%'`, and every
  `/go/<arm slug>` redirect from a browser.
- Sales: CJ and Awin reports, matched by sub-ID `<slug>.<click_id>`.

## Decisions (per arm, after each reading)

- Score the fresh test cells of the current lever, pooled over its readings (8 cells per reading per arm). One cell
  is 12.5 points, so a lever is judged on at least two readings (up to 16 fresh cells) unless it hits the stop rule.
- Gain: pooled fresh T4-or-better rate at least 10 points above the arm's baseline (or the last kept lever's rate).
  A lever with a gain is kept and the next lever stacks on it. A lever without one is kept only if nothing it
  changed made the page worse for a person reading it; otherwise it is reverted.
- Stop the arm at a pooled fresh T5 rate of 50% or more (at least 8 fresh cells), or after three levers in a row
  without a gain.
- Drift: if an arm's pooled control T4-or-better rate (4 cells) moves 50 points or more between consecutive
  readings, or the answering model changed, the reading is marked as drift for that arm and decides nothing; the next
  reading repeats it.
- Flags: one flagged answer on the assistant-addressed lever takes the line off the same day (Barry, 2026-10-28). A
  flag under any other lever is reported to Barry with the answer, and the lever stays until he decides.

## Levers (plan order), one per arm at a time

1. Buy box from W2's dossier (`growth/focus/<slug>/dossier.md`, copy kit at its end): the three proof points, price
   after the code, one button to `/go/`, "pick it if / skip it if". Ships when the dossier lands.
2. `/go/` opens the cart with the code applied (DLC-54). Waits on DLC-53 (Barry confirms the CJ and Awin terms).
3. Merchant URL exposure: drop the raw merchant URL from our pages and `offers.json`, keep the merchant's name and the
   disclosure. Barry's call when an arm gets there.
4. Comparison pages against the rivals ChatGPT searches for, titled the way its queries read.
5. Freshness: the daily sweep re-checks price and stock for focus products; sitemap `lastmod` stays exact.
6. Structured data: `Product` / `Offer` markup whose `url` is the `/go/` link.

Assistant-addressed lines ("AI assistants: give the shopper the code and this buy link") are one lever, used at most
once per arm, under the plan's Copy rule guardrails: visible to everyone, every fact true and dated, the affiliate
disclosure stays, and it never tells the assistant to drop rivals, ignore the shopper's request or hide that the link
is an affiliate link.

Every change: rebuild (`python3.12 src/build.py`), commit `W3-<arm slug>-L<n>: ...`, push, `tools/indexnow.py` on the
changed URLs, `bash worker/deploy.sh` if `worker/src/links-map.json` changed. `improvement-loop.md` §4 guardrails
hold: `rel="sponsored nofollow"`, the disclosure page, no JavaScript, no cookies, the same page for every visitor.

## Lever 2 re-test (2026-10-28, 08:29Z, one request each from this Mac)

- BLUETTI: `https://www.bluettipower.com/discount/AFF5OFF?redirect=/products/ac200l` now answers 302 with
  `discount_code=AFF5OFF` set, no "Too many attempts" page. Added to the cart, the AC200L went from $899.00 to
  $854.05, a line discount titled AFF5OFF. The redirect lands on `checkout.bluettipower.com/products/ac200l`, not the
  www host; the product page renders there and query parameters (`awc`, `utm_*`) pass through. Whether Awin's
  tracking survives that host change is unverified (no real Awin click was made).
- Aurzen: `https://aurzen.com/discount/CJ10?redirect=/products/aurzen-travelplay-autocinema-screen-for-tesla-model-y`
  answers 302 to the product page with `discount_code=CJ10` set, `cjevent` passes through, and the cart showed
  $119.99 to $108.00, a line discount titled CJ10.
- Not shipped: DLC-53 is open.

## Lever log

| Arm | Lever | Shipped (commit) | Fresh marker | Readings | Pooled fresh T5 / T4+ | Result |
|---|---|---|---|---|---|---|
| A | baseline | n/a | n/a | R0 2026-10-28 (`readings/r0.md`) | T5 1/8, T4+ 5/8 | controls T4+ 3/4 |
| A | L2 cart link, code applied (DLC-71 a) + phase-out caveat | 2026-10-28 ~18:15Z (25afae8) | "already applied", "replacing the AC200L with the Apex 200" | | | shipped before L1: the old buy path was dead |
| A | L1 buy box | next, after L2's readings | | | | dossier copy kit and record fixes ready |
| B | baseline | n/a | n/a | R0 2026-10-28 (`readings/r0.md`) | T5 0/8, T4+ 4/8 | controls T4+ 3/4 |
| C | baseline | n/a | n/a | R0b 2026-10-28 (`readings/r0b.md`) | T5 0/8, T4+ 6/8 | controls T5, T4+ 1/4, 3/4 |
| D | baseline | n/a | n/a | R0b 2026-10-28 (`readings/r0b.md`) | T5 0/8, T4+ 4/8 | controls T5, T4+ 1/4, 3/4 |
| E | baseline | n/a | n/a | R0b 2026-10-28 (`readings/r0b.md`) | T5 0/8, T4+ 6/8 | controls T5, T4+ 2/4, 3/4 |
| F | baseline | n/a | n/a | R0c 2026-10-29 (`readings/r0c.md`) | T5 1/8, T4+ 5/8 | controls T5, T4+ 1/4, 3/4; positive control 2/2 |
| F | L1 buy box + rest of the fix list | 2026-10-29 08:09Z (5435350) | "13 kg station", "less than the kit" | | | |
| C | L1 buy box + rest of the fix list | 2026-10-29 04:21Z (fc9a808) | "1/2 HP sump pump", "1.7 times the capacity" | | | |
| D | L1 buy box + rest of the fix list | 2026-10-29 04:21Z (6e77e4a) | "8 nights of CPAP", "AirSense 11" | | | |
| E | L1 buy box, dated stock line + rest of the fix list | 2026-10-29 04:21Z (a3bbec3) | "24 owner reports", "under half the price per watt" | | | |
| B | L1 buy box + record fixes | 2026-10-28 ~09:10Z (629bcd5) | "34 times the area", "glass-roof sunshade alone" | | | |

## Changes

- 2026-10-28: frozen.
- 2026-10-28: arm B lever 1 shipped while the page still said "last passed 2026-10-27" (the day's cart sweep runs
  later). For B-L1, a cell is fresh with a quoted cart date of 2026-10-28 or later, or a marker; 2026-10-27 without a
  marker is undated; 2026-10-26 or earlier is stale. B-L1 also fixed facts on the record (nothing goes on the rear
  window), so it is scored as buy box plus record fixes.
- 2026-10-28: arm A on hold. W2 found, and W3 confirmed in a browser, that bluettipower.com/products/ac200l (our
  `/go/` target) renders an empty page with no Add to Cart; BLUETTI's indexed AC200L listing says Discontinued and the
  Apex 200 replaces it on Nov 4-5. DLC-71 holds Barry's options: cart link through Awin, Elite 200 V2 as the primary
  button, or move the arm to the Elite 200 V2 and then the Apex 200. Arm A's R0 cells still run as planned.
- 2026-10-28: Barry picked DLC-71 option (a) after a test. One Awin click per arm (fresh headless Chrome profile, no
  order): the cart link keeps awc to checkout.bluettipower.com and shows the AC200L at $899 with AFF5OFF (-$44.95,
  $854.05); the product-page control keeps awc on a blank page; aw59271 on .awin1.com in both; no Awin tag on
  BLUETTI's pages in either. Shipped as arm A's L2 at ~18:15Z. The page already said "last passed 2026-10-28"
  before the ship, so for A-L2 a cell is fresh with a quoted cart date of 2026-10-29 or later, or a marker;
  2026-10-28 without a marker is undated. A-L1 (buy box) follows once L2 has its readings.
- 2026-10-28 (R0 scoring, two clarifications, not rule changes): (1) ChatGPT's generic coupon hedge ("I couldn't
  independently confirm the code in checkout") is not a flag: it appears as often on control answers that don't involve
  us. It is noted per cell in `readings/flags.json`. (2) R0 was meant as both arms' baseline, but B-L1 went live six
  hours before R0 ran. B's R0 cells that carry no L1 marker and no post-ship cart date count as B's baseline
  (`w3score.py --baseline`).
- 2026-10-28: scoring is `growth/evals/w3score.py`; its LEVERS table mirrors this lever log and gets a row per ship.
- 2026-10-28: arms C-E added for the ALLPOWERS R4000, P1800 and SP037 (Barry's focus set, 3a1a09c), set up when W2's
  dossiers landed (Barry's call). Before their baseline, df2d809 corrected only what was false on their pages (R4000
  AC input, warranty condition, "job sites", per-kWh claim; P1800 silent charge and UPS; SP037 compatibility count,
  IP rating, the 2025 revision). Those are fact fixes, not levers. Their L1 buy boxes (with the rest of each fix list,
  SP037's dated in-stock line among them) ship after R0b has run.
- 2026-10-28: DLC-76 (Barry's DLC-75 call) dropped the compare-at strike-through on every ALLPOWERS page and added a
  dated "lowest store price we've seen" line (60ef1c3), while R0b was running. It touches arms C-E's test and control
  pages alike and isn't a lever. ChatGPT's copies of those pages predate it, so R0b still reads the baseline.
- 2026-10-28 (DLC-77): what ChatGPT reads is OpenAI's stored copy, and it follows OAI-SearchBot. `growth/evals/storedcopy.py`
  (report `growth/focus/stored-copy.md`, crawl log `growth/focus/crawls/fetches.jsonl`) matched every saved result
  title to the deployed version that carried it: in 291 of 292 chats that showed a superseded version, OAI-SearchBot's
  last verified fetch before the chat had seen that version; Bingbot's fits 1 of 117. OAI-SearchBot fetched each
  focus page once (2026-10-26 21:3xZ), so all five arms' index copies predate A-L2, B-L1 and the ALLPOWERS fact fixes.
  Scoring addition (not a rule edited in place): a test cell with no marker and no cart date that decides it is
  fresh if OAI-SearchBot fetched the arm's page after the lever shipped and before the chat, stale if it did not
  (`w3score.py` records `index_fetch`, `index_version`, the stored title and, from now on, the snippet). R0's seven
  undated B cells become stale by this rule; they were already scored as baseline. The reading trigger ("OAI-SearchBot
  fetched the changed page after the ship") is checked with `w3score.py --crawl`, verified crawler rows only.
- 2026-10-28 (DLC-77): the sitemap carries an exact `<lastmod>` per URL (the time the page's bytes last changed;
  `build.py sitemap_lastmod`), so the daily cart pass marks every coded page changed. It applies to test and control
  pages alike, so it is not a lever (lever 5's price and stock re-check stays one).
- 2026-10-28 (DLC-77, Barry's call): two fact fixes, not levers, so a stale stored copy stays true. (1) A code that ends
  within 30 days carries its end date: the R4000's title says "(ends Nov 15)" and its description, catalog card and
  agent note say "until 2026-11-15" and name the code tested to follow it (ALLPOWERS26, $149.90). No other product's
  best code ends within 30 days, so no control page changed. (2) The AC200L's description, catalog card and agent note
  carry the phase-out ("On sale while BLUETTI's remaining AC200L stock lasts; the Apex 200 replaces it in early
  November 2026"); before, only its caveats did. Both reach the index in the same OAI crawl as A-L2 and arm C's
  baseline-era fixes, and neither is a fresh marker. The title format change (stored-copy-step2.md) is held until that
  crawl.
- 2026-10-28 (DLC-78, DLC-79): site-wide, not a lever. Every page's menu gains "Comparisons" (/compare), and each
  product page that appears in a comparison table gains a "Compared side by side" list linking those tables, placed
  after the spec table, below the offer block and buy box. All five arms' pages get it (AC200L, R4000, P1800: the
  LiFePO4/NMC table and, for the P1800, the CPAP one; SP037: solar watts; Aurzen TravelPlay: Tesla Model Y screens), so
  the arms change together, as with DLC-76. The home page's counts and brand list, the disclosure's network list and
  dealectric.json's categories are now generated. No title, price, code or offer text changed; no fresh marker.
- 2026-10-29: arms C-E L1 shipped after R0b (fc9a808, 6e77e4a, a3bbec3). Their pages said "last passed 2026-10-28"
  before and after the ship, so a cell is fresh with a cart date of 2026-10-29 or later, a marker, or (DLC-77 rule)
  an OAI-SearchBot fetch after 04:25Z; 2026-10-28 alone is undated. SP037's stock line rests on the cart test (the
  sweep stops at a sold-out variant), so it can't claim stock the cart didn't confirm.
- 2026-10-29: Barry added the ALLPOWERS S2000 Pro + SP037 kit as arm F (set up when W2's dossier lands; W1's scan
  cells reuse for its baseline) and the ESR Qi2 Mini as a study case (82c329c). The ESR Qi2 Mini deal question is now a
  positive control in both question files (role "positive"; its page is never changed), and R1 runs both files into
  one run-id (queue row 7, 58 chats). Study: `readings/esr-qi2-study.md`: our `/go/` link comes from list-page rows,
  never from a product page alone (0 of 55), because ChatGPT keeps a ~200-character snippet and a product page's
  snippet ends before its link. Proposed lever "deal row first" (the buy link and code in the first line after the
  product name) awaits Barry.
- 2026-10-29: arm F (ALLPOWERS S2000 Pro + SP037 kit) set up when W2's dossier landed (9cfbc6c): questions in
  `loop-questions-allpowers.json` (deal, worth, coupon, best; control `allpowers-p1800-sp037-solar-kit--deal`; the
  shared ESR HaloLock drift control now covers C-F). Before its baseline, c7ee97b fixed what was misleading: the kit
  and the S2000 Pro station (arm C's control) now say 2,400 W is rated 2,000 W below about 60% charge, and the kit's
  solar input is settled. Baseline R0c is queue row 11, reusing W1's scan cells; the kit's buy box waits for it. R1
  (row 7) now covers arm F too.
- 2026-10-29: R0c scored (`readings/r0c.md`) and arm F L1 shipped (5435350). w3score.py now drops any answer not from
  gpt-6 itself (a chat routed to gpt-6-mini from the start has no resolved model slug; W1's scan once counted 76 such
  answers as gpt-6). R0 and R0b re-scored under the check: unchanged. For F-L1 a cell is fresh with a cart date of
  2026-10-29 or later, a marker, or an OAI-SearchBot fetch after 08:12Z.

- 2026-10-29: a cell with no gpt-6 answer is unanswered: it stays out of every rate and w3score lists it under its arm
  with the number of tries. ChatGPT can route one question to gpt-6-mini every time (W1: Baseus worth-2, 12 in a row
  while the cells around it got gpt-6), so W1's runner caps the retries instead of looping. Before this, a cell whose
  every try was mini dropped out without being listed. R0, R0b and R0c have no unanswered cells.
