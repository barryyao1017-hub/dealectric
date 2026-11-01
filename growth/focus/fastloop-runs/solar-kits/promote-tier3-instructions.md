# Tier 3 instruction set, 2026-11-01: solar kits page + RV page refresh

Sources: `growth/focus/fastloop-runs/solar-kits/outreach.md` (S tasks) and
`growth/focus/fastloop-runs/rv-2kwh/outreach-2026-11-01b.md` (R tasks). Text to paste = the numbered draft in that
file, verbatim, without the leading "> " quote markers. Ordered by demand, then freshness.

Rules for the execution agent:
- Agent's Chrome on localhost:9222 only, background tabs (`ui.Tab`). In a background tab, call
  `Emulation.setFocusEmulationEnabled(enabled=True)` and `el.focus()` before `Input.insertText`.
- Log in through agent-vault where an account exists (`list_accounts`). Google sign-in as barrryyao@gmail.com is
  allowed only where an account already exists (Quora). Never create an account: if the site has no account for us,
  or "Continue with Google" leads to a registration step (choose a username, accept terms), stop and leave the
  sign-up page open for Barry.
- Fill each form up to the final Post / Reply / Submit and stop. Never click it. Leave the tab open, screenshot it to
  `growth/focus/fastloop-runs/solar-kits/staged/<task>.png`.
- Comment forms asking name/email: name "Barry", email barrryyao@gmail.com, website field empty.

| Task | Venue / URL | Account | Text | Stop point |
|---|---|---|---|---|
| S1 | diysolarforum "Need help anker c1000 gens": https://diysolarforum.com/threads/need-help-anker-c1000-gens.132049/ | vault: diysolarforum.com (Barry created 11-01) | solar 2a (no link) | Reply box filled 11-01, "Post reply" not clicked |
| S2 | diysolarforum "Worth waiting for Black Friday Deals?": https://diysolarforum.com/threads/worth-waiting-for-black-friday-deals.131924/ | same as S1 | solar 2b (no link) | Reply box filled 11-01, not posted |
| R1 | My Grand RV "Transcend 151RB for Off-Grid Camping": https://www.mygrandrv.com/threads/grand-design-transcend-151rb-for-off-grid-camping.2219375/ | vault: forestriverforums.com item (RV LIFE login, mygrandrv.com domain approved 10-31) | rv-b 2a (no link) | Reply box filled, "Post reply" not clicked |
| R2 | Airstream Forums "Portable Power Station as House Battery": https://www.airforums.com/threads/portable-power-station-as-house-battery.2216870/ | vault: same RV LIFE item (airforums.com approved 10-31) | rv-b 2b (no link) | Reply box filled |
| S3 | Tacoma World "110V bed outlet": https://www.tacomaworld.com/threads/110v-bed-outlet.884814/ | vault: tacomaworld.com (Barry created 11-01) | solar 2c (no link) | Quick reply on page 2 filled 11-01, "Post Reply" not clicked |
| R3 | Boondock or Bust correction, chuck@boondockorbust.com | Gmail (barrryyao) | rv-b 2c | Gmail draft (made by the main session). Barry: re-check the Elite 200 V2 has no TT-30 before sending |
| S4 | geekbitz.com comment: https://geekbitz.com/best-solar-generators | comment form | solar 2d | Comment filled, not submitted |
| S5 | Quora: https://www.quora.com/What-is-the-most-reliable-portable-solar-generator-for-off-grid-camping-in-2026 | Google as barrryyao (existing account) | solar 2e (disclosed link) | Answer editor filled, "Post" not clicked |
| S6 | trek4tech.com contact form: https://www.trek4tech.com/contact | form | solar 2f | Form filled, not submitted |
| R4 | progressiveradionetwork.com comment: https://progressiveradionetwork.com/best-portable-power-stations-for-rvs | comment form | rv-b 2d | Comment filled, not submitted (low priority) |

Manual for Barry: Reddit and Facebook searches listed in section 3 of each outreach file.
