#!/usr/bin/env python3
"""Query Cloudflare's GraphQL Analytics API for dealectric.com.

The read-only token lives in the macOS keychain (service cloudflare-api-token, account dealectric);
it is never stored in this repo.

  python3 tools/cf.py '{viewer{zones(filter:{zoneTag:$zone}){...}}}'   # query as argument
  python3 tools/cf.py < query.graphql                                    # or on stdin

$zone and $account are substituted with the dealectric.com zone tag and the account tag.
"""
import json, ssl, subprocess, sys, urllib.request

ZONE = "2b54d0073973df64aa0e5b97b4054204"
ACCOUNT = "2edd290b5cc542978327feb2e99c975c"


def token():
    return subprocess.run(["security", "find-generic-password", "-a", "dealectric", "-s", "cloudflare-api-token", "-w"],
                          capture_output=True, text=True, check=True).stdout.strip()


def _ctx():
    """python.org's Python 3.12 has no system CA bundle; use certifi's when it is installed."""
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def query(q):
    q = q.replace("$zone", json.dumps(ZONE)).replace("$account", json.dumps(ACCOUNT))
    req = urllib.request.Request("https://api.cloudflare.com/client/v4/graphql", data=json.dumps({"query": q}).encode(),
                                 headers={"Authorization": f"Bearer {token()}", "Content-Type": "application/json"})
    with urllib.request.urlopen(req, context=_ctx()) as r:
        return json.load(r)


if __name__ == "__main__":
    print(json.dumps(query(sys.argv[1] if len(sys.argv) > 1 else sys.stdin.read()), indent=1))
