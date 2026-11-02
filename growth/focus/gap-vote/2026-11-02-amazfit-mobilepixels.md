# Gap vote (2026-11-02): Amazfit and Mobile Pixels leads

The five clusters that the Claude screen called open (`growth/focus/funnel-amazfit/screen.md`,
`growth/focus/funnel-mobilepixels/screen.md`), two packs each. Each pack: `fastloop.py pack --engine api`, one pinned
OpenAI web search on the predicted ChatGPT query, 12 results, pages read over plain HTTP. The Chrome fallback was off
because Barry was using the laptop, so a few bot-walled pages are empty. Then `fastloop.py vote` (v2 prompt; Sonnet
5.5 / Opus 5.5 / Fable 5.1). Packs and per-model verdicts are in `growth/evals/runs/fastloop/<name>/`. Not yet
confirmed in the app (funnel step 6).

| pack | ChatGPT-style query (API, pinned) | votes | verdict | our pick |
|---|---|---|---|---|
| mpx-triple-1 | best triple screen laptop extender 2026 MacBook Air one external display DisplayLink | open/open/open | **open** | Trio 3 Pro $433.49 |
| mpx-triple-2 | best laptop screen extender 2026 MacBook Air two extra screens | open/open/contested | **open** | Trio 3 Pro $433.49 |
| mpx-stack-1 | best dual screen laptop extender 2026 stacked vertical 16 inch laptop | open/open/open | **open** | Duex Float 2 Pro $263.49 |
| mpx-stack-2 | best portable monitor 2026 that sits above laptop screen | open/open/contested | **open** | Duex Float 2 Pro $263.49 |
| amz-golf-1 | best golf GPS watch 2026 free course maps no subscription heart rate sleep tracking | contested ×3 | **contested** | Balance 2 $299.99 |
| amz-golf-2 | best golf smartwatch 2026 everyday fitness tracking under $300 | open/open/open | **open** | Balance 2 $299.99 |
| amz-iphone-1 | best smartwatch 2026 long battery life iPhone compatible two weeks under $200 | open/open/open | **open** | Active Max $169.99 |
| amz-iphone-2 | best smartwatch for iPhone 2026 week+ battery AMOLED fitness tracking | open/contested/contested | **contested** | Active Max $169.99 |
| amz-hyrox-1 | best watch for HYROX 2026 HYROX race mode budget under $150 | open/open/open | **open** | Active 2 $99.99 |
| amz-hyrox-2 | best budget fitness watch 2026 HYROX training race mode | open/open/open | **open** | Active 2 $99.99 |

8 open, 2 contested, none saturated. Quotes checked: 9–12 of 12 per judge (the misses are pages with no readable
text).

## What's missing (Opus, shortened)

- **Triple screen on a one-display MacBook:** a tested, chip-by-chip list of triple extenders that run both side
  screens with the lid open on an M1–M4 Air, naming the driver or cable each needs, with current prices.
- **Stacked above the laptop:** stacked monitors (Duex Float, UPERFECT Delta and others) compared on lid size and
  stand height for a 16" laptop, single-cable power and video, prices, and one pick. Note: the "sits above" search
  returned the full authority set (Tom's Guide, RTINGS, Wired, Tom's Hardware), and it still came out open because
  none of them answer the stacked question.
- **Golf + everyday fitness under $300:** watches good at both (Vivoactive 6, Approach S44/S50, Balance, Shot Scope),
  with subscription costs and a pick. The stricter "free course maps, no subscription" search was contested.
- **iPhone, 14+ days, under $200:** only iPhone-compatible watches, battery in real use, what you lose on iPhone.
  The broader "weeks of battery" search was contested.
- **Budget HYROX:** under-$150 watches with a native HYROX race mode (Bip 6, Active 2) compared on indoor tracking
  and stations, with a pick. Results are mostly small HYROX blogs.

## Reading

- The judges lean open on narrow queries. The real test is the app check: whether ChatGPT itself searches these
  phrasings (step 6, in the agent's Chrome).
- **The open gaps don't fix the price problem.** Neither brand has a code. Amazon often lists Amazfit below the store
  we link (Active Max $139.99 vs $169.99 on 10-06; Balance 2 $219–249 vs $299.99), so a card-comparison page would
  show our link as the dearer one. Mobile Pixels' store sale prices are the lowest we saw, but they weren't checked
  against Amazon.
- HYROX: Amazfit is HYROX's paid partner, so a "best HYROX watch" pick of an Amazfit needs that disclosed.
- Ranked for a page: triple screen (strongest gap, highest price, most demand) > stacked > HYROX > iPhone battery >
  golf.
