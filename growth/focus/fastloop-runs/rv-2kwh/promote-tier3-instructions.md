# Promote, tier 3: instruction set for /best-2kwh-power-station-for-rv (DLC-114, 2026-11-01)

Source: growth/focus/fastloop-runs/rv-2kwh/outreach.md (research and reasons). Executed by a subagent up to the last click; Barry reviews each filled form in the agent's Chrome (port 9222) and clicks Submit himself.

## Rules for whoever runs this

- Use only the agent's Chrome on localhost:9222 (CDP). Never Barry's personal Chrome, never another debug port.
- **Never click the final Submit / Post / Send.** Stop with the form filled and leave the tab open. Gmail: create a draft, never send.
- **Never create an account.** If a task needs a login, check agent-vault `list_accounts` and log in through `login` only if an account for that site exists. If none exists, open the site's sign-up page in the agent's Chrome and leave it for Barry (fill nothing there, click nothing), then move on: account creation is Barry's step.
- Never type credentials or codes; agent-vault fills them.
- Paste the text exactly; don't add links, signatures or marketing. If the page shows the question was already answered the same way, or the thread is locked, skip and report.
- Before filling, re-read the thread's last posts; if something new changes the answer, report it instead of pasting.
- Take one screenshot of each filled form for Barry (scratchpad), and leave the tab open with a recognizable title.
- Log any touch of dealectric.com with evallib.footprint (the project hook logs browser touches).

## Not in this set

- Reddit: blocked for every tool we have; Barry reads r/RVLiving, r/GoRVing and r/traveltrailers manually and decides.
- powergetup.com: no contact path found. Keystone, Jayco threads: already answered in-thread.

## T1. Reply on Forest River Forums (no link)

- **Where:** https://www.forestriverforums.com/threads/using-a-portable-power-station-with-a-30-amp-rv-outlet.2192187/
- **Account:** RV LIFE forum account (forestriverforums.com). Check agent-vault `list_accounts`; if none, STOP this task (account creation is Barry's step).
- **Steps:** Open the thread, scroll to the reply editor at the bottom, paste the text, do not click 'Post reply'.
- **Rules:** RV LIFE rules: no links to any site we profit from, no commercial signature. The text has no link and no site name.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
Natalie, the short version: yes, it is nearly that simple, with three things worth knowing.

1. **The TT-30 on a 2 kWh station is not a real 30 amp supply.** The inverters in this class (BLUETTI AC200L, Anker C2000, Renogy PowerStation 2000, the Oupes Mega 2 mentioned above) are 2,400 W, and 2,400 W ÷ 120 V is 20 amps. A pedestal gives you 3,600 W. So the trailer works exactly like it is on shore power, but you have a 20 A budget: fridge on propane, water pump, lights, furnace blower, coffee maker, TV, one thing at a time for the big draws. The rooftop AC needs 2,800–3,500 W to start (about 2,000 W with a soft starter) and 1,300–1,900 W to run, so even where it starts, a 2 kWh pack gives you roughly an hour.

2. **On the converter, both camps above are partly right.** The moment you plug in, the converter sees shore power and starts charging your lead-acid battery, and a typical 55 A converter can pull up to ~800 W doing it. That is fine if the battery is low and you want it topped up, but once it is full the converter just idles away station capacity (and you lose 15–20% converting DC to AC and back). The practical rule: flip the converter's breaker off once the house battery is full, and leave the battery connected. Only switching the converter breaker keeps all your 12 V stuff (lights, fridge board, furnace, pump, breakaway) running off the house battery as normal. Do not disconnect the battery itself; that is what kills the 12 V side.

3. **Budget.** A weekend of fridge on propane, furnace blower, lights, pump and phones is about 1.2–1.5 kWh a day, so a 2 kWh station is roughly a day and a half with no sun, two to three days with 200–400 W of portable solar. If your 2-way fridge has an AUTO setting, set it to propane; on AUTO it will quietly take the electric element and use 2.4–3.6 kWh a day, more than the whole pack.

Recharging: a campground or house outlet refills these in about 1–1.5 hours; the truck's 12 V socket is only ~100 W (a full day for a full charge); a 560–800 W DC-DC alternator charger is the drive-and-charge option; 400 W of panel returns 1–1.5 kWh on a good day.
```

## T2. Reply on My Grand RV (no link)

- **Where:** https://www.mygrandrv.com/threads/using-an-anker-c2000-with-a-30-amp-rv-inlet.2203944/
- **Account:** RV LIFE forum account. The vault has only forestriverforums.com; RV LIFE forums may share one account. Try `login` with the forestriverforums.com item on this site's login page; on `origin_mismatch`, call `add_site_domain` (Barry approves the exact domain in a desktop dialog) only if the login page is clearly RV LIFE's own; otherwise stop this task.
- **Steps:** Same as T1.
- **Rules:** Same as T1.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
To your two questions directly:

**Converter breaker:** turn it off once your two AGMs are full, and leave the batteries connected. With the C2000 plugged into the 30 A inlet, your WFCO-style converter treats it as shore power and will push up to ~800 W into the batteries while they want charge; once they are full it just wastes station capacity through a DC→AC→DC loop. Turning only the converter breaker off leaves all 12 V loads (lights, pump, fridge control, furnace) on the AGMs, which is how dry camping normally works anyway.

**30 A inlet vs. plugging appliances straight into the Anker:** electrically it is the same inverter either way. Anker rates the C2000 Gen 2's TT-30R at "120V 20A Max, 2400W Max", the same as its 20 A household outlets, so the shore-cord route does not get you more power, it just lets the trailer's own outlets, microwave and converter run. For an air fryer and a coffee maker, plugging them straight into the Anker is slightly more efficient (no converter idle draw) and lets you keep the station inside. Use the 30 A inlet when you want the hard-wired microwave or the whole trailer live.

**Three days:** a modest load of fridge on propane, furnace blower (nights in Canada in September), lights, pump and phones is roughly 1.2–1.5 kWh a day. Your two AGMs give you about 1 kWh usable (50% rule) and the 200 W panel maybe 0.5–0.8 kWh on a clear September day, so the house side alone is tight for three days. Bring the C2000 (2 kWh) in reserve: either run the trailer from it for a day, or let the converter charge the AGMs from it for an hour each morning, then switch the converter back off. Set the fridge to propane, not AUTO, or it will eat the budget.
```

## T3. Reply on Airstream Forums (no link)

- **Where:** https://www.airforums.com/threads/best-solar-generator-for-30-amp-airstream-use.2179848/
- **Account:** RV LIFE forum account. Same approach as T2.
- **Steps:** Same as T1.
- **Rules:** Same as T1.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
On "reasonable pricing", a different tier than most of the thread: if you give up on running the AC for more than about an hour, the sweet spot for a 30 A Airstream is a 2 kWh station with a built-in TT-30, which is $850–900 right now: BLUETTI AC200L ($899), Anker SOLIX C2000 Gen 2 ($899.99, 41.7 lb, the one to carry) and Renogy PowerStation 2000 ($849). All three are 2,400 W inverters, so the TT-30 socket is really a 20 A supply (2,400 W ÷ 120 V), not 30 A; the trailer works exactly like shore power within that. With your ActiveStart the AC will probably start (start surge drops to ~2,000 W), but at 1,300–1,900 W running, a 2 kWh pack is about an hour, which is why the 3 kWh+ units keep coming up when AC is the goal. For everything else (fridge on propane, pump, lights, furnace blower, coffee, Starlink), 1.2–1.5 kWh a day is typical, so a day and a half with no sun, two to three days with 200–400 W of solar. Two habits: flip the converter breaker off once the house battery is full (it will pull up to ~800 W from the station otherwise), and set the fridge to propane rather than AUTO.

On "here in 5–10 years": BLUETTI, Anker and EcoFlow are the three with the longest track records; Pecron and Oupes are cheaper per Wh but younger. The chemistry (LiFePO4) is the same across all of them now.
```

## T4. Answer on Quora (link with disclosure)

- **Where:** https://www.quora.com/Can-a-portable-power-station-be-used-to-power-an-RV-or-camper
- **Account:** Quora account. Check `list_accounts`; if none, STOP this task (Barry creates it).
- **Steps:** Open the question, click Answer, paste the text into the editor, do not click Post.
- **Rules:** Quora: affiliate links banned in answers; a self-promotional link is allowed as part of a full answer with the affiliation disclosed. Our page carries affiliate links but the link is to our page, not an affiliate URL, and the disclosure is in the text.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
Yes, and for a 30 amp RV it works better than people expect, as long as you understand one number.

**Pick a station with a built-in TT-30 (the RV 30 amp outlet).** Then your shore cord plugs straight in and the RV behaves exactly as if it were on a campground pedestal: all outlets live, converter on, microwave works. In 2026 the 2 kWh units with a real TT-30 are around $850–900: BLUETTI AC200L (2,048 Wh, 2,400 W, $899), Anker SOLIX C2000 Gen 2 (2,048 Wh, 2,400 W, 41.7 lb, $899.99) and Renogy PowerStation 2000 (2,048 Wh, 2,400 W, $849). Jackery's Explorer 2000 v2 and BLUETTI's Elite 200 V2 have no TT-30 and need an adapter.

**The number: the 30 amp socket only delivers about 20 amps.** 30 A × 120 V is 3,600 W; these inverters are 2,400 W, which is 20 A. So you get fridge (on propane), water pump, lights, furnace fan, coffee maker, TV, one heavy appliance at a time. What you do not get is the rooftop air conditioner: a 13,500 BTU unit needs 2,800–3,500 W to start (about 2,000 W with a soft starter) and 1,300–1,900 W to run, so a 2 kWh pack runs it for about an hour even when it starts.

**Two things people get wrong:**
- Your RV's converter will start charging the house battery from the station, up to about 800 W. Fine while the battery is low; once it is full, switch the converter's breaker off (leave the battery connected) so the station is not drained through a DC→AC→DC loop.
- A 2-way fridge on AUTO will pick electric and use 2.4–3.6 kWh a day, more than the whole battery. Set it to propane.

**Budget:** a typical weekend load is 1.2–1.5 kWh a day, so figure a day and a half with no sun, two to three days with 200–400 W of solar. Recharge from any wall outlet in 1–1.5 hours, from a 400 W panel at 1–1.5 kWh a day, or while driving with a 560–800 W DC-DC alternator charger (the cigarette socket is only ~100 W).

I put the full comparison with current prices here: https://dealectric.com/best-2kwh-power-station-for-rv. Disclosure: I run dealectric.com, which earns a commission on some links (the BLUETTI ones on that page; the Anker and Renogy rows are plain links).
```

## T5. Comment on thecampingnerd's TT-30 article (link with disclosure)

- **Where:** https://thecampingnerd.com/power-stations-with-tt-30-rv-outlet/
- **Account:** None (comment form). Name: Barry. Email: hello@dealectric.com. Website: leave blank.
- **Steps:** Scroll to the comment form, fill the comment, name and email, do not tick 'save my name' or any newsletter box, do not click Post Comment.
- **Rules:** Author-moderated; the text invites the author to drop the link.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
Jesse, good piece, and thank you for being clear that the Elite 300 and C2000 Gen 2 are 20 A-class and that the converter will start charging the house batteries. One addition your readers might want: the sub-$1,000 tier. In the 2 kWh class there are three units with a native TT-30 right now, all 2,400 W (so the same 20 A ceiling you describe): BLUETTI AC200L (2,048 Wh, 1,200 W solar input, 62 lb, $899), Anker SOLIX C2000 Gen 2 (2,048 Wh, 800 W solar, 41.7 lb, $899.99) and Renogy PowerStation 2000 (2,048 Wh, 1,200 W solar, 51.8 lb, $849). For a weekender running fridge on propane, pump, lights, furnace blower and coffee (about 1.2–1.5 kWh a day) that tier is a day and a half with no sun, and the converter point matters more because a 55 A converter can pull ~800 W out of a 2 kWh pack. I wrote it up with current prices at https://dealectric.com/best-2kwh-power-station-for-rv. Disclosure: I run dealectric.com, which earns a commission on some links. Feel free to drop the link if you would rather not have it in comments; the numbers stand on their own.
```

## T6. Correction email to Wild Oak Trail

- **Where:** mailto:customersupport@wildoaktrail.com (contact page: https://wildoaktrail.com/pages/contact-us)
- **Account:** None. Create a Gmail DRAFT (Gmail connector `create_draft`), never send.
- **Steps:** Draft to customersupport@wildoaktrail.com, subject 'Correction: Anker SOLIX C2000 Gen 2 does have a TT-30 outlet', body below. Leave it in Drafts.
- **Rules:** A factual correction; no link to our site.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
Hello, a small correction on your "Bluetti vs EcoFlow vs Anker: 2kWh Power Stations Compared" post. It says the Anker SOLIX C2000 Gen 2 "has four standard AC outlets but no dedicated 30A RV port" and marks "30A RV Outlet: No" in the table. The C2000 Gen 2 does have a native TT-30R. Anker's own product page (ankersolix.com/products/c2000-gen2, Specs) lists "AC Output (TT-30R): 120V~ 20A Max, 60Hz, 2400W Max", and the user guide (A1783) gives the same rating. The useful nuance is that it is a 20 A-class TT-30, like the AC200L's, since both are 2,400 W inverters. Since the post steers RV buyers to the AC200L specifically for the port, you may want to update it. Thanks for the otherwise careful comparison.
```

## T7. Correction comment on Outdoor Tech Lab

- **Where:** https://www.outdoortechlab.com/portable-power-station-rv-tested/
- **Account:** None (comment form). Name: Barry. Email: hello@dealectric.com. Website blank.
- **Steps:** Fill the comment form, do not submit.
- **Rules:** Correction only, no link.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
Two numbers to check. (1) The Jackery Explorer 2000 Plus is described as having a "True 30-amp outlet (NEMA TT-30)". Jackery rates that outlet at 25 A (the inverter is 3,000 W; 30 A at 120 V would be 3,600 W), so it is a TT-30 socket, not a 30 A supply. (2) The AC runtimes do not fit the battery sizes: a 15,000 BTU rooftop AC draws roughly 1,500–2,000 W running, so a 2,042 Wh pack gives about an hour, not "3-4 hours max" (the FAQ's own "1-1.5 hours" is the right order of magnitude). Same issue with the Delta 2 Max "2 hours" and the F3800 running two ACs for "4-5 hours" on 3,840 Wh. Happy to be corrected if these were measured with solar input, but then the input wattage should be stated.
```

## T8. Correction comment on kayakcambria

- **Where:** https://kayakcambria.com/best-portable-power-stations-for-rvs/
- **Account:** None (comment form). Name: Barry. Email: hello@dealectric.com. Website blank.
- **Steps:** Fill the comment form, do not submit.
- **Rules:** Correction only, no link.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
One caveat readers need on the AC200L and Elite 300 entries: both have a TT-30 socket, but both are 2,400 W inverters, so the socket delivers about 20 A, not the 30 A (3,600 W) a pedestal gives. "Ran the entire rig" is true only within that 20 A budget, which excludes the rooftop AC for more than about an hour on 2 kWh. Also note the Elite 300's "12V/30A" is a DC output, not a 30 A AC rating. BLUETTI's spec pages list the AC side at 2,400 W total for both.
```

## T9. Correction note to campingsolar.us (if a contact path exists)

- **Where:** https://www.campingsolar.us/bluetti-ac200l-portable-power-station-review/
- **Account:** None. Look for a comment form or contact page; if neither exists, mark the task 'no contact path' and move on.
- **Steps:** If a contact form exists, fill it (name Barry, email hello@dealectric.com, the text below); do not submit. If only an email address, create a Gmail draft instead.
- **Rules:** Correction only, no link.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
Your AC200L review answers "Can the BLUETTI AC200L run a 13,500 BTU RV Air Conditioner?" with "Yes… 1.5 to 2 hours continuously." Two corrections: a 13,500 BTU rooftop unit needs roughly 2,800–3,500 W to start, above the AC200L's 2,400 W continuous and at the edge of its 3,600 W Power Lifting mode (which is for resistive loads, not motors), so it generally needs a soft starter (brings the surge to ~2,000 W). Running draw is 1,300–1,900 W, so 2,048 Wh is about one hour, not 1.5–2.
```
