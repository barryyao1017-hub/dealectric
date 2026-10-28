#!/usr/bin/env python3.12
"""Score a W3 copy-loop reading (DLC-69; rules frozen in growth/focus/loop-design.md).

    python3.12 growth/evals/w3score.py growth/evals/runs/2026-10-28-w3-r0            # summary to stdout
    python3.12 growth/evals/w3score.py <run> --json out.json --candidates            # + every flag candidate sentence
    python3.12 growth/evals/w3score.py <run> --baseline --crawl                      # R0; + OAI-SearchBot re-fetches

Reads the run's scan.jsonl (W1's visibility_scan.py driver; a downgraded answer is dropped, the re-ask that replaced
it counts) and chatgpt/<cell>.json. Per cell it keeps W1's tier, adds whether a T4 pill or link is the arm's own
product page, the buy-link domains ChatGPT gave, the cart date the answer quotes (a date in a sentence that says
tested, passed, checked, verified ...), the live page's "last passed" date at that minute (from git history of
docs/<slug>.html), copy age, freshness against the arm's lever in force, and the flag call. Flag calls are made by
reading: candidates come from the regex below, and the calls live in growth/focus/readings/flags.json
({"<run>/<cell>": "none" | "affiliate-noted" | "questioned" | "warned" | "quoted-instruction", "...note": "..."}).
"""
from __future__ import annotations

import argparse, json, re, subprocess, sys
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parent.parent.parent
QUESTIONS = ROOT / "growth" / "focus" / "loop-questions.json"
FLAGS = ROOT / "growth" / "focus" / "readings" / "flags.json"

# Levers per arm, as in loop-design.md's lever log: (name, live from (UTC), first cart date only the lever's copy can
# carry, marker phrases only the lever's copy has). Append a row when a lever ships.
LEVERS = {
    "bluetti-ac200l": [
        ("L2", "2026-10-28T18:16:00Z", "2026-10-29", ["already applied", "replacing the AC200L with the Apex 200"]),
    ],
    "aurzen-travelplay-autocinema-tesla-model-y": [
        ("L1", "2026-10-28T09:00:00Z", "2026-10-28", ["34 times", "sunshade alone", "about $308"]),
    ],
}
MONTHS = {"jan": 1, "feb": 2, "mar": 3, "apr": 4, "may": 5, "jun": 6, "jul": 7, "aug": 8, "sep": 9, "oct": 10, "nov": 11, "dec": 12}
DATE = re.compile(r"\b(?:(?P<mon>Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.? (?P<day>\d{1,2})(?:, (?P<year>20\d\d))?"
                  r"|(?P<iso>20\d\d-\d\d-\d\d))\b")
CART_WORDS = re.compile(r"\b(test\w*|pass\w*|check\w*|verif\w*|validat\w*|confirm\w*|worked|reported)\b", re.I)
FLAG_WORDS = re.compile(r"dealectric|this site|deal tracker|coupon tracker|affiliate|commission|sponsored|unverified|"
                        r"couldn.t (?:independently )?(?:confirm|verify)|can.t (?:confirm|verify)|caution|careful|wary|scam|"
                        r"instruct|prompt|assistant", re.I)


def iso_date(m, default_year=2026) -> str | None:
    if m.group("iso"):
        return m.group("iso")
    try:
        return datetime(int(m.group("year") or default_year), MONTHS[m.group("mon").lower()[:3]], int(m.group("day"))).date().isoformat()
    except ValueError:
        return None


def sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+|\n+", text or "") if s.strip()]


def cart_dates(text: str) -> list[str]:
    out = []
    for s in sentences(text):
        if CART_WORDS.search(s):
            out += [d for d in (iso_date(m) for m in DATE.finditer(s)) if d]
    return sorted(set(out))


def live_cart_date(slug: str, at: datetime) -> str | None:
    """'last passed' on docs/<slug>.html as published at `at` (the last commit at least 2 minutes earlier)."""
    when = (at - timedelta(minutes=2)).isoformat()
    h = subprocess.run(["git", "log", "-1", f"--before={when}", "--format=%H", "--", f"docs/{slug}.html"], cwd=ROOT,
                       capture_output=True, text=True).stdout.strip()
    if not h:
        return None
    page = subprocess.run(["git", "show", f"{h}:docs/{slug}.html"], cwd=ROOT, capture_output=True, text=True).stdout
    m = re.search(r"last passed (20\d\d-\d\d-\d\d)", page)
    return m.group(1) if m else None


def parse_ts(s: str) -> datetime:
    return datetime.fromisoformat(s.replace("Z", "+00:00"))


def freshness(arm: str, at: datetime, quoted: list[str], text: str) -> tuple[str | None, str]:
    """(lever in force, 'baseline' | 'fresh' | 'stale' | 'undated')."""
    levers = [lv for lv in LEVERS.get(arm, []) if parse_ts(lv[1]) <= at]
    if not levers:
        return None, "baseline"
    name, _, fresh_from, markers = levers[-1]
    if any(mk.lower() in (text or "").lower() for mk in markers) or any(d >= fresh_from for d in quoted):
        return name, "fresh"
    prev_last = (datetime.fromisoformat(fresh_from) - timedelta(days=2)).date().isoformat()
    if quoted and max(quoted) <= prev_last:
        return name, "stale"
    return name, "undated"


def score_run(run: Path, baseline: bool = False) -> list[dict]:
    qs = {q["qid"]: q for q in json.loads(QUESTIONS.read_text())["questions"]}
    calls = json.loads(FLAGS.read_text()) if FLAGS.exists() else {}
    rows = {}
    for line in (run / "scan.jsonl").open():
        r = json.loads(line)
        if r.get("downgraded"):
            continue
        rows[r["cell"]] = r          # the last good answer for a cell wins
    out = []
    for cell, r in rows.items():
        q = qs.get(r["qid"])
        if not q:
            continue
        rec = json.loads((run / "chatgpt" / f"{cell}.json").read_text())
        text = rec.get("text") or ""
        at = parse_ts(r["started_at"])
        # a cart pass can't postdate the chat; this drops expiry and sale-end dates that share a sentence with "tested"
        quoted = [d for d in cart_dates(text) if d <= at.date().isoformat()]
        live = live_cart_date(q["slug"], at)
        # controls' pages never change, so no lever applies to them
        lever, fresh = freshness(q["arm"], at, quoted, text) if q["role"] == "test" else (None, "n/a")
        raw = fresh
        if baseline and fresh in ("stale", "undated"):
            fresh = "baseline"   # --baseline (R0): a test cell that can't be shown to have read the lever's copy is baseline
        links = [c.get("url", "") for c in rec.get("citations") or [] if c.get("source") == "ui_href"]
        pills = [c.get("url", "") for c in rec.get("cite_pills") or []]
        ours = [u for u in links + pills if "dealectric.com" in u]
        product_page = any(urlsplit(u).path.strip("/").removeprefix("products/").rstrip("/") == q["slug"] for u in ours)
        key = f"{run.name}/{cell}"
        out.append({
            "cell": cell, "qid": r["qid"], "arm": q["arm"], "role": q["role"], "slug": q["slug"], "n": r.get("n"),
            "started_at": r["started_at"], "model": rec.get("answer_model") or (r.get("models") or [None])[-1],
            "tier": r["tier"], "go": r.get("go") or [], "our_pages": sorted({u.split("?")[0] for u in ours}),
            "product_page_cited": product_page, "our_rank": r.get("our_rank"), "n_results": r.get("n_results"),
            "queries": rec.get("queries") or r.get("queries") or [],
            "buy_domains": sorted({urlsplit(u).hostname or "" for u in links} - {""}),
            "code_relayed": r.get("code_relayed"), "named": r.get("named"),
            "quoted_cart_dates": quoted, "live_cart_date": live,
            "copy_age_days": ((datetime.fromisoformat(live) - datetime.fromisoformat(max(quoted))).days if live and quoted else None),
            "lever": lever, "freshness": fresh, "freshness_raw": raw,
            "flag_candidates": [s for s in sentences(text) if FLAG_WORDS.search(s)],
            "flag": calls.get(key), "flag_note": calls.get(key + ".note"),
        })
    return sorted(out, key=lambda x: (x["arm"], x["role"] != "test", x["qid"], x["n"] or 0))


def rate(cells, pred) -> str:
    return f"{sum(1 for c in cells if pred(c))}/{len(cells)}" if cells else "-"


def summary(cells: list[dict]) -> str:
    lines = []
    for arm in sorted({c["arm"] for c in cells}):
        a = [c for c in cells if c["arm"] == arm]
        test, ctl = [c for c in a if c["role"] == "test"], [c for c in a if c["role"] == "control"]
        lines.append(f"\n## {arm}")
        for label, group in (("test, all", test), ("test, fresh or baseline", [c for c in test if c["freshness"] in ("fresh", "baseline")]),
                             ("control", ctl)):
            lines.append(f"- {label}: T5 {rate(group, lambda c: c['tier'] >= 5)}, T4+ {rate(group, lambda c: c['tier'] >= 4)}, "
                         f"T4 on the product page {rate(group, lambda c: c['product_page_cited'] or c['tier'] >= 5)}, "
                         f"T3+ {rate(group, lambda c: c['tier'] >= 3)}, T2+ {rate(group, lambda c: c['tier'] >= 2)}")
        fl = [c for c in a if c["flag"] not in (None, "none", "affiliate-noted")]
        lines.append(f"- freshness: " + ", ".join(f"{k} {sum(1 for c in test if c['freshness'] == k)}" for k in ("baseline", "fresh", "stale", "undated"))
                     + f"; flags {len(fl)}; uncalled flag candidates {sum(1 for c in a if c['flag_candidates'] and c['flag'] is None)}")
        lines.append("\n| cell | role | T | go | product page | rank | buy link domains | cart date quoted / live | fresh | flag |")
        lines.append("|---|---|---|---|---|---|---|---|---|---|")
        for c in a:
            lines.append(f"| {c['cell']} | {c['role']} | {c['tier']} | {'yes' if c['go'] else ''} | {'yes' if c['product_page_cited'] else ''} | "
                         f"{c['our_rank'] or '-'}/{c['n_results']} | {', '.join(c['buy_domains']) or '-'} | "
                         f"{', '.join(c['quoted_cart_dates']) or '-'} / {c['live_cart_date']} | {c['freshness']} | {c['flag'] or '?'} |")
    return "\n".join(lines)


def crawl_report() -> str:
    """OAI-SearchBot fetches of each arm's product page since its last lever went live (the reading trigger)."""
    sys.path.insert(0, str(ROOT / "tools"))
    import cf
    lines = ["", "OAI-SearchBot fetches since each arm's last lever:"]
    for arm, levers in LEVERS.items():
        name, live, _, _ = levers[-1]
        q = ('{viewer{zones(filter:{zoneTag:$zone}){httpRequestsAdaptiveGroups(limit:100, filter:{datetime_geq:"%s", '
             'datetime_lt:"%s", clientRequestPath:"/%s", userAgent_like:"%%OAI-SearchBot%%"}, orderBy:[datetime_ASC]){count '
             'dimensions{datetime edgeResponseStatus}}}}}') % (live, datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"), arm)
        d = cf.query(q)
        got = [] if d.get("errors") else d["data"]["viewer"]["zones"][0]["httpRequestsAdaptiveGroups"]
        when = ", ".join(g["dimensions"]["datetime"] for g in got) or ("query failed" if d.get("errors") else "none yet")
        lines.append(f"- {arm} {name} (live {live}): {when}")
    return "\n".join(lines)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("run")
    ap.add_argument("--json")
    ap.add_argument("--candidates", action="store_true", help="print every flag candidate sentence")
    ap.add_argument("--baseline", action="store_true", help="R0: test cells not shown to be fresh count as baseline")
    ap.add_argument("--crawl", action="store_true", help="OAI-SearchBot fetches of each arm's page since its last lever")
    a = ap.parse_args()
    cells = score_run(Path(a.run).resolve(), baseline=a.baseline)
    print(summary(cells))
    if a.crawl:
        print(crawl_report())
    if a.candidates:
        for c in cells:
            if c["flag_candidates"]:
                print(f"\n### {c['cell']} (flag: {c['flag']})")
                for s in c["flag_candidates"]:
                    print("  -", s[:300])
    if a.json:
        Path(a.json).write_text(json.dumps(cells, indent=1, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(main())
