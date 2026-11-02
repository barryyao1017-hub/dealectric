# Promote, tier 3: instruction set for /best-power-bank-for-steam-deck (FC41 run, 2026-11-02)

Source: growth/focus/fastloop-runs/fc41-steamdeck/outreach.md (research and reasons). Executed by a subagent up to the last click; Barry reviews each filled form in the agent's Chrome (port 9222) and clicks Submit himself.

## Rules for whoever runs this

- Use only the agent's Chrome on localhost:9222 (CDP). Never Barry's personal Chrome, never another debug port.
- **Never click the final Submit / Post / Send / Post Comment.** Stop with the form filled and leave the tab open.
- **Never create an account.** None of these tasks needs one. If a form unexpectedly demands a login, stop that task and report.
- Never type passwords or codes. Name and email fields: name `Barry`, email `barrryyao@gmail.com`, website field left empty (the link is in the text).
- Paste the text exactly; don't add links, signatures or marketing. If the page now shows comments that already give the same numbers, or the comment form is closed, skip and report.
- Tick no "subscribe", "save my name" or newsletter boxes.
- Take one screenshot of each filled form (scratchpad), and leave the tab open with a recognizable title.
- These are no-account WordPress comment forms and contact forms: a comment with a link is usually held for moderation, which is fine.

## Not in this set

- Steam Community threads (stale, Steam bans commercial content; outreach.md rows 5-7).
- Reddit, Quora, ResetEra, Lemmy: blocked for our tools; Barry's manual list is outreach.md section 5.

## T1. Comment on GeekChamp "5 Best Portable Chargers for Steam Deck and Other Handheld Consoles"

- **Where:** https://geekchamp.com/5-best-portable-chargers-for-steam-deck-and-other-handheld-consoles-us/
- **Account:** none (comment form: name, email, website).
- **Steps:** Open the article, scroll to "Leave a Reply" / the comment form, paste the text into the comment box, fill name and email as above, do not click "Post Comment".
- **Stop before:** the final submit click.

**Text to paste:**

```text
Useful table. Two gaps a Deck owner will hit right away:

1. How many charges a bank actually gives. You're right that "two full charges" claims are unreliable, but the arithmetic is simple enough to state: a 25,000 mAh bank is 91 Wh at the cells' 3.7 V, and about 85% of that reaches the device after conversion, so roughly 77 Wh. Against the OLED's 50 Wh battery that is about 1.5 charges, against the LCD's 40 Wh about 1.9. In play time, at the 15–25 W a demanding game draws, that's 3–5 extra hours. A 20,000 mAh bank (73–74 Wh) is about 1.2 OLED charges.

2. The Baseus EnerFill FC41's weight: Baseus lists it as about 517 g, so it sits between the INIU 20K (324 g) and the Anker 737 (630 g). Its 140 W is on the built-in USB-C cable, and the list price is $79.99, but Baseus's code FC41 takes it to $46.99 (it passed in Baseus's cart on 2 Nov), which puts it at INIU-20K money with 25% more capacity and no cable to carry. 91 Wh is also under the 100 Wh carry-on line.

I keep the charges-per-handheld math (Deck, Ally, Ally X, Legion Go, Switch 2) and the code status here: https://dealectric.com/best-power-bank-for-steam-deck
I run dealectric.com, which earns a commission on some links.
```

## T2. Comment on GamingOnBatteries "Best Power Banks for Steam Deck in October 2026"

- **Where:** https://gamingonbatteries.com/best-power-bank-steam-deck/
- **Account:** none (comment/review form). If the form is a star-rating "review" form that forces a rating, stop and report instead of rating.
- **Steps:** Open the article, scroll to the comment section ("Be the first to review" / "Leave a comment"), paste the text, fill name and email, do not click submit.
- **Stop before:** the final submit click.

**Text to paste:**

```text
The hours-of-play framing is the right one; here's the charge-count version, since most people think in "how many refills". Rated mAh is at 3.7 V, so 20,000 mAh = 74 Wh and 25,000 mAh = 91 Wh, and about 85% of that arrives at the Deck. That's roughly 1.2 OLED charges (50 Wh) from a 20K bank and 1.5 from a 25K bank, or 1.5 and 1.9 LCD charges (40 Wh). Your 2.75–3 h figure for a 20K bank matches a ~22 W draw, which is about right for a demanding game.

One bank worth adding to the compare: the Baseus EnerFill FC41, 25,000 mAh (91 Wh, so still carry-on legal), two built-in USB-C cables with 140 W on one of them, about 517 g (lighter than the 737 and the Anker 25K). It lists at $79.99 but Baseus's code FC41 made it $46.99 in their cart on 2 Nov 2026, the same price as the INIU 20K 65 W. The 45 W rule you give is the key one: anything under that only slows the drain while playing.

Charges per handheld (Deck OLED/LCD, ROG Ally and Ally X, Legion Go and Go 2, Switch 2) and the code's daily cart test are here: https://dealectric.com/best-power-bank-for-steam-deck
I run dealectric.com, which earns a commission on some links.
```

## T3. Correction note to fone.tips (contact form)

- **Where:** fone.tips contact page (find "Contact" in the site footer of https://fone.tips/best-power-bank-for-steam-deck/).
- **Account:** none. Name `Barry`, email `barrryyao@gmail.com`, subject as below.
- **Steps:** Open the contact form, fill subject and message, do not click "Send". If the only contact route is an email address (no form), create nothing and report the address.
- **Stop before:** the final send click.

**Subject:** Two figures in your Steam Deck power bank guide

**Text to paste:**

```text
Hi, a reader note on https://fone.tips/best-power-bank-for-steam-deck/ (updated Aug 8, 2026). Two numbers are off:

- The Anker Laptop Power Bank 25K is 90 Wh by Anker's own spec (25,000 mAh at 3.6 V), not "about 96 Wh". 96 Wh would be 26,700 mAh.
- It does not refill a 50 Wh Steam Deck OLED "nearly twice". After conversion losses about 85% of 90 Wh reaches the Deck, roughly 76 Wh, which is about 1.5 OLED charges or 1.9 LCD (40 Wh) charges.

The piece also doesn't say whether a bank charges the Deck while gaming: Valve rates the input at 45 W, so a 45 W bank does that at full speed; a 20–30 W bank only slows the drain.

If it helps, my comparison with the per-handheld charge math (Deck, Ally, Legion Go, Switch 2) is at https://dealectric.com/best-power-bank-for-steam-deck
I run dealectric.com, which earns a commission on some links.
```

## T4. Correction note to Geared Gaming (contact form)

- **Where:** Geared Gaming contact page (footer of https://gearedgaming.com/handhelds/best-steam-deck-power-bank).
- **Account:** none. Name `Barry`, email `barrryyao@gmail.com`.
- **Steps:** as T3.
- **Stop before:** the final send click.

**Subject:** Airline-limit and charge-count errors in your Steam Deck power bank page

**Text to paste:**

```text
Hi, on https://gearedgaming.com/handhelds/best-steam-deck-power-bank (updated July 30, 2026):

- The Anker 737 (24,000 mAh, 86.4 Wh) and the INIU 25,000 mAh (92.5 Wh) are both under the 100 Wh carry-on limit, not "near or past" it. Every bank on your list is carry-on legal without airline approval; 101–160 Wh is the band that needs approval.
- A 25,000 mAh bank is not "about two charges" of a Steam Deck OLED. 25,000 mAh is 90–92 Wh; about 85% reaches the Deck (~77 Wh); the OLED battery is 50 Wh, so about 1.5 charges (1.9 for the 40 Wh LCD).

Printing the Wh next to each bank would fix both at once. My own table with Wh, weight and per-handheld charges is at https://dealectric.com/best-power-bank-for-steam-deck
I run dealectric.com, which earns a commission on some links.
```
