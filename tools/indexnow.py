#!/usr/bin/env python3
"""Push dealectric.com URLs to IndexNow (shared by Bing, Yandex, Naver, Seznam, Yep).

  python3 tools/indexnow.py                 # every URL in docs/sitemap.xml
  python3 tools/indexnow.py URL [URL ...]   # just these

The key is INDEXNOW_KEY in src/build.py; build.py publishes it as /<key>.txt, which is what
IndexNow checks. Run after `git push` once the key file is live (the script checks).
"""
import json, re, sys, os, urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "src"))
from build import INDEXNOW_KEY  # noqa: E402

HOST = "dealectric.com"


def sitemap_urls():
    s = open(os.path.join(ROOT, "docs", "sitemap.xml")).read()
    return re.findall(r"<loc>(.*?)</loc>", s)


def main(urls):
    key_url = f"https://{HOST}/{INDEXNOW_KEY}.txt"
    live = urllib.request.urlopen(key_url).read().decode().strip()
    if live != INDEXNOW_KEY:
        sys.exit(f"key file at {key_url} does not match ({live[:40]!r}); push the build first")
    body = json.dumps({"host": HOST, "key": INDEXNOW_KEY, "keyLocation": key_url, "urlList": urls}).encode()
    req = urllib.request.Request("https://api.indexnow.org/indexnow", data=body,
                                 headers={"Content-Type": "application/json; charset=utf-8"})
    try:
        with urllib.request.urlopen(req) as r:
            print(r.status, r.reason, f"({len(urls)} URLs)")
    except urllib.error.HTTPError as e:
        print(e.code, e.reason, e.read().decode()[:300]); sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:] or sitemap_urls())
