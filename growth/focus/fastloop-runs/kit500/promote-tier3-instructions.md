# Promote, tier 3: instruction set for /best-solar-generator-kit-under-500 (kit500 run, 2026-11-02)

Source: growth/focus/fastloop-runs/kit500/outreach.md (research and reasons). Executed by a subagent up to the last click; Barry reviews each filled form in the agent's Chrome (port 9222) and clicks Submit himself.

## Rules for whoever runs this

- Use only the agent's Chrome on localhost:9222 (CDP). Never Barry's personal Chrome, never another debug port.
- **Never click the final Submit / Post / Send / Answer.** Stop with the form filled and leave the tab open. Gmail: create a draft, never send.
- **Never create an account.** If a task needs a login, check agent-vault `list_accounts` and log in through `login` only if an account for that site exists. If none exists, open the site's sign-up page in the agent's Chrome and leave it for Barry (fill nothing there, click nothing), then move on: account creation is Barry's step.
- Never type credentials or codes; agent-vault fills them.
- Paste the text exactly; don't add links, signatures or marketing. If the page shows the question was already answered the same way, or the thread is locked, skip and report.
- Before filling, re-read the thread's last posts; if something new changes the answer (for example Anker or EcoFlow adding a US 100 W bundle under $500, or BLUETTI's kit price moving off $489.99), report it instead of pasting.
- Take one screenshot of each filled form for Barry (scratchpad), and leave the tab open with a recognizable title.
- Log any touch of dealectric.com with evallib.footprint (the project hook logs browser touches).
- Best Buy specific: answers are customer posts and the form usually strips or rejects URLs. Paste the text as given (Barry's rule); if the form rejects the URL, remove only the last two sentences (the dealectric link and the disclosure) and say so in the report.
- Blog comments (T3, T4) are moderated; paste the full text with the link and disclosure, and report that approval is the site owner's call.

## Not in this set

- Reddit and Facebook: blocked for every tool we have; Barry runs the searches in outreach.md section 5 and decides.
- Slickdeals threads (Elite 30 V2 10-06, DARAN 10-14): expired deals, the open question was answered in-thread, and Slickdeals bans self-promotional links.
- BLUETTI forum: behind BLUETTI's SSO login; no account in agent-vault. Quora: no sub-$500 kit question found.
- survivalistboards "What's the Best Portable Solar Kit?" (Google #2 for the main query): TollBit wall; Barry may read it by hand.
- Amazon Q&A: not researched; the browser pane's Amazon session is signed in as Barry, so no agent action there.

## T1. Answer on Best Buy Q&A: Anker SOLIX C300X, "are solar panels included?"

- **Where:** https://www.bestbuy.com/site/questions/anker-solix-c300x-portable-power-station-288wh90000mah-peak-600w-backup-battery-generator-for-campingtravel-emergencies-288-wh-capacity-black/6593888/question/50192aae-1897-3aab-ab11-2ec8d1ddeb0b (asked by BigAl on 2026-11-01, 0 answers when researched). If that URL fails, open the product's Q&A list https://www.bestbuy.com/site/questions/anker-solix-c300x-portable-power-station-90000mah-with-fast-charge-288-wh-capacity-black/6593888 and find the question on page 1.
- **Account:** Best Buy account. Check agent-vault `list_accounts` for bestbuy.com; if none, open https://www.bestbuy.com/identity/signin in the agent's Chrome and STOP this task (account creation is Barry's step).
- **Steps:** Open the question; confirm it still has no answer that covers the 100 W / 11–28 V input and the refill time (if Anker Team has answered with the specs, report and skip); click "Answer this question", paste the text, do not click Submit.
- **Rules:** Best Buy strips links (see Rules above). The answer stands without its last two sentences.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
No. This listing is the station on its own: the C300X and its AC charging cable, no solar panel and (on Anker's DC version at least) no solar cable, so budget for both if you want to charge from the sun. It takes any panel that fits its input: XT60 plug, 11–28 V, 100 W maximum. A 100 W folding panel is the right size; a bigger panel does not charge it any faster, and Anker's 60 W panel takes about twice as long. Anker quotes 194 minutes from a full 100 W, but a folding panel really delivers about 70–80 W in full sun, so plan on roughly 4 hours of good sun to refill the 288 Wh from empty with 100 W, 6–7 hours with 60 W, and a day or more in cloud. If you would rather have the panel in the box: Anker sells the C300X DC with its 60 W panel as a kit ($349.99 on Anker's store; that version has no AC outlet), and the only brand kit under $500 I have found in stock with a 100 W panel is BLUETTI's Elite 30 V2 + 100 W at $489.99 (same 288 Wh, 600 W AC). Jackery's Solar Generator 300 ($379) ships a 40 W panel. I keep the sub-$500 kits compared, with dated prices and how long each panel takes to refill the battery, at https://dealectric.com/best-solar-generator-kit-under-500. Disclosure: I run dealectric.com, which earns a commission on some links there (the BLUETTI one); the Anker and Jackery rows are plain links.
```

## T2. Answer on Best Buy Q&A: EcoFlow RIVER 3 Plus 268 Wh, "running a crockpot while camping"

- **Where:** https://www.bestbuy.com/site/questions/ecoflow-river-3-plus-268wh-portable-power-station-268-wh-capacity-black/6613626 — question 6 on page 1 (asked about 1 month before 2026-11-02; one answer from EcoFlow saying "up to 600 W, send us the wattage").
- **Account:** Same as T1.
- **Steps:** Open the Q&A list, find the crockpot question, confirm nobody has since given the runtime arithmetic or a panel answer; click "Answer this question", paste the text, do not click Submit.
- **Rules:** Same as T1.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
A slow cooker is one of the few kitchen loads a station this size handles: a 6-quart crockpot draws about 150–200 W on high and 70–120 W on low, well under this unit's 600 W. Runtime is the limit, not power. Count on about 85% of the 268 Wh reaching the plug, so roughly 1.5 hours on high or 2–3 hours on low from a full charge; an 8-hour recipe needs the station topped up while it cooks. In camp that means a panel. EcoFlow's answer above says its 110 W panel refills this in about 2 hours; a folding panel really gives 70–80% of its rating, so plan on 3.5–4 hours of full sun, and in good sun the panel about covers a crockpot on low. EcoFlow's US store sells the RIVER 3 Plus and the 110 W panel as two items ($279 + $259 on Nov 2), not as a bundle. If you have not bought yet and want the panel in the box for under $500, BLUETTI's Elite 30 V2 + 100 W kit ($489.99; 288 Wh, 600 W) is the one in-stock brand kit at this size. I keep the sub-$500 kits compared, with panel refill times and dated prices, at https://dealectric.com/best-solar-generator-kit-under-500. Disclosure: I run dealectric.com, which earns a commission on some links there (BLUETTI); the EcoFlow rows are plain links.
```

## T3. Comment on AllProGenerators blog: "Best Solar Generator Under 500: Budget Options and Sizing"

- **Where:** https://allprogenerators.com/blogs/news/best-solar-generator-under-500 (James Paul, Oct 15, 2026; Bing past-month #1 for "best portable power station with solar panel bundle under $500 2026 prices reviews"; 0 comments; Shopify comment form at the bottom: Name, Email, Message; "comments must be approved").
- **Account:** None (name Barry, email hello@dealectric.com).
- **Steps:** Scroll to "Leave a comment", fill Name and Email, paste the text into Message, do not click "Post comment". If the article now names a sub-$500 kit with a 100 W panel, report instead of pasting.
- **Rules:** Retailer's own blog, moderated; approval unlikely. Suggestion, not a correction.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
Useful sizing piece. One addition for readers who want the panel in the box: there is one brand kit under $500 in stock with a 100 W panel, BLUETTI's Elite 30 V2 + 100 W at $489.99 on BLUETTI's US store (288 Wh LiFePO4, 600 W inverter; the two parts cost $538.99 bought apart). The other small kits in stock ship a 40 W panel (Jackery Solar Generator 300, $379) or a 60 W panel with no AC outlet (Anker SOLIX C300X DC, $349.99), and the Jackery 500 V2 + SolarSaga 100 Air is $529 as you say. On the recharging section: a 100 W folding panel really delivers about 70–80 W in full sun, so it refills a 288 Wh station in roughly 4 hours and a 512 Wh one in about 7, a full sunny day. I keep the sub-$500 kits compared with dated prices at https://dealectric.com/best-solar-generator-kit-under-500. Disclosure: I run dealectric.com, which earns a commission on some links there (BLUETTI and ALLPOWERS); the Jackery and Anker rows are plain links.
```

## T4. Comment on backuppowerhub.com: "Best Budget Portable Power Stations Under $500: 7 Top Picks for 2026" (low priority)

- **Where:** https://backuppowerhub.com/?p=291 (Andrew Harrington; updated Sep 28, 2026; 0 comments; WordPress comment form, "comments are reviewed before they appear").
- **Account:** None (name Barry, email hello@dealectric.com, website field: leave empty).
- **Steps:** Scroll to the comment form, fill Name and Email, paste the text, do not click "Post Comment". If the article has since added a kit section, report instead.
- **Rules:** Moderated; suggestion, not a correction.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
None of the seven ships a solar panel, which is the first thing readers of a "solar generator" list ask. For the panel-in-the-box version of two of your picks: BLUETTI sells the Elite 30 V2 with a 100 W panel for $489.99 ($538.99 as parts), the only in-stock brand kit under $500 with a 100 W panel; Anker's C300X DC + 60 W kit is $349.99 but has no AC outlet. Worth a line on refill time too: a 100 W folding panel gives about 70–80 W in full sun, so the 288 Wh units take roughly 4 hours, not the 2–3 hours people infer from the rating. Dated comparison of the sub-$500 kits: https://dealectric.com/best-solar-generator-kit-under-500. Disclosure: I run dealectric.com, which earns a commission on some links there (BLUETTI, ALLPOWERS); the Anker, Jackery and EcoFlow rows are plain links.
```

## T5. Suggestion to thepowerstationguide.com (Google organic #1 for the main target query; optional)

- **Where:** https://thepowerstationguide.com/contact (footer "Technical Support" link; the form was not opened this run). The article is https://thepowerstationguide.com/blog/best-portable-power-stations-solar-bundles (Feb 17, 2026). If the contact page only shows an email address, create a Gmail DRAFT (Gmail connector `create_draft`) to it instead; never send.
- **Account:** None (name Barry, email hello@dealectric.com, subject "Your solar bundle guide: the one kit under $500").
- **Steps:** Open the contact page, fill the fields, paste the text, do not submit. If the bundle guide has since added a sub-$500 pick, report instead.
- **Rules:** Suggestion with the link and disclosure, per Barry's rule.
- **Stop before:** the final submit/post/send click.

**Text to paste:**

```text
Your bundle guide is the first organic result for "best portable solar generator kits under $500" and has no pick under $500. One exists: BLUETTI's Elite 30 V2 + 100 W kit, $489.99 on BLUETTI's US store (288 Wh LiFePO4, 600 W, 200 W solar input; $538.99 as parts). The other in-stock small kits ship a 40 W panel (Jackery Solar Generator 300, $379) or a 60 W panel on a DC-only station (Anker C300X DC, $349.99); EcoFlow sells no RIVER 3 Plus + 110 W bundle in the US; ALLPOWERS' P1800 + 200 W kit is $531 but ships from Dec 15. One number worth revisiting in your 300 Wh guide: a 100 W folding panel delivers about 70–80 W in full sun (Popular Mechanics measured 50–75%), so a 288 Wh station takes roughly 4 hours, not 3. I keep the kits with dated prices at https://dealectric.com/best-solar-generator-kit-under-500. Disclosure: I run dealectric.com, which earns a commission on some links there (BLUETTI, ALLPOWERS).
```
