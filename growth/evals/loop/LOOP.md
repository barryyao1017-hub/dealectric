# Tracked-link improvement loop — iteration log

One row per iteration (growth/improvement-loop.md §5). Numbers are the pooled tracked-link rate on tiers B+C:
L4-api from the harness run, L4-ui from the browser spot-check. Details in `iter-NN.md` next to this file.

Route while the four API keys are missing (DLC-40): the API column is **claude-code** (Claude as an agent through the
Claude Code CLI under the claude.ai subscription, see growth/evals/README.md); the UI column is **ChatGPT logged
out** at chatgpt.com (no login needed). claude.ai, gemini.google.com and grok.com need logins that are not in
agent-vault yet.

| iteration | date | commit | pooled TLR api | pooled TLR ui | per-assistant TLR | change made | decision |
|---|---|---|---|---|---|---|---|
| 0 | 2026-10-20 | d32a405853 | 100% (180/180) | 75% (6/8) | claude-code 100%; ChatGPT ui 75% | baseline, no change (harness: Q19 expected widened, negative-control rule, CLI process-group kill) | continue: homepage product index for ChatGPT's tier-B NOT_FOUND |
