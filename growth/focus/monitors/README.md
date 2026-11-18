# Laptop screen extender / stacked monitor cluster (DLC-290, 2026-11-18)

Barry set this cluster as a focus on 2026-11-17 after the first non-solar sale (2026-11-15, CJ, Mobile Pixels Duex Float 2
Pro, $336.98 order, $23.59 commission). This folder holds the run that grew it.

- `monitorpages.py`: the page driver (tools/abpage.py through growth/focus/open-pages/openpage.py, with this run's rules
  and a table of the screens we link). `KEEP` lists the questions that became pages.
- `harvest_read.py`: prints what ChatGPT did with each harvest question (search words, results, cited results, catalog
  cards, whether a Mobile Pixels or FOPO product was named). `--full` adds every result and the answer text.
- `stores-2026-11-18.json`: the two partner stores' other screens with no product record, read that day.
- `publish.sh`: merge origin/main, rebuild, push; retried when main moves during the build.
- Questions: `growth/focus/ab-harvest-new-2026-11-18-monitors.json` (16 questions, 2 plain gpt-6 chats each, run
  `2026-11-18-monitors-harvest`; chat files are local only, each kept page's `growth/focus/ab/<folder>/harvest.json`
  carries its two chats).

## What existed (map, 2026-11-18)

| Page | ChatGPT landings (all time) | /go/ clicks from ChatGPT |
|---|---:|---:|
| /mobile-pixels-duex-float-2-pro (product) | 2 | 7 (2 through the stacked page, 5 from this page) |
| /best-portable-monitor-above-laptop-screen | 4 | 2 (counted above) |
| /best-triple-screen-laptop-extender-for-macbook-air | 3 | 0 |
| /best-triple-laptop-screen-extender | 2 | 0 |
| /best-triple-screen-laptop-extender-16-inch-1920x1200 | 0 | 0 |
| /mobile-pixels-trio-3-pro, FOPO S11, S9G, S788 (products) | 0, 1, 1, 0 | 0 |

Baseline for the reading, 2026-11-11..11-17 (D1, `bot_like=0`): 7 ChatGPT-sourced `/go/` clicks (all on the Duex Float 2
Pro), 10 ChatGPT landings on the cluster's pages, 1 sale. Queries:

    clicks:   SELECT slug, count(*) FROM clicks WHERE kind='redirect' AND bot_like=0 AND ts>=:from AND ts<:to
              AND (slug LIKE 'mobile-pixels%' OR slug LIKE 'fopo%')
              AND (utm_source='chatgpt.com' OR referrer LIKE '%utm_source=chatgpt%') GROUP BY slug
    landings: SELECT page, count(*) FROM landings WHERE bot_like=0 AND verified_bot='' AND utm_source='chatgpt.com'
              AND ts>=:from AND ts<:to AND (page LIKE '%monitor-above%' OR page LIKE '%extender%'
              OR page LIKE '%mobile-pixels%' OR page LIKE '%fopo%') GROUP BY page
    sales:    SELECT * FROM sales WHERE sub_id LIKE 'mobile-pixels%' OR sub_id LIKE 'fopo%'

## Harvest read (32 chats, all gpt-6, no throttle)

Kept: the results were AI listicles and store pages (itechguides, rottenwifi, theofficejournal, deskgearhq, workcocoon,
twelvetabs), few or none cited, and a screen we link wins or places on the question's own terms.

| Question | Read | Decision |
|---|---|---|
| best laptop screen extender | Listicles only; ChatGPT's top pick is the Trio 3 Pro, shown at $423.99–$429.99 from other sellers while the maker's store has it at $367.99; we were not retrieved | page |
| best laptop screen extender under $300 | Listicles; one chat picks the Duex Max DS at $229.49 (Best Buy), $175.99 at the maker; not retrieved | page |
| best triple laptop screen extender under $400 | Our off-question pages retrieved in both chats (rank 6, ranks 1–2), cited once; the Trio is now under $400 | page |
| best laptop screen extender for a 16 inch laptop | Listicles, one cited; Duex Float named once; not retrieved | page |
| best laptop screen extender for a 17 inch laptop | Listicles, none cited, no cards; FOPO named once; not retrieved | page |
| best laptop screen extender that works without drivers | Plugable, FOPO's store and Best Buy cited; FOPO named once; not retrieved | page |
| best dual screen laptop extender | ChatGPT reads it as two added screens; our triple pages were cited in both chats | covered by existing pages |
| best triple screen extender for a 14 inch laptop | Our pages ranked 1–3 and cited in both chats | covered |
| best triple screen extender for a MacBook Pro | Three of our pages retrieved in both chats, cited once | covered |
| best triple … sharper than 1080p | Our page cited once; the honest picks are 16-inch 2.5K extenders from brands we don't link | no page |
| best stacked monitor for a laptop | Tom's Hardware, Wired, Macworld; the Duex Float 2 Pro already named with a catalog card in 1 of 2 | no page (major reviewers; existing page serves it) |
| best portable monitor that attaches to a laptop | Wired, Tom's Hardware, RTINGS, PCWorld in the results; Duex named in both; our stacked page retrieved at rank 8–9, cited once | no page |
| best portable second monitor for a 16 inch MacBook Pro | RTINGS cited three times, ASUS and LG cards | saturated |
| best 16 inch portable monitor under $250 | Wired cited four times | saturated |
| best 16 inch 2.5K 120Hz portable monitor | ASUS MB16NCG is the honest pick; the Duex Float 2 Pro places for stacked use only | no page |
| best portable dual screen setup for travel | Tom's Hardware and Wired; a situation question (Barry 11-18: no more situation pages) | no page |

Catalog cards (step 1 of the row, read from the same chats instead of a separate cardprobe run): the Trio 3 Pro, the Duex
Float 2 Pro, the Duex Max DS and the Geminos X all have ChatGPT catalog cards, bound to other sellers (Walmart, B&H,
Best Buy, Micro Center) at prices above the maker's store during its sale. The buy slot is therefore not empty for these
products; our edge is the maker-store price through our link.

## Programs in the cluster

- Approved and in use: Mobile Pixels (CJ 5725421, no code; Dealectric-only code requested 11-17, DLC-289), FOPO (Awin
  42800, code FOPO 10%, printed on its site).
- Xebec is on CJ (advertiser 6142467, 15% listed): our status there is `pending_applications`, so an application is
  already in. When it is approved, the Xebec rows on four pages can carry our link.
- CJ advertiser search found no program for UPERFECT, KEFEYA, SideTrak, ARZOPA, Cevaton, Teamgee, KYY, InnoView, JSAUX,
  ViewSonic, Lepow, Kwumsy, Aura Displays or Plugable. Awin's directory was not searched: Awin was signed out in the
  Agent Chrome and its sign-in needs a visible tab. VEVOR (Awin, approved) sells no screen extender.

## What was built (2026-11-18, all live, gate passed at ranks 1, 3 and 6)

| Page | Pick (a product we link) | Angle |
|---|---|---|
| /best-laptop-screen-extender | Mobile Pixels Trio 3 Pro | which laptops run one, two or three added screens (video path against Apple's lid-open display count) |
| /best-laptop-screen-extender-under-300 | Mobile Pixels Duex Max DS | how many screens of each extender light on the shopper's laptop |
| /best-triple-laptop-screen-extender-under-400 | Mobile Pixels Trio 3 Pro | screens lit on a base M1/M2 MacBook Air, row by row |
| /best-laptop-screen-extender-for-16-inch-laptop | FOPO S11 | one video-capable port per screen, or a driver |
| /best-laptop-screen-extender-for-17-inch-laptop | FOPO S11 | side-screen picture height against a 17.3-inch panel, and the maker's fit range |
| /best-laptop-screen-extender-without-drivers | FOPO S11 | driver-free video path per product |

Every row of ours carries its buy link (`all_links`); FOPO rows show the code price beside the name (`buy_by_name`).
New product records: FOPO S1, S7, S10 (code FOPO cart-tested on each, links pre-apply it) and Mobile Pixels Duex Max DS.
The two Mobile Pixels product pages open with a where-to-buy line (`BUY_FIRST` in src/focus.py).

Fixed on the way: the FOPO S788's buy link pointed at a cart variant FOPO had deleted (410); four older pages quoted
Mobile Pixels and FOPO prices from 11-08..11-13 in their prose beside a table showing today's.

## Lessons

- FOPO's product pages carry a hidden "Sold out" badge in the markup, so a page fetch reads "Sold out" for items that are
  in stock (two research agents reported the S10 and S11 sold out). The cart decides: `tools/codecheck_browser.py`.
- A store can replace a product's variants without changing its URL; the record's `cart_variant` then answers 410 and the
  buy link (a cart permalink) is dead while the page still reads fine. `curl -o /dev/null -w '%{http_code}'
  https://<store>/cart/<variant>:1` with a browser user agent shows it.
- Research agents do not always use the fit ranges in our own records: the 17-inch draft left out the S11 (12–18.5 in)
  and S7 (12–17.3 in) and so picked the driver-based S788. Read every draft's "left out" lines against our records.
- Before a page says the maker's store is cheaper than another seller, read that seller the same day: Amazon had the
  Trio 3 Pro at $349.99 against the maker's $367.99, while it had the Duex Max DS and Duex Float 2 Pro $42–44 above.
- Mobile Pixels' prices moved three times in ten days (Trio $509.99 → $433.49 → $367.99). Prose uses `{price:slug}` and
  `{after:slug}` or a dated figure, never a bare dollar amount for our products.

## Reading

Due 2026-12-02 (14 days): clicks, landings and sales for 2026-11-19..12-02 with the queries above, against the baseline
of 7 clicks, 10 landings and 1 sale in the 7 days 11-11..11-17 (so compare per week). Read the six new pages by ChatGPT
rank and citation in plain chats (the harvest questions) and by landings and clicks in D1, not by `/go/` in plain chats.
