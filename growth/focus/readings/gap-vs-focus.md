# Gap pages vs focus pages: category-question discoverability (2026-10-30)

Barry's question after the first sale (DLC-33): is the gap page more discoverable than the focus pages?
Questions: `growth/focus/gap-vs-focus-questions.json` (11 shopper questions, none naming Dealectric or a model), n=2,
signed in (Free), temporary chats, `visibility_scan.py` driver and tiers. Run `growth/evals/runs/2026-10-30-gap-vs-focus/`,
22 cells, all answered by gpt-6, no downgrades.

Tiers: T5 our `/go/` link, T4 our page linked or as a source pill, T2 our page in ChatGPT's results only, T1 absent.

| Arm | Pages | OpenAI's last fetch | T5 | T4+ | T2+ |
|---|---|---|---|---|---|
| gap (solar kits) | /solar-generator-with-panels-included | 10-29 07:12Z (first ever) | 1/6 | 4/6 | 5/6 |
| query (comparison) | /power-station-for-cpap, /solar-watts-to-recharge-power-station | 10-29 07:12Z | 0/4 | 1/4 | 1/4 |
| focus (category) | AC200L, R4000, SP037, P1800 product pages | 10-26 | 0/8 | 0/8 | 0/8 |
| gap, never crawled | /best-power-banks-for-flying, /tesla-model-y-back-seat-screen | never | 0/4 | 0/4 | 0/4 |

Gap vs focus, one-sided Fisher exact: T4+ 4/6 vs 0/8, p = 0.015; T2+ 5/6 vs 0/8, p = 0.003.

## What the answers show

- `gap-solar--budget-1` ("Best solar generator kit with panels for under $1,000?") reproduced the sale's path: two
  product cards whose buttons are our links, "See bundle" -> `/go/bluetti-ac180-200w-solar-kit?utm_source=chatgpt.com`
  and "Check current bundle" -> `/go/allpowers-p1800-sp037-solar-kit?utm_source=chatgpt.com` (the P1800 kit at $658
  "after promotional code", source Dealectric). Same URL shape as the buyer's six clicks.
- When the solar page was in the results it ranked #1 or #2 (5 of 5).
- The camping phrasing missed both times: ChatGPT searched "portable power station solar panel kit/bundle for
  camping" and our page wasn't retrieved. The page's wording is "solar generator with panels included"; the
  retrieval follows the query's words.
- Focus category questions: our pages were not even in the results (0/8). ChatGPT's queries ("best 1kWh LiFePO4
  portable power station under $500 2026", "best 400W portable folding solar panels") return listicles and stores; a
  single-product page doesn't match a "best X" query.
- Never-crawled gap pages: 0/4, as expected. Crawling is the gate; the page shape only matters once OpenAI has it.
- CPAP comparison page: cited once (rank 4), absent once. Informational query, weaker match.

## Limits

n=2 per question, one day, one account. Product-named focus questions were not re-run (W1/W3: T4+ 30/48, T5 2/48,
from the 10-26 copies). The focus pages' W3 changes are not in OpenAI's copy yet (no re-fetch since 10-26).
