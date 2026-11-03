# UGREEN gap funnel (2026-11-03): the "find queries, build pages" test

Barry, 2026-11-03: test the gap method end to end on the newest CJ approval, looping (find a query, build the page,
publish) until he stops it. The loop here stops at the page written and published; no per-page ChatGPT app checks.
Retrieval is read in aggregate (OAI-SearchBot fetches, D1 landings tagged by ChatGPT, the daily update's clicks).

## Brand
- **UGREEN**, CJ 7918281, approved 2026-11-03 06:55Z ("commission started from 8%", 30-day cookie, "up to $180 in
  commission from a single NAS sale"). Program, five products and three codes were onboarded the same morning by
  the supply-loop session (DLC-148, commit dc71c31): `src/links.json` `cj:ugreen`, CJ text link 17334404 used as a
  deep link.
- **Two stores.** `us.ugreen.com` (chargers, banks, docks, cables; Shopify, per-product codes printed on the page
  as "Save N% Code: UL<SKU>") and the NAS store `nas.ugreen.com`, which 301s to `ai.ugreen.com` (NAS, UPS, some docks
  and banks at lower prices than us.ugreen.com: Nexode 200W bank $84.99 vs $129.99, Revodok Max TB5 dock $299.99
  vs $399.99-with-25%-code). The NAS store prints no codes; its prices on 11-03 are a Black Friday sale
  (DXP4800 Plus $619.99 against $729.99 compare-at).
- **CJ deep link lands on both stores with tracking** (curl, 2026-11-03): `tkqlhce.com/click-101901491-17334404?url=`
  → 200 on `us.ugreen.com/products/...?cjevent=...` and on `ai.ugreen.com/products/...?cjevent=...&utm_source=CJ`
  (both from a `nas.ugreen.com` destination and from an `ai.ugreen.com` one). Whether the conversion pixel fires on
  the NAS store's checkout is unverified (no order); the program email promises NAS commission.
- Warranty 2 years (both stores); returns 30 days from delivery (us.ugreen.com: refunds only; NAS store: refund or
  exchange within 30 days of receiving).

## Demand harvest (three Sonnet agents, WebSearch/WebFetch only, 2026-11-03, ~350k tokens)
Reddit is not reachable to the tools; threads came from Apple Community, MacRumors, Unraid/TrueNAS/Proxmox forums,
NASCompares, Level1Techs, DisplayLink forum. Counts are floors.

| Cluster | Threads | Reviewer coverage | UGREEN fit |
|---|---|---|---|
| Prebuilt NAS to run Unraid / TrueNAS / Proxmox | 5+ (three OS forums) | hobbyist how-tos only | DXP4800 Plus (x86, UEFI, UGREEN says third-party OS keeps the warranty) |
| 4-bay NAS with built-in 10GbE on a budget | 3+ | NASCompares tag pages | DXP4800 Plus $619.99: the only 4-bay with 10GbE under $700 seen |
| Plex 4K transcoding NAS with a price cap | 4+ | WunderTech/StarryHope, conflicting | DXP4800 Plus / DXP2800 (Quick Sync) |
| NAS for Docker / Immich / Home Assistant | 5+ | blogs | DXP2800 / DXP4800 Plus |
| All-SSD small NAS | 4+ | one roundup | DXP480T Plus $899.99 (contested vs TerraMaster F8) |
| Dock giving a 16" MacBook Pro the full 140W | 6+ | Tom's Hardware partly | Revodok Max TB5 $299.99 (140W, 180W PSU) |
| MacBook Air M4 → two extended monitors | 10+ | none for M4 | Revodok Max 213 TB4; Revodok DisplayLink units have Tahoe complaints |
| Charger that gives two laptops 100W each | not found (inferred) | Tom's Hardware tested 20 chargers, not this | Nexode 200W 4-port $61.99 ("two USB-C ports each 100W"), Nexode 500W (240W + 100W) |
| Laptop power bank under 100 Wh, N charges | inferred | generic lists | Nexode 200W 25,000 mAh (already in the catalog) |
| Travel charger with EU/UK plugs, retractable cables, cool-running charger, car charger 100W+ | inferred | partial | various Nexode |

## Honest-win and price screen
- Amazon's live November prices were not reachable (pages refuse fetches, trackers 403). Last dated snapshots:
  DXP4800 Plus $565–657 on Amazon (Jan–Jun 2026) against $619.99 on UGREEN's store today; DXP2800 $389.99 both.
  Pages state prices as read on UGREEN's store with the date, and do not claim a price win over Amazon.
- Commission per sale at 8%: DXP4800 Plus ≈ $50, DXP2800 ≈ $31, TB5 dock ≈ $24, Nexode 200W charger ≈ $5.

## Gap vote (OpenAI API packs, `fastloop.py pack --engine api`; judges Sonnet 5.5 / Opus 5.5 / Fable 5.1, v2 prompt)
| pack | ChatGPT-style query | votes | verdict |
|---|---|---|---|
| ug-nas-unraid-1 | best prebuilt NAS for Unraid or TrueNAS 2026 Intel price | open ×3 | **open** |
| ug-nas-unraid-2 | best 4 bay NAS to run Unraid 2026 under $700 x86 | open ×3 | **open** |
| ug-nas-10gbe-1 | NAS with built-in 10GbE under $700 2026 4 bay | open ×3 | **open** |
| ug-nas-10gbe-2 | cheapest 10GbE NAS 2026 4 bay Intel Plex transcoding price | open ×3 | **open** |
| ug-dock-140w-1 | Thunderbolt dock that charges MacBook Pro 16 at 140W 2026 price | open/contested/contested | contested (Tom's Guide, Plugable partly answer it) |
| ug-charger-2laptops-1 | GaN charger that charges two laptops at 100W each at the same time 2026 | open ×3 | **open** |

Note: `fastloop.py vote`'s named-query guard read "10GbE" and "x86" as brand names and skipped three packs; they were
re-run with `--allow-named`. Worth fixing in `named_query()`.

What the judges said is missing, in short: a side-by-side of the actual prebuilt boxes with current prices and, per
model, verified behaviour under TrueNAS/Unraid (BIOS access, USB boot, NIC and iGPU drivers, fan/LED control,
warranty stance, Unraid licence folded into the total); for 10GbE, every under-$700 4-bay with built-in 10GbE
(DXP4800 Plus, DXP4800 GT, DXP4800 Pro on sale, TerraMaster F4-424 Max) with the add-in-card alternatives' total
cost and whether each price is a promo; for the charger, chargers whose allocation tables really hold 100W on two
ports at once, with prices.

## Pages built
See the log below; records in `src/gaps.py` (slugs `best-nas-for-unraid-truenas`, `best-4-bay-nas-10gbe-under-700`,
`usb-c-charger-two-laptops-100w`) and products in `src/products.py` (UGREEN section).

## Log
- 2026-11-03: harvest, screen, votes as above. Dock cluster parked (contested).
- 2026-11-03: three pages built and published (G16 `best-nas-for-unraid-truenas`, G17 `best-4-bay-nas-10gbe-under-700`,
  G18 `usb-c-charger-two-laptops-100w`), with four new product records (DXP4800 Plus $619.99, DXP2800 $389.99,
  Nexode 200W 4-port $61.99, Nexode 500W $249.99 with page code UL55549 = $199.99, cart-tested with the control
  rejected; UL75752 on the 300W also passed but that charger is not listed). Rival facts: two Sonnet research agents
  (~310k tokens); several maker pages (TerraMaster, UGREEN US, CalDigit) answered 429, so those rows cite reviews
  that quote the maker. `fastloop.py check` passes all three at ranks 1/3/6 after trimming: the product-result line
  (~730 chars) and the lead tie on query words and the tie goes to the earlier chunk, so both must fit the rank-6
  share (1,309) together; shorter record title/description and a lead of about 450 chars did it. Cost of the run so
  far: about 1.0M tokens of subagents (3 harvests 350k, Amazon check 105k, 3 research 440k) plus this session's
  own reading and writing; 6 OpenAI search packs and 18 Claude CLI judge calls.
- Open: Amazon's live price for the DXP4800 Plus (unreachable from the tools; last snapshots $565–657); a UGREEN
  primary source for the third-party-OS warranty line (NASCompares quotes a UGREEN rep, 26 Mar 2024); whether the
  CJ pixel fires on the NAS store's checkout (first NAS sale will tell).
