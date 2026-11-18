# Record sources, 2026-11-18 (DLC-313, DLC-317)

Research drafts behind the records added on 2026-11-18: Creality printers (`creality-k2-plus`, `-k2-plus-combo`,
`-k2-pro-combo`, `-k1c`, `-k1-max`), WECREAT laser engravers (`wecreat-vista-10w`, `-vision-20w-rotary`,
`-vision-pro-45w`, `-lumos-10w-diode-ir`, `-lumos-flex`) and the Hohem iSteady MT3 Pro.

Each JSON holds the drafted records with a `sources` list (claim, URL, date read) for the price, each spec group,
warranty, returns and every caveat, plus rival prices and the notes on what could not be verified. The records in
`src/products.py` differ from the drafts in small ways: no dated prices in summaries, rival prices moved to `fit`
with their date, the Hohem MT3 draft was not used (it wins only on weight), and the K2 Plus record carries the
110 V / 15 °C chamber limit from Creality's K2 Pro / K2 Plus chamber guide.

Prices and stock were re-checked the same day: Creality on the store pages (headless store, no cart API), WECREAT
and Hohem in the cart with `tools/codecheck_browser.py` (control code rejected on every run).
