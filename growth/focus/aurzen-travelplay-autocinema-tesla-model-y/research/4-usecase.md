# Aurzen TravelPlay AutoCinema Screen (Tesla Model Y): use-case math

Angle 4 of 5: which projectors fit each mode, how bright and how long they run, setup time, and how it plays for road-trippers and parents. Researched 2026-10-28. Every computed number is labelled **ESTIMATE** with its formula. Inputs carry a source URL and date; inputs I could not source are stated as assumptions with a range.

## Bottom line

- **Our record had the mode geometry wrong.** Aurzen's own manual says: the **Rear-Seat Movie** screen is the rear panel clipped to the *front* center armrest/storage box (front seats moved fully forward), facing the rear seats; the projector hangs from the rear glass roof on a MagPlay suction mount. **Tailgate Camp Movie** is the rear panel attached in the trunk opening, watched from outside. **Starlight Roof Movie** is both panels clipped into the glass-roof rim, silver side up, watched lying down with the rear seats reclined. Nothing goes on the rear window or liftgate glass.
- **Sky-roof mode cannot be filled by any projector I could verify.** The projector sits about 0.56–0.81 m below the roof, so filling a ~1.03 m wide image needs a throw ratio of about 0.54–0.79. ZIP (1.09:1) and ZIP Pro (1.2:1) give roughly a **21–34 inch** picture there, not 47 inches. Most other minis cannot focus that close at all.
- **Rear-seat mode suits the ZIP and ZIP Pro.** From the rear center armrest: about **26–44 inch**. From the roof on MagPlay: about **34–47 inch** (the full panel). MagPlay is unavailable in the US store (checked 2026-10-28) and the ZIP Pro's MagPlay Pro shows "Coming Soon". Bigger 1.2:1 projectors (MoGo 3 Pro, Capsule 3, Atom, Freedo, N2, T2 Plus) need ≥1.06 m and do not fit inside.
- **Tailgate mode fits everything.** Put the lens about 1.12–1.29 m from the screen to fill it. Brightness, not geometry, is the limit: night is fine for all; daylight is not watchable with any of them.
- **A 2-hour movie with Camp Mode on costs about 2–3% of a Model Y Long Range battery in mild weather** (ESTIMATE), 4–6% near freezing, about 10% at −22 °C. The projector's own draw is under 0.2%.
- **Setup time: no owner-reported times exist yet** (product on sale since 2026-08-17, zero reviews). My estimate from the manual's steps: sky-roof 12–24 min the first time, 4–7 min after that; rear-seat 2–4 min repeat; tailgate 3–5 min repeat.

## What the three modes actually are (source check)

From the English manual, page 2 (MAN-EN, https://cdn.shopify.com/s/files/1/0720/5109/7892/files/Aurzen_TravelPlay_AutoCinema_Screen_User_Manual.pdf, undated, accessed 2026-10-28; the Spanish manual MAN-ES says the same, https://cdn.shopify.com/s/files/1/0720/5109/7892/files/Aurzen_Pantalla_de_AutoCinema_TravelPlay_User_Manual.pdf, accessed 2026-10-28) and the product images (https://cdn.shopify.com/s/files/1/0720/5109/7892/files/aurzen-travelplay-three-viewing-modes-tesla-model-y.webp and .../aurzen-travelplay-detachable-front-rear-screens.webp, accessed 2026-10-28):

| Mode (manual name) | Screen | Where the projector goes | Who watches | Panels used |
|---|---|---|---|---|
| Starlight Roof Movie ("Sky-Roof Theater") | Both panels clipped into the mounting slots on the inner rim of the glass roof, silver side up, joined by 2 center + 2 side connect clips; 8 side clips around the edge. "Remove the sunshade from the vehicle's sunroof" first. | On the mattress/folded seats, pointing straight up (manual drawing) | People lying down, rear seats reclined | Front + rear |
| Rear-Seat Movie ("Front Center Armrest Area") | Rear panel clipped to the front center armrest/storage box; front seats moved fully forward. The panel hangs upright between the front seats, facing back. | MagPlay suction mount at "the center of the rear sunroof", ZIP on the mount (manual). A product render instead shows a ZIP Pro sitting on the rear center armrest. | Rear-seat passengers | Rear only |
| Tailgate Camp Movie ("Camping Theater Mode") | Rear panel attached in the trunk opening, liftgate up | Outside, on a stand behind the bumper | People in chairs behind the car | Rear only |

Other fit facts used below: TravelPlay is "designed for the Tesla Model Y Juniper 2025–2026"; on 2020–2024 it fits only in Starlight Roof mode "but the rear screen cannot fully cover the window" (MAN-EN p.3; the Spanish manual says 2022–2024 instead of 2020–2024). Neither source mentions the 6-seat Model Y L.

## Inputs and assumptions

| # | Input | Value used | Source / basis | Date |
|---|---|---|---|---|
| I1 | Front panel | 1,098 × 590 mm | TravelPlay page spec table, https://aurzen.com/products/aurzen-travelplay-autocinema-screen-for-tesla-model-y | accessed 2026-10-28 |
| I2 | Rear panel | 1,031 × 685 mm | same; also MAN-EN p.3 | accessed 2026-10-28 |
| I3 | Rear panel shape | 685 mm is the height at the center notch; the side "legs" run ~90–100 mm lower | My pixel measurement of Aurzen's product image (https://cdn.shopify.com/s/files/1/0720/5109/7892/files/AutoCinema-Screen-for-Tesla-Model-Y_5_11zon.webp). Front panel's measured aspect matched its spec (1.87 vs 1.86), so the scale is trustworthy. **ESTIMATE** | accessed 2026-10-28 |
| I4 | Grey border around the white area | 18 mm per side (range 10–25 mm) | **ASSUMPTION** from product images | n/a |
| I5 | Model Y interior | 2nd-row head room 982–1,001 mm; leg room 1,063 / 1,029 mm; wheelbase 2,890 mm; liftgate opens up to ~2.4 m | Tesla Model Y Owner's Manual, Dimensions, https://www.tesla.com/ownersmanual/modely/en_us/GUID-1E76B638-7B12-4D9A-8767-94B7F1E92A0E.html | accessed 2026-10-28 |
| I6 | Floor to roof, rear seats folded | ~81 cm (32 in); single source, not Juniper-specific; I use 76–86 cm | Teslaunch blog, https://teslaunch.net/blogs/news/best-mattress-tesla-model-y-camping | published 2025-08-02 |
| I7 | Mattress thickness | 8 cm (Tesla's own Model Y air mattress); Teslaunch suggests 3–4 in | Not a Tesla App, https://www.notateslaapp.com/news/4086/tesla-starts-selling-single-person-model-y-air-mattress | published 2026-05-04 |
| I8 | Projector lens height above its base when pointed up | 5–12 cm | **ASSUMPTION** (ZIP Pro body is 115 × 97 × 44 mm folded, per its spec table) | n/a |
| I9 | Rear armrest to front-armrest screen, horizontal | 0.70–1.05 m (central 0.85 m) | **ASSUMPTION**. Cross-check: Aurzen's render shows a ZIP Pro on the rear armrest filling ~82% of the panel width; at 1.2:1 that implies ~1.0 m. A render is not a measurement. | n/a |
| I10 | MagPlay on rear roof glass to the screen | 0.90–1.30 m (central 1.10 m) | **ASSUMPTION**: ~0.9–1.1 m forward plus ~0.4–0.5 m drop from roof to screen center | n/a |
| I11 | Model Y USB-C ports (Juniper, 5-seat) | 1 in the rear compartment of the center console; 2 below the rear cabin vents on the console; 1 USB-A in the glovebox. **No wattage in Tesla's current US manual.** | Tesla manual, Interior Electronics, https://www.tesla.com/ownersmanual/modely/en_us/GUID-A1DF67DE-94B4-4859-98B4-B0A5D342FAB3.html | accessed 2026-10-28 |
| I12 | USB-C wattage | "Three USB-C ports output up to approximately 42W, and two USB-C ports output up to approximately 65W" (a forum quote of an earlier manual; the current US and Japanese manual pages do not say this) | teskas.net thread, https://teskas.net/t/usb/13143?tl=en | posted 2025-07-31; **unverified** |
| I13 | 12 V outlet | Center console front compartment and left side of trunk; "up to 12A continuous draw (16A peak)". Tesla advises against non-Tesla accessories "including power inverters". | Tesla manual, Interior Electronics (I11) | accessed 2026-10-28 |
| I14 | Camp Mode | Keeps climate on, powers USB and the low-voltage outlet, touchscreen stays on for media; Park only; Sentry off | Tesla manual, Operating Climate Controls, https://www.tesla.com/ownersmanual/modely/en_us/GUID-4F3599A1-20D9-4A49-B4A0-5261F957C096.html | accessed 2026-10-28 |
| I15 | Camp Mode drain, mild | ~1%/hour (several owners); ~8% overnight at 20 °C, ~10% at 10 °C, ~14% at 5 °C | Tesla Motors Club, https://teslamotorsclub.com/tmc/threads/battery-use-in-camp-mode.275779/ | posts 2022-08-10/11 |
| I16 | Camp Mode drain, typical | ~10% per 8 h; ~15% per 8 h when cold | Not a Tesla App, https://www.notateslaapp.com/news/830/tesla-camp-mode-a-comprehensive-guide | published 2022-06-25 |
| I17 | Camp Mode drain, hot | Model Y at 85 °F outside, 68 °F cabin: ~30 mi of range over 8 h; 87 °F: ~45 mi over 11 h; "1% ≈ 3 miles" | Tesla Motors Club (I15) | posts 2022-08-11 |
| I18 | Camp Mode drain, near freezing | ~2 kWh/h (Model 3 Performance) | InsideEVs, https://insideevs.com/news/392645/tesla-camp-mode-test-winter/ | published 2020-01-13 |
| I19 | Camp Mode drain, −22 °C | 3.8 kWh/h, cabin at 20 °C (Model Y) | Drive Tesla Canada, https://driveteslacanada.ca/news/tesla-model-y-camping-cold-weather-efficiency-test/ | published 2021-02-02 |
| I20 | Model Y battery | 75.0 kWh usable (Long Range AWD, Juniper, 2025) | EV Database, https://ev-database.org/car/3104/Tesla-Model-Y-Long-Range-AWD | accessed 2026-10-28 |
| I21 | Smaller pack (Standard) | 60 kWh | **ASSUMPTION** for a sensitivity case | n/a |
| I22 | Cinema brightness reference | SMPTE 196M: 16 fL open gate, ~14 fL peak white (~48 cd/m²); current revision 55 cd/m² | Wikipedia, Foot-lambert, https://en.wikipedia.org/wiki/Foot-lambert | accessed 2026-10-28 |
| I23 | Ambient light levels | Full moon 0.05–0.3 lx; end of civil twilight 3.4 lx; sunset 400 lx; overcast day 1,000 lx; daylight (not direct sun) 10,000–25,000 lx | Wikipedia, Lux, https://en.wikipedia.org/wiki/Lux | accessed 2026-10-28 |
| I24 | Ambient light on the screen inside a parked car, daytime | 100–1,000 lx | **ASSUMPTION** (tinted glass, roof shaded or not) | n/a |
| I25 | Screen gain | 0.8–1.0 (matte fabric) | **ASSUMPTION**; Aurzen publishes no gain | n/a |
| I26 | Watchable contrast against ambient light | ≥10:1 on-screen | **ASSUMPTION** (rule of thumb; dark scenes want more) | n/a |
| I27 | Supercharger stop | 20–40 min | Given in the brief; **ASSUMPTION** | n/a |

Projector specs are in the table in section 1d, each with its own source.

## 1. Geometry per mode

### 1a. Largest 16:9 image per panel (ESTIMATE)

Formula: width-limited W = panel width, H = W × 9/16; height-limited H = panel height, W = H × 16/9; take whichever fits. Diagonal (in) = W(mm) × √(16²+9²)/16 ÷ 25.4.

| Panel | Panel size | Largest 16:9 | Diagonal | Area | With 18 mm border (I4) |
|---|---|---|---|---|---|
| Front | 1,098 × 590 mm | 1,049 × 590 mm (height-limited) | 47.4 in | 0.619 m² | 985 × 554 mm, 44.5 in |
| Rear | 1,031 × 685 mm | 1,031 × 580 mm (width-limited; fits above the notch per I3) | 46.6 in | 0.598 m² | 995 × 560 mm, 44.9 in |
| Both, roof, image rotated 90° | 1,275 mm (590 + 685) along the car | 1,275 × 717 mm | 57.6 in | 0.914 m² | Seam crosses the picture; viewer would need to lie across the car. Theoretical only. |

Aurzen's "47 in" matches the front panel's 16:9 maximum. Its "50 in" for the rear panel is the panel's own diagonal rounded up (48.7 in); the largest 16:9 picture on it is 46.6 in. **For copy: "about 45–47 in of 16:9 picture per panel."**

### 1b. Throw distance available (ESTIMATE)

| Mode | Distance D, lens to screen | Formula / basis |
|---|---|---|
| Sky-roof | **0.56–0.81 m** (central 0.65) | D = floor-to-roof (I6: 0.76–0.86) − mattress (I7: 0–0.08) − lens height (I8: 0.05–0.12) |
| Rear-seat, projector on rear armrest | **0.70–1.05 m** (central 0.85) | I9 |
| Rear-seat, projector on MagPlay at the rear roof | **0.90–1.30 m** (central 1.10) | I10 |
| Tailgate | **Unconstrained** (outside the car) | Set by where you put the stand |

### 1c. Throw ratio needed to fill the panel (ESTIMATE)

Formula: TR = D ÷ W, with W = 1.031 m (rear panel; the front panel's 1.049 m changes it by under 2%).

| Mode | TR needed (low / central / high D) | What it means |
|---|---|---|
| Sky-roof | **0.54 / 0.63 / 0.79** | Needs a short-throw lens. Every mini checked here is 1.09–1.25. |
| Rear-seat, armrest | 0.68 / 0.82 / 1.02 | A 1.09–1.2 lens fills 57–94% of the width. |
| Rear-seat, roof mount | 0.87 / 1.07 / 1.26 | A 1.09–1.2 lens fills it at the far end of the range. |
| Tailgate | any | Lens distance to fill = TR × 1.031 m: **ZIP 1.12 m, ZIP Pro and other 1.2:1 models 1.24 m, 1.25:1 models 1.29 m** |

### 1d. Projectors: specs and fit per mode

Minimum distance below is derived from the maker's minimum image size: D_min = TR × (min diagonal × 25.4 × 16/√337). It is an **ESTIMATE** of the closest focus; makers rarely publish focus distance directly. Prices were checked live on 2026-10-28.

| Projector | TR | Min D | Brightness | Battery | Power in | Weight | Price 2026-10-28 | Source |
|---|---|---|---|---|---|---|---|---|
| Aurzen ZIP (US) | 1.09:1 | 0.48 m (20 in min) | 100 ANSI, 720p | 5,000 mAh, up to 1.5 h | 24 W USB-C PD | 280 g | $199.99 (reg. $499.99) | https://aurzen.com/products/aurzen-zip-tri-fold-portable-mini-projector-usa |
| Aurzen ZIP Pro | 1.2:1 | 0.5 m (maker: "0.5m–3m") | 200 ANSI ("200 lm" in table), 1080p | 38 Wh, up to 2.5 h ECO | 65 W USB-C PD; "65W+ PD supports charging while watching. Lower-wattage power banks support power supply." | 586 g | $579.99 (reg. $629.99); pre-order, "dispatch from October 30" | https://aurzen.com/products/aurzen-zip-pro-full-hd-portable-projector |
| XGIMI MoGo 3 Pro | 1.2:1 | 1.06 m (40 in min) | 450 ISO, 1080p | none | USB-C PD 65–150 W; under 150 W it drops to ECO | 1.1 kg | $379 (compare $449), **out of stock** | https://us.xgimi.com/products/mogo-3-pro |
| Nebula Capsule 3 (1080p) | 1.2:1 | 1.06 m (40 in min) | 200 ANSI | 2.5 h (Eco) | PD 20 V/2.25 A (45 W) | 0.85 kg | $399.99 (list $529.99) | https://www.seenebula.com/products/capsule-3-projectors-d2425 (redirects to soundcore.com) |
| Nebula Capsule Air | ~1.22:1 (derived: 100 in at 2.7 m) | unknown | 150 ANSI, 720p | 34 Wh, ~2 h | USB-C | n/a | **Not on Nebula's US store** (product URL 404); price not verified | https://www.jbhifi.com.au/products/nebula-capsule-air-projector (AU listing) |
| Nebula Mars 3 Air | 1.2:1 | 0.80 m (30 in min) | 400 ANSI, 1080p | 2.5 h (Eco) | 19 V/4.74 A DC adapter (~90 W) | 1.69 kg | $519.99 (list $599.99) | https://www.seenebula.com/products/mars-3-air-projectors-d2325 (redirects to soundcore.com) |
| Samsung The Freestyle 2nd Gen | 1.20:1 | 0.79 m (2.6 ft, 29.6 in) | 230 ANSI, 1080p | none built in (battery base / power bank; not verified on samsung.com) | 50 W | 1.8 lb | street $498, MSRP $799 (ProjectorCentral); Samsung US page returned an error | https://www.projectorcentral.com/Samsung-Freestyle_2nd_Gen.htm |
| Dangbei Atom | 1.2:1 | 1.06 m (40 in min) | 1,200 ISO, 1080p laser | none | AC, 80 W | 2.82 lb | $899 (compare $999) | https://us.dangbei.com/products/dangbei-atom-laser-projector-with-google-tv |
| Dangbei N2 | 1.25:1 | 1.11 m (40 in min) | 200 ISO, 1080p LCD | none | AC, ~65 W | 1.72 kg | $199 (compare $229) | https://us.dangbei.com/products/dangbei-n2-mini-portable-projector |
| Dangbei Freedo | 1.2:1 | 1.06 m (40 in min) | 450 ISO, 1080p | ~60 Wh, 2.5 h Eco | USB-C, 65 W+ | 1.4 kg | $439 (compare $599) | https://us.dangbei.com/products/dangbei-freedo-portable-google-tv-projector-with-gimbal-stand |
| Yaber T2 Plus | 1.25:1 | 1.11 m (maker: "Min 3.63 ft") | 350 ISO, 1080p | 2.5 h video | DC adapter; 3.5 h charge | 165 × 140 × 290 mm | $349 ($369 GTV) | https://www.yaber.com/products/t2-t2plus-anywhere-cinema |

Short-throw minis: I could not verify a battery-powered mini with TR ≤ 0.8. The shared web-search budget ran out mid-research, and Optoma's ML1080ST page did not render for a direct fetch. This is the gap that matters for sky-roof mode.

**Image size each can make, per mode (ESTIMATE).** Formula: W = min(D ÷ TR, 1.031 m); "no" when D_min > the available D.

| Projector | Sky-roof (D 0.56–0.81 m) | Rear-seat, armrest (0.70–1.05 m) | Rear-seat, roof mount (0.90–1.30 m) | Tailgate (D free) |
|---|---|---|---|---|
| ZIP (1.09) | **Fits: 23–34 in** | **Fits: 29–44 in** | **Fits: 37–47 in** (full panel from 1.12 m). MagPlay is US-unavailable. | Fits; lens at 1.12 m |
| ZIP Pro (1.2) | **Fits: 21–31 in** | **Fits: 26–40 in** | **Fits: 34–47 in** (full from 1.24 m). MagPlay Pro "Coming Soon" on aurzen.com. | Fits; lens at 1.24 m |
| Freestyle 2nd Gen (1.2) | Marginal: ~30 in, only if D ≥ 0.79 m | Marginal: 30–40 in, only if D ≥ 0.79 m; needs 50 W power | No ceiling mount | Fits; 1.24 m |
| Mars 3 Air (1.2) | Marginal: ~30 in, only if D ≥ 0.80 m | Marginal: 30–40 in if D ≥ 0.80 m; 1.7 kg brick on an armrest; 90 W DC adapter | No | Fits; 1.24 m |
| Capsule Air (~1.22) | Unknown min focus; 21–30 in if it focuses | 26–39 in if it focuses | No mount | Fits; 1.26 m |
| Capsule 3, MoGo 3 Pro, Freedo, Atom (1.2) | **No** (min ~1.06 m) | **No** | No (too heavy for a suction mount; no mount exists) | Fits; 1.24 m |
| N2, T2 Plus (1.25) | **No** (min ~1.11 m) | **No** | No | Fits; 1.29 m |

The sky-roof gap can't be closed by aiming from the far end of the cargo area. That throw meets the roof at roughly 55–60° from perpendicular (about 1.0 m horizontal, 0.65 m vertical). XGIMI's own spec limits auto keystone to a 40° side angle, and the ZIP has vertical-only auto keystone. **ESTIMATE.**

## 2. Brightness

Formulas: illuminance E (lux) = lumens ÷ image area (m²). Screen luminance L (nits) = E × gain ÷ π. On-screen contrast against ambient light C = (E + E_ambient) ÷ E_ambient, capped at the projector's native contrast (ZIP Pro: 300:1). ANSI and ISO 21118 lumens are treated as roughly comparable.

**Full 46.6 in rear-panel image, 0.598 m² (ESTIMATE):**

| Projector | Lumens | E (lux) | L at gain 1.0 / 0.8 (nits) | Max ambient for 10:1 (lux) = E ÷ 9 |
|---|---|---|---|---|
| ZIP | 100 | 167 | 53 / 43 | 19 |
| Capsule Air | 150 | 251 | 80 / 64 | 28 |
| ZIP Pro, Capsule 3, N2 | 200 | 334 | 106 / 85 | 37 |
| Freestyle 2nd Gen | 230 | 385 | 122 / 98 | 43 |
| Yaber T2 Plus | 350 | 585 | 186 / 149 | 65 |
| Mars 3 Air | 400 | 669 | 213 / 170 | 74 |
| MoGo 3 Pro, Freedo | 450 | 753 | 240 / 192 | 84 |
| Dangbei Atom | 1,200 | 2,007 | 639 / 511 | 223 |

Smaller pictures are brighter. The ZIP Pro's ~24 in sky-roof picture (0.54 m wide, 0.165 m²) gets 1,210 lux, about 385 nits. The ZIP's ~27 in roof picture gets ~500 lux. **ESTIMATE.**

Battery or ECO modes lower these numbers. Aurzen does not say by how much (see open questions). The MoGo 3 Pro drops to ECO on any supply under 150 W, and a car USB-C port is under that.

**What works when (ESTIMATE, using I23/I24 and the 10:1 rule):**

| Light | Ambient on screen | ZIP (167 lx) | ZIP Pro (334 lx) | Mars 3 Air (669 lx) | Atom (2,007 lx) |
|---|---|---|---|---|---|
| Night, dark campsite, moon | ≤0.3 lx | 300:1+ (native-limited) | 300:1 (native-limited) | native-limited | native-limited |
| End of civil twilight | 3.4 lx | 50:1 | 99:1 | 198:1 | native-limited |
| Night at a lit charging site (my assumption 10–50 lx) | 10–50 lx | 18:1 to 4:1 | 34:1 to 8:1 | 68:1 to 14:1 | 202:1 to 41:1 |
| Daytime, inside car, shaded (I24) | 100–1,000 lx | 2.7:1 to 1.2:1 | 4.3:1 to 1.3:1 | 7.7:1 to 1.7:1 | 21:1 to 3:1 |
| Sunset outdoors (tailgate) | 400 lx | 1.4:1 | 1.8:1 | 2.7:1 | 6:1 |
| Daylight in shade outdoors (tailgate) | 10,000+ lx | 1.0:1 | 1.0:1 | 1.1:1 | 1.2:1 |

Reading: every listed projector clears the cinema reference of ~48 nits (I22) at full panel size in the dark, the ZIP only just. **Night and late dusk work for all of them.** A lit charging site at night is fine for 200 lm and up. **Daytime inside the car is washed out for every battery mini.** Only the 1,200-lumen, mains-powered Atom gets near 10:1, and only in deep shade. **Daytime tailgate viewing does not work with anything here.** Aurzen's FAQ agrees: "use the screen after sunset or in a low-light environment" (TravelPlay page, accessed 2026-10-28).

## 3. Power

**Projector battery vs a 2-hour movie (ESTIMATE):**

| Projector | Rated runtime | Average draw = Wh ÷ h | 2 h movie on battery? |
|---|---|---|---|
| ZIP Pro | 2.5 h ECO (38 Wh) | 38 ÷ 2.5 ≈ 15 W | Yes in ECO, with ~30 min margin (lab test at 25 °C). Brighter modes: probably not; runtime unpublished. |
| ZIP | 1.5 h (5,000 mAh ≈ 18.5 Wh at an assumed 3.7 V) | ≈ 12 W | **No.** Plug it in (24 W PD; Aurzen: "Plug in and keep watching"). |
| Capsule 3, Mars 3 Air, Freedo, T2 Plus | 2.5 h Eco/video | Freedo: 60 ÷ 2.5 ≈ 24 W | Yes in Eco, small margin |
| Capsule Air | ~2 h (34 Wh) | ≈ 17 W | Borderline. Plug in. |
| MoGo 3 Pro, Freestyle 2nd Gen, Atom, N2 | no battery | 50–80 W rated | Need car power for the whole film |

**Charging from the car:**
- USB-C (I11, I12): ports at the rear of the center console and below the rear vents. They are close to the projector in rear-seat and sky-roof modes, so a 1 m cable is enough. A roof-mounted projector needs about 1.5–2 m. Tesla's current US manual gives no wattage. The 42 W / 65 W figures come from a forum quote and are unverified.
  - The ZIP (24 W) and Capsule 3 (45 W) should run and charge from any port that delivers what that quote claims. **ESTIMATE.**
  - The ZIP Pro needs 65 W+ to charge while playing, but Aurzen says lower-wattage sources still power it. On a 42 W port it should hold charge in ECO (about 15 W draw). **ESTIMATE.**
- Power is on whenever the car is awake: in Camp Mode, Keep Climate On, or while someone sits in a seat. "Keep Accessory Power On" keeps it on with nobody inside (I11).
- 12 V outlet (I13): 12 A continuous is about 144 W at 12 V nominal (**ESTIMATE**; the Juniper's low-voltage system may run above 12 V, unverified). The trunk outlet suits tailgate mode with a USB-C PD car adapter. AC-only projectors (Atom, N2) and the Mars 3 Air's 19 V barrel adapter need an inverter, which Tesla's manual advises against.

**Car battery cost of a 2-hour movie with Camp Mode on (ESTIMATE).** Formula: % = 2 h × drain per hour, or 2 h × kWh/h ÷ pack kWh × 100.

| Conditions | Drain | 2 h on a 75 kWh Long Range | 2 h on a 60 kWh pack (I21) |
|---|---|---|---|
| Mild, ~20 °C | 1%/h (I15); 1.25%/h (I16) | **2–2.5%** (≈1.5–1.9 kWh) | 2.5–3.1% |
| Hot, 85–87 °F | ~30 mi per 8 h ÷ 3 mi per % ≈ 1.25–1.4%/h (I17) | **2.5–2.8%** | ~3.1–3.5% |
| Cold (Not a Tesla App) | 15% per 8 h = 1.9%/h (I16) | 3.8% | 4.7% |
| Near freezing | 2 kWh/h (I18, Model 3) | **5.3%** | 6.7% |
| −22 °C | 3.8 kWh/h (I19) | **10.1%** | 12.7% |

The projector itself adds at most 65 W × 2 h = 0.13 kWh, about 0.17% of 75 kWh. In practice it is the climate, not the movie.

**Sound through the car's speakers:** the ZIP and ZIP Pro both list Bluetooth 5.4 audio out "including Tesla audio systems". The ZIP Pro also pairs two Bluetooth headphones at once (ZIP Pro page, accessed 2026-10-28). Camp Mode keeps the touchscreen and media on (I14), so the car stays a Bluetooth audio target. Lip-sync delay over Bluetooth to the car is not published (open questions). The ZIP Pro's "20–40ms" figure is video latency for wired game mode, not Bluetooth audio.

## 4. Setup time

**Aurzen's claim:** "Quick, Secure Clip-In Installation" and "tool-free", with no minutes stated (TravelPlay page, accessed 2026-10-28). The MagPlay page says "Set up in seconds" for the mount alone (https://aurzen.com/products/magplay-dual-sided-mount-for-zip-projector, accessed 2026-10-28).

**Owner-reported times: none found.**
- The product page review widget showed no reviews on 2026-10-28; the listing was published 2026-08-17 (Shopify JSON).
- Aurzen's YouTube video list (https://www.youtube.com/@Aurzen_Official/videos, accessed 2026-10-28) has no TravelPlay video.
- Web searches turned up only CES 2026 press releases. Angle 2 (owners) reached the same result.

**Estimate from the manual's steps (ESTIMATE; assumptions: 20–45 s per clip the first time, 10–20 s once practiced; 1–2 min per panel to unfold and place the first time):**

| Mode | Steps (MAN-EN) | First time | Repeat | Teardown |
|---|---|---|---|---|
| Sky-roof | Remove any existing roof sunshade; identify F/R; seat both panels in the roof-rim slots silver side up; 8 side clips + 2 center + 2 side connect clips (12 total); recline/fold rear seats; place and connect the projector | **12–24 min** = read/unpack 3–5 + panels 2–4 + 12 clips 4–9 + seats ~1 + projector/casting/Bluetooth pairing 2–5 | **4–7 min** = panels ~1 + clips 2–4 + seats 0.5–1 + projector 0.5–1 | 3–5 min the first time (folding steel-ring panels takes practice; the manual warns to fold "slowly to avoid injury"), ~2–3 min after |
| Rear-seat | Front seats fully forward; clip the rear panel to the front armrest/storage box; MagPlay on the rear roof (or projector on the rear armrest); connect | 6–12 min | **2–4 min** | 1–3 min |
| Tailgate | Liftgate up; attach the rear panel in the trunk; projector on a stand ~1.1–1.3 m back; power cable to the trunk 12 V outlet or console USB-C | 6–12 min | **3–5 min** | 2–3 min |

One-time extra: shipping creases. The manual says to hair-dry the silver side for 1–2 minutes per crease, then let the panel cool for about 15 minutes before installing.

## 5. Road-trip and parent scenarios

All viewing is parked only. Aurzen: "Use only when the vehicle is parked. Do not use while driving"; the manual says "only use when the vehicle is stationary." Tesla allows Camp Mode in Park only (I14).

**A 20–40 minute Supercharger stop (ESTIMATE).** Rear-seat mode is the only one that makes sense. Watch time = stop − (repeat setup 2–4 min + teardown 1–3 min) ≈ **13–37 min**.

| Stop | Watch time | Fits |
|---|---|---|
| 20 min | 13–17 min | One short kids' episode (7–12 min) or two; not a 22-min sitcom episode |
| 30 min | 23–27 min | One 22-min episode |
| 40 min | 33–37 min | One 22-min episode plus a short; not a 45–60 min drama episode |
| Feature film (90–120 min) | n/a | Needs 3–4 stops, or play it on the ZIP Pro battery during a longer meal stop |

Daytime stops are the catch. By section 2, a ZIP Pro picture in a sunlit cabin sits around 1.3–4:1 contrast, which is washed out. Night or covered/garage stops work. On a bright day the car's own screens are the better choice.

**Camping night (sky-roof).**
- Setup 12–24 min the first night, 4–7 min after that, plus the mattress.
- Picture: about 21–31 in with a ZIP Pro, or 23–34 in with a ZIP, pointed straight up. That is roughly a third to half of the panel, and very bright in a dark car (~400–1,200 lux).
- Movie on the ZIP Pro's battery in ECO, or plugged into the console USB-C.
- Camp Mode for the movie costs ~2–3% in mild weather. The whole night costs 8–15% per I15/I16.
- The silver side faces the glass, so the panels double as a roof sunshade in the morning (Aurzen's "2-in-1" claim).

**Kids in car seats.**
- **Forward-facing seats in the outboard rear positions: rear-seat mode works well.** The screen is straight ahead between the front seats.
  - Eye-to-screen distance is roughly 1.0–1.3 m (**ASSUMPTION**). A full 1.03 m wide picture then fills about **43–55° of view** (formula: 2 × atan(W/2 ÷ distance)). That is front-row cinema size. A 0.7 m picture from the armrest is ~39°.
  - Outboard seats sit about 17–19° off-axis (≈0.35–0.40 m lateral offset), which is fine on a matte screen. **ESTIMATE.**
- **A car seat in the middle position blocks the armrest placement.** The rear armrest is the middle seatback, folded down (**ASSUMPTION**, standard 5-seat layout). With a middle car seat, you need the roof mount, which is not sold in the US today, or a clamp or tripod of your own.
- **Hanging a 586 g ZIP Pro on a suction cup above children** is Aurzen's design for this mode, but Aurzen's own safety note says to check the suction surface regularly. For kids, the armrest placement is the cautious choice. This is my judgement, not Aurzen's.
- **Rear-facing infant seats face the liftgate, so no mode gives them a view.**
- **Sky-roof mode needs the rear seats folded,** so car seats come out. It is for lying down: older kids and adults.
- **Parents' seats:** rear-seat mode moves both front seats fully forward and puts the screen between them, so adults up front are cramped beside the panel. The realistic picture is kids in the back and parents outside or at the charger.
- **Sound:** the ZIP Pro's dual Bluetooth headphones let two kids listen without the car speakers, or route sound to the car over Bluetooth.

**Day vs night summary:** night is the use case for all three modes. Late dusk works in the car. Daylight works for none, except possibly a very bright mains projector in deep shade, which defeats the portable setup.

## Summary table

| | Sky-roof (Starlight Roof Movie) | Rear-seat | Tailgate |
|---|---|---|---|
| Screen | Both panels in the roof rim | Rear panel at the front armrest, facing back | Rear panel in the trunk opening, facing out |
| Viewer | Lying down, seats folded | Rear passengers, including forward-facing car seats | Outside, in chairs |
| Lens-to-screen D (ESTIMATE) | 0.56–0.81 m | 0.70–1.05 m (armrest); 0.90–1.30 m (roof mount) | Free |
| TR needed to fill ~47 in (ESTIMATE) | 0.54–0.79 | 0.68–1.02 (armrest); 0.87–1.26 (roof) | Any; lens at 1.12–1.29 m |
| Fits | ZIP (23–34 in), ZIP Pro (21–31 in); Freestyle 2 / Mars 3 Air only at ~30 in if D ≥ 0.8 m | ZIP (29–47 in), ZIP Pro (26–47 in); Freestyle 2 / Mars 3 Air marginal | All listed |
| Doesn't fit | MoGo 3 Pro, Capsule 3, Freedo, Atom, N2, T2 Plus (min focus ≥1.06 m) | Same six | n/a |
| Brightness at night | Very bright (small picture) | Fine for ≥100 lm | Fine for ≥100 lm; ≥400 lm for dusk |
| Daytime | Shaded roof helps; side windows don't | Washed out | Not watchable |
| Setup, first / repeat (ESTIMATE) | 12–24 / 4–7 min | 6–12 / 2–4 min | 6–12 / 3–5 min |
| 2 h movie, Camp Mode, mild (ESTIMATE) | ~2–3% of a 75 kWh pack | same | same (Camp Mode optional outside; the trunk 12 V outlet needs the car awake) |
| Model Y 2020–2024 | Yes, rear panel short of the glass | Not stated by Aurzen | Not stated by Aurzen |

## Open questions / couldn't verify

1. **Real throw distances in a Juniper Model Y.** I6, I9 and I10 are a single vendor blog figure and my assumptions. One tape-measure session would settle all three: floor to roof glass with seats folded, rear armrest to front console, rear roof glass center to the front armrest.
2. **USB-C wattage per port on the Juniper.** Tesla's current US and Japanese manual pages list port locations only. The 42 W / 65 W split is from a forum quote of an earlier manual and does not say which ports are which.
3. **A battery short-throw mini (TR ≤ 0.8) that would fill the roof.** Not checked; the web-search budget ran out. Optoma's ML1080ST page would not render for a direct fetch.
4. **ZIP Pro and ZIP brightness in ECO/battery mode,** and the ZIP Pro's runtime outside ECO. Aurzen publishes neither.
5. **Bluetooth audio lip-sync to Tesla's speakers** for the ZIP / ZIP Pro, and whether either has an audio-delay setting.
6. **Screen gain and the exact white area** inside the grey border (I4, I25).
7. **Samsung Freestyle 2nd Gen battery and current US price** on samsung.com: the US product page returned an error. The Capsule Air's US price and availability: its Nebula US URL returns 404.
8. **Projector minimum focus distances** are derived from each maker's minimum image size, not from published focus specs.
9. **Owner setup times.** None exist yet; re-check after reviews appear. Angle 2 tracks this.
10. **Model Y L (6-seat)** fit is not addressed by Aurzen. Tesla's own Model Y mattress is not compatible with the Y L (I7 source), which hints at a different interior.
11. **Car-interior heat:** some projectors list a 5–35 °C operating range (Dangbei Freedo). A parked Model Y in summer can exceed that before the climate cools it. Not tested.
12. **Does the 8-inch rear touchscreen** below the screen in rear-seat mode add glare? Aurzen's render shows it lit. Untested.

Raw downloads (product JSON/HTML, both manuals, images, maker pages): /private/tmp/claude-501/-Users-jiayiyao-Desktop-dealectric/44f11078-b8ab-412e-a42d-cf3b4ee1b7ef/scratchpad/research/aurzen-usecase/
