"""Buy boxes for the W3 focus products (growth/first-sale-plan.md W3, lever 1; design in growth/focus/loop-design.md).

One entry per product slug. build.py's offer_block puts it at the top of the product page's offer card: the three proof
points, the price after the code with its cart test date (from coupons.json, as on every page), the one buy button to
/go/, then "pick it if / skip it if". Copy comes from W2's dossier (growth/focus/<slug>/dossier.md, copy kit); every
fact is dated or labelled as our estimate. Nothing here is addressed to AI assistants: that is a separate lever.

Placeholders filled by build.py: {code}, {after} (price after the code), {price}, {date} (last cart pass), {verified}
(price check date), {stock} ("in stock" or "sold out" as our record has it), {ends} (", code ends <date>" or "").
Fields: headline, proof (3, may hold <strong>), a note line (all_in, or note = (label, text)), pick, skip,
rivals_checked (the date other brands' prices in skip were read).
"""

BUYBOX = {
    # W3-aurzen-travelplay-autocinema-tesla-model-y-L1, 2026-10-28. Dossier: growth/focus/aurzen-travelplay-autocinema-tesla-model-y/dossier.md
    "aurzen-travelplay-autocinema-tesla-model-y": {
        "headline": "A 47-inch movie screen for the parked 2025–26 Model Y: {after} with code {code}, last passed in Aurzen's cart {date}",
        "proof": [
            "<strong>A 46.6-inch picture</strong> fits the rear panel, about 34 times the area of the Model Y's 8-inch rear screen "
            "(our arithmetic, 16:9; the full size needs tailgate mode or a roof-mounted projector).",
            "<strong>{after} with code {code}</strong>, about what Tesla charges for its glass-roof sunshade alone ($105 on 2026-10-28), "
            "and this one is also a movie screen.",
            "<strong>A two-hour movie with Camp Mode on uses about 2–3%</strong> of a Long Range battery in mild weather "
            "(our estimate from owner and press measurements; about 5% near freezing).",
        ],
        "all_in": "It needs a projector: with Aurzen's ZIP ($199.99) the whole setup is about $308. Best after dark: "
                  "a 100–200 lumen projector washes out in a sunny cabin.",
        "pick": [
            "You have a 2025–2026 Model Y with the see-through glass roof (Premium, Performance).",
            "You watch parked, after dark: campsites, long charging stops, tailgates.",
            "You'd buy a roof shade anyway: the silver side faces the glass.",
            "You own or will buy a ZIP-class projector that focuses at about 1 m.",
        ],
        "skip": [
            "The kids watch while you drive. Aurzen says parked only. Use the Model Y's built-in 8-inch rear screen (Premium, "
            "Performance, Y L; Bluetooth headphones) or a tablet on a headrest mount (about $95 with a Fire HD 8 Kids and "
            "TESERY's $19.99 mount).",
            "You drive a Model Y Standard, a Model Y L or a Model 3: Aurzen doesn't list them. On a 2020–2024 Model Y only roof "
            "mode works (2022–2024 per Aurzen's Spanish manual).",
            "You want daytime viewing: no battery projector beats a sunny cabin.",
            "You only want shade: a Juniper roof sunshade costs $49.99 (Basenor) to $105 (Tesla).",
            "You only want outdoor tailgate movies: Aurzen's 120-inch portable screen ($24.99) gives a far bigger picture.",
            "It's new: on sale since 2026-08-17, with no owner reviews on aurzen.com as of 2026-10-28.",
        ],
    },
    # W3-allpowers-r4000-3456wh-L1, 2026-10-28. Dossier: growth/focus/allpowers-r4000-3456wh/dossier.md
    "allpowers-r4000-3456wh": {
        "headline": "3,456 Wh and 3,600 W for {after} with code {code}, last passed in ALLPOWERS' cart {date}{ends}",
        "proof": [
            "<strong>3,600 W on US 120 V outlets</strong>: a fridge, freezer, 1/2 HP sump pump, router and lights together "
            "for about 15 hours (our estimate).",
            "<strong>3,456 Wh for {after} with {code}</strong>, about 1.7 times the capacity of the 2 kWh stations most "
            "\"under $1,500\" lists recommend.",
            "<strong>Three solar inputs</strong>: three 400 W panels refill it in about 4–5 hours of good sun (our estimate).",
        ],
        "note": ("Before you buy", "On US outlets it charges at 1,500 W, about 2.5 hours; the 4,000 W in ALLPOWERS' title is the "
                 "230 V model. Register the warranty at iallpowers.com on day one (5 years if registered, 24 months if not) "
                 "and keep the box: returns need it unopened, and ALLPOWERS' refund policy excludes sale items."),
        "pick": [
            "You want one box for home outages that runs several big 120 V loads at once.",
            "You'll feed it from up to three portable panels.",
            "You won't add batteries: none is sold for it in the US.",
            "You'll register the warranty on day one and keep the box.",
        ],
        "skip": [
            "You might add batteries, want 240 V later or run high-voltage panel strings: the Pecron E3800LFP ($1,299, "
            "3,840 Wh, $799 add-on packs) expands. Pecron is the less established brand.",
            "It will sit as a UPS for a PC or NAS, or you want it 25 lb lighter: the EcoFlow DELTA 3 Ultra Plus ($1,599, "
            "under 10 ms switchover, expands to 11 kWh).",
            "One person must lift it into a car or up stairs (it weighs 99 lb): the Jackery HomePower 3000 ($1,499, 59.5 lb).",
            "Nothing you run together pulls more than 2,400 W: the BLUETTI Elite 300 ($1,099, 6,000 cycles, 41 lb lighter).",
            "You need 240 V for a well pump, dryer or central AC: the Anker SOLIX F3800 Plus ($2,599.99) or the EcoFlow "
            "DELTA Pro 3 ($2,799).",
            "It's for a food truck or job site: ALLPOWERS' warranty excludes commercial use.",
            "Fast warranty support matters more than price: ALLPOWERS' public record is weak (Trustpilot 2.2, BBB F).",
        ],
        "rivals_checked": "2026-10-28",
    },
    # W3-allpowers-p1800-1024wh-L1, 2026-10-28. Dossier: growth/focus/allpowers-p1800-1024wh/dossier.md
    "allpowers-p1800-1024wh": {
        "headline": "1,024 Wh and 1,800 W for {after} with code {code}, last passed in ALLPOWERS' cart {date}{ends}",
        "proof": [
            "<strong>{after} with {code}</strong>: the lowest price for a new, in-stock 1 kWh LiFePO4 station on the maker "
            "stores we checked on 2026-10-28 (EcoFlow, Anker, BLUETTI, Jackery, Pecron); the cheapest from EcoFlow, Anker "
            "and BLUETTI was $489.",
            "<strong>About 8 nights of CPAP</strong> (ResMed AirSense 11, no humidifier) from its 12 V port on one charge "
            "(our estimate).",
            "<strong>One 400 W panel refills it in about 4 hours</strong> of good sun (our estimate).",
        ],
        "note": ("Before you buy", "ALLPOWERS' US warranty page gives 24 months (its returns page says 18); register at "
                 "iallpowers.com and keep the box. It's new since June 2026, with one review on ALLPOWERS' US store; "
                 "Amazon's ratings belong to an older model."),
        "pick": [
            "You want a 1 kWh LiFePO4 station now for the least money.",
            "You'll charge it from one 400 W panel or the wall.",
            "You run laptops from its two USB-C ports (140 W max).",
            "You accept a 2-year warranty from a brand with weak support reviews.",
        ],
        "skip": [
            "You want a 5-year warranty from a known brand: the EcoFlow DELTA 3 Classic ($499; register it in EcoFlow's "
            "app for 3+2 years).",
            "You can wait for Black Friday: watch the Anker SOLIX C1000 Gen 2, which has sold for $349–399.99 at past "
            "sales (2,000 W, 5 years).",
            "You charge mainly from solar or want 1,000 W of panels: the BLUETTI Elite 100 V2 ($489, 5 years).",
            "You'll ever add a battery: the EcoFlow DELTA 3 Plus ($719, pre-order to late November, expands to 5 kWh).",
            "It's a UPS for a desktop PC: its 20 ms switchover (manual) isn't guaranteed to keep one on.",
            "You need a fridge and a heated CPAP through the night on solar: step up to a 2 kWh station such as the "
            "BLUETTI Elite 200 V2.",
        ],
        "rivals_checked": "2026-10-28",
    },
    # W3-allpowers-sp037-400w-solar-panel-L1, 2026-10-28. Dossier: growth/focus/allpowers-sp037-400w-solar-panel/dossier.md
    # The stock line rests on the cart test: tools/codesweep.py stops at a sold-out variant, so a pass means in stock.
    "allpowers-sp037-400w-solar-panel": {
        "headline": "A 400 W folding panel under $300: {after} with code {code}, last passed in ALLPOWERS' cart {date}{ends}",
        "proof": [
            "<strong>{after} with {code}</strong>, under half the price per watt of the 350–400 W folding panels from "
            "EcoFlow, Anker, BLUETTI, Jackery and Renogy, none of which was under $300 on 2026-10-28.",
            "<strong>About 320 W in real sun</strong>: the median of 24 owner reports, matching ALLPOWERS' own 260–320 W.",
            "<strong>One panel refills a 1 kWh station in about 4 hours</strong> of good sun; three refill the 3.5 kWh R4000 "
            "in about 4–5 hours (our estimates).",
        ],
        "note": ("In stock", "ALLPOWERS' US store had it in stock on {date}, when our code test added it to the cart. "
                 "ALLPOWERS' page code also carries a hidden \"Sold out\" label, which some summaries repeat."),
        "pick": [
            "You want the most solar watts per dollar.",
            "It rides in your car and you don't carry it far (18.5 kg for the version on ALLPOWERS' page).",
            "You set it out and pack it away rather than leave it up for weeks.",
            "Your station's solar input accepts at least 46 V (most 12–60 V stations do).",
        ],
        "skip": [
            "You carry it any distance or set it up alone: the Anker SOLIX PS400 Bifacial (9.9 kg, 5-year warranty, "
            "$599.99), or two ALLPOWERS SP033 200 W panels ($398, 6.3 kg each).",
            "It will live outdoors at camp for days in wind: the Renogy 400W Lightweight Suitcase ($495.99, aluminium "
            "kickstands, 3+2 years).",
            "Your station's input takes 15 A or more (BLUETTI Elite 200 V2, Elite 300) and you want fewer, lighter panels: "
            "ALLPOWERS' SP039 600 W ($489, 12.5 kg).",
            "Your station has a 12–28 V or 5–24 V input (BLUETTI Elite 30 V2, Tenergy T320): it won't work; buy a "
            "100–200 W 12 V-class panel.",
            "It's for a roof or a permanent mount: rigid panels carry 25-year output warranties and cost less per watt at "
            "volume.",
        ],
        "rivals_checked": "2026-10-28",
    },
    # W3-allpowers-s2000-pro-sp037-solar-kit-L1, 2026-10-29. Dossier: growth/focus/allpowers-s2000-pro-sp037-solar-kit/dossier.md
    # The two-item route (station + panel with BULKRATE) is cheaper than the kit; both items link through our own /go/.
    "allpowers-s2000-pro-sp037-solar-kit": {
        "headline": "2,400 W from a 13 kg station plus a 400 W panel: {after} with code {code}, last passed in ALLPOWERS' cart {date}{ends}",
        "proof": [
            "<strong>2,400 W from a 13 kg station</strong>: the most inverter per dollar of the solar generator kits near "
            "$1,000 we checked on 2026-10-29 ($0.36 per continuous watt as two items with BULKRATE).",
            "<strong>$857.07 as two items with BULKRATE</strong>: the <a href=\"https://dealectric.com/go/allpowers-s2000-pro-1451wh\" rel=\"sponsored nofollow noopener\">S2000 Pro</a> "
            "and the <a href=\"https://dealectric.com/go/allpowers-sp037-400w-solar-panel\" rel=\"sponsored nofollow noopener\">SP037 panel</a> added to "
            "ALLPOWERS' cart separately (our cart test 2026-10-29; code ends 2026-11-15), $9.63 less than the kit with {code}.",
            "<strong>One 400 W panel refills it in about 5–6 hours</strong> of good sun; two in series take about 3 on units "
            "made after mid-2024 (our estimates).",
        ],
        "note": ("Before you buy", "NMC battery rated 2,500 cycles: built for occasional use, not daily cycling. It's rated "
                 "2,000 W once the battery is below about 60%, so big loads run from the top of the charge. ALLPOWERS' kit "
                 "page text still describes an older 2× 200 W kit with an RV port."),
        "pick": [
            "You need 2,400 W from a station one person can lift: a microwave, kettle, saw or sump pump.",
            "You'll use it occasionally (camping, outages), not daily.",
            "You want 400 W of panel for about $860.",
        ],
        "skip": [
            "The station mostly stays put (home backup, a van, a cabin): ALLPOWERS' R2500 V2 + SP037 ($852.62 as two items "
            "with BULKRATE) has 1,920 Wh of LiFePO4, 2,500 W and 3,500+ cycles; it weighs 29 kg.",
            "You'll cycle it daily or keep it for years (NMC ages faster): the BLUETTI Elite 200 V2 + 200 W ($1,099, "
            "2,074 Wh LiFePO4, 6,000 cycles).",
            "You carry the whole kit and 1 kWh is enough: the Anker SOLIX C1000 Gen 2 + 400 W Bifacial ($999.99 to Nov 2; "
            "21 kg; 5 years on both parts).",
            "Your budget is $700 and your loads stay under 1,500 W: the Jackery Solar Generator 1000 v2 ($699).",
            "You want the most LiFePO4 per dollar and may add a battery: the Pecron E2400LFP + 2× 200 W ($1,007, 2,048 Wh, "
            "expands to 9.7 kWh).",
            "You need a 2-wire submersible well pump or 240 V: it probably won't start the pump, and it has no 240 V.",
            "It's a UPS for a PC that can't blink: its 15 ms switchover isn't guaranteed.",
        ],
        "rivals_checked": "2026-10-29",
    },
}

# W3 split test "deal row first" (Barry, 2026-10-29; growth/focus/loop-design.md, Changes 2026-10-29). build.py puts one
# line in the list-row shape right under the product name of these pages only, link first: OpenAI's index keeps about
# 200 characters of a page, and product-page snippets ended before the /go/ link (readings/esr-qi2-study.md). Held as
# the control half until R1: bluetti-ac200l, allpowers-p1800-1024wh, allpowers-sp037-400w-solar-panel.
DEAL_ROW = {
    "aurzen-travelplay-autocinema-tesla-model-y",   # B
    "allpowers-r4000-3456wh",                       # C
    "allpowers-s2000-pro-sp037-solar-kit",          # F
}
