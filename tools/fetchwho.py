#!/usr/bin/env python3.12
"""Who fetched dealectric.com: our own evals or outside users? (added 2026-10-28)

Pulls Cloudflare-verified AI Assistant fetches (ChatGPT-User and any other bot Cloudflare files under "AI Assistant")
and the Worker's D1 `clicks` rows (kind ai_fetch and redirect) and `landings` rows (pages opened from a link tagged
utm_source) for a date range, and matches each against the times
we know our own assistants were working:

  * growth/evals/footprint.jsonl, one entry per chat or probe since 2026-10-28 (evallib.footprint);
  * tools/footprint_hook.py entries (source "hook"): an agent session's own WebFetch, curl or browser navigation to
    dealectric.com (window: the 90 s before the entry) or a chat it opened on an assistant app (the 10 min after);
    counted apart as "ours (hook)";
  * backfill: every run file under growth/evals/runs/ with started_at / finished_at (cell JSONs from ui.py, run.py,
    narrowing.py ...), plus chat records that carry no times (image_probe, claudeline, gapexp answers), placed by file
    mtime minus their latency. Those mtime windows are weaker evidence and are counted apart ("ours, by mtime").

Unverified requests under an AI user agent are pulled too and never counted as users: our own clients by user agent
(Claude Code's WebFetch, dealectric-* tools), a scanner that rotates fake AI agents (class "scanner": a secret-hunting
path such as /.env or /sa.json, or any unverified or D1 request in the same country within 10 minutes of one), an
unverified Claude agent inside a Claude chat window of ours, else "ambiguous".

Classes, for a verified fetch:
  ours            inside a known chat window, widened by --slack seconds on both ends (US egress only)
  outside         non-US country. OpenAI's ChatGPT-User exit follows the user's region and every chat of ours egresses
                  from the US, so a non-US assistant fetch is someone else's, whenever it lands.
  ambiguous       US, outside every window but within --near minutes of one (a chat we ran but never logged, e.g. by
                  hand in the agent Chrome, or a fetch ChatGPT made late)
  outside-likely  US, nowhere near any activity of ours

    python3.12 tools/fetchwho.py                       # last 8 days (the Free plan keeps about 8)
    python3.12 tools/fetchwho.py --since 2026-10-27 --until 2026-10-28T12:00 --list ours
    python3.12 tools/fetchwho.py --offsets             # how far fetches land from the nearest chat (to pick --slack)
    python3.12 tools/fetchwho.py --no-d1 --json out.json

A fetch is matched only against chats of the same assistant family (ChatGPT-User against ChatGPT and OpenAI API
chats, Claude-User against Claude ones); footprints of our own direct fetches (copycheck.py) match any
user agent. Index and training crawlers (OAI-SearchBot, GPTBot, ClaudeBot ...) are their own class, "crawler". D1 redirect and landing rows (browsers,
scanners) are matched only against those direct-fetch footprints and our tools' user agents.

Default --slack 120 s, picked from the data on 2026-10-28 (--offsets, 2026-10-20..28): of 262 US ChatGPT-User fetches,
221 landed inside a chat window, 1 within 30 s and 4 within 120 s of one, none between 120 s and 350 s, and the rest
were 6 min to hours away. Run --offsets to re-check.
"""
from __future__ import annotations

import argparse
import bisect
import json
import re
import subprocess
import sys
from collections import Counter, defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "growth" / "evals"))
import cf  # noqa: E402
import evallib as E  # noqa: E402

OUR_COUNTRY = "US"
CLASSES = ["ours", "ours (hook)", "ours (mtime)", "outside", "ambiguous", "outside-likely", "crawler", "scanner"]
CRAWLERS = ("GPTBot", "OAI-SearchBot", "ClaudeBot", "PerplexityBot", "Google-Extended", "CCBot", "Bytespider")
# D1 rows our own tools make under a user agent of their own (tools/linkcheck.py, deploy checks, rawfetch_mcp.py)
# Our own clients: dealectric-* tools (linkcheck, indexnow, deploy checks, rawfetch_mcp.py's claudeline UA, run.py's
# dealectric-eval) and Claude Code's WebFetch ("Claude-User (claude-code/<ver>; ...)"), which runs on this Mac. Nobody
# else's Claude Code fetches our pages in practice (981 such fetches 2026-10-20..28, 855 inside logged claude-code
# cells, the rest the unlogged claudeline runs of 10-25).
OWN_UA_MARKS = ("dealectric", "(claude-code/")
# What the 2026-10-20..28 scanner asked for under rotating fake AI user agents (/.env, /@fs/proc/self/environ, /sa.json)
SECRET_RE = re.compile(r"(^|/)\.(env|git|aws|ssh|svn|npmrc|docker)|/@fs/|/proc/|/etc/passwd|wp-(admin|login|config|content)|phpinfo|"
                       r"\.php\b|(^|/)(sa|service[-_]?account|credentials?|secrets?|keys?|firebase|config|settings)\.(json|ya?ml|js|ts)$|"
                       r"\.(sql|bak|old|swp|pem|key)$|actuator|server-status|\.\./|/vendor/|/node_modules/", re.I)
BURST_S = 600
HOOK_FETCH_S, HOOK_CHAT_S = 90, 600
OURS_BY_SOURCE = {"mtime": "ours (mtime)", "hook": "ours (hook)"}   # windows for footprint_hook.py entries: a fetch ends at the entry, a chat starts there   # a scanner burst: same country, within 10 minutes of a secret-hunting request


def parse_ts(s) -> datetime | None:
    if not s or not isinstance(s, str):
        return None
    try:
        d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None
    return d if d.tzinfo else d.replace(tzinfo=timezone.utc)


def iso(d: datetime) -> str:
    return d.astimezone(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


# ---------------------------------------------------------------- our windows

def run_files():
    """(runs root, json file) for this checkout's runs and every other worktree's: cell JSONs are gitignored, so a
    run made in a worktree exists only there."""
    roots = [E.RUNS_DIR]
    try:
        out = subprocess.run(["git", "worktree", "list", "--porcelain"], cwd=ROOT, capture_output=True, text=True, timeout=20).stdout
        for line in out.splitlines():
            if line.startswith("worktree "):
                r = Path(line[9:]) / "growth" / "evals" / "runs"
                if r.is_dir() and r.resolve() not in {x.resolve() for x in roots}:
                    roots.append(r)
    except (OSError, subprocess.SubprocessError):
        pass
    for root in roots:
        for f in root.rglob("*.json"):
            yield root, f


def load_windows(since: datetime, until: datetime) -> list[dict]:
    """[{start, end, source, label, country}] for every chat or probe of ours we can place in time."""
    lo, hi = since - timedelta(hours=2), until + timedelta(hours=2)
    out = []
    fp = E.footprint_path()
    if fp.exists():
        for line in fp.read_text(encoding="utf-8").splitlines():
            try:
                e = json.loads(line)
            except ValueError:
                continue
            a, b = parse_ts(e.get("started_at")), parse_ts(e.get("finished_at"))
            if a and e.get("source") == "hook":
                # tools/footprint_hook.py logs the moment a session's tool call returned: a fetch happened just before it,
                # a chat it opened runs on for a while after it
                a, b = (a - timedelta(seconds=HOOK_FETCH_S), a) if e.get("kind") == "fetch" else (a, a + timedelta(seconds=HOOK_CHAT_S))
                if b >= lo and a <= hi:
                    out.append({"start": a, "end": b, "source": "hook", "country": None, "family": app_family(e.get("app")),
                                "label": f"{e.get('via')} {e.get('app')} {e.get('kind')} session {(e.get('session_id') or '?')[:8]}"})
                continue
            if a and b and b >= lo and a <= hi:
                out.append({"start": a, "end": b, "source": "footprint", "country": e.get("egress_country"), "family": app_family(e.get("app")),
                            "label": f"{e.get('script')} {e.get('app')} {e.get('run_id') or ''} {e.get('prompt_id') or ''}".strip()})
    files = []
    for root, f in run_files():
        if f.name in ("manifest.json", "summary.json") or f.name.endswith(".tmp"):
            continue
        try:
            files.append((root, f, f.stat().st_mtime))
        except OSError:
            continue
    # A checkout, pull or new worktree stamps every file it writes with the same few seconds; such an mtime says
    # nothing about when the chat ran, so files sharing a 2-second bucket with more than 10 others get no mtime window.
    bulk = Counter((str(root), int(m) // 2) for root, _, m in files)
    for root, f, m in files:
        mt = datetime.fromtimestamp(m, timezone.utc)
        bulk_written = bulk[(str(root), int(m) // 2)] > 10
        try:
            rec = json.loads(f.read_text(encoding="utf-8"))
        except (ValueError, UnicodeDecodeError, OSError):
            continue
        if not isinstance(rec, dict):
            continue
        label = str(f.relative_to(root))
        a, b = parse_ts(rec.get("started_at")), parse_ts(rec.get("finished_at"))
        if a and b:
            if b >= lo and a <= hi:
                out.append({"start": a, "end": b, "source": "run file", "label": label, "country": None,
                            "family": app_family(rec.get("assistant") or rec.get("model") or label)})
            continue
        # a chat record with no times: place it by mtime minus its latency
        if (rec.get("text") or rec.get("answer")) and any(k in rec for k in ("latency_s", "account", "queries", "fetched", "result_urls")):
            if lo <= mt <= hi and not bulk_written:
                lat = rec.get("latency_s") if isinstance(rec.get("latency_s"), (int, float)) else 180
                fam = app_family(rec.get("assistant") or rec.get("model") or label)
                if fam:   # an mtime window with no known assistant would match anything; leave it out
                    out.append({"start": mt - timedelta(seconds=lat + 30), "end": mt + timedelta(seconds=5), "source": "mtime",
                                "label": label, "country": None, "family": fam})
    out.sort(key=lambda w: w["start"])
    return out


def app_family(s) -> str | None:
    """openai / anthropic / google / xai for a footprint app, run-file assistant, model or path; None for direct-fetch
    (our own client, any user agent) and for anything unrecognised."""
    s = str(s or "").lower()
    if not s or s == "direct-fetch":
        return None
    for fam, marks in (("openai", ("chatgpt", "openai", "gpt-")), ("anthropic", ("claude", "anthropic")),
                       ("google", ("gemini",)), ("xai", ("xai", "grok")), ("perplexity", ("perplexity",))):
        if any(m in s for m in marks):
            return fam
    return None


def fetch_family(bot: str) -> str | None:
    return {"ChatGPT-User": "openai", "Claude-User": "anthropic", "Gemini": "google", "Perplexity-User": "perplexity"}.get(bot)


class Index:
    """Nearest-window lookups over sorted windows."""

    def __init__(self, windows: list[dict]):
        self.w = windows
        self.starts = [x["start"] for x in windows]
        self.maxdur = max(((x["end"] - x["start"]) for x in windows), default=timedelta(0))

    def offset(self, t: datetime, families=None) -> tuple[float, dict | None]:
        """Seconds from t to the nearest window whose family is in `families` (0 inside, <0 before its start, >0 after
        its end) and that window."""
        best, bw = None, None
        i = bisect.bisect_right(self.starts, t)
        lo = bisect.bisect_left(self.starts, t - self.maxdur - timedelta(hours=6))
        hi = min(len(self.w), i + 200)
        for x in self.w[lo:hi]:
            if families is not None and x.get("family") not in families:
                continue
            if x["start"] <= t <= x["end"]:
                return 0.0, x
            d = (t - x["end"]).total_seconds() if t > x["end"] else (t - x["start"]).total_seconds()
            if best is None or abs(d) < abs(best):
                best, bw = d, x
        return (best if best is not None else float("inf")), bw


# ---------------------------------------------------------------- fetches

# User agents that claim an AI assistant or crawler, or one of our tools; Cloudflare verifies ChatGPT-User and GPTBot
# but none of the Claude agents (2026-10-28), so for Claude the user agent alone proves nothing.
AI_UA_LIKE = ("%ChatGPT%", "%GPTBot%", "%OAI-SearchBot%", "%Claude%", "%anthropic%", "%Perplexity%", "%MistralAI%", "%DuckAssist%",
              "%dealectric%")


def _cf_rows(flt: str, since: datetime, until: datetime) -> list[dict]:
    rows, t = [], since
    while t < until:
        u = min(t + timedelta(days=1), until)
        q = ('{viewer{zones(filter:{zoneTag:$zone}){httpRequestsAdaptiveGroups(limit:10000, filter:{datetime_geq:"%s", '
             'datetime_lt:"%s", %s}, orderBy:[datetime_ASC]){count dimensions{datetime userAgent clientCountryName '
             'clientRequestPath edgeResponseStatus verifiedBotCategory}}}}}') % (iso(t), iso(u), flt)
        d = cf.query(q)
        if d.get("errors"):
            raise SystemExit(f"Cloudflare: {d['errors']}")
        got = d["data"]["viewer"]["zones"][0]["httpRequestsAdaptiveGroups"]
        if len(got) >= 10000:
            print(f"warning: {iso(t)}..{iso(u)} hit the 10000-row limit; some fetches are missing", file=sys.stderr)
        for g in got:
            dm = g["dimensions"]
            rows.append({"src": "cloudflare", "ts": parse_ts(dm["datetime"]), "n": g["count"], "country": dm["clientCountryName"],
                         "path": dm["clientRequestPath"], "ua": dm["userAgent"], "status": dm["edgeResponseStatus"],
                         "verified": dm.get("verifiedBotCategory") or "", "bot": bot_name(dm["userAgent"])})
        t = u
    return rows


def cf_fetches(since: datetime, until: datetime) -> tuple[list[dict], list[dict]]:
    """(verified AI Assistant requests, unverified requests under an AI or our own user agent), one row per (second,
    UA, country, path), day by day (limit 10000 per query)."""
    verified = _cf_rows('verifiedBotCategory:"AI Assistant"', since, until)
    ors = ",".join('{userAgent_like:"%s"}' % x for x in AI_UA_LIKE)
    unverified = [r for r in _cf_rows(f"OR:[{ors}]", since, until) if not r["verified"]]
    return verified, unverified


def scanner_bursts(rows: list[dict]) -> dict[str, list[datetime]]:
    """{country: sorted times} of secret-hunting requests (SECRET_RE) under an unverified or D1 user agent."""
    out = defaultdict(list)
    for r in rows:
        if not r.get("verified") and SECRET_RE.search(r["path"] or "") and not own_ua(r["ua"]):
            out[r["country"]].append(r["ts"])
    return {k: sorted(v) for k, v in out.items()}


def in_burst(f: dict, bursts: dict[str, list[datetime]]) -> bool:
    ts = bursts.get(f["country"]) or []
    i = bisect.bisect_left(ts, f["ts"] - timedelta(seconds=BURST_S))
    return i < len(ts) and ts[i] <= f["ts"] + timedelta(seconds=BURST_S)


def own_ua(ua: str) -> bool:
    return any(m in (ua or "").lower() for m in OWN_UA_MARKS)


def bot_name(ua: str) -> str:
    for k in ("ChatGPT-User", "Claude-User", "Claude-SearchBot", "Perplexity-User", "MistralAI-User", "Gemini", "DuckAssistBot",
              "OAI-SearchBot", "GPTBot", "ClaudeBot", "PerplexityBot", "dealectric"):
        if k.lower() in (ua or "").lower():
            return k
    return (ua or "?")[:40]


def d1_fetches(since: datetime, until: datetime) -> tuple[list[dict], str | None]:
    rows, err = E.d1_query("SELECT ts, kind, slug, user_agent, country, bot_like, utm_source FROM clicks "
                           f"WHERE kind IN ('ai_fetch','redirect') AND ts >= '{iso(since)}' AND ts < '{iso(until)}' ORDER BY ts")
    out = []
    for r in rows:
        out.append({"src": f"d1 {r['kind']}", "ts": parse_ts(r["ts"]), "n": 1, "country": r.get("country") or "?",
                    "path": f"/go/{r['slug']}", "ua": r.get("user_agent") or "", "bot_like": r.get("bot_like"),
                    "bot": bot_name(r.get("user_agent") or "") if r["kind"] == "ai_fetch" else ("bot-like" if r.get("bot_like") else "browser")})
    # page landings tagged utm_source (the Worker's landing log, W3 step 0, since 2026-10-28): matched like redirects
    lrows, lerr = E.d1_query("SELECT ts, page, utm_source, user_agent, country, bot_like FROM landings "
                             f"WHERE ts >= '{iso(since)}' AND ts < '{iso(until)}' ORDER BY ts")
    for r in lrows:
        out.append({"src": "d1 landing", "ts": parse_ts(r["ts"]), "n": 1, "country": r.get("country") or "?",
                    "path": f"/{r['page']}?utm_source={r.get('utm_source') or ''}", "ua": r.get("user_agent") or "",
                    "bot_like": r.get("bot_like"), "bot": "bot-like" if r.get("bot_like") else "browser"})
    out.sort(key=lambda f: f["ts"])
    return out, err or lerr


def classify(f: dict, idx: Index, slack: float, near_min: float, bursts: dict | None = None) -> dict:
    """Verified Cloudflare rows and D1 rows. D1 cannot see Cloudflare's verification, so it also gets the scanner test."""
    if own_ua(f["ua"]):
        return {**f, "cls": "ours", "why": "our tool's user agent", "off": 0.0, "win": None}
    if f["src"] != "cloudflare" and bursts is not None and (SECRET_RE.search(f["path"] or "") or in_burst(f, bursts)):
        return {**f, "cls": "scanner", "why": f"scanner burst ({f['country']}, within {BURST_S // 60} min of a secret-hunting request)",
                "off": float("inf"), "win": None}
    if f["bot"] in CRAWLERS:
        return {**f, "cls": "crawler", "why": "training/index crawler, not driven by a chat", "off": float("inf"), "win": None}
    fam = fetch_family(f["bot"])
    off, w = idx.offset(f["ts"], families={None} if f["src"] in ("d1 redirect", "d1 landing") else ({fam, None} if fam else None))
    if f["country"] != OUR_COUNTRY:
        return {**f, "cls": "outside", "why": f"country {f['country']}", "off": off, "win": w}
    if w and abs(off) <= slack:
        return {**f, "cls": OURS_BY_SOURCE.get(w["source"], "ours"), "why": f"{w['source']}: {w['label']}", "off": off, "win": w}
    if w and abs(off) <= near_min * 60:
        return {**f, "cls": "ambiguous", "why": f"{off:+.0f}s from {w['source']}: {w['label']}", "off": off, "win": w}
    return {**f, "cls": "outside-likely", "why": "no chat of ours near" + (f" (nearest {off / 60:+.0f} min)" if w else ""), "off": off, "win": w}


def classify_unverified(f: dict, idx: Index, slack: float, bursts: dict) -> dict:
    """A Cloudflare request under an AI user agent that Cloudflare did not verify. Never counted as an outside user:
    an unverified ChatGPT-User or GPTBot does not come from OpenAI, and Cloudflare verifies no Claude agent at all."""
    if own_ua(f["ua"]):
        return {**f, "cls": "ours", "why": "our tool's user agent", "off": 0.0, "win": None}
    if SECRET_RE.search(f["path"] or ""):
        return {**f, "cls": "scanner", "why": "fake AI user agent on a secret-hunting path", "off": float("inf"), "win": None}
    fam = fetch_family(f["bot"])
    # a real Claude fetch can arrive unverified (server-side Claude: API web_fetch, claude.ai), so Claude agents may
    # match Claude chats; other unverified agents only our own direct fetches (copycheck.py). A window of ours beats
    # the burst rule: the scanner also runs from US cloud regions.
    off, w = idx.offset(f["ts"], families={fam, None} if fam == "anthropic" else {None})
    if w and abs(off) <= slack and (fam == "anthropic" or f["country"] == OUR_COUNTRY):
        return {**f, "cls": OURS_BY_SOURCE.get(w["source"], "ours"), "why": f"{w['source']}: {w['label']}", "off": off, "win": w}
    if in_burst(f, bursts):
        return {**f, "cls": "scanner", "why": f"fake AI user agent in a {f['country']} scanner burst", "off": off, "win": w}
    if f["bot"] in CRAWLERS or f["bot"] == "Claude-SearchBot":
        return {**f, "cls": "crawler", "why": "crawler user agent, unverified", "off": off, "win": w}
    return {**f, "cls": "ambiguous", "why": f"unverified {f['bot']}, outside our windows", "off": off, "win": w}


# ---------------------------------------------------------------- report

def offsets_table(rows: list[dict]) -> None:
    us = [r for r in rows if r["country"] == OUR_COUNTRY and r["off"] != float("inf")]
    edges = [0, 5, 10, 30, 60, 120, 300, 600, 1800, 3600]
    print(f"\nUS fetches by distance to the nearest chat window (n={sum(r['n'] for r in us)}):")
    prev = None
    for e in edges:
        k = sum(r["n"] for r in us if abs(r["off"]) <= e and (prev is None or abs(r["off"]) > prev))
        print(f"  {'inside' if e == 0 else f'<= {e:>4}s':>10}  {k}")
        prev = e
    print(f"  {'> 3600s':>10}  {sum(r['n'] for r in us if abs(r['off']) > 3600)}")


def summary(rows: list[dict], title: str) -> None:
    by = Counter()
    for r in rows:
        by[r["cls"]] += r["n"]
    total = sum(by.values())
    print(f"\n{title}: {total} fetches")
    for c in CLASSES:
        if by[c]:
            print(f"  {c:15} {by[c]:5}  ({100 * by[c] / total:.0f}%)")
    bots = defaultdict(Counter)
    for r in rows:
        bots[r["bot"]][r["cls"]] += r["n"]
    if len(bots) > 1:
        for b, c in sorted(bots.items(), key=lambda kv: -sum(kv[1].values())):
            print(f"    {b:22} " + ", ".join(f"{k} {v}" for k, v in c.most_common()))


def listing(rows: list[dict], classes: set[str]) -> None:
    for r in rows:
        if r["cls"] in classes:
            print(f"  {iso(r['ts'])}  {r['cls']:14} {r['country']:3} {r['bot']:13} {r['path'][:60]:60} {r['why'][:90]}")


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    now = datetime.now(timezone.utc)
    ap.add_argument("--since", default=None, help="UTC date or datetime (default: 8 days ago)")
    ap.add_argument("--until", default=None, help="UTC date or datetime (default: now)")
    ap.add_argument("--slack", type=float, default=120, help="seconds a fetch may land outside a chat window and still count as ours")
    ap.add_argument("--near", type=float, default=30, help="minutes: a US fetch this close to a window is ambiguous, farther is outside-likely")
    ap.add_argument("--no-d1", action="store_true")
    ap.add_argument("--offsets", action="store_true", help="print the distance distribution used to pick --slack")
    ap.add_argument("--list", default="outside,outside-likely,ambiguous", help="classes to list row by row ('' for none, 'all')")
    ap.add_argument("--list-unverified", action="store_true", help="also list the unverified Cloudflare rows of those classes")
    ap.add_argument("--json", default=None, help="write every classified row to this file")
    a = ap.parse_args()
    since = parse_ts(a.since) if a.since else now - timedelta(days=8)
    until = parse_ts(a.until) if a.until else now
    if not since or not until:
        raise SystemExit("--since/--until: ISO date or datetime, UTC")

    windows = load_windows(since, until)
    idx = Index(windows)
    src = Counter(w["source"] for w in windows)
    print(f"fetchwho {iso(since)} .. {iso(until)}; our windows: " + ", ".join(f"{v} {k}" for k, v in src.items())
          + f"; footprint log {E.footprint_path()}; slack {a.slack:.0f}s, near {a.near:.0f} min")

    ver, unver = cf_fetches(since, until)
    d1, err = ([], None) if a.no_d1 else d1_fetches(since, until)
    bursts = scanner_bursts(unver + d1)
    cfr = [classify(f, idx, a.slack, a.near) for f in ver]
    summary(cfr, "Cloudflare verified AI Assistant")
    cfu = [classify_unverified(f, idx, a.slack, bursts) for f in unver]
    summary(cfu, "Cloudflare unverified AI or own user agents (never counted as users)")
    d1r = []
    if not a.no_d1:
        if err:
            print(f"\nD1 unavailable: {err}")
        d1r = [classify(f, idx, a.slack, a.near, bursts) for f in d1]
        if d1r:
            summary([r for r in d1r if r["src"] == "d1 ai_fetch"], "D1 /go/ ai_fetch (assistant user agents; overlaps Cloudflare)")
            summary([r for r in d1r if r["src"] == "d1 redirect"], "D1 /go/ redirect (browsers, scanners, curl)")
            summary([r for r in d1r if r["src"] == "d1 landing"], "D1 page landings tagged utm_source (browsers, scanners)")
    if a.offsets:
        offsets_table([r for r in cfr if r["bot"] == "ChatGPT-User"])
    want = set(CLASSES) if a.list == "all" else {c.strip() for c in a.list.split(",") if c.strip()}
    if want:
        print("\nCloudflare verified rows (" + ", ".join(sorted(want)) + "):")
        listing(cfr, want)
        if a.list_unverified:
            print("\nCloudflare unverified rows (" + ", ".join(sorted(want)) + "):")
            listing(cfu, want)
    if a.json:
        def dump(r):
            return {k: (iso(v) if isinstance(v, datetime) else v) for k, v in r.items() if k != "win"}
        Path(a.json).write_text(json.dumps({"since": iso(since), "until": iso(until), "slack_s": a.slack, "near_min": a.near,
                                            "cloudflare": [dump(r) for r in cfr], "cloudflare_unverified": [dump(r) for r in cfu],
                                            "d1": [dump(r) for r in d1r]}, indent=1))
        print(f"\nwrote {a.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
