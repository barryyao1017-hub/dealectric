# worker/ — the dealectric.com edge Worker

One Cloudflare Worker (`dealectric-edge`) routed for two paths; GitHub Pages serves everything else.

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

`src/links-map.json` is written by `python3 src/build.py`; rebuild the site before deploying when
products or programs change.

Commands (run from this folder, token from the keychain):

    export CLOUDFLARE_API_TOKEN=$(security find-generic-password -a dealectric -s cloudflare-workers-token -w)
    npx wrangler d1 execute dealectric --remote --file schema.sql     # first time / schema changes
    npx wrangler deploy
    npx wrangler dev --local --port 8787                               # local test (apply schema with --local first)

Reading the data:

    npx wrangler d1 execute dealectric --remote --command "SELECT slug, count(*) n FROM clicks WHERE bot_like=0 AND kind='redirect' GROUP BY slug ORDER BY n DESC"
    npx wrangler d1 execute dealectric --remote --command "SELECT ts, slug, user_agent FROM clicks WHERE kind='ai_fetch' ORDER BY id DESC LIMIT 50"   # which offers assistants are presenting
    npx wrangler d1 execute dealectric --remote --command "SELECT ts, kind, message, page, agent FROM feedback ORDER BY id DESC LIMIT 50"
