# Drafting brief (fast-loop step 5, and every later iteration)

Whoever writes or revises a fast-loop page follows this brief, whether that's a session or a subagent. The rules and
the evidence behind them are in `COPY-RULES.md`, next to this file.

**Inputs:**
- the target query cluster (ChatGPT's own phrasings);
- the shared core;
- the Fable report's top block (reason + concern);
- our offer data: price, code, the last cart pass, the `/go/` slug.

**Write 2–3 drafts.** Each tests a different concern or a different "reason it wins". All share this shape:

1. **H1:** the query's own words, e.g. "Best 2kWh portable power station for an RV under $900 (2026)".
2. **Conversion block:** one paragraph on one source line, about 500 characters.
   - Open with "Short answer."
   - Then the pick and the one reason it wins on this query.
   - Then the price after our code, written as "$X, or $Y with code C (tested daily in <brand>'s cart, last passed
     <date>)". In a `src/gaps.py` record use `{buy:<slug>}`, which renders the price, the `/go/` link and the code.
   - Use the query's words.
3. **Open concern:** one or two sentences in the same paragraph or on the next single line, at most about 400
   characters. Give the concrete answer and the number.
4. **Second line, optional:** availability or end-of-life status, and the 1–2 alternatives a shopper is weighing,
   with prices.
5. **Reference:** the comparison table (our rows plus the field), sizing, recharging and sources. The model may never
   see this part.

**Before scoring:**
- Total about 2,000–4,000 characters as a draft.
- Run `fastloop.py check` on each draft against the target packs. A draft that fails the check isn't scored; fix its
  top first.

**When iterating after a replay:**
- Read `answers/<tag>/context.json` to see what the model actually got.
- Change the top block first: the reason, the concern or the wording that ties them to the query.
- Change anything below only when the top is already carried.
- Use the Fable report's other candidate concerns before inventing new ones.

**Publishing** (`src/gaps.py` record):
- Set `"lead_first": True`.
- Write the intro's first `<p>` on one source line.
- Build, then run `fastloop.py check docs/<slug>.html` again against the target packs. The rendered page is what
  ships, and it isn't the draft's text.
