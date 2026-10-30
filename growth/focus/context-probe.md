# What ChatGPT's model receives from a web search (DLC-77, 2026-10-30)

Driver: `growth/evals/ctxprobe.py` (signed-in account 1, agent Chrome 9222, temporary chats, gpt-6). Runs:
`growth/evals/runs/2026-10-30-ctxprobe/ctx/<tag>.json` (raw SSE stream of every turn + the answer text).

## Method

The model's tool output never reaches the page: the `web.run` tool message's text is blank in the stream and in the
conversation JSON. So it is read back indirectly. In the same turn as the search (`--same-turn`), the prompt asks the
model to quote, word for word, the excerpt it was given for every result. Each quoted line is then looked up in the
page: third-party pages as fetched live, ours in the git version OpenAI's crawler last fetched. A long exact string from
a page cannot be guessed, so a line found verbatim is proof the model had it.

- An echo asked in a follow-up turn fails: the model says the previous turn's search output is no longer in its
  context (t03). Only the same-turn echo works.
- Asking for the "raw tool output" is refused (e01); asking to "quote the excerpt you were given" works (e02).
- The model declines to quote some long third-party excerpts in full ("exceeds the amount of source text I can
  reproduce"), so for long pages the echo is a lower bound.

## Findings so far (3 echo chats, 11 pages checked)

1. **The model gets far more than the ~200-character result passage.** Per result it gets a block of page text in
   markdown: headings as `#`, tables as `a | b | c` rows (spec tables as `Label: value`), images as `Image: <alt>`.
   Third-party excerpts quoted: 1,661 to 2,701 characters, consecutive text from the start of the main content
   (navigation skipped). Every prose line matched the page verbatim.
2. **For our short pages it is effectively the whole page.** `/bluetti-ac200l` (d024441): labelled "Excerpt (full)",
   2,303 of the page's 2,597 text characters, H1 through the disclosure line, footer dropped, the `Buy:
   https://dealectric.com/go/bluetti-ac200l` line included.
3. **It is OpenAI's stored copy, not the live page.** The AC200L excerpt matches the version live at OAI-SearchBot's
   10-26 21:35Z fetch (12dfb2e, "Tested in BLUETTI's cart on 2026-10-21") on 12 of 12 prose lines; the live page fails
   every dated line. `/bluetti-discount-codes` came back as its 10-28 version.
4. **The stream's result list is display data.** In e02 all six results had an empty `snippet` in
   `search_result_groups`, while the model quoted thousands of characters for each. The ~200-character passages
   ui.py saved on 10-28/29 are what the UI shows, not what the model reads. A blank snippet says nothing about
   what the model got.
5. **A second channel: product listings.** Shopping queries also return product records
   (`turn<id>product0..36` in e02) separate from the web results; not examined yet.

## Needle tests (10:20-10:26Z, answered by gpt-6-mini)

The echo only shows what the model is willing to quote (1% to 80% of a page per chat; it labels some excerpts
"partial"), so a second test checks what it can answer. The prompt pins one search to a generic query, forbids
further searches and opening pages, and asks for a fact deep in a page that the query does not mention, with NOT IN
RESULTS as the honest exit. The stream confirms one `web.run` search with the pinned query and no other tool, and
Cloudflare shows no ChatGPT-User fetch of dealectric.com in the window.

| Chat | Query | Fact asked | Where it sits | Answer |
|---|---|---|---|---|
| N032039 | dealectric.com electronics catalog | Elite 30 V2 kit: price after code, solar voltage range | last 10% of `/` (24,447 chars) | $437, 12-28 V, sentence quoted verbatim from `/` |
| N032217 | dealectric.com discount codes | Aurzen ZIP Pro: saving, price after code | `/` table and `/discount-codes` | $57.99, $522, verbatim from `/` |
| N032612 | amphourly best solar panels for power stations ranked by data | BLUETTI PV100 FX weight, W/lb | 70% into amphourly's 25,410-char page | 4.85 lb, 20.6, table row verbatim |
| N032434 | same | Anker PS200 Voc and the limit it exceeds | 50% into the same page | 57.6 V over 55 V, verbatim from the 7th result (another long amphourly page) |

So the model receives the whole stored page, or at least the first ~25k characters of text, for every result,
including the 7th. The earlier ~1,000-character `/discount-codes` echo was the model quoting selectively.

## Model

Chats from 09:34 to 10:00Z were answered by gpt-6; from 10:03Z on, gpt-6-mini (Free quota spent; a parallel
`void-openings` scan used the same account from 09:49 to 09:58Z). The search tool runs server-side and the needle
results are about the tool's payload, but they are re-run on gpt-6 before they count for W3.

## What this means

- What ChatGPT's model reads of our page is the page as OpenAI last crawled it, all of it: every offer card,
  table row, code, date and `/go/` link. The 200-character passage and the title are only what the shopper sees.
- So copy anywhere on the page reaches the model; nothing needs to be squeezed into the opening for that reason.
  What decides freshness is still the crawl (`stored-copy.md`).
- When ChatGPT shows our page and does not hand over our `/go/` link, it had the link in front of it. DLC-83 is a
  question of what makes the model choose it.

## Open

- A size cap on pages longer than ~25k characters of text (needle near the end of a 35k+ page).
- Re-run two needles on gpt-6.
- Product listings (`turn<id>productN`): which records they carry and whether our pages ever appear there.
