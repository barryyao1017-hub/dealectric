#!/usr/bin/env python3
"""Push dealectric.com URLs to IndexNow (shared by Bing, Yandex, Naver, Seznam, Yep).

  python3 tools/indexnow.py                 # every URL in docs/sitemap.xml
  python3 tools/indexnow.py URL [URL ...]   # just these

The key is INDEXNOW_KEY in src/build.py; build.py publishes it as /<key>.txt, which is what
IndexNow checks. Run after `git push` once the key file is live (the script checks).
"""
import json, re, sys, os, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# Read the key from build.py as text so this script runs on any Python 3 (build.py itself needs 3.12+).
INDEXNOW_KEY = re.search(r'^INDEXNOW_KEY = "([^"]+)"', open(os.path.join(ROOT, "src", "build.py")).read(), re.M).group(1)

HOST = "dealectric.com"
UA = {"User-Agent": "dealectric-indexnow/1.0 (+https://dealectric.com/contact)"}  # Cloudflare 403s the bare urllib UA


def sitemap_urls():
    s = open(os.path.join(ROOT, "docs", "sitemap.xml")).read()
    return re.findall(r"<loc>(.*?)</loc>", s)


def main(urls):
    key_url = f"https://{HOST}/{INDEXNOW_KEY}.txt"
    live = urllib.request.urlopen(urllib.request.Request(key_url, headers=UA)).read().decode().strip()
    if live != INDEXNOW_KEY:
        sys.exit(f"key file at {key_url} does not match ({live[:40]!r}); push the build first")
    body = json.dumps({"host": HOST, "key": INDEXNOW_KEY, "keyLocation": key_url, "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8", **UA})
    try:
        with urllib.request.urlopen(req) as r:
            print(r.status, r.reason, f"({len(urls)} URLs)")
    except urllib.error.HTTPError as e:
        print(e.code, e.reason, e.read().decode()[:300]); sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:] or sitemap_urls())
