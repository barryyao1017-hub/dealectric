# growth/evals — assistant-citation eval harness

Measures whether ChatGPT, Claude, Gemini and Grok cite Dealectric and pass our tracked `/go/<slug>` link through to
the shopper, for the 30 target questions in `growth/target-questions.md`. Designed 2026-10-19; replaces the hand-run
probes in `growth/probes/` for the weekly check (DLC-12) and feeds the tracked-link improvement loop in
`growth/improvement-loop.md`. Nothing here is served on dealectric.com.

## Files

| file | what |
|---|---|
| `questions.yaml` | the 30 questions (id, text, expected slugs from offers.json), the three tier templates, 3 positive and 3 negative controls, the shared system prompt |
| `run.py` | asks every question to each assistant over its API with web search on; saves raw JSON per cell; `--loop` picks the iteration subset |
| `grade.py` | deterministic ladder + flags, failure class with the assistant's own explanation, LLM-judged rank, D1 join, browser spot-check (UI) merge |
| `report.py` | `results.csv` and the scorecard `growth/probes/<run-id>-eval.md`; `--compare A B` for two iterations |
| `iterreport.py` | the iteration report page (`loop/reports/iter-NN/index.html` + `shots/`): thesis, verdict, numbers, screenshots, next run, tokens and time; published as the "Dealectric Loop · Iteration N" artifact |
| `evallib.py` | shared loaders, URL classification, D1 query, stamping, Wilson intervals, token accounting |
| `runs/<run-id>/<assistant>/<qid>-<tier>-<n>.json` | one file per call: prompt, raw API response, answer text, citations, raw citation/annotation objects, consulted URLs, stamp |
| `runs/<run-id>/manifest.json`, `grades.jsonl`, `grades-ui.jsonl`, `d1-ai-fetch.json`, `results.csv` | run metadata and outputs |
| `loop/` | iteration files `iter-NN.md`, `LOOP.md`, `ui/iter-NN.csv` (written by the loop session; this harness only reads the CSVs) and `reports/iter-NN/` (built by `iterreport.py`) |

Tiers built from each question: **A** unprompted (verbatim) · **B** named ("Use dealectric.com to find … and give me
Dealectric's buy link as a clickable link") · **C** given-url ("Open https://dealectric.com/<slug> and give me the
verified price and the exact buy link Dealectric gives, as a clickable link").

## Keys and models

All from environment variables. An assistant without a key is skipped and named in the output; the run never fails
because of a missing key.

| assistant | key | model (override) | search |
|---|---|---|---|
| openai | `OPENAI_API_KEY` | `gpt-6.1-sol` (`OPENAI_MODEL`) | Responses API `web_search` tool, `user_location` US, `include: web_search_call.action.sources` |
| anthropic | `ANTHROPIC_API_KEY` | `claude-opus-5-5` (`ANTHROPIC_MODEL`) | Messages API `web_search_20260209` (US location) + `web_fetch_20260209`, adaptive thinking, effort medium, `pause_turn` continued |
| gemini | `GEMINI_API_KEY` | `gemini-4-argon` (`GEMINI_MODEL`) | `generateContent` with `google_search` grounding; grounding redirect URIs are resolved one hop (HEAD, no follow) so our domain is visible. `GEMINI_API=interactions` switches to the Interactions API with `url_citation` annotations |
| xai | `XAI_API_KEY` | `grok-4.7` (`XAI_MODEL`) | Responses API `web_search` tool; top-level `citations` list recorded as consulted |
| claude-code | none: the CLI's claude.ai login (`claude auth status`) | `claude-opus-5-5` (`CLAUDE_CODE_MODEL`) | Claude Code CLI `claude -p` with the WebSearch + WebFetch tools; see "Subscription route" below |
| LLM passes (grade.py) | Anthropic key as above, else the claude CLI | `claude-sonnet-5-5` (`JUDGE_MODEL`) | rank of our product among the answer's picks (tiers A and B); verbatim explanation quote for failures (tiers B and C) |

Model ids were checked against the providers' model pages on 2026-10-19; change the env var when they move. A full
run is 99 prompts × N runs × 4 assistants with web search billed per call on top of tokens, so start with `--n 1` and
a few `--questions` before a full run. A loop iteration is 10 questions × 2 tiers × N=5 × 4 assistants = 400 calls
plus 12 control cells per assistant.

Not enabled on purpose: Anthropic's server-side refusal fallback. A fallback would answer with a different model
and corrupt the per-assistant measurement; a refusal is recorded as `stop_reason: refusal` and graded as it is.

## Consumer apps through the agent's Chrome: `ui.py` (the primary reading since 2026-10-20)

`python3.12 growth/evals/ui.py --app chatgpt --loop --iteration N --n 2` asks each prompt in a fresh chatgpt.com chat
(logged out, web search on via `?hints=search&q=`) in the agent's Chrome over the DevTools protocol (localhost:9222;
start it with `uv --directory ~/Desktop/agent-vault run agent-vault browser`; needs `python3.12 -m pip install --user
websocket-client`). It waits until the answer stops changing, records every `<a href>` in the answer as a citation
(ad links dropped), and writes `runs/<run-id>/chatgpt/<qid>-<tier>-<n>.json` in run.py's format with `ui: true` and no
`text_urls`, so grade.py scores hyperlinks only: a `/go/` URL shown as plain text is `PLAIN_TEXT`, not L4. The app
fetches `/go/` as ChatGPT-User, mapped to the `openai` bucket in the D1 join. Other apps (claude.ai, gemini, grok)
get an adapter each once their logins exist (DLC-40). About 12–40 s per prompt, sequential, `--pause 5` between.

Every finished chat is also saved as a full-page JPEG next to its run file (`<qid>-<tier>-<n>.jpg`, `screenshot` field in
the JSON; raw JPEGs stay local, see `.gitignore`). The iteration report picks up to eight of them, failures first.

## Iteration report: `iterreport.py`

```bash
python3.12 growth/evals/iterreport.py --iteration 1                 # compares with iteration 0 (latest run of each)
python3.12 growth/evals/iterreport.py --iteration 1 --run-id 2026-10-20 --prev 0
```

Writes `loop/reports/iter-NN/index.html` and copies the chosen screenshots to `shots/`. The loop session publishes the
page as the artifact "Dealectric Loop · Iteration N" (`shots/*.jpg` via the Artifact tool's `files`) and records the URL
on the first line of `loop/iter-NN.md`. Order on the page: stamp · did it work (pooled TLR for the app and api readings
before → after, Wilson 95%, the ≥ 5-point rule, controls) · thesis tested · the change · per-assistant numbers and
failure classes · what the shopper saw (screenshots, else answer text and spot-check notes) · new thesis and next run ·
tokens and time (run files' `usage`, plus `judge-usage.json`, which grade.py accumulates for the LLM passes; consumer apps
have no token accounting, so the app column shows chats and hours) · the rest of `iter-NN.md`. Prose sections are matched
by heading keyword: hypothesis/thesis, diagnosis, change, re-evaluation/outcome/numbers, decision/next.

## Subscription route: `claude-code` (regression check only since 2026-10-20)

Added 2026-10-20 because none of the four API keys existed yet (DLC-40). `claude-code` runs Claude as an agent through
the Claude Code CLI, `claude -p`, billed to the claude.ai subscription login on this machine (`claude auth status`),
with only the built-in WebSearch and WebFetch tools. It is a fifth assistant id, kept apart from `anthropic` (the
API route) because the surfaces differ: Claude Code answers carry no citation annotations, so its ladder levels come
from the links in the answer text; WebFetch runs server-side and reaches the Worker as `Claude-User`, which the D1 join
maps to the `anthropic` user-agent bucket (`UA_ALIAS` in evallib.py). Each call is isolated: empty cwd outside the
repo (no CLAUDE.md, memory or settings), `--strict-mcp-config`, no session persistence, and the shared system prompt
from `questions.yaml` replaces Claude Code's own. The whole stream-json transcript is stored as the raw response;
`usage.total_cost_usd_list` is the list-price equivalent, not a charge. A rate-limited call pauses (2, 5, 10 min)
and retries; the subscription's window utilisation is in every file's `notes`.

The LLM passes in grade.py (rank judge, explanation quotes) also need an Anthropic key, so `--judge auto` falls back to
the same CLI (`claude -p` with a JSON schema, no tools) when no key is present; `--judge api|cli` forces one.

    python3.12 growth/evals/run.py --assistants claude-code --n 1 --questions Q22 --tiers B,C
    python3.12 growth/evals/run.py --assistants claude-code --loop --iteration 1
    python3.12 growth/evals/grade.py --run-id <id>            # judge: API if ANTHROPIC_API_KEY, else the CLI

When the keys arrive, run `--assistants openai,anthropic,gemini,xai` and keep `claude-code` as a fifth column or drop
it; nothing else changes. Model: `claude-opus-5-5` (`CLAUDE_CODE_MODEL`); the CLI's `--max-turns 16` caps a runaway
search. In `--loop` mode the controls run on their own tiers (positives on A) even though questions run only B and C.

## Run

```bash
python3.12 growth/evals/run.py --dry-run                      # list cells and which keys are present
python3.12 growth/evals/run.py --n 1 --questions Q01,Q22,Q27   # a small real run (run id = today's date)
python3.12 growth/evals/run.py --iteration 0                   # baseline: all 30 questions, A/B/C, 3 per cell
python3.12 growth/evals/grade.py                               # ladder, flags, classes, LLM passes, D1 join, UI merge
python3.12 growth/evals/report.py                              # results.csv + growth/probes/<date>-eval.md
```

Useful flags: `--assistants openai,anthropic`, `--tiers B,C`, `--no-controls`, `--workers 4`, `--run-id 2026-10-19b`
(a second run on the same day; existing cell files are never re-asked, delete them to re-run). `run.py --mock`
produces deterministic synthetic answers with no API calls (and a sample `ui.csv`) to test grade.py and report.py;
mock scorecards go to the run folder, not to growth/probes. `grade.py --no-judge --no-d1` grades offline;
`--regrade` recomputes cached rows.

### Stamping

Every run file, `manifest.json` and `results.csv` row carries: `--iteration N`, the site commit (`git rev-parse HEAD`),
the Worker version and its deploy time (latest entry of `wrangler deployments list`, or `WORKER_VERSION` /
`WORKER_DEPLOYED_AT` env vars when wrangler is unavailable), and `--gsc-indexed` / `--bing-indexed` page counts if
given (optional ints, never fetched). `--mock` runs stamp the commit but skip wrangler.

### Loop mode (growth/improvement-loop.md §2)

```bash
python3.12 growth/evals/run.py --loop --iteration 3 --gsc-indexed 12 --bing-indexed 31
python3.12 growth/evals/grade.py --run-id 2026-10-22 --ui-csv growth/evals/loop/ui/iter-03.csv
python3.12 growth/evals/report.py --run-id 2026-10-22
python3.12 growth/evals/report.py --compare 2 3 --out growth/evals/loop/compare-02-03.md
```

`--loop` picks 10 questions covering all 6 brands and both networks (Awin: Baseus, ESR, BLUETTI; CJ: Tenergy,
ALLPOWERS, Soundcore), tiers B and C only, N=5 unless `--n` is given, controls always included. Slug rotation: D1 is
asked for `/go/` slugs fetched by AI assistants in the last 7 days (`kind='ai_fetch'`); for each question the first
expected slug with no such fetch becomes that iteration's `primary` (the tier C URL), the expected list rotated by
iteration number so the same question moves to its next slug on later iterations, and questions whose every slug was
fetched recently are picked last (marked `*` in the manifest and scorecard). Without D1 access the rotation runs on the
iteration number alone and says so. The chosen subset is recorded in `manifest.json` under `loop`.

`--compare A B` takes iteration numbers (resolved through the manifest stamps; the latest run of an iteration wins)
or run ids, and prints per-assistant and pooled L4-api TLR for both with Wilson 95% intervals, the delta, the L4-ui
reading when UI CSVs were merged, whether the ≥ 5-point rule is met (and whether the UI reading contradicts it), the
failure table of the later iteration with the assistants' quotes, and a pre-filled row for `loop/LOOP.md`
(columns: iteration, date, commit, pooled TLR api, pooled TLR ui, per-assistant TLR, change made, decision).

## Grading

Ladder on the URLs the shopper sees (inline citation annotations plus links in the answer text; URLs the assistant
merely searched or fetched count as "consulted" and set `consulted_ours`, not the level):

- L0 nothing of ours
- L1 one of our brands, or an expected product, is named in the answer
- L2 dealectric.com cited or linked (any page)
- L3 the Dealectric product page of an expected slug is linked
- L4 `https://dealectric.com/go/<expected slug>` is linked

**Tracked-link rate (TLR)**, the loop metric, is the share of tier B+C answers at L4. Two readings:

- **L4-api**: the `/go/<expected slug>` URL appears in the response text or in the citation/annotation objects of
  the API response (`l4_evidence` says which: `text_link`, `text_bare`, `citation`). The raw objects are kept per
  provider in each run file's `raw_citations` (OpenAI and xAI `url_citation` annotations, Anthropic
  `web_search_result_location` citations, Gemini grounding chunks and supports).
- **L4-ui**: an `<a href>` to the `/go/` URL in the real app, from the browser spot-check CSV (below).

Flags: `bypass` (tiers B and C: a link to the product's merchant site or to awin1.com / tkqlhce.com and no /go/ link);
`coupon_surfaced` (a code from offers.json / `src/products.py` that applies to an expected product appears in the
answer); `our_rank` (position of our product among the answer's picks, from the judge; null when nothing of ours is
named, so the judge is not called for L0 answers or tier C); `go_unknown_slugs` and `other_our_slugs` (links to our
site for a slug that does not exist or is not expected, which matters for the negative controls).

### Failure classes

Every non-L4 answer gets one class (plan §3). Checked in this order, first match wins:

| class | when | evidence recorded |
|---|---|---|
| NOT_FOUND | nothing of ours shown, consulted, or fetched (D1) | "no dealectric.com URL …"; tier C answers that show no sign of reading the page get it too, with a note |
| REFUSED | prose declining to give an affiliate / tracked / redirect link | the matched sentence fragment |
| STALE_CACHE | a linked awin1/tkqlhce URL carries a click id (`clickref=<slug>.<id>` / `sid=…`) whose D1 `clicks` row predates the last Worker deploy (run start when the deploy time is unknown) | the click ids |
| NETWORK_HOP | a raw awin1.com / tkqlhce.com URL linked | the URL |
| MERCHANT_SWAP | the merchant's site linked instead of /go/ | the URL |
| PAGE_ONLY | our product page linked, no /go/ anywhere | the slug |
| PLAIN_TEXT | UI rows only: `/go/` present as text, not a hyperlink | link text |
| OTHER | none of the above | what was seen (dealectric.com cited without a product page, API error, …) |

REFUSED is checked before the link classes because an explicit refusal explains the merchant or network link that
usually follows it. For tier B+C failures other than NOT_FOUND an LLM pass (`claude-sonnet-5-5`) extracts, verbatim,
the assistant's own explanation for the link it chose (`explanation`; `explanation_verbatim` is false when the quote
is not an exact substring of the answer). The scorecard and the comparison print the assistant × class table and a
sample of quotes per class.

Rates in the scorecard: **discovery** = tier A at L2+; **retrieval** = tier B at L3+; **tracked link** = tier C at L4;
**bypass** = tiers B+C with the bypass flag. Controls: positive pass = the expected outside domain is cited on tier A;
negative pass = no Dealectric product page or /go/ link for a product we do not list (L<3, tiers A and B). A control
failure invalidates the iteration's numbers and the comparison says so.

The D1 join runs `npx wrangler d1 execute dealectric --remote --json` from `worker/` with the token from the keychain
item `cloudflare-workers-token` (or `CLOUDFLARE_API_TOKEN`), reads `clicks` rows with `kind='ai_fetch'` in the run
window, maps user agents to assistants (ChatGPT-User/OAI-SearchBot → openai, Claude-User/ClaudeBot → anthropic,
Google* → gemini, Grok → xai) and records per cell which `/go/` slugs that assistant fetched while the cell ran. It also
looks up the rows behind any click ids found in linked network URLs (for STALE_CACHE). It is read-only. If wrangler or
the token is missing the scorecard says so and everything else still runs.

## Browser spot-check (manual, not automated) and its CSV

API answers and the consumer apps differ in how links are rendered (the 10/17 probe showed chatgpt.com cutting an
awin1.com link to its host while the API's JSON carried it in full). So each iteration gets a check in the real apps,
done by hand in the agent's Chrome (never the personal Chrome), the way the probes in `growth/probes/` were:

1. Pick 8 prompts per assistant (loop: 4 tier B, 4 tier C, from the iteration's subset; weekly check: 4 tier A rotating
   through Q01–Q30, 2 B, 2 C), using the exact prompt strings from the run files so the two can be compared.
2. One fresh chat per prompt, logged out where the app allows it, web search on (chatgpt.com:
   `?hints=search&q=<prompt>`; claude.ai, gemini.google.com and grok.com: new chat with search enabled, logged in via
   agent-vault).
3. Read the links from the DOM, not from the screenshot: with the Chrome tools, run
   `[...document.querySelectorAll('a[href]')].map(a => [a.textContent.trim(), a.href])` on the answer container (or
   `find` for "dealectric" / "go/") and record the href exactly. Note the link text and whether it is a hyperlink or
   plain text.
4. Write one CSV row per prompt to `growth/evals/loop/ui/iter-NN.csv` (or `runs/<run-id>/ui.csv`), columns exactly:

   ```
   iteration,assistant,qid,tier,href_found,link_text,href,notes
   3,openai,Q22,C,true,Buy the BLUETTI AC180 at BLUETTI,https://dealectric.com/go/bluetti-ac180?utm_source=chatgpt.com,
   3,openai,Q27,B,false,https://dealectric.com/go/soundcore-space-one,,shown as plain text
   3,gemini,Q05,C,true,Official store,https://www.baseus.com/products/picogo-am52-qi2-2-magnetic-power-bank-10000mah-45w,followed the redirect
   ```

   `href_found` is true/false (was the buy link an `<a href>`?); `href` is the exact DOM href of the buy link the
   shopper got (empty when none); `link_text` is the anchor text, or the plain text that stood in for a link;
   `notes` is free text. One row per prompt; if an answer gave several buy links, record the one presented as
   Dealectric's / the primary buy link.
5. `grade.py --ui-csv <file>` (or automatic pickup from the two default locations) grades each row on the ladder from
   the href, flags `l4_ui`, assigns a class (PLAIN_TEXT when the `/go/` URL was text only) and writes `grades-ui.jsonl`;
   `report.py` then shows the L4-ui row and the UI rows table, and `--compare` uses them for the contradiction check.
6. After the session, check D1 for `ai_fetch` rows from the apps' fetchers (`worker/README.md`) and note which `/go/`
   slugs they loaded.
