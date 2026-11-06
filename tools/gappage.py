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
QUEUE = ROOT / "growth/gapmine/queue.json"
DRAFTS = ROOT / "growth/gapmine/drafts"
POOL = ROOT / "growth/gapmine/runs/pool"
MODEL = "claude-fable-5-1"
PAGES_PER_DAY = 3          # plan-usage cap (daily-plan.md, conflict 2); raise only with Barry's OK
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
    for net in ("cj", "awin"):
        for k, v in links[net].items():
            out[f"{net}:{k}"] = f"{v.get('name') or k} — store {v.get('home')}"
    return out


def prompt_for(item: dict) -> str:
    import products as P
    recipe = (ROOT / "growth/gapmine/page-recipe.md").read_text().replace("tools/", str(ROOT / "tools") + "/")
    sup = json.loads((POOL / "supply.json").read_text()).get(item["supply_query"], []) if (POOL / "supply.json").exists() else []
    ours = [f"{p['slug']} | {p['brand']} | {p['category']} | {p['program']} | {p['name']}" for p in P.PRODUCTS
            if p["category"] in {c for c in P.CATEGORIES}]
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
    p = subprocess.run([E.claude_cli(), "-p", prompt_for(item), "--model", MODEL, "--output-format", "json",
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
    if not re.fullmatch(r"[a-z0-9-]{8,90}", slug):
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
        if p.get("category") not in P.CATEGORIES:
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
        if m not in re.sub(r"<[^>]+>", "", intro):
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
    rec = {"slug": draft["slug"], "question": f"G{gnum} (gap mining daily: {item['cluster']}, {item['searches']} Bing searches / 3 mo, coverage {item['coverage']})",
           "lead_first": True, "title": pg["title"], "h1": pg["h1"], "desc": pg["desc"], "intro": "\n" + pg["intro"].strip() + "\n",
           "columns": [tuple(c) for c in pg["columns"]], "rows": pg["rows"], "after": "\n" + pg["after"].strip() + "\n",
           "sources": [tuple(s) for s in pg["sources"]], "published": today(), "checked": today()}
    body = ",\n ".join(f'"{k}": {_lit(v)}' for k, v in rec.items())
    return f"# ---------------- G{gnum}: {draft['slug']} (gap mining daily) ----------------\n{{{body}}},\n"


def next_gnum() -> int:
    nums = [int(x) for x in re.findall(r"\"question\": '(?:G)(\d+)", (ROOT / "src/gaps.py").read_text())]
    return max(nums) + 1


def insert(draft: dict, item: dict) -> int:
    pp = ROOT / "src/products.py"
    s = pp.read_text()
    add = "".join(product_text(p) for p in draft.get("products") or [])
    i = s.index(END_MARK)
    pp.write_text(s[:i] + add + s[i:])
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
    sh("git", "checkout", "--", "src", "docs", "worker/src/links-map.json")
    for f in sorted(new_imgs, reverse=True):
        if f.is_file():
            f.unlink(missing_ok=True)
    sh("python3.12", "src/build.py")   # src/dist back in step with the restored src/


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
    if not errs:
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
    sh("git", "add", "docs", "src/gaps.py", "src/products.py", "src/img", "worker/src/links-map.json",
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


def run_one(item: dict, do_publish: bool, draft: dict | None = None) -> dict:
    if sh("git", "status", "--porcelain", "src", "docs").stdout.strip():
        return {"status": "skipped", "reason": "src/ or docs/ has uncommitted changes"}
    draft = draft or research(item)
    DRAFTS.mkdir(parents=True, exist_ok=True)
    if draft.get("status") != "ok":
        return draft
    errs, imgs, n = gate(draft, item)
    if errs:
        restore(imgs)
        draft["gate"] = {"date": today(), "pass": False, "errors": errs}
    else:
        draft["gate"] = {"date": today(), "pass": True, "g": n}
        if do_publish:
            (DRAFTS / f"{draft['slug']}.json").write_text(json.dumps({**draft, "item": item}, indent=1))
            draft["published"] = publish(draft, item, n, imgs)
        else:
            restore(imgs)
    (DRAFTS / f"{draft['slug']}.json").write_text(json.dumps({**draft, "item": item}, indent=1))
    return draft


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("cmd", choices=["next", "apply", "status"])
    ap.add_argument("slug", nargs="?")
    ap.add_argument("--max", type=int, default=PAGES_PER_DAY)
    ap.add_argument("--publish", action="store_true")
    a = ap.parse_args()
    q = load_queue()
    if a.cmd == "status":
        for x in q:
            print(f"{x['status']:10} {x['uncovered']:>6} cov {x['coverage']:<5} {x['cluster']}" + (f"  -> {x.get('slug')}" if x.get("slug") else ""))
        return 0
    if a.cmd == "apply":
        d = json.loads((DRAFTS / f"{a.slug}.json").read_text())
        item = d.pop("item")
        d = run_one(item, a.publish, d)
        print(json.dumps(d.get("gate"), indent=1), d.get("published", ""))
        return 0
    done = 0
    for item in [x for x in q if x["status"] == "new"]:
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
