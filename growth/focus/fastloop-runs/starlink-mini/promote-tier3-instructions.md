# Promote, tier 3: instruction set for /starlink-mini-usb-c-power-requirements (G09, 2026-11-02)

Source: growth/focus/fastloop-runs/starlink-mini/outreach.md (research and reasons). Executed by a subagent up to the last click; Barry reviews each filled form in the agent's Chrome (port 9222) and clicks Submit himself.

Edits to the research drafts: unverified figures removed (the USB-C cable's $33 price, the kit brick's 30 V); Starlink's wording paraphrased rather than quoted. The correction notes in outreach.md section 3 are not in this set (all four blogs are older than 60 days).

## Rules for whoever runs this

- Use only the agent's Chrome on localhost:9222 (CDP). Never Barry's personal Chrome, never another debug port.
- **Never click the final Submit / Post reply / Post / Answer.** Stop with the form filled and leave the tab open.
- **Never create an account.** RV LIFE forums (Thor Forums, iRV2, Forest River, …) share one RV LIFE account (barrryyao). agent-vault holds it as the forestriverforums.com login: navigate to the forum's own login page, call `login` with that account; on `origin_mismatch` for a page that is plainly the RV LIFE / that forum's own login, call `add_site_domain` (Barry approves the domain in a desktop dialog) and retry once; if he declines or it still fails, stop the task and report.
- Quora: "Continue with Google" as barrryyao@gmail.com (CLAUDE.md); if Google asks for a password, use agent-vault's google.com login. Never type credentials. If Quora asks to create a profile or accept terms, stop and report.
- Paste the text exactly. Before pasting, re-read the thread's newest posts; if someone has since given the same numbers, or the thread is locked, skip and report.
- One screenshot of each filled form (scratchpad); leave the tab open with a recognizable title.
- **RV LIFE link rule:** RV LIFE forums forbid links to sites the poster profits from, and one account covers all of them, so a ban would hit every RV LIFE forum. Barry chose on 11-01 to link there anyway; each text answers fully without its last paragraph, so he can delete it before posting.

## T1. Reply on Thor Forums "Starlink Mini Power Options for Dry Camping" (page 21; RV LIFE link rule applies)

- **Where:** https://www.thorforums.com/threads/starlink-mini-power-options-for-dry-camping.2211055/page-21 (go to the last page)
- **Account:** RV LIFE (see Rules).
- **Steps:** Open the last page, read posts after Oct 23, paste into the reply editor, do not click "Post reply".
- **Stop before:** the final submit click.

```text
16ACE27, your 3 hours is the math working, not luck: an 18 V 4 Ah pack is 72 Wh, the Mini draws about 20–25 W once it's locked on (Starlink says 20–40 W, 15 W idle; the app will show you), and a converter loses roughly 15%, so 72 × 0.85 ÷ 22 W ≈ 2.8 hours. A 6 Ah pack gets you about 4 hours, a 9 Ah about 6.

The part the tool-battery route can't fix is Chateau_Nomad's point: there is no low-voltage cutoff, so you are the BMS. For an afternoon that's fine; for a day it isn't.

If you want "a day" from one box, size it from the draw, not from the box's wattage: 24 h × 20 W ≈ 0.5 kWh at the low end, 1 kWh if you plan on Starlink's 40 W figure (snow melt, trees, cold). Two sizes make sense:
- A workday (8–10 h): ~300 Wh. EcoFlow RIVER 3 Plus (286 Wh, $299) or BLUETTI Elite 30 V2 (288 Wh, ~$275). Someone in the iRV2 thread this week gets ~14 h from an Anker SOLIX C300 DC (288 Wh), which matches a 17–20 W real-world draw.
- All day and night: ~1 kWh. ALLPOWERS P1800 (1,024 Wh LiFePO4, two USB-C ports up to 140 W, ~$395–439), Anker SOLIX C1000 Gen 2 ($499.99) or BLUETTI Elite 100 V2 ($499), all 1,024 Wh: about 22–43 h of Mini.

One rule if you power it from a USB-C port instead of the 12 V jack: Starlink's support article says the source must be rated 100 W (20 V at 5 A) and that the Mini won't run on a 65 W supply or anything from 66 to 99 W, even though it only draws 20–40 W. That is why the "30 to 60 W" figures earlier in this thread don't translate: check the USB-C port's own PD rating, and use Starlink's own USB-C cable (a separate accessory; a bank's built-in cables won't do). Also don't charge a phone on the bank's other port while the Mini runs; some banks drop the 20 V profile when a second port wakes up and the Mini reboots.

Hours ≈ battery Wh × 0.85 ÷ watts, if you want to size your own.

I keep the table (watt-hours, USB-C port ratings, hours, prices) at https://dealectric.com/starlink-mini-usb-c-power-requirements. Disclosure: I run dealectric.com, which earns a commission on some links there (the ALLPOWERS and BLUETTI rows); the Anker and EcoFlow rows are plain comparisons.
```

## T2. Reply on iRV2 "looking at a starlink Mini" (RV LIFE link rule applies)

- **Where:** https://www.irv2.com/threads/looking-at-a-starlink-mini.2220262/ (last page)
- **Account:** RV LIFE (see Rules).
- **Steps:** as T1.
- **Stop before:** the final submit click.

```text
Stircrazy, the DC-DC converter 92landyacht pointed you at is the right cheap fix for the camper, and here's why your USB-C outlets didn't work, so you don't buy another one that won't: Starlink's support article says a USB-C source has to be rated 100 W (20 V at 5 A) for the Mini; it won't run from a 65 W port or anything from 66 to 99 W, even though the dish only draws 20–40 W (about 20–24 W in practice, as Fpmtngal saw on the app). Camper USB-C outlets are typically 18–45 W, and the USB-C route also needs Starlink's own USB-C cable.

The 400 W inverter will work but costs you its own idle draw (typically 5–10 W, a quarter to a half of what the Mini uses) plus the brick's losses, so on battery you'll get maybe two-thirds of the hours the converter gives you.

If you'd rather have one box that works in the Bronco, the F-350 and the camper without wiring, a small power station with a real 100 W+ USB-C port does it: 1blue78's Anker SOLIX C300 DC (288 Wh) at ~14 h is typical of the 288 Wh class (EcoFlow RIVER 3 Plus $299, BLUETTI Elite 30 V2 ~$275); a 1,024 Wh unit (ALLPOWERS P1800 ~$395–439, Anker C1000 Gen 2 or BLUETTI Elite 100 V2 at $499) runs the Mini a day and a night. Rule of thumb: hours ≈ Wh × 0.85 ÷ 20–40 W.

I keep the comparison at https://dealectric.com/starlink-mini-usb-c-power-requirements. Disclosure: I run dealectric.com, which earns a commission on some links there.
```

## T3. Quora answer: "What do you use to power a Starlink Mini for Wi-Fi?" (link allowed with disclosure)

- **Where:** https://www.quora.com/What-do-you-use-to-power-a-Starlink-Mini-for-Wi-Fi
- **Account:** Google sign-in (see Rules).
- **Steps:** Click "Answer", paste, do not click "Post".

```text
Three things work, and one common thing doesn't.

Wall power. The kit's own power supply plus the 15 m cable. Nothing to size.

12–48 V DC. The Mini accepts 12–48 V DC, so a car socket adapter (Starlink sells one), a DC-DC converter wired to an RV battery, or an 18/20 V tool-battery adapter all run it. A 4 Ah Ryobi/DeWalt pack (72 Wh) gives about 3 hours; it has no low-voltage cutoff, so don't leave it on overnight.

USB-C PD, with one hard rule. Starlink's support article: use a USB Power Delivery source rated 100 W (20 V at 5 A); the Mini won't run on a 65 W supply or anything from 66 to 99 W. It only draws 20–40 W (15 W idle), but the source must offer the 20 V / 5 A profile. So a phone bank, a 65 W laptop bank, or a car's USB-C port won't start it, and some 100 W+ banks drop the profile when you charge a phone on another port and the Mini reboots. You also need Starlink's own USB-C cable (a separate 5 m accessory); a bank's built-in cables won't do.

How long: hours ≈ battery Wh × 0.85 ÷ watts. A 99 Wh carry-on bank with a 100 W port: about 2–4 hours. A 288 Wh station (EcoFlow RIVER 3 Plus, BLUETTI Elite 30 V2, Anker SOLIX C300): a workday, 6–14 hours depending on draw. A 1,024 Wh station (ALLPOWERS P1800, Anker SOLIX C1000 Gen 2, BLUETTI Elite 100 V2; $395–500 in Nov 2026): about 22–43 hours, a full day and night. That last class is what "all day" actually takes.

I keep the comparison (watt-hours, which USB-C ports qualify, hours, prices) at https://dealectric.com/starlink-mini-usb-c-power-requirements. Disclosure: I run dealectric.com, which earns a commission on some links there.
```

## T4. Quora answer: "Has anyone tried powering the Starlink Mini dish with a 10,000mAh portable battery?"

- **Where:** https://www.quora.com/Has-anyone-tried-powering-the-Starlink-Mini-dish-with-a-10-000mAh-portable-battery-If-so-how-long-does-it-last
- **Account / steps:** as T3.

```text
It almost certainly won't start, and the reason isn't capacity. Starlink's support article says the Mini needs a USB Power Delivery source rated 100 W (20 V at 5 A) and won't run on anything rated below 100 W, 65 W included. A 10,000 mAh phone bank is a 20–30 W device without the 20 V / 5 A profile, so the dish never boots. (It also needs Starlink's own USB-C cable, a separate accessory.)

If it did run, the capacity answer is short: 10,000 mAh at 3.7 V is 37 Wh, the Mini draws 20–40 W (15 W idle), and a converter loses ~15%, so 37 × 0.85 ÷ 25 ≈ 1.3 hours. Sizes that make sense: a 99 Wh bank with a genuine 100 W USB-C port (the biggest you can fly with) gives about 2–4 hours; a 288 Wh power station a workday; a 1,024 Wh station (ALLPOWERS P1800, Anker SOLIX C1000 Gen 2, BLUETTI Elite 100 V2, $395–500) about 22–43 hours.

Comparison with the hours table and which ports qualify: https://dealectric.com/starlink-mini-usb-c-power-requirements. Disclosure: I run dealectric.com, which earns a commission on some links there.
```

## Not executed (text kept for Barry)

- Rokslide "Starlink power" (Aug 11, outside Tier B; no account; Rokslide bans commercial links): draft 2e in outreach.md, post link-free if at all.
- Reddit, Facebook groups, DIY Solar search, Rivian Forums: manual list in outreach.md section 5.
