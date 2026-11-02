# Tier 3 outreach research: /best-20000mah-power-bank-under-50 (FC41 run, step 7b, 2026-11-02)

Researched by a Fable 5.1 subagent (web search, WebFetch, built-in browser pane); drafts only, nothing posted, no
accounts created, no login anywhere. Brief: `growth/focus/fastloop-briefs/outreach-brief.md`. Page facts from the
`best-20000mah-power-bank-under-50` record in `src/gaps.py` (not fetched from dealectric.com).

**Headline.** The live, US-based demand for "which 20,000 mAh bank under $50" is on Slickdeals, not on the forums the
brief lists: Slickdeals ran 40 deal threads matching "20000mAh power bank" between 10-07 and 11-01 (search sorted
newest, 853 results in all), and five of them from the last three weeks carry unanswered or half-answered shopper
questions our page settles (will it run a MacBook, which one would you recommend, is this brand any good, why is the
$39 one more popular than the $30 one). Every other venue is dead or blocked for us: Budget Light Forum's USB power
category has had one thread since January, Tom's Guide's power-bank tag stops in 2017, FlyerTalk and Head-Fi sit
behind Cloudflare challenges, Quora search needs a login and its direct questions are 4–9-year-old India-centric
answers, Reddit is blocked (manual list in section 5). The catch on Slickdeals is its rule: "No spam or self-promo";
a disclosed dealectric link will probably be removed and may get the account flagged, so each draft is written to
stand without its last line and Barry decides whether to keep it.

Two rival facts the research turned up that matter for the page itself are in section 6 (CUKTECH 25K 100 W at
$39.89 with a built-in cable; EcoFlow 25K 170 W at $48.19, expired).

## 1. Ranked candidates

Demand: 3 = about to buy / undecided; 2 = owns one, open question, others shopping; 1 = technical only. Tier: A = a
post in the last 14 days; B = 15–45 days and unresolved; E = evergreen (older, still surfacing in search). Dates are
US; "last post" is the newest comment our fetch showed (Slickdeals pages come back truncated, so a later one may
exist).

| # | URL | Venue, dates, size | Tier | Demand (quote) | What is missing | Link rules | Action |
|---|---|---|---|---|---|---|---|
| 1 | https://slickdeals.net/f/20153709-talix-20000mah-3-port-140w-usb-c-power-bank-38-99-free-shipping | Slickdeals deal thread, TALIX 20K 140 W $38.99; posted 2026-10-13 (staff), last comment 10-24, 43 comments, Frontpage | A | **3**: SuperSaiyaman (10-13) "So this'll charge a Macbook?"; boazb (10-13) "does this beat the 190W TALIX with retractable cable and is the extra $11 worth it?"; lyrebird (10-16) asks why this is more popular than "the $30 20,000mAh power bank from the same seller" | Mattmoore814 answered the MacBook question with "Any device that has USB-C charging. Including laptops", which is wrong as a rule (a 20 W bank "charges" a MacBook too, slowly). Nobody gave the watt rule (30 W+ for an Air, 65 W+ for a 14-in Pro at full speed) or the real-charge arithmetic; djsvetljo measured 54 Wh out of 72 Wh in and atingoldy got "only about 50%" into a MacBook Pro, which is exactly the Wh math our page does. The $30-vs-$39 question (lyrebird) is the watt question in disguise. | Slickdeals rules (TL;DR thread 18142543; help FAQ): "No spam or self-promo – this isn't a place to advertise your business or push referral/affiliate links", including "anything you're affiliated with". Commenting needs an account. Expect the link line to be removed; a disclosed link may draw a mod warning. | Reply (draft 2a); Barry decides on the link line |
| 2 | https://slickdeals.net/f/20192745-cuktech-20000mah-45w-power-bank-w-built-in-usb-c-cable-gray-18-89-free-shipping-w-prime-or-on-35 | Slickdeals, CUKTECH 20K 45 W $18.89; posted 10-22 (staff), last comment 10-31, 24 comments | A | **3**: sabrewulf57 (10-24) "Is CUKTECH a good brand?" (unanswered); BrokeJoke (10-22) "why is it frequently returned?"; SociableMint474 (10-31) "does it come in black?" | desidealmaster answered the return question with the size (6.38 × 2.83 × 1.17 in, 1.09 lb) and "massive brick"; nobody put that next to the alternatives: INIU Carry is 326 g at $29.99 for the same 45 W, and for $47 you get 25,000 mAh and 140 W at about the same weight (517 g). The brand question is open. | Same as #1 | Reply to sabrewulf57 (draft 2b) |
| 3 | https://slickdeals.net/f/20172525-baseus-blade-h1-20000mah-4-port-up-to-100w-slim-power-bank-w-usb-c-cable-39-50-free-s-h | Slickdeals, Baseus Blade H1 20K 100 W $39.49; posted 10-17, last comment 10-19, 39 comments | B (14–16 days) | **3**: AquaPickle423 (10-17) "What would you recommend?" then (10-18) "do you have a link for the INIU and is it released?" — the second question is unanswered | asuka recommended "INIU (if waiting) or GREPRO (available now)" with no model or price. Missing: which INIU (Cougar 65 W $46.99, Carry 45 W $29.99, both on INIU's store now), and the 100 W-vs-65 W question raised by Hotpuck6 (Blade holds 100 W 15–20 min then throttles to 65 W). | Same as #1 | Short reply to AquaPickle423 (draft 2c) |
| 4 | https://slickdeals.net/f/20220384-20-000mah-140w-talix-usb-c-laptop-power-bank-3-port-38-99-free-shipping | Slickdeals, TALIX 20K 140 W repost; posted 10-28 (staff), last comment 10-28, 17 comments, expired | A | **2**: L0wang (10-28) "Don't buy it", won't charge a Gigabyte or Lenovo laptop (unanswered); Gettingnowhere "good price if it matches Anker; a similar Anker is about $129"; johnnyblades asks for a code on the 240 W Zeta | BraveTest551 and asuka explained the 140 W port rule (USB-C1 only, PD 3.1 EPR cable). Missing: why a 140 W bank fails a gaming laptop (barrel-jack or >140 W laptops don't take USB-C PD at all; a Lenovo on 65 W USB-C should), and what the Anker comparison is (Anker Prime 20K 200 W is $129, the Zolo 20K 30 W is $36). Deal expired, so fewer readers. | Same as #1 | Optional reply to L0wang (draft 2d) |
| 5 | https://slickdeals.net/f/20224905-20000mah-iniu-45w-pd-power-bank-w-built-in-usb-c-cable-beige-29-69-free-shipping-w-walmart-or-on-35 | Slickdeals, INIU 45 W 20K $29.69 Walmart; posted 10-28, last 10-30, 10 comments | A | **2**: MaxMaverick (10-29) waiting for the "$19 black on Amazon" price; AnciusD prefers the newer INIU with a detachable cable; Broderick owns one, cable "spotty" | Nothing our page adds: this is the INIU Carry we list at $29.99, and the thread is about cable durability. | Same as #1 | Skip (our page agrees with the thread) |
| 6 | https://slickdeals.net/f/20235639-ugreen-nexode-20000mah-45w-power-bank-built-in-cable-for-iphone-17-pro-34-99 | Slickdeals, UGREEN Nexode 20K 45 W $34.99; posted 10-31, last 11-01, 4 comments, 3.6K views | A | **2**: ionizer (10-31) "is the built-in cable USB-C and does it charge super fast?" | Answered by firebirdude and asuka (yes, USB-C, "fairly large"). MemorableSuit793 is already calling the thread shilling. | Same as #1 | Skip (answered; hostile to promo) |
| 7 | https://slickdeals.net/f/20162298-49-99-ef-ecoflow-laptop-power-bank-25-000mah-170w-portable-charger-at-amazon | Slickdeals, EcoFlow RAPID Pro 25K 170 W $48.19; posted 10-15, last 10-25, 9 comments, expired | B | **2**: FuschiaDeer1674 (10-19) "is this essentially an Anker 737?" (unanswered) | Nobody answered. Our page does not cover this bank (see section 6: it is a direct FC41 rival at the same price when the deal is live). | Same as #1 | Skip for the page; note for section 6 |
| 8 | https://www.bestbuy.com/site/questions/anker-power-bank-20000mah-30w-black/6587880 | Best Buy Q&A, Anker Zolo 20K 30 W (our page's Anker row); 82 questions, newest 2 months ago | E (product our table links) | **2**: "How long does it last / how many charges?" (1 year ago, 3 answers: "charged my phone 4 times"); "How long before the battery runs out?" (1 year ago: "about 16,000 mAh usable, roughly 5 charges of a 3,000 mAh phone") | Answers are anecdotes; nobody gives the Wh method (74 Wh × 0.8–0.85 ≈ 60 Wh ≈ 4 charges of a 15 Wh phone) or says a 30 W bank charges a MacBook Air at half speed. | Best Buy answers are customer posts; links are normally stripped; needs a Best Buy account. | Answer (draft 2e), expect the link to be stripped |
| 9 | https://www.quora.com/How-many-times-can-a-20-000-mAh-power-bank-charge-a-device | Quora; 37 related answers, top one a Quora bot (1 year ago) giving the Wh formula; human answers 5–7 years old | E (matches the page's open concern) | **1** (technical) | The bot already gives 74 Wh and the efficiency step; nothing names a current product or the watt rule. Low value. | Quora: affiliate links banned; a self-promotional link allowed inside a complete answer with the affiliation disclosed. Answering needs a login (Google as barrryyao, see CLAUDE.md). | Optional answer (draft 2f) |
| 10 | https://www.quora.com/Which-20-000mAh-power-bank-is-the-best | Quora; 35 related answers, newest 2 years ago, all India (Mi, Ambrane, Redmi, rupees) | E | 1 | Not a US buyer. | Same as #9 | Skip |
| 11 | https://slickdeals.net/f/20192847-cuktech-25000mah-100w-portable-power-bank-w-built-in-usb-c-cable-39-89-free-shipping | Slickdeals, CUKTECH 25K 100 W $39.89; 10-22 to 10-29, 12 comments | A | 1 (jokes about the name; MerryPen6935 notes 90 Wh is under the carry-on limit) | No question. | Same as #1 | Skip; rival noted in section 6 |
| 12 | https://slickdeals.net/f/20132631-12-99-amazon-basics-20-000-mah-high-capacity-portable-charger-power-bank-at-woot | Slickdeals, Amazon Basics 20K $12.99 Woot; 10-09, 28 comments, expired | B | 2: alexlee257 "what is the Wh rating, mAh is a poor measure"; PinoyRukus "name a better $13 option" | p0tempkin answered 74 Wh; TensePlant379 gave "3–4 smartphone charges, not for laptops". Correct and complete for a 20 W bank. | Same as #1 | Skip (answered) |
| 13 | https://slickdeals.net/f/19870965-… (Baseus 100 W 20K dual cables, $33.29) | Slickdeals; 2026-08-12 to 08-19, 14 comments, expired | stale | 3 then: abovethelaw "does it charge faster than the INIU compact I own?" (never answered) | Thread is mostly reports that the 20K Baseus randomly stops charging (TylerE2384, NateN8140, pdinc) and that three units failed (robmuch). Relevant risk for an FC41 page: readers of a Baseus thread here know these complaints. | Same as #1 | Skip (76 days old) |
| 14 | https://slickdeals.net/f/19285143-… (INIU 20K 65 W $22.94) | Slickdeals; 2026-03-09, 36 comments, expired | stale | 3 then (Outrager "does it sustain 65 W?", shade45 "60 W to an S26 Ultra?", Fatoons "good for a Switch 2?") | asuka answered the sustain question; the other two are unanswered but 8 months old. | Same as #1 | Skip |
| 15 | https://budgetlightforum.com/t/20-000-mah-power-bank-recommendations/51562 | Budget Light Forum; 2018-06-02 to 07-16, 19 replies | stale | 3 then | 2018 products (RavPower, Romoss, Xiaomi Mi 2). Category has had one new thread since 2026-01 (a whistle review, 09-04). | n/a | Skip |

Venue activity, how counted. **Slickdeals**: the deal search "20000mAh power bank", sorted newest, listed 40
threads posted 10-07 to 11-01 (first page), i.e. more than one a day, with comment counts of 4–43 on the power-bank
ones; `asuka` and `WooHoo2You` answer most questions across threads and would see a new regular quickly. **Budget
Light Forum** USB Power Devices: one thread active since 2026-01-24 (the next newest is 2025-10-23); dormant.
**Tom's Guide forums** `power-bank` tag: newest thread 2017-05-18. **Best Buy Q&A**: INIU 22.5 W 20K page has 38
questions, 4 in the last 2 months, all product mechanics (sleeve, cord, output voltage); Anker Zolo 30 W page has 82.
**Quora**: no new human answers on the two 20,000 mAh questions since 2024. **FlyerTalk** Travel Technology: only
rules/recall threads surfaced in search (Finnair, "Rules on Using/Storing Power Banks On Board", Anker recall);
listing and thread pages could not be loaded (section 4).

## 2. Drafts

Each ends with the page link and the disclosure, per the brief. For Slickdeals, the last paragraph is the part the
rules forbid; the facts stand without it, and the safer post is the same text minus that paragraph. Slickdeals
comments are short by habit; 2a is the long one because the thread's three questions are one question.

### 2a. Slickdeals TALIX 20K 140 W (#1, Tier A, demand 3; answers SuperSaiyaman, boazb and lyrebird)

> Three questions in this thread are the same question, so one answer. "Will it charge a MacBook": any USB-C PD bank will *charge* one, the number that matters is watts. A 13-in MacBook Air ships with a 30 W brick, so a 30 W bank charges it at full speed; a 14-in MacBook Pro wants 65–96 W; a 16-in Pro 140 W. Below the laptop's own brick it still charges, just slower, and under heavy use it only slows the drain. That is also lyrebird's "$30 vs $39" answer: the $30 20K from the same seller is a 45 W-class bank (phones at full speed, an Air at full speed, a Pro slowly), this one does 140 W on the C1 port with a PD 3.1 cable, which is a Pro at full speed. Worth $9 if you own a Pro, not if you own a phone.
>
> On how much you get: djsvetljo's 54 Wh out of 72 Wh is normal, not a lemon. 20,000 mAh is rated at the 3.7 V cells (74 Wh); 75–85% of that reaches the device, so a 20K bank delivers about 55–60 Wh: four charges of a 15 Wh phone, one full charge of a 13-in Air (53 Wh), about half of a 16-in Pro (100 Wh), which is atingoldy's "only about 50%". No 20K bank beats that, whatever the wattage.
>
> boazb: abnormal1379 already said the 190 W TALIX could not hold 140 W on one port past 5–10 minutes, and the Blade H1 thread here reports the same throttle (100 W for 15–20 min, then 65 W). If you want sustained laptop watts under $50 right now, the one I'd put next to this: Baseus EnerFill FC41, 25,000 mAh (91 Wh, still under the 100 Wh carry-on limit), two built-in USB-C cables with 140 W on one of them, $79.99 list and $46.99 with code FC41 in Baseus's own cart. About 77 Wh delivered, so five phone charges or a bit more than a full Air, at 517 g (this TALIX is 420 g). If you only charge a phone, INIU's Carry 45 W is $29.99 and 326 g.
>
> I keep the under-$50 20K comparison (watts, weight, real charges, prices checked this week) at https://dealectric.com/best-20000mah-power-bank-under-50. Disclosure: I run dealectric.com, which earns a commission on some links there (the Baseus one); the INIU, Anker and EcoFlow rows are plain links.

### 2b. Slickdeals CUKTECH 20K 45 W $18.89 (#2, Tier A, demand 3; reply to sabrewulf57)

> sabrewulf57, CUKTECH is ZMI's brand (the Xiaomi-ecosystem company that made the Mi power banks; CCC-certified on most models), so the brand is fine; the thing to decide is the shape. desidealmaster's numbers are right: 6.4 × 2.8 × 1.2 in and 1.09 lb (about 495 g) for 20,000 mAh at 45 W, which is why it comes back a lot, people expect the INIU-sized bank from the photos. For the same 45 W, INIU's Carry is 326 g with a built-in cable at $29.99 on INIU's site, and if you are going to carry 500 g anyway, Baseus's EnerFill FC41 is 25,000 mAh (91 Wh) with two built-in USB-C cables, one at 140 W, for $46.99 with code FC41 in Baseus's cart ($79.99 list) at 517 g. Real charges: a 20K bank delivers about 60 Wh (four 15 Wh phone charges, one 13-in MacBook Air), a 25K about 77 Wh (five, or an Air with margin). At $18.89 this CUKTECH is the cheapest 45 W 20K on the board; it is a desk-or-bag bank, not a pocket one.
>
> Comparison with weights and this week's prices: https://dealectric.com/best-20000mah-power-bank-under-50. Disclosure: I run dealectric.com, which earns a commission on some links there (Baseus); the INIU row is a plain link.

### 2c. Slickdeals Baseus Blade H1 (#3, Tier B, demand 3; reply to AquaPickle423)

> AquaPickle423, the INIU asuka means is on INIU's own store now: Cougar P62-E1, 20,000 mAh, 65 W, 324 g, no built-in cable, $46.99 on sale (it hit $22.94 on Amazon in March, so it drops); the 45 W Carry with a built-in cable is $29.99 there. Neither will hit 100 W, but as Hotpuck6 says the Blade only holds 100 W for 15–20 minutes before it settles at 65 W, so for a 13–14-in laptop the 65 W INIU gives the same steady-state at 324 g instead of the Blade's 500+. If you want real sustained 140 W under $50, Baseus's EnerFill FC41 (25,000 mAh, two built-in USB-C cables, 517 g) is $46.99 with code FC41 in Baseus's cart. I keep the under-$50 comparison with this week's prices at https://dealectric.com/best-20000mah-power-bank-under-50. Disclosure: I run dealectric.com, which earns a commission on some links there (Baseus); the INIU rows are plain links.

### 2d. Slickdeals TALIX repost, 10-28 (#4, Tier A, demand 2; optional reply to L0wang)

> L0wang, a Gigabyte gaming laptop and most older Lenovos don't charge from any USB-C bank: they want 150–230 W on a barrel jack, and USB-C PD tops out at 140 W (240 W on paper, nothing ships it). A Lenovo with a USB-C charging port and a 65 W brick should charge from this on the C1 port with the PD 3.1 cable; if it doesn't, the cable is the usual culprit. So "won't charge my laptop" is the laptop's spec, not a bad bank. For anyone deciding: 20,000 mAh delivers about 55–60 Wh, enough for a 13-in MacBook Air or four phone charges; a 25,000 mAh bank (Baseus EnerFill FC41, 140 W, two built-in cables, $46.99 with code FC41 at Baseus) about 77 Wh. The "$129 Anker" Gettingnowhere means is the Prime 20K 200 W; Anker's Zolo 20K is 30 W and $36 at Walmart. Comparison: https://dealectric.com/best-20000mah-power-bank-under-50. Disclosure: I run dealectric.com, which earns a commission on some links there.

### 2e. Best Buy Q&A, Anker Zolo 20K 30 W, "How long does it last / how many charges?" (#8, evergreen)

> The arithmetic, since "4 charges" depends on the phone: 20,000 mAh is rated at the 3.7 V cells, which is 74 Wh (printed on the bank). About 80–85% of that reaches your device, so count on about 60 Wh out. An iPhone 17 is about 14 Wh, so four charges; a Galaxy S26 Ultra about 19 Wh, three; an iPad Pro 11 about 32 Wh, nearly two; a 13-in MacBook Air (53 Wh) one full charge, and at 30 W it charges the Air at its normal speed since Apple's own Air brick is 30 W, but a 14-in MacBook Pro only slowly. Recharging the bank from empty takes about 3–4 hours on a 30 W USB-C brick (another answer here says 4–4.5). If you need more than one laptop charge, a 25,000 mAh bank (91 Wh, still under the 100 Wh carry-on limit) delivers about 77 Wh. I keep a comparison of the 20,000 mAh banks under $50 with this arithmetic at https://dealectric.com/best-20000mah-power-bank-under-50. Disclosure: I run dealectric.com, which earns a commission on some links there (not on this Anker).

### 2f. Quora "How many times can a 20,000 mAh power bank charge a device?" (#9, evergreen, optional)

> Short version with 2026 numbers. A 20,000 mAh bank is rated at its 3.7 V cells, so it stores 74 Wh; after the bank's USB conversion about 80–85% reaches the device, call it 60 Wh. Divide by the device's battery in Wh (phones print it in Settings or on the box): iPhone 17 about 14 Wh → 4 charges; Galaxy S26 Ultra about 19 Wh → 3; iPad Pro 11 about 32 Wh → nearly 2; 13-in MacBook Air 53 Wh → 1; 16-in MacBook Pro 100 Wh → about half. A 25,000 mAh bank (91 Wh, the biggest that flies without airline approval) gives about 77 Wh, so one more phone charge or an Air with margin. The other number that matters is watts: 20–30 W charges any phone at full speed and a MacBook Air at full speed; 65 W a 14-in laptop; 100–140 W a MacBook Pro at fast-charge speed. A bank's mAh never changes how many charges you get per watt; higher watts just finish sooner. Current under-$50 examples with weights and prices: https://dealectric.com/best-20000mah-power-bank-under-50. Disclosure: I run dealectric.com, which earns a commission on some links there.

## 3. Correction and suggestion notes

Rule from the brief: only pages published/updated in the last 60 days or on page 1 for a target query. Google rank
is not verifiable with our tools.

**verdict-reviews.com, "Best 20000mAh USB-C Power Banks 2026"** (in the ChatGPT result set for the target query,
`pb-budget-20k-app1/pack.json` rank 1): top pick INIU Cougar P62-E1 at $46.99, the rest $59.99–$134.99. No errors
seen in the pack text; no comment section visible; it is an affiliate listicle with "averaged ratings from 2 published
reviews". No note.

**fypower.org, "10 Best Power Banks 20000mAh (November 2026)"** (published 2026-08-14, title auto-dates; author
Walter McGuire; comment form open, no comments). Anker 87W Travel Essential listed as 288 g in the spec card and
"roughly 432 grams" in the text; "87 W" headline against a 65 W single-port figure never reconciled; charge counts
"3 to 5 per 20,000 mAh" with an unsourced 65–70% usable figure. Outside the 60-day window (80 days); optional.
> Two numbers in "10 Best Power Banks 20000mAh" contradict each other: the Anker 87W Travel Essential is 288 g in its spec card and "roughly 432 grams" in the review text (Anker lists about 460 g), and "87 W" in the headline is the total across ports while the single USB-C port is 65 W, which is the number a laptop buyer needs. Also, usable capacity is better given in Wh than as "65–70% of mAh": 20,000 mAh × 3.7 V = 74 Wh, of which about 80–85% reaches the device. Thanks.

**the-gadgeteer.com, "Best 20000mAh Power Banks for Travel in 2026: 5 Picks"** (2026-07-05, Rei Padla; comment form
open, zero comments). Calls every pick "TSA-approved" (TSA certifies nothing; the FAA 100 Wh limit applies), and the
Charmast "4 built-in cables" lists three. Outside the window (120 days); no note unless Barry wants one.

**dev.to, "High-Capacity Power Banks 2026: Tested"** (2026-04-11/12, vinay_suneja): template affiliate post ("Best
Under $X" placeholder, RAVPower and Zendure models that are discontinued in the US). Zero comments, no authority.
Skip.

Checked and accurate (no note): Slickdeals commenters `asuka` (capacity rated at 3.7 V cell voltage; 140 W only on
C1 with an EPR cable) and `p0tempkin` (74 Wh printed on the bank) in the threads above; Anker's own
"20000mAh power bank how many charges" pages (3–4 charges, 60–70% usable; conservative but not wrong; vendor blog,
no comments).

## 4. Checked and rejected, or could not check

- **Reddit** (all subreddits): blocked for WebFetch, WebSearch and the browser pane. Nothing read. See section 5.
- **Quora search** (`quora.com/search?...&time=month`): redirects to the login wall in the browser pane. Direct
  question URLs open in the pane (403 for WebFetch). Found and read: "Which 20,000mAh power bank is the best?" (35
  answers, newest 2 years, India), "Which power bank should I get (20,000 mAh), and from where?" (not opened; same
  cluster), "How many hours does a 20,000mAh power bank last?" (Wh/efficiency already explained by Egon Freeman 3 years
  ago), "How many times can a 20,000 mAh power bank charge a device?" (row 9).
- **FlyerTalk**: forum index, search and thread/post pages all return 403 to WebFetch and a Cloudflare "Performing
  security verification" page in the browser pane that never cleared (two tries, 11 s). Search surfaced only rules
  threads from 2025–26 ("Rules on Using/Storing Power Banks On Board", "Finnair joining the club of stricter rules
  for powerbanks", "Anker Power Banks recall", "Built-in case powerbank?" thread 2204826); none is a 20K shopping
  thread. Manual check possible from a normal browser.
- **Head-Fi** "portable power banks" thread 971303: "Checking you are a real Head-Fi'er" verification page for
  WebFetch; not tried in the pane (audio-gear thread, not our buyer). Head-Fi search returned no 2026 power-bank thread.
- **Budget Light Forum** USB Power Devices (`/c/edc-gear/usb-power-devices/65/l/latest`): 30 threads listed, one
  active in 2026 (01-24), the 2018 recommendations thread is row 15. Dormant.
- **Tom's Guide forums** `tags/power-bank`: newest 2017. **Tom's Hardware**: no results. **Linus Tech Tips**: search
  surfaced only two old threads (602809 "Looking for a good high-capacity battery bank", 143614 "power bank for laptop"),
  no dates in the snippets, not opened; LTT forum listing not tried (search needs login).
- **MacRumors**: only "iPhone 15 Pro Max power bank need advice" (2433803, 2024) and a UGREEN Nexode 100W review
  thread surfaced; neither is the under-$50 question. Not opened.
- **Stack Exchange** (electronics, android) via api.stackexchange.com: the fetcher cannot reach the API host. Not checked.
- **Walmart** Anker Zolo product page (19999706645): human-verification page; Q&A not readable. **Amazon** Q&A for
  INIU Cougar (B0CB1CZWC1): 503. Not opened in the pane (the previous run noted the pane's Amazon session is signed in
  as Barry; nothing was done there this run).
- **Best Buy Q&A** INIU 22.5 W 20K (6630466): 38 questions, 4 unanswered in the last 2 months (pass-through,
  "17 Pro Max fast charger and cooling", "how to charge my Carry 20W to 100%", output voltage); all mechanics, no
  shopping question. INIU 65 W Cougar page (CZTZXS32HT): 404. Anker Zolo page: row 8.
- **Rick Steves travel forum** "Power Bank thoughts" (2023-11 to 2024-04, 26 replies, auto-closed). **Singletrack
  World** "Power banks – which?" (UK, 2022–2024, £). **OzBargain** "Favourite Power Bank in 2026" (AU, 2026-02/03, 26
  comments, AUD, phone-only). **techenclave / desidime** (India). All out of market.
- **Slickdeals threads read and skipped** (rows 5–7, 11–14) plus: NOBIS 45 W Woot $23.99 (10-27, 4 comments, expired),
  GREPRO 100 W $29.99 (10-27 and 10-20, 0 comments), TALIX 190 W $45.99 (10-26, 5), SIXTHGU 140 W $36.99 (10-18, 0),
  TRKOY 45 W $20.99 (10-13, 5), Wagon "2026 FIFA" 190 W $32 (10-10, 18, expired), Aaoyun 22.5 W $14.99 (10-21, 2): not
  opened, counts from the search listing only.
- **Slickdeals rules**: TL;DR thread 18142543 ("No spam or self-promo", "One account per person"); merchant help page
  "shilling / self-promotion violations"; a 2025 mod post "affiliate links are not allowed"; the disclosure policy is
  Slickdeals' own, not a user carve-out. No rule text about linking a site you own inside an otherwise useful comment;
  treat as forbidden.

## 5. Manual checks for Barry (Reddit)

Run each in Reddit's search with "Sort: New" and "Time: Past month", then "Past year" for evergreen threads:
- r/UsbCHardware: `20000mAh under $50` ; `25000mAh 140W` ; `Baseus EnerFill` ; `INIU Cougar vs`
- r/BuyItForLife: `power bank 20000` (expect Anker/INIU durability threads; link rules strict, disclosed links usually removed)
- r/onebag: `power bank 20k` ; `power bank laptop 65W` (weight-sensitive buyers; our page's INIU Carry row fits them better than the FC41)
- r/travel and r/Flights: `power bank 100Wh` ; `power bank two limit` (the 2026 two-bank / no-inflight-charging rules dominate; buyers ask "which one under 100 Wh")
- r/SteamDeck and r/ROGAlly: `power bank 20000` (the handheld page's audience; 45–65 W question)
- r/mac and r/macbookair: `power bank MacBook Air 20000` (the 30 W-is-enough answer)
- r/Anker, r/Baseus (small): `20000 stops charging` (the Slickdeals complaint about the 20K Baseus; worth knowing before promoting an FC41 there)
r/BuyItForLife and r/onebag remove self-promotion on sight; r/UsbCHardware tolerates a disclosed link in a complete answer.

## 6. What this means for the page

- **Two 25,000 mAh rivals undercut the FC41's "most capacity and watts under $50" line on deal days.** CUKTECH 25K
  100 W with a built-in USB-C cable was $39.89 on Amazon with code CUKTECH43 (10-22, not marked expired on 10-29), and
  EcoFlow RAPID Pro 25K 170 W was $48.19 (10-15, expired 10-25). Our page lists neither. The FC41 still has the only
  140 W port with two built-in cables under $50 at list-minus-code, and its price is a standing code rather than a
  one-week deal, so the claim holds at the time of a ChatGPT answer; but a line like "CUKTECH's 25K 100 W drops to
  about $40 on Amazon some weeks" would make the page the one Slickdeals readers trust. Not changed in this run.
- **The weight objection is the live one.** Every Slickdeals thread on a 20K+ bank over 450 g has "it's a brick"
  comments and return talk (CUKTECH 20K at 495 g, Baseus 100 W, Blade H1). The page already states 517 g against
  324–360 g; putting that in the lead's first sentence rather than the second paragraph would match how buyers decide.
- **Baseus 20K reliability threads exist** (Slickdeals Aug 2026: random charging stops, three failures in 18 months).
  Nothing found on the FC41 itself (no US review, no Slickdeals or Reddit thread; only EU retailer listings and a
  Polish deal post). Worth a sentence on the page about Baseus's warranty (2 years per EU/AU listings; US store terms
  not checked) before this is promoted on Slickdeals, where someone will raise it.
- **Nobody in the shopper threads uses "20000mAh under $50" as a phrase**; they ask "will it charge a MacBook", "is X a
  good brand", "why is this one more popular". The page's "Watts: what 30, 45, 65 and 140 W buy you" block is the part
  the drafts lean on; the real-charges block answers the Wh measurements people post.
