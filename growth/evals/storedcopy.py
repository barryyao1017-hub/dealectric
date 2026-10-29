#!/usr/bin/env python3.12
"""What ChatGPT actually sees of our pages: its stored search-result copy, against the version that was live (DLC-77).

    python3.12 growth/evals/storedcopy.py              # refresh the crawl log, write growth/focus/stored-copy.md
    python3.12 growth/evals/storedcopy.py --no-fetch   # use the cached crawl log and deployment list only

ChatGPT answers from the title and snippet in its own search results, not from the live page. This joins three
sources, keyed by page path:
  1. every saved ChatGPT cell under growth/evals/runs/ (response.search_results and cite_pills that point at
     dealectric.com): the stored title, the time it was seen, the rank, and the cart dates the answer quoted;
  2. every GitHub Pages deployment (gh api deployments) with the page's <title>, meta description and lead text at
     that commit, so each stored title maps to the version(s) that carried it and the window they were live;
  3. crawler fetches from Cloudflare (OAI-SearchBot, GPTBot, bingbot, ChatGPT-User), appended to
     growth/focus/crawls/fetches.jsonl so the log outlives Cloudflare's retention.

For each sighting it reports the version the stored title matches, how many days that version had been superseded
(days behind live), and which crawler's last fetch before the sighting had seen that version. Snippets were not
saved before 2026-10-28 (ui.py kept domain, title, url, pub_date); cells from ui.py runs after that carry
`snippet` and this report shows it.
"""
from __future__ import annotations

import argparse
import bisect
import collections
import datetime as dt
import html
import json
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import evallib as E  # noqa: E402

sys.path.insert(0, str(E.REPO / "tools"))
CRAWL_LOG = E.REPO / "growth" / "focus" / "crawls" / "fetches.jsonl"
DEPLOYS = E.REPO / "growth" / "focus" / "crawls" / "deployments.json"
REPORT = E.REPO / "growth" / "focus" / "stored-copy.md"
SITE_START = dt.date(2026, 10, 13)
BOTS = {"OAI-SearchBot": "%OAI-SearchBot%", "GPTBot": "%GPTBot%", "bingbot": "%bingbot%", "ChatGPT-User": "%ChatGPT-User%"}

# Focus pages first (growth/focus/loop-design.md arms A-E), then the shared surfaces they appear on.
FOCUS = ["/bluetti-ac200l", "/aurzen-travelplay-autocinema-tesla-model-y", "/allpowers-r4000-3456wh",
         "/allpowers-p1800-1024wh", "/allpowers-sp037-400w-solar-panel"]
SURFACES = ["/discount-codes", "/bluetti-discount-codes", "/aurzen-discount-codes", "/allpowers-discount-codes",
            "/tesla-model-y-back-seat-screen", "/", "/products", "/portable-power-stations"]

_DATE_RE = re.compile(r"(2026-10-\d\d|(?:Oct(?:ober)?\.?\s+\d{1,2}(?:,\s*2026)?))", re.I)
_CART_RE = re.compile(r"(?:passed|tested|checked|verified)[^.\n]{0,60}?" + _DATE_RE.pattern, re.I)


def iso(t: dt.datetime) -> str:
    return t.strftime("%Y-%m-%dT%H:%M:%SZ")


def parse_t(s: str) -> dt.datetime:
    return dt.datetime.fromisoformat(s.replace("Z", "+00:00")).astimezone(dt.timezone.utc).replace(tzinfo=None)


def norm_path(url_or_path: str) -> str:
    p = url_or_path.split("dealectric.com", 1)[-1] if "dealectric.com" in url_or_path else url_or_path
    p = p.split("?")[0].split("#")[0] or "/"
    p = re.sub(r"\.html$", "", p)
    if p != "/":
        p = p.rstrip("/")
    return "/" if p in ("/index", "") else p


def norm_title(s: str) -> str:
    s = html.unescape(s or "").replace("’", "'").replace("–", "-").replace("—", "-")
    s = re.sub(r"\s*[·|\-]\s*Dealectric\s*$", "", s.strip(), flags=re.I)
    return re.sub(r"\s+", " ", s).strip(" .…").lower()


def to_date(s: str) -> str | None:
    s = s.strip()
    if s.startswith("2026-"):
        return s
    m = re.search(r"(\d{1,2})", s)
    return f"2026-10-{int(m.group(1)):02d}" if m else None


# ---- 1. deployments and page versions -------------------------------------------------------------------------

def fetch_deployments() -> list[dict]:
    repo = subprocess.run(["git", "remote", "get-url", "origin"], capture_output=True, text=True, cwd=E.REPO).stdout.strip()
    repo = re.sub(r"\.git$", "", re.sub(r".*github\.com[:/]", "", repo))
    out = subprocess.run(["gh", "api", "--paginate", f"repos/{repo}/deployments?per_page=100",
                          "--jq", '.[] | {sha, at: .created_at, env: .environment}'], capture_output=True, text=True, check=True).stdout
    rows = [json.loads(x) for x in out.splitlines() if x.strip()]
    rows = [r for r in rows if r["env"] == "github-pages"]
    rows.sort(key=lambda r: r["at"])
    return rows


class Blobs:
    """git cat-file --batch, so a few thousand page reads stay fast."""
    def __init__(self):
        self.p = subprocess.Popen(["git", "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, cwd=E.REPO)
        self.cache: dict[str, bytes | None] = {}

    def get(self, spec: str) -> bytes | None:
        if spec in self.cache:
            return self.cache[spec]
        self.p.stdin.write((spec + "\n").encode()); self.p.stdin.flush()
        head = self.p.stdout.readline().decode().split()
        if len(head) < 3 or head[1] == "missing":
            self.cache[spec] = None
            return None
        body = self.p.stdout.read(int(head[2])); self.p.stdout.read(1)
        self.cache[spec] = body
        return body


def page_file(path: str) -> str:
    return "docs/index.html" if path == "/" else f"docs{path}.html"


def extract(page_html: str) -> dict:
    title = re.search(r"<title>(.*?)</title>", page_html, re.S)
    desc = re.search(r'<meta name="description" content="(.*?)"', page_html, re.S)
    body = page_html
    m = re.search(r"<main\b.*?</main>", page_html, re.S)
    if m:
        body = m.group(0)
    body = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", body, flags=re.S)
    text = html.unescape(re.sub(r"\s+", " ", re.sub(r"<[^>]+>", " ", body))).strip()
    text = re.sub(r"^Products › .*? › [A-Za-z]+ ", "", text)   # drop the breadcrumb
    cart = re.search(r"last passed (2026-\d\d-\d\d)", page_html)
    verified = re.search(r"(?:verified|tested in [^,]*?cart,?)\s*(2026-\d\d-\d\d|[A-Z][a-z]+ \d{1,2}, 2026)", page_html)
    return {"title": html.unescape(title.group(1).strip()) if title else "", "desc": html.unescape(desc.group(1)) if desc else "",
            "lead": text[:240], "cart_date": cart.group(1) if cart else (verified.group(1) if verified else None)}


def versions(path: str, deploys: list[dict], blobs: Blobs) -> list[dict]:
    """Consecutive deployments with the same title/description/lead collapse into one version: {from, to, sha, ...}."""
    out: list[dict] = []
    for d in deploys:
        raw = blobs.get(f"{d['sha']}:{page_file(path)}")
        if raw is None:
            continue
        x = extract(raw.decode("utf-8", "replace"))
        key = (x["title"], x["desc"], x["lead"])
        if out and out[-1]["key"] == key:
            continue
        if out:
            out[-1]["to"] = d["at"]
        out.append({**x, "key": key, "from": d["at"], "to": None, "sha": d["sha"][:7]})
    for v in out:
        v.pop("key")
    return out


def live_at(vs: list[dict], t: str) -> int | None:
    idx = None
    for i, v in enumerate(vs):
        if v["from"] <= t:
            idx = i
    return idx


# ---- 2. crawler fetches ---------------------------------------------------------------------------------------

def load_crawls() -> list[dict]:
    if not CRAWL_LOG.exists():
        return []
    return [json.loads(x) for x in CRAWL_LOG.read_text().splitlines() if x.strip()]


def refresh_crawls(rows: list[dict]) -> list[dict]:
    import cf  # tools/cf.py, read-only token from the keychain
    have = {(r["t"], r["bot"], r["path"], r["status"]) for r in rows}
    last = max((r["t"][:10] for r in rows), default=None)
    start = dt.date.fromisoformat(last) - dt.timedelta(days=1) if last else SITE_START
    day, added = start, 0
    end = dt.datetime.now(dt.timezone.utc).replace(tzinfo=None).date()
    while day <= end:
        for bot, like in BOTS.items():
            q = ('{viewer{zones(filter:{zoneTag:$zone}){httpRequestsAdaptiveGroups(limit:10000, filter:{datetime_geq:"%sT00:00:00Z", '
                 'datetime_lt:"%sT00:00:00Z", userAgent_like:"%s"}, orderBy:[datetime_ASC]){count avg{sampleInterval} dimensions{datetime '
                 'clientRequestPath edgeResponseStatus verifiedBotCategory}}}}}') % (day, day + dt.timedelta(days=1), like)
            r = cf.query(q)
            if r.get("errors"):
                print(f"cloudflare {day} {bot}: {r['errors'][0].get('message')}", file=sys.stderr)
                continue
            for g in r["data"]["viewer"]["zones"][0]["httpRequestsAdaptiveGroups"]:
                dm = g["dimensions"]
                row = {"t": dm["datetime"], "bot": bot, "path": dm["clientRequestPath"], "status": dm["edgeResponseStatus"],
                       "verified": dm.get("verifiedBotCategory") or "", "count": g["count"],
                       "sample": (g.get("avg") or {}).get("sampleInterval", 1)}   # >1: the row stands for that many requests
                k = (row["t"], row["bot"], row["path"], row["status"])
                if k not in have:
                    have.add(k); rows.append(row); added += 1
        day += dt.timedelta(days=1)
    rows.sort(key=lambda r: (r["t"], r["bot"], r["path"]))
    CRAWL_LOG.parent.mkdir(parents=True, exist_ok=True)
    CRAWL_LOG.write_text("".join(json.dumps(r) + "\n" for r in rows))
    print(f"crawl log: {added} new rows, {len(rows)} total -> {CRAWL_LOG.relative_to(E.REPO)}", file=sys.stderr)
    return rows


CRAWLER_UAS = ("OAI-SearchBot", "GPTBot", "bingbot")   # UAs scanners spoof; Cloudflare's verifiedBotCategory tells them apart
SWEEP_S = 600   # an unverified fetch this close to a verified one by the same bot belongs to that crawl sweep


def crawl_kind(crawls: list[dict]) -> dict[tuple, str]:
    """Classify each 200 row of a crawler UA: 'verified'; 'sweep' (unverified, but within SWEEP_S of a verified fetch by
    the same bot); or 'dropped' (unverified and alone: a scanner, or a real fetch we cannot tell from one).

    From 2026-10-28 15:29Z Cloudflare leaves verifiedBotCategory empty on part of OpenAI's genuine crawl: on 10-29
    06:38Z one OAI-SearchBot sweep of the brand code pages logged 5 verified and 4 unverified rows within 4 s, and
    ChatGPT then showed /aurzen-discount-codes with the title only the unverified 06:38:11 fetch could have seen.
    Scanners using the UA hit .env paths (404) at other times, so the sweep rule keeps them out."""
    verified = collections.defaultdict(list)
    for r in crawls:
        if r["bot"] in CRAWLER_UAS and r["verified"]:
            verified[r["bot"]].append(parse_t(r["t"]))
    for ts in verified.values():
        ts.sort()
    kind = {}
    for r in crawls:
        if r["status"] != 200 or r["bot"] not in CRAWLER_UAS:
            continue
        key = (r["t"], r["bot"], r["path"])
        if r["verified"]:
            kind[key] = "verified"
            continue
        t, ts = parse_t(r["t"]), verified[r["bot"]]
        i = bisect.bisect_left(ts, t)
        near = [ts[j] for j in (i - 1, i) if 0 <= j < len(ts)]
        kind[key] = "sweep" if any(abs((t - x).total_seconds()) <= SWEEP_S for x in near) else "dropped"
    return kind


def page_crawls(crawls: list[dict], kinds: tuple = ("verified", "sweep")) -> dict[str, dict[str, list[str]]]:
    """{path: {bot: [times of 200 fetches, ascending]}}. Crawler-UA rows count when their crawl_kind is in `kinds`
    (default: verified or in a verified sweep); ChatGPT-User rows always count."""
    kind = crawl_kind(crawls)
    out: dict[str, dict[str, list[str]]] = collections.defaultdict(lambda: collections.defaultdict(list))
    for r in crawls:
        if r["status"] != 200:
            continue
        if r["bot"] in CRAWLER_UAS and kind[(r["t"], r["bot"], r["path"])] not in kinds:
            continue
        out[norm_path(r["path"])][r["bot"]].append(r["t"])
    for p in out.values():
        for b in p.values():
            b.sort()
    return out


def last_before(ts: list[str], t: str) -> str | None:
    prior = [x for x in ts if x <= t]
    return prior[-1] if prior else None


# ---- 3. sightings in saved ChatGPT cells -----------------------------------------------------------------------

def sightings() -> list[dict]:
    """One row per (page, chat): the search-result entry (title, snippet, rank) merged with a source pill if there was one."""
    out: dict[tuple, dict] = {}
    seen_conv = set()
    for f in sorted(E.RUNS_DIR.glob("**/*.json")):
        try:
            d = json.loads(f.read_text())
        except (ValueError, OSError):
            continue
        if not isinstance(d, dict) or not isinstance(d.get("response"), dict):
            continue
        r = d["response"]
        conv = r.get("conversation_id")
        if d.get("reused_from") or (conv and conv in seen_conv):
            continue   # the same chat saved under a second run
        if conv:
            seen_conv.add(conv)
        t = d.get("started_at") or d.get("at") or d.get("finished_at")
        if not t:
            continue
        answer = r.get("answer") or d.get("text") or ""
        cited = {norm_path(c.get("url") or "") for c in (d.get("cite_pills") or []) + (d.get("citations") or [])
                 if "dealectric.com" in (c.get("url") or "")}
        cited |= {norm_path(u.get("url") or "") for u in (r.get("markup_urls") or []) if "dealectric.com" in (u.get("url") or "")}
        quoted = sorted({x for x in (to_date(m.group(1)) for m in _CART_RE.finditer(answer)) if x and x <= t[:10]})
        run = f.relative_to(E.RUNS_DIR).parts[0]
        base = {"t": iso(parse_t(t)), "run": run, "cell": f.stem, "model": d.get("answer_model"), "quoted": quoted}
        for rank, s in enumerate(r.get("search_results") or [], 1):
            if "dealectric.com" not in (s.get("url") or ""):
                continue
            p = norm_path(s["url"])
            out.setdefault((p, run, f.stem), {**base, "path": p, "rank": rank, "title": s.get("title") or "",
                                              "snippet": s.get("snippet"), "pill": False, "cited": p in cited})
        for s in d.get("cite_pills") or []:
            if "dealectric.com" not in (s.get("url") or "") or not s.get("title"):
                continue
            p = norm_path(s["url"])
            row = out.setdefault((p, run, f.stem), {**base, "path": p, "rank": None, "title": s["title"], "snippet": None,
                                                    "pill": True, "cited": True})
            row["pill"] = True
    return list(out.values())


def match(title: str, vs: list[dict]) -> list[int]:
    """Indexes of the versions whose <title> is the stored title (or one is a prefix of the other, >= 20 chars)."""
    n = norm_title(title)
    hits = []
    for i, v in enumerate(vs):
        m = norm_title(v["title"])
        if n == m or (min(len(n), len(m)) >= 20 and (m.startswith(n) or n.startswith(m))):
            hits.append(i)
    return hits


# ---- report ---------------------------------------------------------------------------------------------------

def days(a: str, b: str) -> float:
    return (parse_t(b) - parse_t(a)).total_seconds() / 86400


def analyse(deploys, crawls):
    blobs = Blobs()
    pc = page_crawls(crawls)
    pv = page_crawls(crawls, ("verified",))
    pd = page_crawls(crawls, ("dropped",))
    by_path = collections.defaultdict(list)
    for s in sightings():
        by_path[s["path"]].append(s)
    rows, vers = {}, {}
    for path in set(by_path) | set(FOCUS):
        vs = versions(path, deploys, blobs)
        vers[path] = vs
        out = []
        for s in sorted(by_path.get(path, []), key=lambda x: x["t"]):
            hits = match(s["title"], vs)
            cur = live_at(vs, s["t"])
            row = {**s, "versions": hits, "live": cur, "matched": None, "behind": None, "reflects": None}
            older = [h for h in hits if cur is not None and h <= cur]
            if older:
                m = cur if cur in hits else max(older)
                row["matched"] = m
                row["reflects"] = vs[m]["cart_date"]
                # Days behind as a range: the stored title was carried by versions first..m, so the copy is at least
                # (sighting - end of version m) and at most (sighting - start of the first matching version) old.
                if m == cur:
                    row["behind"] = (0.0, 0.0)
                else:
                    first = min(h for h in older if all(k in hits for k in range(h, m + 1)))
                    row["behind"] = (round(days(vs[m + 1]["from"], s["t"]), 1), round(days(vs[first]["from"], s["t"]), 1))
            for bot in ("OAI-SearchBot", "bingbot"):
                lb = last_before(pc.get(path, {}).get(bot, []), s["t"])
                row[f"last_{bot}"] = lb
                row[f"fits_{bot}"] = None if (lb is None or not hits) else (live_at(vs, lb) in hits)
            lv = last_before(pv.get(path, {}).get("OAI-SearchBot", []), s["t"])
            row["fits_OAI_verified"] = None if (lv is None or not hits) else (live_at(vs, lv) in hits)
            # A dropped unverified fetch is confirmed by title when it is the only fetch that saw the version shown:
            # later than the last counted fetch (which saw another version, or there was none) and before the chat.
            row["oai_dropped_fit"] = None
            if hits and row["fits_OAI-SearchBot"] is not True:
                lb = row["last_OAI-SearchBot"]
                fit = [x for x in pd.get(path, {}).get("OAI-SearchBot", [])
                       if x <= s["t"] and (lb is None or x > lb) and live_at(vs, x) in hits]
                row["oai_dropped_fit"] = fit[-1] if fit else None
            out.append(row)
        rows[path] = out
    return rows, vers, pc


def fmt_t(t: str | None) -> str:
    return t[5:16].replace("T", " ") if t else "never"


def index_state(path: str, vs: list[dict], pc, now: str) -> dict:
    """The version OpenAI's index holds (live at OAI-SearchBot's last fetch) and the versions deployed since."""
    oai = pc.get(path, {}).get("OAI-SearchBot", [])
    last = oai[-1] if oai else None
    held = live_at(vs, last) if last else None
    cur = live_at(vs, now)
    return {"last": last, "held": held, "cur": cur, "pending": (cur - held) if (held is not None and cur is not None) else None,
            "gaps": [round(days(a, b), 1) for a, b in zip(oai, oai[1:])], "fetches": oai,
            "since": round(days(last, now), 1) if last else None}


def write_report(rows, vers, pc, now: str, crawls: list[dict]) -> str:
    L = ["# What ChatGPT sees: stored titles vs live pages (DLC-77)", "",
         f"Generated by `growth/evals/storedcopy.py` at {now}. Do not edit by hand; rerun it.", "",
         "One row per chat in which a dealectric.com page showed up in ChatGPT's search results (`#rank`) or as a source "
         "pill (`pill`). **Version** is the deployed version whose `<title>` the stored title matches (v1 = the page's "
         "first deploy; the version list is under each table). **Reflects** is the cart date that version carried. "
         "**Behind** is how many days old the stored copy was when ChatGPT showed it, as a range: since the matching "
         "version was replaced, and since it first went live (0 = the live version). **Quoted** is the cart date the "
         "answer itself quoted (\"chat day\" = the date of the chat, usually ChatGPT's own \"as of today\", since no index copy "
         "is that new). **OAI / Bing** say whether that crawler's last fetch before the chat saw a version with "
         "the stored title, and when it was.", "",
         "Snippets: no run before 2026-10-28 20:30Z saved them (ui.py kept only domain, title, url, pub_date). ui.py now "
         "keeps `snippet`; the column fills from the next reading.", ""]
    fit = collections.Counter()
    for rs in rows.values():
        for r in rs:
            if r["behind"] and r["behind"][0] > 0:
                for bot in ("OAI-SearchBot", "bingbot"):
                    fit[(bot, r[f"fits_{bot}"])] += 1
                fit[("OAI_verified", r["fits_OAI_verified"])] += 1
    L += ["## Which crawl feeds the stored copy", "",
          "Only chats that showed a superseded version tell the crawlers apart. For those, did the crawler's last fetch "
          "before the chat see the version ChatGPT showed?", "",
          "| crawler | yes | no (it had fetched a newer one) | never fetched the page |", "|---|---|---|---|"]
    for bot, label in (("OAI-SearchBot", "OAI-SearchBot"), ("OAI_verified", "OAI-SearchBot, verified rows only"),
                       ("bingbot", "bingbot")):
        L.append(f"| {label} | {fit[(bot, True)]} | {fit[(bot, False)]} | {fit[(bot, None)]} |")
    kind = crawl_kind(crawls)
    kc = collections.Counter(k for (t, b, p), k in kind.items() if b == "OAI-SearchBot")
    swept = collections.Counter(p for (t, b, p), k in kind.items() if b == "OAI-SearchBot" and k == "sweep" and p != "/robots.txt")
    confirmed = sorted({(r["oai_dropped_fit"], r["path"]) for rs in rows.values() for r in rs if r["oai_dropped_fit"]})
    # Chats whose shown title only a sweep row explains (the last verified fetch saw another version), live copies included.
    by_sweep = sorted({(r["last_OAI-SearchBot"], r["path"]) for rs in rows.values() for r in rs
                       if r["fits_OAI-SearchBot"] and r["fits_OAI_verified"] is not True}, key=lambda x: (x[0] or "", x[1]))
    L += ["", "## Unverified OpenAI fetches", "",
          "Scanners send the OAI-SearchBot UA, so a row counts only when Cloudflare verified it or it sits within "
          f"{SWEEP_S // 60} min of a verified fetch by the same bot (one crawl sweep: from 2026-10-28 15:29Z Cloudflare leaves "
          "part of OpenAI's genuine crawl unverified). Times marked `*` below are such sweep rows. OAI-SearchBot 200 rows: "
          f"{kc['verified']} verified, {kc['sweep']} unverified in a verified sweep, {kc['dropped']} unverified and dropped.", ""]
    if swept:
        L.append("Pages fetched in a sweep without a verified row: " + ", ".join(f"`{p}`" for p in sorted(swept)) + ".")
        L.append("")
    L.append("Sweep rows that a later chat's title confirms (verified rows alone would put an older version in the index): " +
             (", ".join(f"`{p}` {fmt_t(t)}" for t, p in by_sweep) if by_sweep else "none") + ".")
    L.append("")
    L.append("Dropped fetches that a later chat's title confirms (the only fetch that saw the version shown): " +
             (", ".join(f"`{p}` {fmt_t(t)}" for t, p in confirmed) if confirmed else "none") + ".")
    L += ["", "## Index state of the focus pages", "",
          "The version OpenAI's index holds is the one live at OAI-SearchBot's last fetch. A lever is in the index only "
          "once a fetch after its ship has happened.", "",
          "| page | OAI fetches | last fetch | days since | index holds | live | versions pending | gaps between fetches (d) |",
          "|---|---|---|---|---|---|---|---|"]
    for path in FOCUS:
        st = index_state(path, vers.get(path) or [], pc, now)
        L.append(f"| `{path}` | {len(st['fetches'])} | {fmt_t(st['last'])} | {st['since'] if st['since'] is not None else '-'} | "
                 f"{'v%d' % (st['held'] + 1) if st['held'] is not None else 'nothing'} | "
                 f"{'v%d' % (st['cur'] + 1) if st['cur'] is not None else '-'} | {st['pending'] if st['pending'] is not None else 'all'} | "
                 f"{', '.join(map(str, st['gaps'])) or '-'} |")
    L.append("")
    order = FOCUS + SURFACES + sorted(p for p in rows if p not in FOCUS + SURFACES)
    for path in order:
        if path not in rows:
            continue
        vs = vers.get(path) or []
        rs = rows[path]
        L += [f"## `{path}`" + (" (focus)" if path in FOCUS else ""), ""]
        crawl = pc.get(path, {})
        oai, bing = crawl.get("OAI-SearchBot", []), crawl.get("bingbot", [])
        star = lambda x: "*" if kind.get((x, "OAI-SearchBot", path)) == "sweep" else ""
        L.append(f"OAI-SearchBot fetches (200): {', '.join(fmt_t(x) + star(x) for x in oai) or 'none'}. bingbot: {len(bing)} "
                 f"(last {fmt_t(bing[-1] if bing else None)}).")
        if not rs:
            L += ["", "No sighting in any saved ChatGPT cell.", ""]
        else:
            L += ["", "| seen (UTC) | run / cell | shown as | stored title | version | reflects | behind (d) | quoted | snippet | OAI last fetch | Bing last fetch |",
                  "|---|---|---|---|---|---|---|---|---|---|---|"]
            for r in rs:
                ver = ("v" + "/v".join(str(h + 1) for h in r["versions"])) if r["versions"] else "no match"
                b = r["behind"]
                beh = "" if b is None else ("0" if b == (0.0, 0.0) else f"{b[0]:g}–{b[1]:g}")
                fo = lambda k: ("" if r[f"fits_{k}"] is None else ("yes " if r[f"fits_{k}"] else "no ")) + fmt_t(r[f"last_{k}"])
                shown = " + ".join(x for x in ((f"#{r['rank']}" if r["rank"] else ""), ("pill" if r["pill"] else "")) if x)
                snip = (r.get("snippet") or "").replace("|", "/").replace("\n", " ")[:160]
                L.append(f"| {fmt_t(r['t'])} | {r['run']} / {r['cell']} | {shown} | {r['title'].replace('|', '/')[:100]} | {ver} | "
                         f"{r['reflects'] or ''} | {beh} | {', '.join(q + (' (chat day)' if q == r['t'][:10] else '') for q in r['quoted'])} | {snip} | {fo('OAI-SearchBot')} | {fo('bingbot')} |")
        if vs:
            L += ["", "<details><summary>Versions (live window, cart date, title, start of the description)</summary>", "",
                  "| v | live from (UTC) | to | sha | cart date | title | description |", "|---|---|---|---|---|---|---|"]
            for i, v in enumerate(vs):
                L.append(f"| v{i + 1} | {fmt_t(v['from'])} | {fmt_t(v['to']) if v['to'] else 'live'} | {v['sha']} | "
                         f"{v['cart_date'] or ''} | {v['title'].replace('|', '/')} | {v['desc'].replace('|', '/')[:120]} |")
            L += ["", "</details>"]
        L.append("")
    return "\n".join(L) + "\n"


def summary_lines(rows, vers, pc, now: str) -> list[str]:
    out = []
    for path in FOCUS:
        rs = rows.get(path, [])
        st = index_state(path, vers.get(path) or [], pc, now)
        last = rs[-1] if rs else None
        out.append(f"{path}: {len(rs)} chats; latest {fmt_t(last['t']) if last else '-'} behind {last['behind'] if last else '-'} d; "
                   f"OAI last fetch {fmt_t(st['last'])}, {st['pending']} version(s) pending")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--no-fetch", action="store_true", help="use the cached crawl log and deployment list")
    ap.add_argument("--json", type=Path, help="also write the sighting rows as JSON here")
    a = ap.parse_args()
    crawls = load_crawls()
    if a.no_fetch and DEPLOYS.exists():
        deploys = json.loads(DEPLOYS.read_text())
    else:
        deploys = fetch_deployments()
        DEPLOYS.parent.mkdir(parents=True, exist_ok=True)
        DEPLOYS.write_text(json.dumps(deploys, indent=0) + "\n")
        crawls = refresh_crawls(crawls)
    rows, vers, pc = analyse(deploys, crawls)
    now = iso(dt.datetime.now(dt.timezone.utc).replace(tzinfo=None))
    REPORT.write_text(write_report(rows, vers, pc, now, crawls))
    if a.json:
        a.json.write_text(json.dumps(rows, indent=1))
    print(f"wrote {REPORT.relative_to(E.REPO)}")
    print("\n".join(summary_lines(rows, vers, pc, now)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
