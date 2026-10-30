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

## Open

- Is there a length cap on long pages, and where does the excerpt start and end (only the top N characters, or a
  query-picked window)? Needs our long pages (`/products`, `/discount-codes`, `/`) in the results, where we know the
  stored text exactly.
- Does the same page give the same excerpt for different queries?
- Do the product listings carry our pages, and what is in them?
