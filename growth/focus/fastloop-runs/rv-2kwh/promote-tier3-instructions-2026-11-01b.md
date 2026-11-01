# Promote, tier 3, run 2: instruction set for /best-2kwh-power-station-for-rv (DLC-114, 2026-11-01)

Source: `outreach-2026-11-01b.md` (second research pass under `growth/focus/fastloop-briefs/outreach-brief.md`: freshest threads first, scored for buying demand). Same rules as `promote-tier3-instructions.md` ("Rules for whoever runs this"): agent's Chrome on 9222 only, never the final click, never create an account, never type credentials, paste exactly, re-read the thread's last posts first, one screenshot per filled form, footprint logging.

Not in this set: the rvforums.com "Emergency backup power" thread (posted in an off-topic subforum by a 7-post account citing a listicle, poster in American Samoa where most US stores don't ship: reads as content marketing, so answering it reaches no real shopper; draft 2c stays in the research file if Barry disagrees). The Airstream lithium thread (a battery buyer, already answered).

## T0. Remove the link from Barry's Forest River post #21 (fix)

- **Where:** https://www.forestriverforums.com/threads/using-a-portable-power-station-with-a-30-amp-rv-outlet.2192187/page-2 (post by barrryyao, 2026-10-31 22:19)
- **Account:** RV LIFE forum account (agent-vault `list_accounts`, the RV LIFE login).
- **Steps:** Open the post's Edit control. In the editor delete only the last line, "You can see it explained very well here" followed by the dealectric.com link. Change nothing else. Do not click Save.
- **Rules:** RV LIFE Community Rules ban links to any site the poster has a commercial interest in, "including informational pages"; the line also reads as a third party's recommendation of our own site. If the Edit control is gone (edit window closed), report it: Barry can ask a moderator or leave it.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
(delete the last line; nothing to paste)
```

## T10. Reply on Airstream Forums, "Portable Power Station as House Battery" (no link)

- **Where:** https://www.airforums.com/threads/portable-power-station-as-house-battery.2216870/
- **Account:** RV LIFE forum account (airforums.com was added to the RV LIFE vault login on 11-01).
- **Steps:** Open the thread, scroll to the reply editor, paste the text, do not click 'Post reply'.
- **Rules:** RV LIFE rules: no link, no site name, no commercial signature. The text has none.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
You are not missing much, and GOUSC's setup is the practical version of the idea, so a few numbers to put under it.

**The socket is 30 A, the box is not.** Every 2 kWh station in this class (BLUETTI AC200L, Anker SOLIX C2000 Gen 2, Renogy PowerStation 2000, and the Elite 200 V2 GOUSC has) is a 2,400–2,600 W inverter. 2,400 W ÷ 120 V is 20 A. A pedestal gives you 3,600 W. So whether you plug the shore cord into a built-in TT-30 (AC200L, C2000, Renogy) or go through a 50→30 or 50→20 dogbone, the trailer behaves exactly like it is on shore power, but with a 20 A budget: converter, pump, lights, furnace blower, coffee maker, TV, microwave on its own. Not the air conditioner for more than about an hour (13,500 BTU: 2,800–3,500 W to start, ~2,000 W with a soft start, 1,300–1,900 W running). On a 50 A rig the dogbone just puts both legs on the one 120 V feed, which is what happens at any 30 A site; it is not a problem, it is a budget.

**Elite 200 V2 and the adapter.** It has no TT-30, only 20 A household outlets, so GOUSC's 50A→20A cord is the right connection and it is capped at 20 A either way. The AC200L is the same battery with a TT-30 and 1,200 W of solar input; the C2000 Gen 2 is the light one at 41.7 lb.

**The converter.** This is the part that decides whether the "plug in like shore power" idea works. The moment the station feeds the trailer, the converter sees shore power and starts charging the house batteries, and a 55 A converter pulls up to ~800 W doing it, with a 15–20 % DC→AC→DC loss on top. GOUSC's instinct is right: it is a poor way to charge, but it is a fine deliberate one. Let it run for an hour in the morning if the house battery needs it, then switch the converter breaker off and leave the battery connected; the 12 V side (lights, pump, fridge board, furnace, breakaway) keeps running from the house battery as it always does, and the station only carries 120 V loads. Do not pull the battery itself out of the circuit; that is what kills the 12 V side.

**Budget.** A 12 V compressor fridge is ~0.7 kWh a day, a furnace blower 0.3–0.5 kWh on a cold night, lights/pump/phones ~0.2 kWh: 1.2–1.5 kWh a day. A 2 kWh station is a day and a half with no sun, two to three days with 200–400 W of panel. GOUSC's 250 W roof plus a 2 kWh pack is a reasonable three-day rain buffer for a 12 V fridge, if the fridge is the only big load. For a Harvest Host night with a 1,000 W factory inverter already on board, the station is honestly more than you need; its value is the days when the sun does not show.

**Dropping the house batteries entirely** (the YouTube idea): it works electrically if the station's 12 V output can carry your DC loads, but most of these units give 10 A on the 12 V socket (120 W), which will not run a furnace blower plus pump, and the breakaway switch wants a battery that is always there. Keep a battery, even a small one.

So: 2 kWh station in the ~$850–900 range vs. a $2,500 lithium build. The station wins on no wiring, portability and dual use at home; the lithium build wins on usable Ah per dollar and on running the inverter you already have. For "a few days at a HH, sometimes" the station is the smaller project.
```

## T11. Reply on Forest River Forums, "Upgrading a 2024 Viking Battery for Boondocking" (no link)

- **Where:** https://www.forestriverforums.com/threads/upgrading-a-2024-viking-battery-for-boondocking.2213673/ (last page)
- **Account:** RV LIFE forum account.
- **Steps:** Open the thread's last page, paste the text in the reply editor, do not click 'Post reply'.
- **Rules:** RV LIFE rules: no link, no site name. The text has none.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
Arbymail, the 200 Ah LiFePO4 advice above is sound and your WFCO is lithium-capable, so that path is open. Since you have never camped without hookups and want to "try it but only if equipped", one other option fits a 17 ft trailer with a 12 V fridge, and nobody has mentioned it: a 2 kWh portable power station with a built-in TT-30 (the RV 30 amp socket). Your shore cord plugs straight into it, the trailer thinks it is at a campsite, nothing in the trailer gets rewired, and the same box runs your house fridge in an outage. Under $900 there are three with a real TT-30: BLUETTI AC200L (2,048 Wh, 62 lb, 1,200 W solar input), Anker SOLIX C2000 Gen 2 (2,048 Wh, 42 lb) and Renogy PowerStation 2000 (2,048 Wh, 52 lb). All LiFePO4, 3,000+ cycles, recharge from any wall outlet in about 1–1.5 hours.

Three honest caveats:

1. The 30 amp socket on these delivers about 20 amps (2,400 W inverter ÷ 120 V), not the 3,600 W a pedestal gives. Fridge, pump, lights, furnace blower, coffee maker, TV, microwave on its own: fine. The rooftop AC: about an hour, if it starts at all.
2. When you plug in, your converter will start charging the trailer battery from the station (up to ~800 W) and keep idling on it. Let it top the battery up, then flip the converter's breaker off and leave the battery connected; your 12 V stuff keeps running from the battery as normal.
3. Cost per watt-hour is higher than a bare 200 Ah battery (~2.5 kWh usable for $500–700). You are paying for the inverter, charger and portability.

Your budget either way: your half-size 12 V fridge is roughly 0.5–0.7 kWh a day (DJ252's 30–60 Ah in medium temps is the same number), furnace blower 0.3–0.5 kWh on a cold night, lights/pump/phones ~0.2 kWh: about 1.2–1.5 kWh a day. That is a day and a half from a 2 kWh station with no sun, two to three days with a 200–400 W folding panel; the same math applies to a 200 Ah lithium. If you go the battery route, the station is still the easier thing to carry for the first trip; if you go the station route, you still want a decent battery in the box for the breakaway switch and the 12 V side.
```

## T12. Comment on modernsurvivalblog.com's 2 kWh comparison (link with disclosure)

- **Where:** https://modernsurvivalblog.com/alternative-energy/2kwh-portable-power-station-comparison/ (Bing #1 for the target query on 11-01)
- **Account:** None (comment form). Name: Barry. Email: hello@dealectric.com. Website: leave blank.
- **Steps:** Scroll to the comment form, fill name, email and the text, do not click 'Post Comment'.
- **Rules:** No stated link policy; the text discloses the affiliation and offers to have the link stripped.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
Ken, one addition for the RV readers you mention, since the AC200L is the only unit of the three with a TT-30: the socket is a 30 amp shape, but the AC200L is a 2,400 W inverter, so it delivers about 20 amps (2,400 ÷ 120), not the 3,600 W a campground pedestal does. Plugged in, the RV works exactly like shore power within that 20 A: fridge, pump, lights, furnace fan, coffee maker, microwave by itself; the rooftop AC for about an hour. Two things people get wrong: the RV's converter starts charging the house battery from the station (up to ~800 W on a 55 A converter), so switch the converter breaker off once that battery is full; and a 2-way fridge on AUTO picks electric and eats 2.4–3.6 kWh a day, more than the whole pack. The other two 2 kWh units with a native TT-30 under $900 are the Anker SOLIX C2000 Gen 2 (Anker rates its TT-30R at 20 A) and the Renogy PowerStation 2000. I wrote it up with current prices at https://dealectric.com/best-2kwh-power-station-for-rv (disclosure: my site, affiliate links on the BLUETTI rows). Happy for you to strip the link; the numbers stand on their own.
```

## T13. Correction email to thepowerstationguide.com

- **Where:** mailto:contact@thepowerstationguide.com (page: https://thepowerstationguide.com/blog/best-2000wh-portable-power-stations, Bing #2 for the target query)
- **Account:** None. Create a Gmail DRAFT (Gmail connector `create_draft`), never send.
- **Steps:** Draft to contact@thepowerstationguide.com, subject 'Correction: Bluetti Elite 200 V2 has no TT-30 outlet', body below.
- **Rules:** A factual correction; no link to our site.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
Hello, two corrections for "Best 2000Wh Portable Power Stations (2026): 7 Picks". (1) The Bluetti Elite 200 V2 does not have a TT-30 outlet. The article says "The Anker C2000 Gen 2, AFERIY P280 and Bluetti Elite 200 V2 have one", lists its outlets as "Four 120V 20A outlets plus one NEMA TT-30" and gives "TT-30 outlet and 2,600W output" as a strength. BLUETTI's Elite 200 V2 product page (bluettipower.com/products/elite-200-v2-portable-power-station) lists the AC side as "2,600W in total, 120V, 21.6A" with no TT-30; the TT-30 appears only in the AC200L row of BLUETTI's own comparison table on that page ("4 x 120V/20A Outlets, 1 x 120V/30A NEMA TT-30"). RV buyers reading your page would order the wrong unit. (2) The AC200L is listed as "Discontinued by Bluetti". It was in stock on BLUETTI's US store at $899 on 2026-10-31; only BLUETTI Canada marks it discontinued. "Late in its life" would be accurate. Your note that Anker caps the C2000 Gen 2's TT-30R at 20 A is correct and worth extending to every 2,400 W unit. Thanks for an otherwise careful piece.
```

## T14. Correction note to boondockorbust.com

- **Where:** https://boondockorbust.com/contact/ (topic "General feedback"); fallback mailto:chuck@boondockorbust.com
- **Account:** None. Form: name Barry, email hello@dealectric.com. If no usable form, a Gmail DRAFT.
- **Steps:** Fill the contact form with the text below and do not submit; or create a Gmail draft, subject 'Correction: Elite 200 V2 TT-30 line in your RV power article'.
- **Rules:** A factual correction; no link to our site.
- **Stop before:** the final submit/post/send/save click.

**Text to paste:**

```text
Hi Chuck, one correction on "RV Boondocking Power: Lithium vs Power Station 2026" (updated Oct 11). It says "The Elite 200 V2 has a 30 amp RV outlet (TT-30)" and "Its AC outlets include one 120 V/30 A TT-30 RV outlet." The Elite 200 V2 has four 120 V/20 A household outlets and no TT-30; BLUETTI's product page lists its AC output as "2,600W in total, 120V, 21.6A", and in BLUETTI's own comparison table on that page the TT-30 appears only on the AC200L ("1 x 120V/30A NEMA TT-30"). An RVer following the article would need a 5-20P to TT-30R adapter, capped at 20 A. If it helps, the sentence that is true of the AC200L is also worth a caveat: its TT-30 shares the 2,400 W inverter, so it supplies about 20 A, not 30. The rest of the piece (dated prices, sale windows) is unusually careful, which is why this one line stands out.
```

## Execution log (2026-11-01)

Run in the agent's Chrome (localhost:9222) over CDP, background tabs left open; no final click made anywhere. Already signed in to the RV LIFE forums (forestriverforums.com and airforums.com both showed barrryyao), so no vault login was needed.

- **T0: blocked, edit window closed.** Post #21 (post-23924637) shows no Edit control; `/posts/23924637/edit` returns "The time limit to edit this message (60 minutes) has expired." The line "You can see it explained very well here" + the dealectric.com link is still live. Barry's options: Report the post / ask a moderator to remove the line, or leave it. Tab: https://www.forestriverforums.com/posts/23924637/edit (also the thread at .../page-2). Screenshot: /private/tmp/claude-501/-Users-jiayiyao-Desktop-dealectric/c22c5b8b-bb1c-44d4-a829-d2338807c44c/scratchpad/outreach-run2/T0-edit-expired.png
- **T10: filled, waiting for Barry's click (Post reply).** No posts since 2026-09-30 (last: Ginophiles); thread open. Text pasted as rich text: paragraph breaks kept, the ** markers came out as real bold, text matches the block exactly. Tab: https://www.airforums.com/threads/portable-power-station-as-house-battery.2216870/ Screenshot: /private/tmp/claude-501/-Users-jiayiyao-Desktop-dealectric/c22c5b8b-bb1c-44d4-a829-d2338807c44c/scratchpad/outreach-run2/T10-airforums-pps-house-battery.png
- **T11: filled, waiting for Barry's click (Post reply).** Last page is page 2; no posts since 2026-10-28 (tomkatb). Note: Arbymail's 10-28 post says his WFCO is auto-detect and he "should be good", i.e. he seems settled on LiFePO4; the reply's opening already agrees with that path, so not treated as a change. Paragraphs and the 1-2-3 lines kept, text matches exactly. Tab: https://www.forestriverforums.com/threads/upgrading-a-2024-viking-battery-for-boondocking.2213673/page-2 Screenshot: /private/tmp/claude-501/-Users-jiayiyao-Desktop-dealectric/c22c5b8b-bb1c-44d4-a829-d2338807c44c/scratchpad/outreach-run2/T11-forestriver-viking.png
- **T12: filled, waiting for Barry's click (Post Comment); name needs a decision.** wpDiscuz form, 0 comments, 1,400-char limit (text is 1,104). Comment text exact, Name "Barry", Email hello@dealectric.com, no website field exists. The form shows "This name is already in use. If you're a different commenter, please choose a unique alias", so Barry should change the name before posting (it may be rejected as is). Tab: https://modernsurvivalblog.com/alternative-energy/2kwh-portable-power-station-comparison/ Screenshot: /private/tmp/claude-501/-Users-jiayiyao-Desktop-dealectric/c22c5b8b-bb1c-44d4-a829-d2338807c44c/scratchpad/outreach-run2/T12-modernsurvivalblog-comment.png
- **T13: Gmail draft created** (account barrryyao@gmail.com) to contact@thepowerstationguide.com, subject "Correction: Bluetti Elite 200 V2 has no TT-30 outlet", body exact, not sent. Draft id r8045915270017562401: https://mail.google.com/mail/?authuser=barrryyao@gmail.com#all?compose=thread-f:1880632752128267462%2Bmsg-a:r8045915270017562401 (no screenshot; not a page form).
- **T14: filled, waiting for Barry's click (Send Message).** Contact form used (no Gmail draft): Name Barry, Email hello@dealectric.com, Topic "General feedback", message exact; honeypot "website" left empty. Tab: https://boondockorbust.com/contact/ Screenshot: /private/tmp/claude-501/-Users-jiayiyao-Desktop-dealectric/c22c5b8b-bb1c-44d4-a829-d2338807c44c/scratchpad/outreach-run2/T14-boondockorbust-contact.png
- No dealectric.com pages were fetched in this run, so no footprint entries were added.
