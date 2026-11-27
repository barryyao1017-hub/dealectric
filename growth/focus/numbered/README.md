# Numbered "best" pages, 2026-11-26 (DLC-363): monitors, keyboards, dash cams, power banks

Barry, 2026-11-26, after the page-shape read: build "best <product> <number>" pages for the four non-solar clusters
with traffic. His rule: the number a page features is not arbitrary; it captures what buyers in the cluster decide on,
and every featured product is an honest recommendation, starting from the products we link.

Why this shape (D1 since 10-28, shoppers only): "best X" pages with a number in the slug drew 1.88 ChatGPT visits per
page (103 pages, 43 visited), the highest non-seasonal shape, and it held for dash cams (1.75), power banks (6.5, one
page), monitors (1.33). Product pages draw 0.30 a page but hold 5 of the 6 page-traced sales, so every pick here needs a
product record behind it.

## How the numbers were chosen

One desk-research agent per cluster (WebSearch/WebFetch, 11-26): rank what buyers decide on from reviewers (RTINGS,
Wirecutter, DashCamTalk, Macworld, ChargerLAB, PC Gamer...) and Google search suggestions, place each of our products
against the leading rivals, and propose only questions where (a) the number is a real breakpoint, (b) one of our
store-linked products is honestly top 3, (c) no existing page covers it. Reddit was unreachable to the fetch tool.

| Cluster | What buyers decide on, in order | Pages built |
|---|---|---|
| Power banks | capacity tier (5K/10K/20K/25K/40K+); port watts matched to the device (iPhone 17 Pro Max ~36 W, Samsung 45 W needs PPS, MacBook Air fast charge needs a 70 W adapter so a 100 W port, 16-inch MacBook Pro 140 W PD 3.1); the FAA 100 Wh carry-on line; price tier; built-in cable | 20K for MacBook Air (100 W port); 10K with built-in cable (45 W); 25K under $100 (largest under 100 Wh); 40K for laptop (over 100 Wh: not a flying bank) |
| Dash cams | channel count; price cap ($100 strongest, then $200/$150/$300); 4K front; STARVIS 2 + HDR; parking mode | 2-channel (no uncapped page existed); 3-channel under $100; 4K under $200 |
| Laptop screens | screen size / which laptop; price; resolution (1080p soft on Macs at 14-16"); refresh; brightness (250-nit floor); weight (2 lb); one cable | for MacBook Pro 16 (16:10 1600p 120 Hz match); for 13-inch laptops; for MacBook Air 15 (by chip); lightest under 2 lb |
| Keyboards | price tier ($50/$100/$150); layout (60/65/75/TKL/full); wireless that keeps 8K; RT implementation; TMR vs Hall; polling; RT step (marketing only) | 65% low-profile (Lofree Flow 2 68); TMR under $100 (Gamakay TK75 TMR); full-size low-profile with number pad |

Each question in `growth/focus/ab-harvest-new-2026-11-26-numbered.json` carries `why` (the breakpoint and its source,
which the page states in its after-section) and `notes` (the research leads: ours and rivals with prices read 11-26).

## Rejected, because ours would not honestly place

- Freestanding portable monitors by price (under $100/$150/$200), 16-inch 2K, 144 Hz, 17/18-inch: Arzopa (Z1FC $92,
  Z1RC $118, Z3FC $133) and UPERFECT beat the Mobile Pixels Fold and Glance on price and brightness.
- 60% and TKL Hall effect, Hall effect under $150, low-profile under $50: Gamakay has no 60/TKL/full board; Keychron
  K2 HE and MonsGeek M1 V5 TMR beat it at $130.
- 65% Hall effect under $50: real demand, but every Gamakay NS68 and TK68 HE variant was unavailable 11-26. Build on restock.
- 4K 4-channel dash cam, 4K under $100, under $50: ours don't qualify.
- 10K power bank under $30, 10K magnetic under $80 (TORRAS 15 W at $79.99 vs 25 W Qi2.2 rivals at ~$55), 300 W.
- Samsung 45 W (PPS) and 5K magnetic: weak or overlapping; maybe later.

## Existing pages the research flagged (not changed in this run)

- Numbers nobody searches: dash cam "$250" caps (4K front and rear, 360-degree), 4-channel price caps; "1920x1200" in
  two triple-extender slugs (a 16:10 shape, not a resolution step); keyboard "8K polling under $100" (8K wired is
  standard; the real line is 8K over 2.4 GHz); "with number pad under $60" (searches say $50 / $100).
- Picks that may be unbuyable: the Gamakay NS68 (all variants unavailable 11-26) on the under-$50 Hall effect page;
  the FOPO S1 (record out of stock) on the extender under-$150 page.
- store.ddpai.com 301s to www.ddpai.com; record prices out of date: UGREEN 200W (store $80), AOHi Black Warrior ($89.99),
  TORRAS MiniMag Pro ($79.99).

## Run

- Driver `numberedpages.py` (same method as `growth/focus/clusters/clusterpages.py`: tools/abpage.py through openpage.py),
  with a "numbered" page rule: the after-section opens with why the number is the line, every row meets it as its maker
  states it, ranking inside the line uses the cluster's next two decision figures, and the page is skipped if none of
  ours honestly places in the top three.
- `stores-2026-11-26.json`: six partner power banks with no record (UGREEN 48K / 20K 130W / Pro 10K; Baseus FC41 20K,
  FC11 10K, FC41 10K 67W), read from the stores' Shopify .js in a background Agent Chrome tab. Keyboards and screens use
  the 11-21 store list (`growth/focus/clusters/stores-2026-11-21.json`).
- Harvest: `visibility_scan.py --questions growth/focus/ab-harvest-new-2026-11-26-numbered.json --run-id
  2026-11-26-numbered-harvest --n 2` (gpt-6-2).
