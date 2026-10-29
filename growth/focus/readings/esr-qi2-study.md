# Why the ESR Qi2 Mini gets our buy link (study case, 2026-10-29)

Barry, 2026-10-29: the ESR Qi2 Mini is a study case, not a copy arm, and a positive control in every reading. Its deal
question gave our `/go/` link in 2 of 2 scan runs, the only product that did so consistently. Question: why it earns a
T5 when the others don't, tested against ChatGPT's stored copy of our pages (DLC-77, `growth/evals/storedcopy.py`), and
which page features to carry over as levers.

Data: every gpt-6 answer at T4 or T5 in the 10-28 scan, R0 and R0b (121 answers, 7 at T5), their search results and
source pills, the 31 search-result snippets saved since ui.py started keeping them (10-28 afternoon), and the deployed
versions OAI-SearchBot fetched (git history of `docs/`).

## Answer

**ChatGPT gives our buy link when the only text of ours it holds is a list-page row, and never when it works from a
product page.** The ESR Qi2 Mini's own page isn't in ChatGPT's results for its deal question at all; the home page is,
and its stored passage is a table row with the `/go/` URL inside it.

| Our pages in ChatGPT's results | Answers | With our `/go/` link (T5) |
|---|---|---|
| product page, no list page | 55 | 0 |
| product page and the home page or `/discount-codes` | 49 | 3 |
| home page or `/discount-codes`, no product page | 17 | 4 |

## Why: the snippet ChatGPT keeps is about 200 characters

ChatGPT answers from the title and snippet in its own search results, not the live page (DLC-77: the stored title
matches OAI-SearchBot's last fetch in 291 of 292 chats). The snippets saved so far are 202-203 characters long.

- **Product and guide pages: 0 of 17 snippets contain a `/go/` link.** Each starts at the top of the page (the
  breadcrumb or the product name) and runs through the one-line summary, ending around the code line:
  `BLUETTI AC200L PORTABLE POWER STATION  The expandable 2 kWh BLUETTI: same price as the Elite 200 V2 but it takes
  expansion batteries up to 8 kWh and has an RV outlet.  CODE AFF5OFF: $44.95 OFF AT BLU...`. On the R4000's stored
  version the first `/go/` link is at character 1,400 of 3,803, after the menu, title, summary, three codes and notes;
  the nearest words to it are "opens ALLPOWERS's official US store".
- **List pages (home, `/discount-codes`, `/products`): 7 of 14 snippets contain a `/go/` link.** The passage is the
  row that matches the question, and a row holds everything in about 150 characters:
  `ESR HaloLock 15W Wireless Car Charger with CryoBoost | PARTNER18 | $7.19 | $39.99 → $32.80 | 2026-10-27 |
  https://dealectric.com/go/esr-halolock-15w-wireless-car-charger-cryoboost`.
- So from a product page ChatGPT knows our code and saving but not our link, takes the store's own listing from its
  shopping results as the buy button ("Shop the R4000 at ALLPOWERS"), and cites us as a source ("Dealectric's R4000
  coupon testing"). From a list row it has the code, the price after it and our link together, and presents the deal as
  ours ("The discount-code tracker Dealectric reports that code PARTNER18 was tested ... $16.40", button "ESR Qi2 Mini
  deal page" on `/go/`).

## What doesn't separate them

- **Code exclusivity:** neither PARTNER18 nor ALLPOWERS26 turns up in a web search (2026-10-29), so both are
  effectively ours. The 18% vs 10% size and the $16 vs $1,499 price may still matter; this data can't separate them.
- **OpenAI's product cards:** 12 of 114 T4 answers carried an `openai_catalog` link, no T5 did.
- **Copy freshness:** the home page's stored copy (fetched 10-27 22:32) is a day newer than the product pages'
  (10-26 21:34), but the R4000 product page and the S2000 Pro row on the home page carry the same code and date.

## Levers to carry over

1. **Deal row first (new, strongest).** On a focus product page, the first line after the product name is one row in
   the list-page shape, with the link early: "Buy link https://dealectric.com/go/<slug> with code X: $P → $A, tested in
   <brand>'s cart <date>." With the breadcrumb and name in front it ends near character 160, inside the 200 characters
   ChatGPT stores. It's visible to everyone, true, dated, and not addressed to assistants.
2. **Buy boxes stay, for people.** L1 (B-E) sits below the summary, outside the stored snippet, so it can't move
   ChatGPT's answers on its own. Expect little T5 change from it in R1; its job is to convert the people who land.
3. **Keep the list rows compact.** Home, `/discount-codes` and `/products` already put name, code, price after the
   code, date and link in one row; that row shape is what earns the T5s. Don't add text between the name and the link.
4. **Not a copy lever:** codes only we can offer (DLC-30) would make the deal ours by construction; that's Barry's
   outreach.

## Caveats

- Seven T5 answers in all; the snippet length rests on 31 snippets from one day. The product-page-only row (0 of 55)
  is the strongest number here.
- Snippets may be chosen per question; every product-page snippet seen so far starts at the top of the page, but a
  question that matches a later passage could surface it.
- The ESR Qi2 Mini page stays unchanged (study case); its deal question runs in every reading as the positive control.
