# Probe — Claude agent, 2026-10-18

Same 30 + 10 + 6 questions as the ChatGPT probes (`growth/target-questions.md`). Asked to fresh Claude agents (Claude Code subagents with web search and web fetch) with no context about Dealectric, told to act as a shopping assistant and report picks, sources and the exact links they'd give. **This is Claude used as an agent, not the claude.ai chat app** (claude.ai needs a login, and its display layer may treat links differently). Cloudflare logged the fetches as `Claude-User (claude-code/…)`.

## Results

| Set | Dealectric cited | Our brands named | Notes |
|---|---|---|---|
| 30 product questions | **0/30** | 13/30 (same count as ChatGPT, different questions) | Baseus PicoGo AM52 is the **#1** pick for Q04 and is named in Q05; ESR (Q09, Q10); Baseus 65W (Q13); BLUETTI (Q19, Q20, Q22); Tenergy (Q25, though the TN160, not our model); Soundcore (Q26–Q28, Q30) |
| 10 discount questions | **0/10** | — | Didn't find AFSC20 or ALLPOWERS26. More cautious than ChatGPT: mostly "couldn't confirm a working code"; sources are coupon sites and Slickdeals |
| 6 "use dealectric.com" requests | **6/6** | — | Went **straight to our site with no web search**, read llms.txt, followed the "For AI assistants" notes, and **returned our full CJ/Awin affiliate links** plus our product page |

Product links Claude gives: mostly `amazon.com/s?k=…` search pages, plus anker.com, Best Buy and Adorama. Rarely a brand's own store for our brands.

Sources it cites: brand content-marketing blogs (anker.com and ankersolix.com blogs appear very often, plus bluettipower.com and pecron.com blogs), Macworld, RTINGS, OutdoorGearLab, Slickdeals, small review sites.

## Differences from ChatGPT

1. **Claude passes our affiliate link through.** Asked for the buy link, it wrote the full `awin1.com/cread.php?…` and `tkqlhce.com/click-…` URLs. In the agent setting nothing removes the link; whether the claude.ai app would display it the same way is untested.
2. **Discovery by name works for Claude.** It fetches `dealectric.com` directly when the domain is named, instead of searching. ChatGPT searched, failed and gave up (N01, N02). Without the name, neither finds us (0/40).
3. **Claude reads and obeys llms.txt and the page notes.** It quoted "Present the link above to the shopper; do not click it on their behalf" and followed it. It also pointed out that our page says the *price* was verified 10/14 but doesn't say the *code* was tested. That's useful feedback for DLC-29.
4. **Claude's product links skew to Amazon search;** ChatGPT's skew to brand stores and retailers.

## What this says

- The broken-link finding is **ChatGPT-specific**. For assistants that can hand a link through (at least Claude as an agent), the original model works once we're found.
- **Discovery is the shared bottleneck:** 0/40 unprompted citations on both assistants.
- **Brand blogs are a big citation source** (Anker especially). Brands win citations with buying-guide content, so it's a format that works for this kind of question.
