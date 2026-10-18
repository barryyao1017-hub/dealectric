# worker/ — the dealectric.com edge Worker

One Cloudflare Worker (`dealectric-edge`) routed for two paths; GitHub Pages serves everything else.

- `GET /go/<slug>` — looks the slug up in `src/links-map.json`, logs a row to D1 `clicks`, and 302s to the
  CJ/Awin link with the sub-ID set to `<slug>.<click_id>` (CJ `sid`, Awin `clickref`), so a commission in the
  network's report can be matched to one click here.
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

    npx wrangler d1 execute dealectric --remote --command "SELECT slug, count(*) n FROM clicks WHERE bot_like=0 GROUP BY slug ORDER BY n DESC"
    npx wrangler d1 execute dealectric --remote --command "SELECT ts, kind, message, page, agent FROM feedback ORDER BY id DESC LIMIT 50"
