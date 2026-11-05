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
  generic clients keep the redirect.
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
  emails Barry (barrryyao@gmail.com, a verified Email Routing destination) from `sales@mail.dealectric.com`, and writes
  one row to D1 `sales` (unique per network + transaction id, so a sale alerts once).
  - Awin: Toolbox → Transaction Notifications is Enabled, method GET, callback
    `https://dealectric.com/hook/awin?k=<key>&tid=!!!transactionId!!!&c=!!!commission!!!&amt=!!!transactionAmount!!!&cur=!!!transactionCurrency!!!&mid=!!!merchantId!!!&cr=!!!clickRef!!!&date=!!!transactionDate!!!`.
    The key is the Worker secret `AWIN_HOOK_KEY` (keychain `awin-hook-key`); a wrong key gets a 404.
  - CJ: no publisher postback, so the cron trigger queries `publisherCommissions` (commissions.api.cj.com, CID 8096118)
    over the last 3 days of posting dates with the personal access token `dealectric-sale-alerts` (Worker secret
    `CJ_TOKEN`, keychain `cj-api-token`; developers.cj.com → Personal Access Tokens).
  - Amazon Associates has no alert or API for this; check its dashboard.
  - Email needs Email Routing on the sender's domain. It runs on the `mail` subdomain only, so the apex keeps its
    Porkbun forwarding MX. Test the wiring end to end (sends a TEST email, stores nothing):
    `curl "https://dealectric.com/hook/awin?k=$(security find-generic-password -a dealectric -s awin-hook-key -w)&tid=test1&c=1&amt=2&cr=bluetti-ac180.x"`
    (`{"ok": true}`, or the send error with a 502).
  - The daily update (`tools/dailyupdate.py`) still reads CJ as a backup.

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
