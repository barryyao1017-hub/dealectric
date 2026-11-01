# Promote, tier 3: instruction set for /iphone-17-25w-wireless-charger (ESR run, 2026-11-01)

Source: growth/focus/fastloop-runs/esr-25w/outreach.md (research and reasons). Executed by a subagent up to the last click; Barry reviews each filled form in the agent's Chrome (port 9222) and clicks Submit himself.

## Rules for whoever runs this

- Use only the agent's Chrome on localhost:9222 (CDP). Never Barry's personal Chrome, never another debug port.
- **Never click the final Submit / Post / Send / Answer.** Stop with the form filled and leave the tab open. Gmail: create a draft, never send.
- **Never create an account.** If a task needs a login, check agent-vault `list_accounts` and log in through `login` only if an account for that site exists. If none exists, open the site's sign-up page in the agent's Chrome and leave it for Barry (fill nothing there, click nothing), then move on: account creation is Barry's step.
- Never type credentials or codes; agent-vault fills them.
- Paste the text exactly; don't add links, signatures or marketing. If the page shows the question was already answered the same way, or the thread is locked, skip and report.
- Before filling, re-read the thread's last posts; if something new changes the answer (for example a maker publishing an iPhone Duo compatibility list), report it instead of pasting.
- Take one screenshot of each filled form for Barry (scratchpad), and leave the tab open with a recognizable title.
- Log any touch of dealectric.com with evallib.footprint (the project hook logs browser touches).
- MacRumors specific: the rules allow established members to link their own site when it answers a specific question, and treat self-links from new accounts as advertising. If the MacRumors account is new (under ~20 posts), paste the text **without its final paragraph** (the dealectric link and disclosure) and say so in the report; Barry decides.

## Not in this set

- Reddit: blocked for every tool we have; Barry runs the searches in outreach.md section 5 and decides.
- Apple Community: every thread on the topic is closed by the system; nothing can be posted.
- AppleInsider forums: Cloudflare-blocked for our tools; Barry may read discussion/243545 by hand.
- Amazon Q&A for the ESR Cyclone pad: not researched; the browser pane's Amazon session is signed in as Barry, so no agent action there.

## T1. Reply on MacRumors: "Recommended 3in1 charger compatible with the iPhone Duo please!"

- **Where:** https://forums.macrumors.com/threads/recommended-3in1-charger-compatible-with-the-iphone-duo-please.2491721/
- **Account:** MacRumors forum account. Check agent-vault `list_accounts` for forums.macrumors.com; if none, open https://forums.macrumors.com/register/ in the agent's Chrome and STOP this task (account creation is Barry's step).
- **Steps:** Open the thread, confirm it still has only the two posts (StuartMoore 10-14, captain poopers 10-14); scroll to the reply editor at the bottom, paste the text, do not click "Post reply".
- **Rules:** MacRumors: self-promotional links from new accounts are treated as advertising (see Rules above). The text answers fully without its last paragraph.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
Stuart, the reason the Satechi feels slow is the number on the pad, not the phone: Satechi's 3-in-1s are 7.5–15 W pads, and the Duo is a 25 W MagSafe / Qi2 25 W phone (same as the 18 Pro), so you are leaving 40% on the table. Two things to look for in the replacement:

1. **"Qi2.2" or "Qi2 25W" on the iPhone pad.** Anything labelled plain Qi2 or MagSafe-compatible without a wattage is a 15 W pad, and the Duo will sit at 15 W on it no matter what brick you use.
2. **A big enough brick in the box.** A 25 W pad needs a 30 W-or-higher USB-C PD supply on its own; a 3-in-1 that is also running a Watch and AirPods ships with 40–50 W. If a 3-in-1 comes with no brick, budget for one.

The 3-in-1 stands that actually do 25 W to the phone right now: ESR CryoBoost 3-in-1 Qi2.2 ($109.99, 50 W brick included, has a small fan), Belkin UltraCharge Pro 3-in-1 ($129.99, 45 W brick, fan), Anker Prime 3-in-1 ($149.99 list, 45 W, fan), UGREEN MagFlow 3-in-1 ($139.99 list, often ~$90, 45 W, no fan), mophie 3-in-1 Qi2.2 ($149.95, 40 W, no fan). For an Ultra you want the ones with the Apple fast-charge Watch module (ESR, Belkin and Anker list it); a plain Watch puck is noticeably slower on the Ultra battery. The fan matters more than it sounds: at 25 W the phone warms up and iOS slows or holds charging above 80% until it cools, which is why some people see "fast" chargers finish no sooner than the old 15 W one. Macworld clocked ESR's 25 W stand at 0–50% in just over 30 minutes against about 45 minutes on ESR's 15 W stand.

One honest caveat for the Duo: none of these makers list the Duo in their compatibility tables yet (they were specced for the 16/17), so check the hinge and camera-plateau clearance on the stand you pick; in the other Duo thread here someone reports Belkin's 25 W stand holds a Duo fine in phone mode.

I keep the numbers (which iPhones get 25 W, the adapter rule, the model-number check for Apple's old 15 W puck) on a page I maintain: https://dealectric.com/iphone-17-25w-wireless-charger. Disclosure: I run dealectric.com, which earns a commission on some links there (the ESR ones); the Belkin, Anker, UGREEN and Apple rows are plain comparisons.
```

## T2. Reply on MacRumors: "Any Thoughts on a DUO Charging stand?"

- **Where:** https://forums.macrumors.com/threads/any-thoughts-on-a-duo-charging-stand.2492657/
- **Account:** Same as T1.
- **Steps:** Open the thread, re-read posts after dcpmark's 10-29 post; if a Duo-specific 25 W stand has since been posted with specs, report instead of pasting. Otherwise paste into the reply editor, do not click "Post reply".
- **Rules:** Same as T1.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
chrisjj625, on "best options to utilize charging abilities": the Duo is a 25 W MagSafe / Qi2 25 W phone, so the filter is simple. The stand's iPhone pad must say Qi2.2 or Qi2 25W (plain Qi2 and MagSafe-compatible stands are 15 W), and it must be fed by a 30 W-or-higher USB-C PD brick (a 20 W phone brick holds a 25 W pad at about 15 W). The Belkin 25 W stand Macalicious2011 mentioned is exactly that class and ships with its 45 W brick, which is why it works. Apple's own MagSafe Charger also does 25 W, but only the 2024-or-later puck (A2580/A3250/A3502/A3503, printed on the cable; the 2020 A2140 is 15 W), and it comes with no brick, so add Apple's 30 W one.

If you charge while using the phone, consider one with a fan: at 25 W the phone gets warm and iOS slows or pauses charging above 80% until it cools. ESR's Cyclone pad ($43.99, fold-out stand, fan, needs a 35 W brick you supply) and the fan 3-in-1s from ESR, Belkin and Anker are the ones built for that. Same caveat as above: nobody lists the Duo officially yet, so check the fit.

Page with the table and the adapter/model-number checks: https://dealectric.com/iphone-17-25w-wireless-charger. Disclosure: I run dealectric.com, which earns a commission on some links there (ESR); the others are plain links.
```

## T3. Answer on Best Buy Q&A: UGREEN MagFlow Qi2.2 25W pad

- **Where:** https://www.bestbuy.com/site/questions/ugreen-magflow-qi2-2-25w-wireless-charger-magsafe-compatible-charging-pad-for-iphone-16-17-series-black-blue/6644431 — the question by Tony: "To get the 25w charging speed. Does it come with a car charger or a power brick?"
- **Account:** Best Buy account. Check agent-vault `list_accounts` for bestbuy.com; if none, open https://www.bestbuy.com/identity/signin in the agent's Chrome and STOP this task.
- **Steps:** Open the Q&A page, find Tony's question (last on page 1), click "Answer this question", paste the text, do not click Submit.
- **Rules:** Best Buy answers are customer posts; links are usually stripped. Paste the text as given anyway (Barry's rule); if the form rejects the URL, remove only the last two sentences and report.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
No brick in the box, and the brick is what decides whether you get 25 W. This pad needs a USB-C Power Delivery adapter of 30 W or more (the 15 V profile); on a 20 W phone brick it settles at about 15 W, and on a 5 W/12 W USB-A brick lower still. Also only some iPhones take 25 W from it: iPhone 17, 17 Pro, 17 Pro Max, the 18 series and the 16 Plus/16 Pro Max (on iOS 26). The iPhone Air peaks at 20 W, the 16 and 16 Pro at 22.5 W, the 17e and iPhone 12–15 at 15 W. Expect it to slow above 80% when the phone is warm; that is iOS protecting the battery, not the pad. I keep a comparison of the 25 W pads and stands with the adapter rule at https://dealectric.com/iphone-17-25w-wireless-charger. Disclosure: I run dealectric.com, which earns a commission on some links there (not on this UGREEN pad).
```

## T4. Reply on MacRumors: "Can someone outline the new charging speeds to me pls?" (optional, 13-month-old thread)

- **Where:** https://forums.macrumors.com/threads/can-someone-outline-the-new-charging-speeds-to-me-pls.2465580/
- **Account:** Same as T1.
- **Steps:** Open the thread (page 1, mavere's post #9 is the one being answered); paste into the reply editor at the end; do not click "Post reply". If the thread shows as locked, skip and report.
- **Rules:** Same as T1. Reviving an old thread is allowed on MacRumors but may read as promotion; Barry decides.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
Late answer to mavere's "I guess my old MagSafe chargers need to be replaced in order for that to work?": yes if they are the 2020 puck. Apple's first MagSafe Charger (model A2140, printed on the cable) is a 15 W charger and stays 15 W on a 17 Pro whatever brick you plug it into. The 25 W pucks are A2580 / A3250 (2024) and A3502 / A3503 (2025); Settings > General > About shows the model when one is attached. Any Qi2.2 ("Qi2 25W") pad from Belkin, UGREEN, ESR, Anker etc. also does 25 W on the 17/17 Pro/17 Pro Max since iOS 26, while plain Qi2 pads are 15 W and plain Qi 7.5 W. Whichever you buy, it needs a 30 W-or-higher USB-C brick; a 20 W one holds it at 15 W. And 25 W is a peak: the phone warms up and iOS slows or holds charging above 80% until it cools, which is why the fan-cooled pads (ESR, Belkin, Anker) finish earlier in practice. I wrote the table up here: https://dealectric.com/iphone-17-25w-wireless-charger. Disclosure: I run dealectric.com, which earns a commission on some links there.
```

## T5. Reply on MacRumors: "Best wireless charger?!" (optional, 12-month-old thread)

- **Where:** https://forums.macrumors.com/threads/best-wireless-charger.2469429/
- **Account:** Same as T1.
- **Steps:** Same as T4.
- **Rules:** Same as T4.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
Pete, for a 17 Pro the only thing that separates "best" from the rest is 25 W vs 15 W. Any charger marked Qi2.2 / Qi2 25W (or Apple's own 2024-or-later MagSafe puck, A2580/A3250/A3502/A3503 on the cable; the 2020 A2140 is 15 W) gives the 17 Pro 25 W, provided it is on a 30 W-or-higher USB-C brick. Plain Qi2 and "MagSafe-compatible" pads are 15 W. Apple's puck is $39 plus $49 for Apple's 30 W brick; UGREEN's MagFlow Qi2.2 pad is about $26 at Best Buy (no brick); ESR's Cyclone pad is $43.99 and adds a fan, which matters because the phone warms up at 25 W and iOS slows charging above 80% until it cools. Comparison with the adapter rule: https://dealectric.com/iphone-17-25w-wireless-charger. Disclosure: I run dealectric.com, which earns a commission on some links there (ESR).
```

## T6. Answer on Quora: "Can you use a 25W charger on an iPhone?" (optional)

- **Where:** https://www.quora.com/Can-you-use-a-25W-charger-on-an-iPhone
- **Account:** Quora, signed in with Google as barrryyao@gmail.com (Barry, 2026-11-01): when Quora offers "Continue with Google", choose barrryyao and continue.
- **Steps:** Open the question, click Answer, paste the text into the editor (keep the two bold lead-ins as bold if the editor allows; otherwise plain), do not click Post.
- **Rules:** Quora: affiliate links banned in answers; a self-promotional link is allowed as part of a full answer with the affiliation disclosed. The link is to our page, not an affiliate URL, and the disclosure is in the text.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
Yes, and since 2024 "25W" means two different things for an iPhone, so it is worth separating them.

Wired 25 W USB-C brick: every iPhone from the 8 onward charges from it; the phone draws what it can use (about 20 W for iPhone 12–15, up to 27 W for the 15 Pro, up to 40 W for the 17 Pro/Pro Max with a USB-PD adapter of 40 W or more). A 25 W brick is never too much, because the phone sets the current.

25 W wireless (MagSafe / Qi2.2): iPhone 17, 17 Pro and 17 Pro Max, the 18 series, and the 16 Plus / 16 Pro Max charge wirelessly at up to 25 W, but only from a Qi2.2 ("Qi2 25W") charger or Apple's 2024-or-later MagSafe Charger (models A2580, A3250, A3502, A3503; the 2020 A2140 is a 15 W charger and a bigger brick does not change that), and only when that charger is fed by a 30 W-or-higher USB-C adapter. On a 20 W adapter it drops to about 15 W. The iPhone Air peaks at 20 W, the 16 and 16 Pro at 22.5 W, the 17e and iPhone 12–15 at 15 W. At 25 W the phone gets warm and iOS slows or pauses charging above 80% until it cools, which is the reason fan-cooled pads (ESR, Belkin, Anker) exist.

I keep a comparison of the 25 W chargers with current prices here: https://dealectric.com/iphone-17-25w-wireless-charger. Disclosure: I run dealectric.com, which earns a commission on some links there.
```

## T7. Correction note to Smartish (optional: article is from May 2026, rank unverified)

- **Where:** Smartish contact page. Find it from https://smartish.com (footer "Contact" link; URL not verified this run). If only an email address is shown, create a Gmail DRAFT (Gmail connector `create_draft`) to it instead; never send.
- **Account:** None.
- **Steps:** Fill the contact form (name Barry, email hello@dealectric.com, subject "Correction: iPhone 17 MagSafe is 25W, not 15W", the text below); do not submit.
- **Rules:** A factual correction; no link to our site.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
Hello, one correction on "iPhone MagSafe vs USB-C Speed: The 2026 Guide You Need" (May 8, 2026). It says MagSafe "hits 15 watts max with Apple's gear" and, in the FAQ, that an iPhone 17 reaches "a peak of 15 watts" on MagSafe. Apple's iPhone 17 tech specs list MagSafe and Qi2 wireless charging up to 25 W with a 30 W-or-higher adapter (the 16 Plus/16 Pro Max too; the Air is 20 W, the 17e 15 W), and Apple's 2024-or-later MagSafe Charger (A2580/A3250/A3502/A3503) delivers it; only the 2020 A2140 puck is 15 W. Your own October post on the 18 Pro has the 25 W figure, so the May guide now contradicts it. Also "third-party options usually cap at 7.5 watts" is out of date: Qi2 pads are 15 W and Qi2.2 pads 25 W. Thanks for the otherwise useful guide.
```

## T8. Correction note to iphoneipadreview.com (optional, low-authority site)

- **Where:** https://iphoneipadreview.com/best-wireless-charger-for-iphone-17/ — use the site's contact page if one exists (not verified); the page's own "Be the first to review" form is a rating form, not a comment box, so do not use it for the note.
- **Account:** None.
- **Steps:** If a contact form exists, fill it (name Barry, email hello@dealectric.com, the text below); do not submit. If none, mark "no contact path" and move on.
- **Rules:** Correction only, no link.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
Two things readers will trip on in "Best wireless charger for iPhone 17": the comparison table lists all four picks at 15W Qi2 while the headline pick and the intro promise 25W, and the article never says what an iPhone 17 needs for 25W (a Qi2.2 / "Qi2 25W" charger plus a 30W-or-higher USB-C adapter; a 15W Qi2 pad or a 20W brick keeps it at 15W). Apple's iPhone 17 tech specs and its support page on MagSafe charging speeds have the figures. Happy to point you to them.
```
