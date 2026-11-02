# Tier 3 outreach research: /starlink-mini-usb-c-power-requirements (G09, step 7b, 2026-11-02)

Researched by a Fable 5.1 subagent (web search, WebFetch, built-in browser pane); drafts only, nothing posted, no
accounts created, no logins. Brief: `growth/focus/fastloop-briefs/outreach-brief.md`. Page facts from `src/gaps.py`
(record `starlink-mini-usb-c-power-requirements`) and Starlink's support article, re-read 11-02 in the browser pane:
"Use a USB Power Delivery source rated 100 W, 20 V at 5 A. 100 W is the minimum. Starlink Mini will not run on a USB
Power Delivery supply rated below 100 W. That includes a 65 W supply and any supply from 66 W to 99 W."

**Headline.** Two Tier A threads with real people deciding how to power a Mini off-grid right now, both on RV LIFE
forums (Thor Forums, Oct 21–23; iRV2, Oct 29–Nov 1), whose rules forbid links to a site the poster profits from, so
both replies are written to stand without the link and Barry decides whether to keep the last line. Both askers are
owners with an open question (demand 2), not undecided buyers; nobody in either thread has stated the 100 W USB PD
rule, the hours-per-Wh arithmetic, or the "~300 Wh for a workday, ~1 kWh for a day" sizing our page gives. The only
venues where a disclosed link is allowed are two Quora questions (evergreen, one with a joke as its only answer).
Rokslide has a demand-3 question from August (hunter working from a tent for a week, asking for cheaper than a Jackery
1000 v2) but bans commercial links and is outside the 45-day window. No Starlink-specific forum with open posting was
found (starlinkinsider / starlinkhardware have no forum our search could reach; starlinkminiforum.com is an affiliate
blog, blocked for the pane). Reddit and Facebook are blocked for our tools (section 5). Four blogs state a 65 W
minimum that Starlink's own article contradicts; all are older than the brief's 60-day window, so the correction notes
are optional (section 3).

Counts: Tier A 2 (both demand 2), Tier B 0, evergreen 4 (Quora 2, Rokslide 1, iRV2 solar thread 1), corrections 4
(all outside 60 days).

## 1. Ranked candidates

Demand: 3 = about to buy / undecided; 2 = owns one, open question, others shopping; 1 = technical only. Tier: A = post
in last 14 days; B = 15–45 days and unresolved; E = evergreen (older; Google rank not verifiable with our tools, so
"surfaced for" names the query our search tool returned it for).

| # | URL | Venue, dates, size | Tier | Demand (quote) | What is missing | Link rules | Action |
|---|---|---|---|---|---|---|---|
| 1 | https://www.thorforums.com/threads/starlink-mini-power-options-for-dry-camping.2211055/page-21 | Thor Forums (RV LIFE), Modifications and Updates. Opened 2026-08-14 by Scubawise; 21 pages; last post 2026-10-23; views not shown on the thread page. Venue: this section had 8 threads with posts in the last 14 days and 2 Starlink Mini threads with posts since Sep 14 (counted on the section's first page sorted by last post, 11-02). | A | **2** (16ACE27, Oct 21): "So thinking about how to power my Mini when not able to use the RV or car as power sources. Add-on battery packs seem pretty expensive to me … I picked up a Mini adapter for my Ryobi One+ batteries from Amazon for $16 … it ran the Mini for at least 3 hours." Jimbo57 (Oct 22): "I wonder how the Dewalt 60 v batteries would work"; dkoldman (Oct 23) weighing a $16 adapter vs a 2nd battery; jawzilla: adapter "has been in my list for a while". | Chateau_Nomad and dkoldman covered the over-discharge risk (tool packs have no low-voltage cutoff; Ryobi relies on the tool). Nobody has done the arithmetic (18 V × 4 Ah = 72 Wh → about 3 h at 20–25 W, which is exactly what he saw), said what a day needs (~0.5 kWh at 20 W, ~1 kWh at spec), named the USB-C route and its 100 W / 20 V 5 A rule (65–99 W banks fail), or sized the "cheaper than add-on packs" options (a 288 Wh station for a workday, a 1 kWh one for all day). Earlier pages (Aug) have bill_1202 "Costco has 500w power banks" and "I think it needs 30 to 60w" (wrong for USB-C) with no correction. | RV LIFE Community Rules (same set on Thor, iRV2, Forest River, Airstream, Jayco, Keystone, Grand Design; recorded in the rv-2kwh run): no affiliate links, no links to any page on a site you have a commercial interest in "including informational pages" unless on a vendor account; no commercial links in signatures. Posting needs an account (Barry has none on Thor Forums; agent-vault has no RV LIFE login). | Reply (draft 2a), link-free body; Barry decides on the last line |
| 2 | https://www.irv2.com/threads/looking-at-a-starlink-mini.2220262/ | iRV2 (RV LIFE), Technology: Internet, TV, Satellite, Cell Phones. Opened 2026-10-29 by Stircrazy, last post 2026-11-01, 12 posts, 1K views. Venue: 5 Starlink threads with October posts and 7 with posts since Aug 30 in this section (first page sorted by last post, 11-02). | A | **2** (Stircrazy, Oct 29): "how are most people who are just running batteries and solar powering them? … what have you done thats cost efective to power in both a vehicle and the rv?"; Oct 31: "I discovered I have absolutly no 12V cigerette lighter outlets and I don't have an inverter … I have a couple USB A and C outlets but they are not high enough wattage to run the setup. I think I have a little 400 watt inverter in the shop so I will use that untill I either get a proper inverter or install a 12V socket." Nov 1: "ya I am looking at going that way [DC-DC converter]." | 92landyacht gave the right cheap answer (12 → 30 V DC-DC converter); 1blue78 reported an Anker SOLIX C300 DC running the Mini "~14 hours". Missing: why his camper's USB-C outlets fail (a USB-C source must offer the 20 V / 5 A, 100 W profile; 65–99 W does not run it), the inverter's own idle draw (a few watts to ~10 W, a quarter to a half of what the Mini draws), and what a station buys him over the converter (works in truck and camper, hours per Wh). | Same RV LIFE rules. Posting needs an iRV2 account. | Short reply (draft 2b), link-free body; Barry decides on the last line |
| 3 | https://www.quora.com/What-do-you-use-to-power-a-Starlink-Mini-for-Wi-Fi | Quora. One answer (Alec Brusilovsky, 2026-06-09): "Electricity? Just a lucky guess…". Topic tags include "Starlink Mini", "Power Source". | E (surfaced in Quora's related-questions block of the 10,000 mAh question; rank unverified) | **1–2** by wording (asker wants to know what people use; no budget named) | Everything: the 100 W / 20 V 5 A USB-C rule, the 12–48 V DC alternatives, the hours-per-Wh table, which sizes run it for a workday vs a day. | Quora Help Center (read in the rv-2kwh and solar-kits runs): affiliate links banned; a self-promotional link allowed inside a complete, direct answer with the affiliation disclosed. Needs a Quora account (sign in with Google as barrryyao; agent-vault has no Quora login). | Answer with link + disclosure (draft 2c) |
| 4 | https://www.quora.com/Has-anyone-tried-powering-the-Starlink-Mini-dish-with-a-10-000mAh-portable-battery-If-so-how-long-does-it-last | Quora. Asked ~2 years ago; one answer (Hrmeteohub Pljusak, 2y): capacity alone can't answer, lead-acid vs lithium, "Starlink hardware … use about 100W" (that is the Standard dish, not the Mini); no runtime given. | E (first result for its own wording in our quora.com-restricted search; also the only Quora result for "Starlink Mini power bank") | **1–2** ("how long does it last?") | A real answer: a 10,000 mAh phone bank is 37 Wh and, more importantly, almost never offers the 20 V / 5 A 100 W PD profile, so it will not start the Mini at all; a 99 Wh 100 W bank gives ~2–4 h; what a day needs. | Same as #3 | Answer with link + disclosure (draft 2d) |
| 5 | https://rokslide.com/forums/threads/starlink-power.419548/page-2 | Rokslide (hunting). Opened 2025-09-07 by Davisjj8, 2 pages, 13K views, last post 2026-08-13. | E (82 days since last post; surfaced for the hunting-forums query; 13K views) | **3** at the time (mad_angler, Aug 11): "This seems like a good system that will run for an unlimited number of days. But I don't know if there are cheaper options: [Jackery Solar Generator 1000 v2] … I'm thinking of using the starlink while working remotely from a tent for up to a week at a time." | Davisjj8 answered that the Jackery panels are junk in shade and he uses a generator + Milwaukee batteries; wapitibob a 70,000 mAh/145 W MOVESPEED bank; fmyth a Jackery 290 (8 h on the Standard dish via AC). Nobody sized "a week in a tent" (≈0.5–1 kWh/day → a 1 kWh station plus ~200 W of panel, or the DC-only 288 Wh class if he only works part of the day), nor said the 1 kWh class is $395–500 now, not Jackery's $999 bundle. | Rokslide terms (read 11-02): "No commercial or business posts, no links to any commercial site, and no business names or logos … These rights are granted only to paying Rokslide sponsors." Classifieds/PMs need 7 days and 10 posts. Posting needs an account (none in agent-vault). | Optional link-free reply (draft 2e); the thread is 2.5 months quiet |
| 6 | https://www.irv2.com/threads/solar-power-supply-for-starlink-mini-while-boondocking.2206056/ | iRV2, same section as #2. Opened 2026-07-09 by jewhite2017, last post 2026-09-14, 13 posts, views not shown. | E (49 days since last post, just outside B) | **3** at the time: "I would like to get a solar power supply of some sort but cannot seem to be able to find one that is specifically designed to power Starlink … There seems to be a lot of them out there and Amazon seems to carry a number of brands." | pasdad1 said a station + panel is "$200-$300 minimum"; Mike1997 "a small Bluetti"; CIDE an Anker SOLIX C1000 + 100 W panel ran him and the Mini for a month; Brunnie owns a BLUETTI Elite 100. Nobody gave Wh-per-day or the 100 W USB-C rule, but the OP went quiet on Jul 9. | Same RV LIFE rules | Skip unless it wakes up; the facts are in draft 2a |
| 7 | https://www.irv2.com/threads/powering-starlink-mini-while-boondocking.2205466/ | iRV2; 2026-07-05 to 07-09, 18 posts, 50 views | E | 1 (house-battery wiring: upconverters, PoE, 48 V) | Answered in-thread (Fpmtngal: app shows 20–24 W). | RV LIFE | Skip |
| 8 | https://www.airforums.com/threads/powering-a-starlink-mini-on-a-2026-globetrotter.2205067/ | Airstream Forums (RV LIFE); 2026-07-01 onward, 3 pages, 231 views | E | 1 (permanent 12 V install: step-up converter, SAE plug, AIR GEAR MiniLink) | Answered (J.Silvers, SVTRIDE, WillieJ-SMB). | RV LIFE | Skip |
| 9 | https://www.thorforums.com/threads/powering-the-starlink-mini-on-my-2027-palladiums-roof.2215052/ | Thor Forums; 2026-09-14 to 09-27, 13 posts, 2K views | B by date | 1 (cable routing through the roof, PoE confusion) | Not our question. | RV LIFE | Skip |
| 10 | https://www.cybertruckownersclub.com/forum/threads/using-jackery-explorer-100-power-bank-to-power-starlink-mini-from-cybertrucks-usb.47311/ | Cybertruck Owners Club; 2025-08-26 to 09-01, 2 pages | E | 2 then (deek: truck USB drops the Mini under load, "began looking at PB options"; scottyah: "anker solix c300 … kept restarting every three to five mins. A jackery explorer 300 was able to power it") | mongo gave the 100 W (20 V/5 A) rule for USB-C. The C300-restart report is a good example for the page (a 100/140 W port that still fails). 14 months old. | Terms page 403 for the fetcher; not read. | Skip (stale) |
| 11 | https://forum.expeditionportal.com/threads/starlink-mini-power-setup-questions.245565/ | Expedition Portal, Power Systems; 2024-08-19 to 2025-12-12 | E | 3 then (1,000 Wh station + 100 W panel for a Mini and two laptops, "is that reasonable, too big, or too small?") | Answered (rruff: Wh explained; kga1978: Explorer 500 ≈ 24 h). gator70 (Dec 2025) linked PeakDo. | Expedition Portal allows product links; not re-read this run. | Skip (stale) |
| 12 | https://forum.gofastcampers.com/t/starlink-mini-mount-and-power/37146 | Go Fast Campers forum (Discourse); 2026-04-08 to 04-17 | E | 1 (12 V wiring, mounts; fskrc1: Jackery 1500's 100 W USB-C port works) | Nothing open. | Not read | Skip |
| 13 | https://bronco6g.com/forum/threads/starlink-mini-setup-power.124864/ and https://forum.ih8mud.com/threads/starlink-mini.1353091/ | Bronco6G (last post 2026-08-20, 1,957 views); IH8MUD (last post 2026-03-10) | E | 1 (mounts; wjlapier runs a Jackery 1000 v2's 100 W USB-C port) | Nothing open. | Not read | Skip |

## 2. Drafts

Each ends with the page link and the disclosure, per the brief. On the RV LIFE forums (#1, #2) the rules forbid that
last line; the body is written to stand without it, and Barry chooses whether to post with or without it.

### 2a. Thor Forums "Starlink Mini Power Options for Dry Camping", page 21 (Tier A, demand 2, reply to 16ACE27 / Jimbo57 / dkoldman)

> 16ACE27, your 3 hours is the math working, not luck: an 18 V 4 Ah pack is 72 Wh, the Mini draws about 20–25 W once it's locked on (Starlink's spec says 20–40 W, 15 W idle; the app will show you), and a converter loses roughly 15%, so 72 × 0.85 ÷ 22 W ≈ 2.8 hours. A 6 Ah pack gets you about 4 hours, a 9 Ah about 6. Jimbo57, the DeWalt FlexVolt 9 Ah is 162 Wh (it's 54 V ÷ 3 only when the tool pulls the 60 V contact; in an 18/20 V adapter it behaves as a 9 Ah 20 V pack), so about 6 hours.
>
> The part the tool-battery route can't fix is Chateau_Nomad's point: there is no low-voltage cutoff, so you are the BMS. For an afternoon that's fine; for a day it isn't.
>
> If you want "a day" from one box, size it from the draw, not from the box's wattage: 24 h × 20 W ≈ 0.5 kWh at the low end, 1 kWh if you plan on Starlink's 40 W figure (snow melt, trees, cold). Two sizes make sense:
> - **A workday (8–10 h): ~300 Wh.** EcoFlow RIVER 3 Plus (286 Wh, $299) or BLUETTI Elite 30 V2 (288 Wh, ~$275). Someone in the iRV2 thread this week gets ~14 h from an Anker SOLIX C300 DC (288 Wh), which matches a 17–20 W real-world draw.
> - **All day and night: ~1 kWh.** ALLPOWERS P1800 (1,024 Wh LiFePO4, two USB-C ports up to 140 W, ~$395–439), Anker SOLIX C1000 Gen 2 ($499.99) or BLUETTI Elite 100 V2 ($499), all 1,024 Wh: about 22–43 h of Mini. CIDE on iRV2 ran a Mini plus his coach off a C1000 and one 100 W panel for a month.
>
> One rule if you power it from a USB-C port instead of the 12 V jack: Starlink's support article says the port must be rated 100 W (20 V at 5 A), and that a 65 W supply or anything from 66 to 99 W will not run the Mini, even though it only draws 20–40 W. That is why the "500 W power bank" and "30 to 60 W" figures earlier in this thread don't translate: check the USB-C port's own PD rating, and use Starlink's own USB-C cable (it's a separate $33 accessory; the bank's built-in cables won't do). Also don't charge a phone on the bank's other port while the Mini runs; some banks drop the 20 V profile when a second port wakes up and the Mini reboots.
>
> Hours ≈ battery Wh × 0.85 ÷ watts, if you want to size your own.
>
> I keep the table (watt-hours, USB-C port ratings, hours, prices) at https://dealectric.com/starlink-mini-usb-c-power-requirements. Disclosure: I run dealectric.com, which earns a commission on some links there (the ALLPOWERS and BLUETTI rows); the Anker and EcoFlow rows are plain comparisons.

### 2b. iRV2 "looking at a starlink Mini" (Tier A, demand 2, reply to Stircrazy)

> Stircrazy, the DC-DC converter 92landyacht pointed you at is the right cheap fix for the camper, and here's why your USB-C outlets didn't work, so you don't buy another one that won't: Starlink's support article says a USB-C source has to be rated 100 W (20 V at 5 A) for the Mini; it will not run from a 65 W port or anything from 66 to 99 W, even though the dish only draws 20–40 W (about 20–24 W in practice, as Fpmtngal saw on the app). Camper USB-C outlets are 18–45 W, and the USB-C route also needs Starlink's own $33 USB-C cable.
>
> The 400 W inverter will work but costs you its own idle draw (typically 5–10 W, a quarter to a half of what the Mini uses) plus the brick's losses, so on battery you'll get maybe two-thirds of the hours the converter gives you.
>
> If you'd rather have one box that works in the Bronco, the F-350 and the camper without wiring, a small power station with a real 100 W+ USB-C port does it: 1blue78's Anker SOLIX C300 DC (288 Wh) at ~14 h is typical of the 288 Wh class (EcoFlow RIVER 3 Plus $299, BLUETTI Elite 30 V2 ~$275); a 1,024 Wh unit (ALLPOWERS P1800 ~$395–439, Anker C1000 Gen 2 or BLUETTI Elite 100 V2 at $499) runs the Mini a day and a night. Rule of thumb: hours ≈ Wh × 0.85 ÷ 20–40 W.
>
> I keep the comparison at https://dealectric.com/starlink-mini-usb-c-power-requirements. Disclosure: I run dealectric.com, which earns a commission on some links there.

### 2c. Quora "What do you use to power a Starlink Mini for Wi-Fi?" (evergreen; link allowed with disclosure)

> Three things work, and one common thing doesn't.
>
> **Wall power.** The kit's own brick (30 V) plus the 15 m cable. Nothing to size.
>
> **12–48 V DC.** The Mini accepts 12–48 V on its barrel jack, so a car socket adapter (Starlink sells one), a 12 → 30 V DC-DC converter wired to an RV battery, or an 18/20 V tool-battery adapter all run it. A 4 Ah Ryobi/DeWalt pack (72 Wh) gives about 3 hours; it has no low-voltage cutoff, so don't leave it on overnight.
>
> **USB-C PD, with one hard rule.** Starlink's support article: use a USB Power Delivery source rated 100 W (20 V at 5 A); the Mini will not run on a supply rated below 100 W, "that includes a 65 W supply and any supply from 66 W to 99 W". It only draws 20–40 W (15 W idle), but the source must offer the 20 V/5 A profile. So a phone bank, a laptop 65 W bank, or a car's USB-C port won't start it, and some 100 W+ banks drop the profile when you charge a phone on another port and the Mini reboots. You also need Starlink's own USB-C-to-barrel cable (a separate 5 m accessory); the bank's cables don't fit.
>
> How long: hours ≈ battery Wh × 0.85 ÷ watts. A 99 Wh carry-on bank with a 100 W port: about 2–4 hours. A 288 Wh station (EcoFlow RIVER 3 Plus, BLUETTI Elite 30 V2, Anker SOLIX C300): a workday, 6–14 hours depending on draw. A 1,024 Wh station (ALLPOWERS P1800, Anker SOLIX C1000 Gen 2, BLUETTI Elite 100 V2; $395–500 in Nov 2026): about 22–43 hours, i.e. a full day and night. That last class is what "all day" actually takes; the clip-on 99 Wh packs sold for the Mini are an afternoon.
>
> I keep the comparison (watt-hours, which USB-C ports qualify, hours, prices) at https://dealectric.com/starlink-mini-usb-c-power-requirements. Disclosure: I run dealectric.com, which earns a commission on some links there.

### 2d. Quora "Has anyone tried powering the Starlink Mini dish with a 10,000mAh portable battery? If so, how long does it last?" (evergreen; link allowed with disclosure)

> It almost certainly won't start, and the reason isn't capacity. Starlink's support article says the Mini needs a USB Power Delivery source rated 100 W (20 V at 5 A) and will not run on anything rated below 100 W, 65 W included. A 10,000 mAh phone bank is a 20–30 W device without the 20 V/5 A profile, so the dish never boots. (It also needs Starlink's own USB-C-to-barrel cable, a separate accessory.)
>
> If it did run, the capacity answer is short: 10,000 mAh at 3.7 V is 37 Wh, the Mini draws 20–40 W (15 W idle), and a converter loses ~15%, so 37 × 0.85 ÷ 25 ≈ 1.3 hours. Sizes that make sense: a 99 Wh bank with a genuine 100 W USB-C port (the biggest you can fly with) gives about 2–4 hours; a 288 Wh power station a workday; a 1,024 Wh station (ALLPOWERS P1800, Anker SOLIX C1000 Gen 2, BLUETTI Elite 100 V2, $395–500) about 22–43 hours. The other answer's "about 100 W" is the Standard dish; the Mini is a quarter to a third of that.
>
> Comparison with the hours table and which ports qualify: https://dealectric.com/starlink-mini-usb-c-power-requirements. Disclosure: I run dealectric.com, which earns a commission on some links there.

### 2e. Rokslide "Starlink power" (optional, link-free body; reply to mad_angler, Aug 11)

> mad_angler, size it from the Mini's draw rather than the bundle: it uses about 20–25 W once locked on (Starlink says 20–40 W, 15 W idle), so a working day is 200–300 Wh and a full 24 h is 0.5–1 kWh. For a week in a tent you need either a 1 kWh station plus enough panel to put 500 Wh+ back each day (about 200 W of panel in real conditions, which Davisjj8's point about shade cuts further), or you run the Mini only while you work and a 288 Wh unit plus 100 W of panel keeps up. The 1 kWh class is $395–500 now (ALLPOWERS P1800, Anker SOLIX C1000 Gen 2, BLUETTI Elite 100 V2, all 1,024 Wh LiFePO4), well under Jackery's $999 bundle; buy the panel separately. If you power it over USB-C the port must be rated 100 W (20 V/5 A), per Starlink; 65–99 W ports don't start it, and you need Starlink's own USB-C cable. Hours ≈ Wh × 0.85 ÷ watts.
>
> I keep the comparison at https://dealectric.com/starlink-mini-usb-c-power-requirements. Disclosure: I run dealectric.com, which earns a commission on some links there. (Rokslide's rules forbid commercial links; post without this paragraph.)

## 3. Correction and suggestion notes

Rule from the brief: only pages published/updated in the last 60 days or on page 1 for a target query. None of the
four below is inside 60 days and Google rank is not verifiable with our tools, so all are optional; they are listed
because each states a 65 W minimum that Starlink's article explicitly rules out, and the first two appear in our
search tool's results for the "all day" query.

**4WDTalk, "Starlink Mini Power Consumption: Real Watts, Runtime, 12V and Solar"** (https://www.4wdtalk.com/starlink-mini-power-consumption/, Alex Schult, 2026-06-18, no comments). Body: "The dish will not start on USB-C profiles below 65 W, so skip phone chargers"; spec table lists 65 W as the minimum and 100 W as recommended. Starlink: 100 W is the minimum; 65 W and 66–99 W will not run it. Runtime table is straight Wh ÷ W (no losses) while the text says real runtime is 10–15% lower.
> Hello, one correction on the Starlink Mini power article. It says the dish "will not start on USB-C profiles below 65 W" and lists 65 W as the minimum, 100 W as recommended. Starlink's support article "What USB power rating do I need to power my Starlink Mini?" says 100 W (20 V at 5 A) is the minimum and that the Mini "will not run on a USB Power Delivery supply rated below 100 W. That includes a 65 W supply and any supply from 66 W to 99 W." Readers buying a 65 W bank on the strength of the article will get a dish that doesn't boot. Also the runtime table divides Wh by W with no conversion loss, while the text says to expect 10–15% less; applying the 0.85 to the table would make them agree. Thanks.

**Satellite Link Power, "How Long Does Starlink Mini Run on Battery? (2026)"** (https://satellitelinkpower.com/how-long-does-the-starlink-mini-run-on-battery/, 2026-06-04, comment form open, 0 comments). Body and FAQ: "won't run on PD sources below 65W" alongside "recommends a 100W (20V/5A) USB-C PD source". Same correction as above; can be posted as a comment.
> One correction: the article says the Mini "won't run on PD sources below 65W", which implies 65–99 W sources work. Starlink's own USB power rating article says 100 W (20 V/5 A) is the minimum and that "a 65 W supply and any supply from 66 W to 99 W" will not run it. Worth changing, since a 65 W laptop bank is exactly what readers will reach for.

**Budget Seniors, "8 Best Starlink Mini Batteries"** (https://www.budgetseniors.com/starlink/starlink-mini-battery/, 2026-07-31, comment form open, 0 comments). "The minimum for reliable operation: 65W USB-C PD output or 60W DC output" and "65W PD works under normal conditions but may fail during the 60W startup surge", then, correctly, "Requires 100W PD (20V/5A) for guaranteed reliable startup". The two statements conflict; Starlink's article settles it (100 W minimum, 65–99 W will not run it). Same note as above, shortened.

**Dishy Mini Mounts (AU), "Starlink Mini Power Consumption and Battery Runtimes"** (https://www.dishyminimounts.com.au/blogs/starlink-mini-guides/starlink-mini-power-consumption, no date shown, Australian vendor, no comment section). "The power bank must support USB-C Power Delivery (PD) at 65W or higher … Minimum is 65W (20V/3.25A); we recommend 100W (20V/5A)." Wrong per Starlink; Australian audience, no comments; skip unless Barry wants to email them.

Checked and accurate (no note): CTmods "Starlink Mini Won't Power On With USB-C? 100W PD…" (2026-04-06) and "Best Power Banks for Starlink Mini in 2026" (2026-04-16): both quote Starlink's 100 W / 20 V 5 A and the "65 W or lower won't work" line correctly; comments open but moderated, vendor blog, nothing to correct. GLK Power (2026-02-28): 100 W (20 V/5 A) and "45W or 65W PD often fail", hours table with 0.85 factor at 30–40 W; no comments. Nomad Outfit (2026-08-04): leads with 100 W (20 V/5 A) and the 0.85 formula; mentions MobileMustHave selling a kit "for use with a USB-C PD supply of 65W or greater" as a vendor claim; no comments. Anker SOLIX blog (2026-05-11): 20–40 W, 15 W idle, no USB-C PD rule at all (omission, not error); no comments. XTAR-LINK (2026-01-16): no wattage claims. SlashGear (2025-07-29): "a minimum of 20V, 5A (100W)", correct. Woyum (2026-06-24): no USB-C claims; runtime table at ~90% efficiency.

## 4. Checked and rejected, or could not check

- **Reddit** (all subreddits): reddit.com blocked for WebSearch, WebFetch and the browser pane. Search snippets from mirror sites (reddit.sentinel-team.org, lr.in.psf.lt, redlib.nohost.network) show r/Starlink threads "What are you using to power your Starlink Mini", "Mini mobile power setup", and Jan–Feb 2026 posts about an EcoFlow bank cutting out and an Anker bank dropping the 20 V profile when a second port is used; none opened. See section 5.
- **Facebook**: two "fb-answers" pages and one group post are in ChatGPT's result set for the target query (pack.json): https://www.facebook.com/groups/472261552049873/posts/564087766200584/ ("What is the minimum power bank wattage required for … what was the lowest watt powerbank sby tried successfully with the mini?", Cartagena) and https://www.facebook.com/fb-answers/can-you-power-a-starlink-mini-with-usb-c/ (says "at least 60-100W at 20V", wrong per Starlink). Blocked for our tools; manual check (section 5).
- **Quora search** needs a login; direct question URLs open in the pane. Also seen: "Can a power station keep Starlink running during outages?" (OpenBlueprint, 2026-05-09, Standard dish, answered), "How much battery do I need for Starlink and a laptop?" (two answers May 2026, Standard dish, answered), "What is the power required for the Starlink wifi router…" (1y, Standard). None about the Mini beyond rows 3–4.
- **DIY Solar Forum**: search requires login (pane showed the login wall); site-restricted web search returned nothing on "Starlink Mini"; agent-vault has a diysolarforum login but no logins were used this run. Worth a logged-in search later (`starlink mini`, newest first).
- **Tacoma World, Overland Bound, Cruisers Forum, SailNet, The Hull Truth, Sailing Anarchy, iboats, Long Range Hunting, 24hourcampfire, Tundras, Rivian Forums, Jeep Gladiator, Trawler Forum, 4Runners, Tacoma4G, Cheap RV Living, Four Wheel Campers, Wander the West**: site-restricted searches returned no Starlink Mini power threads (the search tool ignored most `site:` filters and returned vendor blogs). Rivian Forums post 607807 ("100W-rated power bank could not run it", per the snippet) is behind a Cloudflare challenge in the pane; date unknown; manual check.
- **Starlink community forums**: starlinkinsider.com and starlinkhardware.com surfaced no forum pages; starlinkminiforum.com is an affiliate "best power bank" page and the pane refused the domain.
- **Amazon Q&A**: Amazon no longer shows public customer Q&A; the PeakDo LinkPower 1 listing (B0F9YH5ZWS, $169, "500+ bought in past month") has only the AI "Looking for specific info?" box. Nothing to answer. The Amazon search results confirm demand: at least ten third-party "Starlink Mini battery pack" listings (99–166 Wh, 4–6 h claims).
- **Best Buy Q&A, Starlink Mini Kit (SKU 6589861)**: 216 questions, 1,302 reviews; no question mentions battery, power bank or USB-C (searched the page); the AI-generated Q&A says 25–40 W. Nothing to answer.
- **Escape forum** "StarLink Mini measured power consumption" (Feb 2025, 784 views): gklott measured ~20 Wh/h, 400–450 Wh/day; answered, stale, RV LIFE.
- **Thor Forums** pages 1–20 of thread 2211055 not read post by post; page 2 (Aug 17–19) has bill_1202 "I think it needs 30 to 60w … Costco has 500w power banks" and Scubawise linking a 130 W USB-C car charger (Chateau_Nomad corrected: that's a phone charger). Draft 2a addresses both without naming them.
- **iRV2 "Where to purchase Starlink"** (Sep 26 – Oct 5, 5K views): buying the kit, not power; skip. **"Using a Firestick With Starlink Mini"** (Aug–Sep): not power.
- **CTmods, XTAR-LINK, GLK Power, Nomad Outfit, Woyum, Satellite Link Power, Budget Seniors, 4WDTalk, Anker SOLIX, EcoFlow and BLUETTI blogs**: vendor or affiliate pages; comment sections open on CTmods (moderated), Satellite Link Power, Budget Seniors, Woyum, XTAR-LINK (moderated); none has a reader question to answer. Several (xtar-link.com, dishyminimounts.com.au, ctmods.com) returned 429 or 403 for the fetcher and were read in the pane.
- **Airstream Forums "Starlink Mini" megathread** (1441539, 21 pages, 12K views): last post 2026-03-07, propane-box mounting; stale.

## 5. Manual checks for Barry (Reddit, Facebook, login-walled forums)

Reddit, "Sort: New", "Past month", then "Past year" for evergreen:
- r/Starlink: `mini power bank` ; `mini battery how long` ; `mini 100W` ; `mini reboot power bank`
- r/Starlink_Support (if active): `mini power`
- r/overlanding, r/vandwellers, r/GoRVing, r/RVLiving, r/TruckCampers: `starlink mini power`
- r/solar, r/SolarDIY, r/preppers: `starlink mini battery`
- r/Bluetti, r/Ecoflow, r/anker, r/Jackery: `starlink mini`
r/Starlink's sidebar bans self-promotion and affiliate links; a disclosed link inside a full answer survives in the
brand subs more often. Expect the "65 W works for me" anecdotes (short cable, warm weather) to come up; the reply is
that Starlink rates the source, not the draw, and a bank that boots the dish on a good day drops it under load.

Facebook: the group post in ChatGPT's result set (above), plus groups "Starlink for RVers", "Starlink Mini Users",
"Starlink Users Group" (names from memory, unverified); search `power bank` and `battery` inside each, Recent posts.

Login-walled: DIY Solar Forum search (agent-vault login exists), RV LIFE search across all brand forums (iRV2 account
needed), Rivian Forums post 607807.

## 6. What this means for the page

- The live demand is "which battery and how many hours", asked by owners who already have the Mini (both Tier A
  askers), and the cheap answers they get are tool-battery adapters and 12 → 30 V DC-DC converters. The page could add
  one line each: "an 18/20 V 4 Ah tool pack (72 Wh) runs it about 3 h, with no low-voltage cutoff" and "from an RV
  battery, a 12 → 30 V DC-DC converter avoids the USB-C rule entirely". Both would make the page the full answer to
  the question as it is actually asked.
- Owners report 17–25 W real draw (iRV2 app readings 18–24 W; Anker C300 DC ≈ 14 h; Escape forum 20 Wh/h), below
  Starlink's 20–40 W. The page's "about 22–43 h" for 1,024 Wh is conservative; a "measured ~20 W → ~43 h" note would
  match what owners see without overpromising.
- Three fresh owner reports (Cybertruck forum: Anker SOLIX C300 restarts every 3–5 min on its 100/140 W port; Reddit
  snippets: EcoFlow bank cuts out, Anker bank drops the profile when a second port wakes) support the page's "keep
  other devices off a bank that reboots the Mini" line; a named example would make it concrete.
Not changed in this run (not in scope).
