# Tools, setup and costs

All scripts run with `python3.12` from the repo root. `git pull` first: the daily cart check pushes from another
clone.

## Driving the ChatGPT app

- Agent Chrome over CDP: port 9222 is profile 1, signed in to Barry's Free account. Port 9223 is profile 2, signed
  out of ChatGPT. Never type credentials; logins go through agent-vault.
- Only the W1 session drives chatgpt.com for scans. Other work adds a row to `growth/focus/chatgpt-queue.md` unless
  Barry says otherwise.
- The Free quota: after it runs out, answers come from gpt-6-mini. Re-ask those answers later, or mark them
  downgraded.

| Tool | What it does |
|---|---|
| `growth/evals/visibility_scan.py --questions <file> --n 2 --run-id <date>-<name>` | Blind question sets in the app; T1–T5 tiers (T5 = our `/go/`). |
| `growth/evals/harvest.py --run <run> --brand <Brand>` | From a scan run: searched or not, the queries, clarifying replies, picks, whether our page was retrieved, cited or linked. |
| `growth/evals/ui.py` | W1's app driver (SSE hook: queries, results, snippets). Its narrow hook can drop chat ends; `cardprobe.py` uses a wide hook. |
| `growth/evals/ctxprobe.py chat "<q>" [--same-turn]` | One temporary chat; saves the raw stream. Same-turn echoes are now refused past ~25 words per source; use needle or grid prompts. |
| `growth/evals/cardprobe.py app\|parse\|report` | Rebuilds the answer from the stream: queries, results, catalog products, links by kind (card, button, cite, text), model. |
| `growth/evals/w3score.py <run> [--crawl]` | W3 readings, with crawl gating. |

## The OpenAI API (key: keychain item `openai-api-key`; `evallib.env_key("OPENAI_API_KEY")` reads it; expires 2026-11-29)

| Tool | What it does |
|---|---|
| `growth/evals/queryreplay.py api\|report` | Replays an app query with `max_tool_calls: 1` and compares results with the app's. Use for the gap map and live retrieval checks. |
| `growth/evals/apiprobe.py` | Needle and echo probes through the API. |
| `growth/evals/cardprobe.py api` | Full API answers, for comparison with the app. |

- **Cost:** web search is $10 per 1,000 calls plus content tokens at the model's rates. A one-search replay is about
  1 cent. The 117-call replay cost about $1.20. Total DLC-77 API spend was about $5, mostly from free-form searching.
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

## Not built yet

- `growth/evals/fastloop.py`: context builder (rival pages cut to the measured share per rank, plus the draft),
  answer replay with search off, and a scorecard (cited, picked, our point carried, `/go/` copied).
- Gap judge prompt, and a calibration script that replays recorded app chats (`runs/2026-10-30-cardprobe/`,
  `runs/2026-10-30-ctxprobe/`) and compares results with what the app did.

## Every probe that touches dealectric.com

Log it with `evallib.footprint(...)` (see `growth/evals/README.md`, "Footprint log"). The project hook already logs
this session's own fetches and browser visits.
