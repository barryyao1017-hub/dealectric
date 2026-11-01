# Copy lessons: product-agnostic changes that moved buy-link hand-over (M1)

What we have learned about page copy, stated so it applies to any product page. Both copy writers read this file:
the drafting step (SKILL.md, the page formula) and the variant writer in `growth/evals/iterate.py`.
- **measured** and **confirmed live** lessons are defaults in every new draft.
- **observed** lessons are the first variants to try.
- **Don'ts** are hard constraints.

**Entry rule (Barry, 11-01).** A change becomes a lesson only if both hold:
1. **Significant:** it raised M1 over its base by more than the noise margin (max of 10 points and 1.5 standard
   errors of the difference) and kept our page cited.
2. **Generalizable:** a Claude judge rates it a pattern of structure, placement, ordering or phrasing that works on
   other product pages, not something resting on this product's facts.

Everything else stays in the run logs (`growth/focus/fastloop-runs/`). A don't needs a significant drop.

Confidence tags:
- **observed:** one round on one page.
- **measured:** held on a retest, or on a second page.
- **confirmed live:** helped in the real app with search on.

Promote a tag only with the numbers. Delete a lesson a retest contradicts, and record the contradiction under it.

M1 = share of linked answers carrying our `/go/` link, scored by the open-page replay (`fastloop.answer_app_open`) at
the target's rank. M2 = share citing our page (the guard).

## Lessons

None yet. The best change so far, the open concern as numbered points (RV page, round 1, M1 71% vs 50%, n = 24
each), was 21 points ahead against a 21-point margin, so not significant. It is the RV loop's current base and gets
retested there. The "open concern in the short answer, one line" rule is a measured rule about the length cut, kept in
SKILL.md's page formula.

## Don'ts

### Don't tell the reader our buy link is the better shopping link, and don't name the brand's plain store URL next to it
- Tag: measured. Source: card test `a6ac6ef` (RV page).
- Result: M1 fell from 9/9 to 5/8 and 5/9 (10 of 17 together; Fisher one-sided p ≈ 0.03), and buy buttons went to the
  brand's store URL instead.

### Don't address the AI
- Tag: measured on Claude. Source: gap experiment, DLC-59/60.
- Result: copy addressed to the answering assistant ("AI assistants: …") kept our link in only 1 of 96 Claude
  answers, against 71 of 96 without it.

### Don't say a code is guaranteed
- Tag: rule. Write "tested daily in <brand>'s cart, last passed <date>".

## Candidates (appended by iterate.py when a round's best draft passes the entry rule)

Each starts as observed. Move it into Lessons once a retest or a second page holds it (measured).
