# Fable research brief (fast-loop step 4)

Fill in the `<…>` fields and send the whole brief to a subagent with `model: "fable"` and web search. The DLC-114 run
used an earlier version of this brief; its report is `growth/focus/fastloop-runs/rv-2kwh/open-concern.md`.

---

You are the research step of Dealectric's ChatGPT fast loop (repo /Users/jiayiyao/Desktop/dealectric). Dealectric
publishes short, factual buying pages for shoppers and the AI assistants that answer them. We are drafting ONE page for
the shopper question "<shopper question>". ChatGPT's own searches for it: <the 2–3 query phrasings>. A three-model
review of ChatGPT's real top results found this gap: "<the vote's missing lead>". The results already agree on: <the
shared core, 4–6 bullets>. Our candidates, with tested codes: <our products, prices, code and last cart pass>.

**How the page will be read** (`growth/focus/fastloop-briefs/COPY-RULES.md`):
- ChatGPT's model sees only part of a page: about 1,000–1,500 characters at the rank a new page usually gets.
- It always keeps the opening, then the passages sharing the most words with the search query.
- So only the top of the page reliably reaches it.

Your findings decide what goes at the top, so rank and compress them for that.

Use web search and page reads. Every factual claim needs a source URL. Mark anything you can't verify as UNVERIFIED
rather than guessing. Today is <date>. Prefer maker spec pages and manuals for specs, and current store pages for
prices (give the date seen).

Deliver a markdown report:

1. **Top block, ready to use.**
   - **The one reason our pick wins on this exact query**, in one sentence of at most 200 characters, in the query's
     words, with its number and source.
   - **The single most important open concern** shoppers still have after reading today's results, with:
     - a one-sentence answer of at most 300 characters, in the query's words, carrying the number that matters;
     - the source;
     - how often owners raise it (thread counts and 2–4 example URLs).
2. **Product facts** for our candidates: the specs the query and the concern turn on, current price on the maker's
   store, and availability or end-of-life status.
3. **The field**: competing products a shopper can buy within the query's constraint today, with the same specs and
   prices (date seen).
4. **Other candidate concerns**, ranked by how often they come up, each with a sourced one-sentence answer. These feed
   later iterations of the top block.
5. **Sources.**

Do not write or modify any files in the repository. Return the report as your final message. Keep it factual and
compact.
