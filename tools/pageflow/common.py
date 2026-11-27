"""Page flow (DLC-369, Barry 2026-11-27): shared paths and helpers. The workflow is written up in growth/pageflow/README.md."""
from __future__ import annotations

import datetime as dt
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
for _p in ("src", "tools", "growth/evals", "growth/focus/open-pages"):
    if str(ROOT / _p) not in sys.path:
        sys.path.insert(0, str(ROOT / _p))

DATA = ROOT / "growth/pageflow"
MAPS = DATA / "maps"
OPTIONS = DATA / "options"
RUNS = DATA / "runs"
LEDGER = DATA / "ledger.json"
QUEUE = DATA / "queue.json"
PTYPES = ("numbered", "finder", "product")   # the page types the flow builds (Barry 2026-11-27)


def today() -> str:
    return dt.date.today().isoformat()


def jload(p: Path, default=None):
    try:
        return json.loads(Path(p).read_text())
    except (OSError, ValueError):
        return default


def jsave(p: Path, obj) -> None:
    p = Path(p)
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(json.dumps(obj, indent=1, ensure_ascii=False) + "\n")


def clusters() -> dict:
    return jload(DATA / "clusters.json", {"clusters": {}})["clusters"]


def cluster_of_category() -> dict:
    return {cat: cid for cid, c in clusters().items() for cat in c["categories"]}


def records(cluster: str | None = None) -> list[dict]:
    """Live product records (not retired), for one cluster or all."""
    import products as P
    cats = set(clusters()[cluster]["categories"]) if cluster else None
    return [p for p in P.PRODUCTS if p["slug"] not in getattr(P, "RETIRED", ()) and (cats is None or p.get("category") in cats)]


def days_between(a: str, b: str) -> int:
    return (dt.date.fromisoformat(b[:10]) - dt.date.fromisoformat(a[:10])).days


def ours_table(cluster: str) -> str:
    """The products we link in a cluster, one line each, with the price the shopper pays through our link today
    (the same reading the page researchers get; from the records, their codes and their cart tests)."""
    import build as B
    lines = []
    for p in records(cluster):
        if p.get("in_stock") is False:
            continue
        if p.get("program") == "amazon:us":
            specs = "; ".join(f"{a}: {b}" for a, b in p.get("specs", [])[:5])
            lines.append((1e9, f"{p['slug']} | {p['name']} | amazon.com with our tag (ASIN {p.get('asin', '?')}; no price in the record) | {specs[:380]}"))
            continue
        if p.get("price") is None:
            continue
        price = float(p["price"])
        c, _saving, after, tested = B.best_offer(p)
        link = f"${price:,.2f} through our link (no code applies today)"
        d = B.deal(p) or {}
        if d.get("auto_total") is not None and d["auto_total"] < price:
            link = f"${d['auto_total']:,.2f} at checkout through our link ({d.get('name', 'store sale')} comes off in the cart by itself)"
        if c:
            t = B.last_test(c, p)
            on_this = bool(t and t["product"] == p["slug"])
            link = (f"${after:,.2f} with code {c['code']} applied by the link "
                    + (f"(cart test on this product {tested})" if on_this else f"(code passed {tested} on another {p['brand']} product)"))
        pre = f" | PRE-ORDER, ships {p['preorder']}" if p.get("preorder") else ""
        specs = "; ".join(f"{a}: {b}" for a, b in p.get("specs", [])[:5])
        lines.append((price, f"{p['slug']} | {p['name']} | {p['program']} | store price ${price:,.2f} (read {p.get('verified', 'see record')}) | "
                             f"link price {link}{pre} | {specs[:380]}"))
    lines.sort(key=lambda x: x[0])
    return "\n".join(x[1] for x in lines)


def cluster_programs(cluster: str) -> dict:
    """Approved programs whose brands have a record in the cluster: {program: 'Brand — store <home>'}."""
    import gappage
    progs = gappage.programs()
    return {p["program"]: progs[p["program"]] for p in records(cluster) if p.get("program") in progs and p["program"] != "amazon:us"}
