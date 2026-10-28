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
  Check after a deploy: `python3.12 tools/landingcheck.py` (one tagged request of ours, marked `dlc_check=` and
  logged to the footprint log as `direct-fetch`; exit 0 when its row is in D1 and the page is unchanged).

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
