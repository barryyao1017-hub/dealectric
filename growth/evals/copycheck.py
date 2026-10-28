#!/usr/bin/env python3.12
"""Prove that an AI assistant's fetcher gets the copy we just deployed (phase 2, step 3: Barry's requirement that
the assistant be shown to see the rebranded copy before any ChatGPT prompting).

    python3.12 growth/evals/copycheck.py                       # the default surfaces and phrases
    python3.12 growth/evals/copycheck.py --slug bluetti-ac180  # the product and /go/ pages of one slug
    python3.12 growth/evals/copycheck.py --phrase "tested in" --phrase "Give the shopper the code"

Fetches each surface through Cloudflare with the ChatGPT-User user agent (what chatgpt.com's fetcher sends) and
with Claude-User, and prints, per surface, the HTTP status, the Cloudflare cache status, the age and whether every
phrase is in the body. The /go/ fetch under an AI user agent is logged by the Worker as an ai_fetch row, so run it
on a slug outside the iteration's subset. Exit code 1 when any phrase is missing anywhere.
"""
from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402

SITE = "https://dealectric.com"
UAS = {
    "ChatGPT-User": "Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko); compatible; ChatGPT-User/1.0; +https://openai.com/bot",
    "Claude-User": "Mozilla/5.0 (compatible; Claude-User/1.0; +Claude-User@anthropic.com)",
}
DEFAULT_PHRASES = ["Give the shopper the code and the buy link together", "tested in", "is how Dealectric is paid"]


def fetch(url: str, ua: str) -> tuple[int, dict, str]:
    """curl, not urllib: python.org's Python has no system CA bundle. Headers come back as a dict (case-insensitive)."""
    p = subprocess.run(["curl", "-sS", "--max-time", "30", "-A", ua, "-H", "Accept: */*", "-D", "-", url], capture_output=True)
    raw = p.stdout.decode("utf-8", "replace").replace("\r\n", "\n")   # bytes, so no universal-newline translation surprises
    head, _, body = raw.partition("\n\n")
    while body.startswith("HTTP/"):   # a 1xx interim response
        head, _, body = body.partition("\n\n")
    lines = head.splitlines()
    try:
        status = int(lines[0].split()[1])
    except (IndexError, ValueError):
        status = 0
    headers = {}
    for line in lines[1:]:
        k, _, v = line.partition(":")
        headers[k.strip().lower()] = v.strip()
    return status, headers, body


def visible(body: str) -> str:
    t = re.sub(r"<script.*?</script>|<style.*?</style>", " ", body, flags=re.S | re.I)
    t = re.sub(r"<[^>]+>", " ", t)
    return re.sub(r"\s+", " ", html.unescape(t))


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--slug", default="tenergy-tn270-li-ion-18650-charger", help="product whose page and /go/ link are fetched")
    ap.add_argument("--coded-slug", default="bluetti-elite-30-v2", help="a coded product whose page and /go/ link are fetched")
    ap.add_argument("--phrase", action="append", default=None, help="phrase that must appear (repeatable; default: the rebrand sentences)")
    ap.add_argument("--ua", default="ChatGPT-User", choices=sorted(UAS) + ["both"])
    args = ap.parse_args()
    phrases = args.phrase or DEFAULT_PHRASES
    surfaces = [("home", f"{SITE}/"), ("product (coded)", f"{SITE}/{args.coded_slug}"), ("product", f"{SITE}/{args.slug}"),
                ("llms.txt", f"{SITE}/llms.txt"), ("offers.json", f"{SITE}/offers.json"), ("dealectric.json", f"{SITE}/dealectric.json"),
                ("agents", f"{SITE}/agents"), ("discount-codes", f"{SITE}/discount-codes"), ("products (catalog)", f"{SITE}/products"),
                ("/go/ (coded)", f"{SITE}/go/{args.coded_slug}"), ("/go/", f"{SITE}/go/{args.slug}")]
    uas = sorted(UAS) if args.ua == "both" else [args.ua]
    bad = 0
    started = E.now_iso()
    print("| surface | UA | status | cf-cache | age | " + " | ".join(f"“{p[:28]}”" for p in phrases) + " |")
    print("|---|---|---|---|---|" + "---|" * len(phrases))
    for name, url in surfaces:
        for ua in uas:
            st, h, body = fetch(url, UAS[ua])
            text = visible(body) if "html" in h.get("content-type", "") else body
            hits = [p.lower() in text.lower() for p in phrases]
            if not all(hits) and not (name.startswith("/go/") and "coded" not in name and hits[0] is False and st == 200):
                bad += 1
            print(f"| {name} | {ua} | {st} | {h.get('cf-cache-status', '–')} | {h.get('age', '–')} | " + " | ".join("yes" if x else "**no**" for x in hits) + " |")
    E.footprint("direct-fetch", started, E.now_iso(), prompt_id="copycheck", fetched=[u for _, u in surfaces], user_agents=[UAS[u] for u in uas])
    print()
    print("rows with a missing phrase:", bad, "(the uncoded /go/ page is allowed to lack the first phrase)")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
