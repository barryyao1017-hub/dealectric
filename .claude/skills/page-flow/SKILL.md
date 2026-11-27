---
name: page-flow
description: How Dealectric adds new pages routinely (numbered "best" pages, feature-finder pages, product pages) from a decision map per cluster, and retires pages that never draw a shopper (tools/pageflow, growth/pageflow). Use when picking which pages to build next for any cluster, adding a cluster, running or debugging the page flow routine, reading its queue, ledger or report, deciding whether a page idea is worth building, or changing the retire rule.
---

# Page flow

The routine is written up in `growth/pageflow/README.md`. Read it before acting. In short:

- **Start from the cluster's decision map**, never from a product or a situation. `growth/pageflow/maps/<cluster>.json`
  holds what buyers decide on (axes), the real breakpoints, the field (ours and rivals) and the lines: one question one
  page answers, with the honest top three and where ours place. `maps.py build <cluster>` researches it; a refresh every
  14 days picks up new reviews and releases.
- **Three page types, all drawn from lines**: numbered (a breakpoint on a number), finder (a yes/no feature few products
  have), product (a partner product with no record that places top three on a line, or a new release).
- **Every idea passes the same gates** (`propose.py`): the line is real and sourced; one of ours is honestly top three and
  buyable; no page of ours covers it; search demand, then openness read from ChatGPT's own results; value orders the
  queue. A hunch is allowed but marked, and fails without demand. No quota: when nothing passes, nothing is built.
- **Traffic steers it** (`ledger.py`): visits a page by cluster and page type is the prior in each line's score, so a page
  type that reads zero in a cluster sinks there by itself. Steer on the share of new pages visited within 14 days and on
  sales, not on page count.
- **Building** reuses the research method (`tools/abpage.py` through `driver.py`): two plain ChatGPT chats per question,
  six angle agents, compose, verify, Amazon links, validation, pick check, fastloop check. The cluster's rules and the
  reason for each number come from the map, so nothing about a cluster is written in code.
- **Publishing** needs `--publish` or `growth/pageflow/AUTOPUBLISH`; without it a run leaves drafts only.
- **Retiring** (`retire.py`): 45+ days at zero and seen by OpenAI's crawler -> one rework -> 30 more days at zero -> a
  noindex page pointing to the nearest live page; at most one retired per two added; off until `growth/pageflow/RETIRE_ON`.

Commands: `python3.12 tools/pageflow/run.py daily [--pages 3] [--clusters 1] [--cluster <id>] [--publish]` runs it all;
`ledger.py`, `ask.py`, `maps.py`, `propose.py`, `driver.py`, `retire.py` are its steps. To add a cluster, add it to
`growth/pageflow/clusters.json`; the next run builds its map.

Honest picks stay the rule: a page leads with the product that wins the line even when it is not ours, and a line where
none of ours is in the top three is not built (it is kept in the map as a note on which product or partner we lack).
