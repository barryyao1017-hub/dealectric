"""Kits (DLC-223, Barry 2026-11-10): researched bundles behind one buy link that opens a filled cart.

A kit is a set of products from src/products.py that are bought together for one need and sold through ONE cart:
- one brand's own Shopify store (network cj / awin / rakuten): /go/<kit slug> opens the store's checkout with every
  item in the cart (Shopify cart permalink /cart/<variant>:<qty>,...) and, when it passed the cart test, the code applied;
- or Amazon (every item `program: "amazon:us"`, any brand): one amazon.com Add-to-Cart link with our tag that puts every
  item in the shopper's Amazon cart after one confirmation click (no /go/ hop: Amazon pays nothing through a redirect).
A link that opens two stores' affiliate links from one click is a forced click (CJ, Awin, Rakuten rules), so a kit never
spans two stores.

Fields:
  slug       the kit's id: /go/<slug> for a store kit
  name       short name for the line on the page ("CPAP camping kit")
  items      [{"slug": <product slug>, "qty": 1, "variant": <Shopify variant id> (store kits), "role": "why it is in the kit"}]
  page       the gap page slug that sells it
Cart test results (what the cart showed, the code, the date) live in src/kits-tested.json, written by tools/kitcheck.py;
the page states a kit price only from a passing test.
"""

KITS = [
 # ---- kit-fridge-solar-backup ----
 {"slug": "kit-fridge-solar-backup", "name": "Fridge outage solar backup", "items": [{"slug": "bluetti-elite-200-v2-2x200w-solar-kit", "qty": 1, "role": "Battery and recharge: BLUETTI's own Elite 200 V2 + 2×200W bundle. 2,073.6 Wh gives about 23 h for a 630 kWh/yr fridge. Two panels in series reach 49.2 V, inside the 60 V input, and need 5.3 full-sun hours to cover a day. $1,499 vs $1,697 bought separately."}, {"slug": "bluetti-solar-charging-cable-mc4-xt60-20a", "qty": 1, "role": "Panel-to-station link: BLUETTI says the Elite 200 V2 ships without a solar cable and names a 20 A MC4-XT60 cable to buy separately."}], "page": "refrigerator-backup-power-supply-battery-and-solar"},
 # ---- kit-shed-solar-400w ----
 {"slug": "kit-shed-solar-400w", "name": "Shed solar power kit", "items": [{"slug": "bluetti-elite-200-v2-2x200w-solar-kit", "qty": 1, "role": "Battery, 2,600 W inverter and solar charger in one, with two 200 W panels. Two panels make 750 Wh on a winter day, leaving 398 Wh after the 352 Wh a day the AC inverter uses at idle. Sold as one bundle SKU, $198 less than the parts."}, {"slug": "bluetti-solar-charging-cable-mc4-xt60-20a", "qty": 1, "role": "Connects the panels' MC4 leads to the station's solar input (20 A max). BLUETTI says the Elite 200 V2 doesn't include a solar charging cable."}], "page": "shed-solar-power-kit"},
 # ---- kit-home-backup-solar ----
 {"slug": "kit-home-backup-solar", "name": "Home outage solar backup kit", "items": [{"slug": "bluetti-elite-200-v2-2x200w-solar-kit", "qty": 1, "role": "Station and panels: 2,073.6 Wh LiFePO4 and 2,600 W, with two 200 W panels that reach 49.2 V in series, under the 60 V solar input. BLUETTI's own bundle SKU costs $198 less than the parts."}, {"slug": "bluetti-solar-charging-cable-mc4-xt60-20a", "qty": 1, "role": "Connects the series pair's single MC4 lead pair to the station. BLUETTI says the Elite 200 V2 ships with no solar cable and needs a 20 A MC4-XT60 cable."}], "page": "emergency-battery-pack-for-home-backup"},
 # ---- kit-church-projector-booth-link ----
 {"slug": "kit-church-projector-booth-link", "name": "Church sanctuary projector kit", "items": [{"slug": "panasonic-pt-vmz62", "qty": 1, "option": "White", "role": "Projector: 6,500 lm (ANSI) WUXGA laser 3LCD, throw 1.09–1.77:1, 280 W in Normal mode"}, {"slug": "avaccess-4kex70-h2-hdbaset-extender", "qty": 1, "role": "Booth-to-ceiling signal link: carries 1080p 197 ft over Cat5e/6 (230 ft on Cat6a) where plain HDMI stops at 49 ft; lists 1920×1200@60"}], "page": "projector-for-church-service-booth-to-ceiling"},
 # ---- kit-sump-pump-battery-backup ----
 {"slug": "kit-sump-pump-battery-backup", "name": "Sump pump battery backup kit", "items": [{"slug": "wayne-esp25n-battery-backup-sump-pump", "qty": 1, "role": "Second pump with its own float switch that starts if the main pump fails or loses power: 1,500 GPH at 10 ft, up to 10,000 gallons per charge"}, {"slug": "wayne-wsb1275-75ah-sump-battery", "qty": 1, "role": "Powers the backup pump, which ships without one: Wayne's recommended 12 V 75 Ah maintenance-free battery; the case holds sealed lead-acid batteries up to group 27"}, {"slug": "wayne-66005-wyn1-check-valve", "qty": 1, "role": "Check valve for the backup pump's discharge line, sold separately: Wayne says the system will not function without two check valves, one per pump line"}], "page": "sump-pump-backup-system-battery-kit"},
 # ---- kit-tiny-home-solar ----
 {"slug": "kit-tiny-home-solar", "name": "Tiny home solar kit", "items": [{"slug": "bluetti-apex-300", "qty": 1, "option": "Apex 300", "role": "Inverter and battery: 3,840 W at 120 V and 240 V together, 2,764.8 Wh. Its 20 W idle loss uses 480 Wh a day before anything else is charged"}, {"slug": "bluetti-sora-500-solar-panel", "qty": 2, "option": "500W Solar Panel | SORA 500", "role": "Solar: one panel on each Apex 300 solar input (49.1 V open-circuit against the 60 V limit). 1,000 W × 4 sun-hours − 480 Wh idle = 3,520 Wh a day"}], "page": "tiny-home-solar-power-kit"},
 # ---- kit-4-bay-plex-us3000 ----
 {"slug": "kit-4-bay-plex-us3000", "name": "4-bay Plex and growth", "items": [{"slug": "ugreen-nasync-dxp4800-plus", "qty": 1, "option": "diskless", "role": "4-bay NAS, Intel Pentium Gold 8505, 10GbE: room to add drives as the library grows"}, {"slug": "ugreen-nas-ups-us3000-120w", "qty": 1, "role": "120 W DC battery backup, 43.2 Wh; the only UGREEN UPS listed for the DXP4800 Plus"}], "page": "home-nas-setup-with-ups-battery-backup"},
 # ---- kit-2-bay-plex-us2000 ----
 {"slug": "kit-2-bay-plex-us2000", "name": "2-bay budget Plex", "items": [{"slug": "ugreen-nasync-dxp2800", "qty": 1, "option": "diskless", "role": "2-bay NAS, Intel N100, 2.5GbE: a mirrored pair for a smaller library"}, {"slug": "ugreen-nas-ups-us2000-72w", "qty": 1, "role": "72 W DC battery backup, 22.2 Wh; covers the DXP2800's 34.7 W measured max"}], "page": "home-nas-setup-with-ups-battery-backup"},
 # ---- kit-4-bay-files-us3000 ----
 {"slug": "kit-4-bay-files-us3000", "name": "4-bay family files", "items": [{"slug": "ugreen-nasync-dh4300-plus", "qty": 1, "option": "diskless", "role": "4-bay ARM NAS, 8 GB, 2.5GbE, for file and photo storage"}, {"slug": "ugreen-nas-ups-us3000-120w", "qty": 1, "role": "120 W DC battery backup, 43.2 Wh; IT-Connect measured 79 min on this NAS with 4 HDDs"}], "page": "home-nas-setup-with-ups-battery-backup"},
 # ---- kit-2-bay-starter-us2000 ----
 {"slug": "kit-2-bay-starter-us2000", "name": "Cheapest photo backup", "items": [{"slug": "ugreen-nasync-dh2300", "qty": 1, "option": "diskless", "role": "2-bay ARM NAS, 4 GB, HDMI, for one or two people's files and photos"}, {"slug": "ugreen-nas-ups-us2000-72w", "qty": 1, "role": "72 W DC battery backup, 22.2 Wh; the DH2300 draws 15–17 W at most"}], "page": "home-nas-setup-with-ups-battery-backup"},
]
