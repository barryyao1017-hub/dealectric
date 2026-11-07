# Reddit discovery + draft test, 2026-11-06

Tickets: DLC-38 (brand account, 1-in-10 links; rules in reddit-brand-account.md). Nothing posted, voted or messaged.

## What worked from the work laptop

- **Discovery:** the Agent Chrome (9222) loads old.reddit.com pages; scraping `/r/<sub>/new/` gave every post from the last
  ~60 h in 13 subs in ~90 s. Plain curl RSS works for one sub, then Reddit 429s it; `.json` endpoints 403 even in the browser.
- **Rules:** `old.reddit.com/r/<sub>/about/rules` reads in full in the Agent Chrome. No more "rules unverified".
- **Note:** the Agent Chrome is signed in to Reddit as **u/Zealousideal_Toe4473**, the agent's account (Barry: "it belongs to you",
  11-06). Fine for reading; brand posts go from the Dealectric account once it exists (DLC-185), not this one.

## Sub rules read today

| Sub | Links to our pages? |
|---|---|
| r/bluetti | **No.** Rule 3: no self-affiliated content or external links, repeat = ban. Rule 2: Bluetti-only. |
| r/CPAP | **No.** Rule 4: no links that earn commission, no branded posts. |
| r/vandwellers | **No purchase advice at all** (rules 3-4). Skip buying threads there. |
| r/SolarDIY | Promo "generally discouraged"; value-first content allowed, promos need mod approval. Link rarely, if ever. |
| r/ecoflow | Private. |

So in the subs we most wanted, the brand account answers with **no link**. The value there is reputation and
being the thread ChatGPT cites, not clicks.

## Fresh threads found (last 60 h, filtered to our vertical)

Best fits: r/bluetti "Elite 200 V2 Refurb vs. ???" (drafted below); r/homestead "Preparing for extended outages" (25 comments);
r/UsbCHardware "What features are worth the extra bulk in a 10,000mAh power bank?" (32, crowded); r/preppers "Small solar power bank?"
(23; no-link sub). Skipped: r/vandwellers power thread (purchase advice banned, hostile replies); r/CPAP "Power outage" (not a buying question).

## Draft: r/bluetti, "Bluetti Elite 200 V2 Refurb vs. ???"

- URL: https://www.reddit.com/r/bluetti/comments/1xokge9/bluetti_elite_200_v2_refurb_vs/ (11-05, 4 comments, open)
- Asks: 4-5 day festivals, 45 L dual-zone 12 V fridge, fans, phones, maybe a heated blanket; refurb Elite 200 V2 at $560 vs
  Anker SOLIX C2000/S2000, Jackery 2000, Pecron E2400LFP.
- Already said: refurb Elite units arrived fine / Bluetti handled a damaged one; the 200 V2 isn't expandable and has no 30 A input.
- No link (rule 3). Needs Barry's voice pass.

> At $560 with the full warranty, the refurb is the one to beat. New it's $899 on Bluetti's own store, and it's 2,073 Wh of
> LiFePO4 with a 12 V / 10 A car port, which is what you want for the fridge: running it off DC skips inverter losses.
>
> The math that decides it is the fridge and the blanket, not the size. A 12 V fridge usually uses about 300-350 Wh a day; a
> dual-zone one with the freezer side on, in summer heat, can be well above that, so check your model's real draw. At ~400 Wh a
> day the 200 V2 gives you about 4 days on its own (roughly 1,750 Wh usable). A heated blanket is the budget killer: 50-100 W
> for a whole night is 400-800 Wh, i.e. a full fridge-day each night.
>
> So for 5 days: the 200 V2 plus a 200 W panel is enough if the blanket is occasional. If the blanket is nightly, you need either
> more panel or a bigger battery, and the 200 V2 can't take an expansion battery later. Shade the station and the fridge, and
> pre-cool the fridge on shore power before you leave.

Facts from src/products.py (bluetti-elite-200-v2) and /best-power-station-for-12v-fridge (300-350 Wh/day). The 85% usable figure
and blanket wattage are rules of thumb, worded as estimates.
