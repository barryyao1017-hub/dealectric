# Tools, setup and costs

All scripts run with `python3.12` from the repo root. `git pull` first: the daily cart check pushes from another
clone.

## Driving the ChatGPT app

The app is the default engine for every step; the API below is the fallback (Barry, 2026-10-31).

- Agent Chrome over CDP, port 9222 only (Barry, 2026-10-31). No second CDP Chrome: the old 9223 profile is retired.
  - Its ChatGPT account switcher holds barryyao1017 (active on 10-31) and barrryyao. A third account may be added.
  - One account is active at a time, so run one chat at a time and switch accounts when a quota runs out.
  - Never type credentials. The vault has no ChatGPT login; Barry signs profiles in himself.
- Check which account is active: open chatgpt.com in a tab and read `/api/auth/session` (`user.email`, `account.planType`).
  Never print the token.
- The Free quota: about 26 gpt-6 answers per account, then gpt-6-mini. Re-ask those answers later or mark them
  downgraded. `fastloop.py` flags them.
- Long prompts (pasted context) go through the composer: open `https://chatgpt.com/?temporary-chat=true`, then
  `ctxprobe.submit(tab, text, 0)`, `wait_turn`, `read_sse`. `ui.ask_chatgpt` puts the prompt in the URL and fails
  at ~45k characters.
- The W1/W3 scan queue (`growth/focus/chatgpt-queue.md`) is being retired. Don't route fast-loop chats through it.

| Tool | What it does |
|---|---|
| `growth/evals/visibility_scan.py --questions <file> --n 2 --run-id <date>-<name>` | Blind question sets in the app; T1–T5 tiers (T5 = our `/go/`). |
| `growth/evals/harvest.py --run <run> --brand <Brand>` | From a scan run: searched or not, the queries, clarifying replies, picks, whether our page was retrieved, cited or linked. |
| `growth/evals/ui.py` | W1's app driver (SSE hook: queries, results, snippets). Its narrow hook can drop chat ends; `cardprobe.py` uses a wide hook. |
| `growth/evals/ctxprobe.py chat "<q>" [--same-turn]` | One temporary chat; saves the raw stream. Same-turn echoes are now refused past ~25 words per source; use needle or grid prompts. |
| `growth/evals/cardprobe.py app\|parse\|report` | Rebuilds the answer from the stream: queries, results, catalog products, links by kind (card, button, cite, text), model. |
| `growth/evals/w3score.py <run> [--crawl]` | W3 readings, with crawl gating. |

## The OpenAI API: fallback only (key: keychain item `openai-api-key`; `evallib.env_key("OPENAI_API_KEY")` reads it; expires 2026-11-29)

| Tool | What it does |
|---|---|
| `growth/evals/queryreplay.py api\|report` | Replays an app query with `max_tool_calls: 1` and compares results with the app's. Use for the gap map and live retrieval checks. |
| `growth/evals/apiprobe.py` | Needle and echo probes through the API. |
| `growth/evals/cardprobe.py api` | Full API answers, for comparison with the app. |

- **Cost:** web search is $10 per 1,000 calls plus content tokens at the model's rates.
  - Prices, third-party listings checked 2026-10-31:
    - gpt-6-luna: $0.10 per million input tokens, $0.50 output.
    - gpt-6.1-sol: $2 / $10 in most listings, $1 / $5 in one. Our 10-30 bill fits $1 / $5 better.
    - Claude Haiku 5.5: $0.10 / $0.50. Claude Sonnet 5.5: $2 / $10.
  - Measured calls (10-30 runs, Luna):
    - One-search replay: ~8.7k input tokens, ~40 output, about 1.1 cents, nearly all search fee. The 117-call
      replay cost about $1.20.
    - Free-form answers: ~26k input tokens with ~4 searches.
    - Total DLC-77 spend was about $5, mostly from free-form searching.
  - Estimates:
    - Per product, one fast-loop cycle: $5–10. Gap map ~$1.50; Haiku first pass, then Sonnet judge only on
      shortlisted queries, ~$0.08 each. Competitor set ~$0.30. Ten drafts ~$2 with Luna answer replay, ~$5 with
      Sol. Two weeks of daily retrieval checks ~$1.
    - One-time setup: $8–10.
- **Defaults:** `max_tool_calls: 1` whenever only the result list matters, and `gpt-6-luna` for routine runs. Account
  is Tier 1: Sol hit HTTP 429 at 6 workers, so use 3.
- `search_context_size` had no visible effect.

## Crawl and stored copy

| Tool | What it does |
|---|---|
| `growth/evals/storedcopy.py [--no-fetch]` | Refreshes the crawl log from Cloudflare (`growth/focus/crawls/fetches.jsonl`); maps each sighting to the version it shows; writes `growth/focus/stored-copy.md`. |
| `tools/fetchwho.py` | Splits AI-assistant fetches and `/go/` rows into ours and outside. |
| `tools/landingcheck.py` | ChatGPT-tagged landings (W3 funnel). |

## Gap and competitor work (built for the gap experiment; reuse)

| Tool | What it does |
|---|---|
| `growth/evals/gapexp.py packs\|gaplabel\|drafts\|run\|grade\|report` | Fetches result sets' page text, labels gaps, drafts pages, then has a model answer from our page among the real result set. Its answers came from Claude; the fast loop needs an OpenAI model and the measured budget. |
| `growth/evals/voidscan.py` | Bing demand and live Bing top 10 per query (Bing Keyword Research: about 120 calls a day before 429s). |
| `growth/evals/compqual.py` | Judges what competitor pages are missing. |

## The fast loop: `growth/evals/fastloop.py` (built 2026-10-31, DLC-112)

| Command | What it does |
|---|---|
| `pack --cell runs/<run>/chatgpt/<qid>.json --name <pack>` | Result set from a recorded app chat: rivals fetched now (cached in `runs/fastloop-cache/`); our pages as OpenAI had them stored at the chat. |
| `pack --query "<q>" --question "<shopper question>" --name <pack> [--engine api]` | Default: runs a pinned one-search chat in the app (one gpt-6 message), refuses it if the stream's query differs, then packs its results. `--engine api`: a one-search API replay (about 1 cent) instead. |
| `pack --cell runs/<run>/ctx/<pinned>.json --question "<q>" --name <pack>` | The same from an existing pinned chat (ctxprobe format). |
| `gap <pack> [<pack> ...]` | Claude judge on the rival results: each source's kind (major reviewer, authority, brand store, retailer, niche reviewer, listicle, forum, spam, off-target), whether it answers the question, the verdict (open, contested, saturated) and what's missing (a lead for the open concern). Several packs: recurring domains. |
| `replay <pack> [--draft d.md\|d.html --url /slug --rank 2] --reps 3 --tag v1 [--engine app\|api]` | Builds the context (length rule) and inserts the draft. `--engine app` pastes it into a Free temporary chat, search off, one chat at a time; it is the default from 10-31. `--engine api` answers through the API with search off, as the fallback. Without `--draft`: the pack as recorded. |
| `check <draft.md\|docs/<slug>.html> --packs <p> ... [--ranks 1,3,6] [--must "<phrase>"]` | The copy-rules gate (`growth/focus/fastloop-briefs/COPY-RULES.md`). It passes only if the `/go/` link and a price sit in the first 600 characters, and the link and each `--must` phrase survive the length cut at each rank in every pack. Exits 1 on failure. |
| `score <pack> [--concern "..."]` | Scorecard per tag: cited (T4+), `/go/`, our pick, relied on us, our point carried, top picks. |
| `calibrate --n 40 --run <date>-fastcal [--engine api] [--no-judge] [--alpha a]`, `calreport --run ...` | Replays recorded app chats and reports agreement with what the app did (all prompts, and blind prompts only). The default engine is the app: 40 chats × reps gpt-6 messages, more than one account's quota. |

Constants and prompts are at the top of the script (`BUDGET`, `ALPHA`, `CAP`, `ANSWER_SYSTEM` and `PROMPT_VERSION`
for the API, `PASTES` and `PASTE_VERSION` for the app); bump the version when changing them, since scores across versions don't compare.

## The improvement loop: `growth/evals/iterate.py` (DLC-116)

Run it unattended with `supervise` (same arguments as `run`):

```
python3.12 growth/evals/iterate.py supervise --target rv-2kwh --run <id>   # defaults: --variants 3 --reps 1
```

- **Sampling (defaults since 11-01):** 1 answer per result set (`--reps 1`) over the target's 18 sets, 3 variants a
  round (`--variants 3`): 18 answers per draft, ~72 chats a round. In `rv-open-1` (6 sets × 2 answers, 5 variants) the
  two answers to one set agreed on M1 72% of the time vs 52% by chance, and M1 ran from 0% to 73% by set, so distinct
  sets buy more than repeat answers. The final check sizes itself to `--final-answers` (36) per page, spread over the
  sets (2 per set at 18); `--final-reps` overrides. `--packs a,b,c` runs on a subset (smoke tests).

- **Restarts:** `supervise` restarts the run when it exits. Exit 75 (quota or stall) waits 10 min; a crash waits 1 min.
  A run whose `heartbeat.json` is quiet for 30 min is killed and restarted. It gives up after 8 restarts or 16 h and
  writes why to `log.md`. Answers are cached, so every restart resumes where the last one stopped.
- **Models:** the `&model=` URL pin does not choose the model; the account's quota does (11-01: Plus answered gpt-6
  under a mini pin). So `--models gpt-6,gpt-6-mini` (the default) accepts both and tags each answer with its model and
  account. Drafts are answered interleaved (rep → result set → draft), and M1/M2 are standardized to the round's model
  mix. `--models gpt-6` is strict: off-model answers are dropped.
- **Accounts:** after a mini answer, the other account is tried next, so both accounts' gpt-6 quota is spent before
  mini counts, and gpt-6 is re-probed every 30 min. A usage-cap notice moves to the other account.
- **Quota waits:** capped by `--max-wait` (60 min). After that the run exits 75 and the supervisor resumes it later.
- **Failed chats:** a failed chat triggers `fastloop.ensure_ready`, which restarts the agent's Chrome with agent-vault's
  launcher if 9222 is down and re-logs ChatGPT in through Google as barrryyao. Failed slots are retried in later
  passes, never skipped.
- **Timeouts and retries:** every CDP command has a 120 s deadline; D1 calls, the variant writer and the lesson judge
  retry.

## Promote (fast loop step 7b), after a page is live

| Tier | Tool | What it does |
|---|---|---|
| 1 Internal links | `src/content.py` (home, the `/guides/portable-power-stations/` hub), `src/gaps.py` / `compare.py` records | Link the new page from the pages OAI-SearchBot fetches most (count them in `growth/focus/crawls/fetches.jsonl`), with anchor text in the query's words. Product pages link back automatically (`compared_in`); `/compare` and `llms.txt` pick it up at build time. |
| 2 Submissions | `python3 tools/indexnow.py <urls>`; Google Search Console in the agent's Chrome (barrryyao) | IndexNow reaches Bing. In Search Console, type the URL in the property's inspect bar and click "Request indexing" (the direct `/search-console/inspect?...` URL 404s). From a background CDP tab, call `Emulation.setFocusEmulationEnabled(true)` and focus the input first, or the typed URL is dropped. No OpenAI route. |
| 3 Outreach (matters most) | Fable research subagent briefed with `growth/focus/fastloop-briefs/outreach-brief.md` (freshest threads first, scored for buying demand) → `outreach.md`; instruction set `promote-tier3-instructions.md`; execution subagent over CDP (`ui.Tab`, `fastloop._click`, agent-vault `login`) | Fill every form up to the final Submit, Gmail drafts for email, sign-up pages left open where an account is missing; Barry reviews and submits. Google sign-in as barrryyao is allowed (Quora, ChatGPT). Worked example: `growth/focus/fastloop-runs/rv-2kwh/`. |

## Every probe that touches dealectric.com

Log it with `evallib.footprint(...)` (see `growth/evals/README.md`, "Footprint log"). The project hook already logs
this session's own fetches and browser visits.
