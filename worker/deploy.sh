#!/bin/bash
# Deploy the edge Worker, then set its page route (dealectric.com/*) to fail open on the Workers daily request limit.
# wrangler deploy resets every route to fail closed (checked 2026-10-28), and a fail-closed page route would answer
# every page with Cloudflare error 1027 once the Free plan's 100,000 requests a day ran out; fail open serves GitHub
# Pages as if the Worker weren't there. /go/ and /feedback stay fail closed: GitHub Pages has nothing at those paths.
#   bash worker/deploy.sh            (token from the keychain unless CLOUDFLARE_API_TOKEN is set)
set -euo pipefail
cd "$(dirname "$0")"
export CLOUDFLARE_API_TOKEN="${CLOUDFLARE_API_TOKEN:-$(security find-generic-password -a dealectric -s cloudflare-workers-token -w)}"
ZONE=2b54d0073973df64aa0e5b97b4054204
PATTERN='dealectric.com/*'

npx --yes wrangler deploy "$@"

api="https://api.cloudflare.com/client/v4/zones/$ZONE/workers/routes"
rid=$(curl -sf -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" "$api" |
  python3 -c "import json,sys; print(next(r['id'] for r in json.load(sys.stdin)['result'] if r['pattern']==sys.argv[1]))" "$PATTERN")
curl -sf -X PUT -H "Authorization: Bearer $CLOUDFLARE_API_TOKEN" -H "Content-Type: application/json" "$api/$rid" \
  -d "{\"pattern\":\"$PATTERN\",\"script\":\"dealectric-edge\",\"request_limit_fail_open\":true}" |
  python3 -c "import json,sys; r=json.load(sys.stdin); ok=r.get('success') and r['result'].get('request_limit_fail_open'); print('route', sys.argv[1], 'fail open' if ok else 'NOT set to fail open'); sys.exit(0 if ok else 2)" "$PATTERN"
