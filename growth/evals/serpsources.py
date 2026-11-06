#!/usr/bin/env python3
"""Free search-result sources for gap mining's coverage reading, each held under a hard cap (DLC-168, 2026-11-05).

Barry, 11-05: discovery must cost $0, with every source limited to zero dollars. So:
- every source has a daily cap (and a lifetime cap for one-time allowances) set below its free quota;
- every call is appended to growth/gapmine/ledger.jsonl before the next one is made;
- any 401/402/403/429 or quota/billing wording stops that source for the day (`stopped` row), and a one-time source
  that says its allowance is used up is stopped for good (`exhausted` row);
- a source without its keychain key is skipped, never signed up for (Barry creates accounts and stores keys).

    fetch(source, query) -> list of {"rank", "title", "url"} or None (skipped / capped / error)
    available() -> sources with a key and room under today's cap, in priority order
    python3.12 growth/evals/serpsources.py status          # used / cap per source today
    python3.12 growth/evals/serpsources.py test <source> "<query>"
"""
from __future__ import annotations

import datetime as _dt
import json
import re
import subprocess
import sys
import time
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "growth" / "gapmine" / "ledger.jsonl"

# Caps sit below each provider's free allowance as published on 2026-11-05 (growth/gapmine/daily-plan.md).
SOURCES = {
    #  name          daily  lifetime  keychain item       pause s
    "claude":     dict(daily=60, life=None, key=None, pause=0),          # claude -p WebSearch: plan usage, no $
    "serpapi":    dict(daily=8, life=None, key="serpapi-api-key", pause=75),   # 250/month, 50/hour; engine=bing
    "tavily":     dict(daily=30, life=None, key="tavily-api-key", pause=1),    # 1,000 credits/month, basic = 1
    "serper":     dict(daily=100, life=2400, key="serper-api-key", pause=1),   # 2,500 one-time
    "jina":       dict(daily=50, life=900, key="jina-api-key", pause=2),       # 10M tokens one-time, >=10k/search
    "bing":       dict(daily=40, life=None, key=None, pause=6),          # Agent Chrome (CDP 9222); blocks after ~300
}
PRIORITY = ["serpapi", "bing", "tavily", "serper", "jina", "claude"]   # Bing-backed first; re-ordered by calibration
# Calibration vs Bing (gapmine.py srccal, 54 Bing-scored queries, 2026-11-05):
#   claude  Spearman 0.29, gate (<0.4) agreement 27/54, open 37 vs Bing's 18 -> NOT used for gating (spam-heavy results)
GATING = {"serpapi", "bing"}   # sources whose coverage may put a cluster in the page queue; others join after srccal >= 0.5
STOP_WORDS = re.compile(r"quota|exceed|limit|credit|billing|payment|insufficient|upgrade|plan", re.I)


def today() -> str:
    return _dt.date.today().isoformat()


def _rows() -> list[dict]:
    if not LEDGER.exists():
        return []
    out = []
    for line in LEDGER.read_text().splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def _log(source: str, query: str, status: str, n: int = 0, note: str = "") -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    with LEDGER.open("a") as f:
        f.write(json.dumps({"ts": _dt.datetime.now().isoformat(timespec="seconds"), "date": today(), "source": source,
                            "q": query, "status": status, "n": n, "note": note[:200]}) + "\n")


def usage(source: str, rows: list[dict] | None = None) -> dict:
    rows = _rows() if rows is None else rows
    mine = [r for r in rows if r["source"] == source]
    calls = [r for r in mine if r["status"] in ("ok", "short", "empty", "error")]   # every request that reached the provider
    return {"today": sum(1 for r in calls if r["date"] == today()), "life": len(calls),
            "stopped": any(r["status"] == "stopped" and r["date"] == today() for r in mine),
            "exhausted": any(r["status"] == "exhausted" for r in mine)}


def key(source: str) -> str | None:
    item = SOURCES[source]["key"]
    if not item:
        return ""
    p = subprocess.run(["security", "find-generic-password", "-s", item, "-w"], capture_output=True, text=True)
    return p.stdout.strip() or None


def room(source: str, rows: list[dict] | None = None) -> int:
    cfg, u = SOURCES[source], usage(source, rows)
    if u["stopped"] or u["exhausted"]:
        return 0
    left = cfg["daily"] - u["today"]
    if cfg["life"] is not None:
        left = min(left, cfg["life"] - u["life"])
    return max(left, 0)


def available() -> list[str]:
    rows = _rows()
    return [s for s in PRIORITY if room(s, rows) > 0 and key(s) is not None]


def _curl(args: list[str], timeout: int = 40) -> tuple[int, str]:
    p = subprocess.run(["curl", "-s", "-4", "--max-time", str(timeout), "-w", "\n%{http_code}", *args],
                       capture_output=True, text=True, errors="replace")
    body, _, code = p.stdout.rpartition("\n")
    return (int(code) if code.isdigit() else 0), body


def _stop_if_quota(source: str, query: str, code: int, body: str) -> bool:
    if code in (401, 402, 403, 429) or (code >= 400 and STOP_WORDS.search(body or "")):
        one_time = SOURCES[source]["life"] is not None
        _log(source, query, "exhausted" if one_time and code in (402, 429) else "stopped", 0, f"HTTP {code}: {body[:150]}")
        return True
    return False


def _norm(items: list[tuple[str, str]]) -> list[dict]:
    out, seen = [], set()
    for title, url in items:
        if url and url.startswith("http") and url not in seen:
            seen.add(url)
            out.append({"rank": len(out) + 1, "title": (title or "").strip(), "url": url})
    return out[:10]


def _tavily(q: str, k: str) -> tuple[int, str, list | None]:
    code, body = _curl(["-X", "POST", "https://api.tavily.com/search", "-H", "Content-Type: application/json",
                        "-H", f"Authorization: Bearer {k}",
                        "-d", json.dumps({"query": q, "search_depth": "basic", "max_results": 10, "country": "united states"})])
    if code != 200:
        return code, body, None
    return code, body, _norm([(r.get("title"), r.get("url")) for r in json.loads(body).get("results") or []])


def _serpapi(q: str, k: str) -> tuple[int, str, list | None]:
    u = "https://serpapi.com/search.json?" + urllib.parse.urlencode({"engine": "bing", "q": q, "cc": "US", "api_key": k})
    code, body = _curl([u])
    if code != 200:
        return code, body, None
    d = json.loads(body)
    if d.get("error"):
        return 429 if STOP_WORDS.search(d["error"]) else 500, d["error"], None
    return code, body, _norm([(r.get("title"), r.get("link")) for r in d.get("organic_results") or []])


def _serper(q: str, k: str) -> tuple[int, str, list | None]:
    code, body = _curl(["-X", "POST", "https://google.serper.dev/search", "-H", f"X-API-KEY: {k}",
                        "-H", "Content-Type: application/json", "-d", json.dumps({"q": q, "gl": "us", "num": 10})])
    if code != 200:
        return code, body, None
    return code, body, _norm([(r.get("title"), r.get("link")) for r in json.loads(body).get("organic") or []])


def _jina(q: str, k: str) -> tuple[int, str, list | None]:
    code, body = _curl(["https://s.jina.ai/?q=" + urllib.parse.quote(q), "-H", f"Authorization: Bearer {k}",
                        "-H", "Accept: application/json", "-H", "X-Respond-With: no-content"])
    if code != 200:
        return code, body, None
    return code, body, _norm([(r.get("title"), r.get("url")) for r in json.loads(body).get("data") or []])


CLAUDE_PROMPT = ('Run exactly one WebSearch with this exact query: "{q}". Then answer ONLY with JSON '
                 '{{"results":[{{"title":"...","url":"..."}}]}} listing every result in the order the tool returned '
                 'them. No other text.')


def _claude(q: str, k: str) -> tuple[int, str, list | None]:
    sys.path.insert(0, str(ROOT / "growth" / "evals"))
    import evallib as E
    exe = E.claude_cli()
    p = subprocess.run([exe, "-p", CLAUDE_PROMPT.format(q=q.replace('"', "'")), "--tools", "WebSearch",
                        "--allowedTools", "WebSearch", "--model", "claude-haiku-5-5", "--output-format", "json",
                        *E.CLI_ISOLATION], capture_output=True, text=True, timeout=180, cwd=E.cli_cwd())
    try:
        d = json.loads(p.stdout)
    except ValueError:
        return 500, (p.stderr or p.stdout)[-300:], None
    res = str(d.get("result") or "")
    if d.get("is_error"):
        return (429 if STOP_WORDS.search(res) else 500), res, None
    m = re.search(r"\{.*\}", res, re.S)
    try:
        items = json.loads(m.group(0)).get("results") or [] if m else []
    except ValueError:
        return 500, res[:300], None
    return 200, "", _norm([(r.get("title"), r.get("url")) for r in items])


def _bing(q: str, k: str) -> tuple[int, str, list | None]:
    sys.path.insert(0, str(ROOT / "growth" / "evals"))
    import serp
    try:
        rows = [r for r in serp.fetch("bing", q) if r.get("rank")]
    except Exception as e:  # noqa: BLE001  (Chrome down, blocked page)
        return 500, str(e), None
    return 200, "", _norm([(r.get("title"), r.get("url")) for r in rows])


FETCH = {"tavily": _tavily, "serpapi": _serpapi, "serper": _serper, "jina": _jina, "claude": _claude, "bing": _bing}


def fetch(source: str, query: str) -> list[dict] | None:
    """One capped reading. Returns the top 10 or None; never exceeds the source's cap and never retries a quota error."""
    if room(source) <= 0:
        return None
    k = key(source)
    if k is None:
        return None
    try:
        code, body, res = FETCH[source](query, k)
    except Exception as e:  # noqa: BLE001
        _log(source, query, "error", 0, repr(e))
        return None
    if res is None:
        if not _stop_if_quota(source, query, code, body):
            _log(source, query, "error", 0, f"HTTP {code}: {body[:150]}")
        return None
    _log(source, query, "ok" if len(res) >= 6 else "short" if res else "empty", len(res))   # short: cut-off page, no reading
    time.sleep(SOURCES[source]["pause"])
    return res


def status() -> str:
    rows = _rows()
    lines = [f"{'source':9} {'today':>9} {'lifetime':>12}  state"]
    for s in PRIORITY:
        c, u = SOURCES[s], usage(s, rows)
        k = key(s)
        state = ("no key (Barry adds it)" if k is None else "exhausted" if u["exhausted"] else
                 "stopped today" if u["stopped"] else "ok")
        life = f"{u['life']}/{c['life']}" if c["life"] else str(u["life"])
        lines.append(f"{s:9} {u['today']:>4}/{c['daily']:<4} {life:>12}  {state}")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) >= 2 and sys.argv[1] == "status":
        print(status())
    elif len(sys.argv) == 4 and sys.argv[1] == "test":
        for r in fetch(sys.argv[2], sys.argv[3]) or []:
            print(r["rank"], r["url"])
        print(status())
    else:
        print(__doc__)
