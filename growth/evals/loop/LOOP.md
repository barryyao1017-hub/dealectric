# Tracked-link improvement loop — iteration log

One row per iteration (growth/improvement-loop.md §5). Numbers are the pooled tracked-link rate on tiers B+C:
L4-api from the harness run, L4-ui from the browser spot-check. Details in `iter-NN.md` next to this file; each
iteration's report page (built by `../iterreport.py`, published as the artifact "Dealectric Loop · Iteration N") is
linked on the first line of its `iter-NN.md`.

Iteration 0 ran on the subscription route: the API column was **claude-code** (Claude as an agent through the Claude
Code CLI), the UI column a manual 8-prompt ChatGPT check. From iteration 1 (Barry, 2026-10-20: shoppers use the
apps) the **primary metric is chatgpt.com logged out, driven by `growth/evals/ui.py`** and recorded in the "pooled
TLR ui" column; claude-code runs once per cell as a regression check ("api" column). claude.ai, gemini.google.com and
grok.com join when their logins exist (DLC-40).

| iteration | date | commit | pooled TLR api | pooled TLR ui | per-assistant TLR | change made | decision |
|---|---|---|---|---|---|---|---|
| 0 | 2026-10-20 | d32a405853 | 100% (180/180) | 75% (6/8) | claude-code 100%; ChatGPT ui 75% | baseline, no change (harness: Q19 expected widened, negative-control rule, CLI process-group kill) | continue: homepage product index for ChatGPT's tier-B NOT_FOUND |
