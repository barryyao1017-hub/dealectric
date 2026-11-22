# Cluster run, 2026-11-21 (DLC-343): keyboards, dash cams, laptop screen extenders

Barry, 2026-11-21, after the read of the week's sales: the three non-solar clusters with a sale each (Mobile Pixels
11-15, ESR 11-20, Gamakay 11-21) get new pages. Brief: 20 candidate questions per cluster in the mix 10 by size or
budget, 4 brand-launch, 4 "best X for Y", 2 question pages; the harvest gate decides which become pages, with a floor
of twelve pages per cluster ("Gate the size, but let's put a floor of twelve pages").

- `clusterpages.py`: the page driver (tools/abpage.py through growth/focus/open-pages/openpage.py, with this run's
  rules, a table of the products we link per cluster and the partner stores' other products). `keep.json` lists the
  questions that became pages.
- `harvest_read.py [k1121|d1121|x1121] [--full] [--json f]`: what ChatGPT did with each harvest question.
- `stores-2026-11-21.json`: the seven partner stores' products with no record, read that day.
- `publish.sh`: merge origin/main, rebuild, push; retried when main moves during the build.
- Questions: `growth/focus/ab-harvest-new-2026-11-21-clusters.json` (60 questions, 2 plain gpt-6 chats each, run
  `2026-11-21-clusters-harvest`; chat files are local only, each kept page's `growth/focus/ab/<folder>/harvest.json`
  carries its chats). Folder prefixes: `k1121-` keyboards, `d1121-` dash cams, `x1121-` extenders. Each question's
  `ptype` (size, brand:<partner>, bestfor, question) goes onto the page record as `"ptype"`, so a later reading can
  split visits by page type.

## Prices (Barry: the store's Black Friday price, less our code, always the lowest price the shopper can pay)

Read 2026-11-21. One cart test per code-carrying brand on a sale-priced product, to see whether the code stacks:

| Partner | Sale | Our code on sale prices | What the pages show |
|---|---|---|---|
| Gamakay | Black Friday, Nov 19-30, prices cut in the store | GK10, New, GK12 all rejected | the sale price, no code; codes marked rejected until 12-01 (DLC-344) |
| Lofree | "Black Friday Month": 20% off keyboards, taken off in the cart; the product page shows the old price | no code | page price plus the checkout total (`deal.auto_total`) |
| Vantrue | Black Friday prices in the store | no code | the sale price |
| DDPAI | Black Friday Mega Sale, Nov 16-30 | SAVEBIGBF, further 12%, passed ($269 -> $236.72), ends 11-30 | sale price less the code |
| Botslab | Black Friday Deals; the site prints BF15 (15%) | AA18, 18%, passed ($234.99 -> $192.70) | sale price less AA18 |
| Mobile Pixels | "up to 60% off"; three screens went UP $40 between 11-18 and 11-21 | no code | the store price of the day |
| FOPO | no change | FOPO, 10%, passed ($199.99 -> $180.00) | store price less the code |

Without the stacking check the pages would have shown a Gamakay price nobody can get ($71.27 for a $79.19 board) and a
Lofree price $31.80 too high. Record changes and six prose corrections on existing pages went out the same evening
(a5d5ce36, b92e958b): the under-$400 triple extender page now picks the FOPO S7 while the Trio 3 Pro is $407.99.

## What existed before the run (D1, 11-12..11-21)

- Keyboards: 7 pages, 8 records. /silent-hall-effect-keyboard 9 ChatGPT visits, 7 Gamakay clicks, 1 sale (11-21).
- Dash cams: 2 pages, 5 records. /best-4-channel-dash-cam 10 visits, 1 click, no sale.
- Extenders: 10 pages, 9 records. 11 Mobile Pixels clicks, 1 sale (11-15); the 11-18 run's reading is due 12-02.
