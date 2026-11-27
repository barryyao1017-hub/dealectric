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

## Result (2026-11-26, pushed 8944173c, Worker redeployed)

12 pages live, 2 skipped by research. Pick = the page's first answer; "ours" = a product we link.

| Page | Pick | Ours on the page |
|---|---|---|
| best-20000mah-power-bank-for-macbook-air | UGREEN Nexode 20K 130W (ours) | UGREEN ×2, Baseus FC41 20K |
| best-10000mah-power-bank-with-built-in-cable | INIU Carry 45W (not ours) | Anker Nano A1638 (2nd; 45 W Galaxy pick) |
| best-25000mah-power-bank-under-100 | UGREEN 145W (ours) | UGREEN ×2, Baseus FC41 25K, AOHi |
| best-40000mah-power-bank-for-laptop | AOHi Starship 40K (ours) | AOHi, UGREEN 48K |
| best-2-channel-dash-cam | VIOFO A329S (not ours) | Vantrue S1 Pro Max 4K+4K (3rd) |
| best-3-channel-dash-cam-under-100 | Vantrue OnDash N4 (ours) | Vantrue |
| best-4k-dash-cam-under-200 | VIOFO A119M Pro, Amazon $132.99 (tagged link) | Vantrue S1 Pro Max 1CH and 4K+2.5K |
| best-laptop-screen-extender-for-13-inch-laptop | Mobile Pixels Duex Plus DS | Mobile Pixels ×2, FOPO ×2 |
| best-laptop-screen-extender-for-macbook-air-15 | Mobile Pixels Duex Float 2 Pro | Mobile Pixels ×4 |
| lightest-laptop-screen-extender-under-2-lb | Mobile Pixels Duex Plus DS | Mobile Pixels ×4 |
| best-65-percent-low-profile-mechanical-keyboard | NuPhy Air65 V3 (not ours) | Lofree Flow 2 68 (2nd; aluminum/VIA) |
| best-tmr-keyboard-under-100 | Gamakay TK75 TMR (ours) | Gamakay |

New records: UGREEN Nexode 20K 130W, UGREEN 48K 300W, Baseus FC41 20K 100W, Vantrue S1 Pro Max 1CH, Lofree Flow 2 68
(Black Friday 20% in cart added by hand, as on its siblings). None has a passing code today, so no `cart_variant`.

Skipped (research reasons in `growth/focus/ab/<folder>/`): x1126-macbook-pro-16 (stores rate-limited; the Float 2 Pro
likely 4th of 4 on brightness and weight), k1126-full-size-low-profile (Keychron K5 Ultra/Max and NuPhy Air100 beat the
Lofree 100-key boards on price and stock; writable if a Keychron Amazon record is added).

## Power stations, 2026-11-27 (Barry: "Yes, power stations")

Why: shopper visits since 10-28 put numbered power-station pages at 3.25 visits/page against 0.31 for every other
power-station page shape (situation pages like "power station to run X in an outage" drew ~0), and BLUETTI + ALLPOWERS
hold 58 of 63 sales. Cluster `s1127` in `numberedpages.py`; questions in
`growth/focus/ab-harvest-new-2026-11-27-numbered-ps.json`; harvest run `2026-11-27-numbered-ps-harvest` (20 chats).

How the numbers were chosen (desk research 11-27, Google suggest + Outdoor Gear Lab, Notebookcheck, StorageReview,
The Solar Lab, Backup Power Hub's store tracker): price cap first ($200 ~300 Wh class; $300 top of the small class;
$400-500 a 1 kWh LiFePO4 unit; $1,000 a 2 kWh unit or the cheapest 3 kWh); capacity tiers (1,000 / 2,000 / 3,000 /
5,000 Wh); continuous AC watts (3,000 W runs heater + microwave or most of a TT-30; 5,000 W+ means a 120/240 V unit;
many "3000W" listings are surge); weight (the ~50 lb one-person carry line, NIOSH 51 lb).

| Page | Pick | Ours placed |
|---|---|---|
| [best-power-station-under-200](https://dealectric.com/best-power-station-under-200) | BLUETTI Elite 30 Mini (ours) | 1 |
| [best-power-station-under-300](https://dealectric.com/best-power-station-under-300) | Pecron E500LFP (Amazon) | Elite 30 V2, Elite 30 Mini lower |
| [best-1000wh-power-station-under-400](https://dealectric.com/best-1000wh-power-station-under-400) | DJI Power 1000 V2 at Micro-Tools $379.99 | Elite 100 Mini 2, P1800 4 |
| [best-power-station-under-500](https://dealectric.com/best-power-station-under-500) | DJI Power 1000 V2 at Micro-Tools | Elite 100 Mini 2 |
| [lightest-2000wh-power-station](https://dealectric.com/lightest-2000wh-power-station) | Anker SOLIX S2000 (ours; ships in 7-13 weeks, said in the answer) | 1 |
| [best-power-station-under-1000](https://dealectric.com/best-power-station-under-1000) | Pecron F3000LFP (pre-order, no link) | Elite 200 V2 2, S2000 3 |
| [best-3000w-power-station](https://dealectric.com/best-3000w-power-station) | Dabbsson 3000L (Amazon $969) | ALLPOWERS R3500 2 |
| [best-3000wh-power-station](https://dealectric.com/best-3000wh-power-station) | BLUETTI Elite 300 (ours) | 1 (Jackery HomePower 3000 tested better but every variant sold out 11-27) |
| [best-5000w-power-station](https://dealectric.com/best-5000w-power-station) | Nature's Generator L6000 (ours; deal ends 11-29) | 1 |
| [best-5000wh-power-station](https://dealectric.com/best-5000wh-power-station) | EcoFlow TITAN 5000 Classic (Amazon) | Anker S5000 2 (ships in 15-16 weeks) |

Rejected: best 500Wh (nothing of ours between 400 and 800 Wh), 2000W (duplicate of best-2000wh-power-station), 30 A /
50 A RV (duplicates, or our 14-50 units sold out), UPS 10 ms (covered), 1500/1800 W (covered; DJI beats the P1800),
plain best 1000Wh (ours 3rd-4th), under $100, lightest 3000Wh, 2000Wh under $700.

Fixes made by hand before publish: the 3000Wh draft led with the sold-out Jackery (moved below the in-stock Elite 300);
both DJI pages' pick line sent shoppers to Amazon at $469.99 while Micro-Tools sold it at $379.99 (row now links
Micro-Tools, no affiliate; `build.py` pick rows take an optional `seller`). Lessons: the research step cannot see that
a rival's Amazon record price differs from the dealer price it quotes; check every keep-pick and Amazon pick line
against the answer's price before publishing. Brand stores 429 WebFetch: read partner prices in the Agent Chrome
first and put them in the question notes (done here; Anker S2000 7-13 weeks and HELIOS $1,599 came from that).
Growatt HELIOS 3600 record still says $1,399 (store page $1,599 on 11-27; not used by these pages).
