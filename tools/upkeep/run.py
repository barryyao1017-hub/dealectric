#!/usr/bin/env python3.12
"""Weekly catalog upkeep for every brand (growth/stock/README.md): read every listed product, update records and every
page that mentions a changed product, keep each sold-out or long-pre-order product's alternative right, rebuild,
commit, deploy and check the links, and write the week's report for the daily update.

Run by tools/codesweep.sh once a week (Sundays), after the daily code tests, in the sweep's clone. By hand:
    python3.12 tools/upkeep/run.py [--brands BLUETTI,OSCAL] [--slugs a,b] [--no-push] [--max-research 15] [--tabs 3]
--no-push: everything up to and including the local commit; nothing is pushed or deployed (a test run).
"""
from __future__ import annotations

import datetime as dt
import json
import os
import subprocess
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "tools"))

import llm  # noqa: E402
import read as R  # noqa: E402
import classify as K  # noqa: E402
import apply as A  # noqa: E402
import alts as L  # noqa: E402
import pages as G  # noqa: E402


def log(m: str) -> None:
    print(f"{time.strftime('%H:%M:%S')} {m}", flush=True)


def sh(cmd, timeout=1800, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, cwd=ROOT, **kw)


def fresh_products():
    import importlib
    import products
    importlib.reload(products)
    return [p for p in products.PRODUCTS if p["slug"] not in products.RETIRED]


def verify_read(rec: dict) -> dict:
    """Read one product live now and classify it (used for an alternative we don't list yet)."""
    import codesweep as C
    t = C.Tab("about:blank")
    t.call("Page.enable")
    try:
        k = R.kind(rec)
        row = {"slug": rec["slug"], "brand": rec["brand"], "kind": k, "url": rec.get("url"), "read_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}
        row.update(R.read_amazon(t, rec) if k == "amazon" else R.read_shopify(t, rec) if k == "shopify" else R.read_other(t, rec))
    except Exception as e:
        return {"status": "unknown", "evidence": f"{type(e).__name__}: {e}"}
    finally:
        t.close()
    return K.classify([row], {rec["slug"]: rec}).get(rec["slug"], {"status": "unknown"})


def d1(sql: str) -> list[dict]:
    tok = subprocess.run(["security", "find-generic-password", "-s", "cloudflare-workers-token", "-w"], capture_output=True, text=True).stdout.strip()
    p = subprocess.run(["npx", "--yes", "wrangler", "d1", "execute", "dealectric", "--remote", "--json", "--command", sql],
                       capture_output=True, text=True, timeout=300, cwd=ROOT / "worker", env={**os.environ, "CLOUDFLARE_API_TOKEN": tok})
    try:
        out = json.loads(p.stdout[p.stdout.find("["):])
        return out[0]["results"]
    except Exception:
        return []


def soldout_clicks(sold: list[str]) -> list[dict]:
    if not sold:
        return []
    ins = ",".join("'" + s.replace("'", "") + "'" for s in sold)
    return d1("SELECT slug, COUNT(*) AS clicks, SUM(utm_source='chatgpt.com') AS chatgpt FROM clicks "
              f"WHERE ts >= datetime('now','-7 days') AND kind='redirect' AND bot_like=0 AND method='GET' AND slug IN ({ins}) "
              "GROUP BY slug ORDER BY clicks DESC")


def check_links(slugs: list[str]) -> list[str]:
    bad = []
    for s in sorted(set(slugs)):
        p = subprocess.run(["curl", "-s", "-o", "/dev/null", "-A", "dealectric-linkcheck-bot", "-w", "%{http_code}", f"https://dealectric.com/go/{s}"],
                           capture_output=True, text=True)
        if p.stdout != "302":
            bad.append(f"{s} {p.stdout}")
    return bad


def name(by, s):
    return (by.get(s) or {}).get("name", s)


def write_report(day_dir: Path, today: str, by: dict, changes: list, alt: dict, pg: dict, index: dict, clicks: list, extra: dict) -> None:
    rep = {"date": today, "changes": changes, "alternatives": alt, "pages": pg, "unlisted": index.get("unlisted", []),
           "soldout_clicks": clicks, **extra, "usage": llm.usage_line()}
    (day_dir / "report.json").write_text(json.dumps(rep, indent=1, ensure_ascii=False) + "\n")
    L_ = [f"# Weekly catalog upkeep, {today}", "", f"Read {extra.get('read', 0)} products; {len(changes)} record changes; "
          f"{len(alt['added'])} alternatives added, {len(alt['replaced'])} replaced, {len(alt['removed'])} removed, "
          f"{len(alt['none'])} with none, {len(alt['pending'])} pending; {len(pg['pages'])} pages edited, {len(pg['failed'])} failed. "
          f"Model use: {llm.usage_line()}.", ""]
    L_ += ["## Flags changed", ""] + [f"- [{name(by, c['slug'])}](https://dealectric.com/{c['slug']}): {c['field']} {c['old']} → {c['new']}" for c in changes] + [""]
    L_ += ["## Alternatives", ""]
    for k, verb in (("added", "added"), ("replaced", "replaced"), ("removed", "removed")):
        for a in alt[k]:
            L_.append(f"- {verb}: [{name(by, a['slug'])}](https://dealectric.com/{a['slug']}) → {name(by, a.get('alt') or '') if a.get('alt') else '-'}"
                      f"{' (was ' + name(by, a['was']) + ')' if a.get('was') else ''}: {a.get('reason') or a.get('why')}")
    L_ += ["", "## No qualifying substitute", ""] + [f"- [{name(by, a['slug'])}](https://dealectric.com/{a['slug']}): {a['why']}" for a in alt["none"]]
    L_ += ["", "## Pending (needs the next run or a hand step)", ""] + [f"- {name(by, a['slug'])}: {a['why']}" for a in alt["pending"]]
    L_ += ["", "## Pages edited", ""] + [f"- [{x['page']}](https://dealectric.com{x['page']}) ({x['source']}): {x['edits']} edits{'; skipped ' + str(len(x['skipped'])) if x['skipped'] else ''}" for x in pg["pages"]]
    L_ += [f"- FAILED [{x['page']}](https://dealectric.com{x['page']}): {x['why']}" for x in pg["failed"]]
    L_ += ["", "## Mentioned on a page but not in the product list", ""] + sorted({f"- {u['brand']} {u['model']} on [{u['page']}](https://dealectric.com{u['page']})" for u in index.get("unlisted", [])})
    L_ += ["", "## Clicks on sold-out products, last 7 days (the cost of keeping the original link)", ""] + \
          [f"- [{name(by, c['slug'])}](https://dealectric.com/{c['slug']}): {c['clicks']} clicks ({c.get('chatgpt') or 0} from ChatGPT)" for c in clicks]
    if extra.get("link_failures"):
        L_ += ["", "## Link check failures", ""] + [f"- {x}" for x in extra["link_failures"]]
    (day_dir / "CHANGES.md").write_text("\n".join(L_) + "\n")


def main(argv: list[str]) -> int:
    opt = lambda k: argv[argv.index(k) + 1] if k in argv else None
    push = "--no-push" not in argv
    today = dt.date.today().isoformat()
    day_dir = ROOT / "growth" / "stock" / today
    day_dir.mkdir(parents=True, exist_ok=True)
    import evallib as E
    if not E.claude_cli_login():
        log("claude CLI is not logged in: reads and record updates run, research and page edits are skipped")
    products = fresh_products()
    sel = R.select(products, set(opt("--slugs").split(",")) if opt("--slugs") else None, set(opt("--brands").split(",")) if opt("--brands") else None)
    log(f"reading {len(sel)} products")
    R.read_all(sel, day_dir / "reads.jsonl", int(opt("--tabs") or 3))
    reads = {json.loads(l)["slug"]: json.loads(l) for l in (day_dir / "reads.jsonl").open() if l.strip()}
    by = {p["slug"]: p for p in products}
    log("classifying")
    statuses = K.classify([reads[p["slug"]] for p in sel if p["slug"] in reads], by)
    (day_dir / "status.json").write_text(json.dumps(statuses, indent=1, ensure_ascii=False) + "\n")
    # the alternatives already chosen are products too: their status comes from the same read when they are in the
    # selection, else from a live read now
    for p in sel:
        a = (p.get("alt") or {}).get("slug")
        if a and a in by and a not in statuses:
            statuses[a] = verify_read(by[a])
    changes = A.apply(sel, statuses, reads, today)
    log(f"{len(changes)} record changes")
    products = fresh_products()
    sel_slugs = {p["slug"] for p in sel}
    alt = L.run([p for p in products if p["slug"] in sel_slugs or p["slug"] in statuses], statuses, day_dir, verify_read,
                int(opt("--max-research") or 15))
    log(f"alternatives: {', '.join(f'{k} {len(v)}' for k, v in alt.items())}")
    changed: dict[str, list[str]] = {}
    for c in changes:
        changed.setdefault(c["slug"], []).append(f"{c['field']}: {c['old']} → {c['new']}")
    products = fresh_products()
    by = {p["slug"]: p for p in products}
    for k in ("added", "replaced"):
        for a in alt[k]:
            changed.setdefault(a["slug"], []).append(f"alternative line now shown under it: {name(by, a['alt'])} ({a['reason']})")
    for a in alt["removed"]:
        changed.setdefault(a["slug"], []).append(f"alternative line removed ({a['why']})")
    index = json.loads((ROOT / "growth" / "stock" / "page-index.json").read_text())
    pg = G.run(changed, index) if E.claude_cli_login() else {"pages": [], "failed": [{"page": "-", "source": "-", "why": "claude CLI not logged in"}]}
    log(f"pages: {len(pg['pages'])} edited, {len(pg['failed'])} failed")
    b = sh(["python3.12", "tools/repolock.py", "run", "upkeep", "--", "python3.12", "src/build.py"], timeout=3600)
    if b.returncode != 0:
        log("build failed:\n" + (b.stdout + b.stderr)[-2000:])
        return 1
    g = sh(["python3.12", "tools/docsguard.py"])
    if g.returncode != 0:
        log("docs guard refused: " + g.stdout[-500:])
        return 1
    index = json.loads((ROOT / "growth" / "stock" / "page-index.json").read_text())
    sold = [s for s, v in statuses.items() if v["status"] == "sold"]
    clicks = soldout_clicks(sold)
    extra = {"read": len(reads)}
    write_report(day_dir, today, by, changes, alt, pg, index, clicks, extra)
    sh(["git", "add", "src", "docs", "worker/src", "growth/stock"])
    msg = (f"upkeep: weekly catalog read {today}: {len(changes)} record changes, alternatives +{len(alt['added'])} "
           f"~{len(alt['replaced'])} -{len(alt['removed'])}, {len(pg['pages'])} pages edited\n\nDetails: growth/stock/{today}/CHANGES.md\n\n"
           "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
    c = sh(["git", "commit", "-q", "-m", msg])
    log("commit: " + (c.stdout + c.stderr).strip()[-300:])
    if not push:
        log("--no-push: stopping before push and deploy")
        return 0
    p = sh(["git", "push", "-q", "origin", "HEAD:main"])
    if p.returncode != 0:
        log("push failed: " + p.stderr[-500:])
        return 1
    if sh(["git", "diff", "--quiet", "HEAD~1", "HEAD", "--", "worker/src/links-map.json"]).returncode != 0:
        d = sh(["bash", "worker/deploy.sh"], timeout=600)
        log("worker deploy: " + (d.stdout + d.stderr).strip()[-200:])
    time.sleep(60)
    link_slugs = list(changed) + [a["alt"] for k in ("added", "replaced") for a in alt[k]]
    bad = check_links([s for s in link_slugs if s in by and not str(by[s].get("program", "")).startswith("amazon")])
    if bad:
        extra["link_failures"] = bad
        write_report(day_dir, today, by, changes, alt, pg, index, clicks, extra)
        sh(["git", "add", "growth/stock"])
        sh(["git", "commit", "-q", "-m", f"upkeep: link check failures {today}\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>"])
        sh(["git", "push", "-q", "origin", "HEAD:main"])
    pages = sorted({x["page"] for x in pg["pages"]} | {f"/{s}" for s in changed})
    if pages:
        sh(["python3.12", "tools/indexnow.py", *[f"https://dealectric.com{x}" for x in pages][:1000]])
    log(f"done; link failures: {len(bad)}; {llm.usage_line()}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
