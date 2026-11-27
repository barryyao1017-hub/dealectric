#!/usr/bin/env python3.12
"""Page ledger (page flow, DLC-369): every page with its cluster, page type and line, its publish date and its shopper
traffic. It is what "recent traffic" and "what worked against what did not" are read from, and what the retire rule
reads.

    python3.12 tools/pageflow/ledger.py build [--no-d1]   # rewrite growth/pageflow/ledger.json
    python3.12 tools/pageflow/ledger.py scores            # visits per page by cluster and page type
    python3.12 tools/pageflow/ledger.py cluster <id>      # one cluster's pages, most visited first

Sources: worker/src/dash-meta.json (every page build.py writes: kind, title, publish date), growth/stock/page-index.json
(the products each page mentions), the records' own flags in src/gaps.py (ptype, flow), and D1 dash_hv / dash_hc / sales
(shoppers only: bot_like = 0). A page type read from the slug instead of the record is marked "ptype_src": "slug".
"""
from __future__ import annotations

import collections
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import common as C  # noqa: E402

ROOT = C.ROOT
KIND_TYPE = {"product": "product", "brand codes": "codes", "seasonal": "seasonal", "site": "site", "kit": "kit"}
# a quantity a shopper chooses by: a price cap, or a number with its unit ("3d" and years are not)
NUMBER = re.compile(r"(?:^|-)(?:under-\d+|\d+(?:\.\d+)?-?(?:k?wh|kw|w|watts?|mah|ah|v|volt|hz|inch|in|channels?|ports?|bays?|tb|gb|lbs?|percent|"
                    r"keys?|amps?|a|lumens?|nits?|k|mm|ft|pack|outlets?|screens?|monitors?|computers?|mp|fps|bit|gbe|gbps|x)|[248]k)(?:-|$)")
QUESTION = re.compile(r"^(how|can|does|do|is|are|what|which|why|will|should)-")


def ptype_from_slug(slug: str) -> str:
    if "-vs-" in slug:
        return "versus"
    if NUMBER.search(slug):
        return "numbered"
    if QUESTION.match(slug):
        return "question"
    if re.search(r"-(with|without|that|compatible)-", slug):
        return "finder"
    if "-for-" in slug:
        return "bestfor"
    return "other"


def page_products() -> dict[str, set]:
    idx = C.jload(ROOT / "growth/stock/page-index.json", {"products": {}})
    out = collections.defaultdict(set)
    for slug, ents in idx["products"].items():
        for e in ents:
            out[e["page"].strip("/")].add(slug)
    return out


def added_dates() -> dict[str, str]:
    """First commit date of every docs/<page>.html, one pass over the history."""
    r = subprocess.run(["git", "log", "--diff-filter=A", "--format=@%cs", "--name-only", "--", "docs"], cwd=ROOT,
                       capture_output=True, text=True)
    out, day = {}, ""
    for line in r.stdout.splitlines():
        if line.startswith("@"):
            day = line[1:]
        elif line.startswith("docs/") and line.endswith(".html") and line.count("/") == 1:
            out[line[5:-5]] = day   # log runs newest first, so the last one written is the first add
    return out


def traffic() -> dict:
    import evallib as E
    out = {"visits": collections.defaultdict(dict), "clicks": collections.defaultdict(dict), "sales_page": collections.Counter(),
           "sales_product": collections.Counter(), "errors": []}
    rows, err = E.d1_query("SELECT page, day, COUNT(*) n FROM dash_hv WHERE bot_like=0 GROUP BY page, day")
    if err:
        out["errors"].append(f"visits: {err}")
    for r in rows:
        out["visits"][r["page"]][r["day"]] = int(r["n"])
    rows, err = E.d1_query("SELECT page, day, COUNT(*) n FROM dash_hc WHERE bot_like=0 AND page IS NOT NULL GROUP BY page, day")
    if err:
        out["errors"].append(f"clicks: {err}")
    for r in rows:
        out["clicks"][r["page"] or ""][r["day"]] = int(r["n"])
    sales, err = E.d1_query("SELECT sub_id, advertiser, sale FROM sales")
    if err:
        out["errors"].append(f"sales: {err}")
    ids = {}
    for s in sales:
        slug, _, cid = (s.get("sub_id") or "").rpartition(".")
        if slug:
            out["sales_product"][slug] += 1
            ids[cid] = slug
    if ids:
        rows, err = E.d1_query("SELECT click_id, page FROM dash_hc WHERE click_id IN (%s)" % ",".join(f"'{c}'" for c in ids if re.fullmatch(r"[\w-]+", c)))
        for r in rows:
            if r.get("page"):
                out["sales_page"][r["page"]] += 1
    return out


def _window(days: dict, start: str, n: int) -> int:
    return sum(v for d, v in days.items() if 0 <= C.days_between(start, d) < n) if start else 0


def build(use_d1: bool = True) -> dict:
    import products as P
    import gaps as G
    meta = C.jload(ROOT / "worker/src/dash-meta.json")["pages"]
    cat = {p["slug"]: p.get("category") for p in P.PRODUCTS}
    ccat = C.cluster_of_category()
    pp = page_products()
    grec = {g["slug"]: g for g in G.GAP_PAGES}
    old = (C.jload(C.LEDGER) or {}).get("pages", {})
    added = added_dates()
    t = traffic() if use_d1 else None
    today = C.today()
    pages = {}
    for m in meta:
        slug = m["page"]
        if not slug:
            continue
        kind = m["kind"]
        g = grec.get(slug, {})
        flow = g.get("flow") or {}
        if kind in KIND_TYPE:
            ptype, src = KIND_TYPE[kind], "kind"
        elif flow.get("ptype") or g.get("ptype"):
            ptype, src = flow.get("ptype") or g["ptype"], "record"
        else:
            ptype, src = ptype_from_slug(slug), "slug"
        if kind == "product":
            cl = ccat.get(cat.get(slug))
        else:
            votes = collections.Counter(ccat.get(cat.get(s)) for s in pp.get(slug, ()))
            votes.pop(None, None)
            cl = flow.get("cluster") or (votes.most_common(1)[0][0] if votes else None)
        pub = m.get("published") or added.get(slug) or old.get(slug, {}).get("published") or ""
        row = {"kind": kind, "ptype": ptype, "ptype_src": src, "cluster": cl, "line": flow.get("line"), "title": m.get("topic", ""),
               "published": pub, "age": C.days_between(pub, today) if pub else None, "products": sorted(pp.get(slug, ()))[:12]}
        if t:
            v, c = t["visits"].get(slug, {}), t["clicks"].get(slug, {})
            row.update(visits=sum(v.values()), v14=_window(v, pub, 14), v28=_window(v, pub, 28),
                       recent28=sum(n for d, n in v.items() if C.days_between(d, today) < 28), last_visit=max(v) if v else "",
                       clicks=sum(c.values()), sales=t["sales_page"].get(slug, 0) + (t["sales_product"].get(slug, 0) if kind == "product" else 0))
        else:
            row.update({k: old.get(slug, {}).get(k, 0) for k in ("visits", "v14", "v28", "recent28", "clicks", "sales")})
            row["last_visit"] = old.get(slug, {}).get("last_visit", "")
        pages[slug] = row
    led = {"built": today, "d1": bool(t) and not t["errors"], "errors": t["errors"] if t else ["built without D1"], "pages": pages}
    led["scores"] = scores(led)
    C.jsave(C.LEDGER, led)
    return led


def scores(led: dict, min_age: int = 7, k: float = 5.0) -> dict:
    """Shopper visits per page for each (cluster, page type), over pages at least `min_age` days old, and the same figure
    shrunk toward the site-wide rate of that page type (k pseudo-pages), which the proposer uses as the prior."""
    cell = collections.defaultdict(lambda: {"pages": 0, "visited": 0, "visits": 0, "clicks": 0, "sales": 0})
    site = collections.defaultdict(lambda: {"pages": 0, "visits": 0})
    for p in led["pages"].values():
        if p["age"] is None or p["age"] < min_age:
            continue
        for key in ((p["cluster"] or "-", p["ptype"]),):
            c = cell[key]
            c["pages"] += 1
            c["visited"] += p["visits"] > 0
            c["visits"] += p["visits"]
            c["clicks"] += p["clicks"]
            c["sales"] += p["sales"]
        site[p["ptype"]]["pages"] += 1
        site[p["ptype"]]["visits"] += p["visits"]
    out = {}
    for (cl, pt), c in cell.items():
        rate = site[pt]["visits"] / site[pt]["pages"] if site[pt]["pages"] else 0
        out.setdefault(cl, {})[pt] = dict(c, per_page=round(c["visits"] / c["pages"], 2),
                                          prior=round((c["visits"] + k * rate) / (c["pages"] + k), 2))
    out["_site"] = {pt: dict(s, per_page=round(s["visits"] / s["pages"], 2) if s["pages"] else 0) for pt, s in site.items()}
    return out


def prior(led: dict, cluster: str, ptype: str) -> float:
    s = led.get("scores", {})
    if ptype in s.get(cluster, {}):
        return s[cluster][ptype]["prior"]
    return s.get("_site", {}).get(ptype, {}).get("per_page", 0.5) or 0.5


def main() -> int:
    cmd = sys.argv[1] if len(sys.argv) > 1 else "scores"
    if cmd == "build":
        led = build("--no-d1" not in sys.argv)
        print(f"ledger: {len(led['pages'])} pages, D1 {'ok' if led['d1'] else led['errors']}")
        return 0
    led = C.jload(C.LEDGER)
    if not led:
        print("no ledger yet: run build")
        return 1
    if cmd == "scores":
        print(f"built {led['built']}; pages 7+ days old; visits = shoppers since 2026-10-28")
        print("cluster | page type | pages | visited | visits | per page | prior | clicks | sales")
        for cl, row in sorted(led["scores"].items()):
            if cl == "_site" or (cl == "-" and "--all" not in sys.argv):
                continue
            for pt, c in sorted(row.items(), key=lambda x: -x[1]["visits"]):
                print(f"{cl} | {pt} | {c['pages']} | {c['visited']} | {c['visits']} | {c['per_page']} | {c['prior']} | {c['clicks']} | {c['sales']}")
        print("site-wide per page:", {pt: s["per_page"] for pt, s in led["scores"]["_site"].items()})
    elif cmd == "cluster":
        rows = [(s, p) for s, p in led["pages"].items() if p["cluster"] == sys.argv[2]]
        for s, p in sorted(rows, key=lambda x: (-x[1]["visits"], x[0])):
            print(f"{p['visits']:3d} v | {p['clicks']:2d} c | {p['sales']} s | {p['ptype']:9s} | {p['published'] or '?':10s} | /{s}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
