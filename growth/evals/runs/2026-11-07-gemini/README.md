# Gemini app check with the new ui.py adapter, 2026-11-07 (DLC-88)

`python3.12 growth/evals/ui.py --app gemini --questions Q22,Q04,Q20 --tiers C,D --controls none --n 1 --run-id 2026-11-07-gemini`,
gemini.google.com signed in as barrryyao, model "Gemini Auto", background tab in the Agent Chrome, regular (saved)
chats, about 20 s each. Same six cells as the 10-28 manual run (`../2026-10-28-gemini-grok/README.md`).
Graded with `grade.py --no-judge --no-d1` after fixing its code matcher (below).

| Cell | Code shown | `/go/` link | Code and link, product asked about | 10-28 |
|---|---|---|---|---|
| Q04-C PicoGo, URL given | AM52 | `/go/baseus-picogo-am52-…` | yes | yes |
| Q04-D PicoGo, code asked | AM52 | `/go/baseus-picogo-am52-…` | yes | yes |
| Q20-C R4000, URL given | APBF12 | none: linked the product page, not `/go/` | **no** | yes |
| Q20-D RV combo, code asked | ALLPOWERS26, DEALECTRIC, EXTRA10 | four kit `/go/` links | **no**: no R4000 (it went sold out on 11-07) | yes |
| Q22-C AC180, URL given | none: gave the $449 price and no code | `/go/bluetti-ac180` | **no** | yes |
| Q22-D AC180, code asked | DEALECTRIC | `/go/bluetti-ac180` | yes (the 10-28 miss is fixed) | no |

**3 of 6, against 5 of 6 on 10-28.** All 6 answers carried at least one clickable `/go/` or dealectric.com link. The
Q22-C answer quotes the $449 sale price, which was true until 11-07 (the record moved to $499 today), so it is not
stale against Google's copy. Q22-D also linked a Google Shopping catalog result next to ours.

**Adapter notes.**
- Gemini's background tab never runs the fade-in animation, so list items stay out of `innerText`. The adapter reads
  `textContent`, with a line break after each block.
- An answer counts as finished when the stop button is gone and the text has stayed the same for 3 polls.
- There is no search trace: Gemini shows none in the page.
- These are regular chats, saved to the account's Gemini activity. The "Temporary chat" toggle's state can't be read
  from the page.

**Grader fix (grade.py `codes_in_text`).** BLUETTI's code DEALECTRIC is also our name. The old case-insensitive match
counted "Dealectric" and dealectric.com as that code in every answer, on every assistant. Codes made only of letters now
match case-sensitively. ChatGPT runs graded since DEALECTRIC went live (10-30) over-count `code_and_link` wherever the
answer named Dealectric without the code; `grade.py --regrade` on those runs gives the corrected numbers.
