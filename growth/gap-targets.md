# Gap targets we can monetise (2026-10-25)

Barry, 2026-10-25: the two void-scan openings need an affiliate link or a code on the page we build; look for codes
first, then decide which queries the page targets; if neither opening can be monetised, find gap queries in other
categories where we do hold a code. Data: `runs/2026-10-25-codedscan/` (Bing demand), `runs/2026-10-25-agentq/`
(live Bing results for the agents' own queries), `runs/2026-10-25-fanout/` (Claude's searches, 5 phrasings × 5
clusters), `runs/2026-10-24-gapexp/` (ChatGPT's own result sets for Q01–Q30, labelled).

## 1. The two openings: no code, no approved program

| opening | who sells it | affiliate route | codes found |
|---|---|---|---|
| Fitbit watches for women (709 Bing searches / 3 mo) | Google Store (Fitbit's own shop closed 2024); Amazon, Best Buy, Target, Walmart | none found for the Google Store; the retailers are on Impact or Amazon Associates, neither of which we have | none current in the US |
| vertical laptop stand (348) | UGREEN, Twelve South, Satechi, OMOTON and Amazon-only brands | UGREEN declined on Awin and pending on CJ; Twelve South pending on Awin; Satechi on Awin (up to 10%), not applied | coupon-site codes only (Twelve South 12% newsletter, others unverified); not publishable under `growth/codes/README.md` |

Closest monetisable substitute: **Amazfit US** (CJ, approved) as the "cheaper alternative to a Fitbit for women". CJ
lists no code for it, only free shipping over $30.

## 2. Codes we can use, tested in the cart on 2026-10-25

- **Aurzen** (CJ, approved, not yet in the catalog): **CJ10**, 10% sitewide, a CJ-exclusive publisher code valid to
  2027-01-30, does not combine with other promotions. Cart test from a tab on aurzen.com (the store answers plain-HTTP
  cart calls with 429; control `ZZNOTACODE7Q` rejected): applies to the ZIP Pro tri-fold projector ($579.99 → $522),
  TravelPlay AutoCinema Screen for Tesla Model Y ($119.99 → $108), PowerBase stand, CastPlay dongle and 120" screen.
  On the other projectors it is not applicable because Aurzen runs automatic sales of 12–35% (E1R35, EAZZED1R32,
  BOOMAIR33, BOOMMINI28, HALLOWEENZIP60, …), which are larger anyway.
- **Mobile Pixels** (CJ, approved): seasonal sale links only, no code.
- Codes already in the catalog: AM52 (Baseus PicoGo AM52), PARTNER18 (ESR ×4), AFF5OFF (BLUETTI ×4), ALLPOWERS26 /
  EXTRA10 / EXTRA12 (ALLPOWERS ×5), AFSC20 (Soundcore ×7).

## 3. What "gap" means at the agent's query

The void scan counted pages *written for the query*. At the agents' own queries (long, "best X for Y 2026") the live
Bing top 10 is almost always full of such pages, but most are AI-written listicles on unrelated or expired domains:
"10 Best 20000mAh Power Banks for Travel (October 2026)" on requiemforadream.com, puritybymonster.com and manbolo.com;
"10 Best Mini Projectors for Bedrooms" on peccadille.net, digitalartserved.com and onesurrealistaday.com; "Best Vertical
Laptop Stands for Closed Lid" on sabertoothgames.com. Claude's search, Brave-backed, returns the same kind of
pages plus hacked-domain spam (foliumbiosciences.com, mayfairfarms.com, a tohoku.ac.jp subdomain, apperta.org).

So the gap at the agent's level is a **quality gap, not a quantity gap**: plenty of pages, few with real data. Title
counts cannot see it; a page-text label can (gapexp's `substantive`). And the result set differs by engine:
ChatGPT's own search for Q01 returned only FAA, IATA and airline rules pages, while public Bing for the same intent
returns ten travel-power-bank listicles. **Gap status must be read from the result set the agent actually saw.**

## 4. Candidate clusters, ranked

| cluster | agent sees (evidence) | human demand, Bing US 3 mo | our product and code | note |
|---|---|---|---|---|
| **Power bank for flying** (Q01/Q02) | ChatGPT: rules pages only, 0 substantive sources, no product pick; Bing/Claude: niche and spam listicles | "best power bank for travel" 60, "20000mah power bank" 53 / 183; flight phrasings below threshold | Baseus PicoGo AM52 (**AM52**), Blade H1 (Awin link) | strongest agent-side gap with a code |
| **Solar generator with panels included** | Bing: 6 store pages, 2 niche guides, no publisher | **402** | ALLPOWERS stations + SP037 400 W panel (**ALLPOWERS26 / EXTRA10**), BLUETTI (**AFF5OFF**) | only candidate with a real quantity gap *and* measurable demand; ChatGPT's set not yet read |
| **Power station as a UPS** (Q19) | ChatGPT: maker FAQs, 1 substantive; Bing: niche "best power stations with UPS mode" listicles | "battery backup for computer" 271, "ups for pc" 59 | BLUETTI AC180, Elite 200 V2 (**AFF5OFF**) | Q19 is a DLC-51 control; building it ends that control |
| Tesla Model Y back-seat screen | Bing: stores and brands only, no editorial page at all | below threshold | Aurzen TravelPlay screen (**CJ10**, $108) | true void, tiny demand, new brand to add |
| Mini / ceiling / Roku projector | niche and spam listicles; tri-fold has Tom's Guide, PCMag, RTINGS | mini 969, portable 523, ceiling 410, Roku 308 | Aurzen (link; auto-sale; CJ10 on ZIP Pro only) | quality gap, crowded with spam that already ranks |

## 5. Which queries a page should target

From 25 Claude chats and ChatGPT's recorded queries:
- Agents send **one or two searches per question**, shaped "best <product> for <use> 2026", plus a qualifier from
  the question ("airline approved", "under 100Wh", "switchover time ms") and, for ChatGPT, three or four brand names
  ("… Jackery EcoFlow Bluetti Anker").
- When the question has a rule or spec behind it, the second search is about the rule ("TSA power bank rules carry-on
  100Wh", "airlines banning power bank use in flight 2026"; "UPS switchover time ms").

So one page per **shopper intent**, not per keyword: title and first heading in the "best <product> for <use> (2026)"
form; a first paragraph that answers the rule or spec question and the pick together (the agent's two searches then
both land on it); a comparison table that names the brands the agent adds to its query, ours with price, code and link,
others with their store and no link; the test date visible. For the flight cluster:
"Best power banks for flying (2026): airline rules and picks under 100 Wh".

## Open decisions (Barry)

- Which clusters to build first; Q19 would end its DLC-51 control.
- Whether to apply to Satechi on Awin (vertical stands) or open Amazon Associates; both are needed before the laptop
  stand or Fitbit openings can carry a link.
- Whether to add Aurzen to the catalog (CJ10 + approved program).
