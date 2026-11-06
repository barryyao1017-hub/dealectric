# x21 gap-mining batch (2026-11-05, DLC-168)

Clusters picked from `growth/gapmine/runs/2026-11-05/report.json`, ranked by uncovered searches (Microsoft Ads Ad
Insight Bing US searches, last 3 months, × (1 − coverage)). One researched page per cluster; research reports are the
`research-*.md` files here (shared brief: `BRIEF.md`). Each page passed `fastloop.py check --ranks 1,3,6` with two
`--must` phrases on its API pack (`growth/evals/runs/fastloop/gm-*`).

| Page | Cluster (uncovered searches, coverage) | Pick | Our earning link |
|---|---|---|---|
| G126 /best-rechargeable-aa-batteries | rechargeable AA + best rechargeable AA (8,029 + 1,769, 0.46) | Panasonic eneloop; eneloop pro for flashes; Tenergy Premium Pro for bulk high-drain | Tenergy (CJ) + Amazon |
| G127 /best-iphone-case-with-wallet | iPhone wallet case (2,970, 0.27) | MagSafe case + ESR Geo Wallet Boost; Smartish Wallet Slayer one-piece | ESR (Awin) + Amazon |
| G128 /best-fitness-tracker-for-women | fitness tracker for women (2,599, 0.72) | Garmin Lily 2 Active; Amazfit Active 2 under $100 | Amazon + Amazfit (CJ) |
| G129 /best-cd-player-with-bluetooth | CD player with Bluetooth (1,866, 0.28) | FiiO DM13 BT; Panasonic SC-PM270 for a system with speakers; 1Mii B06TX add-on | Amazon only |
| G130 /best-mini-projector | best mini projector (674, 0.51) | Nebula Capsule 3; XGIMI MoGo 4; Aurzen BOOM mini budget | Amazon only (Aurzen's ZIP loses) |
| G131 /best-3d-printer-for-kids | 3D printer for kids (2,388, 0.66) | Bambu Lab A1 mini (direct, no affiliate); Flashforge AD5M Pro for teens | Amazon (AD5M Pro) |

## Skipped, and why
- **Home battery backup (general), 2,098 uncovered:** coverage 0.90 (six dedicated "best home battery backup" pages
  in Bing's top 6) and our `/best-solar-generator-for-power-outages` already serves the intent. The uncovered number is
  10% of a 21,855-search head term, not an opening a new page can take.
- **Our approved-but-unlinked brands were not onboarded:** TEAC (CJ) sells no US CD player that transmits Bluetooth
  (PD-301-X has none; its Bluetooth models are receive-only), so it has nothing for G129. BIQU (Awin) sells open-frame
  Klipper kits and QIDI's Q2C loses to the Flashforge on filtration, so neither fits G131.

## Honest-pick calls that cost commission
- Bambu Lab's A1 mini Combo was $369 on Amazon vs $299 on Bambu's own store (2026-11-05), so the kids' pick links to
  Bambu's store with no affiliate link.
- Aurzen BOOM mini: $349.99 on aurzen.com vs $279.99 on Amazon, so it links to Amazon, not through Aurzen's CJ program.
- ESR Geo Wallet Stand: $45.99 on ESR vs $35.30 on Amazon, so Amazon. The Geo Wallet Boost ($36.99 on ESR, $35.99 on
  Amazon) goes through ESR, where ECTRIC18 would make it the cheaper buy once cart-tested.

## Corrections to the research
- ESR Geo Wallet Boost: ESR's store (search endpoint, 2026-11-05) says 4 cards + 3 bills, 1,800 g, $36.99; the agent's
  snippets said 5 cards, 3,200 g, $31.99.
- XGIMI MoGo 3 Pro's ASIN was wrong and it isn't on Amazon US; the page uses the MoGo 4 (B0F3CBV5HP).

## Open
- ECTRIC18 on the Geo Wallet Boost: esrtech.com returned 429 to this laptop, so the record carries `codes_excluded`
  until the daily sweep records a pass.
- Agents' WebFetch failed on this network and the shared WebSearch budget ran out, so several facts came from search
  snippets; prices and ASINs on the pages were re-read from the stores and Amazon directly.
