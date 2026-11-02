# kit500 run, step 4: research report (Fable 5.1 subagent, 2026-11-02)

Query cluster: ChatGPT's searches for "What's the best small solar generator kit under $500?" (harvest
`runs/2026-11-02-harvest-kit500`, gap vote `runs/fastloop/kit-k0*/vote-v2`). Store prices read on the makers' US
stores 2026-11-02 ~00:30–01:00 PT (Shopify product JSON and pages). Reddit was unreachable from every tool; BLUETTI's
forum needs a login.

## 0. Shared core of ChatGPT's 9 results for generic-14 (count = pages making the claim)

- 8/9: the panel is usually not included; "solar generator" mostly means a station that accepts solar.
- 7/9: a real sub-$500 kit is in the 245–300 Wh class: Jackery Explorer 300 / 300 v2 (4), EcoFlow RIVER 3 / 3 Plus (3),
  Anker SOLIX C300 / C300 DC (2), BLUETTI Elite 30 mini (1). None names ALLPOWERS or the Elite 30 V2.
- 7/9: solar refill is the weak point: panels give 50–75% of rating (Popular Mechanics), budget stations cap input at
  ~100–110 W, a full refill from one panel takes most of a sunny day.
- 6/9: LiFePO4 over NMC (2,500–6,000 cycles vs 500–1,000).
- 6/9: what ~300 Wh is for: phones, laptop, lights, router, a CPAP for a night; not a fridge, kettle or heater.
- 6/9: check the station's max solar input watts and voltage window.
- Only 1/9 (powersized) prices a kit against its parts, only 3/9 date their prices: that is the gap.

## 1. Top block

- **Pick (in stock): BLUETTI Elite 30 V2 + 100 W kit**, $489.99, $465.49 with AFF5OFF. The only in-stock brand kit
  under $500 with a 100 W panel and a 600 W inverter; parts apart $538.99 ($289.99 + SP100L $249). Competing small kits
  in stock ship 40 W (Jackery, $379) or 60 W (Anker, $349.99) panels or a 300 W inverter (BLUETTI Elite 30 mini,
  $429.99); EcoFlow sells no RIVER 3 Plus + 110 W bundle; ALLPOWERS' VOLIX P300 kit is sold out.
- **Open concern: does the included 100 W panel refill the battery in a day?** A 100 W panel really delivers about
  70–80 W, so the 288 Wh Elite 30 V2 refills in roughly 4 h of full sun (our arithmetic: 288 ÷ ~75 ÷ ~0.9; BLUETTI
  publishes only 2.2 h at its 200 W, 12–28 V cap); winter or cloud, a day or more. Raised in 6 of 10 owner threads and
  reviews reached, e.g. https://community.bluettipower.com/t/elite-30-v2-pv-charging-while-turned-off/39166/3 ,
  https://community.bluettipower.com/t/charging-time-on-bluetti-premium-30-v2/42628 ,
  https://www.bestbuy.com/site/reviews/jackery-explorer-300-plus-portable-power-solar-generator-40w-solar-panel-black/6549214 ,
  https://slickdeals.net/f/18393244 . Measured in the same class: Explorer 300 + SolarSaga 100, 90–100 W clear midday,
  60–70 W partial cloud, ~5.5 h to full (https://backuppowerhub.com/?p=188).
- **1 kWh line (addendum):** ALLPOWERS P1800 + SF200 200 W kit, $531, $477.90 with ALLPOWERS26 (cart test 2026-11-02,
  pre-applied by the link), 1,024 Wh LiFePO4, 1,800 W; **pre-order, dispatch from Dec 15, 2026**. A 200 W panel
  refills 1,024 Wh in ~7 h of full sun (1.5–2 days); a 100 W panel would take ~14 h (three sunny days), so no
  P1800 + 100 W pairing.

## 2. Product facts

- **Elite 30 V2 + 100 W** (bluettipower.com, variant 47282470027483): $489.99, in stock, 2–5 business days. 288 Wh
  LiFePO4, 3,000+ cycles, 600 W (1,500 W Power Lifting), 980 W UPS bypass ≤10 ms, 4.3 kg, 140 W USB-C, standby 4.5 W,
  <30 dB, 5-year warranty. Solar 200 W max, 12–28 V, 10 A (manual). AC 380 W "70 Mins" full. Which 100 W panel the US
  kit ships is UNVERIFIED (US store's 100 W folding panels: SP100L $249, PV100FX $329). Early Black Friday collection
  lists it at the regular price; last year the station fell to $199, so keep the price dated.
- **VOLIX P300 + 100 W** (iallpowers.com): all three kit variants sold out ($216.99–$228.99). Station $139 and SE100
  $69.99 are in stock separately ($188.09 with ALLPOWERS26). 256 Wh LiFePO4, 300 W, solar 110 W, 11–30 V. Gough Lui's
  measured review (June 2026) found solar-undervoltage latching at sunset; his Nov 2026 update withdrew the
  recommendation (AM/SW radio interference, one unit lost fast charging). Not a lead pick.
- **P1800 + SF200** (variant 48279218028697): see above. P1800 alone $399, pre-order to Dec 7; solar input 650 W,
  11–60 V, 13 A (XT60).

## 3. The field (makers' US stores, 2026-11-02)

| Kit | Wh / output | Panel | Kit price | Parts apart | Stock |
|---|---|---|---|---|---|
| BLUETTI Elite 30 V2 + 100 W | 288 / 600 W | 100 W | $489.99 ($465.49 code) | $538.99 | In stock |
| BLUETTI Elite 30 mini + 100 W | 288 / 300 W | 100 W | $429.99 | $498.99 | Listed in stock (WattList: presale, ships early Nov) |
| ALLPOWERS VOLIX P300 + SE100 | 256 / 300 W | 100 W | $218.99 | $208.99 | Kit sold out; parts in stock |
| ALLPOWERS P1800 + SF200 | 1,024 / 1,800 W | 200 W | $531 ($477.90 code) | SF200 sold out alone | Pre-order, Dec 15 |
| Anker SOLIX C300X DC + 60 W | 288 / DC only | 60 W | $349.99 | $549.98 with a 100 W panel | In stock |
| Jackery Solar Generator 300 (Explorer 300 + 40 W Air) | 292 / 300 W | 40 W | $379 | $538 with a 100 W panel | In stock; + 100 W kit ($579) sold out |
| EcoFlow RIVER 3 Plus + 110 W | 286 / 600 W | 110 W | no US bundle | $538 ($279 + $259) | Both in stock |

Sales live 2026-11-02: EcoFlow Black Friday Nov 2–18; Jackery Halloween sale to Nov 3; none at Anker or ALLPOWERS sitewide.

## 4. Other concerns, by frequency

1. Is ~300 Wh enough? (6/9 results) 288 Wh: phone 20–25 charges, 15 W laptop 15–18 h, 40 W fan 6–7 h, CPAP without
   humidifier 6–8 h; not a fridge, kettle or heater. 600 W inverters (Elite 30 V2, RIVER 3 Plus) run a 500 W device.
2. LiFePO4 vs NMC (6/9): every kit above is LFP.
3. Panel compatibility / input window (6/9): Elite 30 V2 12–28 V MC4 200 W; P300 11–30 V XT60 110 W; C300X DC 11–28 V.
4. Kit vs parts (1/9 + forum): BLUETTI's kit saves $49; ALLPOWERS' P300 kit cost more than its parts; Jackery, Anker,
   EcoFlow sell no 100 W small kit under $500.
5. Stock churn: date every price and stock line.
6. Standby drain while solar charging (Elite 30 V2 powers on with a panel connected; ~2%/h in weak sun).

Full source list: the subagent transcript; key URLs are inline above and in drafts.py `sources`.
