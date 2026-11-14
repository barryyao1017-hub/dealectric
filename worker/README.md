# worker/ — the dealectric.com edge Worker

One Cloudflare Worker (`dealectric-edge`). It answers `/go/` and `/feedback` itself; every other request goes to
GitHub Pages unchanged (since 2026-10-28 the Worker is routed for `dealectric.com/*` to log landings, see below).

- `GET /go/<slug>` — looks the slug up in `src/links-map.json`, logs a row to D1 `clicks`, and 302s to the
  CJ/Awin link with the sub-ID set to `<slug>.<click_id>` (CJ `sid`, Awin `clickref`), so a commission in the
  network's report can be matched to one click here. Verified AI assistant fetchers (Cloudflare bot category
  "AI Assistant", or a ChatGPT-User / Claude-User / Perplexity-User / OAI-SearchBot / GPTBot / ClaudeBot /
  PerplexityBot / Google-Extended user agent) get a 200 `text/plain` page instead of the 302: it tells the
  assistant to present the `/go/` URL itself as the buy link, with the verified price and product page URL.
  That keeps the tracked link in the assistant's answer and sends no bot click to the network (the
  2026-10-18 probe in growth/probes showed ChatGPT following the redirect and linking the merchant page).
  Such rows have `kind = 'ai_fetch'` in `clicks`; browser clicks have `kind = 'redirect'`. curl and other
  generic clients keep the redirect. `bot_like` is 1 for a scanner-looking user agent and, since 2026-11-06, for any
  request from Google's networks (`SCANNER_ASNS`; `clicks.asn` and `landings.asn` store the network): a new YouTube
  video's links drew 12 hits in 2 s from Google's scanners, some posing as ordinary Windows Chrome.
  Since 2026-11-09 (DLC-216) it is also 1 for cloud/hosting networks (`HOSTING_ASNS`, unless the click carries an
  agent tag), for the iOS 13.2.3 and bare `Mozilla/5.0 (compatible)` scraper agents, and for bursts: a browser (same
  user agent, country, network) opening 5+ different offers within 60 s has all its clicks in that window flagged.
  Past rows were reflagged by the same rules on 2026-11-09 (unflagged clicks 1,671 -> 647; ChatGPT-tagged ones the
  daily update counts were unchanged, since its own filter already dropped the bare prober).
- `GET /self-exclude` (2026-11-07) — marks the browser that opens it as one of ours: a one-year `dlx_self=1` cookie,
  after which that browser's `/go/` clicks and tagged landings are stored with `bot_like = 2` and so drop out of every
  shopper count (`tools/dailyupdate.py`, `tools/fetchwho.py` and the queries below all take `bot_like = 0`). Open it
  once in each of Barry's browsers (Personal Chrome profiles, phone, Pane, Agent Chrome); `/self-exclude?off` clears
  it. Linked from nowhere, noindex. It is the only cookie the site ever sets, and it only ever marks our own browsers;
  D1 stores no IP, so nothing else can tell Barry's clicks from a shopper's after the fact.
- Shopper codes (2026-11-12): beside 1 (bot) and 2 (ours), `bot_like = 3` is a partner review (a page or `/go/` link
  opened from an affiliate network's dashboard: Awin, CJ, Rakuten, Impact, ...) and, in `pageviews` only, `4` is a
  visit with no source (no tag, no referrer). An untagged arrival with a Chrome 9+ majors old, or one agent arriving
  untagged from 3+ networks within 2 minutes, is 1; a page opened from our own pages takes its visit's arrival code.
  So `bot_like = 0` is a shopper: a browser that came from an assistant, a search engine or another site. All rows
  since 10-29 were re-judged by these rules on 2026-11-12 (the dashboard showed 29 shoppers by mid-morning that day; 8 by these rules).
  Since 2026-11-13 a page view from one of our own pages with no arrival from the same browser (agent, country, network)
  in the last 30 minutes is a crawler hop (1): a fleet on ~90 networks opened pages and `/go/` links with dealectric.com
  referrers at 05:18Z that day, which put the dashboard at 113 shoppers for 11-12. Stored rows were re-judged the same day.
- `GET|POST /feedback` — accepts `message` (required), `kind`, `page`, `agent`, `contact` as query parameters
  or a JSON/form body; stores a row in D1 `feedback`; returns `{ok, ticket}`. A bare GET returns the usage doc.
  GET is allowed on purpose: most assistants only have a fetch-URL tool.

- Every other path (pages, files): passed to GitHub Pages with `fetch(request)` and returned as is, for every
  visitor and crawler alike: no rewriting, no added header, cookie or script (checked 2026-10-28: same bytes as
  before the route, apart from Cloudflare's own per-request email obfuscation, and Web Analytics is still injected).
  A request whose query carries `utm_source` also writes a row to D1 `landings` (page, query, status, referrer,
  user agent, country, bot flags, `Sec-Purpose`; no IP). `bot_like` is also 1 for a user agent with no browser engine
  token: during a chat ChatGPT's backend fetches the result URLs it shows, utm tag included, as bare
  `Mozilla/5.0 (compatible)` (5 such rows inside W1's scan chats on 2026-10-28, none a person). ChatGPT appends `utm_source=chatgpt.com` to every link it
  shows, source pills included, so a ChatGPT landing, the `/go/` click from that page (its `clicks.referrer` is the
  landing URL) and a sale line up. An exception falls through to the origin (`passThroughOnException`), and the
  `dealectric.com/*` route is set to fail open on the Free plan's daily request limit (about 1-5k requests a day in
  October 2026, against 100k). `wrangler deploy` resets that flag, so deploy with `deploy.sh`, which sets it again.
  One exception since 2026-11-03 (DLC-146): a request that Cloudflare verifies as an "AI Assistant" but whose user
  agent is not one of the answer fetchers above (an agent's own cloud browser, such as Meta's Muse, which reads pages
  as Linux Chrome 138) gets its HTML with `utm_source=<agent>` added to every dealectric.com link (`muse`,
  `chatgpt-agent` or `signed-agent`, from the `Signature-Agent` header when there is one). The shopper's tap on a link
  the agent handed over then carries the tag into `clicks` / `landings`. `/go/` URLs written in page text, JSON-LD and
  `<meta content>` (the description a link preview reads) get the tag too: Muse copied an untagged one from there. Each such page or text fetch also writes a
  row to D1 `agent_pages` (path, user agent, country, ASN and network name, `Signature-Agent`, `Signature-Input`).
  Test locally with `npx wrangler dev --local --local-upstream dealectric.com --upstream-protocol https --var TEST_AGENT_UA:dlc-test-agent`
  and `curl -A dlc-test-agent`.
  Check after a deploy: `python3.12 tools/landingcheck.py` (one tagged request of ours, marked `dlc_check=` and
  logged to the footprint log as `direct-fetch`; exit 0 when its row is in D1 and the page is unchanged).

- `GET /hook/awin?k=<key>&tid=...` and the 30-minute cron (since 2026-11-05) — sale alerts: every new commission
  emails Barry (barrryyao@gmail.com, a verified Email Routing destination) from `sales@dealectric.com`, and writes
  one row to D1 `sales` (unique per network + transaction id, so a sale alerts once).
  - Awin: Toolbox → Transaction Notifications is Enabled, method GET, callback
    `https://dealectric.com/hook/awin?k=<key>&tid=!!!transactionId!!!&c=!!!commission!!!&amt=!!!transactionAmount!!!&cur=!!!transactionCurrency!!!&mid=!!!merchantId!!!&cr=!!!clickRef!!!&date=!!!transactionDate!!!&ct=!!!clickTime!!!`
    (`ct` since 2026-11-13, DLC-209; it replaced `&vc=!!!voucherCode!!!` of 11-08, which is not an Awin macro and came
    through as its own text). Awin cannot tell us the code on an order, but a sale credited by a code assigned to us
    (BLUETTI's DEALECTRIC) arrives with no clickRef and a click time equal to the order time; the alert says so, and
    `sales.click_time` keeps the click time.
    The key is the Worker secret `AWIN_HOOK_KEY` (keychain `awin-hook-key`); a wrong key gets a 404.
  - CJ: no publisher postback, so the cron trigger queries `publisherCommissions` (commissions.api.cj.com, CID 8096118)
    over the last 3 days of posting dates with the personal access token `dealectric-sale-alerts` (Worker secret
    `CJ_TOKEN`, keychain `cj-api-token`; developers.cj.com → Personal Access Tokens).
  - CJ's `coupon` field goes into `sales.voucher` too.
  - Rakuten (since 2026-11-13): no publisher postback either, so the same cron reads the Events API
    (`api.linksynergy.com/events/1.0/transactions`, last 3 days of process dates, 1,000 a page). It signs in with
    `POST /token`, `Authorization: Bearer <token key>` and `scope=<SID>` (var `RAKUTEN_SID` = 4771345); the token key
    is base64 of the Developer Portal app "dealectric-sales-sync"'s `client_id:client_secret` (Worker secret
    `RAKUTEN_TOKEN_KEY`; keychain `rakuten-token-key`, plus `rakuten-client-id` / `rakuten-client-secret`). Rows land in
    `sales` with network `rakuten`, txn_id `<etransaction_id>:<sku>:<process_date>` and sub_id = the click's `u1`.
  - Amazon Associates has no alert or API for this; check its dashboard.
  - `tools/dailyupdate.py` reads the CJ API itself (same token, from the keychain) and the Awin rows from D1 `sales`,
    so the daily update's North Star count covers both networks (since 2026-11-08).
  - Email Routing is switched on for dealectric.com without its MX records, so the apex keeps its Porkbun forwarding
    MX. Never press "Add missing records" on Email Routing → Settings: it would add Cloudflare's MX and take over the
    forwarding. Sending needs only the two authentication records, added by hand on 2026-11-05: TXT
    `cf2024-1._domainkey` (Cloudflare's DKIM key, as shown on that settings page) and Cloudflare in the one apex SPF,
    `v=spf1 include:_spf.porkbun.com include:_spf.mx.cloudflare.net ~all`. Before them Cloudflare's activity log said
    Delivered but Gmail never showed the mail. (Cloudflare's newer "Email Sending" product needs Workers Paid; the
    `send_email` binding to a verified destination is free.) Test the wiring end to end (sends a TEST email, stores
    nothing):
    `curl "https://dealectric.com/hook/awin?k=$(security find-generic-password -a dealectric -s awin-hook-key -w)&tid=test1&c=1&amt=2&cr=bluetti-ac180.x"`
    (`{"ok": true}`, or the send error with a 502).
  - The daily update (`tools/dailyupdate.py`) still reads CJ as a backup.

- `POST /mcp` (since 2026-11-06, DLC-182; `src/mcp.js`, brief `growth/chatgpt-app/brief.md`) — the MCP server for
  the ChatGPT app directory and any other MCP client. Streamable HTTP, stateless JSON replies, no sign-in, no
  sessions; `GET /mcp` answers 405 with a pointer. Three read-only tools: `search_products`, `check_codes`,
  `price_history`. Data comes from `/offers.json` and `/price-history.json` on the origin (both written by
  `src/build.py`; the price history is the cart price per day from `growth/codes/*-checks.jsonl`), cached 5 min, so the
  daily sweep's push keeps the tools current with no redeploy. Amazon records are left out. Buy links carry `?via=app`,
  and `/go/<slug>?via=app` on a checkout record (`cart: true`) lands on the product page through `store_url`, because
  OpenAI's app rules bar linking straight to a checkout. Each tool call writes a row to D1 `mcp_calls` (tool, args,
  result count, client name, user agent, country; no IP). `/.well-known/openai-apps-challenge` serves the Worker secret
  `OPENAI_APPS_CHALLENGE` once it is set (OpenAI's domain check at submission).
  Test locally: `python3 -m http.server 8799 --directory ../docs` and
  `npx wrangler dev --local --port 8788 --var DATA_BASE:http://127.0.0.1:8799`, then
  `npx @modelcontextprotocol/inspector --cli http://localhost:8788/mcp --transport http --method tools/list`.
  Usage: `npx wrangler d1 execute dealectric --remote --command "SELECT ts, tool, args, results, client FROM mcp_calls ORDER BY id DESC LIMIT 20"`.

`src/links-map.json` is written by `python3 src/build.py`; rebuild the site before deploying when
products or programs change.

Commands (run from this folder, token from the keychain):

    export CLOUDFLARE_API_TOKEN=$(security find-generic-password -a dealectric -s cloudflare-workers-token -w)
    npx wrangler d1 execute dealectric --remote --file schema.sql     # first time / schema changes
    bash deploy.sh                                                     # wrangler deploy + page route fail open
    npx wrangler dev --local --port 8787                               # local test (apply schema with --local first)

Reading the data:

    npx wrangler d1 execute dealectric --remote --command "SELECT slug, count(*) n FROM clicks WHERE bot_like=0 AND kind='redirect' GROUP BY slug ORDER BY n DESC"
    npx wrangler d1 execute dealectric --remote --command "SELECT ts, slug, user_agent FROM clicks WHERE kind='ai_fetch' ORDER BY id DESC LIMIT 50"   # which offers assistants are presenting
    npx wrangler d1 execute dealectric --remote --command "SELECT ts, kind, message, page, agent FROM feedback ORDER BY id DESC LIMIT 50"
    # human landings from ChatGPT links, without our own checks (W3 funnel: landing -> /go/ click -> sale)
    npx wrangler d1 execute dealectric --remote --command "SELECT ts, page, status, country, purpose, user_agent FROM landings WHERE utm_source='chatgpt.com' AND bot_like=0 AND verified_bot='' AND query NOT LIKE '%dlc_check=%' ORDER BY id DESC LIMIT 50"
    npx wrangler d1 execute dealectric --remote --command "SELECT ts, slug, referrer FROM clicks WHERE kind='redirect' AND referrer LIKE '%utm_source=%' ORDER BY id DESC LIMIT 50"   # /go/ clicks made from a tagged landing
    # clicks by assistant (ChatGPT sends no referrer but appends ?utm_source=chatgpt.com)
    npx wrangler d1 execute dealectric --remote --command "SELECT utm_source, kind, count(*) n FROM clicks GROUP BY utm_source, kind ORDER BY n DESC"
