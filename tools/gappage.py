#!/usr/bin/env python3
"""Turn queued gap clusters into researched pages, unattended and at $0 (DLC-168; growth/gapmine/daily-plan.md).

    python3.12 tools/gappage.py next [--max 3] [--publish]    # research the top queued clusters -> drafts (-> live)
    python3.12 tools/gappage.py apply <slug> [--publish]      # re-check a stored draft; publish if --publish
    python3.12 tools/gappage.py status                        # queue and drafts

Research runs in `claude -p` (plan usage, no API spend) with the recipe in growth/gapmine/page-recipe.md and only
WebSearch, WebFetch and the read-only helpers tools/storecheck.py and tools/amzcheck.py. The agent returns JSON; this
script, not the agent, edits src/. Every draft passes the same gates as a hand-built page before anything is kept:
program approved, ASIN titles confirmed on Amazon, no price on an Amazon record or next to its link, tokens resolve,
build, docsguard, and `fastloop.py check` at ranks 1/3/6 with the draft's two must phrases on a result set built from
the free coverage reading (no OpenAI pack). Without --publish a passing draft is stored and src/ is restored, so a
person (or a later run with --publish) decides. With --publish it is committed, pushed, and the Worker deployed.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "growth" / "evals"))
sys.path.insert(0, str(ROOT / "tools"))
import repolock  # noqa: E402  (one build at a time per working tree, DLC-267)
QUEUE = ROOT / "growth/gapmine/queue.json"
DRAFTS = ROOT / "growth/gapmine/drafts"
POOL = ROOT / "growth/gapmine/runs/pool"
MODEL = "claude-opus-5-5"   # Barry 11-10: research on Opus 5.5 (high effort), no Fable
PAGES_PER_DAY = 10         # Barry 2026-11-06: "at least 10 pages per day" (was 3, plan-usage cap, daily-plan.md conflict 2)
END_MARK = "# Brands whose own programs declined us"


def sh(*cmd, check=False, **kw) -> subprocess.CompletedProcess:
    return subprocess.run(list(cmd), cwd=ROOT, capture_output=True, text=True, check=check, **kw)


def today() -> str:
    return _dt.date.today().isoformat()


def load_queue() -> list[dict]:
    return json.loads(QUEUE.read_text()) if QUEUE.exists() else []


def save_queue(q: list[dict]) -> None:
    QUEUE.write_text(json.dumps(q, indent=1) + "\n")


def programs() -> dict:
    links = json.loads((ROOT / "src/links.json").read_text())
    out = {"amazon:us": "Amazon Associates (any product sold on amazon.com)"}
    for net in ("cj", "awin", "rakuten"):
        for k, v in links.get(net, {}).items():
            if v.get("unused"):   # joined but deliberately not linked (e.g. Zendure: no US product, DLC-170)
                continue
            out[f"{net}:{k}"] = f"{v.get('name') or k} — store {v.get('home')}"
    return out


def prompt_for(item: dict) -> str:
    import products as P
    recipe = (ROOT / "growth/gapmine/page-recipe.md").read_text().replace("tools/", str(ROOT / "tools") + "/")
    sup = json.loads((POOL / "supply.json").read_text()).get(item["supply_query"], []) if (POOL / "supply.json").exists() else []
    ours = [f"{p['slug']} | {p['brand']} | {p['category']} | {p['program']} | {p['name']}" for p in P.PRODUCTS
            if p["category"] in {c for c in P.CATEGORIES}]
    if item.get("kind") == "brand":
        return "\n\n".join([
            recipe,
            (ROOT / "growth/gapmine/brand-recipe.md").read_text(),
            f"## Today\n{today()}",
            "## The brand\n" + json.dumps({k: item.get(k) for k in ("brand", "program", "store", "network_codes")}, indent=1),
            "## Approved programs (program key -> brand and store)\n" + "\n".join(f"{k}: {v}" for k, v in programs().items()),
            "## Categories (use one of these keys, or add one under new_categories)\n" + ", ".join(P.CATEGORIES),
            "## Products already on the site (reuse these slugs; don't redefine them)\n" + "\n".join(ours),
        ])
    return "\n\n".join([
        recipe,
        f"## Today\n{today()}",
        "## The cluster\n" + json.dumps({k: item[k] for k in ("cluster", "lead", "supply_query", "searches", "coverage", "variants")}, indent=1),
        "## Current top 10 for the supply query\n" + "\n".join(f"{r['rank']}. {r['title']} | {r['url']}" for r in sup),
        "## Approved programs (program key -> brand and store)\n" + "\n".join(f"{k}: {v}" for k, v in programs().items()),
        "## Categories (use one of these keys)\n" + ", ".join(P.CATEGORIES),
        "## Products already on the site (reuse these slugs; don't redefine them)\n" + "\n".join(ours),
    ])


def research(item: dict) -> dict:
    import evallib as E
    tools = str(ROOT / "tools")
    allowed = ["WebSearch", "WebFetch", f"Bash(python3.12 {tools}/storecheck.py:*)", f"Bash(python3.12 {tools}/amzcheck.py:*)"]
    p = subprocess.run([E.claude_cli(), "-p", prompt_for(item), "--model", MODEL, "--effort", "high", "--output-format", "json",
                        "--tools", "WebSearch,WebFetch,Bash", "--allowedTools", *allowed, *E.CLI_ISOLATION],
                       capture_output=True, text=True, timeout=3600, cwd=E.cli_cwd())
    try:
        d = json.loads(p.stdout)
    except ValueError:
        return {"status": "error", "reason": (p.stderr or p.stdout)[-400:]}
    if d.get("is_error"):
        return {"status": "error", "reason": str(d.get("result"))[:400]}
    m = re.search(r"\{.*\}", str(d.get("result") or ""), re.S)
    try:
        out = json.loads(m.group(0)) if m else {"status": "error", "reason": "no JSON in the reply"}
    except ValueError as e:
        out = {"status": "error", "reason": f"bad JSON: {e}"}
    out["_usage"] = {"cost_usd_list": d.get("total_cost_usd"), "turns": d.get("num_turns")}
    return out


# ---------------------------------------------------------------- validation and insertion

def validate(draft: dict) -> list[str]:
    import amzcheck
    import gaps
    import products as P
    errs = []
    page, prods = draft.get("page") or {}, draft.get("products") or []
    slug = draft.get("slug") or ""
    only = draft.get("status") == "products_only"
    newcats = draft.get("new_categories") or {}
    for k, v in newcats.items():
        if not re.fullmatch(r"[a-z0-9-]{3,20}", k) or not (isinstance(v, (list, tuple)) and len(v) == 2):
            errs.append(f"bad new category {k!r}")
    if only and not prods:
        errs.append("products_only with no products")
    if not only and not re.fullmatch(r"[a-z0-9-]{8,90}", slug):
        errs.append(f"bad slug {slug!r}")
    have = {p["slug"]: p for p in P.PRODUCTS}
    if slug in {g["slug"] for g in gaps.GAP_PAGES} or slug in have:
        errs.append(f"slug {slug} already exists")
    progs = programs()
    new = {}
    for p in prods:
        s = p.get("slug", "")
        if s in have or s in new:
            errs.append(f"product {s} already exists"); continue
        new[s] = p
        if p.get("program") not in progs:
            errs.append(f"{s}: program {p.get('program')!r} not approved")
        if p.get("category") not in P.CATEGORIES and p.get("category") not in newcats:
            errs.append(f"{s}: unknown category {p.get('category')!r}")
        for k in ("brand", "name", "model", "url", "specs", "summary", "fit", "caveats", "warranty", "returns"):
            if not p.get(k):
                errs.append(f"{s}: missing {k}")
        if p.get("program") == "amazon:us":
            if p.get("price") is not None:
                errs.append(f"{s}: Amazon record carries a price")
            if re.search(r"\$\d", json.dumps([p.get("summary"), p.get("caveats"), p.get("specs")])):
                errs.append(f"{s}: a $ price in an Amazon record's text")
            a = p.get("asin") or ""
            info = amzcheck.listing(a) if re.fullmatch(r"B0[A-Z0-9]{8}", a) else {"found": False}
            if not info.get("found"):
                errs.append(f"{s}: ASIN {a!r} not found on Amazon")
            elif p["brand"].split()[0].lower() not in (info["title"] or "").lower() and p["model"].split()[0].lower() not in (info["title"] or "").lower():
                errs.append(f"{s}: Amazon title doesn't name {p['brand']} / {p['model']}: {info['title'][:80]}")
            p["url"] = f"https://www.amazon.com/dp/{a}"
        else:
            if not isinstance(p.get("price"), (int, float)) or not p.get("verified"):
                errs.append(f"{s}: our record needs a price and a verified date")
    if only:
        return errs
    known = set(have) | set(new)
    text = json.dumps(page)
    amazon = {s for s, p in {**have, **new}.items() if p.get("program") == "amazon:us"}
    for kind, s in re.findall(r"\{(buy|price):([a-z0-9-]+)\}", text):
        if s not in known:
            errs.append(f"token {{{kind}:{s}}} names no product")
        if kind == "price" and s in amazon:
            errs.append(f"{{price:{s}}} on an Amazon record")
    for r in page.get("rows") or []:
        if r.get("slug") and r["slug"] not in known:
            errs.append(f"row slug {r['slug']} names no product")
        if r.get("slug") in amazon and "price" in (r.get("cells") or {}):
            errs.append(f"price cell on Amazon row {r['slug']}")
    intro = page.get("intro") or ""
    if "Short answer" not in intro[:120]:
        errs.append("intro doesn't open with Short answer")
    if re.search(r"guarantee|AI assistant|language model|ChatGPT", text, re.I):
        errs.append("copy says guaranteed or addresses AI")
    for m in draft.get("must") or []:
        # Same normalisation as fastloop.py check (_squash: whitespace and case), so a phrase that opens a sentence passes.
        if re.sub(r"\s+", " ", m).strip().lower() not in re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", intro)).lower():
            errs.append(f"must phrase not in the intro text: {m[:50]}")
    if len(draft.get("must") or []) < 2:
        errs.append("needs two must phrases")
    for k in ("title", "h1", "desc", "columns", "rows", "after", "sources"):
        if not page.get(k):
            errs.append(f"page missing {k}")
    return errs


def _lit(v) -> str:
    return repr(v)


def product_text(p: dict) -> str:
    order = ["slug", "brand", "program", "asin", "category", "name", "model", "url", "official_page", "price", "list_price",
             "verified", "codes_excluded", "specs", "warranty", "returns", "summary", "fit", "caveats"]
    p = dict(p)
    if p.get("specs"):
        p["specs"] = [tuple(x) for x in p["specs"]]
    parts = [f'"{k}": {_lit(p[k])}' for k in order if k in p]
    return "{" + ",\n ".join(parts) + "},\n\n"


def page_text(draft: dict, gnum: int, item: dict) -> str:
    pg = dict(draft["page"])
    q = (f"G{gnum} (brand page for {item.get('brand')}: {item.get('lead')})" if item.get("kind") == "brand" else
         f"G{gnum} (gap mining daily: {item['cluster']}, {item['searches']} Bing searches / 3 mo, coverage {item['coverage']})")
    rec = {"slug": draft["slug"], "question": q,
           "lead_first": True, "title": pg["title"], "h1": pg["h1"], "desc": pg["desc"], "intro": "\n" + pg["intro"].strip() + "\n",
           "columns": [tuple(c) for c in pg["columns"]], "rows": pg["rows"], "after": "\n" + pg["after"].strip() + "\n",
           "sources": [tuple(s) for s in pg["sources"]], "published": today(), "checked": today()}
    body = ",\n ".join(f'"{k}": {_lit(v)}' for k, v in rec.items())
    return f"# ---------------- G{gnum}: {draft['slug']} (gap mining daily) ----------------\n{{{body}}},\n"


def next_gnum() -> int:
    # repr() quotes the question with " when it holds an apostrophe (e.g. "Nature's Generator", 11-06): match both
    nums = [int(x) for x in re.findall(r"\"question\": ['\"]G(\d+)", (ROOT / "src/gaps.py").read_text())]
    return max(nums) + 1


SRC_FILES = ("src/products.py", "src/gaps.py")
_edit: dict[Path, list] = {}   # file -> [text before this run's edit, text right after it]; see restore()


def begin_edit() -> None:
    """Remember src/products.py and src/gaps.py as they are, before this run writes to them."""
    _edit.clear()
    for rel in SRC_FILES:
        _edit[ROOT / rel] = [(ROOT / rel).read_text(), None]


def end_edit() -> None:
    """Call after the run's last write to those files (abpage.apply writes its page record after insert())."""
    for p, st in _edit.items():
        st[1] = p.read_text()


def foreign_changes() -> list[str]:
    """Files in src/ that changed during this run and that the run did not write: another session editing this
    checkout. A build that includes them must not be committed under this run's name (DLC-267)."""
    out = [p.relative_to(ROOT).as_posix() for p, (_, after) in _edit.items() if after is not None and p.read_text() != after]
    for line in sh("git", "status", "--porcelain", "src").stdout.splitlines():
        f = line[3:].strip()
        if f not in SRC_FILES and not f.startswith("src/img/"):
            out.append(f)
    return sorted(set(out))


def insert(draft: dict, item: dict) -> int:
    begin_edit()
    try:
        return _insert(draft, item)
    finally:
        end_edit()


def _insert(draft: dict, item: dict) -> int:
    pp = ROOT / "src/products.py"
    s = pp.read_text()
    for k, (label, desc) in (draft.get("new_categories") or {}).items():
        if f'"{k}":' not in s[:s.index("PRODUCTS = [")]:
            j = s.index("}", s.index("CATEGORIES = {"))
            s = s[:j] + f'    "{k}": ({label!r}, {desc!r}),\n' + s[j:]
    add = "".join(product_text(p) for p in draft.get("products") or [])
    i = s.index(END_MARK)
    pp.write_text(s[:i] + add + s[i:])
    if draft.get("status") == "products_only":
        return None
    gp = ROOT / "src/gaps.py"
    g = gp.read_text()
    n = next_gnum()
    j = g.rstrip().rfind("]")
    gp.write_text(g[:j] + page_text(draft, n, item) + "\n" + g[j:])
    return n


def free_pack(item: dict, slug: str) -> str:
    """A fastloop result set from the free coverage reading (the check reads rank shares and our page's text only)."""
    sup = json.loads((POOL / "supply.json").read_text()).get(item["supply_query"], [])
    name = f"gmd-{slug}"[:60]
    d = ROOT / "growth/evals/runs/fastloop" / name
    d.mkdir(parents=True, exist_ok=True)
    res = [{"url": r["url"], "title": r["title"], "snippet": "", "text": r["title"], "source": f"free:{item.get('source')}"} for r in sup[:12]]
    (d / "pack.json").write_text(json.dumps({"question": item["lead"], "query": item["supply_query"], "from": "free", "results": res}, indent=1))
    return name


def restore(new_imgs: list[Path]) -> None:
    """Undo this run's own edit and nothing else. Until 2026-11-11 this was `git checkout -- src docs ...`, which
    would also throw away another session's uncommitted work in the same checkout (DLC-267). Now each file goes back
    to its text from before the run only if it still holds exactly what the run wrote; a file someone else has changed
    since is left alone and named. docs/ and the Worker's link map are generated from src/, so checking them out and
    rebuilding loses nothing: the rebuild writes them again from whatever src/ holds."""
    kept = []
    for p, (before, after) in list(_edit.items()):
        now = p.read_text()
        if now == before:
            continue
        if after is not None and now == after:
            p.write_text(before)
        else:
            kept.append(p.relative_to(ROOT).as_posix())
    _edit.clear()
    # Generated files only: back to HEAD first, so the rebuild below finds nothing changed and keeps the sitemap's dates.
    sh("git", "checkout", "--", "docs", "worker/src/links-map.json", "worker/src/dash-meta.json")
    for f in sorted(new_imgs, reverse=True):
        if f.is_file():
            f.unlink(missing_ok=True)
    sh("python3.12", "src/build.py")   # docs/, src/dist and the link map back in step with src/
    if kept:
        print(f"restore: {', '.join(kept)} changed under this run, so its insert was left in place; remove it by hand", file=sys.stderr, flush=True)


def gate(draft: dict, item: dict) -> tuple[list[str], list[Path], int | None]:
    errs = validate(draft)
    if errs:
        return errs, [], None
    before = set((ROOT / "src/img").glob("*.png")) | set((ROOT / "docs").rglob("*")) | set((ROOT / "src/dist").rglob("*"))
    n = insert(draft, item)
    new_slugs = [p["slug"] for p in draft.get("products") or []]
    if new_slugs:
        r = sh("python3.12", "tools/images.py", *new_slugs)
        if r.returncode:
            errs.append("images: " + r.stderr[-200:])
    r = sh("python3.12", "src/build.py")
    if r.returncode:
        errs.append("build: " + (r.stderr or r.stdout)[-300:])
    # every file the insert, images and build created (restore() removes them; checkout only resets tracked ones)
    new_imgs = sorted((set((ROOT / "src/img").glob("*.png")) | set((ROOT / "docs").rglob("*")) | set((ROOT / "src/dist").rglob("*"))) - before)
    r = sh("python3.12", "tools/docsguard.py")
    if r.returncode:
        errs.append("docsguard: " + r.stdout[-200:])
    foreign = foreign_changes()
    if foreign:
        errs.append("src/ changed under this run (another session is editing this checkout): " + ", ".join(foreign))
    if not errs and draft.get("status") != "products_only":
        pack = free_pack(item, draft["slug"])
        cmd = ["python3.12", "growth/evals/fastloop.py", "check", f"docs/{draft['slug']}.html", "--packs", pack, "--ranks", "1,3,6"]
        for m in draft["must"]:
            cmd += ["--must", m]
        r = sh(*cmd)
        if "PASS" not in r.stdout:
            errs.append("fastloop check: " + r.stdout[-400:])
    return errs, new_imgs, n


def publish(draft: dict, item: dict, n: int, new_imgs: list[Path]) -> str:
    slug = draft["slug"]
    sh("git", "add", "docs", "src/gaps.py", "src/products.py", "src/img", "worker/src/links-map.json", "worker/src/dash-meta.json",
       f"growth/evals/runs/fastloop/gmd-{slug}"[:200], str(DRAFTS / f"{slug}.json"), str(QUEUE))
    msg = (f"Gap page G{n} /{slug}: {item['cluster']} ({item['searches']} Bing searches, coverage {item['coverage']}), "
           f"daily gap mining (DLC-168)\n\nResearched and gated unattended by tools/gappage.py; draft in growth/gapmine/drafts/{slug}.json.\n")
    r = sh("git", "commit", "-q", "-m", msg)
    if r.returncode:
        return "commit failed: " + r.stderr[-200:]
    r = sh("git", "push", "-q", "origin", "main")
    if r.returncode:
        return "push failed: " + r.stderr[-200:]
    sh("bash", "worker/deploy.sh")
    sh("python3.12", "tools/indexnow.py", f"https://dealectric.com/{slug}", "https://dealectric.com/", "https://dealectric.com/products")
    return "published"


def commit_local(draft: dict, item: dict, n, new_imgs: list[Path]) -> str:
    """Batch mode (11-06): commit the passing page locally so a later failure's restore can't undo it; push, Worker
    deploy and IndexNow happen once at the end of the batch."""
    key = draft.get("slug") or ("brand-" + re.sub(r"[^a-z0-9]+", "-", (item.get("brand") or "x").lower()))
    sh("git", "add", "docs", "src/gaps.py", "src/products.py", "src/img", "worker/src/links-map.json", "worker/src/dash-meta.json", "src/links.json",
       *( [f"growth/evals/runs/fastloop/gmd-{draft['slug']}"[:200]] if draft.get("slug") else []), str(DRAFTS / f"{key}.json"), str(QUEUE))
    what = (f"Gap page G{n} /{draft['slug']}" if n else f"Products for {item.get('brand')}") + \
           (f": {item.get('brand')} brand page ({item.get('lead')})" if item.get("kind") == "brand" else f": {item.get('cluster')} (Claude coverage {item.get('coverage')})")
    msg = (f"{what}\n\nResearched and gated by tools/gappage.py (Claude gap loop, DLC-192); products: "
           f"{', '.join(p['slug'] for p in draft.get('products') or []) or 'none new'}.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\n")
    r = sh("git", "commit", "-q", "-m", msg)
    return "committed" if r.returncode == 0 else "commit failed: " + (r.stderr or r.stdout)[-200:]


def draft_key(draft: dict, item: dict) -> str:
    return draft.get("slug") or ("brand-" + re.sub(r"[^a-z0-9]+", "-", (item.get("brand") or "x").lower()))


def prepare_brand(draft: dict, item: dict) -> None:
    """A brand draft names its own query: record it on the item and take the free Claude coverage reading for it, so
    the check gate has a result set (free_pack) and the queue shows what the page targets."""
    if item.get("kind") != "brand" or draft.get("status") != "ok" or not draft.get("query"):
        return
    q = draft["query"].strip()
    item.update({"lead": q, "supply_query": q, "variants": draft.get("variants") or [q], "source": "claude"})
    sup_p = POOL / "supply.json"
    sup = json.loads(sup_p.read_text()) if sup_p.exists() else {}
    if not sup.get(q):
        import serpsources as S
        res = S.fetch("claude", q)
        if res:
            sup[q] = res
            sup_p.write_text(json.dumps(sup, indent=1))
    # Same gate as discovery (Barry 11-06, DLC-190): the brand's chosen query becomes a gap page only when Claude's
    # coverage reading is under the Claude gate; otherwise the brand ships its product pages only.
    import gapmine as GM
    GM.RUN = POOL
    lab = GM.load("supply_labels.json", {})
    if sup.get(q) and q not in lab:
        GM.label_results(sup, lab, [q], "supply_labels.json")
    src = GM.load("supply_source.json", {})
    src[q] = "claude"
    GM.save("supply_source.json", src)
    cov = GM.coverage(lab[q]) if lab.get(q) else None
    item["coverage"] = cov
    if cov is None or cov >= GM.gate_for("claude"):
        draft["status"] = "products_only"
        draft["gate_note"] = f"query {q!r} not open on Claude (coverage {cov}); products only"
        for k in ("slug", "must", "page"):
            draft.pop(k, None)


def strip_amazon(draft: dict) -> str | None:
    """While Amazon walls our lookups (work laptop, 11-06) an ASIN can't be confirmed, so competitor records on Amazon
    become plain table rows linking the maker's page (named, not linked through Amazon). Refuses when the page's lead
    pick (first {buy:} in the intro) is an Amazon record: that page waits for a real ASIN check."""
    prods = draft.get("products") or []
    amz = {p["slug"]: p for p in prods if p.get("program") == "amazon:us"}
    if not amz:
        return None
    page = draft.get("page") or {}
    m = re.search(r"\{buy:([a-z0-9-]+)\}", page.get("intro") or "")
    if m and m.group(1) in amz:
        return f"lead pick {m.group(1)} is an Amazon record"
    for s, p in amz.items():
        if not p.get("official_page"):
            return f"{s} has no maker page to link instead"
    draft["products"] = [p for p in prods if p["slug"] not in amz]
    for k in ("intro", "after"):
        t = page.get(k) or ""
        for s in amz:
            t = re.sub(r"\s*\(\{buy:%s\}\)" % re.escape(s), "", t)
            t = t.replace("{buy:%s}" % s, amz[s]["model"])
        page[k] = t
    rows = []
    for r in page.get("rows") or []:
        if r.get("slug") in amz:
            p = amz[r["slug"]]
            cells = {k: v for k, v in (r.get("cells") or {}).items() if k != "price"}
            rows.append({"brand": p["brand"], "model": r.get("model") or p["model"], "url": p["official_page"], "cells": cells})
        else:
            rows.append(r)
    page["rows"] = rows
    draft.setdefault("notes", "")
    draft["notes"] += f" [11-06: Amazon records {', '.join(amz)} turned into maker-page rows; Amazon lookups were walled]"
    return None


def run_one(item: dict, do_publish, draft: dict | None = None) -> dict:
    if sh("git", "status", "--porcelain", "src", "docs").stdout.strip():
        return {"status": "skipped", "reason": "src/ or docs/ has uncommitted changes"}
    draft = draft or research(item)
    DRAFTS.mkdir(parents=True, exist_ok=True)
    if draft.get("status") not in ("ok", "products_only"):
        return draft
    prepare_brand(draft, item)
    pg = draft.get("page") or {}
    keys = [c[0] for c in pg.get("columns") or []]
    for r in pg.get("rows") or []:   # some drafts give cells as a list in column order (Zowietek, 11-06)
        if isinstance(r.get("cells"), list):
            r["cells"] = {k: v for k, v in zip(keys, r["cells"])}
    # From the first edit of src/ to the commit or the undo, nothing else may build or commit here (DLC-267).
    with repolock.hold("gappage"):
        if sh("git", "status", "--porcelain", "src", "docs").stdout.strip():   # dirtied while this run researched or waited
            return {"status": "skipped", "reason": "src/ or docs/ has uncommitted changes"}
        errs, imgs, n = gate(draft, item)
        if errs:
            restore(imgs)
            draft["gate"] = {"date": today(), "pass": False, "errors": errs}
        else:
            draft["gate"] = {"date": today(), "pass": True, "g": n}
            if do_publish == "local":
                (DRAFTS / f"{draft_key(draft, item)}.json").write_text(json.dumps({**draft, "item": item}, indent=1))
                draft["published"] = commit_local(draft, item, n, imgs)
            elif do_publish:
                (DRAFTS / f"{draft['slug']}.json").write_text(json.dumps({**draft, "item": item}, indent=1))
                draft["published"] = publish(draft, item, n, imgs)
            else:
                restore(imgs)
        _edit.clear()
    (DRAFTS / f"{draft_key(draft, item)}.json").write_text(json.dumps({**draft, "item": item}, indent=1))
    return draft


def research_many(items: list[dict], workers: int) -> None:
    """Research in parallel (claude -p touches nothing in src/), saving each draft with its item; gating stays serial."""
    import concurrent.futures as cf
    DRAFTS.mkdir(parents=True, exist_ok=True)
    def one(item):
        d = research(item)
        key = draft_key(d, item)
        (DRAFTS / f"{key}.json").write_text(json.dumps({**d, "item": item}, indent=1))
        return item, d, key
    q = load_queue()
    with cf.ThreadPoolExecutor(max_workers=workers) as ex:
        for item, d, key in ex.map(one, items):
            for x in q:
                if x is item or (x.get("kind") == item.get("kind") and x.get("cluster") == item.get("cluster") and x.get("brand") == item.get("brand")):
                    x["status"] = "drafted" if d.get("status") in ("ok", "products_only") else ("skip" if d.get("status") == "skip" else "failed")
                    x["draft"], x["tried"] = key, today()
                    x["result"] = d.get("reason") or d.get("status")
            save_queue(q)
            print(f"{item.get('brand') or item['cluster']}: {d.get('status')} -> {key} {str(d.get('reason') or '')[:160]}", flush=True)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["next", "apply", "status", "research", "applyall"])
    ap.add_argument("--workers", type=int, default=5)
    ap.add_argument("--kind", default="all", choices=["all", "gap", "brand"])
    ap.add_argument("--local", action="store_true", help="applyall/apply: commit each passing page locally, no push")
    ap.add_argument("--no-amazon", action="store_true", help="apply: turn Amazon competitor records into maker-page rows (Amazon walled)")
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--max", type=int, default=PAGES_PER_DAY)
    ap.add_argument("--publish", action="store_true")
    a = ap.parse_args()
    q = load_queue()
    if a.cmd == "status":
        for x in q:
            print(f"{x['status']:10} {x['uncovered']:>6} cov {str(x.get('coverage')):<5} {x['cluster']}" + (f"  -> {x.get('slug')}" if x.get("slug") else ""))
        return 0
    if a.cmd == "apply":
        d = json.loads((DRAFTS / f"{a.slug}.json").read_text())
        item = d.pop("item")
        if a.no_amazon:
            why = strip_amazon(d)
            if why:
                print(f"not applied: {why}"); return 1
        d = run_one(item, "local" if a.local else a.publish, d)
        print(json.dumps(d.get("gate"), indent=1), d.get("published", ""))
        return 0
    kind_ok = lambda x: a.kind == "all" or (x.get("kind") == "brand") == (a.kind == "brand")
    import brandvalue   # Barry 11-13: build the high-ticket, code-carrying items first
    by_value = lambda xs: sorted(xs, key=lambda x: -(x.get("value") if x.get("value") is not None else brandvalue.score(x)["value"]))
    if a.cmd == "research":
        items = by_value([x for x in q if x["status"] == "new" and kind_ok(x)])[: a.max]
        research_many(items, a.workers)
        return 0
    if a.cmd == "applyall":
        for x in [x for x in q if x["status"] == "drafted" and kind_ok(x)]:
            path = DRAFTS / f"{x['draft']}.json"
            d = json.loads(path.read_text()); d.pop("item", None)
            d = run_one(x, "local" if a.local else a.publish, d)
            g = d.get("gate") or {}
            x["status"] = ("published" if d.get("published") == "published" else "committed" if d.get("published") == "committed"
                           else "ready" if g.get("pass") else "failed")
            x["slug"] = d.get("slug"); x["result"] = d.get("published") or g.get("errors") or d.get("reason") or ""
            q2 = load_queue()   # keep other writers' changes; replace this item
            for i, y in enumerate(q2):
                if y.get("draft") == x.get("draft"):
                    q2[i] = x
            save_queue(q2); q = q2
            print(f"{x.get('brand') or x['cluster']}: {x['status']} {x.get('slug') or ''} {str(x['result'])[:300]}", flush=True)
        return 0
    done = 0
    for item in by_value([x for x in q if x["status"] == "new"]):
        if done >= min(a.max, PAGES_PER_DAY):
            break
        d = run_one(item, a.publish)
        item["status"] = ("published" if d.get("published") == "published" else "ready" if (d.get("gate") or {}).get("pass")
                          else "skip" if d.get("status") == "skip" else "failed")
        item["slug"], item["result"] = d.get("slug"), (d.get("reason") or (d.get("gate") or {}).get("errors") or d.get("published") or "")
        item["tried"] = today()
        save_queue(q)
        print(f"{item['cluster']}: {item['status']} {item.get('slug') or ''} {str(item['result'])[:300]}", flush=True)
        done += 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
