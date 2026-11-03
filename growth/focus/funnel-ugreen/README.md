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
Records in `src/gaps.py` and products in `src/products.py` (UGREEN section).

| # | page | pick | vote |
|---|---|---|---|
| G16 | /best-nas-for-unraid-truenas | DXP4800 Plus $619.99 | open ×3 (two packs) |
| G17 | /best-4-bay-nas-10gbe-under-700 | DXP4800 Plus | open ×3 (two packs) |
| G18 | /usb-c-charger-two-laptops-100w | Nexode 200W $61.99; 500W $199.99 w/ UL55549 | open ×3 |
| G19 | /best-all-nvme-nas-under-900 | DXP480T Plus $899.99 | open ×3 |
| G20 | /best-65w-travel-charger-interchangeable-plugs | Nexode 65W travel $49.99, $37.99 w/ UL90409 | open/open/contested |
| G21 | /best-nas-under-500-for-docker-immich-home-assistant | DXP2800 $389.99 | open ×3 |
| G22 | /best-nas-for-photographers-10tb-raw-lightroom | DXP4800 Plus; DXP2800 | open ×3 |
| G23 | /best-usb-switch-two-computers-keyboard-mouse-ssd | USB-C Switch CM691 $40.99 | open ×3 |
| G24 | /thunderbolt-5-ssd-enclosure-worth-it-macbook-pro-m4 | TB5 enclosure with fan $159.99 w/ UL45789; fanless $159.99 w/ UL95583 | open ×3 |
| G25 | /best-40gbps-nvme-enclosure-no-throttling | 40Gbps fan enclosure CM642 $75.99 w/ UL15976 | open ×3 |
| G26 | /usb-c-cable-240w-and-40gbps | Thunderbolt 5 cable $31.99 | open/contested/open |
| G27 | /best-8-bay-nas-under-1500-home-media | DXP8800 Plus $1,369.99 | open ×3 |
| G28 | /best-6-bay-nas-10gbe-intel-transcoding | DXP6800 Pro $1,099.99 | open ×3 |
| G29 | /best-small-ups-for-home-nas | US3000 $109.99 (UGREEN owners); APC BE600M1 named for the rest | open ×3 |
| G31 | /best-nas-under-500-for-plex-4k-transcoding | DXP2800 $389.99; TerraMaster F2-425 Plus named as the native-app alternative | open ×3 |
| G32 | /best-nas-under-1000-for-small-office-10-users | DXP4800 Plus for hardware; Synology DS925+ named for the office software | open ×3 |
| G33 | /best-nas-for-4k-video-editing-thunderbolt-10gbe | DXP6800 Pro; DXP480T Plus for all-flash Thunderbolt | open ×3 |
| G34 | /best-nas-under-400-for-jellyfin | DXP2800 | open ×3 |
| G35 | /best-2-bay-nas-for-time-machine-backups | DXP2800 (one share per Mac); DS225+ named as the safer software | open ×3 |
| G36 | /power-station-to-run-a-refrigerator-for-24-hours | BLUETTI Elite 200 V2 (other brand); ALLPOWERS S2000 Pro | open ×3 |
| G39 | /best-nas-for-proxmox-virtual-machines-home-lab | DXP4800 Plus; DXP6800 Pro; Minisforum MS-A2 named for bay-less VM hosts | open ×3 |
| G40 | /best-all-in-one-home-server-under-800-docker-plex-vms | DXP4800 Plus; TerraMaster F4-425 Plus named (16 GB stock) | open ×3 |
| G41 | /best-2-bay-nas-under-300-home | DH2300 $239.99 (photos); TerraMaster F2-425 named for Docker/2.5GbE | open ×3 |
| G42 | /best-nas-for-nextcloud-self-hosted-cloud | DXP2800; DXP4800 Plus | open ×3 |
| G43 | /best-nas-to-replace-google-photos-family-library | DXP2800; DH2300 budget | open ×3 |
| G44 | /best-nas-for-immich-iphone-photo-backup | DXP2800 | open ×3 |
| G45 | /best-nas-to-replace-dropbox-freelancer | DXP2800 as the value pick; Synology Drive named for on-demand files and versions | open ×3 |
| G46 | /best-nas-with-thunderbolt-4-direct-to-mac | DXP480T Plus (cheapest TB4 NAS) / DXP6800 Pro; QNAP TBS-h574TX, TS-h966TX, TVS-h874T and DAS arrays named; link explained as an IP bridge, not a drive | open ×3 |
| G47 | /best-nas-for-frigate-security-cameras | DXP4800 Plus with OpenVINO on the iGPU; "untested on UGOS by any reviewer" said in the lead; Frigate's own requirements laid out | open ×3 |
| G48 | /can-a-nas-host-a-minecraft-server | DXP2800 (N100 single-core clock) / DXP4800 Plus for 10+ players or mods; port 25565 / playit.gg | open ×3 |
| G49 | /best-nas-for-music-streaming-navidrome-plexamp | DXP2800 (UGREEN's own Navidrome guide); DH2300 ruled out (no Docker); Plex Pass and Roon prices dated | open ×3 |
| G50 | /qi2-car-charger-that-keeps-iphone-cool | UGREEN MagFlow Pro Qi2 25W car charger (new record, UL75250 $10 off) + ESR HaloLock CryoBoost; Anker Prime AirCool named; every cooling figure labelled a maker's claim | open ×3 |
| G51 | /best-nas-for-paperless-ngx-document-archive | DXP2800; lead says a mini PC or Pi is enough for a small archive and Synology/Asustor have the guides; scanners that write to the consume folder | open ×3 |
| G52 | /best-nas-to-record-reolink-cameras-24-7 | Reolink RLN8-410 named first for camera-only buyers; DXP2800 with UGOS Surveillance Center (called a first-version app) for NAS buyers; Synology licence cost spelled out | open ×3 |
| G53 | /best-nas-for-audiobookshelf-calibre-web | DXP2800; lead says the official iPhone app is TestFlight-only and a Pi/mini PC runs both apps | open ×3 |
| G55 | /best-alternative-to-synology-4-bay-nas-home | DXP4800 Plus; states DSM 7.3's reversal (HDD/SATA open, M.2 still listed-only) before making the Plex/10GbE/price case; UGOS gaps listed | open ×3 |
| G56 | /power-station-to-charge-an-ebike-camping | BLUETTI Elite 200 V2 (only 2 kWh unit with a measured 1,910 Wh); spare battery named as the cheaper answer for one bike; rivals' $/Wh dated | open ×3 |
| G57 | /best-nas-for-pihole-adguard-wireguard-vpn | DXP2800 for storage + VPN; lead says a NAS is the wrong place for house DNS (UGOS holds port 53, reboots drop DNS); QNAP/Asustor named for documented native WireGuard; UGOS VPN Server claim marked unconfirmed | open ×3 |
| G58 | /cheapest-nas-for-infuse-apple-tv-4k-remux | Synology DS223j named first as the proven cheapest; DH2300 as the pick for NFS, 4 GB RAM, quiet, HDMI; "no Infuse-plus-UGOS test exists" said | open ×3 |
| G59 | /best-nas-for-veeam-macrium-windows-image-backups | Synology DS225+ with Active Backup named first for install-and-forget; DXP2800 for Veeam/Macrium users; UGOS has no documented immutable snapshots | open ×3 |
| G60 | /nas-that-runs-on-12v-in-a-van-or-rv | DH2300 (12 V adapter, 3–11 W); DXP2800 also 12 V; DXP4800 Plus/DXP480T Plus need a boost converter; Pi 5 named as drawing a third as much; "no measured van install" said | open ×3 |
| G61 | /power-station-to-run-a-sump-pump-12-hour-outage | BLUETTI Elite 300 (12 h at 10 % duty); R4000 for 25 %; no station-starts-a-pump test exists, lifting watts excluded; battery-backup and water-powered pumps named as the unattended answers | open ×3 |
| G62 | /power-station-for-starlink-mini-and-macbook-off-grid | AC180 for a day, Elite 200 V2 for 3–4 days; Starlink's 100 W PD rule; Anker/Jackery named as lighter with more USB-C | open ×3 |
| G63 | /nas-remote-access-behind-cgnat-starlink-no-port-forwarding | Synology QuickConnect/BeeStation named first as the proven relay; DXP2800 for a household with one tech-comfortable person (UGREENlink + Tailscale); UGREENlink speed and photo-app reliability marked untested | open ×3 |
| G64 | /can-a-nas-replace-icloud-2tb-for-an-iphone-family | "Partly": photos/files/Time Machine yes, device backup and Photos sync no, costs more than $599 over 5 years with off-site; DXP2800 + Immich; BeeStation named for non-technical families | open ×3 |
| G65 | /power-station-for-a-cpap-week-of-camping | AC180 via ResMed's DC converter (9 dry nights); Elite 200 V2 for humidifier-on; ECO-mode warning; Medistrom named for flying | open ×3 |
| G66 | /power-station-to-run-a-chest-freezer-for-3-days | Elite 300 is a 2-day unit alone (19 W idle), 3 days with a 400 W panel; AC200L + B300K for 3 days without sun; solar under storm cloud 10–25 %; generator named for longer outages | open ×3 |
| G67 | /can-a-portable-power-station-charge-an-ev-in-an-emergency | "Barely": 3–7 miles in 1–2 h if the EVSE accepts a floating neutral; call roadside first; Elite 300 as the pick; EcoFlow DP3 / Anker F3800 named as the units sold for EV charging | open ×3 |
| G68 | /nas-that-runs-home-assistant-os-vm-zigbee | DXP2800 runs HAOS in UGOS's VM (verified by two guides) but USB passthrough is contradicted by UGREEN's own article, so a wired SLZB-06 coordinator is the route; Home Assistant Green named as the appliance answer | open ×3 |
| G69 | /can-a-nas-replace-google-drive-for-a-small-team | "Files yes, Docs no"; Synology Drive + Office named for non-technical teams and Workspace Standard for truly remote ones; DXP2800 as the DIY Nextcloud route; the host's upload speed named as the real cost | open ×3 |
| G70 | /best-nas-under-400-for-a-beginner-home-lab | DXP2800 (x86, 8 GB, Compose projects, VM app, SSH); an N100 mini PC named as the better pure-learning buy; TerraMaster F2-425 Plus flagged if under $400; third-party-OS warranty stance marked unofficial | open ×3 |
| G71 | /power-station-to-run-a-window-ac-while-camping | "Only the 3 kWh class, and only with an inverter AC"; Elite 300; R4000 for a conventional unit; EcoFlow Wave 3 named for tents; no measured overnight test exists | open ×3 |
| G72 | /power-station-for-an-aquarium-24-hour-outage | Elite 300 only with the heater setpoint managed (3.1–3.4 kWh otherwise); AC180 for aeration + filtration; battery air pump named as the $30–110 insurance | open ×3 |
| G73 | /power-station-to-keep-insulin-cold-in-a-power-outage | FDA and label rules quoted (in-use insulin fine under 86 °F; unopened stock needs 36–46 °F); AC180 + 12 V compressor cooler on the DC port, 2–3.5 days; Frio wallet named as the cheapest adequate plan | open ×3 |
| G74 | /ups-for-a-bambu-lab-3d-printer-power-outage | CyberPower/APC pure-sine UPS named first for flickers; AC180 for a multi-hour outage; Bambu's own power table and power-loss recovery limits; T320 and US3000 ruled out | open ×3 |
| G75 | /kvm-switch-for-a-mac-and-pc-4k-144hz | "No KVM is proven at 4K144 with a Mac"; monitor with built-in KVM + our UGREEN USB switch as the answer; Level1Techs/TESmart/UGREEN claims laid out; us.ugreen.com KVM prices unreadable (429) | open ×3 |
| G77 | /cheap-nas-as-a-remote-hyper-backup-target | A second Synology with Hyper Backup Vault named first; DH2300 as a single-version rsync mirror (no .hbk, no versions); Backblaze B2 / C2 as the no-hardware answer | open ×3 |
| G78 | /can-you-host-a-wordpress-site-on-a-nas-at-home | "You can, and mostly you shouldn't": shared hosting renewal prices and a VPS named first; DXP2800 behind a Cloudflare Tunnel for hobby/private/staging sites; Xfinity's AUP quoted | open/open/contested |
| G80 | /power-station-to-run-a-pellet-stove-in-an-outage | Elite 300 (13 h at 150 W); R4000 for margin (sold out today); Harman P43 label and owners' Kill-A-Watt readings; no BLUETTI/ALLPOWERS owner run exists | open ×3 |
| G81 | /power-station-to-run-a-gas-furnace-in-an-outage | Elite 300 (about 10 h PSC, 19 h ECM); the only safe hookup is a UL 1008 furnace transfer switch by an electrician (Reliance manual, NEC 702 quoted); AC180/P1800 ruled out for PSC starts | open ×3 |
| G82 | /power-station-for-a-farmers-market-booth | AC180 (restock late Nov) with the Elite 200 V2 as the in-stock fallback; ENERGY STAR mini-fridge data, Vitamix 2 HP; 300 Wh units for lights + reader only | open ×3 |
| G83 | /power-station-and-solar-panel-for-an-off-grid-cabin-weekend | Elite 200 V2 + 350 W ($1,249); ENERGY STAR compact-fridge Wh/day and NREL PVWatts sun-hours by region; December is battery-only | open ×3 |

Parked: 140W TB5 dock (contested), MacBook Air M4 dual-monitor dock (contested), retractable-cable laptop power
bank (saturated: Tom's Guide, Macworld, Wired, Engadget all answer it).

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
- 2026-11-03, iteration 2: vote on five more packs (`ug2-*`): Docker/Immich NAS open ×3, all-NVMe NAS open ×3, travel
  charger open/open/contested, MacBook Air dual-monitor dock contested, retractable-cable bank saturated. Three pages
  built (G19–G21) with two new product records (DXP480T Plus, Nexode 65W travel; UL90409 $12 off cart-tested, control
  rejected; the charger-alone variant is $49.99, the page's $44.98 is a bundle with two cables). All three passed
  `fastloop.py check` first time with the lead kept near 450 chars. Three research agents ~360k tokens. Fixed
  `named_query()`: spec tokens (10gbe, x86, ddr5, pcie4, m.2, tb4) no longer count as names.
- 2026-11-03, batch 3 votes (`ug3-*`): one charger for a 16" MacBook Pro + iPhone + iPad contested ×3 (Tom's Guide,
  TechRadar, Apple); 100W car charger open/contested/contested (Android Central, Wired); Thunderbolt dock with 2.5GbE
  contested ×3 (Tom's Hardware, Macworld); iPad Pro M4 hub open/contested/contested (TechRadar, Tom's Guide);
  **NAS for a photographer with 10 TB of RAW files open ×3** (Fstoppers' guide is a list, no sizing or Lightroom
  facts). Building G22 on the DXP4800 Plus. Batch 4 (`x4-*`, other brands allowed): 3kWh-class power station under
  $1,100 (BLUETTI Elite 300), retractable-cable wall charger, display power bank, Steam Deck dock, USB switch.
- 2026-11-03, G22 built (photographer NAS, 10 TB RAW, Lightroom): Adobe's catalog-must-be-local rule and Smart
  Previews from helpx (read through a text proxy; helpx 403s direct fetches), Fstoppers' 285 MB/s measurement of the
  DXP4800 Plus over 2.5GbE. Drive prices only as a 2026 range (sources disagree; none dated for November).
- 2026-11-03, batch 4 votes (`x4-*`): **3kWh-class power station under $1,100 open ×3** but parked: the judges name
  Pecron, Dabbsson, OUPES and Anker F3000 at sale prices (none linkable; OUPES and Dabbsson are pending on Awin) and
  the BLUETTI Elite 300 was $1,199 on 11-02 ($1,139 with DEALECTRIC), so our pick would not honestly be under $1,100
  until BLUETTI's automatic discount returns ($1,099 on 11-01). Retractable-cable wall charger saturated/contested
  (Android Authority, MacRumors, Macworld, Tom's Hardware); display power bank contested; Steam Deck dock saturated
  (GamesRadar, PCGamesN, Pocket Tactics); **USB switch for two computers open ×3** → G23 on the UGREEN USB-C switch
  ($40.99, 4× 10Gbps).
- 2026-11-03, G23 built (USB switch, two computers): new record `ugreen-usb-c-switch-2-computers-4-port-10gbps` and a
  `usb-switch` category. Only three 10Gbps switches exist (UGREEN, Cable Matters 201160, ATEN US3342). Gate passed
  after two trims: the record line and the lead tie on all eight query words, so 179 + record + lead had to fit 1,309.
- 2026-11-03, batch 5 votes (`x5-*`): Mac mini M4 dock contested (TechRadar, Tom's Guide, Macworld); **40Gbps NVMe
  enclosure that doesn't throttle open ×3**; **Thunderbolt 5 enclosure for a MacBook Pro M4 open ×3**; **240W + 40Gbps
  cable open/contested/open**; 300W desktop charger contested (Macworld, Tom's Hardware, Notebookcheck). Three pages
  built (G24–G26) with four new records: TB5 enclosure fanless (SKU 95583, $229.99, UL95583 $70 off) and with fan
  (SKU 45789, $259.99, UL45789 $100 off; both $159.99 after the code, cheaper than ORICO X50 Pro, OWC and Satechi),
  40Gbps fan enclosure CM642 (SKU 15976, $109.99, UL15976 $34 off), Thunderbolt 5 cable (SKU 45996, $31.99, no code).
  All codes cart-tested with the control rejected. Conflicts recorded on the pages: UGREEN's US page for SKU 95583
  describes fins, ChargerLAB's teardown of "the UGREEN TB5 enclosure" found a fan (SKU unstated); UGREEN's
  "Intel-certified" claim on the TB5 cable could not be checked in Intel's list. Three research agents ~355k tokens.
- 2026-11-03, batch 6 votes (`x6-*`), all five open ×3: 8-bay NAS under $1,500 (→ G27, DXP8800 Plus $1,369.99),
  6-bay NAS with 10GbE and Intel transcoding (→ G28, DXP6800 Pro $1,099.99), small UPS for a home NAS (→ G29, US3000
  $109.99, honest framing: UGREEN's DC UPS fits only its own 2–4-bay NASync units, so the page also names the AC units
  everyone else buys), quietest 2-bay NAS for a bedroom (**parked**: UGREEN quotes 29–34 dB in quiet mode while
  Synology and TerraMaster spec about 19 dB(A), so the DXP2800 would not honestly win), Plex 4K NAS under $500 (→ G31,
  DXP2800). New records: DXP8800 Plus, DXP6800 Pro, US3000 UPS (`ups` category). Four research agents started.
- 2026-11-03, iteration 6 built (G27, G28, G29, G31) from four research agents (~470k tokens). Honesty notes carried
  on the pages: the TerraMaster F6-424 Max has the DXP6800 Pro's chip and dual 10GbE for less (no Thunderbolt or PCIe);
  the TerraMaster F2-425 Plus runs Plex as a native app where UGOS needs Docker; the US3000 UPS fits only UGREEN's
  2–4-bay units and no lab has measured its runtime; the DXP8800 Plus is the only sub-$1,500 8-bay with both built-in
  10GbE and an Intel iGPU. Gate trims needed on G31 (title + record + lead must fit 1,309 at rank 6).
- 2026-11-03, batch 7 votes (`x7-*`), all five open ×3: NAS under $1,000 for a 10-person office (→ G32, DXP4800
  Plus), NAS for 4K video editing over Thunderbolt / 10GbE (→ G33, DXP6800 Pro / DXP480T Plus), Jellyfin NAS under
  $400 (→ G34, DXP2800), 2-bay NAS for Time Machine from two Macs (→ G35, pick pending the UGOS Time Machine facts:
  Synology's DSM is the classic answer), power station to run a full-size refrigerator for 24 h (→ G36, BLUETTI /
  ALLPOWERS, other brands allowed). Five research agents started; no new product records needed.
- 2026-11-03, iteration 7 built (G32–G36) from five research agents (~650k tokens). Honesty notes on the pages: UGOS
  has no native S3/B2 backup, no endpoint backup and reported AD-join failures (G32 names the DS925+ for those);
  UGOS Time Machine quotas are per share, so one share per Mac (G35); the fridge page uses ENERGY STAR medians and
  one named-outlet measurement (Bob Vila, 30+ h on the Elite 200 V2) and labels the rest arithmetic. G36 needed the
  second buy link moved out of the lead to pass rank 6.
- 2026-11-03, batch 8 votes (`x8-*`), all five open ×3. Built: NAS for Proxmox / several VMs (→ G39, DXP4800 Plus /
  DXP6800 Pro), all-in-one home server under $800 (→ G40, DXP4800 Plus); pending the HDMI facts: NAS with HDMI output
  to a TV (→ G38 only if UGOS has a real media interface on HDMI; QNAP HD Station and Asustor Portal do). **Parked**:
  4-bay NAS under $500 (the judges want Intel boxes; UGREEN's only 4-bay under $500 on its US store is the ARM
  DH4300 Plus at $399.99, and the base DXP4800 is not listed there), NAS for backing up several PCs and Macs
  (Synology's Active Backup for Business is the honest pick; UGOS has no endpoint backup, see G32).
- 2026-11-03, G38 (NAS with HDMI to a TV) **parked** after the HDMI research: UGOS Pro's HDMI port plays video only
  when started from the phone app (beta, phone as the remote, no TV interface, no remote or keyboard navigation;
  BGR 2026-10-08, Soundphile 2026-09, ugreen-forum), while QNAP's HD Station and Asustor's Portal are real local
  interfaces. Not an honest win; revisit if UGOS ships a TV interface.
- 2026-11-03, iteration 8 built (G39, G40) from three research agents (~380k tokens, one of them the HDMI verdict
  that parked G38). Honesty notes: Proxmox on UGREEN rests on owner reports (SATA passthrough works, iGPU passthrough
  is a "99%" report, 64 GB is Intel's spec with a 48 GB module owner-verified); the home-server bill with 16 GB and
  an NVMe runs $980–1,050 at late-2026 memory prices, so the page says only the NAS plus one upgrade fits under $800.
- 2026-11-03, batch 9 votes (`x9-*`), all five open ×3: 2-bay NAS under $300 (→ G41, DH2300 $239.99 vs the x86
  TerraMaster F2-425 at the same price, both named), Nextcloud NAS (→ G42, DXP2800 / DXP4800 Plus), family photo
  library as a Google Photos alternative (→ G43, DXP2800 + DH2300), Immich iPhone backup (→ G44, DXP2800), Dropbox
  replacement for a freelancer (→ G45 only if UGREEN's sync client holds up against Synology Drive; else parked).
  Five research agents started; DH2300 record to add.
- 2026-11-03, iteration 9 built (G41–G45) from five research agents (~570k tokens) plus a new DH2300 record (its
  spec table says 1× 1GbE, correcting the harvest's "2.5GbE"). Honesty notes: UGOS Photos' AI features are
  DXP-series items per UGREEN's own notes (the DH2300 gets basic tagging); Immich's iOS backup is opportunistic
  (Immich's docs); UGOS has no official Nextcloud guide; UGREEN's sync client has no on-demand files or client-side
  versions, so G45 names Synology Drive for those. G43 and G44 needed lead trims for rank 6.
- 2026-11-03, batch 10 votes (`x10-*`), all five open ×3: NAS with Thunderbolt 4 (→ G46, DXP480T Plus / DXP6800 Pro),
  NAS for Frigate (→ G47, DXP4800 Plus with OpenVINO on the iGPU), NAS as a Minecraft server (→ G48, DXP2800 /
  DXP4800 Plus), NAS for a FLAC library with Navidrome or Plexamp (→ G49, DXP2800), Qi2 car charger that keeps an
  iPhone cool (→ G50, ESR HaloLock CryoBoost and UGREEN MagFlow Pro car charger; other brand allowed). Five research
  agents started.
- 2026-11-03, iteration 10 built (G46–G50) from five research agents (~600k tokens) plus a new product record
  (UGREEN MagFlow Pro Qi2 25W car charger with cooling, $49.99, UL75250 $10 off cart-tested). Honesty notes: no outlet
  has measured cooled vs uncooled car mounts, so G50 calls every temperature figure a maker's claim and quotes Apple's
  own heat rule instead; Frigate on UGOS has no published working report, said in G47's lead; the DH2300 is ruled out
  for Navidrome/Plex in G49. G46 and G48 needed lead and record trims for rank 6 (record line 700 chars + lead must
  fit 1,309 with the title chunk).
- 2026-11-03, batch 11 votes (`x11-*`), all six open ×3: NAS for Paperless-ngx (→ G51, DXP2800), NAS to record four
  Reolink PoE cameras with no subscription (→ G52, DXP2800 if UGOS has a camera app or the Reolink FTP/SMB route
  holds; else Synology/Reolink NVR named), NAS for Audiobookshelf + Calibre-Web (→ G53, DXP2800), Steam library on a
  10GbE NAS (→ G54 only if a NAS honestly beats a second local SSD for some shopper; else parked), alternative to a
  Synology 4-bay after the drive policy (→ G55, DXP4800 Plus; must state DSM 7.3's status correctly), power station to
  recharge a 700 Wh e-bike twice on a weekend (→ G56, BLUETTI Elite 200 V2 / AC200L / ALLPOWERS S2000 Pro by price per
  Wh). Six research agents started (Sonnet, WebSearch/WebFetch only).
- 2026-11-03, G54 (Steam library on a 10GbE NAS) **parked** after research: the honest first sentence is "buy a second
  NVMe" (a 2 TB drive is cheaper than NAS + NIC and games load about 2× slower off a NAS in the only measured test,
  Club386 on 2.5GbE/HDD); no 10GbE load-time measurement exists, anti-cheat and DirectStorage behaviour on iSCSI is
  unverified, and Steam on SMB is flaky (iSCSI via UGOS SAN Manager works but one PC per LUN). A page would only be
  honest for a multi-PC household, which the query does not ask about. Our own DXP480T Plus iSCSI test would be the
  way back in.
- 2026-11-03, iteration 11 built (G51–G53, G55, G56) from five research agents (~730k tokens); G54 parked (above). No
  new product records. Honesty notes: G52 leads with Reolink's own NVR for anyone who only wants cameras recorded and
  calls UGOS Surveillance Center a 2026 first-version app with undocumented licensing; G55 corrects the query's own
  premise (Synology reversed the HDD lock in DSM 7.3); G51 and G53 say a Pi or mini PC is enough when the buyer does
  not want bays. G53 and G56 needed lead trims for rank 6.
- 2026-11-03, batch 12 votes (`x12-*`): six open ×3, one contested. Open: NAS for Pi-hole/AdGuard + WireGuard (→ G57,
  DXP2800 unless a native WireGuard server on QNAP/Asustor wins), cheapest NAS for Infuse on Apple TV direct play
  (→ G58, DH2300 unless a cheaper Synology/TerraMaster ARM box wins), NAS for Veeam/Macrium image backups of three
  Windows PCs (→ G59, DXP2800 vs Synology Active Backup), NAS on 12 V in a van (→ G60 only if a UGREEN unit takes
  12 V input; else parked), power station for a 1/3 HP sump pump for 12 h (→ G61, BLUETTI AC200L/Elite 200 V2 if a
  motor start is defensible), power station for Starlink Mini + MacBook (→ G62, AC180/Elite 200 V2/R600 by days per
  charge). Contested, parked: cheapest fast external SSD for a Mac mini M4 (two judges: tested enclosure roundups
  exist). Six research agents started.
- 2026-11-03, iteration 12 built (G57–G62) from six research agents (~850k tokens); Mac mini storage parked (contested).
  No new product records. Honesty notes: four of six leads name a rival or a non-NAS first (DS223j cheapest for Infuse,
  DS225+ Active Backup for install-and-forget, a Pi for house DNS, a battery-backup pump for unattended sump duty);
  G57 marks the third-party claim of a native UGOS WireGuard server as unconfirmed; G60 says no measured van install
  exists; G62 notes BLUETTI's page lists the AC180 at $499 against our $449 cart check. G59, G61 and G62 needed lead
  trims for rank 6 (G59 also needed the query word "NAS" in the lead so it outranks the long second paragraph).
- 2026-11-03, batch 13 votes (`x13-*`): six open ×3, one contested. Open: NAS reachable from a phone behind CGNAT/
  Starlink (→ G63, DH2300/DXP2800 via UGREENlink or Tailscale unless Synology QuickConnect/BeeStation plainly wins),
  NAS to replace iCloud+ 2 TB for an Apple family (→ G64, DH2300/DXP2800 with the losses listed), power station for an
  AirSense 11 CPAP for a week (→ G65, AC180/Elite 30 V2 via the ResMed DC converter), power station for a chest freezer
  for 3 days with solar (→ G66, Elite 300/R4000 + 400 W), can a station charge an EV in an emergency (→ G67 only if
  "a few miles" is honestly defensible; else parked as a "no" page), NAS running Home Assistant OS as a VM with a Zigbee
  stick (→ G68 only if UGOS's VM app passes USB through or a network coordinator makes it moot). Contested, parked:
  400 W portable solar panel for a 2 kWh station (all three judges: sizing guides exist). Six research agents started.
- 2026-11-03, iteration 13 built (G63–G68) from six research agents (~900k tokens); 400 W solar panel parked
  (contested). No new product records. Honesty notes: three leads answer "partly" or "barely" before naming our pick
  (iCloud, EV), three name a rival first (QuickConnect, HA Green, a generator); G66 corrects the brief's own premise
  (the Elite 300 is a two-day freezer unit, not three). G63 needed a lead trim for rank 6. Research agents keep
  flagging the same unreadable UGREEN support articles (671, 373, 911, 909, 866, 654): a browser read of those would
  close most of the open facts in DLC-152.
- 2026-11-03, batch 14 votes (`x14-*`), all eight open ×3: NAS to replace Google Drive for a 5-person team (→ G69,
  DXP2800/DXP4800 Plus with Nextcloud, Synology Drive named if it wins), beginner home-lab NAS under $400 (→ G70,
  DXP2800 vs an N100 mini PC), power station for a 5,000 BTU window AC overnight (→ G71, Elite 300/R4000 or parked),
  power station for a 75-gallon aquarium for 24 h (→ G72), small station + fridge to keep insulin cold for two days
  (→ G73, medical: FDA/ADA guidance quoted exactly), UPS for a Bambu P1S (→ G74, a pure-sine computer UPS likely
  named first), KVM for a Mac + PC at 4K 144 Hz (→ G75, needs a UGREEN KVM record if one honestly fits), USB-C 2.5GbE
  adapter for a Mac mini M4 (→ G76, needs a UGREEN adapter record). Eight research agents started.
- 2026-11-03, iteration 14 built (G69–G75) from eight research agents (~1.1M tokens). **G76 (USB-C 2.5GbE adapter for a
  Mac mini) parked**: the right product is UGREEN's $25.99 RTL8156BG adapter sold on Amazon, not on us.ugreen.com, so
  there is no affiliate link to give; recommending a $240 Revodok dock for that query would be dishonest. Honesty notes:
  G69, G74 and G75 name a rival or a non-UGREEN product class first; G71 and G72 say no station covers the naive
  premise; G73 leads with the FDA rule that in-use insulin needs no fridge. Gate pattern seen three times today: when
  the "what to know" paragraph carries more query words than the lead, it outranks it and the buy link is cut; the fix
  is to put the query's own words in the lead (G59, G74, G75). KVM and 2.5GbE agents could not read us.ugreen.com
  (HTTP 429) at all: UGREEN product pricing now needs a browser read or the Shopify .json endpoints.
- 2026-11-03, batch 15 votes (`x15-*`), all seven open (website hosting open/open/contested): cheap NAS as a remote
  Hyper Backup target for a Synology (→ G77, DH2300/DXP2800 as an rsync/WebDAV target, or a DS223j + Vault named if it
  wins), hosting WordPress on a NAS at home (→ G78, "you can, but shared hosting is the better deal" likely first),
  silent all-SSD NAS under $500 (→ G79 only if the DXP2800 with M.2-only pools or SATA SSDs is honest; else parked
  with Beelink/Aiffro/Lincstation named), power station for a pellet stove for 12 h (→ G80, Elite 200 V2/Elite 300),
  power station for a gas furnace (→ G81, Elite 300/R4000 with the transfer-switch rule), farmers-market booth
  (→ G82, AC180/S2000 Pro), off-grid cabin weekend kit (→ G83, Elite 200 V2 + 200 W or S2000 Pro + 400 W). Seven
  research agents started.
- 2026-11-03, iteration 15 built (G77, G78, G80–G83) from seven research agents. **G79 (silent all-SSD NAS under
  $500) parked**: the only all-NVMe UGREEN is the $899.99 DXP480T Plus; the DXP2800 with M.2-only pools is plausible
  but unconfirmed and costs about $810 with two 2 TB drives; the honest picks are the Beelink ME mini ($209–429) and
  TerraMaster F4 SSD ($400), so no page. **The shared WebSearch budget (200 per turn) ran out during this batch**: the
  market-booth, pellet, furnace and cabin agents finished on WebFetch alone, so G82 cites ENERGY STAR and Vitamix
  directly and leaves rival prices thin; no further research agents can run until Barry's next message resets it.
  Stock notes seen on makers' pages today: AC180 out of stock (restock late Nov), R4000 sold out, S2000 Pro sold out,
  P1800 pre-order (Dec 7); the daily sweep should catch these, but the pages say so where it matters.

