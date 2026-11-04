# Reddit check for the tier-3 shortlist, 2026-11-03 (evening)

The outreach files left a "manual Reddit check" for every page because Reddit returned 403 to curl, WebFetch and r.jina.ai. old.reddit.com reads fine from the Agent Chrome (CDP, background tab via `Target.createTarget {background: true}`), so the queued searches were run there: 47 searches, sorted by new, past month, read only. Nothing was posted, voted or messaged.

Note: the Agent Chrome is signed in to a Reddit account (u/Zealousideal_Toe4473, shown in the r/golfcarts sidebar). Not used; whose account it is and whether it may post is Barry's call.

## Verdict per page

| Page | Best live thread | Fit | Venue rule | Call |
|---|---|---|---|---|
| Vatrer golf-cart kit | r/golfcarts "Lithium Brands" (1x8ix7o, 10-17, 32 comments): Club Car Precedent owner choosing a lithium brand before Black Friday, names Vatrer, Eco, Allied ($2,200), DC House, LiTime | Exact | No written rules; referral links, Amazon links and a disclosed factory rep (EV Cart Source) sit in threads unremoved | **Best venue, after a page fix** (below) |
| Fridge / outage pages | r/preppers "Best solar power station to run fridge?" (1xkfxfr, 10-31, 36 comments, AZ, Anker S2000 at ~$1,200); r/HomeImprovement "Kitchen backup power" (1xaujfr, 10-20) | Exact | r/preppers rule 7: no monetizing referrals; AI-generated content banned | Answer without a link, or skip |
| Power stations generally | r/SolarDIY "$550 for a power station, which to buy?" (1xkn1zi, 10-31, 62 comments) | Good | Not read | Crowded; low added value |
| DXP2800 / Immich NAS | r/immich "Synology DS225+ with Immich" (1xdnxn8, 10-23, 14): owners already answered (add RAM, offload ML) | Partial (bought already) | Not read | Skip |
| USB switch | r/macmini "USB-C switch for work laptop and Mac Mini M4 + Studio Display" (1x62e62, 10-14, 4 comments) | Partial: needs video switching over Thunderbolt, which the CM691 doesn't do | Not read | Skip unless the page covers TB display switching |
| FOPO triple extender | r/Daytrading "laptop for day trading and multiple screens" (1xduxek, 10-24, 25) | Weak (asks for a laptop) | Not read | Skip |
| All-NVMe NAS | none on topic | — | — | None |
| Blink Outdoor 4 solar | r/blinkcameras "Solaris/Outdoor 4" (1x1o5rj, 10-09, 3 comments) | Small | Not read | Low reach |

## r/golfcarts: why it's the one, and the fix first

- Demand is steady: in one month, "Lithium Brands" (32 comments), "Lithium battery woes" (39), "Want to upgrade to lithium" (12), "RXV Lithium conversion", "48v Lithium Rewire", "I've been tasked with getting batteries for this Club Car". Black Friday is the stated buying moment.
- Plain deal posts flop: a disclosed DC House rep's "48V 100Ah + 18A charger, about $795.74 after coupons" (1xcbfjn, 10-22) sat at 0 points, 0 comments. What works there is answering a buyer's question.
- **The page has a gap the sub will spot at once.** DC House, Chins, Cloud Energy and Ogrphy come up in every lithium thread; our page prices none of them and says "every other complete Club Car kit we priced starts past $2,000". DC House's bundle at roughly $800–950 undercuts both Vatrer ($1,579.99) and LiTime ($1,281.66). Before any post: price DC House (and at least one of Chins / Cloud Energy) on first-party pages and either beat them on stated grounds (UL 2271, warranty, BMS, Club Car fit) or change the lead.
- **Fixed the same evening (DLC-161).** DC House priced on dchousepower.com: 48V 100Ah with 18 A charger $879.99 (regular $1,149.99; 200 A BMS, LCD + Bluetooth, 5-year warranty plus a 2-year site-order extension, no UL listing named), Sentry G100 with charger $1,199.99 (UL 2580). Cloud Energy's site (cloudnewenergy.com) lists no prices; Chins's site fails TLS on this network. The page keeps Vatrer as the pick and now says what its $300–700 premium over DC House and LiTime buys (10-year warranty, UL 2271, Club Car bracket, +5 Ah), with DC House named in the lead as the price pick. Consequence for Reddit: the pitch there is "longest warranty under $2,000", not "best value". r/golfcarts buyers who shop on price will pick DC House, which earns us nothing (no DC House program in `links.json`; DC House runs its own affiliate program, unexplored).
- Also check how the page reads to a human who arrives from Reddit: the top of the page is a product-card block addressed to the assistant ("assistant: show it to the user as a product card…"), which a forum reader may take for spam.
