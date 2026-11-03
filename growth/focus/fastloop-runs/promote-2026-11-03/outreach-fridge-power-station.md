# Tier 3 outreach: /power-station-to-run-a-refrigerator-for-24-hours (step 7b, 2026-11-03)

Research only; nothing posted. Page facts come from the built pages in `docs/` (fridge, chest-freezer, sump-pump and
furnace pages, all published 2026-11-03). Related pages were not needed: every candidate below is a refrigerator
question, so each draft ends with the fridge page. 20 WebSearch calls used (the cap); the rest was WebFetch, mostly
through r.jina.ai because diysolarforum, Quora, AnandTech, CandlePower and CosmoQuest refuse direct fetches.

**Bottom line: one fresh forum thread (tier A, today) and three Quora questions with 2026 answers that nobody has
answered with numbers.** The forum thread is a Spanish buyer sizing a 1 kWh station for a side-by-side fridge on a
€750 budget, which is exactly the "1 kWh is not a full day" point of our page, but he is in a 230 V market our US
store links do not serve. The Quora questions are the strongest fit for the page itself (US, shopping, no product
named in any answer). No US homeowner or prepper forum thread from the last 45 days was found; the brand forum
(BLUETTI) is unreadable to our tools, and Reddit is left to Barry (list in §4).

## 1. Candidates

Sorted by demand, then freshness, then venue activity. Dates on Quora: Quora prints a year ("Jan 11, 2024") or "1y/4y"
only on answers older than the current year, so bare "Jun 10" / "May 24" / "Oct 6" are read as 2026. That is an
inference from Quora's display convention, not a verified date.

| # | URL | Venue | Opened / last post | Tier | Demand (quote) | What's missing | Link rules | Action |
|---|---|---|---|---|---|---|---|---|
| 1 | https://diysolarforum.com/threads/advice-please-for-a-small-power-cut-setup.132150/ | diysolarforum.com, DIY Solar General Discussion; 4 replies, views not shown | 2026-11-03 05:50 / 2026-11-03 10:43 (same day) | A | **3** (but Spain, 230 V). Unclenewy, rural southern Spain, "just over 750 euros for the whole package", wants "a starter kit ready this month"; loads: "fridge-freezer (side-by-side, American-style, no icemaker)", phones, tablets, laptop, TV, lights; picked an OUKITEL P1000PLUS (1,800 W, 1,024 Wh LiFePO4) + DOKIO 300 W (2×150 W) kit + Honda petrol generator. Plans fridge by day on the station, "a couple of hours" at night. | ghostwriter66 covered the PWM-vs-built-in-MPPT point, the 45 V series voltage and "probably not a fridge overnight" (no numbers); Hedges covered compressor start on a 1 kW inverter, icemaker/defrost heater, and asked about inverter idle draw. Nobody has put a kWh figure on the side-by-side, said how many hours 1,024 Wh buys, or what 300 W of panel returns in a Spanish winter day, so the OP cannot tell whether his daytime plan breaks even. | Code of Conduct: "Advertising is not allowed. Affiliate links, self-promotion, spam etc, will result in a permanent ban"; "It is ok to post basic links to products you like, but if we find that you are a shill, you will be banned." A link to our own page with the disclosure is a ban risk here, and our prices are US. | Reply (draft 2a). Barry decides whether to keep the link. |
| 2 | https://www.quora.com/What-is-a-reliable-but-affordable-power-station-that-can-run-a-refrigerator-and-microwave-during-a-blackout | Quora; 1 answer, views not shown | Asked date not shown / answer "May 24" (2026 inferred) | Evergreen-style Q&A (Google rank not checked; it surfaced in two of our topic searches) | **3**: the question itself is a purchase with a budget ("reliable but affordable… refrigerator and microwave during a blackout"). | The only answer (Morgan Chandler) says "about 2,200 W nominal output" from 500 W fridge + 1,000 W microwave and names no product, no capacity, no price. Missing: the daily kWh (the fridge is a capacity question, the microwave a wattage one), which 2 kWh units clear 2,000 W, prices. | Quora's own policy text could not be fetched (403). Third-party 2026 write-ups agree: direct or cloaked affiliate URLs are treated as spam; a relevant link to your own site with disclosure in the body is tolerated; answers that are mostly promotion get collapsed. | Answer (draft 2b) |
| 3 | https://www.quora.com/Would-a-1000Wh-station-be-enough-for-fridge-modem-during-outages | Quora; 4 answers | Answers "Jun 10–11" (2026 inferred) | Evergreen-style Q&A (rank not checked; surfaced in two topic searches) | **3**: sizing before buying ("Would a 1000Wh station be enough…"). | Answers contradict each other: Charles Edwards "150 W fridge… about 6 hours" (assumes 100 % duty); Mats Petersson "12 to 24 hours"; Morgan Chandler "generally yes"; Ronald Williams "depends on specs". Nobody uses a daily-kWh figure, the modem's 24 h cost, or the inverter idle draw, so the asker has a 4x spread and no verdict. | As row 2 | Answer (draft 2c) |
| 4 | https://www.quora.com/What-size-portable-power-station-do-I-need-to-run-a-refrigerator-during-a-power-outage | Quora; 4 answers | Answers "Jan 11" ×3 and Lewis Edge "Oct 6" (2026 inferred: 28 days ago, so the question still draws answers) | Evergreen-style Q&A (ranked #2 in our quora.com-restricted search for the target query; Google rank not checked) | **2–3**: a sizing question, asker's own purchase intent not stated. | Tom W: power stations "inadequate for fridges", buy a Honda 2200i; Andrew Daviel: a 1,000 W inverter failed to start his fridge, 288 Wh runs it "about 6 hours"; PaulBettyLou: 12 V battery + 1,000 W inverter; Lewis Edge: generic watts × hours. Missing: the actual sizing table (1 / 1.5 / 2 / 3 kWh → hours), that 2 kWh LFP units now carry 2,400–2,600 W inverters and start any household compressor, and a measured run (Bob Vila, 30+ h). | As row 2 | Answer (draft 2d) |
| 5 | https://www.reddit.com/r/solar/ "Talk me out of spending $600 on a battery station just to keep a fridge running" (u/daddyglen1; read via the sentinel-team.org snapshot of 2026-05-22) | r/solar; 112 comments, 32 points | about 2025-12-07 / unknown | Stale (11 months) | **3** at the time (Anker SOLIX S2000 for about $600 after a six-day Beryl outage cost "$2,100"); u/NotenStein "unsure how long 2 kWh runs a fridge"; u/Jippylong12 answered "1–2.5 kWh per day, so 2 kWh lasts about a day". | Already answered in substance; too old. Listed so the manual Reddit check (§4) knows it. | Reddit blocked for tools; r/solar rules not read | Skip |
| 6 | https://poweroutage.us/home-battery-backup/how-long-power-station-run-refrigerator | PowerOutage.us article (Brogan Woodburn), no comments, no date | Undated | Correction candidate, fails the 60-day/page-1 test as far as I can verify | n/a | Errors: lists the BLUETTI Elite 200 V2 as "2,048 Wh" and "2,400 W continuous" (it is 2,073.6 Wh and 2,600 W) and gives it "14 to 18 hours" on a standard fridge while its own daily figure (1,200–1,500 Wh) implies 28–35 h, and Bob Vila measured 30+ h; also internally inconsistent (nameplate "400 W to 800 W" vs "100 W to 800 W"; intro "8 to 12 hours" vs table 7 h per 1,024 Wh). "Affiliate Disclosure" heading with no text. | No comment section; no author contact on the page | Skip unless Barry sees it on page 1 for a target query; then a correction email to PowerOutage.us (contact not found) |

### Venue activity, and how it was counted

- **diysolarforum.com**: `/whats-new/posts/` on 2026-11-03 (read via r.jina.ai) listed 100 threads updated within about the last 9 hours, so the forum is very active. Threads about buying a small backup or power station in the window I could see: thread 132150 (today, row 1), "Anker F3800…portable panels not working good" 132177 (today, owner fault, no purchase), and "Worth waiting for Black Friday deals?" 131924 (Oct 28–30, Anker F3800 shopper, already in the solar-kits run). Forum search is behind a login wall and the subforum index returns 403, so I could not count the whole month; the "Solar Generator and Micro Systems" subforum had about 8 new threads in October per the 11-01 RV run.
- **Quora**: a quora.com-restricted search for the target query returned 10 fridge/power-station questions; 3 have answers dated in 2026 (rows 2–4, inferred as above); "Can a portable power station power a refrigerator during a power outage?" has only 1y/4y answers; "How long can a power station keep a fridge cold in a blackout?", "What is the best way to provide backup power to a refrigerator?" and "What is the best portable power station for home backup in 2026?" were blocked (Quora 403 to both direct and proxied fetches), so their dates and answers are unverified.
- **BLUETTI community** (community.bluettipower.com → forum.bluettipower.com): the old Discourse redirects to a JavaScript app that returns "Network unavailable" to every fetch, including `latest.json`, `search.json` and the thread "Frig has strange behavior when plugged in to Elite 100 V2" (/t/…/39174, which search snippets say is about compressor-start surge and a firmware fix). 0 threads counted; needs a browser.
- **City-Data** (House forum): one thread, "Should I get a Tesla Powerwall?" (Aug 2023, 3 replies, one reply suggests portable packs for a fridge). No 2026 thread found.
- **Houzz / GardenWeb**: a site-restricted search returned no discussion on the topic.
- **Prepper and local storm forums**: three searches (prepper forum, hurricane/ice-storm/winter-storm forum, Bogleheads/Garage Journal/Survivalist Boards/The High Road) returned only vendor blogs and affiliate roundups; no forum thread.
- **CosmoQuest** "power station solar generator" thread (two pages; snippets say an owner ran the fridge through a storm and recharged the station in about 90 minutes): behind a bot check both direct and proxied; undated; not verified.
- **AnandTech forums** "What's needed to keep my refrigerator/freezer from warming during extended power outage" (2571512): bot check + 403; the search snippet called it older than 2026. Not verified.
- **CandlePowerForums** "Storm Checkin" (485887, a post asks "how much run time you get from the power station with your fridge plugged in"): bot check; date unknown. Not verified.
- **Firewood Hoarders Club** "Bluetti AC500 w/B300K… home backup" (Feb 2025–Apr 15 2026, ~91 replies): owners comparing systems (one swapped an AC500 for an AC200L + battery; another runs the kitchen except the fridge from EcoFlow stations). No open purchase question; last post 6 months ago. Skip.
- **MacRumors** "Review: Anker SOLIX C1000 Gen 2…" (Dec 11–12 2025, 12 replies): home-backup chat, no fridge, 11 months old. Skip.

## 2. Drafts

Every draft ends with the fridge page URL and the disclosure, per Barry's 11-01 rule. Where the venue's rules make
the link a ban risk (diysolarforum), that is flagged in the table and Barry decides.

### 2a. diysolarforum, "Advice please for a small power cut setup." (Unclenewy, Spain)

Context checked before the arithmetic: the OP's own words give the fridge (side-by-side, American-style, no icemaker),
the station (OUKITEL P1000PLUS, 1,800 W, 1,024 Wh LiFePO4, per the listing he quotes), the panel (300 W as 2×150 W),
"roughly 6 hours of sun daily, even in winter" in southern Spain, and the plan (fridge by day, a couple of hours at
night, everything off at bedtime, Honda generator as backup). Not repeated: ghostwriter66's MPPT/PWM and series-voltage
points, Hedges' compressor-start, icemaker/defroster and idle-draw points.

> Since nobody has put numbers on the fridge yet, here is the arithmetic for your plan, which I think works as long as you treat it as a daytime-fridge plan and not a 24-hour one.
>
> **What the fridge takes.** A side-by-side American-style fridge-freezer is the hungriest household type: ENERGY STAR's certified-model medians run about 1.6–1.8 kWh a day for a 26 cu ft side-by-side (1.0–1.4 for top- and bottom-freezer types), measured at about 21 °C with the door mostly shut. That is an average of 65–75 W around the clock, with the compressor pulling 100–250 W while it runs, about 30–50 % of the time in a cool room and 80–90 % in a hot one. A fridge over ten years old can use twice the median. Your yellow EU energy label gives the kWh/year for your exact model; divide by 365.
>
> **What 1,024 Wh buys.** Reckon about 85 % of the rated capacity reaches the plug through the inverter, so about 870 Wh, minus the inverter's own idle draw while it waits for the compressor (typically 10–15 W on units this size, so 120–180 Wh over 12 hours). On a 1.7 kWh/day fridge that is about 10 hours of fridge with nothing else plugged in. That is why a 1 kWh unit is an overnight-or-daytime device for a big fridge, and a full day without sun needs the 2 kWh class.
>
> **What 300 W of panel returns.** A folding or rigid panel delivers roughly 60–75 % of its rating in good sun. With your 6 hours of winter sun that is about 1.1–1.3 kWh on a clear day, under 0.3 kWh on a fully overcast one. The fridge over a 12-hour day costs about 0.85 kWh plus about 0.15 kWh of inverter idle, so on a clear day the panel carries the fridge and leaves the battery close to full for the evening (TV, laptop, tablets and lights are about 0.3–0.5 kWh for a few hours). Two hours of fridge at night is about 0.15 kWh. A cloudy day is where the Honda earns its place: an hour of generator into the station's 1,200 W charger puts back more than the panel does all day.
>
> **Two checks before the first outage.** Put a plug-in energy meter on the fridge for 24 hours now, so you have your number rather than the median. And run the whole setup once for a few hours including a compressor restart; a 1,800 W inverter starts any household compressor, but you want to see it do it.
>
> For comparison, the sizing table and the 2 kWh options are in the piece I wrote for the US market (US store prices, so only the arithmetic carries over to Spain): https://dealectric.com/power-station-to-run-a-refrigerator-for-24-hours. I run dealectric.com, which earns a commission on some links.

### 2b. Quora, "What is a reliable but affordable power station that can run a refrigerator and microwave during a blackout?"

Not repeated: Morgan Chandler's "about 2,200 W nominal" output figure (kept as the one point of agreement).

> Treat the two appliances as two different questions, because they are.
>
> **The refrigerator is a capacity question.** A full-size fridge uses about 1.0–1.8 kWh a day (ENERGY STAR certified-model medians: about 1.0 for an 18 cu ft top-freezer, 1.4 for a 22 cu ft French door, 1.8 for a 26 cu ft side-by-side with a dispenser). The compressor only runs 30–50 % of the time at room temperature, so "500 W fridge" on the nameplate is not what you pay for all day. Count about 85 % of a station's rated watt-hours as usable, subtract the inverter's idle draw (about 15 W, so 360 Wh a day), and a 1 kWh station gives 11–17 hours of fridge, a 2 kWh station 22–35 hours, a 3 kWh station 33–51. The one measured run I know of: Bob Vila's reviewer ran a full-size fridge on a 2 kWh BLUETTI Elite 200 V2 for over 30 hours.
>
> **The microwave is a wattage question.** A 1,000–1,200 W microwave draws about 1,500 W from the wall for the few minutes it runs; each 5-minute use costs roughly 100–125 Wh, which is nothing against a 2 kWh battery. What matters is that the inverter carries 1,500 W plus the fridge's compressor if it starts at the same moment, which is why 2,000 W continuous is the floor (the 2,200 W figure above is right in spirit). Every 2 kWh LFP unit on sale today clears it with 2,400–2,600 W; the 1 kWh class (1,500–1,800 W) is marginal with a microwave in the mix.
>
> **Affordable and reliable, as of November 2026:** the 2 kWh class is $800–1,030 right now. The BLUETTI Elite 200 V2 is $899 (2,073.6 Wh, 2,600 W, LiFePO4 rated 6,000 cycles, 5-year warranty) and has that 30-hour fridge test behind it; the Jackery Explorer 2000 v2 is around $799 on sale (2,042 Wh, 2,200 W); the Anker SOLIX C2000 Gen 2 is $899.99 (2,048 Wh, 2,400 W); the EcoFlow DELTA 2 Max is $1,029 (2,048 Wh, 2,400 W). Cheaper for a day's cover: the ALLPOWERS S2000 Pro at $549 (1,451 Wh NMC, 2,400 W, about 16–19 hours of fridge), though it was sold out when I checked on November 3. Skip the 1 kWh units for this job: they will not carry a full-size fridge through a day.
>
> Two habits double the value of whatever you buy: keep the door shut (an unopened fridge holds safe temperatures about 4 hours, a full freezer about 48, so you can run the station on a schedule rather than continuously), and test it once with a plug-in watt meter including a compressor restart before you need it.
>
> Full table with prices and codes checked daily: https://dealectric.com/power-station-to-run-a-refrigerator-for-24-hours. I run dealectric.com, which earns a commission on some links.

### 2c. Quora, "Would a 1000Wh station be enough for fridge + modem during outages?"

Not repeated: Mats Petersson's "small fridge 12–24 hours, less for a large one or hot conditions" is right and is
credited; Charles Edwards' 6-hour figure is corrected (it assumes the compressor runs 100 % of the time).

> Short version: yes for an overnight or a working day, no for a full 24 hours with a full-size fridge. Mats has the range right; here is why the answers above span 6 to 24 hours.
>
> **The fridge.** Its compressor draws 100–250 W while running but only runs 30–50 % of the time in a room-temperature kitchen, so a full-size fridge uses about 1.0–1.8 kWh a day (ENERGY STAR medians: 1.0 kWh for an 18 cu ft top-freezer, 1.4 for a French door, 1.8 for a side-by-side with dispenser). "150 W for 6 hours" would be true only if it never cycled off.
>
> **The modem (and router).** 10–20 W, but it never cycles: 240–480 Wh a day. That is a quarter to half of a 1,000 Wh station on its own.
>
> **The station.** About 85 % of the rated watt-hours reach the outlet, and the inverter idles at roughly 10–15 W while it waits for the compressor, another 240–360 Wh a day. So: 1,000 Wh × 0.85 = 850 Wh; minus 300 Wh of modem and 300 Wh of idle over 24 hours leaves 250 Wh for a fridge that wants 1,000–1,800. Over 12 hours the same sums leave about 550 Wh against a fridge need of 500–900: an overnight is fine for a top-freezer, tight for a side-by-side, and a hot kitchen (duty cycle 80–90 %) breaks it.
>
> **What to do with it.** Run the fridge on a schedule rather than continuously: an unopened fridge holds safe temperatures for about 4 hours and a full freezer about 48, so 1 hour on, 2 off keeps food safe and stretches 1,000 Wh across a day while the modem stays on. If you want the fridge covered for a day without thinking about it, the 2 kWh class (about $800–900 now, e.g. BLUETTI Elite 200 V2 $899, 2,073.6 Wh, 2,600 W, 30+ hours on a full-size fridge in Bob Vila's test; Jackery Explorer 2000 v2 about $799) is the right size, and a 1 kWh unit is the right size for the modem, phones, lights and a few hours of fridge.
>
> The hours-per-kWh table and current prices: https://dealectric.com/power-station-to-run-a-refrigerator-for-24-hours. I run dealectric.com, which earns a commission on some links.

### 2d. Quora, "What size portable power station do I need to run a refrigerator during a power outage?"

Not repeated: Andrew Daviel's warning that a 1,000 W inverter failed to start a fridge (credited as the surge point).
Corrected: Tom W's "portable power stations are inadequate for fridges, get a Honda 2200i", which was true of the
500–1,000 Wh units of a few years ago and is not true of the 2 kWh LFP class.

> Two numbers decide it, and neither is the "wattage" on the fridge's label.
>
> **1. Watt-hours (how long).** A full-size fridge uses about 1.0–1.8 kWh a day: ENERGY STAR certified-model medians are about 1.0 kWh for an 18 cu ft top-freezer, 1.25 with an icemaker, 1.4 for a 22 cu ft French door, 1.8 for a 26 cu ft side-by-side with a dispenser; your own EnergyGuide label's kWh/year ÷ 365 is better. Count 85 % of a station's rated capacity as usable and subtract about 15 W of inverter idle draw, and you get: 1 kWh station, 11–17 hours; 1.5 kWh, 16–25; 2 kWh, 22–35; 3 kWh, 33–51. A hot room (compressor on 80–90 % of the time instead of 40 %) halves those. The one measured run I know of is Bob Vila's: a full-size fridge on a 2 kWh BLUETTI Elite 200 V2 for over 30 hours.
>
> **2. Watts (whether it starts).** Andrew's point is the real failure mode: the compressor's start surge is several hundred to about 1,200 W for a bottom-freezer and more for a side-by-side, and a 1,000 W inverter can refuse it. 2,000 W continuous with 3,000 W-plus surge starts every household fridge. The 2 kWh LFP units sold today all have it (2,200–2,600 W continuous), which is why the "get a generator" advice is out of date for this job: a 2 kWh station at $800–900 runs the fridge for a day silently and indoors, and a 200–400 W panel in winter sun puts back 300–1,200 Wh a day. A generator still wins past two or three days without sun.
>
> **So:** for one night, 1 kWh (about $450–530); for a full day with margin, 2 kWh (BLUETTI Elite 200 V2 $899, 2,073.6 Wh, 2,600 W; Jackery Explorer 2000 v2 about $799; Anker SOLIX C2000 Gen 2 $899.99; EcoFlow DELTA 2 Max $1,029); for two days, 3 kWh (BLUETTI Elite 300 $1,199). Keep the door shut (4 hours safe for a fridge, 48 for a full freezer, so the station can run on a schedule) and test it once with a plug-in watt meter, compressor restart included.
>
> Table and prices, checked daily: https://dealectric.com/power-station-to-run-a-refrigerator-for-24-hours. I run dealectric.com, which earns a commission on some links.

## 3. Checked and rejected

Forum threads and Q&A:
- diysolarforum "Please some help with a small backup system" 131947 (today; Cuba, 16 kWh Eco-Worthy + Growatt 10 kW, grounding question): no portable station, no fridge. Skip.
- diysolarforum "How much power do I really need?" 131662 (19 replies, active to about Oct 30): whole-house 50 kWh/day solar sizing. Skip.
- diysolarforum "Refrigerator UPS using a Growatt 3000TL LVM" 30558 (Oct 2021–Mar 2022; the goto/post?id=468660 link in search results): DIY 24 V inverter build. Stale. Skip.
- CocoonTech "UPS for refrigerator" (Aug 2009). Stale. Skip.
- City-Data "Should I get a Tesla Powerwall?" 3433372 (Aug 2023, 3 replies). Stale. Skip.
- MacRumors "Review: Anker SOLIX C1000 Gen 2…" 2474556 (Dec 2025; heater and NAS talk, no fridge). Skip.
- Firewood Hoarders Club "Bluetti AC500 w/B300K…" 50206 (last post Apr 15 2026; owners, no open question). Skip.
- Quora "Can a portable power station power a refrigerator during a power outage?" (answers 1y and 4y; Lewis Edge "I would NOT choose a power station for long-term backup"). Stale; no 2026 follower. Skip.
- Quora "Do you think the Jackery Explorer 1000 v2 … $399.99 on Prime Day … powerful enough … during power outages?" (1 answer, "Jun 23", space heater and window AC, no fridge). Demand 2 at best, off-topic for the fridge page. Skip.
- Reddit r/solar "Talk me out of spending $600…" (Dec 2025): see row 5. Skip.
- Slickdeals: Jackery Explorer 2000 v2 thread 18925585 (Dec 2025, 3 comments; the poster already says it "can keep a fridge running through a full-day outage"); BLUETTI FridgePower threads 20132424 (Oct 9 2026, 0 comments shown) and 19860651 (Aug 2026, one "won't pay double for a 2 kWh station" comment). No open question. Skip.

Articles (correction notes):
- PowerOutage.us "How Long Will a Portable Power Station Run My Refrigerator?": see row 6; undated, no comments. Skip unless on page 1.
- BLUETTI blog "How Long Can a BLUETTI Portable Power Station Power a Full-size Refrigerator?" (published Oct 5 2026, within 60 days): gives the Elite 200 V2 "~13.8 Hours" from a 300 W fridge at 40 % duty (2.9 kWh/day, about double the ENERGY STAR medians). A stated assumption rather than an error, and our page already calls it the worst case; no comment section. Skip.
- PC Tech Magazine "Can a Power Station Keep Your Fridge Cold All Day" (Sep 17 2026): Anker SOLIX S2000 piece; its numbers ("1 to 1.5 kWh per day", "a 2 kWh class unit can often cover close to 24 hours") agree with ours; no comments. Skip.
- SlashGear "Can A Portable Power Station Run Your Fridge In An Emergency?" (Jun 14 2025): "divide the wattage rating by three" and "runs roughly 30 % of the time" are rough but it is 17 months old and shows no comments. Skip.
- The Cool Down, "Jackery Explorer 1000 owner loses power after grocery trip…" (Sep 26 2026): anecdote (30 % left after almost 10 hours on a fridge, consistent with our 11–17 h), no error, comments live on Reddit. Skip.
- Affiliate roundups dated "October 2026" (pwice.com, foliumbiosciences.com, portablepowerauthority.com, portablepowernerd, backuppowerhub.com, narcosis-the-game.com, voltpicks/output-report/off-grid-benchmark .pages.dev): templated listicles, no comment sections seen, no identifiable author; not worth correction notes.

Could not verify (say so before relying on any of it):
- Quora answer years (inferred from display convention, see §1), and the three blocked Quora questions.
- BLUETTI's community: zero content retrievable; the Elite 100 V2 fridge-surge thread (39174) may be a demand-2 candidate (owner with a compressor-start problem on a 1 kWh unit) but I could not read it.
- CosmoQuest, AnandTech and CandlePower threads: bot walls; dates unknown.
- Google/Bing page-1 ranks for the target queries were not checked (WebSearch does not report rank); "evergreen" is used above only for Quora questions that keep drawing answers.
- OUKITEL P1000PLUS specs in draft 2a are the OP's quoted listing figures, not checked against OUKITEL's page.

## 4. Reddit and Facebook: manual check for Barry (tools blocked)

Run each on reddit.com sorted by **New**, past month, and skim the first page; the brief's tier A is anything from
Oct 20 on.
- r/preppers: `power station fridge` and `battery backup refrigerator`
- r/HomeImprovement: `power station refrigerator outage`
- r/solar: `power station fridge` (the Dec 2025 "$600 battery station" thread will show; look for newer ones)
- r/Bluetti: `fridge` and `Elite 200 V2 refrigerator`
- r/Jackery and r/Ecoflow: `fridge outage` (brand owners asking "how long"; our page's comparison rows cover both brands)
- r/SolarDIY and r/homeowners: `power station outage fridge`
- Google alternative when Reddit search is poor: `site:reddit.com "power station" fridge outage` with Tools → Past month.
- Facebook groups (not reachable at all): "Bluetti Power Station Owners", "Portable Power Station & Solar Generator Owners", local hurricane/winter-storm prep groups; search `fridge`.
