# Stock read and ships-now alternatives, 2026-11-26 (DLC-358)

- `live-read-status.json`: every ALLPOWERS and BLUETTI record read in the Agent Chrome as a shopper sees it (exact variant): ships now / pre-order (latest item's date) / sold out, and the price.
- `decisions.py`: the alternative chosen for each sold-out product and each pre-order shipping more than 14 days out, under Barry's rules (best substitute, ships now > pre-order, lower price within ±25%, same brand, earns), with the runner-up and the reason; `None` entries say why nothing qualified. `src/alternatives.json` is built from it.
- `research/*.md`: candidate spec tables, sources, reviews and winner-vs-runner-up reasoning per size class.
- `amazon-reads.jsonl`: same-day Amazon reads of the Amazon picks (price, stock, delivery).
- `page-text-changes.md`: the stale stock sentences corrected in src/gaps.py.
