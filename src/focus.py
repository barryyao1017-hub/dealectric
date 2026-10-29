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
}
