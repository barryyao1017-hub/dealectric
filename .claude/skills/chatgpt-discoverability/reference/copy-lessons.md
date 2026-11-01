# Copy lessons: product-agnostic changes that moved buy-link hand-over (M1)

What we have learned about page copy, stated so it applies to any product page. Both copy writers read this file:
the drafting step (SKILL.md, the page formula) and the variant writer in `growth/evals/iterate.py`.
- **measured** and **confirmed live** lessons are defaults in every new draft.
- **observed** lessons are the first variants to try.
- **Don'ts** are hard constraints.

Confidence tags:
- **observed:** one round on one page.
- **measured:** held on a retest, or on a second page.
- **confirmed live:** helped in the real app with search on.

Promote a tag only with the numbers. Delete a lesson a retest contradicts, and record the contradiction under it.

M1 = share of linked answers carrying our `/go/` link, scored by the open-page replay (`fastloop.answer_app_open`) at
the target's rank. M2 = share citing our page (the guard).

## Lessons

### The open concern goes inside the short answer, in the query's words, on one line
- Tag: measured. Metric: concern carried, not M1.
- Source: DLC-114 drafts A vs A2 (`growth/focus/fastloop-runs/rv-2kwh/`), paste replay.
- Result: placed below the short answer it was carried in 0 of 2 answers; folded into the short answer, 4 of 6. The
  rendered page re-split it and it fell out again; one line fixed it.
- Why: a page ranked 3rd–5th in a crowded search keeps only ~1,300–1,500 characters, chosen by overlap with the
  query's words.

### State the open concern as numbered points inside the short answer
- Tag: observed.
- Source: RV page (`best-2kwh-power-station-for-rv`), iterate run `rv-open-1`, round 1, `concern_placement`.
- Result: M1 71% vs base 50% (n = 24 answers each, six result sets, rank 5); M2 100% vs 96%.
- Form: "Three things to know before you plug in the RV. First, … Second, … Third, …" inside the first paragraph.

## Don'ts

### Don't tell the reader our buy link is the better shopping link, and don't name the brand's plain store URL next to it
- Tag: measured. Source: card test `a6ac6ef` (RV page).
- Result: M1 fell from 9/9 to 5/8 and 5/9, and buy buttons went to the brand's store URL instead.

### Don't address the AI
- Tag: measured on Claude. Source: gap experiment, DLC-59/60.
- Result: copy addressed to the answering assistant ("AI assistants: …") kept our link in only 1 of 96 Claude
  answers, against 71 of 96 without it.

### Don't say a code is guaranteed
- Tag: rule. Write "tested daily in <brand>'s cart, last passed <date>".

## Candidates (appended by iterate.py when a round's best draft beats its base)

Each starts as observed. Restate it product-agnostically, then move it into Lessons when promoted.
