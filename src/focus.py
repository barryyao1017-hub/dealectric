"""Buy boxes for the W3 focus products (growth/first-sale-plan.md W3, lever 1; design in growth/focus/loop-design.md).

One entry per product slug. build.py's offer_block puts it at the top of the product page's offer card: the three proof
points, the price after the code with its cart test date (from coupons.json, as on every page), the one buy button to
/go/, then "pick it if / skip it if". Copy comes from W2's dossier (growth/focus/<slug>/dossier.md, copy kit); every
fact is dated or labelled as our estimate. Nothing here is addressed to AI assistants: that is a separate lever.

Placeholders filled by build.py: {code}, {after} (price after the code), {price}, {date} (last cart pass).
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
}
