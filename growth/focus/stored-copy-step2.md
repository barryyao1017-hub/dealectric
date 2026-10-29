# DLC-77 step 2: copy that survives OpenAI's stored copy (draft, not shipped)

Measured in `growth/focus/stored-copy.md` (step 1): ChatGPT's result title for a page is the `<title>` that was live
at OAI-SearchBot's last fetch of it (291 of 292 chats that showed a superseded version; Bingbot's last fetch fits 1 of
117). OAI-SearchBot has fetched each focus page once, on 2026-10-26 21:3xZ. So whatever the title and snippet say is
read for days, and sometimes a week, after we change it. Snippets themselves were never saved before 2026-10-28;
`ui.py` keeps them from now on, so which text the snippet comes from (meta description or the first paragraph) is
not known yet. The draft therefore puts the same deal sentence in both.

## Snippets, measured 2026-10-29 (`canary.md`, Result)

Each result carries the title and one passage of about 200 characters, picked for the query from the whole crawled
page. Product-page deal and worth questions got the opening of the body: breadcrumb, H1, the summary line, the start
of the offer card. The meta description did not show. On the AC200L that opening is "same price as the Elite 200 V2",
an undated comparison. So for product pages the place to put the deal is the H1 and summary line, and on the catalog
and codes pages every card is its own passage.

## What the stored copy holds (checked 2026-10-28, after the draft below)

More than the title and the first 200 characters. On 10-28 a ChatGPT answer to "what is dealectric.com" relayed the
About page's "Who" line ("operated by Barry Yao, a machine-learning engineer based in Sunnyvale"), which sits about
1,060 characters into the page and is in neither the title nor the description. No OpenAI agent had requested /about
since OAI-SearchBot's one fetch on 10-21 (crawl log, all user agents), so the text came from the stored copy of
that crawl. An Aurzen answer relayed a caveat from about 5,700 characters in ("the rear panel does not fully cover the
window"), but a ChatGPT-User fetch 23 h earlier could also explain that one. Most likely the index keeps the page
text and the result hands the model a passage picked for the query, not a fixed opening. That is a reading of two
cases, not a measurement: the snippets ui.py now saves will show which passage each query gets.

Separately, a page ChatGPT-User fetched live is reused by the next chats for a few minutes: four NiMH-page answers
quoted its caveats with no fetch of their own, 3-4 minutes after one.

So the draft below (title plus opening) is necessary but not sufficient: each section a query could pick (the offer
card, "who it's for", caveats) should carry the code, the dated price and what the link does on its own.

## Statements on the focus pages that go false as the copy ages

| page | statement | goes false when | in the title / description now |
|---|---|---|---|
| `/allpowers-r4000-3456wh` | "$1,319.12 with code EXTRA12" | EXTRA12 ends 2026-11-15; a copy fetched before then keeps saying it | title and description; only the body says "Expires 2026-11-15" |
| `/bluetti-ac200l` | "$854.05 with code AFF5OFF", buy link to the AC200L | BLUETTI stops selling the AC200L (the Apex 200 replaces it in early November) | title and description; the phase-out is only in the body |
| all five | "$X with code Y" in the title, undated | the store price moves between OAI crawls | title (the description dates the cart pass, not the price) |
| `/bluetti-ac200l` | lead: "same price as the Elite 200 V2" | either price moves | first sentence of the page |

Everything else in the first 200 characters is dated ("last passed <date>") or stays true ("tested daily", as long as
the sweep runs).

## Draft (title, then the description, which would also open the page as its first paragraph)

The cart pass re-reads the price in the brand's cart every day, so "in the cart on <date>" dates the price too.

**A, `/bluetti-ac200l`**
- Title: `BLUETTI AC200L Portable Power Station: $854.05 with code AFF5OFF, tested daily · Dealectric`
- Description: `$854.05 with code AFF5OFF (5% off $899 at BLUETTI's US store) while BLUETTI's stock lasts. Tested daily in BLUETTI's cart, last passed 2026-10-28. Our link opens BLUETTI's checkout with the AC200L in the cart and AFF5OFF applied.`

**B, `/aurzen-travelplay-autocinema-tesla-model-y`**
- Title: `Aurzen TravelPlay AutoCinema Screen for Tesla Model Y: $108 with code CJ10, tested daily · Dealectric`
- Description: `$108 with code CJ10 (10% off $119.99 at Aurzen's US store). Tested daily in Aurzen's cart, last passed 2026-10-28. Our link opens Aurzen's product page; enter CJ10 at checkout.`

**C, `/allpowers-r4000-3456wh`**
- Title: `ALLPOWERS R4000 Portable Power Station: $1,319.12 with code EXTRA12 to Nov 15, tested daily · Dealectric`
- Description: `$1,319.12 with code EXTRA12 (12% off $1,499 at ALLPOWERS' US store) until 2026-11-15; after that ALLPOWERS26 takes 10% off. Tested daily in ALLPOWERS' cart, last passed 2026-10-28. Our link opens ALLPOWERS' product page; enter the code at checkout.`

**D, `/allpowers-p1800-1024wh`**
- Title: `ALLPOWERS P1800 Portable Power Station: $395.10 with code ALLPOWERS26, tested daily · Dealectric`
- Description: `$395.10 with code ALLPOWERS26 (10% off $439 at ALLPOWERS' US store). Tested daily in ALLPOWERS' cart, last passed 2026-10-28. Our link opens ALLPOWERS' product page; enter ALLPOWERS26 at checkout.`

**E, `/allpowers-sp037-400w-solar-panel`**
- Title: `ALLPOWERS SP037 400 W Foldable Solar Panel: $269.10 with code ALLPOWERS26, tested daily · Dealectric`
- Description: `$269.10 with code ALLPOWERS26 (10% off $299 at ALLPOWERS' US store). Tested daily in ALLPOWERS' cart, last passed 2026-10-28. Our link opens ALLPOWERS' product page; enter ALLPOWERS26 at checkout.`

Only arm A's link applies the code today (A-L2). "Opens the checkout with the code applied" on B-E would be false until
their L2 ships (DLC-53), so B-E say what the link does now. When an arm's L2 ships, its sentence changes with it.

The numbers and dates are generated (build.py fills them from products.py and coupons.json), so the sweep keeps them
current; the format is what this step changes.

## Why it isn't shipped yet

Every focus page has 5-6 versions waiting for the next OAI-SearchBot fetch (A-L2, B-L1, the ALLPOWERS fact fixes and
DLC-76). Whatever ships before that fetch enters the index in the same crawl, so it can't be told apart from the lever
in force on that arm. The choice is Barry's (see the DLC-77 report).
