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
import os
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
    # Paid or metered, explicit use only (not in PRIORITY, so the daily run never spends on them until calibrated):
    "dataforseo": dict(daily=150, life=None, key="dataforseo-api-password", pause=0),  # Bing SERP, Standard queue, $1/month cap
    "openai":     dict(daily=60, life=None, key=None, pause=1),          # OpenAI Responses web_search: OpenAI's own index
    "google":     dict(daily=50, life=None, key=None, pause=20),         # Agent Chrome google.com; stops at the /sorry/ check
}
# DataForSEO (Barry 2026-11-06: "okay spending $1 a month"): Bing Organic SERP, Standard queue, billed per SERP of 10
# results ($0.0006 on the pricing page, 2026-11-06). The `cost` DataForSEO returns on each task is logged as `usd` and
# summed per calendar month; the source stops at MONTH_USD. Login = the account email (keychain dataforseo-api-login),
# password = the API password from the dashboard's API Access page (keychain dataforseo-api-password).
MONTH_USD = {"dataforseo": 1.00}
DFS = "https://api.dataforseo.com/v3/serp/bing/organic/"
PRIORITY = ["claude", "serpapi", "bing", "tavily", "serper", "jina"]   # Claude first since 11-06 (DLC-190)
STATUS_ORDER = PRIORITY + ["dataforseo", "openai", "google"]
# Calibration vs Bing (gapmine.py srccal, 54 Bing-scored queries, 2026-11-05):
#   claude  Spearman 0.29, gate (<0.4) agreement 27/54, open 37 vs Bing's 18 -> NOT used for gating (spam-heavy results)
# 11-06 (DLC-190): against OpenAI's own index Bing is weak (Spearman 0.29) and Claude passes (0.64 on 142 clusters), so
# Claude alone gates (at coverage < 0.3, gapmine.GATE_BY_SOURCE) until the paid OpenAI gate is adopted (DLC-191).
GATING = {"claude"}
STOP_WORDS = re.compile(r"quota|exceed|limit|credit|billing|payment|insufficient|upgrade|plan", re.I)


def today() -> str:
    return _dt.date.today().isoformat()


def _retry(fn, tries: int = 10):
    """OneDrive briefly locks files it is syncing ("Operation not permitted", seen 2026-11-06 mid-run); wait it out."""
    for i in range(tries):
        try:
            return fn()
        except PermissionError:
            if i == tries - 1:
                raise
            time.sleep(3)


def _rows() -> list[dict]:
    if not LEDGER.exists():
        return []
    out = []
    for line in _retry(LEDGER.read_text).splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            pass
    return out


def _log(source: str, query: str, status: str, n: int = 0, note: str = "", usd: float | None = None) -> None:
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    row = {"ts": _dt.datetime.now().isoformat(timespec="seconds"), "date": today(), "source": source,
           "q": query, "status": status, "n": n, "note": note[:200]}
    if usd is not None:
        row["usd"] = round(usd, 6)
    def write():
        with LEDGER.open("a") as f:
            f.write(json.dumps(row) + "\n")
    _retry(write)


def usage(source: str, rows: list[dict] | None = None) -> dict:
    rows = _rows() if rows is None else rows
    mine = [r for r in rows if r["source"] == source]
    calls = [r for r in mine if r["status"] in ("ok", "short", "empty", "error")]   # every request that reached the provider
    month = today()[:7]
    return {"today": sum(1 for r in calls if r["date"] == today()), "life": len(calls),
            "month_usd": round(sum(r.get("usd") or 0 for r in mine if r["date"][:7] == month), 4),
            "stopped": any(r["status"] == "stopped" and r["date"] == today() for r in mine),
            "exhausted": any(r["status"] == "exhausted" for r in mine)}


def key(source: str) -> str | None:
    if source == "openai":
        sys.path.insert(0, str(ROOT / "growth" / "evals"))
        import evallib as E
        return E.env_key("OPENAI_API_KEY")
    item = SOURCES[source]["key"]
    if not item:
        return ""
    if source == "dataforseo":
        login = subprocess.run(["security", "find-generic-password", "-s", "dataforseo-api-login", "-w"],
                               capture_output=True, text=True).stdout.strip()
        pw = subprocess.run(["security", "find-generic-password", "-s", item, "-w"], capture_output=True, text=True).stdout.strip()
        return f"{login}:{pw}" if login and pw else None
    p = subprocess.run(["security", "find-generic-password", "-s", item, "-w"], capture_output=True, text=True)
    return p.stdout.strip() or None


def room(source: str, rows: list[dict] | None = None) -> int:
    cfg, u = SOURCES[source], usage(source, rows)
    if u["stopped"] or u["exhausted"]:
        return 0
    if source in MONTH_USD and u["month_usd"] >= MONTH_USD[source]:
        return 0
    # One-off override for a calibration Barry asked for (e.g. SERP_DAILY_CLAUDE=200); the daily run never sets it.
    daily = int(os.environ.get(f"SERP_DAILY_{source.upper()}", cfg["daily"]))
    left = daily - u["today"]
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


def _dfs_call(method: str, path: str, auth: str, body=None) -> tuple[int, dict]:
    args = ["-u", auth, "-X", method, DFS + path]
    if body is not None:
        args += ["-H", "Content-Type: application/json", "-d", json.dumps(body)]
    code, text = _curl(args, timeout=60)
    try:
        return code, json.loads(text)
    except ValueError:
        return code, {"status_code": code, "status_message": text[:200]}


DFS_STOP = {40100: 401, 40104: 401, 40207: 403, 40200: 402, 40210: 402, 40201: 403, 40203: 402, 40202: 429, 40209: 429}


def _dfs_http(sc: int) -> int:
    """DataForSEO answers HTTP 200 and puts its own code in the body (docs.dataforseo.com/v3/appendix/errors):
    auth/verification/IP 40100/40104/40207, payment/funds/cost limit 40200/40210/40203, paused 40201, rate 40202/40209
    stop the source; 40102 (no results) and 40101/40103 (engine error, retry) are per-task errors only."""
    return DFS_STOP.get(sc, 500)


def _dfs_items(task: dict) -> list:
    res = (task.get("result") or [{}])[0] or {}
    org = [i for i in res.get("items") or [] if i.get("type") == "organic"]
    org.sort(key=lambda i: i.get("rank_group") or 99)
    return _norm([(i.get("title"), i.get("url")) for i in org])


def dataforseo_many(queries: list[str], wait_s: int = 2700) -> dict[str, list | None]:
    """Post up to `room` queries in one Standard-queue call, then collect each task (free) until done or `wait_s`.
    Every task's billed cost is logged as `usd` when it is posted; the month's total stops the source at MONTH_USD."""
    out: dict[str, list | None] = {q: None for q in queries}
    auth = key("dataforseo")
    n = min(room("dataforseo"), len(queries))
    if not auth or n <= 0:
        return out
    todo = queries[:n]
    for i in range(0, len(todo), 100):
        chunk = todo[i:i + 100]
        code, d = _dfs_call("POST", "task_post", auth, [{"keyword": q, "location_code": 2840, "language_code": "en",
                                                          "device": "desktop", "depth": 10, "tag": q[:255]} for q in chunk])
        sc = d.get("status_code") or code
        if sc != 20000:
            if not _stop_if_quota("dataforseo", chunk[0], _dfs_http(sc) if sc >= 40000 else code, json.dumps(d)[:300]):
                _log("dataforseo", chunk[0], "error", 0, f"task_post {sc}: {json.dumps(d)[:180]}")
            return out
        ids = {}
        for t in d.get("tasks") or []:
            q = (t.get("data") or {}).get("tag") or (t.get("data") or {}).get("keyword")
            if t.get("status_code") == 20100 and q in out:
                ids[t["id"]] = q
                _log("dataforseo", q, "posted", 0, t["id"], usd=t.get("cost") or 0)
            else:
                _log("dataforseo", q or "?", "error", 0, f"{t.get('status_code')} {t.get('status_message')}")
                if t.get("status_code") in DFS_STOP:
                    _stop_if_quota("dataforseo", q or "?", _dfs_http(t["status_code"]), t.get("status_message") or "")
                    return out
        t0 = time.time()
        while ids and time.time() - t0 < wait_s:
            time.sleep(20)
            for tid, q in list(ids.items()):
                code, g = _dfs_call("GET", f"task_get/regular/{tid}", auth)
                task = (g.get("tasks") or [{}])[0]
                if task.get("status_code") == 20000:
                    res = _dfs_items(task)
                    out[q] = res
                    _log("dataforseo", q, "ok" if len(res) >= 6 else "short" if res else "empty", len(res), tid)
                    del ids[tid]
                elif task.get("status_code") == 40102:   # no search results: a valid, empty reading
                    out[q] = []
                    _log("dataforseo", q, "empty", 0, tid)
                    del ids[tid]
                elif task.get("status_code") not in (40601, 40602, 20100, None):   # 40601/40602: handed / in queue
                    _log("dataforseo", q, "error", 0, f"{task.get('status_code')} {task.get('status_message')}")
                    del ids[tid]
        for tid, q in ids.items():
            _log("dataforseo", q, "error", 0, f"not ready after {wait_s}s: {tid}")
    return out


def _dataforseo(q: str, k: str) -> tuple[int, str, list | None]:
    res = dataforseo_many([q]).get(q)
    return (200, "", res) if res is not None else (599, "no result (logged)", None)


def _openai(q: str, k: str) -> tuple[int, str, list | None]:
    """One web search in OpenAI's own index (the Responses API web_search tool, US), as `fastloop.py pack --engine api`
    runs it: the sources in the order returned, first 10. Titles come from the cached page text when we have it."""
    sys.path.insert(0, str(ROOT / "growth" / "evals"))
    import apiprobe as A
    import evallib as E
    started = E.now_iso()
    status, resp = A.post({"model": "gpt-6-luna", "input": f'Run exactly one web search with this exact query, word for word: "{q}". '
                           "Do not search again and do not open any page. Then reply only with the word DONE.",
                           "store": False, "max_tool_calls": 1, "include": ["web_search_call.action.sources"],
                           "tools": [{"type": "web_search", "user_location": {"type": "approximate", "country": "US"}}]}, k)
    srcs = [s for it in resp.get("output", []) if it.get("type") == "web_search_call"
            for s in ((it.get("action") or {}).get("sources") or [])]
    E.footprint("openai-api", started, E.now_iso(), prompt=q, script="serpsources.py", run_id="srccal",
                retrieved=[{"url": s.get("url")} for s in srcs], error=str(resp.get("error")) if status != 200 else None)
    if status != 200:
        return status, json.dumps(resp.get("error") or resp)[:300], None
    u = resp.get("usage") or {}
    _log("openai", q, "usage", 0, f"in {u.get('input_tokens')} out {u.get('output_tokens')}")
    res = _norm([(s.get("title") or "", s.get("url")) for s in srcs])
    try:   # OpenAI returns URLs only; the labeller reads title + URL, so take each page's title as the API pack does
        import fastloop as F
        F.fetch_all([{"url": r["url"]} for r in res])
        for r in res:
            if not r["title"]:
                r["title"] = ((F.fetch_text(r["url"]).get("text") or "").strip().splitlines() or [""])[0][:120]
    except Exception:  # noqa: BLE001  (a page that won't load keeps its URL only)
        pass
    return 200, "", res


def _google(q: str, k: str) -> tuple[int, str, list | None]:
    sys.path.insert(0, str(ROOT / "growth" / "evals"))
    import serp
    try:
        rows = serp.fetch("google", q)
    except Exception as e:  # noqa: BLE001
        return 500, str(e), None
    if rows and not rows[0].get("rank"):
        note = rows[0].get("note", "")
        blocked = re.search(r"sorry|unusual traffic|captcha|not a robot", note, re.I)
        return (429 if blocked else 500), note, None   # 429 stops the source for the day; never solved
    return 200, "", _norm([(r.get("title"), r.get("url")) for r in rows])


FETCH = {"dataforseo": _dataforseo, "google": _google, "openai": _openai, "tavily": _tavily, "serpapi": _serpapi, "serper": _serper, "jina": _jina, "claude": _claude, "bing": _bing}


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
    if source != "dataforseo":   # dataforseo_many logs its own rows (with the task id)
        _log(source, query, "ok" if len(res) >= 6 else "short" if res else "empty", len(res))   # short: cut-off page, no reading
    time.sleep(SOURCES[source]["pause"])
    return res


def status() -> str:
    rows = _rows()
    lines = [f"{'source':9} {'today':>9} {'lifetime':>12}  state"]
    for s in STATUS_ORDER:
        c, u = SOURCES[s], usage(s, rows)
        k = key(s)
        state = ("no key (Barry adds it)" if k is None else "exhausted" if u["exhausted"] else
                 "stopped today" if u["stopped"] else "ok")
        life = f"{u['life']}/{c['life']}" if c["life"] else str(u["life"])
        if s in MONTH_USD:
            state += f", ${u['month_usd']:.4f} of ${MONTH_USD[s]:.2f} this month"
        lines.append(f"{s:10} {u['today']:>4}/{c['daily']:<4} {life:>12}  {state}")
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
