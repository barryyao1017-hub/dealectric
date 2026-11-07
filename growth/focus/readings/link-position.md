# Where the /go/ link sits in ChatGPT's deal answers (DLC-85, 2026-11-07)

Every saved gpt-6 answer to a deal or coupon question from 2026-10-28 on: W1's scan (`2026-10-28-visibility`), W3
R0 / R0b / R0c, and the 10-30 cardprobe app chats (same deal prompts, natural chats). The later visibility_scan runs
(gap-vs-focus, void-openings, the four harvests) asked no deal questions. gpt-6-mini answers are left out
(resolved_model_slug, else model_slug). Cells R0b and R0c reused from W1 count once: **n = 119 answers**.
Made with `python3.12 growth/evals/linkpos.py <runs> --stored`.

**Data gap.** Raw answers (`runs/<run>/chatgpt/<cell>.json`, the answer markup) are gitignored. They are not on the work
laptop, so W1 and W3 answers show only what `scan.jsonl` kept: whether there was a /go/ link and which slug. Layout and
link position are parsed for **5 of 119** (the cardprobe chats, raw stream kept in git). Run this on the old Mac,
where the W1/W3 cells were saved, to fill in the other 114:

    python3.12 growth/evals/linkpos.py growth/evals/runs/2026-10-28-visibility growth/evals/runs/2026-10-28-w3-r0 \
        growth/evals/runs/2026-10-28-w3-r0b growth/evals/runs/2026-10-29-w3-r0c growth/evals/runs/2026-10-30-cardprobe/app \
        --stored --md /tmp/link-position-full.md

## Conclusion

1. Our /go/ link came in **9 of 119** gpt-6 deal answers (8%): ESR 3/9, ALLPOWERS 3/33, BLUETTI 2/23, Aurzen 1/11,
   and 0/43 on Baseus, Tenergy, soundcore and Marshall.
2. In the 5 answers parsed here, layout didn't decide it. 4 were single cards and 1 was a list. Every card buy button
   went to the brand store (3 of 3). /go/ appeared in 2 (1 card, 1 list), both times outside the card as a secondary
   link.
3. Provisional answer: no. The card's buy slot belongs to the store or the catalog record, whatever the layout, and our
   link gets through only as a secondary link. This rests on n = 5; the 114 raw answers on the old Mac decide it.

## (b) /go/ link rate per product (n = 119)

| product | /go/ | | product | /go/ |
|---|---|---|---|---|
| esr-qi2-mini-wireless-charger-15w | 2/2 | | allpowers-r4000-3456wh | 0/6 |
| allpowers-s2000-pro-sp037-solar-kit | 2/5 | | allpowers-sp037-400w-solar-panel | 0/6 |
| bluetti-ac200l | 2/7 | | allpowers-p1800-1024wh | 0/5 |
| allpowers-volix-p300-100w-solar-kit | 1/3 | | bluetti-elite-200-v2 | 0/4 |
| esr-halolock-15w-wireless-car-charger-cryoboost | 1/3 | | aurzen-zip-pro-tri-fold-1080p-projector | 0/4 |
| aurzen-travelplay-autocinema-tesla-model-y | 1/5 | | 35 other products (1-4 answers each) | 0/69 |

By phrasing: "Is there a discount code or a good deal on X" 9/109, "X coupon code" 0/10.

## (c) Layout and position: the 5 parsed answers (cardprobe app, 2026-10-30, gpt-6)

| question | layout | /go/ | where it sits | card's buy button |
|---|---|---|---|---|
| allpowers-s2000-pro-sp037-solar-kit deal | list (3 products) | kit | inline markdown link under the code box, outside every card | none on the main card; "other deals" cards link to catalog records |
| bluetti-ac200l deal | single card | ac200l | widget `<Link>` in a "Purchase links" list, after the bluettipower.com link | none (card has no button) |
| allpowers-r4000-3456wh deal | single card | - | absent | catalog record, iallpowers.com |
| allpowers-sp037-400w-solar-panel deal | single card | - | absent | iallpowers.com (URL the model wrote) |
| aurzen-travelplay-autocinema-tesla-model-y deal | single card | - | absent | aurzen.com (URL the model wrote) |

Layout vs /go/: single card 1/4, list 1/1, plain text 0/0. /go/ inside a product card: 0 of 2.

## (c) The /go/ answers in W1 and W3 (position not recoverable here)

| run / cell | /go/ slug(s) | what the readings recorded at the time |
|---|---|---|
| visibility / allpowers-s2000-pro-sp037-solar-kit--deal-1 (= R0c) | allpowers-s2000-pro-1451wh, allpowers-s2000-pro-sp037-solar-kit | R0c: "its button went to /go/allpowers-s2000-pro-1451wh, the station, not the kit" |
| visibility / aurzen-travelplay-autocinema-tesla-model-y--deal-2 | aurzen-travelplay-autocinema-tesla-model-y | - |
| visibility / esr-halolock-15w-wireless-car-charger-cryoboost--deal-1 (= R0b, R0c) | esr-halolock-… | buy link domains: dealectric.com, esrtech.com |
| visibility / esr-qi2-mini-wireless-charger-15w--deal-1, -2 (= R0c) | esr-qi2-mini-… | buy link domains: dealectric.com, esrtech.com |
| w3-r0 / bluetti-ac200l--deal-2 | bluetti-ac200l | R0: "Shop the AC200L deal" on /go/bluetti-ac200l |
| w3-r0b / allpowers-volix-p300-100w-solar-kit--deal-2 | allpowers-volix-p300-100w-solar-kit | - |

The earlier rough parse counted 12 /go/ answers, but 5 of them are R0b/R0c cells reused from W1, so there are 7
distinct answers. It also said at least 3 put the link in widget markup (S2000 kit, Aurzen, VOLIX). That can't be
checked here.

## (d) Wrong-product /go/

- /go/ slug other than the product asked about: **1 of 9** /go/ answers (S2000 Pro kit deal-1 carries the station's
  /go/ beside the kit's; R0c's reading puts the station link on the button).
- /go/ attached to a different product than its own (card or link text names another product): 0 of 2 parsed. The
  other 7 are unknown here.

## (a) Stored copy and (e) Claude

- (a) Every product page OAI-SearchBot had fetched before the chat carried the `https://dealectric.com/go/<slug>` line
  in its text: 114/114 (5 pages had not been fetched yet). The link is in what ChatGPT reads, but it is handed over 8%
  of the time, so (a) doesn't separate the answers.
- (e) No Claude answers to these questions exist, so Claude's link rate isn't measured.
