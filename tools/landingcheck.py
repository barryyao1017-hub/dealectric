#!/usr/bin/env python3.12
"""Check the Worker's landing log (W3 step 0, added 2026-10-28): one tagged request, as a browser sends it after a
click on a ChatGPT link, then the D1 `landings` row it should have written.

  python3.12 tools/landingcheck.py                                   # /bluetti-ac200l
  python3.12 tools/landingcheck.py tesla-model-y-back-seat-screen

It also checks that the tagged page is the same bytes as the untagged one, apart from Cloudflare's email obfuscation,
which differs on every request. The request is ours three ways: its user agent carries dealectric-landingcheck
(tools/fetchwho.py counts that as ours), its query carries dlc_check=<id> (filter those rows out of landing counts),
and it goes to the footprint log as app "direct-fetch". Exit 0 when the row is there and the pages match.
"""
import re
import secrets
import ssl
import sys
import time
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "growth" / "evals"))
import evallib as E  # noqa: E402

SITE = "https://dealectric.com"
# A real browser's user agent plus our mark: bot_like stays 0 in D1, so the check goes down the path a person's click takes.
UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/141.0.0.0 "
      "Safari/537.36 dealectric-landingcheck/1.0")
HEADERS = {"User-Agent": UA, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
           "Accept-Language": "en-US,en;q=0.9"}
CF_EMAIL = re.compile(rb'(email-protection#|data-cfemail=")[0-9a-f]+')


def _ctx():
    try:
        import certifi
        return ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        return ssl.create_default_context()


def get(url: str) -> tuple[int, bytes]:
    req = urllib.request.Request(url, headers=HEADERS)
    with urllib.request.urlopen(req, timeout=30, context=_ctx()) as r:
        return r.status, r.read()


def main() -> int:
    page = (sys.argv[1] if len(sys.argv) > 1 else "bluetti-ac200l").strip("/")
    cid = secrets.token_hex(4)
    plain, tagged = f"{SITE}/{page}", f"{SITE}/{page}?utm_source=chatgpt.com&dlc_check={cid}"
    started = E.now_iso()
    err = None
    try:
        s1, b1 = get(plain)
        s2, b2 = get(tagged)
    except Exception as e:  # noqa: BLE001
        err = f"{type(e).__name__}: {e}"
    E.footprint("direct-fetch", started, E.now_iso(), script="landingcheck.py", run_id=f"landingcheck-{cid}", prompt_id=page,
                fetched=[plain, tagged], error=err, user_agent=UA)
    if err:
        print(f"request failed: {err}")
        return 1
    same = s1 == s2 and CF_EMAIL.sub(rb"\1", b1) == CF_EMAIL.sub(rb"\1", b2)
    print(f"untagged {s1} {len(b1)} bytes, tagged {s2} {len(b2)} bytes: {'same page' if same else 'PAGES DIFFER'}")

    row = None
    for _ in range(6):   # the Worker writes after it has answered; give D1 a few seconds
        time.sleep(3)
        rows, qerr = E.d1_query("SELECT ts, page, path, status, query, utm_source, country, bot_like, verified_bot, purpose "
                                f"FROM landings WHERE query LIKE '%dlc_check={cid}%'")
        if qerr:
            print(f"D1 query failed: {qerr}")
            return 1
        if rows:
            row = rows
            break
    if not row:
        print(f"no landings row for dlc_check={cid}")
        return 1
    print(f"{len(row)} landings row(s): {row[0]}")
    return 0 if same and len(row) == 1 else 1


if __name__ == "__main__":
    sys.exit(main())
