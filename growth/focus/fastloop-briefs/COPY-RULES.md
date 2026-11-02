# Copy rules for fast-loop pages (Barry, 2026-11-01)

Every step of the fast loop that decides page content follows these rules. That means the Fable research step, the
drafting step, the scoring and the renderer. The briefs in this folder carry them, `fastloop.py check` enforces them,
and the skill (`.claude/skills/chatgpt-discoverability/SKILL.md`) points here.

## The two facts behind the rules

**1. ChatGPT's model sees only part of a page, and less the lower it ranks.** One search's results share one text
budget. Each page gets a share by its rank, and a page longer than its share is cut [measured, `context-probe.md`].
The cut keeps the page's opening passage, then the passages sharing the most words with ChatGPT's own search query,
in page order. Shares, in characters, as `fastloop.py` models them (calibrated on the measured probes):

| results in the search | rank 1 | rank 3 | rank 6 | rank 10 |
|---|---|---|---|---|
| 9 | 3,825 | 2,208 | 1,561 | n/a |
| 12 (the median) | 3,207 | 1,852 | 1,309 | 1,014 |
| 17 | 2,606 | 1,504 | 1,063 | 824 |

A new page should expect rank 3–6, so plan for **about 1,000–1,500 characters** reaching the model. Rivals at low
ranks reached it with 110–170 words each.

**2. The very top of the page is what counts.** The opening passage is always kept. The shopper's ~200-character
snippet is the H1 plus the summary line. A sentence placed lower survives only if it shares the query's words, and even
then only while the budget lasts. DLC-114 measured it:
- Draft A's open concern sat below the short answer. The cut dropped it, and it was carried in 0 of 2 answers.
- The same concern inside the short answer (A2) was carried in 4 of 6.
- When the rendered page split that short answer across source lines, the concern fell out again.

## The rules

1. **The conversion block opens the page.** Right after the H1, one paragraph on one source line, about 500
   characters, holding:
   - the pick;
   - the price after our code, with the cart-test date ("tested daily in <brand>'s cart, last passed <date>");
   - the `/go/` buy link;
   - the one reason it wins on this exact query.

   Use the query's own words: the category word, the spec words and the constraint (e.g. "2kWh", "RV", "under $900").
2. **The open concern comes next.** One or two sentences, at most about 400 characters, in the query's words. Put
   them in the same paragraph or on the next single line, with the concrete answer and the number that matters
   ("the socket is 30 A, but the inverter caps at 2,400 W, about 20 A").
3. **Everything after that is reference** (the table, sizing, recharge notes, sources). The shopper's decision must
   not depend on it. Assume the model never sees it at rank 3 or lower.
4. **One passage is one source line.** A line break in the HTML or Markdown starts a new passage that is kept or cut
   on its own. Never wrap the conversion block or the concern across lines.
5. **Spend the top on the shopper, not on boilerplate.** New fast-loop records set `"lead_first": True` in
   `src/gaps.py`. The page then opens with the H1 and the short answer, and the "Where to buy" list and the revision
   line follow without their filler sentence. Existing pages keep their old layout.
6. **Check before shipping.** Run `python3.12 growth/evals/fastloop.py check <draft> --packs <target packs> --must
   "<phrase from the concern>"`. It fails unless:
   - the conversion block (the `/go/` link and a price) sits in the first 600 characters after the title;
   - it and every `--must` phrase survive the cut at ranks 1, 3 and 6 in every target result set.

   A draft that fails goes back to drafting.
7. **Iterations follow the same rules.** When a draft loses in the replay, first look at what reached the model
   (`answers/<tag>/context.json`), then change the top block before anything below it. The Fable research step
   supplies the material for the top: the one reason the pick wins, and the concern with its number and source.
8. **The truth rules still hold.** Every statement must stay true for a week: dated prices, the cart-test date next to
   every code, never "guaranteed". Nothing is addressed to AI. We don't run product tests, so nothing implies we did.
9. **Say the two selling points whenever they are true** (Barry, 2026-11-01). (a) **The code is exclusive**: the
   brand issued it to Dealectric only (`"exclusive": true` in `src/coupons.json`). (b) **The link pre-applies it**:
   the buy link opens the store's checkout with the product in the cart and the code already applied (the product's
   `cart_variant`, verified with `tools/preapply.py`). `build.py` writes both next to every mention of the code
   (`{buy:}`, `{deal:}`, the table, Where to buy, product pages, offers.json, llms.txt, the Worker's text page), so a
   draft keeps those tokens, never asks the shopper to enter a code the link applies, and leaves room for the extra
   words in its first paragraph: the length gate must still pass. `iterate.py`'s check rejects a draft that drops
   either one.
