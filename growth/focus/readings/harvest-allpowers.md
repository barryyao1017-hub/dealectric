# Query harvest: what vague shopper questions turn into inside ChatGPT (ALLPOWERS as the test brand)

Run 2026-10-30, `growth/evals/runs/2026-10-30-harvest-allpowers/`. Questions: `growth/focus/harvest-allpowers-questions.json`.
Scoring: `python3.12 growth/evals/harvest.py --run 2026-10-30-harvest-allpowers --brand ALLPOWERS`. Signed-in ChatGPT
(Free), temporary chat, gpt-6 answers only (downgraded gpt-6-mini answers dropped). n=1 per cell.

Asked on Barry's brief: simulate what shoppers really type, generic first, and find patterns that carry over to other
products and verticals, not just ALLPOWERS.

## What was asked

| Level | What the shopper gives | Prompts | Cells done |
|---|---|---|---|
| G0 | category only, no details | "What portable power station should I buy?", "Which solar panel should I buy?", "Is a solar generator worth it?", "What's the best backup battery for my home?", "I want to buy a solar generator. Any recommendations?" | 10/10 |
| G1 | a situation, no product named | outages ("not stuck in the dark"), fridge in an outage, camping phone + lights, van solar, jobsite tools, hurricane season, CPAP, quiet gas-generator alternative | 16/16 |
| G2 | category + one constraint ("best … under $1,000", "for RV", …) | 8 prompts | 0/8, see "Not done" |

Each G0 and G1 prompt was asked twice: **natural** (ChatGPT decides whether to search; `ui.py search=False`, the
way a real shopper's chat starts) and **forced-search** (`hints=search`, how all earlier evals ran).

## Results

| Level | Mode | n | Searched | Asked back | Named products | Products per answer | ALLPOWERS named | Our page in results |
|---|---|---|---|---|---|---|---|---|
| G0 | natural | 5 | 5/5 | 1/5 | 4/5 | 2.6 | 0/5 | 0/5 |
| G0 | forced | 5 | 5/5 | 0/5 | 4/5 | 2.6 | 0/5 | 0/5 |
| G1 | natural | 8 | 6/8 | 0/8 | 7/8 | 2.6 | 0/8 | 0/8 |
| G1 | forced | 8 | 8/8 | 0/8 | 6/8 | 2.4 | 0/8 | 0/8 |

- **Brands picked** (answers naming each, of 26): Jackery 10, Anker 8, EcoFlow 8, BLUETTI 6, Renogy 3. Rooftop and
  whole-home brands (REC, Qcells, Maxeon, Tesla, FranklinWH, Generac) appeared only where the question drifted to
  rooftop or whole-home products (pattern 3). ALLPOWERS: 0/26.
- **Buy buttons:** 17/26 answers carried them. They went to big retailers (Best Buy, Home Depot, Walmart) or brand
  stores, plus one each to energysage.com and outdoorgearlab.com. No affiliate catalog got a button.
- **Who ranks for generic queries** (cells where the site was among ~13 results): Consumer Reports 10/26 (top result
  in 6), OutdoorGearLab 6, TechRadar 5, EnergySage 5 (top in 5, all rooftop or whole-home). Small comparison sites
  do get in: thepowerstationguide.com 4, generatorchecker, buyersheet, poweroutlast 3 each, powerbencher top in 2.

## Patterns that should carry over to other products

1. **ChatGPT searches almost every shopping question, even unprompted.** Natural mode searched 11/13 times. The two
   that didn't (fridge in an outage, camping charging) answered from memory with the big brands (EcoFlow DELTA 2,
   Jackery, BLUETTI AC180, RIVER 2). Forcing search changes little, so earlier forced-search evals were roughly
   representative.
2. **ChatGPT, not the shopper, writes the search, from one template:** `best <ChatGPT's category name> 2026
   [review|comparison] <spec words> <use cases>`.
   - "2026" was in 19 of 26 queries; 16 started with "best".
   - Spec words: capacity, LiFePO4, surge, warranty, sizing.
   - Use cases it adds on its own: camping, home backup, outage.
   - Big-brand names in only 3 of 26 queries, all on purchase-intent prompts ("Any recommendations?", home battery).
   - **Never "deal", "discount", "code" or "coupon" (0 of 26).** Code words come only from the shopper's own wording.

   The shopper's words barely survive; retrieval depends on ChatGPT's category word plus the spec words.
3. **The category word decides the vertical, and generic words drift away from portable gear.**
   - "Which solar panel" → rooftop residential panels (REC, Maxeon, Qcells), never portable panels.
   - "Backup battery for my home" → installed systems (Powerwall, FranklinWH, Enphase), plus one EcoFlow DELTA Pro Ultra.
   - "Not stuck in the dark" → lanterns, headlamps and power banks.
   - "Solar generator" and "portable power station" stay in our category.

   A product can only win a generic question if ChatGPT maps that question's word to the product's category. For any
   new product, ask the bare category question first and see where it lands.
4. **Situation questions search authorities first, products second.** Fridge → USDA and Ready.gov; CPAP → FDA,
   ResMed, Philips; outage → CDC and FEMA. The product part of the query is a sizing query ("starting watts running
   watts sizing", "runtime"). A page that answers sizing with numbers and then names products matches the second
   query; a product page or a codes page matches neither.
5. **Answers are a short list: 2–3 models.** The generic short list is the big four (Jackery, Anker, EcoFlow, BLUETTI).
   Nothing in the result sets put ALLPOWERS on it: the publishers ChatGPT reads (Consumer Reports, OutdoorGearLab,
   TechRadar) do not feature it.
6. **The buy click on generic questions goes to retail and brand catalog cards, not to cited pages.** This fits the
   other session's finding that product cards come from OpenAI's shopping catalog. On generic questions our only
   route to a click is still a link the model writes itself from our page. That needs our page retrieved and our
   product in the short list, and both failed here.

## What this means for Dealectric

- **The generic route is the hardest one for a non-big-four brand.** At G0 and G1, ALLPOWERS is absent from the
  result sets, the short lists and the catalog cards. Our first sale came from a narrower question that matched a
  page title ("solar generator with panels included"). That fits pattern 2: retrieval follows ChatGPT's query, and
  narrow questions keep their distinctive words in it.
- **Our discount-code positioning matches brand-named queries, not generic ones.** Generic queries carry no code
  words (pattern 2). A page that wants generic traffic has to win on the spec and use-case words first; codes
  are the bonus that makes it the most useful page once retrieved (the solar page's win, compqual).
- **Page recipe for a generic or situation question** (applies to any vertical):
  1. Title in ChatGPT's query words: "best <category> 2026" plus the use case and spec words it adds.
  2. Include the big-four models the short list will contain. The shopper is weighing them anyway, and it lets a
     focus product sit next to them in one table (as G04 does).
  3. For situation questions, put the sizing answer first (watts, Wh, runtimes), then the picks.
- **Which focus products can still win generic questions:** stations framed as "portable power station" or "solar
  generator" (P1800, R4000, S2000 Pro kit). Generic wording cannot win the **SP037 400 W panel**: "solar panel"
  drifts to rooftop. It needs a G2 phrasing ("portable solar panel for power station").
- **Product selection, for later verticals:** weigh new focus products by whether the publishers ChatGPT reads
  already list them. A brand absent from Consumer Reports, OutdoorGearLab and TechRadar starts outside the short list
  on every generic question.

## How this fits the stage model (other session's summary, 2026-10-30)

That session studied brand- and product-named questions (W1, "<product> discount code"); this run studied generic ones.
The two agree on:
- one search per question;
- answers taken from OpenAI's stored copy;
- catalog cards taking the buy click.

They differ on one point. Its draft implication 2 ("cards that use the words shoppers' queries use, 'discount
code', the model name") holds for brand-named questions only. Generic queries use category, spec and use-case
words. Hub cards and titles that should catch generic questions need those words.

## Not done, and caveats

- **G2 (8 cells) not run.** The Free-plan quota ran out at 19:26Z. Every retry for four hours came back from
  gpt-6-mini, so the scan was stopped at 23:45Z. Re-run the G2 cells when the quota resets (same command, the scan
  skips answered cells).
- n=1 per cell. Patterns 1, 2 and 5 repeat across most cells. Patterns 3 and 4 rest on 2–4 cells each.
- Results come from one signed-in Free account in California (one home-battery query added "California").
- Only ALLPOWERS's own categories were tested. Patterns 3 and 5 are the ones to re-check first in a new vertical.
