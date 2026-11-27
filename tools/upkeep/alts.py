"""Step 3 of the weekly upkeep: keep each record's alternative ("alt") right, under the rules in growth/stock/RULES.md.

- An original that ships again (now, or a pre-order within 14 days) loses its alternative line (its "alt" is removed).
- A sold-out original, or a pre-order more than 14 days out, keeps its alternative while that alternative still ships
  (now, or sooner than the original when the entry allows it) and stays within ±25% of the original's price; otherwise
  it is researched again. "none" verdicts are retried every 4 weeks.
- Research: one `claude -p` call per original (llm.DEEP, web tools), which returns the winner, the runner-up, the
  reason, the paragraph on why the winner beats the runner-up, the spec table and an independent review. The winner is
  then read live (read.py) and must ship now or sooner, and an Amazon winner must have an Add to Cart button. A winner
  we don't list gets a minimal record when it is sold on Amazon or by a store we already have a program with;
  otherwise the original is listed "pending" in the report for a hand-added record.
Proof for every decision goes to growth/stock/<date>/research/<slug>.md.
"""
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
import urllib.parse
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import apply as A
import classify as K
import llm

ROOT = Path(__file__).resolve().parents[2]
RULES = (ROOT / "growth" / "stock" / "RULES.md").read_text()
NONE_RETRY_DAYS = 28
BAND = 0.25

SCHEMA = {"type": "object", "properties": {
    "winner": {"type": ["object", "null"], "properties": {
        "slug": {"type": ["string", "null"]}, "brand": {"type": "string"}, "name": {"type": "string"}, "model": {"type": "string"},
        "url": {"type": "string"}, "asin": {"type": ["string", "null"]}, "price": {"type": ["number", "null"]},
        "stock": {"type": "string"}, "specs": {"type": "array", "items": {"type": "array", "items": {"type": "string"}}},
        "warranty": {"type": "string"}, "returns": {"type": "string"}, "summary": {"type": "string"}, "fit": {"type": "string"}}},
    "runner_up": {"type": ["object", "null"]}, "reason": {"type": "string"}, "why": {"type": "string"},
    "spec_table_md": {"type": "string"}, "reviews": {"type": "array", "items": {"type": "string"}},
    "none_reason": {"type": ["string", "null"]}, "confident": {"type": "boolean"}}, "required": ["reason", "why", "confident"]}

PROMPT = """You are choosing ONE alternative for a product on Dealectric, a shopping site, under these rules:

{rules}

Today is {today}. The original (its status was read on the store today):
{original}

Candidate pool: products we already list, with today's status and price (prefer these when they are equally good):
{pool}

Also search other stores and Amazon in the same size class (including the same product sold on Amazon). Read specs
from maker pages or manuals, price and stock today, and find at least one independent reviewer or owner source for the
winner. Never invent a figure; write "not confirmed" when you cannot confirm one.

Answer with JSON only: winner (null if nothing qualifies; for a product we list give its slug, else slug null with
brand, name, model, url, asin when on Amazon, price, stock as read, specs [[label, value], ...] from the maker,
warranty, returns, summary (one factual sentence) and fit (one sentence on who it suits); name and model are the
product's plain retail name, never a note), runner_up (same fields),
confident (true only when the winner's specs came from the maker's page or manual and its price and stock were
read today on the store or Amazon listing you name; false for a provisional pick), reason (the line shown on the
page, max 70 characters, comparing to the original, e.g. "same 1,024 Wh LiFePO4 and
1,800 W output"), why (one paragraph: why the winner beats the runner-up under the rules), spec_table_md (a short
markdown table: original vs candidates), reviews (URLs), none_reason (when winner is null)."""


def _price(p: dict, statuses: dict) -> float | None:
    s = statuses.get(p["slug"]) or {}
    return s.get("price") if s.get("price") is not None else p.get("price")


def _ships_ok(q: dict, s_orig: dict, statuses: dict) -> tuple[bool, str | None]:
    """(qualifies, alt_ships text or None) for an alternative's status against the original's."""
    sq = statuses.get(q["slug"])
    if not sq or sq["status"] in ("sold", "unknown"):
        return False, None
    if sq["status"] == "now":
        return True, None
    if not sq.get("ships_date"):
        return False, None
    if s_orig["status"] == "sold" or (s_orig.get("ships_date") and sq["ships_date"] < s_orig["ships_date"]):
        return True, sq.get("ships_text")
    return False, None


def in_band(pp: float | None, pq: float | None) -> bool:
    return bool(pp and pq) and abs(pq - pp) <= BAND * pp


def plan(products: list[dict], statuses: dict, today: str) -> list[dict]:
    """[{slug, action: keep | remove | research, why}] for every record whose alternative needs a look."""
    by = {p["slug"]: p for p in products}
    out = []
    for p in products:
        s = statuses.get(p["slug"])
        if not s or s["status"] == "unknown":
            continue
        a = p.get("alt") or {}
        if not K.far(s):
            if a:
                out.append({"slug": p["slug"], "action": "remove", "why": f"ships again ({s['status']})"})
            continue
        if a.get("slug"):
            q = by.get(a["slug"])
            ok, ships = _ships_ok(q, s, statuses) if q else (False, None)
            if not q:
                out.append({"slug": p["slug"], "action": "research", "why": "its alternative is no longer listed"})
            elif not ok:
                out.append({"slug": p["slug"], "action": "research", "why": f"its alternative {statuses.get(q['slug'], {}).get('status', 'unread')}"})
            elif not in_band(_price(p, statuses), _price(q, statuses)) and not str(q.get("program", "")).startswith("amazon"):
                out.append({"slug": p["slug"], "action": "research", "why": "its alternative left the ±25% price band"})
            else:
                out.append({"slug": p["slug"], "action": "keep", "why": "alternative still ships and fits", "alt_ships": ships})
        elif a.get("none") and (dt.date.fromisoformat(today) - dt.date.fromisoformat(a["checked"])).days < NONE_RETRY_DAYS:
            out.append({"slug": p["slug"], "action": "keep-none", "why": a["none"]})
        else:
            out.append({"slug": p["slug"], "action": "research", "why": "sold out" if s["status"] == "sold" else "long pre-order"})
    return out


def _pool(p: dict, products: list[dict], statuses: dict) -> str:
    rows = []
    for q in products:
        if q["category"] != p["category"] or q["slug"] == p["slug"]:
            continue
        s = statuses.get(q["slug"]) or {}
        rows.append(f"- {q['slug']} | {q['brand']} | {q['name']} | {q['program']} | price {_price(q, statuses)} | "
                    f"{s.get('status', 'unread')} {K.ship_line(s) if s else ''} | specs: {'; '.join(f'{k}: {v}' for k, v in q['specs'])[:400]}")
    return "\n".join(rows[:150]) or "(none in this category)"


def research(p: dict, s: dict, products: list[dict], statuses: dict, today: str) -> dict:
    original = json.dumps({"slug": p["slug"], "brand": p["brand"], "name": p["name"], "price_today": _price(p, statuses),
                           "status_today": K.ship_line(s) or s["status"], "url": p["url"], "specs": p["specs"]}, ensure_ascii=False)
    t = str(ROOT / "tools")
    return llm.ask(PROMPT.format(rules=RULES, today=today, original=original, pool=_pool(p, products, statuses)),
                   models=llm.DEEP, schema=SCHEMA, tools=["WebSearch", "WebFetch", "Bash"],
                   allowed=["WebSearch", "WebFetch", f"Bash(python3.12 {t}/storecheck.py:*)", f"Bash(python3.12 {t}/amzcheck.py:*)"])


def _program_for(url: str, products: list[dict]) -> str | None:
    host = urllib.parse.urlsplit(url).netloc.replace("www.", "")
    for q in products:
        if not str(q.get("program", "")).startswith("amazon") and urllib.parse.urlsplit(q.get("url") or "").netloc.replace("www.", "") == host:
            return q["program"]
    return None


def _new_slug(w: dict, products: list[dict]) -> str:
    label = re.sub(r"\([^)]*\)|,.*$", "", w["name"])          # the retail name, no parentheses, no spec list
    if not label.lower().startswith(w["brand"].lower()):
        label = f"{w['brand']} {label}"
    base = "-".join(re.sub(r"[^a-z0-9]+", "-", label.lower()).strip("-").split("-")[:9])[:60]
    base += "-amazon" if w.get("asin") else ""
    slugs = {q["slug"] for q in products}
    s, n = base, 2
    while s in slugs:
        s, n = f"{base}-{n}", n + 1
    return s


def minimal_record(w: dict, products: list[dict], today: str, category: str) -> dict | None:
    if w.get("asin"):
        prog, url, price = "amazon:us", f"https://www.amazon.com/dp/{w['asin']}", None
    else:
        prog, url, price = _program_for(w["url"], products), w["url"], w.get("price")
        if not prog:
            return None
    return {"slug": _new_slug(w, products), "brand": w["brand"], "program": prog, "category": category,   # the original's category
            "name": w["name"], "model": w.get("model") or w["name"], "url": url, "price": price,
            **({"asin": w["asin"]} if w.get("asin") else {}), "verified": today,
            "specs": [tuple(x[:2]) for x in w.get("specs") or [] if len(x) >= 2] or [("Specs", "see the maker's page")],
            "warranty": w.get("warranty") or "See the maker's warranty page.",
            "returns": w.get("returns") or ("Amazon's return policy applies to Amazon orders." if w.get("asin") else "See the store's return policy."),
            "summary": w.get("summary") or w["name"], "fit": w.get("fit") or "", "caveats": []}


def add_record(rec: dict) -> None:
    txt = A.PRODUCTS_PY.read_text()
    body = '{"slug": ' + repr(rec["slug"]) + "".join(f',\n "{k}": {v!r}' for k, v in rec.items() if k != "slug") + "},\n"
    i = txt.index("\n]\n", txt.index("PRODUCTS = ["))
    A.PRODUCTS_PY.write_text(txt[:i] + "\n\n" + body.rstrip(",\n") + ",\n" + txt[i + 1:])
    subprocess.run([sys.executable, str(ROOT / "tools" / "images.py"), rec["slug"]], capture_output=True, text=True, cwd=ROOT)


def set_alt(slug: str, alt: dict | None) -> None:
    txt = A.PRODUCTS_PY.read_text()
    a, b = A.record_span(txt, slug)
    block = txt[a:b]
    new = re.sub(r', "alt": \{[^{}]*\}', "", block, count=1)
    if alt is not None:
        m = re.match(r'\{"slug": [\'"][^\'"]+[\'"]', new)
        new = new[:m.end()] + f', "alt": {alt!r}' + new[m.end():]
    A.PRODUCTS_PY.write_text(txt[:a] + new + txt[b:])


def write_proof(day_dir: Path, p: dict, s: dict, res: dict, verdict: str) -> None:
    d = day_dir / "research"
    d.mkdir(parents=True, exist_ok=True)
    w = res.get("winner") or {}
    (d / f"{p['slug']}.md").write_text(
        f"# {p['name']}\n\nStatus {dt.date.today().isoformat()}: {K.ship_line(s) or s['status']}. Verdict: {verdict}\n\n"
        f"Winner: {w.get('slug') or w.get('name') or 'none'} ({w.get('url', '')})\n\nReason on the page: {res.get('reason', '')}\n\n"
        f"Why it beats the runner-up: {res.get('why', '')}\n\nRunner-up: {json.dumps(res.get('runner_up'), ensure_ascii=False)}\n\n"
        f"{res.get('spec_table_md', '')}\n\nReviews: {', '.join(res.get('reviews') or [])}\n\nNone reason: {res.get('none_reason') or '-'}\n"
        f"\nModel: {res.get('_model')}\n")


def run(products: list[dict], statuses: dict, day_dir: Path, verify_read, max_research: int = 15, workers: int = 3) -> dict:
    """Apply the plan. verify_read(record) -> status dict for one product read live now (read.py + classify.py)."""
    today = dt.date.today().isoformat()
    by = {p["slug"]: p for p in products}
    steps = plan(products, statuses, today)
    report = {"kept": [], "removed": [], "added": [], "replaced": [], "none": [], "pending": []}
    for st in steps:
        p, s = by[st["slug"]], statuses[st["slug"]]
        a = dict(p.get("alt") or {})
        if st["action"] == "remove":
            set_alt(p["slug"], None)
            report["removed"].append({"slug": p["slug"], "alt": a.get("slug"), "why": st["why"]})
        elif st["action"] == "keep":
            a.update(checked=today, status=K.ship_line(s))
            a.pop("alt_ships", None)
            if st.get("alt_ships"):
                a["alt_ships"] = st["alt_ships"]
            set_alt(p["slug"], a)
            report["kept"].append({"slug": p["slug"], "alt": a["slug"]})
        elif st["action"] == "keep-none":
            report["none"].append({"slug": p["slug"], "why": st["why"], "carried": True})
    todo = [st for st in steps if st["action"] == "research"]
    report["pending"] += [{"slug": st["slug"], "why": "over this run's research cap; next run"} for st in todo[max_research:]]
    todo = todo[:max_research]
    with ThreadPoolExecutor(max_workers=workers) as ex:
        results = list(ex.map(lambda st: (st, research(by[st["slug"]], statuses[st["slug"]], products, statuses, today)), todo))
    for st, res in results:
        p, s = by[st["slug"]], statuses[st["slug"]]
        had = (p.get("alt") or {}).get("slug")
        if res.get("status") == "error":
            report["pending"].append({"slug": p["slug"], "why": f"research failed: {res.get('reason', '')[:160]}"})
            continue
        w = res.get("winner")
        if not w:
            set_alt(p["slug"], {"none": res.get("none_reason") or "nothing qualified", "checked": today})
            write_proof(day_dir, p, s, res, "none")
            report["none"].append({"slug": p["slug"], "why": res.get("none_reason") or "nothing qualified"})
            if had:
                report["removed"].append({"slug": p["slug"], "alt": had, "why": "no qualifying replacement"})
            continue
        if not res.get("confident"):
            report["pending"].append({"slug": p["slug"], "why": f"provisional pick {w.get('name')}: not confirmed today, so not published"})
            write_proof(day_dir, p, s, res, "pending: provisional pick")
            continue
        q = by.get(w.get("slug") or "")
        if not q:   # a product we list under another slug: same Amazon ASIN or same store page
            wu = (w.get("url") or "").split("?")[0].rstrip("/")
            q = next((x for x in products if (w.get("asin") and x.get("asin") == w["asin"]) or
                      (wu and (x.get("url") or "").split("?")[0].rstrip("/") == wu)), None)
        if not q:
            rec = minimal_record(w, products, today, p["category"])
            if not rec:
                report["pending"].append({"slug": p["slug"], "why": f"winner {w.get('name')} is sold by a store we have no program with; add its record by hand"})
                write_proof(day_dir, p, s, res, "pending: needs a hand-added record")
                continue
            sq = verify_read(rec)
            if sq["status"] != "now" and not (sq["status"] == "pre" and sq.get("ships_date") and (s["status"] == "sold" or (s.get("ships_date") and sq["ships_date"] < s["ships_date"]))):
                report["pending"].append({"slug": p["slug"], "why": f"winner {w.get('name')} read {sq['status']} live, not shipping sooner"})
                write_proof(day_dir, p, s, res, f"rejected after live read ({sq['status']})")
                continue
            add_record(rec)
            if rec.get("asin") and sq.get("price") is not None:   # so the line shows Amazon's price before the daily refresh
                amz = json.loads(A.AMAZON.read_text())
                amz["asins"][rec["asin"]] = {"at": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ"), "in_stock": True, "price": sq["price"]}
                A.AMAZON.write_text(json.dumps(amz, indent=1, sort_keys=True) + "\n")
            products.append(rec)
            by[rec["slug"]] = rec
            statuses[rec["slug"]] = sq
            q = rec
        ok, ships = _ships_ok(q, s, statuses)
        if not ok:
            report["pending"].append({"slug": p["slug"], "why": f"winner {q['slug']} doesn't ship now or sooner today"})
            write_proof(day_dir, p, s, res, "rejected: winner doesn't ship")
            continue
        alt = {"slug": q["slug"], "checked": today, "status": K.ship_line(s), "reason": res["reason"][:90], "note": res.get("why", "")[:600]}
        if ships:
            alt["alt_ships"] = ships
        set_alt(p["slug"], alt)
        write_proof(day_dir, p, s, res, f"alternative {q['slug']}")
        report["replaced" if had and had != q["slug"] else "added"].append({"slug": p["slug"], "alt": q["slug"], "was": had, "why": st["why"], "reason": alt["reason"]})
    return report
