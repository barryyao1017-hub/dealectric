#!/usr/bin/env python3.12
"""Page scoreboard: which pages and clusters real shoppers' assistants actually reach (added 2026-11-04).

The gap loop picks queries because they look open; this closes the loop on outcome. For every published page it counts,
over a window:

  fetch    Cloudflare-verified AI Assistant fetches (ChatGPT-User, Claude-User, Perplexity-User ...) that fetchwho.py
           classes as outside or outside-likely: someone else's chat retrieved the page. The impression count.
  amb      the same, classed ambiguous (US, near a chat of ours). Shown, never counted as outside.
  ours     fetches inside our own chat windows (evals). Shown so a busy page isn't mistaken for a popular one.
  land     D1 landings tagged utm_source (a person clicked through from an assistant), outside only.
  go       D1 /go/ redirects from browsers, outside only, and only with provenance: a click from one of our pages is
           credited to that page (referrer), one tagged utm_source by an assistant to the product. A user
           agent + country that opens 4+ different links in one hour is a link-checker sweep and is dropped (10-30..11-04:
           CA, DE, GB, FR and US Chrome UAs each walked 30-46 /go/ links in minutes).
  index    OAI-SearchBot fetches (ChatGPT's index crawler refreshing its stored copy) and the date of the last one.

Pages group into clusters: lead-product category (the first row that is one of our products) plus an intent theme read
from the slug (appliance, place, spec, use case). Each cluster gets a call:

  reinvest   outside fetches + landings >= 3, or any landing
  stop       every page at least --stop-days old and zero outside fetches or landings
  too early  otherwise

Cloudflare's Free plan keeps about 8 days of request data, so fetch and index counts cover at most that; D1 keeps all.

    python3.12 tools/scoreboard.py                     # last 8 days, writes growth/scoreboard/<today>.md
    python3.12 tools/scoreboard.py --days 7 --no-write
    python3.12 tools/scoreboard.py --pages             # also print the per-page table
"""
from __future__ import annotations

import argparse
import re
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "src"))
import fetchwho as F  # noqa: E402
import compare  # noqa: E402
import gaps  # noqa: E402
import products  # noqa: E402

SITE = "https://dealectric.com/"
OUTSIDE = ("outside", "outside-likely")
OURS = ("ours", "ours (hook)", "ours (mtime)")

# Intent themes read from the slug, first match wins. Order matters: an appliance page that names a place ("fridge for
# an RV") is about the appliance.
THEMES = [
    ("appliance", r"fridge|freezer|cpap|sump|insulin|aquarium|pellet|furnace|starlink|window-ac|air-condition|microwave|"
                  r"heater|oxygen|e-?bike|well-pump|space-heater|coffee|tv\b|router|modem"),
    ("nas use case", r"unraid|plex|jellyfin|immich|docker|time-machine|proxmox|nextcloud|paperless|reolink|frigate|"
                     r"audiobookshelf|minecraft|pi-hole|cgnat|haos|home-assistant|veeam|icloud|google-drive|home-lab|"
                     r"photograph|video-edit|backup"),
    ("place / event", r"\brv\b|-rv-|-rv$|cabin|camping|van|booth|market|tailgat|outage|off-grid|hurricane|boat|overland"),
    ("spec", r"lightest|quiet|noise|charge-speed|fastest|ups|expand|expansion|1-?kwh|2-?kwh|3-?kwh|1000w|1-000|10gbe|"
             r"2-5gbe|under-\d|cheapest|budget|lifepo4|watts|solar-watts|vs-|-vs\b|ssd|bay"),
    ("travel", r"flying|airline|travel|carry-on"),
]


def norm_path(p: str) -> str:
    p = (p or "").split("?", 1)[0].strip("/")
    p = re.sub(r"\.html$", "", p)
    if p.startswith("compare/"):            # old /compare/<slug>/ location redirects to /<slug>
        p = p[len("compare/"):]
    return p


def theme(slug: str) -> str:
    for name, rx in THEMES:
        if re.search(rx, slug):
            return name
    return "general"


def page_index() -> dict[str, dict]:
    cat = {p["slug"]: p.get("category", "?") for p in products.PRODUCTS}
    pages = {}
    for kind, recs in (("gap", gaps.GAP_PAGES), ("compare", compare.COMPARISONS)):
        for r in recs:
            lead = next((row["slug"] for row in r.get("rows", []) if row.get("slug") in cat), None)
            c = cat.get(lead, "mixed")
            pages[r["slug"]] = {"slug": r["slug"], "kind": kind, "id": (r.get("question") or "").split(" ")[0],
                                "published": r.get("published"), "cluster": f"{c} · {theme(r['slug'])}",
                                "variant": r.get("copy_variant"),
                                "layout": "ai-note" if r.get("ai_note") else "lead-first" if r.get("lead_first") else "classic"}
    for p in products.PRODUCTS:
        pages.setdefault(p["slug"], {"slug": p["slug"], "kind": "product", "id": "", "published": None,
                                     "cluster": f"{p.get('category', '?')} · product page"})
    return pages


def blank() -> dict:
    return {"fetch": 0, "amb": 0, "ours": 0, "land": 0, "go": 0, "index": 0, "last_index": None, "bots": set()}


SWEEP_SLUGS = 4      # one (user agent, country) opening this many different /go/ links or pages in an hour is a crawler


def sweep_key(r: dict) -> tuple:
    return (r.get("ua") or "", r.get("country") or "", r["ts"].strftime("%Y-%m-%dT%H"), r["src"])


def sweep_keys(d1: list[dict]) -> set[tuple]:
    """D1 redirects and landings from link-checker sweeps: browser-looking user agents that walk the catalog."""
    seen = defaultdict(set)
    for r in d1:
        seen[sweep_key(r)].add(r["path"])
    return {k for k, v in seen.items() if len(v) >= SWEEP_SLUGS}


def collect(since: datetime, until: datetime, slack: float, near: float) -> tuple[dict, list[str]]:
    notes = []
    idx = F.Index(F.load_windows(since, until))
    ver, unver = F.cf_fetches(since, until)
    d1, err = F.d1_fetches(since, until)
    if err:
        notes.append(f"D1 unavailable: {err}")
    bursts = F.scanner_bursts(unver + d1)
    stats = defaultdict(blank)
    for r in (F.classify(f, idx, slack, near) for f in ver):
        if r["cls"] in ("crawler", "scanner") or (r.get("status") or 200) >= 400:
            continue
        s = stats[norm_path(r["path"])]
        n = r.get("n", 1)
        if r["cls"] in OUTSIDE:
            s["fetch"] += n
            s["bots"].add(r["bot"])
        elif r["cls"] == "ambiguous":
            s["amb"] += n
        elif r["cls"] in OURS:
            s["ours"] += n
    sweeps = sweep_keys(d1)
    go_meta = {}
    grows, gerr = F.E.d1_query("SELECT ts, slug, utm_source, referrer FROM clicks WHERE kind='redirect' "
                               f"AND ts >= '{F.iso(since)}' AND ts < '{F.iso(until)}'")
    if gerr:
        notes.append(f"D1 /go/ referrers unavailable: {gerr}")
    for g in grows:
        go_meta[(F.parse_ts(g["ts"]), f"/go/{g['slug']}")] = (g.get("utm_source") or "", g.get("referrer") or "")
    for r in (F.classify(f, idx, slack, near, bursts) for f in d1):
        if r["cls"] not in OUTSIDE or r.get("bot") == "bot-like" or sweep_key(r) in sweeps:
            continue
        if r["src"] == "d1 landing":
            stats[norm_path(r["path"])]["land"] += 1
        elif r["src"] == "d1 redirect":
            # Only clicks with provenance: an assistant's utm tag (credited to the product) or a click from one of our
            # pages (credited to that page). Bare /go/ hits with neither are bots or link checkers (663 of 830, 10-27..11-04).
            utm, ref = go_meta.get((r["ts"], r["path"]), ("", ""))
            if ref.startswith(SITE):
                stats[norm_path(ref[len(SITE):])]["go"] += 1
            elif utm:
                stats[r["path"].removeprefix("/go/")]["go"] += 1
    for r in F._cf_rows('userAgent_like:"%OAI-SearchBot%"', since, until):
        if r["verified"] and (r.get("status") or 200) < 400:
            s = stats[norm_path(r["path"])]
            s["index"] += r.get("n", 1)
            t = r["ts"].date().isoformat()
            s["last_index"] = max(s["last_index"] or t, t)
    return stats, notes


def call(rows: list[dict], stop_days: int) -> str:
    sig = sum(r["fetch"] + r["land"] for r in rows)
    if any(r["land"] for r in rows) or sig >= 3:
        return "reinvest"
    if rows and all(r["age"] is not None and r["age"] >= stop_days for r in rows) and sig == 0:
        return "stop"
    return "too early"


def render(pages: dict, stats: dict, since: datetime, until: datetime, stop_days: int, notes: list[str], with_pages: bool) -> str:
    today = until.date()
    rows = []
    for slug, p in pages.items():
        s = stats.get(slug, blank())
        age = (today - date.fromisoformat(p["published"])).days if p["published"] else None
        rows.append({**p, **s, "age": age})
    known = set(pages)
    other = {k: v for k, v in stats.items() if k not in known and (v["fetch"] or v["land"])}

    out = [f"# Page scoreboard {today.isoformat()}",
           "",
           f"Window {F.iso(since)} .. {F.iso(until)} (Cloudflare fetch and index counts cover at most the last ~8 days; "
           "D1 landings and /go/ cover the whole window). Outside = fetchwho.py classes outside + outside-likely; "
           "ambiguous and our own eval traffic are shown apart and never counted.",
           ""]
    out += [f"> {n}" for n in notes]

    by = defaultdict(list)
    for r in rows:
        if r["kind"] != "product":
            by[r["cluster"]].append(r)
    ordered = sorted(by.items(), key=lambda kv: (-sum(r["fetch"] + 5 * r["land"] for r in kv[1]), kv[0]))
    out += ["## Comparison and gap page clusters", "",
            "| Cluster | Call | Pages | Median age (d) | Outside fetches | Landings | /go/ | Index fetches | Pages indexed | Ours | Ambiguous |",
            "|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|"]
    for name, rs in ordered:
        ages = sorted(r["age"] for r in rs if r["age"] is not None)
        med = ages[len(ages) // 2] if ages else "–"
        out.append(f"| {name} | {call(rs, stop_days)} | {len(rs)} | {med} | {sum(r['fetch'] for r in rs)} | "
                   f"{sum(r['land'] for r in rs)} | {sum(r['go'] for r in rs)} | {sum(r['index'] for r in rs)} | "
                   f"{sum(1 for r in rs if r['index'])} | {sum(r['ours'] for r in rs)} | {sum(r['amb'] for r in rs)} |")

    prod = defaultdict(list)
    for r in rows:
        if r["kind"] == "product":
            prod[r["cluster"].split(" · ")[0]].append(r)
    out += ["", "## Product pages by category", "", "| Category | Pages | Outside fetches | Landings | /go/ | Pages indexed |",
            "|---|---:|---:|---:|---:|---:|"]
    for c, rs in sorted(prod.items(), key=lambda kv: -sum(r["fetch"] + 5 * r["land"] + 5 * r["go"] for r in kv[1])):
        out.append(f"| {c} | {len(rs)} | {sum(r['fetch'] for r in rs)} | {sum(r['land'] for r in rs)} | {sum(r['go'] for r in rs)} | "
                   f"{sum(1 for r in rs if r['index'])} |")

    hits = sorted((r for r in rows if r["fetch"] or r["land"] or r["go"]), key=lambda r: -(r["fetch"] + 5 * r["land"] + 5 * r["go"]))
    out += ["", "## Pages with outside signal", "",
            "| Page | Kind | Cluster | Age (d) | Fetches | Landings | /go/ | Assistants | Last index fetch |",
            "|---|---|---|---:|---:|---:|---:|---|---|"]
    for r in hits:
        out.append(f"| /{r['slug']} | {r['kind']} {r['id']} | {r['cluster']} | {r['age'] if r['age'] is not None else '–'} | "
                   f"{r['fetch']} | {r['land']} | {r['go']} | {', '.join(sorted(r['bots'])) or '–'} | {r['last_index'] or '–'} |")
    if not hits:
        out.append("| (none) | | | | | | | | |")

    comp = [r for r in rows if r["kind"] != "product"]
    unindexed = [r for r in comp if not r["index"]]
    out += ["", f"Comparison/gap pages: {len(comp)}; fetched by OAI-SearchBot in the window: {len(comp) - len(unindexed)}; "
            f"with any outside signal: {sum(1 for r in comp if r['fetch'] or r['land'])}."]
    if other:
        out += ["", "Other paths with outside signal: " + ", ".join(
            f"/{k or ''} ({v['fetch']} fetch, {v['land']} land)" for k, v in sorted(other.items(), key=lambda kv: -(kv[1]["fetch"] + kv[1]["land"])))]
    # Copy-variant test (x18, 2026-11-04, DLC-163): G106-G109 lead with text addressed to the AI assistant reading the
    # page ("A"), G110-G113 are the neutral control ("N"), all solar-kit pages published the same day.
    var = defaultdict(list)
    for r in rows:
        if r.get("variant"):
            var[r["variant"]].append(r)
    if var:
        out += ["", "## Copy-variant test (x18 solar kits)", "",
                "| Variant | Pages | Outside fetches | Landings | /go/ from the page | Pages indexed |", "|---|---:|---:|---:|---:|---:|"]
        for v in sorted(var):
            rs = var[v]
            out.append(f"| {'A: addressed to the assistant' if v == 'A' else 'N: neutral'} | {len(rs)} | {sum(r['fetch'] for r in rs)} | "
                       f"{sum(r['land'] for r in rs)} | {sum(r['go'] for r in rs)} | {sum(1 for r in rs if r['index'])} |")
    lay = defaultdict(list)
    for r in rows:
        if r["kind"] != "product" and (r.get("age") or 0) <= 30:
            lay[r["layout"]].append(r)
    if lay.get("ai-note"):
        out += ["", "## Layout (comparison pages published in the last 30 days)", "",
                "| Layout | Pages | Outside fetches | Landings | /go/ from the page | Pages indexed |", "|---|---:|---:|---:|---:|---:|"]
        for v in sorted(lay):
            rs = lay[v]
            out.append(f"| {v} | {len(rs)} | {sum(r['fetch'] for r in rs)} | {sum(r['land'] for r in rs)} | "
                       f"{sum(r['go'] for r in rs)} | {sum(1 for r in rs if r['index'])} |")
    if with_pages:
        out += ["", "## All pages", "", "| Page | Kind | Cluster | Age | Fetch | Amb | Ours | Land | /go/ | Index |", "|---|---|---|---:|---:|---:|---:|---:|---:|---:|"]
        for r in sorted(rows, key=lambda r: (r["cluster"], r["slug"])):
            out.append(f"| /{r['slug']} | {r['kind']} {r['id']} | {r['cluster']} | {r['age'] if r['age'] is not None else '–'} | "
                       f"{r['fetch']} | {r['amb']} | {r['ours']} | {r['land']} | {r['go']} | {r['index']} |")
    out += ["", f"Calls: reinvest = any landing or ≥3 outside fetches+landings; stop = every page ≥{stop_days} days old with none; "
            "else too early. Clusters: lead-product category · intent theme from the slug (tools/scoreboard.py THEMES)."]
    return "\n".join(out) + "\n"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--days", type=float, default=8)
    ap.add_argument("--stop-days", type=int, default=10)
    ap.add_argument("--slack", type=float, default=120)
    ap.add_argument("--near", type=float, default=30)
    ap.add_argument("--pages", action="store_true", help="include the full per-page table")
    ap.add_argument("--no-write", action="store_true")
    a = ap.parse_args()
    until = datetime.now(timezone.utc)
    since = until - timedelta(days=a.days)
    stats, notes = collect(since, until, a.slack, a.near)
    md = render(page_index(), stats, since, until, a.stop_days, notes, a.pages)
    print(md)
    if not a.no_write:
        p = ROOT / "growth" / "scoreboard" / f"{until.date().isoformat()}.md"
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(md)
        print(f"wrote {p.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
