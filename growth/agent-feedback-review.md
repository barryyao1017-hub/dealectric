# Agent feedback loop: review and MCP go/no-go (DLC-37, DLC-27)

Written 2026-11-07, covering 2026-10-18 (the Worker went live) to 2026-11-07. Data: D1 `clicks`, `feedback` and `landings`.

**Verdict: don't build the MCP server or the OpenAPI listing (DLC-27) yet. In three weeks no agent has written to
`/feedback`; every row came from a crawler or one of our own tests. Agents use us by reading pages and handing over
`/go/` links, which already works and produced the first sale.**

## What the data says

| Signal | Count | Reading |
|---|---|---|
| `/feedback` rows | 8 | 2 our smoke tests (10-18). The other 6 are all "missing_product: Anker Prime 250W power bank" (or "Anker"), and their user agents are Amazonbot, meta-externalagent, Googlebot and the iOS 13 catalog scanner. That message is the **example URL in our own llms.txt**, so crawlers are following the sample link. Real agent feedback: **0**. |
| `/go/` fetched by an AI assistant (`kind='ai_fetch'`) | 501 (158 before 10-28, 343 after) | Growing: 110, 119, then 265 a week across 223 slugs, and 127 on 11-07 alone. Assistants (mostly ChatGPT-User) check our buy links before showing them. This is the "offers assistants present" signal. |
| ChatGPT-tagged `/go/` clicks from real browsers | 105 from 10-29 to 11-07 (4–22 a day) | Shoppers do click our links inside ChatGPT answers; first credited sale 10-29 (DLC-33). Before 10-29: 0. |
| ChatGPT-tagged landings on pages | 98 real-browser, 42 bot-like | The page path works as well as the link path. |
| Muse-tagged clicks (DLC-146) | 0 | No confirmed Muse shopper yet. |

Click counts above are raw D1 rows. The earlier 10-27 read found scanners and our own eval chats inside the
untagged traffic. The ChatGPT-tagged real-browser count still includes some of our own taps, so
`tools/fetchwho.py` is the right tool to split ours from outside.

## Decision

- **MCP / OpenAPI (DLC-27): no-go for now.** The test agreed on 10-18 was "build only if agents actually write to us".
  They don't. They read pages and `offers.json` and relay `/go/` links. An MCP server would also need a registry listing
  to be found, and the Apps SDK review (growth/apps-sdk-eval.md, DLC-145) found directory reach small and the rules unclear on
  affiliate links. **Revisit when either trigger fires:** (1) one genuine agent-written `/feedback` row (user agent
  not a crawler, message not our example), or (2) an assistant platform starts calling MCP servers for shopping queries
  without the user installing them first.
- **Fix the feedback example.** The llms.txt sample message is the only thing crawlers send back. Change it to an
  obviously illustrative value (e.g. `message=example`) and drop rows with that message when counting, so a real
  request stands out. A small build.py change. The 6 Anker rows are crawler noise, not demand (the Anker Prime is
  still worth carrying via Rakuten / Amazon on its own merits, DLC-159).
- **Keep:** `/go/` with its ai_fetch text page, `/feedback` (it costs nothing), and the weekly read in the scorecard (DLC-28).
